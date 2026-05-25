#!/usr/bin/env python3
"""
Experiment 2: Forgetting Curve Music — Music that forgets itself
- 2-min melody in C major, each note has "importance" = consonance score
- Notes decay via Ebbinghaus R = e^(-t/(S*importance))
- Tonic (importance=1.0) persists, tritone (0.3) vanishes fast
- Output: 2-min WAV
"""
import numpy as np
import struct, os

SR = 44100
DURATION = 120
OUT = os.path.join(os.path.dirname(__file__), "forgetting_curve.wav")

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

# C major scale degrees and their consonance (importance) scores
# Based on interval from root: tonic=1.0, octave=1.0, fifth=0.95, etc.
CONSONANCE = {
    'C4': 1.0, 'D4': 0.7, 'E4': 0.85, 'F4': 0.75, 
    'G4': 0.95, 'A4': 0.65, 'B4': 0.5, 'C5': 1.0,
    'F#4': 0.3,  # tritone — forgets fastest
}

FREQ_MAP = {
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
    'G4': 392.00, 'A4': 440.00, 'B4': 493.88, 'C5': 523.25,
    'F#4': 369.99,
}

# Generate a melody — each note is an "engram" that will decay
np.random.seed(12)
melody_notes = ['C4', 'E4', 'G4', 'C5', 'A4', 'F4', 'D4', 'B4', 
                'C4', 'F#4', 'G4', 'E4', 'C4', 'A4', 'F#4', 'C5',
                'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5',
                'G4', 'E4', 'C4', 'F#4', 'D4', 'B4', 'C4', 'C4']

NOTE_DUR = DURATION / len(melody_notes)  # ~3.75s each
S = 15.0  # Stability constant — controls how fast things decay

n_samples = int(SR * DURATION)
output = np.zeros(n_samples)

# Each note persists from its onset with Ebbinghaus decay
for i, note_name in enumerate(melody_notes):
    freq = FREQ_MAP[note_name]
    importance = CONSONANCE[note_name]
    onset = int(i * NOTE_DUR * SR)
    
    # Generate sustained tone that decays per Ebbinghaus
    remaining = n_samples - onset
    t = np.arange(remaining) / SR
    t_from_onset = t  # time since this note started
    
    # Ebbinghaus retention: R = e^(-t / (S * importance))
    retention = np.exp(-t_from_onset / (S * importance))
    
    # Synthesize: sine + slight harmonics
    tone = (0.4 * np.sin(2 * np.pi * freq * t) +
            0.15 * np.sin(2 * np.pi * freq * 2 * t) +
            0.08 * np.sin(2 * np.pi * freq * 3 * t))
    
    # Apply forgetting curve as amplitude envelope
    tone *= retention
    
    # Smooth onset (10ms)
    attack = min(int(0.01 * SR), len(tone))
    tone[:attack] *= np.linspace(0, 1, attack)
    
    output[onset:onset + len(tone)] += tone

# Add a persistent "tonic drone" (C4) that barely decays — it's deeply encoded
t_total = np.arange(n_samples) / SR
tonic_retention = np.exp(-t_total / (S * 1.0))  # importance=1.0, decays slowest
tonic = 0.08 * np.sin(2 * np.pi * 261.63 * t_total) * tonic_retention
output += tonic

# Normalize
mx = np.abs(output).max()
if mx > 0:
    output = output / mx * 0.85

write_wav(OUT, output)
print(f"✅ Written: {OUT}")
print(f"   Duration: {DURATION}s ({DURATION//60}m {DURATION%60}s)")
print(f"   Notes: {len(melody_notes)}, S={S}")
print(f"   Tonic (C) persists longest, tritone (F#) vanishes fastest")
