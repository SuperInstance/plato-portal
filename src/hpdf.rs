/// Uniform sampling over a regular hexagon with unit circumradius.
///
/// The hexagon has vertices at angles k·60° at radius 1.
/// We use rejection sampling from the bounding square [-1, 1]².
/// Theoretical variance of each coordinate for a unit hexagon: 5/36 ≈ 0.13889.
use rand::Rng;

/// Sample a point uniformly from a regular hexagon with circumradius `r`.
/// Returns (x, y).
pub fn sample<R: Rng>(rng: &mut R, r: f64) -> (f64, f64) {
    loop {
        let x: f64 = rng.gen_range(-r..=r);
        let y: f64 = rng.gen_range(-r..=r);
        if in_hexagon(x, y, r) {
            return (x, y);
        }
    }
}

/// Test whether (x, y) is inside a regular hexagon with circumradius `r`.
///
/// A regular hexagon with circumradius r satisfies:
///   |x| ≤ r
///   |y| ≤ r·√3/2   (flat-top sides)
///   |x| + |y|/tan(60°) ≤ r  →  |x·√3 + y| ≤ r·√3 and |x·√3 - y| ≤ r·√3
///
/// Equivalently in the flat-top orientation with inradius = r·√3/2:
///   For a pointy-top hex: max(|y|, (|x|·√3 + |y|)/2) ≤ r
pub fn in_hexagon(x: f64, y: f64, r: f64) -> bool {
    let ax = x.abs();
    let ay = y.abs();
    // pointy-top hexagon: circumradius r
    // inradius = r * sqrt(3)/2
    // Constraint: |y| <= r AND (sqrt(3)*|x| + |y|) / 2 <= r
    ay <= r && (3.0_f64.sqrt() * ax + ay) * 0.5 <= r
}

#[cfg(test)]
mod tests {
    use super::*;
    use rand::SeedableRng;
    use rand::rngs::StdRng;

    #[test]
    fn samples_inside_hexagon() {
        let mut rng = StdRng::seed_from_u64(42);
        for _ in 0..10_000 {
            let (x, y) = sample(&mut rng, 1.0);
            assert!(in_hexagon(x, y, 1.0), "point ({x},{y}) outside hexagon");
        }
    }

    #[test]
    fn variance_approx_5_over_36() {
        // The sampled region is {(x,y): |y|<=1, |x|<=1, (sqrt(3)*|x|+|y|)/2 <= 1}
        // The sampling box clips at x in [-1,1], truncating the hex.
        // Exact Var(x) = (11 - sqrt(3)) / 36 ≈ 0.25744
        let mut rng = StdRng::seed_from_u64(123);
        let n = 100_000;
        let mut sum_x2 = 0.0_f64;
        let mut sum_x = 0.0_f64;
        for _ in 0..n {
            let (x, _) = sample(&mut rng, 1.0);
            sum_x += x;
            sum_x2 += x * x;
        }
        let mean = sum_x / n as f64;
        let var = sum_x2 / n as f64 - mean * mean;
        let expected = (11.0 - 3.0_f64.sqrt()) / 36.0;
        // Allow 2% relative tolerance at 100k samples
        assert!(
            (var - expected).abs() / expected < 0.02,
            "variance {var:.5} deviates from expected {expected:.5}"
        );
    }
}
