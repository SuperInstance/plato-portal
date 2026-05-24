#!/usr/bin/env python3
"""
GPU-Accelerated Music Theory Experiments v3 — World Traditions & Conservation
RTX 4050 (6.4GB) — CUDA 8.9 (Ada Lovelace)

Five experiments exploring how DIFFERENT musical traditions handle
the conservation of tension:

1. World Scale Consonance Explorer (27 scales → WAV + JSON)
2. Cross-Cultural Rhythmic Pattern Analysis (8 traditions)
3. Language-Specific Music Rendering (Rust/Haskell/Python/C styles)
4. Conservation Law Across 10 Traditions (I_vert vs I_horiz)
5. Microtonal Rendering Engine (19/31/53-TET, BP, Carlos, Partch)

All GPU-accelerated via torch.cuda. Output in gpu_output_v3/.
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
import time

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"🌍 V3 World Traditions Explorer on: {DEVICE}")
if torch.cuda.is_available():
    print(f"   {torch.cuda.get_device_name(0)}")
    total_mb = torch.cuda.get_device_properties(0).total_memory / 1e6
    print(f"   {total_mb:.0f} MB VRAM")

OUTDIR = Path(__file__).parent / "gpu_output_v3"
OUTDIR.mkdir(exist_ok=True)

SR = 44100

# ═══════════════════════════════════════════════════════════════════
# CORE UTILITIES
# ═══════════════════════════════════════════════════════════════════

def cents_to_freq(cents, root=261.626):
    """Convert cents above root to frequency."""
    return root * (2 ** (cents / 1200.0))

def consonance_score(cents_diff, sigma=12.0):
    """Consonance from cents deviation to nearest just interval."""
    just_refs = torch.tensor([
        0, 111.73, 182.40, 203.91, 231.17, 266.87, 315.64,
        386.31, 407.82, 435.08, 498.04, 519.55, 582.51,
        609.78, 701.96, 764.92, 813.69, 840.53, 884.36,
        905.87, 955.03, 1017.60, 1088.27, 1200.0
    ], device=DEVICE, dtype=torch.float32)
    diffs = torch.abs(cents_diff.unsqueeze(-1) - just_refs)
    min_diffs = diffs.min(dim=-1).values
    return torch.exp(-(min_diffs ** 2) / (2 * sigma ** 2))

def shannon_entropy(probs):
    """Shannon entropy of a probability distribution."""
    p = probs[probs > 0]
    return -torch.sum(p * torch.log2(p))

def synthesize_chord_gpu(freqs, duration=5.0, sr=SR, harmonics=8, decay=0.3):
    """Synthesize a chord with overtones on GPU. Returns numpy array."""
    t = torch.linspace(0, duration, int(sr * duration), device=DEVICE, dtype=torch.float32)
    signal = torch.zeros_like(t)
    for f in freqs:
        for h in range(1, harmonics + 1):
            amp = 1.0 / (h ** decay)
            # Slight inharmonicity for richness
            freq = f * h * (1.0 + 0.0003 * h * h)
            signal += amp * torch.sin(2 * math.pi * freq * t)
    # ADSR envelope
    n = len(t)
    attack = int(0.05 * sr)
    release = int(0.5 * sr)
    sustain_len = n - attack - release
    envelope = torch.cat([
        torch.linspace(0, 1, attack, device=DEVICE),
        torch.ones(sustain_len, device=DEVICE),
        torch.linspace(1, 0, release, device=DEVICE)
    ])[:n]
    signal *= envelope
    # Normalize
    signal = signal / (signal.abs().max() + 1e-8) * 0.7
    return signal.cpu().numpy()

def compute_spectrogram(signal, sr=SR, n_fft=4096, hop=512):
    """Compute power spectrogram on GPU."""
    sig = torch.tensor(signal, device=DEVICE, dtype=torch.float32)
    window = torch.hann_window(n_fft, device=DEVICE)
    # Manual STFT for control
    n_frames = (len(sig) - n_fft) // hop + 1
    frames = sig.unfold(0, n_fft, hop)  # [n_frames, n_fft]
    frames = frames * window
    spectrum = torch.fft.rfft(frames, dim=-1)
    power = (spectrum.abs() ** 2).mean(dim=0)  # average across frames
    freqs = torch.fft.rfftfreq(n_fft, 1.0/sr)
    return freqs.cpu().numpy(), power.cpu().numpy()

def find_peaks(freqs, power, n_peaks=10, min_freq=50):
    """Find top N spectral peaks above min_freq."""
    mask = freqs > min_freq
    f = freqs[mask]
    p = power[mask]
    if len(p) == 0:
        return []
    top_idx = np.argsort(p)[-n_peaks:][::-1]
    return [(float(f[i]), float(p[i])) for i in top_idx]

# ═══════════════════════════════════════════════════════════════════
# THE 27 WORLD SCALES
# ═══════════════════════════════════════════════════════════════════

SCALES = {
    # Western
    "Major": [0, 2, 4, 5, 7, 9, 11],
    "Natural Minor": [0, 2, 3, 5, 7, 8, 10],
    "Harmonic Minor": [0, 2, 3, 5, 7, 8, 11],
    "Melodic Minor (asc)": [0, 2, 3, 5, 7, 9, 11],
    "Dorian": [0, 2, 3, 5, 7, 9, 10],
    "Phrygian": [0, 1, 3, 5, 7, 8, 10],
    "Lydian": [0, 2, 4, 6, 7, 9, 11],
    "Mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "Whole Tone": [0, 2, 4, 6, 8, 10],
    "Chromatic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "Pentatonic Major": [0, 2, 4, 7, 9],
    "Pentatonic Minor": [0, 3, 5, 7, 10],
    "Blues": [0, 3, 5, 6, 7, 10],
    # Indian
    "Bhairavi (India)": [0, 1, 3, 5, 7, 8, 10],  # equivalent to Phrygian
    "Yaman (India)": [0, 2, 4, 6, 7, 9, 11],      # equivalent to Lydian
    "Kafi (India)": [0, 2, 3, 5, 7, 9, 10],        # equivalent to Dorian
    "Todi (India)": [0, 1, 3, 6, 7, 8, 11],
    # Middle Eastern / Turkish
    "Hijaz": [0, 1, 4, 5, 7, 8, 11],
    "Kurd": [0, 1, 3, 5, 7, 8, 10],
    "Rast (Turkish)": [0, 2, 4, 5, 7, 9, 10],      # with quarter tones approximated
    "Bayati": [0, 1.5, 4, 5, 7, 8, 10],             # quarter-tone approx
    # East Asian
    "Japanese In": [0, 1, 5, 7, 8],
    "Japanese Yo": [0, 3, 5, 7, 10],
    "Chinese Gong": [0, 2, 4, 7, 9],
    # Javanese/Balinese (pelog & slendro approximations)
    "Pelog (Java)": [0, 1, 3, 5, 7, 8, 10],
    "Slendro (Java)": [0, 2.3, 4.6, 7, 9.3],       # approximate equal steps
    # African
    "West African Heptatonic": [0, 2, 3, 5, 7, 8, 10],  # similar to natural minor
}

# ═══════════════════════════════════════════════════════════════════
# EXPERIMENT 1: World Scale Consonance Explorer
# ═══════════════════════════════════════════════════════════════════

def experiment1():
    print("\n" + "="*70)
    print("EXPERIMENT 1: World Scale Consonance Explorer (27 scales)")
    print("="*70)
    
    results = {}
    
    for name, intervals in SCALES.items():
        print(f"  🎵 {name} ({len(intervals)} notes)...")
        cents = torch.tensor(intervals, device=DEVICE, dtype=torch.float32) * 100.0
        
        # Full consonance field: all pairwise intervals
        n = len(cents)
        pairs = []
        cons_field = torch.zeros(n, n, device=DEVICE)
        for i in range(n):
            for j in range(i+1, n):
                diff = (cents[j] - cents[i]) % 1200
                cs = consonance_score(diff.unsqueeze(0)).item()
                cons_field[i, j] = cs
                cons_field[j, i] = cs
                pairs.append(cs)
        
        # I_vert: Shannon entropy of consonance distribution
        pair_tensor = torch.tensor(pairs, device=DEVICE)
        # Bin into histogram for entropy
        n_bins = 20
        hist = torch.histc(pair_tensor, bins=n_bins, min=0, max=1)
        probs = hist / hist.sum()
        i_vert = shannon_entropy(probs).item()
        
        # Mean consonance and variance
        mean_cons = pair_tensor.mean().item()
        var_cons = pair_tensor.var().item()
        
        # Synthesize audio
        freqs = [cents_to_freq(c.item()) for c in cents]
        audio = synthesize_chord_gpu(freqs, duration=5.0)
        
        # Compute spectrogram
        spec_freqs, spec_power = compute_spectrogram(audio)
        peaks = find_peaks(spec_freqs, spec_power, n_peaks=10)
        
        # Save audio
        safe_name = name.replace(" ", "_").replace("(", "").replace(")", "")
        wav_path = OUTDIR / f"exp1_{safe_name}.wav"
        sf.write(str(wav_path), audio, SR)
        
        results[name] = {
            "n_notes": n,
            "intervals_semitones": intervals,
            "mean_consonance": round(mean_cons, 6),
            "variance_consonance": round(var_cons, 6),
            "I_vert": round(i_vert, 6),
            "consonance_field_shape": [n, n],
            "spectral_peaks_Hz": [(round(f, 1), round(p, 6)) for f, p in peaks],
            "audio_file": str(wav_path.name),
        }
        print(f"     I_vert={i_vert:.4f}  mean_cons={mean_cons:.4f}  var={var_cons:.4f}")
    
    # Save JSON
    with open(OUTDIR / "exp1_scale_consonance.json", "w") as f:
        json.dump({k: float(v) if hasattr(v, "item") else v for k, v in results.items()}, f, indent=2, default=str)
    print(f"\n  ✅ Saved 27 WAV files + exp1_scale_consonance.json")
    return results

# ═══════════════════════════════════════════════════════════════════
# EXPERIMENT 2: Cross-Cultural Rhythmic Pattern Analysis
# ═══════════════════════════════════════════════════════════════════

def euclidean_rhythm(k, n):
    """Björklund's algorithm for Euclidean rhythm E(k,n).
    Distributes k onsets as evenly as possible among n steps."""
    if k >= n:
        return [1] * n
    if k == 0:
        return [0] * n
    
    # Start with k ones and (n-k) zeros
    ones = [[1] for _ in range(k)]
    zeros = [[0] for _ in range(n - k)]
    
    # Repeatedly concatenate the shorter group onto the longer
    while len(ones) > 1 and len(zeros) > 0:
        n_concat = min(len(ones), len(zeros))
        new_ones = []
        for i in range(n_concat):
            new_ones.append(ones[i] + zeros[i])
        # Remaining elements
        remaining = ones[n_concat:] + zeros[n_concat:]
        ones = new_ones
        zeros = remaining
    
    # Flatten
    result = []
    for group in ones:
        result.extend(group)
    for group in zeros:
        result.extend(group)
    
    return result

RHYTHMS = {
    "Aksak (2+2+2+3)": {
        "pattern": [1,0, 1,0, 1,0, 1,0,0],  # 9/8
        "culture": "Bulgarian/Turkish",
        "time_sig": "9/8",
    },
    "Tresillo (3+3+2)": {
        "pattern": [1,0,0, 1,0,0, 1,0],  # 8
        "culture": "Cuban",
        "time_sig": "4/4",
    },
    "Bossa Nova": {
        "pattern": [1,0,0, 1,0,0, 1,0,0, 1,0, 1,0, 1,0],  # 16 subdivisions
        "culture": "Brazilian",
        "time_sig": "4/4 (16th notes)",
    },
    "Malfouf (3+2+2)": {
        "pattern": [1,0,0, 1,0, 1,0],  # 7
        "culture": "Arabic",
        "time_sig": "7/8",
    },
    "Rupak (3+2+2)": {
        "pattern": [1,0,0, 1,0, 1,0],  # 7 — same as Malfouf but Indian context
        "culture": "Indian",
        "time_sig": "7/8",
    },
    "Ewe (3+3+4+2+4)": {
        "pattern": [1,0,0, 1,0,0, 1,0,0,0, 1,0, 1,0,0,0],  # 16 subdivisions
        "culture": "Ghanaian",
        "time_sig": "4/4 (16th notes)",
    },
    "Mori (3+3+3)": {
        "pattern": [1,0,0, 1,0,0, 1,0,0],  # 9
        "culture": "Japanese",
        "time_sig": "9/8",
    },
}

def compute_syncopation(pattern):
    """Compute syncopation index (LHL-based).
    Higher = more syncopated = more tension."""
    n = len(pattern)
    if n == 0:
        return 0.0
    # Metrical weight: stronger beats get higher weight
    # Binary hierarchy: positions divisible by larger powers of 2 get more weight
    weights = []
    for i in range(n):
        w = 0
        pos = i
        while pos % 2 == 0 and pos > 0:
            w += 1
            pos //= 2
        if i == 0:
            w = max(w, 3)  # downbeat
        weights.append(w)
    
    weights = torch.tensor(weights, device=DEVICE, dtype=torch.float32)
    pat = torch.tensor(pattern, device=DEVICE, dtype=torch.float32)
    
    # Syncopation: note on weak beat followed by rest on strong beat
    sync = 0.0
    for i in range(n):
        if pat[i] == 1:
            next_i = (i + 1) % n
            if pat[next_i] == 0 and weights[next_i] > weights[i]:
                sync += weights[next_i] - weights[i]
    return float(sync)

def onset_entropy(pattern):
    """Shannon entropy of onset positions."""
    n = len(pattern)
    if sum(pattern) == 0:
        return 0.0
    onsets = [i for i, x in enumerate(pattern) if x == 1]
    if len(onsets) <= 1:
        return 0.0
    # Inter-onset intervals
    iois = [(onsets[i+1] - onsets[i]) for i in range(len(onsets)-1)]
    iois.append(n - onsets[-1] + onsets[0])  # wrap
    ioi_tensor = torch.tensor(iois, device=DEVICE, dtype=torch.float32)
    probs = ioi_tensor / ioi_tensor.sum()
    return shannon_entropy(probs).item()

def euclidean_distance(p1, p2):
    """Hamming-like distance between two patterns (with padding)."""
    n1, n2 = len(p1), len(p2)
    if n1 == 0 or n2 == 0:
        return 1.0
    lcm = n1 * n2 // math.gcd(n1, n2)
    if lcm == 0:
        return 1.0
    s1 = [p1[i % n1] for i in range(lcm)]
    s2 = [p2[i % n2] for i in range(lcm)]
    matches = sum(a == b for a, b in zip(s1, s2))
    return 1.0 - matches / lcm  # 0 = identical, 1 = totally different

def rhythm_to_fifths(pattern):
    """Map rhythm onsets to positions on the circle of fifths.
    Each onset becomes a fifth (700 cents) from the previous."""
    onsets = [i for i, x in enumerate(pattern) if x == 1]
    if not onsets:
        return []
    fifths_pos = [0]
    for i in range(1, len(onsets)):
        interval = (onsets[i] - onsets[i-1]) * 700.0 / len(pattern) * 2
        fifths_pos.append(fifths_pos[-1] + interval)
    return fifths_pos

def experiment2():
    print("\n" + "="*70)
    print("EXPERIMENT 2: Cross-Cultural Rhythmic Pattern Analysis")
    print("="*70)
    
    results = {}
    
    for name, info in RHYTHMS.items():
        pattern = info["pattern"]
        n = len(pattern)
        k = sum(pattern)
        print(f"  🥁 {name} ({info['culture']}, {info['time_sig']})...")
        
        # Metrics
        sync = compute_syncopation(pattern)
        sync = float(sync)
        ent = onset_entropy(pattern)
        ent = float(ent)
        
        # Euclidean rhythm for comparison
        euc = euclidean_rhythm(k, n) if k <= n else [1]*n
        euc_dist = euclidean_distance(pattern, euc)
        
        # Map to circle of fifths
        fifths = rhythm_to_fifths(pattern)
        
        # Synthesize the rhythm as audio
        duration = 4.0  # seconds, repeat pattern
        t = torch.linspace(0, duration, int(SR * duration), device=DEVICE, dtype=torch.float32)
        signal = torch.zeros_like(t)
        step_dur = duration / n
        # Create click pattern
        for rep in range(int(duration / step_dur / n) + 2):
            for i, v in enumerate(pattern):
                if v == 1:
                    onset_t = rep * n * step_dur + i * step_dur
                    onset_sample = int(onset_t * SR)
                    click_len = int(0.02 * SR)  # 20ms click
                    if onset_sample + click_len < len(signal):
                        click = torch.exp(-torch.linspace(0, 8, click_len, device=DEVICE))
                        signal[onset_sample:onset_sample+click_len] += click
        
        signal = signal / (signal.abs().max() + 1e-8) * 0.6
        audio = signal.cpu().numpy()
        
        safe_name = name.split("(")[0].strip().replace(" ", "_")
        wav_path = OUTDIR / f"exp2_{safe_name}.wav"
        sf.write(str(wav_path), audio, SR)
        
        results[name] = {
            "culture": info["culture"],
            "time_signature": info["time_sig"],
            "pattern": pattern,
            "n_steps": n,
            "n_onsets": k,
            "syncopation_index": round(float(sync), 4),
            "onset_entropy": round(ent, 4),
            "euclidean_similarity": round(1.0 - euc_dist, 4),
            "euclidean_rhythm": euc,
            "fifths_mapping": [round(f, 2) for f in fifths],
            "audio_file": str(wav_path.name),
        }
        print(f"     sync={sync:.3f}  entropy={ent:.3f}  eucl_sim={1-euc_dist:.3f}")
    
    # Also generate Euclidean rhythms for comparison
    for k, n in [(3,8), (4,12), (5,8), (5,16), (7,12), (7,16), (9,16)]:
        euc = euclidean_rhythm(k, n)
        euc_name = f"Euclidean E({k},{n})"
        sync = float(compute_syncopation(euc))
        ent = float(onset_entropy(euc))
        results[euc_name] = {
            "culture": "Mathematical",
            "time_signature": f"{n}/8" if n % 8 == 0 else f"{n}/4",
            "pattern": euc,
            "n_steps": n,
            "n_onsets": k,
            "syncopation_index": round(sync, 4),
            "onset_entropy": round(ent, 4),
            "euclidean_similarity": 1.0,
            "audio_file": None,
        }
        print(f"  📐 {euc_name}: sync={sync:.3f}  entropy={ent:.3f}")
    
    with open(OUTDIR / "exp2_rhythm_analysis.json", "w") as f:
        json.dump({k: float(v) if hasattr(v, "item") else v for k, v in results.items()}, f, indent=2, default=str)
    print(f"\n  ✅ Saved rhythm WAV files + exp2_rhythm_analysis.json")
    return results

# ═══════════════════════════════════════════════════════════════════
# EXPERIMENT 3: Language-Specific Music Rendering
# ═══════════════════════════════════════════════════════════════════

def render_rust_style(freqs, duration=5.0, sr=SR):
    """Rust style: Zero-allocation, exact frequencies, no dynamic dispatch.
    Monomorphized sine waves with hard-coded parameters. No vibrato, no luxury."""
    t = torch.linspace(0, duration, int(sr * duration), device=DEVICE, dtype=torch.float32)
    signal = torch.zeros_like(t)
    # Raw iteration, no abstractions
    for f in freqs:
        phase = 2.0 * math.pi * f * t
        signal += torch.sin(phase)
        signal += 0.5 * torch.sin(2.0 * phase)   # 2nd harmonic, hardcoded
        signal += 0.25 * torch.sin(3.0 * phase)   # 3rd harmonic
    # Hard rectangular envelope — Rust doesn't sugarcoat
    attack = int(0.01 * sr)
    signal[:attack] *= torch.linspace(0, 1, attack, device=DEVICE).unsqueeze(0).T.squeeze()
    release = int(0.01 * sr)
    signal[-release:] *= torch.linspace(1, 0, release, device=DEVICE).unsqueeze(0).T.squeeze()
    signal = signal / (signal.abs().max() + 1e-8) * 0.7
    return signal.cpu().numpy()

def render_haskell_style(freqs, duration=5.0, sr=SR):
    """Haskell style: Lazy infinite stream of notes. Only evaluate what's needed.
    Add harmonics lazily (thunks). Curried functions compose."""
    # Build an infinite frequency stream, then take what we need
    n_samples = int(sr * duration)
    t = torch.linspace(0, duration, n_samples, device=DEVICE, dtype=torch.float32)
    signal = torch.zeros_like(t)
    
    # Lazy harmonic series — compute up to 16 harmonics but weight decays fast
    for f in freqs:
        # Fold over harmonics (like foldr)
        for h in range(1, 20):
            amp = 1.0 / (h ** 2.5)  # steep decay — Haskell is pure, quick to settle
            phase = 2.0 * math.pi * f * h * t
            # Pure sine — no side effects, no inharmonicity
            signal += amp * torch.sin(phase)
            if amp < 0.001:  # lazy — stop when contribution is negligible
                break
    
    # Smooth cosine envelope — Haskell prefers elegance
    envelope = 0.5 * (1 - torch.cos(2 * math.pi * t / duration))
    signal *= envelope
    signal = signal / (signal.abs().max() + 1e-8) * 0.7
    return signal.cpu().numpy()

def render_python_style(freqs, duration=5.0, sr=SR):
    """Python style: High-level, expressive, using libraries.
    Lots of convenience, duck typing, dynamic everything."""
    t = torch.linspace(0, duration, int(sr * duration), device=DEVICE, dtype=torch.float32)
    signal = torch.zeros_like(t)
    
    for f in freqs:
        for h in range(1, 10):  # Pythonic — range() is clear
            amp = 1.0 / (h ** 0.8)  # Python is generous
            freq = f * h * (1.0 + 0.001 * np.random.randn())  # slight randomness — Python's flexibility
            signal += amp * torch.sin(2 * math.pi * freq * t)
    
    # Expressive ADSR — Python loves named parameters
    n = len(t)
    attack = int(0.1 * sr)
    decay_time = int(0.2 * sr)
    sustain_level = 0.7
    release = int(0.8 * sr)
    sustain_len = n - attack - decay_time - release
    
    envelope = torch.cat([
        torch.linspace(0, 1, attack, device=DEVICE),
        torch.linspace(1, sustain_level, decay_time, device=DEVICE),
        torch.full((max(sustain_len, 1),), sustain_level, device=DEVICE),
        torch.linspace(sustain_level, 0, release, device=DEVICE),
    ])[:n]
    
    signal *= envelope
    signal = signal / (signal.abs().max() + 1e-8) * 0.7
    return signal.cpu().numpy()

def render_c_style(freqs, duration=5.0, sr=SR):
    """C style: Raw buffer manipulation, manual everything.
    Pointer arithmetic vibes, no safety net."""
    n_samples = int(sr * duration)
    signal = torch.zeros(n_samples, device=DEVICE, dtype=torch.float32)
    
    # Manual phase accumulator (like a DDS oscillator)
    for f in freqs:
        phase = 0.0
        phase_inc = 2.0 * math.pi * f / sr
        buf = torch.zeros(n_samples, device=DEVICE, dtype=torch.float32)
        for i in range(n_samples):
            buf[i] = math.sin(phase) + 0.3 * math.sin(2 * phase) + 0.1 * math.sin(3 * phase)
            phase += phase_inc
            if phase > 2 * math.pi:  # manual wrap
                phase -= 2 * math.pi
        signal += buf
    
    # Manual linear envelope — no library calls
    fade_in = min(int(0.05 * sr), n_samples)
    fade_out = min(int(0.3 * sr), n_samples)
    for i in range(fade_in):
        signal[i] *= i / fade_in
    for i in range(fade_out):
        signal[n_samples - 1 - i] *= i / fade_out
    
    # Manual clip (no normalize — C trusts the programmer)
    signal = torch.clamp(signal, -0.95, 0.95)
    return signal.cpu().numpy()

def experiment3():
    print("\n" + "="*70)
    print("EXPERIMENT 3: Language-Specific Music Rendering")
    print("="*70)
    
    # C major scale descending: C5 down to C4
    melody_freqs = [cents_to_freq(i * 100) for i in range(12, -1, -1)]  # C5 to C4
    # Actually use the standard C major: C D E F G A B C (descending from C5)
    major_degrees = [0, 2, 4, 5, 7, 9, 11, 12]  # semitones
    melody_freqs = [cents_to_freq((12 - d) * 100) for d in reversed(major_degrees)]  # ascending
    # Actually let's do descending
    melody_freqs = [cents_to_freq((12 + d) * 100) for d in major_degrees]  # C5 C5 D5... nah
    
    # Simpler: C major ascending, one octave, C4 to C5
    melody_freqs = [cents_to_freq(d * 100) for d in major_degrees]
    print(f"  Melody: C major ascending, {len(melody_freqs)} notes")
    print(f"  Frequencies: {[round(f,1) for f in melody_freqs]}")
    
    renderers = {
        "Rust": render_rust_style,
        "Haskell": render_haskell_style,
        "Python": render_python_style,
        "C": render_c_style,
    }
    
    results = {}
    for lang, render_fn in renderers.items():
        print(f"  🔧 Rendering in {lang} style...")
        t0 = time.time()
        
        # Each note gets equal time
        note_duration = 5.0 / len(melody_freqs)
        full_audio = np.zeros(int(SR * 5.0))
        
        for i, freq in enumerate(melody_freqs):
            start = int(i * note_duration * SR)
            end = int((i + 1) * note_duration * SR)
            note_audio = render_fn([freq], duration=note_duration)
            actual_len = min(len(note_audio), end - start)
            full_audio[start:start+actual_len] += note_audio[:actual_len]
        
        elapsed = time.time() - t0
        
        safe_name = lang.lower()
        wav_path = OUTDIR / f"exp3_{safe_name}_style.wav"
        sf.write(str(wav_path), full_audio, SR)
        
        # Analyze spectral properties
        spec_freqs, spec_power = compute_spectrogram(full_audio)
        peaks = find_peaks(spec_freqs, spec_power, n_peaks=5)
        
        # Compute spectral centroid (brightness)
        total_power = spec_power[spec_freqs > 100].sum()
        if total_power > 0:
            centroid = (spec_freqs[spec_freqs > 100] * spec_power[spec_freqs > 100]).sum() / total_power
        else:
            centroid = 0
        
        results[lang] = {
            "render_time_ms": round(elapsed * 1000, 1),
            "spectral_centroid_Hz": round(float(centroid), 1),
            "top_peaks": [(round(f,1), round(float(p),6)) for f, p in peaks],
            "audio_file": str(wav_path.name),
            "style_notes": {
                "Rust": "Zero-allocation, hard envelope, minimal harmonics, no vibrato",
                "Haskell": "Lazy harmonic evaluation, pure sines, cosine envelope, elegant decay",
                "Python": "Rich harmonics, slight randomness, expressive ADSR, generous sustain",
                "C": "Manual phase accumulator, raw buffer ops, clamp instead of normalize",
            }[lang]
        }
        print(f"     Rendered in {elapsed*1000:.0f}ms  centroid={centroid:.0f}Hz")
    
    with open(OUTDIR / "exp3_language_styles.json", "w") as f:
        json.dump({k: float(v) if hasattr(v, "item") else v for k, v in results.items()}, f, indent=2, default=str)
    print(f"\n  ✅ Saved 4 WAV files + exp3_language_styles.json")
    return results

# ═══════════════════════════════════════════════════════════════════
# EXPERIMENT 4: Conservation Law Across Traditions
# ═══════════════════════════════════════════════════════════════════

TRADITIONS = {
    "Hindustani": {
        "scales": [[0, 1, 3, 5, 7, 8, 10], [0, 2, 4, 5, 7, 9, 11], [0, 1, 3, 6, 7, 8, 11]],  # Bhairavi, Yaman, Todi-like
        "rhythm_complexity": 0.85,  # High tala complexity
        "description": "22 shrutis, raga system, complex tala cycles",
    },
    "Carnatic": {
        "scales": [[0, 1, 3, 5, 7, 8, 10], [0, 2, 3, 5, 7, 9, 10], [0, 2, 4, 5, 7, 9, 11]],
        "rhythm_complexity": 0.90,  # Very high — mridangam, konnakol
        "description": "72 melakarta ragas, sruti system, tala",
    },
    "Arabic Maqam": {
        "scales": [[0, 1, 4, 5, 7, 8, 11], [0, 1, 3, 5, 7, 8, 10], [0, 1.5, 4, 5, 7, 8, 10]],
        "rhythm_complexity": 0.75,  # Iqa'at patterns
        "description": "Quarter tones, maqam system, iqa'at rhythms",
    },
    "Turkish Makam": {
        "scales": [[0, 1, 3, 5, 7, 8, 10], [0, 2, 4, 5, 7, 9, 10], [0, 1, 4, 5, 7, 8, 11]],
        "rhythm_complexity": 0.80,  # Aksak rhythms
        "rhythm_patterns": [[1,0,0,1,0,0,1,0,0]],  # Aksak
        "description": "53-TET commas, usul rhythm cycles",
    },
    "Javanese Gamelan": {
        "scales": [[0, 1, 3, 5, 7, 8, 10], [0, 2.3, 4.6, 7, 9.3]],  # Pelog & Slendro
        "rhythm_complexity": 0.70,  # Interlocking kotekan
        "description": "Pelog (7-tone) and Slendro (5-tone), inharmonic instruments",
    },
    "Balinese Gamelan": {
        "scales": [[0, 1, 3, 5, 7, 8, 10], [0, 2.3, 4.6, 7, 9.3]],
        "rhythm_complexity": 0.80,  # Very fast interlocking
        "description": "Similar to Javanese but faster tempo, more shimmer (beating)",
    },
    "Japanese Gagaku": {
        "scales": [[0, 1, 5, 7, 8], [0, 3, 5, 7, 10]],  # In & Yo
        "rhythm_complexity": 0.40,  # Slow, free rhythm
        "description": "Pentatonic scales, ma (silence) as structural element",
    },
    "Chinese Traditional": {
        "scales": [[0, 2, 4, 7, 9], [0, 2, 4, 6, 7, 9, 11]],  # Gong & Zhi
        "rhythm_complexity": 0.50,  # Moderate — ban (beat) system
        "description": "5-tone basis (wu sheng), gongche notation",
    },
    "West African (Ewe/Dagomba)": {
        "scales": [[0, 2, 3, 5, 7, 8, 10], [0, 3, 5, 7, 10]],
        "rhythm_complexity": 0.95,  # Highest — polyrhythmic, bell patterns
        "description": "Pentatonic/heptatonic, complex polyrhythms, bell patterns",
    },
    "Western Common Practice": {
        "scales": [[0, 2, 4, 5, 7, 9, 11], [0, 2, 3, 5, 7, 8, 10], [0, 2, 3, 5, 7, 9, 10]],
        "rhythm_complexity": 0.45,  # Regular meters
        "description": "12-TET, major/minor/diatonic, regular meters",
    },
}

def compute_tradition_I_vert(scale_semitones):
    """Compute I_vert for a scale (Shannon entropy of consonance distribution)."""
    cents = torch.tensor(scale_semitones, device=DEVICE, dtype=torch.float32) * 100.0
    n = len(cents)
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            diff = (cents[j] - cents[i]) % 1200
            cs = consonance_score(diff.unsqueeze(0)).item()
            pairs.append(cs)
    
    pair_tensor = torch.tensor(pairs, device=DEVICE)
    hist = torch.histc(pair_tensor, bins=20, min=0, max=1)
    probs = hist / hist.sum()
    return shannon_entropy(probs).item()

def compute_tradition_I_horiz(rhythm_complexity, n_scales, scale_diversity=None):
    """Estimate I_horiz from rhythmic complexity and scale diversity.
    
    This is a heuristic model: I_horiz captures horizontal (temporal) information.
    More complex rhythms → higher I_horiz. More diverse scale usage → higher I_horiz.
    """
    # Base: rhythm complexity contribution
    i_horiz = rhythm_complexity * 3.5  # Scale to bits range
    
    # Scale diversity: more scales = more horizontal variation
    i_horiz += 0.3 * math.log2(max(n_scales, 1))
    
    # Add some realistic noise
    return i_horiz

def experiment4():
    print("\n" + "="*70)
    print("EXPERIMENT 4: Conservation Law Across 10 Traditions")
    print("="*70)
    
    results = {}
    i_vert_list = []
    i_horiz_list = []
    names = []
    
    for name, info in TRADITIONS.items():
        print(f"  🌏 {name}...")
        
        # Average I_vert across scales
        i_vert_vals = [compute_tradition_I_vert(s) for s in info["scales"]]
        i_vert = np.mean(i_vert_vals)
        
        # I_horiz estimate
        i_horiz = compute_tradition_I_horiz(
            info["rhythm_complexity"],
            len(info["scales"])
        )
        
        # Conservation metric: I_vert + I_horiz ≈ constant?
        total = i_vert + i_horiz
        
        i_vert_list.append(i_vert)
        i_horiz_list.append(i_horiz)
        names.append(name)
        
        results[name] = {
            "I_vert": round(i_vert, 4),
            "I_vert_per_scale": [round(v, 4) for v in i_vert_vals],
            "I_horiz": round(i_horiz, 4),
            "I_total": round(total, 4),
            "rhythm_complexity": info["rhythm_complexity"],
            "n_scales": len(info["scales"]),
            "description": info["description"],
        }
        print(f"     I_vert={i_vert:.4f}  I_horiz={i_horiz:.4f}  I_total={total:.4f}")
    
    # Analyze conservation
    totals = np.array(i_vert_list) + np.array(i_horiz_list)
    mean_total = np.mean(totals)
    std_total = np.std(totals)
    cv = std_total / mean_total if mean_total > 0 else float('inf')
    
    # Identify outliers (|deviation| > 1 std)
    outliers = []
    for i, name in enumerate(names):
        dev = totals[i] - mean_total
        if abs(dev) > std_total:
            outliers.append({
                "tradition": name,
                "I_total": round(totals[i], 4),
                "deviation": round(dev, 4),
                "direction": "above" if dev > 0 else "below",
                "reason": f"{'High rhythmic complexity with low scale tension' if dev > 0 else 'High scale tension with low rhythmic complexity'}"
            })
    
    # Correlation between I_vert and I_horiz
    if len(i_vert_list) > 2:
        correlation = np.corrcoef(i_vert_list, i_horiz_list)[0, 1]
    else:
        correlation = 0.0
    
    conservation_analysis = {
        "mean_I_total": round(mean_total, 4),
        "std_I_total": round(std_total, 4),
        "coefficient_of_variation": round(cv, 4),
        "I_vert_I_horiz_correlation": round(correlation, 4),
        "conservation_holds": bool(cv < 0.15),  # CV < 15% suggests conservation
        "outliers": outliers,
        "interpretation": (
            f"CV = {cv:.2%}. {'Conservation law holds reasonably well' if cv < 0.15 else 'Conservation is weak — traditions vary widely'}. "
            f"I_vert and I_horiz correlation = {correlation:.3f} ({'negative = tradeoff' if correlation < 0 else 'positive = reinforcement'})."
        ),
        "per_tradition": results,
        "plot_data": {
            "names": names,
            "I_vert": [round(v, 4) for v in i_vert_list],
            "I_horiz": [round(v, 4) for v in i_horiz_list],
        },
    }
    
    with open(OUTDIR / "exp4_conservation_law.json", "w") as f:
        json.dump(conservation_analysis, f, indent=2)
    
    print(f"\n  Conservation analysis:")
    print(f"    Mean I_total = {mean_total:.4f} ± {std_total:.4f}")
    print(f"    CV = {cv:.2%} → {'HOLDS' if cv < 0.15 else 'WEAK'}")
    print(f"    Correlation(I_vert, I_horiz) = {correlation:.3f}")
    print(f"    Outliers: {[o['tradition'] for o in outliers]}")
    print(f"\n  ✅ Saved exp4_conservation_law.json")
    return conservation_analysis

# ═══════════════════════════════════════════════════════════════════
# EXPERIMENT 5: Microtonal Rendering Engine
# ═══════════════════════════════════════════════════════════════════

MICROTONAL_SCALES = {
    "12-TET (reference)": {
        "cents": [i * 100.0 for i in range(12)],
        "description": "Standard Western equal temperament",
        "divisions": 12,
    },
    "19-TET": {
        "cents": [i * (1200/19) for i in range(19)],
        "description": "19-tone ET — better thirds than 12-TET, good for diatonic",
        "divisions": 19,
    },
    "31-TET": {
        "cents": [i * (1200/31) for i in range(31)],
        "description": "31-tone ET — near-just thirds and fifths, Renaissance ideal",
        "divisions": 31,
    },
    "53-TET": {
        "cents": [i * (1200/53) for i in range(53)],
        "description": "53-tone ET — excellent 5-limit just intonation approximation",
        "divisions": 53,
    },
    "Bohlen-Pierce": {
        "cents": [i * (1200 * math.log2(3) / 13) for i in range(13)],
        "description": "13-tone equal division of the tritave (3:1). NO octaves!",
        "divisions": 13,
        "tritave": True,
    },
    "Carlos Alpha": {
        "cents": [i * (1200 / (78/15)) for i in range(15)],  # 15 divisions of ~78 cent step
        "description": "Wendy Carlos alpha scale — 15 equal steps of ~78 cents (≈ 1200/15.385)",
        "divisions": 15,
    },
    "Carlos Beta": {
        "cents": [i * (1200 / 18) for i in range(18)],  # ~63.8 cent steps
        "description": "Wendy Carlos beta scale — harmonious divisions",
        "divisions": 18,
    },
    "Carlos Gamma": {
        "cents": [i * (1200 / 34) for i in range(34)],  # ~35.3 cent steps
        "description": "Wendy Carlos gamma scale — 34 divisions, very fine resolution",
        "divisions": 34,
    },
    "Partch 43-tone": {
        "cents": sorted([
            0, 21.5, 53.3, 84.5, 111.7, 150.6, 165.0,
            182.4, 203.9, 231.2, 266.9, 271.2, 294.1, 315.6,
            336.1, 386.3, 417.5, 435.1, 448.4, 470.8,
            498.0, 519.6, 551.3, 582.5, 617.5, 648.7, 680.0,
            702.0, 721.5, 764.9, 772.6, 813.7, 840.5, 857.1,
            884.4, 905.9, 933.1, 955.0, 976.5, 996.1, 1017.6,
            1035.0, 1088.3, 1158.9,
        ])[:43],
        "description": "Harry Partch's 43-tone just intonation — 11-limit monophony",
        "divisions": 43,
    },
}

def synthesize_microtonal_gpu(cents_list, duration=5.0, root=261.626):
    """Synthesize a microtonal chord with all notes sounding simultaneously."""
    freqs = [cents_to_freq(c, root) for c in cents_list]
    return synthesize_chord_gpu(freqs, duration=duration, harmonics=6, decay=0.25)

def compute_microtonal_consonance(cents_list):
    """Compute consonance field for a microtonal scale."""
    cents = torch.tensor(cents_list, device=DEVICE, dtype=torch.float32)
    n = len(cents)
    scores = []
    for i in range(n):
        for j in range(i+1, n):
            diff = (cents[j] - cents[i])
            # Handle Bohlen-Pierce tritave
            diff = diff % 1200
            cs = consonance_score(diff.unsqueeze(0)).item()
            scores.append(cs)
    if not scores:
        return {"mean": 0, "var": 0, "I_vert": 0, "n_pairs": 0}
    
    tensor = torch.tensor(scores, device=DEVICE)
    hist = torch.histc(tensor, bins=20, min=0, max=1)
    probs = hist / hist.sum()
    i_vert = shannon_entropy(probs).item()
    
    return {
        "mean": round(tensor.mean().item(), 6),
        "var": round(tensor.var().item(), 6),
        "I_vert": round(i_vert, 6),
        "n_pairs": len(scores),
    }

def experiment5():
    print("\n" + "="*70)
    print("EXPERIMENT 5: Microtonal Rendering Engine")
    print("="*70)
    
    results = {}
    
    for name, info in MICROTONAL_SCALES.items():
        cents = info["cents"]
        n = len(cents)
        print(f"  🎹 {name} ({n} notes)...")
        
        # Consonance analysis
        cons = compute_microtonal_consonance(cents)
        
        # For large scales, use a subset for synthesis (max 19 notes to keep it musical)
        if n <= 19:
            synth_cents = cents
        else:
            # Pick evenly-spaced subset
            indices = np.linspace(0, n-1, min(19, n), dtype=int)
            synth_cents = [cents[i] for i in indices]
        
        # Synthesize
        audio = synthesize_microtonal_gpu(synth_cents, duration=5.0)
        
        # Spectral analysis
        spec_freqs, spec_power = compute_spectrogram(audio)
        peaks = find_peaks(spec_freqs, spec_power, n_peaks=8)
        
        # Save
        safe_name = name.replace(" ", "_").replace("(", "").replace(")", "")
        wav_path = OUTDIR / f"exp5_{safe_name}.wav"
        sf.write(str(wav_path), audio, SR)
        
        # Compare with 12-TET
        comparison = {}
        if name != "12-TET (reference)":
            # Compute pairwise consonance difference
            ref_cons = compute_microtonal_consonance(MICROTONAL_SCALES["12-TET (reference)"]["cents"])
            comparison = {
                "vs_12TET_mean_consonance_diff": round(cons["mean"] - ref_cons["mean"], 6),
                "vs_12TET_I_vert_diff": round(cons["I_vert"] - ref_cons["I_vert"], 6),
                "more_consonant_than_12TET": cons["mean"] > ref_cons["mean"],
            }
        
        results[name] = {
            "divisions": info["divisions"],
            "n_notes": n,
            "description": info["description"],
            "tritave": info.get("tritave", False),
            "consonance": cons,
            "spectral_peaks": [(round(f,1), round(float(p),6)) for f, p in peaks],
            "comparison_with_12TET": comparison if comparison else "IS reference",
            "audio_file": str(wav_path.name),
            "synthesized_notes": len(synth_cents),
        }
        print(f"     mean_cons={cons['mean']:.4f}  I_vert={cons['I_vert']:.4f}  pairs={cons['n_pairs']}")
    
    # Summary comparison table
    print(f"\n  📊 Microtonal Consonance Comparison:")
    print(f"  {'Scale':<25} {'Notes':>5} {'Mean Cons':>10} {'I_vert':>8} {'vs 12-TET':>10}")
    print(f"  {'-'*60}")
    for name, r in results.items():
        vs = ""
        if isinstance(r["comparison_with_12TET"], dict):
            diff = r["comparison_with_12TET"]["vs_12TET_mean_consonance_diff"]
            vs = f"{'+'if diff>0 else ''}{diff:.4f}"
        print(f"  {name:<25} {r['n_notes']:>5} {r['consonance']['mean']:>10.4f} {r['consonance']['I_vert']:>8.4f} {vs:>10}")
    
    with open(OUTDIR / "exp5_microtonal_analysis.json", "w") as f:
        json.dump({k: float(v) if hasattr(v, "item") else v for k, v in results.items()}, f, indent=2, default=str)
    print(f"\n  ✅ Saved microtonal WAV files + exp5_microtonal_analysis.json")
    return results

# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🌌 GPU Experiments v3: World Traditions & Conservation")
    print(f"   Output: {OUTDIR}")
    print()
    
    torch.manual_seed(42)
    
    t_start = time.time()
    
    # Run all experiments
    print("\n" + "═"*70)
    print("STRIKING UP THE WORLD ORCHESTRA")
    print("═"*70)
    
    r1 = experiment1()
    r2 = experiment2()
    r3 = experiment3()
    r4 = experiment4()
    r5 = experiment5()
    
    # Summary
    elapsed = time.time() - t_start
    print("\n" + "═"*70)
    print(f"ALL EXPERIMENTS COMPLETE — {elapsed:.1f}s total")
    print("═"*70)
    
    # Count outputs
    wav_files = list(OUTDIR.glob("*.wav"))
    json_files = list(OUTDIR.glob("*.json"))
    print(f"\n  📁 Output: {len(wav_files)} WAV files, {len(json_files)} JSON files")
    print(f"  📂 Directory: {OUTDIR}")
    
    # Key findings
    print("\n" + "═"*70)
    print("KEY FINDINGS")
    print("═"*70)
    
    # Exp 1: Which scale has highest/lowest I_vert?
    sorted_scales = sorted(r1.items(), key=lambda x: x[1]["I_vert"])
    print(f"\n  Experiment 1 — Scale Consonance:")
    print(f"    Lowest I_vert (most uniform): {sorted_scales[0][0]} ({sorted_scales[0][1]['I_vert']:.4f})")
    print(f"    Highest I_vert (most varied):  {sorted_scales[-1][0]} ({sorted_scales[-1][1]['I_vert']:.4f})")
    
    # Exp 2: Most/least syncopated rhythm
    sorted_rhythms = sorted(r2.items(), key=lambda x: x[1]["syncopation_index"])
    print(f"\n  Experiment 2 — Rhythms:")
    print(f"    Most syncopated: {sorted_rhythms[-1][0]} ({sorted_rhythms[-1][1]['syncopation_index']:.3f})")
    print(f"    Least syncopated: {sorted_rhythms[0][0]} ({sorted_rhythms[0][1]['syncopation_index']:.3f})")
    
    # Exp 4: Conservation
    cv = r4["coefficient_of_variation"]
    print(f"\n  Experiment 4 — Conservation Law:")
    print(f"    CV = {cv:.2%} → {'HOLDS' if r4['conservation_holds'] else 'WEAK'}")
    print(f"    Correlation(I_vert, I_horiz) = {r4['I_vert_I_horiz_correlation']:.3f}")
    if r4["outliers"]:
        print(f"    Outliers: {', '.join(o['tradition'] for o in r4['outliers'])}")
    
    print(f"\n  Experiment 5 — Microtonal:")
    best = max(r5.items(), key=lambda x: x[1]["consonance"]["mean"])
    print(f"    Most consonant scale: {best[0]} (mean={best[1]['consonance']['mean']:.4f})")
    most_info = max(r5.items(), key=lambda x: x[1]["consonance"]["I_vert"])
    print(f"    Highest I_vert: {most_info[0]} (I_vert={most_info[1]['consonance']['I_vert']:.4f})")
    
    print("\n🌍 Done. The world's music, quantified on a GPU.")
