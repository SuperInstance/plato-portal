#!/usr/bin/env python3
"""
Constraint-Theory Audio Demo via DawDreamer

Demonstrates mapping constraint-substrate parameters to audio:
  - Lattice Snap → frequency quantization (pentatonic scale)
  - Funnel → gain envelope (attack/sustain/release)
  - Holonomy → modulation depth (LFO on gain)

Output: examples/constraint_demo.wav

Requirements: pip install dawdreamer numpy
"""

import dawdreamer as daw
import numpy as np
import os
import wave


# ── Constraint Parameter Builders ──────────────────────────────

def lattice_snap_curve(scale_freqs, min_val, max_val, pulses, ascending=True):
    """
    Lattice snap: quantize a continuous sweep to discrete scale degrees.
    Maps constraint lattice structure to frequency (or any quantized parameter).
    """
    t = np.linspace(0, 1, pulses)
    if ascending:
        raw = np.linspace(min_val, max_val, pulses)
    else:
        raw = min_val + (max_val - min_val) * (0.5 + 0.5 * np.sin(2 * np.pi * t))

    snapped = np.array([scale_freqs[np.argmin(np.abs(np.array(scale_freqs) - f))] for f in raw])
    return np.clip((snapped - min_val) / (max_val - min_val), 0, 1)


def funnel_envelope(pulses, attack_frac=0.05, release_frac=0.15, sustain_level=0.6):
    """
    Funnel: shapes energy flow over time. Maps to gain/volume envelope.
    Attack ramps up, sustain holds, release ramps down.
    """
    env = np.ones(pulses) * sustain_level
    attack = int(pulses * attack_frac)
    release = int(pulses * release_frac)
    env[:attack] = np.linspace(0, sustain_level, attack)
    env[-release:] = np.linspace(sustain_level, 0, release)
    return env


def holonomy_modulation(pulses, rate=8, depth=0.1):
    """
    Holonomy: topological winding creates periodic modulation patterns.
    Maps to LFO depth, vibrato, tremolo, or any cyclic parameter.
    """
    t = np.linspace(0, 1, pulses)
    return depth * np.sin(2 * np.pi * rate * t)


# ── Render Pipeline ────────────────────────────────────────────

def render_constraint_audio(output_path="examples/constraint_demo.wav",
                            duration=8.0, bpm=120, sample_rate=44100):
    """Render constraint-theory parameterized audio via DawDreamer Faust synth."""

    engine = daw.RenderEngine(sample_rate, 512)
    engine.set_bpm(bpm)

    # Faust synth: two oscillators with filter
    synth = engine.make_faust_processor('constraint_synth')
    synth.set_dsp_string('''
        freq = hslider("freq", 440, 100, 2000, 1);
        gain = hslider("gain", 0.5, 0, 1, 0.01);
        detune = hslider("detune", 0, -50, 50, 0.1);
        osc1 = os.osc(freq);
        osc2 = os.osc(freq + detune);
        mixed = (osc1 + osc2) * 0.5;
        process = mixed * gain;
    ''')

    # Get parameter names (DawDreamer uses full path names)
    params = synth.get_parameters_description()
    freq_name = [p['name'] for p in params if p['label'] == 'freq'][0]
    gain_name = [p['name'] for p in params if p['label'] == 'gain'][0]
    detune_name = [p['name'] for p in params if p['label'] == 'detune'][0]

    # Calculate PPQN resolution
    ppqn = 960
    beats = int(duration * bpm / 60)
    pulses = beats * ppqn

    # Build constraint parameter curves
    pentatonic = [261.63, 293.66, 329.63, 392.00, 440.00,
                  523.25, 587.33, 659.25, 783.99, 880.00]

    freq_auto = lattice_snap_curve(pentatonic, 100, 2000, pulses, ascending=True)
    gain_auto = funnel_envelope(pulses, attack_frac=0.05, release_frac=0.15, sustain_level=0.6)
    gain_auto += holonomy_modulation(pulses, rate=8, depth=0.1)
    gain_auto = np.clip(gain_auto, 0, 1)
    detune_auto = holonomy_modulation(pulses, rate=4, depth=0.5) + 0.5  # normalized

    # Apply automation
    synth.set_automation(freq_name, freq_auto, ppqn=ppqn)
    synth.set_automation(gain_name, gain_auto, ppqn=ppqn)
    synth.set_automation(detune_name, detune_auto, ppqn=ppqn)

    # Render
    engine.load_graph([(synth, [])])
    engine.render(duration)
    audio = engine.get_audio()

    # Save WAV
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    audio_int = (audio[0] * 32767).astype(np.int16)
    with wave.open(output_path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_int.tobytes())

    print(f"✅ Rendered {duration}s to {output_path} ({os.path.getsize(output_path)} bytes)")
    return output_path


if __name__ == '__main__':
    render_constraint_audio()
