"""Tradition clusters — grouping traditions by constraint similarity."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Sequence


@dataclass(frozen=True)
class Tradition:
    """A tradition with named constraint scores."""

    name: str
    scores: dict[str, float] = field(default_factory=dict)
    category: str = ""

    def distance_to(self, other: Tradition) -> float:
        """Euclidean distance between score vectors (shared keys only)."""
        shared = set(self.scores) & set(other.scores)
        if not shared:
            return float("inf")
        return math.sqrt(sum((self.scores[k] - other.scores[k]) ** 2 for k in shared))

    def score_vector(self, keys: Sequence[str] | None = None) -> list[float]:
        """Return scores as an ordered vector."""
        k = keys or sorted(self.scores)
        return [self.scores.get(key, 0.0) for key in k]


class TraditionCluster:
    """Cluster traditions by their constraint score similarity."""

    def __init__(self, traditions: Sequence[Tradition] | None = None) -> None:
        self._traditions: list[Tradition] = list(traditions or [])

    def add(self, t: Tradition) -> None:
        self._traditions.append(t)

    @property
    def traditions(self) -> list[Tradition]:
        return list(self._traditions)

    def cluster_by_distance(self, threshold: float = 1.0) -> list[list[Tradition]]:
        """Simple greedy clustering by Euclidean distance."""
        if not self._traditions:
            return []
        unassigned = list(self._traditions)
        clusters: list[list[Tradition]] = []
        while unassigned:
            seed = unassigned.pop(0)
            group = [seed]
            remaining: list[Tradition] = []
            for t in unassigned:
                if any(t.distance_to(m) <= threshold for m in group):
                    group.append(t)
                else:
                    remaining.append(t)
            clusters.append(group)
            unassigned = remaining
        return clusters

    def nearest_neighbors(self, tradition: Tradition, k: int = 3) -> list[Tradition]:
        """Find k nearest traditions by score distance."""
        dists = [(t, tradition.distance_to(t)) for t in self._traditions if t != tradition]
        dists.sort(key=lambda x: x[1])
        return [t for t, _ in dists[:k]]

    def category_summary(self) -> dict[str, list[Tradition]]:
        """Group traditions by category."""
        result: dict[str, list[Tradition]] = {}
        for t in self._traditions:
            result.setdefault(t.category, []).append(t)
        return result

    def centroid_scores(self, traditions: Sequence[Tradition] | None = None) -> dict[str, float]:
        """Compute mean score vector for a group of traditions."""
        group = list(traditions or self._traditions)
        if not group:
            return {}
        all_keys = sorted({k for t in group for k in t.scores})
        return {
            key: sum(t.scores.get(key, 0.0) for t in group) / len(group)
            for key in all_keys
        }
