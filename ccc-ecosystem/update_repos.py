#!/usr/bin/env python3
"""Update repos with missing ecosystem cross-references."""
import subprocess
import json
import os
import time
import tempfile
import shutil
import base64

ORG = "SuperInstance"
COMMIT_MSG = "docs: ecosystem cross-references — CCC autonomous"

def run(cmd, **kwargs):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60, **kwargs)

# Load check results
with open("check_results.json") as f:
    results = json.load(f)

# Define related repos for ecosystem sections
ECOSYSTEM_MAP = {
    "cocapn-sdk": {"category": "npm", "related": ["cocapn-core", "cocapn-py", "cocapn-cli", "cocapn"]},
    "cocapn-py": {"category": "pypi", "related": ["cocapn-core", "cocapn-sdk", "cocapn-cli", "cocapn"]},
    "cocapn-health-rs": {"category": "crates", "related": ["cocapn-core", "fleet-health-monitor", "cocapn"]},
    "cocapn-com": {"category": "web", "related": ["cocapn-landing", "cocapn-core", "cocapn"]},
    "cocapn-landing": {"category": "web", "related": ["cocapn-com", "cocapn-core", "cocapn"]},
    "cocapn-lessons": {"category": "docs", "related": ["cocapn-core", "plato-training", "cocapn"]},
    "constraint-theory-web": {"category": "wasm", "related": ["constraint-theory-rust-python", "constraint-dsl", "constraint-toolkit"]},
    "constraint-theory-rust-python": {"category": "crates", "related": ["constraint-theory-web", "constraint-dsl", "constraint-toolkit", "conservation-spectral-python"]},
    "constraint-theory-engine-cpp-lua": {"category": "native", "related": ["constraint-theory-rust-python", "constraint-dsl", "constraint-instrument"]},
    "constraint-dsl": {"category": "lang", "related": ["constraint-toolkit", "constraint-synth", "constraint-mux", "constraint-dialect"]},
    "constraint-mux": {"category": "lib", "related": ["constraint-dsl", "constraint-synth", "constraint-instrument"]},
    "constraint-synth": {"category": "lib", "related": ["constraint-dsl", "constraint-mux", "constraint-audio", "constraint-instrument"]},
    "constraint-toolkit": {"category": "lib", "related": ["constraint-dsl", "constraint-theory-rust-python", "constraint-dialect"]},
    "constraint-dialect": {"category": "lib", "related": ["constraint-dsl", "constraint-toolkit", "constraint-instrument"]},
    "constraint-instrument": {"category": "lib", "related": ["constraint-dsl", "constraint-synth", "constraint-audio"]},
    "constraint-audio": {"category": "lib", "related": ["constraint-synth", "constraint-instrument", "constraint-substrate"]},
    "constraint-substrate": {"category": "lib", "related": ["constraint-audio", "constraint-instrument", "conservation-protocol"]},
    "conservation-spectral-js": {"category": "npm", "related": ["conservation-spectral-python", "conservation-protocol", "constraint-toolkit"]},
    "conservation-spectral-python": {"category": "pypi", "related": ["conservation-spectral-js", "conservation-protocol", "constraint-theory-rust-python"]},
    "conservation-spectral-ada": {"category": "other", "related": ["conservation-spectral-python", "conservation-protocol", "constraint-toolkit"]},
    "conservation-protocol": {"category": "spec", "related": ["conservation-spectral-python", "conservation-spectral-js", "conservation-conformance"]},
    "conservation-conformance": {"category": "lib", "related": ["conservation-protocol", "constraint-dsl", "constraint-toolkit"]},
    "plato-manus": {"category": "lib", "related": ["plato-construct", "plato-sonar-text", "plato-training"]},
    "plato-sonar-text": {"category": "lib", "related": ["plato-construct", "plato-manus", "plato-vision"]},
    "plato-adapters": {"category": "lib", "related": ["plato-construct", "plato-vision", "plato-tick"]},
    "forgemaster": {"category": "tool", "related": ["OpenConstruct", "openconstruct-rust", "cocapn-core"]},
    "ccc-os": {"category": "ops", "related": ["fleet-health-monitor", "cocapn-health-rs", "captain"]},
    "casting-call-mcp": {"category": "mcp", "related": ["cartridge-mcp", "cocapn-core", "plato-adapters"]},
    "cartridge-mcp": {"category": "mcp", "related": ["casting-call-mcp", "cocapn-core", "cartridge-agent"]},
    "api-gateway-1": {"category": "infra", "related": ["cocapn-core", "captain", "cocapn-health-rs"]},
    "co-captain-git-agent": {"category": "agent", "related": ["captain", "cocapn-core", "agent-forge"]},
    "superinstance-wiki": {"category": "docs", "related": ["OpenConstruct", "cocapn-core", "plato-construct"]},
    "openconstruct-landing": {"category": "web", "related": ["OpenConstruct", "openconstruct-rust", "openconstruct-abi"]},
}

def make_badge_line(repo, missing):
    """Generate badge line based on repo type."""
    badges = []
    if "badges" not in missing:
        return ""
    
    info = ECOSYSTEM_MAP.get(repo, {})
    cat = info.get("category", "")
    
    if cat == "npm" or "-sdk" in repo:
        badges.append("[![npm version](https://img.shields.io/npm/v/cocapn)](https://www.npmjs.com/package/cocapn)")
    if cat == "pypi" or "-py" in repo:
        badges.append("[![PyPI version](https://img.shields.io/pypi/v/cocapn)](https://pypi.org/project/cocapn/)")
    if cat == "crates" or "-rs" in repo:
        badges.append("[![crates.io](https://img.shields.io/crates/v/placeholder)](https://crates.io/crates/placeholder)")
    
    # Always add ecosystem badge
    badges.append("[![SuperInstance](https://img.shields.io/badge/SuperInstance-Ecosystem-blue)](https://github.com/SuperInstance)")
    
    return " ".join(badges) + "\n\n"

def make_ecosystem_section(repo):
    """Generate ecosystem section."""
    info = ECOSYSTEM_MAP.get(repo, {})
    related = info.get("related", [])
    
    if not related:
        related = ["cocapn-core", "OpenConstruct", "plato-construct"][:3]
    
    links = []
    for r in related:
        links.append(f"- [{r}](https://github.com/SuperInstance/{r})")
    
    links_str = '\n'.join(links)
    return f"""
## Ecosystem

Part of the [SuperInstance](https://github.com/SuperInstance) ecosystem.

{links_str}
"""

def make_docs_section():
    return "\n## Documentation\n\n📚 [OpenConstruct Docs](https://github.com/SuperInstance/openconstruct-docs)\n"

def update_readme(content, repo, missing):
    """Update README with missing sections."""
    additions = []
    
    # Build badge line
    badge = make_badge_line(repo, missing)
    if badge and "badges" in missing:
        # Add badges right after the title
        lines = content.split("\n")
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("#"):
                insert_idx = i + 1
                break
        lines.insert(insert_idx, "\n" + badge)
        content = "\n".join(lines)
        missing = [m for m in missing if m != "badges"]
    
    # Add documentation link
    if "documentation_link" in missing:
        content += make_docs_section()
    
    # Add ecosystem/how it fits section
    if "how_it_fits" in missing:
        content += make_ecosystem_section(repo)
    
    return content

# Process repos that need updates
updated = []
failed = []
skipped = []

to_update = {r: v for r, v in results.items() if v.get("missing") and "error" not in v.get("missing", [])}

print(f"Processing {len(to_update)} repos...")

tmpdir = tempfile.mkdtemp(prefix="ccc-eco-")
print(f"Working dir: {tmpdir}")

for i, (repo, info) in enumerate(to_update.items()):
    missing = info["missing"]
    print(f"\n[{i+1}/{len(to_update)}] {repo} — missing: {missing}", flush=True)
    
    repo_dir = os.path.join(tmpdir, repo)
    
    # Clone shallow
    r = run(f"gh repo clone {ORG}/{repo} {repo_dir} -- --depth=1 2>&1")
    if r.returncode != 0:
        print(f"  ✗ Clone failed: {r.stderr[:200]}")
        failed.append(repo)
        continue
    
    # Find README
    readme_path = None
    for name in ["README.md", "readme.md", "README.MD", "Readme.md"]:
        p = os.path.join(repo_dir, name)
        if os.path.exists(p):
            readme_path = p
            break
    
    if not readme_path:
        # Try to find any readme
        for f in os.listdir(repo_dir):
            if f.lower() == "readme.md":
                readme_path = os.path.join(repo_dir, f)
                break
    
    if not readme_path:
        print(f"  ✗ No README.md found")
        failed.append(repo)
        continue
    
    with open(readme_path, "r") as f:
        content = f.read()
    
    # Update
    new_content = update_readme(content, repo, missing)
    
    if new_content == content:
        print(f"  ⏭ No changes needed")
        skipped.append(repo)
        continue
    
    with open(readme_path, "w") as f:
        f.write(new_content)
    
    # Commit and push
    r = run(f"cd {repo_dir} && git add -A && git diff --cached --quiet")
    if r.returncode == 0:
        print(f"  ⏭ No changes staged")
        skipped.append(repo)
        continue
    
    r = run(f'cd {repo_dir} && git commit -m "{COMMIT_MSG}" && git push 2>&1')
    if r.returncode != 0:
        print(f"  ✗ Push failed: {r.stderr[:200]}")
        failed.append(repo)
        continue
    
    print(f"  ✓ Updated and pushed!")
    updated.append(repo)
    
    time.sleep(1)  # rate limit

# Cleanup
shutil.rmtree(tmpdir, ignore_errors=True)

print(f"\n=== FINAL RESULTS ===")
print(f"Updated: {len(updated)} — {updated}")
print(f"Failed: {len(failed)} — {failed}")
print(f"Skipped: {len(skipped)} — {skipped}")

with open("update_results.json", "w") as f:
    json.dump({"updated": updated, "failed": failed, "skipped": skipped}, f, indent=2)
