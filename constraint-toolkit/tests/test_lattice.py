"""Tests for the lattice module."""

import pytest
from constraint_toolkit.lattice import ConstraintLattice, LatticeNode


class TestLatticeNode:
    def test_creation(self):
        node = LatticeNode(name="a", level=0)
        assert node.name == "a"
        assert node.level == 0
        assert node.coordinates == ()
        assert node.metadata == {}

    def test_equality(self):
        a = LatticeNode(name="x", level=1)
        b = LatticeNode(name="x", level=1)
        assert a == b

    def test_inequality(self):
        a = LatticeNode(name="x", level=1)
        b = LatticeNode(name="y", level=1)
        assert a != b

    def test_hash(self):
        a = LatticeNode(name="x", level=1)
        b = LatticeNode(name="x", level=1)
        assert hash(a) == hash(b)
        assert {a, b} == {a}

    def test_coordinates_and_metadata(self):
        node = LatticeNode(name="n", level=2, coordinates=(1.0, 2.0), metadata={"key": "val"})
        assert node.coordinates == (1.0, 2.0)
        assert node.metadata["key"] == "val"


class TestConstraintLattice:
    def _make_simple_lattice(self):
        lat = ConstraintLattice()
        lat.add_node(LatticeNode("top", 2))
        lat.add_node(LatticeNode("mid", 1))
        lat.add_node(LatticeNode("bot", 0))
        lat.add_edge("top", "mid")
        lat.add_edge("mid", "bot")
        return lat

    def test_add_nodes(self):
        lat = self._make_simple_lattice()
        assert len(lat.nodes) == 3
        assert len(lat.edges) == 2

    def test_add_edge_missing_node(self):
        lat = ConstraintLattice()
        lat.add_node(LatticeNode("a", 0))
        with pytest.raises(ValueError):
            lat.add_edge("a", "missing")

    def test_leq(self):
        lat = self._make_simple_lattice()
        assert lat.leq("bot", "bot")
        assert lat.leq("bot", "mid")
        assert lat.leq("bot", "top")
        assert not lat.leq("top", "bot")

    def test_join(self):
        lat = self._make_simple_lattice()
        result = lat.join("bot", "mid")
        assert result == "mid"

    def test_join_no_common(self):
        lat = ConstraintLattice()
        lat.add_node(LatticeNode("a", 0))
        lat.add_node(LatticeNode("b", 0))
        assert lat.join("a", "b") is None

    def test_meet(self):
        lat = self._make_simple_lattice()
        result = lat.meet("top", "mid")
        assert result == "mid"

    def test_ancestors(self):
        lat = self._make_simple_lattice()
        assert lat.ancestors("bot") == {"mid", "top"}

    def test_descendants(self):
        lat = self._make_simple_lattice()
        assert lat.descendants("top") == {"mid", "bot"}

    def test_empty_lattice(self):
        lat = ConstraintLattice()
        assert lat.nodes == []
        assert lat.edges == []

    def test_diamond_lattice(self):
        """Test a diamond-shaped lattice (common in constraint theory)."""
        lat = ConstraintLattice()
        lat.add_node(LatticeNode("top", 2))
        lat.add_node(LatticeNode("left", 1))
        lat.add_node(LatticeNode("right", 1))
        lat.add_node(LatticeNode("bottom", 0))
        lat.add_edge("top", "left")
        lat.add_edge("top", "right")
        lat.add_edge("left", "bottom")
        lat.add_edge("right", "bottom")

        assert lat.leq("bottom", "top")
        assert lat.leq("left", "top")
        assert lat.leq("right", "top")
        assert lat.join("left", "right") == "top"
        assert lat.meet("left", "right") == "bottom"
