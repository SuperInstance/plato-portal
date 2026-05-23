"""
Multi-track arrangements and looping — what producers actually need.

Electronic, hip-hop, jazz — real music has multiple instruments playing
together, and those patterns loop with variation. This module provides:

- Track: A single instrument track with its own engine, terrain, and mode
- Arrangement: Multiple tracks playing together, with looping and mutation
- Presets: trap_beat, techno_loop, jazz_combo — ready to go

Usage:
    from constraint_instrument.tracks import trap_beat
    beat = trap_beat(bpm=140, bars=8)
    beat.generate_all()
    beat.loop(times=4)          # 32 bars with variation
    beat.render('trap_beat.wav')
    beat.to_midi('trap_beat.mid')
"""

import copy
import math
import random
import struct
import os
from typing import Dict, List, Optional

from .instrument import Instrument, resolve_key, resolve_terrain, _render_to_wav, _render_to_midi
from .terrain import TERRAINS


class Track:
    """A single instrument track with its own terrain and mode.

    Each track wraps an Instrument instance and adds track-level
    features like quantization, humanization, and voice assignment.
    """

    # Voice-to-register mappings for basic timbral differentiation
    VOICE_RANGES = {
        'piano': (48, 84),
        'bass': (24, 48),
        'synth': (60, 96),
        'hat': (60, 72),       # hi-hats rendered as short high pitches
        'snare': (40, 50),     # snare-ish range
        'kick': (24, 36),      # kick/bass drum range
        'pad': (48, 72),
        'lead': (60, 96),
        'arp': (60, 96),
        'strings': (48, 84),
        'sax': (54, 78),
        'drums': (24, 60),     # general percussion
        'vox': (57, 81),
        'guitar': (40, 72),
        'organ': (48, 84),
    }

    def __init__(self, name: str, mode: str, terrain: str,
                 voice: str = 'piano', key: str = 'C', bpm: int = 120, seed = None):
        """
        Create a track.

        Args:
            name: Track name (e.g. '808', 'hihat', 'melody')
            mode: Engine mode (parker, miles, ella, armstrong, basie, ellington)
            terrain: Terrain name (hip_hop_trap, electronic_techno, blues, etc.)
            voice: Voice/instrument type for register mapping
            key: Musical key
            bpm: Tempo in BPM
            seed: Master seed for deterministic reproducibility
        """
        self.name = name
        self.mode = mode
        self.terrain = terrain
        self.voice = voice
        self.key = key
        self.bpm = bpm
        self.seed = seed
        self.notes: List[dict] = []
        self._instrument = None
        self._bars = 4

    def _get_instrument(self, bars: int = 4) -> Instrument:
        """Lazily create the underlying Instrument."""
        if self._instrument is None:
            self._instrument = Instrument(
                mode=self.mode,
                terrain=self.terrain,
                key=self.key,
                bpm=self.bpm,
                bars=bars,
                seed=self.seed,
            )
        return self._instrument

    def generate(self, bars: int = 4, key: str = None, bpm: int = None) -> List[dict]:
        """Generate notes for this track.

        Args:
            bars: Number of bars to generate
            key: Override key (default: track key)
            bpm: Override BPM (default: track BPM)

        Returns:
            List of note dicts with pitch, velocity, start_time, duration
        """
        use_bars = bars
        use_key = key or self.key
        use_bpm = bpm or self.bpm
        self._bars = use_bars

        inst = self._get_instrument(use_bars)
        inst.bpm = use_bpm
        inst._key = resolve_key(use_key)
        inst.bars = use_bars

        raw_notes = inst.perform(bars=use_bars, bpm=use_bpm)

        # Apply voice range constraints
        self.notes = self._apply_voice_range(raw_notes)
        return self.notes

    def _apply_voice_range(self, notes: List[dict]) -> List[dict]:
        """Constrain notes to the voice's register range."""
        voice_range = self.VOICE_RANGES.get(self.voice, (24, 96))
        low, high = voice_range

        result = []
        for n in notes:
            pitch = n['pitch']
            # Wrap into range using octave transposition
            while pitch < low:
                pitch += 12
            while pitch > high:
                pitch -= 12
            result.append({
                **n,
                'pitch': pitch,
                'voice': self.voice,
                'track': self.name,
            })
        return result

    def quantize(self, grid: int = 16) -> 'Track':
        """Snap note times to a rhythmic grid.

        Args:
            grid: Grid subdivision. 4=quarter, 8=eighth, 16=sixteenth, 32=thirty-second

        Returns:
            self (for chaining)
        """
        if not self.notes:
            return self

        # Duration of one grid unit in seconds
        beat_duration = 60.0 / self.bpm
        grid_duration = beat_duration * 4.0 / grid  # 4 beats per bar, subdivided

        for n in self.notes:
            # Snap start_time to nearest grid point
            grid_pos = round(n['start_time'] / grid_duration)
            n['start_time'] = grid_pos * grid_duration

            # Snap duration to grid (minimum 1 grid unit)
            dur_grids = max(1, round(n['duration'] / grid_duration))
            n['duration'] = dur_grids * grid_duration

        return self

    def humanize(self, timing_ms: float = 10, velocity_range: int = 10) -> 'Track':
        """Add slight random variation to timing and velocity.

        Args:
            timing_ms: Maximum timing offset in milliseconds (±)
            velocity_range: Maximum velocity offset (±)

        Returns:
            self (for chaining)
        """
        if not self.notes:
            return self

        timing_sec = timing_ms / 1000.0

        for n in self.notes:
            n['start_time'] += random.uniform(-timing_sec, timing_sec)
            n['velocity'] = max(1, min(127,
                n['velocity'] + random.randint(-velocity_range, velocity_range)
            ))

        return self

    def clear(self) -> 'Track':
        """Clear all generated notes."""
        self.notes = []
        return self

    @property
    def duration(self) -> float:
        """Total duration of this track in seconds."""
        if not self.notes:
            return 0.0
        return max(n['start_time'] + n['duration'] for n in self.notes)

    def __repr__(self) -> str:
        return f"Track(name={self.name!r}, mode={self.mode!r}, voice={self.voice!r}, notes={len(self.notes)})"


class Arrangement:
    """Multiple tracks playing together.

    An arrangement manages several tracks, each with its own instrument,
    mode, and terrain. Tracks can be generated together, looped with
    variation, and rendered to a single audio file or multi-track MIDI.
    """

    def __init__(self, key: str = 'C', bpm: int = 120, bars: int = 4, seed = None):
        """
        Create an arrangement.

        Args:
            key: Musical key for all tracks
            bpm: Tempo in BPM
            bars: Number of bars per generation cycle
            seed: Master seed for deterministic reproducibility
        """
        self.key = key
        self.bpm = bpm
        self.bars = bars
        self.seed = seed
        self.tracks: List[Track] = []
        self._loop_count = 1  # How many times the arrangement has been looped

    def add_track(self, name: str, mode: str, terrain: str,
                  voice: str = 'piano') -> Track:
        """Add a track to the arrangement.

        Args:
            name: Track name (e.g. '808', 'hihat', 'melody')
            mode: Engine mode (parker, miles, ella, armstrong, basie)
            terrain: Terrain name
            voice: Voice/instrument type

        Returns:
            The created Track
        """
        track = Track(
            name=name, mode=mode, terrain=terrain,
            voice=voice, key=self.key, bpm=self.bpm,
            seed=self.seed,
        )
        self.tracks.append(track)
        return track

    def generate_all(self) -> 'Arrangement':
        """Generate notes for all tracks.

        Returns:
            self (for chaining)
        """
        for track in self.tracks:
            track.generate(bars=self.bars, key=self.key, bpm=self.bpm)
        return self

    def loop(self, times: int = 4) -> 'Arrangement':
        """Repeat the arrangement N times with variation.

        Each repetition applies slight parameter drift and optional
        mutation, creating evolving loops that stay related but never
        repeat exactly.

        Args:
            times: Number of times to loop (total plays = times)

        Returns:
            self (for chaining)
        """
        if times <= 1:
            return self

        if not any(t.notes for t in self.tracks):
            self.generate_all()

        # Calculate the duration of one cycle
        bar_duration = 4.0 * 60.0 / self.bpm
        cycle_duration = self.bars * bar_duration

        # Collect the original notes from all tracks
        original_by_track = {}
        for track in self.tracks:
            original_by_track[track.name] = copy.deepcopy(track.notes)

        # Build looped notes
        for loop_idx in range(1, times):
            offset = loop_idx * cycle_duration

            # Intensity increases slightly with each loop
            drift = 0.05 * loop_idx  # Increasing drift

            for track in self.tracks:
                if track.name not in original_by_track:
                    continue
                base_notes = original_by_track[track.name]

                for n in base_notes:
                    new_note = copy.deepcopy(n)
                    new_note['start_time'] += offset

                    # Apply drift: slight timing and velocity variation
                    new_note['start_time'] += random.uniform(-0.01 * drift, 0.01 * drift)
                    new_note['velocity'] = max(1, min(127,
                        int(new_note['velocity'] + random.gauss(0, 3 * drift))
                    ))

                    # Occasional pitch drift for melodic tracks
                    if track.voice in ('synth', 'lead', 'arp', 'melody', 'piano', 'sax'):
                        if random.random() < 0.05 * drift:
                            new_note['pitch'] += random.choice([-12, -7, -5, -3, -2, 0, 2, 3, 5, 7, 12])

                    track.notes.append(new_note)

        self._loop_count = times
        return self

    def mutate(self, intensity: float = 0.3) -> 'Arrangement':
        """Mutate the arrangement in place.

        Replace some notes, change dynamics, alter pitches.
        intensity 0.0 = identical, 1.0 = completely different.

        Args:
            intensity: Mutation strength (0.0 to 1.0)

        Returns:
            self (for chaining)
        """
        for track in self.tracks:
            if not track.notes:
                continue

            mutated = []
            for n in track.notes:
                if random.random() < intensity:
                    n = copy.deepcopy(n)

                    # Choose mutation type
                    mutation = random.choice(['pitch', 'velocity', 'time', 'duration', 'replace'])

                    if mutation == 'pitch':
                        # Shift pitch by a scale degree
                        n['pitch'] += random.choice([-12, -7, -5, -3, 0, 2, 3, 5, 7, 12])
                        n['pitch'] = max(0, min(127, n['pitch']))

                    elif mutation == 'velocity':
                        # Change dynamics
                        n['velocity'] = max(1, min(127,
                            n['velocity'] + random.randint(-30, 30)
                        ))

                    elif mutation == 'time':
                        # Shift timing slightly
                        n['start_time'] += random.uniform(-0.05, 0.05)

                    elif mutation == 'duration':
                        # Change note length
                        factor = random.uniform(0.5, 2.0)
                        n['duration'] *= factor

                    elif mutation == 'replace':
                        # Replace with a new random note in voice range
                        voice_range = Track.VOICE_RANGES.get(track.voice, (36, 84))
                        n['pitch'] = random.randint(voice_range[0], voice_range[1])
                        n['velocity'] = random.randint(40, 110)
                        n['duration'] = random.uniform(0.05, 0.5)

                mutated.append(n)

            track.notes = mutated

        return self

    def quantize_all(self, grid: int = 16) -> 'Arrangement':
        """Quantize all tracks.

        Args:
            grid: Grid subdivision (4=quarter, 8=eighth, 16=sixteenth)

        Returns:
            self (for chaining)
        """
        for track in self.tracks:
            track.quantize(grid)
        return self

    def humanize_all(self, timing_ms: float = 10, velocity_range: int = 10) -> 'Arrangement':
        """Humanize all tracks.

        Args:
            timing_ms: Maximum timing offset in ms
            velocity_range: Maximum velocity offset

        Returns:
            self (for chaining)
        """
        for track in self.tracks:
            track.humanize(timing_ms, velocity_range)
        return self

    def get_all_notes(self) -> List[dict]:
        """Get all notes from all tracks, sorted by start time."""
        all_notes = []
        for track in self.tracks:
            all_notes.extend(track.notes)
        all_notes.sort(key=lambda n: n['start_time'])
        return all_notes

    @property
    def duration(self) -> float:
        """Total duration of the arrangement in seconds."""
        if not any(t.notes for t in self.tracks):
            return 0.0
        return max(
            (t.duration for t in self.tracks if t.notes),
            default=0.0,
        )

    def render(self, path: str) -> str:
        """Render all tracks to a single WAV file.

        Mixes all tracks together with proper normalization.

        Args:
            path: Output file path

        Returns:
            Path to the rendered file
        """
        all_notes = self.get_all_notes()
        if not all_notes:
            # Write a silent file
            _render_to_wav([], self.bpm, path)
            return path

        return _render_to_wav(all_notes, self.bpm, path)

    def to_midi(self, path: str) -> str:
        """Export all tracks to a multi-track MIDI file.

        Each track becomes a separate MIDI track with its own channel.

        Args:
            path: Output file path (.mid)

        Returns:
            Path to the MIDI file
        """
        try:
            from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
        except ImportError:
            raise ImportError("Install mido for MIDI support: pip install mido")

        mid = MidiFile(ticks_per_beat=480)
        ppq = 480
        ticks_per_second = ppq * self.bpm / 60.0

        # Create a tempo track
        tempo_track = MidiTrack()
        tempo_track.append(MetaMessage('set_tempo', tempo=bpm2tempo(self.bpm), time=0))
        tempo_track.append(MetaMessage('end_of_track', time=0))
        mid.tracks.append(tempo_track)

        # MIDI channel assignments for different voices
        voice_channels = {
            'piano': 0, 'bass': 1, 'synth': 2, 'hat': 9,
            'snare': 9, 'kick': 9, 'pad': 3, 'lead': 4,
            'arp': 5, 'strings': 6, 'sax': 7, 'drums': 9,
            'vox': 8, 'guitar': 10, 'organ': 11,
        }

        for track in self.tracks:
            if not track.notes:
                continue

            midi_track = MidiTrack()
            midi_track.append(MetaMessage('track_name', name=track.name, time=0))

            # Sort note on/off events
            events = []
            for n in track.notes:
                start_tick = int(n['start_time'] * ticks_per_second)
                dur_ticks = int(n['duration'] * ticks_per_second)
                events.append(("on", start_tick, n['pitch'], n['velocity']))
                events.append(("off", start_tick + dur_ticks, n['pitch'], 0))

            events.sort(key=lambda e: (e[1], 0 if e[0] == "off" else 1))

            channel = voice_channels.get(track.voice, 0)

            current_tick = 0
            for event_type, tick, pitch, velocity in events:
                delta = tick - current_tick
                midi_track.append(Message(
                    'note_on' if event_type == "on" else 'note_off',
                    note=max(0, min(127, pitch)),
                    velocity=velocity,
                    time=max(0, delta),
                    channel=channel,
                ))
                current_tick = tick

            midi_track.append(MetaMessage('end_of_track', time=0))
            mid.tracks.append(midi_track)

        mid.save(path)
        return path

    def __repr__(self) -> str:
        tracks_str = ', '.join(t.name for t in self.tracks)
        return f"Arrangement(key={self.key!r}, bpm={self.bpm}, bars={self.bars}, tracks=[{tracks_str}])"


# ══════════════════════════════════════════════════════════════════════
# PRESETS — Ready-made arrangements
# ══════════════════════════════════════════════════════════════════════

def trap_beat(bpm: int = 140, bars: int = 8, seed = None) -> Arrangement:
    """808 + hi-hats + snare + melody — the essential trap beat.

    Args:
        bpm: Tempo (default 140, felt in half-time at 70)
        bars: Bars per cycle (default 8)
        seed: Master seed for deterministic reproducibility

    Returns:
        Arrangement ready for generate_all() and loop()
    """
    arr = Arrangement(key='C', bpm=bpm, bars=bars, seed=seed)
    arr.add_track('808', 'parker', 'hip_hop_trap', 'bass')
    arr.add_track('hihat', 'basie', 'hip_hop_trap', 'hat')
    arr.add_track('snare', 'armstrong', 'hip_hop_trap', 'snare')
    arr.add_track('melody', 'miles', 'hip_hop_trap', 'synth')
    return arr


def techno_loop(bpm: int = 130, bars: int = 8, seed = None) -> Arrangement:
    """Kick + bass + pad + arp — the minimal techno builder.

    Args:
        bpm: Tempo (default 130)
        bars: Bars per cycle (default 8)
        seed: Master seed for deterministic reproducibility

    Returns:
        Arrangement ready for generate_all() and loop()
    """
    arr = Arrangement(key='C', bpm=bpm, bars=bars, seed=seed)
    arr.add_track('kick', 'parker', 'electronic_techno', 'kick')
    arr.add_track('bass', 'ella', 'electronic_techno', 'bass')
    arr.add_track('pad', 'miles', 'electronic_techno', 'pad')
    arr.add_track('arp', 'parker', 'electronic_techno', 'arp')
    return arr


def jazz_combo(bpm: int = 120, bars: int = 16, seed = None) -> Arrangement:
    """Piano + bass + drums + sax — a classic jazz quartet.

    Args:
        bpm: Tempo (default 120)
        bars: Bars per cycle (default 16)
        seed: Master seed for deterministic reproducibility

    Returns:
        Arrangement ready for generate_all() and loop()
    """
    arr = Arrangement(key='C', bpm=bpm, bars=bars, seed=seed)
    arr.add_track('piano', 'ella', 'bebop', 'piano')
    arr.add_track('bass', 'basie', 'bebop', 'bass')
    arr.add_track('drums', 'armstrong', 'bebop', 'drums')
    arr.add_track('sax', 'miles', 'bebop', 'sax')
    return arr


def lofi_beat(bpm: int = 85, bars: int = 8, seed = None) -> Arrangement:
    """Lo-fi hip hop — chill beats to study to.

    Args:
        bpm: Tempo (default 85)
        bars: Bars per cycle (default 8)
        seed: Master seed for deterministic reproducibility

    Returns:
        Arrangement ready for generate_all() and loop()
    """
    arr = Arrangement(key='C', bpm=bpm, bars=bars, seed=seed)
    arr.add_track('keys', 'ella', 'modal_jazz', 'piano')
    arr.add_track('bass', 'basie', 'modal_jazz', 'bass')
    arr.add_track('drums', 'armstrong', 'hip_hop_trap', 'drums')
    arr.add_track('pad', 'miles', 'modal_jazz', 'pad')
    return arr


def house_beat(bpm: int = 124, bars: int = 8, seed = None) -> Arrangement:
    """Four-on-the-floor house — deep and groovy.

    Args:
        bpm: Tempo (default 124)
        bars: Bars per cycle (default 8)
        seed: Master seed for deterministic reproducibility

    Returns:
        Arrangement ready for generate_all() and loop()
    """
    arr = Arrangement(key='C', bpm=bpm, bars=bars, seed=seed)
    arr.add_track('kick', 'parker', 'electronic_techno', 'kick')
    arr.add_track('hat', 'basie', 'electronic_techno', 'hat')
    arr.add_track('bass', 'ella', 'electronic_techno', 'bass')
    arr.add_track('chord', 'miles', 'electronic_techno', 'synth')
    return arr
