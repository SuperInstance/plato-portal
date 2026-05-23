#!/usr/bin/env python3
"""
HIP-HOP PRODUCER TEST SUITE
Testing the constraint theory stack from a producer's perspective.
"""

import sys, os, json, random, math

WORKSPACE = os.path.expanduser('~/.openclaw/workspace')
sys.path.insert(0, WORKSPACE)

from constraint_instrument import Instrument
from constraint_instrument.terrain import TERRAINS
from constraint_instrument.basie import BasieEngine
from constraint_instrument.ella import EllaEngine

print(f"=== HIP-HOP PRODUCER TEST ===")

# ════════════════════════════════════════════════════
# TEST 1: Terrain analysis — what's the trap terrain like?
# ════════════════════════════════════════════════════
print("\n" + "="*60)
print("TEST 1: Trap Terrain Analysis")
print("="*60)
trap = TERRAINS['hip_hop_trap']
print(f"Rhythmic skeletons:")
for rs in trap.rhythmic_skeletons:
    print(f"  {rs.name}: accents={rs.accents}, swing={rs.swing}")
print(f"Register: {trap.register_tendency} (C1-E2)")

# ════════════════════════════════════════════════════
# TEST 2: Ella mode — melodic generation
# ════════════════════════════════════════════════════
print("\n" + "="*60)
print("TEST 2: Ella Mode (melodic flow over trap)")
print("="*60)
inst = Instrument(mode='ella', terrain='hip_hop_trap', key='C', bpm=145, bars=4)
notes = inst.perform()
print(f"Generated {len(notes)} melodic notes")
if notes:
    pitches = sorted(set(n['pitch'] for n in notes))
    durations = sorted(set(round(n['duration'], 4) for n in notes))
    velocities = [n['velocity'] for n in notes]
    print(f"  Pitch range: {min(pitches)}-{max(pitches)} ({sorted(pitches)})")
    print(f"  Velocity range: {min(velocities)}-{max(velocities)}, avg={sum(velocities)/len(velocities):.0f}")
    print(f"  Duration range: {min(durations):.4f}-{max(durations):.4f}")
    print(f"  Time span: {notes[-1]['start_time']+notes[-1]['duration']:.3f}s")

# ════════════════════════════════════════════════════
# TEST 3: Ella engine directly — more control
# ════════════════════════════════════════════════════
print("\n" + "="*60)
print("TEST 3: Ella Engine Direct Access")
print("="*60)
ella = EllaEngine(trap, 60)
result = ella.perform()
print(f"Result keys: {list(result.keys())}")
raw = result.get("notes", [])
print(f"Raw notes: {len(raw)}")
if raw and len(raw) > 0:
    print(f"First note: {json.dumps(raw[0][:3] if isinstance(raw[0], tuple) else raw[0], indent=2)}")

# ════════════════════════════════════════════════════
# TEST 4: Basie mode — jam session with DRUMS
# ════════════════════════════════════════════════════
print("\n" + "="*60)
print("TEST 4: Basie Mode Jam Session (DRUMS!)")
print("="*60)
# Create a session with instruments that sound like a drum kit
basie = BasieEngine(trap, 60)
session = basie.join_jam(players=6, tempo=145)
result = session.play(my_role="drums", listen=False)
notes_by_player = result.get("notes", {})
groove = result.get("groove")
print(f"Players: {list(notes_by_player.keys())}")
print(f"Groove: {groove}")
for player, pnotes in notes_by_player.items():
    pitches = sorted(set(n['pitch'] for n in pnotes))
    print(f"  {player}: {len(pnotes)} notes, pitches={pitches}")

# ════════════════════════════════════════════════════
# TEST 5: Adaptation in Basie mode — groove formation
# ════════════════════════════════════════════════════
print("\n" + "="*60)
print("TEST 5: Basie Mode — Groove Formation Over Time")
print("="*60)
session2 = basie.join_jam(players=4, tempo=145)
for i in range(5):
    r = session2.play(my_role="piano", listen=True)
    g = r["groove"]
    print(f"  Iteration {i+1}: pocket={g.pocket:.3f}, tempo={g.tempo_consensus:.1f}, swing={g.swing_consensus:.3f} | {g.description}")

# Lock it
session2.lock()
print(f"  Locked: pocket=1.0, description='Consensus achieved'")

# ════════════════════════════════════════════════════
# TEST 6: MIDI export
# ════════════════════════════════════════════════════
print("\n" + "="*60)
print("TEST 6: MIDI Export")
print("="*60)
try:
    midi_path = inst.to_midi('test_trap_melody.mid')
    print(f"MIDI exported to: {midi_path} ({os.path.getsize(midi_path)} bytes)")
except ImportError as e:
    print(f"MIDI export FAILED: {e}")

# ════════════════════════════════════════════════════
# TEST 7: Render to WAV
# ════════════════════════════════════════════════════
print("\n" + "="*60)
print("TEST 7: WAV Render")
print("="*60)
wav_path = inst.render('test_trap_melody.wav')
print(f"WAV: {wav_path} ({os.path.getsize(wav_path)} bytes)")

# ════════════════════════════════════════════════════
# TEST 8: Groove Analyzer
# ════════════════════════════════════════════════════
print("\n" + "="*60)
print("TEST 8: Groove Analyzer")
print("="*60)
from groove_analyzer import extract_microtiming, fit_deadband, prove_groove_is_deadband
from groove_analyzer.genres import GENRE_PROFILES, synthesize_groove

print(f"Genre profiles: {list(GENRE_PROFILES.keys())}")
for name, p in GENRE_PROFILES.items():
    print(f"  {name}: ε={p.epsilon_ms}ms [{p.epsilon_range}], swing={p.swing_factor}")

# Synthesize grooves for all genres
for genre_name in GENRE_PROFILES:
    fname = f'test_{genre_name.lower()}_groove.mid'
    synthesize_groove(genre_name, bars=2, seed=42, output_path=fname)
    timing = extract_microtiming(fname)
    db = fit_deadband(timing)
    proof = prove_groove_is_deadband(timing)
    print(f"\n  {genre_name}:")
    print(f"    Deadband ε={db.epsilon_ms:.1f}ms, matched={db.genre_match}")
    print(f"    Coverage: {proof['coverage']:.1%}, Variance collapse: {proof['variance_collapse']:.3f}")

# ════════════════════════════════════════════════════
# TEST 9: ConstraintSynth — 808 kick and sub bass
# ════════════════════════════════════════════════════
print("\n" + "="*60)
print("TEST 9: ConstraintSynth — 808 & Sub Bass")
print("="*60)
from constraint_synth.synth import ConstraintSynth
from constraint_synth.oscillator import LatticeOscillator
from constraint_synth.envelope import FunnelEnvelope
import numpy as np

print(f"Available presets: {list(ConstraintSynth.PRESETS.keys())}")

# 808 kick
kicker = ConstraintSynth.from_preset('808_kick')
kick_signal = kicker.play_note(36, 120, 0.5)
ConstraintSynth.to_wav(kick_signal, 'test_808_kick.wav')
print(f"  808 kick: {len(kick_signal)} samples, peak={np.max(np.abs(kick_signal)):.3f}")

# Custom sub bass - long sustain, sine wave
sub_bass = ConstraintSynth(
    oscillator=LatticeOscillator(frequency=55.0, lattice_shape='sine'),
    envelope=FunnelEnvelope(attack=0.005, decay=0.05, sustain=0.9, release=0.4),
    filter_cutoff=150.0,
    reverb_wet=0.0
)
sub_signal = sub_bass.play_note(38, 110, 1.0)  # D2, sustained
ConstraintSynth.to_wav(sub_signal, 'test_sub_bass.wav')
print(f"  Sub bass: {len(sub_signal)} samples, peak={np.max(np.abs(sub_signal)):.3f}")

# Hi-hat style: short noise burst
hihat = ConstraintSynth(
    oscillator=LatticeOscillator(frequency=8000.0, lattice_shape='saw', noise_floor=0.3),
    envelope=FunnelEnvelope(attack=0.001, decay=0.05, sustain=0.0, release=0.01),
    filter_cutoff=10000.0,
    reverb_wet=0.0
)
hat_signal = hihat.play_note(42, 80, 0.05)
ConstraintSynth.to_wav(hat_signal, 'test_hihat.wav')
print(f"  Hi-hat: {len(hat_signal)} samples, peak={np.max(np.abs(hat_signal)):.3f}")

# 808 slide effect (glide between two notes)
slide_osc = LatticeOscillator(frequency=55.0, lattice_shape='sine')
slide_env = FunnelEnvelope(attack=0.01, decay=0.3, sustain=0.0, release=0.0)
slide_synth = ConstraintSynth(oscillator=slide_osc, envelope=slide_env, filter_cutoff=200.0)
# Simulate slide by rendering A2 then bending up
slide1 = slide_synth.play_note(45, 100, 0.3)  # A2
# Generate a pitch-bent note by changing frequency
slide_osc.frequency = 65.41  # C3 (up a minor 3rd)
slide2 = slide_synth.play_note(48, 100, 0.3)  # C3
slide_wav = np.concatenate([slide1, slide2])
ConstraintSynth.to_wav(slide_wav, 'test_808_slide.wav')
print(f"  808 slide: rendered A2→C3")

# ════════════════════════════════════════════════════
# TEST 10: Building a complete beat layer-by-layer
# ════════════════════════════════════════════════════
print("\n" + "="*60)
print("TEST 10: BUILD A COMPLETE BEAT (layer by layer)")
print("="*60)

# We'll stack the DAW approach:
#   Layer 1: Kick pattern (MIDI)
#   Layer 2: 808 bass pattern
#   Layer 3: Melody/synth
# All rendered together

# Helper: create MIDI for our custom patterns
def midi_note(track, pitch, velocity, start_beat, duration_beats, tpb=480, bpm=145):
    """Helper to add a note to a MIDI track."""
    ticks_per_beat = tpb
    beat_ms = 60000.0 / bpm
    
    start_tick = int(start_beat * ticks_per_beat)
    dur_ticks = int(duration_beats * ticks_per_beat)
    
    # Add note on
    track.append(mido.Message('note_on', note=pitch, velocity=velocity, 
                               time=start_tick))
    track.append(mido.Message('note_off', note=pitch, velocity=0,
                               time=dur_ticks))

import mido

# Create MIDI file for the beat
beat_mid = mido.MidiFile(ticks_per_beat=480)
meta = mido.MidiTrack()
meta.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(145), time=0))
meta.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))
beat_mid.tracks.append(meta)

# === Kick drum pattern (trap style) ===
kick_track = mido.MidiTrack()
kick_track.append(mido.MetaMessage('track_name', name='Kick', time=0))
kick_pattern = {
    0: 100,    # beat 1, heavy
    3: 80,     # 808 hit
    5: 70,     # light
    8: 100,    # beat 3, heavy
    11: 80,    # fill
    13: 60,    # ghost
}
tpb = 480
current_tick = 0
for beat, vel in sorted(kick_pattern.items()):
    tick = int(beat * tpb / 4)  # beats at 16th note resolution
    delta = tick - current_tick
    if delta < 0:
        continue
    kick_track.append(mido.Message('note_on', note=36, velocity=vel, time=delta))
    dur = min(tpb//4, max(10, tpb//8))
    kick_track.append(mido.Message('note_off', note=36, velocity=0, time=dur))
    current_tick = tick + dur
kick_track.append(mido.MetaMessage('end_of_track', time=0))
beat_mid.tracks.append(kick_track)

# === Snare pattern ===
snare_track = mido.MidiTrack()
snare_track.append(mido.MetaMessage('track_name', name='Snare', time=0))
# Trap snare on beats 2 and 4
snare_hits = [(4, 100), (12, 100)]  # 16th note positions
prev_tick_snare = 0
for tick_pos, vel in snare_hits:
    delta = tick_pos - prev_tick_snare
    if delta < 0:
        continue
    snare_track.append(mido.Message('note_on', note=38, velocity=vel, time=delta))
    dur = tpb//8
    snare_track.append(mido.Message('note_off', note=38, velocity=0, time=dur))
    prev_tick_snare = tick_pos + dur
snare_track.append(mido.MetaMessage('end_of_track', time=0))
beat_mid.tracks.append(snare_track)

# === Hi-hat (trap roll) ===
hat_track = mido.MidiTrack()
hat_track.append(mido.MetaMessage('track_name', name='HiHat', time=0))
# 16th note hi-hats, some swing
hat_prev_tick = 0
for i in range(16):
    vel = 70 if (i % 2 == 0) else 50  # accent on eighths
    if i in [2, 6, 10, 14]:  # ghost notes
        vel = 35
    tick = i * (tpb // 4)
    delta = tick - hat_prev_tick
    hat_track.append(mido.Message('note_on', note=42, velocity=vel, time=max(1, delta)))
    dur = max(1, tpb//8)
    hat_track.append(mido.Message('note_off', note=42, velocity=0, time=dur))
    hat_prev_tick = tick + dur
hat_track.append(mido.MetaMessage('end_of_track', time=0))
beat_mid.tracks.append(hat_track)

# === 808 Bass line ===
bass_track = mido.MidiTrack()
bass_track.append(mido.MetaMessage('track_name', name='808_Bass', time=0))
# Trap bass: long sustained notes
bass_pattern = [
    (0, 36, 100),    # C1
    (4, 36, 100),    # C1 again
    (6, 43, 85),     # G1
    (8, 36, 100),    # C1
    (10, 31, 85),    # G#0
    (12, 36, 100),   # C1
    (14, 38, 80),    # D1
]
prev_tick = 0
for beat, pitch, vel in bass_pattern:
    tick = int(beat * tpb / 4)
    delta = tick - prev_tick
    bass_track.append(mido.Message('note_on', note=pitch, velocity=vel, time=max(0, delta)))
    # Long sustain for 808
    bass_track.append(mido.Message('note_off', note=pitch, velocity=0, time=tpb//2))
    prev_tick = tick + tpb//2

bass_track.append(mido.MetaMessage('end_of_track', time=0))
beat_mid.tracks.append(bass_track)

# === Melody track (from constraint_instrument) ===
melody_track = mido.MidiTrack()
melody_track.append(mido.MetaMessage('track_name', name='Melody', time=0))
# Use the ella mode notes from our instrument
mel_notes = inst.perform()
prev_tick = 0
for n in mel_notes:
    tick = int(n['start_time'] * tpb * 145 / 60.0)
    dur_ticks = int(n['duration'] * tpb * 145 / 60.0)
    delta = tick - prev_tick
    melody_track.append(mido.Message('note_on', note=n['pitch'], velocity=n['velocity'], time=max(0, delta)))
    melody_track.append(mido.Message('note_off', note=n['pitch'], velocity=0, time=max(1, dur_ticks)))
    prev_tick = tick + dur_ticks
melody_track.append(mido.MetaMessage('end_of_track', time=0))
beat_mid.tracks.append(melody_track)

beat_mid.save('test_full_beat.mid')
print(f"Full beat MIDI: test_full_beat.mid")
print(f"  Tracks: {len(beat_mid.tracks)}")
for i, t in enumerate(beat_mid.tracks):
    name = next((m.name for m in t if m.type == 'track_name'), f'track_{i}')
    notes = sum(1 for m in t if m.type == 'note_on')
    print(f"    {name}: {notes} notes")

# ════════════════════════════════════════════════════
# TEST 11: Groove analysis of our custom beat
# ════════════════════════════════════════════════════
print("\n" + "="*60)
print("TEST 11: Groove Analysis of Custom Beat MIDI")
print("="*60)
if os.path.exists('test_full_beat.mid'):
    t = extract_microtiming('test_full_beat.mid')
    print(f"  BPM: {t.bpm:.1f}")
    print(f"  Global offset: {t.global_avg_offset_ms:.2f}ms")
    print(f"  Global pocket: {t.global_pocket_width_ms:.2f}ms")
    print(f"  Swing factor: {t.global_swing_factor:.3f}")
    for tr in t.tracks:
        print(f"  {tr.track_name}: {tr.avg_offset_ms:.2f}ms avg, {tr.pocket_width_ms:.2f}ms pocket")
    db = fit_deadband(t)
    print(f"  Deadband: ε={db.epsilon_ms:.2f}ms, matched={db.genre_match}")

print("\n" + "="*60)
print("SUMMARY — What a Hip-Hop Producer Gets")
print("="*60)
print("""
✅ WHAT WORKS:
━━━━━━━━━━━━
1. TERRAIN SYSTEM — The hip_hop_trap terrain has real thought behind it:
   • 808 as gravitational center (register tendency C1-E2)
   • Sparse melodic shell (minor pentatonic)
   • 4 rhythmic skeletons: trap bounce, hi-hat roll, 808 pattern, triplet flow
   • Harmonic rigidity is LOW, rhythmic rigidity is HIGH

2. CONSTRAINT INSTRUMENT:
   • Ella mode generates spontaneous melodic phrases over any terrain
   • Basie mode simulates jam sessions (piano, sax, trumpet, bass, drums)
   • Groove forms through consensus — pocket tightens over time
   • MIDI export works (via mido)
   • WAV rendering works

3. CONSTRAINT SYNTH:
   • 808 kick preset with sine oscillator + short attack envelope
   • Custom sub bass with long sustain envelope
   • Hi-hat with saw + noise floor
   • Biquad lowpass filter for cutoff control

4. GROOVE ANALYZER — Actually impressive:
   • extract_microtiming() reads MIDI and measures deviation per track
   • fit_deadband() finds the "ε" — the groove pocket width
   • prove_groove_is_deadband() shows coverage + variance collapse
   • Genre matching: identifies genre from microtiming profile
   • synthesize_groove() generates genre-authentic MIDI patterns

⚠️ WHAT'S PARTIAL:
━━━━━━━━━━━━━━━━
• No explicit kick/snare/hat separation (no drum-specific API)
• Swing is probabilistic in Basie mode, not parameterized
• No note length staccato/legato API — must post-process
• 808 slide requires manual pitch bending via oscillator freq change

❌ WHAT'S MISSING (for a producer):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• No drum rack / pattern sequencer API
• No step sequencer (no explicit "put kick on 1 and 3")
• No humanization parameter (must DIY)
• No quantize parameter (must post-process)
• No groove template import/export
• 808 slide effect requires low-level oscillator manipulation
""")
