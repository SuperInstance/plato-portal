"""
Ella Mode — Pure Flow. The Tool Disappears.

Ella Fitzgerald scatting — complete mastery. The instrument is
transparent. You don't think about it.

This is the GOAL state: the bathymetric map is internalized.
The performer IS the map.

Key concepts:
- No parameters: the instrument reads intention from trajectory
- Adaptive: follows the performer, not the other way around
- Transparent: no API surface, just music
"""

import random
import math
from typing import List, Optional

from .terrain import Terrain, TERRAINS


class EllaEngine:
    """
    Pure flow. No API parameters. The instrument adapts to you.
    
    Ella mode is reached when all other modes have been internalized:
    - Parker: the lattice is in your nervous system
    - Miles: the frontier is your home
    - Ellington: you compose in real-time
    - Basie: consensus is instant
    - Goodman: you diagnose yourself
    - Armstrong: constraints are your playthings
    
    This engine has no knobs. It reads your trajectory and follows.
    """

    def __init__(self, terrain: Terrain, key: int = 60):
        self.terrain = terrain
        self.key = key
        self._phrase_memory: List[List[dict]] = []
        self._last_direction = 0  # -1=down, 0=flat, 1=up
        self._energy = 0.5  # current energy level, adapts
        self._register_center = (terrain.register_tendency[0] + terrain.register_tendency[1]) // 2

    def perform(self, seed: Optional[int] = None, **kwargs) -> dict:
        """
        Perform. No parameters. The music flows.
        
        The engine adapts based on its own trajectory history,
        building phrases that feel natural and unforced.
        """
        if seed is not None:
            random.seed(seed)

        # Flow generates itself: phrases emerge from the terrain
        notes = []
        t = 0.0
        total_duration = random.uniform(60, 180)  # 1-3 minutes of pure music

        while t < total_duration:
            phrase = self._generate_phrase(t)
            notes.extend(phrase)
            if phrase:
                t = phrase[-1]["start"] + phrase[-1]["duration"]
            else:
                t += 0.5

            # Breath between phrases
            breath = random.uniform(0.3, 1.5)
            # Breath length inversely proportional to energy
            breath *= (1.5 - self._energy)
            t += breath

        return {
            "notes": notes,
            "terrain": self.terrain.name,
            "duration": round(t, 2),
            "mode": "ella",
            # No parameters. Just the music.
        }

    def _generate_phrase(self, start_time: float) -> List[dict]:
        """
        Generate a phrase that flows naturally from the current state.
        No parameters — the phrase emerges from context.
        """
        # Phrase length follows a natural distribution
        # At least 16 notes for a meaningful 4-bar phrase
        phrase_length = max(16, int(random.gauss(24, 6)))
        
        # The phrase has an arc: start, develop, resolve
        degrees = [d.degree for d in self.terrain.scale_degrees]
        weights = [d.weight for d in self.terrain.scale_degrees]

        notes = []
        # Snap starting pitch to nearest terrain degree + key
        current_pitch = self._snap_to_terrain(self._register_center)
        t = start_time

        for i in range(phrase_length):
            # Arc: where in the phrase are we?
            position = i / max(1, phrase_length - 1)  # 0 to 1

            # Energy follows a parabolic arc within the phrase
            phrase_energy = 4 * position * (1 - position)  # peaks at 0.5

            # Pick next degree from terrain, biased by weights
            target_degree = random.choices(degrees, weights=weights, k=1)[0]
            # Add octave offset based on current register
            current_octave = (current_pitch - self.key) // 12
            target_pitch = self.key + current_octave * 12 + target_degree

            # Adjust octave if target is far from current pitch
            if target_pitch < current_pitch - 7:
                target_pitch += 12
            elif target_pitch > current_pitch + 7:
                target_pitch -= 12

            # Direction for optional octave shifts
            if i == 0:
                direction = random.choice([-1, 0, 1])
            elif position < 0.6:
                direction = self._last_direction if random.random() < 0.7 else random.choice([-1, 0, 1])
            else:
                if target_pitch > self._register_center + 7:
                    direction = -1
                elif target_pitch < self._register_center - 7:
                    direction = 1
                else:
                    direction = 0

            self._last_direction = direction

            # Shift by an octave in the phrase direction if energy is high
            if phrase_energy > 0.7 and direction != 0 and random.random() < 0.15:
                target_pitch += direction * 12

            pitch = target_pitch
            # Soft register boundaries (not hard walls)
            pitch = self._soft_clamp(pitch,
                                     self.terrain.register_tendency[0] - 5,
                                     self.terrain.register_tendency[1] + 5)
            current_pitch = pitch

            # Timing: natural rubato
            base_dur = 60.0 / random.randint(*self.terrain.typical_tempo)
            # Vary duration with phrase position
            if position < 0.2 or position > 0.8:
                duration_mult = random.choice([1.0, 1.5, 2.0])
            else:
                duration_mult = random.choice([0.5, 0.5, 1.0, 1.0, 1.5])
            note_dur = base_dur * duration_mult

            # Velocity follows energy
            velocity = int(60 + phrase_energy * 50 + random.gauss(0, 10))
            velocity = max(30, min(120, velocity))

            notes.append({
                "pitch": pitch,
                "velocity": velocity,
                "start": round(t, 3),
                "duration": round(note_dur, 3),
            })
            t += note_dur

        # Update energy based on phrase
        self._energy = 0.7 * self._energy + 0.3 * random.uniform(0.3, 0.9)

        # Drift register center based on energy
        drift = (self._energy - 0.5) * 4
        self._register_center += drift
        # Soft return to center of range
        range_center = (self.terrain.register_tendency[0] + self.terrain.register_tendency[1]) // 2
        self._register_center = 0.95 * self._register_center + 0.05 * range_center

        self._phrase_memory.append(notes)
        return notes

    def _snap_to_terrain(self, pitch: int) -> int:
        """Snap a pitch to the nearest terrain scale degree + key."""
        degrees = [d.degree for d in self.terrain.scale_degrees]
        octave = (pitch - self.key) // 12
        candidates = [self.key + octave * 12 + d for d in degrees] + \
                     [self.key + (octave + 1) * 12 + d for d in degrees] + \
                     [self.key + (octave - 1) * 12 + d for d in degrees]
        return min(candidates, key=lambda c: abs(c - pitch))

    def _soft_clamp(self, value: float, low: float, high: float) -> int:
        """Soft clamp: pushes back toward range but doesn't hard-wall."""
        if value < low:
            value = low + random.uniform(0, 2)
        elif value > high:
            value = high - random.uniform(0, 2)
        return int(value)
