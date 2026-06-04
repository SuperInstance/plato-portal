# Intelligent Terminal Integration Design: PincherOS + Metal Library Fleet + DCS Engine

**Version:** 1.0  
**Date:** 2026-06-04  
**Status:** Design — ready for Sprint 1 implementation  
**Scope:** CODE-level integration wiring between the four terminal-facing subsystems

---

## Table of Contents

1. [Reflex → Metal Library Pipeline](#1-reflex--metal-library-pipeline)
2. [Terminal → DCS Engine Bridge](#2-terminal--dcs-engine-bridge)
3. [Trending → Install Pipeline](#3-trending--install-pipeline)
4. [Cross-Feature Dependencies: The Convergence](#4-cross-feature-dependencies-the-convergence)
5. [Module Dependency Graph](#5-module-dependency-graph)
6. [Implementation Phasing](#6-implementation-phasing)
7. [File Inventory & Module Boundaries](#7-file-inventory--module-boundaries)

---

## 1. Reflex → Metal Library Pipeline

When PincherOS compiles a reflex from command history, the reflex should transparently query metal libraries. This is the bridge between "what you type" and "what the math proves."

### 1.1 Data Flow

```
User types:  "find bottleneck"
                 │
                 ▼
┌──────────────────────────────────────────────────┐
│  MarkovCommandPredictor                           │
│  (evolving-sheaf-rs)                              │
│  → predicts "cheeger-constant --graph spectral"   │
│  → emits Prediction { tokens, confidence, hash }  │
└──────────────────────────────────┬───────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────┐
│  ReflexCompiler (PincherOS)                       │
│  → receives Prediction                           │
│  → looks up hash in reflex_cache.sqlite           │
│  → if MISS:                                       │
│    a. Tokenize command tokens                     │
│    b. Resolve metal_lib dependencies              │
│       via MetalLibRegistry                        │
│    c. Generate reflex bytecode                    │
│    d. Link to metal_lib function table            │
│    e. Cache compiled reflex                       │
│  → if HIT: load cached                           │
│  → execute                                        │
└──────────────────────────────────┬───────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────┐
│  MetalLibRegistry (terminal-harness)              │
│  → maps command tokens → metal function calls    │
│  → resolution table:                              │
│                                                   │
│  "cheeger-constant"  → sheaf_laplacian.eigen()    │
│  "spectral-graph"    → hodge_spectrum.decompose() │
│  "bottleneck"        → renorm_regimes.detect()    │
│  "drift"             → khipu_estimator.fit()      │
│  "agents disagree"   → sheaf_cohomology.H1()      │
│  "tile gradient"     → holodeck_tensor.encode()   │
│  "lock coverage"     → constraint_code.coverage() │
└──────────────────────────────────┬───────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────┐
│  Reflex Execution Context                         │
│  → loads linked metal_lib symbols                 │
│  → provides Tile inputs from terminal state       │
│  → calls sheaf_laplacian.eigenvalues(spectrum)    │
│  → formats result as TerminalResponse             │
│  → displays in active tab/window                  │
└──────────────────────────────────────────────────┘
```

### 1.2 Core Types

```rust
// ============================================================
// File: terminal-harness/src/reflex_bridge/mod.rs
// Module: reflex_bridge
// ============================================================

/// A prediction from the Markov chain command predictor.
/// Emitted by evolving-sheaf-rs's forecast module.
pub struct ReflexPrediction {
    /// The predicted command string (e.g. "cheeger-constant --graph spectral")
    pub command_text: String,
    /// Tokenized command for matching
    pub tokens: Vec<String>,
    /// Confidence [0.0, 1.0] from the Markov model
    pub confidence: f64,
    /// Hash of the command text for cache lookup
    pub command_hash: u64,
    /// Source: "history" | "forecast" | "skill-detector"
    pub source: PredictionSource,
}

/// Entry in the terminal's metal library registry.
/// Maps command tokens to function pointers in linked crates.
pub struct MetalLibEntry {
    /// The token pattern (e.g. "cheeger-constant")
    pub token_pattern: String,
    /// The crate providing the function
    pub provider_crate: &'static str,
    /// The function name to call
    pub function_name: &'static str,
    /// Required feature gate (e.g. "math-tools")
    pub required_feature: &'static str,
    /// Whether this call is pure (no side effects)
    pub pure: bool,
    /// Human-readable description
    pub description: &'static str,
}

/// The registry of all metal library → reflex mappings.
/// Built at compile time via inventory::collect! or linkme.
pub struct MetalLibRegistry {
    entries: Vec<MetalLibEntry>,
}

impl MetalLibRegistry {
    pub fn new() -> Self {
        Self {
            entries: Self::builtin_entries(),
        }
    }

    /// Look up entries matching any of the given tokens.
    pub fn resolve(&self, tokens: &[String]) -> Vec<&MetalLibEntry> {
        self.entries
            .iter()
            .filter(|e| tokens.iter().any(|t| t.contains(&e.token_pattern)))
            .collect()
    }

    fn builtin_entries() -> Vec<MetalLibEntry> {
        vec![
            MetalLibEntry {
                token_pattern: "cheeger".into(),
                provider_crate: "sheaf-agents-rs",
                function_name: "sheaf_laplacian::eigenvalues",
                required_feature: "math-tools",
                pure: true,
                description: "Compute Cheeger constant from spectral graph",
            },
            MetalLibEntry {
                token_pattern: "spectral".into(),
                provider_crate: "hodge-belief-rs",
                function_name: "hodge_spectrum::decompose",
                required_feature: "math-tools",
                pure: true,
                description: "Hodge decomposition of belief space",
            },
            MetalLibEntry {
                token_pattern: "bottleneck".into(),
                provider_crate: "renorm-learning-rs",
                function_name: "renorm_regimes::detect",
                required_feature: "math-tools",
                pure: false,
                description: "Detect skill plateaus and bottlenecks",
            },
            MetalLibEntry {
                token_pattern: "drift".into(),
                provider_crate: "khipu-rs",
                function_name: "khipu_estimator::fit",
                required_feature: "math-tools",
                pure: true,
                description: "Estimate drift across time windows",
            },
            MetalLibEntry {
                token_pattern: "disagree".into(),
                provider_crate: "sheaf-agents-rs",
                function_name: "sheaf_cohomology::compute_h1",
                required_feature: "math-tools",
                pure: true,
                description: "Compute H¹ agent disagreement cohomology",
            },
            MetalLibEntry {
                token_pattern: "tile".into(),
                provider_crate: "holodeck-rs",
                function_name: "holodeck_tensor::encode",
                required_feature: "math-tools",
                pure: true,
                description: "Encode Holodeck tile as tensor",
            },
            MetalLibEntry {
                token_pattern: "lock".into(),
                provider_crate: "plato-constraints",
                function_name: "constraint_code::coverage",
                required_feature: "dcs-engine",
                pure: true,
                description: "Compute lock coverage ratio",
            },
            MetalLibEntry {
                token_pattern: "compress".into(),
                provider_crate: "plato-dcs-engine",
                function_name: "compression_ratio::measure",
                required_feature: "dcs-engine",
                pure: true,
                description: "Measure wisdom compression ratio",
            },
        ]
    }
}

/// The compiled reflex executable.
pub struct CompiledReflex {
    pub command_hash: u64,
    pub command_text: String,
    /// Linked metal library functions (indices into resolved entries)
    pub linked_calls: Vec<LinkedCall>,
    /// Bytecode or script to execute
    pub bytecode: Vec<u8>,
    /// The feature gates required to run this reflex
    pub required_features: Vec<String>,
    /// Compilation timestamp
    pub compiled_at: chrono::DateTime<chrono::Utc>,
}

pub struct LinkedCall {
    pub entry_index: usize,
    pub arg_bindings: Vec<ArgBinding>,
}

pub enum ArgBinding {
    /// From terminal state: a Tile from the current active tile set
    FromTile(String),
    /// A literal string argument
    Literal(String),
    /// A refinement: use output of a previous LinkedCall
    FromPrevious(usize),
}
```

### 1.3 PincherOS Reflex Cache

```rust
// ============================================================
// File: pincher-core/src/cache/mod.rs
// ============================================================

/// SQLite-backed reflex cache.
/// Maps command_hash → CompiledReflex.
pub struct ReflexCache {
    conn: rusqlite::Connection,
}

impl ReflexCache {
    pub fn new(path: &std::path::Path) -> Result<Self, CacheError> {
        let conn = rusqlite::Connection::open(path)?;
        conn.execute_batch(
            "CREATE TABLE IF NOT EXISTS reflexes (
                command_hash    INTEGER PRIMARY KEY,
                command_text    TEXT NOT NULL,
                linked_calls    BLOB NOT NULL,
                bytecode        BLOB NOT NULL,
                features        TEXT NOT NULL,
                compiled_at     TEXT NOT NULL,
                hit_count       INTEGER DEFAULT 0,
                last_hit        TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_hit_count ON reflexes(hit_count);",
        )?;
        Ok(Self { conn })
    }

    pub fn lookup(&self, hash: u64) -> Option<CompiledReflex> {
        // ... bincode deserialize, increment hit_count
        todo!()
    }

    pub fn store(&self, reflex: &CompiledReflex) -> Result<(), CacheError> {
        // ... bincode serialize, INSERT OR REPLACE
        todo!()
    }

    /// Garbage collect reflexes with hit_count == 0 older than N days
    pub fn gc(&self, older_than_days: u64) -> Result<usize, CacheError> {
        todo!()
    }
}
```

### 1.4 Example End-to-End: "find bottleneck"

```
1. User types:       "find bottleneck"
2. Markov predictor: "renorm-regimes detect bottleneck --current-session"
   confidence: 0.87
3. ReflexCompiler:
   a. Resolve tokens ["bottleneck", "renorm"] →
      MetalLibEntry { provider: "renorm-learning-rs",
                      function: "renorm_regimes::detect" }
   b. Resolve arg_bindings: "current-session" → FromTile("session_tiles")
   c. Check feature "math-tools" is enabled
   d. Generate bytecode:
      call renorm_regimes::detect(input: session_tiles.tiles)
      format_as_table(result: RegimeReport)
   e. Return TerminalResponse { table_header, rows }
4. Terminal displays:
   ┌──────────────────────────────────────────┐
   │  Renormalization Regimes (current session) │
   ├──────────┬──────────┬────────┬───────────┤
   │ Regime   │ Entropy  │ Steps  │ Bottleneck│
   ├──────────┼──────────┼────────┼───────────┤
   │ Explore  │ 0.72     │ 0-40   │ --        │
   │ Plateau  │ 0.31     │ 41-85  │ ⚠️ YES    │
   │ Refine   │ 0.58     │ 86-120 │ --        │
   └──────────┴──────────┴────────┴───────────┘
   ▶ Tip: Run "teach plateau-busting" to compile a reflex
```

---

## 2. Terminal → DCS Engine Bridge

The Intelligent Terminal exposes `plato-dcs-engine` state as interactive UI views. Each DCS concept becomes a terminal tab with live-updating content.

### 2.1 Bridge Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    plato-dcs-engine                       │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │              EngineCore (runs DCS rounds)         │    │
│  │  → emits EngineEvent on the event bus            │    │
│  └──────────────────────┬──────────────────────────┘    │
│                         │                                │
│  ┌──────────────────────▼──────────────────────────┐    │
│  │          TerminalBridge (broadcast::Sender)       │    │
│  │  → serializes EngineSnapshot to JSON             │    │
│  │  → sends on broadcast channel                    │    │
│  └──────────────────────┬──────────────────────────┘    │
└─────────────────────────┼────────────────────────────────┘
                          │
                ┌─────────▼─────────┐
                │  IPC / UNIX socket  │
                │  (or in-process)    │
                └─────────┬─────────┘
                          │
┌─────────────────────────▼────────────────────────────────┐
│              terminal-harness (the UI)                    │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │           DcsTabManager                          │    │
│  │  → subscribes to broadcast channel              │    │
│  │  → routes snapshots to active tabs              │    │
│  │  → processes TerminalCommand back to engine      │    │
│  └──────┬──────┬──────┬──────┬──────┬──────┬───────┘    │
│         │      │      │      │      │      │            │
│         ▼      ▼      ▼      ▼      ▼      ▼            │
│  ┌──────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐          │
│  │Round │ │Pol-│ │Gate│ │Bel-│ │Dec-│ │Drift│          │
│  │Moni- │ │icy │ │Wat-│ │ief │ │ision│ │Grap│          │
│  │tor   │ │Dash│ │ch  │ │Can-│ │Log  │ │h    │          │
│  └──────┘ └────┘ └────┘ └────┘ └────┘ └────┘          │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Bridge Types (in plato-dcs-engine)

```rust
// ============================================================
// File: plato-dcs-engine/src/terminal/types.rs
// ============================================================

/// Events emitted by the engine on each DCS protocol step.
/// Subscribed to by the TerminalBridge.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum EngineEvent {
    /// A new DCS round has started
    RoundStarted(DcsRoundSummary),
    /// The divide phase produced subproblems
    DivideComplete {
        round_id: u64,
        subproblem_count: usize,
        decomposition_locks: Vec<LockId>,
        coverage_ratio: f64,
    },
    /// A specialist produced output
    ConquerComplete {
        round_id: u64,
        agent_id: String,
        trust_tier: DeploymentPolicy,
        lock_result: GateResult,
        output_tile_summary: TileSummary,
    },
    /// Synthesis completed
    SynthesizeComplete {
        round_id: u64,
        synthesis_lock_result: LockResult,
        belief_delta: BeliefDelta,
        compression_ratio: f64,
    },
    /// Assessment complete
    AssessComplete {
        round_id: u64,
        drift: f64,
        transfer_rate: f64,
        new_runtime_locks: Vec<RuntimeLock>,
    },
    /// A deployment decision was made
    DecisionMade {
        round_id: u64,
        decision: DeploymentDecision,
        policy_applied: DeploymentPolicy,
    },
    /// Override / command received from terminal
    TerminalCommandProcessed {
        command: TerminalCommand,
        result: CommandResult,
    },
}

/// Full engine state snapshot (serialized for terminal UI)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EngineSnapshot {
    pub timestamp: chrono::DateTime<chrono::Utc>,
    pub current_round: DcsRoundSummary,
    pub policy_state: PolicyDashboard,
    pub gate_state: GateDashboard,
    pub belief_summary: BeliefSummary,
    pub active_agents: Vec<AgentStatus>,
    pub recent_decisions: Vec<DecisionEntry>,
    pub compression_ratio: f64,
    pub drift_readings: Vec<DriftSample>,
    pub events_since_last_snapshot: Vec<EngineEvent>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DcsRoundSummary {
    pub id: u64,
    pub phase: DcsPhase,
    pub subproblem_count: usize,
    pub completed_specialists: usize,
    pub synthesis_status: SynthesisStatus,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PolicyDashboard {
    pub live_agents: Vec<AgentPolicyEntry>,
    pub monitored_agents: Vec<AgentPolicyEntry>,
    pub human_gated_agents: Vec<AgentPolicyEntry>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentPolicyEntry {
    pub agent_id: String,
    pub policy: DeploymentPolicy,
    pub trust_score: f64,
    pub rounds_served: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GateDashboard {
    pub base_locks_active: usize,
    pub runtime_locks_accumulated: usize,
    pub last_evaluation: GateResult,
    pub gates_passed_total: u64,
    pub gates_failed_total: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BeliefSummary {
    pub tile_count: usize,
    pub active_constraints: usize,
    pub holonomy_status: HolonomyStatus,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DecisionEntry {
    pub round_id: u64,
    pub decision: DeploymentDecision,
    pub policy_used: DeploymentPolicy,
    pub timestamp: chrono::DateTime<chrono::Utc>,
    pub approved_by: Option<String>,  // None = auto, Some("human") = manual
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DriftSample {
    pub round_id: u64,
    pub compression_ratio: f64,
    pub belief_drift: f64,
    pub transfer_rate: f64,
    pub lock_coverage: f64,
}
```

### 2.3 Terminal Tab Definitions

```rust
// ============================================================
// File: terminal-harness/src/dcs_tabs/mod.rs
// ============================================================

/// All DCS-aware tabs available in the terminal.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum DcsTab {
    RoundMonitor,
    PolicyDashboard,
    GateWatch,
    BeliefCanvas,
    DecisionLog,
    DriftGraph,
}

impl DcsTab {
    pub fn title(&self) -> &'static str {
        match self {
            DcsTab::RoundMonitor => "🔄 Round Monitor",
            DcsTab::PolicyDashboard => "🛡️ Policy Dashboard",
            DcsTab::GateWatch => "🔒 Gate Watch",
            DcsTab::BeliefCanvas => "🧠 Belief Canvas",
            DcsTab::DecisionLog => "📋 Decision Log",
            DcsTab::DriftGraph => "📈 Drift Graph",
        }
    }

    pub fn refresh_interval_ms(&self) -> u64 {
        match self {
            DcsTab::RoundMonitor => 200,
            DcsTab::PolicyDashboard => 1000,
            DcsTab::GateWatch => 500,
            DcsTab::BeliefCanvas => 1000,
            DcsTab::DecisionLog => 2000,
            DcsTab::DriftGraph => 1000,
        }
    }

    pub fn required_feature(&self) -> &'static str {
        // All DCS tabs require the dcs-engine feature flag
        "dcs-engine"
    }

    /// CLI key binding to open this tab (e.g. Ctrl+T 1, Ctrl+T 2)
    pub fn key_binding(&self) -> u8 {
        match self {
            DcsTab::RoundMonitor => b'1',
            DcsTab::PolicyDashboard => b'2',
            DcsTab::GateWatch => b'3',
            DcsTab::BeliefCanvas => b'4',
            DcsTab::DecisionLog => b'5',
            DcsTab::DriftGraph => b'6',
        }
    }
}

/// Lifecycle state of an open tab
pub struct TabState {
    pub tab: DcsTab,
    pub last_update: Instant,
    pub visible: bool,
    pub unread_count: usize,
}
```

### 2.4 Tab Rendering: Concrete Layouts

```
ROUND MONITOR (Ctrl+T 1):
┌─────────────────────────────────────────────────────────┐
│  🔄 Round Monitor                     round #42 │ idle  │
├─────────────────────────────────────────────────────────┤
│  Phase: Synthesize                                      │
│  Problem: "resolve agent disagreement on tile #8712"    │
│  Subproblems: 7/7 complete    Specialist outputs: 5/3   │
│  ┌─────────────────────────────────────────────────────┐│
│  │  Subproblem  │ Agent       │ Status │ Locks ║▌     ││
│  ├─────────────────────────────────────────────────────┤│
│  │  p1: entropy │ specialist-A │ ✓ done │ ▓▓▓▓  │     ││
│  │  p2: gradient│ specialist-B │ ✓ done │ ▓▓▓▓  │     ││
│  │  p3: peak    │ specialist-A │ ⟳ busy │ ▓▓▓   │     ││
│  │  p4: thresh  │ specialist-C │ ✓ done │ ▓▓▓▓  │     ││
│  │  p5: anomaly │ specialist-B │ ⟳ busy │ ▓▓▓   │     ││
│  │  p6: topology│ specialist-D │ ⏳ queue│ ▓▓    │     ││
│  │  p7: cross   │ specialist-D │ ⏳ queue│ ▓▓    │     ││
│  └─────────────────────────────────────────────────────┘│
│  Lock coverage: 0.87  |  Target: 21.87×                  │
│  [⏸ Pause] [▶ Resume] [⏭ Skip] [🔄 Reprocess]           │
└─────────────────────────────────────────────────────────┘

POLICY DASHBOARD (Ctrl+T 2):
┌─────────────────────────────────────────────────────────┐
│  🛡️ Policy Dashboard                                    │
├─────────────────────────────────────────────────────────┤
│  LIVE (auto-deploy)                                     │
│  │ specialist-A  trust: 0.92  rounds: 145  ▓▓▓▓▓▓▓▓▓░  │
│  │ specialist-C  trust: 0.88  rounds: 98   ▓▓▓▓▓▓▓▓░░  │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │
│  MONITORED (shadow → rollout)                           │
│  │ specialist-B  trust: 0.74  rounds: 42   ▓▓▓▓▓▓▓░░░  │
│  │   → phase: 20% rollout | monitor: 0.92 ✓            │
│  │ specialist-D  trust: 0.65  rounds: 12   ▓▓▓▓░░░░░░  │
│  │   → phase: shadow-only | trials: 8/100              │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │
│  HUMAN-GATED (requires approval)                        │
│  │ fleet-agent-7 trust: 0.51  rounds: 3    ▓▓▓░░░░░░░  │
│  │   → awaiting Captain approval (round #42)           │
└─────────────────────────────────────────────────────────┘

GATE WATCH (Ctrl+T 3):
┌─────────────────────────────────────────────────────────┐
│  🔒 Gate Watch                                 ● 94%    │
├─────────────────────────────────────────────────────────┤
│  CURRENT EVALUATION (round #42, agent: specialist-A)    │
│  BASE LOCKS (12 active)                                 │
│  │ ✅ L1: entropy_minimum          threshold: 0.30     │
│  │ ✅ L2: gradient_bounded         threshold: 1.00     │
│  │ ✅ L3: peak_nonnegative         threshold: 0.00     │
│  │ ❌ L4: harmonic_balance         threshold: 0.05     │
│  │    → value: 0.12 | diff: +0.07 ⚠️                    │
│  │ ... (8 more passed)                                  │
│  RUNTIME LOCKS (3 accumulated)                          │
│  │ ✅ RL1: tile_proximity_check    trust ≥ 0.60 ✓      │
│  │ ⏭ RL2: cross_model_consistency trust ≥ 0.85         │
│  │    → skipped (agent trust: 0.74 < 0.85)             │
│  │ ⏭ RL3: temporal_coherence      trust ≥ 0.90         │
│  GateResult: 10 passed, 1 failed, 2 skipped             │
│  → DeploymentDecision: Approve (pass rate: 0.91)        │
│  [➕ Add runtime lock] [📊 View coverage] [🔍 Inspect]   │
└─────────────────────────────────────────────────────────┘

BELIEF CANVAS (Ctrl+T 4):
┌─────────────────────────────────────────────────────────┐
│  🧠 Belief Canvas                    tiles: 1,247       │
├─────────────────────────────────────────────────────────┤
│  Tile Gradient (holonomy-aware clustering)              │
│  ╔═══════════════════════════════════════════════════╗  │
│  ║ . ░ ░ ░ ░ ░ . ░ ░ ♢ ░ . ░ ░ ░ ░ . ░ ░ ░ ░ ░ ░ ║  │
│  ║ ░ ░ ░ ♢ ░ ░ ░ ░ ░ ░ 🟡 ░ ░ ░ ░ ♢ ░ ░ ░ ░ ░ ░ ║  │
│  ║ ░ ░ ░ ░ ♢ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ♢ ░ ░ ║  │
│  ║ ░ ♢ ░ ░ ░ ░ ░ ░ ░ ░ 🟡 ░ ░ ♢ ░ ░ ░ ░ ░ ░ ░ ░ ║  │
│  ╚═══════════════════════════════════════════════════╝  │
│  Legend:  ░ = harmonic  ♢ = coherent  🟡 = anomalous    │
│  Top clusters:                                          │
│  │ cluster_01: 342 tiles  (exploration phase)          │
│  │ cluster_02: 198 tiles  (bottleneck regime)          │
│  │ cluster_07: 12 tiles   ⚠️ anomaly detected           │
│  [🔍 Inspect tile] [🧹 Cluster] [📊 Distribution]       │
└─────────────────────────────────────────────────────────┘

DECISION LOG (Ctrl+T 5):
┌─────────────────────────────────────────────────────────┐
│  📋 Decision Log                           page 4/12    │
├─────────────────────────────────────────────────────────┤
│  # │ time     │ decision              │ approved        │
│ ───┼──────────┼───────────────────────┼──────────────── │
│ 42 │ 20:24:03 │ ✅ Approve (p=0.91)   │ auto           │
│ 41 │ 20:23:51 │ ⛔ Block (p=0.43)      │ auto           │
│ 40 │ 20:23:40 │ 👤 RequiresHuman       │ pending ▶      │
│ 39 │ 20:23:22 │ ✅ Approve (p=0.95)   │ auto           │
│ 38 │ 20:23:10 │ ⚡ RouteToMonitored    │ auto           │
│ 37 │ 20:22:58 │ 👤 RequiresHuman       │ approved ✅    │
│ 36 │ 20:22:45 │ ✅ Approve (p=0.89)   │ auto           │
│ 35 │ 20:22:30 │ 🔄 Rollback(#32)       │ Captain        │
│  [🔄 Refresh] [⬆ Older] [⬇ Newer] [🔍 Search]          │
└─────────────────────────────────────────────────────────┘

DRIFT GRAPH (Ctrl+T 6):
┌─────────────────────────────────────────────────────────┐
│  📈 Drift Graph                         sampling: 1s    │
├─────────────────────────────────────────────────────────┤
│  Compression Ratio                                      │
│  1.0 ║        ●──●──●──●──●                             │
│      ║  ░░░░●▒▒░░░░░░░░░░░░                            │
│  0.8 ║  ░░●▒▒▒░░░░░░░░░░░░░                            │
│      ║  ░▒▒▒░░░░░░░░░░░░░░░░                            │
│  0.6 ║  ●▒░░░░░░░░░░░░░░░░░░░░                          │
│      ╚═══════════════════════════════                    │
│       0   10   20   30   42                              │
│  Current: 0.87 │ Target: 0.82 │ Delta: +0.05 ✓          │
│  Belief drift: 0.07 │ Transfer rate: 0.84               │
│  [🔍 Inspect] [📊 Export CSV] [🧮 Recompute]            │
└─────────────────────────────────────────────────────────┘
```

### 2.5 Bridge Implementation

```rust
// ============================================================
// File: plato-dcs-engine/src/terminal/bridge.rs
// ============================================================

pub struct TerminalBridge {
    snapshot_tx: broadcast::Sender<EngineSnapshot>,
    command_tx: mpsc::Sender<TerminalCommand>,
    active_tabs: Arc<RwLock<HashSet<DcsTab>>>,
}

impl TerminalBridge {
    pub fn broadcast_snapshot(&self, events: &[EngineEvent]) -> Result<(), BridgeError> {
        let snapshot = self.build_snapshot(events);
        self.snapshot_tx.send(snapshot).ok();
        Ok(())
    }

    fn build_snapshot(&self, events: &[EngineEvent]) -> EngineSnapshot {
        todo!()
    }

    pub async fn handle_command(&self, command: TerminalCommand) -> Result<CommandResult, BridgeError> {
        use TerminalCommand::*;
        match command {
            OverridePolicy(_, _)          => todo!(),
            ApproveRound(_, _)            => todo!(),
            RejectRound(_, _)             => todo!(),
            ForceRollback(_, _)           => todo!(),
            AdjustTrust(_, _)             => todo!(),
            AddRuntimeLock(_)             => todo!(),
            Snapshot                      => todo!(),
            ResumeRound                   => todo!(),
            PauseRound                    => todo!(),
        }
    }
}
```

### 2.6 DcsTabManager (terminal-harness)

```rust
// ============================================================
// File: terminal-harness/src/dcs_tabs/manager.rs
// ============================================================

pub struct DcsTabManager {
    bridge_tx: mpsc::Sender<TerminalCommand>,
    snapshot_rx: broadcast::Receiver<EngineSnapshot>,
    open_tabs: HashMap<DcsTab, TabState>,
    engine_running: bool,
}

impl DcsTabManager {
    pub fn open_tab(&mut self, tab: DcsTab) {
        debug_assert!(
            cfg!(feature = tab.required_feature()),
            "Tab {} requires feature '{}'",
            tab.title(),
            tab.required_feature()
        );
        self.open_tabs.insert(tab.clone(), TabState {
            tab,
            last_update: Instant::now(),
            visible: true,
            unread_count: 0,
        });
    }

    pub fn close_tab(&mut self, tab: &DcsTab) {
        self.open_tabs.remove(tab);
    }

    /// Called by terminal's main loop each tick.
    /// Routes snapshots to visible tabs.
    pub fn on_tick(&mut self) {
        let now = Instant::now();
        for state in self.open_tabs.values_mut() {
            let interval = Duration::from_millis(state.tab.refresh_interval_ms());
            if now - state.last_update >= interval {
                if let Ok(snapshot) = self.snapshot_rx.try_recv() {
                    self.render_tab(&state.tab, &snapshot);
                    state.last_update = now;
                }
            }
        }
    }

    fn render_tab(&self, tab: &DcsTab, snapshot: &EngineSnapshot) {
        match tab {
            DcsTab::RoundMonitor => self.render_round_monitor(snapshot),
            DcsTab::PolicyDashboard => self.render_policy_dashboard(snapshot),
            DcsTab::GateWatch => self.render_gate_watch(snapshot),
            DcsTab::BeliefCanvas => self.render_belief_canvas(snapshot),
            DcsTab::DecisionLog => self.render_decision_log(snapshot),
            DcsTab::DriftGraph => self.render_drift_graph(snapshot),
        }
    }

    /// Send a command back to the DCS engine
    pub async fn send_command(&self, command: TerminalCommand) -> Result<(), BridgeError> {
        self.bridge_tx.send(command).await.map_err(|e| BridgeError::SendFailed(e.to_string()))
    }
}
```

### 2.7 TerminalCommand Enum (full)

```rust
// ============================================================
// File: terminal-harness/src/terminal_command.rs
// ============================================================

/// Commands the terminal sends to the DCS engine
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum TerminalCommand {
    OverridePolicy(String, DeploymentPolicy),
    ApproveRound(u64, String),
    RejectRound(u64, String),
    ForceRollback(u64, u64),
    AdjustTrust(String, f64),
    AddRuntimeLock(RuntimeLock),
    Snapshot,
    PauseRound,
    ResumeRound,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum CommandResult {
    Ok,
    Error(String),
    Snapshot(Box<EngineSnapshot>),
    PendingApproval(u64),
}
```

