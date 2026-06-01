#!/usr/bin/env python3
"""Fetch and check READMEs for ecosystem cross-references."""
import subprocess
import json
import os
import sys
import time

ORGS = ["SuperInstance", "superinstance"]
ORG = "SuperInstance"

def get_repos():
    with open("top50.txt") as f:
        return [line.strip() for line in f if line.strip()]

def fetch_readme(repo):
    """Fetch README content via gh api."""
    for branch in ["main", "master"]:
        try:
            result = subprocess.run(
                ["gh", "api", f"/repos/{ORG}/{repo}/readme", "--jq", ".content"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                import base64
                return base64.b64decode(result.stdout.strip()).decode("utf-8", errors="replace")
        except:
            pass
    return None

def fetch_file(repo, path):
    """Fetch a file from repo."""
    try:
        result = subprocess.run(
            ["gh", "api", f"/repos/{ORG}/{repo}/contents/{path}", "--jq", ".content"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            import base64
            return base64.b64decode(result.stdout.strip()).decode("utf-8", errors="replace")
    except:
        pass
    return None

def check_readme(repo, content):
    """Check what sections are missing."""
    if content is None:
        return {"error": "no readme", "missing": ["all"]}
    
    content_lower = content.lower()
    missing = []
    
    # Check for docs link
    has_docs = "openconstruct-docs" in content or "documentation" in content_lower
    if not has_docs:
        missing.append("documentation_link")
    
    # Check for ecosystem/org link
    has_ecosystem = "superinstance" in content_lower and ("github.com/superinstance" in content_lower or "ecosystem" in content_lower)
    if not has_ecosystem:
        missing.append("ecosystem_link")
    
    # Check for related repos / how it fits
    has_related = "related" in content_lower or "how it fits" in content_lower or "ecosystem" in content_lower
    if not has_related:
        missing.append("how_it_fits")
    
    # Check for install instructions (packages)
    is_package = any(x in repo.lower() for x in ["-py", "-sdk", "-rs", "-js", "-ada"])
    has_install = False
    if is_package:
        has_install = any(x in content_lower for x in ["pip install", "npm install", "cargo add", "install"])
        if not has_install:
            missing.append("install_instructions")
        has_badge = "shields.io" in content_lower or "badge" in content_lower
        if not has_badge:
            missing.append("badges")
    
    # Check for DEPENDENCIES.md
    has_deps = False  # checked separately
    
    return {"missing": missing, "has_docs": has_docs, "has_ecosystem": has_ecosystem, "has_related": has_related}

repos = get_repos()
results = {}

for i, repo in enumerate(repos):
    print(f"[{i+1}/{len(repos)}] Checking {repo}...", flush=True)
    content = fetch_readme(repo)
    check = check_readme(repo, content)
    
    # Also check for DEPENDENCIES.md
    deps = fetch_file(repo, "DEPENDENCIES.md")
    check["has_dependencies_md"] = deps is not None
    
    results[repo] = check
    print(f"  → missing: {check['missing']}, has_deps_md: {check['has_dependencies_md']}", flush=True)
    time.sleep(0.5)  # rate limit

# Summary
print("\n=== SUMMARY ===")
need_update = {r: v for r, v in results.items() if v.get("missing")}
print(f"Total repos: {len(repos)}")
print(f"Need updates: {len(need_update)}")
print(f"Have DEPENDENCIES.md: {sum(1 for v in results.values() if v.get('has_dependencies_md'))}")

with open("check_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nResults saved to check_results.json")
