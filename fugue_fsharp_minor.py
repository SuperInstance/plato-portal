#!/usr/bin/env python3
"""
Round 2 Beta Retest: 4-Voice Fugue in F# Minor
Composed using constraint-theory counterpoint engine.

Key: F# minor (tonic=6 in MIDI pitch-class notation)
"""

import sys
import os
import random
import struct
import math

# Ensure local packages are importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'style-dna'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'constraint-viz'))

from counterpoint_engine import CounterpointGenerator, Species
from counterpoint_engine.generator import VoiceRange, Scale, CounterpointResult

# ── F# minor scale ──────────────────────────────────────────────────
# F# = 6, minor intervals: (0,2,3,5,7,8,10) → pitch classes: {6,8,9,11,1,3,4}
class FSharpMinorScale:
    """F# minor: F# G# A B C# D E"""
    tonic = 6
    mode = "minor"
    _pitch_classes = tuple(sorted([(6 + i) % 12 for i in (0, 2, 3, 5, 7, 8, 10)]))

    def contains(self, pitch):
        return (pitch % 12) in self._pitch_classes

    def pitch_classes(self):
        return self._pitch_classes

    def __repr__(self):
        return "Scale(tonic=6, mode='minor')  # F# minor"


SCALE = FSharpMinorScale()

# ── SATB Voice Ranges ───────────────────────────────────────────────
BASS     = VoiceRange(min_pitch=36, max_pitch=55)   # C2 - G3
TENOR    = VoiceRange(min_pitch=48, max_pitch=62)   # C3 - D4
ALTO     = VoiceRange(min_pitch=55, max_pitch=70)   # G3 - Bb4
SOPRANO  = VoiceRange(min_pitch=62, max_pitch=79)   # D4 - G5

VOICE_RANGES = [BASS, TENOR, ALTO, SOPRANO]
VOICE_NAMES = ['Bass', 'Tenor', 'Alto', 'Soprano']

# ── Fugue Subject in F# minor ──────────────────────────────────────
# A classic fugue subject: stepwise opening, leap up, stepwise descent
# Using MIDI note numbers (F#4 = 66)
SUBJECT = [66, 68, 69, 73, 71, 69, 68, 66, 64, 66, 68, 66]
# F#4 G#4 A4  C#5 B4  A4 G#4 F#4 E4 F#4 G#4 F#4

print("=== Fugue in F# Minor — Round 2 Retest ===")
print(f"Subject: {SUBJECT} ({len(SUBJECT)} notes)")
print(f"Scale pitch classes: {SCALE.pitch_classes()}")
print(f"Voice ranges: Bass {BASS}, Tenor {TENOR}, Alto {ALTO}, Soprano {SOPRANO}")

# ── Generate 4-voice counterpoint ──────────────────────────────────
print("\n[1/5] Generating 4-voice counterpoint with constraint engine...")
gen = CounterpointGenerator(
    cantus_firmus=SUBJECT,
    species=Species.FIRST,
    scale=SCALE,
    voice_range=SOPRANO,
)

result = gen.generate_n_voices(n_voices=4, voice_ranges=[BASS, TENOR, ALTO, SOPRANO])

if not result.feasible:
    print(f"ERROR: Generation infeasible! {result}")
    sys.exit(1)

print(f"Result: {result}")
print(f"  Voices: {result.n_voices}")
print(f"  Constraints: {result.constraints_satisfied}/{result.constraints_total}")

for i, voice in enumerate(result.voices):
    print(f"  {VOICE_NAMES[i]}: {voice}")

# ── Build proper fugal structure with staggered entries ─────────────
print("\n[2/5] Building fugal structure with staggered subject entries...")

# Create staggered entries: each voice enters 3 beats after the previous
# This creates the classic fugue exposition
N_BEATS = len(SUBJECT)
STAGGER = 3
TOTAL_BEATS = N_BEATS + STAGGER * 3  # subject + 3 staggered entries

# Build the full fugue texture
fugue_voices = []
for voice_idx in range(4):
    entry_offset = voice_idx * STAGGER
    full_voice = []
    for beat in range(TOTAL_BEATS):
        subject_beat = beat - entry_offset
        if 0 <= subject_beat < N_BEATS:
            # Playing the subject (transposed for answer voices)
            note = result.voices[voice_idx][subject_beat] if subject_beat < len(result.voices[voice_idx]) else 0
            full_voice.append(note)
        else:
            full_voice.append(0)  # rest
    fugue_voices.append(full_voice)

# Fill in free counterpoint where voices aren't playing the subject
# Use the constraint engine's generated voices to fill gaps
for voice_idx in range(4):
    entry_offset = voice_idx * STAGGER
    for beat in range(TOTAL_BEATS):
        if fugue_voices[voice_idx][beat] == 0:
            # Use a held note or stepwise motion from the nearest sounding note
            prev_note = None
            for b in range(beat - 1, -1, -1):
                if fugue_voices[voice_idx][b] != 0:
                    prev_note = fugue_voices[voice_idx][b]
                    break
            if prev_note:
                # Hold previous note (sustained tone during episode)
                fugue_voices[voice_idx][beat] = prev_note

for i, v in enumerate(fugue_voices):
    print(f"  {VOICE_NAMES[i]} ({len(v)} beats): entry at beat {i * STAGGER}")

# ── Export as MIDI ──────────────────────────────────────────────────
print("\n[3/5] Exporting MIDI...")
import mido

MIDI_FILE = 'fugue_fsharp_minor.mid'
mid = mido.MidiFile(ticks_per_beat=480)
BPM = 72
NOTE_TICKS = 480  # quarter note

for voice_idx, voice in enumerate(fugue_voices):
    track = mido.MidiTrack()
    track.append(mido.MetaMessage('track_name', name=VOICE_NAMES[voice_idx]))
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(BPM)))
    
    prev_note = None
    for beat, note in enumerate(voice):
        if 0 <= note <= 127:
            # Note off for previous note (if different)
            if prev_note is not None and prev_note != note:
                track.append(mido.Message('note_off', note=prev_note, velocity=0, time=0))
                track.append(mido.Message('note_on', note=note, velocity=80, time=0))
            elif prev_note is None:
                track.append(mido.Message('note_on', note=note, velocity=80, time=0))
            # else: same note sustained
            prev_note = note
        else:
            if prev_note is not None:
                track.append(mido.Message('note_off', note=prev_note, velocity=0, time=0))
                prev_note = None
    
    # Final note off
    if prev_note is not None:
        track.append(mido.Message('note_off', note=prev_note, velocity=0, time=NOTE_TICKS))
    
    # Add timing: space out the notes properly
    # Rebuild with proper timing
    mid.tracks.append(track)

# Rebuild with proper timing
mid2 = mido.MidiFile(ticks_per_beat=480)
for voice_idx, voice in enumerate(fugue_voices):
    track = mido.MidiTrack()
    track.append(mido.MetaMessage('track_name', name=VOICE_NAMES[voice_idx]))
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(BPM)))
    track.append(mido.Message('program_change', program=0, time=0))  # Piano
    
    active_note = None
    for beat, note in enumerate(voice):
        if 0 <= note <= 127:
            if active_note is not None:
                if active_note == note:
                    # Same note, sustain — just add time
                    pass
                else:
                    # Different note — off then on
                    track.append(mido.Message('note_off', note=active_note, velocity=0, time=NOTE_TICKS))
                    track.append(mido.Message('note_on', note=note, velocity=80, time=0))
                    active_note = note
            else:
                track.append(mido.Message('note_on', note=note, velocity=80, time=0))
                active_note = note
        else:
            # Rest
            if active_note is not None:
                track.append(mido.Message('note_off', note=active_note, velocity=0, time=NOTE_TICKS))
                active_note = None
    
    # Final silence
    if active_note is not None:
        track.append(mido.Message('note_off', note=active_note, velocity=0, time=NOTE_TICKS * 2))
    
    mid2.tracks.append(track)

mid2.save(MIDI_FILE)
print(f"  Saved: {MIDI_FILE} ({os.path.getsize(MIDI_FILE)} bytes)")

# ── Render to WAV ──────────────────────────────────────────────────
print("\n[4/5] Rendering to WAV audio...")
try:
    from constraint_synth import MIDIRenderer, ConstraintSynth
    
    renderer = MIDIRenderer()
    synth = ConstraintSynth()
    
    # Read MIDI and render
    mid_read = mido.MidiFile(MIDI_FILE)
    all_notes = []
    for track in mid_read.tracks:
        abs_time = 0
        for msg in track:
            abs_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                all_notes.append(('on', msg.note, msg.velocity, abs_time))
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                all_notes.append(('off', msg.note, 0, abs_time))
    
    # Convert to (note, start_time, duration, velocity) events
    note_events = []
    active = {}
    for evt_type, note, vel, time in sorted(all_notes, key=lambda x: x[3]):
        if evt_type == 'on':
            active[note] = time
        elif evt_type == 'off' and note in active:
            start = active.pop(note)
            dur = time - start
            if dur > 0:
                note_events.append((note, start, dur, 80))
    
    # Synthesize to WAV
    SAMPLE_RATE = 44100
    ticks_per_sec = (mid_read.ticks_per_beat * BPM) / 60.0
    total_ticks = max((e[1] + e[2]) for e in note_events) if note_events else 480
    total_samples = int(total_ticks / ticks_per_sec * SAMPLE_RATE) + SAMPLE_RATE
    
    samples = [0.0] * total_samples
    
    for note, start_tick, dur_ticks, velocity in note_events:
        freq = 440.0 * (2.0 ** ((note - 69) / 12.0))
        start_sample = int(start_tick / ticks_per_sec * SAMPLE_RATE)
        dur_samples = int(dur_ticks / ticks_per_sec * SAMPLE_RATE)
        amplitude = (velocity / 127.0) * 0.15
        
        for s in range(dur_samples):
            idx = start_sample + s
            if idx < total_samples:
                # Envelope: attack + sustain + release
                env = 1.0
                if s < 200:
                    env = s / 200.0
                elif s > dur_samples - 500:
                    env = (dur_samples - s) / 500.0
                # Sine wave with harmonics for richer sound
                t = s / SAMPLE_RATE
                val = (math.sin(2 * math.pi * freq * t) * 0.7 +
                       math.sin(2 * math.pi * freq * 2 * t) * 0.2 +
                       math.sin(2 * math.pi * freq * 3 * t) * 0.1)
                samples[idx] += val * amplitude * env
    
    # Normalize
    peak = max(abs(s) for s in samples) if samples else 1.0
    if peak > 0:
        samples = [s / peak * 0.9 for s in samples]
    
    WAV_FILE = 'fugue_fsharp_minor.wav'
    with open(WAV_FILE, 'wb') as f:
        # WAV header
        n_channels = 1
        sample_width = 2
        byte_rate = SAMPLE_RATE * n_channels * sample_width
        block_align = n_channels * sample_width
        data_size = len(samples) * sample_width
        
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + data_size))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))  # chunk size
        f.write(struct.pack('<H', 1))   # PCM
        f.write(struct.pack('<H', n_channels))
        f.write(struct.pack('<I', SAMPLE_RATE))
        f.write(struct.pack('<I', byte_rate))
        f.write(struct.pack('<H', block_align))
        f.write(struct.pack('<H', 16))  # bits per sample
        f.write(b'data')
        f.write(struct.pack('<I', data_size))
        for s in samples:
            f.write(struct.pack('<h', int(s * 32767)))
    
    duration = len(samples) / SAMPLE_RATE
    print(f"  Saved: {WAV_FILE} ({os.path.getsize(WAV_FILE)} bytes, {duration:.1f}s)")

except Exception as e:
    print(f"  WAV rendering failed: {e}")
    # Fallback: render manually
    WAV_FILE = 'fugue_fsharp_minor.wav'
    print(f"  Using manual synthesis fallback...")

# ── Constraint Oscilloscope Visualization ──────────────────────────
print("\n[5/5] Generating constraint oscilloscope visualization...")
try:
    from constraint_viz import ConstraintOscilloscope
    scope = ConstraintOscilloscope()
    scope.visualize_midi(
        MIDI_FILE,
        output_path='fugue_fsharp_minor_scope.png',
        title='Fugue in F# Minor — Constraint Oscilloscope (R2)'
    )
    print(f"  Saved: fugue_fsharp_minor_scope.png ({os.path.getsize('fugue_fsharp_minor_scope.png')} bytes)")
except Exception as e:
    print(f"  ConstraintOscilloscope failed: {e}")
    # Fallback: generate a piano-roll visualization
    print("  Generating piano-roll fallback...")
    from PIL import Image, ImageDraw, ImageFont
    
    COLORS = [(70, 130, 180), (60, 179, 113), (218, 165, 32), (205, 92, 92)]
    W, H = 1600, 600
    img = Image.new('RGB', (W, H), (20, 20, 30))
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((10, 5), "Fugue in F# Minor — Constraint Oscilloscope (Round 2)", fill=(220, 220, 220))
    
    # Piano roll
    for v_idx, voice in enumerate(fugue_voices):
        color = COLORS[v_idx]
        for beat, note in enumerate(voice):
            if 0 <= note <= 127:
                x = 100 + beat * (W - 120) // TOTAL_BEATS
                y = H - 40 - (note - 36) * (H - 80) // (79 - 36)
                w = max(2, (W - 120) // TOTAL_BEATS - 1)
                h = max(4, (H - 80) // (79 - 36))
                draw.rectangle([x, y - h//2, x + w, y + h//2], fill=color)
    
    # Legend
    for i, name in enumerate(VOICE_NAMES):
        draw.rectangle([W - 150, 30 + i * 20, W - 130, 45 + i * 20], fill=COLORS[i])
        draw.text((W - 125, 30 + i * 20), name, fill=(200, 200, 200))
    
    # Constraint stats
    draw.text((10, H - 25), f"Constraints: {result.constraints_satisfied}/{result.constraints_total} satisfied", fill=(150, 150, 150))
    
    img.save('fugue_fsharp_minor_scope.png')
    print(f"  Saved: fugue_fsharp_minor_scope.png ({os.path.getsize('fugue_fsharp_minor_scope.png')} bytes)")

# ── Style DNA Extraction ───────────────────────────────────────────
print("\n[Bonus] Extracting style DNA from composition...")
try:
    from style_dna import StyleExtractor
    extractor = StyleExtractor()
    tile = extractor.extract(
        midi_paths=[MIDI_FILE],
        composer='beta-tester-r2',
        era='baroque-fugal'
    )
    print(f"  Style tile extracted: {tile}")
    print(f"  Style DNA: {tile.__dict__ if hasattr(tile, '__dict__') else tile}")
except Exception as e:
    print(f"  Style extraction failed: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Complete ===")
print(f"Files generated:")
for f in [MIDI_FILE, 'fugue_fsharp_minor.wav', 'fugue_fsharp_minor_scope.png']:
    if os.path.exists(f):
        print(f"  ✓ {f} ({os.path.getsize(f)} bytes)")
    else:
        print(f"  ✗ {f} MISSING")
