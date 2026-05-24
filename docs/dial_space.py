#!/usr/bin/env python3
"""
DIAL SPACE VISUALIZER — Interactive Parameter Space Explorer
Implements the "dials not laws" insight: musical styles as points in (I_vert, I_horiz, I_spectral) space.

Outputs:
  - dial_space.json   (tradition positions, clusters, hull, empty regions)
  - transition_*.wav  (interpolation paths between select tradition pairs)
  - random_baseline.json (statistical comparison vs random)
  - unexplored_regions.json (coordinates of unexplored dial positions)
"""

import json
import os
import numpy as np
from scipy.spatial import ConvexHull, Delaunay
from scipy.spatial.distance import cdist
from scipy.stats import permutation_test
from sklearn.cluster import KMeans
import soundfile as sf

# ── Output directory ──────────────────────────────────────────────
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dial_output")
os.makedirs(OUT, exist_ok=True)

# ── Tradition Data ────────────────────────────────────────────────
TRADITIONS = {
    "Hindustani":   {"I_vert": 2.77, "I_horiz": 3.45, "I_spectral": 2.5},
    "Carnatic":     {"I_vert": 2.77, "I_horiz": 3.63, "I_spectral": 2.8},
    "Arabic":       {"I_vert": 2.94, "I_horiz": 3.10, "I_spectral": 2.3},
    "Turkish":      {"I_vert": 2.83, "I_horiz": 3.28, "I_spectral": 2.2},
    "Javanese":     {"I_vert": 2.31, "I_horiz": 2.75, "I_spectral": 3.0},
    "Balinese":     {"I_vert": 2.31, "I_horiz": 3.10, "I_spectral": 3.2},
    "Gagaku":       {"I_vert": 2.38, "I_horiz": 1.70, "I_spectral": 3.5},
    "Chinese":      {"I_vert": 2.32, "I_horiz": 2.05, "I_spectral": 2.0},
    "West African": {"I_vert": 2.41, "I_horiz": 3.63, "I_spectral": 2.6},
    "Western ET":   {"I_vert": 2.72, "I_horiz": 2.05, "I_spectral": 1.8},
}

names = list(TRADITIONS.keys())
points = np.array([[v["I_vert"], v["I_horiz"], v["I_spectral"]] for v in TRADITIONS.values()])


# ── 1. Cluster Detection (K-Means) ──────────────────────────────
def find_clusters(pts, names, k_range=(2, 5)):
    """Try multiple k values, return best by silhouette."""
    from sklearn.metrics import silhouette_score
    results = {}
    for k in range(k_range[0], k_range[1] + 1):
        km = KMeans(n_clusters=k, n_init=20, random_state=42)
        labels = km.fit_predict(pts)
        sil = silhouette_score(pts, labels) if k < len(pts) else -1
        results[k] = {"labels": labels.tolist(), "silhouette": float(sil), "centers": km.cluster_centers_.tolist()}
    best_k = max(results, key=lambda k: results[k]["silhouette"])
    return best_k, results


# ── 2. Convex Hull ───────────────────────────────────────────────
def compute_hull(pts):
    """Compute convex hull of tradition points."""
    hull = ConvexHull(pts)
    return {
        "vertices": hull.vertices.tolist(),
        "volume": float(hull.volume),
        "area": float(hull.area),
        "simplices": hull.simplices.tolist(),
        "vertex_coords": pts[hull.vertices].tolist(),
        "vertex_names": [names[i] for i in hull.vertices],
    }


# ── 3. Random Baseline ──────────────────────────────────────────
def random_baseline(pts, n_random=10000, n_iter=1000):
    """Compare observed clustering to random point distributions."""
    rng = np.random.default_rng(42)
    lo, hi = pts.min(axis=0), pts.max(axis=0)

    random_pts = rng.uniform(lo, hi, size=(n_random, len(lo)))

    # Mean nearest-neighbor distance for traditions
    from scipy.spatial.distance import pdist
    obs_mean_dist = float(np.mean(pdist(pts)))

    # Random baselines: sample 10 points many times, compute mean pairwise dist
    rand_dists = []
    for _ in range(n_iter):
        sample = rng.uniform(lo, hi, size=(len(pts), len(lo)))
        rand_dists.append(float(np.mean(pdist(sample))))
    rand_dists = np.array(rand_dists)

    # p-value: fraction of random samples with >= observed mean distance
    p_value = float(np.mean(rand_dists >= obs_mean_dist))

    # Also check nearest-neighbor distance
    obs_nn = float(np.mean(np.min(cdist(pts, pts) + np.eye(len(pts)) * 999, axis=1)))
    rand_nn = []
    for _ in range(n_iter):
        sample = rng.uniform(lo, hi, size=(len(pts), len(lo)))
        d = cdist(sample, sample) + np.eye(len(pts)) * 999
        rand_nn.append(float(np.mean(np.min(d, axis=1))))
    rand_nn = np.array(rand_nn)
    p_nn = float(np.mean(rand_nn <= obs_nn))

    return {
        "observed_mean_pairwise_dist": obs_mean_dist,
        "random_mean_pairwise_dist_mean": float(rand_dists.mean()),
        "random_mean_pairwise_dist_std": float(rand_dists.std()),
        "p_value_pairwise": p_value,
        "observed_mean_nn_dist": obs_nn,
        "random_mean_nn_dist_mean": float(rand_nn.mean()),
        "random_mean_nn_dist_std": float(rand_nn.std()),
        "p_value_nn": p_nn,
        "conclusion": "Traditions cluster MORE than random (nn p={:.3f})".format(p_nn) if p_nn < 0.05
                      else "Traditions do NOT significantly cluster beyond random",
        "n_random_points": n_random,
        "n_permutations": n_iter,
    }


# ── 4. Unexplored Regions ───────────────────────────────────────
def find_unexplored(pts, n_grid=30):
    """Find the largest empty regions inside the bounding box but outside the convex hull."""
    lo = pts.min(axis=0) - 0.1
    hi = pts.max(axis=0) + 0.1

    # Grid sample the space
    grid = np.mgrid[
        lo[0]:hi[0]:complex(n_grid),
        lo[1]:hi[1]:complex(n_grid),
        lo[2]:hi[2]:complex(n_grid),
    ].reshape(3, -1).T

    # Points inside convex hull
    hull = ConvexHull(pts)
    delaunay = Delaunay(pts[hull.vertices])
    inside = delaunay.find_simplex(grid) >= 0

    # For each grid point, compute distance to nearest tradition
    dists = np.min(cdist(grid, pts), axis=1)

    # Among points inside hull, find the ones farthest from any tradition
    inside_dists = dists.copy()
    inside_dists[~inside] = -1

    # Also find points outside hull but within bounding box — these are completely unexplored
    outside = ~inside
    outside_pts = grid[outside]

    # Top 10 emptiest interior points
    top_interior_idx = np.argsort(inside_dists)[-10:][::-1]
    emptiest_interior = grid[top_interior_idx].tolist()
    emptiest_interior_dists = inside_dists[top_interior_idx].tolist()

    # Sample of unexplored exterior points (random 20)
    rng = np.random.default_rng(42)
    if len(outside_pts) > 20:
        ext_sample = rng.choice(len(outside_pts), 20, replace=False)
        unexplored_exterior = outside_pts[ext_sample].tolist()
    else:
        unexplored_exterior = outside_pts.tolist()

    # Largest empty sphere (center, radius)
    best_idx = np.argmax(inside_dists)
    empty_center = grid[best_idx].tolist()
    empty_radius = float(inside_dists[best_idx])

    return {
        "largest_empty_sphere": {
            "center": empty_center,
            "radius": empty_radius,
            "interpretation": "Dial position farthest from all known traditions (inside explored region)"
        },
        "emptiest_interior_points": [
            {"coords": c, "min_dist_to_tradition": d}
            for c, d in zip(emptiest_interior, emptiest_interior_dists)
        ],
        "unexplored_exterior_sample": unexplored_exterior,
        "hull_volume": float(hull.volume),
        "bounding_box_volume": float(np.prod(hi - lo)),
        "fill_fraction": float(hull.volume / np.prod(hi - lo)),
    }


# ── 5. Dial-Based Audio Synthesis ────────────────────────────────
SR = 22050  # sample rate

def synthesize_from_dials(I_vert, I_horiz, I_spectral, duration=10.0):
    """
    Synthesize audio from dial positions:
      I_vert    → scale density (high=chromatic many notes, low=pentatonic few)
      I_horiz   → rhythmic complexity (high=syncopated, low=even pulse)
      I_spectral→ timbral richness (high=many partials, low=pure tone)
    """
    t = np.linspace(0, duration, int(SR * duration), endpoint=False)
    rng = np.random.default_rng(42)

    # ── Scale from I_vert ──
    # Map I_vert range [2.3, 3.0] → [5, 12] notes per octave
    n_notes = int(np.interp(I_vert, [2.3, 3.0], [5, 12]))
    base_freq = 220.0  # A3
    # Generate scale: equal divisions of the octave + slight random detuning
    scale_ratios = np.sort(rng.uniform(1.0, 2.0, n_notes))
    scale_ratios = np.concatenate([[1.0], scale_ratios])  # include root
    scale_freqs = base_freq * scale_ratios

    # ── Rhythm from I_horiz ──
    # Map I_horiz [1.7, 3.7] → bpm + syncopation
    bpm = np.interp(I_horiz, [1.7, 3.7], [60, 180])
    beat_len = 60.0 / bpm
    # Number of attacks
    n_attacks = int(duration / beat_len)
    # Syncopation: higher I_horiz → more offbeat placement
    syncopation = np.interp(I_horiz, [1.7, 3.7], [0.0, 0.4])
    attack_times = np.array([i * beat_len + rng.uniform(-syncopation * beat_len, syncopation * beat_len)
                             for i in range(n_attacks)])
    attack_times = np.clip(attack_times, 0, duration - 0.5)

    # ── Timbre from I_spectral ──
    # Map I_spectral [1.8, 3.5] → [1, 8] harmonics
    n_harmonics = int(np.interp(I_spectral, [1.8, 3.5], [1, 8]))
    harmonic_decay = np.interp(I_spectral, [1.8, 3.5], [0.7, 0.3])  # higher richness → slower harmonic decay

    # ── Build audio ──
    audio = np.zeros_like(t)
    envelope_len = int(0.15 * SR)  # 150ms envelope

    for atk_time in attack_times:
        # Pick a note from the scale
        freq = rng.choice(scale_freqs)
        atk_sample = int(atk_time * SR)

        # Generate harmonic content
        for h in range(1, n_harmonics + 1):
            amp = harmonic_decay ** (h - 1)
            freq_h = freq * h
            if freq_h > SR / 2:
                break
            tone = amp * np.sin(2 * np.pi * freq_h * t)

            # Apply envelope at attack point
            env = np.ones_like(t)
            # Attack ramp
            start = atk_sample
            end_attack = min(start + envelope_len, len(t))
            if start < len(t):
                env[:start] = 0
                if start < end_attack:
                    env[start:end_attack] = np.linspace(0, 1, end_attack - start)
                # Decay over ~0.5 seconds
                decay_len = int(0.5 * SR)
                decay_start = end_attack
                decay_end = min(decay_start + decay_len, len(t))
                if decay_start < decay_end:
                    env[decay_start:decay_end] = np.linspace(1, 0, decay_end - decay_start)
                env[decay_end:] = 0

            audio += tone * env

    # Normalize
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak * 0.8

    return audio.astype(np.float32)


def generate_transition(name_a, name_b, n_steps=5, duration_each=2.0):
    """Generate audio interpolating between two traditions' dial positions."""
    a = np.array([TRADITIONS[name_a]["I_vert"], TRADITIONS[name_a]["I_horiz"], TRADITIONS[name_a]["I_spectral"]])
    b = np.array([TRADITIONS[name_b]["I_vert"], TRADITIONS[name_b]["I_horiz"], TRADITIONS[name_b]["I_spectral"]])

    audio_segments = []
    for i in range(n_steps):
        alpha = i / (n_steps - 1)
        pos = a * (1 - alpha) + b * alpha
        seg = synthesize_from_dials(pos[0], pos[1], pos[2], duration=duration_each)
        # Crossfade
        fade = int(0.05 * SR)
        if i > 0 and len(audio_segments) > 0:
            # Overlap last `fade` samples
            overlap = min(fade, len(audio_segments), len(seg))
            audio_segments[-overlap:] = audio_segments[-overlap:] * np.linspace(1, 0, overlap) + \
                                         seg[:overlap] * np.linspace(0, 1, overlap)
            audio_segments = np.concatenate([audio_segments, seg[overlap:]])
        else:
            audio_segments = seg

    return audio_segments


# ══════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════
def main():
    print("═" * 60)
    print("  DIAL SPACE VISUALIZER")
    print("  Musical Traditions as Points in Parameter Space")
    print("═" * 60)

    # ── Step 1: Build tradition point data ──
    print("\n[1/6] Mapping tradition positions...")
    tradition_data = {}
    for name, vals in TRADITIONS.items():
        tradition_data[name] = {
            "I_vert": vals["I_vert"],
            "I_horiz": vals["I_horiz"],
            "I_spectral": vals["I_spectral"],
        }

    # ── Step 2: Cluster detection ──
    print("[2/6] Running K-means clustering...")
    best_k, cluster_results = find_clusters(points, names)
    clusters_out = {
        "best_k": best_k,
        "silhouette": cluster_results[best_k]["silhouette"],
        "cluster_assignments": {
            names[i]: cluster_results[best_k]["labels"][i] for i in range(len(names))
        },
        "centers": {
            f"cluster_{c}": {
                "I_vert": cluster_results[best_k]["centers"][c][0],
                "I_horiz": cluster_results[best_k]["centers"][c][1],
                "I_spectral": cluster_results[best_k]["centers"][c][2],
            }
            for c in range(best_k)
        },
        "all_k_results": {str(k): {"silhouette": v["silhouette"]} for k, v in cluster_results.items()},
    }
    print(f"    Best k={best_k} (silhouette={clusters_out['silhouette']:.3f})")
    for name, cl in clusters_out["cluster_assignments"].items():
        print(f"      {name:15s} → cluster {cl}")

    # ── Step 3: Convex hull ──
    print("[3/6] Computing convex hull...")
    hull_data = compute_hull(points)
    print(f"    Hull volume: {hull_data['volume']:.4f}")
    print(f"    Hull vertices: {hull_data['vertex_names']}")

    # ── Step 4: Random baseline ──
    print("[4/6] Comparing to random baseline (10000 points, 1000 permutations)...")
    baseline = random_baseline(points, n_random=10000, n_iter=1000)
    print(f"    Observed mean pairwise dist: {baseline['observed_mean_pairwise_dist']:.4f}")
    print(f"    Random mean pairwise dist:   {baseline['random_mean_pairwise_dist_mean']:.4f} ± {baseline['random_mean_pairwise_dist_std']:.4f}")
    print(f"    Nearest-neighbor p-value:    {baseline['p_value_nn']:.4f}")
    print(f"    → {baseline['conclusion']}")

    # ── Step 5: Unexplored regions ──
    print("[5/6] Finding unexplored regions...")
    unexplored = find_unexplored(points)
    print(f"    Largest empty sphere center: {unexplored['largest_empty_sphere']['center']}")
    print(f"    Largest empty sphere radius: {unexplored['largest_empty_sphere']['radius']:.4f}")
    print(f"    Hull fill fraction of bounding box: {unexplored['fill_fraction']:.1%}")

    # ── Step 6: Transition audio ──
    print("[6/6] Generating transition audio...")
    # Pick interesting pairs to transition between
    transition_pairs = [
        ("Hindustani", "Western ET"),
        ("Balinese", "Arabic"),
        ("Gagaku", "West African"),
        ("Chinese", "Carnatic"),
        ("Javanese", "Turkish"),
    ]

    transition_meta = []
    for name_a, name_b in transition_pairs:
        print(f"    {name_a} → {name_b}...")
        audio = generate_transition(name_a, name_b, n_steps=7, duration_each=1.5)
        fname = f"transition_{name_a.replace(' ','_').lower()}_to_{name_b.replace(' ','_').lower()}.wav"
        fpath = os.path.join(OUT, fname)
        sf.write(fpath, audio, SR)
        transition_meta.append({
            "from": name_a,
            "to": name_b,
            "file": fname,
            "duration_s": len(audio) / SR,
            "n_steps": 7,
        })

    # ── Also generate a sample for the emptiest dial position ──
    empty_center = unexplored["largest_empty_sphere"]["center"]
    print(f"    Synthesizing sample at unexplored point {empty_center}...")
    unexplored_audio = synthesize_from_dials(empty_center[0], empty_center[1], empty_center[2], duration=10.0)
    sf.write(os.path.join(OUT, "unexplored_dial_sample.wav"), unexplored_audio, SR)

    # ── Save JSON outputs ──
    dial_space_json = {
        "traditions": tradition_data,
        "clusters": clusters_out,
        "convex_hull": hull_data,
    }
    with open(os.path.join(OUT, "dial_space.json"), "w") as f:
        json.dump(dial_space_json, f, indent=2, ensure_ascii=False)

    with open(os.path.join(OUT, "random_baseline.json"), "w") as f:
        json.dump(baseline, f, indent=2, ensure_ascii=False)

    with open(os.path.join(OUT, "unexplored_regions.json"), "w") as f:
        json.dump(unexplored, f, indent=2, ensure_ascii=False)

    with open(os.path.join(OUT, "transitions.json"), "w") as f:
        json.dump(transition_meta, f, indent=2, ensure_ascii=False)

    print(f"\n{'═' * 60}")
    print(f"  Done! All outputs saved to: {OUT}")
    print(f"  Files:")
    for fn in sorted(os.listdir(OUT)):
        size = os.path.getsize(os.path.join(OUT, fn))
        print(f"    {fn:45s} {size:>10,} bytes")
    print(f"{'═' * 60}")


if __name__ == "__main__":
    main()
