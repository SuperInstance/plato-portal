#!/usr/bin/env python3
"""
Experiment 1: Memory Reverb
- Store recent audio, extract spectral patterns every 2s into short-term memory
- Consolidate short-term into long-term (cluster similar spectra)
- Reverb generates echoes from MEMORY not delay — "recalled" patterns
- Output: 30s WAV
"""
import numpy as np
import struct, json, os
from collections import defaultdict

SR = 44100
DURATION = 30
OUT = os.path.join(os.path.dirname(__file__), "memory_reverb.wav")

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

def extract_spectrum(audio, sr=SR, n_fft=2048):
    """Extract simplified spectral fingerprint."""
    window = np.hanning(len(audio))
    windowed = audio * window
    spectrum = np.abs(np.fft.rfft(windowed, n=n_fft))
    # Bin into 32 bands
    band_size = len(spectrum) // 32
    bands = np.array([np.mean(spectrum[i*band_size:(i+1)*band_size]) for i in range(32)])
    mx = bands.max()
    if mx > 0:
        bands /= mx
    return bands

def spectrum_to_audio(bands, duration=0.5, sr=SR):
    """Synthesize audio from spectral bands."""
    n_samples = int(sr * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    freqs = np.linspace(100, 4000, 32)
    audio = np.zeros(n_samples)
    for i, (freq, amp) in enumerate(zip(freqs, bands)):
        if amp > 0.05:
            audio += amp * np.sin(2 * np.pi * freq * t) * np.exp(-3 * t / duration)
    mx = np.abs(audio).max()
    if mx > 0:
        audio /= mx
    return audio * 0.3

# Phase 1: Generate source material — evolving drone with harmonic changes
def generate_source(duration, sr=SR):
    n = int(sr * duration)
    t = np.linspace(0, duration, n, endpoint=False)
    audio = np.zeros(n)
    base_freqs = [130.81, 196.0, 261.63, 329.63, 392.0]  # C3, G3, C4, E4, G4
    for i, freq in enumerate(base_freqs):
        # Slowly modulate amplitude
        mod = 0.5 + 0.5 * np.sin(2 * np.pi * (0.05 + i * 0.02) * t)
        audio += mod * 0.15 * np.sin(2 * np.pi * freq * t)
    # Add noise texture
    audio += 0.02 * np.random.randn(n)
    return audio

source = generate_source(DURATION)

# Phase 2: Extract spectral memories every 2 seconds
CHUNK = SR * 2
short_term = []
for i in range(0, len(source) - CHUNK, CHUNK):
    chunk = source[i:i + CHUNK]
    spectrum = extract_spectrum(chunk)
    short_term.append({'spectrum': spectrum, 'time': i / SR})

print(f"Extracted {len(short_term)} spectral snapshots")

# Phase 3: Consolidate — cluster similar spectra into long-term memory
def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)

# Simple greedy clustering
clusters = []
used = [False] * len(short_term)
THRESHOLD = 0.7

for i, stm in enumerate(short_term):
    if used[i]:
        continue
    cluster = [i]
    used[i] = True
    centroid = stm['spectrum'].copy()
    for j in range(i + 1, len(short_term)):
        if used[j]:
            continue
        sim = cosine_sim(centroid, short_term[j]['spectrum'])
        if sim > THRESHOLD:
            cluster.append(j)
            used[j] = True
            centroid = np.mean([short_term[k]['spectrum'] for k in cluster], axis=0)
    clusters.append({'centroid': centroid, 'members': cluster, 'weight': len(cluster)})

print(f"Consolidated into {len(clusters)} long-term memory clusters")
for c in clusters:
    print(f"  Cluster: {len(c['members'])} members, weight={c['weight']}")

# Phase 4: Synthesize output with MEMORY-BASED reverb
output = source.copy()

# Generate "recalled" echoes from consolidated memories at random intervals
np.random.seed(42)
n_recall_events = 60

for event in range(n_recall_events):
    # Pick a memory cluster (weighted by cluster size = strength)
    weights = np.array([c['weight'] for c in clusters])
    weights = weights / weights.sum()
    cluster_idx = np.random.choice(len(clusters), p=weights)
    cluster = clusters[cluster_idx]
    
    # When to recall (spread across the piece)
    recall_time = np.random.uniform(2, DURATION - 3)
    recall_pos = int(recall_time * SR)
    
    # Generate audio from this memory
    recall_audio = spectrum_to_audio(cluster['centroid'], duration=np.random.uniform(0.3, 1.0))
    
    # Fade it in
    fade = np.linspace(0, 1, min(len(recall_audio), int(0.05 * SR)))
    recall_audio[:len(fade)] *= fade
    
    # Add to output
    end = min(recall_pos + len(recall_audio), len(output))
    length = end - recall_pos
    output[recall_pos:end] += recall_audio[:length] * 0.2

# Normalize
mx = np.abs(output).max()
if mx > 0:
    output = output / mx * 0.85

write_wav(OUT, output)
print(f"\n✅ Written: {OUT}")
print(f"   Duration: {DURATION}s, SR: {SR}Hz")
