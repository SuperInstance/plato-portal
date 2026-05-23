#!/usr/bin/env python3
"""
Better Preset — Pushing the constraint-synth to its actual limits.

The synth has ONE real synthesis trick: additive harmonics via lattice_stretch.
Let's use that, plus layered oscillators and careful envelope design, to make
something that actually sounds pleasant.

Strategy:
- Layer multiple oscillators (fundamental + harmonics) by mixing render passes
- Use triangle wave (richest built-in waveform that isn't harsh)
- Use slow attack for pad sounds (the envelope is the best part of this synth)
- Apply the consonance filter as a genuine lowpass (it removes non-harmonic content)
- Add vibrato via frequency modulation of the oscillator parameter
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'constraint-synth'))

from constraint_synth import ConstraintSynth, LatticeOscillator, FunnelEnvelope, ConsonanceFilter

SAMPLE_RATE = 44100


def layered_pad(chord_notes, duration=4.0):
    """
    Create a lush pad by layering triangle+sine oscillators for each chord tone,
    with slow envelopes and heavy filtering.
    """
    layers = []
    
    for i, pitch in enumerate(chord_notes):
        # Main tone: triangle (warmest built-in waveform)
        synth_tri = ConstraintSynth(
            LatticeOscillator(lattice_shape="triangle", frequency=1),  # freq overridden
            FunnelEnvelope(attack=0.8, decay=0.3, sustain=0.6, release=1.5),
            ConsonanceFilter(cutoff=0.3, resonance=0.8),
        )
        
        # Sub sine: pure fundamental for body
        synth_sub = ConstraintSynth(
            LatticeOscillator(lattice_shape="sine", frequency=1),
            FunnelEnvelope(attack=1.0, decay=0.2, sustain=0.5, release=1.8),
        )
        
        # Generate each layer
        vel = 60 + (i * 5)  # slight velocity variation
        tri = synth_tri.play_note(pitch, vel, duration)
        sub = synth_sub.play_note(pitch - 12, vel // 2, duration)  # octave below, quieter
        
        layers.append(tri * 0.6)
        layers.append(sub * 0.3)
    
    # Mix all layers
    max_len = max(len(l) for l in layers)
    mix = np.zeros(max_len)
    for layer in layers:
        padded = np.zeros(max_len)
        padded[:len(layer)] = layer
        mix += padded
    
    return mix


def evolving_tone(fundamental_pitch=60, duration=8.0):
    """
    Create an evolving tone by stitching together short segments with
    slightly different parameters — simulating slow parameter sweeps.
    """
    segments = []
    segment_dur = 0.5
    n_segments = int(duration / segment_dur)
    
    for i in range(n_segments):
        # Slowly evolve the lattice_stretch and cutoff
        t_frac = i / n_segments
        stretch = 1.0 + 0.003 * np.sin(2 * np.pi * t_frac * 2)  # subtle detune wobble
        cutoff = 0.2 + 0.3 * np.sin(2 * np.pi * t_frac)  # filter sweep
        
        synth = ConstraintSynth(
            LatticeOscillator(
                lattice_shape="triangle",
                lattice_stretch=stretch,
            ),
            FunnelEnvelope(attack=0.01, decay=0.05, sustain=0.8, release=0.1),
            ConsonanceFilter(cutoff=cutoff, resonance=1.2),
        )
        
        seg = synth.play_note(fundamental_pitch, 80, segment_dur + 0.15)  # overlap for smoothness
        segments.append(seg)
    
    # Crossfade segments
    overlap_samples = int(0.1 * SAMPLE_RATE)
    result = segments[0]
    for seg in segments[1:]:
        # Simple crossfade in overlap region
        fade_out = np.linspace(1, 0, overlap_samples)
        fade_in = np.linspace(0, 1, overlap_samples)
        result[-overlap_samples:] = result[-overlap_samples:] * fade_out + seg[:overlap_samples] * fade_in
        result = np.concatenate([result, seg[overlap_samples:]])
    
    return result


def ambient_progression():
    """
    A slowly evolving ambient chord progression — the kind of thing
    that actually works with this synth's strengths (sine/triangle + slow envelopes).
    
    Progression: Cmaj7 → Am7 → Fmaj7 → Gsus4
    """
    chords = [
        [60, 64, 67, 71],   # Cmaj7
        [57, 60, 64, 67],   # Am7
        [53, 57, 60, 64],   # Fmaj7
        [55, 59, 62, 67],   # Gsus4
    ]
    
    all_audio = np.array([])
    
    for chord in chords:
        pad = layered_pad(chord, duration=3.5)
        # Crossfade between chords
        if len(all_audio) > 0:
            cf_len = int(1.0 * SAMPLE_RATE)  # 1 second crossfade
            cf_len = min(cf_len, len(all_audio), len(pad))
            fade_out = np.linspace(1, 0, cf_len)
            fade_in = np.linspace(0, 1, cf_len)
            all_audio[-cf_len:] = all_audio[-cf_len:] * fade_out + pad[:cf_len] * fade_in
            all_audio = np.concatenate([all_audio, pad[cf_len:]])
        else:
            all_audio = pad
    
    return all_audio


def shimmer_bell(melody_notes, duration_per=1.5):
    """
    Bell-like tones using eisenstein lattice (6-level quantization = ringy)
    with very short attack and long release.
    """
    layers = []
    for pitch, vel in melody_notes:
        synth = ConstraintSynth(
            LatticeOscillator(lattice_shape="eisenstein", snap_threshold=0.7,
                            lattice_stretch=1.003),  # slight inharmonicity = bell-like
            FunnelEnvelope(attack=0.001, decay=0.1, sustain=0.1, release=1.2),
            ConsonanceFilter(cutoff=0.5, resonance=1.5),
        )
        tone = synth.play_note(pitch, vel, duration_per)
        
        # Add a pure sine octave up for shimmer
        synth2 = ConstraintSynth(
            LatticeOscillator(lattice_shape="sine"),
            FunnelEnvelope(attack=0.001, decay=0.05, sustain=0.05, release=0.8),
        )
        shimmer = synth2.play_note(pitch + 12, vel // 3, duration_per)
        
        # Pad to same length
        max_len = max(len(tone), len(shimmer))
        padded = np.zeros(max_len)
        padded[:len(tone)] += tone * 0.7
        padded[:len(shimmer)] += shimmer * 0.3
        layers.append(padded)
    
    # Stack with timing offsets (arpeggio feel)
    total_len = sum(len(l) for l in layers) + len(layers) * int(0.3 * SAMPLE_RATE)
    mix = np.zeros(total_len)
    pos = 0
    for layer in layers:
        end = pos + len(layer)
        if end <= total_len:
            mix[pos:end] += layer
        pos += len(layer) + int(0.3 * SAMPLE_RATE)
    
    return mix[:pos]


def main():
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'better_preset_output')
    os.makedirs(output_dir, exist_ok=True)
    
    print("🎛️  Better Preset Generator — pushing constraint-synth to its limits\n")
    
    # 1. Ambient chord progression (the synth's strongest use case)
    print("  Rendering ambient progression...")
    audio = ambient_progression()
    # Normalize
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak * 0.8
    path = os.path.join(output_dir, "ambient_progression.wav")
    ConstraintSynth.to_wav(audio, path)
    print(f"    ✓ ambient_progression.wav ({len(audio)/SAMPLE_RATE:.1f}s)")
    
    # 2. Evolving tone (filter sweep)
    print("  Rendering evolving tone...")
    audio = evolving_tone(60, 8.0)
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak * 0.8
    path = os.path.join(output_dir, "evolving_tone.wav")
    ConstraintSynth.to_wav(audio, path)
    print(f"    ✓ evolving_tone.wav ({len(audio)/SAMPLE_RATE:.1f}s)")
    
    # 3. Shimmer bell melody
    print("  Rendering shimmer bells...")
    melody = [(72, 80), (76, 70), (79, 75), (84, 65), (79, 70), (76, 80), (72, 85)]
    audio = shimmer_bell(melody, duration_per=2.0)
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak * 0.8
    path = os.path.join(output_dir, "shimmer_bells.wav")
    ConstraintSynth.to_wav(audio, path)
    print(f"    ✓ shimmer_bells.wav ({len(audio)/SAMPLE_RATE:.1f}s)")
    
    # 4. Full arrangement: ambient pad + bells
    print("  Rendering combined arrangement...")
    pad = ambient_progression()
    bells = shimmer_bell([(72, 50), (76, 45), (79, 50), (84, 40)], duration_per=3.0)
    
    # Pad bells to length of pad
    combined = pad.copy()
    if len(bells) < len(combined):
        combined[:len(bells)] += bells * 0.4
    else:
        combined += bells[:len(combined)] * 0.4
    
    peak = np.max(np.abs(combined))
    if peak > 0:
        combined = combined / peak * 0.8
    path = os.path.join(output_dir, "combined_arrangement.wav")
    ConstraintSynth.to_wav(combined, path)
    print(f"    ✓ combined_arrangement.wav ({len(combined)/SAMPLE_RATE:.1f}s)")
    
    print(f"\n✅ All rendered to {output_dir}/")


if __name__ == "__main__":
    main()
