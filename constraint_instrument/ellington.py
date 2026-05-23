"""
Ellington Mode — The Architect.

Duke Ellington composed frameworks for his musicians to emerge within.
This mode lets you DESIGN the constraint architecture — the scaffolding
within which emergence happens.

Key concepts:
- Chart: a composed framework with planned constraint configurations
- Section: a segment with specific constraint profiles
- Personality: player traits that shape how constraints are navigated
- Release points: where constraints relax or tighten
"""

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .terrain import Terrain, TERRAINS


@dataclass
class PlayerPersonality:
    """Musical personality that shapes constraint navigation."""
    name: str
    instrument: str
    traits: List[str]  # e.g., "bold", "lyrical", "angular"
    register_preference: str = "middle"  # low, middle, high, wide
    rhythmic_tendency: float = 0.5  # 0=behind, 0.5=on, 1=ahead
    density: float = 0.5  # 0=sparse, 1=dense


@dataclass
class ConstraintProfile:
    """A configuration of constraints for a section."""
    name: str
    harmonic_freedom: float = 0.5   # 0=strict changes, 1=free
    rhythmic_freedom: float = 0.5   # 0=strict time, 1=rubato
    register_range: Tuple[int, int] = (48, 84)
    density: float = 0.5            # 0=sparse, 1=dense
    blues_inflection: float = 0.0   # 0=none, 1=full blues
    chromatic_allowed: float = 0.3  # how much chromaticism
    description: str = ""


@dataclass
class Section:
    """A section of the chart with its own constraint profile."""
    name: str
    description: str
    bars: int
    constraint_profile: ConstraintProfile
    soloist: Optional[str] = None
    backgrounds: bool = False
    constraint_changes: List[dict] = field(default_factory=list)
    # e.g., [{"at_bar": 4, "relax": "rhythmic_freedom", "to": 0.8}]


@dataclass
class Chart:
    """A composed framework — the Ellington architecture."""
    title: str
    sections: List[Section]
    players: Dict[str, PlayerPersonality] = field(default_factory=dict)
    key: int = 60
    tempo: int = 140

    def assign(self, instrument: str, personality: str) -> None:
        """Assign a player with personality traits to an instrument chair."""
        traits = [t.strip() for t in personality.split(",")]
        register_map = {"low": "low", "middle": "middle", "high": "high"}
        reg = "middle"
        for t in traits:
            if "upper" in t or "high" in t:
                reg = "high"
            elif "low" in t or "deep" in t:
                reg = "low"

        density = 0.5
        if "dense" in traits or "angular" in traits:
            density = 0.7
        elif "sparse" in traits or "lyrical" in traits:
            density = 0.3

        rhythmic = 0.5
        if "ahead" in traits or "driving" in traits:
            rhythmic = 0.7
        elif "behind" in traits or "laid" in traits:
            rhythmic = 0.3

        self.players[instrument] = PlayerPersonality(
            name=instrument,
            instrument=instrument,
            traits=traits,
            register_preference=reg,
            rhythmic_tendency=rhythmic,
            density=density,
        )

    def total_bars(self) -> int:
        return sum(s.bars for s in self.sections)


class EllingtonEngine:
    """The architect: compose frameworks for emergence."""

    def __init__(self, terrain: Terrain, key: int = 60):
        self.terrain = terrain
        self.key = key

    def compose(self, sections: List[str], constraints: List[str],
                title: str = "Untitled") -> Chart:
        """
        Compose a chart from natural language section and constraint descriptions.
        Parses into structured Chart with ConstraintProfiles.
        """
        parsed_sections = []
        for i, desc in enumerate(sections):
            # Parse section description
            name = desc.split(":")[0].strip() if ":" in desc else f"section_{i+1}"
            section_desc = desc.split(":", 1)[1].strip() if ":" in desc else desc

            # Determine constraint profile from description
            profile = self._parse_profile(section_desc, name)
            bars = self._estimate_bars(section_desc)

            # Check for soloist
            soloist = None
            for instrument in ["sax", "trumpet", "piano", "guitar", "bass", "drums"]:
                if instrument in section_desc.lower():
                    soloist = instrument

            backgrounds = "background" in section_desc.lower()

            parsed_sections.append(Section(
                name=name,
                description=section_desc,
                bars=bars,
                constraint_profile=profile,
                soloist=soloist,
                backgrounds=backgrounds,
            ))

        return Chart(
            title=title,
            sections=parsed_sections,
            key=self.key,
            tempo=random.randint(*self.terrain.typical_tempo),
        )

    def render(self, chart: Chart, bpm: Optional[int] = None) -> dict:
        """
        Render a chart to MIDI notes.
        Each section generates notes based on its constraint profile
        and assigned player personalities.
        """
        bpm = bpm or chart.tempo
        beat_dur = 60.0 / bpm
        all_notes = []
        t = 0.0

        for section in chart.sections:
            section_dur = section.bars * 4 * beat_dur  # assume 4/4

            if section.soloist and section.soloist in chart.players:
                player = chart.players[section.soloist]
                notes = self._render_solo(section, player, t, bpm)
            else:
                notes = self._render_ensemble(section, t, bpm)

            all_notes.extend(notes)
            t += section_dur

        return {
            "title": chart.title,
            "notes": all_notes,
            "tempo": bpm,
            "key": chart.key,
            "total_bars": chart.total_bars(),
            "sections": len(chart.sections),
        }

    def _parse_profile(self, desc: str, name: str) -> ConstraintProfile:
        """Parse natural language into a constraint profile."""
        desc_lower = desc.lower()

        harmonic = 0.5
        if "open" in desc_lower or "free" in desc_lower:
            harmonic = 0.8
        elif "strict" in desc_lower or "tight" in desc_lower:
            harmonic = 0.2

        rhythmic = 0.5
        if "rubato" in desc_lower or "open" in desc_lower:
            rhythmic = 0.8
        elif "locked" in desc_lower or "grid" in desc_lower:
            rhythmic = 0.1

        density = 0.5
        if "full" in desc_lower or "ensemble" in desc_lower:
            density = 0.8
        elif "sparse" in desc_lower or "open" in desc_lower:
            density = 0.3

        blues = 0.3 if "blues" in desc_lower else 0.0

        return ConstraintProfile(
            name=name,
            harmonic_freedom=harmonic,
            rhythmic_freedom=rhythmic,
            density=density,
            blues_inflection=blues,
            description=desc,
        )

    def _estimate_bars(self, desc: str) -> int:
        """Estimate bars from description."""
        desc_lower = desc.lower()
        if "intro" in desc_lower:
            return 4
        if "outro" in desc_lower:
            return 8
        if "solo" in desc_lower:
            return 32
        if "shout" in desc_lower:
            return 16
        return 16  # default

    def _render_solo(self, section: Section, player: PlayerPersonality,
                     start_time: float, bpm: int) -> List[dict]:
        """Render a solo section for a specific player."""
        profile = section.constraint_profile
        beat_dur = 60.0 / bpm
        duration = section.bars * 4 * beat_dur
        notes = []
        t = start_time

        degree_weights = {d.degree: d.weight for d in self.terrain.scale_degrees}
        all_degrees = list(degree_weights.keys())

        while t < start_time + duration:
            # Note density affected by profile and player personality
            if random.random() > profile.density * player.density:
                # rest
                t += beat_dur * random.choice([0.5, 1.0])
                continue

            degree = random.choices(all_degrees,
                                    weights=[degree_weights.get(d, 0.5) for d in all_degrees])[0]
            register_offset = {"low": -12, "middle": 0, "high": 12}.get(player.register_preference, 0)
            pitch = self.key + degree + register_offset

            # Rhythmic tendency: slight timing offset
            timing_offset = (player.rhythmic_tendency - 0.5) * 0.1 * beat_dur

            velocity = random.randint(60, 100)
            note_len = beat_dur * random.choice([0.5, 1.0, 1.0, 2.0])

            notes.append({
                "pitch": max(21, min(108, pitch)),
                "velocity": velocity,
                "start": round(t + timing_offset, 3),
                "duration": round(note_len, 3),
                "section": section.name,
                "player": player.name,
            })
            t += note_len

        return notes

    def _render_ensemble(self, section: Section, start_time: float,
                         bpm: int) -> List[dict]:
        """Render an ensemble section (simplified)."""
        profile = section.constraint_profile
        beat_dur = 60.0 / bpm
        duration = section.bars * 4 * beat_dur
        notes = []
        t = start_time

        degrees = [d.degree for d in self.terrain.scale_degrees]

        while t < start_time + duration:
            if random.random() > profile.density:
                t += beat_dur
                continue

            # Ensemble: multiple notes (chords)
            n_voices = random.randint(2, 4)
            base_degree = random.choice(degrees)
            for v in range(n_voices):
                pitch = self.key + base_degree + v * random.choice([3, 4, 7])
                notes.append({
                    "pitch": max(21, min(108, pitch)),
                    "velocity": random.randint(50, 90),
                    "start": round(t, 3),
                    "duration": round(beat_dur * random.choice([1.0, 2.0, 4.0]), 3),
                    "section": section.name,
                    "player": "ensemble",
                })
            t += beat_dur * random.choice([1.0, 2.0, 4.0])

        return notes
