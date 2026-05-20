/// 2×2 eigendecomposition and matrix classification.
///
/// For a real 2×2 matrix [[a, b], [c, d]], compute eigenvalues and classify
/// the dynamical character (stable/unstable node, saddle, spiral, center, etc.).

#[derive(Debug, Clone, PartialEq)]
pub enum MatrixClass {
    /// Both eigenvalues real, same sign (|λ1| ≠ |λ2|): stable or unstable node
    Node { stable: bool },
    /// Both eigenvalues real, opposite signs: saddle point
    Saddle,
    /// Complex conjugate eigenvalues with nonzero real part: spiral
    Spiral { stable: bool },
    /// Purely imaginary eigenvalues: center (neutrally stable)
    Center,
    /// Repeated real eigenvalue
    Degenerate { stable: bool },
    /// Zero matrix or both eigenvalues zero
    Zero,
}

#[derive(Debug, Clone)]
pub enum Eigenvalues {
    Real(f64, f64),
    Complex { real: f64, imag: f64 }, // λ = real ± imag·i
}

/// Compute eigenvalues of a real 2×2 matrix [[a, b], [c, d]].
pub fn eigenvalues(a: f64, b: f64, c: f64, d: f64) -> Eigenvalues {
    let tr = a + d;
    let det = a * d - b * c;
    let discriminant = tr * tr - 4.0 * det;

    if discriminant >= 0.0 {
        let sqrt_disc = discriminant.sqrt();
        Eigenvalues::Real((tr + sqrt_disc) * 0.5, (tr - sqrt_disc) * 0.5)
    } else {
        Eigenvalues::Complex {
            real: tr * 0.5,
            imag: (-discriminant).sqrt() * 0.5,
        }
    }
}

/// Classify the dynamical character of a 2×2 real matrix.
pub fn classify(a: f64, b: f64, c: f64, d: f64) -> MatrixClass {
    const EPS: f64 = 1e-12;
    let eigs = eigenvalues(a, b, c, d);
    match eigs {
        Eigenvalues::Complex { real, imag: _ } => {
            if real.abs() < EPS {
                MatrixClass::Center
            } else {
                MatrixClass::Spiral { stable: real < 0.0 }
            }
        }
        Eigenvalues::Real(l1, l2) => {
            if l1.abs() < EPS && l2.abs() < EPS {
                MatrixClass::Zero
            } else if (l1 - l2).abs() < EPS {
                MatrixClass::Degenerate { stable: l1 < 0.0 }
            } else if l1 * l2 < 0.0 {
                MatrixClass::Saddle
            } else {
                // Same sign
                let stable = l1 < 0.0 && l2 < 0.0;
                MatrixClass::Node { stable }
            }
        }
    }
}

/// Compute eigenvector for eigenvalue `lambda` of [[a,b],[c,d]].
/// Returns a unit vector (vx, vy), or None if degenerate.
pub fn eigenvector(a: f64, b: f64, c: f64, d: f64, lambda: f64) -> Option<(f64, f64)> {
    // (A - λI)v = 0
    // Row 0: (a - λ)vx + b·vy = 0
    // Row 1: c·vx + (d - λ)vy = 0
    let r0 = (a - lambda, b);
    let r1 = (c, d - lambda);

    let (vx, vy) = if r0.0.abs() + r0.1.abs() > r1.0.abs() + r1.1.abs() {
        (-r0.1, r0.0)
    } else {
        (-r1.1, r1.0)
    };

    let norm = (vx * vx + vy * vy).sqrt();
    if norm < 1e-14 {
        None
    } else {
        Some((vx / norm, vy / norm))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn identity_is_degenerate_node() {
        match classify(1.0, 0.0, 0.0, 1.0) {
            MatrixClass::Degenerate { stable: false } => {}
            other => panic!("expected Degenerate{{stable:false}}, got {other:?}"),
        }
    }

    #[test]
    fn negative_identity_is_stable_degenerate() {
        match classify(-1.0, 0.0, 0.0, -1.0) {
            MatrixClass::Degenerate { stable: true } => {}
            other => panic!("expected Degenerate{{stable:true}}, got {other:?}"),
        }
    }

    #[test]
    fn rotation_is_center() {
        // [[0, -1], [1, 0]]: eigenvalues ±i
        match classify(0.0, -1.0, 1.0, 0.0) {
            MatrixClass::Center => {}
            other => panic!("expected Center, got {other:?}"),
        }
    }

    #[test]
    fn stable_spiral() {
        // [[-1, -2], [2, -1]]: tr=-2, det=5, disc=-16 → λ = -1 ± 2i
        match classify(-1.0, -2.0, 2.0, -1.0) {
            MatrixClass::Spiral { stable: true } => {}
            other => panic!("expected Spiral{{stable:true}}, got {other:?}"),
        }
    }

    #[test]
    fn saddle_point() {
        // [[2, 0], [0, -3]]: eigenvalues 2, -3
        match classify(2.0, 0.0, 0.0, -3.0) {
            MatrixClass::Saddle => {}
            other => panic!("expected Saddle, got {other:?}"),
        }
    }

    #[test]
    fn unstable_node() {
        // [[3, 1], [0, 2]]: eigenvalues 3, 2
        match classify(3.0, 1.0, 0.0, 2.0) {
            MatrixClass::Node { stable: false } => {}
            other => panic!("expected Node{{stable:false}}, got {other:?}"),
        }
    }

    #[test]
    fn eigenvalues_symmetric() {
        // Symmetric [[5, 2], [2, 3]]: det=11, tr=8, disc=64-44=20
        let eigs = eigenvalues(5.0, 2.0, 2.0, 3.0);
        match eigs {
            Eigenvalues::Real(l1, l2) => {
                let sum = l1 + l2;
                let prod = l1 * l2;
                assert!((sum - 8.0).abs() < 1e-10, "trace mismatch: {sum}");
                assert!((prod - 11.0).abs() < 1e-10, "det mismatch: {prod}");
            }
            _ => panic!("expected real eigenvalues"),
        }
    }
}
