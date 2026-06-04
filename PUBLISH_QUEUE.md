# SuperInstance Ecosystem — Publish Queue

**Generated:** 2026-06-02
**Scope:** 406 top-level repositories in `/home/phoenix/.openclaw/workspace`
**Methodology:** Automated inventory of all repos, followed by deep analysis of publish infrastructure (Cargo.toml, pyproject.toml, setup.py, package.json), registry name availability, and library-quality assessment.

---

## Executive Summary

| Category | Rust (crates.io) | Python (PyPI) | JS/TS (npm) | Total |
|----------|------------------|---------------|-------------|-------|
| **(1) Ready to publish now** | 20 | 16 | 4 | **40** |
| **(2) Needs publish metadata** | 20 | 23 | 3 | **46** |
| **(3) Needs renaming to avoid conflicts** | 25 | 34 | 1 | **60** |
| **(4) Needs cleanup / not a package** | 7 binary-only + 4 experiments | 2 script-only + 6 experiments | 5 app-only + 7 experiments | **31** |
| **(5) Needs publish file created** | 1 | 10 | 0 | **11** |
| **Not recommended / docs / research** | — | — | — | **~218** |

**Total actionable packages:** 157 repos that should eventually be published.
**Quick wins (can publish today):** 40 repos.
**Estimated total effort to clear queue:** ~200–300 person-hours.

---

## (1) Ready to Publish Now

These repositories have complete metadata, are structured as libraries, have unique names on their target registries, and are substantial enough to publish immediately.

### Rust — crates.io (20 crates)

| # | Repo | Crate Name | Lines | Files | Action | Effort |
|---|------|------------|-------|-------|--------|--------|
| 1 | `conservation-spectral-v2` | `conservation-spectral-v2` | 1,913 | 9 | `cargo publish --dry-run` → publish | 15 min |
| 2 | `constraint-theory-rust-python` | `flux-constraint` | 1,133 | 7 | `cargo publish --dry-run` → publish | 15 min |
| 3 | `eisenstein-vs-z2-rs` | `eisenstein-vs-z2` | 665 | 4 | `cargo publish --dry-run` → publish | 15 min |
| 4 | `lau-agent-topology` | `lau-agent-topology` | 934 | 4 | `cargo publish --dry-run` → publish | 15 min |
| 5 | `lau-calm-noether-readme` | `lau-calm-noether` | 2,893 | 11 | `cargo publish --dry-run` → publish | 15 min |
| 6 | `lau-connes-spectral-triple` | `lau-connes-spectral-triple` | 1,289 | 6 | `cargo publish --dry-run` → publish | 15 min |
| 7 | `lau-constitutive-compute` | `lau-constitutive-compute` | 2,177 | 9 | `cargo publish --dry-run` → publish | 15 min |
| 8 | `lau-eigenfunction-policy-readme` | `lau-eigenfunction-policy` | 2,662 | 10 | `cargo publish --dry-run` → publish | 15 min |
| 9 | `lau-geometric-deep-learning` | `lau-geometric-deep-learning` | 4,301 | 14 | `cargo publish --dry-run` → publish | 15 min |
| 10 | `lau-geometric-growth` | `lau-geometric-growth` | 2,638 | 11 | `cargo publish --dry-run` → publish | 15 min |
| 11 | `lau-geometric-measure` | `lau-geometric-measure` | 3,861 | 10 | `cargo publish --dry-run` → publish | 15 min |
| 12 | `lau-mirror-control` | `lau-mirror-control` | 736 | 6 | `cargo publish --dry-run` → publish | 15 min |
| 13 | `lau-naturality-boundary` | `lau-naturality-boundary` | 3,289 | 11 | `cargo publish --dry-run` → publish | 15 min |
| 14 | `lau-penrose-growth` | `lau-penrose-growth` | 2,400 | 11 | `cargo publish --dry-run` → publish | 15 min |
| 15 | `lau-reward-hacking-detector-readme` | `lau-reward-hacking-detector` | 1,722 | 1 | `cargo publish --dry-run` → publish | 15 min |
| 16 | `lau-ricci-curvature-agents` | `lau-ricci-curvature-agents` | 2,765 | 10 | `cargo publish --dry-run` → publish | 15 min |
| 17 | `lau-sheaf-neural` | `lau-sheaf-neural` | 4,031 | 11 | `cargo publish --dry-run` → publish | 15 min |
| 18 | `lau-spectral-gap-experiment-readme` | `lau-spectral-gap-experiment` | 1,816 | 6 | `cargo publish --dry-run` → publish | 15 min |
| 19 | `lau-stochastic-homotopy` | `lau-stochastic-homotopy` | 3,210 | 13 | `cargo publish --dry-run` → publish | 15 min |
| 20 | `lau-tropical-geometry-agents` | `lau-tropical-geometry-agents` | 3,896 | 11 | `cargo publish --dry-run` → publish | 15 min |

### Python — PyPI (16 packages)

| # | Repo | Package Name | Lines | Files | Action | Effort |
|---|------|--------------|-------|-------|--------|--------|
| 1 | `agent-field` | `agent-field` | 368 | 2 | `python -m build` → `twine upload` | 1–2 h |
| 2 | `agentic-compiler` | `agentic-compiler` | 1,341 | 3 | `python -m build` → `twine upload` | 1–2 h |
| 3 | `cocapn-benchmark` | `cocapn-benchmark` | 425 | 6 | `python -m build` → `twine upload` | 1–2 h |
| 4 | `constraint-instrument` | `constraint-instrument` | 11,907 | 39 | `python -m build` → `twine upload` | 1–2 h |
| 5 | `constraint-theory-core` | `constraint-theory-core` | 3,715 | 15 | `python -m build` → `twine upload` | 1–2 h |
| 6 | `flux-algebra` | `flux-algebra` | 4,528 | 11 | `python -m build` → `twine upload` | 1–2 h |
| 7 | `flux-lib-py` | `flux-lib` | 1,731 | 9 | `python -m build` → `twine upload` | 1–2 h |
| 8 | `groove-analyzer` | `groove-analyzer` | 2,326 | 15 | `python -m build` → `twine upload` | 1–2 h |
| 9 | `hebbian-router` | `hebbian-router` | 356 | 2 | `python -m build` → `twine upload` | 1–2 h |
| 10 | `mud-arena` | `mud-arena` | 4,358 | 13 | `python -m build` → `twine upload` | 1–2 h |
| 11 | `plato-room-musician` | `plato-room-musician` | 956 | 6 | `python -m build` → `twine upload` | 1–2 h |
| 12 | `spline-midi-smooth` | `spline-midi-smooth` | 1,278 | 7 | `python -m build` → `twine upload` | 1–2 h |
| 13 | `swarm-rooms` | `swarm-rooms` | 252 | 4 | `python -m build` → `twine upload` | 1–2 h |
| 14 | `thermal-budget` | `thermal-budget` | 308 | 2 | `python -m build` → `twine upload` | 1–2 h |
| 15 | `tile-memory` | `tile-memory` | 1,331 | 9 | `python -m build` → `twine upload` | 1–2 h |
| 16 | `vector-novelty` | `vector-novelty` | 340 | 2 | `python -m build` → `twine upload` | 1–2 h |

### JavaScript — npm (4 packages)

| # | Repo | Package Name | Lines | Files | Action | Effort |
|---|------|--------------|-------|-------|--------|--------|
| 1 | `conservation-spectral-js` | `conservation-spectral` | 1,922 | 14 | Already published; verify metadata is current | 5 min |
| 2 | `dodecet-encoder` | `@superinstance/dodecet-encoder` | 946 | 3 | `npm run build` → `npm publish --access public` | 10 min |
| 3 | `flux-check-js` | `@superinstance/flux-check` | 2,242 | 13 | Already published; verify metadata is current | 5 min |
| 4 | `polyformalism-a2a-js` | `@superinstance/polyformalism-a2a` | 787 | 7 | Already published; verify metadata is current | 5 min |

---

## (2) Needs Cargo.toml / pyproject.toml / package.json

These repos are structured as libraries but are missing a root-level publish manifest. Some have manifests in subdirectories.

### Needs Cargo.toml (1 crate)

| # | Repo | Suggested Name | Language | Action | Effort |
|---|------|----------------|----------|--------|--------|
| 1 | `guard2mask` | `guard2mask` | Rust | Create `Cargo.toml` with `[package]`, `[lib]`, dependencies. Add LICENSE. Verify `cargo test`. | 1–2 h |

### Needs pyproject.toml (10 packages)

| # | Repo | Suggested Name | Language | Action | Effort |
|---|------|----------------|----------|--------|--------|
| 1 | `flux-negative-space` | `flux-negative-space` | Python | Write root `pyproject.toml` (PEP 621). Pin deps. Add LICENSE. | 30–60 min |
| 2 | `fleet-router-integration` | `fleet-router-integration` | Python | Write root `pyproject.toml`. Add test deps. Add LICENSE. | 30 min |
| 3 | `acg_protocol` | `acg-protocol` | Python | Write root `pyproject.toml`. Audit imports (pymongo, ragas?). Add LICENSE. | 1 h |
| 4 | `cyclotomic-field` | `cyclotomic-field` | Python | Write root `pyproject.toml`. Move tests to `tests/`. | 30 min |
| 5 | `hex-zhc` | `hex-zhc` | Python | Write root `pyproject.toml`. Check matplotlib/numpy deps. | 30 min |
| 6 | `agent-native-language` | `agent-native-language` | Python | Write root `pyproject.toml`. Add LICENSE. | 30 min |
| 7 | `musicdb-to-json` | `musicdb-to-json` | Python | Write root `pyproject.toml` with `[project.scripts]`. Migrate `requirements.txt` deps. | 30–60 min |
| 8 | `eisenstein-triples` | `eisenstein-triples` | Python | Write root `pyproject.toml`. Decide public API. | 30 min |
| 9 | `SuperInstance/superinstance` | `superinstance` | Python | Write `pyproject.toml` (or promote to standalone repo). Add deps, LICENSE. | 30 min |
| 10 | `a2a-conservation` | `a2a-conservation` | Python | Write root `pyproject.toml` if these scripts are reused by other repos. | 30 min |

### Needs package.json (0 new packages)

No repositories without any `package.json` were identified as clearly needing one. Two ambiguous cases (`ct-bridge-npm`, `court-jester`) contain only compiled `dist/` artifacts with no source — they need source recovery before any packaging.

---

## (3) Needs Renaming to Avoid Conflicts

These repositories have complete or mostly-complete metadata, but their chosen package/crate name is **already taken** on the target registry. They need a new unique name before publishing. Some also need metadata fixes.

### Rust — crates.io (25 crates)

| # | Repo | Current Name | Status | Suggested Rename | Also Needs Metadata? | Effort |
|---|------|--------------|--------|------------------|----------------------|--------|
| 1 | `conservation-spectral` | `conservation-spectral-core` | Taken | `si-conservation-spectral` | No | 1 h |
| 2 | `constraint-audio` | `constraint-audio` | Taken | `constraint-theory-audio` | No | 1 h |
| 3 | `constraint-mux` | `constraint-mux` | Taken | `constraint-mux-serial` | No | 1 h |
| 4 | `constraint-theory-llvm` | `constraint-theory-llvm` | Taken | `constraint-llvm-backend` | No | 1 h |
| 5 | `dodecet-encoder` | `dodecet-encoder` | Taken | `dodecet-12bit-encoder` | No | 1 h |
| 6 | `eisenstein` | `eisenstein` | Taken | `eisenstein-integers` | No | 1 h |
| 7 | `fleet-math-c` | `fleet-math-c` | Taken | `fleet-math-ffi` | No | 1 h |
| 8 | `flux-fracture` | `flux-fracture` | Taken | `flux-fracture-linalg` | No | 1 h |
| 9 | `flux-lucid` | `flux-lucid` | Taken | `flux-lucid-cdcl` | No | 1 h |
| 10 | `flux-verify-api` | `flux-verify-api` | Taken | `flux-verify-smt` | `repository` | 1.5 h |
| 11 | `flux-vm-v3` | `flux-vm-v3` | Taken | `flux-vm-constraint` | `description`, `license`, `repository` | 2 h |
| 12 | `holonomy-consensus` | `holonomy-consensus` | Taken | `holonomy-fleet-consensus` | No | 1 h |
| 13 | `lau-agent-thermodynamics` | `lau-agent-thermodynamics` | Taken | `si-agent-thermodynamics` | No | 1 h |
| 14 | `lau-banach-agents` | `lau-banach-agents` | Taken | `si-banach-agents` | `repository` | 1.5 h |
| 15 | `lau-categorical-mechanics` | `lau-categorical-mechanics` | Taken | `si-categorical-mechanics` | No | 1 h |
| 16 | `lau-control-theory-agents` | `math` (placeholder) | Taken | `lau-control-theory-agents` | `name`, `description`, `repository` | 1 h |
| 17 | `lau-dg-algebra` | `lau-dg-algebra` | Taken | `si-dg-algebra` | No | 1 h |
| 18 | `lau-dynamical-algebra` | `math` (placeholder) | Taken | `lau-dynamical-algebra` | `name`, `description`, `repository` | 1 h |
| 19 | `lau-free-probability-agents` | `lau-free-probability-agents` | Taken | `si-free-probability` | No | 1 h |
| 20 | `lau-information-geometry-agents` | `lau-information-geometry-agents` | Taken | `si-info-geometry` | No | 1 h |
| 21 | `lau-measure-agents` | `lau-measure-agents` | Taken | `si-measure-agents` | `description`, `repository` | 1.5 h |
| 22 | `lau-quantum-groups-agents` | `math` (placeholder) | Taken | `lau-quantum-groups-agents` | `name`, `description`, `repository` | 1 h |
| 23 | `memory-crystal` | `memory-crystal` | Taken | `si-memory-crystal` | `repository` | 1.5 h |
| 24 | `penrose-memory` | `penrose-memory` | Taken | `penrose-memory-palace` | No | 1 h |
| 25 | `superinstance-ffi` | `superinstance-ffi` | Taken | `si-math-ffi` | No | 1 h |

### Python — PyPI (34 packages)

| # | Repo | Current Name | Status | Suggested Rename | Also Needs Metadata? | Effort |
|---|------|--------------|--------|------------------|----------------------|--------|
| 1 | `ai-forest` | `plato-sdk` | Taken | `ai-forest-sdk` | `license`, `authors` | 4–8 h |
| 2 | `cocapn-core` | `cocapn` | Taken | `cocapn-core` (use repo name) | `authors` | 4–8 h |
| 3 | `collective-ai` | `collective-ai` | Taken | `collective-inference` | — | 4–8 h |
| 4 | `commit-predictor` | `commit-predictor` | Taken | `fleet-commit-predictor` | — | 4–8 h |
| 5 | `conservation-spectral-python` | `conservation-spectral` | Taken | `conservation-spectral-py` | `authors` | 4–8 h |
| 6 | `constraint-synth` | `constraint-synth` | Taken | `constraint-synthesizer` | `license`, `authors` | 4–8 h |
| 7 | `constraint-theory-py` | `constraint-theory` | Taken | `constraint-theory-py` | — | 4–8 h |
| 8 | `constraint-theory-rust-python` | `flux-constraint` | Taken | `flux-constraint-py` | `authors` | 4–8 h |
| 9 | `counterpoint-engine` | `counterpoint-engine` | Taken | `counterpoint-music` | — | 4–8 h |
| 10 | `ct-tools` | `ct-tools` | Taken | `constraint-tools` | — | 4–8 h |
| 11 | `device-router` | `device-router` | Taken | `ml-device-router` | — | 4–8 h |
| 12 | `eisenstein-embed` | `eisenstein-embed` | Taken | `eisenstein-embedding` | `license` | 4–8 h |
| 13 | `fleet-agent` | `fleet-agent` | Taken | `fleet-coordination` | `license`, `authors` | 4–8 h |
| 14 | `fleet-calibrator` | `fleet-calibrator` | Taken | `fleet-model-calibrator` | `license`, `authors` | 4–8 h |
| 15 | `fleet-health-monitor` | `quartermaster-gc` | Taken | `fleet-health-monitor` (use repo name) | — | 4–8 h |
| 16 | `fleet-murmur` | `quartermaster-gc` | Taken | `fleet-murmur-gc` | — | 4–8 h |
| 17 | `fleet-router` | `fleet-router` | Taken | `fleet-ai-router` | `license`, `authors` | 4–8 h |
| 18 | `flux-genome` | `flux-genome` | Taken | `flux-music-genome` | `license`, `authors` | 4–8 h |
| 19 | `flux-genome-py` | `flux-genome` | Taken | `flux-genome-py` | `license`, `authors` | 4–8 h |
| 20 | `flux-hyperbolic` | `flux-hyperbolic` | Taken | `flux-hyperbolic-geometry` | `license`, `authors` | 4–8 h |
| 21 | `flux-hyperbolic-py` | `flux-hyperbolic` | Taken | `flux-poincare-geometry` | `license`, `authors` | 4–8 h |
| 22 | `flux-index` | `flux-index` | Taken | `flux-code-index` | — | 4–8 h |
| 23 | `flux-tensor-midi` | `flux-tensor-midi` | Taken | `flux-tensor-midi` (check again) | — | 4–8 h |
| 24 | `holonomy-harmony` | `holonomy-harmony` | Taken | `holonomy-chords` | — | 4–8 h |
| 25 | `luciddreamer` | `luciddreamer` | Taken | `lucid-dreamer-ai` | — | 4–8 h |
| 26 | `luciddreamer-agent` | `luciddreamer-agent` | Taken | `lucid-agent` | — | 4–8 h |
| 27 | `micro-onnx` | `micro-onnx` | Taken | `micro-onnx-export` | — | 4–8 h |
| 28 | `plato-core` | `plato-core` | Taken | `plato-mesh-core` | `authors` | 4–8 h |
| 29 | `polyformalism-a2a-python` | `polyformalism-a2a` | Taken | `polyformalism-py` | — | 4–8 h |
| 30 | `quality-gate-stream` | `quartermaster-gc` | Taken | `quality-gate-stream` (use repo name) | — | 4–8 h |
| 31 | `sunset-ecosystem` | `sunset-ecosystem` | Taken | `sunset-agent-ecosystem` | `authors` | 4–8 h |
| 32 | `tensor-spline` | `tensor-spline` | Taken | `tensor-spline-layers` | — | 4–8 h |
| 33 | `training-throttle` | `training-throttle` | Taken | `ml-training-throttle` | — | 4–8 h |
| 34 | `triplet-miner` | `triplet-miner` | Taken | `git-triplet-miner` | — | 4–8 h |

### JavaScript — npm (1 package)

| # | Repo | Current Name | Status | Suggested Rename | Also Needs Metadata? | Effort |
|---|------|--------------|--------|------------------|----------------------|--------|
| 1 | `moo` | `moo` | Taken (by tjvr) | `@superinstance/moo` or `moo-extended` | N/A (clone of upstream) | 15 min decision |

> ⚠️ **Critical:** `moo` is a direct clone of the popular `tjvr/moo` tokenizer (~1M+ downloads/week). Do **not** publish under `moo`. Either fork to a scoped name, delete and use upstream, or verify modifications warrant a new package.

---

## (4) Needs Cleanup

These repos have publish infrastructure but are not ready for publication due to being binary-only, script-only, experiments, stubs, or apps.

### Rust — Binary-only or Experiments (11 repos)

| # | Repo | Category | Why Excluded | Action | Effort |
|---|------|----------|--------------|--------|--------|
| 1 | `OpenShell` | BINARY_ONLY | Workspace root; 179K lines; no lib.rs | Distribute via `cargo install --git` or release binaries | N/A |
| 2 | `analog-spectral` | BINARY_ONLY | `src/main.rs` only; spectral thermostat | Distribute as binary | N/A |
| 3 | `conservation-protocol` | BINARY_ONLY | `src/main.rs` only; no metadata | Distribute as binary | N/A |
| 4 | `flux-tensor-midi` | BINARY_ONLY | Workspace root; 70K lines; no root package | Publish workspace members individually | N/A |
| 5 | `lighthouse-cli` | BINARY_ONLY | CLI fleet task manager | Distribute as binary | N/A |
| 6 | `openhuman` | BINARY_ONLY | 428K-line server app | Distribute as binary | N/A |
| 7 | `warp-flux-poc` | BINARY_ONLY | PoC plugin architecture demo | Archive or absorb | N/A |
| 8 | `flux-algebra-rs` | EXPERIMENT | 353-line stub; name taken | Archive or absorb into larger crate | N/A |
| 9 | `flux-ffi` | EXPERIMENT | 275-line tiny wrapper; name taken | Archive or absorb | N/A |
| 10 | `spectral-conservation` | EXPERIMENT | 167-line single file; name taken | Archive or absorb | N/A |
| 11 | `turbovec` | EXPERIMENT | Workspace root; no package name | Investigate publishing members | N/A |

### Python — Script-only or Experiments (8 repos)

| # | Repo | Category | Why Excluded | Action | Effort |
|---|------|----------|--------------|--------|--------|
| 1 | `BusinessLog` | SCRIPT_ONLY | No `__init__.py`; just scripts | Refactor into package, add `__init__.py`, API design | 1–2 d |
| 2 | `cicd-agent` | SCRIPT_ONLY | No `__init__.py`; just scripts | Refactor into package, add `__init__.py`, API design | 1–2 d |
| 3 | `bootstrap-spark` | EXPERIMENT | 142 lines; unstable API | Stabilize API, add tests, expand docs | 4–8 h |
| 4 | `cocapn-oneiros` | EXPERIMENT | 2 lines; empty package | Implement core functionality | 1–3 d |
| 5 | `constraint-audio` | EXPERIMENT | 0 lines; empty package | Implement core functionality | 1–3 d |
| 6 | `plato-escalation-gate` | EXPERIMENT | 111 lines; 1 file | Stabilize API, add tests | 4–8 h |
| 7 | `plato-model-ocean` | EXPERIMENT | 321 lines; 1 file | Stabilize API, add tests | 4–8 h |
| 8 | `plato-room-intelligence` | EXPERIMENT | 231 lines; 1 file | Stabilize API, add tests | 4–8 h |

### JavaScript — App-only or Experiments (12 repos)

| # | Repo | Category | Why Excluded | Action | Effort |
|---|------|----------|--------------|--------|--------|
| 1 | `constraint-theory-web` | APP_ONLY | Educational website / deployed site | Deploy via Cloudflare Pages; not npm | N/A |
| 2 | `lucineer` | APP_ONLY | Next.js web app | Deploy as web app; not npm | N/A |
| 3 | `openhuman` | APP_ONLY | Tauri desktop app | Build release binaries; not npm | N/A |
| 4 | `pasture-ai` | APP_ONLY | Next.js web dashboard | Deploy as web app; not npm | N/A |
| 5 | `zerolang` | APP_ONLY | Language toolchain / compiler | Build release binaries; not npm | N/A |
| 6 | `agent-field` | EXPERIMENT | Python package with 0 JS files | Deprecate npm stub or add JS shim | 30 min |
| 7 | `collective-ai` | EXPERIMENT | Python package with 0 JS files | Deprecate npm stub or add JS shim | 30 min |
| 8 | `commit-predictor` | EXPERIMENT | Python package with 0 JS files | Deprecate npm stub or add JS shim | 30 min |
| 9 | `constraint-inference` | EXPERIMENT | Archived; superseded by forgemaster | Do not publish | N/A |
| 10 | `luciddreamer` | EXPERIMENT | 50-line JS stub; real value is Python | Deprecate npm stub or expand to JS SDK | 30 min |
| 11 | `swarm-rooms` | EXPERIMENT | Python package with 0 JS files | Deprecate npm stub or add JS shim | 30 min |
| 12 | `training-throttle` | EXPERIMENT | 158-line JS shim for Python pkg | Merge into larger SDK or deprecate | 30 min |

---

## Cross-Language Repos (Multiple Manifests)

Some repositories contain publishable code in **multiple languages**. They appear in multiple categories above. For these, decide on a per-language publishing strategy.

| Repo | Rust | Python | JS/TS | Notes |
|------|------|--------|-------|-------|
| `OpenShell` | Workspace | — | — | Publish individual member crates, not root |
| `SuperInstance` | — | SDK ready | Schemas ready | Publish both independently |
| `agent-field` | — | Ready | JS stub | Publish Python; fix or deprecate npm stub |
| `collective-ai` | — | Ready | JS stub | Publish Python; fix or deprecate npm stub |
| `commit-predictor` | — | Ready | JS stub | Publish Python; fix or deprecate npm stub |
| `constraint-audio` | Needs rename | Experiment | — | Rust rename needed; Python is empty |
| `constraint-theory-rust-python` | Ready | Needs rename | — | Publish Rust crate; rename Python bindings |
| `dodecet-encoder` | Needs rename | — | Ready | Rename Rust crate; publish npm package |
| `flux-tensor-midi` | Workspace | Needs rename | — | Publish members individually |
| `luciddreamer` | — | Needs rename | JS stub | Rename Python; fix or deprecate npm stub |
| `penrose-memory` | Needs rename | Ready | — | Rename Rust crate; publish Python package |
| `swarm-rooms` | — | Ready | JS stub | Publish Python; fix or deprecate npm stub |
| `training-throttle` | — | Needs rename | JS stub | Rename Python; fix or deprecate npm stub |

---

## Priority Action Plan

### Sprint 1 — Quick Wins (~2 days)
1. **Publish 20 Rust crates** (Category 1) — run `cargo publish --dry-run` and publish.
2. **Publish 16 Python packages** (Category 1) — build wheels and upload to PyPI.
3. **Publish `dodecet-encoder` to npm** — only unpublished JS library ready to go.
4. **Add missing metadata to 3 JS packages** — `SuperInstance`, `fleet-murmur-worker`, `intent-inference`.

### Sprint 2 — Fill Metadata Gaps (~1 week)
1. **Fix 20 Rust crates** (Category 2, Rust) — add `description`, `license`, `repository`.
2. **Fix 23 Python packages** (Category 2, Python) — add `license`, `authors`, `classifiers`.
3. **Create `Cargo.toml` for `guard2mask`**.
4. **Create `pyproject.toml` for 9 Python packages** without any manifest.

### Sprint 3 — Rename & Publish (~2 weeks)
1. **Rename 25 Rust crates** — search crates.io for unique names, update `Cargo.toml`, republish.
2. **Rename 34 Python packages** — search PyPI for unique names, update `pyproject.toml`, republish.
3. **Resolve `moo` npm conflict** — scoped name or delete.

### Sprint 4 — Cleanup & Refactor (~1–2 weeks)
1. **Refactor 2 Python script-only repos** into proper packages.
2. **Decide fate of 8 Python experiments** — implement, archive, or absorb.
3. **Resolve 5 ambiguous repos** (`ct-bridge-npm`, `court-jester`, `flux-tensor-midi-gh`, `deadband-constrained`, `a2a-conservation`).
4. **Deprecate or fix 6 npm Python stubs**.

---

## Not Recommended for Publishing

These 218+ repositories are documentation, research, experiments, apps, tests, or hardware projects and should **not** be published as packages:

**Docs & Research:** `docs`, `experiments`, `fm-research`, `polyformalism-thinking`, `flux-research`, `research`, `dissertation`, `papers`, `proposals`, `reviews`, `discussions`, `orations`, `AI-Writings`, `ai-writings`, `wiki`, `superinstance-wiki`, `message-in-a-bottle`, `archive`, `references`, `vocabularies`, `roadmaps`

**Hardware & Apps:** `openarm`, `platoclaw`, `zeroclaw-plato`, `repos`, `cocapn-ai-web`, `lucineer`, `pasture-ai`, `constraint-theory-web`

**Tests & Examples:** `tests`, `examples`, `flux-integration-tests`, `integration_tests`, `playtest-results`, `benchmarks`

**Proofs-of-Concept:** `px4-conservation-poc`, `octomap-conservation-poc`, `warp-flux-poc`

**Infrastructure & Config:** `docker`, `migrations`, `fleet-stack`, `fleet-gateway`, `fleet-simulation`, `device-router` (ops side), `SuperInstance/fleet`, `SuperInstance/agents`, `SuperInstance/protocols`

**Very Small / Stubs:** `penrose` (single script), `ccc-ecosystem` (utility scripts), `musicdb-to-json` (CLI, maybe), `galois-unification-proofs`, `constraint-theory-math`

---

## Methodology

1. **Inventory:** Scanned all 406 top-level directories for `Cargo.toml`, `pyproject.toml`, `setup.py`, and `package.json`.
2. **Source counting:** Counted `.rs`, `.py`, `.js`, `.ts` files per repo (max depth 3).
3. **Library detection:** Checked for `src/lib.rs`, `[lib]` in `Cargo.toml`, `__init__.py` for Python, and `main`/`module`/`exports` for JS.
4. **Registry checks:** Used `curl` against crates.io API, PyPI JSON API, and npm registry to check name availability.
5. **Human judgment:** Categorized repos by substance, maturity, and whether they provide reusable library value vs. being apps/experiments/docs.

---

*End of report. This queue should be reviewed quarterly as the ecosystem evolves.*
