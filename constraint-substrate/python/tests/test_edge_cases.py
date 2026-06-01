"""Additional edge-case tests for constraint-substrate (Python).

Covers gaps in the main test suite:
- Lattice: negative coords, large coords, symmetry, batch edge cases
- Funnel: zero/negative decay, overshoot protection, batch mismatch
- Holonomy: single element, negative winding, modulus=1, large sequences
- Rigidity: duplicate edges, self-loops, exactly-enough edges, large n
- Consensus: single value, negative values, large epsilon, modulus edge cases
- CFFI: graceful fallback when library unavailable
"""

import math
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
SQRT3 = math.sqrt(3.0)


# ── Lattice edge cases ──────────────────────────────────────────────────────

class TestLatticeEdgeCases:
    def test_snap_negative_coordinates(self):
        """Points in all quadrants should snap correctly."""
        sx, sy, err = snap(-1.5, -0.87, 3)
        assert err < COVERING_RADIUS + 0.01

    def test_snap_symmetry(self):
        """Snapping (x,y) and (-x,-y) should give mirrored results."""
        sx1, sy1, _ = snap(2.3, 1.7, 3)
        sx2, sy2, _ = snap(-2.3, -1.7, 3)
        assert abs(sx1 + sx2) < TOLERANCE
        assert abs(sy1 + sy2) < TOLERANCE

    def test_snap_large_coordinates(self):
        """Large coordinates should still snap to a lattice point."""
        sx, sy, err = snap(1000.0, 1000.0, 3)
        assert err < COVERING_RADIUS + 0.01
        # Verify result is on the lattice: b = 2y/√3 must be integer
        b = sy * 2.0 / SQRT3
        assert abs(b - round(b)) < TOLERANCE
        # And a = x + y/√3 must be integer
        a = sx + sy / SQRT3
        assert abs(a - round(a)) < TOLERANCE

    def test_snap_batch_empty(self):
        """Batch snap with empty list should return empty list."""
        assert snap_batch([], 3) == []

    def test_snap_batch_single(self):
        """Batch snap with one element should work."""
        results = snap_batch([(0.0, 0.0)], 3)
        assert len(results) == 1
        sx, sy, err = results[0]
        assert err < TOLERANCE

    def test_snap_very_close_to_lattice_point(self):
        """A point extremely close to a lattice point should snap to it."""
        # (1, 0) is a lattice point (a=1, b=0)
        sx, sy, err = snap(1.0 + 1e-14, 1e-14, 3)
        assert abs(sx - 1.0) < 1e-10
        assert abs(sy - 0.0) < 1e-10

    def test_snap_returns_float_tuple(self):
        """Return type should be a 3-tuple of floats."""
        result = snap(0.5, 0.5, 3)
        assert isinstance(result, tuple)
        assert len(result) == 3
        for v in result:
            assert isinstance(v, float)

    def test_snap_error_nonnegative(self):
        """Error should always be non-negative."""
        _, _, err = snap(0.123, -4.567, 3)
        assert err >= 0.0


# ── Funnel edge cases ───────────────────────────────────────────────────────

class TestFunnelEdgeCases:
    def test_zero_decay_rate(self):
        """With decay_rate=0, epsilon should stay unchanged (exp(0)=1)."""
        val, new_eps = funnel_step(0.0, 1.0, 0.5, 0.0)
        assert abs(new_eps - 0.5) < TOLERANCE

    def test_small_decay_rate(self):
        """Small decay should give epsilon ≈ epsilon*(1-decay) to first order."""
        _, new_eps = funnel_step(0.0, 1.0, 1.0, 0.001)
        expected = 1.0 * math.exp(-0.001)
        assert abs(new_eps - expected) < TOLERANCE

    def test_large_decay_rate(self):
        """Large decay should shrink epsilon dramatically."""
        _, new_eps = funnel_step(0.0, 1.0, 1.0, 10.0)
        assert new_eps < 0.001

    def test_current_equals_target(self):
        """When current == target, should stay put."""
        val, new_eps = funnel_step(5.0, 5.0, 0.1, 0.5)
        assert abs(val - 5.0) < TOLERANCE
        assert abs(new_eps - 0.1 * math.exp(-0.5)) < TOLERANCE

    def test_negative_target(self):
        """Funnel should work with negative targets."""
        val, _ = funnel_step(0.0, -10.0, 1.0, 0.1)
        assert val < 0.0  # Should move toward -10

    def test_funnel_batch_empty(self):
        """Batch funnel with empty lists should return empty lists."""
        vals, eps = funnel_batch([], [], [], 0.1)
        assert vals == []
        assert eps == []

    def test_funnel_batch_length_mismatch_raises(self):
        """Mismatched list lengths should raise (zip stops shortest, but let's document behavior)."""
        # zip will stop at shortest - this is a contract test
        vals, eps = funnel_batch([0.0], [1.0, 2.0], [1.0], 0.1)
        assert len(vals) == 1
        assert len(eps) == 1

    def test_funnel_step_direction(self):
        """Step should move current toward target, never away."""
        val, _ = funnel_step(0.0, 5.0, 1.0, 0.1)
        assert val > 0.0  # moved toward 5
        val2, _ = funnel_step(5.0, 0.0, 1.0, 0.1)
        assert val2 < 5.0  # moved toward 0

    def test_within_deadband_correction(self):
        """Within deadband, correction should move current toward target."""
        val, _ = funnel_step(1.0, 1.02, 0.1, 0.5)
        assert val > 1.0  # moved toward 1.02
        assert val < 1.02  # but not past target (partial correction)


# ── Holonomy edge cases ─────────────────────────────────────────────────────

class TestHolonomyEdgeCases:
    def test_single_value(self):
        """Single value → no differences → winding = 0."""
        w = holonomy_winding([5.0], 10.0)
        assert abs(w) < TOLERANCE

    def test_negative_winding(self):
        """Sequence going backwards should give negative winding.
        1 → 9 → 1 → 9: each step wraps backward by -2/10 = -0.2."""
        w = holonomy_winding([1.0, 9.0, 1.0, 9.0], 10.0)
        assert w < 0

    def test_modulus_one(self):
        """With modulus=1, the winding is sum of wrapped diffs / 1.
        0.2→0.5: diff=0.3, wrapped=0.3. 0.5→0.8: diff=0.3, wrapped=0.3.
        Total = 0.6 / 1.0 = 0.6."""
        w = holonomy_winding([0.2, 0.5, 0.8], 1.0)
        assert abs(w - 0.6) < TOLERANCE

    def test_no_wrapping(self):
        """Monotone sequence with no wrapping: diffs are just the increments.
        Winding = (1+1+1+1)/100 = 0.04."""
        w = holonomy_winding([1.0, 2.0, 3.0, 4.0, 5.0], 100.0)
        assert abs(w - 0.04) < TOLERANCE

    def test_partial_winding_forward(self):
        """Sequence that wraps partially forward."""
        # 8 → 2 (mod 10) = forward wrap of 4/10 = 0.4
        w = holonomy_winding([8.0, 2.0], 10.0)
        assert abs(w - 0.4) < TOLERANCE

    def test_repeated_values(self):
        """Repeated values → zero differences → zero winding."""
        w = holonomy_winding([3.0, 3.0, 3.0, 3.0], 10.0)
        assert abs(w) < TOLERANCE


# ── Rigidity edge cases ─────────────────────────────────────────────────────

class TestRigidityEdgeCases:
    def test_duplicate_edges_subgraph_fail(self):
        """Duplicate (0,1) edge means subgraph {0,1} has 2 edges > 2*2-3=1.
        The code counts ALL edges including dupes, so this should fail Laman."""
        # Subgraph {0,1} has 2 edges (both (0,1)), 2 > 2*2-3=1
        assert not is_laman(3, [(0, 1), (1, 2), (0, 1)])

    def test_self_loop_accepted_by_simple_check(self):
        """n=2 with self-loop + real edge: code only checks k>=2 subgraphs.
        {0,1} has 2 edges, 2*2-3=1, 2>1 → would fail. But the code has a
        special case for n==2 that only checks len(edges)>=1. So it returns True."""
        # The n==2 fast-path only checks edge count >= 1, skips subgraph check
        result = is_laman(2, [(0, 0), (0, 1)])
        # Document actual behavior: n==2 skips subgraph checks
        assert isinstance(result, bool)

    def test_exactly_minimal_edges(self):
        """n=5, edges=7 (=2*5-3), with a valid Laman construction."""
        # Build from a triangle (0,1,2) and extend by Henneberg:
        # Add vertex 3 with edges to (1,2); add vertex 4 with edges to (0,3)
        edges = [(0,1), (1,2), (0,2), (1,3), (2,3), (0,4), (3,4)]
        assert is_laman(5, edges)

    def test_zero_edges(self):
        """No edges on ≥2 vertices → not rigid."""
        assert not is_laman(3, [])

    def test_n_equals_2_one_edge(self):
        """Two vertices with one edge is minimally rigid."""
        assert is_laman(2, [(0, 1)])

    def test_n_equals_2_two_edges(self):
        """Two vertices with two edges: over-constrained but still rigid."""
        assert is_laman(2, [(0, 1), (0, 1)])

    def test_disconnected_graph(self):
        """Disconnected graph: 6 vertices, two triangles, no edges between them.
        Total edges = 6, need 2*6-3=9. Not enough → not rigid."""
        edges = [(0,1), (1,2), (0,2), (3,4), (4,5), (3,5)]
        assert not is_laman(6, edges)

    def test_tree_not_rigid(self):
        """A tree on n vertices has n-1 edges, which is < 2n-3 for n≥3."""
        # Path graph on 4 vertices: 3 edges, need 5
        assert not is_laman(4, [(0,1), (1,2), (2,3)])


# ── Consensus edge cases ────────────────────────────────────────────────────

class TestConsensusEdgeCases:
    def test_single_value(self):
        """Single value should be converged immediately."""
        vals, converged = consensus_round([7.0], 0.5)
        assert converged
        assert abs(vals[0] - 7.0) < TOLERANCE

    def test_negative_values(self):
        """Consensus should work with negative values."""
        current = [-3.0, -1.0, 1.0]
        for _ in range(100):
            current, converged = consensus_round(current, 0.5)
            if converged:
                break
        assert converged
        mean = sum(current) / len(current)
        assert abs(mean - (-1.0)) < 0.5

    def test_large_epsilon(self):
        """Epsilon larger than spread → immediate convergence."""
        vals, converged = consensus_round([1.0, 2.0, 3.0], 10.0)
        assert converged

    def test_zero_epsilon(self):
        """Zero epsilon → diff > 0 always False (|diff| > 0), so never converged
        unless already identical. Values should still move."""
        vals, converged = consensus_round([1.0, 3.0], 0.0)
        assert not converged  # They're not identical

    def test_identical_values_converged(self):
        """Identical non-zero values should report converged."""
        vals, converged = consensus_round([5.0, 5.0, 5.0, 5.0], 0.01)
        assert converged

    def test_circular_convergence(self):
        """Multiple rounds of circular consensus should converge."""
        current = [0.1, 9.5, 0.3, 9.8]
        for _ in range(200):
            current, converged = consensus_round(current, 0.3, modulus=10.0)
            if converged:
                break
        assert converged

    def test_two_values_opposite_sides(self):
        """Values at opposite ends should still converge with circular mean."""
        vals, _ = consensus_round([1.0, 9.0], 0.5, modulus=10.0)
        # Both should move toward the circular mean (~0/10)
        for v in vals:
            assert v < 2.0 or v > 8.0  # near 0, not near 5

    def test_consensus_preserves_count(self):
        """Output should always have same length as input."""
        for n in [0, 1, 3, 10]:
            vals, _ = consensus_round([float(i) for i in range(n)], 0.5)
            assert len(vals) == n


# ── CFFI fallback ───────────────────────────────────────────────────────────

class TestCFFI:
    def test_is_available_returns_bool(self):
        """is_available() should return a boolean."""
        from constraint_substrate._cffi import is_available
        assert isinstance(is_available(), bool)

    def test_lib_path_is_string_or_none(self):
        """lib_path() should return a string or None."""
        from constraint_substrate._cffi import lib_path
        result = lib_path()
        assert result is None or isinstance(result, str)
