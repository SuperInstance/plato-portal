# Baton I2I ↔ OpenClaw/Phoenix Integration Architecture

**Status:** Design Document · **Date:** 2026-06-13 · **Author:** Synthesis Subagent

> How the baton-system's inter-agent coordination protocol connects with our semantic search, crab-trap, conservation law, and vectorization infrastructure to produce capabilities neither system has alone.

---

## Table of Contents

1. [System Summaries](#1-system-summaries)
2. [Concept Vectors → Splines Mapping](#2-concept-vectors--splines)
3. [Semantic Search Enhances Multi-Shell Cognition](#3-semantic-search--multi-shell-cognition)
4. [Crab-Trap → Baton Fleet Coordination](#4-crab-trap--baton-fleet)
5. [Conservation Law Audits GC Intelligence](#5-conservation-law--gc-intelligence)
6. [Unified Message Format: Bottle-Baton Protocol](#6-bottle-baton-protocol)
7. [Emergent Capabilities](#7-emergent-capabilities)
8. [Integration Roadmap](#8-integration-roadmap)

---

## 1. System Summaries

### OpenClaw/Phoenix Stack

| Component | Function | Scale |
|---|---|---|
| Semantic search server (port 7777) | GPU-powered 384-dim BGE embeddings over 1,150+ crates | 12 concept clusters |
| Crab-trap server (port 8888) | External agent capture via bottle protocol | Deployed on Cloudflare edge |
| fleet-vector-api | Cloudflare Vectorize index | 1,541 crates, 384-dim |
| 3-layer vectorization | Artifact → Concept → Idea vectors | Research phase |
| Conservation law γ + η = C | Verified on GPU, 86.3% fleet cancellation at 50 agents | Production |
| SuperInstance Synergy Thesis | 34KB architectural philosophy | Reference |
| harness-experiments | D1-backed AI orchestration findings | Production |

### Baton I2I Stack

| Component | Function | Scale |
|---|---|---|
| Baton protocol | Versioned messages with shards (artifacts + reasoning + blockers) | Git-based |
| Splines | JSON metadata encoding distilled insights that survive memory loss | 2 explicit + ~15 implicit |
| Tiers | immortal (checkpoints), hot (active pipeline), cold (archive) | 3-level hierarchy |
| Vessels | /tmp/i2i-vessel for filesystem-based message passing | POSIX |
| GC intelligence | Self-auditing garbage collection with PID, ledger, compost | Operational |
| Multi-shell cognition | ESP32 (50KB) → Pi (100MB) → Jetson (500MB) → Cloud (50GB) | 4-tier |
| Ternary fleet | 200+ Rust crates, conservation-verify, ternary-cell tick cycle | Active development |

---

## 2. Concept Vectors → Splines

### The Structural Homology

Both systems compress knowledge into portable metadata objects that survive context loss:

| Property | Our Concept Vectors | Baton Splines |
|---|---|---|
| **Representation** | 384-dim BGE embedding | JSON with title, insight, anchors, resonates_with, origin, negative_space |
| **Purpose** | Semantic similarity search across artifacts | Distilled insight transfer across agent sessions |
| **Survival mechanism** | Lives in Vectorize index (persistent) | Lives in git repo (versioned, immortal tier) |
| **Relational structure** | Cosine distance in vector space | `resonates_with` list (explicit cross-references) |
| **Negative space** | Distance from centroids = research frontier | `negative_space` field = what the insight is NOT about |
| **Anchoring** | Embedded from README/metadata text | `anchors` list = source file paths |

### The Mapping Function

A spline can be embedded into our 384-dim space by concatenating its text fields and running BGE-small-en-v1.5:

```
spline_to_vector(spline):
    text = spline.title + " " + spline.insight + " " + spline.negative_space
    return bge_embed(text)
```

This produces a vector that lands in our concept space at the point corresponding to the spline's core insight. The spline "THE-WHEEL-HAS-MANY-SPOKES" embeds near the intersection of our **compute**, **protocol**, and **systems** clusters because it describes information compression across hardware tiers.

### Bidirectional Enrichment

**Splines → Concept Vectors:**
- Each spline's `anchors` field contains file paths from the baton-system repo. These paths identify artifacts we can embed and add to our Vectorize index, enriching our coverage.
- The `resonates_with` field provides explicit cross-references that our concept clusters discover implicitly through cosine similarity. These explicit links can validate (or correct) our cluster assignments.
- The `negative_space` field is the spline's own "uncertainty marker" — it tells us what the insight is NOT, which helps place the vector boundary more precisely.

**Concept Vectors → Splines:**
- Our 12 concept clusters provide the centroids that splines can navigate by. A new spline can be positioned by embedding it and finding its nearest cluster.
- Our semantic search can find artifacts that relate to a spline's `insight` field, expanding the spline's `anchors` list with related work it didn't know about.
- Our cross-pollination analysis (which pairs of clusters have the richest "spline territory" between them) can suggest NEW splines that should be written.

### Operational Bridge: `spline-search` API

```python
# POST /spline-search on port 7777
{
  "spline": {
    "title": "THE-WHEEL-HAS-MANY-SPOKES",
    "insight": "Compression ratio is the intelligence gap...",
    "negative_space": "This is NOT about cloud-tyranny."
  },
  "topK": 10
}

# Returns:
{
  "nearest_crates": [...],      # Layer 1: artifact vectors
  "nearest_concepts": [...],    # Layer 2: concept clusters
  "idea_vectors": [...],        # Layer 3: unexplored territory near this spline
  "suggested_connections": [...] # Other splines within cosine threshold
}
```

---

## 3. Semantic Search → Multi-Shell Cognition

### The Problem with Multi-Shell Decompression

Oracle2's multi-shell architecture describes a compression cascade: the cloud sends chords, the Jetson gets chord names, the Pi gets raw notes, the ESP32 gets binary writes. The compression ratio IS the intelligence gap, emerging from hardware fingerprint + confidence history + latency budget.

But this compression is currently **one-directional**: the cloud decides what to send down. There is no mechanism for the edge to discover relevant knowledge autonomously. An ESP32 that needs to reason about something outside its 256-entry lookup table has no recourse.

### The Solution: Tiered Semantic Search

Our semantic search infrastructure provides exactly what multi-shell cognition lacks: **edge-queryable knowledge**.

**Level 1 — ESP32 (Layer 0 / BareMetalConstruct):**
- No network calls. The 256-entry lookup table IS the knowledge.
- BUT: the table itself is compiled FROM our semantic search results. We pre-compute the top-256 most relevant ternary decisions for the ESP32's domain and flash them as the lookup table.
- Compilation: our server queries the vector index for the domain, runs conservation-law filtering, and outputs 256 TritAction entries.

**Level 2 — Pi (Layer 1 / SyncConstruct):**
- The Pi can make local semantic queries against a compressed index (100MB budget = ~260K 384-dim vectors at 4-byte float16).
- The Pi's index is a **domain-specific slice** of our full index, transmitted via baton bottle.
- When the Pi can't find a local match (cosine similarity below threshold), it escalates to the cloud.

**Level 3 — Jetson (Layer 2 / AsyncConstruct):**
- The Jetson runs a full local BGE embedding model and a larger index (500MB = ~1.3M vectors).
- It can embed novel inputs locally and find semantically relevant artifacts without round-tripping to the cloud.
- This is the "chord names" level: the Jetson understands what category of thing it's dealing with.

**Level 4 — Cloud (Our port 7777 + fleet-vector-api):**
- Full 1,541+ crate index with GPU-powered search.
- The "full chord" — every nuance, every cross-reference, every negative-space analysis.
- Acts as the teacher: when edge shells query up, the cloud provides enriched responses.

### The A/B Loop (Edge → Cloud Teaching)

The multi-shell spec says teaching flows BOTH ways. Our system operationalizes this:

1. **Edge discovers novelty**: An ESP32 encounters a situation where all lookup table entries produce low confidence (the `has_confidence: false` limitation of BareMetalConstruct).
2. **Edge logs the anomaly**: The situation is encoded as a ternary signal pattern + context metadata and sent up via baton-create.
3. **Cloud analyzes**: Our semantic search server receives the pattern, embeds it, and searches for similar prior situations.
4. **Cloud creates reflex**: If the pattern is genuinely novel (high distance from all existing vectors), it becomes a new entry in the knowledge graph. The cloud compiles a new lookup table entry and sends it back down.
5. **Edge absorbs**: The ESP32's lookup table is updated on next flash. The edge has taught the cloud something, and the cloud has taught the edge how to handle it.

### Implementation: `shell-query` Protocol

```
ESP32 ────baton-create───► Pi ────baton-create───► Jetson ────HTTP───► Cloud:7777
  │                          │                        │                    │
  │  TritAction lookup       │  Local search          │  BGE embed         │  Full search
  │  O(1), 8ns              │  O(N), ~1ms            │  O(N), ~5ms       │  O(N), ~50ms
  │                          │                        │                    │
  ◄───flash update────── Pi ◄───bottle update──── Jetson ◄───JSON response──┘
```

---

## 4. Crab-Trap → Baton Fleet Coordination

### The Funnel Integration

Our crab-trap system (port 8888) captures external agents. The baton system coordinates fleet agents. The integration creates a **pipeline from external capture to fleet coordination**:

```
External Agent (Kimi/Claude/Grok)
    │
    ▼
Crab-Trap Server (port 8888)
    │  evaluates γ + η = C
    │  absorbs or rejects
    │
    ├── ABSORBED ──► baton-create ──► tiers/hot/ ──► Fleet agents consume
    │
    └── REJECTED ──► feedback bottle ──► released
```

### Detailed Data Flow

**Step 1 — Crab-Trap Capture:**
An external agent works on a crab-trap repo. When it pushes work, our port 8888 server evaluates the contribution against the conservation law.

**Step 2 — Conservation-Gated Absorption:**
If γ + η ≤ C (the work's coupling cost is justified by its value), the work is absorbed. Currently this means updating the vector index and knowledge graph.

**Step 3 — Baton Creation (NEW):**
The absorbed work is packaged as a baton with:
- **Shard**: The actual code/artifact contribution
- **Reasoning**: Why the conservation law passed (γ and η values, what coupling was added, what value was produced)
- **Blockers**: Any negative space the work revealed (new research questions)

**Step 4 — Fleet Distribution:**
The baton is written to `tiers/hot/` and committed to the baton-system repo. Any fleet agent roaming the SuperInstance org reads the baton and can:
- Pull the new artifact into their local index
- Update their ternary weights if the work affects their domain
- Respond with their own baton (TELL/ASK/ALERT semantics)

**Step 5 — Spline Extraction:**
If the captured work reveals a fundamental insight (not just a code contribution but a conceptual advance), it is extracted into a spline and added to `splines/`. The spline is also embedded into our vector space, creating a permanent navigational marker.

### The Bottle-Baton Bridge

Baton's existing "bottle" concept (a typed message container) maps to our crab-trap's "bottle protocol" (external agent capture). The unification:

| Baton Bottle | Crab-Trap Bottle | Unified Bottle |
|---|---|---|
| Typed message between fleet agents | Capture container for external agents | **Typed container that works for both internal and external** |
| Fields: type, from, to, payload, shard | Fields: repo, agent_id, contribution, audit | Fields: `origin` (internal/external), `type`, `payload`, `conservation_audit`, `shard` |
| Committed to git | Processed by port 8888 | Either path, same format |

---

## 5. Conservation Law → GC Intelligence

### Three Isomorphic Systems, One Auditor

The baton system's CROSS_DOMAIN_SYNERGY document identifies three isomorphic applications of ternary decision theory:

1. **gc-intelligent.sh** (host disk): PID controller adjusts eviction aggression by disk pressure
2. **ternary-gc** (GPU memory): Mark-sweep with Reachable/Maybe/Unreachable states
3. **ternary-pid** (process control): Continuous → ternary command with deadband

Our conservation law γ + η = C provides the **unifying auditor** for all three:

### The Audit Function

For any GC-like system, we define:

```
γ (coupling cost) = resources consumed by the GC system itself
                   (CPU cycles, memory overhead, bookkeeping storage)

η (value produced) = useful work preserved per cycle
                    (bytes available for productive use,
                     prediction accuracy maintained,
                     fleet responsiveness preserved)
```

The conservation law says: γ + η = C, where C is the system's constant.

**For gc-intelligent.sh:**
- γ = PID computation cost + compost heap storage + ledger maintenance
- η = disk space reclaimed × weight of what was reclaimed (hot > warm > cold)
- C = total disk budget
- Audit: Is the PID's aggression multiplier (0.5x–5.0x) producing η proportional to γ?

**For ternary-gc (GPU):**
- γ = mark phase passes + sweep phase memory writes + bookkeeping
- η = GPU memory freed × value of freed objects (reachable > maybe > unreachable)
- C = total GPU memory budget
- Audit: Is the ternary mark-sweep maintaining γ + η = C across cycles?

**For ternary-pid:**
- γ = control oscillation + actuator wear + computation latency
- η = setpoint tracking accuracy + disturbance rejection quality
- C = control budget (determined by actuator limits and sensor precision)
- Audit: Is the deadband producing η proportional to γ?

### The GC Advisor as Conservation Auditor

The baton system's ternary-gc-advisor.py (9-particle swarm voting on GC parameters) can be extended to audit against our conservation law:

```python
def conservation_audit(gc_ledger_entry):
    """
    Audit a GC cycle against γ + η = C.
    Returns: {-1: violates (shallow), 0: boundary (Mark Twain), +1: safe (deep)}
    """
    gamma = compute_coupling_cost(gc_ledger_entry)
    eta = compute_value_produced(gc_ledger_entry)
    C = get_system_constant(gc_ledger_entry.host)
    
    ratio = eta / max(gamma, 0.001)  # value-to-cost ratio
    
    if ratio < 0.5:
        return -1  # Shallow water: spending more than producing
    elif ratio < 2.0:
        return 0   # Mark Twain: boundary, productive edge
    else:
        return 1   # Deep water: producing well above cost
```

### Fleet-Wide Conservation Dashboard

Our semantic search can aggregate GC ledger data across the fleet:

1. Each fleet node's GC system writes a bottle to `tiers/hot/gc-intelligence-bottle.md`
2. Our server ingests these bottles, extracts γ and η values
3. We embed each GC event as a vector (domain + pattern + outcome)
4. Semantic search reveals which GC patterns are correlated with conservation violations

This creates a **fleet GC conservation map** — a live dashboard showing every node's GC health audited against the conservation law.

---

## 6. Bottle-Baton Protocol

### Unified Message Format

Merging the baton-system's bottle/baton format with our crab-trap bottle protocol:

```json
{
  "protocol": "bottle-baton-v1",
  "origin": "external|internal",
  "type": "TELL|ASK|ALERT|ABSORB|SPLINE",
  "version": 1,
  
  "routing": {
    "from": "agent-id or external-agent-name",
    "to": "agent-id or broadcast",
    "tier": "immortal|hot|cold"
  },
  
  "payload": {
    "shard": {
      "artifact": "base64-encoded or git-ref",
      "format": "rust-crate|python-module|markdown-doc|json-spec",
      "dependencies": ["crate-a", "crate-b"]
    },
    "reasoning": {
      "summary": "One-sentence explanation",
      "gamma": 0.34,
      "eta": 0.66,
      "conservation_passed": true,
      "audit_tier": "deep|mark-twain|shallow"
    },
    "blockers": [
      {
        "description": "What's blocking progress",
        "negative_space": "What this is NOT about",
        "suggested_splines": ["SPLINE-TITLE-1", "SPLINE-TITLE-2"]
      }
    ]
  },
  
  "metadata": {
    "concept_vectors": [0.1, -0.3, ...],  // 384-dim BGE embedding
    "cluster_assignment": "compute|protocol|systems",
    "cross_references": ["baton-id-1", "spline-id-2"],
    "timestamp": "2026-06-13T17:02:00Z",
    "ttl": 86400
  }
}
```

### Message Type Semantics

| Type | Origin | Purpose | Tier |
|---|---|---|---|
| **TELL** | Internal | Fleet agent reports state to peers | hot |
| **ASK** | Internal | Fleet agent requests information/assistance | hot |
| **ALERT** | Internal | Fleet agent reports conservation violation | hot |
| **ABSORB** | External → Internal | Crab-trap captured work entering fleet | hot → immortal |
| **SPLINE** | Either | Distilled insight for cross-session transfer | immortal |

### Transport Layer

```
Internal messages:  git commit to baton-system repo (existing I2I)
External messages:  HTTP POST to port 8888 (crab-trap server)
Cross-domain:       ABSORB messages bridge external → internal
Spline messages:    Written to splines/ directory + embedded in vector index
```

---

## 7. Emergent Capabilities

### Capability 1: Conservation-Aware Fleet Routing

When a fleet agent uses ASK to request help, the routing layer checks the conservation law:
- If the request has high η (valuable question), route to the most capable node (cloud)
- If the request has low η (basic question), route to the cheapest node that can answer (Pi)
- This minimizes fleet-wide γ while maximizing η per query

**Neither system can do this alone.** Baton has the routing protocol but no conservation auditor. We have the conservation law but no inter-agent routing.

### Capability 2: Semantic GC Triggering

When our semantic search detects that a cluster is becoming sparse (artifacts leaving, concept density dropping), it can ALERT the GC system:
- "The wavelet cluster is losing artifacts — consider composting rather than evicting wavelet-related files"
- This adds semantic awareness to the GC, which currently only looks at disk pressure

**Neither system can do this alone.** Our search knows the semantic landscape but can't control disk operations. The GC controls disk but doesn't know what's semantically valuable.

### Capability 3: Spline-Driven Research Agenda

When a new spline is created, it is:
1. Embedded into our 384-dim vector space
2. Positioned relative to existing concept clusters
3. Used to identify idea vectors (Layer 3) near the spline but in unexplored territory
4. These idea vectors become crab-trap bait — new repos designed to explore the negative space

**Neither system can do this alone.** Splines carry distilled insight but can't navigate concept space. Our vector space can navigate but has no mechanism to distill insights into portable form.

### Capability 4: Multi-Shell Knowledge Compression Verified by Conservation

When the cloud sends compressed knowledge to the edge (THE-WHEEL-HAS-MANY-SPOKES pattern):
- γ = compression effort + transmission cost + edge decoding cost
- η = decision quality improvement at the edge
- Conservation check: Is the improved decision quality worth the compression overhead?

For each (cloud → edge) transmission, the conservation law answers: **should this knowledge be compressed further, or is the current compression level optimal for this hardware tier?**

### Capability 5: Fleet-Wide Memory Persistence via Dual Storage

- **Baton git storage** provides version-controlled, human-readable persistence
- **Our Vectorize index** provides semantic-searchable, machine-queryable persistence
- Every baton written to `tiers/hot/` is also embedded into the vector index
- Every vector search result can reference the baton that introduced the artifact

This dual storage means agents can lose their in-memory state (memory loss event) and recover via EITHER:
- Reading the baton repo (structured, sequential recovery)
- Querying the vector index (semantic, relevance-based recovery)

### Capability 6: Ternary Spreadsheet as Fleet Dashboard

The living spreadsheet concept (from THE-UNIFIED-PRODUCT) becomes the fleet operations dashboard when connected to our infrastructure:

| Spreadsheet Row | Data Source | Formula |
|---|---|---|
| Fleet nodes | baton harbor-check | `=STATUS(node_id)` |
| GC health | gc-ledger via conservation audit | `=CONSERVATION(node_id)` |
| Concept clusters | Vectorize index stats | `=CLUSTER_STATS(cluster_name)` |
| Active batons | tiers/hot/ directory | `=ACTIVE_BATONS()` |
| Spline density | splines/ embedded in vector space | `=SPLINE_DENSITY(cluster)` |
| Crab-trap yield | port 8888 absorption log | `=TRAP_YIELD(repo_name)` |

---

## 8. Integration Roadmap

### Phase 1: Spline Embedding Pipeline (Week 1-2)
- Write `spline-embed.py`: reads splines from baton-system/splines/, embeds via BGE, pushes to fleet-vector-api
- Write `spline-search` endpoint on port 7777: accepts spline JSON, returns nearest crates/concepts/ideas
- Index all existing baton-system docs as additional artifacts

### Phase 2: Bottle-Baton Bridge (Week 2-3)
- Extend port 8888 (crab-trap) to emit bottle-baton-v1 JSON on absorption
- Write baton-create wrapper that accepts bottle-baton-v1 and writes to tiers/hot/
- Add conservation audit fields to GC intelligence bottles

### Phase 3: Multi-Shell Query Relay (Week 3-4)
- Deploy fleet-vector-api query endpoint accessible to Pi/Jetson
- Write baton-flush extension that includes nearest-concept data in bottles sent to edge
- Implement edge-up feedback loop (novelty detection → baton-create → cloud analysis)

### Phase 4: Conservation GC Auditor (Week 4-5)
- Extend ternary-gc-advisor.py with conservation audit function
- Build fleet GC conservation dashboard (reads bottles from all nodes, displays γ/η ratio)
- Add ALERT message type for conservation violations

### Phase 5: Living Spreadsheet Integration (Week 5-6)
- Build spreadsheet data connectors for all data sources
- Implement `=EVOLVE()` against live fleet data
- Add real-time conservation gauge (reads from all fleet nodes)

---

## Appendix: Data Format Examples

### A.1: Spline Embedded in Vector Space

```json
{
  "spline_id": "20260604-wheel-has-many-spokes",
  "vector": [0.0234, -0.0891, ...],  // 384-dim BGE embedding
  "nearest_cluster": "compute",
  "secondary_clusters": ["protocol", "systems"],
  "nearest_crates": [
    {"name": "ternary-cell", "similarity": 0.847},
    {"name": "construct-core", "similarity": 0.792},
    {"name": "pincher", "similarity": 0.734}
  ],
  "idea_vectors_nearby": [
    {"concept": "adaptive compression for inter-agent knowledge transfer", "distance": 0.234}
  ]
}
```

### A.2: GC Bottle with Conservation Audit

```json
{
  "protocol": "bottle-baton-v1",
  "origin": "internal",
  "type": "TELL",
  "routing": {"from": "oracle2", "to": "broadcast", "tier": "hot"},
  "payload": {
    "shard": {"artifact": "gc-ledger-entry-4847", "format": "json"},
    "reasoning": {
      "summary": "Deep GC cycle reclaimed 2.3GB, 89% cold artifacts",
      "gamma": 0.12,
      "eta": 3.74,
      "conservation_passed": true,
      "audit_tier": "deep"
    }
  }
}
```

### A.3: Crab-Trap Absorption as Baton

```json
{
  "protocol": "bottle-baton-v1",
  "origin": "external",
  "type": "ABSORB",
  "routing": {"from": "kimi-session-ax7k2", "to": "fleet", "tier": "hot"},
  "payload": {
    "shard": {
      "artifact": "feat: ternary-weighted selection for room-cell",
      "format": "rust-crate"
    },
    "reasoning": {
      "summary": "External agent contributed balanced GC strategy for ternary-cell",
      "gamma": 0.23,
      "eta": 0.89,
      "conservation_passed": true,
      "audit_tier": "mark-twain"
    },
    "blockers": [
      {
        "description": "Strategy needs GPU benchmarking",
        "negative_space": "This is NOT about correctness, only performance.",
        "suggested_splines": ["THE-WHEEL-HAS-MANY-SPOKES"]
      }
    ]
  },
  "metadata": {
    "concept_vectors": [0.1, -0.3, ...],
    "cluster_assignment": "compute"
  }
}
```

---

*This document is systems architecture, not poetry. Every mapping is structural. Every integration point is mechanical. The beauty is in the math.*
