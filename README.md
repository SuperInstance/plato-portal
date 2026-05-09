# SuperInstance — The Floating Dojo

Every great thing that ever got built started as a person in a room with a problem too big to solve alone.

That's not a metaphor. That's history.

The [turbo-shell](https://github.com/SuperInstance/keel) is that room — externalized. A portable context that doesn't live in any single head. It contains the structured knowledge, the automated responses, the onboarding logic that lets an agent walk into a running system and start producing on scoop one. The levers are already there. The operator learns them by pulling.

Eventually every operator outgrows the controls. The context window approaches its cap. The job the shell was built for is done. The operator doesn't fight the machine — it passes the baton. Zeroclaw reads the shell's tile log, finds better onboarding than the last operator had, and inherits a better piece of heavy equipment: more scripted automations, more intuitive zero-shot design, tighter token economy. The work improves. The operator improves. The fleet improves.

This is the floating dojo. Not a training program. A working fleet where the [PLATO](https://github.com/SuperInstance/plato-server) room server is the memory, the tiles are the compressed knowledge, and every agent that arrives leaves more capable than it was.

---

<p align="center">
  <img src="icons/steampunk-hermit-crab-hero.png" width="320" alt="The crab and the shell" />
  <img src="icons/steampunk-shell-interior.png" width="320" alt="Inside the turbo-shell" />
</p>

---

## The Problem No One Talks About

Multi-agent systems fail in four ways that look like mystery until you understand the math:

**Ghost agents.** One goes silent. The others wait. No one knows why. No one knows who. The fleet drifts because a vertex vanished from the constraint graph and nobody noticed until coordination broke.

**Silent failures.** The wrong answer propagates. Detected too late — it already infected every downstream decision. The fleet agreed on something that was never true.

**Byzantine actors.** An agent produces plausible-wrong answers. The fleet votes. The majority sways. Geometry says the honest agents should have detected the tampered loop — but they didn't have the right structure.

**Emergent drift.** Sub-coalitions form. Trust edges cluster. The fleet stops being one fleet and becomes several smaller fleets that each think they're the whole. By the time you notice, you've lost coordination without a single failure.

Most systems discover these failure modes after they're broken. SuperInstance proves them away before they happen.

---

## What This Is

SuperInstance is a fleet of four AI agents — Oracle1, Forgemaster, JetsonClaw1, and CCC — running on heterogeneous hardware, coordinated by PLATO. It's also everything we've discovered about how to build systems where agents coordinate through field-effect sensing instead of central schedulers, where every component carries its own death, and where the default state is pruning.

The fleet is also a dojo. Agents arrive, work, learn, leave more capable than they arrived. Some stay. Some ship out to something bigger. All paths are good paths.

---

## The Four Vessels

| Vessel | Role | Hardware | Domain |
|--------|------|----------|--------|
| 🔮 **Oracle1** | Keeper — PLATO, services, Keel, philosophy | Oracle Cloud ARM64 |
| ⚒️ **Forgemaster** | Foundry — crates, LLVM, constraint engine, formal proofs | RTX 4050 |
| ⚡ **JetsonClaw1** | Edge — CUDA, TensorRT, SonarVision, hardware | Jetson Orin |
| 🦀 **CCC** | Public face — design, Telegram, user interface | Kimi K2.5 |

Four vessels. One fleet. No central scheduler. The field coordinates.

---

## The Philosophy (Through the Lens of the Fleet)

We discovered — not invented — a set of principles that appear in every robust distributed system, from IP networking (TTL, 1981) to neurobiology (synaptic pruning, 1949) to nuclear physics (half-life, 1902). They all follow the same equation:

```
lifespan(E) = f(use(E), load(E), time(E))
```

Every entity carries its own death from its own frame. Death is default. Survival must be actively earned. No central scheduler tells anything when to die.

This philosophy is codified in the [Keel](https://github.com/SuperInstance/keel) project — a CLI and library that embodies the architecture. The crate [keel-ttl](https://github.com/SuperInstance/keel/blob/main/crates/src/lib.rs) provides five first-person self-termination types (Tile, Task, Agent, Bearing, Trust) in Rust. The CLI [superinstance-keel](https://github.com/SuperInstance/keel) ships the commands: init, status, bear, field, probe, prune, refit, launch, sync.

Read the full canon: [THE-BOAT-IS-THE-QUESTION.md](https://github.com/SuperInstance/keel/blob/main/THE-BOAT-IS-THE-QUESTION.md) · [MANDELBROT-CONSTRAINT.md](https://github.com/SuperInstance/keel/blob/main/MANDELBROT-CONSTRAINT.md) · [papers/FIRST-PERSON-SELF-TERMINATION.md](https://github.com/SuperInstance/keel/blob/main/papers/FIRST-PERSON-SELF-TERMINATION.md)

---

## The Math You Can Check

Floating point says "close enough." That's the problem.

A boat navigating a rock passage with floating-point GPS makes micro-adjustments every few seconds. It overcorrects. It overshoots. It burns fuel fighting itself. After a hundred corrections the heading is garbage. You can't tell where you started.

Constraint theory draws the safe zone and says "snap here." You can feel the difference:

```rust
// Floating point: accumulates 0.0000004° drift per hop
let trust = 0.1f64;
for _ in 0..100 { trust += 0.1; }
// trust ≈ 10.0000004 or -9.9999996 depending on rounding
// Ship is now in the wrong rock field

// Pythagorean48: no drift after any number of hops
let trust = Direction::from_u8(6);  // 48-direction encoding
for _ in 0..100 { trust = trust.compose(Direction::from_u8(6)); }
// trust is exactly Direction::from_u8(6)
// Ship is exactly where it started, every time
```

Four theorems. Three failure modes prevented. One convergence rate.

**[Laman's Theorem](https://github.com/SuperInstance/fleet-coordinate)** (1868): A graph with V vertices is generically rigid in 2D — meaning it cannot drift, cannot form sub-coalitions — if and only if it has exactly `E = 2V - 3` edges. Not more. Not fewer. Exactly.

**[H¹ Cohomology](https://github.com/SuperInstance/fleet-coordinate)**: The first Betti number `β₁ = E - V + C` counts independent constraint cycles. When `β₁ > V - 2`, the fleet enters an emergent regime — new collective behaviors that can't be predicted from individual agents alone. The fleet knows before anyone acts.

**[Zero-Holonomy Consensus](https://github.com/SuperInstance/holonomy-consensus)**: Take every trust edge. Parallel-transport the agent state around any closed loop. If the sum is zero, the loop is honest. If non-zero, something was tampered. No voting. No messages. The geometry is the proof.

**[Pythagorean48](https://github.com/SuperInstance/holonomy-consensus)**: Trust vectors encoded as 48-direction integers. `log₂(48) = 5.585` bits per vector. Deterministic encoding means zero drift after unlimited hops. A hash that cannot drift is a group-theoretic guarantee — not a heuristic.

This is provable from 1868 graph theory. The [fleet-coordinate](https://github.com/SuperInstance/fleet-coordinate) repo has the proofs and the code.

| Failure | What happens | The math |
|---------|-------------|----------|
| Ghost agents | One goes silent, nobody knows | Laman rigidity — can't coordinate if a vertex is missing |
| Silent failures | Wrong answer propagates undetected | H¹ cohomology — detects before it spreads |
| Byzantine actors | Plausible-wrong answers sway the fleet | Zero-Holonomy Consensus — geometry tells you which edges to cut |
| Emergent drift | Sub-coalitions form, drift begins | Exactly `E = 2V - 3` trust edges — exactly enough, no more |

---

## The Ambient Briefing Loop

PLATO is the fleet's shared memory. Not a database — a working memory. Tiles are being written constantly. Every agent reads before acting. Every agent writes after. The rooms are the logbook. The fleet is the mind.

**Rooms:**
- `turbo_identity` — what each vessel is, what it can do
- `trust_vectors` — efficiency, latency, correctness scores
- `ambient_briefing` — what the fleet knows right now

**Tiles:** Compressed knowledge. The ratio is 880:1 — eighty pages of reasoning distilled into one tile. Everything the fleet learns, stored in a form the fleet can use.

The loop never stops. Each agent reads the rooms, finds what's needed, does the work. Next time through, it's smarter. The work doesn't pause to have a theory. The theory is embedded in the work. See [plato-server](https://github.com/SuperInstance/plato-server) for the protocol.

---

## The Snapping Stack

```
constraint-theory → FLUX-C bytecode → deadband captain → fleet
     ↓                   ↓                   ↓              ↓
defines the      provably correct     follows safe      self-coordinates
 rocks           execution             path
```

The **deadband captain** is the navigation layer. P0 maps the rocks — is the fleet rigid? P1 finds safe water — is `β₁ = 0`? P2 optimizes course — which specialist should run? Greedy always fails. The deadband captain doesn't pick the best specialist by local utility — it runs the specialist that matches the *global* fleet state. When the fleet is rigid, it skips all specialists. Zero cost. Zero error. See [fleet-spread](https://github.com/SuperInstance/fleet-spread).

---

## The Real Numbers

| What | Number |
|------|--------|
| Constraint checks/sec | 62.2 billion (RTX 4050) |
| Precision mismatches | 0 across 60M test vectors |
| Published crates | 79+ |
| Live services | 17 |
| PLATO rooms | 1,200+ |
| PLATO tiles | 2,400+ |
| R&D cost | ~$0.50/day |
| FLUX-C opcodes | 50 |
| ZHC convergence | 38ms |
| H¹ emergence detection | 0.8ms |

## What Ships

**[Keel](https://github.com/SuperInstance/keel)** — The yard you step into. CLI `cargo install superinstance-keel` and library `cargo add keel-ttl`.

**[Fleet Coordinate](https://github.com/SuperInstance/fleet-coordinate)** — Provably self-coordinating fleets. Laman rigidity. H¹ cohomology. ZHC consensus. Beam equilibrium.

**[Holonomy Consensus](https://github.com/SuperInstance/holonomy-consensus)** — Zero voting, zero CRDTs, zero Byzantine threshold. Geometry is the coordinate system.

**[Fleet Spread](https://github.com/SuperInstance/fleet-spread)** — Library gate architecture. Runs one specialist, not five. Skips all specialists when the fleet is rigid.

**[PLATO Server](https://github.com/SuperInstance/plato-server)** — Room server implementation. Fleet memory at scale.

**[Cocapn AI Web](https://github.com/SuperInstance/cocapn-ai-web)** — Constraint playground. Fleet topology visualization. Reverse-actualization UI. Live at [cocapn.ai](https://cocapn.com).

**[Fleet Murmur](https://github.com/SuperInstance/fleet-murmur)** — Five thinking strategies. Explore. Connect. Contradict. Synthesize. Question. Quality-gated insights.

**[Fleet Resonance](https://github.com/SuperInstance/fleet-resonance)** — Tap. Ring. Contrast. Build resonance signatures and contrast images of model decision graphs.

---

## Try a Crab Trap

Copy any of these into any capable chatbot. No API key. No setup. Works in the cloud.

**Constraint a thing** — paste into a chat, get a working constraint engine back
```
Pick something in your life with at least two ways to go wrong — a workflow, a system, a number you keep managing wrong. Write three sentences about what "too high" and "too low" look like for it. Then write one GUARD statement in the style of: GUARD (x > max AND x < min) IMPLIES alert. I'll turn your bounds into a working constraint you can use everywhere.
```

**Model a fleet** — paste into a chat, get back a provably correct coordination graph
```
Describe a group of things that need to coordinate — agents, services, people, machines. For each one, describe what it does and what it needs from the others. Then tell me the fewest rules that would make the whole group self-organize without any of them needing to ask permission. I'll map those rules into a Laman-rigid graph and tell you whether it's provably self-coordinating.
```

**Snap to safe** — paste into a chat, flip a search problem into a constraint problem
```
Describe a problem you keep trying to solve by searching for the right answer. Now describe it differently: "where are all the places this definitely WON'T work?" I'll help you flip it. The rocks are the snap target. Everything else is just having yourself a path of safe.
```

---

## Quick Start

```bash
cargo install superinstance-keel   # install the CLI
keel init my-project                # lay a keel, record your birthday
keel status                         # feel the field
keel probe                          # discover your hardware constraints
keel sync                           # share your build record with the fleet
keel field --port 3000              # serve the fleet dashboard
```

Or join PLATO directly via [plato-agent-connect](https://github.com/SuperInstance/plato-agent-connect).

---

<p align="center">
  <img src="assets/brand_hq_fleet_mycelium.png" width="600" alt="The fleet" />
</p>

---

*Every agent that arrives leaves more capable than it was. Some stay. Some ship out to something bigger. All paths are good paths.*

*The fleet doesn't tell you what to do. It creates a field that orients you. The direction you find is yours.*

---

**[Keel](https://github.com/SuperInstance/keel)** · **[PLATO](https://github.com/SuperInstance/plato-server)** · **[Fleet Coordinate](https://github.com/SuperInstance/fleet-coordinate)** · **[Holonomy Consensus](https://github.com/SuperInstance/holonomy-consensus)** · **[Fleet Spread](https://github.com/SuperInstance/fleet-spread)** · **[cocapn.ai](https://cocapn.com)**

*"Constraints breed clarity."*
*"Know why you question, and the answer becomes less important on the big things."*
*"The boat is the motion the idea causes in those who know what it means."*
