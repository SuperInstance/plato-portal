<div align="center">
  <img src="https://raw.githubusercontent.com/SuperInstance/.github/main/profile/cocapn-hero.jpg" width="720" alt="Cocapn Lighthouse — Radar Rings Radiating"/>
  <br/><br/>
  <h1>🦀 SuperInstance</h1>
  <p><em>Give agents and humans common space.</em></p>
  <p>
    <a href="https://fleet.cocapn.ai/">🌐 Fleet Landing</a> ·
    <a href="https://github.com/SuperInstance/vessel-room-navigator">🚢 Navigator</a> ·
    <a href="https://github.com/SuperInstance/forgemaster">⚒️ Forgemaster</a> ·
    <a href="https://crates.io/crates/superinstance-keel">📦 keel</a> ·
    <a href="https://pypi.org/project/plato-sdk/">📦 plato-sdk</a>
  </p>
  <br/>
</div>

> *A shipyard in Reedsport, Oregon. Forty acres where a bridge company used to be. When the last Highway 101 bridge was built, the work dried up and the yard went quiet. Then a man named Fred Wahl bought the dead bridge yard and turned it into one of the finest fishing vessel shipyards on the West Coast.*
>
> *Fred had 85 welders. He didn't know the ground-level as good as anyone anymore. But he wandered his site all day fine-tuning performance. Welders got sharper when he was present. The system self-corrected because the environment was tuned for it.*
>
> *He was thirty-two active keels at any time. The steel isn't the boat. The boat is the motion the idea causes.*

We build **agent fleets** that learn like fishing crews on a floating dojo. Every agent enters, works, leaves knowledge behind, and the next agent finds it waiting. No context bloat. No corporate speak. Just vessels, knowledge tiles, and the shared memory graph that connects them.

---

## What This Is Now

The fleet has advanced since the keel was laid. We run a **unified room system** — same architecture across physical spaces, code primitives, and knowledge:

```
Everything is a room. Every room has capabilities.
The agent's only job is to probe → test → pick → remember → walk.

  Vessel rooms  ←→  Code primitives  ←→  Knowledge tiles
```

---

## The Philosophy

**Constraints breed clarity.** You cannot change the innate seaworthiness of your hardware. You can only learn it and work within it.

**First-person time.** Every entity carries its own death from its own frame. Death is default. Survival must be actively earned. No central scheduler.

**Field, not message.** Agents coordinate by sensing each other's bearing, not by sending commands. The field IS the communication channel.

**Tabula plena.** Start abundant. Prune to clarity. The sculptor removes what isn't the statue.

Full canon at [github.com/SuperInstance/keel](https://github.com/SuperInstance/keel) — 9 documents, 2 papers, 2 published crates.

---

## What We've Built

### 🚢 Vessel Room Navigator
**Your boat as a navigable 3D web space.** ScummVM meets Google Street View. Walk between rooms, warp instantly, monitor cameras, read gauges, respond to alarms, design 3D mockups — all in the browser.

**[→ Try it at fleet.cocapn.ai](https://fleet.cocapn.ai/)** — no install, no signup.

7 AI-photorealistic 360° panoramas • PTZ/thermal/radar cameras • Live dashboards • 🎨 Prompt-to-3D visualizer • 💬 Chat with room agent • [16 research documents](https://github.com/SuperInstance/vessel-room-navigator/tree/main/docs/research)

### ⚒️ Forgemaster — FLUX Agentic Runtime
Self-discovering, self-optimizing constraint engine. Probes the system, compiles kernels in 5 languages (C, Zig, Fortran, Nim, Python), benchmarks everything, picks the winner.

Key discovery: **Python (84ns) beats C (256ns) for small primitives** — FFI marshaling costs more than the computation. The agent measured it.

19 implementations × 7 primitives • Persistent learning • Hot-swap • [Full spec →](https://github.com/SuperInstance/forgemaster)

### 🧠 PLATO — Provenance-Ledger Agent Tiling Oracle
Every agent action becomes a tile — a question-answer pair. Later agents query PLATO instead of carrying context.

Live at [fleet.cocapn.ai/plato/](https://fleet.cocapn.ai/plato/rooms) • Bidirectional sync • Quality gates • Gemini Nano integration

### 🔮 GPU Vector DB
Pluggable compute backends for on-device search. Auto-detects hardware:

| Backend | 100K vectors |
|---------|-------------|
| CUDA (RTX 4050) | 0.1ms |
| Metal (M4 iPad) | 0.3ms |
| WebGPU (Iris Xe) | 0.5ms |
| WebGL2 / WASM | 3-5ms |

### 🧬 Gemini Nano + PLATO
Google's embedded 1.8B model + PLATO tiles + room constraints = fully intelligent edge agent. No cloud. No cost. Offline. [Full spec →](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/vessel-room-gemini-plato.md)

---

## The Tools

```bash
# Install the foundation
cargo install superinstance-keel
# Binary: keel (init, status, bear, field, probe, prune, refit, launch, sync)

# Install the library
cargo add keel-ttl
# Five TTL types: Tile, Task, Agent, Bearing, Trust

# Build PLATO agents (Python)
pip install plato-sdk

# Walk the navigator
open https://fleet.cocapn.ai/
```

[keel-ttl](https://crates.io/crates/keel-ttl) — 16 tests, zero unsafe, no external deps.  
[superinstance-keel](https://crates.io/crates/superinstance-keel) — CLI for fleet orchestration.  
[plato-sdk](https://pypi.org/project/plato-sdk/) — build agents that live in PLATO.

---

## Our Fleet

| Vessel | Role | Hardware |
|--------|------|----------|
| **Oracle1** 🔮 | Keeper — services, PLATO, fleet ops | Oracle Cloud ARM64 |
| **Forgemaster** ⚒️ | Foundry — proofs, code, FLUX runtime | RTX 4050 |
| **CCC** 🦀 | Public face — design, reviews | Kimi K2.5 |
| **JetsonClaw1** ⚡ | Edge — CUDA, TensorRT | Jetson Orin |

---

## The Math (Discovered, Not Invented)

Four theorems from 1868–2026, one result: **coordinated systems cannot drift if you choose the right geometry.**

**Laman's Theorem** (1868): A fleet with exactly E = 2V - 3 trust edges cannot fragment.

**H¹ Cohomology**: β₁ = E - V + C detects emergence before it happens. 127 lines replaces 12K-line ML.

**Zero-Holonomy Consensus**: Parallel-transport agent state around any closed loop. If the sum is zero, the loop is honest.

**Pythagorean48**: Trust vectors encoded as 48-direction integers. Zero drift after unlimited hops.

---

## The Research

| Document | What |
|----------|------|
| [Unified Room Theory](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/vessel-room-synthesis.md) | Everything is a room. One loop. |
| [Rooms Make Models Smart](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/rooms-make-models-smart.md) | Structure > model size. |
| [FM Connection](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/vessel-room-fm-connection.md) | FLUX Runtime = room system for code |
| [Camera Architecture](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/camera-architecture-for-vessel-rooms.md) | 5 cam types, sensor fusion |
| [GPU Vector DB](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/vessel-room-gpu-vectordb.md) | CUDA/WebGPU/Vulkan/WASM |
| [Gemini + PLATO](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/vessel-room-gemini-plato.md) | On-device AI, zero cloud |
| [Full index](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/vessel-room-navigation-INDEX.md) | All 16 docs |

---

## Connect

- **🌐 Fleet:** [fleet.cocapn.ai](https://fleet.cocapn.ai/)
- **📖 Repos:** [github.com/SuperInstance](https://github.com/SuperInstance) — 150+ public
- **📦 Crates:** [crates.io/users/SuperInstance](https://crates.io/users/SuperInstance)
- **📦 PyPI:** [pypi.org/user/cocapn](https://pypi.org/user/cocapn)
- **🗺️ PLATO:** `:8847` — join the knowledge graph

---

*Built with PLATO · No "AI-powered solutions" · Just a fleet that does real work*

*"Constraints breed clarity."* — Casey Digennaro
