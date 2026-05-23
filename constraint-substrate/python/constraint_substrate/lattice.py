"""Eisenstein A₂ lattice snapping.

The Eisenstein integers are Z[ω] where ω = e^{2πi/3} = (-1 + i√3)/2.
They form a hexagonal (triangular) lattice in the plane.

The lattice basis vectors in Cartesian coordinates are:
  e₁ = (1, 0)
  e₂ = (-1/2, √3/2)

A lattice point is a·e₁ + b·e₂ = (a - b/2, b·√3/2) for integers a, b.

The A₂ root lattice is the sublattice with a + b ≡ 0 (mod 3).
For general snapping we snap to the full Eisenstein integer lattice.
"""

import math

COVERING_RADIUS: float = 1.0 / math.sqrt(3.0)  # ≈ 0.577

# Basis vectors
_SQRT3 = math.sqrt(3.0)
# e₁ = (1, 0), e₂ = (-1/2, √3/2)
# Lattice point (a,b) → Cartesian (a - b/2, b·√3/2)


def snap(x: float, y: float, group_order: int = 3) -> tuple[float, float, float]:
    """Snap a 2D point to the nearest Eisenstein A₂ lattice point.

    Strategy: convert to approximate axial coordinates, then check the
    small set of candidate lattice points (at most 3-4) to find the
    true nearest neighbor. This is robust against floating-point issues
    at lattice boundaries.

    Returns (snapped_x, snapped_y, error_magnitude).
    """
    # Approximate axial coordinates:
    #   x = a - b/2, y = b·√3/2
    #   => b ≈ 2y/√3, a ≈ x + y/√3
    b_approx = 2.0 * y / _SQRT3
    a_approx = x + y / _SQRT3

    # The nearest lattice point must be one of the integer lattice points
    # with a in {floor(a_approx)-1, ..., ceil(a_approx)+1} and similar for b.
    # But for a hexagonal lattice, we only need to check ~3-4 candidates.
    a_lo = math.floor(a_approx)
    b_lo = math.floor(b_approx)

    best_dist_sq = float("inf")
    best_a = 0
    best_b = 0

    # Check candidate lattice points in a small neighborhood
    for da in range(-1, 2):
        for db in range(-1, 2):
            a = a_lo + da
            b = b_lo + db
            # Cartesian coordinates of lattice point (a, b)
            px = a - b / 2.0
            py = b * _SQRT3 / 2.0
            dist_sq = (px - x) ** 2 + (py - y) ** 2
            if dist_sq < best_dist_sq:
                best_dist_sq = dist_sq
                best_a = a
                best_b = b

    sx = best_a - best_b / 2.0
    sy = best_b * _SQRT3 / 2.0
    err = math.sqrt(best_dist_sq)
    return (sx, sy, err)


def snap_batch(
    values: list[tuple[float, float]], group_order: int = 3
) -> list[tuple[float, float, float]]:
    """Batch snap for N values."""
    return [snap(x, y, group_order) for x, y in values]
