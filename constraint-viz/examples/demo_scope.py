#!/usr/bin/env python3
"""Constraint Oscilloscope demo — visualize constraint structure at 4 scales.

Generates a synthetic MIDI file, then renders a 4-panel PNG showing
sample-level, note-level, phrase-level, and piece-level views.
"""

import os
import sys
import tempfile

# Ensure the package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo

from constraint_viz import ConstraintOscilloscope


def generate_demo_midi(path: str):
    """Create a simple 8-bar MIDI file for visualization."""
    mid = MidiFile(ticks_per_beat=480)
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(120), time=0))
    track.append(MetaMessage("time_signature", numerator=4, denominator=4, time=0))

    # Simple C major scale pattern over 8 bars
    notes = [60, 62, 64, 65, 67, 69, 71, 72, 71, 69, 67, 65, 64, 62, 60, 59]
    velocities = [80, 85, 90, 95, 100, 95, 90, 100, 95, 90, 85, 80, 75, 80, 85, 70]

    dur = 480  # quarter note
    for i in range(8):
        for j, (note, vel) in enumerate(zip(notes, velocities)):
            offset = i * len(notes)
            track.append(Message("note_on", note=note, velocity=vel, time=0))
            track.append(Message("note_off", note=note, velocity=0, time=dur))

    mid.save(path)
    print(f"  Generated demo MIDI: {path}")


def main():
    outdir = os.environ.get("DEMO_OUTPUT", os.path.join(os.path.dirname(__file__), "..", "..", "demo", "output"))
    os.makedirs(outdir, exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as f:
        midi_path = f.name

    try:
        generate_demo_midi(midi_path)

        scope = ConstraintOscilloscope()
        output_png = os.path.join(outdir, "constraint_scope.png")
        scope.visualize_midi(midi_path, output_path=output_png, title="Constraint Oscilloscope — Demo")
        print(f"  ✅ Saved 4-panel visualization: {output_png}")
    finally:
        os.unlink(midi_path)


if __name__ == "__main__":
    main()
