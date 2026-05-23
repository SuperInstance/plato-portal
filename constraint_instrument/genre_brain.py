"""
Genre Brain — load a genre and the system auto-configures everything.

"The killer feature from the Hermes synthesis that nobody asked for
 but everyone would love."

Each genre preset encodes real musical knowledge distilled from
user reports (jazz saxophonist, hip-hop producer, math educator,
electronic producer). Load one and the whole system adapts:
diagnostic weights, grid quantization, loop behavior, terrain,
mode, texture evolution.

Usage:
    from constraint_instrument.genre_brain import GenreBrain

    brain = GenreBrain('jazz')
    inst = brain.create_instrument(key='Bb', bpm=180, bars=8)
    notes = inst.perform()

    # Or apply to an existing instrument
    brain.configure_instrument(inst)

    # Get the raw config
    config = brain.get_preset()
"""

from typing import Any, Dict, List, Optional, Union

from .instrument import Instrument, resolve_terrain, resolve_key, TERRAIN_ALIASES


class GenreBrain:
    """Auto-configure everything for a specific genre."""

    PRESETS: Dict[str, dict] = {
        'jazz': {
            'description': 'Bebop jazz — rubato solos, chord awareness, arc phrases',
            'default_mode': 'parker',
            'default_terrain': 'bebop',
            'diagnostic_weights': {
                'direction': 0.35,    # jazz cares about where lines go
                'curvature': 0.30,    # time feel is critical
                'structure': 0.20,    # solo architecture
                'position': 0.15,     # less important (out notes are valid)
            },
            'grid': None,             # no grid — rubato OK
            'loop': False,            # jazz solos don't loop
            'min_notes_per_bar': 4,
            'max_notes_per_bar': 16,
            'phrase_preference': 'arc',  # rise → peak → fall
            'chord_awareness': True,
            'default_bpm': 140,
            'default_bars': 8,
            'default_key': 'Bb',
        },
        'hip_hop': {
            'description': 'Hip-hop / trap — grid-locked, groove-centric, loop-based',
            'default_mode': 'basie',
            'default_terrain': 'hip_hop_trap',
            'diagnostic_weights': {
                'position': 0.40,     # 808 must hit on 1
                'curvature': 0.30,    # groove is everything
                'structure': 0.20,    # arrangement matters
                'direction': 0.10,    # less important
            },
            'grid': 16,               # 16th note grid
            'loop': True,
            'loop_mutate': 0.1,       # subtle variation
            'min_notes_per_bar': 2,   # 808 + hat
            'max_notes_per_bar': 32,  # hi-hat rolls
            'swing': 0.0,            # trap = straight
            'default_bpm': 140,
            'default_bars': 8,
            'default_key': 'C',
        },
        'techno': {
            'description': 'Techno / electronic — rigid grid, evolving textures, minimal pitch',
            'default_mode': 'ella',
            'default_terrain': 'electronic_techno',
            'diagnostic_weights': {
                'curvature': 0.40,    # texture evolution
                'position': 0.30,     # grid alignment
                'structure': 0.20,    # build → drop → breakdown
                'direction': 0.10,    # least important
            },
            'grid': 16,
            'loop': True,
            'loop_mutate': 0.05,      # very subtle
            'texture_automation': True,
            'arrangement': ['intro', 'build', 'drop', 'breakdown', 'build', 'drop', 'outro'],
            'default_bpm': 130,
            'default_bars': 16,
            'default_key': 'C',
        },
        'classical': {
            'description': 'Classical counterpoint — voice leading, consonance, formal coherence',
            'default_mode': 'ellington',
            'default_terrain': 'classical_counterpoint',
            'diagnostic_weights': {
                'position': 0.35,     # consonance matters
                'direction': 0.30,    # voice leading
                'structure': 0.25,    # formal coherence
                'curvature': 0.10,
            },
            'grid': None,
            'loop': False,
            'strict_rules': True,
            'default_bpm': 80,
            'default_bars': 8,
            'default_key': 'C',
        },
        'education': {
            'description': 'Education mode — balanced diagnostics, math explanations, visualizations',
            'default_mode': 'goodman',
            'default_terrain': 'modal_jazz',
            'diagnostic_weights': {
                'position': 0.25,
                'direction': 0.25,
                'curvature': 0.25,
                'structure': 0.25,
            },
            'show_math': True,        # explain the WHY
            'exercises': True,
            'visualize': True,
            'default_bpm': 100,
            'default_bars': 4,
            'default_key': 'C',
        },
        'blues': {
            'description': 'Delta blues — raw, vocal phrasing, blue notes',
            'default_mode': 'miles',
            'default_terrain': 'delta_blues',
            'diagnostic_weights': {
                'curvature': 0.35,    # vocal phrasing
                'direction': 0.30,    # narrative arc
                'position': 0.20,     # blue notes are off-grid
                'structure': 0.15,
            },
            'grid': None,
            'loop': False,
            'phrase_preference': 'wail',
            'default_bpm': 90,
            'default_bars': 12,
            'default_key': 'E',
        },
        'ambient': {
            'description': 'Ambient — sparse, evolving, texture-first',
            'default_mode': 'ella',
            'default_terrain': 'free_improvisation',
            'diagnostic_weights': {
                'curvature': 0.45,    # slow texture evolution
                'direction': 0.25,
                'structure': 0.20,
                'position': 0.10,
            },
            'grid': None,
            'loop': True,
            'loop_mutate': 0.02,      # almost static
            'texture_automation': True,
            'default_bpm': 60,
            'default_bars': 16,
            'default_key': 'C',
        },
        'gospel': {
            'description': 'Gospel — pentatonic runs, call-response, fullness',
            'default_mode': 'armstrong',
            'default_terrain': 'gospel',
            'diagnostic_weights': {
                'direction': 0.35,    # upward resolution
                'curvature': 0.30,    # vocal inflection
                'position': 0.20,
                'structure': 0.15,
            },
            'grid': None,
            'loop': False,
            'phrase_preference': 'soar',
            'default_bpm': 100,
            'default_bars': 8,
            'default_key': 'G',
        },
    }

    # Aliases for convenience
    ALIASES: Dict[str, str] = {
        'trap': 'hip_hop',
        'hip-hop': 'hip_hop',
        'hiphop': 'hip_hop',
        'rap': 'hip_hop',
        'edm': 'techno',
        'electronic': 'techno',
        'house': 'techno',
        'classical_counterpoint': 'classical',
        'counterpoint': 'classical',
        'math': 'education',
        'teaching': 'education',
        'delta_blues': 'blues',
        'delta': 'blues',
    }

    def __init__(self, genre: str):
        """Load a genre brain preset.

        Args:
            genre: Genre name. E.g. 'jazz', 'hip_hop', 'techno',
                   'classical', 'education', 'blues', 'ambient', 'gospel'.
                   Aliases accepted (e.g. 'trap' → 'hip_hop').

        Raises:
            ValueError: If genre is unknown.
        """
        key = genre.strip().lower()

        # Resolve alias
        key = self.ALIASES.get(key, key)

        if key not in self.PRESETS:
            available = sorted(set(list(self.PRESETS.keys()) + list(self.ALIASES.keys())))
            raise ValueError(
                f"Unknown genre '{genre}'. Available genres: {', '.join(available)}"
            )

        self._genre_key = key
        self._preset = dict(self.PRESETS[key])  # shallow copy

    @property
    def genre(self) -> str:
        """Return the canonical genre name."""
        return self._genre_key

    @property
    def description(self) -> str:
        """Return a human-readable description of this genre preset."""
        return self._preset.get('description', '')

    def get_preset(self) -> dict:
        """Return the full genre configuration (copy)."""
        return dict(self._preset)

    def get_diagnostic_weights(self) -> Dict[str, float]:
        """Return the diagnostic weight overrides for this genre."""
        return dict(self._preset.get('diagnostic_weights', {}))

    def create_instrument(self, **overrides) -> Instrument:
        """Create a fully-configured Instrument for this genre.

        Any Instrument constructor parameter can be overridden:
            key, bpm, bars

        Additional genre-brain-specific overrides:
            mode, terrain (override genre defaults)

        Returns:
            Instrument configured for the genre.
        """
        # Start with genre defaults
        params = {
            'mode': self._preset['default_mode'],
            'terrain': self._preset['default_terrain'],
            'key': self._preset.get('default_key', 'C'),
            'bpm': self._preset.get('default_bpm', 100),
            'bars': self._preset.get('default_bars', 4),
        }

        # Apply user overrides
        params.update(overrides)

        return Instrument(**params)

    def configure_instrument(self, instrument: Instrument) -> Instrument:
        """Apply genre settings to an existing Instrument.

        This re-creates the engine with genre-appropriate mode and terrain,
        preserving the instrument's key, bpm, and bars.

        Args:
            instrument: An existing Instrument instance.

        Returns:
            The same Instrument (modified in place via re-init pattern).
        """
        # We rebuild the instrument with genre defaults but keep user's params
        Instrument.__init__(
            instrument,
            mode=self._preset['default_mode'],
            terrain=self._preset['default_terrain'],
            key=instrument._key,
            bpm=instrument.bpm,
            bars=instrument.bars,
        )
        return instrument

    def configure_diagnostic(self, diagnostic) -> dict:
        """Return genre-specific diagnostic weight overrides.

        Pass the result to GoodmanEngine.diagnose() or use directly.
        """
        return self.get_diagnostic_weights()

    def quantize_notes(self, notes: list, bpm: int = None) -> list:
        """Quantize notes to this genre's grid.

        Args:
            notes: List of note dicts with 'start_time' and 'duration'.
            bpm: Tempo. If None, uses genre default.

        Returns:
            Quantized note list (copy).
        """
        grid = self._preset.get('grid')
        if grid is None:
            # No quantization for this genre
            return list(notes)

        use_bpm = bpm or self._preset.get('default_bpm', 120)
        beat_duration = 60.0 / use_bpm
        grid_step = beat_duration / grid  # e.g. 16th note = beat/4

        quantized = []
        for n in notes:
            qn = dict(n)
            # Snap start_time to nearest grid point
            if grid_step > 0:
                qn['start_time'] = round(n['start_time'] / grid_step) * grid_step
                # Snap duration to grid multiples (minimum 1 grid step)
                dur_steps = max(1, round(n['duration'] / grid_step))
                qn['duration'] = dur_steps * grid_step
            quantized.append(qn)

        return quantized

    def apply_loop(self, notes: list, bars: int = None, bpm: int = None,
                   mutation_rate: float = None) -> list:
        """Apply loop behavior to notes if genre requires it.

        For loop-based genres (techno, hip-hop), repeats the pattern
        with optional subtle mutation per repetition.

        For non-loop genres, returns notes unchanged.

        Args:
            notes: List of note dicts (typically 1-bar pattern).
            bars: Number of bars to fill. If None, uses genre default.
            bpm: Tempo. If None, uses genre default.
            mutation_rate: Override the genre's loop_mutate rate.

        Returns:
            Extended note list (or original if genre doesn't loop).
        """
        if not self._preset.get('loop', False):
            return list(notes)

        use_bpm = bpm or self._preset.get('default_bpm', 120)
        use_bars = bars or self._preset.get('default_bars', 4)
        mutate = mutation_rate if mutation_rate is not None else self._preset.get('loop_mutate', 0.05)

        import random

        bar_duration = 4.0 * 60.0 / use_bpm
        result = []

        for bar_idx in range(use_bars):
            offset = bar_idx * bar_duration
            for n in notes:
                nn = dict(n)
                nn['start_time'] = n['start_time'] + offset

                # Apply subtle mutation
                if mutate > 0 and random.random() < mutate:
                    # Slightly shift timing
                    shift = random.gauss(0, 0.01)  # ~10ms jitter
                    nn['start_time'] = max(0, nn['start_time'] + shift)

                if mutate > 0 and random.random() < mutate:
                    # Slightly vary velocity
                    nn['velocity'] = max(1, min(127, n['velocity'] + random.randint(-5, 5)))

                result.append(nn)

        return result

    def get_arrangement(self) -> Optional[List[str]]:
        """Return the arrangement structure for this genre, if any."""
        return self._preset.get('arrangement')

    def create_arrangement(self, bpm: int = None, bars: int = None, **kwargs):
        """Create a fully configured Arrangement for this genre.

        For techno and house, auto-applies TextureAutomation.
        For other genres, returns a plain Arrangement with genre-appropriate tracks.

        Args:
            bpm: Override genre default BPM.
            bars: Override genre default bars.
            **kwargs: Additional overrides.

        Returns:
            Arrangement instance, optionally with texture automation applied.
        """
        from .tracks import Arrangement, techno_loop, house_beat
        from .texture import TextureAutomation

        use_bpm = bpm or self._preset.get('default_bpm', 120)
        use_bars = bars or self._preset.get('default_bars', 8)
        use_key = kwargs.get('key', self._preset.get('default_key', 'C'))

        # Genre-specific presets with texture
        if self._genre_key == 'techno':
            arr = techno_loop(bpm=use_bpm, bars=use_bars)
            structure = 'build_drop' if use_bars == 16 else 'peak_time' if use_bars == 32 else 'minimal'
            tex = TextureAutomation(structure, bars=use_bars, bpm=use_bpm)
            tex.generate()
            tex.apply_to_arrangement(arr)
            arr._texture = tex  # attach for later export
            return arr

        elif self._genre_key in ('house',) or self._genre_key == 'techno' and use_bars != 16:
            arr = house_beat(bpm=use_bpm, bars=use_bars)
            structure = 'deep_house' if use_bars == 24 else 'minimal'
            tex = TextureAutomation(structure, bars=use_bars, bpm=use_bpm)
            tex.generate()
            tex.apply_to_arrangement(arr)
            arr._texture = tex
            return arr

        elif self._genre_key == 'ambient':
            arr = Arrangement(key=use_key, bpm=use_bpm, bars=use_bars)
            arr.add_track('drone', 'ella', 'free_improvisation', 'pad')
            arr.add_track('texture', 'miles', 'free_improvisation', 'synth')
            tex = TextureAutomation('ambient_drone', bars=use_bars, bpm=use_bpm)
            tex.generate()
            tex.apply_to_arrangement(arr)
            arr._texture = tex
            return arr

        else:
            # Generic arrangement — no texture automation
            arr = Arrangement(key=use_key, bpm=use_bpm, bars=use_bars)
            return arr

    def summary(self) -> str:
        """Return a human-readable summary of this genre configuration."""
        p = self._preset
        lines = [
            f"Genre: {self._genre_key}",
            f"  {p.get('description', '')}",
            f"  Mode: {p['default_mode']} | Terrain: {p['default_terrain']}",
            f"  Key: {p.get('default_key', 'C')} | BPM: {p.get('default_bpm', 120)} | Bars: {p.get('default_bars', 4)}",
            f"  Grid: {p.get('grid', 'none (rubato)')} | Loop: {p.get('loop', False)}",
        ]

        weights = p.get('diagnostic_weights', {})
        if weights:
            ordered = sorted(weights.items(), key=lambda x: -x[1])
            top = ordered[0]
            lines.append(f"  Top diagnostic: {top[0]} ({top[1]:.0%})")

        if p.get('arrangement'):
            lines.append(f"  Arrangement: {' → '.join(p['arrangement'])}")

        return '\n'.join(lines)

    def __repr__(self) -> str:
        return f"GenreBrain(genre={self._genre_key!r})"


# ── Convenience ──────────────────────────────────────────────────────

def list_genres() -> list:
    """Return all available genre names (canonical + aliases)."""
    canonical = list(GenreBrain.PRESETS.keys())
    aliases = list(GenreBrain.ALIASES.keys())
    return sorted(set(canonical + aliases))


def genre_summary_table() -> str:
    """Return a formatted table of all genres."""
    lines = [f"{'Genre':<15} {'Mode':<12} {'Terrain':<25} {'Grid':<8} {'Loop'}",
             "─" * 70]

    for name, p in GenreBrain.PRESETS.items():
        grid = str(p.get('grid', 'none'))
        loop = str(p.get('loop', False))
        lines.append(
            f"{name:<15} {p['default_mode']:<12} {p['default_terrain']:<25} {grid:<8} {loop}"
        )

    return '\n'.join(lines)
