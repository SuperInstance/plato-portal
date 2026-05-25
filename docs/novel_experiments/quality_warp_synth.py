#!/usr/bin/env python3
"""
Experiment 5: Quality Warp Synth — Language quality during synthesis
- I-IV-V-I chord progression
- Synthesize with different precision: f64 (clean), f32 (warm), f16 (lo-fi), int8 (crunchy)
- Measure spectral differences between precision levels
- Output: 4 WAVs + quality comparison JSON
"""
import numpy as np
import struct, os, json

SR = 44100
DURATION = 8  # 2s per chord × 4 chords
OUT_DIR = os.path.dirname(__file__)

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

# Chord progression I-IV-V-I in C major
CHORDS = {
    'I':  [261.63, 329.63, 392.00],   # C E G
    'IV': [261.63, 349.23, 440.00],   # C F A
    'V':  [196.00, 329.63, 392.00],   # G B(?) actually G B D... let me fix
    'I2': [261.63, 329.63, 392.00],   # C E G
}
# Fix V chord: G B D
CHORDS['V'] = [196.00, 246.94, 293.66]  # G3 B3 D4

def generate_chord_progression(dtype_float=True):
    """Generate chord progression at specified precision."""
    n_samples = int(SR * DURATION)
    audio = np.zeros(n_samples, dtype=np.float64)
    
    chord_dur = DURATION / 4
    for ci, (name, freqs) in enumerate(CHORDS.items()):
        start = int(ci * chord_dur * SR)
        end = int((ci + 1) * chord_dur * SR)
        n = end - start
        t = np.arange(n, dtype=np.float64) / SR
        
        chord_audio = np.zeros(n, dtype=np.float64)
        for freq in freqs:
            # Rich tone with harmonics
            tone = (0.3 * np.sin(2 * np.pi * freq * t) +
                    0.1 * np.sin(2 * np.pi * freq * 2 * t) +
                    0.05 * np.sin(2 * np.pi * freq * 3 * t))
            # Envelope
            env = np.ones(n)
            attack = int(0.02 * SR)
            release = int(0.05 * SR)
            env[:attack] = np.linspace(0, 1, attack)
            env[-release:] = np.linspace(1, 0, release)
            chord_audio += tone * env
        
        audio[start:end] = chord_audio
    
    return audio

def quantize_f32(audio):
    """Simulate float32 precision."""
    return audio.astype(np.float32).astype(np.float64)

def quantize_f16(audio):
    """Simulate float16 precision."""
    return audio.astype(np.float16).astype(np.float64)

def quantize_int8(audio):
    """Simulate int8 precision."""
    # Scale to [-127, 127]
    scaled = audio * 127.0
    quantized = np.round(scaled).astype(np.int8)
    return quantized.astype(np.float64) / 127.0

def compute_spectrum(audio, sr=SR):
    spectrum = np.abs(np.fft.rfft(audio))
    freqs = np.fft.rfftfreq(len(audio), 1/sr)
    return freqs, spectrum

def spectral_diff(spec_a, spec_b):
    """Normalized spectral difference."""
    diff = np.abs(spec_a - spec_b)
    return float(np.mean(diff) / (np.mean(spec_a) + 1e-10))

# Generate reference (f64)
reference = generate_chord_progression()

# Generate at different precisions
versions = {
    'f64': reference.copy(),
    'f32': quantize_f32(reference),
    'f16': quantize_f16(reference),
    'int8': quantize_int8(reference),
}

# Write WAVs and measure
freqs_ref, spec_ref = compute_spectrum(reference)
results = {}

for name, audio in versions.items():
    wav_path = os.path.join(OUT_DIR, f"quality_warp_{name}.wav")
    write_wav(wav_path, audio)
    
    freqs, spec = compute_spectrum(audio)
    diff = spectral_diff(spec_ref, spec)
    
    # Compute SNR relative to reference
    noise = audio - reference
    signal_power = np.mean(reference**2)
    noise_power = np.mean(noise**2)
    snr = 10 * np.log10(signal_power / (noise_power + 1e-20))
    
    # Dynamic range
    dr = 20 * np.log10(np.max(np.abs(audio) + 1e-20) / (np.min(np.abs(audio[audio != 0]) + 1e-20)))
    
    results[name] = {
        'spectral_diff_vs_f64': round(diff, 6),
        'snr_db': round(snr, 2),
        'dynamic_range_db': round(dr, 2),
        'file': f"quality_warp_{name}.wav",
    }
    
    print(f"  {name}: spectral_diff={diff:.6f}, SNR={snr:.1f}dB, DR={dr:.1f}dB")

# Save JSON
json_path = os.path.join(OUT_DIR, "quality_comparison.json")
with open(json_path, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n✅ Written: 4 WAVs + quality_comparison.json")
for name, r in results.items():
    print(f"   {name}: {r['file']} (SNR: {r['snr_db']}dB)")
