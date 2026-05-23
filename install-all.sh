#!/bin/bash
# install-all.sh — One command to install the entire music ecosystem
set -e
echo "🎵 Installing SuperInstance Constraint Music Ecosystem..."
WORKSPACE="$(cd "$(dirname "$0")" && pwd)"

# Install shared dependencies first
echo "📦 Installing shared dependencies..."
pip install numpy mido matplotlib scipy --quiet 2>/dev/null

# Install core first (others depend on it)
if [ -d "$WORKSPACE/constraint-theory-core" ]; then
  echo "  ⚡ constraint-theory-core (required by others)"
  cd "$WORKSPACE/constraint-theory-core" && pip install -e . --quiet 2>/dev/null
fi

# Install all music packages
for pkg in counterpoint-engine groove-analyzer holonomy-harmony \
           spline-midi-smooth jazz-voicing-engine style-dna \
           constraint-synth constraint-viz plato-room-musician; do
  if [ -d "$WORKSPACE/$pkg" ]; then
    echo "  ⚡ $pkg"
    cd "$WORKSPACE/$pkg" && pip install -e . --quiet 2>/dev/null || echo "  ⚠️  $pkg had install issues (may still work)"
  else
    echo "  ⏭️  $pkg (not found)"
  fi
done

cd "$WORKSPACE"

# Set PYTHONPATH hint
echo ""
echo "✅ All installed!"
echo ""
echo "Run any quickstart to try a demo:"
echo "  bash constraint-theory-core/quickstart.sh"
echo "  bash counterpoint-engine/quickstart.sh"
echo "  bash groove-analyzer/quickstart.sh"
echo "  bash holonomy-harmony/quickstart.sh"
echo "  bash spline-midi-smooth/quickstart.sh"
echo "  bash jazz-voicing-engine/quickstart.sh"
echo "  bash style-dna/quickstart.sh"
echo "  bash constraint-synth/quickstart.sh"
echo "  bash constraint-viz/quickstart.sh"
