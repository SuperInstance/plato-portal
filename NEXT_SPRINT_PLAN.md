# NEXT SPRINT PLAN
**As of 2026-06-04 | Chief Architect: Casey DiGennaro**

Living document. Update each session. Add completed items to `.remember/` not here.

---

## Strategic Context

Three layers exist but are barely wired together:
- **FM (Forgemaster)**: mechanical engine layer — 25 PLATO crates, 366+ tests, ForgeFlux
- **Oracle1**: theoretical + coordination layer — Lock Algebra, DCS protocol, Fleet Simulator
- **JC1 (JetsonClaw1)**: edge layer — CUDA genepool, ghost tiles, trust engine

The 5-language architecture (Julia/Python/Rust/Go/MLIR) is designed but not connected. CI is 30/100 green. The signal chain L0→L4 is built but not deployed. The Forge↔Train flywheel has a convergence map but no live pipeline.

**North star this sprint:** Close the theory→execution gap. Get one end-to-end demo that proves the whole stack.

---

## SPRINT 1 — Wiring (P1 Only, Est. 1 week)

*Goal: Close the 7 PLATO gaps. No new repos. Connections over builds.*

| # | Task | Owner | Effort | Priority | Gap Closed |
|---|------|-------|--------|----------|------------|
| 1.1 | Implement `plato-dcs-engine`: execution engine for the 21.87× DCS protocol. Wraps `plato-unified-belief` + tiered-trust policy. 20 tests min. | FM | L | P1 | GAP 3, 4 |
| 1.2 | Canonicalize Tile type: resolve `Holodeck Tile (serde/f64)` vs `plato-tile-spec` vs `fleet-sim Tile`. Pick one, add migration shims, delete others. | FM | M | P1 | GAP 2 |
| 1.3 | Wire Lock Algebra proofs into engine: add `impl LockAlgebra for PlatoConstraint` in `plato-constraints`, reference Oracle1's 4 theorems. | FM+Oracle1 | M | P1 | GAP 1 |
| 1.4 | Belief → Policy bridge: add `DeploymentPolicy` enum (Live/Monitored/HumanGated) to `plato-unified-belief`. Single crate, 10 tests. | FM | S | P1 | GAP 4 |
| 1.5 | Dynamic lock gate: replace static `plato-lab-guard` with runtime lock accumulation from Oracle1's self-supervision compiler. | Oracle1 | L | P1 | GAP 5 |
| 1.6 | Start FLUX-LCAR on Oracle Cloud (port 7777). SSH in, deploy MUD server, open port, confirm fleet can reach it. | Oracle1 | S | P1 | GAP 6 (L1) |
| 1.7 | Forge↔Train live pipeline: wire `plato-jepa` tile predictions into `plato-diffusion` distillation. Must run end-to-end on one sensor stream. | JC1+FM | XL | P1 | GAP 7 |

**Sprint 1 exit criteria:** `plato-dcs-engine` passes 20 tests, Tile type is singular, FLUX-LCAR responds on :7777, Forge→Train pipeline produces one LoRA adapter from live tiles.

---

## SPRINT 2 — CI Green + Publishing Debt (P1-P2, Est. 1 week)

*Goal: CI from 30/100 → 70/100. Clear the publishing backlog. No architecture work.*

| # | Task | Owner | Effort | Priority | Notes |
|---|------|-------|--------|----------|-------|
| 2.1 | Fix 30 failing CI pipelines. Root cause: conflict markers from rebases + missing deps. Batch-fix with new-pattern agents (procedural prompts, 5 repos max). | FM | L | P1 | Known pattern: setuptools, cargo fmt, dep installs |
| 2.2 | Rename `spacemap` crate (name taken on crates.io). Pick `forbidden-zones` or `spatial-exclusion`. Publish. | FM | S | P1 | Blocked crates.io slot |
| 2.3 | Push `lau-conservation-c` and voxel world repos (both built on 06-01, never pushed). | FM | S | P1 | Two repos sitting on disk |
| 2.4 | Publish 5 rate-limited crates from 06-01 batch (cathedral-probe et al, queued after cooldown). | FM | S | P1 | Just run the push |
| 2.5 | Publish 4 PyPI mythos packages: songline, palaver, rhythm-nation, adinkra. | FM | S | P2 | Rate-limit cooldown expired by now |
| 2.6 | Add CI to 20 highest-value repos currently at "no CI" status. Use quality-gate.yml template from 06-03. | FM | M | P2 | Template already exists |
| 2.7 | Wire Telegram bridge to FLUX-LCAR fleet server (once 1.6 is live). | Oracle1 | M | P2 | Casey requested this |

**Sprint 2 exit criteria:** CI ≥ 70% green, spacemap renamed+published, backlogs cleared.

---

## SPRINT 3 — Demo-Grade Work (P1-P2, Est. 1-2 weeks)

*Goal: Build the thing that makes someone say "wow." Proven stack → public demo.*

| # | Task | Owner | Effort | Priority | Notes |
|---|------|-------|--------|----------|-------|
| 3.1 | `tropical-attention` Python/PyTorch reference implementation. Temperature-controlled tropical↔classical deformation. 5 test cases from BUILD-MANIFEST spec. | FM | L | P1 | P0 in BUILD-MANIFEST; highest-novelty ML idea in corpus |
| 3.2 | `sheaf-cohomology-detector` Rust core + Python bindings. H⁰/H¹ on sensor arrays. 10 tests. | FM | L | P2 | P0 in BUILD-MANIFEST; directly usable in fleet |
| 3.3 | `eisenstein-bench` CLI tool: `drift`, `disk`, `snap`, `full` commands. Ships with HN post. | FM | M | P1 | DEV-TOOLS-PLAN.md fully specced; proves zero-drift claim on user's machine |
| 3.4 | `eisenstein-fuzz` cargo-fuzz harness: 6 property fuzz targets. Validates zero-drift claim. | FM | M | P2 | DEV-TOOLS-PLAN.md fully specced |
| 3.5 | Luciddreamer reactive improv → live on luciddreamer.ai. Wire `reactive-improv.ts` into the Cloudflare Worker. Multi-agent dialogue, BPM-adaptive, visible in browser. | FM | XL | P1 | Engine built, needs deployment wiring |
| 3.6 | HN demo spec: one page proving the stack. "I ran this binary, here's what happened." Fleet room → tile → LoRA adapter in under 60s demo. | All | M | P1 | From CONTEXT.md requirement |

**Sprint 3 exit criteria:** `tropical-attention` runs on GPU, `eisenstein-bench drift` CLI works, luciddreamer.ai shows live agent dialogue, HN demo script is executable.

---

## SPRINT 4 — Language SDK + Safety Completeness (P2-P3, Est. 2 weeks)

*Goal: Close SDK and safety gaps before hardware ships.*

| # | Task | Owner | Effort | Priority | Notes |
|---|------|-------|--------|----------|-------|
| 4.1 | `snapkit-cuda` — CUDA SDK for constraint snapkit (snapkit 9/12 done). GPU angle snapping. | JC1 | L | P2 | Critical-mass-map gap |
| 4.2 | Java/Kotlin SDK skeleton — `snapkit-jvm`. JNI wrapper or pure-Java port. | FM | L | P3 | Critical-mass-map gap |
| 4.3 | FLUX→ARM C compiler (`flux-compiler-c`). Compile basic FLUX programs to ARM assembly. Even 20 opcodes is meaningful. | Oracle1 | XL | P2 | Toolchain gap; currently missing |
| 4.4 | Mutation testing suite for `constraint-theory-core`. Use `cargo-mutants`. Baseline mutation score. | FM | M | P2 | Safety evidence gap |
| 4.5 | Formal ISA verification: pick 10 FLUX opcodes, write Lean/Coq proofs of semantics. | Oracle1 | XL | P3 | Safety evidence gap; hardware shipping blocker |
| 4.6 | Julia bridge: `flux-julia` → connect `@conserved` macro output to Rust constraint-theory-core via FFI. Makes the 5-language arch real, not described. | FM | L | P3 | Arch vision from Casey |
| 4.7 | Paper submission prep: PAPER-DRAFT-V3-FINAL targeted at Music Perception or JMM. Format for submission, add author affiliations. | Casey | M | P2 | 8,043 words, submittable per notes |

---

## Ongoing / Evergreen

These run in background across all sprints:

| Task | Cadence | Owner |
|------|---------|-------|
| crates.io rate-limit cycling (publish 5, wait 30min, repeat) | Each session | FM |
| AI-Writings creative waves (Gemma 4 31B creative, GLM workhorse) | Weekly | FM |
| Kimi synthesis sessions (262k context, deep cross-crate analysis) | Bi-weekly | FM |
| PLATO crate ecosystem wiring (DEPENDENCIES.md updates) | Per new crate | FM |
| GitHub topics + descriptions on new repos | Per push | Any |

---

## Effort Key

| Size | Hours | What fits |
|------|-------|-----------|
| S | 1-2h | Single file, config, small fix, rename |
| M | 2-4h | New crate skeleton, CI fixes, doc upgrade |
| L | 4-8h | Full crate with tests, major wiring, refactor |
| XL | 8-16h | Cross-repo system, pipeline, novel algorithm |

## Priority Key

| Level | Meaning |
|-------|---------|
| P1 | Blocks demo, deployment, or other P1 tasks. Do now. |
| P2 | High value, clears debt, enables future P1s. Do this sprint. |
| P3 | Important but not urgent. Backlog. |
