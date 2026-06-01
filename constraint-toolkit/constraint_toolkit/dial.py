"""Dial positions — representing constraint values on circular/rotary dials."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class DialPosition:
    """A position on a circular dial (angle in radians, 0 to 2π)."""

    name: str
    angle: float
    radius: float = 1.0

    def __post_init__(self) -> None:
        # Normalize angle to [0, 2π)
        object.__setattr__(self, "angle", self.angle % (2 * math.pi))

    def distance_to(self, other: DialPosition) -> float:
        """Angular distance (shortest arc) between two dial positions."""
        diff = abs(self.angle - other.angle)
        return min(diff, 2 * math.pi - diff)

    def cartesian(self) -> tuple[float, float]:
        """Convert to (x, y) cartesian coordinates."""
        return (self.radius * math.cos(self.angle), self.radius * math.sin(self.angle))


class DialSpace:
    """A collection of dial positions with proximity and clustering operations."""

    def __init__(self, positions: Sequence[DialPosition] | None = None) -> None:
        self._positions: list[DialPosition] = list(positions or [])

    def add(self, pos: DialPosition) -> None:
        self._positions.append(pos)

    @property
    def positions(self) -> list[DialPosition]:
        return list(self._positions)

    def nearest(self, pos: DialPosition) -> DialPosition | None:
        """Find the nearest position in the space to the given position."""
        if not self._positions:
            return None
        return min(self._positions, key=lambda p: pos.distance_to(p))

    def within(self, pos: DialPosition, max_angle: float) -> list[DialPosition]:
        """Return all positions within max_angle radians of pos."""
        return [p for p in self._positions if pos.distance_to(p) <= max_angle]

    def diameter(self) -> float:
        """Maximum angular distance between any two positions."""
        if len(self._positions) < 2:
            return 0.0
        return max(a.distance_to(b) for a in self._positions for b in self._positions)

    def mean_angle(self) -> float | None:
        """Compute the circular mean angle."""
        if not self._positions:
            return None
        sin_sum = sum(math.sin(p.angle) for p in self._positions)
        cos_sum = sum(math.cos(p.angle) for p in self._positions)
        return math.atan2(sin_sum, cos_sum) % (2 * math.pi)

    def cluster(self, threshold: float = math.pi / 4) -> list[list[DialPosition]]:
        """Group positions by angular proximity using simple threshold clustering."""
        if not self._positions:
            return []
        unassigned = list(self._positions)
        clusters: list[list[DialPosition]] = []
        while unassigned:
            seed = unassigned.pop(0)
            cluster = [seed]
            remaining: list[DialPosition] = []
            for p in unassigned:
                if seed.distance_to(p) <= threshold:
                    cluster.append(p)
                else:
                    remaining.append(p)
            clusters.append(cluster)
            unassigned = remaining
        return clusters
