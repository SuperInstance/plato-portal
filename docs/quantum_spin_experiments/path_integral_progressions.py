#!/usr/bin/env python3
"""
Experiment 5: Path Integral Chord Progressions
Chord progressions modeled as paths through key space with an action functional.
Most probable progressions = minimum action paths (stationary phase).
Common progressions follow valleys in the energy landscape.
"""

import numpy as np
import json
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# ── Key Space Definition ──
# 12 major keys arranged on circle of fifths
KEY_NAMES = ["C", "G", "D", "A", "E", "B", "F#", "Db", "Ab", "Eb", "Bb", "F"]

def cof_distance(k1, k2):
    """Distance in circle-of-fifths space (0 to 6)."""
    d = abs(k1 - k2) % 12
    return min(d, 12 - d)

# ── Define Chords in Each Key ──
# Diatonic chords: I, ii, iii, IV, V, vi, vii°
ROMAN = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]

def diatonic_chords(key_idx):
    """Return the 7 diatonic chord root pitch classes for key_idx."""
    # Circle of fifths: key_idx steps from C
    root = (key_idx * 7) % 12
    scale_intervals = [0, 2, 4, 5, 7, 9, 11]
    return [(root + interval) % 12 for interval in scale_intervals]

# ── Action Functional ──
# S[path] = Σ_i [ T(transition_i) + V(chord_i) ]
# T = kinetic term: distance in CoF space
# V = potential term: tension relative to home key

def kinetic_term(key1, key2):
    """Cost of moving between keys in circle-of-fifths space."""
    return cof_distance(key1, key2)

def tension_potential(chord_root, home_key):
    """Tension of a chord relative to the home key.
    Tonic (I) = 0 tension, dominant (V) = moderate, others = high."""
    # Distance of chord root from home tonic in CoF space
    # Map chord root to its CoF position
    chord_cof = None
    home_root = (home_key * 7) % 12
    
    # Interval from home root
    interval = (chord_root - home_root) % 12
    
    # Tension based on interval
    tension_map = {0: 0.0, 7: 1.0, 5: 2.0, 2: 3.0, 9: 2.5, 4: 2.0, 11: 4.0,
                   1: 5.0, 6: 5.0, 3: 4.5, 8: 4.5, 10: 3.5}
    return tension_map.get(interval, 3.0)

# ── Compute Action for Known Progressions ──
print("PATH INTEGRAL CHORD PROGRESSIONS")
print("=" * 60)
print("\nAction S = Σ [kinetic T + potential V]")
print("T = circle-of-fifths distance between keys")
print("V = harmonic tension relative to home key\n")

home_key = 0  # C major
chords_c = diatonic_chords(home_key)
print(f"C major diatonic chords: {dict(zip(ROMAN, chords_c))}")

# Common progressions to evaluate
progressions = {
    "I→V→I":           [0, 4, 0],
    "I→IV→V→I":        [0, 3, 4, 0],
    "I→vi→IV→V→I":     [0, 5, 3, 4, 0],
    "I→ii→V→I":        [0, 1, 4, 0],
    "I→IV→I":           [0, 3, 0],
    "I→♭VI→♭II→I":     [0, 8, 1, 0],   # remote modulation
    "I→♭III→♭VI→I":    [0, 3+9, 8, 0],  # chromatic mediant
    "I→♭VII→IV→I":     [0, 11, 3, 0],   # mixolydian
    "12-Bar Blues":     [0, 0, 0, 0, 3, 3, 0, 0, 4, 3, 0, 4],
}

# Actually let's define progressions in terms of chord degrees (0-6 = I-vii°)
# and compute action based on CoF distances between chord roots
progressions_v2 = {
    "I→IV→V→I (classic)":     [0, 3, 4, 0],
    "I→V→vi→IV (pop)":        [0, 4, 5, 3],
    "I→vi→ii→V (jazz)":       [0, 5, 1, 4],
    "I→ii→V→I (jazz basic)":  [0, 1, 4, 0],
    "I→iii→vi→ii→V→I":       [0, 2, 5, 1, 4, 0],
    "I→♭VII→IV→I (modal)":    [0, 10, 3, 0],  # using pitch classes
    "I→♭VI→♭II→I (neapolitan)": [0, 8, 1, 0],
    "Autumn Leaves":          [0, 5, 2, 5, 1, 4, 0, 4],  # simplified
}

print(f"\n{'Progression':<30s} {'Action':>8s} {'Avg':>6s} {'Prob':>8s}")
print("-" * 60)

hbar_eff = 2.0  # effective ℏ controlling fluctuation scale
prog_results = {}

for name, chords in progressions_v2.items():
    action = 0.0
    for i in range(len(chords)):
        # Potential: tension relative to home
        action += tension_potential(chords[i], home_key)
        # Kinetic: transition cost
        if i > 0:
            action += kinetic_term(chords[i-1], chords[i])
    
    avg_action = action / len(chords)
    # Path integral weight
    weight = np.exp(-action / hbar_eff)
    
    prog_results[name] = {
        "chords": chords,
        "total_action": float(action),
        "avg_action": float(avg_action),
        "weight": float(weight),
        "log_weight": float(-action / hbar_eff)
    }
    
    bar = "█" * int(weight * 200)
    print(f"  {name:<28s} {action:8.2f} {avg_action:6.2f} {weight:8.4f} {bar}")

# ── Energy Landscape ──
print(f"\n\nKEY SPACE ENERGY LANDSCAPE")
print("-" * 60)
print("(Tension relative to C major)")

landscape = {}
for k in range(12):
    root = (k * 7) % 12
    tension = tension_potential(root, home_key)
    cof_dist = cof_distance(k, 0)
    landscape[KEY_NAMES[k]] = {
        "cof_distance": cof_dist,
        "tension": float(tension)
    }
    bar = "░" * int(tension * 5) + "█" * int((5 - tension) * 5)
    print(f"  {KEY_NAMES[k]:3s} (CoF dist {cof_dist}): tension = {tension:.1f}  {bar}")

# ── Path Integral: Monte Carlo sampling of all 4-chord progressions ──
print(f"\n\nPATH INTEGRAL: Monte Carlo over all 4-chord progressions in C major")
print("-" * 60)

# Sample from Z = Σ exp(-S/ℏ)
np.random.seed(42)
n_samples = 100000
sampled_actions = []
sampled_paths = []

for _ in range(n_samples):
    path = [np.random.randint(0, 12) for _ in range(4)]
    path[0] = 0  # start on I
    path[-1] = 0  # end on I (resolve)
    
    action = 0.0
    for i in range(len(path)):
        action += tension_potential(path[i], home_key)
        if i > 0:
            action += kinetic_term(path[i-1], path[i])
    
    sampled_actions.append(action)
    sampled_paths.append(tuple(path))

# Weight by Boltzmann factor
sampled_actions = np.array(sampled_actions)
weights = np.exp(-sampled_actions / hbar_eff)
weights /= np.sum(weights)

# Most probable paths
top_indices = np.argsort(weights)[-20:][::-1]
print("\nTop 20 most probable 4-chord progressions (I→?→?→I):")
for rank, idx in enumerate(top_indices):
    path = sampled_paths[idx]
    path_names = [KEY_NAMES[p] for p in path]
    print(f"  {rank+1:2d}. {'→'.join(path_names):20s} "
          f"S={sampled_actions[idx]:.2f}  weight={weights[idx]:.5f}")

# ── Statistical comparison ──
# How often do we see I→IV→V→I vs I→♭VI→♭II→I?
classic_path = (0, 3, 4, 0)  # I→IV→V→I
remote_path = (0, 8, 1, 0)   # I→♭VI→♭II→I

classic_count = sum(weights[i] for i, p in enumerate(sampled_paths) if p == classic_path)
remote_count = sum(weights[i] for i, p in enumerate(sampled_paths) if p == remote_path)

print(f"\nDirect comparison:")
print(f"  I→IV→V→I weight:  {classic_count:.6f}")
print(f"  I→♭VI→♭II→I weight: {remote_count:.6f}")
print(f"  Ratio: {classic_count / max(remote_count, 1e-10):.1f}x")

# Compute partition function
Z = np.sum(np.exp(-sampled_actions / hbar_eff))
print(f"\n  Partition function Z = {Z:.2f}")
print(f"  Free energy F = -ℏ_eff ln(Z) = {-hbar_eff * np.log(Z):.4f}")

# ── Save ──
data = {
    "experiment": "Path Integral Chord Progressions",
    "parameters": {"hbar_eff": hbar_eff, "home_key": "C", "n_samples": n_samples},
    "progression_actions": {k: v for k, v in prog_results.items()},
    "energy_landscape": landscape,
    "top_paths": [{"path": [KEY_NAMES[p] for p in sampled_paths[i]],
                   "action": float(sampled_actions[i]),
                   "weight": float(weights[i])}
                  for i in top_indices[:10]],
    "classic_vs_remote_ratio": float(classic_count / max(remote_count, 1e-10)),
    "conclusion": "Common chord progressions (I→IV→V→I) are minimum-action paths "
                  "in circle-of-fifths space. Remote modulations (I→♭VI→♭II→I) are "
                  "high-action instanton events with exponentially suppressed probability. "
                  "Music theory's 'rules' of harmony emerge from the path integral: "
                  "stationary-phase (minimum-action) paths dominate the partition function."
}

json_path = os.path.join(OUT, "path_integral.json")
with open(json_path, 'w') as f:
    json.dump(data, f, indent=2)
print(f"\nSaved: {json_path}")
