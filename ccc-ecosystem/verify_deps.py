#!/usr/bin/env python3
"""Verify DEPENDENCIES.md files and check bidirectional links."""
import subprocess
import json
import os
import tempfile
import shutil
import base64
import time

ORG = "SuperInstance"
COMMIT_MSG = "docs: ecosystem cross-references — CCC autonomous"

def run(cmd, **kwargs):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60, **kwargs)

def fetch_file(repo, path):
    """Fetch a file from repo via API."""
    try:
        r = subprocess.run(
            ["gh", "api", f"/repos/{ORG}/{repo}/contents/{path}", "--jq", ".content"],
            capture_output=True, text=True, timeout=30
        )
        if r.returncode == 0:
            return base64.b64decode(r.stdout.strip()).decode("utf-8", errors="replace")
    except:
        pass
    return None

# Repos with DEPENDENCIES.md from initial scan
deps_repos = ["cocapn-core", "OpenConstruct", "openconstruct-rust", "openconstruct-abi", "plato-vision", "plato-tick"]

# Also scan more repos for DEPENDENCIES.md
additional_repos = [
    "cocapn", "cocapn-cli", "cocapn-sdk", "cocapn-py", "cocapn-health-rs",
    "cocapn-explain", "cocapn-explain-rs", "cocapn-benchmark", "captain",
    "fleet-health-monitor", "fleet-cicd-agent", "forgemaster", "ccc-os",
    "plato-construct", "plato-manus", "plato-sonar-text", "plato-training",
    "plato-adapters", "constraint-dsl", "constraint-toolkit",
    "conservation-spectral-python", "conservation-protocol",
    "api-gateway-1", "co-captain-git-agent", "agent-forge",
    "casting-call-mcp", "cartridge-mcp"
]

all_repos = deps_repos + additional_repos
deps_data = {}

print("=== Scanning for DEPENDENCIES.md ===")
for repo in all_repos:
    content = fetch_file(repo, "DEPENDENCIES.md")
    if content:
        deps_data[repo] = content
        print(f"  ✓ {repo} has DEPENDENCIES.md")
    time.sleep(0.3)

print(f"\nFound {len(deps_data)} repos with DEPENDENCIES.md")

# Parse dependencies and check bidirectional links
print("\n=== Checking bidirectional links ===")

def parse_deps(content):
    """Extract repo links from DEPENDENCIES.md."""
    import re
    links = re.findall(r'https://github\.com/SuperInstance/([a-zA-Z0-9_.-]+)', content)
    return set(links)

dep_graph = {}
for repo, content in deps_data.items():
    deps = parse_deps(content)
    dep_graph[repo] = deps
    print(f"  {repo} → depends on: {deps or '(none)'}")

# Check bidirectional links
print("\n=== Missing bidirectional links ===")
updates_needed = {}

for repo, deps in dep_graph.items():
    for dep in deps:
        if dep not in dep_graph:
            # Dependency doesn't have DEPENDENCIES.md yet
            print(f"  {dep} (no DEPENDENCIES.md) ← should list {repo} as dependent")
            if dep not in updates_needed:
                updates_needed[dep] = set()
            updates_needed[dep].add(repo)
        elif repo not in dep_graph.get(dep, set()):
            print(f"  {dep} should list {repo} as dependent (reverse link missing)")
            if dep not in updates_needed:
                updates_needed[dep] = set()
            updates_needed[dep].add(repo)

# Verify links exist
print("\n=== Verifying linked repos exist ===")
all_linked = set()
for deps in dep_graph.values():
    all_linked.update(deps)

for linked_repo in sorted(all_linked):
    r = run(f"gh api /repos/{ORG}/{linked_repo} --jq '.name' 2>&1")
    if r.returncode != 0:
        print(f"  ✗ {linked_repo} — does not exist!")
    time.sleep(0.2)

# Update repos that need bidirectional fixes
print(f"\n=== Updating {len(updates_needed)} repos with missing reverse links ===")

tmpdir = tempfile.mkdtemp(prefix="ccc-deps-")
updated_deps = []

for repo, missing_dependents in updates_needed.items():
    repo_dir = os.path.join(tmpdir, repo)
    
    r = run(f"gh repo clone {ORG}/{repo} {repo_dir} -- --depth=1 2>&1")
    if r.returncode != 0:
        print(f"  ✗ Can't clone {repo}")
        continue
    
    deps_path = os.path.join(repo_dir, "DEPENDENCIES.md")
    
    if os.path.exists(deps_path):
        with open(deps_path) as f:
            content = f.read()
    else:
        content = f"# Dependencies\n\n## Upstream\n\nNone.\n\n## Downstream\n\n"
    
    # Add missing dependents
    additions = []
    for dep in sorted(missing_dependents):
        if dep not in content:
            additions.append(f"- [{dep}](https://github.com/SuperInstance/{dep})")
    
    if not additions:
        continue
    
    # Find or create Downstream section
    if "## Downstream" in content:
        # Add after Downstream header
        block = "\n".join(additions) + "\n"
        content = content.replace("## Downstream\n", f"## Downstream\n{block}")
    else:
        content += f"\n## Downstream\n\n" + "\n".join(additions) + "\n"
    
    with open(deps_path, "w") as f:
        f.write(content)
    
    r = run(f'cd {repo_dir} && git add -A && git diff --cached --quiet')
    if r.returncode == 0:
        continue
    
    r = run(f'cd {repo_dir} && git commit -m "{COMMIT_MSG}" && git push 2>&1')
    if r.returncode != 0:
        print(f"  ✗ Push failed for {repo}: {r.stderr[:200]}")
        continue
    
    print(f"  ✓ Updated {repo} with dependents: {missing_dependents}")
    updated_deps.append(repo)
    time.sleep(1)

shutil.rmtree(tmpdir, ignore_errors=True)

print(f"\n=== DEPENDENCIES.md Summary ===")
print(f"Repos with DEPENDENCIES.md: {len(deps_data)}")
print(f"Repos updated with reverse links: {len(updated_deps)}")
print(f"Updated: {updated_deps}")
