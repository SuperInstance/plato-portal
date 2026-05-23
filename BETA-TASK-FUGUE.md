# Zero-Shot Task: Compose a Fugue in D Minor
**Time to complete**: ~5 minutes (script execution), ~4 min of debugging broken deps
**Wrong turns**: 4

## Step-by-step log

### 1. Workspace exploration (30s)
- Ran `find` to scan workspace files and directories
- Ran `pip list` to find installed music packages
- **Found**: `counterpoint-engine` directory, `flux-tensor-midi`, `mido`, `constraint-synth`, `groove-analyzer`, `jazz-voicing-engine`
- **Obvious from file names**: `counterpoint-engine/examples/basic_counterpoint.py` — immediately showed me the API

### 2. Reading source code (2 min)
- Read `basic_counterpoint.py` example → showed `CounterpointGenerator`, `Species`, `Scale` API
- Read `generator.py` → discovered `generate_n_voices()` method, `Scale(tonic, mode)`, `VoiceRange`, `CounterpointResult.to_midi()`
- Read `__init__.py` → saw exports, confirmed available classes
- **Key discovery**: `generate_n_voices(n_voices=4, voice_ranges=[...])` does multi-voice generation with Laman rigidity

### 3. Writing the fugue script (2 min)
- Wrote a Python script using the discovered API
- D minor = `Scale(tonic=2, mode="minor")` (D=2 in pitch class)
- Used 4 voice ranges for SATB
- Built fugal structure: staggered subject entries in each voice

### 4. Dependency hell (4 wrong turns, ~4 min)
- **Turn 1**: `ModuleNotFoundError: No module named 'flux_tensor_midi'` — `tensor_output.py` imports it but it's broken
- **Turn 2**: Tried `importlib.util` to bypass `__init__.py` — but `generator.py` itself imports `from counterpoint_engine.rules` which triggers `__init__.py` again
- **Turn 3**: Tried mocking `flux_tensor_midi` — but `tensor_output.py` also imports `flux_tensor_midi.midi.events`
- **Turn 4**: More mock modules needed — `constraint_theory_core.rigidity` also imported by `rules.py` and `laman_counterpoint.py`
- **Solution**: Mocked ALL broken transitive dependencies (`flux_tensor_midi.*`, `constraint_theory_core.*`) with dummy modules before importing

### 5. Successful generation (instant)
- `CounterpointGenerator.generate_n_voices()` worked perfectly
- Generated 4 voices, 222/222 constraints satisfied
- Exported to MIDI via `to_midi()` — but wrote my own MIDI export for more control

### 6. Audio rendering (discovered constraint-synth, 1 min)
- Found `constraint-synth` package already installed
- `MIDIRenderer.render()` + `ConstraintSynth.to_wav()` — worked on first try
- Generated 28.7s WAV file

### 7. Visualization (2 min)
- Wrote a piano-roll visualization using PIL
- Read MIDI back with `mido`, plotted notes as colored rectangles
- Generated 1200x412 PNG

## API Discoveries

### What was obvious from examples
- `CounterpointGenerator(cantus_firmus, species, scale, voice_range)` — basic API clear from example
- `Species.FIRST` enum
- `Scale(tonic, mode)` for key specification
- MIDI note numbers as integers

### What required reading source code
- `generate_n_voices(n_voices, voice_ranges)` — multi-voice generation (not in example)
- `CounterpointResult.to_midi(filename, bpm)` — built-in MIDI export (not in example)
- `CounterpointResult.voices` — list of voice lists
- `CounterpointResult.feasible` — whether generation succeeded
- `VoiceRange(min_pitch, max_pitch)` — explicit pitch bounds per voice
- `constraint-synth`'s `MIDIRenderer` and `ConstraintSynth.to_wav()` — found by reading demo script

### What was confusing
- **Broken dependencies everywhere**: `flux_tensor_midi` and `constraint_theory_core` are imported but not installable. The `__init__.py` eagerly imports `tensor_output` which cascades into broken deps, making the entire package unusable without mocking.
- **No clear "fugue" API**: The engine does counterpoint (note-against-note) but has no fugal structure (subject, answer, episodes). Had to build fugue logic manually.

## Final Result

**Files produced:**
- `fugue_d_minor.mid` (1.1 KB) — 4-track MIDI, 72 BPM, D minor
- `fugue_d_minor.wav` (2.5 MB) — rendered audio, 28.7 seconds
- `fugue_d_minor_pianoroll.png` (7.3 KB) — piano-roll visualization

**Does it sound like a fugue?** Partially. The staggered entry structure is there (bass → tenor → alto → soprano), and the counterpoint engine ensures proper voice leading. However:
- The "fugal answer" is just a transposed subject, not a proper tonal answer
- No episodes (development sections) between entries
- The free counterpoint after subject entries is generated, not composed
- The MIDI rest handling could be cleaner

It's more accurately described as "4-voice first-species counterpoint with staggered subject entries in D minor."

## Friction Score: 6/10

The API itself is well-designed and intuitive. The massive friction came from:
1. **Broken dependencies** (4/10 of the friction) — spent more time mocking modules than writing music
2. **No fugue-specific API** (1/10) — had to build fugal structure from counterpoint primitives
3. **Rest handling in MIDI** (1/10) — the `to_midi()` method doesn't handle rests/staggered entries

## What Would Have Made This Easier?
1. **Lazy imports in `__init__.py`** — Don't eagerly import `tensor_output` with broken deps
2. **A `FugueGenerator` class** or at least a fugal answer helper
3. **An example showing multi-voice or fugue generation**
4. **`constraint-synth` mentioned in the counterpoint-engine docs** — I only found it by accident via `pip list`

## What Surprised You (good)?
- The `generate_n_voices()` method with Laman graph rigidity — serious math under the hood
- 222/222 constraints satisfied — perfect result on first try
- `constraint-synth` rendered audio from MIDI in one line of code
- The API is actually quite clean once you get past the dependency issues

## What Surprised You (bad)?
- The entire package is broken at import time due to missing transitive deps
- No `pip install` can fix it — `flux_tensor_midi` isn't on PyPI and its local install is broken
- The example only shows 2-voice first-species — no multi-voice or advanced usage demo
- `to_midi()` on `CounterpointResult` exists but isn't documented in the example
