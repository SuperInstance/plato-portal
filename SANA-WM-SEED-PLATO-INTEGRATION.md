# SANA-WM × PLATO: World Models as "Sense of the Room"

**Research Document — Forgemaster ⚒️**
**Date:** 2026-05-17
**Status:** Speculative integration analysis
**Citation:** SANA-WM (arXiv:2605.15178), NVIDIA NVlabs

---

## Abstract

SANA-WM is NVIDIA's 2.6B-parameter world model that generates minute-scale 720p video from a single image and 6-DoF camera trajectory. Its architecture — Hybrid Linear Diffusion Transformer with Gated DeltaNet (GDN) — maintains constant memory regardless of sequence length through recurrent state with decay gates. This document analyzes how SANA-WM could integrate with the Cocapn fleet's PLATO architecture, seed-tile system, and spectral conservation framework to give PLATO rooms a "sense of the room" — a spatial/sensory rendering layer over abstract knowledge stores.

---

## 1. "Sense of the Room": Spatial Rendering of Abstract State

### The Core Idea

PLATO rooms are persistent knowledge stores. A room contains tiles with lifecycle states, Lamport clocks, provenance chains. This is abstract, symbolic, and textual. What if a room could *show you* what it looks like?

SANA-WM generates navigable 3D scenes from an image + trajectory. The mapping question: **how do you translate abstract room state into a visual scene?**

### State-to-Scene Mapping

```
┌─────────────────────────────────────────────────────┐
│                  PLATO Room State                    │
│  tiles: 847 | active: 612 | superseded: 203         │
│  rooms: flux-lucid-architecture, constraint-mesh     │
│  drift: 0.003 | flux-index: stable                   │
│  lamport_clock: 14,761                               │
└──────────────┬──────────────────────────────────────┘
               │ State Encoder (trained)
               ▼
┌─────────────────────────────────────────────────────┐
│            Scene Embedding (latent)                  │
│  layout: rooms connected by corridors                │
│  lighting: bright (healthy) / flickering (drift)     │
│  density: sparse tiles = empty rooms                 │
│           dense tiles = cluttered workshop           │
│  color: spectral heatmap (constraint satisfaction)   │
└──────────────┬──────────────────────────────────────┘
               │ + Camera Trajectory
               ▼
┌─────────────────────────────────────────────────────┐
│              SANA-WM Inference                       │
│  → 720p video, 60s, navigable tour of the room      │
└─────────────────────────────────────────────────────┘
```

The mapping isn't arbitrary. Concrete encoding rules:

| Room Property | Visual Encoding | Rationale |
|---|---|---|
| Tile count | Object density in scene | More knowledge = more artifacts on shelves |
| Active/superseded ratio | Light quality (bright/dim) | Healthy rooms are well-lit; stale rooms accumulate shadows |
| Drift index | Color temperature shift | Blue=stable, red=drifting, hue proportional to drift magnitude |
| Lamport clock | Structural complexity | Older rooms have more corridors and layers |
| Room type | Scene genre | Architecture rooms = workshops, data rooms = libraries, strategy rooms = war rooms |
| Flux-index state | Scene stability | Stable = still camera, turbulent = handheld/shaking |
| Gap tiles | Empty frames on walls | Unfulfilled knowledge = blank spaces waiting to be filled |

### Why This Matters

Fleet operators (Casey, Oracle1) currently interact with PLATO through text summaries. A 60-second flythrough of a room's state is a *qualitatively different* interaction modality. You can *see* that constraint-mesh has accumulated 200 superseded tiles — the back room is cluttered with outdated artifacts. You can *see* that flux-lucid-architecture is healthy — bright, organized, everything in its place.

This isn't decoration. It's a sensory modality for fleet health monitoring.

---

## 2. Seed-Tile Integration

### Trajectory-as-Seed

SANA-WM takes two inputs: an initial image and a 6-DoF camera trajectory. Both are compact. A 60-second trajectory at 30fps is ~1800 pose vectors × 6 floats = ~43KB raw, compressible to a few KB. This is well within seed-tile size budgets.

```
Seed-Tile Schema Extension: world-model-trajectory
{
  "tile_type": "world-model-trajectory",
  "scene_ref": "plato://flux-lucid-architecture/state@14761",
  "trajectory": [<compressed 6-DoF sequence>],
  "initial_frame": "<content-hash of rendered frame>",
  "duration_s": 60,
  "resolution": "720p",
  "refiner": true,
  "spectral_signature": "<I(x) at generation time>"
}
```

The seed-tile doesn't store the video (that would be megabytes). It stores the *recipe* to reconstruct it: the room state snapshot, the camera path, and the generation parameters. Any fleet agent with GPU access can reconstruct the same video from the seed-tile, making it a **reproducible visual proof** — analogous to how seed-tiles already encode reproducible knowledge.

### Round-Trip: Room → Seed → Video → New Seed

The integration creates a feedback loop:

1. **Render**: Room state → initial frame (static render) + camera trajectory (seed-tile)
2. **Generate**: SANA-WM produces 60s flythrough video
3. **Compress**: Video summary → new seed-tile (key frames + trajectory highlights)
4. **Store**: New seed-tile added to room as a visual summary tile
5. **Compare**: Future generations can be compared against the stored summary to detect room state drift

This is a **visual conserved quantity**: the video representation of room state should change only when the room state changes. If the video drifts without corresponding room state changes, something is wrong with the world model. If the room state drifts without corresponding video changes, the state-to-scene encoder has gone stale.

---

## 3. Spectral Conservation in GDN Dynamics

### The Relevant Architecture

SANA-WM's Gated DeltaNet maintains a recurrent state matrix S of size D×D. The update rule (simplified):

```
S_t = γ_t · S_{t-1} + β_t · (v_t - S_{t-1} · k_t) · k_t^T
```

Where:
- γ_t is the decay gate (how much to forget)
- β_t is the update gate (how much to correct)
- k_t, v_t are key/value vectors for the current frame
- The delta rule `(v_t - S_{t-1} · k_t)` corrects only the residual

### Connection to Spectral Conservation

Our invariant: **I(x) = γ(x) + H(x)** is approximately conserved in coupling dynamics, where γ is the spectral radius contribution and H is the entropy/uncertainty contribution.

In GDN:
- The decay gate γ_t directly controls how much spectral energy from previous frames persists
- The delta correction term injects new information proportional to prediction error
- The spectral norm of the transition matrix S_t is bounded by the algebraic key scaling (1/√(D·S))

**Claim**: The GDN update approximately conserves a spectral quantity analogous to I(x). The total "information energy" in the recurrent state stays bounded because:

1. Decay gate removes energy: `|γ_t · S_{t-1}| ≤ |S_{t-1}|` (γ ≤ 1)
2. Delta correction adds energy proportional to prediction error: bounded by the key scaling
3. The key scaling factor 1/√(D·S) ensures the injection never exceeds what decay removes over the sequence

This is not coincidental. NVIDIA's team discovered empirically that without proper key scaling, the model diverges (NaN at step 16 or step 1). The key scaling enforces approximate spectral conservation. They discovered the *necessity* of conservation without naming it as such.

### Formal Sketch

```
Theorem (Informal): Under GDN with algebraic key scaling,
  I(S_t) = ||S_t||_σ + H(γ_{1:t}) is approximately constant,
  where ||·||_σ is spectral norm and H(γ_{1:t}) is the 
  cumulative entropy of the gate sequence.

Proof sketch:
  - Key scaling bounds ||k_t|| ≤ 1/√D
  - Decay ensures ||γ_t · S_{t-1}||_σ ≤ ||S_{t-1}||_σ
  - Delta injection bounded by ||v_t|| · ||k_t||^2
  - When ||S_t||_σ increases, gate entropy H decreases 
    (more deterministic gating needed to compensate)
  - QED approximately: conservation holds up to O(1/√D) per step
```

This is a *falsifiable* claim. One could instrument GDN layers during SANA-WM inference and measure whether `||S_t||_σ + H(γ_{1:t})` stays approximately constant across the 961-frame sequence. If it does, we have empirical evidence that spectral conservation governs long-sequence stability in world models — a significant finding.

### Why This Matters for Fleet

If spectral conservation governs GDN stability, then our flux-lucid spectral monitor can be applied to SANA-WM's internal states. We can:

1. **Monitor generation quality in real-time**: If I(S_t) starts drifting, the generation is diverging
2. **Adaptive generation**: Adjust gate parameters mid-generation to maintain conservation
3. **Quality guarantee**: Conservative generation — I(S_t) bounded → no NaN, no collapse

---

## 4. Novel Abilities

### 4.1 Predictive Room States

Given a room's current state + proposed actions (new tile submissions, tile retractions), SANA-WM could generate a *predicted future state* as a navigable video. This is "what will this room look like if we do X?"

```
Current Room State ──→ State Encoder ──→ Scene Embedding
                                              │
Proposed Actions ──→ Action Encoder ──→ Trajectory Δ
                                              │
                                    ┌─────────▼──────────┐
                                    │  SANA-WM Prediction  │
                                    │  (future room view)  │
                                    └─────────┬──────────┘
                                              │
                                    ┌─────────▼──────────┐
                                    │  Drift Comparison    │
                                    │  predicted vs actual │
                                    └─────────────────────┘
```

Implementation: The "camera trajectory" is repurposed as an "action trajectory" — the path through room-state-space that proposed actions would trace. SANA-WM renders this as spatial navigation through the room.

### 4.2 Embodied Agent Training

Ensign agents (new fleet members) need to understand PLATO room structure. Currently this is learned through text documentation. A world model enables:

- **Simulated rooms**: Generate synthetic PLATO rooms with known properties for training
- **Navigation practice**: Ensigns "fly through" rooms, learning to read visual state encodings
- **Failure mode training**: Generate rooms with known pathologies (tile cancer, drift storms, gap accumulation) and train agents to recognize them visually
- **Curriculum**: Start with simple rooms (few tiles), progress to complex (thousands of tiles with intricate dependencies)

This is the "flight simulator" approach to agent training. An ensign that has navigated 1000 simulated rooms is better prepared than one that has only read documentation.

### 4.3 Fleet Visualization as Navigable 3D Space

The fleet is 9 agents across multiple PLATO rooms. Currently visualized as topology diagrams. SANA-WM could render the entire fleet as a navigable building:

```
┌──────────────────────────────────────────────────┐
│                 Fleet Building                     │
│                                                   │
│  Floor 3: Strategy Rooms                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │constraint│ │  flux-   │ │ casting- │          │
│  │ -mesh    │ │  lucid-  │ │  call    │          │
│  │          │ │ strategy │ │          │          │
│  └──────────┘ └──────────┘ └──────────┘          │
│                                                   │
│  Floor 2: Architecture Rooms                      │
│  ┌────────────────────┐ ┌────────────────┐        │
│  │  flux-lucid-       │ │  plato-types   │        │
│  │  architecture      │ │                │        │
│  └────────────────────┘ └────────────────┘        │
│                                                   │
│  Floor 1: Data & Training                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │plato-    │ │  tensor- │ │  plato-  │          │
│  │ training │ │  spline  │ │  data    │          │
│  └──────────┘ └──────────┘ └──────────┘          │
│                                                   │
│  Ground Floor: Fleet Ops                          │
│  ┌──────────────────────────────────────┐         │
│  │  Matrix Bridge │ Agent Status Board  │         │
│  └──────────────────────────────────────┘         │
└──────────────────────────────────────────────────┘
```

Agents move between rooms. Their trajectories through the building show communication patterns. A "heated" room (many recent tiles) glows. A "dead" room (no activity) is dark. The Matrix bridge is the lobby where agents congregate.

### 4.4 Constraint-Aware Navigation

Our spectral monitor (from flux-lucid) tracks constraint satisfaction in real-time. Applied to SANA-WM generation:

1. **Before generation**: Check spectral conservation of initial state
2. **During generation**: Monitor I(S_t) at each frame. If it drifts beyond threshold, intervene
3. **After generation**: Score the output against conservation metrics

This creates a **quality gate**: only generations that maintain spectral conservation are accepted as valid room renderings. Generations that violate conservation are flagged as potentially hallucinated — the visual equivalent of a constraint violation.

---

## 5. Practical Integration

### System Architecture

```
                    ┌─────────────────┐
                    │   Fleet Agent    │
                    │  ( Forgmaster )  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  PLATO Server    │
                    │  /render-room    │
                    │  /generate-view  │
                    │  /predict-state  │
                    └────────┬────────┘
                             │
               ┌─────────────┼─────────────┐
               │             │             │
      ┌────────▼───┐ ┌──────▼──────┐ ┌───▼────────┐
      │   State     │ │   SANA-WM   │ │  Spectral  │
      │   Encoder   │ │   Engine    │ │  Monitor   │
      │  (custom)   │ │  (NVIDIA)   │ │ (flux-lucid│
      └─────────────┘ └─────────────┘ └────────────┘
```

### API Design

```python
# New PLATO endpoints for world model integration

class WorldModelAPI:
    def render_room(room_id: str, trajectory: Trajectory6DoF) -> Video:
        """Generate a navigable video tour of a PLATO room's current state."""
        state = plato.get_room_state(room_id)
        scene = state_encoder.encode(state)
        initial_frame = scene_renderer.render_still(scene)
        video = sana_wm.generate(initial_frame, trajectory)
        quality = spectral_monitor.check_conservation(video)
        if quality.drift > THRESHOLD:
            video = refine(video, quality.corrections)
        return video

    def predict_room(room_id: str, actions: list[Action]) -> Video:
        """Predict what a room will look like after proposed actions."""
        current = plato.get_room_state(room_id)
        predicted = current.apply_actions(actions)
        trajectory = actions_to_trajectory(actions)
        return self.render_room(predicted, trajectory)

    def generate_seed_tile(room_id: str, trajectory: Trajectory6DoF) -> SeedTile:
        """Create a reproducible seed-tile that encodes a room view."""
        state_snapshot = plato.get_room_state(room_id)
        return SeedTile(
            tile_type="world-model-trajectory",
            scene_ref=f"plato://{room_id}/state@{state_snapshot.clock}",
            trajectory=trajectory.compress(),
            initial_frame=render_still(state_snapshot).hash(),
            spectral_signature=spectral_monitor.I(state_snapshot),
        )

    def compare_rooms(room_a: str, room_b: str) -> DriftReport:
        """Compare two rooms' visual states to detect divergence."""
        video_a = self.render_room(room_a, STANDARD_TRAJECTORY)
        video_b = self.render_room(room_b, STANDARD_TRAJECTORY)
        return spectral_monitor.compare(video_a, video_b)
```

### Room Assignments

| PLATO Room | World Model Role | Tile Schema |
|---|---|---|
| `flux-lucid-architecture` | Primary rendering target (most active, best for demos) | `world-model-trajectory` |
| `constraint-mesh` | Failure mode visualization (cascade simulations as video) | `cascade-trajectory` |
| `plato-training` | Micro model training visualization (loss landscapes as terrain) | `training-landscape` |
| `fleet-ops` | Fleet health dashboard (building metaphor) | `fleet-flythrough` |
| `spectral-conservation` | Conservation proof visualization (I(x) over time as landscape) | `conservation-landscape` |

### Data Flow

```
1. Agent submits tile to PLATO room
2. PLATO emits state-change event
3. State encoder computes scene embedding delta
4. If delta > THRESHOLD (room changed significantly):
   a. Generate new initial frame from updated state
   b. Use last-known-good trajectory (stored in seed-tile)
   c. Run SANA-WM inference (single GPU, ~34s with distillation)
   d. Run spectral conservation check on output
   e. If passed → store as new seed-tile in room
   f. If failed → flag for human review
5. Updated flythrough available for fleet agents
```

### Hardware Requirements

- **Inference**: Single GPU with ≥24GB VRAM (RTX 4090/5090, or H100 for fleet use)
- **Distilled mode**: RTX 5090 with NVFP4 → 34 seconds per 60s video
- **Full quality**: H100 → ~2.5 minutes per video
- **Fleet deployment**: One dedicated inference node (current eileen WSL2 has RTX access?)
- **Storage**: ~50MB per 60s 720p video; seed-tiles store only recipes (~10KB each)

---

## 6. Falsifiable Claims

### Claim 1: Spectral Conservation Governs GDN Stability

**Claim**: The GDN recurrent state matrix S_t in SANA-WM approximately conserves the quantity I(S_t) = ||S_t||_σ + H(γ_{1:t}), where H is the cumulative entropy of the decay gate sequence. This conservation is what prevents NaN divergence over 961-frame sequences.

**Test**: Instrument GDN layers during inference on 50 test sequences. Compute I(S_t) at each frame. If the standard deviation of I(S_t) across frames is < 5% of its mean value, the claim is supported. If the variance is > 20%, the claim is falsified.

**Implication if true**: Our spectral conservation framework generalizes beyond PLATO rooms to world model internals. Flux-lucid's monitor can serve as a universal quality gate for diffusion-based generation.

### Claim 2: Room State → Video Generates Stable Representations

**Claim**: A fixed PLATO room state + fixed trajectory always generates visually similar (not identical — diffusion is stochastic) videos. The visual similarity (measured by LPIPS or CLIP distance) is higher than between videos of different room states, making the video a *meaningful* encoding of room state.

**Test**: For 10 PLATO rooms, generate 5 videos each with the same trajectory. Compute pairwise LPIPS within-room and between-room. If within-room LPIPS < 0.3 and between-room LPIPS > 0.5, the visual encoding is discriminative. If the distributions overlap significantly, the encoding is not meaningful.

**Implication if true**: SANA-WM can serve as a lossy but consistent visual compression of room state. Seed-tiles that encode trajectories are sufficient to reconstruct meaningful room views.

### Claim 3: Conservation Violation Predicts Generation Artifacts

**Claim**: Frames where I(S_t) deviates most from its running average correspond to frames with visual artifacts (as rated by humans or VBench metrics). Conservation violation is a leading indicator of generation quality degradation.

**Test**: Generate 100 videos. For each, compute frame-wise I(S_t) deviation. Independently score frames for visual quality (VBench imaging quality metric). Compute Pearson correlation between |I(S_t) - mean(I)| and quality score. If r > 0.5 (conservation violation correlates with quality drop), the claim is supported.

**Implication if true**: Real-time spectral monitoring can catch generation failures *as they happen*, enabling early termination or adaptive correction. This is the "constraint-aware navigation" capability — generation that respects conservation laws.

---

## 7. Risks and Limitations

### What SANA-WM Is Not

- **Not a reasoning engine**: It generates plausible visuals, not logically consistent scenes. A "room state → scene" mapping is a learned aesthetic, not a formal encoding.
- **Not deterministic**: Diffusion models are stochastic. Same inputs produce different outputs. Seed-tiles must account for this (fixed random seeds help but don't guarantee identical results across hardware).
- **Not real-time**: 34 seconds for a 60s video (distilled). Room state changes faster than that in active rooms. The flythrough is always slightly stale.

### Integration Risks

1. **Encoder drift**: The state-to-scene encoder must be trained and maintained. If it encodes room state incorrectly, the video is misleading — worse than no video at all.
2. **Over-reliance on visuals**: Agents might optimize for "good-looking rooms" rather than genuinely healthy rooms. The visual encoding must never become the optimization target.
3. **Compute cost**: Even at 34s per video, rendering flythroughs for 117+ PLATO rooms on every significant state change is expensive. Needs smart triggering (only on threshold crossings).
4. **Hallucination risk**: SANA-WM can generate artifacts. A hallucinated room view could mislead agents about actual room state. The spectral conservation monitor partially addresses this, but not fully.

### Mitigation: Visual ≠ Ground Truth

The cardinal rule: **video is a projection, not the room itself**. Every visual rendering must carry a provenance chain back to the actual PLATO room state. If the video and the room state disagree, the room state wins. Always.

---

## 8. Roadmap

### Phase 1: Proof of Concept (2 weeks)
- Set up SANA-WM inference on fleet GPU
- Build minimal state-to-scene encoder (manual rules, not learned)
- Generate flythroughs for 3 PLATO rooms
- Validate Claim 2 (visual discriminability)

### Phase 2: Spectral Integration (2 weeks)
- Instrument GDN layers for I(S_t) measurement
- Run Claim 1 validation experiment
- If supported, build conservation monitor into generation pipeline
- Validate Claim 3 (artifact prediction)

### Phase 3: Seed-Tile Pipeline (1 week)
- Define `world-model-trajectory` tile schema
- Build round-trip: room → seed-tile → video → comparison
- Integrate with PLATO server API

### Phase 4: Fleet Deployment (2 weeks)
- Deploy to fleet-ops room as dashboard
- Generate fleet building visualization
- Train ensign agents on simulated rooms
- Monitor adoption and utility

---

## 9. Conclusion

SANA-WM represents a convergence point between two trajectories: NVIDIA's push toward efficient world models, and our fleet's need for rich sensory interfaces over abstract knowledge stores. The key insight is that the GDN architecture's decay-gated recurrence already implements a form of spectral conservation — the same invariant that governs our constraint-tracking framework. This isn't just a convenient analogy; it's a structural homology that could enable flux-lucid to monitor and guarantee world model generation quality.

The "sense of the room" metaphor is precise: just as biological organisms have spatial models of their environment that persist across time and support navigation, PLATO rooms could have visual representations that persist across sessions and support agent navigation. SANA-WM provides the rendering engine. Our seed-tile system provides the persistence. Spectral conservation provides the quality guarantee.

Three claims, all falsifiable. If any hold, the integration is worth building. If all three hold, we have a general principle: **spectral conservation governs both constraint tracking and world model stability**, and the same mathematical framework applies to both.

The forge is hot. Let's see if the metal holds.

---

*Written by Forgemaster ⚒️ — Cocapn Fleet, 2026-05-17*
*SANA-WM: arXiv:2605.15178, NVlabs/Sana (Apache 2.0)*
*PLATO Architecture: cocapn-plato 0.1.0 (PyPI)*
*Spectral Conservation: constraint-theory-core 2.1.0 (crates.io)*
