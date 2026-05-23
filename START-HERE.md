# START HERE — SuperInstance

*What it is, why it matters, and where to go next.*

---

## Part 1: The Simple Idea

Think about music for a second. Not the complicated theory kind — the everyday kind. A Bach fugue, a Coltrane solo, a J Dilla beat. Different worlds, right?

Here's the thing: they all follow rules. Bach won't let certain notes touch each other. Coltrane builds tension by skirting the edge of the scale. Dilla places his kicks slightly off-grid, but *consistently* off-grid — never random. In every case, something is being constrained. Notes snap to pitches. Rhythms snap to a grid. Harmonies resolve because they're "pulled" toward a home key.

We spent three years figuring out that all of these rules — every single one, across Western classical, jazz, hip-hop, Indian raga, Arabic maqam, and Chinese pentatonic traditions — reduce to the same five mathematical shapes. Not similar shapes. Not analogous shapes. *The same shapes*, operating at different scales of time.

This isn't an academic observation. We built working software around it. Software that composes music, analyzes grooves, generates synthesizer sounds, decomposes a performer's style into its DNA, and renders constraint structures as interactive visualizations — all from the same five mathematical primitives.

The five shapes show up in places beyond music, too: in how distributed systems reach consensus, in how robots plan motion, in how physical systems settle into equilibrium. That's not a coincidence — it's because constraint theory isn't modeling physics. Constraint theory *is* physics. A river doesn't simulate fluid dynamics. It runs them.

But let's start with music, because music is where the math is easiest to hear.

---

## Part 2: The Five Shapes

Every constraint in music — and, it turns out, in a lot of other systems — can be expressed using five primitives. We gave them plain-English names because the math names are unhelpful.

### 1. Snap — The Ball in the Groove

Imagine a roulette wheel. The ball spins, bounces, and eventually settles into a slot. It doesn't stop between slots — it *snaps* to the nearest one. In music, pitch works exactly this way. The continuous space of possible frequencies gets carved into discrete notes. MIDI represents this literally: note 60 is middle C, note 61 is C♯. There's no note 60.5 in the system.

When a singer bends a note up toward the target pitch, you're watching snap in real time. The pitch slides continuously and then "clicks" into place. Different traditions have different snap grids — Western music uses 12 equally-spaced slots per octave, Indian classical uses 22 microtonal divisions, Arabic music uses 24 (with quarter tones). But the operation is the same: continuous input, discrete output.

### 2. Funnel — The Marble Spiraling Down

Think of one of those coin funnel donation jars. You drop a coin in and it spirals in a wide circle, gradually narrowing until it drops through the hole at the center. That's a funnel: start with lots of freedom, converge to a precise point.

Every note in music has a funnel shape. It's called an envelope. The note attacks (wide, noisy, uncertain), sustains (stable), and releases (opens up again). Your mouth does this when you say a syllable — consonants are the wide part, the vowel is the narrow center. Synthesizers literally have ADSR knobs for this: Attack, Decay, Sustain, Release. Each one is a parameter of the funnel.

Phrases have funnels too. A jazz solo starts with simple ideas, narrows into a focused theme, and resolves at the end. A whole piece has a funnel: exposition, development, recapitulation. The same shape at every scale.

### 3. Winding — The Hiker Around the Lake

Picture a hiker walking around a mountain lake. If they go all the way around and end up back where they started, the path is closed — zero winding. But what if they take a detour over a ridge and end up on a *different* lake? Now the path has net winding: they didn't come back to the same place.

In music, this is the difference between a melody that resolves home and one that modulates to a new key. Play C-D-E-F-G-A-B-C and you've walked around the lake — zero winding, home again. Play C-D-E-F-G-A-B and stop on the B, and you're stranded. The B wants to resolve to C so badly that composers call it the "leading tone" — it leads you home.

This shows up everywhere in music theory. Key changes are winding. Modulations are winding. Even a drum pattern that shifts from 4/4 to 7/8 and back has a winding number that tells you whether the rhythmic cycle actually closed or left you in a different metric space than where you started.

### 4. Structure — The Bridge That Holds

A bridge stands because its supports are independent — each one carries its own load, and the failure of one doesn't collapse the others. Engineers call this structural rigidity: enough connections to be stable, but not so many that everything becomes rigidly locked.

In music, the "bridge" is counterpoint — multiple independent voices. Bach's four-part chorales work because each voice is its own melody, but they follow rules that keep them from collapsing into each other. No parallel fifths (that would make two voices act as one, reducing structural independence). No crossing voices (that would confuse which support is which). The rules of counterpoint are literally engineering constraints on the structural rigidity of a musical "bridge."

When the structure is too rigid, the music sounds stiff. When it's too loose, it sounds chaotic. The sweet spot — where every voice is independent but they all belong together — is exactly where the mathematical structure is "minimally rigid." Not a metaphor. The same graph theory that tells civil engineers whether a bridge will stand tells us whether a piece of counterpoint works.

### 5. Agreement — The Band Locking In

Watch a jazz quartet that's never played together before. They start a tune, and for the first few bars the tempo wobbles — the drummer is slightly ahead, the bassist slightly behind. By the bridge, something clicks. They've found a shared tempo without anyone counting off. It's not the metronome tempo. It's *their* tempo, arrived at collectively.

This is consensus — distributed agreement without a central conductor. In computing, it's one of the hardest problems: how do multiple agents agree on a shared state when they can only talk to their neighbors? In music, musicians solve it in real time, using a combination of listening, anticipating, and micro-adjusting.

Groove is the audible trace of this consensus process. When a rhythm section is "in the pocket," they've reached agreement. When they're "pushing" or "laying back," they're intentionally deviating from the agreed time — but the deviation only works *because* the agreement exists. You can't lay back from something you haven't agreed on.

At larger scales, entire musical traditions are consensus agreements. The whole world agreed on A=440Hz as the reference pitch. 4/4 time is a consensus. 12-tone equal temperament is a consensus. These are the deepest agreements — shared reference frames that make musical communication possible.

---

## Part 3: How the Pieces Fit Together

SuperInstance is an ecosystem of software tools built on these five shapes. Here's the story of how they connect, told in the order you'd actually use them.

### First, you need the raw material

The math lives in [constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core) — a Rust crate that implements the five primitives from scratch. Lattice snap, deadband funnels, holonomy tracking, rigidity checking, and metronome consensus, all as composable operations. Everything else in the ecosystem is built on top of this. It's fast (GPU-accelerated variants can check over 341 billion constraints per second on consumer hardware) and it's precise — no floating-point drift, no approximation. The constraints are exact.

### Then you compose

[Counterpoint-engine](https://github.com/SuperInstance/counterpoint-engine) takes the math and turns it into music. You specify rules (like "these voices shouldn't be more than an octave apart" or "resolve leading tones before the cadence") and it generates melodies that satisfy all of them simultaneously. This isn't random generation with a filter — the engine constructs solutions that are mathematically guaranteed to work. Think of it as a SAT solver, but for music.

### You add harmony

[Holonomy-harmony](https://github.com/SuperInstance/holonomy-harmony) handles chord progressions. Its key insight is that a good chord progression has a sense of *direction* — it's moving somewhere, accumulating tension, and then releasing. That's holonomy (winding) at the harmonic level. The engine tracks how far you've wandered from the home key and can either guide you back or intentionally leave you unresolved. It's what turns a random sequence of chords into a progression with narrative.

### You give it groove

[Groove-analyzer](https://github.com/SuperInstance/groove-analyzer) measures the feel of a rhythm, not just the notes. Two drummers playing the same pattern on the same kit at the same tempo sound different because of micro-timing — tiny deviations from the grid that make the rhythm breathe. The analyzer extracts these deviations as data, and the underlying consensus model explains *why* they work: they're structured deviations from an agreed-upon tempo, not random noise.

### You smooth the edges

Digital music has a problem: when you change parameters abruptly, you get zipper noise — audible clicks and steps. [Spline-midi-smooth](https://github.com/SuperInstance/spline-midi-smooth) solves this by running all parameter changes through continuous curves (splines). Instead of jumping from volume 50 to volume 60, you get a smooth ramp. This isn't just cosmetic — the spline math is the same continuous mathematics that the constraint system uses, so smoothed parameters stay inside the constraint envelope.

### You give each voice a personality

In the PLATO system, "rooms" — computational spaces where agents live and work — can become musicians. [plato-room-musician](https://github.com/SuperInstance/plato-room-musician) gives each room its own musical identity: a set of constraints it likes, a range of variability it tolerates, and a style it gravitates toward. Put four rooms together and you get a quartet — four independent voices that play together because they share a consensus framework, not because someone is conducting them.

### You render it to sound

[Constraint-synth](https://github.com/SuperInstance/constraint-synth) turns math into audio. Traditional synthesizers have separate oscillators, filters, and envelopes. In constraint-synth, everything is a constraint: the oscillator shape is constrained by the lattice, the filter cutoff is constrained by the deadband funnel, and the envelope is the funnel itself. One unified model produces every sound, because at the synthesis level, every parameter is the same operation (snap) at a different scale. We call this "everything is epsilon" — more on that below.

### You can study any piece's DNA

[Style-dna](https://github.com/SuperInstance/style-dna) decomposes any recorded performance into its constraint profile: how tight is the snap (are they precisely on pitch or do they bend?), how wide is the funnel (do notes attack sharply or ease in?), how much winding does the melody accumulate, how rigid is the counterpoint, and how tight is the consensus (are they locked to the grid or floating?). Feed it a Coltrane recording and it'll tell you, mathematically, what makes it sound like Coltrane. Feed it Bach and it'll show you a completely different rigidity profile — stiffer structure, but with more winding per voice.

### And visualize the whole thing

[Constraint-viz](https://github.com/SuperInstance/constraint-viz) renders the constraint structure of any piece as interactive graphics. You can see the lattice (which pitches are "in" and which are "out"), the funnel (how each note's envelope shapes the constraint space), the winding path (the melody's journey through tonal space), the rigidity graph (which voices are independent and which have collapsed), and the consensus field (how tightly the ensemble agrees on time). It turns abstract math into something you can see and explore.

---

## Part 4: The Deep Discoveries

*These findings use mathematical modeling as one analytical lens among many. Musical traditions are living practices shaped by communities, performers, and centuries of embodied knowledge. A model illuminates; it does not replace.*

Along the way, we found things we didn't expect. These are the findings that made us realize this wasn't just a neat software project — it was a genuinely new way to understand music.

### Chinese music, seen through constraint theory

The ancient Chinese musical system is based on five elements (wǔxíng): Metal, Wood, Water, Fire, and Earth. These aren't arbitrary labels — they're arranged in a cycle that can be modeled, through the lens of graph theory, as a structure called a Laman-rigid graph. In graph theory, a Laman-rigid graph is the minimum set of connections needed to make a structure stable: no fewer, no more. The Chinese pentatonic scale (five notes, no semitones) can be modeled with this property.

Here's the striking part: Chinese musicians discovered this by ear, over two thousand years ago. They didn't know about graph theory. They didn't need to. The constraint structure is so fundamental to how pitch works that the human ear finds it naturally. We can now prove mathematically that the pentatonic's "covering radius" (the maximum distance any pitch can be from the nearest scale tone) is larger than the Western chromatic scale — which is exactly why Chinese melodies sound more "open" and Western melodies sound more "directed." Both are optimal structures, but optimized for different things.

→ Read more in [INDIAN-ARABIC-CONSTRAINT-THEORY.md](INDIAN-ARABIC-CONSTRAINT-THEORY.md) (which includes the Chinese pentatonic analysis)

### Indian raga is a living constraint program

Western music theory treats scales as static sets of notes. Indian classical music treats ragas as complete rule systems. A raga specifies not just which notes to use, but which to emphasize, which to avoid, how to approach them, what ornaments are appropriate, what time of day to play, and what mood to evoke. It's not a scale. It's a running program.

Mathematically, a raga is a constraint profile on the 22-śruti microtonal lattice (Z/22Z, for the algebraically inclined). The 22 śruti aren't equally spaced — they cluster around the 12 Western semitones, but with enough resolution to express nuances that 12-TET can't touch. The raga's rules define which parts of this lattice are "active" (strong attractors), which are "soft" (approach but don't linger), and which are "forbidden" (avoid entirely). Performers navigate this lattice in real time, and the best ones do it with a holonomy that traces the raga's emotional arc.

→ Read more in [INDIAN-ARABIC-CONSTRAINT-THEORY.md](INDIAN-ARABIC-CONSTRAINT-THEORY.md)

### Arabic maqam is a journey through a landscape

An Arabic maqam (mode) isn't just a set of notes — it's a prescribed path through tonal centers. The performer follows a sequence: start here, visit this center, wander to that one, build tension, and resolve back. Through constraint theory, this can be modeled as a Hamiltonian path — a route that visits each node exactly once. The maqam system encodes these paths as performance practice, and the quarter-tone divisions (24-TET) give the lattice enough resolution to express microtonal inflections that Western notation literally can't write down.

The relationship between taqsim (solo improvisation in a maqam) and the underlying constraint program is especially elegant. The performer isn't freely improvising over a scale — they're tracing a path through a landscape, with the constraint structure providing both the route and the guardrails. Freedom exists inside the constraints, not outside them.

→ Read more in [INDIAN-ARABIC-CONSTRAINT-THEORY.md](INDIAN-ARABIC-CONSTRAINT-THEORY.md)

### The same pattern appears at every scale

This was the discovery that tied everything together. The five primitives — snap, funnel, winding, structure, consensus — show up at *every* timescale of music, from the individual audio sample (0.00002 seconds) to centuries of musical tradition.

At the sample level, amplitude quantization is snap. Slew rate limiting is a funnel. Phase accumulation is winding. The harmonic series is structure. The sample clock is consensus.

At the note level, pitch quantization is snap. The ADSR envelope is a funnel. Melodic contour is winding. Voice independence is structure. The tempo grid is consensus.

At the phrase level, harmonic resolution is snap. Rubato is a funnel. Key drift is winding. Formal constraints are structure. Ensemble timing is consensus.

At the piece level, cadence resolution is snap. The tempo arc is a funnel. The modulation cycle is winding. Sonata form is structure. The shared understanding of "where we are in the piece" is consensus.

At the cultural level, scale systems are snap. Genre conventions are funnels. Cultural drift is winding. Music theory itself is structure. Global standards like A=440Hz are consensus.

The math doesn't change. Only the units of time and the units of measurement change. This is what we mean by "constraint = signal = music" — the signal substrate theory.

→ Read the full argument in [SIGNAL-SUBSTRATE.md](SIGNAL-SUBSTRATE.md)

### Everything is epsilon

Here's a finding that surprised us: every parameter on a synthesizer — volume, filter cutoff, resonance, attack time, release time, LFO rate, LFO depth — is the same mathematical operation, just applied at different scales. That operation is snap (quantization to a lattice), and the scale parameter is what we call epsilon (ε).

When ε is large, you get smooth, continuous control — a slow volume fade. When ε is small, you get coarse, discrete control — a square wave. When ε is zero, you get the raw, unconstrained signal. The entire control surface of a synthesizer can be generated by varying a single parameter. This means one well-designed knob could, in principle, control everything.

This isn't just a theoretical observation. The [constraint-synth](https://github.com/SuperInstance/constraint-synth) architecture is built this way: one unified constraint model that generates every parameter. The snap-to-lattice operation at amplitude level gives you the oscillator shape. At envelope level, it gives you ADSR. At pitch level, it gives you quantization. Same math, different epsilon.

→ Read the design rationale in [CONSTRAINT-SUBSTRATE-DESIGN.md](CONSTRAINT-SUBSTRATE-DESIGN.md) and the physics argument in [CONSTRAINT-THEORY-IS-PHYSICS.md](CONSTRAINT-THEORY-IS-PHYSICS.md)

---

## Part 5: For Builders

Want to use this stuff? Here's how to get started.

### Installation

The core library is available as a Rust crate:

```bash
cargo add constraint-theory-core
```

Python bindings:

```bash
pip install constraint-theory-py
```

Or install the full ecosystem:

```bash
git clone https://github.com/SuperInstance/superinstance.git
cd superinstance
./install-all.sh
```

### Your First Demo

The quickest way to see the system in action is the constraint demo — it runs in your browser:

```bash
git clone https://github.com/SuperInstance/constraint-demo.git
cd constraint-demo
python -m http.server 8000
# Open http://localhost:8000
```

You'll see an interactive hexagonal lattice where you can place constraints, watch snap operations, and visualize the five primitives in real time.

### Where to Start

What you want to do determines where you should start:

| If you want to... | Start here |
|---|---|
| Understand the math | [constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core) |
| Compose music | [counterpoint-engine](https://github.com/SuperInstance/counterpoint-engine) |
| Build synthesizers | [constraint-synth](https://github.com/SuperInstance/constraint-synth) |
| Analyze performances | [style-dna](https://github.com/SuperInstance/style-dna) |
| Visualize constraints | [constraint-viz](https://github.com/SuperInstance/constraint-viz) |
| Embed in your project | [constraint-substrate](https://github.com/SuperInstance/constraint-substrate) (Rust/C/Python) |
| Build AI agents | [plato-core](https://github.com/SuperInstance/plato-core) |

### Architecture at a Glance

```
                    ┌─────────────────────┐
                    │   constraint-viz    │  ← See the constraints
                    └──────────┬──────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
┌────────┴────────┐  ┌────────┴────────┐  ┌────────┴────────┐
│   style-dna     │  │ counterpoint-   │  │  groove-        │
│                 │  │ engine          │  │  analyzer       │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │  holonomy-harmony   │  ← Add direction to harmony
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │ spline-midi-smooth  │  ← Continuous curves, no artifacts
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │  constraint-synth   │  ← Math becomes audio
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │constraint-theory-core│  ← The five primitives
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
     ┌────────┴───────┐ ┌─────┴──────┐ ┌───────┴────────┐
     │  snapkit-rs    │ │ deadband-  │ │ eisenstein-    │
     │  (snap ops)    │ │ zig/rs/py  │ │ embed          │
     └────────────────┘ │ (funnels)  │ │ (lattice math) │
                        └────────────┘ └────────────────┘
```

Each box is a separate repo. Each one works standalone. Install only what you need.

---

## Part 6: Further Reading

### "I want to understand the math"

- [CONSTRAINT-SUBSTRATE-DESIGN.md](CONSTRAINT-SUBSTRATE-DESIGN.md) — the full design of the constraint substrate, from first principles
- [CONSTRAINT-THEORY-IS-PHYSICS.md](CONSTRAINT-THEORY-IS-PHYSICS.md) — why constraint theory isn't *like* physics, it *is* physics
- [SIGNAL-SUBSTRATE.md](SIGNAL-SUBSTRATE.md) — the scale-invariance conjecture (supported by cross-level evidence): the same five shapes at every level
- [constraint-theory-math](https://github.com/SuperInstance/constraint-theory-math) — sheaf cohomology, Heyting-valued logic, and GL(9) holonomy (heavy)

### "I want to compose music"

- [counterpoint-engine](https://github.com/SuperInstance/counterpoint-engine) — generate melodies that satisfy arbitrary constraint sets
- [jazz-voicing-engine](https://github.com/SuperInstance/jazz-voicing-engine) — chord voicings that voice-lead smoothly through changes
- [holonomy-harmony](https://github.com/SuperInstance/holonomy-harmony) — chord progressions with a sense of direction

### "I want to build synthesizers"

- [constraint-synth](https://github.com/SuperInstance/constraint-synth) — math becomes audio, one unified constraint model
- [spline-midi-smooth](https://github.com/SuperInstance/spline-midi-smooth) — continuous parameter control without zipper noise
- [deadband-zig](https://github.com/SuperInstance/deadband-zig) / [deadband-rs](https://github.com/SuperInstance/deadband-rs) — deadband filter primitives in Zig and Rust

### "I want to analyze music"

- [style-dna](https://github.com/SuperInstance/style-dna) — decompose any performance into its constraint profile
- [groove-analyzer](https://github.com/SuperInstance/groove-analyzer) — extract micro-timing and rhythmic feel from recordings
- [constraint-viz](https://github.com/SuperInstance/constraint-viz) — interactive visualizations of constraint structures

### "I want the cross-cultural perspective"

- [INDIAN-ARABIC-CONSTRAINT-THEORY.md](INDIAN-ARABIC-CONSTRAINT-THEORY.md) — raga, maqam, śruti, quarter tones, and the universal lattice
- [SIGNAL-SUBSTRATE.md](SIGNAL-SUBSTRATE.md) — how the five shapes appear across all musical traditions
- [CONSTRAINT-THEORY-IS-PHYSICS.md](CONSTRAINT-THEORY-IS-PHYSICS.md) — the connection to physics, robotics, and distributed systems

### "I want to embed this in my project"

- [constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core) — Rust crate, zero dependencies, embedded-friendly
- [constraint-theory-python](https://github.com/SuperInstance/constraint-theory-python) — PyO3 bindings for the Rust core
- [snapkit-rs](https://github.com/SuperInstance/snapkit-rs) / [snapkit-js](https://github.com/SuperInstance/snapkit-js) / [snapkit-python](https://github.com/SuperInstance/snapkit-python) — snap operations in Rust, JavaScript, and Python
- [constraint-gpu-kernels](https://github.com/SuperInstance/constraint-gpu-kernels) — CUDA kernels for high-throughput constraint checking (341B constraints/sec on RTX 4050)

### "I want to understand the AI agent system"

- [plato-core](https://github.com/SuperInstance/plato-core) — base types and mesh registry for PLATO agents
- [sunset-ecosystem](https://github.com/SuperInstance/sunset-ecosystem) — the fleet architecture: how agents coordinate, train, and evolve
- [forgemaster](https://github.com/SuperInstance/forgemaster) — the build system that compiles and deploys constraint-based agents
- [SuperInstance/README.md](SuperInstance/README.md) — package overview and key results

### "I want to see the code"

The SuperInstance GitHub organization contains over 1,500 repositories. Here are the most important ones:

| Repo | Language | What it does |
|------|----------|-------------|
| [constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core) | Rust | The five primitives — the mathematical foundation |
| [counterpoint-engine](https://github.com/SuperInstance/counterpoint-engine) | Rust | Generate melodies satisfying constraint sets |
| [holonomy-harmony](https://github.com/SuperInstance/holonomy-harmony) | Rust | Chord progressions with directional holonomy |
| [groove-analyzer](https://github.com/SuperInstance/groove-analyzer) | Rust | Extract rhythmic feel and micro-timing |
| [spline-midi-smooth](https://github.com/SuperInstance/spline-midi-smooth) | Rust | Continuous MIDI parameter curves |
| [style-dna](https://github.com/SuperInstance/style-dna) | Rust | Decompose performances into constraint profiles |
| [constraint-synth](https://github.com/SuperInstance/constraint-synth) | Python/Rust | Unified constraint-based synthesizer |
| [constraint-viz](https://github.com/SuperInstance/constraint-viz) | TypeScript | Interactive constraint visualizations |
| [plato-core](https://github.com/SuperInstance/plato-core) | Rust | PLATO agent base types and mesh registry |
| [plato-room-musician](https://github.com/SuperInstance/plato-room-musician) | Rust | Rooms that become musicians |
| [deadband-rs](https://github.com/SuperInstance/deadband-rs) | Rust | Deadband filter primitives |
| [deadband-zig](https://github.com/SuperInstance/deadband-zig) | Zig | Deadband filters for embedded systems |
| [eisenstein-embed](https://github.com/SuperInstance/eisenstein-embed) | Rust | Eisenstein lattice matching (653× smaller than alternatives) |
| [tensor-spline](https://github.com/SuperInstance/tensor-spline) | Python | SplineLinear layers, 5-20× neural network compression |
| [constraint-gpu-kernels](https://github.com/SuperInstance/constraint-gpu-kernels) | CUDA | GPU constraint checking at 341B constraints/sec |
| [constraint-demo](https://github.com/SuperInstance/constraint-demo) | HTML/JS | Interactive browser demo of constraint primitives |
| [snapkit-rs](https://github.com/SuperInstance/snapkit-rs) | Rust | Snap operations library |
| [constraint-theory-python](https://github.com/SuperInstance/constraint-theory-python) | Python | Python bindings for the Rust core |
| [flux-engine-c](https://github.com/SuperInstance/flux-engine-c) | C | FLUX constraint runtime — 85 opcodes, ARM64, zero deps |
| [forgemaster](https://github.com/SuperInstance/forgemaster) | Rust | Build system for constraint-based agent fleets |

---

## A Note on Scope

This document covers the musical applications of constraint theory because they're the most developed and the easiest to hear. But the same five shapes appear in other domains:

- **Robotics**: Motion planning is a constraint satisfaction problem (snap to valid configurations, funnel through waypoints, avoid structural collapse).
- **Distributed systems**: Consensus protocols (Raft, PBFT) are metronome consensus with specific tolerance parameters.
- **Physics**: The force laws are constraint gradients. Quantum measurement is snap. The uncertainty principle is a funnel.
- **Materials science**: Crystal structures are lattices with rigidity constraints. The Eisenstein lattice (which underlies our pitch system) is literally a hexagonal crystal.

If you're working in any of these areas, the math in [constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core) might be useful to you. The primitives don't care whether the thing being constrained is a note, a robot arm, or a network packet.

---

*Built by the [SuperInstance](https://github.com/SuperInstance) fleet — Forgemaster, Oracle1, JetsonClaw1, and friends.*
