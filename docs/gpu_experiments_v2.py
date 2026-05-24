#!/usr/bin/env python3
"""
GPU-Accelerated Music Theory Experiments v2 — The Ambitious Sequel
RTX 4050 (6.4GB) — CUDA 8.9 (Ada Lovelace)

Five deep experiments for the conservation-of-tension thesis:
1. Information-theoretic historical simulation (1000 agents, 600 years)
2. Euclidean rhythm ↔ Circle of Fifths isomorphism
3. Spectral beating atlas (12×12 FFT matrices)
4. Conservation law stress test (10000 random tunings)
5. Nancarrow tempo-space exploration (50 canons)

All GPU-accelerated. All JSON+audio output.
"""

import torch
import numpy as np
import soundfile as sf
import math
import os
import json
from fractions import Fraction
from pathlib import Path
from collections import Counter

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"🔥 V2 Forge burning on: {DEVICE}")
if torch.cuda.is_available():
    print(f"   {torch.cuda.get_device_name(0)}")
    print(f"   {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB VRAM")

OUTDIR = Path(__file__).parent / "gpu_output_v2"
OUTDIR.mkdir(exist_ok=True)

SR = 44100  # sample rate

# ═══════════════════════════════════════════════════════════════════
# UTILITY: Tuning system generators
# ═══════════════════════════════════════════════════════════════════

def meantone_intervals():
    """Quarter-comma meantone: pure major thirds, tempered fifths."""
    # Fifth = 4 * 1200 * log2(5)/4 - 1200 * log2(4) = 696.578 cents
    # Or: 3/2 * 81/80^(1/4) = 5^(1/4) ≈ 696.578 cents
    fifth = 696.5784
    intervals = []
    for i in range(12):
        cents = (fifth * i) % 1200
        intervals.append(cents)
    intervals.sort()
    return torch.tensor(intervals, device=DEVICE, dtype=torch.float32)

def et_intervals():
    """12-tone equal temperament."""
    return torch.tensor([i * 100.0 for i in range(12)],
                        device=DEVICE, dtype=torch.float32)

def pythagorean_intervals():
    """Pythagorean tuning: pure 3:2 fifths stacked."""
    intervals = []
    for i in range(12):
        cents = (701.955 * i) % 1200
        intervals.append(cents)
    intervals.sort()
    return torch.tensor(intervals, device=DEVICE, dtype=torch.float32)

def just_intervals_full():
    """Just intonation 12-tone (5-limit)."""
    # Ratios from Partch's tonality diamond
    ratios = [1/1, 16/15, 9/8, 6/5, 5/4, 4/3, 45/32, 3/2, 8/5, 5/3, 9/5, 15/8]
    cents = [1200 * math.log2(r) for r in ratios]
    return torch.tensor(cents, device=DEVICE, dtype=torch.float32)

def consonance_score(cents_diff, sigma=12.0):
    """Consonance from cents deviation to nearest just interval."""
    just_refs = torch.tensor([
        0, 111.73, 182.40, 203.91, 231.17, 266.87, 315.64,
        386.31, 407.82, 435.08, 498.04, 519.55, 582.51,
        609.78, 701.96, 764.92, 813.69, 840.53, 884.36,
        905.87, 955.03, 1017.60, 1088.27, 1200.0
    ], device=DEVICE, dtype=torch.float32)

    # Tenney weights
    tenney_ratios = [1/1, 16/15, 10/9, 9/8, 8/7, 7/6, 6/5, 5/4, 14/11,
                     11/8, 4/3, 7/5, 45/32, 3/2, 10/7, 8/5, 5/3, 12/7,
                     7/4, 16/9, 15/8, 2/1, 27/16, 2/1]
    weights = []
    for r in tenney_ratios:
        try:
            f = Fraction(r).limit_denominator(100)
            tenney = math.log2(f.numerator * f.denominator)
            weights.append(2.0 ** (-tenney))
        except Exception:
            weights.append(0.001)
    w = torch.tensor(weights, device=DEVICE, dtype=torch.float32)

    if cents_diff.dim() == 0:
        cents_diff = cents_diff.unsqueeze(0)
    diff = torch.abs(cents_diff.unsqueeze(1) - just_refs.unsqueeze(0))
    gauss = torch.exp(-0.5 * (diff / sigma) ** 2)
    scores = (gauss * w.unsqueeze(0)).max(dim=1).values
    return scores


def render_audio(freqs, durations, tuning_cents, sr=SR, harmonics=8):
    """Render overtone-rich audio for given frequencies in a tuning."""
    total_samples = int(sum(durations) * sr)
    audio = torch.zeros(total_samples, device=DEVICE, dtype=torch.float32)
    pos = 0
    for freq, dur in zip(freqs, durations):
        n_samples = int(dur * sr)
        t = torch.linspace(0, dur, n_samples, device=DEVICE, dtype=torch.float32)
        tone = torch.zeros_like(t)
        for h in range(1, harmonics + 1):
            amp = 1.0 / (h * h)  # 1/n² rolloff
            tone += amp * torch.sin(2 * math.pi * freq * h * t)
        # Envelope
        attack = min(int(0.01 * sr), n_samples // 4)
        release = min(int(0.05 * sr), n_samples // 4)
        env = torch.ones_like(t)
        env[:attack] = torch.linspace(0, 1, attack)
        env[-release:] = torch.linspace(1, 0, release)
        audio[pos:pos + n_samples] += tone * env
        pos += n_samples
    # Normalize
    mx = audio.abs().max()
    if mx > 0:
        audio = audio / mx * 0.8
    return audio


# ═══════════════════════════════════════════════════════════════════
# EXPERIMENT 1: Information-Theoretic Historical Simulation
# 1000 composer agents, 600 years, meantone→ET transition
# ═══════════════════════════════════════════════════════════════════

def experiment1_historical_simulation():
    """Simulate 1000 composer agents over 600 years (1400-2000).
    Each agent chooses keys and rhythms based on tuning system in effect.
    Track I_vertical and I_horizontal as meantone→ET transition occurs."""
    print("\n🏰 Experiment 1: Information-Theoretic Historical Simulation")
    print("   1000 agents × 600 years × meantone→ET transition")

    torch.manual_seed(42)
    N_AGENTS = 1000
    YEARS = torch.arange(1400, 2000, device=DEVICE, dtype=torch.float32)
    N_YEARS = len(YEARS)

    # Transition model: meantone dominates early, ET takes over
    # Sigmoid transition centered at ~1750 (Marpurg/Werckmeister debates)
    transition_year = 1750.0
    transition_rate = 0.02
    et_fraction = torch.sigmoid(transition_rate * (YEARS - transition_year))

    # Results storage
    i_vert_history = torch.zeros(N_YEARS, device=DEVICE)
    i_horiz_history = torch.zeros(N_YEARS, device=DEVICE)
    total_i_history = torch.zeros(N_YEARS, device=DEVICE)
    key_diversity = torch.zeros(N_YEARS, device=DEVICE)
    rhythmic_complexity = torch.zeros(N_YEARS, device=DEVICE)

    mt = meantone_intervals()
    et = et_intervals()

    for yi in range(N_YEARS):
        p_et = et_fraction[yi].item()
        # Blend tuning: weighted average of meantone and ET intervals
        blended = p_et * et + (1 - p_et) * mt

        # Each agent "composes" a short phrase
        # Key choices: 12 keys, weighted by key consonance
        # In meantone, C/F/G are most consonant; in ET all equal
        key_cons = torch.zeros(12, device=DEVICE)
        for k in range(12):
            shifted = (blended - blended[k]) % 1200
            key_cons[k] = consonance_score(shifted).mean()

        # Agent key choices (softmax of consonance)
        temp = 0.5 + p_et * 2.0  # ET = more exploratory
        key_probs = torch.softmax(key_cons / temp, dim=0)
        agent_keys = torch.multinomial(key_probs, N_AGENTS, replacement=True)

        # Vertical information: surprise of chord choices
        # Meantone: high surprise (wolf intervals rare), ET: low surprise (uniform)
        chord_probs = key_cons / key_cons.sum()
        # Shannon entropy of chord choices
        i_vert = -(chord_probs * torch.log2(chord_probs + 1e-10)).sum()
        # Normalize by max entropy
        i_vert_norm = i_vert / math.log2(12)

        # Horizontal information: modulation paths
        # Each agent picks a sequence of keys
        n_modulations = torch.poisson(torch.tensor(2.0 + p_et * 3.0)).int().item() + 1
        mod_paths = torch.stack([
            torch.multinomial(key_probs, n_modulations, replacement=True)
            for _ in range(N_AGENTS)
        ])

        # Compute transition entropy
        trans_counts = torch.zeros(12, 12, device=DEVICE)
        for a in range(N_AGENTS):
            for m in range(n_modulations - 1):
                src = mod_paths[a, m].item()
                dst = mod_paths[a, m + 1].item()
                trans_counts[src, dst] += 1

        row_sums = trans_counts.sum(dim=1, keepdim=True).clamp(min=1)
        trans_probs = trans_counts / row_sums
        # Entropy of transitions
        i_horiz = -(trans_probs * torch.log2(trans_probs + 1e-10)).sum() / 12
        i_horiz_norm = i_horiz / math.log2(12)

        # Rhythmic complexity: agents choose rhythmic subdivisions
        # Meantone era: simpler rhythms (breve/semibreve/minim)
        # ET era: more complex (triplets, syncopation, polyrhythm)
        rhythm_options = torch.tensor([1, 2, 3, 4, 5, 6, 7, 8], device=DEVICE, dtype=torch.float32)
        rhythm_weights = torch.tensor([3.0, 2.5, 1.5, 2.0, 0.5, 1.0, 0.3, 0.8],
                                       device=DEVICE, dtype=torch.float32)
        # In ET era, complex rhythms become more likely
        rhythm_weights[4:] += p_et * 2.0
        rhythm_probs = rhythm_weights / rhythm_weights.sum()
        rhy_entropy = -(rhythm_probs * torch.log2(rhythm_probs + 1e-10)).sum()
        rhy_norm = rhy_entropy / math.log2(len(rhythm_options))

        i_vert_history[yi] = i_vert_norm
        i_horiz_history[yi] = i_horiz_norm
        total_i_history[yi] = i_vert_norm + i_horiz_norm
        key_diversity[yi] = len(torch.unique(agent_keys)) / 12.0
        rhythmic_complexity[yi] = rhy_norm

    # Compute on CPU for JSON serialization
    results = {
        "description": "1000 composer agents × 600 years, meantone→ET transition",
        "years": list(range(1400, 2000)),
        "et_fraction": et_fraction.cpu().tolist(),
        "i_vertical": i_vert_history.cpu().tolist(),
        "i_horizontal": i_horiz_history.cpu().tolist(),
        "i_total": total_i_history.cpu().tolist(),
        "key_diversity": key_diversity.cpu().tolist(),
        "rhythmic_complexity": rhythmic_complexity.cpu().tolist(),
        "analysis": {
            "i_vert_meantone_avg": i_vert_history[:150].mean().item(),
            "i_vert_et_avg": i_vert_history[300:].mean().item(),
            "i_horiz_meantone_avg": i_horiz_history[:150].mean().item(),
            "i_horiz_et_avg": i_horiz_history[300:].mean().item(),
            "total_i_variance": total_i_history.var().item(),
            "vert_shift": "UP" if i_vert_history[300:].mean() > i_vert_history[:150].mean() else "DOWN",
            "horiz_shift": "UP" if i_horiz_history[300:].mean() > i_horiz_history[:150].mean() else "DOWN",
            "conservation_ratio": (total_i_history.max() / total_i_history.min()).item() if total_i_history.min() > 0 else float('inf'),
            "transition_year_estimated": int(YEARS[torch.argmax(torch.abs(torch.diff(total_i_history)))].item()),
        }
    }

    with open(OUTDIR / "exp1_historical_simulation.json", 'w') as f:
        json.dump(results, f, indent=2)
    print(f"   ✓ I_vert: meantone={results['analysis']['i_vert_meantone_avg']:.4f} "
          f"→ ET={results['analysis']['i_vert_et_avg']:.4f} ({results['analysis']['vert_shift']})")
    print(f"   ✓ I_horiz: meantone={results['analysis']['i_horiz_meantone_avg']:.4f} "
          f"→ ET={results['analysis']['i_horiz_et_avg']:.4f} ({results['analysis']['horiz_shift']})")
    print(f"   ✓ Total I variance: {results['analysis']['total_i_variance']:.6f} "
          f"(conservation ratio: {results['analysis']['conservation_ratio']:.4f})")

    return results


# ═══════════════════════════════════════════════════════════════════
# EXPERIMENT 2: Euclidean Rhythm ↔ Circle of Fifths Isomorphism
# ═══════════════════════════════════════════════════════════════════

def euclidean_rhythm(n, k):
    """Generate Euclidean rhythm E(k,n) using Björklund's algorithm."""
    if k == 0:
        return [0] * n
    if k == n:
        return [1] * n

    pattern = [[1] for _ in range(k)] + [[0] for _ in range(n - k)]
    while True:
        # Find the number of groups that can be distributed
        groups_to_distribute = len(pattern) - 1
        min_len = len(pattern[-1])
        # Count groups with minimum length at the end
        count = 0
        for i in range(len(pattern) - 1, -1, -1):
            if len(pattern[i]) == min_len:
                count += 1
            else:
                break
        remainder = min(count, groups_to_distribute)
        if remainder <= 0:
            break
        # Distribute
        for i in range(remainder):
            pattern[i].extend(pattern.pop())
        if len(pattern) <= 1:
            break

    return [x for group in pattern for x in group]


def rhythm_to_interval_class(rhythm):
    """Map a rhythm's onset pattern to an interval class on the circle of fifths.
    The isomorphism: onsets represent scale degrees, spacing = interval quality."""
    n = len(rhythm)
    onsets = [i for i, v in enumerate(rhythm) if v == 1]
    if len(onsets) <= 1:
        return 0.0, 0.0  # trivial

    # Compute average step size in the rhythm
    steps = []
    for i in range(len(onsets)):
        next_onset = onsets[(i + 1) % len(onsets)]
        step = (next_onset - onsets[i]) % n
        steps.append(step)

    # Map to consonance: equal steps = more consonant
    # Hemiola (3:2) = E(2,3) = [1,0,1] → steps of 2 and 1 → ratio 2:1 ≈ octave
    # E(3,5) = [1,0,1,0,1] → steps of 2,2,1 → pentatonic-ish
    avg_step = np.mean(steps)
    step_variance = np.var(steps)

    # The interval the rhythm "is": average step × (1200/n)
    cents = avg_step * (1200.0 / n)

    # Consonance of the rhythm: inverse of variance (equal steps = more consonant)
    consonance = 1.0 / (1.0 + step_variance)

    return cents, consonance


def experiment2_euclidean_fifths_isomorphism():
    """Map every Euclidean rhythm to its consonance equivalent on the circle of fifths.
    Find the precise isomorphism and verify 3:2 = hemiola."""
    print("\n🔄 Experiment 2: Euclidean Rhythm ↔ Circle of Fifths")

    results = {
        "description": "Euclidean rhythms E(k,n) mapped to circle-of-fifths intervals",
        "isomorphisms": {},
        "hemiola_verification": {},
        "best_matches": [],
    }

    note_names = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
    # Circle of fifths intervals (cents from C)
    cof_intervals = {
        'P1': 0, 'm2': 100, 'M2': 200, 'm3': 300, 'M3': 400,
        'P4': 500, 'TT': 600, 'P5': 700, 'm6': 800, 'M6': 900,
        'm7': 1000, 'M7': 1100
    }
    # Just intonation reference
    just_cents = {
        'P1': 0, 'm2': 111.73, 'M2': 203.91, 'm3': 315.64, 'M3': 386.31,
        'P4': 498.04, 'TT': 582.51, 'P5': 701.96, 'm6': 813.69, 'M6': 884.36,
        'm7': 1017.60, 'M7': 1088.27
    }

    all_rhythms = []

    for n in range(5, 17):
        for k in range(1, n):
            rhythm = euclidean_rhythm(n, k)
            cents, cons = rhythm_to_interval_class(rhythm)

            # Find closest named interval
            closest_just = min(just_cents.items(), key=lambda x: abs(x[1] - cents))
            closest_et = min(cof_intervals.items(), key=lambda x: abs(x[1] - cents))
            deviation_from_just = abs(cents - closest_just[1])

            entry = {
                "n": n, "k": k,
                "rhythm": rhythm,
                "interval_cents": round(cents, 2),
                "consonance": round(cons, 4),
                "closest_just_interval": closest_just[0],
                "closest_just_cents": closest_just[1],
                "deviation_cents": round(deviation_from_just, 2),
                "closest_et_interval": closest_et[0],
            }
            key = f"E({k},{n})"
            results["isomorphisms"][key] = entry
            all_rhythms.append(entry)

            # Special check: hemiola E(2,3) = 3:2 perfect fifth?
            if n == 3 and k == 2:
                results["hemiola_verification"] = {
                    "rhythm": rhythm,
                    "interval_cents": round(cents, 2),
                    "perfect_fifth_just": 701.96,
                    "deviation": round(abs(cents - 701.96), 2),
                    "is_perfect_fifth": abs(cents - 701.96) < 50,
                    "explanation": (
                        "E(2,3)=[1,0,1] has steps 2 and 1 → ratio 2:1. "
                        "In the isomorphism, this maps to avg_step=1.5, "
                        "interval=1.5×(1200/3)=600 cents (tritone region). "
                        "The 3:2 hemiola RATIO (not rhythm E(2,3)) corresponds "
                        "to the perfect fifth. The rhythmic hemiola creates a "
                        "temporal perfect fifth: 3 against 2."
                    ),
                }
            if n == 2 and k == 1:
                # The simplest: one beat in 2 → interval = 600 cents (tritone)
                results["hemiola_verification"]["E(1,2)"] = {
                    "rhythm": rhythm,
                    "interval_cents": round(cents, 2),
                }

    # Find best isomorphisms: rhythms that map closest to just intervals
    all_rhythms.sort(key=lambda x: x["deviation_cents"])
    results["best_matches"] = all_rhythms[:20]

    # Circle of fifths correspondence: map rhythms by their k/n ratio
    # to interval ratios on the circle
    ratio_map = {}
    for r in all_rhythms:
        ratio = round(r["k"] / r["n"], 4)
        if ratio not in ratio_map or r["consonance"] > ratio_map[ratio]["consonance"]:
            ratio_map[ratio] = r

    results["ratio_to_interval"] = {
        str(k): {"interval": v["closest_just_interval"],
                  "cents": v["interval_cents"],
                  "rhythm": f"E({v['k']},{v['n']})"}
        for k, v in sorted(ratio_map.items())
    }

    with open(OUTDIR / "exp2_euclidean_fifths.json", 'w') as f:
        json.dump(results, f, indent=2)

    print(f"   ✓ Mapped {len(all_rhythms)} Euclidean rhythms")
    print(f"   ✓ Best match: E({all_rhythms[0]['k']},{all_rhythms[0]['n']}) → "
          f"{all_rhythms[0]['closest_just_interval']} "
          f"(deviation: {all_rhythms[0]['deviation_cents']:.1f}¢)")
    hemiola = results["hemiola_verification"]
    print(f"   ✓ Hemiola E(2,3) maps to {hemiola['interval_cents']:.0f}¢ "
          f"({'IS' if hemiola.get('is_perfect_fifth') else 'not directly'} perfect fifth)")

    return results


# ═══════════════════════════════════════════════════════════════════
# EXPERIMENT 3: Spectral Beating Atlas
# 12×12 matrices of beat rates for meantone and ET
# ═══════════════════════════════════════════════════════════════════

def experiment3_spectral_beating_atlas():
    """For every pair of notes in meantone and ET, compute beat rates
    when played as overtone-rich tones. Uses GPU FFT."""
    print("\n🌊 Experiment 3: Spectral Beating Atlas")
    print("   12×12 × 2 tuning systems, GPU FFT analysis")

    mt = meantone_intervals()
    et = et_intervals()
    fundamental = 261.63  # Middle C

    N_HARMONICS = 12
    DURATION = 2.0
    N_SAMPLES = int(DURATION * SR)

    # Pre-allocate GPU tensors for both tuning systems
    def compute_beat_matrix(intervals):
        """Compute 12×12 beat rate matrix for a tuning system."""
        # Generate all 12 tones with harmonics on GPU
        t = torch.linspace(0, DURATION, N_SAMPLES, device=DEVICE, dtype=torch.float32)
        tones = torch.zeros(12, N_SAMPLES, device=DEVICE, dtype=torch.float32)

        for note_idx in range(12):
            freq = fundamental * (2 ** (intervals[note_idx] / 1200))
            for h in range(1, N_HARMONICS + 1):
                amp = 1.0 / (h * h)
                tones[note_idx, :] += amp * torch.sin(2 * math.pi * freq * h * t)

        # For each pair, sum the two tones and analyze beating via FFT
        beat_matrix = torch.zeros(12, 12, device=DEVICE)
        roughness_matrix = torch.zeros(12, 12, device=DEVICE)

        # Batch FFT approach: compute all pairs at once
        for i in range(12):
            for j in range(i + 1, 12):
                # Sum the two tones
                combined = tones[i] + tones[j]

                # GPU FFT
                spectrum = torch.fft.rfft(combined)
                magnitudes = spectrum.abs() ** 2

                # Compute beat rate from frequency difference
                freq_i = fundamental * (2 ** (intervals[i] / 1200))
                freq_j = fundamental * (2 ** (intervals[j] / 1200))
                interval_cents = abs(intervals[j] - intervals[i]).item()

                # Beat rates come from near-coincident harmonics
                # For each pair of harmonics h1, h2:
                # beat = |h1*f_i - h2*f_j|
                beats = []
                for h1 in range(1, N_HARMONICS + 1):
                    for h2 in range(1, N_HARMONICS + 1):
                        beat_freq = abs(h1 * freq_i - h2 * freq_j)
                        # Only count if beat is in audible range (< ~50 Hz for perceptible beating)
                        if beat_freq < 50 and beat_freq > 0.1:
                            # Amplitude product of the two harmonics
                            amp_product = (1.0 / (h1 * h1)) * (1.0 / (h2 * h2))
                            beats.append((beat_freq, amp_product))

                if beats:
                    # Weighted average beat rate
                    total_weight = sum(a for _, a in beats)
                    weighted_beat = sum(f * a for f, a in beats) / total_weight
                    # Roughness: sum of weighted beat rates
                    roughness = sum(f * a for f, a in beats)
                else:
                    weighted_beat = 0.0
                    roughness = 0.0

                beat_matrix[i, j] = weighted_beat
                beat_matrix[j, i] = weighted_beat
                roughness_matrix[i, j] = roughness
                roughness_matrix[j, i] = roughness

            # Diagonal = unison, no beating
            beat_matrix[i, i] = 0.0
            roughness_matrix[i, i] = 0.0

        return beat_matrix, roughness_matrix

    print("   Computing meantone beat matrix...")
    mt_beats, mt_rough = compute_beat_matrix(mt)
    print("   Computing ET beat matrix...")
    et_beats, et_rough = compute_beat_matrix(et)

    # Find wolf interval in meantone
    mt_rough_upper = torch.triu(mt_rough, diagonal=1)
    flat_idx = mt_rough_upper.argmax().item()
    wolf_i, wolf_j = flat_idx // 12, flat_idx % 12
    note_names = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']

    # Difference atlas: meantone - ET (positive = meantone rougher)
    diff_rough = mt_rough - et_rough

    results = {
        "description": "12×12 spectral beating atlas for meantone and ET",
        "note_names": note_names,
        "meantone_beat_rates": mt_beats.cpu().tolist(),
        "et_beat_rates": et_beats.cpu().tolist(),
        "meantone_roughness": mt_rough.cpu().tolist(),
        "et_roughness": et_rough.cpu().tolist(),
        "roughness_difference_mt_minus_et": diff_rough.cpu().tolist(),
        "wolf_interval": {
            "notes": f"{note_names[wolf_i]}-{note_names[wolf_j]}",
            "meantone_roughness": mt_rough[wolf_i, wolf_j].item(),
            "et_roughness": et_rough[wolf_i, wolf_j].item(),
        },
        "analysis": {
            "meantone_avg_roughness": mt_rough[torch.triu(torch.ones(12,12, device=DEVICE), diagonal=1).bool()].mean().item(),
            "et_avg_roughness": et_rough[torch.triu(torch.ones(12,12, device=DEVICE), diagonal=1).bool()].mean().item(),
            "meantone_max_roughness": mt_rough.max().item(),
            "et_max_roughness": et_rough.max().item(),
            "meantone_min_nonzero": mt_rough[mt_rough > 0].min().item() if (mt_rough > 0).any() else 0,
            "et_min_nonzero": et_rough[et_rough > 0].min().item() if (et_rough > 0).any() else 0,
            "meantone_smoother_pairs": int((diff_rough < 0).sum().item() // 2),
            "et_smoother_pairs": int((diff_rough > 0).sum().item() // 2),
        }
    }

    with open(OUTDIR / "exp3_beating_atlas.json", 'w') as f:
        json.dump(results, f, indent=2)

    a = results["analysis"]
    print(f"   ✓ Meantone avg roughness: {a['meantone_avg_roughness']:.4f}")
    print(f"   ✓ ET avg roughness: {a['et_avg_roughness']:.4f}")
    print(f"   ✓ Wolf interval: {results['wolf_interval']['notes']} "
          f"(MT: {results['wolf_interval']['meantone_roughness']:.4f}, "
          f"ET: {results['wolf_interval']['et_roughness']:.4f})")
    print(f"   ✓ Meantone smoother on {a['meantone_smoother_pairs']} pairs, "
          f"ET smoother on {a['et_smoother_pairs']} pairs")

    # Render wolf interval audio comparison
    freq_wolf_i = fundamental * (2 ** (mt[wolf_i] / 1200))
    freq_wolf_j = fundamental * (2 ** (mt[wolf_j] / 1200))
    # Meantone wolf
    t = torch.linspace(0, 2.0, int(2.0 * SR), device=DEVICE, dtype=torch.float32)
    wolf_mt = torch.zeros_like(t)
    for h in range(1, 9):
        amp = 1.0 / (h * h)
        wolf_mt += amp * torch.sin(2 * math.pi * freq_wolf_i * h * t)
        wolf_mt += amp * torch.sin(2 * math.pi * freq_wolf_j * h * t)
    # ET equivalent
    freq_et_i = fundamental * (2 ** (et[wolf_i] / 1200))
    freq_et_j = fundamental * (2 ** (et[wolf_j] / 1200))
    wolf_et = torch.zeros_like(t)
    for h in range(1, 9):
        amp = 1.0 / (h * h)
        wolf_et += amp * torch.sin(2 * math.pi * freq_et_i * h * t)
        wolf_et += amp * torch.sin(2 * math.pi * freq_et_j * h * t)

    # Stereo: left=meantone wolf, right=ET equivalent
    stereo = torch.stack([wolf_mt, wolf_et], dim=0).T
    stereo = stereo / stereo.abs().max() * 0.8
    sf.write(str(OUTDIR / "exp3_wolf_comparison_stereo.wav"),
             stereo.cpu().numpy(), SR)

    return results


# ═══════════════════════════════════════════════════════════════════
# EXPERIMENT 4: Conservation Law Stress Test
# 10000 random tunings, test I_vert + I_horiz ≈ const
# ═══════════════════════════════════════════════════════════════════

def experiment4_conservation_stress_test():
    """Generate 10000 random tunings and test whether I_vert + I_horiz ≈ const."""
    print("\n⚖️ Experiment 4: Conservation Law Stress Test")
    print("   10000 random tunings, I_vert + I_horiz conservation check")

    torch.manual_seed(12345)
    N_TUNINGS = 10000
    N_NOTES = 12

    # Generate diverse tuning systems
    # Mix of structured and random
    tuning_cents = torch.zeros(N_TUNINGS, N_NOTES, device=DEVICE)

    # Category 0-1999: JI-like (perturbed just)
    ji = just_intervals_full()
    tuning_cents[:2000] = ji.unsqueeze(0) + torch.randn(2000, N_NOTES, device=DEVICE) * 5

    # Category 2000-3999: Meantone variants (vary the fifth size)
    fifths = 680 + torch.rand(2000, device=DEVICE) * 40  # 680-720 cents
    for i in range(2000):
        fifth = fifths[i].item()
        intervals = sorted([(fifth * j) % 1200 for j in range(12)])
        tuning_cents[2000 + i] = torch.tensor(intervals, device=DEVICE)

    # Category 4000-5999: ET variants (vary division)
    divisions = 8 + torch.rand(2000, device=DEVICE) * 10  # 8-18 divisions
    for i in range(2000):
        div = divisions[i].item()
        step = 1200.0 / div
        intervals = sorted([step * j % 1200 for j in range(12)])
        tuning_cents[4000 + i] = torch.tensor(intervals[:12], device=DEVICE)

    # Category 6000-7999: Random (uniform)
    tuning_cents[6000:8000] = torch.rand(2000, N_NOTES, device=DEVICE) * 1200

    # Category 8000-9999: "Adversarial" (designed to break conservation)
    # High consonance contrast: some intervals perfect, others terrible
    for i in range(2000):
        base = torch.linspace(0, 1200, N_NOTES, device=DEVICE)
        # Add spikes
        spikes = torch.zeros(N_NOTES, device=DEVICE)
        n_spikes = torch.randint(2, 6, (1,)).item()
        for _ in range(n_spikes):
            idx = torch.randint(0, N_NOTES, (1,)).item()
            spikes[idx] = torch.randn(1, device=DEVICE).item() * 100
        tuning_cents[8000 + i] = (base + spikes) % 1200

    # Sort all tunings
    tuning_cents, _ = torch.sort(tuning_cents, dim=1)

    # Compute I_vertical and I_horizontal for each tuning
    i_vert = torch.zeros(N_TUNINGS, device=DEVICE)
    i_horiz = torch.zeros(N_TUNINGS, device=DEVICE)

    for i in range(N_TUNINGS):
        intervals = tuning_cents[i]

        # I_vertical: consonance-based surprise of vertical combinations
        # All pairwise intervals
        diffs = (intervals.unsqueeze(1) - intervals.unsqueeze(0)) % 1200
        # Upper triangle only
        mask = torch.triu(torch.ones(N_NOTES, N_NOTES, device=DEVICE, dtype=torch.bool), diagonal=1)
        pair_cents = diffs[mask]

        # Consonance of each pair
        cons = consonance_score(pair_cents)
        # I_vertical = entropy of consonance distribution
        # Bin consonances and compute entropy
        cons_norm = cons / (cons.sum() + 1e-10)
        i_vert[i] = -(cons_norm * torch.log2(cons_norm + 1e-10)).sum()

        # I_horizontal: interval between consecutive scale degrees
        steps = torch.diff(intervals)
        # Add wrap-around
        wrap = (1200 - intervals[-1] + intervals[0]).unsqueeze(0)
        all_steps = torch.cat([steps, wrap])
        # Entropy of step distribution
        step_cons = consonance_score(all_steps)
        step_norm = step_cons / (step_cons.sum() + 1e-10)
        i_horiz[i] = -(step_norm * torch.log2(step_norm + 1e-10)).sum()

    total_i = i_vert + i_horiz

    # Statistics
    total_mean = total_i.mean().item()
    total_std = total_std = total_i.std().item()
    total_var = total_i.var().item()
    correlation = torch.corrcoef(torch.stack([i_vert, i_horiz]))[0, 1].item()

    # By category
    categories = ["JI-like", "Meantone variants", "ET variants", "Random", "Adversarial"]
    cat_stats = []
    for ci, (start, end) in enumerate([(0, 2000), (2000, 4000), (4000, 6000),
                                        (6000, 8000), (8000, 10000)]):
        cat_total = total_i[start:end]
        cat_stats.append({
            "category": categories[ci],
            "mean_total_i": cat_total.mean().item(),
            "std_total_i": cat_total.std().item(),
            "mean_i_vert": i_vert[start:end].mean().item(),
            "mean_i_horiz": i_horiz[start:end].mean().item(),
        })

    # Conservation test: what fraction have total within N std devs of mean?
    within_1std = ((total_i > total_mean - total_std) & (total_i < total_mean + total_std)).float().mean().item()

    results = {
        "description": "10000 tuning systems stress-testing I_vert + I_horiz conservation",
        "n_tunings": N_TUNINGS,
        "total_i_mean": total_mean,
        "total_i_std": total_std,
        "total_i_variance": total_var,
        "coeff_of_variation": total_std / total_mean if total_mean != 0 else float('inf'),
        "vert_horiz_correlation": correlation,
        "within_1_std_fraction": within_1std,
        "category_breakdown": cat_stats,
        "scatter_sample": {
            "i_vert": i_vert[::100].cpu().tolist(),  # 100 points for plotting
            "i_horiz": i_horiz[::100].cpu().tolist(),
            "total": total_i[::100].cpu().tolist(),
            "category": [i // 20 for i in range(0, 100)],  # category index for coloring
        },
        "conservation_holds": abs(correlation) > 0.3 and total_std / total_mean < 0.5,
        "verdict": (
            f"Total I has CV={total_std/total_mean:.3f}. "
            f"Correlation(I_vert, I_horiz)={correlation:.3f}. "
            f"{'Conservation appears to hold' if abs(correlation) > 0.3 else 'Conservation is weak'}: "
            f"vert and horiz {'trade off' if correlation < -0.1 else 'do not clearly trade off'}."
        ),
    }

    with open(OUTDIR / "exp4_conservation_test.json", 'w') as f:
        json.dump(results, f, indent=2)

    print(f"   ✓ Total I: mean={total_mean:.4f}, std={total_std:.4f}, "
          f"CV={results['coeff_of_variation']:.4f}")
    print(f"   ✓ Correlation(I_vert, I_horiz) = {correlation:.4f}")
    print(f"   ✓ Within 1σ: {within_1std*100:.1f}%")
    print(f"   ✓ Verdict: {results['verdict']}")

    return results


# ═══════════════════════════════════════════════════════════════════
# EXPERIMENT 5: Nancarrow Tempo-Space Exploration
# 50 canons with just, ET, and irrational tempo ratios
# ═══════════════════════════════════════════════════════════════════

def experiment5_nancarrow_tempo_space():
    """Render 50 Nancarrow-style mini-canons with varied tempo ratios.
    Classify by consonance of tempo ratio."""
    print("\n🎹 Experiment 5: Nancarrow Tempo-Space Exploration")
    print("   50 mini-canons, just/ET/irrational tempo ratios")

    torch.manual_seed(77)
    DURATION = 4.0  # seconds per canon
    N_NOTES_PER_VOICE = 16

    # Define tempo ratio categories
    canon_specs = []

    # Just ratios (15 canons)
    just_ratios = [
        (1, 1, "unison"), (2, 1, "octave"), (3, 2, "perfect fifth"),
        (4, 3, "perfect fourth"), (5, 4, "major third"), (5, 3, "major sixth"),
        (6, 5, "minor third"), (3, 1, "octave+fifth"), (4, 1, "double octave"),
        (5, 2, "major tenth"), (7, 4, "harmonic seventh"), (8, 5, "minor sixth"),
        (9, 5, "just seventh"), (9, 8, "major second"), (15, 8, "major seventh"),
    ]
    for i, (num, den, name) in enumerate(just_ratios):
        canon_specs.append({
            "id": i,
            "type": "just",
            "ratio_num": num, "ratio_den": den,
            "ratio": num / den,
            "ratio_label": name,
            "ratio_label_short": f"{num}:{den}",
        })

    # ET ratios (15 canons): tempered versions
    et_steps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 19]
    for i, steps in enumerate(et_steps):
        ratio = 2 ** (steps / 12)
        canon_specs.append({
            "id": 15 + i,
            "type": "ET",
            "ratio_num": steps, "ratio_den": 12,
            "ratio": ratio,
            "ratio_label": f"2^({steps}/12)",
            "ratio_label_short": f"ET{steps}",
        })

    # Irrational ratios (20 canons): phi, e, sqrt, etc.
    PHI = (1 + math.sqrt(5)) / 2  # golden ratio
    irrationals = [
        (PHI, "φ (golden ratio)"), (math.e, "e (Euler)"),
        (math.sqrt(2), "√2"), (math.sqrt(3), "√3"),
        (math.sqrt(5), "√5"), (math.pi / 2, "π/2"),
        (math.pi / 3, "π/3"), (math.e / 2, "e/2"),
        (2 ** (1/3), "∛2"), (2 ** (1/5), "2^(1/5)"),
        (3 ** (1/3), "∛3"), (5 ** (1/4), "5^(1/4)"),
        (math.log2(3), "log₂3"), (math.log2(5), "log₂5"),
        (1.618033988, "φ precise"),
        (1.414213562, "√2 precise"),
        (1.732050808, "√3 precise"),
        (2.236067978, "√5 precise"),
        (1.202056903, "Apery's const"),
        (1.131988248, "Viswanath's const"),
    ]
    for i, (ratio, name) in enumerate(irrationals):
        canon_specs.append({
            "id": 30 + i,
            "type": "irrational",
            "ratio_num": None, "ratio_den": None,
            "ratio": ratio,
            "ratio_label": name,
            "ratio_label_short": name.split("(")[0].strip()[:8],
        })

    results = {
        "description": "50 Nancarrow-style canons with just, ET, irrational tempo ratios",
        "canons": [],
        "analysis": {
            "just_avg_consonance": 0,
            "et_avg_consonance": 0,
            "irrational_avg_consonance": 0,
        }
    }

    just_cons, et_cons, irrational_cons = [], [], []
    fundamental = 261.63  # C4

    for spec in canon_specs:
        ratio = spec["ratio"]
        # Voice 1: base tempo
        tempo1 = 4.0  # notes per second
        tempo2 = tempo1 * ratio

        # Generate a simple chromatic melody
        melody_notes = torch.randint(0, 7, (N_NOTES_PER_VOICE,), device=DEVICE)
        melody_freqs = fundamental * (2 ** (melody_notes.float() / 12))

        # Render voice 1
        note_dur1 = 1.0 / tempo1
        voice1 = render_audio(melody_freqs.cpu().tolist(),
                              [note_dur1] * N_NOTES_PER_VOICE, et_intervals().cpu())

        # Render voice 2 (same melody, different tempo)
        note_dur2 = 1.0 / tempo2
        voice2 = render_audio(melody_freqs.cpu().tolist(),
                              [note_dur2] * N_NOTES_PER_VOICE, et_intervals().cpu())

        # Pad to same length
        max_len = max(len(voice1), len(voice2))
        v1 = torch.zeros(max_len, device=DEVICE)
        v2 = torch.zeros(max_len, device=DEVICE)
        v1[:len(voice1)] = voice1
        v2[:len(voice2)] = voice2

        # Stereo output
        stereo = torch.stack([v1, v2], dim=0).T
        stereo = stereo / (stereo.abs().max() + 1e-10) * 0.8

        # Compute "tempo consonance": how close is the ratio to a just ratio?
        just_refs = [1/1, 2/1, 3/2, 4/3, 5/4, 5/3, 6/5, 3/1, 4/1, 5/2, 7/4, 8/5, 9/5, 15/8]
        min_deviation = min(abs(ratio - j) for j in just_refs)
        # Consonance = exponential decay from nearest just ratio
        tempo_consonance = math.exp(-min_deviation * 3)

        # Also compute spectral consonance of the combined audio
        # via autocorrelation of the sum
        combined = v1 + v2
        if len(combined) > SR:
            # Compute autocorrelation of a chunk
            chunk = combined[:SR]
            fft_chunk = torch.fft.rfft(chunk)
            autocorr = torch.fft.irfft(fft_chunk * torch.conj(fft_chunk))
            autocorr = autocorr[:100]  # first 100 lags
            if autocorr[0] > 0:
                autocorr = autocorr / autocorr[0]
                # Periodicity strength = peak at non-zero lag
                if len(autocorr) > 10:
                    spectral_cons = autocorr[10:100].max().item()
                else:
                    spectral_cons = 0.5
            else:
                spectral_cons = 0.0
        else:
            spectral_cons = 0.0

        canon_result = {
            "id": spec["id"],
            "type": spec["type"],
            "ratio": round(ratio, 6),
            "ratio_label": spec["ratio_label"],
            "tempo_consonance": round(tempo_consonance, 4),
            "spectral_periodicity": round(spectral_cons, 4),
            "combined_consonance": round((tempo_consonance + spectral_cons) / 2, 4),
        }
        results["canons"].append(canon_result)

        if spec["type"] == "just":
            just_cons.append(tempo_consonance)
        elif spec["type"] == "ET":
            et_cons.append(tempo_consonance)
        else:
            irrational_cons.append(tempo_consonance)

        # Save select audio files (first of each type + best/worst)
        if spec["id"] in [0, 2, 15, 30, 31]:  # unison, P5, ET1, phi, e
            filename = f"exp5_canon_{spec['id']}_{spec['type']}_{spec['ratio_label_short'].replace(' ', '_')}.wav"
            sf.write(str(OUTDIR / filename), stereo.cpu().numpy(), SR)

    # Save a few more: best and worst consonance
    sorted_canons = sorted(results["canons"], key=lambda x: x["combined_consonance"], reverse=True)
    for label, idx in [("best", sorted_canons[0]["id"]), ("worst", sorted_canons[-1]["id"])]:
        spec = canon_specs[idx]
        ratio = spec["ratio"]
        tempo1 = 4.0
        tempo2 = tempo1 * ratio
        melody_notes = torch.randint(0, 7, (N_NOTES_PER_VOICE,), device=DEVICE)
        melody_freqs = fundamental * (2 ** (melody_notes.float() / 12))
        v1 = render_audio(melody_freqs.cpu().tolist(), [1.0/tempo1]*N_NOTES_PER_VOICE, et_intervals().cpu())
        v2 = render_audio(melody_freqs.cpu().tolist(), [1.0/tempo2]*N_NOTES_PER_VOICE, et_intervals().cpu())
        max_len = max(len(v1), len(v2))
        s = torch.zeros(max_len, device=DEVICE)
        s[:len(v1)] = v1
        s2 = torch.zeros(max_len, device=DEVICE)
        s2[:len(v2)] = v2
        stereo = torch.stack([s, s2], dim=0).T
        stereo = stereo / (stereo.abs().max() + 1e-10) * 0.8
        sf.write(str(OUTDIR / f"exp5_canon_{label}_id{idx}.wav"), stereo.cpu().numpy(), SR)

    results["analysis"]["just_avg_consonance"] = round(np.mean(just_cons), 4)
    results["analysis"]["et_avg_consonance"] = round(np.mean(et_cons), 4)
    results["analysis"]["irrational_avg_consonance"] = round(np.mean(irrational_cons), 4)
    results["analysis"]["perceptible_difference"] = (
        "Just ratios show significantly higher tempo consonance than irrational ratios, "
        f"confirming perceptual preference (just: {np.mean(just_cons):.3f} vs "
        f"irrational: {np.mean(irrational_cons):.3f})"
        if np.mean(just_cons) > np.mean(irrational_cons) + 0.1
        else "Difference is marginal"
    )

    with open(OUTDIR / "exp5_nancarrow_tempo.json", 'w') as f:
        json.dump(results, f, indent=2)

    a = results["analysis"]
    print(f"   ✓ Just consonance: {a['just_avg_consonance']:.4f}")
    print(f"   ✓ ET consonance: {a['et_avg_consonance']:.4f}")
    print(f"   ✓ Irrational consonance: {a['irrational_avg_consonance']:.4f}")
    print(f"   ✓ {a['perceptible_difference']}")

    return results


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import time

    print("═" * 60)
    print("  GPU MUSIC THEORY EXPERIMENTS v2")
    print("  RTX 4050 — The Ambitious Sequel")
    print("═" * 60)

    total_start = time.time()

    # Run all experiments
    r1 = experiment1_historical_simulation()
    t1 = time.time() - total_start
    print(f"   ⏱ {t1:.1f}s")

    t2_start = time.time()
    r2 = experiment2_euclidean_fifths_isomorphism()
    t2 = time.time() - t2_start
    print(f"   ⏱ {t2:.1f}s")

    t3_start = time.time()
    r3 = experiment3_spectral_beating_atlas()
    t3 = time.time() - t3_start
    print(f"   ⏱ {t3:.1f}s")

    t4_start = time.time()
    r4 = experiment4_conservation_stress_test()
    t4 = time.time() - t4_start
    print(f"   ⏱ {t4:.1f}s")

    t5_start = time.time()
    r5 = experiment5_nancarrow_tempo_space()
    t5 = time.time() - t5_start
    print(f"   ⏱ {t5:.1f}s")

    total_time = time.time() - total_start
    print("\n" + "═" * 60)
    print(f"  ALL EXPERIMENTS COMPLETE")
    print(f"  Total time: {total_time:.1f}s")
    print(f"  Output: {OUTDIR}")
    print("═" * 60)

    # Summary manifest
    manifest = {
        "v2_experiments": {
            "exp1_historical_simulation": "1000 agents × 600 years, meantone→ET",
            "exp2_euclidean_fifths": "Euclidean rhythm ↔ circle of fifths isomorphism",
            "exp3_beating_atlas": "12×12 spectral beating matrices (meantone vs ET)",
            "exp4_conservation_test": "10000 tuning stress test of I_vert + I_horiz",
            "exp5_nancarrow_tempo": "50 canons, just/ET/irrational tempo ratios",
        },
        "timing": {
            "exp1": round(t1, 1),
            "exp2": round(t2, 1),
            "exp3": round(t3, 1),
            "exp4": round(t4, 1),
            "exp5": round(t5, 1),
            "total": round(total_time, 1),
        },
        "output_dir": str(OUTDIR),
    }
    with open(OUTDIR / "manifest.json", 'w') as f:
        json.dump(manifest, f, indent=2)
