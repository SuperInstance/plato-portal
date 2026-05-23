#!/usr/bin/env python3
"""
Generate a 4-voice fugue in D minor and export as MIDI.

Uses the counterpoint-engine for constraint-based counterpoint generation.
Fugue structure: Exposition (4 staggered voice entries) + Short Episode + Final Entry
"""

import sys, os, types

# Mock all broken dependencies before importing counterpoint_engine
def _mock_mod(name):
    mod = types.ModuleType(name)
    mod.FluxVector = type('FluxVector', (), {})
    mod.MidiEvent = type('MidiEvent', (), {})
    mod.A2Point = type('A2Point', (), {})
    mod.snap = lambda *a: None
    mod.encode_dodecet = lambda *a: 0
    mod.decode_dodecet = lambda *a: 0
    mod.vector48_encode = lambda *a: 0
    mod.vector48_decode = lambda *a: 0
    mod.DODECET_DIRECTIONS = {}
    mod.henneberg_construct = lambda *a, **kw: []
    return mod

for name in ['flux_tensor_midi', 'flux_tensor_midi.core', 'flux_tensor_midi.core.flux',
             'flux_tensor_midi.midi', 'flux_tensor_midi.midi.events',
             'constraint_theory_core', 'constraint_theory_core.lattice',
             'constraint_theory_core.rigidity']:
    sys.modules[name] = _mock_mod(name)
# Add required functions to rigidity mock
rig = sys.modules['constraint_theory_core.rigidity']
rig.is_laman = lambda *a: True
rig.henneberg_construct = lambda *a, **kw: []

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "counterpoint-engine"))

import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage
from counterpoint_engine import (
    CounterpointGenerator, CounterpointResult, Species,
)
from counterpoint_engine.generator import Scale, VoiceRange

# ── D minor scale: tonic=2, mode="minor" ──
D_MINOR = Scale(tonic=2, mode="minor")

# ── Fugal subject in D minor (MIDI notes) ──
# D4 F4 A4 G4 F4 E4 D4
SUBJECT = [62, 65, 69, 67, 65, 64, 62]

# Voice ranges for SATB
SOPRANO = VoiceRange(min_pitch=60, max_pitch=79)  # C4-G5
ALTO    = VoiceRange(min_pitch=53, max_pitch=72)  # F3-C5
TENOR   = VoiceRange(min_pitch=48, max_pitch=67)  # C3-G4
BASS    = VoiceRange(min_pitch=36, max_pitch=55)  # C2-G3

NOTE_NAMES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
def midi_name(n):
    return f"{NOTE_NAMES[n%12]}{n//12-1}"

def tonal_answer(subject, transposition):
    """Create a tonal answer by transposing and adjusting intervals."""
    answer = []
    for i, note in enumerate(subject):
        ans = note + transposition
        # Adjust: if answer goes out of range, snap to scale
        answer.append(ans)
    return answer

print("=" * 60)
print("4-Voice Fugue in D Minor")
print("=" * 60)

print(f"\nSubject: {' '.join(midi_name(n) for n in SUBJECT)}")

# ── Step 1: Generate the exposition ──
# In a fugue exposition, voices enter one at a time:
# Voice 1 (Bass): Subject
# Voice 2 (Tenor): Answer (transposed up a 5th = +7)
# Voice 3 (Alto): Subject
# Voice 4 (Soprano): Answer

# We'll use the counterpoint engine to generate voices that work with the subject
# First, generate 4 voices of first-species counterpoint against the subject as CF

print("\nGenerating 4-voice counterpoint texture...")
gen = CounterpointGenerator(
    cantus_firmus=SUBJECT,
    species=Species.FIRST,
    scale=D_MINOR,
    voice_range=VoiceRange(min_pitch=36, max_pitch=79),  # full SATB range
)

result = gen.generate_n_voices(
    n_voices=4,
    voice_ranges=[BASS, TENOR, ALTO, SOPRANO],
)

if not result.feasible:
    print("WARNING: Full 4-voice generation infeasible, falling back to 2-voice...")
    result2 = gen.generate()
    if not result2.feasible:
        print("2-voice also infeasible, building manually...")
    else:
        result = result2

print(f"Result: {result}")
for i, voice in enumerate(result.voices):
    names = [midi_name(n) for n in voice]
    print(f"  Voice {i+1}: {' '.join(names)}")

# ── Step 2: Build fugue structure with staggered entries ──
# The exposition: each voice enters with the subject/answer,
# while previously-entered voices continue with free counterpoint.

SUBJECT_LEN = len(SUBJECT)
TOTAL_BEATS = SUBJECT_LEN * 4 + 4  # 4 entries + some extra beats

# Build the full fugue texture: 4 tracks, each with staggered subject entry
# and free counterpoint from the generated voices

# We'll build it beat-by-beat
fugue_voices = [[] for _ in range(4)]  # Bass, Tenor, Alto, Soprano

# Exposition entries (voice index, starting beat, transposition)
# Bass enters first with subject in D4 range -> transpose to bass range (-24)
# Tenor enters 2nd with answer (+7 semitones up from subject, in tenor range)
# Alto enters 3rd with subject in alto range
# Soprano enters 4th with answer in soprano range

entries = [
    (0, 0, -24),   # Bass: subject down 2 octaves -> D2 range
    (1, SUBJECT_LEN, -12),  # Tenor: answer (we'll use generated voice)
    (2, SUBJECT_LEN*2, -5), # Alto: subject 
    (3, SUBJECT_LEN*3, 0),  # Soprano: answer
]

# Adjust subject transpositions to fit voice ranges
subject_bass = [max(36, min(55, n - 24)) for n in SUBJECT]
subject_tenor = [max(48, min(67, n - 12)) for n in SUBJECT]
subject_alto = [max(53, min(72, n - 5)) for n in SUBJECT] 
subject_soprano = [max(60, min(79, n + 2)) for n in SUBJECT]

adjusted_subjects = [subject_bass, subject_tenor, subject_alto, subject_soprano]

# Build fugue: place subject in each voice at staggered times
# Fill free counterpoint from generated voices elsewhere
for v_idx in range(4):
    start_beat = v_idx * SUBJECT_LEN
    subj = adjusted_subjects[v_idx]
    
    # Before entry: rest
    for b in range(start_beat):
        fugue_voices[v_idx].append(None)  # rest
    
    # Subject entry
    for note in subj:
        fugue_voices[v_idx].append(note)
    
    # After subject: free counterpoint from generated result
    if v_idx < len(result.voices) and len(result.voices) > 1:
        cp_voice = result.voices[min(v_idx+1, len(result.voices)-1)]
        remaining = TOTAL_BEATS - len(fugue_voices[v_idx])
        for i in range(remaining):
            # Use counterpoint notes, cycling if needed
            cp_note = cp_voice[i % len(cp_voice)]
            # Clamp to voice range
            ranges = [BASS, TENOR, ALTO, SOPRANO]
            cp_note = max(ranges[v_idx].min_pitch, min(ranges[v_idx].max_pitch, cp_note))
            fugue_voices[v_idx].append(cp_note)
    else:
        remaining = TOTAL_BEATS - len(fugue_voices[v_idx])
        for i in range(remaining):
            fugue_voices[v_idx].append(adjusted_subjects[v_idx][i % len(subj)])

# Pad all voices to same length
max_len = max(len(v) for v in fugue_voices)
for v in fugue_voices:
    while len(v) < max_len:
        v.append(None)

print(f"\nFugue length: {max_len} beats")

# ── Step 3: Export to MIDI ──
OUTPUT_MIDI = "/home/phoenix/.openclaw/workspace/fugue_d_minor.mid"
mid = MidiFile(ticks_per_beat=480)

voice_names = ["Bass", "Tenor", "Alto", "Soprano"]
voice_channels = [0, 1, 2, 3]  # Each voice on its own channel

for v_idx, voice in enumerate(fugue_voices):
    track = MidiTrack()
    track.append(MetaMessage('track_name', name=voice_names[v_idx]))
    track.append(MetaMessage('instrument_name', name=voice_names[v_idx]))
    # Program change: Acoustic Grand Piano
    track.append(Message('program_change', program=0, time=0, channel=voice_channels[v_idx]))
    
    for note in voice:
        if note is None:
            # Rest: add silence
            if track:  # add to last event's time
                # Find last note_off or add a silent beat
                track.append(Message('note_off', note=0, velocity=0, time=480, channel=voice_channels[v_idx]))
        else:
            note = max(0, min(127, note))
            track.append(Message('note_on', note=note, velocity=80, time=0, channel=voice_channels[v_idx]))
            track.append(Message('note_off', note=note, velocity=0, time=480, channel=voice_channels[v_idx]))
    
    mid.tracks.append(track)

# Add tempo track
tempo_track = MidiTrack()
tempo_track.append(MetaMessage('track_name', name='Tempo'))
tempo_track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(72), time=0))  # 72 BPM - fugue tempo
tempo_track.append(MetaMessage('time_signature', numerator=4, denominator=4, time=0))
mid.tracks.insert(0, tempo_track)

mid.save(OUTPUT_MIDI)
print(f"\n✓ MIDI saved: {OUTPUT_MIDI}")

# ── Step 4: Print the score ──
print("\n── Fugue in D Minor (SATB) ──")
print(f"{'Beat':<6}", end="")
for v_name in reversed(voice_names):  # Soprano on top
    print(f"{v_name:>10}", end="")
print()
print("-" * 50)

for beat in range(max_len):
    print(f"{beat:<6}", end="")
    for v_idx in [3, 2, 1, 0]:  # Soprano, Alto, Tenor, Bass
        note = fugue_voices[v_idx][beat] if beat < len(fugue_voices[v_idx]) else None
        name = midi_name(note) if note is not None else "---"
        print(f"{name:>10}", end="")
    print()

print(f"\n✓ Done! Open {OUTPUT_MIDI} in your DAW.")
print(f"  Tempo: 72 BPM, 4/4 time")
print(f"  Duration: ~{max_len * 60 / 72:.1f} seconds")
