# Learning Paths

Pick your path. Follow it start to finish. Every step links to something real — a doc to read, a script to run, a concept to sit with.

Each path is self-contained. You don't need to have read anything else first.

---

## Path 1: "I'm a Musician Who Codes"

**Goal:** Compose a piece using the constraint tools and render it to audio.
**Time:** ~3 hours (2 hours core + 1 hour exploration)

| # | Step | Time |
|---|------|------|
| 1 | Read [START-HERE.md](START-HERE.md) Part 1–3 — the big picture | 15 min |
| 2 | Install: `pip install constraint-theory-core` | 1 min |
| 3 | Run [lattice basics](constraint-theory-core/examples/lattice_basics.py) — see the lattice snap into place | 10 min |
| 4 | Install: `pip install counterpoint-engine` | 1 min |
| 5 | Run [basic counterpoint](counterpoint-engine/examples/basic_counterpoint.py) — generate your first fugue | 15 min |
| 6 | Read the [counterpoint-engine README](https://github.com/SuperInstance/counterpoint-engine) — understand species counterpoint | 10 min |
| 7 | Install: `pip install holonomy-harmony groove-analyzer` | 1 min |
| 8 | Run [Coltrane vs Pachelbel](holonomy-harmony/examples/coltrane_vs_pachelbel.py) — see holonomy in action | 10 min |
| 9 | Run [groove analysis](groove-analyzer/examples/analyze_grooves.py) — feel the deadband | 10 min |
| 10 | Install: `pip install constraint-synth` | 1 min |
| 11 | Run [demo synth](constraint-synth/examples/demo_synth.py) — render to WAV | 10 min |
| 12 | Run the [full pipeline](examples/full_pipeline_demo.py) — everything wired together | 15 min |
| 13 | Try [jazz voicings](jazz-voicing-engine/examples/jazz_arrangement.py) | 15 min |
| 14 | Explore [style-dna](style-dna/) — extract musical personality from MIDI | 20 min |

**What you'll have at the end:** A composed-and-rendered piece of music, plus an intuition for how constraints create structure instead of restricting creativity.

---

## Path 2: "I'm a Mathematician / Physicist"

**Goal:** Understand the mathematical framework and see the proofs.
**Time:** ~4 hours

| # | Step | Time |
|---|------|------|
| 1 | Read [START-HERE.md](START-HERE.md) — full document | 20 min |
| 2 | Read [DEEP-MATH-MUSICAL-STRUCTURE.md](DEEP-MATH-MUSICAL-STRUCTURE.md) — group theory, Betti numbers, Lyapunov exponents | 40 min |
| 3 | Read [SIGNAL-SUBSTRATE.md](SIGNAL-SUBSTRATE.md) — constraint as signal at every scale | 30 min |
| 4 | Read [CONSTRAINT-SUBSTRATE-DESIGN.md](CONSTRAINT-SUBSTRATE-DESIGN.md) — the API contract and mathematical specs | 30 min |
| 5 | Read [CHINESE-MUSIC-CONSTRAINT-THEORY.md](CHINESE-MUSIC-CONSTRAINT-THEORY.md) — wǔxíng as Laman rigidity | 30 min |
| 6 | Read [INDIAN-ARABIC-CONSTRAINT-THEORY.md](INDIAN-ARABIC-CONSTRAINT-THEORY.md) — rāga and maqām through constraint algebra | 40 min |
| 7 | Examine [constraint-substrate/rust/src/lib.rs](constraint-substrate/rust/src/lib.rs) — the math in code | 20 min |
| 8 | Run tests: `cd constraint-substrate/rust && cargo test` | 5 min |
| 9 | Read [ARCHITECTURE-DEEP-THINK.md](ARCHITECTURE-DEEP-THINK.md) — performance analysis | 30 min |
| 10 | Read [ASSEMBLY-FIRST-SYNTH-DESIGN.md](ASSEMBLY-FIRST-SYNTH-DESIGN.md) — 64 voices in 54ns | 30 min |

**What you'll have at the end:** A rigorous understanding of the algebraic topology, rigidity theory, and dynamical systems underlying the entire framework.

---

## Path 3: "I'm an Audio Engineer / Producer"

**Goal:** Use the tools to make real music.
**Time:** ~2 hours

| # | Step | Time |
|---|------|------|
| 1 | Read [START-HERE.md](START-HERE.md) Part 1–3 | 15 min |
| 2 | Run `./demo/setup.sh` — install everything | 5 min |
| 3 | Run the [full pipeline demo](examples/full_pipeline_demo.py) — idea to audio | 10 min |
| 4 | Read [SOUND-PARAMETER-ATLAS.md](SOUND-PARAMETER-ATLAS.md) — the 85 dials that matter | 30 min |
| 5 | Explore [constraint-synth presets](constraint-synth/examples/) — Bach Organ, Joplin Piano, Aphex Glitch | 20 min |
| 6 | Try [groove-analyzer](groove-analyzer/) — analyze your own MIDI grooves | 15 min |
| 7 | Try [spline-midi-smooth](spline-midi-smooth/) — smooth your automation curves | 10 min |
| 8 | Read [AI-BAND-DESIGN.md](AI-BAND-DESIGN.md) — PLATO rooms as musician personas | 30 min |

**What you'll have at the end:** Working familiarity with the sound-design surface, plus presets you can bend toward your own productions.

---

## Path 4: "I'm a Software Engineer Integrating This"

**Goal:** Embed constraint primitives in a production system.
**Time:** ~3 hours

| # | Step | Time |
|---|------|------|
| 1 | Read [START-HERE.md](START-HERE.md) Part 5–6 — integration and deployment | 10 min |
| 2 | Read [CONSTRAINT-SUBSTRATE-DESIGN.md](CONSTRAINT-SUBSTRATE-DESIGN.md) — the API contract | 20 min |
| 3 | Choose your language and read the implementation: | 20 min |
|   | → Rust: [constraint-substrate/rust/](constraint-substrate/rust/) | |
|   | → C: [constraint-substrate/c/](constraint-substrate/c/) | |
|   | → Python: [constraint-substrate/python/](constraint-substrate/python/) | |
| 4 | Run tests in your chosen language | 5 min |
| 5 | Read [INTEGRATION-LAYER-DESIGN.md](INTEGRATION-LAYER-DESIGN.md) — builder pattern | 20 min |
| 6 | Read [DAW-INTEGRATION-REPORT.md](DAW-INTEGRATION-REPORT.md) — real-time performance | 15 min |
| 7 | Explore [flux-tensor-midi](https://github.com/SuperInstance/flux-tensor-midi) — tensor representation of MIDI | 20 min |
| 8 | Read the [roadmap](flux-tensor-midi/ROADMAP.md) — what's coming | 10 min |
| 9 | **Build something:** use constraint-substrate in a toy project | 60 min |

**What you'll have at the end:** A working integration in your language of choice, plus a clear mental model of the substrate API surface.

---

## Path 5: "I'm Curious and Non-Technical"

**Goal:** Understand the ideas without touching code.
**Time:** ~1 hour

| # | Step | Time |
|---|------|------|
| 1 | Read [START-HERE.md](START-HERE.md) Part 1–4 — concepts, analogies, the "why" | 30 min |
| 2 | Skim [SOUND-PARAMETER-ATLAS.md](SOUND-PARAMETER-ATLAS.md) — look at the diagrams and analogies | 15 min |
| 3 | Skim [CHINESE-MUSIC-CONSTRAINT-THEORY.md](CHINESE-MUSIC-CONSTRAINT-THEORY.md) — cultural connections between music and mathematics | 15 min |
| 4 | If intrigued, try the [web playground](demo/playground.html) — click around, no install needed | 15 min |

**What you'll have at the end:** A genuine understanding of the core insight — that music, across every culture, is structured by constraint, and that these constraints have a shared mathematical shape.

---

## Path 6: "I Want to Understand the AI Agent System"

**Goal:** Understand PLATO, sunset agents, and the fleet architecture.
**Time:** ~3 hours

| # | Step | Time |
|---|------|------|
| 1 | Read [START-HERE.md](START-HERE.md) Part 3 — the PLATO rooms section | 5 min |
| 2 | Read [AI-BAND-DESIGN.md](AI-BAND-DESIGN.md) — rooms as musician personas | 40 min |
| 3 | Read the [plato-core README](https://github.com/SuperInstance/plato-core) — tile lifecycle | 15 min |
| 4 | Read the [plato-types README](https://github.com/SuperInstance/plato-types) — Lamport clocks, provenance | 10 min |
| 5 | Read the [plato-mcp README](https://github.com/SuperInstance/plato-mcp) — MCP integration | 10 min |
| 6 | Read the [sunset-ecosystem README](https://github.com/SuperInstance/sunset-ecosystem) — agent lifecycle | 15 min |
| 7 | Read the [fleet-stack README](https://github.com/SuperInstance/fleet-stack) — deployment | 10 min |
| 8 | Read the [forgemaster README](https://github.com/SuperInstance/forgemaster) — the agentic compiler | 20 min |
| 9 | Explore the fleet coordination files in [forgemaster/fleet/](forgemaster/fleet/) | 30 min |

**What you'll have at the end:** A clear picture of how autonomous agents collaborate to compose, perform, and evolve music — and how to build your own agent rooms.

---

## Path 7: "I Want the Cross-Cultural Deep Dive"

**Goal:** The grand tour of musical civilizations through the lens of constraint theory.
**Time:** ~4 hours

| # | Step | Time |
|---|------|------|
| 1 | Read [START-HERE.md](START-HERE.md) Part 4 — the cultural thesis | 10 min |
| 2 | Read [DEEP-MATH-MUSICAL-STRUCTURE.md](DEEP-MATH-MUSICAL-STRUCTURE.md) — the universal math beneath the diversity | 40 min |
| 3 | Read [CHINESE-MUSIC-CONSTRAINT-THEORY.md](CHINESE-MUSIC-CONSTRAINT-THEORY.md) — wǔxíng, pentatonic rigidity | 40 min |
| 4 | Read [INDIAN-ARABIC-CONSTRAINT-THEORY.md](INDIAN-ARABIC-CONSTRAINT-THEORY.md) — rāga, maqām, and constraint algebra | 50 min |
| 5 | Read [COMPOSER-MIDI-SOURCES.md](COMPOSER-MIDI-SOURCES.md) — where to get real composer data | 20 min |
| 6 | Read [STYLE-DNA-DESIGN.md](STYLE-DNA-DESIGN.md) — decomposing composer personality into parameters | 40 min |
| 7 | Run [style-dna examples](style-dna/examples/) — extract personality from MIDI files | 20 min |
| 8 | Read [SOUND-PARAMETER-ATLAS.md](SOUND-PARAMETER-ATLAS.md) — the "10 new paradigms" section | 30 min |

**What you'll have at the end:** A deep appreciation that Bach, Coltrane, Ravi Shankar, and a Beijing opera singer are all solving the same constraint satisfaction problem — just with different variables, different bounds, and different tastes in objective functions.

---

*These paths overlap intentionally. If you finish yours and want more, the adjacent paths are where the interesting connections live.*
