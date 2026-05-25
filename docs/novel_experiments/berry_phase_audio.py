#!/usr/bin/env python3
"""
Experiment 6: Berry Phase Audio — Audible Berry phase
- Play chords around circle of fifths: C-G-D-A-E-B-F#-C#-G#-D#-A#-F-C
- Each chord 2 seconds, just intonation
- Final C is 23.46 cents sharp — the Berry phase is AUDIBLE
- Output: 24s WAV
"""
import numpy as np
import struct, os, json

SR = 44100
DURATION = 26  # 13 chords × 2s
OUT = os.path.join(os.path.dirname(__file__), "berry_phase.wav")

def write_wav(path, samples, sr=SR):
    samples = np.clip(samples, -1.0, 1.0)
    data = (samples * 32767).astype(np.int16)
    with open(path, 'wb') as f:
        n = len(data)
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + n * 2))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<IHHIIHH', 16, 1, 1, sr, sr * 2, 2, 16))
        f.write(b'data')
        f.write(struct.pack('<I', n * 2))
        f.write(data.tobytes())

# Circle of fifths in just intonation
# Each step up a fifth = frequency ratio 3/2
# Starting from C = 261.63 Hz
# After 12 steps: (3/2)^12 = 531441/4096 ≈ 129.746... (should be 128 = 2^7)
# The discrepancy: 531441/4096 / 128 = 531441/524288 ≈ 1.01364
# In cents: 1200 * log2(531441/524288) ≈ 23.46 cents (Pythagorean comma)

C_BASE = 261.63  # C4 in equal temperament

# Build circle of fifths
circle = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'F', 'C_final']
fifths_freq = [C_BASE]

for i in range(12):
    fifths_freq.append(fifths_freq[-1] * 3 / 2)
    # Bring down by octave if needed
    while fifths_freq[-1] > 2 * C_BASE:
        fifths_freq[-1] /= 2

# For each note in the circle, build a major triad in just intonation
# Root, major third (5/4), fifth (3/2)
CHORD_DUR = 2.0
n_samples = int(SR * DURATION)
output = np.zeros(n_samples)

berry_data = []

for i, (note, root) in enumerate(zip(circle, fifths_freq)):
    start = int(i * CHORD_DUR * SR)
    end = int((i + 1) * CHORD_DUR * SR)
    n = end - start
    t = np.arange(n, dtype=np.float64) / SR
    
    # Just intonation triad: root, major third (5/4), fifth (3/2)
    third = root * 5 / 4
    fifth = root * 3 / 2
    
    # Bring third and fifth into comfortable range
    while third > 2 * C_BASE:
        third /= 2
    while fifth > 2 * C_BASE:
        fifth /= 2
    
    chord = (0.3 * np.sin(2 * np.pi * root * t) +
             0.2 * np.sin(2 * np.pi * third * t) +
             0.2 * np.sin(2 * np.pi * fifth * t) +
             0.08 * np.sin(2 * np.pi * root * 2 * t))  # octave doubling
    
    # Envelope
    attack = int(0.02 * SR)
    release = int(0.08 * SR)
    env = np.ones(n)
    env[:min(attack, n)] = np.linspace(0, 1, min(attack, n))
    env[-min(release, n):] = np.linspace(1, 0, min(release, n))
    
    output[start:end] += chord * env
    
    # Compute cents deviation from equal temperament
    if i < 12:
        # Equal temperament semitone position
        semitones = (i * 7) % 12  # Circle of fifths maps
        et_freq = C_BASE * (2 ** (semitones / 12))
    else:
        et_freq = C_BASE * 2  # Octave above
    
    cents_diff = 1200 * np.log2(root / et_freq) if et_freq > 0 else 0
    
    berry_data.append({
        'note': note,
        'frequency_just': round(root, 4),
        'frequency_et': round(et_freq, 4),
        'cents_deviation': round(cents_diff, 2),
    })
    
    print(f"  {note:4s}: {root:8.2f} Hz (ET: {et_freq:8.2f} Hz, Δ: {cents_diff:+.2f} cents)")

# Add final reference: pure ET C for comparison
ref_start = int(12 * CHORD_DUR * SR)
ref_end = int(13 * CHORD_DUR * SR)
n_ref = ref_end - ref_start
t_ref = np.arange(n_ref, dtype=np.float64) / SR
ref_c = C_BASE * 2  # ET octave

print(f"\n  Berry phase (final C vs initial C):")
print(f"  Initial C: {C_BASE:.2f} Hz")
print(f"  Final C (after 12 just-intonation fifths): {fifths_freq[-1]:.4f} Hz")
berry_phase_cents = 1200 * np.log2(fifths_freq[-1] / C_BASE)
print(f"  Discrepancy: {berry_phase_cents:.2f} cents (Pythagorean comma)")
print(f"  This IS the Berry phase — audible as ~quarter-tone sharpness!")

# Normalize
mx = np.abs(output).max()
if mx > 0:
    output = output / mx * 0.85

write_wav(OUT, output)

# Save analysis
json_path = os.path.join(os.path.dirname(__file__), "berry_phase_analysis.json")
with open(json_path, 'w') as f:
    json.dump({
        'berry_phase_cents': round(berry_phase_cents, 2),
        'initial_c_hz': C_BASE,
        'final_c_hz': round(fifths_freq[-1], 4),
        'pythagorean_comma_ratio': round(531441/524288, 6),
        'chords': berry_data
    }, f, indent=2)

print(f"\n✅ Written: {OUT}")
print(f"✅ Written: {json_path}")
print(f"   Berry phase: {berry_phase_cents:.2f} cents ≈ quarter-tone sharp")
