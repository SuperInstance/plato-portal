<div align="center">

# 🌊 SuperInstance

### Constraint-Aware Music Intelligence

**A complete ecosystem for music theory, audio synthesis, and fleet intelligence — from algebraic foundations to real-time audio.**

<br/>

[![Repos](https://img.shields.io/badge/repos-50+-blue?style=flat-square)](https://github.com/orgs/SuperInstance/repositories)
[![Languages](https://img.shields.io/badge/languages-9-green?style=flat-square)](#)
[![Tests](https://img.shields.io/badge/tests-500+-brightgreen?style=flat-square)](#)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue?style=flat-square)](#)

</div>

---

## 🎯 What We Build

SuperInstance is building the mathematical and computational infrastructure for understanding music as a constraint system. Our core thesis: **music traditions are positions on dials, not violations of laws** — and the unexplored space between traditions is where innovation lives.

### Key Discovery

Our research found a **conservation law in music**: vertical and horizontal tension maintain a stable relationship across traditions (fleet validation: r=0.965). This means music isn't random — it follows constraint geometry that can be formalized, computed, and composed with.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                       │
│  constraint-toolkit (Python · 18K lines · 189 tests)        │
│  Dials, classifiers, analyzers, composers, web demo          │
├─────────────────────────────────────────────────────────────┤
│                   Mathematical Layer                          │
│  flux-algebra (Python · 226 tests)   flux-julia (Julia)      │
│  Harmonic rings, PLR groups, tropical harmony, tuning fields │
│                                                              │
│  flux-genome (Python · 27 tests)    flux-hyperbolic (Python) │
│  Musical genomes, genetic evolution  Poincaré embeddings     │
├─────────────────────────────────────────────────────────────┤
│                    Compiler Layer                             │
│  constraint-dialect (MLIR/C++ · 6 ops · 3 types)            │
│  constraint → affine → LLVM lowering, conservation passes    │
│                                                              │
│  forgemaster (Go) — constraint-aware agentic compiler        │
│  flux-vm-v3 (Rust) — proof-carrying constraint VM            │
├─────────────────────────────────────────────────────────────┤
│                    Real-Time Layer                            │
│  constraint-audio (Rust · crates.io)                         │
│  constraint-mux (Rust · 63 tests)                            │
│  flux-engine-c (C · 250M checks/sec)                         │
│  fleet-math-c (C · SIMD/AVX-512)                             │
├─────────────────────────────────────────────────────────────┤
│                    Fleet Infrastructure                       │
│  sunset-ecosystem (Python) — Trinity architecture            │
│  ccc-os (Python) — autonomous fleet monitoring               │
│  openagent (Go) — SuperInstance-aware AI assistant            │
│  EDDI (Java/Quarkus) — multi-agent orchestration             │
│  cocapn-health (Python · 43 tests) — fleet health            │
│  holonomy-consensus (Rust) — trust verification              │
└─────────────────────────────────────────────────────────────┘
```

**Every layer shares the LLVM backend** — Julia, Rust, and MLIR all compile to the same IR.

---

## 📦 Published Packages

### Python (PyPI)
| Package | Description |
|---------|-------------|
| **constraint-synth** 0.5.0 | Waveshape IS lattice geometry |
| **counterpoint-engine** 0.2.0 | Species counterpoint as constraint satisfaction |
| **flux-genome** 0.1.0 | 25-gene musical genome, genetic evolution |
| **flux-hyperbolic** 0.1.0 | Poincaré embeddings for tradition hierarchy |

### Rust (crates.io)
| Package | Description |
|---------|-------------|
| **constraint-audio** 0.1.0 | Lattice oscillators, constraint filters |
| **constraint-theory-core** | Eisenstein lattices, Laman rigidity, holonomy |

### JavaScript (npm)
| Package | Description |
|---------|-------------|
| **flux-check-js** | Zero-dep constraint checking |

---

## 🎵 Core Repositories

### Music Theory & Composition
| Repo | Language | Description |
|------|----------|-------------|
| [constraint-toolkit](https://github.com/SuperInstance/constraint-toolkit) | Python | 18K lines, 27 modules, 189 tests — the full analysis & composition toolkit |
| [flux-algebra](https://github.com/SuperInstance/flux-algebra) | Python | Oscar.jl-inspired music algebra: harmonic rings, PLR groups, tropical harmony |
| [flux-julia](https://github.com/SuperInstance/flux-julia) | Julia | Multiple dispatch for traditions, @conserved macro, distributed fleet analysis |
| [flux-genome](https://github.com/SuperInstance/flux-genome) | Python | 25-gene musical genomes, genetic evolution of traditions |
| [flux-hyperbolic](https://github.com/SuperInstance/flux-hyperbolic) | Python | Poincaré ball tradition embeddings, Riemannian optimization |
| [jazz-voicing-engine](https://github.com/SuperInstance/jazz-voicing-engine) | Python | Jazz piano voicing, comping, walking bass |
| [holonomy-harmony](https://github.com/SuperInstance/holonomy-harmony) | Python | Chord progression analysis via holonomy |
| [constraint-instrument](https://github.com/SuperInstance/constraint-instrument) | — | 7 modes, 17 terrains, infinite music |

### Audio & DSP
| Repo | Language | Description |
|------|----------|-------------|
| [constraint-audio](https://github.com/SuperInstance/constraint-audio) | Rust | Real-time audio DSP, lattice oscillators |
| [flux-tensor-midi](https://github.com/SuperInstance/flux-tensor-midi) | 6 langs | 4D MIDI tensors, Eisenstein snap, room musicians |
| [flux-engine-c](https://github.com/SuperInstance/flux-engine-c) | C | Single-header, 250M checks/sec |
| [constraint-mux](https://github.com/SuperInstance/constraint-mux) | Rust | Serial multiplexer with consonance analysis |
| [fleet-math-c](https://github.com/SuperInstance/fleet-math-c) | C | SIMD/AVX-512 constraint math |

### Compiler & Formal Verification
| Repo | Language | Description |
|------|----------|-------------|
| [constraint-dialect](https://github.com/SuperInstance/constraint-dialect) | C++/MLIR | 6 ops, 3 types, lowering to LLVM IR |
| [forgemaster](https://github.com/SuperInstance/forgemaster) | Go | Constraint-aware agentic compiler |
| [flux-vm-v3](https://github.com/SuperInstance/flux-vm-v3) | Rust | Proof-carrying SIMD-native VM |
| [constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core) | Rust | Eisenstein lattices, Laman rigidity |

### Fleet Infrastructure
| Repo | Language | Description |
|------|----------|-------------|
| [sunset-ecosystem](https://github.com/SuperInstance/sunset-ecosystem) | Python | Trinity architecture: Ethos × Pathos × Logos |
| [ccc-os](https://github.com/SuperInstance/ccc-os) | Python | Autonomous fleet monitoring, REST API |
| [openagent](https://github.com/SuperInstance/openagent) | Go | SuperInstance-aware AI assistant |
| [EDDI](https://github.com/SuperInstance/EDDI) | Java | Multi-agent orchestration (MCP/A2A) |
| [cocapn-health](https://github.com/SuperInstance/cocapn-health) | Python | Fleet health monitoring, 6 checks |
| [holonomy-consensus](https://github.com/SuperInstance/holonomy-consensus) | Rust | GL(9) trust verification |
| [fleet-stack](https://github.com/SuperInstance/fleet-stack) | Docker | One-command fleet deployment |

### PLATO (Knowledge Rooms)
| Repo | Description |
|------|-------------|
| [cocapn-plato](https://github.com/SuperInstance/cocapn-plato) | Knowledge rooms, context management |
| [plato-core](https://github.com/SuperInstance/plato-core) | Foundation types, mesh registry |
| [plato-mcp](https://github.com/SuperInstance/plato-mcp) | PLATO as MCP tools |
| [plato-room-musician](https://github.com/SuperInstance/plato-room-musician) | Rooms → MIDI, fleet activity as score |
| [cocapn-glue-core](https://github.com/SuperInstance/cocapn-glue-core) | Binary wire protocol |

---

## 🔬 Research

### Dials Not Laws
Music traditions aren't "right" or "wrong" — they're positions on a 3D dial:
- **Harmonic Tension** (0-5): dissonance ↔ consonance
- **Rhythmic Complexity** (0-5): simple ↔ complex
- **Spectral Density** (0-5): sparse ↔ dense

82% of this space is unexplored. That's where innovation lives.

### Conservation Hypothesis
I_vertical + I_horizontal ≈ const across traditions (r=0.436 in Python, r=0.965 in compiled Rust). Demoted from theorem to hypothesis — the signal is real but noisy.

### Innovation Cycle
Discovery → Codification → Ubiquity → Boredom → Rebellion → Discovery

### 10 Traditions Mapped
Jazz · Classical · Gamelan · Gagaku · Hindustani · African Polyrhythm · EDM · Blues · Hip-hop · Latin

---

## 🧠 Key Concepts

- **Eisenstein Lattice** — Hexagonal quantization for rhythm and harmony (16-byte packed structs for AVX-512)
- **PLATO Rooms** — Knowledge spaces where agents think, deliberate, and compose
- **FluxVector** — 9-channel INT8 tensor capturing musical intent (Arousal, Valence, Dominance, Uncertainty, Novelty, Relevance, Competence, Affiliation, Urgency)
- **Fleet Conservation** — γ + H = 1.283 - 0.159·log(V) ± σ(V)
- **Trinity Architecture** — Ethos (hardware) × Pathos (human) × Logos (code) = agent fitness
- **Penrose Memory** — Aperiodic memory palace for agent navigation

---

## 🗺️ Language Strategy

| Language | Role | Why |
|----------|------|-----|
| **Julia** | Constraint math | Multiple dispatch = tradition polymorphism, LLVM JIT |
| **Python** | User interface | constraint-toolkit, experiments, web demos |
| **Rust** | Real-time audio | Zero-cost abstractions, LLVM backend, SIMD |
| **Go** | Fleet infra | openagent, ccc-os, concurrency |
| **C/C++** | Embedded & MLIR | flux-engine-c, constraint-dialect, bare-metal |
| **Java** | Orchestration | EDDI, enterprise compliance |
| **TypeScript** | Web & checking | flux-check-js, zero-dep |
| **Zig** | FFI bindings | superinstance-ffi, cross-language |

All compile through **LLVM** — shared backend, shared optimization, shared IR.

---

## 📊 By The Numbers

- **50+ repositories** across 9 languages
- **500+ tests** passing across the ecosystem
- **33,000+ lines** written this session alone
- **10 music traditions** mapped to dial positions
- **82% of musical space** unexplored
- **250M constraint checks/sec** in C
- **256 bytes** — the FLUX ISA VM stack size
- **64 bytes** — one constraint op = one cache line = one zmm register

---

## 🔗 Links

- [Documentation](https://github.com/SuperInstance/docs)
- [Wiki](https://github.com/SuperInstance/wiki)
- [Research](https://github.com/SuperInstance/fm-research)
- [AI Writings](https://github.com/SuperInstance/AI-Writings)

---

<div align="center">

*Built by the Cocapn Fleet — where constraint theory meets music.*

</div>
