#!/usr/bin/env python3
"""
Experiment 3: Cross-Tradition Hybridization
=============================================
Take pairs of traditions and create musical hybrids by interpolating their
dial positions. Test all 45 pairs at 25%, 50%, 75% interpolation.
"""

import json
import numpy as np
import wave
from pathlib import Path
from itertools import combinations

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

SAMPLE_RATE = 44100
DURATION = 4.0

# ── Tradition dial positions ─────────────────────────────────────────────────

TRADITIONS = {
    "western_classical": np.array([0.72, 0.68, 0.55]),
    "jazz":              np.array([0.65, 0.74, 0.60]),
    "gamelan":           np.array([0.40, 0.58, 0.70]),
    "carnatic":          np.array([0.62, 0.70, 0.50]),
    "blues":             np.array([0.55, 0.72, 0.45]),
    "gagaku":            np.array([0.35, 0.40, 0.75]),
    "arabic_maqam":      np.array([0.58, 0.65, 0.52]),
    "flamenco":          np.array([0.52, 0.78, 0.48]),
    "throat_singing":    np.array([0.30, 0.35, 0.82]),
    "minimalism":        np.array([0.75, 0.30, 0.25]),
}

TRADITION_NAMES = list(TRADITIONS.keys())
TRADITION_POSITIONS = np.array(list(TRADITIONS.values()))


# ── Audio synthesis ──────────────────────────────────────────────────────────

def generate_wav(filepath, samples, sr=SAMPLE_RATE):
    samples = np.clip(samples, -1.0, 1.0)
    pcm = (samples * 32767).astype(np.int16)
    with wave.open(str(filepath), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())


def synthesize_from_dials(dials, seed=0):
    """Synthesize audio from interpolated dial positions."""
    rng = np.random.default_rng(seed)
    i_vert, i_horiz, i_spectral = np.clip(dials, 0, 1)
    total_samples = int(SAMPLE_RATE * DURATION)
    audio = np.zeros(total_samples)

    n_voices = max(2, int(2 + i_vert * 5))
    base_freq = rng.uniform(180, 350)

    if i_vert > 0.5:
        consonant_intervals = [0, 3, 5, 7, 12, 15, 17, 19]
        freqs = [base_freq * 2 ** (consonant_intervals[i % len(consonant_intervals)] / 12)
                 for i in range(n_voices)]
    else:
        freqs = [base_freq * 2 ** (rng.uniform(-6, 18) / 12) for _ in range(n_voices)]

    beat_period = rng.uniform(0.2, 0.5)
    n_beats = int(DURATION / beat_period) + 1

    for beat in range(n_beats):
        jitter = rng.normal(0, (1.0 - i_horiz) * 0.15) * beat_period
        t_start = beat * beat_period + jitter

        s0 = int(t_start * SAMPLE_RATE)
        if s0 >= total_samples:
            break

        dur = beat_period * rng.uniform(0.3, 1.0) * (0.5 + 0.5 * i_horiz)
        s1 = min(int((t_start + dur) * SAMPLE_RATE), total_samples)
        n_samp = s1 - s0
        if n_samp <= 0:
            continue

        t = np.arange(n_samp) / SAMPLE_RATE
        note_audio = np.zeros(n_samp)

        for v in range(n_voices):
            amp = rng.uniform(0.05, 0.15) / n_voices
            freq = freqs[v]
            phase = 2 * np.pi * freq * t

            sig = amp * np.sin(phase)
            n_harmonics = max(1, int(1 + i_spectral * 8))
            for h in range(2, n_harmonics + 1):
                sig += (amp / h ** 1.5) * np.sin(h * phase + rng.uniform(0, 2 * np.pi))

            note_audio += sig

        attack = min(300, n_samp // 4)
        release = min(300, n_samp // 4)
        env = np.ones(n_samp)
        if attack > 0:
            env[:attack] = np.linspace(0, 1, attack)
        if release > 0:
            env[-release:] = np.linspace(1, 0, release)

        audio[s0:s1] += note_audio * env

    peak = np.max(np.abs(audio))
    if peak > 0:
        audio /= peak
    return audio


def score_consonance(dials):
    """Score consonance of dial position — higher = more structured."""
    surplus = np.sum(dials) - 1.5  # Above random baseline
    # Consonance favors balanced, high dials
    balance = 1.0 - np.std(dials)  # Uniform across axes = balanced
    return float(surplus + 0.3 * balance)


# ── Hybridization ────────────────────────────────────────────────────────────

def interpolate_dials(trad1_pos, trad2_pos, alpha):
    """Interpolate between two traditions: alpha=0 → trad1, alpha=1 → trad2."""
    return (1 - alpha) * trad1_pos + alpha * trad2_pos


def run_experiment():
    print("Cross-Tradition Hybridization Experiment")
    print(f"{'='*60}")

    pairs = list(combinations(TRADITION_NAMES, 2))
    print(f"Testing {len(pairs)} tradition pairs at 3 interpolation points each = "
          f"{len(pairs) * 3} hybrids")

    all_hybrids = []
    interpolation_points = [0.25, 0.50, 0.75]

    for i, (t1_name, t2_name) in enumerate(pairs):
        t1_pos = TRADITIONS[t1_name]
        t2_pos = TRADITIONS[t2_name]

        pair_data = {
            "tradition_1": t1_name,
            "tradition_2": t2_name,
            "interpolations": {},
        }

        for alpha in interpolation_points:
            hybrid_pos = interpolate_dials(t1_pos, t2_pos, alpha)
            consonance = score_consonance(hybrid_pos)

            # Distance to nearest tradition (other than the parents)
            other_traditions = [
                (name, pos) for name, pos in TRADITIONS.items()
                if name not in (t1_name, t2_name)
            ]
            dists = [(name, float(np.linalg.norm(hybrid_pos - pos)))
                     for name, pos in other_traditions]
            nearest_other = min(dists, key=lambda x: x[1])

            # Distance to nearest unexplored region center
            # (points far from ALL traditions)
            all_dists = [float(np.linalg.norm(hybrid_pos - pos)) for pos in TRADITION_POSITIONS]
            min_dist_to_any = min(all_dists)

            pair_data["interpolations"][str(alpha)] = {
                "dials": {"vert": float(hybrid_pos[0]),
                          "horiz": float(hybrid_pos[1]),
                          "spectral": float(hybrid_pos[2])},
                "consonance": consonance,
                "nearest_other_tradition": nearest_other[0],
                "distance_to_nearest_other": nearest_other[1],
                "min_distance_to_any_tradition": min_dist_to_any,
            }

            all_hybrids.append({
                "pair": f"{t1_name}_x_{t2_name}",
                "alpha": alpha,
                "dials": hybrid_pos.tolist(),
                "consonance": consonance,
                "min_distance": min_dist_to_any,
            })

        if (i + 1) % 10 == 0:
            print(f"  ... {i+1}/{len(pairs)} pairs processed")

    # Analysis
    print(f"\n{'='*60}")
    print("HYBRID ANALYSIS")
    print(f"{'='*60}")

    # Sort by consonance
    by_consonance = sorted(all_hybrids, key=lambda x: x["consonance"], reverse=True)
    by_dissonance = sorted(all_hybrids, key=lambda x: x["consonance"])
    by_unexplored = sorted(all_hybrids, key=lambda x: x["min_distance"], reverse=True)

    # Most consonant hybrid
    most_consonant = by_consonance[0]
    print(f"\nMost consonant hybrid: {most_consonant['pair']} @ {most_consonant['alpha']}")
    print(f"  Dials: ({most_consonant['dials'][0]:.3f}, "
          f"{most_consonant['dials'][1]:.3f}, {most_consonant['dials'][2]:.3f})")
    print(f"  Consonance: {most_consonant['consonance']:.4f}")

    # Most dissonant hybrid
    most_dissonant = by_dissonance[0]
    print(f"\nMost dissonant hybrid: {most_dissonant['pair']} @ {most_dissonant['alpha']}")
    print(f"  Dials: ({most_dissonant['dials'][0]:.3f}, "
          f"{most_dissonant['dials'][1]:.3f}, {most_dissonant['dials'][2]:.3f})")
    print(f"  Consonance: {most_dissonant['consonance']:.4f}")

    # Hybrid closest to unexplored regions
    most_unexplored = by_unexplored[0]
    print(f"\nHybrid closest to unexplored: {most_unexplored['pair']} @ {most_unexplored['alpha']}")
    print(f"  Dials: ({most_unexplored['dials'][0]:.3f}, "
          f"{most_unexplored['dials'][1]:.3f}, {most_unexplored['dials'][2]:.3f})")
    print(f"  Min distance to tradition: {most_unexplored['min_distance']:.4f}")

    # Check: any hybrids more consonant than BOTH parents?
    parent_beaters = []
    for h in all_hybrids:
        pair_names = h["pair"].split("_x_")
        t1, t2 = pair_names[0], pair_names[1]
        parent_consonances = [
            score_consonance(TRADITIONS[t1]),
            score_consonance(TRADITIONS[t2]),
        ]
        if h["consonance"] > max(parent_consonances):
            parent_beaters.append(h)

    print(f"\nHybrids that beat both parents: {len(parent_beaters)}/{len(all_hybrids)}")
    if parent_beaters:
        best_beater = max(parent_beaters, key=lambda x: x["consonance"])
        print(f"  Best: {best_beater['pair']} @ {best_beater['alpha']} "
              f"(consonance={best_beater['consonance']:.4f})")

    # Synthesize top 10 hybrids
    print("\nSynthesizing top 10 hybrid WAV files...")
    wav_files = {}

    # Mix of interesting hybrids: top 5 consonant + top 5 novel
    interesting = []
    seen_keys = set()
    
    # Top 5 consonant
    for h in by_consonance[:5]:
        key = f"{h['pair']}_{h['alpha']}"
        if key not in seen_keys:
            interesting.append(("consonant", h))
            seen_keys.add(key)

    # Top 5 novel
    for h in by_unexplored[:5]:
        key = f"{h['pair']}_{h['alpha']}"
        if key not in seen_keys:
            interesting.append(("novel", h))
            seen_keys.add(key)

    # If we don't have 10, add parent beaters
    if len(interesting) < 10:
        for h in parent_beaters[:5]:
            key = f"{h['pair']}_{h['alpha']}"
            if key not in seen_keys:
                interesting.append(("beater", h))
                seen_keys.add(key)

    interesting = interesting[:10]

    for idx, (label, h) in enumerate(interesting):
        dials = np.array(h["dials"])
        audio = synthesize_from_dials(dials, seed=200 + idx)
        filename = f"hybrid_{idx+1:02d}_{h['pair']}_{int(h['alpha']*100)}pct.wav"
        # Clean filename
        filename = filename.replace(" ", "_")
        generate_wav(OUTPUT_DIR / filename, audio)
        wav_files[f"hybrid_{idx+1}"] = {
            "file": str(OUTPUT_DIR / filename),
            "label": label,
            "pair": h["pair"],
            "alpha": h["alpha"],
            "consonance": h["consonance"],
        }
        print(f"  {idx+1}. [{label}] {h['pair']} @ {h['alpha']*100:.0f}% "
              f"→ consonance={h['consonance']:.4f}")

    # Also synthesize specific interesting crosses mentioned in the spec
    special_crosses = [
        ("carnatic", "gagaku", 0.5, "carnatic_x_gagaku"),
        ("western_classical", "jazz", 0.5, "classical_x_jazz"),
        ("blues", "throat_singing", 0.5, "blues_x_throat"),
    ]

    for t1, t2, alpha, name in special_crosses:
        if t1 in TRADITIONS and t2 in TRADITIONS:
            hybrid = interpolate_dials(TRADITIONS[t1], TRADITIONS[t2], alpha)
            audio = synthesize_from_dials(hybrid, seed=300 + hash(name) % 1000)
            filename = f"hybrid_special_{name}.wav"
            generate_wav(OUTPUT_DIR / filename, audio)
            wav_files[f"special_{name}"] = str(OUTPUT_DIR / filename)

    # Save data
    data = {
        "experiment": "hybridization",
        "n_pairs": len(pairs),
        "n_hybrids_total": len(all_hybrids),
        "traditions": {k: v.tolist() for k, v in TRADITIONS.items()},
        "most_consonant": {
            "pair": most_consonant["pair"],
            "alpha": most_consonant["alpha"],
            "dials": most_consonant["dials"],
            "consonance": most_consonant["consonance"],
        },
        "most_dissonant": {
            "pair": most_dissonant["pair"],
            "alpha": most_dissonant["alpha"],
            "dials": most_dissonant["dials"],
            "consonance": most_dissonant["consonance"],
        },
        "most_unexplored": {
            "pair": most_unexplored["pair"],
            "alpha": most_unexplored["alpha"],
            "dials": most_unexplored["dials"],
            "min_distance": most_unexplored["min_distance"],
        },
        "parent_beaters": {
            "count": len(parent_beaters),
            "best": {
                "pair": parent_beaters[0]["pair"],
                "alpha": parent_beaters[0]["alpha"],
                "consonance": parent_beaters[0]["consonance"],
            } if parent_beaters else None,
        },
        "all_hybrids": all_hybrids,
        "wav_files": wav_files,
    }

    with open(OUTPUT_DIR / "hybrid_data.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"\nSaved hybrid_data.json")

    return data


if __name__ == "__main__":
    run_experiment()
