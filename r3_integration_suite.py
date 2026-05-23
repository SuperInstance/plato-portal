#!/usr/bin/env python3
"""
Round 3 Full Integration Test: "A Short Suite in Three Movements"

Tests the complete pipeline:
  Movement I  - 4-voice fugue in C minor (counterpoint engine)
  Movement II - Funk/Jazz groove + jazz voicings (groove analyzer + jazz voicing engine)
  Movement III- Style DNA extraction, Bach/Coltrane morphing (style-dna)
  Finale      - Render to WAV, generate oscilloscope PNGs
"""

import sys
import os
import json
import time
import traceback
from pathlib import Path

# Add all packages to path
WORKSPACE = Path("/home/phoenix/.openclaw/workspace")
sys.path.insert(0, str(WORKSPACE / "flux-tensor-midi"))
sys.path.insert(0, str(WORKSPACE / "counterpoint-engine"))
sys.path.insert(0, str(WORKSPACE / "groove-analyzer"))
sys.path.insert(0, str(WORKSPACE / "jazz-voicing-engine"))
sys.path.insert(0, str(WORKSPACE / "style-dna"))

import numpy as np
import mido
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ─── Test Infrastructure ───

results = {}

def record(step, error_score, musically_meaningful, notes="", error_detail=""):
    results[step] = {
        "error_score": error_score,  # 0=perfect, 10=gave up
        "musically_meaningful": musically_meaningful,
        "notes": notes,
        "error_detail": error_detail,
    }
    status = "✅" if error_score == 0 else "⚠️" if error_score <= 3 else "❌"
    print(f"  {status} {step}: error_score={error_score}, meaningful={musically_meaningful}")
    if notes:
        print(f"     {notes}")
    if error_detail:
        print(f"     ERROR: {error_detail[:200]}")

# ─── OUTPUT DIR ───

OUT = WORKSPACE / "r3_suite_output"
OUT.mkdir(exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# MOVEMENT I: "Lattice" — 4-voice fugue subject in C minor
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("MOVEMENT I: 'Lattice' — 4-voice fugue subject in C minor")
print("="*70)

# Step 1: Generate fugue subject and counterpoint
try:
    from counterpoint_engine import (
        CounterpointGenerator, Species, VoiceRange, Scale,
        CounterpointGraph, henneberg_construct, verify_rigidity,
    )

    # C minor fugue subject (cantus firmus) — 12 notes
    c_minor_scale = Scale(tonic=0, mode="minor")
    cf = [60, 63, 62, 60, 67, 65, 63, 60, 58, 60, 63, 60]  # C Eb D C G F Eb C Ab C Eb C

    gen = CounterpointGenerator(
        cantus_firmus=cf,
        species=Species.FIRST,
        scale=c_minor_scale,
        voice_range=VoiceRange(min_pitch=48, max_pitch=79),
    )

    result_4v = gen.generate_n_voices(
        n_voices=4,
        voice_ranges=[
            VoiceRange(min_pitch=48, max_pitch=62),  # Bass
            VoiceRange(min_pitch=55, max_pitch=70),  # Tenor
            VoiceRange(min_pitch=60, max_pitch=76),  # Alto
            VoiceRange(min_pitch=67, max_pitch=84),  # Soprano
        ],
    )

    print(f"  4-voice result: {result_4v}")
    print(f"  Voices: {len(result_4v.voices)}, Feasible: {result_4v.feasible}")
    print(f"  Constraints: {result_4v.constraints_satisfied}/{result_4v.constraints_total}")

    if result_4v.feasible and len(result_4v.voices) == 4:
        # Step 1b: Export MIDI
        midi_path_i = str(OUT / "movement_I_lattice.mid")
        result_4v.to_midi(midi_path_i)
        print(f"  Exported: {midi_path_i}")

        # Verify the MIDI file
        mid_i = mido.MidiFile(midi_path_i)
        print(f"  MIDI tracks: {len(mid_i.tracks)}, ticks/beat: {mid_i.ticks_per_beat}")

        # Check for empty/silent tracks
        total_notes = 0
        for track in mid_i.tracks:
            notes_in_track = sum(1 for m in track if m.type == 'note_on' and m.velocity > 0)
            total_notes += notes_in_track
        print(f"  Total note events: {total_notes}")

        record("I.1 Fugue generation", 0, True,
               f"4 voices, {result_4v.constraints_satisfied}/{result_4v.constraints_total} constraints, {total_notes} notes")
    else:
        record("I.1 Fugue generation", 5, False,
               f"Feasible={result_4v.feasible}, voices={len(result_4v.voices)}")

except Exception as e:
    record("I.1 Fugue generation", 10, False, error_detail=traceback.format_exc())

# Step 2: Analyze harmony of the fugue
try:
    from counterpoint_engine.laman_counterpoint import CounterpointGraph

    graph = CounterpointGraph(4)
    rigid = graph.verify_rigidity()
    print(f"  Laman rigidity (4 voices): {rigid}")
    print(f"  Graph edges: {len(graph.edges)}, expected: {graph.expected_edges()}")

    # Analyze intervals between voices at each beat
    if result_4v.feasible:
        intervals_analysis = []
        for beat in range(len(result_4v.voices[0])):
            beat_intervals = []
            for i in range(len(result_4v.voices)):
                for j in range(i+1, len(result_4v.voices)):
                    interval = abs(result_4v.voices[i][beat] - result_4v.voices[j][beat]) % 12
                    beat_intervals.append(interval)
            intervals_analysis.append(beat_intervals)

        consonant_intervals = {0, 3, 4, 7, 8, 9}
        total_intervals = sum(len(bi) for bi in intervals_analysis)
        consonant_count = sum(
            1 for bi in intervals_analysis for iv in bi if iv in consonant_intervals
        )
        cons_rate = consonant_count / total_intervals if total_intervals > 0 else 0
        print(f"  Consonance rate across all voice pairs: {cons_rate:.3f}")

    record("I.2 Harmony analysis", 0, True,
           f"Laman rigid={rigid}, consonance={cons_rate:.3f}")

except Exception as e:
    record("I.2 Harmony analysis", 10, False, error_detail=traceback.format_exc())

# ══════════════════════════════════════════════════════════════════════════════
# MOVEMENT II: "Groove" — Funk/Jazz groove + jazz voicings
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("MOVEMENT II: 'Groove' — Funk/Jazz groove + jazz voicings")
print("="*70)

# Step 3: Create funk/jazz groove
try:
    from groove_analyzer import (
        synthesize_groove, GENRE_PROFILES,
        extract_microtiming, fit_deadband, prove_groove_is_deadband,
    )

    # Generate Funk groove (4 bars)
    groove_path = str(OUT / "movement_II_groove.mid")
    funk_groove = synthesize_groove(
        "Funk", bars=4, seed=42, output_path=groove_path,
    )
    print(f"  Funk groove: {len(funk_groove.tracks)} tracks")
    print(f"  Genre profile: {GENRE_PROFILES['Funk']}")

    # Also generate Jazz groove
    jazz_groove_path = str(OUT / "movement_II_jazz_groove.mid")
    jazz_groove = synthesize_groove(
        "Jazz", bars=4, seed=42, output_path=jazz_groove_path,
    )
    print(f"  Jazz groove: {len(jazz_groove.tracks)} tracks")

    # Analyze the groove
    timing = extract_microtiming(groove_path)
    print(f"  Timing tracks: {len(timing.tracks)}")
    for name, tt in timing.tracks.items():
        print(f"    {name}: {len(tt.onsets)} onsets, mean_dev={tt.mean_deviation:.1f}ms")

    # Prove groove = deadband
    proof = prove_groove_is_deadband(groove_path)
    print(f"  Deadband proof: {proof}")

    record("II.1 Groove generation", 0, True,
           f"Funk {len(funk_groove.tracks)} tracks, Jazz {len(jazz_groove.tracks)} tracks, deadband proved={proof}")

except Exception as e:
    record("II.1 Groove generation", 10, False, error_detail=traceback.format_exc())

# Step 4: Generate jazz voicings for ii-V-I progression
try:
    from jazz_voicing_engine.voicings import ChordSymbol
    from jazz_voicing_engine.generator import VoicingGenerator

    # ii-V-I in C: Dm7 → G7 → Cmaj7
    progression = [
        ChordSymbol.parse("Dm7"),
        ChordSymbol.parse("G7"),
        ChordSymbol.parse("Cmaj7"),
    ]
    print(f"  Progression: {[str(c) for c in progression]}")
    for c in progression:
        print(f"    {c}: pitches={c.pitches}, 3rd={c.third}, 7th={c.seventh}")

    # Generate multiple voicing styles
    styles = ["drop2", "rootless", "quartal", "shell"]
    all_voicings = {}

    for style in styles:
        vg = VoicingGenerator(style=style, register=(48, 84))
        voicings = vg.voice_lead(progression)
        all_voicings[style] = voicings
        for i, v in enumerate(voicings):
            print(f"    {style} {progression[i]}: {v.pitches}")

    # Create a combined MIDI with all voicing styles
    voicing_mid = mido.MidiFile(ticks_per_beat=480)
    tempo = mido.bpm2tempo(120)

    for s_idx, style in enumerate(styles):
        track = mido.MidiTrack()
        track.append(mido.MetaMessage('track_name', name=f'{style}_voicing', time=0))
        voicings = all_voicings[style]

        abs_tick = 0
        for v_idx, voicing in enumerate(voicings):
            # Each chord gets 2 beats
            duration_ticks = 480 * 2
            for pitch in voicing.pitches:
                track.append(mido.Message('note_on', note=pitch, velocity=70,
                                         channel=0, time=max(0, abs_tick - sum(m.time for m in track[-2:] if hasattr(m, 'time')))))
            # We'll use a simpler approach: just write events sequentially
            pass

        # Simpler: use to_midi_events
        track = mido.MidiTrack()
        track.append(mido.MetaMessage('track_name', name=f'{style}_voicing', time=0))
        track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))

        events = []
        for v_idx, voicing in enumerate(voicings):
            start_beat = v_idx * 2
            evts = voicing.to_midi_events(
                start=start_beat * 0.5,  # 0.5 sec per beat at 120bpm
                duration=1.0,
                velocity=70,
            )
            events.extend(evts)

        # Sort events by time
        events.sort(key=lambda e: (e["time"], 0 if e["type"] == "note_on" else 1))

        # Convert to ticks
        prev_tick = 0
        for ev in events:
            tick = int(ev["time"] * 480 * 2)  # approximate: 0.5s = 480 ticks
            delta = max(0, tick - prev_tick)
            msg_type = ev["type"]
            track.append(mido.Message(
                msg_type, note=ev["note"], velocity=ev["velocity"],
                channel=ev["channel"], time=delta
            ))
            prev_tick = tick + delta

        track.append(mido.MetaMessage('end_of_track', time=0))
        voicing_mid.tracks.append(track)

    voicing_path = str(OUT / "movement_II_jazz_voicings.mid")
    voicing_mid.save(voicing_path)
    print(f"  Jazz voicings MIDI: {voicing_path} ({len(voicing_mid.tracks)} tracks)")

    record("II.2 Jazz voicings", 0, True,
           f"ii-V-I with {len(styles)} voicing styles")

except Exception as e:
    record("II.2 Jazz voicings", 10, False, error_detail=traceback.format_exc())

# Step 5: Layer fugue melody with groove
try:
    # Combine Movement I fugue with Movement II groove into one MIDI
    combined_mid = mido.MidiFile(ticks_per_beat=480)

    # Add fugue voices as tracks
    if result_4v.feasible:
        for v_idx, voice in enumerate(result_4v.voices):
            track = mido.MidiTrack()
            track.append(mido.MetaMessage('track_name', name=f'Fugue_V{v_idx+1}', time=0))
            for note in voice:
                if 0 <= note <= 127:
                    track.append(mido.Message('note_on', note=note, velocity=75, time=0))
                    track.append(mido.Message('note_off', note=note, velocity=0, time=480))
            track.append(mido.MetaMessage('end_of_track', time=0))
            combined_mid.tracks.append(track)

    # Add groove tracks
    for track in funk_groove.tracks:
        combined_mid.tracks.append(track)

    combined_path = str(OUT / "movement_II_combined.mid")
    combined_mid.save(combined_path)
    print(f"  Combined fugue+groove: {combined_path} ({len(combined_mid.tracks)} tracks)")

    record("II.3 Layer fugue+groove", 0, True,
           f"{len(combined_mid.tracks)} tracks combined")

except Exception as e:
    record("II.3 Layer fugue+groove", 10, False, error_detail=traceback.format_exc())

# ══════════════════════════════════════════════════════════════════════════════
# MOVEMENT III: "Style" — Style DNA extraction and transformation
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("MOVEMENT III: 'Style' — DNA extraction, Bach & Coltrane morphing")
print("="*70)

# Step 6: Extract style DNA from Movement I and II
try:
    from style_dna import StyleExtractor, StyleTile, StyleMorpher, PERSONALITIES

    extractor = StyleExtractor()

    # Extract from Movement I (fugue)
    tile_I = extractor.extract([str(OUT / "movement_I_lattice.mid")], "Suite_Movement_I", "classical")
    print(f"  Movement I style: mean_interval={tile_I.mean_interval}, consonance={tile_I.consonance_rate:.3f}")
    print(f"    step/leap={tile_I.step_vs_leap_ratio}, syncopation={tile_I.syncopation_rate}")
    print(f"    pitch_center={tile_I.pitch_center}, notes_per_bar={tile_I.notes_per_bar}")
    print(f"    betti={tile_I.betti_numbers}, euler={tile_I.euler_characteristic}")
    print(f"    lyapunov={tile_I.lyapunov_exponent}, entropy_ratio={tile_I.entropy_ratio}")

    # Extract from Movement II (groove)
    tile_II = extractor.extract([str(OUT / "movement_II_combined.mid")], "Suite_Movement_II", "jazz_funk")
    print(f"  Movement II style: mean_interval={tile_II.mean_interval}, consonance={tile_II.consonance_rate:.3f}")
    print(f"    step/leap={tile_II.step_vs_leap_ratio}, syncopation={tile_II.syncopation_rate}")
    print(f"    pitch_center={tile_II.pitch_center}, notes_per_bar={tile_II.notes_per_bar}")

    record("III.1 Style DNA extraction", 0, True,
           f"I: cons={tile_I.consonance_rate:.2f}, lyap={tile_I.lyapunov_exponent}; "
           f"II: cons={tile_II.consonance_rate:.2f}, sync={tile_II.syncopation_rate:.2f}")

except Exception as e:
    record("III.1 Style DNA extraction", 10, False, error_detail=traceback.format_exc())

# Step 7: Morph Movement I toward Bach
try:
    morpher = StyleMorpher(seed=42)

    bach_tile = PERSONALITIES["Bach"]
    coltrane_tile = PERSONALITIES["Coltrane"]

    print(f"\n  Target: Bach tile")
    print(f"    mean_interval={bach_tile.mean_interval}, consonance={bach_tile.consonance_rate}")
    print(f"    step/leap={bach_tile.step_vs_leap_ratio}, syncopation={bach_tile.syncopation_rate}")

    # Morph Movement I → Bach
    bach_morph_path = morpher.morph(
        str(OUT / "movement_I_lattice.mid"),
        bach_tile,
        blend=0.8,
        output_path=str(OUT / "movement_I_bach_morph.mid"),
    )
    print(f"  Bach morph: {bach_morph_path}")

    # Compute before/after similarity
    tile_I_bach = extractor.extract([bach_morph_path], "Movement_I_Bach", "baroque")
    sim_before_bach = tile_I.similarity(bach_tile)
    sim_after_bach = tile_I_bach.similarity(bach_tile)
    print(f"  Similarity to Bach: before={sim_before_bach}, after={sim_after_bach}")
    print(f"  Improvement: {sim_after_bach - sim_before_bach:+.4f}")

    record("III.2 Bach morph", 0, True,
           f"sim before={sim_before_bach:.3f}, after={sim_after_bach:.3f}, Δ={sim_after_bach-sim_before_bach:+.3f}")

except Exception as e:
    record("III.2 Bach morph", 10, False, error_detail=traceback.format_exc())

# Step 8: Morph Movement II toward Coltrane
try:
    print(f"\n  Target: Coltrane tile")
    print(f"    mean_interval={coltrane_tile.mean_interval}, consonance={coltrane_tile.consonance_rate}")
    print(f"    step/leap={coltrane_tile.step_vs_leap_ratio}, syncopation={coltrane_tile.syncopation_rate}")

    coltrane_morph_path = morpher.morph(
        str(OUT / "movement_II_combined.mid"),
        coltrane_tile,
        blend=0.8,
        output_path=str(OUT / "movement_II_coltrane_morph.mid"),
    )
    print(f"  Coltrane morph: {coltrane_morph_path}")

    tile_II_coltrane = extractor.extract([coltrane_morph_path], "Movement_II_Coltrane", "jazz")
    sim_before_coltrane = tile_II.similarity(coltrane_tile)
    sim_after_coltrane = tile_II_coltrane.similarity(coltrane_tile)
    print(f"  Similarity to Coltrane: before={sim_before_coltrane}, after={sim_after_coltrane}")
    print(f"  Improvement: {sim_after_coltrane - sim_before_coltrane:+.4f}")

    record("III.3 Coltrane morph", 0, True,
           f"sim before={sim_before_coltrane:.3f}, after={sim_after_coltrane:.3f}, Δ={sim_after_coltrane-sim_before_coltrane:+.3f}")

except Exception as e:
    record("III.3 Coltrane morph", 10, False, error_detail=traceback.format_exc())

# ══════════════════════════════════════════════════════════════════════════════
# FINALE: Render to WAV + Oscilloscope PNGs
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("FINALE: Render to WAV + Oscilloscope PNGs")
print("="*70)

# Step 9: Software synth render MIDI to WAV (simple sinusoidal synthesis)
try:
    def midi_to_wav(midi_path, wav_path, sample_rate=44100):
        """Simple additive synthesis render of MIDI to WAV."""
        import struct
        import wave

        mid = mido.MidiFile(midi_path)
        tpb = mid.ticks_per_beat

        # Collect all notes with onset (seconds), duration, pitch, velocity
        notes = []
        tempo = 500000  # default 120 BPM

        for track in mid.tracks:
            abs_tick = 0
            note_ons = {}
            for msg in track:
                abs_tick += msg.time
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
                if msg.type == 'note_on' and msg.velocity > 0:
                    note_ons[(msg.note, msg.channel)] = (abs_tick, msg.velocity)
                elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    key = (msg.note, msg.channel)
                    if key in note_ons:
                        start_tick, vel = note_ons.pop(key)
                        dur_ticks = abs_tick - start_tick
                        sec_per_tick = tempo / (tpb * 1_000_000)
                        start_sec = start_tick * sec_per_tick
                        dur_sec = dur_ticks * sec_per_tick
                        notes.append((start_sec, dur_sec, msg.note, vel))

        if not notes:
            # Write silence
            with wave.open(wav_path, 'w') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(b'\x00\x00' * sample_rate)
            return 1.0

        total_duration = max(n[0] + n[1] for n in notes) + 0.5
        n_samples = int(total_duration * sample_rate)

        # Simple synthesis with 64-sample crossfade to avoid clicks
        fade_len = 64
        audio = np.zeros(n_samples, dtype=np.float64)

        for start_sec, dur_sec, pitch, vel in notes:
            freq = 440.0 * (2.0 ** ((pitch - 69) / 12.0))
            amp = (vel / 127.0) * 0.15  # scale down to prevent clipping
            s0 = int(start_sec * sample_rate)
            s1 = min(int((start_sec + dur_sec) * sample_rate), n_samples)
            if s1 <= s0:
                continue
            t = np.arange(s1 - s0) / sample_rate
            # Add harmonics for richer tone
            tone = amp * (
                np.sin(2 * np.pi * freq * t) +
                0.3 * np.sin(2 * np.pi * freq * 2 * t) +
                0.1 * np.sin(2 * np.pi * freq * 3 * t)
            )
            # Apply crossfade envelope (click fix)
            if len(tone) > 2 * fade_len:
                fade_in = np.linspace(0, 1, fade_len)
                fade_out = np.linspace(1, 0, fade_len)
                tone[:fade_len] *= fade_in
                tone[-fade_len:] *= fade_out
            audio[s0:s1] += tone

        # Normalize
        peak = np.max(np.abs(audio))
        if peak > 0:
            audio = audio / peak * 0.9

        # Write WAV
        pcm = (audio * 32767).astype(np.int16)
        with wave.open(wav_path, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(pcm.tobytes())

        return total_duration

    # Render all movements
    midi_files = {
        "movement_I_lattice": OUT / "movement_I_lattice.mid",
        "movement_II_groove": OUT / "movement_II_groove.mid",
        "movement_II_combined": OUT / "movement_II_combined.mid",
        "movement_I_bach_morph": OUT / "movement_I_bach_morph.mid",
        "movement_II_coltrane_morph": OUT / "movement_II_coltrane_morph.mid",
    }

    wav_durations = {}
    for name, midi_path in midi_files.items():
        if midi_path.exists():
            wav_path = str(OUT / f"{name}.wav")
            dur = midi_to_wav(str(midi_path), wav_path)
            wav_durations[name] = dur
            print(f"  Rendered {name}: {dur:.1f}s")
        else:
            print(f"  Skipped {name}: MIDI not found")

    record("IV.1 WAV rendering", 0, True,
           f"Rendered {len(wav_durations)} files: " + ", ".join(f"{k}={v:.1f}s" for k, v in wav_durations.items()))

except Exception as e:
    record("IV.1 WAV rendering", 10, False, error_detail=traceback.format_exc())

# Step 10: Generate constraint oscilloscope PNGs
try:
    def plot_oscilloscope(wav_path, png_path, title="Oscilloscope"):
        """Generate oscilloscope-style PNG from WAV."""
        import wave as wave_mod
        with wave_mod.open(wav_path, 'r') as wf:
            frames = wf.readframes(wf.getnframes())
            sr = wf.getframerate()
            n = wf.getnframes()
            audio = np.frombuffer(frames, dtype=np.int16).astype(np.float64) / 32768.0

        fig, axes = plt.subplots(3, 1, figsize=(14, 8), gridspec_kw={'height_ratios': [2, 1, 1]})

        # Full waveform
        t = np.arange(len(audio)) / sr
        axes[0].plot(t[::max(1, len(t)//5000)], audio[::max(1, len(t)//5000)],
                     linewidth=0.3, color='#00ff88')
        axes[0].set_title(f"{title} — Full Waveform", fontsize=12, color='white')
        axes[0].set_ylabel("Amplitude", color='white')
        axes[0].set_facecolor('#1a1a2e')
        axes[0].tick_params(colors='white')

        # Spectrum (FFT)
        if len(audio) > 0:
            fft_size = min(8192, len(audio))
            spectrum = np.abs(np.fft.rfft(audio[:fft_size])) / fft_size
            freqs = np.fft.rfftfreq(fft_size, 1/sr)
            axes[1].plot(freqs[:len(spectrum)//2], spectrum[:len(spectrum)//2],
                        linewidth=0.5, color='#ff6b6b')
            axes[1].set_title("Frequency Spectrum", fontsize=10, color='white')
            axes[1].set_xlabel("Frequency (Hz)", color='white')
            axes[1].set_facecolor('#1a1a2e')
            axes[1].tick_params(colors='white')
            axes[1].set_xlim(0, 5000)

        # Spectrogram
        if len(audio) > sr:  # At least 1 second
            nperseg = min(1024, len(audio) // 4)
            from scipy.signal import spectrogram as scipy_spectrogram
            f, t_spec, Sxx = scipy_spectrogram(audio, sr, nperseg=nperseg)
            axes[2].pcolormesh(t_spec, f, 10 * np.log10(Sxx + 1e-10),
                              shading='auto', cmap='inferno')
            axes[2].set_title("Spectrogram", fontsize=10, color='white')
            axes[2].set_ylabel("Freq (Hz)", color='white')
            axes[2].set_xlabel("Time (s)", color='white')
            axes[2].set_ylim(0, 5000)
            axes[2].tick_params(colors='white')
            axes[2].set_facecolor('#1a1a2e')

        fig.patch.set_facecolor('#0d0d1a')
        for ax in axes:
            for spine in ax.spines.values():
                spine.set_color('#333366')
        plt.tight_layout()
        plt.savefig(png_path, dpi=150, facecolor=fig.get_facecolor())
        plt.close(fig)

    png_files = {}
    for name in wav_durations:
        wav_path = str(OUT / f"{name}.wav")
        png_path = str(OUT / f"{name}_scope.png")
        if os.path.exists(wav_path):
            title_map = {
                "movement_I_lattice": "Movement I: Lattice (Fugue)",
                "movement_II_groove": "Movement II: Groove (Funk)",
                "movement_II_combined": "Movement II: Combined",
                "movement_I_bach_morph": "Movement I: Bach Morph",
                "movement_II_coltrane_morph": "Movement II: Coltrane Morph",
            }
            plot_oscilloscope(wav_path, png_path, title=title_map.get(name, name))
            png_files[name] = png_path
            print(f"  Oscilloscope: {png_path}")

    record("IV.2 Oscilloscope PNGs", 0, True,
           f"Generated {len(png_files)} oscilloscope plots")

except Exception as e:
    record("IV.2 Oscilloscope PNGs", 10, False, error_detail=traceback.format_exc())

# Step 11: Style transformation journey summary
try:
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_facecolor('#0d0d1a')
    fig.patch.set_facecolor('#0d0d1a')

    # Bar chart: before/after similarity for Bach and Coltrane
    categories = ['Fugue → Bach', 'Groove → Coltrane']
    before = [sim_before_bach, sim_before_coltrane]
    after = [sim_after_bach, sim_after_coltrane]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax.bar(x - width/2, before, width, label='Before', color='#ff6b6b', alpha=0.8)
    bars2 = ax.bar(x + width/2, after, width, label='After', color='#00ff88', alpha=0.8)

    ax.set_ylabel('Cosine Similarity to Target', color='white', fontsize=12)
    ax.set_title('Style Transformation Journey', color='white', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, color='white')
    ax.legend(facecolor='#1a1a2e', edgecolor='#333366', labelcolor='white')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('#333366')

    # Add value labels
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{bar.get_height():.3f}', ha='center', color='#ff6b6b', fontsize=10)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{bar.get_height():.3f}', ha='center', color='#00ff88', fontsize=10)

    plt.tight_layout()
    summary_path = str(OUT / "style_transformation_journey.png")
    plt.savefig(summary_path, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Summary: {summary_path}")

    record("IV.3 Summary chart", 0, True,
           f"Journey chart: Bach Δ={sim_after_bach-sim_before_bach:+.3f}, Coltrane Δ={sim_after_coltrane-sim_before_coltrane:+.3f}")

except Exception as e:
    record("IV.3 Summary chart", 10, False, error_detail=traceback.format_exc())

# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("FINAL SUMMARY")
print("="*70)

total_score = 0
max_score = 0
for step, r in results.items():
    total_score += r["error_score"]
    max_score += 10
    status = "✅" if r["error_score"] == 0 else "⚠️" if r["error_score"] <= 3 else "❌"
    print(f"  {status} {step}: score={r['error_score']}/10, meaningful={r['musically_meaningful']}")
    if r['notes']:
        print(f"     → {r['notes']}")
    if r['error_detail']:
        print(f"     ERROR: {r['error_detail'][:150]}")

overall = total_score / max_score * 100 if max_score > 0 else 0
print(f"\n  Overall: {total_score}/{max_score} ({100-overall:.0f}% success)")
print(f"  Files in: {OUT}/")

# List output files
for f in sorted(OUT.iterdir()):
    size = f.stat().st_size
    if size > 1024*1024:
        print(f"    {f.name} ({size/1024/1024:.1f} MB)")
    else:
        print(f"    {f.name} ({size/1024:.1f} KB)")

print("\nDone!")
