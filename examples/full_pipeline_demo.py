#!/usr/bin/env python3
"""
Full Pipeline Demo: From idea to audio using the entire constraint-theory ecosystem.

This demonstrates:
1. Generate counterpoint (counterpoint-engine)
2. Analyze harmony (holonomy-harmony)
3. Apply groove (groove-analyzer)
4. Smooth dynamics (spline-midi-smooth)
5. Map to PLATO rooms (plato-room-musician)
6. Extract/morph style (style-dna)
7. Render to audio (constraint-synth)
"""

import sys
import os
import glob
import tempfile

# Add all repos to path
WORKSPACE = '/home/phoenix/.openclaw/workspace'
for repo in ['counterpoint-engine', 'holonomy-harmony', 'groove-analyzer',
             'spline-midi-smooth', 'plato-room-musician',
             'style-dna', 'constraint-synth']:
    sys.path.insert(0, os.path.join(WORKSPACE, repo))


def main():
    print("=" * 70)
    print("🎵  CONSTRAINT-THEORY MUSIC ECOSYSTEM — FULL PIPELINE DEMO")
    print("=" * 70)

    # ── Step 1: Generate 4-voice first-species counterpoint ────────────
    print("\n── Step 1: Counterpoint Generation ──────────────────────────")
    from counterpoint_engine import CounterpointGenerator, CounterpointResult

    # A simple cantus firmus in C major (ascending then descending)
    cf = [60, 62, 64, 65, 67, 69, 68, 67, 65, 64, 62, 60]
    gen = CounterpointGenerator(cantus_firmus=cf)
    result_4v = gen.generate_n_voices(n_voices=4)

    print(f"   Generated {result_4v.n_voices}-voice counterpoint (species {result_4v.species})")
    print(f"   Constraints satisfied: {result_4v.constraints_satisfied}/{result_4v.constraints_total}")
    for i, voice in enumerate(result_4v.voices):
        print(f"   Voice {i+1}: {voice}")
    assert result_4v.feasible, "Counterpoint generation failed!"
    print("   ✅ Counterpoint generated")

    # Export to MIDI for later rendering
    midi_counterpoint = os.path.join(WORKSPACE, 'examples', '_pipeline_counterpoint.mid')
    result_4v.to_midi(midi_counterpoint, bpm=100)
    print(f"   Saved: {midi_counterpoint}")

    # ── Step 2: Analyze a chord progression with holonomy ──────────────
    print("\n── Step 2: Harmony Analysis (Holonomy) ─────────────────────")
    from holonomy_harmony import analyze_progression, PROGRESSIONS

    # Analyze the Pachelbel Canon progression
    symbols, key_tonic, mode = PROGRESSIONS["pachelbel_canon"]
    analysis = analyze_progression(symbols, key_tonic, mode)
    print(f"   Progression: {' '.join(symbols)}")
    print(f"   Holonomy: {analysis.holonomy.holonomy} (type: {analysis.holonomy.progression_type})")
    print(f"   Stability: {analysis.stability_score:.2f}")
    print(f"   Modulations: {len(analysis.modulations)}")
    print(f"   Modal interchanges: {len(analysis.modal_interchanges)}")
    print("   ✅ Harmony analyzed")

    # ── Step 3: Synthesize a groove ────────────────────────────────────
    print("\n── Step 3: Groove Synthesis ─────────────────────────────────")
    from groove_analyzer import synthesize_groove

    groove_mid = synthesize_groove("Funk", bars=4, seed=42)
    groove_path = os.path.join(WORKSPACE, 'examples', '_pipeline_groove.mid')
    groove_mid.save(groove_path)
    print(f"   Genre: Funk, bars: 4")
    print(f"   Tracks: {len(groove_mid.tracks)}")
    print(f"   Saved: {groove_path}")
    print("   ✅ Groove synthesized")

    # ── Step 4: Smooth CC data with splines ────────────────────────────
    print("\n── Step 4: Spline Smoothing ─────────────────────────────────")
    import numpy as np
    from spline_midi_smooth import cubic_hermite

    # Simulate some stepped CC data (e.g., volume control)
    cc_points = [(float(i), 64 + 30 * (i % 3)) for i in range(16)]
    spline_fn = cubic_hermite(cc_points)

    # Evaluate the smooth curve at higher resolution
    smooth_x = np.linspace(0, 15, 64)
    smooth_y = spline_fn(smooth_x)
    print(f"   Input: {len(cc_points)} stepped CC points")
    print(f"   Output: {len(smooth_y)} smooth interpolated values")
    print(f"   Range: [{smooth_y.min():.1f}, {smooth_y.max():.1f}]")
    print("   ✅ CC data smoothed")

    # ── Step 5: PLATO room → MIDI channel mapping ─────────────────────
    print("\n── Step 5: PLATO Room Mapping ───────────────────────────────")
    from plato_room_musician import SyntheticFetcher, RoomMapper

    fetcher = SyntheticFetcher(seed=42)
    rooms = fetcher.get_rooms()
    mapper = RoomMapper()

    room_names = list(rooms.keys())[:5]
    channels = {name: mapper.channel_for(name) for name in room_names}
    print(f"   Fetched {len(rooms)} synthetic PLATO rooms")
    for name, ch in channels.items():
        print(f"   Room '{name}' → MIDI channel {ch}")
    print("   ✅ Rooms mapped to MIDI channels")

    # ── Step 6: Style DNA extraction & comparison ──────────────────────
    print("\n── Step 6: Style DNA ────────────────────────────────────────")
    from style_dna import StyleExtractor, PERSONALITIES

    extractor = StyleExtractor()
    # Use existing MIDI files in the workspace
    midis = glob.glob(os.path.join(WORKSPACE, '*.mid'))
    if midis:
        try:
            tile = extractor.extract(midis[:3], composer="Demo", era="mixed")
            # Compare against known personalities
            scores = {}
            for name, personality in PERSONALITIES.items():
                scores[name] = tile.similarity(personality)
            best_match = max(scores, key=scores.get) if scores else "N/A"
            best_score = scores.get(best_match, 0)
            print(f"   Analyzed {len(midis[:3])} MIDI files")
            print(f"   Best personality match: {best_match} (similarity={best_score:.3f})")
            if len(scores) > 1:
                sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                for name, score in sorted_scores[:3]:
                    print(f"     {name}: {score:.3f}")
            print("   ✅ Style DNA extracted")
        except Exception as e:
            print(f"   ⚠️  Style extraction skipped: {e}")
            print("   (Continuing without style analysis)")
    else:
        print("   ⚠️  No MIDI files found — skipping style extraction")

    # ── Step 7: Render to audio ────────────────────────────────────────
    print("\n── Step 7: Render to Audio ──────────────────────────────────")
    from constraint_synth import ConstraintSynth, LatticeOscillator, FunnelEnvelope, MIDIRenderer

    synth = ConstraintSynth(
        oscillator=LatticeOscillator(lattice_shape="triangle"),
        envelope=FunnelEnvelope(attack=0.01, decay=0.1, sustain=0.7, release=0.3)
    )

    out_path = os.path.join(WORKSPACE, 'examples', 'full_pipeline_output.wav')

    if os.path.exists(midi_counterpoint):
        # Render the counterpoint MIDI we generated in step 1
        renderer = MIDIRenderer(synth=synth)
        audio = renderer.render(midi_counterpoint)
        synth.to_wav(audio, out_path)
        duration = len(audio) / 44100
        print(f"   Rendered counterpoint MIDI to audio")
    else:
        # Fallback: render a simple C major arpeggio
        melody_notes = [
            (60, 100, 0.5), (64, 100, 0.5), (67, 100, 0.5), (72, 100, 1.0),
            (67, 90, 0.5), (64, 90, 0.5), (60, 80, 1.0),
        ]
        audio = synth.render_melody(melody_notes)
        synth.to_wav(audio, out_path)
        duration = len(audio) / 44100
        print(f"   Rendered C major arpeggio to audio")

    print(f"   Duration: {duration:.1f}s")
    print(f"   Output: {out_path}")
    print("   ✅ Audio rendered")

    # ── Summary ────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("🎉  FULL PIPELINE COMPLETE")
    print("=" * 70)
    print("""
    idea → counterpoint → harmony → groove → smoothing → rooms → style → audio

    Every stage is grounded in constraint theory:
    • Counterpoint = constraint satisfaction (Laman rigidity)
    • Harmony = holonomy (cycle consistency on the tonal graph)
    • Groove = deadband funnel (microtiming converges to a pocket)
    • Smoothing = cubic splines within deadband bounds
    • Rooms = PLATO tile → note mapping
    • Style = topological DNA (Betti numbers, Lyapunov, entropy ratio)
    • Synth = lattice geometry (waveshape IS lattice shape)
    """)


if __name__ == "__main__":
    main()
