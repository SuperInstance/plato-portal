#!/usr/bin/env python3
"""
Experiment 4: Time-Reversal Experiment
=======================================
If the Innovation Cycle is real, we can PREDICT what music would sound like
if modern dial positions were applied to earlier eras' instruments/techniques.

Synthesizes anachronistic hybrids: Baroque hip-hop, Classical AI,
Renaissance electronic, etc. Tests universality of the dial space.
"""

import json
import numpy as np
import wave
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

SAMPLE_RATE = 44100
DURATION = 5.0

# ── Tradition / era dial positions ───────────────────────────────────────────

ERAS = {
    "renaissance":      {"dials": [0.45, 0.55, 0.30], "instruments": "lute_voice_organ",
                         "period": "1400-1600"},
    "baroque":          {"dials": [0.72, 0.60, 0.40], "instruments": "harpsichord_strings_organ",
                         "period": "1600-1750"},
    "classical":        {"dials": [0.68, 0.65, 0.42], "instruments": "strings_woodwinds_piano",
                         "period": "1750-1820"},
    "romantic":         {"dials": [0.70, 0.62, 0.48], "instruments": "full_orchestra",
                         "period": "1820-1900"},
    "modernist":        {"dials": [0.45, 0.50, 0.55], "instruments": "extended_techniques",
                         "period": "1900-1950"},
}

MODERN_STYLES = {
    "hip_hop":          {"dials": [0.40, 0.85, 0.65], "features": "strong_rhythm_bass_samples"},
    "electronic":       {"dials": [0.50, 0.80, 0.90], "features": "synthesized_repetitive_drops"},
    "ai_generated":     {"dials": [0.60, 0.55, 0.85], "features": "maximal_spectral_blend"},
    "ambient":          {"dials": [0.55, 0.25, 0.70], "features": "slow_textural_drone"},
    "math_rock":        {"dials": [0.45, 0.90, 0.50], "features": "complex_time_signatures"},
}


# ── Audio synthesis with era-specific character ──────────────────────────────

def generate_wav(filepath, samples, sr=SAMPLE_RATE):
    samples = np.clip(samples, -1.0, 1.0)
    pcm = (samples * 32767).astype(np.int16)
    with wave.open(str(filepath), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())


def era_waveform(t, freq, era_instrument, rng):
    """Generate era-appropriate waveform character."""
    phase = 2 * np.pi * freq * t

    if "harpsichord" in era_instrument:
        # Plucked string: bright, fast decay
        sig = np.sin(phase) + 0.5 * np.sin(2 * phase) + 0.3 * np.sin(3 * phase)
        return sig / 1.8

    elif "lute" in era_instrument:
        # Warm plucked: softer harmonics
        sig = np.sin(phase) + 0.25 * np.sin(2 * phase)
        return sig / 1.25

    elif "organ" in era_instrument:
        # Sustained, additive synthesis
        sig = np.sin(phase)
        for h in range(2, 8):
            sig += (0.5 / h) * np.sin(h * phase)
        return sig / 2.5

    elif "strings" in era_instrument:
        # Bowed: sawtooth-ish but warm
        sig = np.zeros_like(t)
        for h in range(1, 10):
            sig += ((-1) ** (h + 1)) * np.sin(h * phase) / h
        return sig * (2 / np.pi) * 0.7

    elif "orchestra" in era_instrument:
        # Rich: multiple timbres
        sig = np.sin(phase) + 0.4 * np.sin(2 * phase) + 0.2 * np.sin(3 * phase)
        sig += 0.15 * np.sin(4 * phase)
        return sig / 1.75

    elif "extended" in era_instrument:
        # Modernist: some inharmonic content
        sig = np.sin(phase) + 0.3 * np.sin(2.01 * phase)  # Slight detuning
        sig += 0.2 * np.sin(3.14 * phase)  # Near-pi = very dissonant
        return sig / 1.5

    else:
        return np.sin(phase)


def synthesize_anachronism(era_key, modern_key, seed=0):
    """
    Synthesize a time-reversed hybrid: modern dial positions applied to
    an earlier era's instrumental character.
    
    The dials come from the modern style, but the timbre/voice production
    comes from the historical era.
    """
    rng = np.random.default_rng(seed)
    era = ERAS[era_key]
    modern = MODERN_STYLES[modern_key]

    # Use MODERN dials for structure, ERA instruments for timbre
    dials = np.array(modern["dials"])
    era_instrument = era["instruments"]
    i_vert, i_horiz, i_spectral = np.clip(dials, 0, 1)

    total_samples = int(SAMPLE_RATE * DURATION)
    audio = np.zeros(total_samples)

    # Number of voices from vertical complexity
    n_voices = max(2, int(2 + i_vert * 6))

    # Base frequency chosen to feel appropriate for the era
    base_freqs = {
        "renaissance": 220,
        "baroque": 261,
        "classical": 293,
        "romantic": 246,
        "modernist": 277,
    }
    base_freq = base_freqs.get(era_key, 261)

    # Generate voice frequencies
    if i_vert > 0.5:
        # Consonant intervals
        intervals = [0, 3, 5, 7, 12, 15, 17]
        freqs = [base_freq * 2 ** (intervals[i % len(intervals)] / 12)
                 for i in range(n_voices)]
    else:
        freqs = [base_freq * 2 ** (rng.uniform(-5, 12) / 12)
                 for _ in range(n_voices)]

    # Rhythmic structure from horizontal dial
    bpm = 60 + i_horiz * 120  # 60-180 BPM
    beat_period = 60.0 / bpm
    n_beats = int(DURATION / beat_period) + 1

    # Spectral richness
    n_harmonics = max(1, int(1 + i_spectral * 8))

    for beat in range(n_beats):
        # Timing jitter inversely proportional to I_horiz
        jitter = rng.normal(0, (1.0 - i_horiz) * 0.1) * beat_period
        t_start = beat * beat_period + jitter

        s0 = int(t_start * SAMPLE_RATE)
        if s0 >= total_samples:
            break

        dur = beat_period * rng.uniform(0.4, 1.2)
        s1 = min(int((t_start + dur) * SAMPLE_RATE), total_samples)
        n_samp = s1 - s0
        if n_samp <= 0:
            continue

        t = np.arange(n_samp) / SAMPLE_RATE
        note_audio = np.zeros(n_samp)

        for v in range(min(n_voices, 6)):  # Cap voices to avoid clipping
            amp = rng.uniform(0.03, 0.10)
            freq = freqs[v % len(freqs)]
            # Use era-appropriate waveform
            base_sig = era_waveform(t, freq, era_instrument, rng)
            note_audio += amp * base_sig

        # Envelope: era-appropriate
        attack = min(800, n_samp // 4)
        release = min(800, n_samp // 4)

        if "harpsichord" in era_instrument or "lute" in era_instrument:
            # Plucked: fast attack, medium decay
            attack = min(100, n_samp // 8)
            release = min(int(n_samp * 0.6), n_samp // 2)
        elif "organ" in era_instrument:
            # Sustained: medium attack, sudden release
            attack = min(200, n_samp // 6)
            release = min(100, n_samp // 10)
        elif "strings" in era_instrument or "orchestra" in era_instrument:
            # Bowed: slow attack, medium release
            attack = min(500, n_samp // 3)
            release = min(400, n_samp // 4)

        env = np.ones(n_samp)
        if attack > 0:
            env[:attack] = np.linspace(0, 1, attack)
        if release > 0:
            env[-release:] = np.linspace(1, 0, release)

        audio[s0:s1] += note_audio * env

    # Add subtle room reverb (simple delay-based)
    delay_samples = int(0.08 * SAMPLE_RATE)
    reverb = np.zeros_like(audio)
    for d in range(1, 5):
        decay = 0.3 / d
        shifted = np.roll(audio, delay_samples * d)
        shifted[:delay_samples * d] = 0
        reverb += decay * shifted
    audio = audio + 0.2 * reverb

    peak = np.max(np.abs(audio))
    if peak > 0:
        audio /= peak
    return audio


def score_plausibility(dials, era_key, modern_key):
    """
    Score how plausible an anachronistic combination is.
    Tests whether the dial position would produce "beyond random"
    structure regardless of era.
    """
    surplus = np.sum(dials) - 1.5  # Random baseline

    # Era compatibility: how far are the dials from the era's natural position?
    era_dials = np.array(ERAS[era_key]["dials"])
    modern_dials = np.array(MODERN_STYLES[modern_key]["dials"])

    distance_from_era = np.linalg.norm(dials - era_dials)
    distance_from_modern = np.linalg.norm(dials - modern_dials)

    # A "plausible" anachronism would still be beyond random
    # but might have interesting tensions
    plausibility = surplus - 0.2 * distance_from_era

    return {
        "structure_surplus": float(surplus),
        "beyond_random": surplus > 0,
        "distance_from_era": float(distance_from_era),
        "distance_from_modern": float(distance_from_modern),
        "plausibility": float(plausibility),
        "tension": float(distance_from_era * distance_from_modern),  # Interesting if both are big
    }


def run_experiment():
    print("Time-Reversal Experiment: Anachronistic Musical Hybrids")
    print(f"{'='*60}")

    # Define the specific anachronisms from the spec
    anachronisms = [
        # (era, modern_style, description)
        ("baroque", "hip_hop", "Baroque Hip-Hop — Bach counterpoint + hip-hop rhythm"),
        ("classical", "ai_generated", "Classical AI — Mozartean melody + AI spectral maximalism"),
        ("renaissance", "electronic", "Renaissance Electronic — Josquin + synthesized timbres"),
        ("romantic", "ambient", "Romantic Ambient — Full orchestra + ambient textures"),
        ("baroque", "math_rock", "Baroque Math Rock — Harpsichord + complex time signatures"),
        ("classical", "electronic", "Classical Electronic — Strings + drops"),
        ("renaissance", "hip_hop", "Renaissance Hip-Hop — Lute + beats"),
        ("modernist", "ambient", "Modernist Ambient — Extended techniques + drones"),
    ]

    results = []
    wav_files = {}

    for idx, (era_key, modern_key, description) in enumerate(anachronisms):
        print(f"\n{idx+1}. {description}")
        print(f"   Era: {era_key} | Modern: {modern_key}")

        modern_dials = np.array(MODERN_STYLES[modern_key]["dials"])
        scores = score_plausibility(modern_dials, era_key, modern_key)

        print(f"   Dials: vert={modern_dials[0]:.2f}, horiz={modern_dials[1]:.2f}, "
              f"spectral={modern_dials[2]:.2f}")
        print(f"   Structure surplus: {scores['structure_surplus']:.3f} "
              f"({'beyond random' if scores['beyond_random'] else 'below random'})")
        print(f"   Distance from era: {scores['distance_from_era']:.3f}")
        print(f"   Tension: {scores['tension']:.3f}")

        # Synthesize
        audio = synthesize_anachronism(era_key, modern_key, seed=500 + idx)
        filename = f"anachronism_{idx+1:02d}_{era_key}_{modern_key}.wav"
        generate_wav(OUTPUT_DIR / filename, audio)
        wav_files[f"anachronism_{idx+1}"] = str(OUTPUT_DIR / filename)
        print(f"   → {filename}")

        results.append({
            "rank": idx + 1,
            "era": era_key,
            "era_period": ERAS[era_key]["period"],
            "modern_style": modern_key,
            "description": description,
            "dials": modern_dials.tolist(),
            "scores": scores,
            "wav": str(OUTPUT_DIR / filename),
        })

    # Analysis
    print(f"\n{'='*60}")
    print("TIME-REVERSAL ANALYSIS")
    print(f"{'='*60}")

    beyond_random_count = sum(1 for r in results if r["scores"]["beyond_random"])
    print(f"Beyond random: {beyond_random_count}/{len(results)}")

    highest_tension = max(results, key=lambda x: x["scores"]["tension"])
    print(f"Highest tension: {highest_tension['description']} "
          f"(tension={highest_tension['scores']['tension']:.3f})")

    highest_plausibility = max(results, key=lambda x: x["scores"]["plausibility"])
    print(f"Most plausible: {highest_plausibility['description']} "
          f"(plausibility={highest_plausibility['scores']['plausibility']:.3f})")

    # Additional analysis: what would happen if we reversed the cycle?
    print(f"\nReversing the Innovation Cycle:")
    print(f"  If the dial is universal, anachronistic positions should still")
    print(f"  produce 'beyond random' structure regardless of era.")
    print(f"  Result: {beyond_random_count}/{len(results)} pass the test")

    if beyond_random_count == len(results):
        print(f"  → STRONG evidence for dial universality")
    elif beyond_random_count > len(results) // 2:
        print(f"  → MODERATE evidence — most positions work across eras")
    else:
        print(f"  → WEAK evidence — dial positions may be era-dependent")

    # Generate one bonus: "what if AI existed in 1600?"
    print(f"\nBonus: AI in the Renaissance...")
    all_modern_dials = np.array(MODERN_STYLES["ai_generated"]["dials"])
    bonus_audio = synthesize_anachronism("renaissance", "ai_generated", seed=999)
    generate_wav(OUTPUT_DIR / "anachronism_bonus_renaissance_ai.wav", bonus_audio)
    wav_files["bonus_renaissance_ai"] = str(OUTPUT_DIR / "anachronism_bonus_renaissance_ai.wav")

    # Save data
    data = {
        "experiment": "time_reversal",
        "eras": {k: v for k, v in ERAS.items()},
        "modern_styles": {k: v for k, v in MODERN_STYLES.items()},
        "results": results,
        "analysis": {
            "beyond_random_count": beyond_random_count,
            "total_anachronisms": len(results),
            "highest_tension": {
                "description": highest_tension["description"],
                "tension": highest_tension["scores"]["tension"],
            },
            "highest_plausibility": {
                "description": highest_plausibility["description"],
                "plausibility": highest_plausibility["scores"]["plausibility"],
            },
            "dial_universality_verdict": (
                "strong" if beyond_random_count == len(results)
                else "moderate" if beyond_random_count > len(results) // 2
                else "weak"
            ),
        },
        "wav_files": wav_files,
    }

    with open(OUTPUT_DIR / "reversal_data.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"\nSaved reversal_data.json")

    return data


if __name__ == "__main__":
    run_experiment()
