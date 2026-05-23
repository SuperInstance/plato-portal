"""
Miles Mode — Frontier Explorer.

Miles Davis always found something new. This mode shows you where
the unexplored territory IS in your constraint space.

Key concepts:
- Frontier: the boundary between explored and unexplored constraint space
- Exploration map: tracking what combinations have been used
- Originality score: am I repeating myself?
"""

import random
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from .terrain import Terrain, TERRAINS


@dataclass
class FrontierRegion:
    """An unexplored or under-explored region of constraint space."""
    coordinates: Tuple[int, ...]  # (scale_region, rhythm_region, register_region)
    distance: float               # how far from explored territory
    features: List[str]           # what's interesting about it
    visits: int = 0


@dataclass
class ExplorationState:
    """Tracks what regions of constraint space have been explored."""
    visited_regions: Set[Tuple[int, ...]] = field(default_factory=set)
    visit_counts: Dict[Tuple[int, ...], int] = field(default_factory=dict)
    melodic_contours: List[Tuple[int, ...]] = field(default_factory=list)
    scale_combos: Set[Tuple[int, ...]] = field(default_factory=set)
    rhythm_combos: Set[Tuple[int, ...]] = field(default_factory=set)


class MilesEngine:
    """The frontier explorer: always find something new."""

    def __init__(self, terrain: Terrain, key: int = 60):
        self.terrain = terrain
        self.key = key
        self.state = ExplorationState()
        self._performances: List[dict] = []

    def frontier(self, n: int = 5) -> List[FrontierRegion]:
        """
        Find the nearest unexplored regions of constraint space.
        Returns the n closest frontier regions.
        """
        regions = []

        # Generate candidate regions (scale, rhythm, register combinations)
        scale_degrees = [d.degree for d in self.terrain.scale_degrees]
        rhythms = list(range(len(self.terrain.rhythmic_skeletons)))
        registers = [(r // 12) for r in range(self.terrain.register_tendency[0],
                                                self.terrain.register_tendency[1], 12)]

        for _ in range(50):  # sample candidates
            s = random.choice(scale_degrees)
            r = random.choice(rhythms) if rhythms else 0
            reg = random.choice(registers) if registers else 5
            coords = (s, r, reg)

            if coords not in self.state.visited_regions:
                # Calculate distance from nearest explored region
                min_dist = float('inf')
                for visited in self.state.visited_regions:
                    dist = sum(abs(a - b) for a, b in zip(coords, visited))
                    min_dist = min(min_dist, dist)

                if min_dist == float('inf'):
                    min_dist = 1.0

                features = []
                if s not in [d.degree for d in self.terrain.scale_degrees[:3]]:
                    features.append("unusual scale degree")
                if r not in [0]:
                    features.append("alternative rhythm")
                if reg > 6:
                    features.append("high register")
                elif reg < 4:
                    features.append("low register")
                if not features:
                    features.append("untried combination")

                regions.append(FrontierRegion(
                    coordinates=coords,
                    distance=min_dist,
                    features=features,
                ))

        # Sort by distance (closest frontiers first)
        regions.sort(key=lambda r: r.distance)
        return regions[:n]

    def perform(self, explore: bool = True, anchor: Optional[str] = None,
                risk: float = 0.5, minutes: float = 2.0) -> dict:
        """
        Perform at the edge of explored territory.
        
        Args:
            explore: push toward unexplored territory
            anchor: keep one foot in known ground (e.g., "so_what", "kind_of_blue")
            risk: how far from safety (0=safe, 1=free fall)
            minutes: duration
        """
        frontiers = self.frontier() if explore else []

        bpm = random.randint(*self.terrain.typical_tempo)
        beat_dur = 60.0 / bpm
        notes = []
        t = 0.0
        duration = minutes * 60.0

        degree_weights = {d.degree: d.weight for d in self.terrain.scale_degrees}
        all_degrees = list(degree_weights.keys())

        # Anchor: known ground to return to
        anchor_degrees = {
            "so_what": [0, 2, 4, 5, 7, 9],
            "kind_of_blue": [0, 3, 5, 7, 10],
            "all_blues": [0, 3, 5, 6, 7, 10],
            "fluorescence": [0, 2, 4, 6, 8, 10],
        }
        safe_degrees = anchor_degrees.get(anchor, [0, 4, 7]) if anchor else [0, 4, 7]

        while t < duration:
            if explore and frontiers and random.random() < risk:
                # Push toward frontier
                target = random.choice(frontiers)
                frontier_degree = target.coordinates[0]
                pitch = self.key + frontier_degree + (target.coordinates[2] - 5) * 12
                target.visits += 1
            elif random.random() < 0.3:
                # Return to anchor
                degree = random.choice(safe_degrees)
                pitch = self.key + degree
            else:
                # Normal exploration within terrain
                degree = random.choices(all_degrees,
                                        weights=[degree_weights.get(d, 0.5) for d in all_degrees])[0]
                pitch = self.key + degree

            velocity = random.randint(50, 100)
            note_len = beat_dur * random.choice([0.5, 1.0, 1.5, 2.0, 4.0])
            notes.append({
                "pitch": max(21, min(108, pitch)),
                "velocity": velocity,
                "start": round(t, 3),
                "duration": round(note_len, 3),
            })

            # Record contour
            if len(notes) >= 2:
                contour_step = notes[-1]["pitch"] - notes[-2]["pitch"]
                # (simplified contour tracking)

            t += note_len

        # Record this performance's exploration
        explored = set()
        for n in notes:
            degree = (n["pitch"] - self.key) % 12
            explored.add((degree, 0, n["pitch"] // 12))
        self.state.visited_regions.update(explored)

        performance = {
            "notes": notes,
            "tempo": bpm,
            "terrain": self.terrain.name,
            "key": self.key,
            "risk": risk,
            "anchor": anchor,
            "frontiers_explored": len([f for f in frontiers if f.visits > 0]),
        }
        self._performances.append(performance)
        return performance

    def originality(self, last_n: int = 10) -> dict:
        """
        Diagnose repetition: am I playing the same things?
        Returns an originality analysis.
        """
        recent = self._performances[-last_n:] if self._performances else []

        if not recent:
            return {"score": 1.0, "message": "No performances yet. Go explore!",
                    "contours_used": [], "unique_ratio": 1.0}

        # Extract melodic contours (direction changes)
        all_contours = []
        for perf in recent:
            notes = perf["notes"]
            contour = tuple(
                1 if notes[i+1]["pitch"] > notes[i]["pitch"]
                else (-1 if notes[i+1]["pitch"] < notes[i]["pitch"] else 0)
                for i in range(min(len(notes)-1, 16))
            )
            if contour:
                all_contours.append(contour)

        # Count unique vs repeated contours
        unique_contours = set(all_contours)
        unique_ratio = len(unique_contours) / max(1, len(all_contours))

        # Find most repeated contour
        from collections import Counter
        contour_counts = Counter(all_contours)
        most_common = contour_counts.most_common(3)

        score = unique_ratio
        if score > 0.8:
            message = "Highly original — you're covering new ground."
        elif score > 0.5:
            message = "Decent variety, but some patterns recurring."
            if most_common:
                message += f" Your most common contour appeared {most_common[0][1]} times."
                message += " Try inverting it."
        else:
            message = "Repetition detected! You're looping. Try a different risk level or anchor."

        return {
            "score": round(score, 3),
            "message": message,
            "contours_analyzed": len(all_contours),
            "unique_contours": len(unique_contours),
            "unique_ratio": round(unique_ratio, 3),
            "most_common": [(c, count) for c, count in most_common],
        }
