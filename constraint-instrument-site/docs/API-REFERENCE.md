# API Reference — The Constraint Instrument

*Every public class, method, and parameter. Usage examples for each.*

---

## Installation

```bash
pip install constraint-instrument
```

Requires Python 3.9 or later. The package includes pre-built wheels for macOS (ARM64 + x86_64), Linux (x86_64 + ARM64), and Windows (x86_64). The constraint engine is a Rust core compiled to native code via PyO3 — no external dependencies.

---

## Quick Start

```python
from constraint_instrument import Session, Terrain, Mode

session = Session(mode=Mode.MONK, terrain=Terrain.BLUES)
audio = session.generate(bars=8, bpm=120)
audio.export("monk_blues.wav")
```

---

## Module Structure

```
constraint_instrument/
├── Session              # Main entry point
├── Mode                 # Playing personality enum
├── Terrain              # Harmonic landscape enum
├── TerrainSpec          # Custom terrain definition
├── DiagnosticEngine     # Goodman — analyze playing
├── Monitor              # Constraint validation engine
├── Audio                # Rendered audio container
├── ConstraintProfile    # Five-dimension analysis result
├── MonitorLog           # Constraint check log
└── presets/             # Named presets (mode + terrain combos)
```

---

## `Session`

The main entry point. A `Session` represents a single instrument session with a mode, terrain, and set of parameters.

### Constructor

```python
Session(
    mode: Mode = Mode.ELLA,
    terrain: Terrain = Terrain.BLUES,
    bpm: float = 120.0,
    time_signature: tuple[int, int] = (4, 4),
    key: str = "C",
    monitor_enabled: bool = True,
    monitor_log_level: str = "info",  # "debug" | "info" | "warn" | "none"
    seed: int | None = None,         # For reproducible output
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mode` | `Mode` | `Mode.ELLA` | The playing personality. See [Mode](#mode). |
| `terrain` | `Terrain` | `Terrain.BLUES` | The harmonic landscape. See [Terrain](#terrain). |
| `bpm` | `float` | `120.0` | Tempo in beats per minute. Range: 20–300. |
| `time_signature` | `tuple[int, int]` | `(4, 4)` | Time signature as (beats, subdivision). Supported: (2,4), (3,4), (4,4), (5,4), (6,8), (7,8), (3,8), (12,8). |
| `key` | `str` | `"C"` | Root key. Any note name: C, C#, Db, D, … B. |
| `monitor_enabled` | `bool` | `True` | Enable the Monitor for constraint validation. |
| `monitor_log_level` | `str` | `"info"` | Monitor logging verbosity. `"debug"` logs every constraint check. |
| `seed` | `int \| None` | `None` | Random seed for reproducible generation. Pass the same seed to get the same output. |

### Methods

#### `Session.generate()`

```python
session.generate(
    bars: int = 8,
    voices: int = 1,
    output_format: str = "audio",  # "audio" | "midi" | "both"
) -> Audio | MidiFile | tuple[Audio, MidiFile]
```

Generate music within the session's constraints.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `bars` | `int` | `8` | Number of bars to generate. Range: 1–256. |
| `voices` | `int` | `1` | Number of independent voices. Range: 1–8. Multi-voice uses the structure (rigidity) constraint to ensure independence. |
| `output_format` | `str` | `"audio"` | Output format. `"audio"` returns an `Audio` object. `"midi"` returns a `MidiFile`. `"both"` returns a tuple. |

**Returns:** `Audio`, `MidiFile`, or `tuple[Audio, MidiFile]` depending on `output_format`.

**Example:**

```python
# Single voice, audio output
audio = session.generate(bars=12)

# Four-voice counterpoint
audio = session.generate(bars=16, voices=4)

# Get MIDI for DAW import
midi = session.generate(bars=32, output_format="midi")
midi.save("output.mid")
```

#### `Session.generate_stream()`

```python
session.generate_stream(
    bars_per_chunk: int = 4,
    total_bars: int | None = None,
) -> Generator[Audio, None, None]
```

Generate music as a stream of chunks. Useful for real-time applications and low-latency playback.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `bars_per_chunk` | `int` | `4` | Bars per yielded chunk. |
| `total_bars` | `int \| None` | `None` | Total bars. `None` = infinite stream. |

**Yields:** `Audio` objects, one per chunk.

**Example:**

```python
# Live-stream to audio device
for chunk in session.generate_stream(bars_per_chunk=2, total_bars=64):
    chunk.play(blocking=False)
```

#### `Session.diagnose()`

```python
session.diagnose(
    input: str | MidiFile | Audio,
) -> DiagnosticReport
```

Run the Goodman diagnostic engine on an input. Analyzes the input's constraint profile.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input` | `str \| MidiFile \| Audio` | required | A file path (`.mid`, `.wav`, `.mp3`), a `MidiFile`, or an `Audio` object. Audio inputs are transcribed internally. |

**Returns:** `DiagnosticReport` — see [DiagnosticReport](#diagnosticreport).

**Example:**

```python
report = session.diagnose("my_solo.mid")
print(report.summary)
print(report.profile)
print(report.prescription)
```

#### `Session.get_monitor_log()`

```python
session.get_monitor_log() -> MonitorLog
```

Retrieve the Monitor's constraint check log from the most recent `generate()` or `generate_stream()` call.

**Returns:** `MonitorLog` — see [MonitorLog](#monitorlog).

#### `Session.set_custom_terrain()`

```python
session.set_custom_terrain(spec: TerrainSpec)
```

Replace the session's terrain with a custom specification.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `spec` | `TerrainSpec` | required | Custom terrain definition. See [TerrainSpec](#terrainspec). |

**Example:**

```python
from constraint_instrument import TerrainSpec

my_terrain = TerrainSpec(
    name="hungarian_minor",
    notes=[0, 2, 3, 6, 7, 8, 11],  # semitone offsets from root
    snap_tolerance=0.3,              # how tightly pitches snap (0.0 = strict, 1.0 = free)
    accent_pattern=[1, 0, 1, 0],    # beat accent pattern
    description="Hungarian minor — raised 4th and 7th",
)
session.set_custom_terrain(my_terrain)
```

#### `Session.set_mode()`

```python
session.set_mode(mode: Mode)
```

Change the session's mode mid-session. Takes effect on the next `generate()` call.

---

## `Mode`

An enum of the seven playing personalities.

```python
from constraint_instrument import Mode
```

| Value | Name | Behavior |
|-------|------|----------|
| `Mode.PARKER` | Velocity | High-density, every note is a constraint solution |
| `Mode.MILES` | Space | Wide-open phrasing, silence as constraint release |
| `Mode.ELLA` | Flow | Smooth voice leading, continuous phrases |
| `Mode.MONK` | Disruption | Controlled dissonance, intentional constraint violations |
| `Mode.BACH` | Structure | Multi-voice counterpoint with rigidity constraints |
| `Mode.COLTRANE` | Exploration | Outer-limit harmony, high winding numbers |
| `Mode.JOBIM` | Warmth | Extended harmonies, gentle syncopation, color |

**Example:**

```python
session.set_mode(Mode.MONK)
audio = session.generate(bars=8)
```

---

## `Terrain`

An enum of the 17 built-in harmonic landscapes.

```python
from constraint_instrument import Terrain
```

| Value | Character | Lattice |
|-------|-----------|---------|
| `Terrain.BLUES` | Raw, between-the-cracks | 12-tone, relaxed snap |
| `Terrain.MAJOR` | Bright, resolved | 7-tone diatonic |
| `Terrain.MINOR` | Dark, tense | 7-tone with flat 3/6/7 |
| `Terrain.DORIAN` | Jazzy minor | 7-tone, major 6th |
| `Terrain.MIXOLYDIAN` | Bluesy major | 7-tone, flat 7th |
| `Terrain.PHRYGIAN` | Spanish, dark | 7-tone, flat 2nd |
| `Terrain.LYDIAN` | Dreamy, floating | 7-tone, sharp 4th |
| `Terrain.CHROMATIC` | Dense, all notes | 12-tone, full snap |
| `Terrain.WHOLE_TONE` | Floating, unresolved | 6-tone symmetric |
| `Terrain.PENTATONIC` | Open, universal | 5-tone minimal rigidity |
| `Terrain.OCTATONIC` | Symmetric, modern | 8-tone alternating |
| `Terrain.MODAL` | Spacious, time-constrained | Duration constraints |
| `Terrain.FREE` | No pitch constraints | Rhythm and dynamics only |
| `Terrain.SILENCE` | No constraints | Release / dissolve |
| `Terrain.RAGA` | Microtonal, path-governed | 22-śruti with direction rules |
| `Terrain.MAQAM` | Quarter-tone, journey | 24-TET with Hamiltonian paths |
| `Terrain.CUSTOM` | User-defined | See `TerrainSpec` |

**Example:**

```python
# List all terrains
for t in Terrain:
    print(f"{t.name}: {t.description}")
```

---

## `TerrainSpec`

Define a custom terrain with full control over the constraint parameters.

### Constructor

```python
TerrainSpec(
    name: str,
    notes: list[int],
    snap_tolerance: float = 0.5,
    snap_mode: str = "nearest",        # "nearest" | "gravity" | "directional"
    funnel_attack: float = 0.1,
    funnel_release: float = 0.3,
    accent_pattern: list[int] | None = None,
    winding_limit: float | None = None,
    allowed_intervals: list[int] | None = None,
    forbidden_intervals: list[int] | None = None,
    approach_rules: dict[int, list[int]] | None = None,
    description: str = "",
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | required | Terrain name. Used in logging and output metadata. |
| `notes` | `list[int]` | required | Semitone offsets from root that define the pitch lattice. E.g., `[0, 2, 4, 5, 7, 9, 11]` for major. |
| `snap_tolerance` | `float` | `0.5` | How tightly pitches snap to lattice points. `0.0` = strict (exact pitch only). `1.0` = free (anything goes). |
| `snap_mode` | `str` | `"nearest"` | Snap strategy. `"nearest"` = quantize to closest lattice point. `"gravity"` = weighted by harmonic importance. `"directional"` = approach rules apply (see `approach_rules`). |
| `funnel_attack` | `float` | `0.1` | Attack time in seconds for the note envelope funnel. Short = percussive. Long = smooth. |
| `funnel_release` | `float` | `0.3` | Release time in seconds. Short = abrupt cutoff. Long = fade. |
| `accent_pattern` | `list[int] \| None` | `None` | Beat accent pattern as a list of 1s (accent) and 0s (no accent). E.g., `[1, 0, 1, 0]` for backbeat emphasis. `None` = uniform accents. |
| `winding_limit` | `float \| None` | `None` | Maximum harmonic winding distance from tonic. `None` = no limit. Low values keep you home; high values encourage modulation. |
| `allowed_intervals` | `list[int] \| None` | `None` | Melodic intervals allowed (in semitones). `None` = all. E.g., `[1, 2, 3, 4, 5, 7]` to disallow jumps larger than a fifth. |
| `forbidden_intervals` | `list[int] \| None` | `None` | Melodic intervals explicitly forbidden. Takes precedence over `allowed_intervals`. E.g., `[6]` to forbid tritones. |
| `approach_rules` | `dict[int, list[int]] \| None` | `None` | Direction rules for approaching specific notes. Key = target note offset, value = list of valid approach offsets. E.g., `{11: [7, 9]}` means the leading tone (11) must be approached from the dominant (7) or supertonic (9). This is how raga-style rules work. |
| `description` | `str` | `""` | Human-readable description. Used in logging and documentation. |

**Example:**

```python
# Define a hirajoshi scale (Japanese pentatonic)
hirajoshi = TerrainSpec(
    name="hirajoshi",
    notes=[0, 2, 3, 7, 8],
    snap_tolerance=0.4,
    description="Japanese pentatonic — Hirajoshi scale",
)

# Define a terrain with raga-style approach rules
bhairavi = TerrainSpec(
    name="bhairavi",
    notes=[0, 1, 3, 5, 6, 8, 10, 12],  # with octave
    snap_tolerance=0.2,
    snap_mode="directional",
    approach_rules={
        1: [0, 3],    # flat 2nd approached from root or 4th
        10: [8, 12],  # flat 7th approached from 6th or octave
    },
    description="Bhairavi raga — deep, devotional",
)
```

---

## `Audio`

A container for rendered audio. Returned by `Session.generate()` when `output_format="audio"`.

### Methods

#### `Audio.export()`

```python
audio.export(path: str, format: str = "wav") -> Path
```

Write audio to disk.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `str` | required | Output file path. |
| `format` | `str` | `"wav"` | Audio format: `"wav"`, `"flac"`, `"mp3"`, `"ogg"`. |

**Returns:** `Path` to the written file.

#### `Audio.play()`

```python
audio.play(blocking: bool = True)
```

Play audio through the system's default audio output.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `blocking` | `bool` | `True` | If `True`, block until playback completes. If `False`, return immediately. |

#### `Audio.to_numpy()`

```python
audio.to_numpy() -> np.ndarray
```

Return audio samples as a NumPy array. Shape: `(channels, samples)`. Dtype: `float32`, range `[-1.0, 1.0]`.

#### `Audio.to_bytes()`

```python
audio.to_bytes(format: str = "wav") -> bytes
```

Serialize audio to raw bytes in the specified format.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `sample_rate` | `int` | Sample rate in Hz (typically 44100 or 48000). |
| `duration` | `float` | Duration in seconds. |
| `channels` | `int` | Number of audio channels (1 = mono, 2 = stereo). |
| `samples` | `int` | Total number of samples per channel. |

---

## `MidiFile`

A container for generated MIDI data. Returned by `Session.generate()` when `output_format="midi"`.

### Methods

#### `MidiFile.save()`

```python
midi.save(path: str) -> Path
```

Write MIDI to disk as a standard `.mid` file.

#### `MidiFile.to_bytes()`

```python
midi.to_bytes() -> bytes
```

Serialize to raw MIDI bytes.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `tracks` | `int` | Number of MIDI tracks. |
| `ticks_per_beat` | `int` | MIDI resolution in ticks per beat. |
| `duration_seconds` | `float` | Total duration in seconds at the session's BPM. |

---

## `DiagnosticReport`

Returned by `Session.diagnose()`. Contains the Goodman diagnostic analysis.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `profile` | `ConstraintProfile` | The five-dimension constraint analysis. |
| `summary` | `str` | Human-readable text summary of strengths and weaknesses. |
| `prescription` | `Prescription` | Recommended practice modes and terrains. |
| `scores` | `dict[str, float]` | Numeric scores (0.0–1.0) for each dimension. |
| `raw_data` | `dict` | Raw analysis data for programmatic use. |

### `ConstraintProfile`

The five-dimension analysis of a performance.

| Dimension | Type | Description |
|-----------|------|-------------|
| `snap_tightness` | `float` | How precisely pitches land on scale degrees. 1.0 = perfect, 0.0 = no correlation with the lattice. |
| `funnel_shape` | `FunnelProfile` | Attack and release characteristics. Contains `attack_sharpness`, `sustain_stability`, and `release_shape`. |
| `winding` | `float` | Average harmonic winding per phrase. High = adventurous, low = stays home. |
| `structural_independence` | `float` | Independence of voices (multi-voice) or phrases (single-voice). 1.0 = fully independent. |
| `consensus` | `float` | Temporal consistency. 1.0 = metronomic, 0.0 = arrhythmic. |

### `Prescription`

Goodman's practice recommendations.

| Property | Type | Description |
|----------|------|-------------|
| `recommended_mode` | `Mode` | The mode most likely to strengthen your weak dimension. |
| `recommended_terrain` | `Terrain` | The terrain that targets your gaps. |
| `focus_areas` | `list[str]` | Which dimensions to prioritize (e.g., `["consensus", "winding"]`). |
| `exercise_suggestions` | `list[str]` | Specific practice exercises. |

**Example:**

```python
report = session.diagnose("student_performance.mid")
print(report.summary)
# Output:
# "Strong snap (0.92) and consensus (0.88). Winding is low (0.31) —
#  your phrases tend to stay close to home. Try Coltrane mode over
#  a chromatic terrain to push your harmonic range. Your funnel release
#  is sharp (0.15) — practice with Miles mode to develop longer sustain."

print(report.scores)
# {"snap_tightness": 0.92, "winding": 0.31, "consensus": 0.88, ...}

# Generate the prescribed backing track
prescription = report.prescription
practice_session = Session(
    mode=prescription.recommended_mode,
    terrain=prescription.recommended_terrain,
)
backing = practice_session.generate(bars=32)
backing.export("practice_backing.wav")
```

---

## `MonitorLog`

The Monitor's constraint validation log. Retrieve with `Session.get_monitor_log()`.

### Methods

#### `MonitorLog.to_dict()`

```python
log.to_dict() -> dict
```

Return the full log as a nested dictionary.

#### `MonitorLog.violations()`

```python
log.violations() -> list[ConstraintViolation]
```

Return only the constraint violations (notes that were snapped or adjusted).

#### `MonitorLog.summary()`

```python
log.summary() -> str
```

Human-readable summary of constraint checks performed.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `total_checks` | `int` | Total constraint checks performed. |
| `snaps` | `int` | Number of pitch snap corrections. |
| `consensus_adjustments` | `int` | Number of temporal consensus adjustments. |
| `winding_corrections` | `int` | Number of winding limit enforcement actions. |
| `structure_fixes` | `int` | Number of voice independence corrections. |

**Example:**

```python
audio = session.generate(bars=8)
log = session.get_monitor_log()

print(log.summary())
# "287 constraint checks: 14 snaps (4.9%), 2 consensus adjustments (0.7%),
#  0 winding corrections, 1 structure fix."

for v in log.violations():
    print(f"Bar {v.bar}, Beat {v.beat}: {v.description}")
    # "Bar 3, Beat 2.5: Pitch 61.3 snapped to 61 (C#). Lattice distance: 0.3 semitones."
```

---

## `Presets`

Named combinations of mode + terrain + parameters for common use cases.

```python
from constraint_instrument.presets import (
    bebop_blues,       # Parker mode + blues terrain, 180 BPM
    modal_ballad,      # Miles mode + modal terrain, 72 BPM
    jazz_counterpoint, # Bach mode + dorian terrain, 4 voices
    free_jazz,         # Coltrane mode + free terrain
    bossa_nova,        # Jobim mode + major terrain, 130 BPM
)
```

### Usage

```python
session = bebop_blues(key="Bb")
audio = session.generate(bars=12)
```

### Available Presets

| Preset | Mode | Terrain | BPM | Key | Notes |
|--------|------|---------|-----|-----|-------|
| `bebop_blues` | Parker | Blues | 180 | Bb | Classic bebop blues |
| `modal_ballad` | Miles | Modal | 72 | D | So What vibes |
| `jazz_counterpoint` | Bach | Dorian | 120 | C | 4-voice |
| `free_jazz` | Coltrane | Free | — | — | No tempo constraint |
| `bossa_nova` | Jobim | Major | 130 | G | Gentle syncopation |
| `monk_quartet` | Monk | Chromatic | 140 | Eb | Controlled chaos |
| `ella_scat` | Ella | Blues | 160 | F | Flowing lines |

---

## Command-Line Interface

The instrument ships with a CLI for quick use without writing Python.

### `generate`

```bash
python3 -m constraint_instrument generate \
    --mode ella \
    --terrain blues \
    --bars 8 \
    --bpm 140 \
    --key F \
    --voices 1 \
    --output solo.wav \
    --format wav \
    --seed 42
```

**Flags:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--mode` | `str` | `ella` | One of: parker, miles, ella, monk, bach, coltrane, jobim |
| `--terrain` | `str` | `blues` | One of the 17 terrain names, or a path to a custom terrain JSON file |
| `--bars` | `int` | `8` | Number of bars |
| `--bpm` | `float` | `120` | Tempo |
| `--key` | `str` | `C` | Root key |
| `--voices` | `int` | `1` | Number of voices |
| `--output` | `str` | required | Output file path |
| `--format` | `str` | `wav` | Output format: wav, flac, mp3, midi |
| `--seed` | `int` | random | Random seed for reproducibility |

### `diagnose`

```bash
python3 -m constraint_instrument diagnose \
    --input my_playing.mid \
    --output report.json
```

**Flags:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--input` | `str` | required | Path to input file (.mid, .wav, .mp3) |
| `--output` | `str` | stdout | Path for JSON report output |
| `--terrain` | `str` | auto-detected | Override terrain for analysis context |

### `demo`

```bash
python3 -m constraint_instrument demo [--output demo.wav]
```

Generates and plays the 30-second demo (blues → bebop → ballad → fade). Optional `--output` saves to file instead of playing.

### `viz`

```bash
python3 -m constraint_instrument viz --terrain blues --animate --port 8080
```

Launches an interactive visualization of the constraint structure for the given terrain. Opens in your browser.

**Flags:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--terrain` | `str` | `blues` | Terrain to visualize |
| `--animate` | flag | off | Animate snap/funnel/winding operations |
| `--port` | `int` | `8080` | Local port for the visualization server |

### `tour`

```bash
python3 -m constraint_instrument tour
```

Interactive API tour. Walks through every major API call with inline explanations and examples. Good for developers getting started.

---

## Custom Terrain JSON Format

For CLI use, custom terrains can be specified as JSON files:

```json
{
  "name": "hungarian_minor",
  "notes": [0, 2, 3, 6, 7, 8, 11],
  "snap_tolerance": 0.3,
  "snap_mode": "nearest",
  "funnel_attack": 0.1,
  "funnel_release": 0.3,
  "accent_pattern": [1, 0, 1, 0],
  "winding_limit": null,
  "allowed_intervals": null,
  "forbidden_intervals": [6],
  "approach_rules": null,
  "description": "Hungarian minor — raised 4th and 7th"
}
```

Pass with `--terrain path/to/terrain.json` on the CLI, or load with `TerrainSpec.from_json("path/to/terrain.json")` in Python.

---

## Error Handling

All errors are subclasses of `ConstraintInstrumentError`.

| Error | When it happens |
|-------|----------------|
| `InvalidModeError` | Unknown mode name |
| `InvalidTerrainError` | Unknown terrain name or malformed terrain spec |
| `InvalidKeyError` | Key string not parseable (e.g., `"X#"`) |
| `GenerationError` | Constraint system couldn't find a valid solution (very rare; try relaxing constraints) |
| `DiagnosticError` | Input file couldn't be parsed or transcribed |
| `MonitorViolationError` | Monitor detected an unresolvable constraint violation (shouldn't happen in normal use) |

---

## Performance

- **Generation:** ~50ms for 8 bars, single voice (on modern hardware). Scales linearly with bars and voices.
- **Diagnosis:** ~200ms for a 4-minute MIDI file. Audio transcription adds ~1-2x real-time (so a 4-minute recording takes ~4-8 minutes).
- **Monitor overhead:** < 0.1ms per constraint check. Typically < 1% of generation time.
- **Memory:** ~50MB base + ~10MB per concurrent voice.

For GPU-accelerated generation (needed for very high voice counts or real-time streaming), install the CUDA extension:

```bash
pip install constraint-instrument[cuda]
```

This uses the [constraint-gpu-kernels](https://github.com/SuperInstance/constraint-gpu-kernels) to check constraints at up to 341 billion operations per second on consumer GPUs.

---

## Version

Current version: `0.1.0` (pre-release)

The API may change between minor versions during pre-release. Pin your version in production:

```
constraint-instrument>=0.1.0,<0.2.0
```

---

*Questions? Open an issue at [github.com/SuperInstance/constraint-instrument](https://github.com/SuperInstance/constraint-instrument).*
