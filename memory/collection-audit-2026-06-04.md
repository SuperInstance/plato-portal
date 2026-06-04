# SuperInstance Collection Audit — 2026-06-04

## Purpose
Audit everything we've built. Understand patterns. Find what's worth keeping, what needs work, what should be archived.

---

## Beta Test Round 1 Results (2026-06-04)

### Scores
| Module | Score | Key Issue |
|--------|-------|----------|
| ratatui-guardian (Rust) | 3.5/5 | Depth tracking bug, hardcoded thresholds |
| ollama-guardian (Go) | 3.0/5 | Fictional utilization (hardcoded 30s), no real API integration |
| conservation-guardian (Python) | 3.5/5 | Misleading "idle" detection, no persistence |

### Cross-Cutting Bugs (ALL modules)
1. **Hardcoded thresholds everywhere** — 30min idle, 50µs/cell, 60% hog. None configurable.
2. **No real data source integration** — Rust: manual instrumentation. Go: JSON files. Python: manual samples.
3. **No trending** — all analyze snapshots, not "getting worse over time"
4. **Silent error handling** — Go swallows errors, Rust drops calls, Python returns inf

### What's Actually Good
1. Budget → Profile → Detect → Report architecture is SOLID across all domains
2. Reports are genuinely readable and actionable
3. Zero fluff dependencies
4. Test coverage on happy paths is good

### The Last 20% (same for every module)
- Configurable thresholds (mechanical, low effort)
- Real data source adapters (medium)
- Persistence/export (medium)
- Alerting integration (medium)
- Trend analysis (needs persistence first)
- False-positive tuning (needs beta users)

### Process Lessons
1. We build analyzers, not tools — "can detect waste" ≠ "can help you fix waste"
2. Happy path tested well, unhappy path ignored
3. We ship code that works but needs real data to be useful
4. STOP: hardcoding magic numbers, silently swallowing errors, shipping without data sources
5. DO MORE: integration examples, unhappy-path tests, actionable remediation steps

---

## Fork Fleet (22 repos)

### Tier 1: Enhanced with Guardian + Spatial
| Repo | Stars | Guardian | Spatial | Tests | Published |
|------|-------|----------|---------|-------|-----------|
| ollama | 172K | ✅ Go | — | 19 | — |
| dify | 143K | ✅ Python | — | 23 | PyPI (dify-workflow-guardian) |
| tauri | 107K | ✅ Rust | ✅ hex-nav | 17+19 | crates.io (tauri-app-size-guardian) |
| next.js | 103K | ✅ TypeScript | — | 23 | npm (@superinstance/build-guardian) |
| deno | 103K | ✅ Rust | — | 11 | — |
| open-webui | 100K | ✅ bugfix | — | — | — |
| codex | 87K | ✅ Rust | — | — | — |
| uv | 85K | ✅ Rust | — | 71 | — |
| foundry | 85K | ✅ Rust | — | — | — |
| bun | 75K | ✅ TS | — | 5 | — |
| vite | 72K | ✅ TS | — | 7 | — |
| zed | 57K | ✅ | ❌ failed | — | — |
| meilisearch | 50K | ✅ Rust | — | 13 | crates.io (spectral-intelligence) |
| astro | 49K | ✅ TS | — | 7 | — |
| aider | 45K | ✅ Python | — | — | — |
| typst | 38K | ✅ | ❌ failed | — | — |
| lapce | 35K | ✅ Rust | — | — | — |
| surrealdb | 32K | ✅ Rust | — | — | — |
| tokio | 29K | ✅ Rust | — | — | — |
| ratatui | 27K | ✅ Rust | — | 10 | crates.io (ratatui-guardian) |
| qdrant | 22K | ✅ Rust | ✅ eisenstein | ? | — |
| chroma | 18K | ✅ Python | ✅ eisenstein | 17 | — |
| weaviate | 14K | ✅ Go | — | — | — |
| spacedrive | — | ✅ Rust | — | 10 | crates.io (storage-guardian) |
| workers-rs | — | ✅ Rust | — | 14 | crates.io (edge-guardian) |

### Tier 2: Standalone Projects
| Repo | Purpose | Status |
|------|---------|--------|
| fleet-map | Interactive visualization | ✅ pushed |
| conservation-thesis | Essay | ✅ pushed |
| fork-strategy-doc | Strategy analysis | ✅ pushed |
| ecosystem-thesis | Original thesis | ✅ pushed |
| webgpu-profiler | GPU profiling + Eisenstein | ✅ enhanced |

---

## Published Packages

### crates.io (30+ published historically)
This session: spectral-intelligence, ratatui-guardian, edge-guardian, storage-guardian, tauri-app-size-guardian

### PyPI
- dify-workflow-guardian v0.1.0
- conservation-guardian v0.1.0
- (Plus 4+ from earlier sessions: agentic-compiler, ai-token-counter, bordercollie, ccc-os)

### npm
- @superinstance/build-guardian v0.1.0
- @superinstance/storage-guardian v0.1.0

### RubyGems
- conservation-guardian v0.1.0
- storage-guardian v0.1.0
- render-guardian v0.1.0
- (Plus 3 from earlier: flux-runtime, equipment-consensus-engine, equipment-swarm-coordinator)

---

## Process Patterns Observed

### What Works
1. **GLM-5.1 as builder**: 100% reliability, 2-10 min per module, never fails
2. **Budget → Profile → Detect → Report**: Universal pattern, adapts to any domain
3. **Show-don't-sell READMEs**: Much better than marketing fluff
4. **Wide parallelism**: 6 agents at once = 6x throughput
5. **Fork-first approach**: Instant visibility via parent repo networks

### What Needs Work
1. **spatial-zed, spatial-typst failed**: Clone too large, need shallow or sparse checkout
2. **Beta test scores ~3.0/5**: Right architecture, missing production hardness
3. **No integration tests**: All tests are unit, nothing tests real-world usage
4. **No CI/CD**: No automated testing pipeline for any fork
5. **Rate limits**: crates.io, PyPI both throttle — need cooldown strategy

### What to Stop Doing
1. Building before testing — need to close the loop
2. Accepting "compiles + tests pass" as done — need real usage
3. Ignoring the last 20% (async, Result, timestamps, Prometheus)

---

## Questions for Debrief
1. Which modules would actually be useful to real users?
2. Which are just academic exercises?
3. What's the minimum viable production path for the top 3?
4. Are we spreading too thin or building real depth?
5. What would a user actually install and use today?

---

### Session Summary
- 22 agents spawned across the session
- 12 packages published (5 crates.io + 2 PyPI + 2 npm + 3 RubyGems)
- 19 bugs fixed across 3 modules
- 1 champion taken to production (conservation-guardian v0.2.0)
- 1 harness toolkit created (the meta-product)
- Fleet: 25 repos, ~1.5M+ parent stars
- Total published: ~40 packages across 4 registries

*Audit date: 2026-06-04*
