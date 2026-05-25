#!/usr/bin/env python3
"""
Predicted EEG/fMRI Response Map for Dial-Space Traditions
==========================================================

Based on published neuroscience of musical consonance:
- Bidelman & Krishnan (2009): Brainstem FFR correlates with consonance
- Blood et al. (1999): Dissonance → parahippocampal; consonance → orbitofrontal
- Trainor et al. (2002): Consonance preferences emerge at 4 months
- McDermott et al. (2010): Consonance preference is partly cultural
- Sachs et al. (2008): Midbrain reward regions respond to consonance

Maps Tenney height (consonance metric) to predicted neural activation patterns
for each tradition at their (I_vert, I_horiz, I_spectral) dial position.
"""

import json
import math
import os

# ─── Configuration ──────────────────────────────────────────────────────

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "neuro_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Tradition dial positions (from dial_space.json)
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

# Historical styles mapped to approximate dial positions
HISTORICAL_STYLES = {
    "Renaissance (c.1450)":     {"I_vert": 1.80, "I_horiz": 1.20, "I_spectral": 0.8},
    "Baroque (c.1700)":         {"I_vert": 2.20, "I_horiz": 1.50, "I_spectral": 1.0},
    "Classical (c.1780)":       {"I_vert": 2.00, "I_horiz": 1.80, "I_spectral": 1.1},
    "Romantic (c.1850)":        {"I_vert": 2.60, "I_horiz": 2.20, "I_spectral": 1.3},
    "Early Jazz (c.1920)":      {"I_vert": 2.50, "I_horiz": 2.80, "I_spectral": 1.5},
    "Bebop (c.1945)":           {"I_vert": 2.80, "I_horiz": 3.20, "I_spectral": 1.6},
    "Rock (c.1965)":            {"I_vert": 2.30, "I_horiz": 2.50, "I_spectral": 2.0},
    "Minimalism (c.1970)":      {"I_vert": 1.50, "I_horiz": 2.80, "I_spectral": 2.2},
    "Electronic (c.1995)":      {"I_vert": 2.00, "I_horiz": 3.00, "I_spectral": 2.8},
    "AI-generated (c.2025)":    {"I_vert": 3.00, "I_horiz": 3.00, "I_spectral": 3.0},
}

# Innovation cycle phases
INNOVATION_PHASES = {
    "Phase 1: Discovery":   {"novelty": 0.95, "familiarity": 0.20, "emotional_intensity": 0.85},
    "Phase 2: Codification": {"novelty": 0.65, "familiarity": 0.50, "emotional_intensity": 0.60},
    "Phase 3: Ubiquity":    {"novelty": 0.20, "familiarity": 0.90, "emotional_intensity": 0.40},
    "Phase 4: Saturation":  {"novelty": 0.05, "familiarity": 0.98, "emotional_intensity": 0.20},
    "Phase 5: Rebellion":   {"novelty": 0.75, "familiarity": 0.30, "emotional_intensity": 0.90},
    "Phase 6: Synthesis":   {"novelty": 0.50, "familiarity": 0.60, "emotional_intensity": 0.70},
}


# ─── Neural Model ──────────────────────────────────────────────────────

def tenney_height(dial_pos):
    """
    Approximate Tenney height from dial position.
    Lower Tenney height = more consonant (simpler ratios).
    
    Tenney height H(p/q) = log₂(p) + log₂(q) for interval p/q.
    We map from dial coordinates to an effective consonance level.
    
    High I_vert → more complex vertical ratios → higher Tenney height
    High I_horiz → more complex rhythmic/harmonic changes → moderate effect
    High I_spectral → richer timbres → higher effective consonance can coexist
    
    Dial values range ~1.5-4.0. We map to Tenney height ~1.5-8.0:
      I_vert=1.5, I_horiz=1.5, I_spectral=1.5 → ~2.5 (highly consonant, like Renaissance)
      I_vert=3.0, I_horiz=3.5, I_spectral=3.0 → ~7.0 (complex, like Carnatic)
    """
    # Weighted combination: vertical complexity matters most for consonance
    raw = (dial_pos["I_vert"] * 1.2 + dial_pos["I_horiz"] * 0.5 + dial_pos["I_spectral"] * 0.3)
    # Map to Tenney height range (1.5-8.0 for musical intervals)
    return 1.0 + raw * 0.8


def consonance_score(tenney_h):
    """Map Tenney height to consonance score (0-1, 1=most consonant)."""
    # Tenney height ~2 = unison/octave (max consonance)
    # Tenney height ~12 = highly complex/dissonant
    return max(0.0, min(1.0, 1.0 - (tenney_h - 2.0) / 12.0))


def predict_brainstem_ffr(consonance):
    """
    Brainstem Frequency-Following Response amplitude.
    Based on Bidelman & Krishnan (2009): FFR is stronger and more phase-locked
    for consonant intervals. FFR amplitude normalized to 0-1 scale.
    """
    # FFR strength: exponential decay with dissonance
    return 0.3 + 0.7 * consonance ** 0.8


def predict_cortical_activation(consonance, spectral_complexity):
    """
    Predict cortical activation pattern.
    Based on Blood et al. (1999), Sachs et al. (2008):
    - Consonance → orbitofrontal cortex (reward), nucleus accumbens
    - Dissonance → parahippocampal gyrus, amygdala (negative valence)
    - Complex spectra → broader auditory cortex activation
    - Temporal complexity → supplementary motor area, basal ganglia
    
    Returns dict of brain regions with predicted activation (0-1).
    """
    dissonance = 1.0 - consonance
    
    return {
        "orbitofrontal_cortex": round(0.2 + 0.8 * consonance, 3),       # Reward/pleasure
        "nucleus_accumbens": round(0.15 + 0.7 * consonance, 3),          # Dopamine reward
        "auditory_cortex_primary": round(0.4 + 0.3 * spectral_complexity, 3),  # Always active
        "auditory_cortex_secondary": round(0.3 + 0.4 * spectral_complexity, 3), # Pattern processing
        "parahippocampal_gyrus": round(0.1 + 0.7 * dissonance, 3),      # Dissonance/discomfort
        "amygdala": round(0.05 + 0.6 * dissonance, 3),                   # Threat/novelty
        "superior_temporal_gyrus": round(0.3 + 0.4 * consonance, 3),     # Music-specific
        "supplementary_motor_area": round(0.2 + 0.3 * spectral_complexity, 3), # Rhythm entrainment
        "prefrontal_cortex_dorsolateral": round(0.1 + 0.5 * dissonance, 3),  # Working memory for complex patterns
        "cerebellum": round(0.2 + 0.2 * spectral_complexity, 3),         # Temporal prediction
        "insula": round(0.1 + 0.4 * dissonance + 0.2 * spectral_complexity, 3), # Interoception/emotional
    }


def predict_pleasantness(consonance, novelty_factor=0.5):
    """
    Predicted "pleasantness" rating (1-10 scale).
    
    Based on:
    - Base pleasantness from consonance (Schwartz et al. 2003)
    - Novelty boost: mild novelty increases pleasure (Berlyne's Wundt curve)
    - Too much novelty → unpleasant (neophobia)
    
    The inverted-U relationship: optimal arousal is mid-range.
    """
    base = consonance * 7.0 + 2.0  # 2-9 range
    # Novelty bonus/penalty (Berlyne's Wundt curve)
    # Peak pleasantness at moderate novelty
    novelty_effect = 2.0 * novelty_factor * (1.0 - novelty_factor) * 4.0  # 0-2 range
    return round(max(1.0, min(10.0, base + novelty_effect - 1.0)), 1)


def predict_adaptation_rate(consonance, novelty_factor=0.5):
    """
    Predicted neural adaptation rate (how fast the brain habituates).
    
    Based on:
    - Higher consonance → faster adaptation (brain expects the pattern)
    - Higher novelty → slower adaptation (brain keeps attending)
    - Musical training reduces adaptation rate
    
    Expressed as half-life in seconds (lower = faster habituation).
    """
    # Base adaptation: consonant music → faster habituation
    base_halflife = 5.0 + 25.0 * (1.0 - consonance)  # 5-30 seconds
    
    # Novelty slows adaptation
    novelty_slowdown = 1.0 + novelty_factor * 2.0
    
    return round(base_halflife * novelty_slowdown, 1)


def predict_neural_response(dial_pos, novelty_factor=0.5):
    """Full neural response prediction for a given dial position."""
    th = tenney_height(dial_pos)
    cons = consonance_score(th)
    spectral_norm = dial_pos["I_spectral"] / 4.0  # normalize to 0-1
    
    return {
        "dial_position": dial_pos,
        "tenney_height": round(th, 2),
        "consonance_score": round(cons, 3),
        "brainstem_FFR_amplitude": round(predict_brainstem_ffr(cons), 3),
        "cortical_activation": predict_cortical_activation(cons, spectral_norm),
        "predicted_pleasantness": predict_pleasantness(cons, novelty_factor),
        "neural_adaptation_halflife_s": predict_adaptation_rate(cons, novelty_factor),
    }


def compute_neural_distance(resp1, resp2):
    """
    Neural distance between two predicted responses.
    Lower = more similar brain responses predicted.
    """
    # Use cortical activation vectors
    regions = ["orbitofrontal_cortex", "nucleus_accumbens", "parahippocampal_gyrus",
               "amygdala", "auditory_cortex_primary", "auditory_cortex_secondary",
               "superior_temporal_gyrus", "insula"]
    
    c1 = resp1["cortical_activation"]
    c2 = resp2["cortical_activation"]
    
    sq_dist = sum((c1[r] - c2[r]) ** 2 for r in regions)
    return round(math.sqrt(sq_dist), 3)


# ─── Main Predictions ──────────────────────────────────────────────────

def main():
    results = {
        "metadata": {
            "title": "Predicted Neural Responses for Musical Traditions",
            "basis": [
                "Bidelman & Krishnan (2009) - Brainstem FFR correlates with consonance",
                "Blood et al. (1999) - Dissonance/consonance cortical mapping",
                "Sachs et al. (2008) - Midbrain reward response to consonance",
                "Trainor et al. (2002) - Consonance preference emergence",
                "Berlyne (1971) - Wundt curve for novelty-pleasure",
            ],
            "note": "These are computational PREDICTIONS based on published data, not measured responses. Testable with EEG/fMRI.",
        },
        "traditions": {},
        "historical_styles": {},
        "innovation_cycle_neural": {},
        "tradition_similarity_matrix": {},
        "novel_predictions": {},
        "heatmap_data": {},
    }

    # ── Tradition predictions ──
    print("Computing tradition neural predictions...")
    for name, dial in TRADITIONS.items():
        # Assign novelty based on how different from Western ET
        novelty = math.sqrt(sum((dial[k] - TRADITIONS["Western ET"][k]) ** 2 
                                for k in ["I_vert", "I_horiz", "I_spectral"])) / 3.0
        novelty = min(1.0, novelty)
        results["traditions"][name] = predict_neural_response(dial, novelty)

    # ── Historical style predictions ──
    print("Computing historical style neural predictions...")
    for name, dial in HISTORICAL_STYLES.items():
        novelty = math.sqrt(sum((dial[k] - TRADITIONS["Western ET"][k]) ** 2 
                                for k in ["I_vert", "I_horiz", "I_spectral"])) / 3.0
        novelty = min(1.0, novelty)
        results["historical_styles"][name] = predict_neural_response(dial, novelty)

    # ── Innovation cycle neural predictions ──
    print("Computing innovation cycle neural predictions...")
    for phase, props in INNOVATION_PHASES.items():
        # Map phase properties to an effective dial position
        # Discovery: high novelty, low familiarity → high I_vert (new sounds), moderate rest
        # Saturation: low novelty, high familiarity → moderate I_vert, low everything
        effective_dial = {
            "I_vert": 1.5 + props["novelty"] * 2.0,
            "I_horiz": 1.0 + props["novelty"] * 2.5,
            "I_spectral": 0.5 + props["emotional_intensity"] * 3.0,
        }
        neural = predict_neural_response(effective_dial, props["novelty"])
        neural["phase_properties"] = props
        neural["effective_dial"] = {k: round(v, 2) for k, v in effective_dial.items()}
        results["innovation_cycle_neural"][phase] = neural

    # ── Tradition similarity matrix (novel prediction) ──
    print("Computing neural similarity matrix...")
    trad_names = list(TRADITIONS.keys())
    trad_responses = {n: results["traditions"][n] for n in trad_names}
    
    sim_matrix = {}
    for n1 in trad_names:
        sim_matrix[n1] = {}
        for n2 in trad_names:
            dist = compute_neural_distance(trad_responses[n1], trad_responses[n2])
            sim_matrix[n1][n2] = dist
    
    results["tradition_similarity_matrix"] = sim_matrix

    # ── Novel predictions ──
    print("Generating novel testable predictions...")
    
    # Prediction 1: Traditions at similar dial positions → similar neural responses
    similar_pairs = []
    for i, n1 in enumerate(trad_names):
        for n2 in trad_names[i+1:]:
            dist = sim_matrix[n1][n2]
            # Also compute dial-space distance
            dial_dist = math.sqrt(sum(
                (TRADITIONS[n1][k] - TRADITIONS[n2][k]) ** 2 
                for k in ["I_vert", "I_horiz", "I_spectral"]
            ))
            similar_pairs.append({
                "tradition_1": n1,
                "tradition_2": n2,
                "neural_distance": dist,
                "dial_distance": round(dial_dist, 3),
                "prediction": f"EEG responses to {n1} and {n2} music should be {'similar' if dist < 0.15 else 'distinct'}"
            })
    
    similar_pairs.sort(key=lambda x: x["neural_distance"])
    
    # Correlation between dial distance and neural distance
    dial_dists = [p["dial_distance"] for p in similar_pairs]
    neural_dists = [p["neural_distance"] for p in similar_pairs]
    mean_dd = sum(dial_dists) / len(dial_dists)
    mean_nn = sum(neural_dists) / len(neural_dists)
    cov = sum((dd - mean_dd) * (nn - mean_nn) for dd, nn in zip(dial_dists, neural_dists)) / len(dial_dists)
    std_dd = math.sqrt(sum((dd - mean_dd)**2 for dd in dial_dists) / len(dial_dists))
    std_nn = math.sqrt(sum((nn - mean_nn)**2 for nn in neural_dists) / len(neural_dists))
    correlation = cov / (std_dd * std_nn) if std_dd * std_nn > 0 else 0
    
    results["novel_predictions"] = {
        "prediction_1_neural_similarity": {
            "statement": "Traditions at similar dial positions should produce similar EEG/fMRI responses, regardless of geographic origin",
            "supporting_evidence": f"Dial distance–neural distance correlation: r = {correlation:.3f}",
            "testable_with": "Cross-cultural EEG study: play music from each tradition to naive listeners, measure FFR + cortical ERP",
            "closest_pairs": similar_pairs[:5],
            "most_distant_pairs": similar_pairs[-5:],
        },
        "prediction_2_adaptation_cycle": {
            "statement": "Music in Phase 4 (Saturation) should show fastest neural adaptation (habituation), Phase 1 (Discovery) slowest",
            "mechanism": "Familiarity speeds up predictive coding — the brain's prediction error drops faster",
            "testable_with": "Long-duration EEG: measure N1/P2 habituation rates for novel vs. familiar musical styles",
            "phase_ordering": [
                {"phase": p, "adaptation_halflife_s": results["innovation_cycle_neural"][p]["neural_adaptation_halflife_s"]}
                for p in INNOVATION_PHASES
            ],
        },
        "prediction_3_consonance_universal": {
            "statement": "Brainstem FFR response to consonance should be similar across all listeners (culturally invariant), but cortical pleasantness ratings should vary by cultural background",
            "basis": "FFR is subcortical (pre-conscious), pleasantness involves cortical + limbic (culturally shaped)",
            "testable_with": "Compare FFR amplitude (brainstem) vs. subjective pleasantness ratings across listeners from different musical traditions",
            "predicted_tradition_ranking_by_FFR": sorted(
                [(n, results["traditions"][n]["brainstem_FFR_amplitude"]) for n in trad_names],
                key=lambda x: -x[1]
            ),
        },
        "prediction_4_reward_prediction": {
            "statement": "Music near the listener's cultural tradition should activate nucleus accumbens more than equally consonant unfamiliar music",
            "mechanism": "Reward combines acoustic consonance with cultural familiarity (statistical learning)",
            "testable_with": "fMRI with listeners from 3+ traditions hearing each tradition's music",
        },
    }

    # ── Heatmap data ──
    print("Generating cortical activation heatmap data...")
    
    # Sample 10x10x10 grid of dial space
    heatmap_points = []
    for iv in [round(1.0 + i * 0.3, 1) for i in range(10)]:
        for ih in [round(1.0 + i * 0.3, 1) for i in range(10)]:
            dial = {"I_vert": iv, "I_horiz": ih, "I_spectral": 2.0}
            resp = predict_neural_response(dial, 0.5)
            heatmap_points.append({
                "I_vert": iv,
                "I_horiz": ih,
                "I_spectral": 2.0,
                "orbitofrontal": resp["cortical_activation"]["orbitofrontal_cortex"],
                "parahippocampal": resp["cortical_activation"]["parahippocampal_gyrus"],
                "FFR_amplitude": resp["brainstem_FFR_amplitude"],
                "pleasantness": resp["predicted_pleasantness"],
            })
    
    results["heatmap_data"] = {
        "description": "Cortical activation predicted at I_spectral=2.0 slice across I_vert x I_horiz",
        "points": heatmap_points,
        "tradition_overlay": {
            name: {"I_vert": TRADITIONS[name]["I_vert"], "I_horiz": TRADITIONS[name]["I_horiz"]}
            for name in TRADITIONS
        },
    }

    # ── Write outputs ──
    output_path = os.path.join(OUTPUT_DIR, "neuro_predictions.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Wrote: {output_path}")

    # ── Adaptation rates separate file ──
    adaptation = {
        "metadata": {
            "description": "Predicted neural adaptation rates across the Innovation Cycle",
            "basis": "Predictive coding theory: familiarity → faster prediction error minimization → faster habituation",
            "measured_as": "N1/P2 ERP amplitude reduction over repeated exposure (half-life in seconds)",
        },
        "phases": {},
        "tradition_adaptation": {},
    }
    
    for phase, neural in results["innovation_cycle_neural"].items():
        adaptation["phases"][phase] = {
            "halflife_s": neural["neural_adaptation_halflife_s"],
            "pleasantness": neural["predicted_pleasantness"],
            "consonance": neural["consonance_score"],
            "interpretation": {
                "Phase 1: Discovery": "Novel sounds sustain attention — slow adaptation drives exploration",
                "Phase 2: Codification": "Patterns become recognizable — moderate adaptation as schemas form",
                "Phase 3: Ubiquity": "Highly predictable — fast adaptation, brain conserves resources",
                "Phase 4: Saturation": "Maximum habituation — 'boredom' is neural efficiency",
                "Phase 5: Rebellion": "Violation of expectations → renewed attention, slow adaptation",
                "Phase 6: Synthesis": "Balanced novelty-familiarity → sustained engagement",
            }.get(phase, ""),
        }
    
    for name, neural in results["traditions"].items():
        adaptation["tradition_adaptation"][name] = {
            "halflife_s": neural["neural_adaptation_halflife_s"],
            "pleasantness": neural["predicted_pleasantness"],
            "consonance": neural["consonance_score"],
        }
    
    adaptation_path = os.path.join(OUTPUT_DIR, "adaptation_rates.json")
    with open(adaptation_path, "w") as f:
        json.dump(adaptation, f, indent=2)
    print(f"Wrote: {adaptation_path}")

    # ── Print summary ──
    print("\n" + "="*70)
    print("NEURAL PREDICTIONS SUMMARY")
    print("="*70)
    
    print("\n--- Tradition Neural Profiles ---")
    for name, neural in results["traditions"].items():
        print(f"\n  {name}:")
        print(f"    Tenney height: {neural['tenney_height']:.2f}")
        print(f"    Consonance: {neural['consonance_score']:.3f}")
        print(f"    Brainstem FFR: {neural['brainstem_FFR_amplitude']:.3f}")
        print(f"    Pleasantness: {neural['predicted_pleasantness']}/10")
        print(f"    Adaptation half-life: {neural['neural_adaptation_halflife_s']:.1f}s")
        top_region = max(neural['cortical_activation'].items(), key=lambda x: x[1])
        print(f"    Peak cortical activation: {top_region[0]} ({top_region[1]:.3f})")
    
    print("\n--- Innovation Cycle Adaptation ---")
    for phase, neural in results["innovation_cycle_neural"].items():
        print(f"  {phase}: half-life={neural['neural_adaptation_halflife_s']:.1f}s, pleasantness={neural['predicted_pleasantness']}/10")
    
    print("\n--- Most Similar Neural Profiles ---")
    for pair in similar_pairs[:5]:
        print(f"  {pair['tradition_1']} ↔ {pair['tradition_2']}: neural_dist={pair['neural_distance']:.3f}, dial_dist={pair['dial_distance']:.3f}")
    
    print(f"\n  Dial–Neural distance correlation: r = {correlation:.3f}")
    
    print("\nDone.")


if __name__ == "__main__":
    main()
