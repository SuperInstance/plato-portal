# musicpy Integration Evaluation

**Date:** 2026-05-22
**Package:** musicpy v7.12 (⭐1460 on GitHub)
**Evaluated by:** R&D subagent

## Executive Summary

**Recommendation: CONDITIONAL ADOPT** — musicpy is a useful composition front-end that bridges nicely into our constraint theory back-end. Its chord/scale DSL and MIDI I/O fill a real gap (we have theory but poor composition UX). However, it lacks constraint theory, cross-cultural tunings, and style analysis — precisely our differentiators. The integration is complementary, not overlapping.

**Integration depth:** Front-end DSL + MIDI I/O layer. Our ecosystem handles the math; musicpy handles the music representation.

---

## 1. Package Overview

musicpy is a Python music programming language with:
- **Data structures:** `note`, `chord`, `scale`, `piece`, `track` — all theory-aware
- **Arithmetic:** `+`, `-`, `*`, `/` on chords/scales (transpose, invert, stretch)
- **Composition primitives:** chord progressions, arpeggiation, random composing, negative harmony
- **Analysis:** chord detection, scale detection, rhythm analysis, similarity search
- **I/O:** MIDI read/write, MusicXML, JSON, YAML

### Key Stats
- **Version:** 7.12
- **Dependencies:** mido (MIDI), pygame-ce (playback)
- **Install:** `pip install musicpy` (clean install, no conflicts)
- **License:** MIT
- **Python:** 3.7+

---

## 2. Overlap & Complementarity Matrix

| Capability | musicpy | Our Ecosystem | Overlap? | Notes |
|---|---|---|---|---|
| Chord/scale representation | ✅ Rich DSL (`C('Cmaj7')`, `scale('C','dorian')`) | ❌ Minimal (raw MIDI pitch lists) | None | musicpy fills a real gap |
| Pitch operations (transpose, invert) | ✅ `.up()`, `.down()`, `.inversion()` | ⚠️ Partial (lattice snap, interval math) | Low | musicpy is more ergonomic |
| Counterpoint generation | ⚠️ Random composing only | ✅ Full SAT/UNSAT backtracking with Laman proof | None | Our engine is far stronger |
| Lattice quantization | ❌ | ✅ A₂ Eisenstein snap with covering radius proof | None | Our unique capability |
| Laman rigidity | ❌ | ✅ Voice graph is minimally rigid (2N-3 edges) | None | Our unique capability |
| Deadband funnel | ❌ | ✅ ε(t) = ε₀·e^(-λt) convergence model | None | Our unique capability |
| Scale detection | ✅ `detect_scale()`, multiple algorithms | ❌ | None | musicpy adds this |
| Chord analysis | ✅ `chord_analysis()`, `detect()` | ❌ | None | musicpy adds this |
| Style DNA / morphing | ❌ | ✅ StyleTile with 25+ deep invariants | None | Our unique capability |
| Cross-cultural scales | ⚠️ Standard modes (dorian, phrygian, etc.) | ✅ Z/22Z, Z/24Z, Z/53Z microtonal lattices | Low | Our scales go far beyond 12-TET |
| MIDI I/O | ✅ Read/write with instruments, tempo, tracks | ⚠️ Basic mido usage | High | musicpy's MIDI layer is richer |
| MusicXML export | ✅ | ❌ | None | musicpy adds this |
| Rhythm analysis | ✅ `analyze_rhythm()` | ⚠️ Microtiming extraction (groove-analyzer) | Medium | Different angles (structure vs timing) |
| Groove / microtiming | ❌ | ✅ Deadband ε pocket fitting per genre | None | Our unique capability |
| Negative harmony | ✅ `negative_harmony()` | ❌ | None | musicpy adds this |
| Holonomy verification | ❌ | ✅ Cycle consistency in O(log N) | None | Our unique capability |
| Synthesis / rendering | ⚠️ pygame playback only | ✅ Lattice-geometric oscillator → WAV | None | Our synth is far more interesting |
| Experimental music (serial, aleatoric) | ⚠️ Permutation via itertools, random_composing | ⚠️ Constraint-based generation | Low | Neither has deep serialism support |

---

## 3. Proof of Concept Results

**File:** `examples/musicpy_constraint_composition.py`

### Pipeline demonstrated:
1. ✅ **musicpy** defines ii-V-I-vi chord progression — ergonomic chord DSL
2. ✅ **constraint-theory-core** snaps pitches to A₂ lattice — covering radius guarantee
3. ✅ **counterpoint-engine** generates SAT counter-melody — 26/26 constraints satisfied
4. ⚠️ **style-dna** API would work but needs pip install (not on PyPI yet)
5. ✅ **groove-analyzer** API compatible — deadband ε fitting
6. ⚠️ **musicpy MIDI output** works but `piece()` / `track()` API has quirks
7. ✅ **constraint-synth** renders lattice-geometric WAV

### Issues encountered:
- musicpy's `piece()` + `track()` API doesn't compose with `write()` cleanly — needs chord-level writes
- `write()` takes `(chord, bpm, name=...)` not `(piece, name=...)` in practice
- `negative_harmony()` takes `(scale, chord)` not `(chord, scale)` — arg order is non-obvious
- `chord_analysis()` crashes on single-voiced chords — needs multi-note input

### What works beautifully:
- `C('Cmaj7')` — chord construction is ergonomic
- `@` operator for sequential composition — `c1 @ c2 @ c3` 
- `.up()`, `.down()`, `.inversion()` — pitch arithmetic is clean
- Scale objects with mode support (dorian, phrygian, lydian, mixolydian, etc.)
- Our `counterpoint-engine` output (MIDI pitch lists) maps directly to musicpy's `degree_to_note()`

---

## 4. What musicpy Has That We're Missing

### Worth adopting:

1. **Chord DSL** — `C('Cmaj7')`, `C('Dm9')`, etc. We currently work with raw pitch lists. This would massively improve ergonomics for composition demos and education.

2. **Scale objects with modes** — `scale('C', 'dorian')` returns all notes. We have math on Z/nZ groups but no convenient music-facing API.

3. **Chord detection** — `detect()` and `detect_scale()` analyze a set of pitches and return named chords/scales. Useful for reverse-engineering MIDI input.

4. **Negative harmony** — Mirror chords through the axis between tonic and tritone. Simple but musically useful transformation we don't have.

5. **MusicXML export** — Would let our output load into MuseScore, Finale, Dorico.

6. **Sequential composition operator** — The `@` operator to chain chords sequentially is elegant. We should steal this pattern.

7. **Named chord database** — musicpy has an extensive chord type database (jazz chords, extensions, alterations). We have none of this.

### Not worth adopting:
- **pygame playback** — We have constraint-synth for audio rendering
- **`random_composing()`** — Too naive; our constraint-based generation is better
- **JSON/YAML serialization** — We have our own formats

---

## 5. What We Have That musicpy's Missing

### Our unique differentiators (musicpy can't replicate these):

1. **Eisenstein A₂ lattice snap** — Every point snaps within ρ = 1/√3, proved by geometry. musicpy has no lattice theory.

2. **Deadband funnels** — ε(t) = ε₀·e^(-λt) convergence model for temporal constraints. musicpy has no concept of tolerance bands.

3. **Laman rigidity** — Voice graphs are minimally rigid (2N-3 edges, load-bearing). musicpy doesn't model voice independence mathematically.

4. **Counterpoint as SAT/UNSAT** — Every rule returns a proof token. musicpy's "counterpoint" is random note selection.

5. **Cross-cultural microtonal scales** — Z/22Z (Indian), Z/24Z (Arabic), Z/53Z (Turkish). musicpy is 12-TET only.

6. **Style DNA extraction** — Betti numbers, Lyapunov exponents, entropy ratios, holonomy ranges. musicpy has no deep analysis.

7. **Style morphing** — Per-layer adjustments (register, rhythm, harmony) with blend parameter. musicpy has no style transfer.

8. **Holonomy verification** — Cycle consistency checking in O(log N). musicpy has no verification machinery.

9. **Lattice-geometric synthesis** — Oscillator shapes = lattice geometries. musicpy has pygame playback only.

10. **Groove as deadband ε** — Genre-specific pocket fitting (EDM≈3ms, Jazz≈40ms). musicpy has no microtiming analysis.

---

## 6. Integration Architecture

```
┌─────────────────────────────────────────────────┐
│                  User / Composer                  │
│         (writes in musicpy DSL)                   │
│  C('Cmaj7') @ C('Dm7') @ C('G7')                │
└──────────────────┬──────────────────────────────┘
                   │ chord/scale objects
                   ▼
┌──────────────────────────────────────────────────┐
│              musicpy Adapter Layer                │
│  • Extract pitch lists from musicpy chords        │
│  • Convert back to musicpy after processing       │
│  • Handle MIDI I/O via musicpy's rich API         │
└──────┬───────────┬───────────┬───────────────────┘
       │           │           │
       ▼           ▼           ▼
┌────────────┐ ┌─────────┐ ┌──────────┐
│ constraint │ │counter- │ │ style-   │
│  theory    │ │ point   │ │   dna    │
│   core     │ │ engine  │ │          │
│            │ │         │ │          │
│ • snap     │ │ • SAT/  │ │ • extract│
│ • funnel   │ │   UNSAT │ │ • morph  │
│ • holonomy │ │ • Laman │ │ • compare│
└─────┬──────┘ └────┬────┘ └────┬─────┘
      │              │           │
      ▼              ▼           ▼
┌─────────────────────────────────────────────────┐
│              musicpy Output Layer                 │
│  • MIDI write with instruments, tempo, tracks     │
│  • MusicXML export                                │
│  • Or: constraint-synth → WAV                     │
└─────────────────────────────────────────────────┘
```

### Adapter pattern:
```python
# musicpy chord → our pitch list
def musicpy_to_pitches(chord_obj):
    return [n.degree for n in chord_obj.notes]

# our pitch list → musicpy chord
def pitches_to_musicpy(pitch_list):
    return mp.chord([mp.degree_to_note(p) for p in pitch_list])
```

---

## 7. Risks & Concerns

1. **API stability** — musicpy's `write()` API is inconsistent (chord vs piece vs track). Multiple paths to MIDI output with unclear semantics. May break between versions.

2. **12-TET lock-in** — musicpy assumes 12-tone equal temperament throughout. Our Z/22Z, Z/24Z, Z/53Z scales can't be represented natively. We'd need to bypass musicpy's pitch model for microtonal work.

3. **Dependency surface** — pygame-ce is a heavy dependency for what we need (MIDI I/O). We already use mido directly.

4. **Single maintainer** — musicpy appears to be a one-person project. Low bus factor.

5. **License** — MIT is fine for our purposes.

6. **No constraint theory** — musicpy's "composition" is purely generative/random. It doesn't understand why rules exist or prove satisfaction. It can't verify its own output.

---

## 8. Recommended Integration Path

### Phase 1: Composition Front-End (Low effort, high value)
- Use musicpy as the **user-facing composition DSL**
- Users write chord progressions, melodies, and scales in musicpy syntax
- Internally extract pitch lists and run through our constraint pipeline
- Use musicpy's MIDI write for output (richer than our raw mido usage)

### Phase 2: Analysis Import (Medium effort)
- Use `detect_scale()`, `detect()` for MIDI input analysis
- Feed detected structures into style-dna for deep profiling
- Use chord detection to map MIDI input → constraint problems

### Phase 3: Microtonal Bypass (High effort, future)
- Extend musicpy's pitch model or bypass it for Z/22Z, Z/24Z, Z/53Z work
- This is a fork-or-extend decision that depends on community engagement

### NOT recommended:
- Replacing our constraint engine with musicpy's random composing
- Using pygame playback instead of constraint-synth
- Depending on musicpy for any correctness guarantees

---

## 9. Verdict

musicpy is the **composition UX layer we're missing**. Our ecosystem has deep mathematical theory but poor ergonomics for actual music-making. musicpy has great ergonomics but no theory. Together they form a complete pipeline:

**musicpy (compose it) → constraint theory (prove it) → constraint-synth (hear it)**

The integration is real and works. The risks are manageable (API quirks, 12-TET limitation). The value proposition is clear: our tools become usable by musicians, and musicpy gets mathematical rigor it can't provide alone.

**Action:** Add musicpy as an optional dependency. Build the adapter layer. Ship composition demos that show the combined pipeline.
