#!/usr/bin/env python3
"""
GPU Visualization: The Innovation Cycle Across Music History
=============================================================
Plots the 6-phase cycle (Discovery → Codification → Ubiquity → Boredom → Rebellion → Discovery)
for 10 major Western music styles, with dial positions, cycle acceleration, technology correlation,
and phase detection. Synthesizes representative 5-second audio clips using torch (GPU/DirectML).
"""

import json
import math
import os
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from scipy.optimize import curve_fit
import soundfile as sf

try:
    import torch
    HAS_TORCH = True
    if hasattr(torch, 'directml') and torch.directml.is_available():
        DEVICE = "dml"
        print("[torch] Using DirectML GPU backend")
    elif torch.cuda.is_available():
        DEVICE = "cuda"
        print("[torch] Using CUDA GPU backend")
    else:
        DEVICE = "cpu"
        print("[torch] Using CPU backend")
except ImportError:
    HAS_TORCH = False
    DEVICE = "cpu"
    print("[torch] Not available, using numpy for audio synthesis")

# ─── Output directory ───
OUT_DIR = Path(__file__).parent / "innovation_output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_RATE = 44100
DURATION = 5.0  # seconds per clip

# ═══════════════════════════════════════════════════════════════════════════════
# 1. DATA MODEL
# ═══════════════════════════════════════════════════════════════════════════════

PHASES = [
    "Discovery",      # 1 — small community, novel
    "Codification",   # 2 — theory formalized, textbooks
    "Ubiquity",       # 3 — mainstream, commercial peak
    "Boredom",        # 4 — over-familiar, enters curricula
    "Rebellion",      # 5 — active rejection, rule-breaking
]

# Each style: name, date range, dial position (I_vert, I_horiz, I_spectral),
# phase timing (fraction of lifespan per phase), and synthesis params.
STYLES = [
    {
        "name": "Renaissance Polyphony",
        "start": 1450, "end": 1600,
        "dial": [2.0, 1.0, 1.5],
        # Phase fractions: [Discovery, Codification, Ubiquity, Boredom, Rebellion]
        "phase_fracs": [0.20, 0.30, 0.25, 0.15, 0.10],
        "synth": {"base_freq": 220, "harmonics": [1, 0.5, 0.3, 0.15, 0.08],
                  "vibrato_rate": 5.0, "vibrato_depth": 0.005,
                  "modality": "dorian", "n_voices": 4},
    },
    {
        "name": "Baroque",
        "start": 1600, "end": 1750,
        "dial": [3.0, 2.0, 1.5],
        "phase_fracs": [0.15, 0.25, 0.30, 0.15, 0.15],
        "synth": {"base_freq": 261.6, "harmonics": [1, 0.7, 0.4, 0.25, 0.12, 0.06],
                  "vibrato_rate": 6.0, "vibrato_depth": 0.008,
                  "modality": "major", "n_voices": 3},
    },
    {
        "name": "Classical",
        "start": 1750, "end": 1820,
        "dial": [2.5, 1.5, 1.5],
        "phase_fracs": [0.15, 0.25, 0.30, 0.15, 0.15],
        "synth": {"base_freq": 293.7, "harmonics": [1, 0.4, 0.15, 0.05],
                  "vibrato_rate": 4.5, "vibrato_depth": 0.003,
                  "modality": "major", "n_voices": 2},
    },
    {
        "name": "Romantic",
        "start": 1820, "end": 1900,
        "dial": [3.5, 2.0, 2.0],
        "phase_fracs": [0.15, 0.20, 0.25, 0.20, 0.20],
        "synth": {"base_freq": 220, "harmonics": [1, 0.6, 0.35, 0.2, 0.1, 0.05, 0.03],
                  "vibrato_rate": 5.5, "vibrato_depth": 0.015,
                  "modality": "minor", "n_voices": 3},
    },
    {
        "name": "Ragtime",
        "start": 1895, "end": 1920,
        "dial": [2.5, 3.5, 1.5],
        "phase_fracs": [0.15, 0.20, 0.30, 0.20, 0.15],
        "synth": {"base_freq": 261.6, "harmonics": [1, 0.5, 0.2, 0.08],
                  "vibrato_rate": 0.0, "vibrato_depth": 0.0,
                  "modality": "major", "n_voices": 2, "syncopation": True},
    },
    {
        "name": "Jazz",
        "start": 1920, "end": 1955,
        "dial": [3.5, 3.5, 2.0],
        "phase_fracs": [0.15, 0.20, 0.25, 0.20, 0.20],
        "synth": {"base_freq": 220, "harmonics": [1, 0.4, 0.2, 0.12, 0.08, 0.04],
                  "vibrato_rate": 5.0, "vibrato_depth": 0.01,
                  "modality": "blues", "n_voices": 3, "swing": True},
    },
    {
        "name": "Rock & Roll",
        "start": 1950, "end": 1975,
        "dial": [1.5, 2.5, 3.0],
        "phase_fracs": [0.10, 0.15, 0.35, 0.20, 0.20],
        "synth": {"base_freq": 164.8, "harmonics": [1, 0.8, 0.6, 0.4, 0.3, 0.2, 0.15, 0.1],
                  "vibrato_rate": 0.0, "vibrato_depth": 0.0,
                  "modality": "major", "n_voices": 1, "distortion": 0.3},
    },
    {
        "name": "Punk / New Wave",
        "start": 1975, "end": 1990,
        "dial": [0.5, 2.0, 3.5],
        "phase_fracs": [0.10, 0.10, 0.30, 0.25, 0.25],
        "synth": {"base_freq": 164.8, "harmonics": [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.5, 0.5],
                  "vibrato_rate": 0.0, "vibrato_depth": 0.0,
                  "modality": "major", "n_voices": 1, "distortion": 0.7},
    },
    {
        "name": "Hip-hop",
        "start": 1985, "end": 2015,
        "dial": [1.0, 4.0, 4.0],
        "phase_fracs": [0.15, 0.15, 0.30, 0.20, 0.20],
        "synth": {"base_freq": 82.4, "harmonics": [1, 0.3, 0.1],
                  "vibrato_rate": 0.0, "vibrato_depth": 0.0,
                  "modality": "minor", "n_voices": 1, "beat": True},
    },
    {
        "name": "AI Music",
        "start": 2020, "end": 2035,
        "dial": [4.0, 4.0, 4.0],
        "phase_fracs": [0.30, 0.25, 0.20, 0.15, 0.10],
        "synth": {"base_freq": 261.6, "harmonics": [1, 0.5, 0.33, 0.25, 0.2, 0.16, 0.14, 0.12],
                  "vibrato_rate": 7.0, "vibrato_depth": 0.02,
                  "modality": "chromatic", "n_voices": 4},
    },
]

# Technology eras and cycle lengths
TECH_ERAS = [
    {"name": "Printing Press", "start": 1450, "cycle_years": 200},
    {"name": "Sheet Music", "start": 1800, "cycle_years": 100},
    {"name": "Player Piano / Recording", "start": 1890, "cycle_years": 30},
    {"name": "Radio / TV", "start": 1925, "cycle_years": 20},
    {"name": "Internet", "start": 1995, "cycle_years": 10},
    {"name": "AI Generation", "start": 2020, "cycle_years": 5},
]


# ═══════════════════════════════════════════════════════════════════════════════
# 2. AUDIO SYNTHESIS (GPU via torch)
# ═══════════════════════════════════════════════════════════════════════════════

# Scale/mode definitions (semitone offsets from root)
SCALES = {
    "dorian":    [0, 2, 3, 5, 7, 9, 10],
    "major":     [0, 2, 4, 5, 7, 9, 11],
    "minor":     [0, 2, 3, 5, 7, 8, 10],
    "blues":     [0, 3, 5, 6, 7, 10],
    "chromatic": list(range(12)),
}


def _to_tensor(arr):
    if HAS_TORCH:
        return torch.tensor(arr, dtype=torch.float32, device=DEVICE)
    return arr


def _from_tensor(t):
    if HAS_TORCH and hasattr(t, 'cpu'):
        return t.cpu().numpy()
    return t


def generate_clip(style):
    """Synthesize a 5-second representative audio clip for a style."""
    s = style["synth"]
    n_samples = int(SAMPLE_RATE * DURATION)
    t = np.linspace(0, DURATION, n_samples, endpoint=False)

    base_freq = s["base_freq"]
    harmonics = s["harmonics"]
    vibrato_rate = s.get("vibrato_rate", 0)
    vibrato_depth = s.get("vibrato_depth", 0)
    modality = s.get("modality", "major")
    n_voices = s.get("n_voices", 1)
    syncopation = s.get("syncopation", False)
    swing = s.get("swing", False)
    distortion = s.get("distortion", 0.0)
    beat = s.get("beat", False)

    scale = SCALES.get(modality, SCALES["major"])

    # Build a melodic contour — pick notes from the scale
    np.random.seed(hash(style["name"]) % 2**31)
    n_notes = int(DURATION * 2.5)  # ~2.5 notes/sec base
    note_dur = DURATION / n_notes
    note_indices = np.random.randint(0, len(scale), size=n_notes)
    octave_shifts = np.random.choice([-12, 0, 0, 12], size=n_notes)
    midi_notes = [60 + scale[i] + o for i, o in zip(note_indices, octave_shifts)]
    freqs = [440.0 * (2 ** ((m - 69) / 12.0)) for m in midi_notes]

    # Convert to torch tensor on GPU
    t_gpu = _to_tensor(t)
    audio = _to_tensor(np.zeros(n_samples, dtype=np.float32))

    for voice in range(n_voices):
        voice_offset = voice * 4  # semitone offset for harmony
        voice_freq_mult = 2 ** (voice_offset / 12.0)
        voice_audio = _to_tensor(np.zeros(n_samples, dtype=np.float32))

        for i, freq in enumerate(freqs):
            s_start = int(i * note_dur * SAMPLE_RATE)
            s_end = min(int((i + 1) * note_dur * SAMPLE_RATE), n_samples)
            if s_start >= n_samples:
                break
            seg_len = s_end - s_start
            if seg_len <= 0:
                continue

            t_seg = t_gpu[s_start:s_end] - t_gpu[s_start]
            f = freq * voice_freq_mult

            # Vibrato
            if vibrato_rate > 0:
                mod = _to_tensor(np.sin(2 * np.pi * vibrato_rate * _from_tensor(t_seg))) * vibrato_depth * f
            else:
                mod = 0

            # Sum harmonics
            seg = _to_tensor(np.zeros(seg_len, dtype=np.float32))
            t_np = _from_tensor(t_seg)
            for h_idx, h_amp in enumerate(harmonics):
                h_num = h_idx + 1
                if vibrato_rate > 0:
                    vibrato_mod = np.sin(2 * np.pi * vibrato_rate * t_np) * vibrato_depth * f * h_num
                else:
                    vibrato_mod = 0.0
                wave = np.sin(2 * np.pi * t_np * f * h_num + vibrato_mod) * h_amp
                seg = seg + _to_tensor(wave)

            # Simple envelope
            attack = min(int(0.01 * SAMPLE_RATE), seg_len // 4)
            release = min(int(0.05 * SAMPLE_RATE), seg_len // 4)
            env = np.ones(seg_len, dtype=np.float32)
            if attack > 0:
                env[:attack] = np.linspace(0, 1, attack)
            if release > 0:
                env[-release:] = np.linspace(1, 0, release)
            seg = seg * _to_tensor(env)

            # Syncopation: randomly mute some on-beat segments
            if syncopation and i % 2 == 0 and np.random.random() < 0.3:
                seg = seg * 0.1

            # Swing: delay every other note slightly
            if swing and i % 2 == 1:
                shift = int(0.03 * SAMPLE_RATE)
                if shift < seg_len:
                    seg = _to_tensor(np.concatenate([np.zeros(shift, dtype=np.float32), _from_tensor(seg[:-shift])]))

            voice_audio[s_start:s_end] = voice_audio[s_start:s_end] + seg * (1.0 / n_voices)

        audio = audio + voice_audio * (1.0 / n_voices)

    # Distortion (soft clipping via tanh)
    if distortion > 0:
        gain = 1.0 + distortion * 5.0
        audio_np = _from_tensor(audio)
        audio = _to_tensor(np.tanh(audio_np * gain) / np.tanh(gain))

    # Beat emphasis for hip-hop
    if beat:
        beat_interval = int(0.5 * SAMPLE_RATE)  # 120 BPM
        beat_env = np.ones(n_samples, dtype=np.float32)
        for b in range(0, n_samples, beat_interval):
            attack_len = min(int(0.01 * SAMPLE_RATE), n_samples - b)
            beat_env[b:b + attack_len] = 1.3
        audio = audio * _to_tensor(beat_env)
        # Add a kick-like low freq pulse
        kick = np.zeros(n_samples, dtype=np.float32)
        for b in range(0, n_samples, beat_interval):
            klen = min(int(0.15 * SAMPLE_RATE), n_samples - b)
            t_k = np.linspace(0, 0.15, klen, endpoint=False)
            kick[b:b + klen] = np.sin(2 * np.pi * 60 * t_k * np.exp(-t_k * 20)) * 0.5
        audio = audio + _to_tensor(kick)

    # Normalize
    audio_np = _from_tensor(audio).astype(np.float32)
    peak = np.max(np.abs(audio_np))
    if peak > 0:
        audio_np = audio_np / peak * 0.8

    return audio_np


# ═══════════════════════════════════════════════════════════════════════════════
# 3. PHASE DETECTION ALGORITHM
# ═══════════════════════════════════════════════════════════════════════════════

def detect_phase(style, current_year=None):
    """
    Given a style's metrics, determine which phase it's in.
    Uses heuristic scoring based on the phase fractions and current position.
    """
    if current_year is None:
        current_year = 2026

    start = style["start"]
    end = style["end"]
    fracs = style["phase_fracs"]

    if current_year < start:
        return "Pre-Discovery", 0.0
    if current_year > end:
        # Beyond nominal end — it's in legacy/nostalgia territory
        return "Legacy / Revival", 1.0

    position = (current_year - start) / (end - start)
    cumulative = 0.0
    for i, frac in enumerate(fracs):
        cumulative += frac
        if position <= cumulative:
            progress = (position - (cumulative - frac)) / frac
            return PHASES[i], progress
    return PHASES[-1], 1.0


# ═══════════════════════════════════════════════════════════════════════════════
# 4. PLOTTING
# ═══════════════════════════════════════════════════════════════════════════════

STYLE_COLORS = [
    "#8B4513",  # Renaissance - brown
    "#DAA520",  # Baroque - goldenrod
    "#4682B4",  # Classical - steel blue
    "#8B0000",  # Romantic - dark red
    "#FFD700",  # Ragtime - gold
    "#FF8C00",  # Jazz - dark orange
    "#DC143C",  # Rock - crimson
    "#FF1493",  # Punk - deep pink
    "#8A2BE2",  # Hip-hop - blue violet
    "#00CED1",  # AI - dark turquoise
]


def plot_timeline(styles):
    """Fig 1: Historical timeline with phase bands for each style."""
    fig, ax = plt.subplots(figsize=(18, 8))

    for idx, style in enumerate(styles):
        start = style["start"]
        end = style["end"]
        lifespan = end - start
        fracs = style["phase_fracs"]
        color = STYLE_COLORS[idx]
        y = len(styles) - 1 - idx

        cumulative = 0
        phase_colors = ["#2ecc71", "#3498db", "#f1c40f", "#e67e22", "#e74c3c"]
        for p_idx, frac in enumerate(fracs):
            x_start = start + cumulative * lifespan
            x_end = start + (cumulative + frac) * lifespan
            ax.barh(y, x_end - x_start, left=x_start, height=0.7,
                    color=phase_colors[p_idx], edgecolor='white', linewidth=0.5, alpha=0.85)
            # Phase label if wide enough
            if x_end - x_start > 15:
                ax.text((x_start + x_end) / 2, y, PHASES[p_idx][:4],
                        ha='center', va='center', fontsize=6, color='black', fontweight='bold')
            cumulative += frac

        ax.text(start - 5, y, style["name"], ha='right', va='center',
                fontsize=9, fontweight='bold', color=color)

    ax.set_xlim(1400, 2040)
    ax.set_ylim(-0.5, len(styles) - 0.5)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_title("The Innovation Cycle Across Music History\n"
                 "(Green=Discovery → Blue=Codify → Yellow=Ubiquity → Orange=Boredom → Red=Rebellion)",
                 fontsize=13, fontweight='bold')
    ax.set_yticks([])

    # Technology annotations
    for tech in TECH_ERAS:
        if 1420 < tech["start"] < 2040:
            ax.axvline(tech["start"], color='gray', linestyle=':', alpha=0.4)
            ax.text(tech["start"], len(styles) - 0.3, tech["name"],
                    rotation=90, fontsize=6, color='gray', va='top', ha='right')

    plt.tight_layout()
    path = OUT_DIR / "01_timeline_phases.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  ✓ Saved {path}")


def plot_dial_positions(styles):
    """Fig 2: 3D scatter of dial positions (I_vert, I_horiz, I_spectral)."""
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    for idx, style in enumerate(styles):
        iv, ih, is_ = style["dial"]
        ax.scatter(iv, ih, is_, c=STYLE_COLORS[idx], s=120, edgecolors='black',
                   linewidth=0.5, zorder=5)
        ax.text(iv + 0.1, ih + 0.1, is_ + 0.1, style["name"],
                fontsize=7, color=STYLE_COLORS[idx])

    # Draw arrows connecting styles chronologically
    for i in range(len(styles) - 1):
        iv1, ih1, is1 = styles[i]["dial"]
        iv2, ih2, is2 = styles[i + 1]["dial"]
        ax.plot([iv1, iv2], [ih1, ih2], [is1, is2], 'k-', alpha=0.3, linewidth=1)

    ax.set_xlabel("I_vertical (Harmonic Complexity)", fontsize=10)
    ax.set_ylabel("I_horizontal (Rhythmic Complexity)", fontsize=10)
    ax.set_zlabel("I_spectral (Timbral Novelty)", fontsize=10)
    ax.set_title("Dial Positions Across Music Styles\n"
                 "(Arrows show chronological evolution)", fontsize=12, fontweight='bold')
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_zlim(0, 5)

    plt.tight_layout()
    path = OUT_DIR / "02_dial_positions.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  ✓ Saved {path}")


def plot_acceleration(styles):
    """Fig 3: Cycle acceleration curve with exponential fit."""
    # Time between Discovery phases
    discovery_years = [s["start"] for s in styles]
    intervals = []
    interval_labels = []
    for i in range(1, len(discovery_years)):
        gap = discovery_years[i] - discovery_years[i - 1]
        intervals.append(gap)
        interval_labels.append(f"{styles[i-1]['name'][:12]}→{styles[i]['name'][:12]}")

    # Discovery number (1-indexed)
    x_data = np.arange(1, len(intervals) + 1, dtype=float)
    y_data = np.array(intervals, dtype=float)

    # Fit exponential: y = a * e^(b*x)
    def exp_decay(x, a, b):
        return a * np.exp(-b * x)

    try:
        popt, _ = curve_fit(exp_decay, x_data, y_data, p0=[200, 0.3], maxfev=5000)
        a_fit, b_fit = popt
        fit_label = f"y = {a_fit:.0f} · e^(-{b_fit:.3f}x)"
    except Exception:
        a_fit, b_fit = 200, 0.3
        fit_label = "Fit failed"

    x_smooth = np.linspace(0.5, len(intervals) + 3, 200)
    y_fit = exp_decay(x_smooth, a_fit, b_fit)

    # Predict when AI music gets replaced
    # Find where the curve drops to < 2 years
    replacement_interval = max(exp_decay(len(intervals) + 1, a_fit, b_fit), 1.0)
    ai_discovery = 2020
    predicted_replacement_year = ai_discovery + replacement_interval

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Left: Bar chart of intervals
    colors_bar = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(intervals)))
    bars = ax1.bar(range(len(intervals)), intervals, color=colors_bar, edgecolor='black', linewidth=0.5)
    ax1.set_xticks(range(len(intervals)))
    ax1.set_xticklabels(interval_labels, rotation=45, ha='right', fontsize=7)
    ax1.set_ylabel("Years Between Discovery Phases")
    ax1.set_title("Cycle Acceleration: Time Between Innovation Waves", fontweight='bold')
    for bar, val in zip(bars, intervals):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                 f"{val:.0f}yr", ha='center', fontsize=8, fontweight='bold')

    # Right: Exponential fit
    ax2.plot(x_data, y_data, 'ro', markersize=10, label="Observed intervals")
    ax2.plot(x_smooth, y_fit, 'b--', linewidth=2, label=fit_label)
    ax2.axhline(y=replacement_interval, color='green', linestyle=':', alpha=0.7)
    ax2.text(len(intervals) + 0.5, replacement_interval + 3,
             f"Predicted next cycle: {replacement_interval:.0f} years\n"
             f"→ AI music replaced by ~{predicted_replacement_year:.0f}",
             fontsize=9, color='green', fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    ax2.set_xlabel("Cycle Number")
    ax2.set_ylabel("Interval (years)")
    ax2.set_title("Exponential Acceleration of Musical Innovation", fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    path = OUT_DIR / "03_acceleration.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  ✓ Saved {path}")

    return predicted_replacement_year, replacement_interval


def plot_tech_correlation():
    """Fig 4: Technology correlation — reproductive tech vs cycle length."""
    fig, ax = plt.subplots(figsize=(12, 6))

    years = [t["start"] for t in TECH_ERAS]
    cycles = [t["cycle_years"] for t in TECH_ERAS]
    names = [t["name"] for t in TECH_ERAS]

    # Log scale for cycle length
    ax.semilogy(years, cycles, 'bo-', markersize=10, linewidth=2)

    for x, y, name in zip(years, cycles, names):
        ax.annotate(name, (x, y), textcoords="offset points",
                    xytext=(10, 10), fontsize=9,
                    arrowprops=dict(arrowstyle='->', color='gray'),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.8))

    ax.set_xlabel("Year of Technology Introduction", fontsize=11)
    ax.set_ylabel("Innovation Cycle Length (years)", fontsize=11)
    ax.set_title("Reproductive Technology ↔ Musical Innovation Cycle Speed\n"
                 "Each new reproduction technology halves the cycle time", fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, which='both')
    ax.set_xlim(1400, 2035)
    ax.set_ylim(2, 300)

    plt.tight_layout()
    path = OUT_DIR / "04_technology_correlation.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  ✓ Saved {path}")


def plot_phase_radar(styles):
    """Fig 5: Radar/spider chart showing phase distribution per style."""
    n_phases = len(PHASES)
    angles = np.linspace(0, 2 * np.pi, n_phases, endpoint=False).tolist()
    angles += angles[:1]  # close the polygon

    fig, axes = plt.subplots(2, 5, figsize=(20, 8), subplot_kw=dict(polar=True))
    axes = axes.flatten()

    for idx, style in enumerate(styles):
        ax = axes[idx]
        fracs = style["phase_fracs"] + [style["phase_fracs"][0]]  # close
        ax.fill(angles, fracs, alpha=0.25, color=STYLE_COLORS[idx])
        ax.plot(angles, fracs, 'o-', color=STYLE_COLORS[idx], linewidth=2, markersize=5)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([p[:5] for p in PHASES], fontsize=6)
        ax.set_title(style["name"], fontsize=8, fontweight='bold', pad=15, color=STYLE_COLORS[idx])
        ax.set_ylim(0, 0.4)
        ax.set_yticks([0.1, 0.2, 0.3])
        ax.set_yticklabels(['10%', '20%', '30%'], fontsize=5)

    fig.suptitle("Phase Duration Distribution per Style\n"
                 "(How long each style spends in each innovation phase)",
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    path = OUT_DIR / "05_phase_radar.png"
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  ✓ Saved {path}")


def plot_phase_detection(styles):
    """Fig 6: Current phase detection snapshot (2026)."""
    fig, ax = plt.subplots(figsize=(14, 7))

    phase_colors_map = {
        "Discovery": "#2ecc71",
        "Codification": "#3498db",
        "Ubiquity": "#f1c40f",
        "Boredom": "#e67e22",
        "Rebellion": "#e74c3c",
        "Pre-Discovery": "#bdc3c7",
        "Legacy / Revival": "#9b59b6",
    }

    for idx, style in enumerate(styles):
        phase, progress = detect_phase(style, 2026)
        y = len(styles) - 1 - idx
        color = phase_colors_map.get(phase, "#95a5a6")

        # Draw background bar
        ax.barh(y, 1.0, height=0.6, color='#ecf0f1', edgecolor='gray', linewidth=0.5)
        # Draw progress bar
        ax.barh(y, progress, height=0.6, color=color, edgecolor='gray', linewidth=0.5, alpha=0.8)

        label = f"{style['name']}  —  {phase} ({progress:.0%})"
        ax.text(-0.02, y, label, ha='right', va='center', fontsize=9,
                fontweight='bold', color=STYLE_COLORS[idx])

    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.5, len(styles) - 0.5)
    ax.set_title("Phase Detection Snapshot: 2026\n"
                 "Where each style is in the innovation cycle right now",
                 fontsize=12, fontweight='bold')
    ax.set_xlabel("Phase Progress")
    ax.set_yticks([])

    # Legend
    patches = [mpatches.Patch(color=c, label=l) for l, c in phase_colors_map.items()]
    ax.legend(handles=patches, loc='lower right', fontsize=8, ncol=2)

    plt.tight_layout()
    path = OUT_DIR / "06_phase_detection_2026.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  ✓ Saved {path}")


# ═══════════════════════════════════════════════════════════════════════════════
# 5. MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  Innovation Cycle: GPU Music History Visualization")
    print("=" * 60)

    # ── Generate audio clips ──
    print("\n♪ Synthesizing representative audio clips...")
    audio_data = {}
    for style in STYLES:
        name = style["name"]
        safe = name.lower().replace(" ", "_").replace("/", "-").replace("&", "and")
        wav_path = OUT_DIR / f"clip_{safe}.wav"
        print(f"  Generating: {name}...", end=" ", flush=True)
        clip = generate_clip(style)
        sf.write(str(wav_path), clip, SAMPLE_RATE)
        audio_data[name] = str(wav_path)
        print(f"✓ ({wav_path.name})")

    # ── Phase detection ──
    print("\n Phase Detection (2026):")
    phase_results = {}
    for style in STYLES:
        phase, progress = detect_phase(style, 2026)
        phase_results[style["name"]] = {"phase": phase, "progress": round(progress, 3)}
        print(f"  {style['name']:25s} → {phase:20s} ({progress:.0%})")

    # ── Generate plots ──
    print("\n📊 Generating visualizations...")
    plot_timeline(STYLES)
    plot_dial_positions(STYLES)
    predicted_year, predicted_interval = plot_acceleration(STYLES)
    plot_tech_correlation()
    plot_phase_radar(STYLES)
    plot_phase_detection(STYLES)

    # ── Assemble JSON output ──
    output = {
        "metadata": {
            "title": "Innovation Cycle Across Music History",
            "generated": "2026-05-24",
            "device": DEVICE,
        },
        "styles": [],
        "technology_eras": TECH_ERAS,
        "phase_detection_2026": phase_results,
        "acceleration": {
            "fit": f"y = {200:.0f} · e^(-0.3x)",
            "observed_intervals": {
                f"{STYLES[i]['name']} → {STYLES[i+1]['name']}": STYLES[i+1]["start"] - STYLES[i]["start"]
                for i in range(len(STYLES) - 1)
            },
            "predicted_next_replacement": {
                "interval_years": round(predicted_interval, 1),
                "predicted_year": round(predicted_year),
                "note": "Based on exponential acceleration fit; AI music may be disrupted sooner or later"
            }
        },
        "audio_clips": audio_data,
    }

    for style in STYLES:
        output["styles"].append({
            "name": style["name"],
            "start": style["start"],
            "end": style["end"],
            "dial": {
                "I_vertical": style["dial"][0],
                "I_horizontal": style["dial"][1],
                "I_spectral": style["dial"][2],
            },
            "phase_fractions": {
                PHASES[i]: style["phase_fracs"][i] for i in range(5)
            },
            "phase_2026": phase_results[style["name"]],
        })

    json_path = OUT_DIR / "innovation_data.json"
    with open(json_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\n  ✓ Saved {json_path}")

    print("\n" + "=" * 60)
    print(f"  Done! All outputs in {OUT_DIR}/")
    print(f"  6 visualizations + {len(STYLES)} audio clips + JSON data")
    print(f"  Predicted AI music disruption: ~{predicted_year:.0f} (every {predicted_interval:.0f} years)")
    print("=" * 60)


if __name__ == "__main__":
    main()
