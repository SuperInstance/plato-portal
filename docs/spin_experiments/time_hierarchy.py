#!/usr/bin/env python3
"""Experiment 6: Time hierarchy — spins across all scales from Planck to cosmic."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, json

OUT = os.path.dirname(__file__)

# --- Define the hierarchy ---
levels = [
    {"name": "Planck time", "t": 5.39e-44, "color": "purple", "domain": "Quantum gravity"},
    {"name": "Nuclear (strong force)", "t": 1e-23, "color": "indigo", "domain": "Nuclear physics"},
    {"name": "Atomic (electron orbit)", "t": 1.5e-16, "color": "blue", "domain": "Atomic physics"},
    {"name": "Molecular vibration", "t": 1e-14, "color": "cyan", "domain": "Chemistry"},
    {"name": "Sound period (440 Hz)", "t": 2.27e-3, "color": "green", "domain": "Music (tone)"},
    {"name": "Musical beat (120 BPM)", "t": 0.5, "color": "limegreen", "domain": "Music (rhythm)"},
    {"name": "Musical phrase", "t": 4.0, "color": "yellow", "domain": "Music (form)"},
    {"name": "Neural oscillation (theta)", "t": 0.125, "color": "gold", "domain": "Neuroscience"},
    {"name": "Neural oscillation (alpha)", "t": 0.1, "color": "orange", "domain": "Neuroscience"},
    {"name": "Circadian rhythm", "t": 86400, "color": "orangered", "domain": "Biology"},
    {"name": "Lunar cycle", "t": 2.55e6, "color": "red", "domain": "Astronomy"},
    {"name": "Earth orbit", "t": 3.15e7, "color": "darkred", "domain": "Astronomy"},
    {"name": "Galactic rotation", "t": 7.1e15, "color": "black", "domain": "Cosmology"},
]

# --- 6a. Logarithmic timeline ---
fig, ax = plt.subplots(figsize=(14, 8))

log_times = [np.log10(l["t"]) for l in levels]
colors = [l["color"] for l in levels]
names = [l["name"] for l in levels]

for i, (lt, c, name) in enumerate(zip(log_times, colors, names)):
    ax.plot(lt, i, 'o', color=c, ms=12, zorder=5)
    ax.annotate(f'{name}\n(t = {levels[i]["t"]:.2e} s, f = {1/levels[i]["t"]:.2e} Hz)',
                (lt, i), fontsize=7, xytext=(8, 0), textcoords='offset points',
                va='center')
    ax.annotate(levels[i]["domain"], (lt, i), fontsize=6, xytext=(8, -12), 
                textcoords='offset points', va='center', color='gray')

ax.set_xlabel('log₁₀(Time / seconds)')
ax.set_ylabel('Level')
ax.set_title('Time Hierarchy: Spins at Every Scale from Planck to Galactic')
ax.set_xlim(-50, 18)
ax.grid(True, alpha=0.3)

plt.savefig(os.path.join(OUT, 'time_hierarchy.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✓ time_hierarchy.png")

# --- 6b. Spin frequency power law ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6), tight_layout=True)

log_frequencies = [np.log10(1.0 / l["t"]) for l in levels]

ax = axes[0]
ax.scatter(log_times, log_frequencies, c=range(len(levels)), cmap='rainbow', s=80, zorder=5)
ax.plot([-50, 18], [50, -18], 'k--', lw=1, alpha=0.3, label='slope = -1 (trivial: f = 1/t)')
for i, name in enumerate(names):
    ax.annotate(name.split('(')[0].strip(), (log_times[i], log_frequencies[i]),
                fontsize=6, xytext=(5, 5), textcoords='offset points')
ax.set_xlabel('log₁₀(Time / s)')
ax.set_ylabel('log₁₀(Frequency / Hz)')
ax.set_title('Spin Frequency vs Timescale\n(Every level is a "spin" at some frequency)')
ax.legend()
ax.grid(True, alpha=0.3)

# Mark neural-musical boundary
ax.axhspan(np.log10(1), np.log10(100), alpha=0.15, color='green', label='Neural-Musical boundary')
ax.annotate('Neural-Musical\nBoundary\n(r=0.862, 98%)', 
            xy=(-3, 1.5), fontsize=9, color='green',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

# --- 6c. Information density across scales ---
ax = axes[1]
# Shannon information rate ∝ bandwidth ∝ frequency
# At each level, the "information rate" is proportional to the spin frequency
info_rates = [1.0 / l["t"] for l in levels]
log_info = [np.log10(ir) for ir in info_rates]

ax.barh(range(len(levels)), log_info, color=colors, alpha=0.7)
ax.set_yticks(range(len(levels)))
ax.set_yticklabels([l["name"] for l in levels], fontsize=7)
ax.set_xlabel('log₁₀(Information rate / bits per second)')
ax.set_title('Information Rate Across Scales')

# Mark where our correlations live
ax.axvline(np.log10(10), color='green', ls='--', lw=2, alpha=0.7)
ax.annotate('Our neural-brain\ncorrelation (r=0.862)\nlives here', 
            xy=(np.log10(10), 5), fontsize=8, color='green',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

plt.savefig(os.path.join(OUT, 'time_scales_detail.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✓ time_scales_detail.png")

# --- 6d. The grand unified spin picture ---
fig, ax = plt.subplots(figsize=(14, 8))

# Concentric rings representing spin levels
max_r = 10
for i, level in enumerate(levels):
    r = max_r * (i + 1) / len(levels)
    theta = np.linspace(0, 2*np.pi, 200)
    freq = 1.0 / level["t"]
    # Number of cycles in the ring proportional to log frequency
    n_cycles = max(1, int(np.log10(freq) / 2))
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    ax.plot(x, y, color=level["color"], alpha=0.6, lw=2)
    # Mark the domain
    ax.annotate(f'{level["name"]}\n({level["domain"]})', 
                xy=(r*np.cos(np.pi/4), r*np.sin(np.pi/4)),
                fontsize=6, ha='left', color=level["color"])

# Center = singularity (pure information)
center = plt.Circle((0, 0), 0.3, color='black', fill=True)
ax.add_patch(center)
ax.annotate('CENTER = SINGULARITY\n(Pure direction/information)', (0, 0), 
            fontsize=8, ha='center', va='center', color='white', fontweight='bold')

ax.set_xlim(-11, 11)
ax.set_ylim(-11, 11)
ax.set_aspect('equal')
ax.set_title('The Grand Spin Hierarchy: From Quantum to Cosmic, Same Mathematics')
ax.axis('off')

plt.savefig(os.path.join(OUT, 'grand_spin_hierarchy.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✓ grand_spin_hierarchy.png")

# --- Save ---
results = {
    "experiment": "time_hierarchy",
    "levels": [{"name": l["name"], "time_s": l["t"], "frequency_hz": 1.0/l["t"], "domain": l["domain"]} for l in levels],
    "key_findings": {
        "neural_musical_boundary": "1-100 Hz — where our neural-brain correlation (r=0.862) and tradition recognition (98%) operate",
        "ITH_operates_at": "cultural level — years to centuries",
        "power_law": "f ∝ 1/t across ~60 orders of magnitude — same spin mathematics everywhere"
    },
    "insight": "The SAME spin mathematics (complex exponentials, Fourier decomposition) applies at every timescale from Planck time to galactic rotation. Our brain's music processing sits at the neural-musical boundary — the sweet spot where biological oscillators meet acoustic spins."
}
with open(os.path.join(OUT, 'time_hierarchy.json'), 'w') as f:
    json.dump(results, f, indent=2)

print("\n✅ Experiment 6 complete: time_hierarchy")
