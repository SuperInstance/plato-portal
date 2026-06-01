"""Tests for the visualization module."""

import math
import pytest
from constraint_toolkit.lattice import ConstraintLattice, LatticeNode
from constraint_toolkit.dial import DialPosition, DialSpace
from constraint_toolkit.tradition import Tradition, TraditionCluster
from constraint_toolkit.visualization import (
    render_lattice,
    render_dial,
    render_dial_histogram,
    render_tradition_heatmap,
    render_cluster_summary,
)


class TestRenderLattice:
    def test_empty(self):
        lat = ConstraintLattice()
        assert "empty" in render_lattice(lat).lower()

    def test_single_node(self):
        lat = ConstraintLattice()
        lat.add_node(LatticeNode("root", 0))
        result = render_lattice(lat)
        assert "root" in result

    def test_multi_level(self):
        lat = ConstraintLattice()
        lat.add_node(LatticeNode("top", 2))
        lat.add_node(LatticeNode("mid", 1))
        lat.add_node(LatticeNode("bot", 0))
        lat.add_edge("top", "mid")
        lat.add_edge("mid", "bot")
        result = render_lattice(lat)
        assert "top" in result
        assert "mid" in result
        assert "bot" in result

    def test_diamond_lattice(self):
        lat = ConstraintLattice()
        lat.add_node(LatticeNode("top", 2))
        lat.add_node(LatticeNode("L", 1))
        lat.add_node(LatticeNode("R", 1))
        lat.add_node(LatticeNode("bot", 0))
        lat.add_edge("top", "L")
        lat.add_edge("top", "R")
        lat.add_edge("L", "bot")
        lat.add_edge("R", "bot")
        result = render_lattice(lat)
        assert all(name in result for name in ["top", "L", "R", "bot"])


class TestRenderDial:
    def test_empty(self):
        ds = DialSpace()
        assert "empty" in render_dial(ds).lower()

    def test_single_position(self):
        ds = DialSpace([DialPosition("x", 0)])
        result = render_dial(ds, radius=6)
        assert "x" in result
        assert "0.0°" in result

    def test_multiple_positions(self):
        ds = DialSpace([
            DialPosition("a", 0),
            DialPosition("b", math.pi / 2),
            DialPosition("c", math.pi),
        ])
        result = render_dial(ds, radius=6)
        assert "a" in result
        assert "b" in result
        assert "c" in result
        assert "+" in result  # center marker

    def test_has_circle_markers(self):
        ds = DialSpace([DialPosition("x", 0)])
        result = render_dial(ds, radius=6)
        assert "·" in result  # circle outline


class TestRenderDialHistogram:
    def test_empty(self):
        assert "empty" in render_dial_histogram(DialSpace()).lower()

    def test_basic_histogram(self):
        ds = DialSpace([
            DialPosition("a", 0),
            DialPosition("b", 0.1),
            DialPosition("c", math.pi),
        ])
        result = render_dial_histogram(ds, bins=4)
        assert "█" in result or "(" in result  # has bars or counts
        assert "0.0°" in result


class TestRenderTraditionHeatmap:
    def test_empty(self):
        tc = TraditionCluster()
        assert "empty" in render_tradition_heatmap(tc).lower()

    def test_with_data(self):
        tc = TraditionCluster([
            Tradition("jazz", {"harmony": 8.0, "rhythm": 9.0}),
            Tradition("classical", {"harmony": 9.0, "rhythm": 3.0}),
        ])
        result = render_tradition_heatmap(tc)
        assert "jazz" in result
        assert "classical" in result
        assert "harmony" in result
        assert "rhythm" in result
        # Should contain heat chars
        assert any(c in result for c in "░▒▓█")

    def test_custom_keys(self):
        tc = TraditionCluster([
            Tradition("a", {"x": 5.0, "y": 3.0}),
        ])
        result = render_tradition_heatmap(tc, keys=["y"])
        assert "y" in result
        assert "x" not in result.split("\n")[0]  # x not in header


class TestRenderClusterSummary:
    def test_empty(self):
        tc = TraditionCluster()
        assert "no traditions" in render_cluster_summary(tc).lower()

    def test_with_clusters(self):
        tc = TraditionCluster([
            Tradition("a", {"x": 1.0}, "group1"),
            Tradition("b", {"x": 1.1}, "group1"),
            Tradition("c", {"x": 5.0}, "group2"),
        ])
        result = render_cluster_summary(tc, threshold=1.0)
        assert "Cluster" in result
        assert "centroid" in result
        assert "a" in result
