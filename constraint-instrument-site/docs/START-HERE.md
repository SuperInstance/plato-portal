# The Constraint Instrument — Start Here

*An instrument for musicians who think in shapes, not symbols.*

---

## Part 1: What Is This?

The Constraint Instrument is a tool that helps you hear the shape of music. Every piece of music you've ever played or listened to is built from constraints — the scale pins down which notes are allowed, the tempo pins down when they land, the chord progression pins down where the tension lives. You already know this intuitively: when you feel a V7 resolving to I, you're feeling a constraint releasing. The instrument makes those shapes tangible. You choose a constraint terrain (the harmonic landscape you're playing over) and a mode (the way the instrument interacts with you), and it generates music that follows those rules — or tells you what rules you're already following when you play.

Think of it as a practice partner, a compositional sketchpad, and a diagnostic tool rolled into one. It doesn't replace your ears. It sharpens them.

---

## Part 2: Install

One command:

```bash
pip install constraint-instrument && python3 -m constraint_instrument generate --mode ella --terrain blues --bars 4 --output my_first_solo.wav
```

That installs the instrument and generates a four-bar blues solo in the style of Ella Fitzgerald's phrasing logic. Play the WAV file. You just used the instrument.

Requirements: Python 3.9+, ~200MB disk for the full install (includes audio render pipeline). Works on macOS, Linux, and Windows.

---

## Part 3: Listen

After install, play the built-in demo:

```bash
python3 -m constraint_instrument demo
```

This produces a 30-second audio file and plays it. Here's what you're hearing:

| Section | Time | Terrain | What's happening |
|---------|------|---------|-----------------|
| **Blues** | 0:00–0:10 | `blues` | A 12-bar blues with classic dominant-7 voicings. The constraint lattice is loose — lots of blue notes that sit between the cracks of the 12-tone grid. You can hear the snap operation pulling pitches toward the nearest scale degree. |
| **Bebop** | 0:10–0:18 | `chromatic` | The terrain tightens. Chromatic passing tones fill the gaps between chord tones. The lattice snaps harder — every pitch locks to a precise semitone, but the harmonic rhythm doubles. More notes, less breathing room. |
| **Ballad** | 0:18–0:26 | `modal` | The terrain opens up. The constraint is no longer "which notes" but "how long." Notes sustain, space becomes the instrument. The funnel shape dominates — wide attacks, long releases. |
| **Fade** | 0:26–0:30 | `silence` | All constraints release. The consensus that held the tempo together dissolves. |

Each section is a different constraint terrain. The instrument navigates between them the way a musician navigates between feels — not by switching presets, but by letting the underlying rules change shape.

---

## Part 4: The 7 Modes

A *mode* is not a scale. It's a playing personality — the way the instrument responds to you, or the way it generates music on its own. Each mode is named after a musician's approach, because the approach *is* the constraint system.

### Parker — Velocity

Charlie Parker played so many notes that people thought it was chaos. It wasn't. Every note served the chord, the beat, and the phrase simultaneously. Parker mode generates high-density lines where every note is a constraint solution — no filler, no waste. Practice with this mode to build speed with intention. If a note doesn't belong, the instrument won't play it, which means every note you hear is a valid choice. Learn to hear why.

### Miles — Space

Miles Davis said it best: "It's not the notes you play, it's the notes you don't play." Miles mode generates music by removing constraints rather than adding them. The result is wide-open phrasing where the silence between notes does as much harmonic work as the notes themselves. Practice with this mode to develop your sense of when not to play.

### Ella — Flow

Ella Fitzgerald's phrasing was a river — continuous, unbroken, always finding the path of least resistance through the changes. Ella mode generates melodic lines that prioritize smooth voice leading and connected phrases. No awkward jumps, no stranded endings. Practice with this mode to develop legato phrasing and melodic continuity across chord changes.

### Monk — Disruption

Thelonious Monk played wrong notes on purpose. But they were the *right* wrong notes — dissonances that resolved in unexpected ways, creating tension that ordinary harmony couldn't reach. Monk mode introduces controlled disruptions: intentional constraint violations that resolve within one or two beats. Practice with this mode to expand your comfort zone with dissonance and surprise.

### Bach — Structure

J.S. Bach wrote music where every voice is independent but every voice belongs. The constraint is structural rigidity — enough connections to be stable, not so many that everything locks up. Bach mode generates multi-voice counterpoint where each voice follows its own logic while the whole remains coherent. Practice with this mode to develop independence of voices and an ear for counterpoint.

### Coltrane — Exploration

John Coltrane pushed past the boundaries of the harmony, venturing into harmonic territories that the chord symbols didn't explicitly allow — but that the underlying constraint structure made inevitable. Coltrane mode generates lines that explore the outer limits of the current terrain, using higher winding numbers and deeper lattice traversal. Practice with this mode to develop your ability to navigate outside changes while maintaining a thread back home.

### Jobim — Warmth

Antonio Carlos Jobim wrote music that feels like a sunset — warm, bittersweet, harmonically rich but never harsh. Jobim mode generates music with extended harmonies (9ths, 11ths, 13ths), gentle syncopation, and smooth voice leading through complex chords. Practice with this mode to develop your ear for color and your touch for tenderness.

---

## Part 5: The 17 Terrains

A *terrain* is the harmonic and rhythmic landscape the instrument operates over. Changing the terrain changes everything — which notes are available, how much rhythmic freedom exists, how tension builds and releases.

| Terrain | Character | Key constraint |
|---------|-----------|---------------|
| `blues` | Raw, vocal, between-the-cracks | Loose pitch lattice with blue notes |
| `major` | Bright, stable, resolved | Standard diatonic snap |
| `minor` | Dark, tense, inward | Flattened 3rd/6th/7th snap |
| `dorian` | Jazzy minor, funky | 6th stays major, 7th flat |
| `mixolydian` | Bluesy major, dominant | Flat 7th over major triad |
| `phrygian` | Spanish, dark, exotic | Flat 2nd creates tension |
| `lydian` | Dreamy, floating, bright | Sharp 4th lifts the ceiling |
| `chromatic` | Dense, bebop, all notes | Every semitone available |
| `whole-tone` | Floating, unresolved | Symmetric 6-note lattice |
| `pentatonic` | Open, folk, universal | 5-note minimal rigidity |
| `octatonic` | Symmetric, modern, edgy | Alternating whole/half steps |
| `modal` | Open, spacious, time-based | Constraint on duration, not pitch |
| `free` | No pitch constraints | Only rhythm and dynamics |
| `silence` | No constraints | The release — consensus dissolves |
| `raga` | Microtonal, rule-governed | śruti lattice with path constraints |
| `maqam` | Quarter-tone, journey | Hamiltonian path through tonal centers |
| `custom` | You define it | Arbitrary constraint specification |

Each terrain corresponds to a specific lattice geometry. The `blues` terrain, for example, uses a 12-tone lattice with relaxed snap parameters (pitches can sit between scale degrees). The `raga` terrain uses a 22-śruti lattice with directional constraints (certain notes must be approached from specific directions). The `custom` terrain accepts a JSON specification of your own constraints — see the [API Reference](API-REFERENCE.md).

---

## Part 6: The Diagnostic

Goodman is the diagnostic engine inside the instrument. Named after Benny Goodman — a musician whose technical precision was legendary — Goodman listens to what you play and tells you what constraints you're already following, and which ones you're fighting against.

### How it works

1. **You play.** Feed Goodman a MIDI file, a live MIDI stream, or an audio recording (it transcribes audio using the built-in pitch tracker).

2. **Goodman analyzes.** It decomposes your playing into five constraint dimensions:
   - **Snap tightness:** How precisely do your pitches land on scale degrees? Are you bending, sliding, or hitting dead center?
   - **Funnel shape:** How do your notes attack and release? Sharp staccato, smooth legato, or somewhere between?
   - **Winding:** How much harmonic distance do you cover? Do you stay home, or do you wander?
   - **Structural independence:** If you're playing multiple voices, how independent are they? (If single-voice, this measures phrase independence.)
   - **Consensus:** How consistent is your time? Are you locked to a grid, floating, or somewhere in the pocket?

3. **Goodman reports.** You get a constraint profile — a fingerprint of your playing style. It might say:
   - "Your snap tightness is high on chord tones but loose on passing tones — good bebop vocabulary, but your approach notes are inconsistent."
   - "Your winding number stays below 2 in every phrase — you're staying close to home. Try venturing to the outer tones."
   - "Your consensus is drifting — your internal clock slows by ~3 BPM over the course of a chorus. Practice with a click at half-time."

4. **Goodman prescribes.** Based on your profile, it suggests specific terrains and modes to practice with. Think of it as a constraint-aware practice routine.

```bash
python3 -m constraint_instrument diagnose --input my_playing.mid
```

The output includes the five-dimension profile, a text summary, and recommended practice modes.

---

## Part 7: The Monitor

The Monitor is the invisible engineer running behind everything. You don't interact with it directly — it ensures that the instrument's output always satisfies the constraints you've set.

### What it does

- **Validates** every generated note against the current terrain's lattice before it reaches your ears. If a note would violate a constraint, the Monitor snaps it to the nearest valid pitch — or flags it as an intentional violation (in Monk mode, for example).
- **Tracks holonomy** across the entire piece. If the harmonic winding accumulates too much tension without resolution, the Monitor nudges the generator toward a cadence.
- **Maintains consensus** across multi-voice output. When four voices are playing, the Monitor ensures they share a common time base — the same consensus that keeps a rhythm section in the pocket.
- **Logs everything.** Every constraint check, every snap, every consensus adjustment is logged. If you want to understand *why* the instrument made a particular choice, the Monitor's logs tell the full story.

### Why it matters

Most music software generates output and hopes it sounds good. The Monitor guarantees it's structurally sound before you hear it. This is the difference between "sounds like music" and "is music" — the constraint satisfaction is mathematically exact, not approximate.

The Monitor runs in real time and adds less than 0.1ms of latency per constraint check. You won't notice it's there. That's the point.

---

## Part 8: What's Happening Mathematically

If you want to go deeper than the musician-friendly descriptions above, here's the mathematical skeleton:

### The Five Primitives

All music constraint operations reduce to five mathematical shapes:

1. **Snap** — Quantization to a lattice. Pitch snapping is quantization on Z/12Z (or Z/22Z for microtonal systems). The operation is: given a continuous input x, find the nearest lattice point ℓ such that ‖x − ℓ‖ is minimized over the lattice.

2. **Funnel** — A deadband filter. The deadband is an interval [−ε, ε] within which the output doesn't change. This creates the attack-sustain-release shape: wide at the boundaries (sensitive to input), narrow at the center (stable). Mathematically, it's a hysteresis operator.

3. **Winding** — Holonomy tracking. As a melody moves through tonal space (represented as a Tonnetz graph), the winding number counts net harmonic displacement. Zero winding = returned to tonic. Non-zero winding = you're in a different key than where you started.

4. **Structure** — Rigidity checking. Using Laman's theorem from graph theory: a structure with n vertices is minimally rigid when it has exactly 2n − 3 edges, and every subset of k vertices spans at most 2k − 3 edges. This determines whether multi-voice counterpoint is structurally sound.

5. **Consensus** — Distributed agreement. Modeled as a Kuramoto-coupled oscillator system. Each voice is an oscillator; the consensus parameter (coupling strength) determines how tightly they synchronize. High coupling = tight unison. Low coupling = free polyrhythm.

### Scale Invariance

The same five operations appear at every timescale of music — from individual audio samples (microseconds) to entire musical traditions (centuries). Only the units change; the math doesn't. This is the *signal substrate conjecture*: constraint = signal = music at every scale.

### For the full mathematical treatment

→ [constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core) — the Rust crate implementing all five primitives from scratch

→ [CONSTRAINT-SUBSTRATE-DESIGN.md](https://github.com/SuperInstance/superinstance/blob/main/CONSTRAINT-SUBSTRATE-DESIGN.md) — the full design document

→ [SIGNAL-SUBSTRATE.md](https://github.com/SuperInstance/superinstance/blob/main/SIGNAL-SUBSTRATE.md) — the scale-invariance conjecture

→ [DEEP-MATH-MUSICAL-STRUCTURE.md](https://github.com/SuperInstance/superinstance/blob/main/DEEP-MATH-MUSICAL-STRUCTURE.md) — group theory, Betti numbers, and Lyapunov exponents in music

---

## Part 9: Join the Project

The Constraint Instrument is part of the [SuperInstance](https://github.com/SuperInstance) ecosystem — a collection of over 1,500 repositories exploring the mathematical structure of music and beyond.

### Get involved

- **GitHub:** [github.com/SuperInstance/constraint-instrument](https://github.com/SuperInstance/constraint-instrument)
- **Report bugs:** Open an issue on GitHub
- **Contribute terrain definitions:** Fork the repo, add a terrain spec to `terrains/`, submit a PR
- **Contribute mode definitions:** Same process — add a mode to `modes/`
- **Discuss:** GitHub Discussions on the constraint-instrument repo

### Related projects

| Project | What it does |
|---------|-------------|
| [constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core) | The mathematical engine (Rust) |
| [counterpoint-engine](https://github.com/SuperInstance/counterpoint-engine) | Constraint-satisfaction composition |
| [holonomy-harmony](https://github.com/SuperInstance/holonomy-harmony) | Chord progressions with direction |
| [groove-analyzer](https://github.com/SuperInstance/groove-analyzer) | Extract rhythmic feel from recordings |
| [style-dna](https://github.com/SuperInstance/style-dna) | Decompose any performance into a constraint profile |
| [constraint-synth](https://github.com/SuperInstance/constraint-synth) | Math becomes audio |
| [constraint-viz](https://github.com/SuperInstance/constraint-viz) | Interactive visualizations |

### License

MIT. Use it, modify it, build on it. Just give credit.

---

*The Constraint Instrument is built on the insight that every musical tradition on Earth uses the same five constraint shapes — snap, funnel, winding, structure, and consensus — at every timescale. The instrument makes those shapes audible.*
