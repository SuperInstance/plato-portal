#!/bin/bash
# constraint-viz quickstart — generate oscilloscope visualizations
set -e
echo "📊 Constraint Viz — Quick Start"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$SCRIPT_DIR"

# Install deps
pip install -e "$WORKSPACE/constraint-synth" --quiet 2>/dev/null || true
pip install -e . --quiet 2>/dev/null || true

# If no MIDI files exist, generate one from constraint-synth first
MIDI_COUNT=$(ls "$WORKSPACE"/*.mid 2>/dev/null | wc -l)

python3 -c "
import sys, os, glob
sys.path.insert(0, '$SCRIPT_DIR')
sys.path.insert(0, '$WORKSPACE/constraint-synth')

from constraint_viz.multi_scale import ConstraintOscilloscope

scope = ConstraintOscilloscope()

# Find MIDI files
midis = sorted(glob.glob(os.path.join('$WORKSPACE', '*.mid')))
if not midis:
    # Try to find any .mid anywhere nearby
    midis = sorted(glob.glob(os.path.join('$WORKSPACE', '**', '*.mid'), recursive=True))[:5]

if not midis:
    print('⚠️  No MIDI files found — creating a synthetic demo...')
    import numpy as np
    # Generate a synthetic visualization without MIDI
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    out_dir = os.path.join('$SCRIPT_DIR', 'output')
    os.makedirs(out_dir, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Constraint Oscilloscope — Synthetic Demo', fontsize=14)
    
    t = np.linspace(0, 4*np.pi, 1000)
    axes[0,0].plot(t, np.sin(t)); axes[0,0].set_title('Sample Level')
    axes[0,1].plot(t[:200], np.sin(t[:200])*np.exp(-0.1*np.arange(200))); axes[0,1].set_title('Note Level')
    axes[1,0].plot(t, np.sin(t) + 0.3*np.sin(3*t)); axes[1,0].set_title('Phrase Level')
    axes[1,1].plot(t, np.sin(t) + np.cumsum(np.random.randn(1000)*0.01)); axes[1,1].set_title('Piece Level')
    
    for ax in axes.flat:
        ax.set_xlabel('Time')
        ax.set_ylabel('Constraint Value')
    
    plt.tight_layout()
    out_path = os.path.join(out_dir, 'synthetic_scope.png')
    fig.savefig(out_path, dpi=100)
    plt.close(fig)
    print(f'  ✅ Synthetic demo → {out_path}')
else:
    midis = midis[:5]
    print(f'Visualizing {len(midis)} MIDI files...')
    for midi_path in midis:
        name = os.path.basename(midi_path).replace('.mid', '')
        out_dir = os.path.join('$SCRIPT_DIR', 'output')
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, f'{name}_scope.png')
        try:
            scope.visualize_midi(midi_path, out)
            print(f'  ✅ {name} → {out}')
        except Exception as e:
            print(f'  ⚠️  {name}: {e}')

print()
print('✅ constraint-viz works!')
"
