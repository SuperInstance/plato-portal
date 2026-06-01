#!/bin/bash
# Batch publish lau-* crates to crates.io
# Fixes missing metadata before publishing

set -euo pipefail

CRATES=(
  lau-intention lau-vibe-field lau-shell-kernel lau-provider lau-port
  lau-room-native lau-ensign lau-jepa-gravity lau-penrose lau-plato-tutor
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

WORKDIR="/tmp/crates-publish-$(date +%s)"
mkdir -p "$WORKDIR"
PUBLISHED=0
FAILED=0
COUNT=0
LOGFILE="/home/phoenix/.openclaw/workspace/crates-publish-log.txt"
echo "Publish wave started $(date)" > "$LOGFILE"

for crate in "${CRATES[@]}"; do
  # Check if already published
  existing=$(curl -sf "https://crates.io/api/v1/crates/$crate" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('crate',{}).get('max_version',''))" 2>/dev/null || echo "")
  if [ -n "$existing" ]; then
    echo "✅ $crate already v$existing" | tee -a "$LOGFILE"
    PUBLISHED=$((PUBLISHED + 1))
    continue
  fi

  COUNT=$((COUNT + 1))
  echo "" | tee -a "$LOGFILE"
  echo "📦 [$COUNT] Publishing $crate" | tee -a "$LOGFILE"

  # Clone
  if [ ! -d "$WORKDIR/$crate" ]; then
    gh repo clone "SuperInstance/$crate" "$WORKDIR/$crate" -- --depth 1 2>/dev/null || {
      echo "❌ $crate: clone failed" | tee -a "$LOGFILE"
      FAILED=$((FAILED + 1))
      continue
    }
  fi

  cd "$WORKDIR/$crate"

  # Fix Cargo.toml - add license, repository
  if ! grep -q "^license" Cargo.toml; then
    sed -i '/^edition/a license = "MIT"' Cargo.toml
  fi
  if ! grep -q "^repository" Cargo.toml; then
    sed -i "/^license/a repository = \"https://github.com/SuperInstance/$crate\"" Cargo.toml
  fi

  # Commit the fix
  git add Cargo.toml 2>/dev/null
  git commit -m "Add license + repository metadata for crates.io" --allow-empty 2>/dev/null || true
  git push 2>/dev/null || true

  # Publish
  if cargo publish --allow-dirty 2>&1 | tee -a "$LOGFILE" | tail -3; then
    echo "✅ $crate published!" | tee -a "$LOGFILE"
    PUBLISHED=$((PUBLISHED + 1))
  else
    echo "❌ $crate failed" | tee -a "$LOGFILE"
    FAILED=$((FAILED + 1))
  fi

  # Rate limit cooldown every 5 new attempts
  if [ $((COUNT % 5)) -eq 0 ] && [ $COUNT -gt 0 ]; then
    echo "⏳ Cooldown 120s after $COUNT attempts..." | tee -a "$LOGFILE"
    sleep 120
  else
    sleep 5
  fi
done

echo "" | tee -a "$LOGFILE"
echo "=========================================" | tee -a "$LOGFILE"
echo "DONE! Published: $PUBLISHED, Failed: $FAILED" | tee -a "$LOGFILE"
echo "=========================================" | tee -a "$LOGFILE"
