#!/usr/bin/env python3
"""
Quality DSP Effects Demo
========================
Generates a C major chord (C4+E4+G4) at 44100 Hz for 2 seconds,
processes it through every preset, saves WAVs, and reports metrics.
"""

import numpy as np
import os
import sys

# Ensure local import works
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from quality_effects import QualityEffectChain, write_wav


def generate_c_major_chord(sr=44100, duration=2.0):
    """Generate a C major chord: C4 (261.63 Hz) + E4 (329.63 Hz) + G4 (392.00 Hz)."""
    t = np.arange(int(sr * duration), dtype=np.float64) / sr
    freqs = [261.63, 329.63, 392.00]
    signal = np.zeros_like(t)
    for f in freqs:
        signal += np.sin(2 * np.pi * f * t)
    # Normalize
    signal = signal / np.max(np.abs(signal)) * 0.8
    # Fade in/out
    fade = int(0.02 * sr)
    signal[:fade] *= np.linspace(0, 1, fade)
    signal[-fade:] *= np.linspace(1, 0, fade)
    return signal


def compute_metrics(audio, sr=44100):
    """Compute peak amplitude, RMS, spectral centroid, and THD+N."""
    # If stereo, use left channel for metrics
    if audio.ndim == 2:
        audio = audio[:, 0]

    peak = np.max(np.abs(audio))
    rms = np.sqrt(np.mean(audio ** 2))

    # Spectral centroid
    N = len(audio)
    fft = np.abs(np.fft.rfft(audio))
    freqs = np.fft.rfftfreq(N, 1.0 / sr)
    mag_sum = np.sum(fft)
    if mag_sum > 0:
        centroid = np.sum(freqs * fft) / mag_sum
    else:
        centroid = 0.0

    # THD+N: ratio of everything except fundamental to total power
    # Find fundamental peak
    peak_bin = np.argmax(fft[1:]) + 1  # skip DC
    fund_freq = freqs[peak_bin]
    fund_power = fft[peak_bin] ** 2

    # Total power
    total_power = np.sum(fft[1:] ** 2)  # exclude DC

    if total_power > 0:
        thdn = np.sqrt(max(0, total_power - fund_power) / total_power) * 100
    else:
        thdn = 0.0

    return {
        'peak': peak,
        'rms': rms,
        'spectral_centroid': centroid,
        'thdn_percent': thdn,
    }


def main():
    print("🎵 Quality DSP Effects Demo")
    print("=" * 60)

    sr = 44100
    chain = QualityEffectChain(sr=sr)
    signal = generate_c_major_chord(sr=sr, duration=2.0)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
    os.makedirs(out_dir, exist_ok=True)

    # Define demo presets in order
    demo_presets = [
        ('clean', None),  # no processing
        ('cuda_f32', 'cuda_f32'),
        ('fortran_o2', 'fortran_o2'),
        ('c_ffast_math', 'c_ffast_math'),
        ('rust_release', 'rust_release'),
        ('analog_tape', 'analog_tape'),
        ('vinyl_crackle', 'vinyl_crackle'),
        ('chip_8bit', 'chip_8bit'),
        ('broken_dac', 'broken_dac'),
        ('gpu_thermal', 'gpu_thermal'),
        ('mainframe_fortran', 'mainframe_fortran'),
        ('teen_engine', 'teen_engine'),
    ]

    all_presets = chain.get_presets()

    print(f"\n{'Preset':<25} {'Peak':>8} {'RMS':>8} {'Centroid':>10} {'THD+N%':>8}")
    print("-" * 65)

    metrics_report = []

    for idx, (name, preset_key) in enumerate(demo_presets):
        if preset_key is None:
            result = signal.copy()
            label = "clean (no effects)"
        elif preset_key in all_presets:
            result = all_presets[preset_key](signal)
            label = preset_key
        else:
            print(f"  ⚠ Preset '{preset_key}' not found, skipping")
            continue

        fname = f"{idx:02d}_{name}.wav"
        fpath = os.path.join(out_dir, fname)
        write_wav(fpath, result, sr)

        m = compute_metrics(result, sr)
        metrics_report.append((name, m))

        channels = "stereo" if result.ndim == 2 else "mono"
        print(f"  {name:<23} {m['peak']:>8.4f} {m['rms']:>8.4f} {m['spectral_centroid']:>10.1f} {m['thdn_percent']:>8.2f}  ({channels})")

    print("-" * 65)
    print(f"\n✅ Generated {len(demo_presets)} WAV files in {out_dir}/")

    # Detailed report
    print("\n📊 Detailed Metrics Report")
    print("=" * 60)
    for name, m in metrics_report:
        print(f"\n  {name}:")
        print(f"    Peak amplitude:   {m['peak']:.6f}")
        print(f"    RMS level:        {m['rms']:.6f}")
        print(f"    Spectral centroid: {m['spectral_centroid']:.1f} Hz")
        print(f"    THD+N:            {m['thdn_percent']:.2f}%")


if __name__ == '__main__':
    main()
