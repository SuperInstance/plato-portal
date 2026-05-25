#!/usr/bin/env python3
"""
Consonance Fingerprinting
=========================

Can you IDENTIFY a person by their consonance preferences?

Everyone has a unique "consonance fingerprint" — a set of dial positions they find
most pleasing, shaped by cultural background, musical training, and individual neurology.

This script generates:
1. Interactive experiment data (20 pairs for user testing)
2. Automated analysis (100 random dial positions scored)
3. Crossover hit finder (mainstream + adventurous appeal)
4. "Most foreign" dial position finder

Based on the dial-space framework and tradition positions.
"""

import json
import math
import os
import random

# ─── Configuration ──────────────────────────────────────────────────────

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "neuro_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)  # Reproducibility

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

# Musical intervals with their approximate dial-space coordinates
# I_vert maps to consonance complexity, I_horiz to temporal familiarity,
# I_spectral to timbral brightness
INTERVAL_PAIRS = [
    {
        "id": 1,
        "description": "Perfect octave (2:1) vs. Tritone (45:32)",
        "option_a": {"name": "Perfect Octave", "I_vert": 1.0, "I_horiz": 1.0, "I_spectral": 1.5, "consonance": 0.95},
        "option_b": {"name": "Tritone", "I_vert": 3.5, "I_horiz": 2.0, "I_spectral": 2.0, "consonance": 0.25},
        "tests": "basic consonance preference",
    },
    {
        "id": 2,
        "description": "Perfect fifth (3:2) vs. Minor second (25:24)",
        "option_a": {"name": "Perfect Fifth", "I_vert": 1.2, "I_horiz": 1.2, "I_spectral": 1.6, "consonance": 0.90},
        "option_b": {"name": "Minor Second", "I_vert": 3.8, "I_horiz": 1.5, "I_spectral": 1.8, "consonance": 0.15},
        "tests": "simple interval preference",
    },
    {
        "id": 3,
        "description": "Major triad (4:5:6) vs. Cluster chord (15:16:17)",
        "option_a": {"name": "Major Triad", "I_vert": 1.8, "I_horiz": 1.5, "I_spectral": 1.8, "consonance": 0.85},
        "option_b": {"name": "Tone Cluster", "I_vert": 4.0, "I_horiz": 2.0, "I_spectral": 2.5, "consonance": 0.10},
        "tests": "harmonic complexity tolerance",
    },
    {
        "id": 4,
        "description": "Steady pulse (repetition) vs. Syncopated rhythm",
        "option_a": {"name": "Steady 4/4 Pulse", "I_vert": 1.5, "I_horiz": 1.0, "I_spectral": 1.2, "consonance": 0.70},
        "option_b": {"name": "Polyrhythm 7:5", "I_vert": 2.0, "I_horiz": 3.5, "I_spectral": 1.5, "consonance": 0.40},
        "tests": "horizontal complexity preference",
    },
    {
        "id": 5,
        "description": "Pure sine tone vs. Rich overtones (sawtooth wave)",
        "option_a": {"name": "Pure Sine", "I_vert": 1.0, "I_horiz": 1.0, "I_spectral": 0.5, "consonance": 0.60},
        "option_b": {"name": "Sawtooth (rich harmonics)", "I_vert": 1.5, "I_horiz": 1.2, "I_spectral": 3.5, "consonance": 0.55},
        "tests": "spectral richness preference",
    },
    {
        "id": 6,
        "description": "Pentatonic melody vs. Chromatic melody",
        "option_a": {"name": "Pentatonic", "I_vert": 1.5, "I_horiz": 2.0, "I_spectral": 1.5, "consonance": 0.80},
        "option_b": {"name": "12-tone row", "I_vert": 3.5, "I_horiz": 3.0, "I_spectral": 1.8, "consonance": 0.20},
        "tests": "melodic complexity preference",
    },
    {
        "id": 7,
        "description": "Gamelan-style inharmonic timbre vs. Western harmonic timbre",
        "option_a": {"name": "Gamelan (inharmonic)", "I_vert": 2.0, "I_horiz": 2.5, "I_spectral": 3.5, "consonance": 0.45},
        "option_b": {"name": "Piano (harmonic)", "I_vert": 2.0, "I_horiz": 2.5, "I_spectral": 1.5, "consonance": 0.75},
        "tests": "timbral consonance preference",
    },
    {
        "id": 8,
        "description": "Drone + microtonal ornament vs. Chord progression",
        "option_a": {"name": "Drone + Microtones", "I_vert": 3.0, "I_horiz": 1.5, "I_spectral": 2.5, "consonance": 0.50},
        "option_b": {"name": "I-IV-V-I Progression", "I_vert": 1.5, "I_horiz": 3.0, "I_spectral": 1.5, "consonance": 0.80},
        "tests": "vertical vs. horizontal orientation",
    },
    {
        "id": 9,
        "description": "Slow tempo (Adagio) vs. Fast tempo (Presto)",
        "option_a": {"name": "Adagio (60 BPM)", "I_vert": 2.0, "I_horiz": 1.5, "I_spectral": 2.0, "consonance": 0.65},
        "option_b": {"name": "Presto (200 BPM)", "I_vert": 2.0, "I_horiz": 3.8, "I_spectral": 2.2, "consonance": 0.45},
        "tests": "tempo / horizontal density preference",
    },
    {
        "id": 10,
        "description": "Just intonation thirds vs. Equal temperament thirds",
        "option_a": {"name": "Just Major Third (5:4)", "I_vert": 1.3, "I_horiz": 1.5, "I_spectral": 1.8, "consonance": 0.85},
        "option_b": {"name": "ET Major Third (400¢)", "I_vert": 2.0, "I_horiz": 1.5, "I_spectral": 1.8, "consonance": 0.65},
        "tests": "tuning system sensitivity",
    },
    {
        "id": 11,
        "description": "Solo voice (monophonic) vs. Full orchestra",
        "option_a": {"name": "Solo Voice", "I_vert": 1.0, "I_horiz": 2.0, "I_spectral": 2.0, "consonance": 0.50},
        "option_b": {"name": "Full Orchestra", "I_vert": 3.0, "I_horiz": 3.0, "I_spectral": 3.0, "consonance": 0.70},
        "tests": "textural complexity preference",
    },
    {
        "id": 12,
        "description": "Repetitive minimalism vs. Through-composed",
        "option_a": {"name": "Minimalist Repetition", "I_vert": 1.2, "I_horiz": 1.5, "I_spectral": 2.0, "consonance": 0.60},
        "option_b": {"name": "Through-composed", "I_vert": 2.5, "I_horiz": 3.5, "I_spectral": 2.5, "consonance": 0.50},
        "tests": "structural predictability preference",
    },
    {
        "id": 13,
        "description": "Arabic maqam quarter tones vs. Western semitones",
        "option_a": {"name": "Maqam Quarter Tones", "I_vert": 3.2, "I_horiz": 2.5, "I_spectral": 2.0, "consonance": 0.35},
        "option_b": {"name": "Western Semitones", "I_vert": 2.0, "I_horiz": 2.5, "I_spectral": 1.5, "consonance": 0.70},
        "tests": "pitch granularity cultural preference",
    },
    {
        "id": 14,
        "description": "Tonal resolution (V→I) vs. Unresolved suspension",
        "option_a": {"name": "Resolved (V→I)", "I_vert": 1.5, "I_horiz": 2.5, "I_spectral": 1.5, "consonance": 0.85},
        "option_b": {"name": "Unresolved Suspension", "I_vert": 2.5, "I_horiz": 2.5, "I_spectral": 2.0, "consonance": 0.40},
        "tests": "closure preference (tonal vs. open)",
    },
    {
        "id": 15,
        "description": "Balinese gong kebyar vs. Bach chorale",
        "option_a": {"name": "Gong Kebyar", "I_vert": 2.3, "I_horiz": 3.5, "I_spectral": 3.5, "consonance": 0.30},
        "option_b": {"name": "Bach Chorale", "I_vert": 2.0, "I_horiz": 1.5, "I_spectral": 1.5, "consonance": 0.80},
        "tests": "cultural style preference",
    },
    {
        "id": 16,
        "description": "Funk groove (strong syncopation) vs. March (straight rhythm)",
        "option_a": {"name": "Funk Groove", "I_vert": 2.0, "I_horiz": 3.5, "I_spectral": 2.5, "consonance": 0.55},
        "option_b": {"name": "March", "I_vert": 1.5, "I_horiz": 1.5, "I_spectral": 1.5, "consonance": 0.65},
        "tests": "groove/syncopation preference",
    },
    {
        "id": 17,
        "description": "Indian raga alap (slow unfold) vs. Jazz solo (fast changes)",
        "option_a": {"name": "Raga Alap", "I_vert": 3.0, "I_horiz": 1.0, "I_spectral": 2.5, "consonance": 0.45},
        "option_b": {"name": "Jazz Bebop Solo", "I_vert": 2.5, "I_horiz": 3.5, "I_spectral": 2.0, "consonance": 0.50},
        "tests": "horizontal density vs. vertical complexity",
    },
    {
        "id": 18,
        "description": "Silence + single note vs. Dense cluster",
        "option_a": {"name": "Single Note from Silence", "I_vert": 0.5, "I_horiz": 1.0, "I_spectral": 1.0, "consonance": 0.70},
        "option_b": {"name": "Dense Tone Cluster", "I_vert": 4.0, "I_horiz": 1.5, "I_spectral": 3.0, "consonance": 0.05},
        "tests": "density tolerance",
    },
    {
        "id": 19,
        "description": "Major key (happy) vs. Minor key (sad)",
        "option_a": {"name": "C Major", "I_vert": 1.5, "I_horiz": 2.0, "I_spectral": 2.0, "consonance": 0.80},
        "option_b": {"name": "C Minor", "I_vert": 2.0, "I_horiz": 2.0, "I_spectral": 1.8, "consonance": 0.70},
        "tests": "emotional valence preference",
    },
    {
        "id": 20,
        "description": "Familiar pop song structure vs. Free improvisation",
        "option_a": {"name": "Pop (Verse-Chorus)", "I_vert": 1.5, "I_horiz": 2.0, "I_spectral": 2.0, "consonance": 0.75},
        "option_b": {"name": "Free Improvisation", "I_vert": 3.5, "I_horiz": 3.5, "I_spectral": 3.0, "consonance": 0.25},
        "tests": "structural predictability tolerance",
    },
]


# ─── Utility Functions ──────────────────────────────────────────────────

def dial_distance(a, b):
    """Euclidean distance in (I_vert, I_horiz, I_spectral) space."""
    return math.sqrt(sum(
        (a.get(k, 0) - b.get(k, 0)) ** 2
        for k in ["I_vert", "I_horiz", "I_spectral"]
    ))


def find_closest_tradition(user_profile):
    """Find the tradition closest to user's preference profile."""
    distances = {}
    for name, dial in TRADITIONS.items():
        distances[name] = dial_distance(user_profile, dial)
    
    sorted_traditions = sorted(distances.items(), key=lambda x: x[1])
    return sorted_traditions


def generate_fingerprint_report(user_profile, tradition_distances):
    """Generate a personalized 'musical DNA' report."""
    closest = tradition_distances[0]
    second = tradition_distances[1]
    farthest = tradition_distances[-1]
    
    # Determine user's "axis tendencies"
    avg_trad = {
        "I_vert": sum(t["I_vert"] for t in TRADITIONS.values()) / len(TRADITIONS),
        "I_horiz": sum(t["I_horiz"] for t in TRADITIONS.values()) / len(TRADITIONS),
        "I_spectral": sum(t["I_spectral"] for t in TRADITIONS.values()) / len(TRADITIONS),
    }
    
    vert_tendency = "complex" if user_profile.get("I_vert", 2) > avg_trad["I_vert"] else "simple"
    horiz_tendency = "complex" if user_profile.get("I_horiz", 2) > avg_trad["I_horiz"] else "simple"
    spec_tendency = "rich" if user_profile.get("I_spectral", 2) > avg_trad["I_spectral"] else "pure"
    
    report = {
        "your_dial_position": {
            k: round(v, 2) for k, v in user_profile.items()
        },
        "closest_tradition": {
            "name": closest[0],
            "distance": round(closest[1], 3),
            "meaning": f"Your taste most resembles {closest[0]} music",
        },
        "second_closest": {
            "name": second[0],
            "distance": round(second[1], 3),
        },
        "most_foreign": {
            "name": farthest[0],
            "distance": round(farthest[1], 3),
            "meaning": f"{farthest[0]} music would feel most unfamiliar to you",
        },
        "axis_profile": {
            "vertical_complexity": f"You prefer {vert_tendency} harmonic structures",
            "horizontal_complexity": f"You prefer {horiz_tendency} rhythmic/melodic patterns",
            "spectral_richness": f"You prefer {spec_tendency} timbres",
        },
        "comfort_zone": {
            "center": {k: round(v, 2) for k, v in user_profile.items()},
            "radius": round(closest[1] + 0.3, 2),
            "description": f"You'll likely enjoy music within {round(closest[1] + 0.3, 1)} dial units of your profile",
        },
        "exploration_recommendation": {
            "nearby": f"Try {second[0]} music — close to your taste but new",
            "stretch": f"Try {tradition_distances[4][0]} or {tradition_distances[5][0]} music — different enough to be interesting",
            "adventure": f"Try {farthest[0]} music — maximum contrast with your preferences",
        },
    }
    return report


# ─── Automated Analysis ────────────────────────────────────────────────

def score_mainstream_appeal(dial_pos):
    """
    Score for mainstream appeal = proximity to Western cluster.
    Western ET is the global "pop music" center of gravity.
    """
    western = TRADITIONS["Western ET"]
    dist = dial_distance(dial_pos, western)
    # Inverse distance, normalized: 1.0 = Western center, 0.0 = very far
    return max(0.0, 1.0 - dist / 3.0)


def score_adventurous_appeal(dial_pos, sampled_positions):
    """
    Score for adventurous appeal = distance from nearest existing tradition.
    Higher = more unexplored territory.
    """
    min_dist = min(dial_distance(dial_pos, t) for t in TRADITIONS.values())
    # Also consider distance from other sampled positions (novelty)
    if sampled_positions:
        nearest_sampled = min(dial_distance(dial_pos, s) for s in sampled_positions)
        novelty_bonus = min(1.0, nearest_sampled / 2.0)
    else:
        novelty_bonus = 0.5
    
    return min(1.0, min_dist / 2.0) * 0.7 + novelty_bonus * 0.3


def main():
    # ─── 1. Interactive Experiment Data ──
    print("Generating consonance fingerprint experiment data...")
    
    fingerprint_data = {
        "metadata": {
            "title": "Consonance Fingerprint — Interactive Experiment",
            "description": "20 pairwise comparisons to map your unique consonance profile",
            "instructions": "For each pair, choose which sounds better to you. There are no wrong answers.",
            "output_note": "Your choices are mapped to (I_vert, I_horiz, I_spectral) space",
        },
        "pairs": INTERVAL_PAIRS,
        "scoring": {
            "description": "After completing all 20 pairs, your profile is computed as the weighted average of your chosen options",
            "weights": "Each choice adds to your cumulative dial position. Equal weighting.",
            "mapping": {
                "high_I_vert_choice": "You prefer complex, dissonant harmonies",
                "high_I_horiz_choice": "You prefer complex rhythms and fast harmonic rhythm",
                "high_I_spectral_choice": "You prefer rich, complex timbres",
            },
        },
        "tradition_reference": {name: dial for name, dial in TRADITIONS.items()},
    }
    
    # ─── 2. Automated Crossover Analysis ──
    print("Running automated crossover analysis (100 random dial positions)...")
    
    # Generate 100 random positions
    random_positions = []
    for i in range(100):
        pos = {
            "id": i + 1,
            "I_vert": round(random.uniform(1.0, 4.0), 2),
            "I_horiz": round(random.uniform(1.0, 4.0), 2),
            "I_spectral": round(random.uniform(0.5, 4.0), 2),
        }
        random_positions.append(pos)
    
    # Score each position
    scored_positions = []
    all_positions = [TRADITIONS[n] for n in TRADITIONS]
    
    for pos in random_positions:
        main = score_mainstream_appeal(pos)
        adv = score_adventurous_appeal(pos, all_positions)
        pos["mainstream_appeal"] = round(main, 3)
        pos["adventurous_appeal"] = round(adv, 3)
        pos["crossover_score"] = round(main * 0.5 + adv * 0.5, 3)
        pos["difference_from_western"] = round(dial_distance(pos, TRADITIONS["Western ET"]), 3)
        
        # Find nearest tradition
        nearest = min(TRADITIONS.items(), key=lambda t: dial_distance(pos, t[1]))
        pos["nearest_tradition"] = nearest[0]
        pos["distance_to_nearest"] = round(nearest[1], 3) if isinstance(nearest[1], float) else round(dial_distance(pos, nearest[1]), 3)
        
        scored_positions.append(pos)
    
    # Find crossover hit
    crossover_hit = max(scored_positions, key=lambda p: p["crossover_score"])
    
    # Find most foreign
    most_foreign = max(scored_positions, key=lambda p: p["difference_from_western"])
    
    # Find highest mainstream
    highest_mainstream = max(scored_positions, key=lambda p: p["mainstream_appeal"])
    
    # Find highest adventurous
    highest_adventurous = max(scored_positions, key=lambda p: p["adventurous_appeal"])
    
    # Generate a sample fingerprint report for a hypothetical user
    # (Simulated: user who picks "middle ground" options)
    sample_profile = {
        "I_vert": 2.30,
        "I_horiz": 2.50,
        "I_spectral": 2.00,
    }
    tradition_distances = find_closest_tradition(sample_profile)
    sample_report = generate_fingerprint_report(sample_profile, tradition_distances)
    
    # ─── Write fingerprint experiment ──
    fingerprint_path = os.path.join(OUTPUT_DIR, "consonance_fingerprint.json")
    with open(fingerprint_path, "w") as f:
        json.dump(fingerprint_data, f, indent=2)
    print(f"Wrote: {fingerprint_path}")
    
    # ─── Write crossover analysis ──
    crossover_data = {
        "metadata": {
            "title": "Crossover Analysis — Mainstream vs. Adventurous Dial Positions",
            "n_positions_sampled": 100,
            "western_reference": TRADITIONS["Western ET"],
            "scoring": {
                "mainstream_appeal": "Proximity to Western ET cluster (inverse distance, normalized 0-1)",
                "adventurous_appeal": "Distance from nearest existing tradition + novelty bonus",
                "crossover_score": "Average of mainstream and adventurous scores",
            },
        },
        "crossover_hit": crossover_hit,
        "most_foreign": most_foreign,
        "highest_mainstream": highest_mainstream,
        "highest_adventurous": highest_adventurous,
        "all_positions": scored_positions,
        "tradition_positions": {name: dial for name, dial in TRADITIONS.items()},
    }
    
    crossover_path = os.path.join(OUTPUT_DIR, "crossover_analysis.json")
    with open(crossover_path, "w") as f:
        json.dump(crossover_data, f, indent=2)
    print(f"Wrote: {crossover_path}")
    
    # ─── Print summary ──
    print("\n" + "="*70)
    print("CONSONANCE FINGERPRINTING SUMMARY")
    print("="*70)
    
    print("\n--- Interactive Experiment ---")
    print(f"  20 pairwise comparison pairs generated")
    print(f"  Each maps to (I_vert, I_horiz, I_spectral) space")
    print(f"  Result: personal consonance fingerprint + closest tradition match")
    
    print("\n--- Crossover Analysis (100 random positions) ---")
    print(f"\n  🎯 CROSSOVER HIT (best of both worlds):")
    print(f"     Position: I_vert={crossover_hit['I_vert']}, I_horiz={crossover_hit['I_horiz']}, I_spectral={crossover_hit['I_spectral']}")
    print(f"     Mainstream appeal: {crossover_hit['mainstream_appeal']:.3f}")
    print(f"     Adventurous appeal: {crossover_hit['adventurous_appeal']:.3f}")
    print(f"     Crossover score: {crossover_hit['crossover_score']:.3f}")
    print(f"     Nearest tradition: {crossover_hit['nearest_tradition']}")
    
    print(f"\n  🌍 MOST FOREIGN (maximally different from Western):")
    print(f"     Position: I_vert={most_foreign['I_vert']}, I_horiz={most_foreign['I_horiz']}, I_spectral={most_foreign['I_spectral']}")
    print(f"     Distance from Western: {most_foreign['difference_from_western']:.3f}")
    print(f"     Nearest tradition: {most_foreign['nearest_tradition']}")
    
    print(f"\n  📊 HIGHEST MAINSTREAM:")
    print(f"     Position: I_vert={highest_mainstream['I_vert']}, I_horiz={highest_mainstream['I_horiz']}, I_spectral={highest_mainstream['I_spectral']}")
    print(f"     Mainstream appeal: {highest_mainstream['mainstream_appeal']:.3f}")
    
    print(f"\n  🧭 HIGHEST ADVENTUROUS:")
    print(f"     Position: I_vert={highest_adventurous['I_vert']}, I_horiz={highest_adventurous['I_horiz']}, I_spectral={highest_adventurous['I_spectral']}")
    print(f"     Adventurous appeal: {highest_adventurous['adventurous_appeal']:.3f}")
    
    print("\n--- Sample Fingerprint Report (hypothetical user) ---")
    print(f"  Profile: I_vert={sample_profile['I_vert']}, I_horiz={sample_profile['I_horiz']}, I_spectral={sample_profile['I_spectral']}")
    print(f"  Closest tradition: {sample_report['closest_tradition']['name']} (dist={sample_report['closest_tradition']['distance']})")
    print(f"  Most foreign: {sample_report['most_foreign']['name']} (dist={sample_report['most_foreign']['distance']})")
    for axis, desc in sample_report["axis_profile"].items():
        print(f"  {axis}: {desc}")
    
    print("\nDone.")


if __name__ == "__main__":
    main()
