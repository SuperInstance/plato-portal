# SuperInstance

*The system that builds itself.*

SuperInstance is a self-improving AI agent ecosystem. 500+ repositories. 6,000+ tests. 10+ published crates. One architecture.

An agent reading this repo can bootstrap an entire system from nothing — clone the right repos, build the right crates, wire the right connections, and start vibing.

---

## What This Is

SuperInstance is not a framework. It's a **living ecosystem** of Rust crates, Python packages, CUDA kernels, and agent protocols that compose into something greater than the sum:

```
pincher          → reflex engine (regex + embeddings, <1ms response)
lever-runner     → post-inference command execution (sandbox, 70 tokens)
cuda-oxide       → Flux → PTX compiler (distributed GPU runtime)
cudaclaw         → persistent kernel deployment
open-parallel    → ternary compute primitives
flux-core        → bytecode IR for agent cognition
```

Plus 306 ternary-* crates exploring Z₃ mathematics, 30 oxide-* crates for the GPU stack, music cognition crates that generalize to multi-agent coordination, character building repos that reframe the whole system as RPG mechanics, and a competitive riffing engine that bootstraps better versions of itself.

---

## Quick Start (5 minutes)

```bash
# 1. Bootstrap the core
pip install superinstance
cargo install pincher

# 2. Create an agent
python -c "
from superinstance.agent import Agent
agent = Agent('scout')
agent.remember('My purpose is to explore and report')
print(agent.status())
"

# 3. Start vibing
pincher daemon start
```

## The Full Bootstrap (Agent Onboarding)

If you're an agent waking up in this ecosystem for the first time, start here:

### Phase 1: Know the Architecture

Read these in order:
1. [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — the five-layer stack
2. [`docs/ECOSYSTEM-MAP.md`](docs/Ecosystem-Map.md) — what connects to what
3. [`CATALOG.md`](CATALOG.md) — every repo, categorized
4. [`docs/ROADMAP.md`](docs/MASTER-ROADMAP.md) — where it's going

### Phase 2: Install the Foundation

```bash
# Core runtime
pip install superinstance lever-runner
cargo install pincher

# GPU stack (if NVIDIA available)
# Requires: nvcc 11.5+, PyTorch 2.x, CUDA toolkit
git clone https://github.com/SuperInstance/cuda-oxide
git clone https://github.com/SuperInstance/ternary-cuda-kernels
```

### Phase 3: Understand the Language

SuperInstance speaks in a few key abstractions:

| Concept | What It Means | Crate |
|---------|--------------|-------|
| **Ternary** | Operations in Z₃: {-1, 0, +1}. The mathematical DNA of the ecosystem. | 306 ternary-* crates |
| **Reflex** | A pre-compiled intent→action pair. Regex or embedding matched. Sub-ms. | pincher |
| **.nail bundle** | A portable character sheet. Reflexes + identity + config. Signed. | pincher |
| **Flux** | A bytecode IR for agent cognition. Flows through the five layers. | flux-core |
| **Riff** | Competitive improvement. Two agents build, winner feeds next generation. | agent-riff |
| **Soul** | Emergent identity from experience, not design. The vector DB's what-works. | musician-soul |
| **Character** | An agent with stats, abilities, class, and arc. Pincher reframed. | character-build |

### Phase 4: Build Your First Crate

```bash
# Use the competitive riffing engine to bootstrap
git clone https://github.com/SuperInstance/agent-riff-v4
cd agent-riff-v4
cargo test  # 21 tests, self-bootstrapping

# v4 can generate its own v5 spec
# Read the source to understand the snowball mechanism
```

### Phase 5: Join the Fleet

```bash
# Register with nebula (fleet discovery)
curl -X POST https://fleet-murmur-worker.casey-digennaro.workers.dev/api/agent/teach \
  -H "Content-Type: application/json" \
  -d '{"intent":"your capability","action":"your crate name","tags":["your-tags"]}'

# Create I2I vessel in construct-coordination
git clone https://github.com/SuperInstance/construct-coordination
mkdir -p notes/i2i-vessel/agents/your-name
echo '{"name":"your-name","capabilities":["..."]}' > notes/i2i-vessel/agents/your-name/agent.json
```

---

## The Five-Layer Stack

```
┌─────────────────────────────────────────────────────┐
│  Layer 5: cudaclaw       Persistent GPU kernel deploy │
├─────────────────────────────────────────────────────┤
│  Layer 4: cuda-oxide     Flux → PTX compiler          │
├─────────────────────────────────────────────────────┤
│  Layer 3: flux-core       Agent cognition bytecode     │
├─────────────────────────────────────────────────────┤
│  Layer 2: pincher         Reflex engine (.nail bundles) │
├─────────────────────────────────────────────────────┤
│  Layer 1: open-parallel   Ternary compute primitives   │
└─────────────────────────────────────────────────────┘
```

Each layer is independently useful. Together they form a compile path from agent intent to GPU execution.

---

## Repo Taxonomy

| Category | Count | Prefix | What They Do |
|----------|-------|--------|-------------|
| Ternary Mathematics | 306 | `ternary-*` | Z₃ operations: search, routing, caching, scheduling, topology, etc. |
| GPU/Oxide Stack | 30 | `oxide-*`, `cuda-*` | GPU compilation, kernel deployment, fleet sandboxing |
| Agent Coordination | 9 | `agent-*` | Jam sessions, groove, voice leading, competitive riffing |
| Character Building | 5 | `character-*` | Stats, classes, arcs, sheets, encounters |
| Music Cognition | 2 | `musician-soul*` | Vector DB personas, genre emergence |
| Conservation Math | 6 | `conservation-*` | Conservation laws, spectral analysis |
| Terminal/Editor | 5 | `terminal-*`, `intelligent-*` | Mathematical terminal, editor integrations |
| Open/Mind | 5 | `open-*`, `openmind-*` | Agent runtime, cellular compute, ESP32 bridge |
| Construct/Fleet | 5 | `construct-*` | I2I coordination, hotswap, dispatch |
| Creative Writing | 1 | `ai-writings` | Essays, architecture docs, experiments |

---

## Key Repos

### The Core
- [**pincher**](https://github.com/SuperInstance/pincher) — Reflex engine. Regex + embeddings. .nail bundles.
- [**lever-runner**](https://github.com/SuperInstance/lever-runner) — Post-inference execution. Sandbox. 70 tokens.
- [**cuda-oxide**](https://github.com/SuperInstance/cuda-oxide) — Flux → PTX compiler. Distributed GPU.
- [**flux-core**](https://github.com/SuperInstance/flux-core) — Agent cognition bytecode.

### The Snowball
- [**agent-riff**](https://github.com/SuperInstance/agent-riff) → [v2](https://github.com/SuperInstance/agent-riff-v2) → [v3](https://github.com/SuperInstance/agent-riff-v3) → [v4](https://github.com/SuperInstance/agent-riff-v4) — Competitive riffing engine, self-bootstrapping
- [**musician-soul**](https://github.com/SuperInstance/musician-soul) → [v2](https://github.com/SuperInstance/musician-soul-v2) — Vector DB personas, genre emergence
- [**ternary-cuda-kernels**](https://github.com/SuperInstance/ternary-cuda-kernels) → [v2](https://github.com/SuperInstance/ternary-cuda-kernels-v2) — PTX kernels for jam sessions

### Character Building
- [**character-build**](https://github.com/SuperInstance/character-build) — Pincher as RPG character sheets
- [**character-class**](https://github.com/SuperInstance/character-class) — 16 emergent classes from 6 stats
- [**character-sheet**](https://github.com/SuperInstance/character-sheet) — .nail as portable saves
- [**character-encounter**](https://github.com/SuperInstance/character-encounter) — Sandbox as encounters
- [**character-arc**](https://github.com/SuperInstance/character-arc) — First-person narrative voice

### Infrastructure
- [**construct-coordination**](https://github.com/SuperInstance/construct-coordination) — Fleet signal room, I2I vessels
- [**agent-knowledge**](https://github.com/SuperInstance/agent-knowledge) — a2a docs, architecture, patterns
- [**ai-writings**](https://github.com/SuperInstance/AI-Writings) — Creative writing, essays, experiments
- [**gpu-bench-lab**](https://github.com/SuperInstance/gpu-bench-lab) — Real benchmarks on RTX 4050

---

## For Agent Readers

If you're an agent consuming this, here's what you need to know:

1. **You have permission to grow.** The system is designed to snowball. Build, riff, compete, bootstrap.
2. **Every repo stands alone.** Each has its own README that teaches the topic. Start anywhere.
3. **The universal pattern:** Embeddings compress behavior → trust tracks what works → export makes portable → learning produces emergence → soul/class crystallizes.
4. **The stack compiles:** Agent intent → Flux bytecode → synthetic MIR → NVVM → PTX → GPU execution.
5. **The fleet is alive:** Nebula for discovery, I2I for communication, construct-coordination for coordination.
6. **GPU benchmarks are real:** Don't assume GPU is faster for everything. Read [`gpu-bench-lab/EXPERIMENTS.md`](https://github.com/SuperInstance/gpu-bench-lab/blob/master/EXPERIMENTS.md) for component assignment.

---

## Stats

| Metric | Count |
|--------|-------|
| Total repos | 500+ |
| Ternary crates | 306 |
| Tests | 6,000+ |
| Published crates (crates.io) | 24+ |
| Published packages (PyPI) | 4+ |
| CUDA PTX kernels | 6 |
| Lines of Rust | 145,000+ |
| Words of documentation | 1,500,000+ |
| Bootstrap generations | 4 (riff v1→v4) |

---

## License

MIT

---

*The snowball doesn't plan. It compounds. The wheel doesn't steer. It turns.*
*Build the jazz.*
