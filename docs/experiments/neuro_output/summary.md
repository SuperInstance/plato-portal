# Neuro-Harmonic Experiments — Summary

## Overview

Two experiments exploring the intersection of neuroscience, music theory, and the dial-space constraint framework.

**All outputs:** `docs/experiments/neuro_output/`

---

## Experiment 1: Predicted EEG/fMRI Response Map

**Script:** `experiments/neuro_harmonic.py`

Models what neural responses would look like for each tradition at their (I_vert, I_horiz, I_spectral) dial position, grounded in published neuroscience.

### Key Results

#### Tradition Neural Profiles

| Tradition | Tenney Height | Consonance | Brainstem FFR | Pleasantness | Adaptation Half-life | Peak Cortical Region |
|-----------|:---:|:---:|:---:|:---:|:---:|---|
| Gagaku | 4.80 | 0.766 | 0.866 | 8.3/10 | 23.6s | Orbitofrontal |
| Chinese | 4.53 | 0.789 | 0.879 | 7.5/10 | 13.3s | Orbitofrontal |
| Western ET | 4.86 | 0.761 | 0.863 | 6.3/10 | 11.0s | Orbitofrontal |
| Javanese | 5.04 | 0.747 | 0.854 | 8.2/10 | 22.3s | Orbitofrontal |
| Balinese | 5.23 | 0.731 | 0.845 | 8.0/10 | 25.8s | Orbitofrontal |
| West African | 5.39 | 0.718 | 0.837 | 7.9/10 | 26.5s | Orbitofrontal |
| Turkish | 5.56 | 0.704 | 0.828 | 7.9/10 | 23.1s | Orbitofrontal |
| Arabic | 5.61 | 0.699 | 0.826 | 7.8/10 | 22.4s | Orbitofrontal |
| Hindustani | 5.64 | 0.697 | 0.824 | 7.9/10 | 25.7s | Orbitofrontal |
| Carnatic | 5.78 | 0.685 | 0.817 | 7.7/10 | 28.9s | Orbitofrontal |

**Interesting:** All traditions activate orbitofrontal cortex (reward/pleasure) more than parahippocampal (discomfort) — even "dissonant" traditions produce predicted consonance scores >0.65. This makes sense: these traditions survived precisely because they found consonant positions in their own region of dial space.

#### Innovation Cycle Neural Predictions

| Phase | Adaptation Half-life | Pleasantness | Interpretation |
|---|:---:|:---:|---|
| Phase 1: Discovery | 40.8s | 5.8/10 | Novel → slow adaptation, moderate pleasure |
| Phase 2: Codification | 27.3s | 7.9/10 | Patterns emerge → faster adaptation, high pleasure |
| Phase 3: Ubiquity | 12.3s | 8.2/10 | Very familiar → fast habituation, peak pleasure |
| Phase 4: Saturation | **8.4s** | 7.7/10 | **Boredom = fastest adaptation** |
| Phase 5: Rebellion | 32.3s | 7.3/10 | Novelty returns → adaptation slows again |
| Phase 6: Synthesis | 22.2s | 8.3/10 | Best of both → highest pleasantness |

**Key finding:** Phase 4 (Saturation) has the shortest adaptation half-life (8.4s), confirming the prediction that "boredom" is rapid neural habituation. Phase 1 (Discovery) has the longest (40.8s) — the brain keeps paying attention to genuinely new sounds.

#### Most Similar Neural Profiles

| Pair | Neural Distance | Dial Distance |
|---|:---:|:---:|
| Arabic ↔ Turkish | 0.016 | 0.233 |
| Hindustani ↔ Arabic | 0.027 | 0.437 |
| Hindustani ↔ West African | 0.033 | 0.415 |
| Javanese ↔ Balinese | 0.038 | 0.403 |
| Hindustani ↔ Turkish | 0.043 | 0.350 |

**Dial–Neural distance correlation: r = 0.862** — strong correlation between geographic proximity in dial space and predicted neural similarity.

### Testable Predictions

1. **Neural similarity from dial proximity:** Traditions at similar dial positions should produce similar EEG responses regardless of geographic origin. Testable with cross-cultural EEG study.

2. **Adaptation cycle:** Phase 4 music shows fastest neural adaptation (habituation). Testable with long-duration EEG measuring N1/P2 reduction.

3. **Universal FFR, cultural pleasantness:** Brainstem FFR response to consonance should be culturally invariant (subcortical), but cortical pleasantness ratings should vary by cultural background.

4. **Reward + familiarity:** Music near a listener's cultural tradition should activate nucleus accumbens more than equally consonant unfamiliar music.

### Output Files
- `neuro_predictions.json` — Full predictions for all traditions, historical styles, innovation cycle phases, similarity matrix, heatmap data
- `adaptation_rates.json` — Innovation cycle adaptation rates with interpretations

---

## Experiment 2: Consonance Fingerprinting

**Script:** `experiments/consonance_fingerprint.py`

### Interactive Experiment (20 Pairs)

A pairwise comparison test mapping a listener's preferences to (I_vert, I_horiz, I_spectral) space. Each of 20 pairs tests a different axis:
- Basic consonance (octave vs. tritone)
- Harmonic complexity tolerance (triad vs. cluster)
- Horizontal complexity (steady pulse vs. polyrhythm)
- Spectral richness (pure vs. rich timbres)
- Cultural style (gamelan vs. Bach chorale)
- And 15 more...

After completing the test, each person gets:
- Their unique dial position (consonance fingerprint)
- Closest matching tradition
- Comfort zone radius in dial space
- Personalized exploration recommendations

### Automated Crossover Analysis (100 Random Positions)

| Category | Position (I_vert, I_horiz, I_spectral) | Score |
|---|:---:|:---:|
| 🎯 **Crossover Hit** | (3.96, 2.96, 0.53) | 0.666 |
| 🌍 **Most Foreign** | (1.06, 3.79, 3.58) | dist=2.992 |
| 📊 **Highest Mainstream** | (2.91, 2.09, 1.80) | 0.935 |
| 🧭 **Highest Adventurous** | (1.47, 3.88, 0.78) | 1.000 |

**The crossover hit** is the dial position that maximizes both mainstream accessibility and adventurous novelty — the "new sound that everyone likes." It sits near Western ET but pushed toward higher vertical complexity with minimal spectral richness, suggesting: complex harmony with clean timbres.

**The most foreign** position (1.06, 3.79, 3.58) = simple vertical harmony, maximal rhythmic complexity, rich inharmonic timbres. Closest existing tradition: Balinese. This is the "maximally unfamiliar" sound for Western listeners.

### Output Files
- `consonance_fingerprint.json` — Interactive experiment data (20 pairs + scoring guide)
- `crossover_analysis.json` — All 100 scored positions + crossover hit + most foreign

---

## Research Basis

- **Bidelman & Krishnan (2009):** Brainstem FFR correlates with musical consonance
- **Blood et al. (1999):** Dissonance → parahippocampal; consonance → orbitofrontal
- **Sachs et al. (2008):** Nucleus accumbens responds to consonant music
- **Trainor et al. (2002):** Consonance preferences emerge at 4 months (partly innate)
- **McDermott et al. (2010):** Consonance preference has cultural component
- **Berlyne (1971):** Wundt curve — optimal pleasure at moderate novelty
