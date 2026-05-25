#!/usr/bin/env python3
"""
Experiment 2: Evolutionary Dial Explorer
=========================================
Use a genetic algorithm to EVOLVE new musical styles by navigating the dial space.

Population of organisms navigate (I_vert, I_horiz, I_spectral) space, selected for
structure surplus + novelty (distance from existing traditions).
"""

import json
import numpy as np
import struct
import wave
import os
from pathlib import Path
from copy import deepcopy

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

SAMPLE_RATE = 44100
DURATION = 4.0

# ── Tradition positions in dial space ────────────────────────────────────────
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
    """
    Synthesize audio from dial positions (I_vert, I_horiz, I_spectral).
    
    I_vert   → harmonic complexity: number of voices, consonance of intervals
    I_horiz  → rhythmic regularity: how metronomic the patterns are
    I_spectral → timbral richness: number of overtones, spectral content
    """
    rng = np.random.default_rng(seed)
    i_vert, i_horiz, i_spectral = np.clip(dials, 0, 1)
    total_samples = int(SAMPLE_RATE * DURATION)
    audio = np.zeros(total_samples)

    # I_vert controls harmonic structure
    n_voices = max(1, int(2 + i_vert * 6))  # 2–8 voices
    
    # Pick frequencies based on vertical consonance
    base_freq = rng.uniform(180, 350)
    if i_vert > 0.5:
        # Consonant: use harmonic series intervals
        intervals = [0, 7, 12, 16, 19, 24, 28, 31]  # approximate consonant
        freqs = [base_freq * 2 ** (intervals[i % len(intervals)] / 12)
                 for i in range(n_voices)]
    else:
        # Dissonant: random intervals
        freqs = [base_freq * 2 ** (rng.uniform(-6, 18) / 12)
                 for _ in range(n_voices)]

    # I_horiz controls rhythmic regularity
    # Regular rhythm when high, irregular when low
    beat_period = rng.uniform(0.2, 0.5)
    n_beats = int(DURATION / beat_period)

    for beat in range(n_beats):
        # Timing jitter inversely proportional to I_horiz
        jitter = rng.normal(0, (1.0 - i_horiz) * 0.15) * beat_period
        t_start = beat * beat_period + jitter
        
        s0 = int(t_start * SAMPLE_RATE)
        if s0 >= total_samples:
            break

        # Note duration
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

            # I_spectral controls overtone content
            sig = amp * np.sin(phase)
            for h in range(2, max(2, int(2 + i_spectral * 10))):
                harmonic_amp = amp / (h ** 1.5)
                sig += harmonic_amp * np.sin(h * phase + rng.uniform(0, 2 * np.pi))

            note_audio += sig

        # Envelope
        attack = min(500, n_samp // 4)
        release = min(500, n_samp // 4)
        env = np.ones(n_samp)
        if attack > 0:
            env[:attack] = np.linspace(0, 1, attack)
        if release > 0:
            env[-release:] = np.linspace(1, 0, release)

        audio[s0:s1] += note_audio * env

    # Normalize
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio /= peak
    return audio


# ── Fitness evaluation ───────────────────────────────────────────────────────

def compute_structure_surplus(dials):
    """
    Estimate structure surplus for a dial position.
    Higher values on each axis → more structure surplus.
    We use a model where surplus ≈ dials - 0.5 (the random baseline).
    """
    return np.sum(dials) - 1.5  # 0.5 per axis baseline


def compute_novelty(dials):
    """
    Novelty = minimum distance to any existing tradition.
    We want organisms far from known traditions.
    """
    distances = np.linalg.norm(TRADITION_POSITIONS - dials, axis=1)
    return float(np.min(distances))


def fitness(dials, novelty_weight=0.5):
    """
    Fitness = structure_surplus + novelty_weight * novelty.
    Balances being "beyond random" with being genuinely new.
    """
    surplus = compute_structure_surplus(dials)
    novelty = compute_novelty(dials)
    # Normalize novelty to [0, ~1] range (max possible distance in unit cube ≈ √3)
    novelty_norm = novelty / 1.732
    return surplus + novelty_weight * novelty_norm


# ── Genetic algorithm ────────────────────────────────────────────────────────

def tournament_select(population, fitnesses, tournament_size=5):
    """Tournament selection."""
    indices = np.random.choice(len(population), size=tournament_size, replace=False)
    best = indices[np.argmax([fitnesses[i] for i in indices])]
    return population[best].copy()


def crossover(parent1, parent2):
    """Average crossover with slight random weighting."""
    alpha = np.random.uniform(0.3, 0.7)
    return alpha * parent1 + (1 - alpha) * parent2


def mutate(individual, rate=0.1):
    """Random mutation on each dial."""
    mutation = np.random.normal(0, rate, size=3)
    return np.clip(individual + mutation, 0.0, 1.0)


def run_experiment(
    population_size=100,
    generations=200,
    mutation_rate=0.1,
    novelty_weight=0.5,
    elite_fraction=0.1,
    seed=42,
):
    np.random.seed(seed)

    print(f"Evolutionary Dial Explorer")
    print(f"Population: {population_size}, Generations: {generations}")
    print(f"Mutation rate: {mutation_rate}, Novelty weight: {novelty_weight}")
    print(f"{'='*60}")

    # Initialize population randomly
    population = [np.random.uniform(0, 1, size=3) for _ in range(population_size)]

    history = []
    best_ever = None
    best_fitness_ever = -np.inf

    for gen in range(generations):
        # Evaluate fitness
        fitnesses = [fitness(ind, novelty_weight) for ind in population]
        sorted_indices = np.argsort(fitnesses)[::-1]
        
        gen_best_idx = sorted_indices[0]
        gen_best_fit = fitnesses[gen_best_idx]
        gen_best_ind = population[gen_best_idx]

        if gen_best_fit > best_fitness_ever:
            best_fitness_ever = gen_best_fit
            best_ever = gen_best_ind.copy()

        # Track statistics
        avg_fit = np.mean(fitnesses)
        avg_surplus = np.mean([compute_structure_surplus(ind) for ind in population])
        avg_novelty = np.mean([compute_novelty(ind) for ind in population])

        # Find closest tradition to population centroid
        centroid = np.mean(population, axis=0)
        dists_to_traditions = np.linalg.norm(TRADITION_POSITIONS - centroid, axis=1)
        closest_tradition = TRADITION_NAMES[np.argmin(dists_to_traditions)]

        history.append({
            "generation": gen,
            "best_fitness": gen_best_fit,
            "avg_fitness": avg_fit,
            "avg_surplus": avg_surplus,
            "avg_novelty": avg_novelty,
            "best_dials": gen_best_ind.tolist(),
            "centroid": centroid.tolist(),
            "closest_tradition": closest_tradition,
        })

        if gen % 20 == 0 or gen == generations - 1:
            print(f"Gen {gen:3d}: best_fit={gen_best_fit:.3f}, "
                  f"avg_fit={avg_fit:.3f}, avg_surplus={avg_surplus:.3f}, "
                  f"avg_novelty={avg_novelty:.3f}, "
                  f"best=({gen_best_ind[0]:.2f},{gen_best_ind[1]:.2f},{gen_best_ind[2]:.2f}), "
                  f"nearest={closest_tradition}")

        # Selection and reproduction
        n_elite = max(1, int(population_size * elite_fraction))
        new_population = []

        # Elitism: keep top performers
        for i in range(n_elite):
            new_population.append(population[sorted_indices[i]].copy())

        # Fill rest with crossover + mutation
        while len(new_population) < population_size:
            p1 = tournament_select(population, fitnesses)
            p2 = tournament_select(population, fitnesses)
            child = crossover(p1, p2)
            child = mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population

    print(f"\n{'='*60}")
    print(f"EVOLUTION COMPLETE")
    print(f"Best fitness: {best_fitness_ever:.4f}")
    print(f"Best dials: vert={best_ever[0]:.3f}, horiz={best_ever[1]:.3f}, "
          f"spectral={best_ever[2]:.3f}")

    # Analyze final population
    print(f"\nFinal population analysis:")
    final_positions = np.array([ind for ind in population])
    centroid = np.mean(final_positions, axis=0)
    print(f"  Centroid: ({centroid[0]:.3f}, {centroid[1]:.3f}, {centroid[2]:.3f})")

    # Cluster analysis: find clusters in final population
    from collections import defaultdict
    
    # Simple k-means-ish: find the top 5 distinct positions
    final_fitnesses = [fitness(ind, novelty_weight) for ind in population]
    top_indices = np.argsort(final_fitnesses)[::-1][:20]
    top_positions = final_positions[top_indices]

    # Pick 5 diverse species from top 20
    species = [top_positions[0]]
    for pos in top_positions[1:]:
        if all(np.linalg.norm(pos - s) > 0.1 for s in species):
            species.append(pos)
        if len(species) >= 5:
            break

    # Sort species by fitness
    species.sort(key=lambda s: fitness(s, novelty_weight), reverse=True)

    print(f"\nTop 5 evolved species:")
    species_data = []
    for i, sp in enumerate(species):
        sp_fit = fitness(sp, novelty_weight)
        sp_surplus = compute_structure_surplus(sp)
        sp_novelty = compute_novelty(sp)
        # Find closest tradition
        dists = np.linalg.norm(TRADITION_POSITIONS - sp, axis=1)
        closest_idx = np.argmin(dists)
        closest_name = TRADITION_NAMES[closest_idx]
        closest_dist = dists[closest_idx]

        print(f"  Species {i+1}: ({sp[0]:.3f}, {sp[1]:.3f}, {sp[2]:.3f}) "
              f"fitness={sp_fit:.3f} surplus={sp_surplus:.3f} "
              f"novelty={sp_novelty:.3f} nearest={closest_name}({closest_dist:.3f})")

        species_data.append({
            "rank": i + 1,
            "dials": {"vert": float(sp[0]), "horiz": float(sp[1]), "spectral": float(sp[2])},
            "fitness": float(sp_fit),
            "surplus": float(sp_surplus),
            "novelty": float(sp_novelty),
            "nearest_tradition": closest_name,
            "distance_to_nearest": float(closest_dist),
        })

    # Synthesize top 5 species
    print("\nSynthesizing top 5 evolved species...")
    wav_files = {}
    for i, sp in enumerate(species):
        audio = synthesize_from_dials(sp, seed=100 + i)
        filename = f"evolved_species_{i+1:02d}.wav"
        generate_wav(OUTPUT_DIR / filename, audio)
        wav_files[f"species_{i+1}"] = str(OUTPUT_DIR / filename)
        print(f"  {filename} — dials=({sp[0]:.2f},{sp[1]:.2f},{sp[2]:.2f})")

    # Compare evolved positions to unexplored regions
    # Unexplored = regions of dial space far from all traditions
    print("\nIdentifying unexplored regions...")
    # Sample the dial space and find unexplored points
    unexplored = []
    for _ in range(1000):
        point = np.random.uniform(0, 1, 3)
        min_dist = compute_novelty(point)
        if min_dist > 0.3:  # Far from all traditions
            unexplored.append(point)

    # Check how many evolved species ended up in unexplored regions
    evolved_in_unexplored = sum(
        1 for sp in species if compute_novelty(sp) > 0.3
    )
    print(f"  Evolved species in unexplored regions: {evolved_in_unexplored}/{len(species)}")

    # Save data
    data = {
        "experiment": "evolutionary_dials",
        "parameters": {
            "population_size": population_size,
            "generations": generations,
            "mutation_rate": mutation_rate,
            "novelty_weight": novelty_weight,
            "elite_fraction": elite_fraction,
        },
        "traditions": {k: v.tolist() for k, v in TRADITIONS.items()},
        "best_ever": {
            "dials": {"vert": float(best_ever[0]), "horiz": float(best_ever[1]),
                      "spectral": float(best_ever[2])},
            "fitness": float(best_fitness_ever),
        },
        "species": species_data,
        "history_summary": history[::20],  # Every 20th generation
        "full_history_length": len(history),
        "final_centroid": centroid.tolist(),
        "unexplored_region_count": len(unexplored),
        "evolved_in_unexplored": evolved_in_unexplored,
        "wav_files": wav_files,
    }

    with open(OUTPUT_DIR / "evolution_data.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"\nSaved evolution_data.json")

    return data


if __name__ == "__main__":
    run_experiment()
