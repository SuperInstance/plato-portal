"""
TextureAutomation — evolving parameter curves for electronic music.

"What makes techno sound like techno: evolving textures."

Generates per-bar parameter curves (filter, reverb, density, velocity, swing)
that follow arrangement structures (build_drop, peak_time, minimal, etc.).
Wire into Arrangement to modulate tracks over time, or export as JSON/MIDI CC
for DAW automation.

Usage:
    from constraint_instrument.texture import TextureAutomation

    tex = TextureAutomation('build_drop', bars=16, bpm=130)
    curves = tex.generate()

    # Apply to an Arrangement
    from constraint_instrument.tracks import techno_loop
    arr = techno_loop(bpm=130, bars=16)
    tex.apply_to_arrangement(arr)

    # Export
    tex.export_json()   # dict for DAW import
    tex.export_midi_cc()  # CC74=filter, CC91=reverb
"""

import copy
import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class TextureCurve:
    """A parameter curve over time (list of values per bar)."""

    name: str
    values: List[float]  # 0.0-1.0, one per bar

    def at(self, bar: int) -> float:
        """Get value at bar (with linear interpolation).

        Args:
            bar: Bar number (can be fractional for interpolation).

        Returns:
            Interpolated value between 0.0 and 1.0.
        """
        if not self.values:
            return 0.0
        if bar <= 0:
            return self.values[0]
        if bar >= len(self.values) - 1:
            return self.values[-1]

        # Linear interpolation
        lo = int(bar)
        hi = min(lo + 1, len(self.values) - 1)
        frac = bar - lo
        return self.values[lo] * (1.0 - frac) + self.values[hi] * frac

    def normalize(self):
        """Scale values to 0-1 range (in place)."""
        if not self.values:
            return
        lo = min(self.values)
        hi = max(self.values)
        if hi - lo < 1e-9:
            # Constant curve — set to 0.5
            self.values = [0.5] * len(self.values)
            return
        self.values = [(v - lo) / (hi - lo) for v in self.values]

    def __repr__(self) -> str:
        preview = ', '.join(f'{v:.2f}' for v in self.values[:8])
        ellipsis = ', ...' if len(self.values) > 8 else ''
        return f"TextureCurve({self.name!r}, [{preview}{ellipsis}], bars={len(self.values)})"


# ── Curve generator helpers ──────────────────────────────────────────

def _ramp(start: float, end: float, length: int) -> List[float]:
    """Linear ramp from start to end over length steps."""
    if length <= 0:
        return []
    if length == 1:
        return [(start + end) / 2.0]
    return [start + (end - start) * i / (length - 1) for i in range(length)]


def _plateau(value: float, length: int, wobble: float = 0.02) -> List[float]:
    """Flat plateau with optional subtle wobble for organic feel."""
    return [max(0.0, min(1.0, value + random.gauss(0, wobble))) for _ in range(length)]


def _exp_ramp(start: float, end: float, length: int, exponent: float = 2.0) -> List[float]:
    """Exponential ramp — slow start, fast finish (or vice versa)."""
    if length <= 0:
        return []
    if length == 1:
        return [(start + end) / 2.0]
    raw = []
    for i in range(length):
        t = i / (length - 1)
        if start < end:
            # Rising: slow then fast
            v = start + (end - start) * (t ** exponent)
        else:
            # Falling: fast then slow
            v = start + (end - start) * (1.0 - (1.0 - t) ** exponent)
        raw.append(v)
    return raw


# ── Section parameter profiles ───────────────────────────────────────

# Each section maps to parameter targets:
#   filter_cutoff, reverb_wet, note_density, velocity, swing
SECTION_PROFILES = {
    # (filter, reverb, density, velocity, swing)
    'breakdown':  (0.15, 0.60, 0.20, 0.30, 0.10),
    'intro':      (0.20, 0.50, 0.25, 0.35, 0.10),
    'groove':     (0.50, 0.25, 0.55, 0.60, 0.30),
    'build':      (0.55, 0.35, 0.60, 0.65, 0.20),
    'accent':     (0.65, 0.30, 0.70, 0.70, 0.40),
    'peak':       (0.90, 0.20, 0.90, 0.90, 0.15),
    'drop':       (0.95, 0.15, 0.95, 0.95, 0.10),
    'release':    (0.40, 0.50, 0.40, 0.50, 0.20),
    'outro':      (0.25, 0.55, 0.25, 0.35, 0.10),
}

# Transition curves between sections
TRANSITION_STYLES = {
    # How to transition into this section from the previous
    'breakdown':  'exp_fall',   # quick fade down
    'intro':      'ramp_up',    # gentle rise
    'groove':     'flat',       # hold steady
    'build':      'exp_rise',   # slow then fast rise
    'accent':     'step',       # immediate change
    'peak':       'exp_rise',
    'drop':       'step',       # sudden hit
    'release':    'exp_fall',
    'outro':      'exp_fall',
}


class TextureAutomation:
    """Generate parameter curves for arrangement sections.

    Used by Arrangement to modulate synth parameters over time.
    This is what makes techno sound like techno: evolving textures.
    """

    STRUCTURES = {
        'build_drop': [
            ('breakdown', 4),
            ('build', 4),
            ('drop', 4),
            ('release', 4),
        ],
        'peak_time': [
            ('intro', 8),
            ('build', 8),
            ('peak', 8),
            ('outro', 8),
        ],
        'minimal': [
            ('groove', 4),
            ('accent', 4),
        ],
        'roller': [
            ('groove', 8),
            ('build', 4),
            ('drop', 4),
        ],
        'deep_house': [
            ('intro', 4),
            ('groove', 8),
            ('build', 4),
            ('accent', 4),
            ('outro', 4),
            # 24 bars total
        ],
        'ambient_drone': [
            ('intro', 8),
            ('groove', 8),
            ('release', 8),
            ('outro', 8),
        ],
    }

    PARAM_NAMES = ['filter_cutoff', 'reverb_wet', 'note_density', 'velocity', 'swing']

    def __init__(self, structure: str = 'build_drop', bars: int = 16, bpm: int = 130):
        """Create a TextureAutomation.

        Args:
            structure: Structure name from STRUCTURES.
            bars: Total bars (must match structure bar count).
            bpm: Tempo.

        Raises:
            ValueError: If structure is unknown.
        """
        if structure not in self.STRUCTURES:
            available = ', '.join(sorted(self.STRUCTURES.keys()))
            raise ValueError(
                f"Unknown structure '{structure}'. Available: {available}"
            )

        self.structure = structure
        self.bars = bars
        self.bpm = bpm
        self.curves: Dict[str, TextureCurve] = {}
        self._sections: List[Tuple[str, int, int]] = []  # (name, start_bar, end_bar)

        # Validate bar count matches structure
        structure_bars = sum(b for _, b in self.STRUCTURES[structure])
        if bars != structure_bars:
            # Allow flexible bar counts by scaling sections
            pass  # We'll handle this in generate()

    def _build_sections(self) -> List[Tuple[str, int, int]]:
        """Expand the structure into (name, start_bar, end_bar) tuples."""
        sections = self.STRUCTURES[self.structure]
        total_struct_bars = sum(b for _, b in sections)

        result = []
        bar = 0
        for name, count in sections:
            # Scale section length to fit requested bar count
            scaled = max(1, round(count * self.bars / total_struct_bars))
            result.append((name, bar, bar + scaled))
            bar += scaled

        # Adjust last section to end exactly at self.bars
        if result:
            last_name, last_start, _ = result[-1]
            result[-1] = (last_name, last_start, self.bars)

        return result

    def get_section(self, bar: int) -> str:
        """Which section is bar N in?

        Args:
            bar: Bar number (0-indexed).

        Returns:
            Section name (e.g. 'breakdown', 'build', 'drop').
        """
        if not self._sections:
            self._sections = self._build_sections()

        for name, start, end in self._sections:
            if start <= bar < end:
                return name

        # Past the end — return last section
        if self._sections:
            return self._sections[-1][0]
        return 'groove'

    def generate(self) -> Dict[str, TextureCurve]:
        """Generate all parameter curves for the arrangement.

        Returns:
            Dict mapping parameter names to TextureCurve instances:
            - filter_cutoff: how open the lowpass filter is (0=closed, 1=open)
            - reverb_wet: reverb amount (0=dry, 1=wet)
            - note_density: notes per bar (0=min, 1=max)
            - velocity: average velocity (0=quiet, 1=loud)
            - swing: swing amount (0=straight, 1=full swing)
        """
        self._sections = self._build_sections()

        # Build curves per parameter
        raw_curves = {name: [] for name in self.PARAM_NAMES}

        for sec_name, start_bar, end_bar in self._sections:
            length = end_bar - start_bar
            profile = SECTION_PROFILES.get(sec_name, (0.5, 0.3, 0.5, 0.5, 0.2))
            transition = TRANSITION_STYLES.get(sec_name, 'flat')

            # Get the previous section's ending values for smooth transitions
            prev_values = None
            if start_bar > 0 and raw_curves['filter_cutoff']:
                prev_values = tuple(c[-1] for c in raw_curves.values())

            for param_idx, param_name in enumerate(self.PARAM_NAMES):
                target = profile[param_idx]

                if prev_values is not None and transition != 'flat':
                    prev_val = prev_values[param_idx]
                    segment = self._generate_transition(
                        prev_val, target, length, transition
                    )
                elif transition == 'flat' or prev_values is None:
                    # Plateau with subtle organic wobble
                    segment = _plateau(target, length, wobble=0.015)
                else:
                    segment = _plateau(target, length, wobble=0.015)

                raw_curves[param_name].extend(segment)

        # Trim/pad to exact bar count
        for name in self.PARAM_NAMES:
            vals = raw_curves[name]
            if len(vals) < self.bars:
                # Pad with last value
                vals.extend([vals[-1] if vals else 0.5] * (self.bars - len(vals)))
            elif len(vals) > self.bars:
                vals = vals[:self.bars]
            raw_curves[name] = vals

        # Create TextureCurve objects
        self.curves = {}
        for name in self.PARAM_NAMES:
            self.curves[name] = TextureCurve(
                name=name,
                values=[max(0.0, min(1.0, v)) for v in raw_curves[name]],
            )

        return self.curves

    def _generate_transition(self, start_val: float, end_val: float,
                             length: int, style: str) -> List[float]:
        """Generate a transition segment between two values.

        Args:
            start_val: Starting value.
            end_val: Ending value.
            length: Number of bars in the section.
            style: Transition style name.

        Returns:
            List of float values for this section.
        """
        if length <= 0:
            return []

        if style == 'step':
            # Immediate jump to target (after first bar transition)
            result = [_lerp(start_val, end_val, 0.3)]  # quick snap
            result.extend(_plateau(end_val, length - 1, wobble=0.01))
            return result

        elif style == 'ramp_up':
            return _ramp(start_val, end_val, length)

        elif style == 'exp_rise':
            return _exp_ramp(start_val, end_val, length, exponent=2.5)

        elif style == 'exp_fall':
            return _exp_ramp(start_val, end_val, length, exponent=2.5)

        elif style == 'flat':
            return _plateau(end_val, length, wobble=0.01)

        else:
            return _ramp(start_val, end_val, length)

    def apply_to_arrangement(self, arrangement) -> 'TextureAutomation':
        """Modulate an Arrangement's tracks based on texture curves.

        For each bar, adjusts filter envelope, reverb, density, velocity,
        and swing of all tracks in the arrangement.

        Args:
            arrangement: An Arrangement instance from tracks.py.

        Returns:
            self (for chaining).
        """
        if not self.curves:
            self.generate()

        bar_duration = 4.0 * 60.0 / arrangement.bpm

        for track in arrangement.tracks:
            if not track.notes:
                continue

            for note in track.notes:
                # Determine which bar this note falls in
                bar = int(note['start_time'] / bar_duration)
                bar = max(0, min(bar, self.bars - 1))

                # Get texture values at this bar
                vel_curve = self.curves.get('velocity')
                filter_curve = self.curves.get('filter_cutoff')
                density_curve = self.curves.get('note_density')

                # Modulate velocity based on curve
                if vel_curve:
                    vel_factor = vel_curve.at(bar)
                    # Map 0-1 to 0.3-1.0 range (don't go silent)
                    scaled = 0.3 + 0.7 * vel_factor
                    note['velocity'] = max(1, min(127,
                        int(note['velocity'] * scaled)
                    ))

                # Modulate duration based on density (higher density = shorter notes)
                if density_curve:
                    density = density_curve.at(bar)
                    # density 0 = long notes (factor 1.5), density 1 = short (factor 0.5)
                    dur_factor = 1.5 - density
                    note['duration'] = max(0.02, note['duration'] * dur_factor)

                # Store filter info as metadata (for MIDI CC export)
                if filter_curve:
                    note['_filter_cutoff'] = filter_curve.at(bar)

        return self

    def export_json(self) -> dict:
        """Export curves as JSON-serializable dict for DAW automation import.

        Returns:
            Dict with structure:
            {
                "structure": "build_drop",
                "bars": 16,
                "bpm": 130,
                "sections": [{"name": "breakdown", "start": 0, "end": 4}, ...],
                "curves": {
                    "filter_cutoff": [0.15, 0.16, ...],
                    "reverb_wet": [...],
                    ...
                }
            }
        """
        if not self.curves:
            self.generate()

        sections = []
        for name, start, end in self._sections:
            sections.append({'name': name, 'start': start, 'end': end})

        return {
            'structure': self.structure,
            'bars': self.bars,
            'bpm': self.bpm,
            'sections': sections,
            'curves': {
                name: curve.values
                for name, curve in self.curves.items()
            },
        }

    def export_midi_cc(self) -> List[dict]:
        """Export as MIDI CC events for MIDI automation.

        Maps:
            CC74 = filter_cutoff (brightness)
            CC91 = reverb_wet (reverb depth)
            CC76 = note_density (contour)
            CC11 = velocity (expression)
            CC10 = swing (pan used as proxy)

        Returns:
            List of CC event dicts:
            {"cc": int, "value": int (0-127), "bar": int, "time_offset": float}
        """
        if not self.curves:
            self.generate()

        cc_map = {
            'filter_cutoff': 74,
            'reverb_wet': 91,
            'note_density': 76,
            'velocity': 11,
            'swing': 10,
        }

        bar_duration = 4.0 * 60.0 / self.bpm
        events = []

        for param_name, cc_num in cc_map.items():
            curve = self.curves.get(param_name)
            if not curve:
                continue

            for bar, value in enumerate(curve.values):
                events.append({
                    'cc': cc_num,
                    'value': max(0, min(127, int(value * 127))),
                    'bar': bar,
                    'time_offset': bar * bar_duration,
                })

        events.sort(key=lambda e: (e['time_offset'], e['cc']))
        return events

    def __repr__(self) -> str:
        curves_str = ', '.join(self.curves.keys()) if self.curves else 'not generated'
        return f"TextureAutomation(structure={self.structure!r}, bars={self.bars}, bpm={self.bpm}, curves=[{curves_str}])"


def _lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation."""
    return a + (b - a) * t
