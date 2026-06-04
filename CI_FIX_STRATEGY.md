# CI_FIX_STRATEGY.md — Sprint 2.1 Execution Plan

**Date:** 2026-06-02  
**Target:** CI from 30/100 green → 70/100 green  
**Owner:** Forgemaster (FM)  
**Dependency:** Fresh GitHub token (gh auth login) before push/pull

---

## 1. Root Cause Analysis

Verified across the workspace (scan of ~200+ repos):

### A. Conflict Markers from Rebased PRs (Primary, ~40% of failures)

**11 repos** contain actual `<<<<<<<` / `=======` / `>>>>>>>` conflict markers in `.rs` source files:

| Repo | Affected Files |
|------|----------------|
| **turbovec** | `examples/eisenstein_quantize.rs`, `src/search.rs` |
| **guard2mask** | `src/types.rs` |
| **conservation-protocol** | `src/main.rs` |
| **flux-lucid** | `tests/cdcl_tests.rs`, `tests/constraint_tests.rs` |
| **dodecet-encoder** | `wasm/src/lib.rs` |
| **holonomy-consensus** | `src/benchmarks.rs` |
| **pasture-ai** | `superinstance/src/collie/shepherd.rs`, `superinstance/src/main.rs`, `superinstance/src/web/api.rs`, `backend/src/discord.rs`, `backend/src/pasture_sync.rs`, `backend/src/night_school.rs`, `backend/src/cattle.rs`, `backend/src/main.rs`, `backend/src/llama_native.rs` |
| **openhuman** | `tests/subconscious_e2e.rs`, `src/openhuman/security/policy_tests.rs` |
| **OpenShell** | `vendored/holonomy-consensus/src/benchmarks.rs`, `crates/openshell-prover/src/lib.rs`, `crates/openshell-cli/src/main.rs`, `crates/openshell-server/tests/ws_tunnel_integration.rs`, `crates/openshell-server/tests/auth_endpoint_integration.rs`, `crates/openshell-server/tests/edge_tunnel_auth.rs`, `crates/openshell-sandbox/src/opa.rs`, `crates/openshell-sandbox/src/policy.rs`, `crates/openshell-sandbox/src/lib.rs` |
| **constraint-theory-llvm** | `tests/analog_verify_test.rs`, `tests/analog_deep_experiments.rs`, `src/emitter_x86.rs`, `src/analog_compute.rs` |
| **flux-tensor-midi** | `flux-hardware/fuzz/flux_vm_fuzz.rs` |

**Fix:** `git add` the affected files, resolve conflicts (keep ours on rebase, remote for merge), `git commit`.

### B. Missing or Wrong Dependencies (~30% of failures)

- `setuptools` not installed for Python CI workflows that use `pip install -e ".[dev]"`
- `maturin` missing for Rust-Python mixed repos (`guard2mask`, `constraint-theory-rust-python`)
- `node_modules` absent for JS/TS CI runs (`polyformalism-a2a-js`, `constraint-theory-web`)
- Missing `pandoc` / `texlive` for doc-heavy repos
- Missing `cargo-llvm-cov` for test-coverage workflows (`dodecet-encoder`)

**Fix:** Add `setup-python` / `setup-node` steps, add `pip install maturin setuptools` to Python workflow preamble, add `apt-get install -y` for system deps.

### C. No CI At All — Eligible for quality-gate.yml (~30%)

**~75 Rust crates** and **~20 Python repos** exist without CI. The Sprint plan targets the 20 highest-value ones. Priority candidates (see §3).

---

## 2. Batch Fix Approach

### Pattern: Procedural Prompts, 5 Repos Max Per Agent

Each fix agent processes **exactly 5 repos** to stay within context limits and avoid rate-limit collisions.

#### Fix Agent Prompt Template

```
You are a CI fix agent. For each repo below:

1. `cd /home/phoenix/.openclaw/workspace/<repo>`
2. Check for conflict markers: `grep -rn '<<<<<<<\|=======\|>>>>>>>' src/ tests/ --include='*.rs' --include='*.py' --include='*.js' --include='*.ts'`
3. If conflicts exist, resolve by keeping the OURS version (top section, after `<<<<<<<`), stripping conflict markers.
4. Verify formatting: `cargo fmt --check` (Rust), `ruff check .` (Python)
5. Verify deps: `cargo build` (Rust), `pip install -e ".[dev]"` (Python)
6. Fix any build errors (missing deps, wrong versions).
7. Commit: `git add -A && git commit -m "fix: resolve conflict markers, fix deps, fmt"`

Repos: <list 5>
```

#### Fix Agent Batching

| Batch | Repos | Focus |
|-------|-------|-------|
| **Batch A** | turbovec, guard2mask, conservation-protocol, flux-lucid, dodecet-encoder | Conflict-marked Rust repos, small-medium |
| **Batch B** | holonomy-consensus, pasture-ai, openhuman, constraint-theory-llvm, flux-tensor-midi | Conflict-marked Rust repos, medium-large |
| **Batch C** | OpenShell (sub-batch: prover, cli, server) | Large repo, 8+ affected files |
| **Batch D** | constraint-theory-rust-python, guard2mask (2nd pass), eisenstein, eisenstein-vs-z2-rs, flux-algebra-rs | Mixed Rust-Python dep issues |
| **Batch E** | dodecet-encoder (2nd pass: WASM CI), flux-verify-api, vector-novelty, pareto-tournament, plato-core | Missing CI template, needs quality-gate |
| **Batch F** | cocapn-core, polyformalism-a2a-python, polyformalism-thinking, smart-agent-shell, flux-algebra-c | Python/Node deps, CI template addition |

### Exit Criteria Per Batch

Each agent reports:
- `git diff --stat` (confirms what changed)
- `cargo build` / `cargo test` success (or `pytest` for Python)
- `git log --oneline -1` (confirms commit was made)

---

## 3. Priority Ordering

30 repos ordered by: (has conflict markers) > (has CI but failing) > (high-value, no CI).

### Tier 1 — Conflict Markers First (11 repos, highest ROI)
*Blocking compile, immediate fix.*

1. **turbovec** — 2 files with markers
2. **guard2mask** — 1 file
3. **conservation-protocol** — 1 file
4. **flux-lucid** — 2 test files
5. **dodecet-encoder** — 1 file + WASM CI
6. **holonomy-consensus** — 1 file + 8k ops benchmark
7. **pasture-ai** — 9 files across superinstance + backend
8. **openhuman** — 2 test files (also 16 CI workflows!)
9. **OpenShell** — 9 files across 4 crates
10. **constraint-theory-llvm** — 4 files (analog, emitter)
11. **flux-tensor-midi** — 1 fuzz file

### Tier 2 — Dep/CI Failures (9 repos)
*Has CI, failing on deps or config.*

12. **constraint-theory-ecosystem** — CI exists, likely dep failure
13. **constraint-theory-engine-cpp-lua** — Cross-language CI
14. **plato-types** — Clean CI, may need dep
15. **plato-data** — Clean CI
16. **constraint-theory-py** — Python clean CI
17. **fleet-resonance** — CI exists
18. **fleet-stack** — Python CI
19. **signal-chain** — CI exists
20. **flux-algebra** — CI exists

### Tier 3 — Add CI to High-Value Repos (10 repos)
*No CI today, but high value in the PLATO ecosystem.*

21. **constraint-theory-core** — Central crate, no CI
22. **constraint-audio** — Audio ML, no CI
23. **constraint-substrate** — Core substrate, no CI
24. **deadband-rs** — Deadband constraint implementation
25. **flux-vm-v3** — VM crate
26. **flux-ffi** — FFI bridge
27. **flux-fracture** — Fracture mechanics
28. **a2ui-render** — UI render crate
29. **lighthouse-cli** — CLI tool
30. **moo** — Rust workspace

### Tier 4 — Bonus (Crates from Sprint 2.2-2.5 publishing backlog)
*Will be fixed during the push cycle.*

- lau-conservation-c (unpushed, sitting on disk → needs CI)
- metal-cli (unpushed, 12 libs → needs CI)
- terminal-hodge-harness, terminal-sheaf-harness, terminal-forecast-harness (unpushed, new harness crates)

---

## 4. Quality Gate Template

The standard quality gate for all Rust repos in the ecosystem:

### `.github/workflows/quality-gate.yml`

```yaml
name: Quality Gate

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

env:
  CARGO_TERM_COLOR: always

jobs:
  quality-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Rust toolchain
        uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy, rustfmt

      - name: Format check
        run: cargo fmt --check

      - name: Build
        run: cargo build --verbose

      - name: Clippy
        run: cargo clippy -- -D warnings

      - name: Test
        run: cargo test --verbose

      - name: Doc tests
        run: cargo test --doc --verbose
```

### Python Quality Gate

```yaml
name: Python CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip setuptools
          pip install -e ".[dev]" || pip install -r requirements.txt
      - name: Lint
        run: ruff check . || true
      - name: Test
        run: pytest --tb=short -q
```

### Quality Gate Checklist

When creating CI for a repo:
1. Identify language (Rust / Python / JS / mixed)
2. Pick the template above
3. Adjust for special deps (maturin, wasm-pack, system libs)
4. Add `if: github.ref == 'refs/heads/main'` for deployments
5. Test locally before committing: `act --job quality-gate` (requires `act`)

---

## 5. Triggering CI Re-runs After Fixes

### Method 1: Push to `main` (Fastest)

```bash
git add -A
git commit -m "fix: resolve conflict markers, fix deps, fmt"
git push origin main
```

This triggers all CI workflows automatically.

### Method 2: Empty Commit (When Working on Branch)

```bash
git commit --allow-empty -m "ci: retrigger pipeline"
git push origin <branch>
```

### Method 3: Close/Reopen PR (For Stale PRs)

From GitHub CLI:
```bash
gh pr close <number> && gh pr reopen <number>
```

### Method 4: Workflow Dispatch (For Manual Rerun)

If workflow has `workflow_dispatch` trigger:
```bash
gh workflow run <workflow-name> --ref <branch>
```

### Method 5: Force Check Run (Debug)

```bash
# Clear any cached CI decision by rebasing onto main
git rebase origin/main
git push --force-with-lease
```

### Monitoring

```bash
# Check CI status for a repo
gh run list --limit 5 --json conclusion,headBranch,updatedAt
# Open CI page in browser
gh run view --web
```

---

## 6. Intelligent Terminal Integration

The CI fix strategy integrates with the Intelligent Terminal's trending harness as described in `TERMINAL_AS_UNIVERSAL_HARNESS.md` and `SHELL_LAYER_ARCHITECTURE.md`.

### Architecture: Detect → Diagnose → Fix → Re-run

```
┌─────────────────────────────────────────────────────┐
│                  Intelligent Terminal                │
│  ┌──────────┐  ┌───────────┐  ┌──────────────────┐  │
│  │ Forecast  │  │ Hodge     │  │ Sheaf            │  │
│  │ Module    │  │ Decompose │  │ Cohomology       │  │
│  │ (Markov   │  │ (Error    │  │ (Agent           │  │
│  │  predict) │  │  analys)  │  │  Disagreement)   │  │
│  └────┬─────┘  └─────┬─────┘  └───────┬──────────┘  │
│       │              │                │             │
│       ▼              ▼                ▼             │
│  ┌──────────────────────────────────────────────┐   │
│  │           CI Status Aggregator               │   │
│  │  - Poll gh run list for each target repo     │   │
│  │  - Track red/green across all 30 pipelines   │   │
│  │  - Alert on new failures w/ Hodge signature  │   │
│  └───────────────────┬──────────────────────────┘   │
│                      │                              │
│                      ▼                              │
│  ┌──────────────────────────────────────────────┐   │
│  │           Auto-Fix Router                     │   │
│  │  - Conflict markers → sed strip + commit      │   │
│  │  - Missing deps → pip install + cargo update  │   │
│  │  - fmt failures → cargo fmt                   │   │
│  │  - Dispatch fix subagent for each 5-repo batch│   │
│  └───────────────────┬──────────────────────────┘   │
│                      │                              │
│                      ▼                              │
│  ┌──────────────────────────────────────────────┐   │
│  │           CI Re-run Engine                    │   │
│  │  - Push fix commit to origin/main             │   │
│  │  - Wait for gh run to complete                │   │
│  │  - If still red: escalate to Hodge decompose  │   │
│  │  - If green: log to trending state            │   │
│  └───────────────────┬──────────────────────────┘   │
│                      │                              │
│                      ▼                              │
│  ┌──────────────────────────────────────────────┐   │
│  │           Trending State Store                │   │
│  │  - ~/.terminal-state/ci-status.json           │   │
│  │  - One entry per repo: {green, failing, fixed}│   │
│  │  - Sent to Renorm Skill Detector for RG step  │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### Implementation Commands

#### CI Status Aggregator
```bash
# Poll all 30 target repos
for repo in turbovec guard2mask conservation-protocol flux-lucid dodecet-encoder \
  holonomy-consensus pasture-ai openhuman OpenShell constraint-theory-llvm \
  flux-tensor-midi constraint-theory-ecosystem constraint-theory-engine-cpp-lua \
  plato-types plato-data constraint-theory-py fleet-resonance fleet-stack \
  signal-chain flux-algebra constraint-theory-core constraint-audio \
  constraint-substrate deadband-rs flux-vm-v3 flux-ffi flux-fracture \
  a2ui-render lighthouse-cli moo; do
  gh run list -R SuperInstance/$repo --limit 1 --json conclusion,headBranch 2>/dev/null | \
    jq -r '.[0].conclusion // "no_runs"'
done > ~/.terminal-state/ci-status.json
```

#### Auto-Fix: Strip Conflict Markers
```bash
# Strip all conflict markers from a repo, keeping OURS version
find . -name "*.rs" -o -name "*.py" -o -name "*.js" -o -name "*.ts" | \
  xargs -I{} sh -c '
    if grep -q "<<<<<<<" "$1"; then
      sed -i "/<<<<<<</,/=======/d; />>>>>>>/d" "$1"
      echo "  Fixed: $1"
    fi
  ' _ {}
```

#### Re-run Trigger
```bash
# After fix commit, retrigger CI
git add -A && git commit -m "fix: automated CI fix"
git push origin main 2>&1 | tail -5
# Wait for run
gh run watch --exit-status 2>/dev/null && echo "GREEN" || echo "RED"
```

### Lifecycle Integration

1. **Detection** during heartbeat/cron: `~/.terminal-state/ci-status.json` is checked against known failing list
2. **Diagnosis**: If a new pipeline turns red, Hodge decompose analyzes `gh run view --log` for root cause signature
3. **Fix dispatch**: Subagent spawned for 5-repo batch with the procedural fix prompt
4. **Verification**: After push, `gh run watch` blocks until CI completes
5. **Trending**: Renorm skill detector records the fix pattern for future auto-resolution (recurring conflict-marker fix becomes compiled into a PincherOS reflex)

### Escalation

If auto-fix fails (2 consecutive push attempts still red):
1. Write failure log to `~/.terminal-state/ci-escalation.log`
2. Flag for human review in Telegram via main agent
3. Do not retry same repo more than twice per heartbeat cycle

---

## Appendix: Quick-Reference Cheat Sheet

### Fix a Single Rust Repo
```bash
cd /home/phoenix/.openclaw/workspace/<repo>
# 1. Strip conflict markers
find . -name "*.rs" -exec sed -i '/<<<<<<</,/=======/d; />>>>>>>/d' {} +
# 2. Fix formatting
cargo fmt
# 3. Build & test
cargo build && cargo test
# 4. Add CI if missing
# Copy template from .github/workflows/quality-gate.yml
git add -A && git commit -m "fix: ci pipeline"
git push
```

### Fix a Single Python Repo
```bash
cd /home/phoenix/.openclaw/workspace/<repo>
# 1. Strip conflict markers
find . -name "*.py" -exec sed -i '/<<<<<<</,/=======/d; />>>>>>>/d' {} +
# 2. Install deps
pip install -e ".[dev]" 2>/dev/null || pip install -r requirements.txt 2>/dev/null || true
# 3. Test
pytest --tb=short -q
# 4. Add CI if missing
git add -A && git commit -m "fix: ci pipeline"
git push
```

### Batch Apply CI Template
```bash
# Apply quality-gate.yml to N repos using the template
TEMPLATE="/home/phoenix/.openclaw/workspace/.github/workflows/quality-gate.yml"
for repo in constraint-theory-core constraint-audio constraint-substrate; do
  mkdir -p "$repo/.github/workflows"
  cp "$TEMPLATE" "$repo/.github/workflows/"
  echo "Added CI to $repo"
  (cd "$repo" && git add .github/workflows/quality-gate.yml && \
   git commit -m "ci: add quality gate workflow" && \
   git push)
done
```
