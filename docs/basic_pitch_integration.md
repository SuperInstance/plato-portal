# basic-pitch Integration Notes

## What It Does
[spotify/basic-pitch](https://github.com/spotify/basic-pitch) converts audio files (WAV, MP3, etc.) to MIDI with pitch bend detection. Combined with our style-dna, this creates an **audio→MIDI→style analysis** pipeline.

## Latency
| Audio Duration | Conversion Time | Rate |
|---|---|---|
| 1.6s clip | 0.06s | ~0.04x realtime |
| 12.7s clip | 0.74s (warm) / 12.4s (cold) | ~0.06-0.97x realtime |
| 28.7s clip | ~1.5s (estimated) | ~0.05x realtime |

First run is slower (model loading). Subsequent runs are fast. **For a 30s clip, expect ~1-2s after warm start.**

## Accuracy
- **Monophonic melodies**: Very good. Clean pitch detection, reasonable rhythm.
- **Polyphonic (piano, organ)**: Decent but not perfect. Misses inner voices, may merge close pitches. Our 12.7s fugue yielded 49 notes (reasonable extraction from a complex piece).
- **Pitch bend**: basic-pitch detects pitch bends, useful for expressive instruments (sax, voice).
- **Short/synthetic clips**: Very short clips (<2s) may produce few notes — expected.

## Limitations
1. **Percussion ignored** — basic-pitch only extracts pitched notes. Drum tracks produce nothing useful.
2. **Polyphony is lossy** — chord voicings may be simplified, inner voices dropped.
3. **No instrument detection** — all notes go to one MIDI track, no program changes.
4. **Requires numpy<2** — tflite_runtime is incompatible with numpy 2.x. This may conflict with other packages (e.g., opencv-python).
5. **No tempo detection** — the MIDI is in absolute time, no tempo map. style-dna handles this, but downstream tools may need one.
6. **16kHz resampling** — internally resamples to 22kHz. Fine for most music, but very high harmonics are lost.

## User Story Impact
**Before**: "Give me a MIDI file and I'll analyze your style."
**After**: "Drop any audio file — MP3, WAV, recording from your phone — and I'll tell you what composer you play like, morph your style, or generate new music in your voice."

This is a **huge** UX win. Most musicians have recordings, not MIDI files. basic-pitch bridges that gap.

## Integration Points
- `examples/audio_to_analysis.py` — ready-to-use CLI bridge script
- Can be called from constraint-synth as a preprocessor
- Could be exposed via API endpoint for web tools

## Dependencies
```
pip install basic-pitch  # pulls in librosa, tflite_runtime, etc.
# WARNING: requires numpy<2
```

## Date
Evaluated 2026-05-22. basic-pitch v0.4.0.
