# Plato DCS Engine — Design Document

**Version:** 0.1 (Sprint 1 Planning Document)
**Author:** Forgemaster (FM) with Oracle1 cross-reference
**Date:** 2026-06-04
**Status:** Design — pre-implementation
**Target Crate:** `plato-dcs-engine` (Rust, new crate under PLATO ecosystem)

---

## 1. Overview

`plato-dcs-engine` is a Rust execution engine that implements the **21.87× DCS (Divide-Conquer-Synthesize) protocol** as a practical runtime layer over `plato-unified-belief`. It answers the question: *given a fleet of agents with heterogeneous trust levels and a stream of observations (tiles), how do you decide what to deploy, to whom, and with what safeguards?*

The engine is the bridge between three previously disconnected layers:

| Layer | Theory | Implementation |
|-------|--------|----------------|
| **Lock Algebra** | Oracle1 — formal constraint composition | `plato-constraints` crate |
| **Unified Belief** | Oracle1 — belief accumulation over DCS rounds | `plato-unified-belief` crate |
| **Tiered Trust** | Oracle1 — Live/Monitored/HumanGated policy | `DeploymentPolicy` enum (new) |
| **DCS Protocol** | 21.87× generalist advantage (proven in simulation) | `plato-dcs-engine` (this crate) |

The engine wraps `plato-unified-belief` and feeds it through a **dynamic lock gate** (replacing the old static `plato-lab-guard`) that enforces deployment policy at runtime, using Lock Algebra proofs as constraint filters.

---

## 2. Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    plato-dcs-engine                       │
│                                                          │
│  ┌─────────────┐   ┌───────────────┐   ┌────────────┐  │
│  │ DcsProtocol  │──▶│ BeliefIntegra-│──▶│ PolicyGate │  │
│  │ (round mgmt) │   │ tor (wraps    │   │ (enforces  │  │
│  │              │   │ plato-unified-│   │ Deployment │  │
│  │              │   │ belief)       │   │ Policy)    │  │
│  └──────┬───────┘   └───────┬───────┘   └─────┬──────┘  │
│         │                   │                  │         │
│         ▼                   ▼                  ▼         │
│  ┌─────────────┐   ┌───────────────┐   ┌────────────┐  │
│  │ LockAlgebra  │   │ TieredTrust   │   │ DynamicLock│  │
│  │ Pipeline     │   │ (policy fetch │   │ Gate (diff │  │
│  │ (constraint  │   │  + delegation)│   │ + lock     │  │
│  │  filters)    │   │               │   │  accum)    │  │
│  └─────────────┘   └───────────────┘   └────────────┘  │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │              Intelligent Terminal Bridge         │    │
│  │          (harness module — injects engine        │    │
│  │           decisions into terminal UX)            │    │
│  └─────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘

           │                         │
           ▼                         ▼
    ┌──────────────┐       ┌──────────────────┐
    │ plato-unified │       │  plato-constraints│
    │ -belief       │       │  (Lock Algebra)   │
    └──────────────┘       └──────────────────┘
```

### 2.1 Module Boundaries

#### `plato-dcs-engine` (this crate)
- **DcsProtocol**: round-based DCS lifecycle (Divide → Conquer → Synthesize → Assess)
- **BeliefIntegrator**: wraps `plato-unified-belief`, converting DCS round outputs into belief updates
- **PolicyGate**: evaluates `DeploymentPolicy` at every decision point
- **LockAlgebraPipeline**: applies Lock Algebra constraint proofs as filters during Divide and Synthesize phases
- **TieredTrust**: resolves an agent's trust tier from its trust score and provenance
- **DynamicLockGate**: replaces static `plato-lab-guard` — accumulates locks at runtime from self-supervision compiler output
- **IntelligentTerminalBridge**: harness module that surfaces engine state to the terminal UI

#### `plato-unified-belief` (external dependency)
- `BeliefState` — unified belief accumulation across DCS rounds
- `BeliefDelta` — incremental belief update
- `BeliefMerger` — merge conflicting beliefs from multiple specialists

#### `plato-constraints` (external dependency)
- `LockAlgebra` trait — `impl LockAlgebra for PlatoConstraint`
- `PlatoConstraint` — the canonical constraint type for the engine
- `LockSet` — composed constraints with sequential ⊕ / parallel ⊗ / conditional ⊕_c operators

---

## 3. The 21.87× DCS Protocol

### 3.1 Origin

The DCS protocol was discovered through GPU-simulated experiments with up to 1,024 virtual agents. The core finding: a **Divide-Conquer-Synthesize** architecture with specialist agents (each +5.88× on their domain) and a generalist synthesizer (+21.87× over solving alone) produces results far beyond the sum of its parts. The multiplier comes from *structured entropy reduction* — each phase constrains the solution space, and the compounding effect yields 21.87×.

### 3.2 Engine Implementation

The protocol is expressed as a round-based state machine:

```rust
pub enum DcsPhase {
    /// Divide: decompose problem P into subproblems {p_i}
    /// Each subproblem gets a LockAlgebra constraint filter
    Divide,
    /// Conquer: dispatch subproblems to specialist agents
    /// Each specialist runs within its own constraint perimeter
    Conquer,
    /// Synthesize: merge specialist outputs through belief integrator
    Synthesize,
    /// Assess: evaluate synthesis quality, update beliefs, compute drift
    Assess,
}

pub struct DcsRound {
    pub id: u64,
    pub phase: DcsPhase,
    pub problem: ProblemSpec,
    pub subproblems: Vec<Subproblem>,
    pub specialist_outputs: Vec<Tile>,
    pub synthesis: SynthesisResult,
    pub belief_delta: Option<BeliefDelta>,
    pub round_summary: RoundSummary,
}
```

### 3.3 Why 21.87×?

The multiplier is not arbitrary; it emerges from the covering-code bound on constraint-space reduction:

```
H(P)  = entropy of the full problem space
H(L* ∘ P) = entropy after applying composed lock set L*

Compression ratio:  H(L* ∘ P) / H(P)
Empirically:        1/21.87 ≈ 4.57% of original entropy remains

This is the practical bound for n ≥ 7 locks (Lock Algebra Theorem 2:
critical mass at n ≥ 7 locks covering code theory).
```

The engine does **not** hard-code 21.87 — it measures the actual compression ratio each round and reports it as a diagnostic signal. 21.87× is the *expected* value under a well-constitued lock set; poor lock composition yields lower ratios and triggers alerts.

---

## 4. Lock Algebra Proofs → Constraints

### 4.1 The `LockAlgebra` Trait

```rust
/// Lock Algebra formal composition for PLATO constraints.
/// Mirrors Oracle1's 4 theorems.
pub trait LockAlgebra {
    type Trigger;
    type Opcode;
    type Constraint;

    /// Sequential composition L1 ⊕ L2
    fn seq(self, other: impl LockAlgebra) -> ComposedLock<Self, Other>;

    /// Parallel composition L1 ⊗ L2 (disjoint triggers)
    fn par(self, other: impl LockAlgebra) -> ComposedLock<Self, Other>;

    /// Conditional composition L1 ⊕_p L2
    fn cond(self, predicate: Predicate, other: impl LockAlgebra) -> ConditionalLock<Self, Other>;

    /// Theorem 1: Lock Monotonicity — verify monotonic compilation
    fn check_monotonicity(&self, bytecode: &[u8]) -> bool;

    /// Theorem 2: Critical Mass — n ≥ 7 locks → code theory coverage
    fn coverage_ratio(&self) -> f64;

    /// Theorem 3: Wisdom Compression — measured vs theoretical (≥ 82%)
    fn compression_ratio(&self) -> f64;

    /// Theorem 4: Cross-Model Transfer — verify transfer rate (≥ 80%)
    fn transfer_rate(&self, model_id: &str) -> f64;
}
```

### 4.2 `impl LockAlgebra for PlatoConstraint`

The implementation wires Oracle1's 4 theorems into `plato-constraints`:

```rust
impl LockAlgebra for PlatoConstraint {
    type Trigger = ConstraintTrigger;
    type Opcode = ConstraintOp;
    type Constraint = PlatoConstraint;

    fn seq(self, other: PlatoConstraint) -> ComposedLock<Self, Other> {
        // L1 ⊕ L2: (t1 ∪ t2, o2 ∘ o1, c1 ∧ c2)
        ComposedLock {
            trigger: self.trigger.union(&other.trigger),
            opcode: other.opcode.compose(self.opcode),
            constraint: self.constraint.and(other.constraint),
        }
    }

    fn check_monotonicity(&self, bytecode: &[u8]) -> bool {
        // Theorem 1: For any lock L and bytecodes B1 ⊆ B2,
        // L(B1) ⊆ L(B2). Verify the subsequence containment.
        monotonicity_check::verify(self, bytecode)
    }

    fn coverage_ratio(&self) -> f64 {
        // Theorem 2: With n ≥ 7 locks, coverage approaches 1.0
        // Returns the measured code-theory coverage fraction.
        code_coverage::covering_code_bound(self.lock_count())
    }

    fn compression_ratio(&self) -> f64 {
        // Theorem 3: Expected ≥ 0.82 (82% compression)
        information_ratio::compression_factor(self)
    }

    fn transfer_rate(&self, model_id: &str) -> f64 {
        // Theorem 4: Expected ≥ 0.80 (80% cross-model transfer)
        cross_model::transfer_coefficient(self, model_id)
    }
}
```

### 4.3 Wiring into Engine Phases

Each DCS phase uses Lock Algebra differently:

| Phase | Lock Usage | Theorem Applied |
|-------|-----------|-----------------|
| **Divide** | Apply decomposition locks to partition problem into leverage-optimal subproblems | Theorem 2 (Critical Mass) — ensure n ≥ 7 subproblem constraints |
| **Conquer** | Apply per-specialist locks to constrain agent output space | Theorem 1 (Monotonicity) — verify outputs don't regress |
| **Synthesize** | Apply synthesis lock L_s to merge specialist outputs | Theorem 3 (Compression) — verify ≥ 82% wisdom retained |
| **Assess** | Check cross-model consistency of merged belief | Theorem 4 (Transfer) — verify ≥ 80% consistent across models |

---

## 5. DeploymentPolicy Enum

New enum in `plato-unified-belief` crate, used by the engine's `PolicyGate`:

```rust
/// Deployment policy for a DCS round's output.
/// Mirrors Oracle1's three-tier trust model.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum DeploymentPolicy {
    /// Tier 1: Live Experimentation
    /// Auto-deploy. No human oversight. Feedback loop is direct.
    /// Domain: NPCs, games, creative tools, UX experiments.
    Live {
        rollback_strategy: RollbackStrategy,  // Instant / Staged
        ab_test_cutoff: f64,                  // e.g. 0.85 confidence to promote
    },

    /// Tier 2: Monitored Deployment
    /// Shadow-mode first, then graduated rollout.
    /// Domain: stock trading, fleet coordination, logistics.
    Monitored {
        shadow_trials: usize,                 // backtest / shadow runs
        rollout_steps: Vec<f64>,             // e.g. [0.05, 0.20, 0.50, 1.0]
        monitor_threshold: f64,              // automatic rollback below this
    },

    /// Tier 3: Human-Gated
    /// Simulation first, human explicitly approves.
    /// Domain: autopilot, medical, safety-critical.
    HumanGated {
        simulation_required: bool,            // must run digital twin first
        approval_timeout_secs: u64,           // human must respond within
        override_available: bool,             // can captain override mid-execution
    },
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum RollbackStrategy {
    /// Atomically swap back to previous bytecode
    Instant,
    /// Stage rollback across nodes over a window
    Staged { window_secs: u64, batch_size: usize },
}
```

### 5.1 TieredTrust Resolution

The engine resolves which `DeploymentPolicy` applies to a given agent based on:

```rust
pub fn resolve_policy(
    trust_score: f64,
    provenance_chain: &ProvenanceChain,
    domain: DomainCategory,
) -> DeploymentPolicy {
    match domain {
        DomainCategory::Creative | DomainCategory::GameNpc | DomainCategory::UxExperiment => {
            DeploymentPolicy::Live {
                rollback_strategy: RollbackStrategy::Instant,
                ab_test_cutoff: 0.85,
            }
        }
        DomainCategory::FleetCoord | DomainCategory::Trading | DomainCategory::Logistics => {
            if trust_score > 0.7 && provenance_chain.is_intact() {
                DeploymentPolicy::Monitored {
                    shadow_trials: 100,
                    rollout_steps: vec![0.05, 0.20, 0.50, 1.0],
                    monitor_threshold: 0.90,
                }
            } else {
                DeploymentPolicy::HumanGated {
                    simulation_required: true,
                    approval_timeout_secs: 3600,
                    override_available: true,
                }
            }
        }
        DomainCategory::Autopilot | DomainCategory::Medical | DomainCategory::SafetyCritical => {
            DeploymentPolicy::HumanGated {
                simulation_required: true,
                approval_timeout_secs: 300,
                override_available: true,
            }
        }
    }
}
```

---

## 6. Dynamic Lock Gate

### 6.1 Problem with `plato-lab-guard`

The old `plato-lab-guard` was a **static** gate — a hard-coded set of constraint checks applied before any tile left a PLATO room. It had no runtime adaptation:

- No awareness of agent trust tier
- No awareness of deployment domain
- No accumulation of new locks from self-supervision
- Could not distinguish "newly discovered safe pattern" from "previously unknown risk"

### 6.2 Dynamic Lock Gate

The new gate is **dynamic** — it accumulates locks at runtime from three sources:

```rust
pub struct DynamicLockGate {
    /// Base locks: compiled from LockAlgebra critical-mass constraints
    base_locks: Vec<PlatoConstraint>,

    /// Runtime locks: accumulated from Oracle1's self-supervision compiler
    /// These are constraints discovered by the fleet during operation
    runtime_locks: Arc<RwLock<Vec<RuntimeLock>>>,

    /// Self-supervision feed: where new constraints come from
    supervision_receiver: mpsc::Receiver<RuntimeLock>,
}

impl DynamicLockGate {
    /// Evaluate a tile against the accumulated lock set
    pub fn evaluate(&self, tile: &Tile, agent_trust: f64) -> GateResult {
        let mut passed = Vec::new();
        let mut failed = Vec::new();

        // Always apply base locks
        for lock in &self.base_locks {
            if lock.evaluate(tile) {
                passed.push(lock.id());
            } else {
                failed.push(lock.id());
            }
        }

        // Apply runtime locks that are within the agent's trust horizon
        let runtime = self.runtime_locks.read().unwrap();
        for lock in runtime.iter() {
            if lock.trust_threshold <= agent_trust {
                if lock.evaluate(tile) {
                    passed.push(lock.id());
                } else {
                    failed.push(lock.id());
                }
            }
        }

        GateResult { passed, failed, agent_trust }
    }

    /// Accumulate a new constraint from the self-supervision compiler
    pub fn accumulate_lock(&self, lock: RuntimeLock) -> Result<(), LockError> {
        // Validate monotonicity before accepting
        if lock.check_monotonicity() {
            self.runtime_locks.write().unwrap().push(lock);
            Ok(())
        } else {
            Err(LockError::NonMonotonic(lock))
        }
    }
}

pub struct RuntimeLock {
    pub id: LockId,
    pub constraint: PlatoConstraint,
    pub trust_threshold: f64,   // minimum agent trust to apply this lock
    pub provenance: LockProvenance, // how was this lock discovered?
    pub discovered_at: Instant,
    pub monotonic: bool,         // validated against Theorem 1
}

pub struct GateResult {
    pub passed: Vec<LockId>,
    pub failed: Vec<LockId>,
    pub agent_trust: f64,
}

impl GateResult {
    pub fn deployment_decision(&self, policy: &DeploymentPolicy) -> DeploymentDecision {
        let pass_rate = self.passed.len() as f64
            / (self.passed.len() + self.failed.len()) as f64;

        match policy {
            DeploymentPolicy::Live { ab_test_cutoff, .. } => {
                if pass_rate >= ab_test_cutoff {
                    DeploymentDecision::Approve
                } else {
                    DeploymentDecision::RouteToPolicy(DeploymentPolicy::Monitored {
                        shadow_trials: 10,
                        rollout_steps: vec![0.05],
                        monitor_threshold: 0.85,
                    })
                }
            }
            DeploymentPolicy::Monitored { monitor_threshold, .. } => {
                if pass_rate >= monitor_threshold {
                    DeploymentDecision::Approve
                } else {
                    DeploymentDecision::Degrade
                }
            }
            DeploymentPolicy::HumanGated { .. } => {
                DeploymentDecision::RequiresHumanApproval(self)
            }
        }
    }
}

pub enum DeploymentDecision {
    Approve,
    Degrade,
    Block(String),
    RequiresHumanApproval(GateResult),
    RouteToPolicy(DeploymentPolicy),
}
```

### 6.3 Self-Supervision Feed

Oracle1's self-supervision compiler runs as a background process that:

1. Monitors tile streams for patterns (tile A → tile B → good outcome)
2. Extracts the implied constraint: "if tile A appears, tile B must follow"
3. Formulates it as a `RuntimeLock`
4. Validates monotonicity (Theorem 1) before enqueueing
5. The engine's `DynamicLockGate` picks it up on the next `evaluate()` call

This is how the fleet *learns new safety rules without human intervention* — agents discover constraints through operation, and the gate accumulates them automatically.

---

## 7. Intelligent Terminal Bridge

### 7.1 Purpose

The Intelligent Terminal is a harness module — a terminal UI that surfaces the engine's internal state, allowing a human (captain or developer) to monitor, intervene, and review decisions.

### 7.2 Bridge API

```rust
/// Bridge between DCS Engine and Intelligent Terminal UI.
/// The terminal subscribes to engine events and renders them.
pub struct IntelligentTerminalBridge {
    engine_snapshot_rx: broadcast::Receiver<EngineSnapshot>,
    command_tx: mpsc::Sender<TerminalCommand>,
}

/// Engine state snapshot sent to the terminal each tick
pub struct EngineSnapshot {
    pub current_round: DcsRound,
    pub policy_state: PolicyState,
    pub gate_state: GateState,
    pub belief_summary: BeliefSummary,
    pub active_agents: Vec<AgentStatus>,
    pub recent_decisions: Vec<DeploymentDecision>,
    pub compression_ratio: f64,
    pub drift_readings: Vec<DriftSample>,
}

/// Commands the terminal can send back to the engine
pub enum TerminalCommand {
    OverridePolicy(DeploymentPolicy),
    ApproveRound(u64, ApprovalNotes),
    RejectRound(u64, RejectionReason),
    ForceRollback(u64, RollbackTarget),
    AdjustTrust(String, f64),  // agent_id, new trust score
    AddRuntimeLock(RuntimeLock),
    Snapshot,                  // request a full state snapshot
}
```

### 7.3 Terminal Views

The Intelligent Terminal exposes at minimum:

| View | Description |
|------|-------------|
| **Round Monitor** | Live DCS round state: phase, subproblem counts, synthesis progress |
| **Policy Dashboard** | Current `DeploymentPolicy` for each active agent, color-coded by tier |
| **Gate Watch** | Lock evaluation results: pass/fail counts, runtime lock accumulation |
| **Belief Canvas** | Visual representation of `plato-unified-belief` state (tile gradient) |
| **Decision Log** | Chronological log of deployment decisions with human approval prompts |
| **Drift Graph** | Real-time compression ratio and belief drift across rounds |

---

## 8. Data Flow (End-to-End Example)

```
1. Problem arrives at engine
   │
   ▼
2. DcsProtocol::Divide
   │  - Apply decomposition locks (Theorem 2: ≥ 7 constraints)
   │  - LockAlgebraPipeline filters subproblem space
   │  - Produces n subproblems with per-specialist constraints
   ▼
3. DcsProtocol::Conquer
   │  - Dispatch to specialist agents
   │  - Each agent evaluated against DynamicLockGate
   │  - LockAlgebraPipeline applies Theorem 1 (monotonicity)
   │  - PolicyGate checks agent's DeploymentPolicy
   │  - Specialists produce constrained output tiles
   ▼
4. DcsProtocol::Synthesize
   │  - BeliefIntegrator merges tiles into plato-unified-belief
   │  - LockAlgebraPipeline applies synthesis lock (Theorem 3: ≥ 82% compression)
   │  - DynamicLockGate evaluates merged belief
   │  - PolicyGate makes deployment decision
   ▼
5. DcsProtocol::Assess
   │  - Compute cross-model transfer (Theorem 4: ≥ 80%)
   │  - Measure compression ratio, drift
   │  - Update agent trust scores
   │  - Self-supervision compiler feeds new RuntimeLocks
   ▼
6. DeploymentDecision emitted
   │  - Approve: output deployed per policy
   │  - RouteToPolicy: downgrade to stricter policy
   │  - RequiresHumanApproval: terminal bridge alert
   │  - Block: output quarantined
   ▼
7. Intelligent Terminal updates
   │  - Snapshot sent to terminal
   │  - Human can override, approve, or rollback
```

---

## 9. Crate Structure

```
plato-dcs-engine/
├── Cargo.toml
├── src/
│   ├── lib.rs                  # Public API, re-exports
│   ├── protocol/
│   │   ├── mod.rs
│   │   ├── dcs.rs              # DcsProtocol, DcsRound, DcsPhase
│   │   ├── divide.rs           # Problem decomposition
│   │   ├── conquer.rs          # Specialist dispatch + constraint perimeters
│   │   ├── synthesize.rs       # Belief integration + synthesis lock
│   │   └── assess.rs           # Round assessment, drift measurement
│   ├── belief/
│   │   ├── mod.rs
│   │   └── integrator.rs       # BeliefIntegrator — wraps plato-unified-belief
│   ├── policy/
│   │   ├── mod.rs
│   │   ├── gate.rs             # PolicyGate — evaluates DeploymentPolicy
│   │   └── tiers.rs            # TieredTrust resolver
│   ├── lock_algebra/
│   │   ├── mod.rs
│   │   ├── pipeline.rs         # LockAlgebraPipeline — applies Lock Algebra filters
│   │   ├── monotonicity.rs     # Theorem 1 verification
│   │   ├── coverage.rs         # Theorem 2 critical-mass bound
│   │   ├── compression.rs      # Theorem 3 wisdom compression measurement
│   │   └── transfer.rs         # Theorem 4 cross-model transfer check
│   ├── gate/
│   │   ├── mod.rs
│   │   ├── dynamic.rs          # DynamicLockGate — runtime lock accumulation
│   │   ├── supervision.rs      # Self-supervision compiler feed
│   │   └── evaluator.rs        # Gate evaluation logic
│   ├── terminal/
│   │   ├── mod.rs
│   │   ├── bridge.rs           # IntelligentTerminalBridge
│   │   └── types.rs            # Snapshot types, TerminalCommand enum
│   └── types.rs                # Common types (DeploymentDecision, GateResult, etc.)
└── tests/
    ├── mod.rs
    ├── scenario_*.rs           # 20 test scenarios (see §10)
    └── helpers.rs              # Shared test fixtures
```

### Cargo.toml Dependencies

```toml
[package]
name = "plato-dcs-engine"
version = "0.1.0"
edition = "2021"

[dependencies]
plato-unified-belief = { path = "../plato-unified-belief" }
plato-constraints = { path = "../plato-constraints" }
plato-types = { path = "../plato-types" }
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
thiserror = "1"
tracing = "0.1"

[dev-dependencies]
rand = "0.8"
tempfile = "3"
criterion = "0.5"
```

---

## 10. Test Scenarios (20 Minimum)

Each scenario is a `#[test]` function that exercises a specific engine behavior. Tests are grouped by capability area.

### 10.1 Core DCS Protocol (6 tests)

| # | Test | What It Proves |
|---|------|----------------|
| T1 | `dcs_full_round_live_policy` | Full DCS round with `DeploymentPolicy::Live` — Divide→Conquer→Synthesize→Assess, output approved at >0.85 pass rate |
| T2 | `dcs_full_round_monitored_policy` | Full DCS round with `DeploymentPolicy::Monitored` — shadow mode, graduated rollout step-adherence |
| T3 | `dcs_full_round_human_gated_policy` | Full round produces `RequiresHumanApproval` decision, blocks until human responds |
| T4 | `dcs_divide_rejects_underconstrained` | Divide phase rejects problem when Theorem 2 (n < 7 locks) is violated |
| T5 | `dcs_synthesize_merges_conflicting_beliefs` | Two specialists produce contradictory tiles; belief integrator resolves via holonomy check |
| T6 | `dcs_assess_detects_drift` | Round completes but Assess phase detects compression ratio < 0.82, triggers alert |

### 10.2 Lock Algebra Integration (4 tests)

| # | Test | What It Proves |
|---|------|----------------|
| T7 | `lock_algebra_seq_composition` | Sequential ⊕ produces correct trigger union, opcode composition, ANDed constraint |
| T8 | `lock_algebra_par_composition` | Parallel ⊗ merges disjoint triggers, applies opcodes to non-overlapping regions |
| T9 | `lock_algebra_cond_composition` | Conditional ⊕_p selects correct branch based on predicate evaluation |
| T10 | `lock_algebra_monotonicity_rejects_violation` | `check_monotonicity()` returns false for a deliberately non-monotonic constraint set |

### 10.3 DeploymentPolicy (3 tests)

| # | Test | What It Proves |
|---|------|----------------|
| T11 | `resolve_policy_high_trust_monitored` | Agent with trust > 0.7 and intact provenance gets `Monitored` for logistics domain |
| T12 | `resolve_policy_low_trust_human_gated` | Agent with trust < 0.5 gets `HumanGated` even for non-critical domain |
| T13 | `resolve_policy_safety_critical_always_gated` | Autopilot domain always returns `HumanGated` regardless of trust |

### 10.4 Dynamic Lock Gate (3 tests)

| # | Test | What It Proves |
|---|------|----------------|
| T14 | `dynamic_gate_base_locks_always_apply` | Base locks fire regardless of agent trust tier |
| T15 | `dynamic_gate_runtime_lock_accumulation` | New runtime lock enqueued via `accumulate_lock()` is applied on next evaluate() |
| T16 | `dynamic_gate_trust_gated_runtime_locks` | Runtime lock with trust_threshold = 0.9 skips evaluation for agent with trust = 0.3 |

### 10.5 Policy Escalation / Degradation (2 tests)

| # | Test | What It Proves |
|---|------|----------------|
| T17 | `policy_escalation_live_to_monitored` | Live policy route-to-monitored when pass rate < 0.85 cutoff |
| T18 | `policy_degradation_monitored_to_human_gated` | Monitored policy degrades to HumanGated when shadow trials fail monitor_threshold |

### 10.6 Intelligent Terminal Bridge (2 tests)

| # | Test | What It Proves |
|---|------|----------------|
| T19 | `terminal_bridge_snapshots` | Bridge produces valid `EngineSnapshot` after each DCS round |
| T20 | `terminal_bridge_approve_command` | `TerminalCommand::ApproveRound` is accepted by engine and changes deployment state |

---

## 11. Implementation Order (Sprint 1 Phasing)

Based on the Sprint plan's P1 priority:

| Phase | Files | Depends On |
|-------|-------|------------|
| **Phase 1** — Types + Core | `types.rs`, `protocol/dcs.rs`, `Cargo.toml` | Sprint 1.4 (DeploymentPolicy enum) |
| **Phase 2** — Lock Algebra | `lock_algebra/*` + `impl LockAlgebra for PlatoConstraint` in `plato-constraints` | Sprint 1.3 |
| **Phase 3** — Policy + Gate | `policy/*`, `gate/*` | Phase 1 + 2 |
| **Phase 4** — Belief Wire | `belief/*` | `plato-unified-belief` crate |
| **Phase 5** — Terminal Bridge | `terminal/*` | Phase 3 |
| **Phase 6** — Tests | `tests/*` (all 20) | All phases |

---

## 12. Exit Criteria

From the Sprint 1 plan:

> **Sprint 1 exit criteria:** `plato-dcs-engine` passes 20 tests, Tile type is singular, FLUX-LCAR responds on :7777, Forge→Train pipeline produces one LoRA adapter from live tiles.

Specific to this crate:

| Criterion | How to Verify |
|-----------|---------------|
| 20 tests pass | `cargo test -- --test-threads=1` — all green |
| Full DCS round completes | Round state machine reaches Assess phase without error |
| Lock Algebra proofs wire in | `impl LockAlgebra for PlatoConstraint` compiles, 4 theorems accessible |
| DeploymentPolicy enforces at runtime | PolicyGate returns correct decision for each tier |
| Dynamic lock gate replaces static guard | `DynamicLockGate` accepts runtime locks, applies trust thresholds |
| Intelligent Terminal bridge functions | Bridge produces snapshots; terminal commands change engine state |
| Belief integration works | `BeliefIntegrator` merges ≥2 specialist tiles into unified belief |
