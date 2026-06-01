"""Tests for the tradition module."""

import math
import pytest
from constraint_toolkit.tradition import Tradition, TraditionCluster


class TestTradition:
    def test_creation(self):
        t = Tradition(name="jazz", scores={"harmony": 8.5, "rhythm": 9.0}, category="music")
        assert t.name == "jazz"
        assert t.scores["harmony"] == 8.5
        assert t.category == "music"

    def test_distance_same(self):
        t = Tradition(name="a", scores={"x": 1.0})
        assert t.distance_to(t) == 0.0

    def test_distance_different(self):
        a = Tradition(name="a", scores={"x": 0.0, "y": 0.0})
        b = Tradition(name="b", scores={"x": 3.0, "y": 4.0})
        assert abs(a.distance_to(b) - 5.0) < 1e-9

    def test_distance_no_shared_keys(self):
        a = Tradition(name="a", scores={"x": 1.0})
        b = Tradition(name="b", scores={"y": 1.0})
        assert a.distance_to(b) == float("inf")

    def test_score_vector(self):
        t = Tradition(name="a", scores={"b": 2.0, "a": 1.0})
        assert t.score_vector() == [1.0, 2.0]  # sorted keys
        assert t.score_vector(keys=["b", "a"]) == [2.0, 1.0]


class TestTraditionCluster:
    def _make_cluster(self):
        return TraditionCluster([
            Tradition("jazz", {"harmony": 8.0, "rhythm": 9.0}, "music"),
            Tradition("blues", {"harmony": 7.0, "rhythm": 7.0}, "music"),
            Tradition("classical", {"harmony": 9.0, "rhythm": 3.0}, "music"),
            Tradition("cooking", {"flavor": 8.0, "technique": 7.0}, "culinary"),
        ])

    def test_empty(self):
        tc = TraditionCluster()
        assert tc.traditions == []
        assert tc.cluster_by_distance() == []
        assert tc.nearest_neighbors(Tradition("x", {"a": 1})) == []
        assert tc.category_summary() == {}
        assert tc.centroid_scores() == {}

    def test_traditions(self):
        tc = self._make_cluster()
        assert len(tc.traditions) == 4

    def test_add(self):
        tc = TraditionCluster()
        tc.add(Tradition("x", {"a": 1}))
        assert len(tc.traditions) == 1

    def test_cluster_by_distance(self):
        tc = TraditionCluster([
            Tradition("a", {"x": 1.0}),
            Tradition("b", {"x": 1.1}),
            Tradition("c", {"x": 5.0}),
        ])
        clusters = tc.cluster_by_distance(threshold=1.0)
        assert len(clusters) == 2
        names = [{t.name for t in c} for c in clusters]
        assert {"a", "b"} in names

    def test_nearest_neighbors(self):
        tc = self._make_cluster()
        target = Tradition("test", {"harmony": 7.5, "rhythm": 8.5})
        neighbors = tc.nearest_neighbors(target, k=2)
        assert len(neighbors) == 2
        assert neighbors[0].name == "jazz"

    def test_category_summary(self):
        tc = self._make_cluster()
        summary = tc.category_summary()
        assert "music" in summary
        assert "culinary" in summary
        assert len(summary["music"]) == 3
        assert len(summary["culinary"]) == 1

    def test_centroid_scores(self):
        tc = TraditionCluster([
            Tradition("a", {"x": 2.0, "y": 4.0}),
            Tradition("b", {"x": 4.0, "y": 6.0}),
        ])
        centroid = tc.centroid_scores()
        assert abs(centroid["x"] - 3.0) < 1e-9
        assert abs(centroid["y"] - 5.0) < 1e-9
