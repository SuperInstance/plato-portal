# Mining Consensus — lau-* Repo Action Plan

## Methodology
3 independent reviewers (GLM-5.1 builder lens, GLM-5.1 user lens, DeepSeek code lens) evaluated 120 lau-* repos.

## Consensus: Top 8 Diamonds (all 3 reviewers agree)

These repos have real code (20K-112K LOC each with tests), solve problems Rust lacks, and could gain real users if renamed and published.

| Current Name | New Standalone Name | Target Users | Why Rust Needs It |
|---|---|---|---|
| lau-time-series | `rusty-series` | Data engineers, IoT devs | No comprehensive time-series crate in Rust |
| lau-a2a-protocol | `agent-to-agent` | AI agent builders | Google A2A — first-mover Rust impl |
| lau-database-theory | `db-internals` | DB hackers, students | Best "build your own DB" in Rust |
| lau-queueing-theory | `queueing-theory` | SREs, capacity planners | Unique — load modeling |
| lau-topological-data-analysis | `tda-rs` | Data scientists | Only TDA crate in Rust |
| lau-scheduling-theory | `scheduling-rs` | Ops/infra engineers | Fleet/task scheduling |
| lau-fluid-dynamics | `cfd-rs` | Physics sim devs | Only CFD crate in Rust |
| lau-convex-optimization | `convex-rs` | ML/ops researchers | Interior point, proximal operators |

## Strong Keep (educational, 15 repos)
- neural-networks, statistical-learning, numerical-pde, numerical-linear-algebra
- operating-systems, robotics, computer-vision, computer-graphics
- graph-theory, dynamical-systems, chaos-theory, information-theory
- solid-mechanics, electromagnetism, harmonic-analysis

## Keep As-Is (PLATO-specific, 15 repos)
- ai-tutor, construct, construct-cli, leaderboard, constellation
- fibonacci-growth, achievements, collab, mission, weather, voice
- consciousness-bridge, destruction-transform, token-economy, tutorial

## Archive Immediately (44 repos)
All lau-shell-*, lau-vibe-*, lau-ensign-*, lau-*-agents (superseded), and pure esoteric math:
- derived-topos, mirror-symmetry, contact-geometry, hodge-theory, sheaf-cohomology
- ricci-flow-agents, noncommutative-agents, symplectic-agent, dynamical-systems-agents
- hodge-decomposition-agents, teleomorphic, jepa-gravity, gravity-field, landauer-meter
- shell-kernel, shell-transport, shell-lifecycle, shell-interface, shell-spawn, inter-shell
- bytecode, blueprint, vibe-compiler, vibe-field, vibe-visualizer, wasm-bridge
- tick-runtime, tile-store, async-tick, ts-bridge, circuit, affordance
- domestication, inheritance, provenance, tradition-proof, trading, tensor-midi
- conservation-guard, conservation-engine, fixedpoint, time, evolution

## Execution Plan

### Phase 1: Rename + Publish Top 8 (this session)
For each diamond:
1. Fork lau-X → SuperInstance/new-name
2. Strip all PLATO/LAU/agent references from code and docs
3. Update Cargo.toml with standalone name + description
4. Add real README with examples
5. Publish to crates.io

### Phase 2: Archive 44 repos
```bash
for repo in [list]; do gh repo archive SuperInstance/$repo --yes; done
```

### Phase 3: Keep educational repos as-is for now
May consolidate into a monorepo later.

---

*Consensus of 3 independent model reviews. The hard truth: 70% of repos are archive candidates. The 8 diamonds could become real community tools.*
