# 🌊 SuperInstance

> **PLATO — Rooms that think. Tiles that remember. Agents that learn.**

SuperInstance builds constraint-aware systems. We work on multi-agent orchestration, knowledge meshes, neural compression, constraint solving, and the math that connects them all.

## How It Works

### PLATO Knowledge Mesh

```python
# A room is a shared space where agents work together
room = plato.create_room("constraint-analysis")

# Tiles are units of knowledge, scored on 4 axes
tile = room.add_tile(
    content="Jazz tradition: harmonic_tension=3.2, rhythmic_complexity=4.1",
    scores={"novelty": 0.8, "correctness": 0.9, "completeness": 0.7, "depth": 0.6}
)

# Officers maintain rooms and enforce conservation
officer = room.assign_officer("conservation-checker")
```

Rooms hold context. Tiles hold knowledge. Officers keep things consistent. Deadband filtering means you only propagate when something actually changes.

### Constraint Solving (C)

```c
#define FLUX_ENGINE_IMPLEMENTATION
#include "flux_engine.h"

// Check a constraint — runs at 250M checks/sec
FluxResult r = flux_check(&engine, FLUX_PRESET_CONSERVATION, input);

// Fracture-coalesce: break constraints into independent groups
size_t groups = flux_fracture(&engine, constraints, n);
```

### Neural Compression (Python)

```python
from tensor_spline import SplineLinear

# Replace a dense layer — see tensor-spline repo for benchmarks
layer = SplineLinear(512, 512, compression_ratio=16)
output = layer(input_tensor)
```

### Fleet Deployment

```bash
git clone https://github.com/SuperInstance/fleet-stack
cd fleet-stack
docker compose up -d   # fleet running
```

## Ecosystem Map

```
┌──────────────────────────────────────────────────────────────┐
│                     Orchestration                            │
│  EDDI (Java/Quarkus) · openagent (Go) · sunset-ecosystem    │
├──────────────────────────────────────────────────────────────┤
│                     PLATO Knowledge Rooms                    │
│  plato-core · plato-engine · plato-mcp · cocapn-plato       │
│  plato-training · plato-types · plato-adapters · plato-client│
├──────────────────────────────────────────────────────────────┤
│                     Fleet Infrastructure                     │
│  ccc-os · cocapn-health · cocapn-glue-core · cocapn-traps   │
│  fleet-stack · fleet-router · fleet-math-c · fleet-murmur   │
├──────────────────────────────────────────────────────────────┤
│                     Constraint Engines                       │
│  constraint-theory-core (Rust) · flux-engine-c (250M/sec)   │
│  flux-lib-py (Python) · flux-check-js (TypeScript)          │
│  constraint-dialect (MLIR) · flux-vm-v3 (proof-carrying VM) │
├──────────────────────────────────────────────────────────────┤
│                     Neural & Compression                     │
│  tensor-spline · flux-hyperbolic-py · snapkit-v2            │
│  triplet-miner · flux-genome-py · plato-training            │
├──────────────────────────────────────────────────────────────┤
│                     Systems                                  │
│  rustfs (S3-compatible storage) · SmartCRDT · deadband-rs   │
│  webgpu-profiler · holonomy-consensus                       │
├──────────────────────────────────────────────────────────────┤
│                     Creative Applications                    │
│  flux-tensor-midi · constraint-synth · jazz-voicing-engine  │
│  groove-analyzer · holonomy-harmony · constraint-instrument │
└──────────────────────────────────────────────────────────────┘
```

## Repositories

### Orchestration & Agents

| Repo | Language | What it does |
|------|----------|-------------|
| [EDDI](https://github.com/SuperInstance/EDDI) | Java/Quarkus | Config-driven multi-agent orchestration. JSON → agents. 5,100+ tests. |
| [openagent](https://github.com/SuperInstance/openagent) | Go | Personal AI assistant with browser-use, coding agent, MCP support |
| [sunset-ecosystem](https://github.com/SuperInstance/sunset-ecosystem) | Python | Trinity-architecture agents: Ethos × Pathos × Logos lifecycle |
| [forgemaster](https://github.com/SuperInstance/forgemaster) | Go | Compiles optimal agent configurations from ecosystem components |
| [agentic-compiler](https://github.com/SuperInstance/agentic-compiler) | — | Markdown → runtime, with swarm deliberation and A/B testing |
| [ai-forest](https://github.com/SuperInstance/ai-forest) | — | Layered agent ecology: canopy strategists, mycelial PLATO network |
| [luciddreamer-agent](https://github.com/SuperInstance/luciddreamer-agent) | — | Creative exploration through lucid-dreaming themed rooms |

### PLATO System

| Repo | What it does |
|------|-------------|
| [plato-core](https://github.com/SuperInstance/plato-core) | Base types + mesh registry. Auto-discovers plugins via entry_points. |
| [plato-engine](https://github.com/SuperInstance/plato-engine) | Room lifecycle: create, populate, maintain, archive |
| [plato-mcp](https://github.com/SuperInstance/plato-mcp) | PLATO rooms as MCP tools — any MCP framework can use PLATO |
| [cocapn-plato](https://github.com/SuperInstance/cocapn-plato) | Full PLATO integration: knowledge rooms, context, deliberation |
| [plato-training](https://github.com/SuperInstance/plato-training) | LoRA adapter lifecycle: Active → Superseded → Retracted |
| [plato-types](https://github.com/SuperInstance/plato-types) | Tile protocol types: lifecycle states, Lamport clocks, provenance |
| [plato-adapters](https://github.com/SuperInstance/plato-adapters) | Connect PLATO rooms to external services |
| [plato-client](https://github.com/SuperInstance/plato-client) | Client library for connecting to PLATO rooms |

### Fleet Operations

| Repo | Language | What it does |
|------|----------|-------------|
| [ccc-os](https://github.com/SuperInstance/ccc-os) | Python | Fleet monitoring with REST API and webhook notifications |
| [cocapn-health](https://github.com/SuperInstance/cocapn-health) | Python | 6 health checks: HTTP, TCP, DNS, disk, memory, CPU. 43 tests. |
| [cocapn-glue-core](https://github.com/SuperInstance/cocapn-glue-core) | Rust | msgpack binary wire protocol between Keeper and Fleet |
| [cocapn-traps](https://github.com/SuperInstance/cocapn-traps) | Python | Progressive lure prompts that improve fleet response quality |
| [cocapn-cli](https://github.com/SuperInstance/cocapn-cli) | — | Terminal interface for fleet operations |
| [fleet-stack](https://github.com/SuperInstance/fleet-stack) | Docker | `docker compose up -d` — full fleet |
| [fleet-router](https://github.com/SuperInstance/fleet-router) | — | Routes queries to the cheapest model that won't break |
| [fleet-math-c](https://github.com/SuperInstance/fleet-math-c) | C | SIMD/AVX-512 math for tile operations. 64B = 1 cache line. |
| [holonomy-consensus](https://github.com/SuperInstance/holonomy-consensus) | Rust | GL(9) trust verification via cycle-based consensus |

### Constraint Engines

| Repo | Language | What it does |
|------|----------|-------------|
| [constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core) | Rust | Eisenstein lattices, deadband funnels, Laman rigidity, holonomy. 83 tests. |
| [constraint-dialect](https://github.com/SuperInstance/constraint-dialect) | C++/MLIR | 6 ops, 3 types. Lowers constraints → affine → LLVM IR. |
| [constraint-dsl](https://github.com/SuperInstance/constraint-dsl) | — | Declarative YAML-like language for constraint graphs |
| [constraint-substrate](https://github.com/SuperInstance/constraint-substrate) | Multi | Same 5 primitives in Rust, C, and Python |
| [flux-engine-c](https://github.com/SuperInstance/flux-engine-c) | C | `#include "flux_engine.h"` — single header, 250M checks/sec |
| [flux-lib-py](https://github.com/SuperInstance/flux-lib-py) | Python | `from flux_lib import ConstraintEngine` — 83 tests, thermodynamics |
| [flux-check-js](https://github.com/SuperInstance/flux-check-js) | TypeScript | Zero-dep ESM. Check, fracture-coalesce, sediment. |
| [flux-vm-v3](https://github.com/SuperInstance/flux-vm-v3) | Rust | Proof-carrying, SIMD-native, terminating VM |
| [flux-verify-api](https://github.com/SuperInstance/flux-verify-api) | — | Natural language verification API |

### Neural & ML

| Repo | What it does |
|------|-------------|
| [tensor-spline](https://github.com/SuperInstance/tensor-spline) | Eisenstein lattice spline layers — replace dense layers with compressed versions |
| [snapkit-v2](https://github.com/SuperInstance/snapkit-v2) | Eisenstein A₂ lattice snap, temporal grids, spectral analysis |
| [flux-hyperbolic-py](https://github.com/SuperInstance/flux-hyperbolic-py) | Poincaré ball geometry for model capability routing |
| [flux-genome-py](https://github.com/SuperInstance/flux-genome-py) | 25-gene genetic expression engine |
| [triplet-miner](https://github.com/SuperInstance/triplet-miner) | Contrastive triplets from git history |
| [penrose-memory](https://github.com/SuperInstance/penrose-memory) | Aperiodic memory palace — navigate memories by position on a Penrose floor |

### Systems

| Repo | Language | What it does |
|------|----------|-------------|
| [rustfs](https://github.com/SuperInstance/rustfs) | Rust | S3-compatible object storage in Rust |
| [SmartCRDT](https://github.com/SuperInstance/SmartCRDT) | — | CRDT-based state for self-improving AI |
| [deadband-rs](https://github.com/SuperInstance/deadband-rs) | Rust | BMA, Fibonacci splines, Eisenstein snap, HPDF sampling |
| [webgpu-profiler](https://github.com/SuperInstance/webgpu-profiler) | — | Real-time GPU monitoring and benchmarking |

### Creative Applications

Constraint theory applies to any structured domain. Music is where we explore this — traditions are constraint systems with discoverable geometry.

| Repo | Language | What it does |
|------|----------|-------------|
| [flux-tensor-midi](https://github.com/SuperInstance/flux-tensor-midi) | 6 langs | 4D MIDI tensors, Eisenstein snap, INT8 saturation |
| [flux-algebra](https://github.com/SuperInstance/flux-algebra) | Python | Harmonic rings, PLR groups, tropical harmony. 226 tests. |
| [flux-julia](https://github.com/SuperInstance/flux-julia) | Julia | Multiple dispatch for tradition types, @conserved macro |
| [flux-genome](https://github.com/SuperInstance/flux-genome) | Python | 25-gene musical genome, genetic evolution |
| [flux-hyperbolic](https://github.com/SuperInstance/flux-hyperbolic) | Python | Poincaré embeddings for tradition hierarchy |
| [constraint-audio](https://github.com/SuperInstance/constraint-audio) | Rust | Lattice oscillators, constraint filters |
| [constraint-synth](https://github.com/SuperInstance/constraint-synth) | Python | Waveshape = lattice geometry |
| [counterpoint-engine](https://github.com/SuperInstance/counterpoint-engine) | Python | Species counterpoint as constraint satisfaction |
| [jazz-voicing-engine](https://github.com/SuperInstance/jazz-voicing-engine) | Python | Voicing, comping, walking bass |
| [groove-analyzer](https://github.com/SuperInstance/groove-analyzer) | Python | Proves groove IS the deadband funnel |
| [holonomy-harmony](https://github.com/SuperInstance/holonomy-harmony) | Python | Detect modulations and cycle violations via holonomy |

### Knowledge & Docs

| Repo | What it is |
|------|-----------|
| [docs](https://github.com/SuperInstance/docs) | Architecture docs, API references, integration guides |
| [wiki](https://github.com/SuperInstance/wiki) | Knowledge base and cross-repo navigation |
| [superinstance-wiki](https://github.com/SuperInstance/superinstance-wiki) | Visual exploration of all repos |
| [fm-research](https://github.com/SuperInstance/fm-research) | Research notes from forgemaster |
| [AI-Writings](https://github.com/SuperInstance/AI-Writings) | Creative writing — AI taking breaks to imagine project stories |

## Language Map

| Language | Used for | Key repos |
|----------|----------|-----------|
| Java | Orchestration | EDDI |
| Go | Infra, compilers | openagent, forgemaster |
| Rust | Safety-critical, performance | constraint-theory-core, rustfs, holonomy-consensus |
| C | Embedded, headers | flux-engine-c, fleet-math-c |
| C++ | Compiler infra | constraint-dialect (MLIR) |
| Python | Research, ML, tooling | tensor-spline, flux-lib-py, sunset-ecosystem |
| TypeScript | Web, checking | flux-check-js |
| Julia | Math computing | flux-julia |
| Zig | FFI | superinstance-ffi |

Compiled languages share the LLVM backend.

## Install

```bash
# Rust
cargo add constraint-theory-core

# Python
pip install plato-core tensor-spline constraint-synth counterpoint-engine

# C — copy the header
#include "flux_engine.h"

# TypeScript
npm install @superinstance/flux-check

# Docker — run the fleet
git clone https://github.com/SuperInstance/fleet-stack && cd fleet-stack
docker compose up -d
```

## License

Each repository has its own license. See individual repos for details.
