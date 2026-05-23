"""
CLI entry point: python -m constraint_instrument

Usage:
    # Quick start — generate and play defaults
    python3 -m constraint_instrument
    python3 -m constraint_instrument --play

    # Customize everything
    python3 -m constraint_instrument --mode parker --terrain bebop --key E --bpm 140 --bars 8

    # Render to file
    python3 -m constraint_instrument --mode ella --terrain blues --output solo.wav

    # Diagnose a MIDI file
    python3 -m constraint_instrument diagnose song.mid

    # Interactive REPL
    python3 -m constraint_instrument --repl

    # List terrains
    python3 -m constraint_instrument --list-terrains
"""

import argparse
import sys
import os

from . import Instrument, TERRAINS
from .instrument import resolve_terrain, TERRAIN_ALIASES, NOTE_TO_MIDI
from .analyzer import ConstraintAnalyzer, print_analysis_report
from .genre_brain import GenreBrain, genre_summary_table


def cmd_quick(args):
    """Generate (and optionally play/save) a performance."""
    # If --genre specified, use GenreBrain to auto-configure
    if getattr(args, 'genre', None):
        brain = GenreBrain(args.genre)
        # argparse defaults are always set; only override genre defaults
        # if user explicitly passed non-default values
        overrides = {
            'key': args.key,
            'bpm': args.bpm,
            'bars': args.bars,
        }
        inst = brain.create_instrument(**overrides)
        # Print genre info
        print(f"  Genre:   {brain.genre}")
    else:
        inst = Instrument(
            mode=args.mode,
            terrain=args.terrain,
            key=args.key,
            bpm=args.bpm,
            bars=args.bars,
        )
    notes = inst.perform()
    print(f"  Mode:    {inst.mode}")
    print(f"  Terrain: {inst.terrain_name}")
    print(f"  Key:     {inst._key} | BPM: {inst.bpm} | Bars: {inst.bars}")
    print(f"  Notes:   {len(notes)}")

    if args.output:
        path = inst.render(args.output)
        print(f"  Saved:   {path}")
    elif args.play:
        # Render to temp wav and play
        genre_tag = f"{args.genre}" if args.genre else f"{args.mode}"
        path = inst.render(f"{genre_tag}_{inst.terrain_name}_{args.key}.wav")
        print(f"  Rendered: {path}")
        print(f"  Playing...")
        ok = inst.play()
        if not ok:
            print(f"  (Audio playback unavailable. File saved at {path})")
    else:
        # Default: render to wav
        genre_tag = f"{args.genre}" if args.genre else f"{args.mode}"
        default_out = f"{genre_tag}_{inst.terrain_name}_{args.key}.wav"
        path = inst.render(default_out)
        print(f"  Saved:   {path}")

    if args.diagnose:
        print()
        report = inst.diagnose()
        print(report)


def cmd_diagnose_file(args):
    """Diagnose a MIDI file."""
    from .goodman import GoodmanEngine
    from .terrain import TERRAINS as T

    filepath = args.midi_file
    if not os.path.exists(filepath):
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    inst = Instrument(mode="goodman", terrain="blues")
    report = inst.diagnose(filepath)
    print(report)


def cmd_analyze(args):
    """Analyze external music through the constraint lens."""
    analyzer = ConstraintAnalyzer()
    filepath = args.input_file

    if not os.path.exists(filepath):
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    # Detect file type
    ext = os.path.splitext(filepath)[1].lower()
    is_audio = ext in ('.wav', '.mp3', '.flac', '.ogg', '.m4a', '.aac', '.wma', '.aiff')

    # Parse overrides
    key = getattr(args, 'key', None)
    if key and key != 'C':
        from .instrument import resolve_key
        try:
            key = resolve_key(key)
        except (ValueError, TypeError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        key = None

    terrain_name = getattr(args, 'terrain', None)
    bpm = getattr(args, 'bpm', None)

    print(f"  Analyzing: {filepath}")
    if is_audio:
        print(f"  (Audio file detected — extracting pitches...)")
        report = analyzer.from_audio(filepath, key=key, terrain_name=terrain_name, bpm=bpm)
    else:
        report = analyzer.from_midi(filepath, key=key, terrain_name=terrain_name, bpm=bpm)

    if report.overall_score == 0 and len(report.orders) == 1 and report.orders[0].order == -1:
        print(f"  Error: {report.orders[0].detail}")
        sys.exit(1)

    # Detect terrain
    terrain_info = None
    notes = None
    # Re-load notes for terrain detection
    if not is_audio:
        try:
            engine_temp = GoodmanEngine()
            notes = engine_temp._load_midi(filepath)
        except Exception:
            pass

    if notes:
        terrain_info = analyzer.detect_terrain(notes)

    # Print full report
    output = print_analysis_report(report, terrain_info=terrain_info)
    print(output)

    # Prescriptions
    if report.prescriptions:
        print("\n📋 PRESCRIPTIONS:")
        for p in report.prescriptions:
            print(f"\n  [{p.order_name}] Focus: {p.focus}")
            print(f"  {p.rationale}")
            for ex in p.exercises:
                print(f"    • {ex}")


def cmd_compare(args):
    """Compare two performances."""
    analyzer = ConstraintAnalyzer()

    file_a = args.file_a
    file_b = args.file_b

    for f in [file_a, file_b]:
        if not os.path.exists(f):
            print(f"Error: file not found: {f}", file=sys.stderr)
            sys.exit(1)

    label_a = args.label_a if hasattr(args, 'label_a') and args.label_a else os.path.basename(file_a)
    label_b = args.label_b if hasattr(args, 'label_b') and args.label_b else os.path.basename(file_b)

    print(f"  Comparing: {label_a} vs {label_b}")

    # Load each
    report_a = analyzer.from_midi(file_a)
    report_b = analyzer.from_midi(file_b)

    result = analyzer.compare(report_a, report_b, label_a, label_b)

    # Also show terrain matches
    terrain_a = analyzer.detect_terrain(file_a)
    terrain_b = analyzer.detect_terrain(file_b)

    if terrain_a.get('terrain'):
        print(f"  {label_a} terrain: {terrain_a['terrain']} (conf: {terrain_a['confidence']:.0%})")
    if terrain_b.get('terrain'):
        print(f"  {label_b} terrain: {terrain_b['terrain']} (conf: {terrain_b['confidence']:.0%})")

    print()
    print(result["verdict"])


def cmd_terrains(args):
    """List all available terrains."""
    print(f"Available terrains ({len(TERRAINS)}):\n")
    # Group: show aliases
    shown = set()
    for name in sorted(TERRAINS.keys()):
        t = TERRAINS[name]
        aliases = [k for k, v in TERRAIN_ALIASES.items() if v == name and k != name]
        alias_str = f"  (aliases: {', '.join(aliases)})" if aliases else ""
        print(f"  {name:25s} {t.description[:60]}{alias_str}")
    print()


def cmd_repl(args):
    """Interactive REPL mode."""
    import readline  # noqa — enables arrow keys

    # Initial state
    state = {
        'mode': args.mode,
        'terrain': args.terrain,
        'key': args.key,
        'bpm': args.bpm,
        'bars': args.bars,
    }
    inst = None

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  Constraint Instrument REPL                                 ║")
    print("║  Commands: mode, terrain, key, bpm, bars, generate,        ║")
    print("║            play, render, diagnose, morph, info, help, quit ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not line:
            continue

        parts = line.split()
        cmd = parts[0].lower()

        if cmd in ('quit', 'exit', 'q'):
            print("Bye.")
            break

        elif cmd == 'help':
            print("Commands:")
            print("  mode <name>          Set mode (parker, miles, ella, etc.)")
            print("  terrain <name>       Set terrain (blues, bebop, delta_blues, etc.)")
            print("  key <note>           Set key (C, Eb, F#, etc.)")
            print("  bpm <number>         Set tempo")
            print("  bars <number>        Set number of bars")
            print("  generate [bars]      Generate a performance")
            print("  play                 Play the last performance")
            print("  render <file>        Render to WAV/MID file")
            print("  diagnose             Diagnose the last performance")
            print("  morph <from> <to>    Morph between terrains")
            print("  info                 Show current state")
            print("  genre <name>         Load genre preset (auto-configure mode, terrain, weights)")
            print("  modes                List available modes")
            print("  quit                 Exit")

        elif cmd == 'mode':
            if len(parts) < 2:
                print(f"Current mode: {state['mode']}")
            else:
                m = parts[1].lower()
                if m in Instrument.MODES:
                    state['mode'] = m
                    inst = None  # reset
                    print(f"Mode → {m}")
                else:
                    print(f"Unknown mode '{m}'. Available: {', '.join(Instrument.MODES)}")

        elif cmd == 'terrain':
            if len(parts) < 2:
                print(f"Current terrain: {state['terrain']}")
            else:
                try:
                    resolved = resolve_terrain(parts[1])
                    state['terrain'] = resolved
                    inst = None
                    print(f"Terrain → {resolved}")
                except ValueError as e:
                    print(str(e))

        elif cmd == 'key':
            if len(parts) < 2:
                from .instrument import NOTE_TO_MIDI, resolve_key
                k = state.get('_raw_key', state.get('key', 'C'))
                print(f"Current key: {k}")
            else:
                from .instrument import resolve_key
                try:
                    resolved = resolve_key(parts[1])
                    state['key'] = resolved
                    state['_raw_key'] = parts[1]
                    inst = None
                    print(f"Key → {parts[1]} (MIDI {resolved})")
                except (ValueError, TypeError) as e:
                    print(str(e))

        elif cmd == 'bpm':
            if len(parts) < 2:
                print(f"Current BPM: {state['bpm']}")
            else:
                try:
                    state['bpm'] = int(parts[1])
                    if inst:
                        inst.bpm = state['bpm']
                    print(f"BPM → {state['bpm']}")
                except ValueError:
                    print(f"Invalid BPM: {parts[1]}")

        elif cmd == 'bars':
            if len(parts) < 2:
                print(f"Current bars: {state['bars']}")
            else:
                try:
                    state['bars'] = int(parts[1])
                    if inst:
                        inst.bars = state['bars']
                    print(f"Bars → {state['bars']}")
                except ValueError:
                    print(f"Invalid bars: {parts[1]}")

        elif cmd == 'generate':
            override_bars = None
            if len(parts) >= 2:
                try:
                    override_bars = int(parts[1])
                except ValueError:
                    pass

            key_val = state.get('_raw_key', state.get('key', 'C'))
            inst = Instrument(
                mode=state['mode'],
                terrain=state['terrain'],
                key=key_val,
                bpm=state['bpm'],
                bars=override_bars or state['bars'],
            )
            notes = inst.perform()
            print(f"Generated {len(notes)} notes ({inst.bars} bars at {inst.bpm} BPM)")

        elif cmd == 'play':
            if inst is None or inst._last_notes is None:
                print("Nothing to play. Run 'generate' first.")
            else:
                print("Playing...")
                ok = inst.play()
                if not ok:
                    print("(Audio playback unavailable. Install pygame or simpleaudio.)")

        elif cmd == 'render':
            if inst is None or inst._last_notes is None:
                print("Nothing to render. Run 'generate' first.")
            else:
                outfile = parts[1] if len(parts) >= 2 else "output.wav"
                path = inst.render(outfile)
                print(f"Saved → {path}")

        elif cmd == 'diagnose':
            if inst is None or inst._last_notes is None:
                print("Nothing to diagnose. Run 'generate' first.")
            else:
                report = inst.diagnose()
                print(report)

        elif cmd == 'morph':
            if len(parts) < 3:
                print("Usage: morph <source_terrain> <target_terrain>")
            else:
                from .terrain_morph import TerrainMorpher
                try:
                    morpher = TerrainMorpher(parts[1], parts[2])
                    # Show a few blend steps
                    for step in [0.0, 0.25, 0.5, 0.75, 1.0]:
                        t = morpher.blend(step)
                        pct = int(step * 100)
                        print(f"  {pct:3d}% → {t.name} | chromatic: {t.chromatic_density:.2f} | "
                              f"tempo: {t.typical_tempo[0]}-{t.typical_tempo[1]}")
                except ValueError as e:
                    print(str(e))

        elif cmd == 'info':
            key_val = state.get('_raw_key', state.get('key', 'C'))
            print(f"  Mode:    {state['mode']}")
            print(f"  Terrain: {state['terrain']}")
            print(f"  Key:     {key_val}")
            print(f"  BPM:     {state['bpm']}")
            print(f"  Bars:    {state['bars']}")
            if inst and inst._last_notes is not None:
                print(f"  Notes:   {len(inst._last_notes)} (ready)")

        elif cmd == 'genre':
            if len(parts) < 2:
                print(f"Current genre: (none — use 'genre jazz' to load one)")
            else:
                try:
                    from .genre_brain import GenreBrain
                    brain = GenreBrain(parts[1])
                    state['mode'] = brain.get_preset()['default_mode']
                    state['terrain'] = brain.get_preset()['default_terrain']
                    state['bpm'] = brain.get_preset().get('default_bpm', state['bpm'])
                    state['bars'] = brain.get_preset().get('default_bars', state['bars'])
                    state['_genre'] = brain
                    inst = None
                    print(f"Genre → {brain.genre}")
                    print(f"  Mode: {state['mode']} | Terrain: {state['terrain']} | BPM: {state['bpm']} | Bars: {state['bars']}")
                except ValueError as e:
                    print(str(e))

        elif cmd == 'terrains':
            cmd_terrains(None)

        elif cmd == 'modes':
            print(f"Available modes: {', '.join(Instrument.MODES)}")

        else:
            print(f"Unknown command: {cmd}. Type 'help' for commands.")


def main():
    parser = argparse.ArgumentParser(
        prog="constraint_instrument",
        description="Constraint-music instrument — seven modes, infinite terrains.\n"
                    "Just run it to hear music. Customize with flags.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Primary flags (no subcommand needed)
    parser.add_argument("--mode", "-m", default="ella",
                        choices=Instrument.MODES,
                        help="Performance mode (default: ella)")
    parser.add_argument("--terrain", "-t", default="blues",
                        help="Musical terrain (default: blues)")
    parser.add_argument("--key", "-k", default="C",
                        help="Musical key: C, Db, D, Eb, E, F, F#, G, Ab, A, Bb, B (default: C)")
    parser.add_argument("--bpm", "-b", type=int, default=100,
                        help="Tempo in BPM (default: 100)")
    parser.add_argument("--bars", type=int, default=4,
                        help="Number of bars (default: 4)")
    parser.add_argument("--output", "-o", default=None,
                        help="Output file path (.wav or .mid)")
    parser.add_argument("--play", "-p", action="store_true",
                        help="Play through speakers after generating")
    parser.add_argument("--diagnose", "-d", action="store_true",
                        help="Diagnose the generated performance")
    parser.add_argument("--repl", action="store_true",
                        help="Start interactive REPL mode")
    parser.add_argument("--genre", "-g", default=None,
                        help="Genre preset (jazz, hip_hop, techno, classical, education, blues, ambient, gospel). Auto-configures mode, terrain, weights.")
    parser.add_argument("--list-terrains", action="store_true",
                        help="List all available terrains")
    parser.add_argument("--list-genres", action="store_true",
                        help="List all available genre presets")

    # Subcommand: diagnose a MIDI file
    sub = parser.add_subparsers(dest="command")
    diag_parser = sub.add_parser("diagnose", help="Diagnose a MIDI file")
    diag_parser.add_argument("midi_file", help="Path to MIDI file")

    # Subcommand: analyze external music
    analyze_parser = sub.add_parser("analyze", help="Analyze external music (MIDI or audio)")
    analyze_parser.add_argument("input_file", help="Path to MIDI or audio file")
    analyze_parser.add_argument("--terrain", "-t", default=None,
                               help="Override terrain (blues, bebop, delta_blues, etc.)")
    analyze_parser.add_argument("--key", "-k", default=None,
                               help="Override key (C, Eb, F#, etc.)")
    analyze_parser.add_argument("--bpm", "-b", type=int, default=None,
                               help="Override BPM")

    # Subcommand: compare two performances
    compare_parser = sub.add_parser("compare", help="Compare two performances")
    compare_parser.add_argument("file_a", help="First MIDI/audio file")
    compare_parser.add_argument("file_b", help="Second MIDI/audio file")
    compare_parser.add_argument("--label-a", default=None, help="Label for first file")
    compare_parser.add_argument("--label-b", default=None, help="Label for second file")

    args = parser.parse_args()

    if args.command == "diagnose":
        cmd_diagnose_file(args)
    elif args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "compare":
        cmd_compare(args)
    elif args.list_terrains:
        cmd_terrains(args)
    elif args.list_genres:
        print("Available genre presets:\n")
        print(genre_summary_table())
        print()
    elif args.repl:
        cmd_repl(args)
    else:
        cmd_quick(args)


if __name__ == "__main__":
    main()
