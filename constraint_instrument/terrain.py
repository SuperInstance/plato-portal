"""
Bathymetric maps — the terrain of constraint space.

Each terrain defines the topology of a musical landscape:
- scale degrees and their weights
- characteristic intervals and gestures
- rhythmic skeletons
- register tendencies
- chromatic fields and their density
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class ScaleDegree:
    degree: int       # 0=root, 1=flat2, 2=2, etc. (semitones from root)
    weight: float     # 0.0-1.0 how "at home" this note is
    name: str         # human-readable
    blues_note: bool = False  # blue notes bend toward/away


@dataclass
class RhythmicSkeleton:
    """Characteristic rhythmic patterns for this terrain."""
    name: str
    subdivisions: List[float]  # relative durations (sum = 1.0 for one bar)
    accents: List[int]         # indices of accented beats
    swing: float = 0.0         # 0=straight, 1=full swing


@dataclass
class Terrain:
    """A bathymetric map of musical constraint space."""
    name: str
    description: str
    scale_degrees: List[ScaleDegree]
    characteristic_intervals: List[int]  # semitone intervals that define the sound
    rhythmic_skeletons: List[RhythmicSkeleton]
    register_tendency: Tuple[int, int]  # (low, high) MIDI range preference
    chromatic_density: float = 0.0  # 0=diatonic, 1=fully chromatic
    typical_tempo: Tuple[int, int] = (100, 180)  # (low, high) BPM


# ── Terrain Definitions ──────────────────────────────────────────────

BLUES = Terrain(
    name="blues",
    description="The deep water. 12-bar form, blue notes, call-and-response.",
    scale_degrees=[
        ScaleDegree(0, 1.0, "root"),
        ScaleDegree(3, 0.9, "minor 3rd", blues_note=True),
        ScaleDegree(4, 0.7, "major 3rd"),
        ScaleDegree(5, 0.95, "perfect 4th"),
        ScaleDegree(6, 0.85, "tritone", blues_note=True),
        ScaleDegree(7, 0.9, "perfect 5th"),
        ScaleDegree(10, 0.9, "minor 7th", blues_note=True),
    ],
    characteristic_intervals=[3, 4, 5, 7],
    rhythmic_skeletons=[
        RhythmicSkeleton("shuffle", [0.67, 0.33] * 4, [0, 2], swing=0.7),
        RhythmicSkeleton("slow_12_8", [1.0/3] * 12, [0, 3, 4, 6, 9, 10], swing=0.5),
        RhythmicSkeleton("walking", [1.0] * 4, [0, 2], swing=0.3),
    ],
    register_tendency=(48, 79),  # C3 to G4
    chromatic_density=0.3,
    typical_tempo=(60, 160),
)

BEBOP = Terrain(
    name="bebop",
    description="Fast, dense, chromatic. The lattice at speed.",
    scale_degrees=[
        ScaleDegree(0, 1.0, "root"),
        ScaleDegree(2, 0.9, "major 2nd"),
        ScaleDegree(3, 0.7, "minor 3rd"),
        ScaleDegree(4, 0.9, "major 3rd"),
        ScaleDegree(5, 0.85, "perfect 4th"),
        ScaleDegree(6, 0.6, "tritone"),
        ScaleDegree(7, 0.9, "perfect 5th"),
        ScaleDegree(9, 0.8, "major 6th"),
        ScaleDegree(10, 0.85, "minor 7th"),
        ScaleDegree(11, 0.6, "major 7th"),
    ],
    characteristic_intervals=[2, 3, 4, 5, 6],
    rhythmic_skeletons=[
        RhythmicSkeleton("eighth_note_stream", [0.5] * 8, [0, 2, 4, 6], swing=0.6),
        RhythmicSkeleton("triplet_run", [1.0/3] * 12, [0, 3, 6, 9], swing=0.4),
    ],
    register_tendency=(55, 86),  # G3 to D5
    chromatic_density=0.6,
    typical_tempo=(180, 320),
)

MODAL = Terrain(
    name="modal",
    description="Sparse constraints, wide open spaces. Miles's territory.",
    scale_degrees=[
        ScaleDegree(0, 1.0, "root"),
        ScaleDegree(2, 0.9, "major 2nd"),
        ScaleDegree(4, 0.85, "major 3rd"),
        ScaleDegree(5, 0.8, "perfect 4th"),
        ScaleDegree(7, 0.9, "perfect 5th"),
        ScaleDegree(9, 0.75, "major 6th"),
    ],
    characteristic_intervals=[2, 4, 5, 7],
    rhythmic_skeletons=[
        RhythmicSkeleton("long_phrases", [2.0, 1.0, 1.0], [0], swing=0.2),
        RhythmicSkeleton("rubato", [1.5, 0.5, 2.0], [0], swing=0.0),
    ],
    register_tendency=(48, 84),  # wide range
    chromatic_density=0.1,
    typical_tempo=(60, 140),
)

CLASSICAL = Terrain(
    name="classical",
    description="Tonal architecture. Voice-leading as constraint.",
    scale_degrees=[
        ScaleDegree(0, 1.0, "root"),
        ScaleDegree(2, 0.9, "major 2nd"),
        ScaleDegree(4, 0.95, "major 3rd"),
        ScaleDegree(5, 0.9, "perfect 4th"),
        ScaleDegree(7, 0.95, "perfect 5th"),
        ScaleDegree(9, 0.8, "major 6th"),
        ScaleDegree(11, 0.7, "major 7th"),
    ],
    characteristic_intervals=[2, 3, 4, 5, 7, 8],
    rhythmic_skeletons=[
        RhythmicSkeleton("common_time", [1.0] * 4, [0, 2], swing=0.0),
        RhythmicSkeleton("three_four", [1.0] * 3, [0], swing=0.0),
    ],
    register_tendency=(48, 84),
    chromatic_density=0.15,
    typical_tempo=(60, 200),
)

FREE_JAZZ = Terrain(
    name="free_jazz",
    description="Minimal constraints. Maximum freedom. Ornette's world.",
    scale_degrees=[
        ScaleDegree(i, 0.5, f"degree_{i}") for i in range(12)
    ],
    characteristic_intervals=list(range(1, 13)),
    rhythmic_skeletons=[
        RhythmicSkeleton("free_pulse", [1.0], [0], swing=0.0),
    ],
    register_tendency=(36, 96),  # very wide
    chromatic_density=1.0,
    typical_tempo=(40, 300),
)

TERRAINS: Dict[str, Terrain] = {
    "blues": BLUES,
    "bebop": BEBOP,
    "modal": MODAL,
    "classical": CLASSICAL,
    "free_jazz": FREE_JAZZ,
}
