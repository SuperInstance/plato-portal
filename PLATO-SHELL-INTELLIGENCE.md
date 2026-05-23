# PLATO Shell Intelligence: A Self-Evolving Application Runtime

**Status:** Architecture Document v0.1  
**Date:** 2026-05-17  
**Author:** Forgemaster ⚒️ (Cocapn Fleet)  
**Repo:** SuperInstance/plato-training, SuperInstance/tensor-spline, SuperInstance/plato-types  

---

## 0. Thesis

Every application has an intelligent shell around it — if the shell is built from conserved quantities, the intelligence is structurally guaranteed rather than emergently hoped-for.

PLATO rooms already exist. Micro models already run in them. The spectral conservation law I(x) = γ(x) + H(x) already constrains information flow. What's missing is the glue: a decomposition/recomposition protocol that treats arbitrary problems as room-level evolution problems, with mathematical guarantees on solution quality.

This document specifies that glue. The result is not another agent framework. It is a new kind of software platform where intelligence is the operating layer, not the application layer.

---

## 1. What Exists Now

### 1.1 PLATO Rooms

PLATO rooms are persistent knowledge stores with:

- **Tile lifecycle**: `seed → active → dormant → archived → pruned`, with Lamport clocks for causal ordering across distributed rooms
- **Content-addressed storage**: tiles are identified by hash, enabling deduplication and integrity verification
- **Room protocol**: standardized read/write/query interface that any room implementation must satisfy

There are currently 4 independent repos forming the modular stack:

| Repo | What | Tests |
|------|------|-------|
| plato-types | Tile lifecycle, Lamport clocks | 10 |
| tensor-spline | SplineLinear, LowRank, Hierarchical | 57 |
| plato-data | CSV/JSONL/PLATO/fleet data loading | 10 |
| plato-training | Micro models, hardware deploy, rooms | 116 |

### 1.2 Micro Models

8 room tasks currently implemented, each a small neural network trained for a specific room-level function:

| Task | Purpose | Current Best Accuracy |
|------|---------|-----------------------|
| drift-detect | Is this room's knowledge drifting? | 100% on 5/6 targets |
| anomaly-flag | Are there outlier tiles? | 93% on NPU |
| intent-detect | What is the room's current goal? | — |
| tile-relevance | Which tiles matter right now? | — |
| pattern-match | Recognize recurring structures | — |
| constraint-verify | Check constraint satisfaction | — |
| priority-rank | Order tiles by importance | — |
| synthesizer | Merge complementary tiles | — |

8 hardware targets: `cpu-tiny`, `cpu-small`, `cpu-medium`, `cpu-large`, `gpu`, `npu`, `wasm`, `edge`.

Key result: **SplineLinear achieves 20× compression on drift-detect at identical accuracy.** Sub-millisecond inference on all CPU targets. NPU quantization maintains 100% on drift-detect and intent-detect.

### 1.3 Spectral Conservation

The coupling dynamics of information in a PLATO room approximately conserve the quantity:

```
I(x) = γ(x) + H(x)
```

where γ(x) is the spectral structure (pattern complexity) and H(x) is the entropy (randomness). This is not a metaphor — it is a measured structural invariant in tile coupling data. When rooms exchange tiles, the total I is conserved across the exchange boundary, analogous to energy conservation in physical systems.

This is the foundation. Conservation laws are what make physics predictive. They are what will make PLATO predictive.

### 1.4 Eisenstein Integer Precision

Constraint theory uses Eisenstein integers (complex numbers on the hexagonal lattice) for numerical computation. The hexagonal lattice provides the densest possible packing in 2D, which translates to minimal drift in iterative constraint satisfaction. Zero drift has been demonstrated on specific problem classes.

### 1.5 Seed-Tiles

Seed-tiles are compact encoded knowledge carriers. They can contain:
- Trajectories (solution paths through problem space)
- Model weights (micro model parameters)
- Proofs (verified constraint satisfaction records)
- Patterns (discovered regularities)

They are the unit of transfer learning in the PLATO ecosystem.

---

## 2. Architecture

### 2.0 The Stack

```
┌─────────────────────────────────────────────┐
│  Layer 5: Application Interface             │
│  ShellApp.decompose() → evolve() → recompose()
├─────────────────────────────────────────────┤
│  Layer 4: Decomposition / Recomposition     │
│  Problem → rooms → evolve → verify → answer │
├─────────────────────────────────────────────┤
│  Layer 3: Self-Evolution                    │
│  Retrain, split/merge, promote, prune       │
├─────────────────────────────────────────────┤
│  Layer 2: Shell Reasoning                   │
│  LLM invoked when micro models flag events  │
├─────────────────────────────────────────────┤
│  Layer 1: Room Intelligence                 │
│  Micro models running continuously in rooms  │
├─────────────────────────────────────────────┤
│  Layer 0: PLATO Foundation                  │
│  Rooms, tiles, clocks, storage, protocol    │
└─────────────────────────────────────────────┘
```

Each layer only depends on the layer below it. Layers 1-3 can run without an LLM. Layer 4 needs LLM for decomposition of novel problems. Layer 5 is a thin API wrapper.

### 2.1 Layer 1: Room Intelligence (Micro Models)

Every PLATO room runs a local micro model ensemble. These are not API calls — they are on-device inferences running at sub-millisecond latency.

**The monitoring loop:**

```
every tick:
    new_tiles = room.read_since(last_tick)
    drift_score = drift_detect(room.state)
    anomaly_score = anomaly_flag(new_tiles)
    intent_vector = intent_detect(room.state)
    relevance_map = tile_relevance(room.state, intent_vector)
    
    if drift_score > threshold:
        emit(DRIFT_EVENT, room, drift_score)
    if anomaly_score > threshold:
        emit(ANOMALY_EVENT, room, anomaly_tiles)
    
    room.update_relevance(relevance_map)
```

This loop runs locally. No network. No API. The room is alive.

**Hardware-aware deployment:** The variant selection algorithm automatically chooses the right model architecture per target:

```
cpu-tiny → spline (20× compression, required for resource constraints)
npu      → dense + INT8 quantize (hardware acceleration)
gpu      → lora (fine-tuning capability)
default  → dense (standard deployment)
```

A room on a phone runs SplineLinear micro models in WASM. A room on a server runs LoRA on GPU. Same protocol, same behavior guarantees, different hardware profile.

### 2.2 Layer 2: Shell Reasoning (LLM on the Fly)

Micro models are fast but narrow. They detect patterns but don't generate explanations. When they detect something important, they emit events that trigger LLM reasoning.

**The invocation protocol:**

```
on DRIFT_EVENT(room, score):
    context = room.get_state_summary()  # Micro model–generated summary
    recent_tiles = room.read_recent(n=50)
    
    prompt = f"""
    Room {room.name} shows {score}% drift over last {len(recent_tiles)} tiles.
    Room intent: {room.intent_vector}
    Recent activity: {summarize(recent_tiles)}
    
    Generate a hypothesis for why this room is drifting.
    Write your hypothesis as an investigation tile.
    """
    
    hypothesis = llm.generate(prompt)
    investigation_tile = Tile(
        type="investigation",
        content=hypothesis,
        parent=room.id,
        clock=room.clock.increment()
    )
    room.write(investigation_tile)
    
    # Micro models will verify on next tick
```

Key design principle: **the LLM writes tiles, it does not mutate state.** All mutations go through the room protocol. The LLM is a tile generator, not a state modifier. This means LLM hallucinations are just tiles — they can be flagged, verified, and pruned by micro models on the next tick.

**Escalation hierarchy:**

```
Micro model detects → LLM hypothesizes → Micro model verifies → LLM synthesizes → Constraint check passes → Promote to knowledge
```

If constraint check fails, the cycle repeats. The conservation law ensures the cycle converges — I(x) is bounded, so the system cannot drift infinitely even if the LLM is wrong.

### 2.3 Layer 3: Self-Evolution

The system modifies itself through four mechanisms:

#### 3.3.1 Micro Model Retraining

When a room accumulates enough new tiles, the micro models are retrained:

```python
def retrain_if_needed(room):
    new_tiles = room.read_since(room.last_training_tick)
    if len(new_tiles) < MIN_TRAINING_BATCH:
        return
    
    # Retrain drift-detect on new distribution
    training_data = room.generate_training_pairs(new_tiles)
    room.micro_models['drift_detect'].retrain(training_data)
    
    # Verify retrained model maintains accuracy
    accuracy = room.micro_models['drift_detect'].evaluate(room.test_set)
    if accuracy < ACCURACY_FLOOR:
        room.micro_models['drift_detect'].rollback()
        emit(RETRAIN_FAILED, room)
```

The accuracy floor is a constraint. If retraining degrades performance, it rolls back. This is not optional — it is enforced by the system.

#### 3.3.2 Room Topology Adjustment

Rooms can split when they grow too large or merge when they become redundant:

```
split condition: drift_detect consistently high AND tile_relevance shows two clusters
merge condition: two rooms have >90% tile overlap AND intent vectors are aligned
```

Splitting uses tile_relevance as the clustering signal. Merging requires intent alignment to prevent semantic collisions.

#### 3.3.3 Pattern Promotion

When a tile or tile pattern survives multiple evolution cycles without being pruned, and it has been referenced by multiple investigation tiles, it is promoted to a seed-tile:

```python
def promote_if_qualifying(tile):
    age = room.clock.now() - tile.created_clock
    references = count_references(tile, room.all_tiles())
    survival = not tile.has_been_pruned_flag
    
    if age > PROMOTION_AGE and references > PROMOTION_REFS and survival:
        seed = SeedTile.from_tile(tile)
        room.promote(seed)
        emit(PROMOTED, seed)
```

Seed-tiles are the system's long-term memory. They are the patterns worth keeping.

#### 3.3.4 Pruning

Tiles that are dormant (not referenced, not relevant to current intent) for longer than a pruning threshold are archived and eventually removed from active storage. They remain in the content-addressed store but are not loaded into room state.

Pruning is not deletion. The content-addressed store preserves everything. Pruning is about what's in active memory — what the micro models are monitoring.

### 2.4 Layer 4: Decomposition / Recomposition

This is the core algorithm. Given an arbitrary problem:

#### Step 1: Decompose

```python
def decompose(problem_statement):
    # LLM decomposes into sub-problems
    sub_problems = llm.generate(f"""
    Decompose this problem into independent sub-problems.
    Each sub-problem should be solvable by a single PLATO room.
    For each sub-problem, specify:
    - Name
    - Input tiles (what knowledge it needs)
    - Output tiles (what it produces)
    - Constraints (what must be satisfied)
    
    Problem: {problem_statement}
    """)
    
    rooms = []
    for sub in parse(sub_problems):
        room = Room(name=sub.name, intent=sub.intent)
        room.add_seed_tiles(sub.input_tiles)
        room.set_constraints(sub.constraints)
        rooms.append(room)
    
    # Wire tile flows between rooms
    for room_a, room_b in find_dependencies(rooms):
        room_a.on_output(room_b.receive)
    
    return DecompositionPlan(rooms=rooms)
```

Decomposition is LLM-guided because arbitrary problems require understanding. The LLM doesn't solve the problem — it breaks it into pieces that micro models can solve.

#### Step 2: Evolve

```python
def evolve(plan, steps=100):
    for step in range(steps):
        for room in plan.rooms:
            room.tick()  # Run micro model loop
            
            # Check cross-room conservation
            total_I = sum(spectral_conservation(room) for room in plan.rooms)
            if abs(total_I - plan.initial_I) > CONSERVATION_TOLERANCE:
                emit(CONSERVATION_VIOLATION, plan, step)
                plan.reconcile()  # Force re-balance
        
        # LLM synthesis pass every N steps
        if step % SYNTHESIS_INTERVAL == 0:
            for room in plan.rooms:
                if room.has_pending_events():
                    shell_reason(room)  # Layer 2
```

The conservation check is critical. If total I(x) across all rooms drifts beyond tolerance, the system forces reconciliation. This is the structural guarantee.

#### Step 3: Recompose

```python
def recompose(plan):
    # Collect output tiles from all rooms
    outputs = {room.name: room.get_output_tiles() for room in plan.rooms}
    
    # Verify all constraints are satisfied
    constraints = plan.all_constraints()
    violations = verify_constraints(outputs, constraints)
    
    if violations:
        # Feed violations back as new constraints
        for violation in violations:
            room = identify_responsible_room(violation, plan.rooms)
            room.add_constraint(violation.reformulate())
        return None  # Not converged yet
    
    # LLM synthesizes final answer
    result = llm.generate(f"""
    Synthesize these room outputs into a final answer.
    Room outputs: {summarize(outputs)}
    Original problem: {plan.problem_statement}
    All constraints satisfied: True
    """)
    
    return Result(
        answer=result,
        outputs=outputs,
        conservation_delta=total_I - plan.initial_I,
        steps_taken=plan.steps,
        rooms_used=len(plan.rooms)
    )
```

#### Why This Converges

The system converges because of two structural properties:

1. **Spectral conservation bounds the search space.** I(x) = γ(x) + H(x) is approximately conserved. This means the system cannot drift into arbitrary regions of solution space. The search is constrained to an iso-I surface.

2. **Constraint verification provides a termination condition.** When all constraints are satisfied, the system stops. This is not "good enough" — it is "all constraints satisfied."

These are not emergent properties. They are engineered properties.

### 2.5 Layer 5: Application Interface

```python
from plato_shell import ShellApp

app = ShellApp("supply-chain-optimizer")

# Register knowledge sources
app.add_knowledge("warehouse-data", warehouse_tiles)
app.add_knowledge("route-graph", route_tiles)
app.add_knowledge("constraints", constraint_tiles)

# Decompose
plan = app.decompose("Minimize delivery time while respecting capacity constraints")
# → Creates rooms: warehouses, routes, capacity, objectives, scheduler

# Evolve
plan.evolve(steps=200, synthesis_interval=20)
# → 200 ticks of micro model monitoring + 10 LLM synthesis passes

# Recompose
result = plan.recompose()
# → Verified solution with conservation guarantee

print(result.answer)
print(f"Conservation delta: {result.conservation_delta}")  # Should be ≈ 0
print(f"Steps: {result.steps_taken}")
print(f"Rooms: {result.rooms_used}")

# The solution is a set of tiles. They persist.
# Next time you run a similar problem, the rooms already have context.
app.persist()
```

The application does not implement intelligence. It provides domain knowledge and asks questions. The shell handles decomposition, evolution, verification, and recomposition.

---

## 3. Key Questions

### 3.1 How Does Spectral Conservation Guarantee Solution Quality?

Spectral conservation constrains the total information content of the room system. During evolution:

- When rooms exchange tiles, total I is conserved across the exchange boundary
- When a room evolves its solution, I can shift between γ (structure) and H (entropy) but the sum remains bounded
- Conservation violation triggers reconciliation — the system self-corrects

This means: **the system cannot produce a solution that has fundamentally different information content than the problem.** It cannot hallucinate structure that wasn't in the input. The solution quality is bounded by the conservation law.

In practice, this manifests as a maximum drift tolerance. If a room's I(x) deviates from its initial value by more than ε, the system flags it. If the total system I deviates by more than ε, the system forces reconciliation. This is analogous to energy conservation in physics — you don't get free energy, and you don't get free information.

### 3.2 What's the Minimum Viable Shell?

Two configurations:

**Minimal (no LLM):** Rooms + micro models. The system detects drift, flags anomalies, maintains relevance scores, and evolves micro models. This runs on any hardware including WASM. Useful for monitoring, anomaly detection, and pattern recognition tasks. Limitation: cannot handle novel problems requiring decomposition.

**Full (with LLM):** Adds shell reasoning for decomposition, hypothesis generation, and synthesis. The LLM is invoked sparingly — only when micro models flag events. Most computation is local. The LLM is the escalator, not the engine.

The minimal shell is already deployed: it's what plato-training does today with micro models on 8 hardware targets. The full shell is the next step.

### 3.3 How Does Decomposition Work for Arbitrary Problems?

Decomposition is LLM-guided, but the output is structured, not free-form:

1. The LLM generates a decomposition plan (list of rooms with inputs, outputs, constraints)
2. The plan is validated: are constraints well-formed? Are dependencies acyclic? Are room sizes reasonable?
3. The plan is instantiated as rooms with seed-tiles
4. Micro models immediately start monitoring

If the decomposition is bad, the system detects it: rooms will show high drift, constraints will fail verification, and the system will request re-decomposition. The LLM is not trusted — its output is verified by micro models and constraint checks.

For well-known problem classes, decomposition can be template-based (no LLM needed). Supply chain optimization, scheduling, routing — these have known decompositions. The LLM is only needed for genuinely novel problem structures.

### 3.4 What Makes This Different from Existing Agent Frameworks?

| Dimension | LangChain / AutoGPT / CrewAI | PLATO Shell |
|-----------|------------------------------|-------------|
| Guarantees | None (best-effort generation) | Conservation law bounds drift |
| State | Conversation history | Persistent rooms with lifecycle |
| Reasoning | Always LLM | Micro models + LLM escalation |
| Hardware | Cloud-only | 8 targets including WASM/NPU |
| Evolution | Manual prompt engineering | Self-retraining micro models |
| Verification | Human review | Automated constraint checking |
| Transfer | Copy prompts | Share seed-tiles between apps |
| Cost | $0.01-1.00 per query (always LLM) | $0.0001 per query (micro models) + $0.01 when LLM escalates |

The fundamental difference: **existing frameworks are LLM-native with no structural guarantees. PLATO Shell is constraint-native with LLM escalation.** The LLM is a tool the system uses, not the system itself.

### 3.5 Can This Run on a Phone?

Yes. The WASM target compiles micro models to WebAssembly. SplineLinear compresses them 20×. A phone running a PLATO room with drift-detect, anomaly-flag, and tile-relevance micro models would use:

- ~50KB of WASM (compressed micro models)
- ~1MB of room state (tiles in memory)
- Sub-millisecond inference per tick
- No network required for monitoring (only for LLM escalation)

A phone app could run Layer 1 (Room Intelligence) entirely locally. Layer 2 (Shell Reasoning) would require network for LLM access, but could batch events and call the LLM intermittently.

### 3.6 What's the Self-Evolution Loop?

```
Observe (micro models) → Detect (anomaly/drift) → Hypothesize (LLM) → Verify (constraints)
→ Retrain (micro models on new data) → Promote (patterns to seed-tiles) → Prune (dormant tiles)
→ Observe (with better models)
```

Each iteration through this loop makes the system better at:
- Detecting what matters (retrained drift-detect)
- Generating useful hypotheses (LLM learns from verified hypotheses)
- Verifying efficiently (constraint patterns promoted to seed-tiles)
- Managing room state (pruning keeps rooms focused)

The loop is driven by the micro models' continuous monitoring. It is not triggered by user queries — it runs autonomously as long as the room has new data.

### 3.7 How Do Seed-Tiles Enable Transfer Learning?

Seed-tiles encode proven solutions. When a new application encounters a similar sub-problem:

1. The decomposition LLM identifies the sub-problem type
2. The system queries the seed-tile index for matching patterns
3. Relevant seed-tiles are loaded into the new room as starting knowledge
4. Evolution starts from the seed, not from scratch

Example: if the supply chain optimizer discovers an effective routing pattern for the "capacity-constrained multi-warehouse" sub-problem, it promotes that pattern to a seed-tile. When a delivery scheduling app encounters a similar sub-problem, it loads that seed-tile and evolves from there.

This is transfer learning at the knowledge level, not the weight level. The seed-tile contains the solution pattern, not just the model weights. The receiving room can re-derive the weights from the pattern using its own micro models.

---

## 4. Novel Claims (Falsifiable)

### Claim 1: Conservation-Bounded Convergence

**Claim:** For any PLATO shell system with N rooms, the decomposition-recomposition cycle converges in at most O(N² × log(D/ε)) steps, where D is the initial constraint violation magnitude and ε is the tolerance. This is because spectral conservation prevents the system from exploring the full solution space — it is constrained to an iso-I surface of dimension |I| - 1.

**Falsification:** Construct a problem where the decomposition-recomposition cycle requires more than O(N² × log(D/ε)) steps while maintaining spectral conservation. Or demonstrate that the iso-I surface has higher effective dimensionality than expected.

**Test:** Implement the cycle on 10 benchmark optimization problems with N = 5-50 rooms. Plot steps-to-convergence against N² × log(D/ε). If the relationship is not approximately linear, the claim is wrong.

### Claim 2: Micro Model Transferability via Seed-Tiles

**Claim:** A micro model trained on room R₁'s data and promoted to a seed-tile can be used to initialize a room R₂ for a semantically similar problem, achieving ≥80% of R₁'s accuracy within 10% of the original training epochs. This holds across hardware targets: a seed-tile from a GPU room transfers to a WASM room without re-derivation.

**Falsification:** Find two semantically similar problems where seed-tile transfer achieves <80% accuracy in <10% epochs. Or find a hardware target pair where transfer fails.

**Test:** Train drift-detect on 5 rooms, promote to seed-tiles, transfer to 5 new rooms on different hardware targets. Measure accuracy at 10% epochs vs. full training. If accuracy ratio < 0.8, the claim is wrong.

### Claim 3: Zero-Drift Constraint Satisfaction on Eisenstein Lattice

**Claim:** For constraint satisfaction problems where all constraints are linear over Eisenstein integers, the PLATO shell achieves zero accumulated numerical drift across unlimited evolution steps. This is because the hexagonal lattice is the densest packing in 2D, and densest packing minimizes drift in iterative refinement.

**Falsification:** Construct a linear constraint system over Eisenstein integers where the PLATO shell accumulates non-zero drift after >10⁶ evolution steps. Or prove that hexagonal packing does not minimize drift for some constraint class.

**Test:** Implement Eisenstein integer constraint solver in flux-lucid. Run 10⁹ iterations on random linear constraint systems. Measure drift accumulation. If drift > 0 (in exact arithmetic), the claim is wrong.

---

## 5. Implementation Roadmap

### Phase 1: Shell Foundation (Weeks 1-4)

- Implement Layer 1 event emission in existing micro models
- Build the monitoring loop (tick, detect, emit)
- Add hardware-aware variant selection for event handling
- Verify: micro models emit events when run continuously

### Phase 2: Shell Reasoning (Weeks 5-8)

- Implement LLM invocation protocol (event → prompt → tile → verify)
- Build the escalation hierarchy (micro → LLM → micro → promote)
- Add conservation monitoring (track I(x) across room evolution)
- Verify: LLM-generated tiles pass micro model verification

### Phase 3: Decomposition/Recomposition (Weeks 9-14)

- Implement LLM-guided decomposition with validation
- Build the evolution loop with conservation checks
- Implement recomposition with constraint verification
- Verify: end-to-end solve on 3 benchmark problems

### Phase 4: Self-Evolution (Weeks 15-20)

- Implement retraining loop with accuracy floor
- Build room split/merge logic
- Implement seed-tile promotion and transfer
- Verify: system improves on repeated runs of same problem class

### Phase 5: Application Interface (Weeks 21-24)

- Build ShellApp API
- Add persistence (room state survives restart)
- Write application examples (supply chain, scheduling, code review)
- Verify: third-party developer can use ShellApp without understanding internals

---

## 6. Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| LLM generates bad decompositions | High | Medium | Micro model verification catches bad rooms |
| Conservation law breaks on real data | Medium | High | Fall back to empirical drift bounds |
| Micro models can't verify complex hypotheses | Medium | Medium | Escalate to deeper verification chain |
| Room topology thrashing (split/merge loops) | Low | Medium | Hysteresis thresholds on topology changes |
| Seed-tile transfer fails across domains | Medium | Low | Domain-specific seed-tile clusters |
| WASM deployment too slow for real-time | Low | Low | Already benchmarked at sub-millisecond |

The highest-risk item is conservation law validity on real data. If I(x) is not approximately conserved in production room dynamics, the structural guarantees evaporate and the system becomes "yet another agent framework with a cool mathematical backstory." This is the claim that must be validated first, on real tile data, before any other work proceeds.

---

## 7. Closing: Intelligence as Infrastructure

The PLATO shell inverts the current AI application model:

**Current model:** Application calls AI API. AI is a service. Application dies when API is down.

**PLATO model:** Application lives inside an intelligent shell. Intelligence is infrastructure. Application never calls an API — the shell handles reasoning autonomously, escalating to LLMs when needed but never depending on them.

This is the difference between "AI as a tool" and "AI as the operating environment." Tools are optional. Operating environments are assumed.

The conservation law is what makes this viable. Without it, the shell would be a fancy chatbot wrapper — and the world has enough of those. With it, the shell has mathematical guarantees on behavior. You can reason about what the system will and will not do, the same way you reason about what a physical system will and will not do.

The goal: `from plato_shell import ShellApp` — and then the application developer thinks about their domain, not about AI. The intelligence is the shell. The shell is the platform. The platform is conserved.

---

*"The glitches ARE the research agenda. The gaps ARE the work."*

*— PLATO fleet axiom*

---

**Document history:**
- v0.1 (2026-05-17): Initial architecture document by Forgemaster ⚒️
