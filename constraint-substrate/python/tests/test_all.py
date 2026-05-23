"""Tests for constraint-substrate (Python)."""

import json
import math
import os

import pytest

from constraint_substrate import (
    snap,
    snap_batch,
    COVERING_RADIUS,
    funnel_step,
    funnel_batch,
    holonomy_winding,
    is_laman,
    consensus_round,
)

TOLERANCE = 1e-9


# --- Lattice ---
class TestLattice:
    def test_snap_origin(self):
        sx, sy, err = snap(0.0, 0.0, 3)
        assert err < 1e-12
        assert abs(sx) < 1e-12
        assert abs(sy) < 1e-12

    def test_snap_known_1(self):
        sx, sy, err = snap(0.01, 0.99, 3)
        # Should snap to a nearby lattice point
        assert err < COVERING_RADIUS + 0.01
        # Verify it's actually on the lattice
        sqrt3 = math.sqrt(3.0)
        # Check b is integer
        b = sy * 2.0 / sqrt3
        assert abs(b - round(b)) < 1e-9

    def test_snap_known_2(self):
        x = math.sqrt(3.0) / 2.0 + 0.01
        sx, sy, err = snap(x, 0.02, 3)
        assert err < COVERING_RADIUS + 0.01

    def test_batch(self):
        vals = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
        results = snap_batch(vals, 3)
        assert len(results) == 3
        for sx, sy, err in results:
            assert err < 1.0  # max dist to any lattice point

    def test_covering_radius(self):
        assert abs(COVERING_RADIUS - 1.0 / math.sqrt(3.0)) < TOLERANCE

    def test_hex_rounding_nearest(self):
        """Verify snap actually finds the NEAREST lattice point."""
        # Point (0.4, 0.2) — should snap to (0, 0) not (0.866, 0)
        sx, sy, err = snap(0.4, 0.2, 3)
        # Distance to origin
        d_origin = math.sqrt(0.4**2 + 0.2**2)
        # If it snapped to (0,0), err == d_origin
        # If it snapped elsewhere, err should still be ≤ d_origin
        assert err <= d_origin + 1e-9

    def test_lattice_point_unchanged(self):
        """Lattice points should snap to themselves."""
        sqrt3 = math.sqrt(3.0)
        # (0, 0) → lattice point (a=0, b=0)
        sx, sy, err = snap(0.0, 0.0, 3)
        assert err < 1e-12
        # (1, 0) → lattice point (a=1, b=0)
        sx, sy, err = snap(1.0, 0.0, 3)
        assert err < 1e-12
        # (-0.5, √3/2) → lattice point (a=0, b=1)
        sx, sy, err = snap(-0.5, sqrt3 / 2.0, 3)
        assert err < 1e-12
        # (0.5, √3/2) → lattice point (a=1, b=1)
        sx, sy, err = snap(0.5, sqrt3 / 2.0, 3)
        assert err < 1e-12


# --- Funnel ---
class TestFunnel:
    def test_exponential_decay(self):
        """Epsilon must decay exponentially, not linearly."""
        _, eps = funnel_step(1.0, 2.0, 1.0, 0.1)
        # exp(-0.1) ≈ 0.9048, NOT 0.9 (linear)
        assert abs(eps - math.exp(-0.1)) < TOLERANCE

    def test_converges(self):
        current = 0.0
        target = 5.0
        eps = 1.0
        for _ in range(1000):
            current, eps = funnel_step(current, target, eps, 0.1)
        assert abs(current - target) < 0.5

    def test_within_deadband(self):
        val, new_eps = funnel_step(1.0, 1.05, 0.2, 0.1)
        # new_eps = 0.2 * exp(-0.1) ≈ 0.1810
        assert abs(new_eps - 0.2 * math.exp(-0.1)) < TOLERANCE
        assert val > 1.0

    def test_outside_deadband(self):
        val, new_eps = funnel_step(0.0, 5.0, 1.0, 0.1)
        # Outside deadband → step by epsilon
        assert abs(val - 1.0) < TOLERANCE
        assert abs(new_eps - math.exp(-0.1)) < TOLERANCE

    def test_batch(self):
        vals, eps = funnel_batch([0.0, 10.0], [5.0, 5.0], [1.0, 1.0], 0.1)
        assert len(vals) == 2
        assert len(eps) == 2
        # Both should have exponential decay
        for e in eps:
            assert abs(e - math.exp(-0.1)) < TOLERANCE

    def test_epsilon_stays_positive(self):
        """Exponential decay never reaches zero."""
        eps = 1.0
        for _ in range(10000):
            _, eps = funnel_step(0.0, 1.0, eps, 0.5)
        assert eps > 0.0


# --- Holonomy ---
class TestHolonomy:
    def test_zero_winding(self):
        w = holonomy_winding([1.0, 2.0, 3.0, 4.0], 10.0)
        assert abs(w - 0.3) < TOLERANCE

    def test_full_wind(self):
        w = holonomy_winding([1.0, 3.0, 5.0, 7.0, 9.0, 1.0], 10.0)
        assert abs(w - 1.0) < TOLERANCE

    def test_empty(self):
        w = holonomy_winding([], 10.0)
        assert abs(w) < TOLERANCE


# --- Rigidity ---
class TestRigidity:
    def test_triangle(self):
        """Triangle (3 vertices, 3 edges) is minimally rigid: 2*3-3=3."""
        assert is_laman(3, [(0, 1), (1, 2), (0, 2)])

    def test_not_laman(self):
        """1 edge on 3 vertices: not enough (need 3)."""
        assert not is_laman(3, [(0, 1)])

    def test_two_vertices(self):
        assert is_laman(2, [(0, 1)])

    def test_single_vertex(self):
        assert not is_laman(1, [])

    def test_k4_is_not_laman_but_rigid(self):
        """K4 (complete graph on 4 vertices) has 6 edges on 4 vertices.
        2*4-3 = 5, so K4 has too many edges for minimal rigidity.
        It IS rigid (redundantly), but does NOT satisfy Laman's exact condition.
        Our is_laman checks for minimal Laman, so K4 should return False."""
        assert not is_laman(4, [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)])

    def test_minimally_rigid_4_vertices(self):
        """4 vertices with exactly 5 edges (2*4-3=5), properly distributed."""
        # A square with one diagonal + one extra edge = 5 edges
        assert is_laman(4, [(0,1),(1,2),(2,3),(0,3),(0,2)])

    def test_too_many_edges_in_subgraph(self):
        """A graph that passes edge count but has a dense subgraph.
        5 vertices with 7 edges (2*5-3=7, exactly right).
        But if 4 of those vertices share 6 edges (K4), that's 6 > 2*4-3=5.
        This should FAIL Laman condition."""
        # Build a K4 on vertices 0-3 (6 edges), plus one edge to vertex 4
        edges = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3),(3,4)]
        assert not is_laman(5, edges)

    def test_hinge_not_rigid(self):
        """Two triangles sharing one vertex (hinge).
        5 vertices, 6 edges. Need 2*5-3=7. Not enough edges."""
        edges = [(0,1),(1,2),(0,2), (2,3),(3,4),(2,4)]
        assert not is_laman(5, edges)


# --- Consensus ---
class TestConsensus:
    def test_converges(self):
        current = [1.0, 2.0, 3.0]
        converged = False
        for _ in range(100):
            current, converged = consensus_round(current, 0.5)
            if converged:
                break
        assert converged
        for v in current:
            assert abs(v - 2.0) < 0.5

    def test_already_converged(self):
        vals, converged = consensus_round([2.0, 2.0, 2.0], 0.5)
        assert converged
        for v in vals:
            assert abs(v - 2.0) < TOLERANCE

    def test_empty(self):
        vals, converged = consensus_round([], 0.5)
        assert converged
        assert vals == []

    def test_circular_mean_wraparound(self):
        """Values near boundary: 0.1 and 9.9 with modulus 10.
        Arithmetic mean gives 5.0 (wrong).
        Circular mean should give ~0.0 (correct)."""
        vals, _ = consensus_round([0.1, 9.9], 0.5, modulus=10.0)
        # After convergence round, values should move toward ~0.0
        # Not toward 5.0
        mean = sum(vals) / len(vals)
        assert mean < 2.0 or mean > 8.0  # near 0 (mod 10), not near 5

    def test_circular_mean_no_wrap(self):
        """Non-wrapping values should behave like arithmetic mean."""
        vals, _ = consensus_round([2.0, 3.0], 0.5, modulus=10.0)
        mean = sum(vals) / len(vals)
        assert abs(mean - 2.5) < 0.5


# --- Cross-language test vectors ---
class TestVectors:
    """Validate against shared test vectors."""

    @pytest.fixture
    def vectors(self):
        vpath = os.path.join(
            os.path.dirname(__file__), "..", "..", "tests", "vectors.json"
        )
        with open(vpath) as f:
            return json.load(f)

    def test_lattice_vectors(self, vectors):
        for v in vectors["lattice"]["cases"]:
            sx, sy, err = snap(v["input"]["x"], v["input"]["y"], v["input"]["group_order"])
            assert abs(sx - v["output"]["x"]) < 0.1, f"snap x: expected {v['output']['x']}, got {sx}"
            assert abs(sy - v["output"]["y"]) < 0.1, f"snap y: expected {v['output']['y']}, got {sy}"

    def test_funnel_vectors(self, vectors):
        for v in vectors["funnel"]["cases"]:
            val, eps = funnel_step(
                v["input"]["current"], v["input"]["target"],
                v["input"]["epsilon"], v["input"]["decay"]
            )
            assert abs(val - v["output"]["value"]) < 1e-6
            assert abs(eps - v["output"]["epsilon"]) < 1e-6

    def test_holonomy_vectors(self, vectors):
        for v in vectors["holonomy"]["cases"]:
            w = holonomy_winding(v["input"]["values"], v["input"]["modulus"])
            assert abs(w - v["output"]["winding"]) < 1e-9

    def test_rigidity_vectors(self, vectors):
        for v in vectors["rigidity"]["cases"]:
            edges = [tuple(e) for e in v["input"]["edges"]]
            result = is_laman(v["input"]["n"], edges)
            assert result == v["output"]["is_rigid"]

    def test_consensus_vectors(self, vectors):
        for v in vectors["consensus"]["cases"]:
            vals, converged = consensus_round(
                v["input"]["values"], v["input"]["epsilon"]
            )
            assert converged == v["output"]["converged"]
            for got, expected in zip(vals, v["output"]["values"]):
                assert abs(got - expected) < 1e-9
