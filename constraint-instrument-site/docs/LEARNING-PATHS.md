# Learning Paths — The Constraint Instrument

Pick your path. Follow it in order. Each step links to something real.

---

## Path 1: "I'm a Musician"

**Goal:** Generate music that sounds like music, then understand why it works.
**Time:** ~2 hours

| # | Step | Time | Notes |
|---|------|------|-------|
| 1 | Read [START-HERE.md](START-HERE.md) Parts 1–3 | 10 min | The "what" and the demo |
| 2 | Install and run the demo: `pip install constraint-instrument && python3 -m constraint_instrument demo` | 5 min | Listen to the four terrains |
| 3 | Generate your first solo: `python3 -m constraint_instrument generate --mode ella --terrain blues --bars 8 --output blues_solo.wav` | 5 min | Try Ella over blues |
| 4 | Change the mode, keep the terrain: generate with `--mode monk` and `--mode miles` over the same blues changes | 5 min | Hear how the same terrain sounds different under different constraint personalities |
| 5 | Change the terrain: try `--terrain modal --mode miles` and `--terrain chromatic --mode parker` | 5 min | Hear how terrain reshapes the possibilities |
| 6 | Run the diagnostic on your own playing: `python3 -m constraint_instrument diagnose --input your_file.mid` | 10 min | If you have a MIDI file of yourself playing, feed it in. If not, use one of the built-in samples: `--input @samples/parker_confirmation.mid` |
| 7 | Read your diagnostic report. Note which constraint dimensions are strong and which are weak. | 5 min | The five dimensions: snap, funnel, winding, structure, consensus |
| 8 | Practice with the prescribed mode: Goodman recommends a mode/terrain combo based on your diagnostic. Generate a backing track with that combo and practice along. | 30 min | This is the core loop: diagnose → prescribe → practice → re-diagnose |
| 9 | Read [START-HERE.md](START-HERE.md) Parts 4–5 — the modes and terrains in depth | 15 min | Now that you've heard them, the descriptions will click |
| 10 | Explore the [API Reference](API-REFERENCE.md) for custom terrain definitions | 10 min | When you're ready to define your own harmonic worlds |

**What you'll have at the end:** A constraint profile of your own playing, a practice routine tailored to your weak spots, and an intuition for how constraints create musical shape.

---

## Path 2: "I'm a Developer"

**Goal:** Integrate the constraint instrument into your own tools, or build new ones on top of it.
**Time:** ~3 hours

| # | Step | Time | Notes |
|---|------|------|-------|
| 1 | `pip install constraint-instrument` | 1 min | Python 3.9+ |
| 2 | Read the [API Reference](API-REFERENCE.md) — skim all public classes and methods | 15 min | Get the lay of the land |
| 3 | Run the interactive API tour: `python3 -m constraint_instrument tour` | 10 min | Walks you through every major API call with inline explanations |
| 4 | Build a simple generator script: import `constraint_instrument`, create a `Session`, set a mode and terrain, call `generate()`, write to WAV | 20 min | Your first programmatic use |
| 5 | Explore custom terrains: define a terrain as a JSON spec with lattice, snap parameters, funnel shapes, and rhythmic constraints | 20 min | See [API Reference: TerrainSpec](API-REFERENCE.md#terrainspec) |
| 6 | Hook into the Monitor: enable logging on your `Session` and examine the constraint check log after generation | 15 min | Every snap, every consensus adjustment — it's all there |
| 7 | Build a real-time pipeline: feed live MIDI into the diagnostic, get a running constraint profile | 30 min | Requires a MIDI input device or virtual MIDI port |
| 8 | Integrate with your DAW: use the `--output midi` flag to generate MIDI files, or the `--osc` flag to stream to OSC-capable software | 20 min | Works with Ableton, Logic, Reaper, Max/MSP, Pure Data |
| 9 | Read [constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core) — understand the math engine under the hood | 30 min | Rust crate, GPU-accelerated, 341B constraints/sec |
| 10 | Build something new: a web UI, a mobile practice app, a generative album, a teaching tool | 60 min | The API is the same regardless of what you build |

**What you'll have at the end:** A working integration in Python, a custom terrain, and a clear path to building whatever you want on top of the constraint engine.

---

## Path 3: "I'm a Mathematician"

**Goal:** Understand the formal framework, verify the claims, and explore the open problems.
**Time:** ~4 hours

| # | Step | Time | Notes |
|---|------|------|-------|
| 1 | Read [START-HERE.md](START-HERE.md) Part 8 — the mathematical summary | 10 min | The five primitives formalized |
| 2 | Read [CONSTRAINT-SUBSTRATE-DESIGN.md](https://github.com/SuperInstance/superinstance/blob/main/CONSTRAINT-SUBSTRATE-DESIGN.md) | 30 min | The full substrate design, from first principles |
| 3 | Read [SIGNAL-SUBSTRATE.md](https://github.com/SuperInstance/superinstance/blob/main/SIGNAL-SUBSTRATE.md) | 30 min | Scale-invariance: same five shapes at every level |
| 4 | Read [DEEP-MATH-MUSICAL-STRUCTURE.md](https://github.com/SuperInstance/superinstance/blob/main/DEEP-MATH-MUSICAL-STRUCTURE.md) | 40 min | Group theory, Betti numbers, Lyapunov exponents |
| 5 | Examine the five primitives in code: [constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core) source | 30 min | Lattice snap, deadband funnels, holonomy tracking, rigidity checking, metronome consensus |
| 6 | Run the proof suite: `cd constraint-theory-core && cargo test` | 5 min | Verify the formal properties hold |
| 7 | Read the formal proofs: [FORMAL-UNIFIED-THEOREM.md](https://github.com/SuperInstance/superinstance/blob/main/FORMAL-UNIFIED-THEOREM.md) | 20 min | Deadband + snap + lattice convergence |
| 8 | Read the cross-cultural analysis: [INDIAN-ARABIC-CONSTRAINT-THEORY.md](https://github.com/SuperInstance/superinstance/blob/main/INDIAN-ARABIC-CONSTRAINT-THEORY.md) | 40 min | Raga (22-śruti lattice), maqam (Hamiltonian paths), Chinese pentatonic (Laman rigidity) |
| 9 | Explore the [open problems catalog](https://github.com/SuperInstance/superinstance/blob/main/OPEN-PROBLEMS-CATALOG.md) | 20 min | What's not yet proven |
| 10 | Contribute: if you find a proof gap, a stronger bound, or a new connection, open a PR | ongoing | The math is alive |

**What you'll have at the end:** A rigorous understanding of the algebraic topology, rigidity theory, and dynamical systems underlying the instrument, plus a map of open problems to explore.

---

## Path 4: "I'm an Educator"

**Goal:** Use the Constraint Instrument as a teaching tool — for music theory, mathematics, or both.
**Time:** ~2 hours to learn the tool; ongoing curriculum integration

| # | Step | Time | Notes |
|---|------|------|-------|
| 1 | Read [START-HERE.md](START-HERE.md) in full | 20 min | Understand the instrument from the musician's perspective first |
| 2 | Run the demo and listen carefully to each section | 5 min | Blues → bebop → ballad → fade — each is a different constraint world |
| 3 | Use the terrain system as a teaching tool: start students on `pentatonic` (5 notes, hard to sound bad), then move to `major`, `minor`, `blues`, `chromatic` | 15 min | The terrain progression mirrors traditional music theory pedagogy |
| 4 | Demonstrate the five constraint shapes with the built-in visualizer: `python3 -m constraint_instrument viz --terrain blues --animate` | 10 min | Shows the lattice, snap operations, funnel envelopes, winding paths, and consensus fields in real time |
| 5 | Use the diagnostic as a practice assessment tool | 15 min | Students play, Goodman reports — objective feedback on pitch accuracy, timing, phrasing, and independence |
| 6 | Design a lesson plan: "What is a scale?" becomes "What is a snap lattice?" — the same concept, but now students can *see* and *hear* the constraint operation | 30 min | Connects to the math without requiring math prerequisites |
| 7 | For math classes: use the instrument as a concrete example of lattice theory, graph rigidity, coupled oscillators, and algebraic topology | 20 min | The five primitives are teachable at multiple levels — high school through graduate |
| 8 | Explore cross-cultural connections: the `raga` and `maqam` terrains open discussions about how different musical traditions arrive at the same mathematical shapes independently | 15 min | See [INDIAN-ARABIC-CONSTRAINT-THEORY.md](https://github.com/SuperInstance/superinstance/blob/main/INDIAN-ARABIC-CONSTRAINT-THEORY.md) |
| 9 | Read the [API Reference](API-REFERENCE.md) for programmatic curriculum generation | 10 min | Auto-generate exercises at increasing difficulty |

**What you'll have at the end:** A working knowledge of the instrument as a teaching tool, a framework for connecting music theory to mathematics through constraints, and a set of lesson-ready demos.

---

## Where the Paths Cross

- The **musician** who finishes Path 1 and wants to go deeper → Path 3 (math) or Path 2 (dev)
- The **developer** who finishes Path 2 and wants to understand the "why" → Path 3 (math) or Path 1 (musician's ear)
- The **mathematician** who finishes Path 3 and wants to hear the math → Path 1 (listen)
- The **educator** who finishes Path 4 and wants to build tools → Path 2 (dev)

Every path leads back to the same insight: music is structured by constraint, and the constraints have a shared mathematical shape that transcends any single tradition.
