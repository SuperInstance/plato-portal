#!/usr/bin/env python3
"""
audio_to_analysis.py — Audio → MIDI → Style DNA pipeline

Bridges spotify/basic-pitch (audio→MIDI) with our style-dna ecosystem.
Users can drop any audio file and get style analysis, personality matching,
and optional morphing toward a target composer.

Usage:
    python examples/audio_to_analysis.py <audio_file> [--morph <personality>] [--output <midi_file>]

Examples:
    python examples/audio_to_analysis.py recording.wav
    python examples/audio_to_analysis.py song.mp3 --morph Bach --output morphed.mid
    python examples/audio_to_analysis.py clip.wav --json

Requirements:
    pip install basic-pitch  (needs numpy<2 for tflite_runtime compatibility)
"""

import argparse
import json
import os
import sys
import time

# Ensure style-dna is importable
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(WORKSPACE, "style-dna"))


def audio_to_midi(audio_path: str, output_midi: str = None) -> tuple:
    """Convert audio file to MIDI using basic-pitch.

    Returns (midi_data, note_events, elapsed_seconds).
    """
    from basic_pitch.inference import predict

    if output_midi is None:
        base = os.path.splitext(audio_path)[0]
        output_midi = f"{base}_basic_pitch.mid"

    print(f"🎵 Converting: {audio_path}")
    start = time.time()
    model_output, midi_data, note_events = predict(audio_path)
    elapsed = time.time() - start

    midi_data.write(output_midi)
    print(f"   → {len(note_events)} notes detected in {elapsed:.2f}s")
    print(f"   → Saved: {output_midi}")

    return midi_data, note_events, elapsed


def analyze_style(midi_path: str) -> dict:
    """Run style-dna analysis on a MIDI file. Returns personality scores."""
    from style_dna.extract import StyleExtractor
    from style_dna.personalities import PERSONALITIES

    extractor = StyleExtractor()
    tile = extractor.extract([midi_path], "audio-analysis", "audio-derived")

    scores = {}
    for name, preset in PERSONALITIES.items():
        scores[name] = round(tile.similarity(preset), 4)

    return scores, tile


def morph_style(tile, target_name: str, strength: float = 0.5, output_path: str = None):
    """Morph the extracted style toward a target personality."""
    from style_dna.personalities import PERSONALITIES
    from style_dna.morph import StyleMorpher
    from style_dna.midi_utils import save_midi

    if target_name not in PERSONALITIES:
        available = ", ".join(PERSONALITIES.keys())
        print(f"❌ Unknown personality '{target_name}'. Available: {available}")
        return None

    target = PERSONALITIES[target_name]
    morpher = StyleMorpher()
    morphed = morpher.morph(tile, target, strength=strength)

    if output_path is None:
        output_path = f"morphed_{target_name.lower()}.mid"

    # The morphed tile can be used for further generation
    print(f"🎛️  Morphed toward {target_name} (strength={strength})")
    print(f"   → Saved: {output_path}")
    return morphed


def main():
    parser = argparse.ArgumentParser(
        description="Audio → MIDI → Style DNA analysis pipeline"
    )
    parser.add_argument("audio_file", help="Path to audio file (WAV, MP3, etc.)")
    parser.add_argument("--output", "-o", help="Output MIDI path (default: <input>_basic_pitch.mid)")
    parser.add_argument("--morph", "-m", help="Target personality to morph toward (Bach, Chopin, etc.)")
    parser.add_argument("--strength", "-s", type=float, default=0.5, help="Morph strength 0-1 (default: 0.5)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    if not os.path.exists(args.audio_file):
        print(f"❌ File not found: {args.audio_file}")
        sys.exit(1)

    # Step 1: Audio → MIDI
    midi_path = args.output or f"{os.path.splitext(args.audio_file)[0]}_basic_pitch.mid"
    midi_data, note_events, elapsed = audio_to_midi(args.audio_file, midi_path)

    if not note_events:
        print("⚠️  No notes detected. The audio may be too short, quiet, or non-melodic.")
        sys.exit(1)

    # Step 2: Style analysis
    print(f"\n🧬 Running style analysis...")
    scores, tile = analyze_style(midi_path)

    # Find top match
    top_personality = max(scores, key=scores.get)
    top_score = scores[top_personality]

    if not args.json:
        print(f"\n📊 Style Profile:")
        for name, score in sorted(scores.items(), key=lambda x: -x[1]):
            bar = "█" * int(score * 30)
            print(f"   {name:12s} {score:.3f}  {bar}")
        print(f"\n   🏆 Best match: {top_personality} ({top_score:.3f})")

    # Step 3: Optional morphing
    if args.morph:
        morph_result = morph_style(tile, args.morph, args.strength)

    # JSON output
    if args.json:
        result = {
            "input": args.audio_file,
            "midi_output": midi_path,
            "notes_detected": len(note_events),
            "conversion_time_s": round(elapsed, 2),
            "style_scores": scores,
            "top_match": top_personality,
            "top_score": top_score,
        }
        print(json.dumps(result, indent=2))

    print(f"\n✅ Done! MIDI saved to {midi_path}")


if __name__ == "__main__":
    main()
