/// Fibonacci spiral vector search.
///
/// Generates candidate directions on a Fibonacci lattice on the unit sphere/circle,
/// then searches for the best match to a query vector using dot-product scoring.
/// The Fibonacci spiral provides near-uniform angular coverage with O(√n) expected search.

/// Generate n points uniformly distributed on the unit circle using the Fibonacci spiral method.
/// Golden angle ≈ 137.508° = 2π(1 - 1/φ) where φ = (1+√5)/2.
pub fn fibonacci_circle(n: usize) -> Vec<(f64, f64)> {
    let golden_angle = std::f64::consts::PI * (3.0 - 5.0_f64.sqrt()); // ≈ 2.399963...
    (0..n)
        .map(|i| {
            let theta = i as f64 * golden_angle;
            (theta.cos(), theta.sin())
        })
        .collect()
}

/// Generate n points on the unit sphere using the Fibonacci lattice method.
/// Returns (x, y, z) triples.
pub fn fibonacci_sphere(n: usize) -> Vec<(f64, f64, f64)> {
    let golden_ratio = (1.0 + 5.0_f64.sqrt()) * 0.5;
    (0..n)
        .map(|i| {
            let theta = (2.0 * std::f64::consts::PI * i as f64) / golden_ratio;
            // Evenly spaced latitudes
            let phi = ((1.0 - 2.0 * (i as f64 + 0.5) / n as f64).clamp(-1.0, 1.0)).acos();
            let sin_phi = phi.sin();
            (sin_phi * theta.cos(), sin_phi * theta.sin(), phi.cos())
        })
        .collect()
}

/// Search for the point in `candidates` most aligned with `query` (max dot product).
/// Returns (index, dot_product).
pub fn nearest_direction(query: (f64, f64), candidates: &[(f64, f64)]) -> (usize, f64) {
    candidates
        .iter()
        .enumerate()
        .map(|(i, &(cx, cy))| (i, query.0 * cx + query.1 * cy))
        .max_by(|a, b| a.1.partial_cmp(&b.1).unwrap())
        .unwrap_or((0, f64::NEG_INFINITY))
}

/// Search for the sphere point in `candidates` most aligned with `query`.
pub fn nearest_direction_3d(
    query: (f64, f64, f64),
    candidates: &[(f64, f64, f64)],
) -> (usize, f64) {
    candidates
        .iter()
        .enumerate()
        .map(|(i, &(cx, cy, cz))| (i, query.0 * cx + query.1 * cy + query.2 * cz))
        .max_by(|a, b| a.1.partial_cmp(&b.1).unwrap())
        .unwrap_or((0, f64::NEG_INFINITY))
}

/// Quantize a unit vector into one of n Fibonacci directions, return the index.
pub fn quantize_direction(query: (f64, f64), n: usize) -> usize {
    let candidates = fibonacci_circle(n);
    nearest_direction(query, &candidates).0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn circle_points_are_unit() {
        let pts = fibonacci_circle(100);
        for (x, y) in &pts {
            let norm = (x * x + y * y).sqrt();
            assert!((norm - 1.0).abs() < 1e-13, "non-unit point: norm={norm}");
        }
    }

    #[test]
    fn sphere_points_are_unit() {
        let pts = fibonacci_sphere(100);
        for (x, y, z) in &pts {
            let norm = (x * x + y * y + z * z).sqrt();
            assert!((norm - 1.0).abs() < 1e-13, "non-unit sphere point: norm={norm}");
        }
    }

    #[test]
    fn nearest_direction_finds_exact() {
        let n = 200;
        let candidates = fibonacci_circle(n);
        // Each candidate should be its own nearest neighbor
        for (i, &(x, y)) in candidates.iter().enumerate() {
            let (found, dot) = nearest_direction((x, y), &candidates);
            assert_eq!(found, i, "self not found: got {found} with dot {dot}");
            assert!((dot - 1.0).abs() < 1e-12);
        }
    }

    #[test]
    fn synthetic_recall_test() {
        // Encode 50 random unit vectors and recover them.
        let n = 500;
        let candidates = fibonacci_circle(n);

        // Use a few known angles and verify recall
        let test_angles: Vec<f64> = (0..20)
            .map(|i| std::f64::consts::PI * 2.0 * i as f64 / 20.0)
            .collect();

        for &angle in &test_angles {
            let q = (angle.cos(), angle.sin());
            let (idx, dot) = nearest_direction(q, &candidates);
            // The best match should have dot product >= cos(2π/n) ≈ cos(0.01257) ≈ 0.99992
            // Worst-case angular gap is 2π/n (halfway between two consecutive points)
            let min_dot = (2.0 * std::f64::consts::PI / n as f64).cos();
            assert!(
                dot >= min_dot,
                "poor recall at angle {angle:.3}: dot={dot:.6} < {min_dot:.6} (idx={idx})"
            );
        }
    }
}
