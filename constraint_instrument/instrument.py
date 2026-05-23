"""
The Instrument — the primary API surface.

A violinist doesn't think "I need to place my finger at 659.25Hz."
They hear the note and their hand goes there. The instrument disappears.
Our API must work the same way.
"""

import random
from typing import Dict, List, Optional, Union

from .terrain import Terrain, TERRAINS
from .parker import ParkerEngine
from .miles import MilesEngine
from .ellington import EllingtonEngine, Chart
from .basie import BasieEngine, JamSession
from .goodman import GoodmanEngine, DiagnosticReport
from .armstrong import ArmstrongEngine
from .ella import EllaEngine


# ── MIDI Rendering ───────────────────────────────────────────────────

def _render_to_midi(notes: List[dict], bpm: int = 120, filepath: str = "output.mid") -> str:
    """Render notes to a MIDI file. Returns filepath."""
    try:
        import mido
        from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo

        mid = MidiFile(ticks_per_beat=480)
        track = MidiTrack()
        mid.tracks.append(track)

        # Tempo
        track.append(MetaMessage('set_tempo', tempo=bpm2tempo(bpm), time=0))

        ppq = 480
        ticks_per_second = ppq * bpm / 60.0

        # Sort notes by start time
        sorted_notes = sorted(notes, key=lambda n: n["start"])

        # Convert to events
        events = []
        for n in sorted_notes:
            start_tick = int(n["start"] * ticks_per_second)
            dur_ticks = int(n["duration"] * ticks_per_second)
            events.append(("on", start_tick, n["pitch"], n["velocity"]))
            events.append(("off", start_tick + dur_ticks, n["pitch"], 0))

        # Sort events by tick, note_off before note_on at same tick
        events.sort(key=lambda e: (e[1], 0 if e[0] == "off" else 1))

        current_tick = 0
        for event_type, tick, pitch, velocity in events:
            delta = tick - current_tick
            track.append(Message(
                'note_on' if event_type == "on" else 'note_off',
                note=max(0, min(127, pitch)),
                velocity=velocity,
                time=max(0, delta),
            ))
            current_tick = tick

        mid.save(filepath)
        return filepath
    except ImportError:
        # Fallback: save as JSON
        import json
        json_path = filepath.replace(".mid", ".json")
        with open(json_path, "w") as f:
            json.dump({"notes": notes, "bpm": bpm}, f, indent=2)
        return json_path


def _render_to_wav(notes: List[dict], bpm: int = 120, filepath: str = "output.wav",
                   sample_rate: int = 44100) -> str:
    """Render notes to a WAV file using sine wave synthesis. Returns filepath."""
    import struct
    import math

    duration = 0
    for n in notes:
        end = n["start"] + n["duration"]
        if end > duration:
            duration = end
    duration += 1.0  # padding

    num_samples = int(duration * sample_rate)
    samples = [0.0] * num_samples

    for n in notes:
        freq = 440.0 * (2.0 ** ((n["pitch"] - 69) / 12.0))
        amp = (n["velocity"] / 127.0) * 0.3
        start_sample = int(n["start"] * sample_rate)
        dur_samples = int(n["duration"] * sample_rate)

        for i in range(dur_samples):
            idx = start_sample + i
            if idx >= num_samples:
                break
            # Envelope: quick attack, sustain, quick release
            env = 1.0
            attack = min(1.0, i / (0.01 * sample_rate))
            release = min(1.0, (dur_samples - i) / (0.05 * sample_rate))
            env = attack * release

            t = i / sample_rate
            # Sine + slight harmonics for warmth
            val = math.sin(2 * math.pi * freq * t) * 0.7
            val += math.sin(2 * math.pi * freq * 2 * t) * 0.2
            val += math.sin(2 * math.pi * freq * 3 * t) * 0.1

            samples[idx] += val * amp * env

    # Normalize
    peak = max(abs(s) for s in samples) if samples else 1.0
    if peak > 0:
        samples = [s / peak * 0.8 for s in samples]

    # Write WAV
    with open(filepath, 'wb') as f:
        # RIFF header
        data_size = num_samples * 2  # 16-bit
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + data_size))
        f.write(b'WAVE')
        # fmt chunk
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))  # chunk size
        f.write(struct.pack('<H', 1))   # PCM
        f.write(struct.pack('<H', 1))   # mono
        f.write(struct.pack('<I', sample_rate))
        f.write(struct.pack('<I', sample_rate * 2))  # byte rate
        f.write(struct.pack('<H', 2))   # block align
        f.write(struct.pack('<H', 16))  # bits per sample
        # data chunk
        f.write(b'data')
        f.write(struct.pack('<I', data_size))
        for s in samples:
            val = max(-32768, min(32767, int(s * 32767)))
            f.write(struct.pack('<h', val))

    return filepath


class Instrument:
    """
    The constraint-music instrument.
    
    Create it like you'd pick up an instrument — choose your mode,
    your voice, and the terrain you want to explore.
    
    Usage:
        inst = Instrument(mode="miles", voice="piano", terrain="blues")
        solo = inst.perform(minutes=2)
        inst.render("solo.wav")
    """

    MODES = ("parker", "miles", "ellington", "basie", "goodman", "armstrong", "ella")
    VOICES = ("piano", "sax", "drums", "voice", "guitar", "orchestra", "bass", "trumpet")

    def __init__(self, mode: str = "ella", voice: str = "piano",
                 terrain: str = "blues", key: int = 60):
        if mode not in self.MODES:
            raise ValueError(f"Unknown mode '{mode}'. Choose from: {', '.join(self.MODES)}")
        if terrain not in TERRAINS:
            raise ValueError(f"Unknown terrain '{terrain}'. Choose from: {', '.join(TERRAINS.keys())}")

        self.mode = mode
        self.voice = voice
        self.terrain_name = terrain
        self._terrain = TERRAINS[terrain]
        self._key = key
        self._last_performance: Optional[dict] = None

        # Initialize the appropriate engine
        self._engine = self._create_engine(mode)

    def _create_engine(self, mode: str):
        """Create the mode-specific engine."""
        engines = {
            "parker": lambda: ParkerEngine(self._terrain, self._key),
            "miles": lambda: MilesEngine(self._terrain, self._key),
            "ellington": lambda: EllingtonEngine(self._terrain, self._key),
            "basie": lambda: BasieEngine(self._terrain, self._key),
            "goodman": lambda: GoodmanEngine(self._terrain, self._key),
            "armstrong": lambda: ArmstrongEngine(self._terrain, self._key),
            "ella": lambda: EllaEngine(self._terrain, self._key),
        }
        return engines[mode]()

    # ── Parker Mode Methods ──────────────────────────────────────────

    def practice(self, **kwargs) -> list:
        """Practice mode (Parker). Build muscle memory for constraint navigation."""
        assert self.mode == "parker", "practice() is only available in Parker mode"
        return self._engine.practice(**kwargs)

    def feel_trajectory(self, progression: str, **kwargs) -> object:
        """Feel a trajectory through pitch space (Parker)."""
        assert self.mode == "parker", "feel_trajectory() is only available in Parker mode"
        return self._engine.feel_trajectory(progression, **kwargs)

    # ── Miles Mode Methods ───────────────────────────────────────────

    def frontier(self, n: int = 5) -> list:
        """Find unexplored regions (Miles)."""
        assert self.mode == "miles", "frontier() is only available in Miles mode"
        return self._engine.frontier(n)

    def originality(self, last_n: int = 10) -> dict:
        """Check if you're repeating yourself (Miles)."""
        assert self.mode == "miles", "originality() is only available in Miles mode"
        return self._engine.originality(last_n)

    # ── Ellington Mode Methods ───────────────────────────────────────

    def compose(self, sections: list, constraints: list, **kwargs) -> Chart:
        """Compose a framework (Ellington)."""
        assert self.mode == "ellington", "compose() is only available in Ellington mode"
        return self._engine.compose(sections, constraints, **kwargs)

    # ── Basie Mode Methods ───────────────────────────────────────────

    def join_jam(self, **kwargs) -> JamSession:
        """Join a jam session (Basie)."""
        assert self.mode == "basie", "join_jam() is only available in Basie mode"
        return self._engine.join_jam(**kwargs)

    # ── Goodman Mode Methods ─────────────────────────────────────────

    def diagnose(self, source=None) -> DiagnosticReport:
        """
        Diagnose what's missing (Goodman).
        source can be a list of notes or a filepath to a MIDI file.
        """
        assert self.mode == "goodman", "diagnose() is only available in Goodman mode"
        if isinstance(source, str):
            return self._engine.diagnose_midi_file(source)
        elif isinstance(source, list):
            return self._engine.diagnose(source)
        elif self._last_performance and "notes" in self._last_performance:
            return self._engine.diagnose(self._last_performance["notes"])
        else:
            raise ValueError("Provide notes or a MIDI filepath to diagnose()")

    def prescribe(self, missing_order: int, **kwargs):
        """Get exercises for a missing order (Goodman)."""
        assert self.mode == "goodman", "prescribe() is only available in Goodman mode"
        return self._engine.prescribe(missing_order, **kwargs)

    # ── Armstrong Mode Methods ───────────────────────────────────────

    def load(self, song: str) -> None:
        """Load a song as starting point (Armstrong)."""
        assert self.mode == "armstrong", "load() is only available in Armstrong mode"
        self._engine.load(song)

    def remove_constraint(self, name: str) -> bool:
        """Remove a constraint layer (Armstrong)."""
        assert self.mode == "armstrong", "remove_constraint() is only available in Armstrong mode"
        return self._engine.remove_constraint(name)

    def keep_constraint(self, name: str) -> bool:
        """Keep a specific constraint (Armstrong)."""
        assert self.mode == "armstrong", "keep_constraint() is only available in Armstrong mode"
        return self._engine.keep_constraint(name)

    # ── Universal Methods ────────────────────────────────────────────

    def perform(self, **kwargs) -> dict:
        """
        Perform. All modes support this, with mode-specific behavior.
        
        Parker: perform internalized vocabulary
        Miles: explore the frontier
        Ellington: render a chart (pass chart=)
        Basie: play in a jam session (pass session=)
        Goodman: N/A — use diagnose instead
        Armstrong: perform with removed constraints
        Ella: pure flow, no parameters
        """
        if self.mode == "parker":
            result = self._engine.perform(**kwargs)
        elif self.mode == "miles":
            result = self._engine.perform(**kwargs)
        elif self.mode == "ellington":
            chart = kwargs.pop("chart", None)
            if chart is None:
                raise ValueError("Ellington mode perform() requires chart= (use compose() first)")
            result = self._engine.render(chart, **kwargs)
        elif self.mode == "basie":
            session = kwargs.pop("session", None)
            if session is None:
                raise ValueError("Basie mode perform() requires session= (use join_jam() first)")
            result = session.play(**kwargs)
        elif self.mode == "goodman":
            raise ValueError("Goodman mode doesn't perform — use diagnose() instead")
        elif self.mode == "armstrong":
            result = self._engine.perform(**kwargs)
        elif self.mode == "ella":
            result = self._engine.perform(**kwargs)
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

        self._last_performance = result
        return result

    def render(self, filepath: str = "output.wav", bpm: Optional[int] = None) -> str:
        """
        Render the last performance to a file.
        
        Supports:
        - .wav — audio synthesis (sine waves, always available)
        - .mid — MIDI file (requires mido package)
        """
        if self._last_performance is None:
            raise ValueError("No performance to render. Call perform() first.")

        notes = self._last_performance.get("notes", [])
        render_bpm = bpm or self._last_performance.get("tempo", 120)

        if filepath.endswith(".mid"):
            return _render_to_midi(notes, render_bpm, filepath)
        elif filepath.endswith(".wav"):
            return _render_to_wav(notes, render_bpm, filepath)
        else:
            raise ValueError("Unsupported format. Use .wav or .mid")

    @property
    def info(self) -> dict:
        """Get instrument info."""
        return {
            "mode": self.mode,
            "voice": self.voice,
            "terrain": self.terrain_name,
            "key": self._key,
            "has_performance": self._last_performance is not None,
        }

    def __repr__(self) -> str:
        return f"Instrument(mode={self.mode!r}, voice={self.voice!r}, terrain={self.terrain_name!r})"
