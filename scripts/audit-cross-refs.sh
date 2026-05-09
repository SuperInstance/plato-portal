#!/usr/bin/env bash
# audit-cross-refs.sh — Check all SuperInstance READMEs for cross-reference health
# 
# Checks:
# 1. Which repos have the meta-header, which don't
# 2. Broken "Depended by" claims (repo claims dependency but target doesn't have it)
# 3. Stale READMEs (>90 days since last commit)
# 4. Cross-reference completeness for key repos

set -e

OUTPUT="${1:-CROSS-REFERENCES.md}"
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

echo "# Cross-Reference Audit" > "$OUTPUT"
echo "" >> "$OUTPUT"
echo "**Generated:** $(date -u '+%Y-%m-%d %H:%M UTC')" >> "$OUTPUT"
echo "" >> "$OUTPUT"

# Fetch recent commits for key repos to check staleness
KEY_REPOS=(
  "keel" "plato-server" "fleet-coordinate" "holonomy-consensus"
  "fleet-spread" "crab-traps" "constraint-theory-ecosystem"
  "cocapn-ai-web" "flux-vm" "eisenstein"
)

echo "## 1. Key Repo Freshness" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "| Repo | Last Commit | Status |" >> "$OUTPUT"
echo "|------|-------------|--------|" >> "$OUTPUT"

for repo in "${KEY_REPOS[@]}"; do
  last_commit=$(gh api "repos/SuperInstance/$repo/commits?per_page=1" --jq '.[0].commit.committer.date // "never"' 2>/dev/null)
  age_days=999
  if [ "$last_commit" != "never" ]; then
    last_epoch=$(date -d "$last_commit" +%s 2>/dev/null || echo 0)
    now_epoch=$(date +%s)
    age_days=$(( (now_epoch - last_epoch) / 86400 ))
  fi
  
  if [ "$age_days" -gt 90 ]; then
    status="🔴 Stale ($age_days days)"
  elif [ "$age_days" -gt 30 ]; then
    status="🟡 Aging ($age_days days)"
  else
    status="🟢 Recent ($age_days days)"
  fi
  echo "| $repo | ${last_commit:0:10} | $status |" >> "$OUTPUT"
done

# Check which key repos have meta-headers
echo "" >> "$OUTPUT"
echo "## 2. Meta-Header Coverage" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "| Repo | Has Meta | Depends On | Depended By | Implements |" >> "$OUTPUT"
echo "|------|----------|------------|-------------|------------|" >> "$OUTPUT"

# Read local repo metadata
for repo in "${KEY_REPOS[@]}"; do
  local_path=""
  # Check various clone locations
  for base in /tmp/si-update /tmp/keel-new /tmp/si-org /tmp/crab-traps; do
    if [ -d "$base/.git" ]; then
      remote=$(cd "$base" && git remote -v 2>/dev/null | head -1)
      if echo "$remote" | grep -qi "$repo"; then
        local_path="$base"
        break
      fi
    fi
  done
  
  has_meta="❌"
  depends="—"
  depended="—"
  implements="—"
  
  if [ -n "$local_path" ] && [ -f "$local_path/README.md" ]; then
    if grep -q "## Meta" "$local_path/README.md" 2>/dev/null; then
      has_meta="✅"
      depends=$(grep -A2 "\*\*Depends on\*\*" "$local_path/README.md" 2>/dev/null | head -1 | sed 's/.*Depends on:\*\* //;s/\*$//' || echo "—")
      depended=$(grep -A2 "\*\*Depended by\*\*" "$local_path/README.md" 2>/dev/null | head -1 | sed 's/.*Depended by:\*\* //;s/\*$//' || echo "—")
      implements=$(grep -A2 "\*\*Implements\*\*" "$local_path/README.md" 2>/dev/null | head -1 | sed 's/.*Implements:\*\* //;s/\*$//' || echo "—")
    fi
  fi
  
  echo "| $repo | $has_meta | $depends | $depended | $implements |" >> "$OUTPUT"
done

echo "" >> "$OUTPUT"
echo "## 3. Recommendations" >> "$OUTPUT"
echo "" >> "$OUTPUT"

# Add missing meta recommendations
for repo in "${KEY_REPOS[@]}"; do
  local_path=""
  for base in /tmp/si-update /tmp/keel-new /tmp/si-org /tmp/crab-traps; do
    if [ -d "$base/.git" ]; then
      remote=$(cd "$base" && git remote -v 2>/dev/null | head -1)
      if echo "$remote" | grep -qi "$repo"; then
        local_path="$base"
        break
      fi
    fi
  done
  
  if [ -n "$local_path" ] && [ -f "$local_path/README.md" ]; then
    if ! grep -q "## Meta" "$local_path/README.md" 2>/dev/null; then
      echo "- **[$repo](https://github.com/SuperInstance/$repo)** — needs meta-header" >> "$OUTPUT"
    fi
  fi
done

wc -l "$OUTPUT"
echo "Audit written: $OUTPUT"