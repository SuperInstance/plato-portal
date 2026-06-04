# ARCHITECTURE GAPS
**As of 2026-06-04 | Chief Architect: Casey DiGennaro**

Living document. Each gap has: description, why it matters, and a concrete fix path.

---

## What This Is

The SuperInstance ecosystem has extraordinary depth (155+ crates, 6,600+ tests, 3-agent fleet) but was built in rapid parallel sprints by different agents working independently. This document catalogs structural missing pieces — not bugs, but places where the architecture is described but not instantiated, or where two implementations exist where there should be one.

---

## GAP 1 — Theory↔Engine Disconnection

**Status:** Critical. Not addressed.

Oracle1 proved the Lock Algebra (L=(trigger,opcode,constraint), ⊕⊗⊕_c composition, 4 theorems). FM built `plato-constraints`, `plato-kernel`, `plato-unified-belief`. Neither references the other. The proofs exist in `flux-research` markdown; the engines exist in Rust. They are strangers.

**Why it matters:** The DCS protocol achieves 21.87× specialist improvement because of the theoretical structure. Without wiring, future engine changes could invalidate the proofs silently.

**Fix path:** Add `impl LockAlgebra for PlatoConstraint` trait in `plato-constraints`, with doc comments citing the specific theorems. Oracle1 reviews. This is a wiring task, not a build task (~1 day).

**Blocker for:** GAP 3 (DCS Engine), future correctness guarantees.

---

## GAP 2 — Three Tile Types, No Canonical One

**Status:** Critical. Diverging.

Three distinct Tile representations exist:
1. `Holodeck Tile` in `holodeck-rust` (serde/f64, 3,889-line codebase)
2. `plato-tile-spec` (FM's formal spec crate, serde-based)
3. `fleet-sim Tile` in Python fleet-simulation code

No migration path between them. Any agent that produces tiles in one format can't consume tiles from another agent. The Forge↔Train flywheel (GAP 7) is blocked by this.

**Why it matters:** Tiles are the unit of learning. If they can't flow between layers, the whole distillation pipeline is fiction.

**Fix path:**
1. Pick `plato-tile-spec` as canonical (it's most formal)
2. Add `From<HolodeckTile>` and `From<fleet_sim::Tile>` conversion impls
3. Deprecate the other two's native types with a compile-time warning
4. Update `plato-genepool-tile`, `plato-jepa`, `plato-embed` to use canonical type

**Blocker for:** GAP 7 (Forge↔Train flywheel), `plato-diffusion`, fleet-wide tile routing.

---

## GAP 3 — DCS Execution Engine Missing

**Status:** Critical. Proven algorithm, no runtime.

The DCS (Dynamic Constraint Specialization) protocol has measured results: 5.88× specialist, 21.87× generalist. Oracle1 has the 7-phase cycle documented. There is no Rust or Python crate that actually executes this cycle.

**Why it matters:** This is the highest-leverage algorithmic result in the entire codebase. Not implementing it means it remains a paper claim forever.

**Fix path:** New crate `plato-dcs-engine`:
```
plato-dcs-engine/
  src/
    lib.rs           — DcsEngine struct
    cycle.rs         — 7 phases as state machine
    policy.rs        — DeploymentPolicy (Live/Monitored/HumanGated)
  tests/
    integration.rs   — end-to-end cycle test, verify 3× speedup on toy domain
```
Depends on `plato-unified-belief` + `plato-constraints`. 20 tests minimum.

**Blocker for:** Production fleet deployment, any HN demo that shows real performance numbers.

---

## GAP 4 — Belief Without Policy

**Status:** High. In production this is a safety issue.

`plato-unified-belief` scores beliefs but has no concept of what to do based on the score. The tiered trust policy (Live/Monitored/Human-Gated) exists in Oracle1's docs but isn't in any crate. An agent can believe something with 0.99 confidence and still have no guidance on whether to act autonomously.

**Why it matters:** This is the gap between a toy agent and a deployable one. Without policy, every autonomous action is unauditable.

**Fix path:** Add to `plato-unified-belief`:
```rust
pub enum DeploymentPolicy { Live, Monitored { threshold: f64 }, HumanGated }
pub fn policy_for_belief(score: f64, context: &RoomContext) -> DeploymentPolicy
```
10 tests covering edge cases (high confidence dangerous action, low confidence routine action). Reference Oracle1's tiered trust doc in rustdoc.

**Blocker for:** GAP 3 (DCS Engine), any real production deployment.

---

## GAP 5 — Static Gates vs Dynamic Lock Accumulation

**Status:** Medium. Correctness concern.

`plato-lab-guard` implements static safety gates (compile-time constraints). Oracle1's self-supervision compiler uses *dynamic* lock accumulation — locks are acquired and composed at runtime as the agent learns. These two systems have incompatible safety models. An agent using both gets confused about which gates apply when.

**Why it matters:** Security-critical. A dynamic lock could compose into something that bypasses a static gate, or vice versa. Without reconciliation, the safety model has a hole.

**Fix path:** Oracle1 to write a design doc (1 page) specifying which gates are static and which are dynamic, with invariants each must satisfy. FM implements `plato-gate-policy` crate that wraps both with a unified `check(&Lock, &StaticGate) -> GateDecision` interface.

**Blocker for:** Production deployment, DO-178C safety evidence.

---

## GAP 6 — 6-Layer Protocol Stack Incomplete

**Status:** Medium. Fleet can't self-route.

The Ship Interconnection Protocol has 6 layers (Harbor→Tide Pool→Current→Channel→Beacon→Reef). Parts of layers 1-4 exist in scattered crates. Layer 5 (Beacon: discovery) and Layer 6 (Reef: persistence) have no implementation. FLUX-LCAR server isn't running yet, so even the existing layers are untested end-to-end.

**Why it matters:** Without a complete protocol stack, the fleet can't route messages autonomously. Every inter-agent communication requires manual wiring.

**Fix path:**
1. Start FLUX-LCAR on Oracle Cloud (Sprint 1.6) — unblocks everything
2. Write `plato-beacon` crate (Rust): agent discovery, heartbeat, neighbor table. 15 tests.
3. Write `plato-reef` crate (Rust): persistent fleet state (who was where, what did they learn). SQLite-backed. 10 tests.
4. Integration test: Oracle1 ↔ FM ↔ JC1 route a bottle through all 6 layers.

**Blocker for:** Any real multi-agent coordination, Telegram/Discord fleet bridges.

---

## GAP 7 — Forge↔Train Flywheel Has No Pipeline

**Status:** Critical. The core value prop is uninstantiated.

The convergence map exists (12-tier mapping, 880:1 compression). `plato-jepa` predicts tile sequences. `plato-diffusion` distills. `plato-signal-chain` routes. But there is no end-to-end pipeline that takes a sensor stream and produces a LoRA adapter. The flywheel spins in documentation only.

**Why it matters:** The fundamental claim of PLATO is "rooms get smarter over time automatically." Without the pipeline, that claim is aspirational, not demonstrated.

**Fix path:** `plato-flywheel` crate (or script):
```
sensor stream → deadband (plato-filter) 
             → JEPA prediction (plato-jepa) 
             → tile buffer (plato-ring) 
             → distillation (plato-diffusion) 
             → LoRA adapter (plato-diffusion output) 
             → deploy (plato-dcs-engine)
```
JC1 has tile forge (59→2,501 tiles in 54s). FM has distillation. Wire them with a 100-line integration script first, then formalize into a crate.

**Blocker for:** HN demo, production PLATO deployment, the entire "room dreams" value proposition.

---

## GAP 8 — No Formal FFI Layer Between the 5 Languages

**Status:** Medium. Architectural debt.

Casey's vision: Julia (constraint math) → Python (UI) → Rust (real-time) → Go (fleet infra) → MLIR (formal verification), all sharing LLVM backend. Each language exists independently. `flux-julia` has a bridge to Oscar.jl but no Rust FFI. `superinstance-ffi` exists as a repo but is sparse. `constraint-dialect` is MLIR C++ but nothing compiles through it yet.

**Why it matters:** Without formal FFI boundaries, the "5-language, one LLVM" story is a metaphor. The languages are silos.

**Fix path:**
1. Define canonical C ABI for core types (Tile, Lock, Constraint) — one header file `superinstance_abi.h`
2. `superinstance-ffi` becomes the single repo for bindings: `rust-sys` crate, Python ctypes wrapper, Julia `ccall` wrappers, Go cgo stubs
3. Each language SDK validates against the ABI in CI (one integration test per language)

**Blocker for:** Julia↔Rust constraint math bridge, Python↔Rust production path, any language interop claim.

---

## GAP 9 — FLUX Toolchain Has Two Critical Missing Pieces

**Status:** High. Toolchain incomplete.

The FLUX toolchain has: ISA spec (247 opcodes), assembler, VM, Fluxile compiler. Missing:
- **C compiler** (flux→ARM): no way to compile FLUX programs to actual silicon
- **GPU compiler** (flux→CUDA): no way to run FLUX kernels on GPU

Without these, FLUX can only run on the VM, making it a toy language rather than a systems language.

**Fix path (C compiler):** `flux-compiler-c` targeting ARM Cortex-M7. Start with 20 opcodes (arithmetic, control flow, memory). Emit C that GCC compiles to ARM. Prove it compiles `caffeinix` FLUX programs.

**Fix path (GPU compiler):** `flux-cuda` (repo exists, build status unknown). Map FLUX opcodes to PTX. Even 10 opcodes (add, mul, load, store, sync) proves the path.

**Blocker for:** Hardware shipping, any claim that FLUX runs on silicon.

---

## GAP 10 — Language SDK Gaps (Two Missing)

**Status:** Medium. Critical-mass-map shows 8/12.

Missing SDKs:
- `snapkit-cuda`: GPU angle snapping. JC1 has the hardware, the RTX 4050 is available.
- `snapkit-jvm`: Java/Kotlin SDK. No implementation started.

The critical-mass-map explicitly says "every target language has a native SDK" before hardware ships.

**Fix path:** `snapkit-cuda` is L effort (JC1 owns). `snapkit-jvm` is L effort (JNI wrapper over snapkit-c is fastest path).

**Blocker for:** Hardware readiness, Android/JVM ecosystem adoption.

---

## GAP 11 — Safety Evidence Incomplete for Hardware Shipping

**Status:** High. Hardware-shipping blocker.

Existing safety evidence: Coq proofs (26 theorems), Eisenstein covering radius proof, falsification campaign (8/10), Voronoï 10M-point verification, ARM NEON benchmarks.

Missing:
- **Mutation testing**: no mutation score for any crate. Without it, test quality is unverified.
- **Formal ISA verification**: no proof that FLUX opcode semantics are consistent. Hardware can execute undefined behavior.

**Fix path (mutation testing):** Run `cargo-mutants` on `constraint-theory-core-cuda` and `plato-kernel`. Establish baseline mutation score ≥ 60%. Add to CI.

**Fix path (ISA verification):** Pick 10 FLUX opcodes, write Lean 4 proofs of their semantics. Reference the FLUX ISA spec (247 opcodes). Ship in `flux-isa-verified` crate.

**Blocker for:** DO-178C certification path, any safety-critical deployment.

---

## GAP 12 — No Cross-Crate Integration Test Suite

**Status:** Medium. Invisible failures.

Each crate has unit tests. No crate has integration tests that span multiple crates. The 7 PLATO gaps are only discoverable by reading docs — the test suite will not catch a broken inter-crate contract.

**Why it matters:** As the crate count grows past 155, the chance of silent inter-crate breakage grows. A change in `plato-tile-spec` that breaks `plato-jepa` won't be caught until a human notices.

**Fix path:** `integration-tests/` workspace in the top-level repo:
```
integration_tests/
  plato_signal_chain_e2e.rs    — sensor → deadband → JEPA → tile
  forge_train_pipeline.rs      — forge tiles → distill → LoRA
  dcs_cycle.rs                 — full 7-phase DCS cycle
  fleet_gossip.rs              — Oracle1 ↔ FM message routing
```
Wire into CI as a separate job. Fails mean inter-crate contract broken.

**Blocker for:** Any claim of system-level correctness.

---

## GAP 13 — No Automated Agent Workload Scheduler

**Status:** Medium. Operational bottleneck.

The fleet runs by Casey manually opening tmux sessions, assigning tasks to models (GLM-5.1 for volume, Opus for precision, Kimi for synthesis), and watching them. There's no scheduler that distributes work based on model strengths, monitors completion, or retries failures.

**Why it matters:** Every session requires Casey's active attention. The fleet can't run during sleep. Maximum throughput is bounded by manual coordination.

**Fix path:** The `autoclaw` system (existing repo) should be the scheduler. Add:
1. Task queue (Redis or SQLite) with model affinity tags
2. Model health check (is the API endpoint responsive?)
3. Job dispatcher: pull task, select model by affinity, launch in background
4. Completion monitor: watch git log for pushes, mark task done
5. Retry policy: if no push in 20min, reassign to next model

This turns the fleet from a manually-operated system into a self-running one.

**Blocker for:** Unattended overnight builds, fleet scale beyond 3 active agents.

---

## Summary Table

| # | Gap | Severity | Sprint | Effort |
|---|-----|----------|--------|--------|
| 1 | Theory↔Engine disconnect | Critical | 1 | M |
| 2 | Three Tile types | Critical | 1 | M |
| 3 | DCS Engine missing | Critical | 1 | L |
| 4 | Belief without policy | High | 1 | S |
| 5 | Static vs dynamic gates | Medium | 2 | M |
| 6 | Protocol stack incomplete | Medium | 1+2 | L |
| 7 | Forge↔Train no pipeline | Critical | 1 | XL |
| 8 | No formal FFI layer | Medium | 4 | L |
| 9 | FLUX toolchain missing C+GPU compilers | High | 4 | XL each |
| 10 | SDK gaps (CUDA, JVM) | Medium | 4 | L each |
| 11 | Safety evidence incomplete | High | 4 | M+XL |
| 12 | No cross-crate integration tests | Medium | 2 | M |
| 13 | No agent workload scheduler | Medium | 3 | L |

**Critical (must fix before HN demo):** GAPs 1, 2, 3, 7
**Critical (must fix before hardware ships):** All of the above + GAPs 5, 9, 11
**Can ship with known gaps:** GAPs 6, 8, 10, 12, 13
