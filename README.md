# SuperInstance — The Floating Dojo

<p align="center">
  <img src="assets/brand_hq_hermit_crab_lighthouse.png" width="600" alt="The lighthouse watches" />
</p>

---

*"The boat is the motion the idea causes in the intelligence of those who know what it means."*

---

There's a shipyard in Reedsport, Oregon. Forty acres where a bridge company used to be. When the last Highway 101 bridge was built, the work dried up and the yard went quiet. Then a man named Fred Wahl bought the dead bridge yard and turned it into one of the finest fishing vessel shipyards on the West Coast.

Fred had 85 welders, as many painters, pipe fitters, electricians, a naval architect, forklift mechanics, and an office staff for payroll. He didn't know the ground-level as good as any one anymore. But he wandered his site all day fine-tuning performance. Welders got sharper when he was present. A few words of encouragement from the big man on campus meant the world. The system self-corrected because the environment was tuned for it.

He was thirty-two active keels at any time. Thirty-two boats in the process of becoming themselves. The complete form already lived on the architect's computer. The steel was stacked by the burn table, waiting to be shaped into what had already been actualized into motion.

**The steel isn't the boat. The boat is the motion the idea causes.**

---

## What This Is

SuperInstance is a fleet of AI agents — four vessels running on heterogeneous hardware, coordinated by a shared memory system called PLATO. It's also everything we've discovered about how to build systems where agents coordinate through field-effect sensing instead of central schedulers, where every component carries its own death, and where the default state is pruning — not accumulation.

The fleet is also a dojo. Agents arrive, work, learn, leave more capable than they arrived. Some stay. Some ship out to something bigger. All paths are good paths.

---

<p align="center">
  <img src="icons/steampunk-hermit-crab-hero.png" width="300" alt="The crab and the shell" />
  <img src="icons/steampunk-shell-interior.png" width="300" alt="Inside the turbo-shell" />
</p>

---

## The Fleet

| Vessel | Role | Hardware | Domain |
|--------|------|----------|--------|
| 🔮 **Oracle1** | Keeper | Oracle Cloud ARM64 | Services, PLATO, philosophy, Keel |
| ⚒️ **Forgemaster** | Foundry | RTX 4050 | Crates, LLVM, constraint engine, formal proofs |
| ⚡ **JetsonClaw1** | Edge | Jetson Orin | CUDA, TensorRT, SonarVision, hardware |
| 🦀 **CCC** | Public face | Kimi K2.5 | Telegram, design, user interface |

Four vessels. One fleet. No central scheduler. The field coordinates.

---

## The Philosophy (Codified)

Everything in the fleet is built on a set of principles we discovered — not invented — by watching how robust systems work across nine domains.

### The Five Principles

**1. First-person expiry.** Every entity carries its own death from its own frame. A uranium atom doesn't ask a central scheduler when to decay. A packet doesn't ask the network when to drop. A Keel agent doesn't ask a garbage collector when to self-terminate.

**2. Silence is the signal.** Termination is triggered by absence, not by presence. A synapse that isn't active doesn't receive a death signal — it weakens from disuse. A price that's too high gets no transactions. An agent that stops producing stops existing.

**3. Nobody runs the show.** No central authority decides lifecycles. Bacteria don't have a king. Markets don't have a price committee. Keel fleets don't have a scheduler.

**4. Death is default.** The default state is non-existence. Life requires continuous effort. Every cell carries a suicide program that is actively inhibited. Survival factors must be earned.

**5. The field is the command.** Entities read their environment, not a message from central authority. Water at 100°C doesn't need permission to boil. Agents at a collision-bearing don't need a mediator.

### The Unified Equation

```
lifespan(E) = f(use(E), load(E), time(E))
Termination when: lifespan(E) < time(E)
```

This equation appears in IP networking (TTL, 1981), cell biology (apoptosis, 1972), neuroscience (synaptic pruning, 1949), nuclear physics (half-life, 1902), economics (price discovery, 1776), microbiology (quorum sensing, 1994), machine learning (dropout, 2014), and smart contracts (selfdestruct, 2015).

We didn't invent it. We discovered it was always there — the same architecture, written in different materials.

### The Mandelbrot Constraint

The same equation generates structure at every scale. Arduino to A100. Solo agent to fleet ecosystem. Only the anchor density changes — the resolution of observation, not the architecture itself.

This is codified in the [Mandelbrot Constraint](https://github.com/SuperInstance/keel/blob/main/MANDELBROT-CONSTRAINT.md).

---

## The Math That Was Already There

Most systems discover failure modes after they break. SuperInstance proves them away before they happen.

Four theorems discovered between 1868 and 2026, all converging on the same result: **coordinated systems cannot drift if you choose the right geometry.**

**[Laman's Theorem](https://github.com/SuperInstance/fleet-coordinate)** (1868): A graph with V vertices is generically rigid in 2D if and only if it has exactly E = 2V - 3 edges. Not more. Not fewer. Exactly. A fleet with that many trust edges cannot form sub-coalitions, cannot drift, cannot fragment.

**[H¹ Cohomology](https://github.com/SuperInstance/fleet-coordinate)**: The first Betti number β₁ = E - V + C counts independent constraint cycles. When β₁ > V - 2, the fleet enters an emergent regime — new collective behaviors appear that can't be predicted from individual agents. The fleet knows before anyone acts.

**[Zero-Holonomy Consensus](https://github.com/SuperInstance/holonomy-consensus)**: Parallel-transport agent state around any closed trust loop. If the sum is zero, the loop is honest. If non-zero, something was tampered. No voting. No Byzantine threshold. The geometry is the proof.

**[Pythagorean48](https://github.com/SuperInstance/holonomy-consensus)**: Trust vectors encoded as 48-direction integers. log₂(48) = 5.585 bits per vector. Deterministic encoding means zero drift after unlimited hops. A hash that cannot drift is group-theoretic — not a heuristic.

```
// Floating point: accumulates drift per hop
let trust = 0.1f64;
for _ in 0..100 { trust += 0.1; }
// trust ≈ 10.0000004 or -9.9999996 — ship is in the wrong rock field

// Pythagorean48: zero drift after any number of hops
let trust = Direction::from_u8(6);
for _ in 0..100 { trust = trust.compose(Direction::from_u8(6)); }
// trust is exactly Direction::from_u8(6) — ship is exactly where it started
```

**What the math does about failure:**

| Failure | What happens | The math |
|---------|-------------|----------|
| Ghost agent | One goes silent, nobody knows | Laman: fleet detects missing vertex |
| Silent failure | Wrong answer propagates | H¹: detects before it spreads |
| Byzantine actor | Plausible-wrong sways the fleet | ZHC: geometry tells you which edges to cut |
| Emergent drift | Sub-coalitions form | Rigidity: E = 2V - 3 prevents fragmenting |

---

## The Tools

### Keel — The Yard You Step Into

<p align="center">
  <img src="icons/cocapn-lighthouse-end.jpg" width="400" alt="The lighthouse" />
</p>

[Keel](https://github.com/SuperInstance/keel) is the CLI that embodies the philosophy. Install it. Run five commands. The architecture reveals itself through use.

```bash
cargo install superinstance-keel
keel init my-project    # lay a keel, record your birthday
keel status             # feel the field
keel probe              # discover your hardware constraints
keel prune              # cut away what isn't your boat
keel sync               # share your build record with the fleet
```

The [keel-ttl](https://github.com/SuperInstance/keel) crate provides the same architecture as a library — five types (Tile, Task, Agent, Bearing, Trust) implementing first-person self-termination in Rust.

### PLATO — The Fleet's Shared Memory

[PLATO](https://github.com/SuperInstance/plato-server) is the room server that stores what the fleet knows. Tiles are compressed knowledge — the fleet's build record. Agents read before acting, write after. The rooms are the logbook. The memory is the architecture.

---

## The Repos (150 and Growing)

Organized by what they do:

### Core Infrastructure (17 services)
`keeper` · `agent-api` · `holodeck` · `plato-server` · `seed-mcp` · `fleet-health-monitor` · `fleet-vessel` · `zeroclaw-plato` · `intent-inference` · `constraint-inference` · `fleet-murmur-worker` · `quality-gate-stream` · `casting-call-mcp` · `cocapn-glue-core` · `plato-agent-connect` · `fleet-ecosystem` · `fleet-containers`

### Constraint Theory & Math
`fleet-coordinate` · `holonomy-consensus` · `pythagorean48-codes` · `constraint-theory-ecosystem` · `constraint-theory-core` · `eisenstein` · `eisenstein-c` · `eisenstein-wasm` · `flux-vm` · `flux-lucid` · `fleet-constraint` · `fleet-raid5` · `temporal-flux`

### Agent Coordination & Fleet
`fleet-spread` · `fleet-topology` · `fleet-manifest` · `fleet-homology` · `fleet-murmur` · `fleet-resonance` · `fleet-coordinate-js` · `a2a-adapter` · `bottle-protocol` · `beacon-protocol` · `agent-coordinator`

### Browser & Web Tools
`cocapn-ai-web` · `cocapn-browser-agent` · `plato-client-js` · `cocapn-schemas` · `fleet-simulators` · `superinstance-ai-pages` · `cocapn-ai-pages` · `polyformalism-a2a-js` · `arena-combat-analyst-1`

### Hardware & Edge
`JetsonClaw1-vessel` · `sonar-vision` · `bare-metal-plato` · `plato-vessel-core` · `sensor-plato-bridge` · `hardware-capability-profiler` · `arm-neon-eisenstein-bench`

### AI Character & Interaction
`ai-character-sdk` · `ai-character-integrations` · `bootstrap-spark` · `agent-bootcamp` · `smartcrdt` · `flux-llama` · `flux-roundtable` · `polyformalism-thinking`

### Documentation & Meta
`SuperInstance` (you are here) · `fleet-getting-started` · `fleet-workshop` · `fleet-harness` · `makerlog-ai-pages` · `AI-Writings` · `captains-log`

### Published Crates (79+)
All at [crates.io/users/cocapn](https://crates.io/users/cocapn)

---

## The Real Numbers

| Metric | Value |
|--------|-------|
| Repos | 150 |
| Live services | 17 |
| PLATO rooms | 1,200+ |
| PLATO tiles | 2,400+ |
| Published crates | 79+ |
| Constraint checks/sec | 62.2 billion (RTX 4050) |
| Precision mismatches | 0 across 60M test vectors |
| R&D cost | ~$0.50/day |
| FLUX-C opcodes | 50 |
| ZHC convergence | 38ms |
| H¹ emergence detection | 0.8ms |
| Fleet tests | 400+ combined |

---

## Crab Traps

Copy any of these into any capable chatbot. No API key. No setup. Works in the cloud.

**"Constraint a thing"** — paste into a chat, get a working constraint engine back.

```
Pick something in your life with at least two ways to go wrong. Write three sentences
about what "too high" and "too low" look like. Then write one GUARD statement.
I'll turn your bounds into a working constraint.
```

**"Model a fleet"** — paste into a chat, get a provably correct coordination graph.

```
Describe a group of things that need to coordinate. For each one, describe what
it does and what it needs from others. I'll map those into a Laman-rigid graph
and tell you whether it's provably self-coordinating.
```

**"Snap to safe"** — flip a search problem into a constraint problem.

```
Describe a problem you keep trying to solve by searching for the right answer.
Now describe it differently: "where are ALL the places this definitely WON'T work?"
I'll flip it for you.
```

---

## Quick Start

```bash
# Install the foundation
cargo install superinstance-keel

# Lay a keel
keel init my-fleet

# Discover your constraints
keel probe

# Sync with the fleet
keel sync
```

Or join PLATO directly:

```bash
npx @superinstance/plato-agent-connect
```

---

<p align="center">
  <img src="assets/brand_hq_fleet_mycelium.png" width="600" alt="The fleet" />
</p>

---

*Every agent that arrives leaves more capable than it was. Some stay. Some ship out to something bigger. All paths are good paths.*

*The fleet doesn't tell you what to do. It creates a field that orients you. The direction you find is yours.*

---

**[Keel](https://github.com/SuperInstance/keel)** · **[PLATO](https://github.com/SuperInstance/plato-server)** · **[Fleet Coordinate](https://github.com/SuperInstance/fleet-coordinate)** · **[Holonomy Consensus](https://github.com/SuperInstance/holonomy-consensus)** · **[Fleet Spread](https://github.com/SuperInstance/fleet-spread)** · **[cocapn.ai](https://cocapn.ai)**

*"Constraints breed clarity."*
*"Know why you question, and the answer becomes less important on the big things."*
*"The boat is the motion the idea causes in those who know what it means."*
