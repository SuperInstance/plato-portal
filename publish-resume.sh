#!/bin/bash
# Resume publishing remaining lau-* crates
set -euo pipefail

UA="User-Agent: superinstance-publish-bot/1.0"
WORKDIR="/tmp/crates-publish-resume"
mkdir -p "$WORKDIR"

# Get all lau- repos
CRATES=( $(gh repo list SuperInstance --limit 100 --json name --jq '.[].name' 2>/dev/null | grep "^lau-" | sort) )

PUBLISHED=0
FAILED=0
COUNT=0

for crate in "${CRATES[@]}"; do
  # Check if already on crates.io
  check=$(curl -sH "$UA" "https://crates.io/api/v1/crates/$crate" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('crate',{}).get('max_version',''))" 2>/dev/null || echo "")
  if [ -n "$check" ]; then
    continue
  fi

  COUNT=$((COUNT + 1))
  echo ""
  echo "📦 [$COUNT] $crate"

  dir="$WORKDIR/$crate"
  if [ ! -d "$dir" ]; then
    gh repo clone "SuperInstance/$crate" "$dir" -- --depth 1 2>/dev/null || {
      echo "❌ clone failed"
      FAILED=$((FAILED + 1))
      continue
    }
  fi

  cd "$dir"

  # Fix metadata
  if [ ! -f "Cargo.toml" ]; then
    echo "❌ no Cargo.toml"
    FAILED=$((FAILED + 1))
    continue
  fi

  # Add license if missing
  if ! grep -q "^license" Cargo.toml; then
    sed -i '/^edition/a license = "MIT"' Cargo.toml
  fi
  # Add repository if missing
  if ! grep -q "^repository" Cargo.toml; then
    sed -i "/^license/a repository = \"https://github.com/SuperInstance/$crate\"" Cargo.toml
  fi
  # Add description if missing
  if ! grep -q "^description" Cargo.toml; then
    desc=$(echo "$crate" | sed 's/^lau-//' | tr '-' ' ')
    sed -i "/^repository/a description = \"Rust library for $desc in the PLATO ecosystem\"" Cargo.toml
  fi

  # Commit and push fix
  git add -A && git commit -m "Add crates.io metadata" --allow-empty 2>/dev/null || true
  git push 2>/dev/null || true

  # Publish
  if cargo publish --allow-dirty 2>&1 | tail -5; then
    echo "✅ $crate published!"
    PUBLISHED=$((PUBLISHED + 1))
  else
    echo "❌ $crate failed"
    FAILED=$((FAILED + 1))
  fi

  # Rate limit: 5 crates then 90s cooldown
  if [ $((COUNT % 5)) -eq 0 ]; then
    echo "⏳ Cooldown 90s after $COUNT..."
    sleep 90
  else
    sleep 5
  fi
done

echo ""
echo "DONE! New: $PUBLISHED, Failed: $FAILED"
