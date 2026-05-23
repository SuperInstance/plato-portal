"""
Armstrong Mode — Liberation Through Constraint Removal.

Louis Armstrong showed that sometimes removing constraints reveals
new territory. This mode helps you FIND liberation by selectively
removing constraints while keeping the ones that matter.

Key concepts:
- Constraint layers: pitch_grid, time_grid, key, form, ...
- Removal as creative tool: take away and see what emerges
- Higher-order preservation: keep emotional trajectory, phrasing
"""

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from .terrain import Terrain, TERRAINS


@dataclass
class ConstraintLayer:
    """A layer of constraint that can be removed or kept."""
    name: str
    description: str
    order: int  # 0=lowest (pitch), 3=highest (form)
    active: bool = True
    weight: float = 1.0  # how strongly this constraint binds


# ── Default Constraint Layers ────────────────────────────────────────

DEFAULT_LAYERS = [
    ConstraintLayer("pitch_grid", "Fixed pitch classes (12-tone equal temperament)", 0),
    ConstraintLayer("time_grid", "Fixed rhythmic grid (meter)", 0),
    ConstraintLayer("key", "Tonal center and scale", 1),
    ConstraintLayer("harmonic_rhythm", "Rate of chord changes", 1),
    ConstraintLayer("form", "Song structure (AABA, blues, etc.)", 2),
    ConstraintLayer("phrasing", "Phrase lengths and shapes", 2),
    ConstraintLayer("emotional_trajectory", "Overall emotional arc", 3),
    ConstraintLayer("register", "Range boundaries", 1),
    ConstraintLayer("density", "Note density limits", 1),
    ConstraintLayer("articulation", "Articulation patterns", 2),
]


class ArmstrongEngine:
    """Liberation through constraint removal."""

    def __init__(self, terrain: Terrain, key: int = 60):
        self.terrain = terrain
        self.key = key
        self.layers: Dict[str, ConstraintLayer] = {l.name: l for l in DEFAULT_LAYERS}
        self._base_notes: Optional[List[dict]] = None

    def load(self, song: str) -> None:
        """Load a song as the starting point."""
        # Generate a basic rendition of the song
        self._base_notes = self._generate_song(song)

    def remove_constraint(self, name: str) -> bool:
        """Remove a constraint layer. Returns True if it existed."""
        if name in self.layers:
            self.layers[name].active = False
            return True
        return False

    def keep_constraint(self, name: str) -> bool:
        """Explicitly keep a constraint layer."""
        if name in self.layers:
            self.layers[name].active = True
            self.layers[name].weight = 1.5  # extra emphasis
            return True
        return False

    def perform(self, forget_lyrics: bool = False, minutes: float = 2.0) -> dict:
        """
        Perform with the current constraint configuration.
        Removed constraints add freedom; kept ones provide structure.
        """
        base = self._base_notes or self._generate_song("default")

        if forget_lyrics:
            self.remove_constraint("pitch_grid")

        notes = self._apply_constraints(base, minutes)

        active = [name for name, layer in self.layers.items() if layer.active]
        removed = [name for name, layer in self.layers.items() if not layer.active]

        return {
            "notes": notes,
            "active_constraints": active,
            "removed_constraints": removed,
            "freedom_level": len(removed) / max(1, len(self.layers)),
            "terrain": self.terrain.name,
            "key": self.key,
        }

    def _apply_constraints(self, base: List[dict], minutes: float) -> List[dict]:
        """Apply constraint configuration to generate performance."""
        notes = []
        t = 0.0
        duration = minutes * 60.0
        bpm = random.randint(*self.terrain.typical_tempo)
        beat_dur = 60.0 / bpm

        degrees = [d.degree for d in self.terrain.scale_degrees]
        weights = [d.weight for d in self.terrain.scale_degrees]

        while t < duration:
            # Base: pick from terrain
            pitch = self.key

            if self.layers["pitch_grid"].active:
                degree = random.choices(degrees, weights=weights)[0]
                pitch = self.key + degree
            else:
                # Free pitch: continuous space (quantized to semitones but unrestricted)
                pitch = self.key + random.randint(-12, 24)

            if not self.layers["key"].active:
                # Drift from tonal center
                pitch += random.choice([-5, -2, 2, 5, 7])

            if not self.layers["register"].active:
                pitch = random.randint(21, 108)
            else:
                pitch = max(self.terrain.register_tendency[0],
                           min(self.terrain.register_tendency[1], pitch))

            # Duration
            if self.layers["time_grid"].active:
                note_len = beat_dur * random.choice([0.5, 1.0, 1.0, 2.0])
            else:
                note_len = random.uniform(0.1, beat_dur * 4)

            # Density (but always allow some notes through)
            if self.layers["density"].active and len(notes) > 3:
                if random.random() > 0.6:
                    t += beat_dur * random.choice([0.5, 1.0])
                    continue

            # Phrasing constraint
            if self.layers["phrasing"].active and random.random() < 0.1:
                # Insert phrase break
                t += beat_dur * random.choice([1.0, 2.0, 4.0])
                continue

            velocity = random.randint(50, 110)
            if not self.layers["articulation"].active:
                velocity = random.randint(30, 127)

            notes.append({
                "pitch": max(21, min(108, pitch)),
                "velocity": velocity,
                "start": round(t, 3),
                "duration": round(note_len, 3),
            })
            t += note_len

        return notes

    def _generate_song(self, song: str) -> List[dict]:
        """Generate a basic song as starting point."""
        bpm = 100
        beat_dur = 60.0 / bpm
        notes = []
        degrees = [d.degree for d in self.terrain.scale_degrees]
        weights = [d.weight for d in self.terrain.scale_degrees]

        for i in range(32):
            degree = random.choices(degrees, weights=weights)[0]
            notes.append({
                "pitch": self.key + degree,
                "velocity": random.randint(60, 90),
                "start": round(i * beat_dur, 3),
                "duration": round(beat_dur, 3),
            })
        return notes

    def reset_constraints(self) -> None:
        """Reset all constraints to active."""
        for layer in self.layers.values():
            layer.active = True
            layer.weight = 1.0
