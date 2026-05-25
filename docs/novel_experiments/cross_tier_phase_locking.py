#!/usr/bin/env python3
"""
Experiment 3: Cross-Tier Phase Locking — Audible consolidation
- Fast oscillator (440 Hz) + slow oscillator (4.4 Hz with 100th harmonic)
- Coupling K sweeps 0→1 over 30 seconds
- Hear memory consolidation in real-time
- Output: 30s WAV
"""
import numpy as np
import struct, os

SR = 44100
DURATION = 30
OUT = os.path.join(os.path.dirname(__file__), "cross_tier_phase_locking.wav")

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

n_samples = int(SR * DURATION)
t = np.linspace(0, DURATION, n_samples, endpoint=False)

# Two coupled oscillators — Kuramoto-like model
# Fast tier (working memory): 440 Hz
# Slow tier (long-term memory): 4.4 Hz, with 100th harmonic at 440 Hz
f_fast = 440.0
f_slow = 4.4

dt = 1.0 / SR
phase_fast = np.zeros(n_samples)
phase_slow = np.zeros(n_samples)

# Initial phases
phase_fast[0] = 0.0
phase_slow[0] = 0.0

# Coupling sweeps from 0 to 1
for i in range(1, n_samples):
    K = i / n_samples  # 0 → 1 sweep
    
    # Phase difference (at the shared harmonic: slow's 100th = 440 Hz)
    # We track the effective phase diff between the two oscillators
    delta_phi = phase_fast[i-1] - 100 * phase_slow[i-1]
    
    # Kuramoto coupling: both feel the coupling
    # Fast oscillator adjusts toward slow's harmonic
    # Slow oscillator adjusts toward fast / 100
    
    coupling_fast = K * np.sin(delta_phi)
    coupling_slow = K * np.sin(delta_phi) * 0.01  # Much weaker influence on slow tier
    
    phase_fast[i] = phase_fast[i-1] + 2 * np.pi * f_fast * dt + coupling_fast * dt * 50
    phase_slow[i] = phase_slow[i-1] + 2 * np.pi * f_slow * dt + coupling_slow * dt

# Synthesize
# Fast tier: direct sine
fast_audio = np.sin(phase_fast) * 0.4

# Slow tier: fundamental + harmonics up to 100th
# We can't practically generate 100th harmonic directly, so we use
# the tracked phase to show the effect
slow_audio = np.sin(phase_slow) * 0.3  # 4.4 Hz fundamental (sub-audio, felt as pulsing)

# The 100th harmonic of slow — this is what couples to fast
slow_100th = np.sin(100 * phase_slow) * 0.3

# Combined: you hear fast oscillator gradually locking to slow oscillator's harmonic
# At K=0: beating between 440 Hz and 440 Hz → no beat (they start in sync)
# Actually let's make them start OUT of phase for dramatic effect
# Reset with initial phase offset
phase_fast[0] = 0.0
phase_slow[0] = np.pi / 50  # Offset so 100th harmonic starts π/2 out of phase

for i in range(1, n_samples):
    K = i / n_samples
    delta_phi = phase_fast[i-1] - 100 * phase_slow[i-1]
    coupling_fast = K * np.sin(delta_phi)
    coupling_slow = K * np.sin(delta_phi) * 0.01
    
    phase_fast[i] = phase_fast[i-1] + 2 * np.pi * f_fast * dt + coupling_fast * dt * 50
    phase_slow[i] = phase_slow[i-1] + 2 * np.pi * f_slow * dt + coupling_slow * dt

# Recompute audio with phase offset
fast_audio = np.sin(phase_fast) * 0.35
slow_audio = np.sin(phase_slow) * 0.15  # Low frequency pulsing
slow_harmonic = np.sin(100 * phase_slow) * 0.35  # The coupling harmonic

# The interference between fast_audio and slow_harmonic shows the locking
output = fast_audio + slow_harmonic + slow_audio

# Normalize
mx = np.abs(output).max()
if mx > 0:
    output = output / mx * 0.85

write_wav(OUT, output)
print(f"✅ Written: {OUT}")
print(f"   Duration: {DURATION}s")
print(f"   Fast tier: {f_fast} Hz (working memory)")
print(f"   Slow tier: {f_slow} Hz with 100th harmonic at {f_slow*100} Hz (long-term)")
print(f"   Coupling K sweeps 0 → 1")
print(f"   At start: beating between detuned oscillators")
print(f"   At end: phase-locked = 'consolidated'")
