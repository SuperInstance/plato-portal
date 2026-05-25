# Dial — An Esoteric Programming Language for Music

> *"Where code becomes sound, and dials become art."*

## Overview

**dial** is an esoteric programming language where programs are sequences of musical dial positions on a 3D consonance lattice. Each dial setting maps to coordinates `(V, H, S)` representing Vertical consonance, Horizontal motion, and Spectral brightness — the three axes of musical quality.

Programs in dial don't just describe computation — they describe a journey through musical possibility space.

## Language Specification

### Syntax

A dial program consists of lines in one of these forms:

#### Comments
```
# This is a comment
```
Lines starting with `#` are ignored.

#### Dial Commands (sound-producing)
```
V:{float} H:{float} S:{float} [label]
```
- `V` — Vertical consonance (0.0 = pure dissonance, 3.0 = pure consonance)
- `H` — Horizontal motion (0.0 = static, 3.0 = rapid motion)
- `S` — Spectral brightness (0.0 = dark/flat, 3.0 = bright/harmonic-rich)
- `label` — optional identifier for jumps

The three floats define a point in 3D consonance space. The interpreter synthesizes audio at this coordinate using the lattice oscillator model.

#### Variable Assignment
```
let {name} = {expression}
```
Expressions support basic arithmetic (`+`, `-`, `*`, `/`) and variable references.

#### Jumps
```
-> label
```
Unconditional jump to a labeled dial command.

#### Conditional Jumps
```
if {expression} {op} {expression} -> label
```
Where `op` is one of: `<`, `>`, `<=`, `>=`, `==`, `!=`

#### Unplayed Directive
```
unplayed
```
Synthesizes the nearest unexplored region of the consonance lattice. The interpreter tracks which regions have been visited and picks the closest untouched area.

#### Rest
```
rest {duration}
```
Inserts silence for `duration` beats.

#### Tempo
```
tempo {bpm}
```
Sets the tempo in beats per minute (default: 120).

#### Duration
```
dur {beats}
```
Sets the duration of subsequent notes in beats (default: 1).

#### Tradition Hint
```
tradition {name}
```
Hints the oscillator toward a specific tradition's tuning/ornamentation. Traditions include: `carnatic`, `western`, `jazz`, `gamelan`, `blues`, `arabic`, `japanese`, `throat_singing`.

#### Volume
```
vol {0.0-1.0}
```
Sets the volume for subsequent notes.

#### Fade
```
fade {target_vol} {beats}
```
Gradually transitions volume over `beats` duration.

### Semantics

1. **Execution** proceeds line-by-line from top to bottom.
2. Each dial command **produces one note** (or chord) at the specified coordinates.
3. The **consonance score** of a position determines harmonic quality:
   - Positions near tradition clusters sound familiar and pleasant
   - Positions in unexplored regions sound alien, interesting, or chaotic
   - Positions below the random threshold sound like "anti-music"
4. **Transitions** between dial positions create melodic contours.
5. The interpreter **maintains state**: current position, variables, visited regions, tempo, duration, volume.

### Consonance Lattice Model

The 3D space `(V, H, S)` maps to sound via:

| Range | V (Vertical) | H (Horizontal) | S (Spectral) |
|-------|-------------|-----------------|---------------|
| 0.0-1.0 | Dissonant clusters | Glacial/no motion | Sub-bass, dark |
| 1.0-2.0 | Tension | Moderate flow | Mid-range, warm |
| 2.0-3.0 | Consonant harmony | Rapid arpeggiation | Bright, harmonic-rich |

### Tradition Landmarks

Known tradition clusters in the lattice:

| Tradition | V | H | S |
|-----------|---|---|---|
| Western Tonal | 2.72 | 2.05 | 1.80 |
| Carnatic | 2.77 | 3.63 | 2.80 |
| Jazz | 2.30 | 2.50 | 2.10 |
| Gamelan | 1.40 | 1.20 | 2.90 |
| Blues | 2.10 | 2.80 | 1.60 |
| Arabic Maqam | 2.50 | 3.10 | 2.30 |
| Japanese | 1.80 | 1.50 | 2.20 |
| Throat Singing | 2.90 | 0.80 | 3.00 |

### Output

The interpreter produces:
- **WAV audio** — the synthesized output
- **Consonance log** — a JSON file mapping each note to its consonance score and nearest tradition

## Usage

```bash
python dial_interpreter.py program.dial [-o output.wav] [--log log.json] [--sample-rate 44100] [--visualize]
```

### Flags
- `-o` — Output WAV file (default: `output.wav`)
- `--log` — Save consonance log as JSON
- `--sample-rate` — Audio sample rate (default: 44100)
- `--visualize` — Show a 3D plot of the dial positions visited

## Installation

```bash
pip install numpy scipy matplotlib
```

## Example

```dial
# A simple ascending passage
tempo 100
dur 0.5

V:1.0 H:2.0 S:1.0
V:1.5 H:2.0 S:1.5
V:2.0 H:2.0 S:2.0
V:2.5 H:2.0 S:2.5
V:3.0 H:2.0 S:3.0

# Now explore the unknown
unplayed
```

## Philosophy

dial is built on the premise that **musical quality is a function of position in consonance space**. By treating coordinates as the fundamental unit of composition, we can:

- Navigate between traditions smoothly
- Discover unexplored musical territories
- Make the act of programming an act of musical exploration
- Encode musical ideas as geometric journeys

The language is intentionally minimal — the complexity lives in the lattice, not the syntax.

## License

MIT
