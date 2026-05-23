"""
The Instrument — the primary API surface.

A violinist doesn't think "I need to place my finger at 659.25Hz."
They hear the note and their hand goes there. The instrument disappears.
Our API must work the same way.

Usage:
    inst = Instrument(mode='parker', terrain='delta_blues', key='E', bpm=120, bars=8)
    notes = inst.perform()           # returns list of note dicts
    inst.play()                      # plays through speakers
    inst.render('output.wav')        # saves to file
    inst.to_midi('output.mid')       # saves MIDI
    inst.diagnose()                  # diagnoses its own output
"""

import random
import struct
import math
import os
import sys
from typing import Dict, List, Optional, Union

from .terrain import Terrain, TERRAINS
from .parker import ParkerEngine
from .miles import MilesEngine
from .ellington import EllingtonEngine, Chart
from .basie import BasieEngine, JamSession
from .goodman import GoodmanEngine, DiagnosticReport
from .armstrong import ArmstrongEngine
from .ella import EllaEngine
from .seed_manager import SeedManager


# ── Key Resolution ───────────────────────────────────────────────────

NOTE_TO_MIDI = {
    'C': 60, 'C#': 61, 'Db': 61,
    'D': 62, 'D#': 63, 'Eb': 63,
    'E': 64,
    'F': 65, 'F#': 66, 'Gb': 66,
    'G': 67, 'G#': 68, 'Ab': 68,
    'A': 69, 'A#': 70, 'Bb': 70,
    'B': 71,
}

# Terrain aliases — musician-friendly names map to internal names
TERRAIN_ALIASES = {
    'blues': 'blues',
    'delta_blues': 'delta_blues',
    'delta': 'delta_blues',
    'bebop': 'bebop',
    'modal': 'modal',
    'modal_jazz': 'modal_jazz',
    'classical': 'classical',
    'classical_counterpoint': 'classical_counterpoint',
    'counterpoint': 'classical_counterpoint',
    'free_jazz': 'free_jazz',
    'free': 'free_jazz',
    'free_improvisation': 'free_improvisation',
    'bluegrass': 'bluegrass',
    'hip_hop': 'hip_hop_trap',
    'hip_hop_trap': 'hip_hop_trap',
    'trap': 'hip_hop_trap',
    'afro_cuban': 'afro_cuban',
    'latin': 'afro_cuban',
    'indian_raga': 'indian_raga',
    'raga': 'indian_raga',
    'chinese_silk_bamboo': 'chinese_silk_bamboo',
    'silk_bamboo': 'chinese_silk_bamboo',
    'electronic': 'electronic_techno',
    'electronic_techno': 'electronic_techno',
    'techno': 'electronic_techno',
    'gospel': 'gospel',
    'bebop_rich': 'bebop_rich',
}


def resolve_key(key) -> int:
    """Resolve a key specification to a MIDI note number.
    
    Accepts:
        str: 'C', 'Eb', 'F#'
        int: MIDI note number (passed through)
    """
    if isinstance(key, int):
        return key
    if isinstance(key, str):
        k = key.strip().capitalize()
        # Handle flats/sharps: 'eb' -> 'Eb', 'f#' -> 'F#'
        if len(key.strip()) >= 2:
            raw = key.strip()
            letter = raw[0].upper()
            accidental = raw[1:].lower()
            k = letter + accidental
        if k in NOTE_TO_MIDI:
            return NOTE_TO_MIDI[k]
        raise ValueError(
            f"Unknown key '{key}'. Use: {', '.join(sorted(set(NOTE_TO_MIDI.values())))} "
            f"or note names like C, Db, D, Eb, E, F, F#, G, Ab, A, Bb, B"
        )
    raise TypeError(f"key must be str or int, got {type(key).__name__}")


def resolve_terrain(name: str) -> str:
    """Resolve a terrain name (with aliases) to the internal TERRAINS key."""
    lookup = name.strip().lower()
    if lookup in TERRAIN_ALIASES:
        resolved = TERRAIN_ALIASES[lookup]
        if resolved in TERRAINS:
            return resolved
    if lookup in TERRAINS:
        return lookup
    available = sorted(set(list(TERRAINS.keys()) + list(TERRAIN_ALIASES.keys())))
    raise ValueError(f"Unknown terrain '{name}'. Available: {', '.join(available)}")


# ── Audio Playback ───────────────────────────────────────────────────

def _play_wav(filepath: str) -> bool:
    """Try to play a WAV file through speakers. Returns True if successful."""
    # Try pygame
    try:
        import pygame
        pygame.mixer.init(frequency=44100, size=-16, channels=1)
        sound = pygame.mixer.Sound(filepath)
        sound.play()
        # Wait for playback to finish
        import time
        time.sleep(sound.get_length())
        pygame.mixer.quit()
        return True
    except Exception:
        pass

    # Try simpleaudio
    try:
        import simpleaudio
        wave_obj = simpleaudio.WaveObject.from_wave_file(filepath)
        play_obj = wave_obj.play()
        play_obj.wait_done()
        return True
    except Exception:
        pass

    # Try aplay (Linux)
    try:
        result = os.system(f"aplay -q '{filepath}' 2>/dev/null")
        if result == 0:
            return True
    except Exception:
        pass

    # Try afplay (macOS)
    try:
        result = os.system(f"afplay '{filepath}' 2>/dev/null")
        if result == 0:
            return True
    except Exception:
        pass

    return False


# ── WAV Rendering ────────────────────────────────────────────────────

def _render_to_wav(notes: List[dict], bpm: int = 120, filepath: str = "output.wav",
                   sample_rate: int = 44100) -> str:
    """Render notes to a WAV file using sine wave synthesis. Returns filepath."""
    if not notes:
        # Write a tiny silent WAV
        with open(filepath, 'wb') as f:
            f.write(b'RIFF' + struct.pack('<I', 36 + 0) + b'WAVE')
            f.write(b'fmt ' + struct.pack('<IHHIIHH', 16, 1, 1, sample_rate, sample_rate * 2, 2, 16))
            f.write(b'data' + struct.pack('<I', 0))
        return filepath

    duration = 0
    for n in notes:
        end = n["start_time"] + n["duration"]
        if end > duration:
            duration = end
    duration += 0.5  # padding

    num_samples = int(duration * sample_rate)
    samples = [0.0] * num_samples

    for n in notes:
        freq = 440.0 * (2.0 ** ((n["pitch"] - 69) / 12.0))
        amp = (n["velocity"] / 127.0) * 0.3
        start_sample = int(n["start_time"] * sample_rate)
        dur_samples = int(n["duration"] * sample_rate)

        for i in range(dur_samples):
            idx = start_sample + i
            if idx >= num_samples:
                break
            # Envelope: quick attack, sustain, quick release
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
        data_size = num_samples * 2
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + data_size))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<IHHIIHH', 16, 1, 1, sample_rate, sample_rate * 2, 2, 16))
        f.write(b'data')
        f.write(struct.pack('<I', data_size))
        for s in samples:
            val = max(-32768, min(32767, int(s * 32767)))
            f.write(struct.pack('<h', val))

    return filepath


def _render_to_midi(notes: List[dict], bpm: int = 120, filepath: str = "output.mid") -> str:
    """Render notes to a MIDI file. Returns filepath."""
    try:
        from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
    except ImportError:
        raise ImportError("Install mido for MIDI support: pip install mido")

    mid = MidiFile(ticks_per_beat=480)
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(MetaMessage('set_tempo', tempo=bpm2tempo(bpm), time=0))

    ppq = 480
    ticks_per_second = ppq * bpm / 60.0

    sorted_notes = sorted(notes, key=lambda n: n["start_time"])

    events = []
    for n in sorted_notes:
        start_tick = int(n["start_time"] * ticks_per_second)
        dur_ticks = int(n["duration"] * ticks_per_second)
        events.append(("on", start_tick, n["pitch"], n["velocity"]))
        events.append(("off", start_tick + dur_ticks, n["pitch"], 0))

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


# ── Note Normalization ───────────────────────────────────────────────

def _normalize_notes(notes: list, bpm: int = 120, bars: int = 4, key: int = 60) -> List[dict]:
    """Normalize note dicts from any engine into the canonical format.
    
    Ensures every note has: pitch (int), velocity (int), start_time (float), duration (float).
    Handles engines that use 'start' instead of 'start_time'.
    Clamps performance to requested bars if specified.
    """
    normalized = []
    for n in notes:
        if not isinstance(n, dict):
            continue
        # Handle 'start' -> 'start_time'
        start = n.get("start_time", n.get("start", 0.0))
        duration = n.get("duration", 0.25)
        pitch = n.get("pitch", key)
        velocity = n.get("velocity", 80)

        normalized.append({
            "pitch": int(max(0, min(127, pitch))),
            "velocity": int(max(1, min(127, velocity))),
            "start_time": float(start),
            "duration": float(max(0.01, duration)),
        })

    # Clamp to bars if we have bpm
    if bpm and bars:
        bar_duration = 4.0 * 60.0 / bpm  # 4 beats per bar
        max_time = bars * bar_duration
        normalized = [n for n in normalized if n["start_time"] < max_time]

    return normalized


class Instrument:
    """
    The constraint-music instrument.
    
    Create it like you'd pick up an instrument — choose your mode,
    your terrain, and your key.
    
    Usage:
        inst = Instrument(mode='parker', terrain='delta_blues', key='E', bpm=120, bars=8)
        notes = inst.perform()           # returns list of note dicts
        inst.play()                      # plays through speakers
        inst.render('output.wav')        # saves to file
        inst.to_midi('output.mid')       # saves MIDI
        inst.diagnose()                  # diagnoses its own output
    """

    MODES = ("parker", "miles", "ellington", "basie", "goodman", "armstrong", "ella")

    def __init__(self, mode: str = "ella", terrain: str = "blues",
                 key = 'C', bpm: int = 100, bars: int = 4, seed = None):
        """
        Create an Instrument.
        
        Args:
            mode: Performance mode. One of: parker, miles, ellington, basie, goodman, armstrong, ella
            terrain: Musical terrain/landscape. Names like 'blues', 'bebop', 'delta_blues', 'modal_jazz', etc.
            key: Musical key — a note name like 'C', 'Eb', 'F#' or a MIDI note number (default: 60 = C4)
            bpm: Tempo in beats per minute (default: 100)
            bars: Number of bars to generate (default: 4)
            seed: Master seed for deterministic reproducibility (None = non-deterministic)
        """
        mode = mode.lower().strip()
        if mode not in self.MODES:
            raise ValueError(f"Unknown mode '{mode}'. Choose from: {', '.join(self.MODES)}")

        self.terrain_name_raw = terrain
        terrain_key = resolve_terrain(terrain)

        if terrain_key not in TERRAINS:
            raise ValueError(f"Unknown terrain '{terrain}'. Available: {', '.join(sorted(TERRAINS.keys()))}")

        self.mode = mode
        self.terrain_name = terrain_key
        self._terrain = TERRAINS[terrain_key]
        self._key = resolve_key(key)
        if bars < 1:
            raise ValueError("bars must be >= 1")
        self.bpm = int(bpm)
        self.bars = int(bars)
        self._last_notes: Optional[List[dict]] = None

        # Seed manager for deterministic reproducibility
        self._seed_manager = SeedManager(master_seed=seed) if seed is not None else None

        # Initialize the appropriate engine
        self._engine = self._create_engine(mode)

    def _create_engine(self, mode: str):
        """Create the mode-specific engine."""
        engines = {
            "parker": lambda: ParkerEngine(self._terrain, self._key),
            "miles": lambda: MilesEngine(self._terrain, self._key),
            "ellington": lambda: EllingtonEngine(self._terrain, self._key),
            "basie": lambda: BasieEngine(self._terrain, self._key),
            "goodman": lambda: GoodmanEngine(terrain=self._terrain, key=self._key),
            "armstrong": lambda: ArmstrongEngine(self._terrain, self._key),
            "ella": lambda: EllaEngine(self._terrain, self._key),
        }
        return engines[mode]()

    def perform(self, bars: Optional[int] = None, bpm: Optional[int] = None,
                **kwargs) -> List[dict]:
        """
        Perform! Returns a list of note dicts.
        
        Each note: {'pitch': int, 'velocity': int, 'start_time': float, 'duration': float}
        
        Args:
            bars: Override the number of bars (default: use constructor value)
            bpm: Override the tempo (default: use constructor value)
            **kwargs: Passed to the mode-specific engine
        """
        use_bars = bars or self.bars
        use_bpm = bpm or self.bpm

        # Seed global random for determinism if seed was provided
        if self._seed_manager is not None:
            self._seed_manager.seed_global('perform')

        # Ella ignores bars/bpm — it flows on its own
        if self.mode == "ella":
            result = self._engine.perform(**kwargs)
            raw_notes = result.get("notes", [])
        elif self.mode == "parker":
            result = self._engine.perform(**kwargs)
            raw_notes = result.get("notes", [])
        elif self.mode == "miles":
            result = self._engine.perform(**kwargs)
            raw_notes = result.get("notes", [])
        elif self.mode == "armstrong":
            result = self._engine.perform(**kwargs)
            raw_notes = result.get("notes", [])
        elif self.mode == "ellington":
            # Ellington needs a chart — auto-compose one
            chart = kwargs.pop("chart", None)
            if chart is None:
                sections = ["A", "A", "B", "A"]
                constraints = [
                    {"type": "scale_adherence", "strictness": 0.8},
                    {"type": "rhythmic_density", "density": 0.5},
                ]
                chart = self._engine.compose(sections, constraints)
            result = self._engine.render(chart, bpm=use_bpm)
            raw_notes = result.get("notes", [])
        elif self.mode == "basie":
            # Basie needs a jam session — auto-create one
            session = kwargs.pop("session", None)
            if session is None:
                session = self._engine.join_jam(players=4, tempo=use_bpm)
            result = session.play(my_role="piano", bars=use_bars, **kwargs)
            notes_by_player = result.get("notes", {})
            # Flatten player-keyed dict into a single list
            if isinstance(notes_by_player, dict):
                raw_notes = []
                for player_notes in notes_by_player.values():
                    if isinstance(player_notes, list):
                        raw_notes.extend(player_notes)
            else:
                raw_notes = notes_by_player
        elif self.mode == "goodman":
            # Goodman diagnoses — but we can still generate notes for it
            # Use ella as the generator, then diagnose
            ella = EllaEngine(self._terrain, self._key)
            result = ella.perform()
            raw_notes = result.get("notes", [])
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

        # Normalize to consistent format
        notes = _normalize_notes(raw_notes, bpm=use_bpm, bars=use_bars, key=self._key)
        self._last_notes = notes
        return notes

    def play(self) -> bool:
        """
        Play the last performance through speakers.
        
        Tries: pygame -> simpleaudio -> aplay/afplay
        
        Returns True if playback succeeded, False otherwise.
        """
        if self._last_notes is None:
            self.perform()

        # Render to temp WAV, play, clean up
        import tempfile
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tmp_path = tmp.name
        tmp.close()

        try:
            _render_to_wav(self._last_notes, self.bpm, tmp_path)
            success = _play_wav(tmp_path)
            if not success:
                print("Install pygame or simpleaudio for audio playback:", file=sys.stderr)
                print("  pip install pygame", file=sys.stderr)
                print("  pip install simpleaudio", file=sys.stderr)
            return success
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    def render(self, filepath: str = "output.wav", bpm: Optional[int] = None) -> str:
        """
        Render the last performance to a file.
        
        Supports: .wav (always), .mid (requires mido package)
        """
        if self._last_notes is None:
            self.perform()

        render_bpm = bpm or self.bpm

        if filepath.endswith(".mid"):
            return _render_to_midi(self._last_notes, render_bpm, filepath)
        elif filepath.endswith(".wav"):
            return _render_to_wav(self._last_notes, render_bpm, filepath)
        else:
            # Default to WAV
            return _render_to_wav(self._last_notes, render_bpm, filepath)

    def to_midi(self, filepath: str = "output.mid", bpm: Optional[int] = None) -> str:
        """
        Export the last performance as a MIDI file.
        
        Requires: pip install mido
        """
        if self._last_notes is None:
            self.perform()
        render_bpm = bpm or self.bpm
        return _render_to_midi(self._last_notes, render_bpm, filepath)

    def diagnose(self, source=None) -> 'DiagnosticReport':
        """
        Diagnose what's in the music — what's working, what's missing.
        
        Works from any mode. If source is a filepath (str), reads a MIDI file.
        If source is a list of note dicts, diagnoses those.
        If no source, diagnoses the last performance.
        """
        # Create a Goodman engine for diagnosis
        goodman = GoodmanEngine(terrain=self._terrain, key=self._key)

        if isinstance(source, str):
            return goodman.diagnose_midi_file(source)
        elif isinstance(source, list):
            return goodman.diagnose(source)
        elif self._last_notes is not None:
            return goodman.diagnose(self._last_notes)
        else:
            # Generate first, then diagnose
            self.perform()
            return goodman.diagnose(self._last_notes)

    # ── Mode-specific methods (preserved for advanced use) ───────────

    def practice(self, **kwargs) -> list:
        """Practice mode (Parker). Build muscle memory."""
        assert self.mode == "parker", "practice() is only available in Parker mode"
        return self._engine.practice(**kwargs)

    def feel_trajectory(self, progression: str, **kwargs) -> object:
        """Feel a trajectory through pitch space (Parker)."""
        assert self.mode == "parker", "feel_trajectory() is only available in Parker mode"
        return self._engine.feel_trajectory(progression, **kwargs)

    def frontier(self, n: int = 5) -> list:
        """Find unexplored regions (Miles)."""
        assert self.mode == "miles", "frontier() is only available in Miles mode"
        return self._engine.frontier(n)

    def originality(self, last_n: int = 10) -> dict:
        """Check if you're repeating yourself (Miles)."""
        assert self.mode == "miles", "originality() is only available in Miles mode"
        return self._engine.originality(last_n)

    def compose(self, sections: list, constraints: list, **kwargs) -> Chart:
        """Compose a framework (Ellington)."""
        assert self.mode == "ellington", "compose() is only available in Ellington mode"
        return self._engine.compose(sections, constraints, **kwargs)

    def join_jam(self, **kwargs) -> JamSession:
        """Join a jam session (Basie)."""
        assert self.mode == "basie", "join_jam() is only available in Basie mode"
        return self._engine.join_jam(**kwargs)

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

    def prescribe(self, missing_order: int, **kwargs):
        """Get exercises for a missing order (Goodman)."""
        assert self.mode == "goodman", "prescribe() is only available in Goodman mode"
        return self._engine.prescribe(missing_order, **kwargs)

    # ── Info ─────────────────────────────────────────────────────────

    @property
    def info(self) -> dict:
        """Get instrument info."""
        return {
            "mode": self.mode,
            "terrain": self.terrain_name,
            "key": self._key,
            "bpm": self.bpm,
            "bars": self.bars,
            "seed": self._seed_manager.master_seed if self._seed_manager else None,
            "has_performance": self._last_notes is not None,
            "note_count": len(self._last_notes) if self._last_notes else 0,
        }

    def __repr__(self) -> str:
        seed_str = f", seed={self._seed_manager.master_seed}" if self._seed_manager else ""
        return f"Instrument(mode={self.mode!r}, terrain={self.terrain_name!r}, key={self._key}, bpm={self.bpm}, bars={self.bars}{seed_str})"
