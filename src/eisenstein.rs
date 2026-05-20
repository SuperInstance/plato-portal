/// Snap a Cartesian point (x, y) to the nearest Eisenstein integer.
///
/// The Eisenstein lattice Z[ω] has basis vectors:
///   e1 = (1, 0)
///   e2 = ω = (-1/2, √3/2)
///
/// A lattice point n·e1 + m·e2 has Cartesian coords:
///   X = n - m/2
///   Y = m·√3/2
///
/// Inverse: given (x, y),
///   m = y / (√3/2) = 2y/√3
///   n = x + m/2
///
/// Returns (n, m, error) where error is the Euclidean distance from (x,y) to the snapped point.
pub fn snap(x: f64, y: f64) -> (i64, i64, f64) {
    const SQRT3_OVER2: f64 = 0.8660254037844386_f64; // √3/2

    // Project into oblique lattice coordinates
    let m_f = y / SQRT3_OVER2;
    let n_f = x + 0.5 * m_f;

    // Round to nearest integer lattice point
    let nr = n_f.round() as i64;
    let mr = m_f.round() as i64;

    // Back-project to Cartesian
    let sx = nr as f64 - 0.5 * mr as f64;
    let sy = mr as f64 * SQRT3_OVER2;

    let err = ((x - sx).powi(2) + (y - sy).powi(2)).sqrt();
    (nr, mr, err)
}

/// Return the Cartesian coordinates of an Eisenstein integer (n, m).
pub fn to_cartesian(n: i64, m: i64) -> (f64, f64) {
    const SQRT3_OVER2: f64 = 0.8660254037844386_f64;
    let x = n as f64 - 0.5 * m as f64;
    let y = m as f64 * SQRT3_OVER2;
    (x, y)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn lattice_points_snap_with_zero_error() {
        for n in -5_i64..=5 {
            for m in -5_i64..=5 {
                let (x, y) = to_cartesian(n, m);
                let (sn, sm, err) = snap(x, y);
                assert_eq!(sn, n, "n mismatch for ({n},{m})");
                assert_eq!(sm, m, "m mismatch for ({n},{m})");
                assert!(err < 1e-10, "non-zero error {err} for ({n},{m})");
            }
        }
    }
}
