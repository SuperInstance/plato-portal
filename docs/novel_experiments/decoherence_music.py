#!/usr/bin/env python3
"""
Experiment 4: Decoherence Music — Audible quantum forgetting
- Pure tone with harmonics 1-16
- Apply increasing phase noise (σ: 0→π over 60s)
- Lower harmonics decohere slowly (long-term memory), higher decohere fast (working memory)
- Output: 60s WAV
"""
import numpy as np
import struct, os

SR = 44100
DURATION = 60
OUT = os.path.join(os.path.dirname(__file__), "decoherence.wav")

def write_wav(path, samples, sr=SR):
    samples = np.clip(samples, -1.0, 1.0)
    data = (samples * 32767).astype(np.int16)
    with open(path, 'wb') as f:
        n = len(data)
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + n * 2))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(b'fmt ')
        f.write(struct.pack('<IHHIIHH', 16, 1, 1, sr, sr * 2, 2, 16))
        f.write(b'data')
        f.write(struct.pack('<I', n * 2))
        f.write(data.tobytes())

n_samples = int(SR * DURATION)
t = np.linspace(0, DURATION, n_samples, endpoint=False)

BASE_FREQ = 110.0  # A2 — rich, low fundamental
N_HARMONICS = 16

np.random.seed(77)

output = np.zeros(n_samples)

for h in range(1, N_HARMONICS + 1):
    freq = BASE_FREQ * h
    
    # Phase noise: σ increases over time from 0 to π
    # Higher harmonics decohere FASTER — their coherence rate is proportional to harmonic number
    # σ_h(t) = (t/T) * π * (h / N_HARMONICS)^0.5
    # So harmonic 1 gets σ_max = π * 0.25, harmonic 16 gets σ_max = π
    
    decoherence_rate = np.sqrt(h / N_HARMONICS)  # 0.25 to 1.0
    sigma = (t / DURATION) * np.pi * decoherence_rate
    
    # Generate phase noise as integrated random walk (smooth noise)
    # Use filtered noise for smooth phase perturbation
    noise_bandwidth = max(2, h)  # Higher harmonics get faster-varying noise
    raw_noise = np.random.randn(n_samples)
    
    # Simple low-pass filter via running average (using cumsum for speed)
    kernel_size = max(1, SR // noise_bandwidth)
    cs = np.cumsum(raw_noise)
    cs = np.insert(cs, 0, 0)
    smooth_noise = (cs[kernel_size:] - cs[:-kernel_size]) / kernel_size
    # Pad to same length
    smooth_noise = np.pad(smooth_noise, (0, n_samples - len(smooth_noise)), mode='edge')
    
    # Normalize noise to unit variance, then scale by sigma
    smooth_noise /= (np.std(smooth_noise) + 1e-10)
    phase_noise = smooth_noise * sigma
    
    # Synthesize harmonic with phase noise
    clean_phase = 2 * np.pi * freq * t
    noisy_phase = clean_phase + phase_noise
    
    # Amplitude decreases with harmonic number (natural rolloff)
    amp = 0.3 / h
    
    # Coherence envelope: amplitude of coherent component decreases
    # as decoherence increases (phase noise reduces coherent energy)
    coherence = np.exp(-0.5 * sigma**2)  # Gaussian coherence decay
    
    # Coherent part (in phase)
    coherent = amp * np.sin(clean_phase) * coherence
    
    # Decoherent part (noisy phase) — energy is preserved but scattered
    decoherent = amp * np.sin(noisy_phase) * (1 - coherence) * 0.5
    
    output += coherent + decoherent

# Normalize
mx = np.abs(output).max()
if mx > 0:
    output = output / mx * 0.85

write_wav(OUT, output)
print(f"✅ Written: {OUT}")
print(f"   Duration: {DURATION}s, Fundamental: {BASE_FREQ} Hz")
print(f"   Harmonics 1-{N_HARMONICS}")
print(f"   Lower harmonics (long-term memory) stay coherent longer")
print(f"   Higher harmonics (working memory) decohere first")
