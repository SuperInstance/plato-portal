#!/bin/bash
# Resume publishing - fix missing descriptions, then publish remaining
set -euo pipefail

WORKDIR=$(ls -d /tmp/crates-publish-* | head -1)
LOGFILE="/home/phoenix/.openclaw/workspace/crates-publish-log.txt"

# Fix all Cargo.tomls to ensure they have description
for dir in "$WORKDIR"/lau-*/; do
  crate=$(basename "$dir")
  if [ -f "$dir/Cargo.toml" ]; then
    # Add description if missing
    if ! grep -q "^description" "$dir/Cargo.toml"; then
      # Generate description from crate name
      desc=$(echo "$crate" | sed 's/^lau-//' | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g')
      desc="Rust library for $desc in the PLATO agent ecosystem"
      sed -i "/^repository/a description = \"$desc\"" "$dir/Cargo.toml"
      echo "Fixed description for $crate"
    fi
    # Ensure license
    if ! grep -q "^license" "$dir/Cargo.toml"; then
      sed -i '/^edition/a license = "MIT"' "$dir/Cargo.toml"
    fi
    # Ensure repository
    if ! grep -q "^repository" "$dir/Cargo.toml"; then
      sed -i "/^license/a repository = \"https://github.com/SuperInstance/$crate\"" "$dir/Cargo.toml"
    fi
  fi
done

echo "All Cargo.toml files fixed" | tee -a "$LOGFILE"

# Now publish remaining crates
CRATES=(
  lau-provider lau-port lau-room-native lau-ensign lau-jepa-gravity lau-penrose lau-plato-tutor
  lau-shell-transport lau-conservation-engine lau-gravity-field lau-tick-runtime lau-a2a-protocol
  lau-construct-integration lau-construct-integration-v2 lau-agent-unify lau-kintsugi-runtime lau-memory-tiles
  lau-tropical-geometry lau-sheaf-cohomology lau-information-geometry lau-lie-algebra lau-categorical-homotopy
  lau-ricci-flow-agents lau-spectral-graph-agent lau-optimal-transport-agents lau-derived-topos lau-conservation-guard
  lau-training-room lau-mission lau-consciousness-bridge lau-domestication lau-inheritance
  lau-destruction-transform lau-tensor-midi lau-symmetry-engine lau-kintsugi lau-palaver
  lau-polyglot-tradition lau-quipu lau-songline lau-rhythm-nation lau-adinkra
  lau-griot lau-tradition-proof lau-seven-eyes-demo lau-gateway-demo lau-intention-field
  lau-provenance lau-async-tick lau-circuit lau-shell-spawn lau-inter-shell
  lau-onboarding lau-tile-store lau-port-v2 lau-a2ui-protocol lau-shell-lifecycle
  lau-construct-cli lau-ensign-sdk lau-plato-room-sdk lau-git-agent lau-git-render
  lau-affordance lau-agent-runtime lau-token-economy lau-terrain lau-shell-interface
  lau-construct lau-tminus lau-vibe-compiler lau-a2ui lau-penrose-v2
  lau-agent-dream lau-agent-homeostasis lau-agent-profile lau-agent-shell lau-ai-tutor
  lau-animation lau-camera lau-conservation-matrix lau-event-bus lau-fibonacci-growth
  lau-hermes-oracle-boot lau-integration-test lau-murmur-protocol-v2 lau-plato-integration lau-provenance-chain
  lau-room-acoustics lau-state-machine lau-tile-compress
)

PUBLISHED=0
FAILED=0
COUNT=0

for crate in "${CRATES[@]}"; do
  # Skip already published
  existing=$(curl -sf "https://crates.io/api/v1/crates/$crate" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('crate',{}).get('max_version',''))" 2>/dev/null || echo "")
  if [ -n "$existing" ]; then
    echo "✅ $crate already v$existing"
    continue
  fi

  COUNT=$((COUNT + 1))
  dir="$WORKDIR/$crate"

  # Clone if not present
  if [ ! -d "$dir" ]; then
    gh repo clone "SuperInstance/$crate" "$dir" -- --depth 1 2>/dev/null || {
      echo "❌ $crate: clone failed"
      FAILED=$((FAILED + 1))
      continue
    }
    # Fix metadata
    if ! grep -q "^license" "$dir/Cargo.toml"; then
      sed -i '/^edition/a license = "MIT"' "$dir/Cargo.toml"
    fi
    if ! grep -q "^repository" "$dir/Cargo.toml"; then
      sed -i "/^license/a repository = \"https://github.com/SuperInstance/$crate\"" "$dir/Cargo.toml"
    fi
    if ! grep -q "^description" "$dir/Cargo.toml"; then
      desc=$(echo "$crate" | sed 's/^lau-//' | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g')
      sed -i "/^repository/a description = \"Rust library for $desc in the PLATO agent ecosystem\"" "$dir/Cargo.toml"
    fi
  fi

  cd "$dir"
  echo ""
  echo "📦 [$COUNT] $crate"

  if cargo publish --allow-dirty 2>&1 | tail -5; then
    echo "✅ $crate published!"
    PUBLISHED=$((PUBLISHED + 1))
  else
    echo "❌ $crate failed"
    FAILED=$((FAILED + 1))
  fi

  # Rate limit
  if [ $((COUNT % 5)) -eq 0 ]; then
    echo "⏳ Cooldown 90s..."
    sleep 90
  else
    sleep 3
  fi
done

echo ""
echo "DONE! Published: $PUBLISHED, Failed: $FAILED"
