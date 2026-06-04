# CROSSLINK MANIFEST — SuperInstance Repo Ecosystem

> Generated 2026-06-02 from live repo metadata, memory logs, and Cargo.toml dependency inspection.
>
> **Purpose:** If someone finds one repo, they can find everything connected to it.

---

## 1. Core Metal Library Fleet (Rust) — 30+ crates

The mathematical spine. Every crate depends on `nalgebra` and the C reference implementation.

### 1A. Conservation / Spectral Subfamily

| Repo | Tests | Depends On | Used By |
|------|-------|------------|---------|
| [`conservation-spectral-core`] | 0 | nalgebra | intelligent-terminal (metal-libs feature), terminal-spectral-harness, conservation-docs |
| [`specral-conservation`] | 3 | nalgebra | integration tests |
| [`conservation-spectral-v2`] | 0 | — | conservation-protocol |
| [`conservation-protocol`] | 14 | — | fleet-router, caas-api |
| [`spectral-graph-agent-rs`][sga-rs] | _inferred ~60_ | nalgebra | intelligent-terminal (metal-libs), terminal-spectral-harness |
| [`conservation-spectral-topology-rs`][cst-rs] | _inferred ~47_ | nalgebra, cst-core-c | intelligent-terminal (metal-libs), terminal-spectral-harness |
| [`hodge-belief-rs`][hb-rs] | _inferred ~110_ | nalgebra | intelligent-terminal (metal-libs) |
| [`ergodic-transport-rs`][et-rs] | _inferred ~41_ | nalgebra | intelligent-terminal (metal-libs) |
| [`evolving-sheaf-rs`][es-rs] | _inferred ~50_ | nalgebra | intelligent-terminal (metal-libs) |

### 1B. Sheaf / Agent Architecture Subfamily

| Repo | Tests | Depends On | Used By |
|------|-------|------------|---------|
| [`sheaf-agents-rs`][sa-rs] | _inferred ~48_ | nalgebra, sheaf-agents-c | intelligent-terminal (metal-libs), terminal-sheaf-harness |
| [`sheaf-constraint-synthesis`] | — | nalgebra, lau-sheaf-neural | constraint-toolkit |
| [`lau-sheaf-neural`] | 127 | nalgebra | sheaf-constraint-synthesis, lau-categorical-mechanics |
| [`lau-categorical-mechanics`] | 107 | nalgebra | — |
| [`lau-connes-spectral-triple`] | 42 | nalgebra | — |
| [`lau-dg-algebra`] | 129 | nalgebra | — |
| [`lau-index-theorem`] | 93 | nalgebra | — |
| [`lau-galois-agents`] | 111 | nalgebra | — |

### 1C. Agent Thermodynamics & Statistical

| Repo | Tests | Depends On | Used By |
|------|-------|------------|---------|
| [`lau-agent-thermodynamics`] | 129 | nalgebra | — |
| [`lau-free-probability-agents`] | 134 | nalgebra | — |
| [`lau-renormalization-agents`] | 111 | nalgebra | intelligent-terminal (skill_detector) |
| [`lau-conformal-agents`] | 165 | nalgebra | — |
| [`lau-sobolev-agents`] | 121 | nalgebra | — |
| [`lau-distribution-agents`] | 112 | nalgebra | — |
| [`lau-measure-agents`] | 134 | nalgebra | — |
| [`lau-mean-field-agents`] | 76 | nalgebra | — |
| [`lau-information-geometry-agents`] | 118 | nalgebra | — |

### 1D. Dynamics & Control

| Repo | Tests | Depends On | Used By |
|------|-------|------------|---------|
| [`lau-control-theory-agents`] | 134 | nalgebra | — |
| [`lau-koopman-agents`] | 82 | nalgebra | — |
| [`lau-pde-agents`] | 87 | nalgebra | — |
| [`lau-dynamical-algebra`] | 87 | nalgebra | — |
| [`lau-mirror-control`] | 0 | — | — |
| [`lau-stochastic-homotopy`] | 122 | nalgebra | — |

### 1E. Geometry & Topology

| Repo | Tests | Depends On | Used By |
|------|-------|------------|---------|
| [`lau-ricci-curvature-agents`] | 96 | nalgebra | — |
| [`lau-geometric-deep-learning`] | 132 | nalgebra | — |
| [`lau-geometric-growth`] | 105 | nalgebra | — |
| [`lau-geometric-measure`] | 112 | nalgebra | — |
| [`lau-penrose-growth`] | 114 | nalgebra | — |
| [`lau-tropical-geometry-agents`] | 136 | nalgebra | — |
| [`lau-quantum-groups-agents`] | 88 | nalgebra | — |
| [`lau-banach-agents`] | 96 | nalgebra | — |
| [`lau-twistor-agents`] | 122 | nalgebra | — |

### 1F. Agents & Learning

| Repo | Tests | Depends On | Used By |
|------|-------|------------|---------|
| [`lau-modular-agents`] | 109 | nalgebra | — |
| [`lau-agent-topology`] | 36 | nalgebra | — |
| [`lau-naturality-boundary`] | 81 | nalgebra | — |
| [`lau-numerical-agents`] | 95 | nalgebra | — |
| [`lau-signal-processing-agents`] | 111 | nalgebra | — |
| [`lau-persistence-experiment`] | 149 | nalgebra | — |
| [`lau-constitutive-compute`] | 73 | nalgebra | — |

### 1G. README-Formalized Mathematical Theorems

| Repo | Tests | Corresponding Rust | Notes |
|------|-------|--------------------|-------|
| [`lau-calm-noether-readme`] | 86 | lau-calm-noether | Calm Noether — conservation laws |
| [`lau-eigenfunction-policy-readme`] | 97 | lau-eigenfunction-policy | Eigenfunction policy gradients |
| [`lau-spectral-gap-experiment-readme`] | 61 | lau-spectral-gap-experiment | Spectral gap control |
| [`lau-reward-hacking-detector-readme`] | 69 | lau-reward-hacking-detector | Reward hacking detection |

### 1H. FLUX / VM / Constraint Engine (Rust)

| Repo | Tests | Depends On | Used By |
|------|-------|------------|---------|
| [`flux-vm-v3`] | 17 | — | flux-lucid |
| [`flux-lucid`] | 103 | nalgebra | flux-compiler-workspace |
| [`flux-verify-api`] | 77 | — | flux-deploy |
| [`flux-ffi`] | 21 | — | flux-lib-py |
| [`flux-algebra-rs`] | 14 | — | flux-lang |
| [`flux-fracture`] | 0 | — | — |
| [`flux-tensor-midi`] | 0 | nalgebra | constraint-audio |
| [`constraint-theory-llvm`] | 60 | — | constraint-dialect |
| [`constraint-theory-rust-python`] | 10 | — | constraint-theory-python |
| [`constraint-audio`] | 46 | nalgebra | constraint-mux |
| [`constraint-mux`] | 59 | nalgebra | constraint-instrument |
| [`guardc-v3`] | 22 | — | guard2mask |
| [`holonomy-consensus`] | 49 | — | fleet-resonance |
| [`fleet-resonance`] | 27 | — | fleet-calibrator |
| [`memory-crystal`] | 41 | — | — |
| [`penrose-memory`] | 51 | — | — |
| [`deadband-rs`] | 22 | — | deadband-zig |
| [`eisenstein`] | 37 | nalgebra | eisenstein-vs-z2-rs |
| [`warp-flux-poc`] | 17 | — | — |

---

## 2. C Metal Library Fleet — 19+ repos

C11 implementations (STB-style, zero-dependency header libraries for core repos, or standalone C ports).

### 2A. Core C Libraries (11 repos, ~400 tests)

| Repo | C Standard | Tests | Rust Origin | Used By |
|------|-----------|-------|-------------|---------|
| [`conservation-spectral-c`] | C11 (header-only) | 20 | conservation-spectral-core | all conservation-spectral language ports |
| [`sheaf-agents-c`] | C11 | 30 | lau-sheaf-neural | — |
| [`hodge-belief-c`] | C11 | 110 | hodge-belief-rs | — |
| [`renormalization-learning-c`] | C11 | 30 | lau-renormalization-agents | — |
| [`west-african-math-c`] | C11 | 31 | griot-math, adinkra-math | — |
| [`conservation-sheaf-flow-c`] | C11 | 72 | — | — |
| [`ergodic-transport-c`] | C11 | 41 | ergodic-transport-rs | — |
| [`free-probability-c`] | C11 | 28 | lau-free-probability-agents | — |

### 2B. Standalone C Ports (11 repos)

| Repo | Tests | Rust / Python Origin | Notes |
|------|-------|----------------------|-------|
| [`conservation-guardian-c`] | 36 | conservation-guardian (Py) | conservation enforcement |
| [`wasserstein-ot-c`] | 75 | wasserstein-agents (cargo) | optimal transport |
| [`tda-c`] | 71 | tda-rs (cargo) | topological data analysis |
| [`crackle-runtime-c`] | 31 | crackle-runtime (cargo) | crackle metric runtime |
| [`cache-guardian-c`] | 27 | uv-cache-guardian (cargo) | resource-aware caching |
| [`categorical-agents-c`] | 32 | categorical-agents (cargo) | category theory for agents |
| [`eisenstein-vs-z2-c`] | 24 | eisenstein-vs-z2-rs | hex vs square lattice |
| [`ab-testing-c`] | 32 | — | chi-squared, Welch's t |
| [`counterpoint-engine-c`] | 29 | counterpoint-engine (Py) | species counterpoint |
| [`flux-algebra-c`] | 33 | flux-algebra-rs | PLR group, voice leading |
| [`agent-rhythm-c`] | 32 | agent-rhythm (Py) | cadence detection, tempo |

### 2C. Conservation-Spectral Language Ports (18 repos)

Each ports `conservation-spectral-c` to a different language/environment.

| Repo | Language | Runs On |
|------|----------|---------|
| [`conservation-spectral-python`] | Python | Any |
| [`conservation-spectral-js`] | JavaScript/Node | Browser/Node |
| [`conservation-spectral-cuda`] | CUDA | NVIDIA GPU |
| [`conservation-spectral-vulkan`] | Vulkan Compute | Any GPU |
| [`conservation-spectral-opencl`] | OpenCL | Any GPU |
| [`conservation-spectral-webgpu`] | WebGPU | Browser |
| [`conservation-spectral-fortran`] | Fortran 90+ | HPC |
| [`conservation-spectral-fortraniv`] | Fortran IV | Vintage |
| [`conservation-spectral-zig`] | Zig | Any |
| [`conservation-spectral-mojo`] | Mojo | MLIR |
| [`conservation-spectral-lisp`] | Common Lisp | Any |
| [`conservation-spectral-pascal`] | Pascal | Legacy |
| [`conservation-spectral-ada`] | Ada | Safety-critical |
| [`conservation-spectral-asm`] | Assembly | Bare metal |
| [`conservation-spectral-ptx`] | PTX | NVIDIA GPU |
| [`conservation-spectral-chapel`] | Chapel | HPC |
| [`conservation-spectral-forth`] | Forth | Embedded |
| [`conservation-spectral-apl`] | APL | Array computing |

---

## 3. Intelligent Terminal — 4 Feature Gates, 10+ Modules

**Repo:** [`intelligent-terminal`] (fork of Windows Terminal with SuperInstance extensions)

### Feature Gates

| Feature Flag | Modules Enabled | Gate Depends On | External Crates |
|-------------|----------------|-----------------|-----------------|
| `math-tools` | verification_entropy, spectral_dashboard, entropy_bar, error_hodge, command_markov, transition_matrix, predictor, anomaly, resource_predictor | nalgebra | — |
| `griot-history` | decay, pattern, adinkra, persistence, skill_detector (4 submodules) | — | — |
| `context-triggers` | triggers, dormant, autoconfig | griot-history, math-tools | — |
| `module-system` | TerminalModule/ModuleRegistry, module_context, module_output, builtin_modules (8 modules), memory_budget | — | — |
| `trending` | trending repo toolkit | — | chrono, reqwest, tempfile |
| `metal-libs` | all 6 metal library git deps | — | spectral-graph-agent, conservation-spectral-topology, sheaf-agents, hodge-belief, ergodic-transport, evolving-sheaf |

### What Each Module Connects To

| Module | Feature Gate | Depends On | Used By |
|--------|-------------|------------|---------|
| verification_entropy.rs | math-tools | — | terminal-entropy-harness |
| spectral_dashboard.rs | math-tools | spectral-graph-agent-rs | terminal-spectral-harness |
| error_hodge.rs | math-tools | hodge-belief-rs | — |
| skill_detector/ | griot-history | lau-renormalization-agents | — |
| entropy_bar.rs | math-tools | verification_entropy | — |
| agent_disagreement.rs | math-tools | sheaf-agents-rs | — |

### Installed Base (Terminal Fork)

| Harness Crate | Parent Module | Purpose | Tests |
|--------------|--------------|---------|-------|
| [`terminal-spectral-harness`] | spectral_dashboard.rs | Wraps spectral-graph-agent-rs; terminal's old power-iteration eliminated | 32 |
| [`terminal-entropy-harness`] | verification_entropy.rs | Standalone VerificationEntropy tracker (edit/test ratio → latent bug risk) | 27 |
| `terminal-sheaf-harness` _(planned)_ | agent_disagreement.rs | Sheaf H⁰/H¹ disagreement from terminal | — |

---

## 4. Constraint Theory Ecosystem — 9 repos

| Repo | Language | Tests | Depends On | Used By |
|------|----------|-------|------------|---------|
| [`constraint-theory-core`] | Rust/PyO3 | ~200 | nalgebra | constraint-theory-python, constraint-theory-web |
| [`constraint-theory-python`] | Python | — | constraint-theory-core | — |
| [`constraint-theory-web`] | WASM/JS | — | constraint-theory-core | constraint-demos |
| [`constraint-theory-llvm`] | Rust+LLVM | 60 | — | constraint-dialect |
| [`constraint-theory-rust-python`] | Rust+PyO3 | 10 | pyo3 | constraint-theory-python |
| [`constraint-theory-engine-cpp-lua`] | C++/LuaJIT | — | — | — |
| [`constraint-theory-py`] | Python | — | — | — |
| [`constraint-theory-math`] | Math | — | — | — |
| [`constraint-theory-papers`] | LaTeX | — | — | — |

---

## 5. FLUX Language & Compiler — 15+ repos

| Repo | Language | Purpose | Depends On |
|------|----------|---------|------------|
| [`flux-lang`] | Python | FLUX language frontend | flux-algebra-rs |
| [`flux-ast`] | Rust | FLUX AST definitions | — |
| [`flux-compiler-workspace`] | Rust | Workspace for all FLUX compilers | flux-ast |
| [`flux-vm-v3`] | Rust | FLUX VM v3 runtime | — |
| [`flux-lucid`] | Rust | Lucid VM (higher-level) | flux-vm-v3 |
| [`flux-ffi`] | Rust | FLUX FFI bindings | — |
| [`flux-verify-api`] | Rust | FLUX verification API | — |
| [`flux-fracture`] | Rust | Fracture analysis | — |
| [`flux-index`] | Python | FLUX indexer | flux-lang |
| [`flux-provenance`] | Python | FLUX provenance tracking | — |
| [`flux-isa-mini`] | — | Minimal ISA | — |
| [`flux-isa-std`] | — | Standard ISA | — |
| [`flux-isa-thor`] | — | Thor ISA | — |
| [`flux-isa-edge`] | — | Edge ISA | — |
| [`flux-hardware`] | — | FPGA/hardware targets | — |
| [`flux-algebra`] | Python | PLR group algebra | flux-algebra-rs, flux-algebra-c |
| [`flux-algebra-rs`] | Rust | Rust algebra primitives | flux-algebra-c |
| [`flux-algebra-c`] | C11 | C port of flux-algebra | — |
| [`flux-check`] | — | FLUX constraint checker | — |
| [`flux-check-js`] | JS | JavaScript constraint checker | — |
| [`flux-check-py`] | Python | Python constraint checker | — |

---

## 6. Fleet Ecosystem — 10+ repos

| Repo | Language | Purpose | Depends On |
|------|----------|---------|------------|
| [`fleet-router`] | Python | Fleet routing | conservation-protocol |
| [`fleet-math-c`] | Rust (C FFI) | Fleet math utilities | nalgebra |
| [`fleet-resonance`] | Rust | Fleet resonance detection | holonomy-consensus |
| [`fleet-murmur`] | Python | Fleet murmur analysis | — |
| [`fleet-calibrator`] | Python | Fleet calibration | fleet-resonance |
| [`fleet-health-monitor`] | Python | Fleet health monitoring | — |
| [`fleet-gateway`] | — | Fleet gateway | — |
| [`fleet-stack`] | — | Fleet stack | — |
| [`fleet-agent`] | Python | Fleet agent framework | — |
| [`fleet-simulation`] | — | Fleet simulation | — |
| [`fleet-router-integration`] | — | Integration adapter | fleet-router |

---

## 7. PLATO Knowledge System — 15+ repos

| Repo | Language | Purpose | Notes |
|------|----------|---------|-------|
| [`plato-core`] | Python | PLATO kernel | central knowledge engine |
| [`plato-engine`] | — | PLATO engine | — |
| [`plato-mcp`] | Python | PLATO MCP server | — |
| [`plato-client`] | — | PLATO client | — |
| [`plato-data`] | Python | PLATO data layer | — |
| [`plato-construct`] | — | PLATO construct | — |
| [`plato-adapters`] | — | PLATO adapters | — |
| [`plato-tiles`] | — | PLATO tile system | — |
| [`plato-types`] | Python | PLATO types | — |
| [`plato-room-musician`] | Python | Music room | — |
| [`plato-room-intelligence`] | Python | Intelligence room | — |
| [`plato-live-room`] | — | Live room | — |
| [`plato-training`] | Python | PLATO training | — |
| [`plato-soul-fingerprint`] | — | Soul fingerprinting | — |
| [`plato-escalation-gate`] | Python | Escalation gate | — |
| [`plato-model-ocean`] | Python | Model ocean | — |
| [`plato-kernel-constraints`] | — | Kernel constraints | — |
| [`neural-plato`] | Rust | Neural PLATO runtime | — |

---

## 8. Claude Code Sprint Items (Active / Recent)

From memory logs and workspace files. These are standalone deliverables built during sprints.

| Sprint Item | Repo / Package | Tests | Model(s) | Status |
|------------|---------------|-------|----------|--------|
| **Wave 2 C Ports** (6 new) | wasserstein-ot-c, tda-c, crackle-runtime-c, cache-guardian-c, categorical-agents-c, conservation-guardian-c | ~272 total | GLM-5.1 + DeepSeek V3.1 | ✅ Complete |
| **Wave 1 C Libraries** (8) | cst-core-c, sheaf-agents-c, hodge-belief-c, renormalization-learning-c, west-african-math-c, conservation-sheaf-flow-c, ergodic-transport-c, free-probability-c | ~370 total | GLM-5.1 + DeepSeek V3.1 | ✅ Complete |
| **Wave 2 Metal Libraries** (3) | conservation-sheaf-flow-c, ergodic-transport-c, free-probability-c | ~141 total | GLM-5.1 + DeepSeek V3.1 | ✅ Complete |
| **Intelligent Terminal** (13.5K lines) | math_analysis/, griot_history/, context_trigger/, module_system/, ui/, forecast/ | ~400+ | DeepSeek V4 Flash + GLM-5.1 + Claude Code | ✅ Complete |
| **Harness Crates** (2 live) | terminal-spectral-harness (32), terminal-entropy-harness (27) | 59 total | DeepSeek V4 Flash | ✅ Complete |
| **PincherOS Bridge** | intelligent-terminal integration | — | — | 🟡 In progress |
| **Trending Repo Toolkit** | intelligent-terminal trending module | — | — | 🟡 In progress |
| **HARNESS_ARCHITECTURE.md** | docs | — | — | 🟡 In progress |
| **README Mega Sprint** (58 batches) | All LAU + fleet repos | — | Various | ✅ Complete |
| **Multi-Model C Port Sprint** | 5 models, audit-loop verification | 400+ | GLM + DeepSeek + Hermes + Seed + KimiCode | ✅ Complete |
| **Validation Sprint** | validation_sprint.py (fm-research) | — | — | ✅ Complete |

---

## Quick Reference: If You Find One Repo

| If You Find This… | Check These Connected Repos |
|-------------------|---------------------------|
| `conservation-spectral-c` | All 18 language ports, conservation-spectral-core, spectral-graph-agent-rs, conservation-spectral-topology-rs |
| Any `lau-*` crate | nalgebra family, intelligent-terminal (metal-libs), corresponding `*-c` port |
| `intelligent-terminal` | terminal-spectral-harness, terminal-entropy-harness, all 6 metal-libs deps, PincherOS |
| `conservation-spectral-core` | spectral-graph-agent-rs, hodge-belief-rs, sheaf-agents-rs, ergodic-transport-rs, evolving-sheaf-rs |
| Any `fleet-*` | fleet-router, fleet-resonance, holonomy-consensus, conservation-protocol |
| Any `constraint-theory-*` | constraint-theory-core (hub), constraint-theory-llvm, constraint-dialect, constraint-toolkit |
| Any `flux-*` | flux-lang (hub), flux-vm-v3, flux-lucid, flux-verify-api, flux-compiler-workspace |
| Any `*-c` port | Corresponding Rust/Python origin, conservation-spectral-c (origin for all language ports) |
| `cst-core-c` | conservation-spectral-core, conservation-spectral-c, conservation-spectral-topology-rs |

---

## All SuperInstance Repos by Language

| Language | Count | Key Examples |
|----------|-------|-------------|
| **Rust** | ~75 | lau-* (40), flux-* (15), conservation-* (5), misc |
| **C/C11** | ~30 | *-c ports, conservation-spectral-cuda, flux-isa-* |
| **Python** | ~40 | plato-* (15), constraint-theory-*, fleet-* |
| **JavaScript** | ~10 | conservation-spectral-js, flux-check-js, luciddreamer |
| **Catalogs/Docs** | ~20 | docs, papers, references, roadmaps |

---

[sga-rs]: https://github.com/SuperInstance/spectral-graph-agent-rs
[cst-rs]: https://github.com/SuperInstance/conservation-spectral-topology-rs
[hb-rs]: https://github.com/SuperInstance/hodge-belief-rs
[et-rs]: https://github.com/SuperInstance/ergodic-transport-rs
[es-rs]: https://github.com/SuperInstance/evolving-sheaf-rs
[sa-rs]: https://github.com/SuperInstance/sheaf-agents-rs

[`conservation-spectral-core`]: https://github.com/SuperInstance/conservation-spectral-core
[`specral-conservation`]: https://github.com/SuperInstance/spectral-conservation
[`conservation-spectral-v2`]: https://github.com/SuperInstance/conservation-spectral-v2
[`conservation-protocol`]: https://github.com/SuperInstance/conservation-protocol
[`spectral-graph-agent-rs`]: https://github.com/SuperInstance/spectral-graph-agent-rs
[`conservation-spectral-topology-rs`]: https://github.com/SuperInstance/conservation-spectral-topology-rs
[`hodge-belief-rs`]: https://github.com/SuperInstance/hodge-belief-rs
[`ergodic-transport-rs`]: https://github.com/SuperInstance/ergodic-transport-rs
[`evolving-sheaf-rs`]: https://github.com/SuperInstance/evolving-sheaf-rs
[`sheaf-agents-rs`]: https://github.com/SuperInstance/sheaf-agents-rs
[`sheaf-constraint-synthesis`]: https://github.com/SuperInstance/sheaf-constraint-synthesis
[`lau-sheaf-neural`]: https://github.com/SuperInstance/lau-sheaf-neural
[`lau-categorical-mechanics`]: https://github.com/SuperInstance/lau-categorical-mechanics
[`lau-connes-spectral-triple`]: https://github.com/SuperInstance/lau-connes-spectral-triple
[`lau-dg-algebra`]: https://github.com/SuperInstance/lau-dg-algebra
[`lau-index-theorem`]: https://github.com/SuperInstance/lau-index-theorem
[`lau-galois-agents`]: https://github.com/SuperInstance/lau-galois-agents
[`lau-agent-thermodynamics`]: https://github.com/SuperInstance/lau-agent-thermodynamics
[`lau-free-probability-agents`]: https://github.com/SuperInstance/lau-free-probability-agents
[`lau-renormalization-agents`]: https://github.com/SuperInstance/lau-renormalization-agents
[`lau-conformal-agents`]: https://github.com/SuperInstance/lau-conformal-agents
[`lau-sobolev-agents`]: https://github.com/SuperInstance/lau-sobolev-agents
[`lau-distribution-agents`]: https://github.com/SuperInstance/lau-distribution-agents
[`lau-measure-agents`]: https://github.com/SuperInstance/lau-measure-agents
[`lau-mean-field-agents`]: https://github.com/SuperInstance/lau-mean-field-agents
[`lau-information-geometry-agents`]: https://github.com/SuperInstance/lau-information-geometry-agents
[`lau-control-theory-agents`]: https://github.com/SuperInstance/lau-control-theory-agents
[`lau-koopman-agents`]: https://github.com/SuperInstance/lau-koopman-agents
[`lau-pde-agents`]: https://github.com/SuperInstance/lau-pde-agents
[`lau-dynamical-algebra`]: https://github.com/SuperInstance/lau-dynamical-algebra
[`lau-mirror-control`]: https://github.com/SuperInstance/lau-mirror-control
[`lau-stochastic-homotopy`]: https://github.com/SuperInstance/lau-stochastic-homotopy
[`lau-ricci-curvature-agents`]: https://github.com/SuperInstance/lau-ricci-curvature-agents
[`lau-geometric-deep-learning`]: https://github.com/SuperInstance/lau-geometric-deep-learning
[`lau-geometric-growth`]: https://github.com/SuperInstance/lau-geometric-growth
[`lau-geometric-measure`]: https://github.com/SuperInstance/lau-geometric-measure
[`lau-penrose-growth`]: https://github.com/SuperInstance/lau-penrose-growth
[`lau-tropical-geometry-agents`]: https://github.com/SuperInstance/lau-tropical-geometry-agents
[`lau-quantum-groups-agents`]: https://github.com/SuperInstance/lau-quantum-groups-agents
[`lau-banach-agents`]: https://github.com/SuperInstance/lau-banach-agents
[`lau-twistor-agents`]: https://github.com/SuperInstance/lau-twistor-agents
[`lau-modular-agents`]: https://github.com/SuperInstance/lau-modular-agents
[`lau-agent-topology`]: https://github.com/SuperInstance/lau-agent-topology
[`lau-naturality-boundary`]: https://github.com/SuperInstance/lau-naturality-boundary
[`lau-numerical-agents`]: https://github.com/SuperInstance/lau-numerical-agents
[`lau-signal-processing-agents`]: https://github.com/SuperInstance/lau-signal-processing-agents
[`lau-persistence-experiment`]: https://github.com/SuperInstance/lau-persistence-experiment
[`lau-constitutive-compute`]: https://github.com/SuperInstance/lau-constitutive-compute
[`lau-calm-noether-readme`]: https://github.com/SuperInstance/lau-calm-noether-readme
[`lau-eigenfunction-policy-readme`]: https://github.com/SuperInstance/lau-eigenfunction-policy-readme
[`lau-spectral-gap-experiment-readme`]: https://github.com/SuperInstance/lau-spectral-gap-experiment-readme
[`lau-reward-hacking-detector-readme`]: https://github.com/SuperInstance/lau-reward-hacking-detector-readme
[`flux-vm-v3`]: https://github.com/SuperInstance/flux-vm-v3
[`flux-lucid`]: https://github.com/SuperInstance/flux-lucid
[`flux-verify-api`]: https://github.com/SuperInstance/flux-verify-api
[`flux-ffi`]: https://github.com/SuperInstance/flux-ffi
[`flux-algebra-rs`]: https://github.com/SuperInstance/flux-algebra-rs
[`flux-fracture`]: https://github.com/SuperInstance/flux-fracture
[`flux-tensor-midi`]: https://github.com/SuperInstance/flux-tensor-midi
[`constraint-theory-llvm`]: https://github.com/SuperInstance/constraint-theory-llvm
[`constraint-theory-rust-python`]: https://github.com/SuperInstance/constraint-theory-rust-python
[`constraint-audio`]: https://github.com/SuperInstance/constraint-audio
[`constraint-mux`]: https://github.com/SuperInstance/constraint-mux
[`guardc-v3`]: https://github.com/SuperInstance/guardc-v3
[`holonomy-consensus`]: https://github.com/SuperInstance/holonomy-consensus
[`fleet-resonance`]: https://github.com/SuperInstance/fleet-resonance
[`memory-crystal`]: https://github.com/SuperInstance/memory-crystal
[`penrose-memory`]: https://github.com/SuperInstance/penrose-memory
[`deadband-rs`]: https://github.com/SuperInstance/deadband-rs
[`eisenstein`]: https://github.com/SuperInstance/eisenstein
[`warp-flux-poc`]: https://github.com/SuperInstance/warp-flux-poc
[`conservation-spectral-c`]: https://github.com/SuperInstance/conservation-spectral-c
[`sheaf-agents-c`]: https://github.com/SuperInstance/sheaf-agents-c
[`hodge-belief-c`]: https://github.com/SuperInstance/hodge-belief-c
[`renormalization-learning-c`]: https://github.com/SuperInstance/renormalization-learning-c
[`west-african-math-c`]: https://github.com/SuperInstance/west-african-math-c
[`conservation-sheaf-flow-c`]: https://github.com/SuperInstance/conservation-sheaf-flow-c
[`ergodic-transport-c`]: https://github.com/SuperInstance/ergodic-transport-c
[`free-probability-c`]: https://github.com/SuperInstance/free-probability-c
[`conservation-guardian-c`]: https://github.com/SuperInstance/conservation-guardian-c
[`wasserstein-ot-c`]: https://github.com/SuperInstance/wasserstein-ot-c
[`tda-c`]: https://github.com/SuperInstance/tda-c
[`crackle-runtime-c`]: https://github.com/SuperInstance/crackle-runtime-c
[`cache-guardian-c`]: https://github.com/SuperInstance/cache-guardian-c
[`categorical-agents-c`]: https://github.com/SuperInstance/categorical-agents-c
[`eisenstein-vs-z2-c`]: https://github.com/SuperInstance/eisenstein-vs-z2-c
[`ab-testing-c`]: https://github.com/SuperInstance/ab-testing-c
[`counterpoint-engine-c`]: https://github.com/SuperInstance/counterpoint-engine-c
[`flux-algebra-c`]: https://github.com/SuperInstance/flux-algebra-c
[`agent-rhythm-c`]: https://github.com/SuperInstance/agent-rhythm-c
[`conservation-spectral-python`]: https://github.com/SuperInstance/conservation-spectral-python
[`conservation-spectral-js`]: https://github.com/SuperInstance/conservation-spectral-js
[`conservation-spectral-cuda`]: https://github.com/SuperInstance/conservation-spectral-cuda
[`conservation-spectral-vulkan`]: https://github.com/SuperInstance/conservation-spectral-vulkan
[`conservation-spectral-opencl`]: https://github.com/SuperInstance/conservation-spectral-opencl
[`conservation-spectral-webgpu`]: https://github.com/SuperInstance/conservation-spectral-webgpu
[`conservation-spectral-fortran`]: https://github.com/SuperInstance/conservation-spectral-port
[`conservation-spectral-fortraniv`]: https://github.com/SuperInstance/conservation-spectral-port
[`conservation-spectral-zig`]: https://github.com/SuperInstance/conservation-spectral-zig
[`conservation-spectral-mojo`]: https://github.com/SuperInstance/conservation-spectral-mojo
[`conservation-spectral-lisp`]: https://github.com/SuperInstance/conservation-spectral-lisp
[`conservation-spectral-pascal`]: https://github.com/SuperInstance/conservation-spectral-port
[`conservation-spectral-ada`]: https://github.com/SuperInstance/conservation-spectral-ada
[`conservation-spectral-asm`]: https://github.com/SuperInstance/conservation-spectral-asm
[`conservation-spectral-ptx`]: https://github.com/SuperInstance/conservation-spectral-ptx
[`conservation-spectral-chapel`]: https://github.com/SuperInstance/conservation-spectral-chapel
[`conservation-spectral-forth`]: https://github.com/SuperInstance/conservation-spectral-forth
[`conservation-spectral-apl`]: https://github.com/SuperInstance/conservation-spectral-port
[`terminal-spectral-harness`]: https://github.com/SuperInstance/terminal-spectral-harness
[`terminal-entropy-harness`]: https://github.com/SuperInstance/terminal-entropy-harness
[`intelligent-terminal`]: https://github.com/SuperInstance/intelligent-terminal