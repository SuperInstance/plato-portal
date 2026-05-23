#!/usr/bin/env python3
"""Constraint Substrate Demo — 5 Primitives in Musical Action.

Demonstrates lattice_snap, funnel, is_laman, consensus, and holonomy
with real musical numbers and a text-based piano roll visualization.
Shows the 4-order diagnostic interpretation.
"""

import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "python"))

from constraint_substrate import (
    snap,
    funnel_step,
    holonomy_winding,
    is_laman,
    consensus_round,
)
from constraint_substrate._cffi import is_available as cffi_available


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# MIDI-like note numbers for a C major scale (C4 = 60)
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def midi_to_name(midi):
    return f"{NOTE_NAMES[int(midi) % 12]}{int(midi) // 12 - 1}"

def midi_to_freq(midi):
    return 440.0 * (2.0 ** ((midi - 69) / 12.0))

def pitch_class(midi):
    return midi % 12


def text_piano_roll(notes, label="", width=48, low=48, high=84):
    """Render a simple text-based piano roll.
    
    notes: list of (start_beat, duration, midi_note) tuples
    """
    print(f"\n  🎹 Piano Roll: {label}")
    print("  " + "-" * width)
    
    # Build grid
    span = high - low
    for midi in range(high, low - 1, -1):
        is_black = NOTE_NAMES[midi % 12] in ("C#", "D#", "F#", "G#", "A#")
        key = "♯" if is_black else "│"
        row = [key] * width
        
        for start, dur, note in notes:
            if note == midi:
                beat_start = int(start * width / 4) % width
                beat_len = max(1, int(dur * width / 4))
                for c in range(beat_start, min(beat_start + beat_len, width)):
                    row[c] = "█"
        
        name = midi_to_name(midi)
        marker = "►" if any(n[2] == midi for n in notes) else " "
        print(f"  {marker}{name:>4} {''.join(row)}")
    
    # Beat markers
    beat_row = "  " + " " * 6
    for i in range(width):
        if i % (width // 4) == 0:
            beat_row += str(i // (width // 4) + 1)
        else:
            beat_row += " "
    print(beat_row)
    print("  " + "-" * width)


# ---------------------------------------------------------------------------
# Order Diagnostic
# ---------------------------------------------------------------------------

def order_diagnostic(order_values):
    """Print 4-order diagnostic interpretation.
    
    0th order: snap position (where things are)
    1st order: funnel direction (where things are going)
    2nd order: consensus change (how they're agreeing)
    3rd order: Laman structure (how rigid the relationships are)
    """
    print("\n  ╔═══════════════════════════════════════════╗")
    print("  ║  4-ORDER Diagnostic                       ║")
    print("  ╚═══════════════════════════════════════════╝")
    
    labels = [
        ("0th — Position (snap)", "Where the voices sit on the lattice"),
        ("1st — Direction (funnel)", "Which way each voice is moving"),
        ("2nd — Agreement (consensus)", "How the voices converge"),
        ("3rd — Structure (Laman)", "Rigidity of harmonic framework"),
    ]
    
    for i, ((label, desc), val) in enumerate(zip(labels, order_values)):
        print(f"\n  Order {i}: {label}")
        print(f"    → {desc}")
        print(f"    → Value: {val}")


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main():
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  CONSTRAINT SUBSTRATE — Musical Demo                            ║")
    print("║  5 Primitives × Real Musical Numbers                            ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    
    if cffi_available():
        print("  🔗 C FFI backend: AVAILABLE")
    else:
        print("  🐍 C FFI backend: not loaded (using pure Python)")
    
    print()
    
    # =========================================================================
    # 1. LATTICE SNAP — Snap pitch to Eisenstein lattice
    # =========================================================================
    print("━" * 66)
    print("  1. LATTICE SNAP — Pitch → Eisenstein A₂ Lattice")
    print("━" * 66)
    
    # Musical interpretation: map pitch space onto the Eisenstein lattice
    # Using pitch-class vectors (2D representation of harmonic relationships)
    pitches = [
        ("C4", 60, 0.0, 0.0),
        ("E4", 64, 1.5, 0.866),
        ("G4", 67, 0.7, 1.2),
        ("A4", 69, -0.5, 1.5),
        ("Bb4", 70, 2.1, 0.3),
    ]
    
    snapped_notes = []
    print(f"\n  {'Note':>5} | {'Input (x,y)':>18} | {'Snapped (x,y)':>18} | {'Error':>8}")
    print("  " + "-" * 60)
    
    for name, midi, x, y in pitches:
        sx, sy, err = snap(x, y)
        print(f"  {name:>5} | ({x:6.3f}, {y:6.3f}) | ({sx:6.3f}, {sy:6.3f}) | {err:.6f}")
        snapped_notes.append((0, 1, midi))
    
    # Snap a detuned note
    detuned_x, detuned_y = 1.73, 0.52
    sx, sy, err = snap(detuned_x, detuned_y)
    print(f"\n  Snapping detuned pitch ({detuned_x}, {detuned_y})")
    print(f"    → Lattice point: ({sx:.3f}, {sy:.3f}), error: {err:.4f}")
    
    order_0 = f"5 voices snapped to lattice, max error = {max(snap(x,y)[2] for _,_,x,y in pitches):.4f}"
    
    # =========================================================================
    # 2. FUNNEL — Move toward a target
    # =========================================================================
    print(f"\n{'━' * 66}")
    print("  2. FUNNEL — Deadband Convergence (Voice Leading)")
    print("━" * 66)
    
    # A voice leading scenario: move from current chord toward target chord
    voice_names = ["Soprano", "Alto", "Tenor", "Bass"]
    current = [67, 64, 60, 48]   # C major: G4, E4, C4, C3
    target  = [65, 62, 57, 50]   # Different target
    
    epsilon = 2.0
    decay = 0.15
    
    print(f"\n  Current chord: {', '.join(f'{n} ({midi_to_name(n)})' for n in current)}")
    print(f"  Target chord:  {', '.join(f'{n} ({midi_to_name(n)})' for n in target)}")
    print(f"  Epsilon: {epsilon}, Decay: {decay}")
    print()
    
    # Run 8 steps of funnel
    funnel_history = [current[:]]
    cur_vals = current[:]
    cur_eps = [epsilon] * 4
    
    for step_num in range(8):
        new_vals = []
        new_eps = []
        for i in range(4):
            v, e = funnel_step(cur_vals[i], target[i], cur_eps[i], decay)
            new_vals.append(round(v, 3))
            new_eps.append(round(e, 4))
        funnel_history.append(new_vals[:])
        cur_vals = new_vals
        cur_eps = new_eps
        
        names = [midi_to_name(int(round(v))) for v in cur_vals]
        print(f"  Step {step_num+1}: [{', '.join(f'{v:6.2f}' for v in cur_vals)}] → {', '.join(names)}  (eps: {cur_eps[0]:.4f})")
    
    # Piano roll of funnel convergence
    funnel_notes = []
    for step_i, chord in enumerate(funnel_history):
        for note in chord:
            funnel_notes.append((step_i, 0.8, int(round(note))))
    text_piano_roll(funnel_notes, "Voice Leading via Funnel", low=45, high=72)
    
    order_1 = f"Voices converge from {current} toward {target} over 8 funnel steps"
    
    # =========================================================================
    # 3. LAMAN RIGIDITY — Check a chord progression
    # =========================================================================
    print(f"\n{'━' * 66}")
    print("  3. LAMAN RIGIDITY — Harmonic Framework Rigidity")
    print("━" * 66)
    
    # Model chord progressions as graphs:
    # Vertices = chord members, Edges = voice-leading relationships
    
    progressions = [
        ("I-V-I (4 voices, 3 chords)", 12, [
            # 3 chords × 4 voices = 12 vertices
            # Within-chord edges (triadic)
            (0,1),(1,2),(0,2),   # I: C-E-G
            (3,4),(4,5),         # I bass doubling
            (6,7),(7,8),(6,8),   # V: G-B-D
            (9,10),(10,11),(9,11), # I: C-E-G return
            # Voice-leading edges (between chords)
            (2,6),(1,7),(0,6),   # I→V
            (6,9),(7,10),(8,11), # V→I
        ]),
        ("Single triad", 3, [(0,1),(1,2),(0,2)]),
        ("Parallel 5ths (weak)", 8, [
            (0,1),(1,2),(0,2),(3,4),(4,5),(3,5),
            (0,3),(1,4),(2,5),(6,7)
        ]),
    ]
    
    print()
    for name, n, edges in progressions:
        rigid = is_laman(n, edges)
        status = "🔒 RIGID" if rigid else "🔓 NOT rigid"
        print(f"  {name}: {status}  ({len(edges)} edges, {n} vertices, need ≥{2*n-3})")
    
    order_3 = f"Checked {len(progressions)} progressions for structural rigidity"
    
    # =========================================================================
    # 4. CONSENSUS — Multiple voices agreeing
    # =========================================================================
    print(f"\n{'━' * 66}")
    print("  4. CONSENSUS — Metronome Agreement Between Voices")
    print("━" * 66)
    
    # 4 voices trying to agree on a tempo (BPM) or pitch
    voice_tempi = [118.0, 122.0, 119.0, 121.0]
    eps = 2.0
    
    print(f"\n  Initial tempi: {voice_tempi}")
    print(f"  Epsilon: {eps}")
    print()
    
    converged = False
    for rnd in range(10):
        voice_tempi, converged = consensus_round(voice_tempi, eps)
        eps *= math.exp(-0.2)  # decay epsilon
        print(f"  Round {rnd+1}: {[f'{v:.2f}' for v in voice_tempi]}  (converged: {converged}, eps: {eps:.3f})")
        if converged:
            break
    
    print(f"\n  Final consensus: {voice_tempi[0]:.2f} BPM after {rnd+1} rounds")
    
    # Circular consensus with modulus (pitch classes)
    print("\n  Circular consensus (pitch classes, mod 12):")
    pitch_classes = [1.0, 11.0, 0.5, 10.8]  # near C/C# wrap-around
    print(f"  Initial: {[f'{v:.1f}' for v in pitch_classes]}")
    pc_result, pc_conv = consensus_round(pitch_classes, 2.0, modulus=12.0)
    print(f"  After 1 round: {[f'{v:.2f}' for v in pc_result]}  (converged: {pc_conv})")
    
    order_2 = f"4 voices reached tempo consensus at {voice_tempi[0]:.1f} BPM"
    
    # =========================================================================
    # 5. HOLONOMY — Winding through pitch space
    # =========================================================================
    print(f"\n{'━' * 66}")
    print("  5. HOLONOMY — Winding Number in Pitch Space")
    print("━" * 66)
    
    sequences = [
        ("Ascending scale (C-C)", [0, 2, 4, 5, 7, 9, 11, 12]),
        ("Descending scale", [12, 10, 8, 7, 5, 3, 1, 0]),
        ("Chromatic ascent", list(range(13))),
        ("Circle of 5ths (mod 12)", [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5, 0]),
    ]
    
    print()
    for name, vals in sequences:
        # Normalize to pitch classes for winding
        w = holonomy_winding(vals, 12.0)
        winds = f"{w:.2f}"
        print(f"  {name:30s}: winding = {winds}")
    
    # =========================================================================
    # 4-Order Diagnostic
    # =========================================================================
    order_diagnostic([order_0, order_1, order_2, order_3])
    
    # Final piano roll: the converged chord
    final_notes = [(0, 1, int(round(v))) for v in funnel_history[-1]]
    text_piano_roll(final_notes, "Final Converged Chord", low=45, high=72)
    
    print("\n  ✅ Demo complete — 5 primitives exercised with musical numbers.")
    print()


if __name__ == "__main__":
    main()
