#!/usr/bin/env python3
"""Visualize the fugue as a piano-roll style image."""
import sys, os

# Mock dependencies
import types
def _mock_mod(name):
    mod = types.ModuleType(name)
    mod.FluxVector = type('FluxVector', (), {})
    mod.MidiEvent = type('MidiEvent', (), {})
    mod.A2Point = type('A2Point', (), {})
    mod.snap = lambda *a: None
    mod.encode_dodecet = lambda *a: 0
    mod.decode_dodecet = lambda *a: 0
    mod.vector48_encode = lambda *a: 0
    mod.vector48_decode = lambda *a: 0
    mod.DODECET_DIRECTIONS = {}
    mod.henneberg_construct = lambda *a, **kw: []
    return mod

for name in ['flux_tensor_midi', 'flux_tensor_midi.core', 'flux_tensor_midi.core.flux',
             'flux_tensor_midi.midi', 'flux_tensor_midi.midi.events',
             'constraint_theory_core', 'constraint_theory_core.lattice',
             'constraint_theory_core.rigidity']:
    sys.modules[name] = _mock_mod(name)
rig = sys.modules['constraint_theory_core.rigidity']
rig.is_laman = lambda *a: True
rig.henneberg_construct = lambda *a, **kw: []

import mido
import numpy as np

mid = mido.MidiFile('/home/phoenix/.openclaw/workspace/fugue_d_minor.mid')

# Extract notes from all tracks
voices = []
voice_names = []
for track in mid.tracks:
    if track.name == 'Tempo':
        continue
    voice_names.append(track.name)
    notes = []
    current_time = 0
    active_notes = {}
    for msg in track:
        current_time += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
            active_notes[msg.note] = current_time
        elif msg.type == 'note_off':
            if msg.note in active_notes:
                start = active_notes.pop(msg.note)
                notes.append((msg.note, start, current_time))
    voices.append(notes)

# Create piano-roll image
total_ticks = mid.length * mid.ticks_per_beat * 2  # approximate
min_note = 36  # C2
max_note = 79  # G5
note_range = max_note - min_note + 1

# Use ticks per beat for scaling
ticks_per_beat = mid.ticks_per_beat
total_beats = int(mid.length * 2) + 1

img_width = total_beats * 20  # 20 pixels per beat
img_height = note_range * 8  # 8 pixels per semitone

# Use PIL for image
from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGB', (img_width + 120, img_height + 60), '#1a1a2e')
draw = ImageDraw.Draw(img)

colors = ['#e94560', '#0f3460', '#16c79a', '#f5a623']  # Bass, Tenor, Alto, Soprano

# Draw grid
for note in range(min_note, max_note + 1):
    y = img_height - (note - min_note) * 8 + 30
    if note % 12 == 0:  # C notes
        draw.line([(100, y), (img_width + 100, y)], fill='#333355', width=1)
        note_names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        name = f"{note_names[note%12]}{note//12-1}"
        draw.text((5, y - 6), name, fill='#666688')

# Draw notes
for v_idx, notes in enumerate(voices):
    color = colors[v_idx % len(colors)]
    for (note, start, end) in notes:
        x = 100 + int(start / ticks_per_beat * 20)
        w = max(int((end - start) / ticks_per_beat * 20), 4)
        y = img_height - (note - min_note) * 8 + 30
        draw.rectangle([x, y - 6, x + w, y + 2], fill=color)

# Legend
for i, name in enumerate(voice_names):
    draw.rectangle([10, 5 + i * 18, 25, 15 + i * 18], fill=colors[i])
    draw.text((30, 3 + i * 18), name, fill='white')

# Title
draw.text((img_width // 2 - 40, img_height + 35), "Fugue in D Minor", fill='white')

output_path = '/home/phoenix/.openclaw/workspace/fugue_d_minor_pianoroll.png'
img.save(output_path)
print(f"✓ Piano roll saved: {output_path} ({img.width}x{img.height})")
