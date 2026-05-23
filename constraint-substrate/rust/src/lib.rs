//! constraint-substrate — The 5 irreducible constraint primitives.
//!
//! Zero external dependencies. Works in `no_std` with `alloc`.

#![cfg_attr(not(feature = "std"), no_std)]

extern crate alloc;

use alloc::vec::Vec;

pub mod lattice {
    //! Eisenstein A₂ lattice snapping.

    /// Snap a 2D value to the nearest Eisenstein A₂ lattice point.
    ///
    /// The Eisenstein integers are Z[ω] where ω = e^{2πi/3}.
    /// Basis vectors in Cartesian coordinates:
    ///   e₁ = (1, 0)
    ///   e₂ = (-1/2, √3/2)
    /// Lattice point (a,b) → Cartesian (a - b/2, b·√3/2).
    ///
    /// Strategy: convert to approximate axial coordinates, then check
    /// candidate lattice points in a small neighborhood.
    ///
    /// Returns (snapped_x, snapped_y, error_magnitude).
    pub fn snap(x: f64, y: f64, _group_order: u32) -> (f64, f64, f64) {
        let sqrt3 = 3.0_f64.sqrt();

        // Approximate axial coordinates:
        //   x = a - b/2, y = b·√3/2
        //   => b ≈ 2y/√3, a ≈ x + y/√3
        let b_approx = 2.0 * y / sqrt3;
        let a_approx = x + y / sqrt3;

        let a_lo = a_approx.floor();
        let b_lo = b_approx.floor();

        let mut best_dist_sq = f64::INFINITY;
        let mut best_a: i64 = 0;
        let mut best_b: i64 = 0;

        // Check candidate lattice points in a small neighborhood
        for da in -1i64..=1 {
            for db in -1i64..=1 {
                let a = a_lo as i64 + da;
                let b = b_lo as i64 + db;
                // Cartesian coordinates of lattice point (a, b)
                let px = a as f64 - b as f64 / 2.0;
                let py = b as f64 * sqrt3 / 2.0;
                let dist_sq = (px - x) * (px - x) + (py - y) * (py - y);
                if dist_sq < best_dist_sq {
                    best_dist_sq = dist_sq;
                    best_a = a;
                    best_b = b;
                }
            }
        }

        let sx = best_a as f64 - best_b as f64 / 2.0;
        let sy = best_b as f64 * sqrt3 / 2.0;
        let err = ((sx - x) * (sx - x) + (sy - y) * (sy - y)).sqrt();
        (sx, sy, err)
    }

    /// Batch snap for N values (SIMD-ready structure).
    pub fn snap_batch(values: &[(f64, f64)], group_order: u32) -> Vec<(f64, f64, f64)> {
        values.iter().map(|(x, y)| snap(*x, *y, group_order)).collect()
    }

    /// Covering radius of A₂ lattice.
    pub fn covering_radius() -> f64 {
        1.0 / 3.0_f64.sqrt()
    }

    /// Covering radius as a constant (precomputed)
    pub const COVERING_RADIUS: f64 = 0.5773502691896258;
}

pub mod funnel {
    //! Deadband convergence funnel with exponential decay.

    /// One step of deadband convergence with exponential decay.
    ///
    /// The epsilon (deadband width) decays exponentially:
    ///     new_eps = epsilon * exp(-decay_rate)
    /// NOT linearly as epsilon * (1 - decay_rate).
    ///
    /// Exponential decay ensures:
    /// - Strictly positive epsilon (never reaches zero)
    /// - Smooth, natural convergence characteristic
    /// - Consistent halving behavior independent of current epsilon
    ///
    /// Returns (new_value, new_epsilon).
    pub fn step(current: f64, target: f64, epsilon: f64, decay_rate: f64) -> (f64, f64) {
        let diff = target - current;
        let new_eps = epsilon * (-decay_rate).exp();
        if diff.abs() < epsilon {
            // Within deadband — snap toward target
            let correction = diff * (1.0 - (-decay_rate).exp());
            (current + correction, new_eps)
        } else {
            // Outside deadband — pull toward target
            let step_size = diff.signum() * epsilon;
            (current + step_size, new_eps)
        }
    }

    /// Batch funnel step for N agents.
    pub fn step_batch(
        currents: &[f64],
        targets: &[f64],
        epsilons: &[f64],
        decay: f64,
    ) -> (Vec<f64>, Vec<f64>) {
        let n = currents.len();
        let mut new_values = Vec::with_capacity(n);
        let mut new_eps = Vec::with_capacity(n);
        for i in 0..n {
            let (v, e) = step(currents[i], targets[i], epsilons[i], decay);
            new_values.push(v);
            new_eps.push(e);
        }
        (new_values, new_eps)
    }
}

pub mod holonomy {
    //! Holonomy / winding number computation.

    /// Compute holonomy (winding number) of a sequence of values modulo `modulus`.
    pub fn winding(values: &[f64], modulus: f64) -> f64 {
        if values.is_empty() {
            return 0.0;
        }
        let mut total = 0.0;
        for i in 1..values.len() {
            let diff = values[i] - values[i - 1];
            let wrapped = diff - modulus * (diff / modulus).round();
            total += wrapped;
        }
        total / modulus
    }
}

pub mod rigidity {
    //! Laman rigidity checking.

    use alloc::vec;
    use alloc::collections::BTreeSet;

    /// Count edges where both endpoints lie in the vertex subset.
    fn edge_count_in_subgraph(edges: &[(u32, u32)], vertex_set: &BTreeSet<u32>) -> usize {
        let mut count = 0usize;
        for (u, v) in edges {
            if vertex_set.contains(u) && vertex_set.contains(v) {
                count += 1;
            }
        }
        count
    }

    /// Generate combinations of k items from n vertices.
    /// Returns sets of vertex indices.
    fn combinations(n: u32, k: u32) -> Vec<BTreeSet<u32>> {
        if k == 0 || k > n {
            return vec![];
        }
        let mut result = vec![];
        let mut current: BTreeSet<u32> = BTreeSet::new();
        combinations_recursive(0, n, k, &mut current, &mut result);
        result
    }

    fn combinations_recursive(
        start: u32,
        n: u32,
        k: u32,
        current: &mut BTreeSet<u32>,
        result: &mut Vec<BTreeSet<u32>>,
    ) {
        if current.len() == k as usize {
            result.push(current.clone());
            return;
        }
        for i in start..n {
            current.insert(i);
            combinations_recursive(i + 1, n, k, current, result);
            current.remove(&i);
        }
    }

    /// Check if a graph with `n` vertices and given edges satisfies
    /// Laman's condition for generic rigidity in 2D.
    ///
    /// Laman's theorem: a graph G = (V, E) is generically minimally rigid
    /// in 2D if and only if:
    ///   1. |E| = 2|V| - 3 (for |V| >= 2)
    ///   2. For every subset of k >= 2 vertices, the induced subgraph
    ///      has at most 2k - 3 edges.
    ///
    /// We also accept graphs with |E| >= 2|V| - 3 as rigid.
    /// For n <= 10, exact enumeration is used.
    pub fn is_laman(n: u32, edges: &[(u32, u32)]) -> bool {
        if n < 2 {
            return false;
        }
        if n == 2 {
            return edges.len() >= 1;
        }
        let required = 2 * n as usize - 3;
        if edges.len() < required {
            return false;
        }

        // Condition 2: every subset of k vertices must have at most 2k-3 edges.
        // For n <= 10, enumerate all subsets.
        if n <= 10 {
            for k in 2..=n {
                let limit = 2 * k as usize - 3;
                for subset in combinations(n, k) {
                    if edge_count_in_subgraph(edges, &subset) > limit {
                        return false;
                    }
                }
            }
        }
        // For n > 10 we skip the subgraph check (would need pebble game algorithm).

        true
    }
}

pub mod consensus {
    //! Metronome consensus rounds with circular mean support.

    /// Compute circular mean using atan2.
    ///
    /// If modulus is None or <= 0, falls back to arithmetic mean.
    /// Otherwise, treats values as cyclic on [0, modulus).
    fn circular_mean(values: &[f64], modulus: Option<f64>) -> f64 {
        if values.is_empty() {
            return 0.0;
        }

        match modulus {
            Some(m) if m > 0.0 => {
                let two_pi = 2.0 * core::f64::consts::PI;
                let mut sin_sum = 0.0;
                let mut cos_sum = 0.0;
                for v in values {
                    let angle = (v / m) * two_pi;
                    sin_sum += angle.sin();
                    cos_sum += angle.cos();
                }
                let n = values.len() as f64;
                let mut mean_angle = (sin_sum / n).atan2(cos_sum / n);
                if mean_angle < 0.0 {
                    mean_angle += two_pi;
                }
                (mean_angle / two_pi) * m
            }
            _ => {
                values.iter().sum::<f64>() / values.len() as f64
            }
        }
    }

    /// One round of metronome consensus.
    ///
    /// If modulus is provided, uses circular mean (atan2-based) to correctly
    /// handle wrap-around for cyclic/phase values. Otherwise uses arithmetic mean.
    ///
    /// Returns (new_values, converged).
    pub fn round(values: &[f64], epsilon: f64, modulus: Option<f64>) -> (Vec<f64>, bool) {
        if values.is_empty() {
            return (Vec::new(), true);
        }

        let mean = circular_mean(values, modulus);
        let mut new_values = Vec::with_capacity(values.len());
        let mut all_converged = true;

        for v in values {
            let mut diff = mean - v;
            // For cyclic values, take shortest path around the circle
            // Use proper Euclidean modulo (always non-negative for positive divisor)
            if let Some(m) = modulus {
                if m > 0.0 {
                    let shifted = diff + m / 2.0;
                    let rem = shifted - (shifted / m).floor() * m;
                    diff = rem - m / 2.0;
                }
            }
            if diff.abs() > epsilon {
                all_converged = false;
                new_values.push(v + diff.signum() * epsilon * 0.5);
            } else {
                new_values.push(mean);
            }
        }
        (new_values, all_converged)
    }
}
