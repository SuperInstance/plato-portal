"""
Parker Mode — The Practice Engine.

Charlie Parker internalized the lattice through relentless practice.
This mode helps you BUILD muscle memory for constraint navigation,
not just play the right notes.

Key concepts:
- Trajectory: the path through pitch space, not just target notes
- Internalization: repeating until the constraint disappears
- Vocabulary: musical phrases tied to constraint configurations
"""

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .terrain import Terrain, TERRAINS


@dataclass
class VocabularyItem:
    """A musical phrase tied to a constraint context."""
    name: str
    notes: List[int]        # MIDI pitches (relative to key)
    durations: List[float]  # relative durations
    context: str            # e.g., "ii-V-I", "blues_turnaround"
    difficulty: float = 0.5 # 0=easy, 1=hard


@dataclass
class Trajectory:
    """A path through constraint space — not just notes but HOW to move."""
    start: int              # starting scale degree
    path: List[int]         # sequence of scale degrees
    curvature: List[float]  # how much to bend between each step
    register: str = "tenor" # tenor, alto, bass, treble
    voiceleading: str = "smooth"  # smooth, parallel, contrary


@dataclass
class PracticeSession:
    """One practice block with metrics."""
    focus: str
    tempo: int
    repetitions: int
    accuracy: float = 0.0
    internalization: float = 0.0  # 0=conscious, 1=automatic
    duration_seconds: float = 0.0


# ── Built-in Vocabulary ──────────────────────────────────────────────

BEBOP_VOCABULARY: List[VocabularyItem] = [
    VocabularyItem("chromatic_enclosure", [2, 1, 0, -1, 0], [0.5, 0.5, 0.5, 0.5, 1.0],
                   "ii-V-I", 0.6),
    VocabularyItem("approach_tone", [-1, 0], [0.5, 1.0], "any", 0.3),
    VocabularyItem("triplet_run", [0, 2, 4, 5, 7, 9, 11, 12], [1/3]*8,
                   "I", 0.7),
    VocabularyItem("diminished_run", [0, 3, 6, 9, 0], [0.5]*4 + [1.0],
                   "V7", 0.8),
    VocabularyItem("blues_cliche", [0, -1, 0, 3, 4, 3, 0], [0.5, 0.25, 0.25, 0.5, 0.5, 0.5, 1.0],
                   "I7", 0.4),
    VocabularyItem("parker_omnibook_1", [12, 11, 9, 7, 5, 4, 2, 0], [0.5]*8,
                   "I", 0.5),
]

BLUES_VOCABULARY: List[VocabularyItem] = [
    VocabularyItem("blue_3rd_bend", [3, 2.5, 3, 4], [0.5, 1.0, 0.5, 1.0],
                   "I7", 0.5),
    VocabularyItem("turnaround", [5, 4, 3, 2, 1, 0], [0.5]*5 + [1.5],
                   "turnaround", 0.4),
    VocabularyItem("train_whistle", [0, 7, 0, 10, 7], [1.0, 0.5, 0.5, 1.0, 1.0],
                   "I7", 0.3),
    VocabularyItem("moan", [5, 4, 3, 3], [1.0, 1.0, 0.5, 1.5],
                   "IV7", 0.4),
]


class ParkerEngine:
    """The practice engine: build muscle memory for constraint navigation."""

    def __init__(self, terrain: Terrain, key: int = 60):
        self.terrain = terrain
        self.key = key  # MIDI pitch of the root
        self._vocabulary: Dict[str, List[VocabularyItem]] = {
            "bebop": BEBOP_VOCABULARY,
            "blues": BLUES_VOCABULARY,
        }
        self._practice_history: List[PracticeSession] = []
        self._internalization_map: Dict[str, float] = {}  # vocab_name -> level

    def get_vocabulary(self, focus: Optional[str] = None) -> List[VocabularyItem]:
        """Get vocabulary items, optionally filtered by focus area."""
        items = []
        for vocab_list in self._vocabulary.values():
            items.extend(vocab_list)
        if focus:
            items = [v for v in items if focus in v.context or focus in v.name]
        return items

    def practice(self, focus: Optional[str] = None, tempo: int = 120,
                 sessions: int = 1) -> List[PracticeSession]:
        """
        Run practice sessions building internalization.
        Returns session results with accuracy and internalization metrics.
        """
        vocab = self.get_vocabulary(focus)
        if not vocab:
            vocab = self.get_vocabulary()

        results = []
        for _ in range(sessions):
            item = random.choice(vocab)
            # Simulate practice: accuracy improves with repetition
            base_accuracy = random.gauss(0.7, 0.15)
            accuracy = max(0.0, min(1.0, base_accuracy))

            # Internalization increases with accuracy and practice count
            key = item.name
            prev = self._internalization_map.get(key, 0.0)
            internalization = min(1.0, prev + accuracy * 0.1)
            self._internalization_map[key] = internalization

            session = PracticeSession(
                focus=item.name,
                tempo=tempo,
                repetitions=random.randint(4, 12),
                accuracy=accuracy,
                internalization=internalization,
                duration_seconds=random.uniform(60, 300),
            )
            results.append(session)
            self._practice_history.append(session)

        return results

    def feel_trajectory(self, progression: str, voiceleading: str = "smooth",
                        register: str = "tenor") -> Trajectory:
        """
        Generate a trajectory through pitch space for internalization.
        The trajectory captures HOW to move, not just WHERE to land.
        """
        # Map common progressions to scale degree paths
        progressions = {
            "ii-V-I": [2, 4, 5, 7, 0],
            "I-vi-ii-V": [0, 9, 2, 5, 0],
            "blues_12": [0, 0, 0, 0, 5, 5, 0, 0, 7, 5, 2, 5, 0],
            "rhythm": [0, 3, 5, 0, 0, 3, 5, 0],
            "tritone_sub": [0, 6, 5, 0],
        }
        path = progressions.get(progression, [0, 2, 4, 5, 7, 0])

        # Generate curvature based on terrain's chromatic density
        curvature = []
        for i in range(len(path) - 1):
            if self.terrain.chromatic_density > 0.5:
                curvature.append(random.uniform(-2.0, 2.0))
            else:
                curvature.append(random.uniform(-0.5, 0.5))

        return Trajectory(
            start=path[0],
            path=path,
            curvature=curvature,
            register=register,
            voiceleading=voiceleading,
        )

    def perform(self, changes: str = "blues_12", minutes: float = 2.0,
                internalization_threshold: float = 0.5) -> dict:
        """
        Generate a solo. The more internalized, the more fluid.
        Low internalization = mechanical, high = flowing.
        """
        traj = self.feel_trajectory(changes)
        avg_internalization = (
            sum(self._internalization_map.values()) / max(1, len(self._internalization_map))
        )
        if avg_internalization < internalization_threshold:
            avg_internalization = internalization_threshold  # floor

        # Generate MIDI notes based on trajectory and internalization
        notes = self._generate_notes(traj, minutes, avg_internalization)

        return {
            "notes": notes,
            "internalization": avg_internalization,
            "trajectory": traj,
            "terrain": self.terrain.name,
            "key": self.key,
            "tempo": random.randint(*self.terrain.typical_tempo),
        }

    def _generate_notes(self, traj: Trajectory, minutes: float,
                        internalization: float) -> List[dict]:
        """Generate a sequence of MIDI notes."""
        notes = []
        t = 0.0
        duration = minutes * 60.0  # seconds
        bpm = random.randint(*self.terrain.typical_tempo)
        beat_dur = 60.0 / bpm

        degree_weights = {d.degree: d.weight for d in self.terrain.scale_degrees}

        while t < duration:
            # Pick from trajectory or chromatic neighbor based on internalization
            if random.random() < internalization:
                # High internalization: follow trajectory smoothly
                degree = random.choice(traj.path)
            else:
                # Low internalization: more random exploration
                degree = random.choice(list(degree_weights.keys()))

            pitch = self.key + degree
            # Add microtonal curvature if terrain has blues notes
            velocity = random.randint(60, 110)

            note_len = beat_dur * random.choice([0.5, 1.0, 1.0, 2.0])
            notes.append({
                "pitch": pitch,
                "velocity": velocity,
                "start": round(t, 3),
                "duration": round(note_len, 3),
            })
            t += note_len

        return notes

    def midi_to_events(self, notes: List[dict], bpm: int = 120) -> List[Tuple[int, int, int, int]]:
        """Convert internal note format to (pitch, start_tick, duration_ticks, velocity)."""
        ppq = 480  # pulses per quarter note
        events = []
        for n in notes:
            start_tick = int(n["start"] * (ppq * bpm / 60.0))
            dur_ticks = int(n["duration"] * (ppq * bpm / 60.0))
            events.append((n["pitch"], start_tick, dur_ticks, n["velocity"]))
        return events

    @property
    def practice_log(self) -> List[PracticeSession]:
        return self._practice_history.copy()

    @property
    def internalization_levels(self) -> Dict[str, float]:
        return self._internalization_map.copy()
