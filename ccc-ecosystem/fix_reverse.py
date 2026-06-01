#!/usr/bin/env python3
"""Fix reverse links in existing DEPENDENCIES.md files."""
import subprocess
import os
import tempfile
import shutil
import time
import base64

ORG = "SuperInstance"
COMMIT_MSG = "docs: ecosystem cross-references — CCC autonomous"

def run(cmd, **kwargs):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60, **kwargs)

# Reverse links that need to be added
reverse_fixes = {
    "cocapn-core": {"OpenConstruct"},
    "openconstruct-abi": {"OpenConstruct", "plato-vision", "plato-tick"},
    "openconstruct-rust": {"OpenConstruct"},
    "plato-tick": {"OpenConstruct"},
}

tmpdir = tempfile.mkdtemp(prefix="ccc-reverse-")
updated = []

for repo, missing_deps in reverse_fixes.items():
    repo_dir = os.path.join(tmpdir, repo)
    
    r = run(f"gh repo clone {ORG}/{repo} {repo_dir} -- --depth=1 2>&1")
    if r.returncode != 0:
        print(f"✗ Can't clone {repo}")
        continue
    
    deps_path = os.path.join(repo_dir, "DEPENDENCIES.md")
    if not os.path.exists(deps_path):
        print(f"✗ No DEPENDENCIES.md in {repo}")
        continue
    
    with open(deps_path) as f:
        content = f.read()
    
    additions = []
    for dep in sorted(missing_deps):
        if dep.lower() not in content.lower():
            additions.append(f"- [{dep}](https://github.com/SuperInstance/{dep})")
    
    if not additions:
        print(f"⏭ {repo} already up to date")
        continue
    
    # Add to Downstream section
    block = "\n".join(additions) + "\n"
    if "## Downstream" in content:
        content = content.replace("## Downstream\n", f"## Downstream\n{block}")
    else:
        content += f"\n## Downstream\n\n" + block
    
    with open(deps_path, "w") as f:
        f.write(content)
    
    r = run(f'cd {repo_dir} && git add -A && git diff --cached --quiet')
    if r.returncode == 0:
        continue
    
    r = run(f'cd {repo_dir} && git commit -m "{COMMIT_MSG}" && git push 2>&1')
    if r.returncode != 0:
        print(f"✗ Push failed for {repo}: {r.stderr[:200]}")
        continue
    
    print(f"✓ Updated {repo} with reverse deps: {missing_deps}")
    updated.append(repo)
    time.sleep(1)

shutil.rmtree(tmpdir, ignore_errors=True)
print(f"\nUpdated {len(updated)} repos with reverse links: {updated}")
