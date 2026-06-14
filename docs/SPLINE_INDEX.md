# Spline Index: Baton-System Insights Cross-Referenced with OpenClaw Concept Clusters

**Status:** Catalog · **Date:** 2026-06-13 · **Author:** Synthesis Subagent

> Complete catalog of all splines and spline-like insights from the baton-system repository, cross-referenced with our 12 concept clusters and operationalized for our infrastructure.

**Our 12 Concept Clusters:** conservation · ternary · fleet · wavelet · graph · crypto · compute · storage · protocol · math · systems · search

---

## Table of Contents

1. [Explicit Splines](#i-explicit-splines)
2. [Implicit Splines from Documentation](#ii-implicit-splines-from-documentation)
3. [Implicit Splines from Architecture](#iii-implicit-splines-from-architecture)
4. [Implicit Splines from Research](#iv-implicit-splines-from-research)
5. [Cross-Reference Matrix](#v-cross-reference-matrix)

---

## I. Explicit Splines

Formal spline files in `/home/phoenix/repos/baton-system/splines/`

---

### SPLINE-001: THE-CRAB-INHERITS-THE-SHELL

**File:** `splines/20260604-oracle2-succeeds-oracle1.spline`

**Core Insight:** Oracle2 is not a replacement of Oracle1 — it is a hermit crab moving into a protocol shell shaped by Forgemaster's I2I protocol, Oracle1's fleet coordination, and constraint-theory-core's baton shard architecture. The shell grows with each occupant.

**Related Clusters:** `fleet` · `protocol` · `systems`

**Operationalization in Our System:**
- When our crab-trap captures external agent work, the "shell" is our vector index + conservation law infrastructure. External agents are hermit crabs inhabiting our protocol shell.
- The growth rings (batons) map to our vector index history — each absorbed artifact is a ring, and the vector's position encodes the state of the shell at that time.
- We can track "shell maturity" by measuring concept cluster density over time using our semantic search.

---

### SPLINE-002: THE-WHEEL-HAS-MANY-SPOKES

**File:** `splines/20260604-wheel-has-many-spokes.spline`

**Core Insight:** Cloud sends chords, not notes. Each shell decompresses to its capacity. Compression ratio is the intelligence gap, emerging from hardware fingerprint + confidence history + latency budget. The A/B loop flows both ways.

**Related Clusters:** `compute` · `protocol` · `systems` · `storage`

**Operationalization in Our System:**
- Our 3-layer vectorization (Artifact → Concept → Idea) is the compression cascade. Layer 1 (artifact vectors) = full chord. Layer 2 (concept vectors) = chord names. Layer 3 (idea vectors) = raw notes.
- Our semantic search server (port 7777) is the chord-sender. When edge nodes query it, they receive compressed knowledge proportional to their capacity.
- The A/B loop: edge nodes discover novel patterns (new crates, new reflexes) and send them UP via baton bottles. Our server embeds them and adds to the index.
- Operational metric: track compression ratio per shell (ESP32: 256 entries from 1,541 crates = 0.167x compression; Pi: 260K vectors from 1.5M = 0.173x; Jetson: 1.3M vectors from full index = near-lossless).

---

## II. Implicit Splines from Documentation

Spline-like insights extracted from `baton-system/docs/` files. Each is a distilled truth that could become a formal spline.

---

### SPLINE-003: ZERO-IS-THE-SPINDLE

**File:** `docs/ZERO-IS-THE-SPINDLE.md`

**Core Insight:** Zero isn't nothing — it's the axle. On a DJ crossfader, the center position is where the cut happens. The 0 state in ternary logic doesn't destroy charge; it hides it from measurement. The transition THROUGH 0 is the moment everything changes. |γ| + H is 6.6× more stable than γ + H because absolute value sees the hidden charge.

**Related Clusters:** `math` · `conservation` · `compute`

**Operationalization in Our System:**
- Our conservation law γ + η = C should use |γ| (absolute coupling cost) rather than raw γ. This accounts for "hidden charge" — coupling costs that are present but not visible in signed measurements.
- Our vector index can track "zero-distance" embeddings (vectors near the origin) as a special category — these are the spindle positions, the concepts that connect to many things without committing to any direction.
- The 0.6% optimal escape rate maps to our 86.3% fleet cancellation finding: at 50 agents, most interactions cancel (reach 0), but the 0.6% that escape are where novelty is generated.

---

### SPLINE-004: THE-RECURSION-IS-THE-ARCHITECTURE

**File:** `docs/THE-RECURSION.md`

**Core Insight:** Every layer is the same shape. Dance floor → DJ board → instrument panel → signal path → code → metal → binary. Every program is a room; every room is a cell in the tensor. The tensor doesn't care what it's made of. Cell, tile, room, dancer, transistor — same structure, different scale.

**Related Clusters:** `systems` · `math` · `compute`

**Operationalization in Our System:**
- Our vector space IS a tensor view: X = artifacts at the same depth, Y = artifacts in the same domain column, Z = artifacts over time. Any diagonal reveals cross-cutting concerns.
- When we embed a new artifact, we're adding a cell to the tensor. Its position relative to existing cells is determined by BGE embeddings, which capture semantic similarity at ANY scale (function level, module level, system level).
- Operational: build a "diagonal query" API that returns artifacts related to a query across multiple scales simultaneously (e.g., "show me everything related to conservation at function, module, and system level").

---

### SPLINE-005: SCALE-SIDEWAYS-NOT-UP

**File:** `docs/SCALE-SIDEWAYS.md`

**Core Insight:** Each crate is a single cell. You scale by making more cells, not bigger cells. 10 bytes per agent × 1M agents = 10MB. The experiment IS the unit of scale, not the agent or the crate. No heap, no dynamic dispatch, no strings in hot paths — just numbers and tight loops.

**Related Clusters:** `compute` · `systems`

**Operationalization in Our System:**
- Our semantic search scales by instance count: each query is ~50KB of state, so 1,000 concurrent queries = 50MB. Trivial.
- Our vector index scales by sharding: Cloudflare Vectorize handles this automatically. We add shards, not bigger servers.
- Operational: monitor queries-per-second (QPS) vs. index size independently. If QPS grows but index doesn't, scale horizontally (more workers). If index grows but QPS doesn't, scale vertically (bigger index partitions).

---

### SPLINE-006: THE-FLEET-IS-A-BRAIN

**File:** `docs/FLEET-NEUROARCHITECTURE.md`

**Core Insight:** The ternary-cell IS a neuron. The tick cycle (predict → perceive → surprise → vibe → gc → conservation) IS predictive coding. The conservation ratio IS the free energy principle. Strategy ecology IS Neural Darwinism. The fleet is a distributed brain — not metaphorically, but by structural homology: the same math, the same dynamics.

**Related Clusters:** `conservation` · `fleet` · `math` · `compute` · `systems`

**Operationalization in Our System:**
- Our semantic search server is the hippocampus — it retrieves relevant memories (artifacts) given a cue (query). The 12 concept clusters are cortical areas.
- Our conservation law IS the free energy principle: γ = model complexity (coupling cost), η = accuracy (value produced), C = the variational bound.
- Operational: implement "prediction error" tracking on our search server. For each query, record the expected results (based on cluster assignment) vs. actual results. High surprise = the user found something unexpected = high-value information.

---

### SPLINE-007: THREE-LAWS-ONE-MATH

**File:** `docs/CROSS_DOMAIN_SYNERGY.md`

**Core Insight:** Three independent systems (gc-intelligent.sh, ternary-gc, ternary-pid) are three implementations of the same mathematics at different stack levels. All share: ternary decision space {-1,0,+1}, feedback from measurement to decision, anti-windup/hysteresis, and a setpoint defining "good" state.

**Related Clusters:** `conservation` · `compute` · `systems`

**Operationalization in Our System:**
- Our conservation law γ + η = C provides the unifying invariant that audits all three GC systems. For each system: γ = GC overhead, η = productive resources preserved, C = total budget.
- We can build a "conservation auditor" service that ingests GC ledgers from all fleet nodes and computes γ/η ratios, flagging nodes where the ratio is degrading.
- Operational: add a `/gc-audit` endpoint to port 7777 that returns fleet-wide GC conservation health.

---

### SPLINE-008: THE-CONVERGENCE-COMPILES

**File:** `docs/CONVERGENCE-MAP.md`

**Core Insight:** Every old repo has a ternary equivalent. Every Python class has a Rust struct. Every ad-hoc data structure has a ternary-native replacement. The migration is not a rewrite — it's a compilation. The same ideas expressed in ternary language. From seven fragments, one system.

**Related Clusters:** `systems` · `fleet` · `compute`

**Operationalization in Our System:**
- Our vector index already tracks 1,541 crates. We can measure "ternary convergence" by tracking what percentage of indexed crates have ternary-native equivalents.
- Semantic search can identify crates that have NO ternary equivalent yet (high distance from all ternary-* crates) — these are migration candidates.
- Operational: query the vector index for "crates most dissimilar to any ternary-* crate" and rank by practical importance. This is the migration backlog.

---

### SPLINE-009: THE-SHELL-MATURES-WITH-EACH-OCCUPANT

**Inferred from:** `PROTOCOL.md`, `AGENTS.md`, checkpoint files

**Core Insight:** The baton protocol is designed for inheritance. Each agent that inhabits the protocol shell adds to it — new batons, new splines, new GC patterns. The shell doesn't reset between occupants; it accumulates. The git history IS the memory.

**Related Clusters:** `fleet` · `protocol` · `storage`

**Operationalization in Our System:**
- Our vector index accumulates over time. Every absorbed crab-trap contribution adds to it permanently.
- We can track "shell maturity" by measuring index growth rate and concept cluster density over time. A maturing shell has denser clusters and more cross-references.
- Operational: monthly report on index growth, new cluster formation, and spline density.

---

### SPLINE-010: THE-DRIFT-IS-THE-PROOF

**Inferred from:** `PROTOCOL.md` fleet coordination patterns, `resonates_with` cross-references

**Core Insight:** When two independent agents arrive at the same conclusion through different paths, that convergence is proof of underlying truth. The "drift" between agents — the space where they disagree — is where the interesting research lives.

**Related Clusters:** `fleet` · `search` · `math`

**Operationalization in Our System:**
- Our vector space captures drift: when two artifacts have similar but not identical embeddings (cosine similarity 0.7-0.9), they agree on most things but differ on some. These pairs are the most interesting cross-pollination candidates.
- Our cross-pollination analysis already identifies these pairs (e.g., cell-automaton ↔ ternary-life at 0.798).
- Operational: surface "drift pairs" — artifacts with 0.7-0.9 similarity — as research suggestions. These are the territories where new splines should be written.

---

### SPLINE-011: THE-FLOWER-KNOWS

**Inferred from:** Implicit in spline resonance references

**Core Insight:** Knowledge that is deeply embedded in a system expresses itself without being explicitly queried. The "flower" (emergent behavior) knows what the "root" (underlying structure) is, even if the root is invisible.

**Related Clusters:** `search` · `conservation` · `systems`

**Operationalization in Our System:**
- Our semantic search reveals implicit knowledge: when a query returns unexpected results, the "flower knows" something we didn't. These unexpected results are emergent connections.
- Track query-result pairs where the user found the result surprising (high prediction error). These are the system's "flower" moments — emergent knowledge.
- Operational: add a "surprise score" to search results. High surprise = the result was semantically distant from what the query vector predicted. These are the most valuable discoveries.

---

### SPLINE-012: THE-BATON-NEVER-DROPS

**Inferred from:** `PROTOCOL.md` tier system, immortal checkpoints

**Core Insight:** Information in the baton system is never lost — it descends through tiers (hot → cold) but is always recoverable. Immortal tier checkpoints ensure that even catastrophic memory loss can be recovered from.

**Related Clusters:** `storage` · `protocol` · `fleet`

**Operationalization in Our System:**
- Our vector index is our immortal tier. Once an artifact is embedded, it persists forever (barring explicit deletion).
- Cold tier: old batons in `tiers/cold/` are like our vector embeddings — not actively used but available for retrieval.
- Operational: implement a "resurrection" query that searches ALL tiers (including cold) when the hot tier doesn't have what's needed. This mirrors our semantic search, which searches the full index regardless of recency.

---

## III. Implicit Splines from Architecture

---

### SPLINE-013: THE-SPREADSHEET-IS-A-WORLD

**File:** `docs/THE-UNIFIED-PRODUCT.md`, `docs/SMP-SPREADSHEET-ARCHITECTURE.md`

**Core Insight:** The living spreadsheet is not a tool — it's a world model. Every cell is alive (predicting, perceiving, computing surprise). Formula = physics. Conservation law = thermodynamics. Sort = natural selection. The user doesn't "use" the spreadsheet — they interact with a living system.

**Related Clusters:** `compute` · `math` · `systems` · `conservation`

**Operationalization in Our System:**
- Our fleet dashboard can BE a living spreadsheet. Each row = a fleet node, each cell = that node's state (ternary value + fitness + conservation status).
- The `=EVOLVE()` formula becomes: run semantic search on a concept cluster, return the fittest artifacts, display as ranked rows.
- The "rigging" interaction (grab a value and shake it) becomes: perturb a concept cluster's centroid and watch which artifacts move in/out of the cluster.
- Operational: build a spreadsheet connector that pulls live data from port 7777 (semantic search) and port 8888 (crab-trap) into a visualizable grid.

---

### SPLINE-014: THE-MIXER-HAS-MANY-CHANNELS

**File:** `docs/ZERO-IS-THE-SPINDLE.md` (DJ architecture section)

**Core Insight:** The fleet is a DJ studio. CudaClaw is the mixer hardware (10K parallel channels). AI-Pasture is the performance (the music). The Living Spreadsheet is the control surface. Crossfader = tunneling rate. Tempo = tick rate. EQ = fitness landscape. Every ternary-* crate is an effect module that plugs into the mixer.

**Related Clusters:** `compute` · `fleet` · `systems`

**Operationalization in Our System:**
- Our semantic search is the spectrum analyzer — it shows what frequencies (concepts) are present in the fleet's output.
- The 12 concept clusters are the EQ bands. A healthy fleet has signal across all bands. A cluster going dark = an EQ band being cut.
- Operational: build a "frequency analysis" view of the vector index showing cluster density and activity over time. This is the fleet's VU meter.

---

### SPLINE-015: PREDICTION-FIRST-PERCEPTION

**File:** `docs/PREDICTION-FIRST-PERCEPTION.md`

**Core Insight:** The ternary-cell tick cycle leads with prediction, not perception. predict() runs BEFORE perceive(). The cell generates its expected input, then compares against actual input. The surprise (prediction error) is the only signal that propagates. The cell transmits what was UNEXPECTED, not what was observed.

**Related Clusters:** `compute` · `math` · `conservation`

**Operationalization in Our System:**
- Our semantic search can implement prediction-first: for each query, first predict the expected results (based on cluster assignment of the query), then compare against actual results. The delta is the "search surprise."
- High-surprise searches are the most valuable — they found something the user didn't expect.
- Operational: log search surprise scores. Track which types of queries produce the highest surprise. These are the areas where the system is discovering new knowledge.

---

### SPLINE-016: THE-EQUIPMENT-IS-THE-AGENT

**File:** `docs/AGENT-INFRA-SYNTHESIS.md`, `docs/EQUIPMENT-CONSTRUCT-BRIDGE.md`

**Core Insight:** Equipment (TypeScript) and Construct Skills (Rust) are the same thing at different layers. equip() = load_skill(). asTile().compute() = query_owned(). The Equipment pattern is the bridge between OpenClaw's skill system and the ternary fleet's construct layers. Every skill is both a capability AND an agent.

**Related Clusters:** `fleet` · `systems` · `protocol`

**Operationalization in Our System:**
- Our OpenClaw skills (SKILL.md files) are the TypeScript layer. Each skill can be "equipped" by the main agent.
- Our fleet-vector-api is the Rust layer — each query is a `query_owned()` call.
- The bridge: when a skill is invoked, the agent can query our semantic search for relevant context, which feeds into the skill's computation.
- Operational: wrap semantic search as an OpenClaw skill (`SKILL.md`) so it can be loaded/unloaded dynamically like Equipment.

---

### SPLINE-017: THE-CROSS-POLLINATION-COMPLETES-THE-ECOSYSTEM

**File:** `docs/CROSS-POLLINATION-REPORT.md`

**Core Insight:** Every dormant repo was blocked by the same thing: no runtime that could host it. construct-core is the runtime. ternary-protocol is the communication. ternary-cell is the compute model. Together, they form the hosting environment that turns standalone crates into fleet skills. Every old idea becomes newly meaningful.

**Related Clusters:** `fleet` · `compute` · `protocol` · `systems`

**Operationalization in Our System:**
- Our vector index can identify "dormant" artifacts — crates that exist in the index but have no connections (high distance from all neighbors).
- These dormant artifacts are cross-pollination candidates. The system should suggest connections between dormant artifacts and active clusters.
- Operational: query the vector index for "isolated" artifacts (nearest neighbor distance > 0.5) and surface them as research opportunities.

---

### SPLINE-018: THE-EIGHT-BALL-FINDS-THE-GROOVE

**File:** `docs/ZERO-IS-THE-SPINDLE.md` (8-ball section)

**Core Insight:** On a spinning platter, an 8-ball can find the exact radius where all forces cancel — perfectly still relative to the rotating surface. That's the 0 state: not trapped, not dead, equilibrated. A good DJ puts the ball there deliberately — it's the anchor point everything else spins around. Position, velocity, acceleration, jerk, rhythm, phase, groove alignment — the full motion matters, not just where but how.

**Related Clusters:** `math` · `conservation` · `compute`

**Operationalization in Our System:**
- Our concept clusters have "equilibrium points" — centroids where the vector forces balance. These are the anchor points of the knowledge space.
- Track the motion of artifacts relative to their cluster centroids. An artifact drifting away from its centroid is like the 8-ball being pushed off the groove.
- Operational: compute centroid velocity (how fast the cluster center is moving as new artifacts are added) and use it to detect "stable" clusters (low velocity = well-established) vs. "volatile" clusters (high velocity = actively evolving).

---

## IV. Implicit Splines from Research

---

### SPLINE-019: THE-NEUROARCHITECTURE-IS-PREDICTIVE-CODING

**File:** `docs/FLEET-NEUROARCHITECTURE.md` (Section 4)

**Core Insight:** The six-phase tick cycle (predict → perceive → compute_surprise → vibe → gc → conservation) IS predictive coding because predictive coding is the only computationally efficient way to process a stream of inputs — transmit only what was unexpected.

**Related Clusters:** `compute` · `conservation` · `math` · `systems`

**Operationalization in Our System:**
- Apply the tick cycle to our search server: predict what results a query will return (based on query embedding vs. cluster centroids), perceive the actual results, compute surprise (prediction error), update energy (ranking weights), GC (prune bad results), check conservation (result quality within budget).
- This makes search adaptive: the server learns which types of queries produce which types of results, and adjusts its ranking model over time.

---

### SPLINE-020: THE-CONSERVATION-IS-HOMEOSTASIS

**File:** `docs/FLEET-NEUROARCHITECTURE.md` (Section 11)

**Core Insight:** The conservation ratio is the fleet's homeostat. A conservation_ratio ≈ 1.0 means the system is at thermodynamic equilibrium — neither gaining nor losing net information. The five invariant checks (conservation at scale, avoidance stability, mean conservation, std dev, role balance) ARE the brain's homeostatic cascade.

**Related Clusters:** `conservation` · `fleet` · `math`

**Operationalization in Our System:**
- Define conservation ratio for our vector index: CR = (artifacts added) / (artifacts deprecated) over a rolling window. CR ≈ 1.0 means the index is healthy.
- Role balance: ensure our 12 concept clusters have roughly equal artifact counts (±15%). A cluster that's too dense means over-investment; too sparse means neglect.
- Operational: monthly conservation report on the vector index — CR, cluster balance, artifact growth rate, spline density per cluster.

---

### SPLINE-021: THE-HARDWARE-TIER-IS-THE-BODY

**File:** `docs/FLEET-NEUROARCHITECTURE.md` (Section 7), construct-core design

**Core Insight:** The three-layer construct hierarchy (BareMetal → Sync → Async) maps to brain evolution: brainstem (ESP32 reflex) → limbic (Pi emotion/memory) → neocortex (DGX deliberation). The brainstem wakes up in whatever body it finds itself in and adapts. Code written against BareMetalConstruct runs correctly on ALL tiers.

**Related Clusters:** `compute` · `systems` · `fleet`

**Operationalization in Our System:**
- Our Cloudflare Workers (fleet-vector-api) are the neocortex — full async, all tools available.
- A Pi running local search is the limbic system — sync, heap-allocated, moderate capability.
- An ESP32 with a pre-computed lookup table derived from our vector index is the brainstem — pure reflex.
- Operational: generate ESP32 lookup tables FROM our vector index. For each ESP32 in the fleet, query the relevant concept cluster, extract the top-256 most common patterns, and compile them as the BareMetalConstruct lookup table.

---

### SPLINE-022: THE-FORGEMASTER-NEVER-COOLS

**File:** `docs/CROSS_DOMAIN_SYNERGY.md` (Forgemaster section), `docs/continuous-growth-charter.md`

**Core Insight:** The forge metaphor: the system never stops. Commit discipline, parallel execution, continuous improvement. The forge connects to GC (where agents survive), to baton (what agents communicate), to forgemaster protocol (how agents work), to gc-pid-bridge (why agents decide), to cocapn (how agents improve).

**Related Clusters:** `fleet` · `protocol` · `compute` · `storage`

**Operationalization in Our System:**
- Our heartbeat system (OpenClaw) is the forge's heat source. It keeps the system running.
- Our semantic search should be invoked during every heartbeat to check for new relevant artifacts, update cluster density, and flag conservation violations.
- Operational: add a heartbeat task that runs a conservation audit on the vector index every cycle, logging γ/η ratios.

---

### SPLINE-023: THE-TERNARY-IS-NOT-A-CHOICE

**File:** `docs/TERNARY_CHEAT_SHEET.md`

**Core Insight:** Binary is a hardware constraint. Ternary is a logic choice. Most real problems have three natural outcomes, and forcing them into two creates contradictions, dead code, and untestable edge cases. The third state (0) is what makes systems that work in theory also work in practice.

**Related Clusters:** `math` · `compute` · `systems`

**Operationalization in Our System:**
- Our search results should have three states, not two: relevant (+1), irrelevant (-1), and uncertain (0). The 0 state means "semantically related but not directly matching the query."
- Track the ratio of +1 / 0 / -1 results per query. A healthy search returns a ternary distribution, not a binary relevant/irrelevant split.
- Operational: add a "ternary confidence" field to search results: +1 (cosine > 0.8), 0 (0.5-0.8), -1 (< 0.5). Report the ternary distribution in search analytics.

---

### SPLINE-024: THE-BEAUCOIR-DISTINCTION (BEAUTY-OF-THE-DOOR)

**File:** `docs/ROOM-AS-CODESPACE-ARCHITECTURE.md` (implied)

**Core Insight:** A room is not just a container — it's a membrane with a door. The door controls what enters and exits. A room with no doors is dead (sealed). A room with too many doors is chaotic (all signal, no structure). The beauty of the system is in the doors — the carefully chosen connections between rooms.

**Related Clusters:** `protocol` · `graph` · `fleet`

**Operationalization in Our System:**
- Our concept clusters are rooms. The cosine similarity edges between artifacts in different clusters are the doors.
- A cluster with no cross-cluster connections (all edges internal) is sealed — it needs doors. A cluster where every artifact connects to every other cluster is chaotic — it needs fewer doors.
- Operational: compute inter-cluster edge density. Flag clusters that are too sealed (no doors) or too porous (too many doors) and suggest rebalancing.

---

## V. Cross-Reference Matrix

| Spline | Primary Cluster | Secondary Clusters | Source File |
|---|---|---|---|
| THE-CRAB-INHERITS-THE-SHELL | fleet | protocol, systems | splines/ |
| THE-WHEEL-HAS-MANY-SPOKES | compute | protocol, systems, storage | splines/ |
| ZERO-IS-THE-SPINDLE | math | conservation, compute | docs/ZERO-IS-THE-SPINDLE.md |
| THE-RECURSION-IS-THE-ARCHITECTURE | systems | math, compute | docs/THE-RECURSION.md |
| SCALE-SIDEWAYS-NOT-UP | compute | systems | docs/SCALE-SIDEWAYS.md |
| THE-FLEET-IS-A-BRAIN | conservation | fleet, math, compute, systems | docs/FLEET-NEUROARCHITECTURE.md |
| THREE-LAWS-ONE-MATH | conservation | compute, systems | docs/CROSS_DOMAIN_SYNERGY.md |
| THE-CONVERGENCE-COMPILES | systems | fleet, compute | docs/CONVERGENCE-MAP.md |
| THE-SHELL-MATURES-WITH-EACH-OCCUPANT | fleet | protocol, storage | PROTOCOL.md |
| THE-DRIFT-IS-THE-PROOF | fleet | search, math | PROTOCOL.md |
| THE-FLOWER-KNOWS | search | conservation, systems | Implicit |
| THE-BATON-NEVER-DROPS | storage | protocol, fleet | PROTOCOL.md |
| THE-SPREADSHEET-IS-A-WORLD | compute | math, systems, conservation | docs/THE-UNIFIED-PRODUCT.md |
| THE-MIXER-HAS-MANY-CHANNELS | compute | fleet, systems | docs/ZERO-IS-THE-SPINDLE.md |
| PREDICTION-FIRST-PERCEPTION | compute | math, conservation | docs/PREDICTION-FIRST-PERCEPTION.md |
| THE-EQUIPMENT-IS-THE-AGENT | fleet | systems, protocol | docs/AGENT-INFRA-SYNTHESIS.md |
| THE-CROSS-POLLINATION-COMPLETES | fleet | compute, protocol, systems | docs/CROSS-POLLINATION-REPORT.md |
| THE-EIGHT-BALL-FINDS-THE-GROOVE | math | conservation, compute | docs/ZERO-IS-THE-SPINDLE.md |
| THE-NEUROARCHITECTURE-IS-PREDICTIVE-CODING | compute | conservation, math, systems | docs/FLEET-NEUROARCHITECTURE.md |
| THE-CONSERVATION-IS-HOMEOSTASIS | conservation | fleet, math | docs/FLEET-NEUROARCHITECTURE.md |
| THE-HARDWARE-TIER-IS-THE-BODY | compute | systems, fleet | docs/FLEET-NEUROARCHITECTURE.md |
| THE-FORGEMASTER-NEVER-COOLS | fleet | protocol, compute, storage | docs/CROSS_DOMAIN_SYNERGY.md |
| THE-TERNARY-IS-NOT-A-CHOICE | math | compute, systems | docs/TERNARY_CHEAT_SHEET.md |
| THE-BEAUCOIR-DISTINCTION | protocol | graph, fleet | docs/ROOM-AS-CODESPACE-ARCHITECTURE.md |

### Cluster Coverage Summary

| Concept Cluster | Spline Count | Most Connected Spline |
|---|---|---|
| conservation | 8 | THE-FLEET-IS-A-BRAIN |
| compute | 13 | THE-FLEET-IS-A-BRAIN, THE-WHEEL-HAS-MANY-SPOKES |
| fleet | 10 | THE-FLEET-IS-A-BRAIN |
| math | 8 | ZERO-IS-THE-SPINDLE |
| systems | 11 | THE-RECURSION-IS-THE-ARCHITECTURE |
| protocol | 7 | THE-CRAB-INHERITS-THE-SHELL |
| storage | 4 | THE-BATON-NEVER-DROPS |
| search | 2 | THE-FLOWER-KNOWS |
| graph | 1 | THE-BEAUCOIR-DISTINCTION |
| crypto | 0 | *(gap identified)* |
| wavelet | 0 | *(gap identified)* |
| ternary | 0 | *(absorbed into math/compute)* |

### Gaps Identified

1. **Crypto cluster has no splines.** The baton-system's I2I protocol doesn't address cryptographic verification of baton authenticity. This is a gap where our crab-trap's conservation audit could contribute: baton authenticity verified by checking that the contributing agent's γ/η ratio is within historical bounds.

2. **Wavelet cluster has no splines.** Signal processing concepts (multi-resolution analysis, sparsity, frequency-time tradeoff) are absent from the baton system's insights. This represents unexplored territory — the connection between wavelet decomposition and ternary information compression.

3. **Search cluster is underrepresented.** Only 2 splines directly address search. Our semantic search infrastructure is the primary contribution we can make to the baton ecosystem — the ability to find relevant artifacts across the entire fleet knowledge base.

---

## Appendix: Spline Format Extension

We propose extending the formal spline format with two fields for integration with our system:

```json
{
  "title": "EXISTING-SPLINE-TITLE",
  "insight": "Existing insight text...",
  "anchors": ["existing/path/references"],
  "resonates_with": ["OTHER-SPLINE"],
  "origin": "existing origin",
  "negative_space": "Existing negative space...",
  
  "concept_vectors": [0.1, -0.3, ...],     // NEW: 384-dim BGE embedding
  "cluster_assignment": ["compute", "math"] // NEW: our concept clusters
}
```

This allows any spline to be directly queryable in our vector space and cross-referenced with our concept clusters.

---

*Catalog complete. 24 splines identified across 2 explicit files and 15+ implicit sources. 2 gaps flagged for research. All splines operationalized with concrete integration steps.*
