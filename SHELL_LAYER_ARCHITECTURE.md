# Shell-Layer Durability Boundary
## Intelligent Terminal Fork — Fallback Architecture

**Document:** Shell-Layer Durability Boundary  
**Project:** SuperInstance/intelligent-terminal (Windows Terminal fork, ~13,500 lines Rust)  
**Purpose:** Define the durability contract across all three layers  
**Principle:** Machine code (cold path / fixed point). Fluid code (hot path / transformation graph). Natural (outermost ring / shell interface).

> **⚠️ CORRECTION from earlier session:** The three layers are **concentric, not stacked failure-handoff**. See `THREE_LAYER_CORRECTION.md` for the corrected model. The shell is NOT the fallback — it is the natural layer interface, the outermost ring. Every boundary is a dual aspect functor running in both directions. Sections below use 

---

## 1. The Three-Layer Model

The terminal operates across three semantic layers, each with a distinct failure mode and a defined handoff to the layer below.

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 1 — MACHINE CODE (The Fixed Point)                       │
│                                                                 │
│  Compiled Rust. Feature-gated. Zero-cost when disabled.         │
│  math_analysis/ griot_history/ context_trigger/ module_system/  │
│  ui/entropy_bar  ui/agent_disagreement  forecast/ skill_detector│
│                                                                 │
│  Invariant: if cargo build passes, the type system holds.       │
│  Failure signature: process panic, OOM, SIGABRT, timeout.       │
│  Handoff trigger: module enters DEGRADED or EVICTED state.      │
└──────────────────────────────┬──────────────────────────────────┘
                               │  escalates on module failure
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 2 — FLUID CODE (The Semantic Layer)                      │
│                                                                 │
│  Context triggers. Module lifecycle FSM. Natural language intent.│
│  7 auto-activation rules. Memory budget. LRU eviction.          │
│                                                                 │
│  Characteristic: adaptive, context-sensitive, intent-driven.    │
│  Failure signature: trigger never fires, FSM deadlocks,         │
│    memory budget exhausted, Windows Terminal Agent process dies. │
│  Handoff trigger: fallback_threshold crossed (see §3).          │
└──────────────────────────────┬──────────────────────────────────┘
                               │  escalates on fluid layer failure
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 3 — SHELL FALLBACK (The Durability Boundary)             │
│                                                                 │
│  Shell scripts. Unix pipes. Env vars. History files.            │
│  Always available while the OS runs.                            │
│                                                                 │
│  Characteristic: dumb but reliable. Composable. Stateless.      │
│  Failure signature: OS-level failure (catastrophic — not our    │
│    problem to solve here).                                      │
│  Handoff trigger: escalate to natural language (§6).            │
└─────────────────────────────────────────────────────────────────┘
```

### Why Shell Is the Boundary, Not the Floor

The shell layer predates the terminal fork. It will exist after every module is disabled, after the agent process dies, after the memory budget is exhausted. It is not the floor — it is the *boundary* between what the terminal computes and what the human types. A well-designed shell fallback means no module failure is ever catastrophic: the terminal degrades gracefully to a state the user can still navigate.

The three-layer contract:

| Layer | What it knows | What it can lose | What it always keeps |
|-------|---------------|------------------|----------------------|
| Machine code | Full math runtime, type-verified state | Nothing (compiled) | The binary |
| Fluid code | Context, intent, activation state | Trigger timing, module order | The FSM state file |
| Shell | Command history, env vars, raw files | Computed state | The ability to type |

---

## 2. Fallback Chain Per Module

Each module has three defined states: **ACTIVE** (full math runtime), **DEGRADED** (partial fallback), **SHELL** (pure shell replacement). State transitions are one-directional during a session; recovery can restore ACTIVE from SHELL only on explicit user request or process restart.

---

### 2.1 Entropy Bar (`ui/entropy_bar`)

**What it does:** Always-visible gauge showing edit/test ratio as a proxy for verification entropy. Tracks the ratio of source-mutating commands to test-validating commands over a rolling window.

**Active state:**  
Real-time entropy computation over command stream. Hodge decomposition on error signals informs the gauge color (gradient = fixable, harmonic = systemic, curl = oscillating).

**Failure modes:**
- Metrics pipe from `math_analysis/` breaks (timeout > 500ms)
- UI rendering stalls in terminal VT layer
- Memory eviction removes entropy window buffer

**DEGRADED fallback (fluid layer survives):**
```
entropy_approximate = edit_commands / max(1, test_commands)
# counts cargo/git/edit vs cargo test/pytest from last 50 commands
# displayed as plain text ratio, no color coding
```

**SHELL fallback (full shell replacement):**
```bash
# Inline entropy check — run at any point to see current ratio
alias entropy='python3 -c "
import subprocess, re
hist = subprocess.check_output([\"bash\",\"-i\",\"-c\",\"history 50\"], text=True, stderr=subprocess.DEVNULL)
cmds = [l.split(None,1)[1] if len(l.split(None,1))>1 else \"\" for l in hist.splitlines()]
edits = sum(1 for c in cmds if re.match(r\"(vim|nano|sed|awk|echo.*>|cargo|git add|git commit)\", c))
tests = sum(1 for c in cmds if re.match(r\"(cargo test|pytest|go test|jest|make test)\", c))
ratio = edits / max(1, tests)
print(f\"entropy: {ratio:.2f} ({edits} edits / {tests} tests)\")
"'
```

**State preservation:**  
On DEGRADED transition, entropy module writes `~/.terminal-state/entropy.json`:
```json
{"window_size": 50, "edit_count": 14, "test_count": 6, "last_ratio": 2.33, "timestamp": 1748901234}
```
Shell fallback reads this file first; falls back to live `history` computation if stale (>300s).

---

### 2.2 Hodge Error Decomposition (`math_analysis/error_hodge`)

**What it does:** Decomposes error signals into three orthogonal components via Hodge decomposition on the error 1-form:
- **H⁰ (harmonic):** Systemic errors — same root cause recurring across contexts
- **grad (gradient):** Directional errors — fixable by moving toward a known solution
- **curl (curl):** Oscillating errors — fix causes regression, regression causes fix

**Active state:**  
Eigendecomposition on the Laplacian of the error graph. Displayed as colored stack traces with component annotation.

**Failure modes:**
- Singular or near-singular Laplacian (degenerate error graph)
- Eigendecomposition exceeds time budget (>2s)
- Insufficient error samples (<3) for meaningful decomposition

**DEGRADED fallback:**  
Pattern-match error text against a static dictionary of known error signatures. Classify by exit code + stderr keyword:
```
exit 1 + "cannot find" → gradient (fixable, path/import issue)
exit 1 + "type mismatch" → gradient (fixable, type error)  
exit 1 + repeated same error → harmonic (systemic)
exit 0 + test failure → curl (oscillating, logic regression)
```

**SHELL fallback:**
```bash
# Hodge-lite: classify last N errors from cargo/compiler output
alias hodge-lite='
  LOG=~/.terminal-state/errors.log
  if [ -f "$LOG" ]; then
    SYSTEMIC=$(grep -c "E0" "$LOG" 2>/dev/null || echo 0)  # compiler codes
    FIXABLE=$(grep -c "cannot find\|not found\|undefined" "$LOG" 2>/dev/null || echo 0)
    OSCILLATE=$(grep -c "regression\|was passing\|revert" "$LOG" 2>/dev/null || echo 0)
    echo "harmonic(systemic)=$SYSTEMIC gradient(fixable)=$FIXABLE curl(oscillating)=$OSCILLATE"
  else
    echo "hodge: no error log. run: cargo test 2>>~/.terminal-state/errors.log"
  fi
'
```

**State preservation:**  
On each error event, module appends to `~/.terminal-state/errors.log` (rolling 500 lines). Hodge decomposition result written to `~/.terminal-state/hodge-last.json`:
```json
{"harmonic": 0.12, "gradient": 0.71, "curl": 0.17, "n_samples": 23, "dominant": "gradient"}
```

---

### 2.3 Markov Command Predictor (`math_analysis/command_markov`, `forecast/`)

**What it does:** Builds a transition matrix over command sequences, computes the stationary distribution, and predicts the next likely command. The forecast module surfaces the top-3 candidates as inline suggestions.

**Active state:**  
Full transition matrix over last N=500 commands. Power-iteration for stationary distribution. Confidence weighted by recency decay.

**Failure modes:**
- Transition matrix is reducible (no stationary distribution exists — user has disconnected workflow segments)
- Power iteration fails to converge (absorbing states, cyclic structure)
- Cold start: insufficient history (<20 commands)
- Memory budget exhausted; matrix evicted

**DEGRADED fallback:**  
Bigram frequency table only (no matrix inversion). Top-3 commands following the current command, by raw count:
```
given current command C, return top-3 most frequent C → ? transitions from history
```

**SHELL fallback:**
```bash
# Markov-lite: frequency-based next-command suggestion
markov_suggest() {
  local current="${1:-$(history 1 | awk '{print $2}')}"
  local hist_file="${HISTFILE:-~/.bash_history}"
  # Find lines after occurrences of $current, count next commands
  awk -v cmd="$current" '
    found {print; found=0}
    $0 == cmd {found=1}
  ' "$hist_file" | sort | uniq -c | sort -rn | head -3 | \
    awk '{printf "  [%d] %s\n", $1, $2}'
}
# Usage: markov_suggest "cargo test"
```

**State preservation:**  
Transition matrix serialized on eviction to `~/.terminal-state/markov-matrix.msgpack` (binary, compact). Shell fallback ignores this file — it computes directly from `$HISTFILE`. On recovery, module deserializes the matrix and continues without cold start.

---

### 2.4 Spectral Dashboard (`math_analysis/spectral_dashboard`)

**What it does:** Spectral analysis of the command stream. Treats the sequence of commands as a time-domain signal and computes frequency components via DFT — identifying periodic workflow patterns (daily build cycle, edit-test-commit loop), aperiodic bursts (debugging sessions), and phase drift between expected and actual workflow rhythm.

**Active state:**  
Sliding DFT window over last 200 commands. Phase alignment detection against learned baseline. Rendered as frequency histogram in terminal sidebar.

**Failure modes:**
- Window too small for meaningful DFT (<32 samples)
- New session: no baseline to align against
- Rendering failure in VT layer
- Agent process dies mid-computation

**DEGRADED fallback:**  
Simple time-bucketed command histogram: group commands by hour-of-day, show peak hours and current deviation from peak:
```
08:00-10:00: build phase (peak)
14:00-16:00: debug phase (peak)  
Current: 19:42 — off-peak; last command 8m ago
```

**SHELL fallback:**
```bash
# Spectral-lite: command rhythm from history timestamps
alias spectral-lite='
  if command -v fc >/dev/null 2>&1; then
    fc -l -100 | awk "NR%10==0 {print NR, \$2}" | head -10
  else
    history 100 | awk "NR%10==0 {print NR, \$2}" | head -10
  fi
  echo "---"
  echo "workflow phase estimate:"
  HOUR=$(date +%H)
  if [ "$HOUR" -lt 12 ]; then echo "  morning: likely build/setup"
  elif [ "$HOUR" -lt 17 ]; then echo "  afternoon: likely debug/iterate"
  else echo "  evening: likely commit/review"
  fi
'
```

**State preservation:**  
Power spectrum snapshot to `~/.terminal-state/spectral-cache.json` on module eviction. Includes learned baseline vector (128 floats) for phase alignment on recovery.

---

### 2.5 Skill Detector (`skill_detector/`)

**What it does:** Renormalization group (RG) analysis of command sequences to detect skill-level transitions and workflow phase boundaries. The RG flow identifies fixed points (stable workflow patterns), relevant operators (new tools being integrated), and irrelevant operators (commands that drop out as skill increases). Detects transitions: novice → journeyman → expert → mastery.

**Active state:**  
Multi-scale coarse-graining of command history. Fixed-point detection via β-function computation. Phase boundary detection at critical coarse-graining scales.

**Failure modes:**
- RG flow diverges (no fixed point — user in completely novel workflow)  
- Insufficient history for multi-scale analysis (<100 commands)
- β-function computation exceeds memory budget

**DEGRADED fallback:**  
Heuristic skill proxy: vocabulary richness (unique commands / total commands), flag complexity (avg flags per command), pipe depth (avg pipeline length):
```
skill_score = 0.4 * (unique_cmds/total_cmds) 
            + 0.3 * avg_flags_per_cmd/3.0
            + 0.3 * avg_pipe_depth/2.0
```

**SHELL fallback:**
```bash
alias skill-lite='
  HIST="${HISTFILE:-~/.bash_history}"
  TOTAL=$(wc -l < "$HIST")
  UNIQUE=$(sort -u "$HIST" | wc -l)
  PIPES=$(grep -c "|" "$HIST" || echo 0)
  FLAGS=$(grep -o "\-\-[a-z]*" "$HIST" | wc -l)
  echo "vocabulary density: $(echo "scale=2; $UNIQUE*100/$TOTAL" | bc)%"
  echo "pipe usage: $(echo "scale=2; $PIPES*100/$TOTAL" | bc)% of commands"
  echo "flag usage: ~$(echo "scale=1; $FLAGS/$TOTAL" | bc) flags/cmd avg"
'
```

**State preservation:**  
Skill profile (current RG fixed-point coordinates, phase label, trajectory) to `~/.terminal-state/skill-profile.json`. Shell fallback cannot reconstruct RG trajectory but can display the last known phase label.

---

### 2.6 Agent Disagreement Visualization (`ui/agent_disagreement`)

**What it does:** Computes H⁰ and H¹ sheaf cohomology on the agent response graph. H⁰ = global consensus (connected components of agreement), H¹ = irreducible disagreement loops (topological obstacles to consensus). Rendered as a live graph in the terminal sidebar.

**Active state:**  
Sheaf Laplacian on agent response similarity graph. Betti numbers β₀, β₁ computed via sparse eigendecomposition. Color-coded: β₀ = number of consensus clusters, β₁ = number of disagreement cycles.

**Failure modes:**
- Fewer than 2 agents active (H¹ undefined)
- Agent process dies (response graph incomplete)
- Eigendecomposition stalls (large agent fleet)
- Response similarity matrix is rank-deficient

**DEGRADED fallback:**  
Pairwise diff: compute Levenshtein distance or token overlap between agent responses. Display top-3 most-disagreeing pairs:
```
agent_A vs agent_B: 34% agreement
agent_A vs agent_C: 89% agreement  
Consensus cluster: {A,C}; outlier: {B}
```

**SHELL fallback:**
```bash
# Disagreement-lite: diff agent output files
alias disagree-lite='
  DIR=~/.terminal-state/agent-responses
  if [ -d "$DIR" ]; then
    ls "$DIR"/*.txt 2>/dev/null | while read f1; do
      read f2
      if [ -n "$f2" ]; then
        OVERLAP=$(comm -12 <(sort "$f1") <(sort "$f2") | wc -l)
        TOTAL=$(cat "$f1" "$f2" | sort -u | wc -l)
        echo "$(basename $f1) vs $(basename $f2): $(echo "scale=0; $OVERLAP*100/$TOTAL" | bc)% overlap"
      fi
    done
  else
    echo "no agent responses in $DIR"
    echo "agents write responses to: $DIR/<name>.txt"
  fi
'
```

**State preservation:**  
Each agent response written to `~/.terminal-state/agent-responses/<agent-name>.txt` on generation. Sheaf Laplacian serialized to `~/.terminal-state/disagreement.json` (β₀, β₁, component membership).

---

### 2.7 Griot History (`griot_history/`)

**What it does:** Temporal decay of command relevance, pattern mining for workflow sequences, adinkra compression of command history (Ghanaian symbolic encoding of recurring patterns), and persistence barcodes for command topology (which workflows are persistent vs transient).

**Active state:**  
Exponential decay on command recency weights. Prefix tree pattern mining. Adinkra symbol assignment to recurring command sequences. Persistence diagram over command filtration.

**Failure modes:**
- Decay computation overflow (very long sessions)
- Pattern database corrupted
- Persistence barcode computation stalls (complex filtration)
- adinkra symbol table exceeds memory budget

**DEGRADED fallback:**  
Raw `HISTFILE` access with simple recency weighting (linear, not exponential). No adinkra compression. No persistence barcodes:
```bash
tail -n 200 "$HISTFILE" | sort | uniq -c | sort -rn | head -20
```

**SHELL fallback:**  
Griot history IS the shell layer — `~/.bash_history` is the ultimate fallback. The module adds structure on top of what already exists. Shell fallback = direct history file access, no module dependency.

**State preservation:**  
Griot history module writes to `~/.terminal-state/griot-weights.json` (command → relevance weight mapping). This file is the primary persistence artifact. Shell fallback can use it for weighted frequency analysis even without the module running.

---

### 2.8 Context Trigger FSM (`context_trigger/`)

**What it does:** Seven auto-activation rules that evaluate environment conditions and trigger module lifecycle transitions. Module lifecycle FSM with states: INACTIVE → ACTIVATING → ACTIVE → DEGRADED → EVICTED → INACTIVE.

**Active state:**  
All 7 rules evaluated on each command completion event. FSM state tracked per-module. Triggers include: error rate spike, directory change to known project type, idle timeout, memory pressure.

**Failure modes:**
- FSM deadlocks (ACTIVATING never reaches ACTIVE — module init hangs)
- All 7 trigger rules return false simultaneously (environment doesn't match any rule)
- Memory pressure triggers mass eviction, FSM loses track of module states
- Windows Terminal Agent process dies mid-FSM-transition

**DEGRADED fallback:**  
Manual activation only. Rules engine suspended. User can manually trigger module activation via explicit terminal command (see `terminal-ctrl` CLI wrapper). FSM state preserved in `~/.terminal-state/fsm-state.json`.

**SHELL fallback:**
```bash
# Manual module activation when context triggers are down
alias terminal-activate='
  echo "context_trigger FSM offline — manual activation:"
  echo "  export TERMINAL_ENTROPY=1       # enable entropy bar"
  echo "  export TERMINAL_HODGE=1         # enable Hodge error decomp"
  echo "  export TERMINAL_MARKOV=1        # enable command prediction"
  echo "  export TERMINAL_SPECTRAL=1      # enable spectral dashboard"
  echo "  export TERMINAL_SKILL=1         # enable skill detector"
  echo "  export TERMINAL_FORECAST=1      # enable forecast module"
  echo ""
  echo "All env vars read on next shell init or: source ~/.terminalrc"
'
```

**State preservation:**  
FSM state written to `~/.terminal-state/fsm-state.json` on each transition. Format:
```json
{
  "entropy_bar": "ACTIVE",
  "hodge": "DEGRADED",
  "markov": "EVICTED",
  "spectral": "INACTIVE",
  "skill_detector": "ACTIVE",
  "forecast": "ACTIVE",
  "agent_disagreement": "INACTIVE"
}
```

---

### 2.9 Module System (`module_system/`)

**What it does:** TerminalModule trait, memory budget enforcement, LRU eviction policy. Tracks per-module memory allocation, evicts least-recently-used modules when budget is exceeded.

**Active state:**  
Hard memory budget (configurable, default 64MB for all modules combined). LRU eviction queue. Memory pressure events trigger orderly eviction with state serialization.

**Failure modes:**
- Budget exceeded before any module can evict (all modules active simultaneously, spike)
- Eviction loop: eviction frees memory → module reactivates → budget exceeded → eviction
- Module refuses to evict (missing TerminalModule::serialize implementation)

**DEGRADED fallback:**  
Single-module mode: disable all modules except entropy_bar (lowest memory cost). User selects which module to activate at any time; only one runs.

**SHELL fallback:**
```bash
# Module budget check when module_system is down
alias budget-check='
  STATE_DIR=~/.terminal-state
  echo "=== terminal module memory budget ==="
  for f in "$STATE_DIR"/*.json; do
    SIZE=$(wc -c < "$f" 2>/dev/null || echo 0)
    echo "  $(basename $f): ${SIZE}B"
  done
  TOTAL=$(du -sh "$STATE_DIR" 2>/dev/null | awk "{print \$1}")
  echo "state total: $TOTAL"
  echo "set TERMINAL_BUDGET_MB=N to adjust (default 64)"
'
```

---

## 3. Event Detection: Shell Fallback vs Context Trigger

The distinction between a **context trigger event** (handled within Layer 2) and a **shell fallback event** (requires Layer 3) is critical. Routing to the wrong layer wastes resources or drops state.

### 3.1 Detection Matrix

| Condition | Layer | Signal | Action |
|-----------|-------|--------|--------|
| Module computation timeout (>2s) | Layer 2 → degraded | `module::poll()` returns `Poll::Pending` after deadline | Activate DEGRADED path within same module |
| Math runtime returns NaN/Inf | Layer 2 → degraded | Computation result fails sanity check | Use DEGRADED approximation, log to error store |
| Memory budget crossed 90% | Layer 2 → eviction | `module_system::pressure_event()` | LRU eviction, state serialization |
| Memory budget crossed 100% | Layer 2 → shell | OOM kill signal or allocation failure | Emergency snapshot, all modules to SHELL state |
| Context trigger rule stale (>5 consecutive misses) | Layer 2 → Layer 3 | `trigger::consecutive_misses() >= 5` | Disable trigger engine, activate manual shell activation |
| Windows Terminal Agent SIGTERM | Layer 2 → Layer 3 | `agent::heartbeat()` returns `Err` | Snapshot all module state, activate all shell fallbacks |
| Windows Terminal Agent SIGKILL / crash | Layer 3 only | No heartbeat for >10s | Shell fallbacks activate from last snapshot; no clean handoff |
| Shell state files corrupted | Layer 3 → escape hatch | CRC check fails on `.json` files | Escalate to natural language (§6) |

### 3.2 Fallback Threshold Definition

The `fallback_threshold` for each module is defined in `context_trigger/thresholds.rs` as a `FallbackThreshold` struct:

```rust
pub struct FallbackThreshold {
    pub timeout_ms: u64,          // max computation time before degraded
    pub min_samples: usize,       // min data points before math is valid
    pub memory_budget_bytes: u64, // eviction threshold
    pub consecutive_miss_limit: u8, // trigger misses before shell activation
}
```

Default values per module:

| Module | timeout_ms | min_samples | memory_budget_bytes | consecutive_miss_limit |
|--------|-----------|-------------|---------------------|----------------------|
| entropy_bar | 500 | 5 | 2MB | 3 |
| hodge | 2000 | 3 | 8MB | 5 |
| markov | 1000 | 20 | 16MB | 5 |
| spectral | 3000 | 32 | 12MB | 7 |
| skill_detector | 5000 | 100 | 20MB | 10 |
| forecast | 1000 | 20 | 16MB | 5 |
| agent_disagreement | 2000 | 2 | 8MB | 5 |

---

## 4. State Preservation Protocol

### 4.1 The Snapshot Contract

Every module implementing `TerminalModule` must implement the snapshot interface:

```rust
pub trait TerminalModule {
    // ... existing trait methods ...
    
    /// Write enough state for shell fallback to reconstruct approximate behavior.
    /// Must complete in <100ms. Must not fail silently.
    fn snapshot(&self) -> Result<ModuleSnapshot, SnapshotError>;
    
    /// Restore from shell-fallback-written state (may be stale).
    /// Module validates staleness and decides whether to cold-start or warm-start.
    fn restore(&mut self, snapshot: &ModuleSnapshot) -> RestoreResult;
    
    /// Approximate shell equivalent of this module's primary output.
    /// Printed to stderr when module enters SHELL state.
    fn shell_hint(&self) -> &'static str;
}
```

### 4.2 Snapshot Directory Structure

```
~/.terminal-state/
├── fsm-state.json              # Module FSM state (all modules)
├── entropy.json                # Entropy bar last values
├── hodge-last.json             # Hodge decomposition result
├── errors.log                  # Rolling error log (500 lines)
├── markov-matrix.msgpack       # Transition matrix (binary)
├── spectral-cache.json         # Power spectrum + baseline
├── skill-profile.json          # RG fixed-point + phase label
├── disagreement.json           # Sheaf cohomology result
├── griot-weights.json          # Command relevance weights
├── agent-responses/            # Per-agent response files
│   ├── agent_a.txt
│   └── agent_b.txt
└── MANIFEST.json               # Snapshot timestamps + CRC checksums
```

### 4.3 Write Policy

| Event | Snapshot written |
|-------|-----------------|
| Graceful module shutdown | Full snapshot, all fields |
| DEGRADED state entry | Partial snapshot (computed fields only) |
| SIGTERM received | Emergency snapshot (best-effort, <100ms) |
| Timer tick (every 60s) | Incremental snapshot (changed fields only) |
| Memory budget crossed 80% | Proactive snapshot before potential eviction |

### 4.4 Staleness Protocol

Shell fallback reads `MANIFEST.json` first. If a snapshot is older than `max_staleness_seconds` (default: 300s per module), the fallback degrades to live computation from `$HISTFILE` and system state. Stale snapshots are never deleted automatically — they accumulate as a historical record that can inform recovery.

### 4.5 Recovery Sequence

When a module recovers from SHELL state back to ACTIVE:

1. Read `MANIFEST.json` — identify snapshot timestamp
2. Call `restore()` with the snapshot
3. Module validates: is the snapshot usable? (not too stale, not corrupted)
4. If usable: warm-start (no cold start penalty, continue from last known state)
5. If not usable: cold-start, but populate history from `$HISTFILE` where possible
6. Update FSM state from SHELL → ACTIVATING → ACTIVE

---

## 5. Event Detection: What Triggers Shell vs Context

### 5.1 The Discriminating Question

> "Is the module's math runtime unable to compute, or is the module's context unavailable?"

**Math runtime failure** → the module is active but cannot produce a result. The shell fallback produces an approximate result using simpler methods. The module stays in DEGRADED state and retries on the next event.

**Context unavailable** → the trigger conditions don't match the environment. The module never activates. Shell fallback activates proactively (via env var or manual command). The module stays in INACTIVE state until trigger conditions are satisfied.

**Process death** → the entire agent is gone. Shell fallbacks activate from last snapshot. No retry is possible until the agent restarts.

### 5.2 Detection Implementation

```rust
pub enum FallbackReason {
    ComputationTimeout { module: ModuleId, elapsed_ms: u64 },
    InsufficientSamples { module: ModuleId, have: usize, need: usize },
    MemoryEviction { module: ModuleId, budget_bytes: u64, used_bytes: u64 },
    TriggerStaleness { rule_id: u8, consecutive_misses: u8 },
    AgentHeartbeatLost { last_seen_s: u64 },
    SnapshotCorrupted { file: PathBuf, crc_expected: u32, crc_actual: u32 },
}

pub fn should_activate_shell(reason: &FallbackReason) -> bool {
    match reason {
        FallbackReason::ComputationTimeout { elapsed_ms, .. } if *elapsed_ms < 5000 => false, // stay DEGRADED
        FallbackReason::InsufficientSamples { .. } => false, // stay INACTIVE, wait for data
        FallbackReason::MemoryEviction { .. } => true,       // evicted = shell
        FallbackReason::TriggerStaleness { consecutive_misses, .. } 
            if *consecutive_misses >= 5 => true,
        FallbackReason::AgentHeartbeatLost { .. } => true,   // always shell on death
        FallbackReason::SnapshotCorrupted { .. } => true,    // needs human intervention
        _ => false,
    }
}
```

---

## 6. The Escape Hatch: When Shell Can't Handle It

Shell fallback covers every module. But three conditions can exhaust the shell layer:

1. **Shell state files are corrupted** (CRC fails in `MANIFEST.json`)
2. **History file is empty or inaccessible** (`$HISTFILE` missing, permissions wrong)
3. **The shell itself is the broken component** (interactive shell crashes, PATH corrupted)

These are not runtime failures — they are environment failures. The escape hatch escalates to natural language.

### 6.1 Escalation Sequence

When `should_escalate_to_natural_language()` returns `true`, the terminal prints:

```
═══════════════════════════════════════════════════════
TERMINAL FALLBACK ESCALATION
═══════════════════════════════════════════════════════

The shell layer cannot reconstruct module state.
Reason: [specific reason from FallbackReason enum]

Last known state:
  Module: [module name]
  Last snapshot: [timestamp or "none"]
  FSM state: [state]

To recover manually, describe what you were doing:

  claude -p "My terminal module [X] failed. I was [description of task].
             What commands should I run to [accomplish goal]?"

Or check the state directory:
  ls -la ~/.terminal-state/
  cat ~/.terminal-state/MANIFEST.json

═══════════════════════════════════════════════════════
```

### 6.2 The Line You Can Type

Every module failure chain ends at a line the user can type. This is not a feature — it is a design invariant. The escape hatch makes it explicit:

| Module failed | The line you type |
|---------------|------------------|
| entropy_bar | `history 50 \| awk '{print $2}' \| sort \| uniq -c \| sort -rn` |
| hodge | `cargo test 2>&1 \| grep "^error" \| sort \| uniq -c \| sort -rn` |
| markov/forecast | `history 100 \| awk '{print $2}' \| sort \| uniq -c \| sort -rn \| head -10` |
| spectral | `history 200 \| awk 'NR%20==0{print NR, $2}'` |
| skill_detector | `sort -u ~/.bash_history \| wc -l` (vocabulary size = skill proxy) |
| agent_disagreement | `diff <(cat ~/.terminal-state/agent-responses/agent_a.txt) <(cat ~/.terminal-state/agent-responses/agent_b.txt)` |
| all modules (agent dead) | `cat ~/.terminal-state/fsm-state.json` (last known state) |
| all state corrupted | `claude -p "help me understand my current terminal workflow"` |

---

## 7. Implementation Checklist

When adding a new terminal module, the shell-layer durability contract requires:

- [ ] `TerminalModule::snapshot()` implemented — completes in <100ms
- [ ] `TerminalModule::restore()` implemented — validates staleness, chooses warm/cold start
- [ ] `TerminalModule::shell_hint()` returns a valid shell command the user can type
- [ ] Module writes to a documented file in `~/.terminal-state/`
- [ ] Module's `FallbackThreshold` values set in `context_trigger/thresholds.rs`
- [ ] Shell fallback alias/function documented in `shell/fallbacks.sh`
- [ ] Entry in §2 of this document with all three states defined

No module ships without a shell fallback. The fallback ships before the module is marked stable.

---

## Closing

This architecture makes the terminal indestructible. Every module has a fallback. Every fallback has a shell. Every shell has a line you can type.

The math runtime can fail. The context triggers can go stale. The Windows Terminal Agent process can die. None of these conditions end the session. The user retains the ability to understand what was being computed, reconstruct an approximation using standard Unix tools, and decide whether to restart the module or proceed manually.

The shell layer is not the floor — it is the boundary between what the machine computes and what the human intends. That boundary is always available. That is what makes the terminal a tool rather than a dependency.

---

*Document version: 2026-06-02. Module count: 8 primary modules + module_system + context_trigger FSM.*  
*Total codebase: ~13,500 lines Rust. All modules feature-gated. Zero-cost when disabled.*
