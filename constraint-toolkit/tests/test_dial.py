"""Tests for the dial module."""

import math
import pytest
from constraint_toolkit.dial import DialPosition, DialSpace


class TestDialPosition:
    def test_creation(self):
        pos = DialPosition(name="a", angle=math.pi / 2)
        assert pos.name == "a"
        assert abs(pos.angle - math.pi / 2) < 1e-9

    def test_angle_normalization(self):
        pos = DialPosition(name="a", angle=3 * math.pi)
        assert abs(pos.angle - math.pi) < 1e-9

    def test_distance_same(self):
        pos = DialPosition(name="a", angle=0)
        assert pos.distance_to(pos) == 0.0

    def test_distance_opposite(self):
        a = DialPosition(name="a", angle=0)
        b = DialPosition(name="b", angle=math.pi)
        assert abs(a.distance_to(b) - math.pi) < 1e-9

    def test_distance_shortest_arc(self):
        a = DialPosition(name="a", angle=0.1)
        b = DialPosition(name="b", angle=2 * math.pi - 0.1)
        assert abs(a.distance_to(b) - 0.2) < 1e-6

    def test_cartesian(self):
        pos = DialPosition(name="a", angle=0, radius=2.0)
        x, y = pos.cartesian()
        assert abs(x - 2.0) < 1e-9
        assert abs(y) < 1e-9

    def test_cartesian_quarter(self):
        pos = DialPosition(name="a", angle=math.pi / 2, radius=1.0)
        x, y = pos.cartesian()
        assert abs(x) < 1e-9
        assert abs(y - 1.0) < 1e-9


class TestDialSpace:
    def _make_space(self):
        return DialSpace([
            DialPosition("a", 0),
            DialPosition("b", math.pi / 2),
            DialPosition("c", math.pi),
            DialPosition("d", 3 * math.pi / 2),
        ])

    def test_empty(self):
        ds = DialSpace()
        assert ds.positions == []
        assert ds.nearest(DialPosition("x", 0)) is None
        assert ds.diameter() == 0.0
        assert ds.mean_angle() is None
        assert ds.cluster() == []

    def test_positions(self):
        ds = self._make_space()
        assert len(ds.positions) == 4

    def test_add(self):
        ds = DialSpace()
        ds.add(DialPosition("a", 0))
        assert len(ds.positions) == 1

    def test_nearest(self):
        ds = self._make_space()
        target = DialPosition("x", math.pi / 2 + 0.1)
        nearest = ds.nearest(target)
        assert nearest is not None
        assert nearest.name == "b"

    def test_within(self):
        ds = self._make_space()
        target = DialPosition("x", 0)
        result = ds.within(target, math.pi / 4)
        names = {p.name for p in result}
        assert "a" in names
        assert "b" not in names

    def test_diameter(self):
        ds = self._make_space()
        assert abs(ds.diameter() - math.pi) < 1e-9

    def test_mean_angle(self):
        ds = DialSpace([DialPosition("a", 0), DialPosition("b", 0)])
        mean = ds.mean_angle()
        assert mean is not None
        assert abs(mean) < 1e-9

    def test_cluster(self):
        ds = DialSpace([
            DialPosition("a", 0),
            DialPosition("b", 0.1),
            DialPosition("c", 0.2),
            DialPosition("d", math.pi),
        ])
        clusters = ds.cluster(threshold=0.5)
        assert len(clusters) == 2
        assert len(clusters[0]) == 3  # a, b, c
        assert len(clusters[1]) == 1  # d
