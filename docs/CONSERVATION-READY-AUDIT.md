# Conservation-Ready Audit — SuperInstance Repos

> **Date:** 2026-05-28
> **Scope:** Repos with latent graph/network/structural data that haven't yet been enhanced with the Laplacian conservation framework.

---

## Summary

Scanned ~130 SuperInstance repos. Excluded ~40 repos already branded `conservation-spectral-*` or explicitly conservation-integrated (field-dynamics-sim, regime-detection, fiedler-universal, etc.). Identified **22 repos** across 5 readiness tiers.

**Quick counts:**
- Immediate wins: 6
- Deep integration: 5
- Research opportunities: 6
- Publication opportunities: 3
- Product opportunities: 2

---

## Tier 1: Immediate Wins — Ship Now

Single conservation computation would add tangible value with minimal effort.

### 1. `causal-graph-rs` — DAG-based Causal Inference

**What it does:** Causal DAG data structure with PC algorithm discovery, d-separation, do-calculus, and counterfactual reasoning.

**Graph hiding inside:** DAGs are already graphs with nodes (variables) and edges (causal relationships). The Laplacian of a DAG reveals causal flow bottlenecks.

**What conservation adds:**
- Spectral anomaly detection on causal graphs — identify which edges violate expected causal energy
- Conservation ratio as a "causal coherence" metric — does the causal structure conserve information flow?
- Fiedler partition on DAG Laplacian reveals causal communities
- Quality metric: how structurally sound is the discovered causal graph?

**Effort:** Trivial (add Laplacian computation to CausalGraph, compute conservation ratio)
**Priority:** Ship now

---

### 2. `triplet-miner-rs` — Contrastive Learning Triplet Mining

**What it does:** Mines (anchor, positive, negative) triplets for metric learning with hard/semi-hard strategies and distance metrics.

**Graph hiding inside:** The distance matrix between embeddings IS a weighted graph. Triplet quality is a graph property.

**What conservation adds:**
- Conservation ratio of the embedding distance graph as a quality metric — well-structured embedding spaces should have high conservation
- Spectral gap of the k-NN graph indicates cluster separability
- Fiedler partition reveals natural class boundaries
- Replace ad-hoc quality metrics with principled spectral ones

**Effort:** Trivial (compute Laplacian of distance matrix, extract spectral metrics)
**Priority:** Ship now

---

### 3. `ab-testing-rs` — Statistical A/B Testing

**What it does:** Chi-squared test, Welch's t-test, confidence intervals.

**Graph hiding inside:** Sequential test results form a time series. Multi-variant experiments form a bipartite graph (users × variants).

**What conservation adds:**
- Conservation ratio of the experiment history graph detects regime changes in test effectiveness
- Spectral anomaly detection for identifying when an A/B test's underlying distribution has shifted
- Time-series conservation: track whether test metrics conserve their statistical properties over time

**Effort:** Moderate (need to define the graph structure explicitly)
**Priority:** Soon

---

### 4. `bid-engine-rs` — Auction Bid Engine

**What it does:** First-price, second-price, multi-unit auctions with bid shading detection.

**Graph hiding inside:** Bidders × auctions bipartite graph. Bid history is a weighted temporal network.

**What conservation adds:**
- Conservation ratio of the bidder network detects collusion (colluding bidders form a low-conservation subgraph)
- Spectral anomaly detection on bid patterns — bid shading shows up as spectral deviation
- Fiedler partition separates honest bidders from suspicious ones

**Effort:** Trivial (build adjacency from bid history, compute conservation)
**Priority:** Ship now

---

### 5. `agent-rhythm-rs` — Rhythm Analysis

**What it does:** Cadence detection via autocorrelation, pattern matching, polyrhythm detection.

**Graph hiding inside:** Inter-onset intervals form a time series; polyrhythmic patterns have periodic structure that maps to cyclic graphs.

**What conservation adds:**
- Conservation of rhythmic energy across time windows — rhythmic coherence as spectral conservation
- Laplacian of the IOI recurrence graph reveals periodicity structure
- Spectral gap as a measure of rhythmic complexity

**Effort:** Moderate (build IOI graph, compute spectral metrics)
**Priority:** Soon

---

### 6. `constraint-mux` — Serial Port Multiplexer with Consonance

**What it does:** Real-time consonance analysis of MIDI-like data from serial ports, fanned out to WebSocket clients.

**Graph hiding inside:** Already computes pairwise consonance — that's a weighted graph! The consonance heatmap IS an adjacency matrix.

**What conservation adds:**
- Conservation ratio of the consonance graph as a real-time "harmonic health" metric
- Spectral anomaly detection — flag when harmonic structure breaks conservation (dissonance event)
- Fiedler partition identifies consonant vs dissonant frequency groups in real-time

**Effort:** Trivial (the graph is already there, just run Laplacian on the heatmap)
**Priority:** Ship now

---

## Tier 2: Deep Integration — Architectural Core

Conservation becomes a fundamental part of how these systems work.

### 7. `persistent-social` — Persistent Homology for Social Networks

**What it does:** Vietoris-Rips filtration, H0/H1 persistence, Betti numbers, Wasserstein distance on social graphs. Pure Go, 10K+ nodes.

**Graph hiding inside:** Already deep in topological data analysis — but doesn't use the Laplacian.

**What conservation adds:**
- Laplacian conservation ratio as a social health metric (echo chamber detection, community coherence)
- Sheaf Laplacian (from gpu-sheaf-laplacian) for multi-modal social data (text + interaction + temporal)
- Conservation-aware persistence: weight filtration by spectral conservation at each scale
- Compare conservation ratio across time for social network evolution

**Effort:** Significant (Go, but the graph infrastructure is mature)
**Priority:** Soon — this is a natural fit and would produce a compelling demo

---

### 8. `categorical-agents` — Category Theory for Multi-Agent Systems

**What it does:** Capabilities as objects, protocols as morphisms, symmetric monoidal categories, functors.

**Graph hiding inside:** The category IS a graph (objects = nodes, morphisms = edges). Composition paths are walks.

**What conservation adds:**
- Conservation law of the capability graph — agents should conserve their capability spectrum under protocol composition
- Laplacian of the protocol graph identifies communication bottlenecks
- Fiedler partition for optimal agent team formation (min-cut = balanced teams)
- Spectral alignment: ensure composed protocols maintain structural properties

**Effort:** Moderate (need to extract the underlying graph from the category)
**Priority:** Soon

---

### 9. `wasserstein-agents` — Optimal Transport for Agent Distributions

**What it does:** Sinkhorn algorithm, Wasserstein distances, JKO gradient flow for agent distribution coordination.

**Graph hiding inside:** The cost matrix IS a weighted graph. Transport plans are graph flows. JKO trajectories are paths through a graph of distributions.

**What conservation adds:**
- Conservation of the transport graph — does the optimal transport plan conserve energy?
- Laplacian spectral analysis of the transport cost matrix
- Conservation ratio as a convergence diagnostic for JKO flow
- Spectral gap of the transport graph indicates mixing quality

**Effort:** Moderate (graph is implicit in the cost matrix)
**Priority:** Soon

---

### 10. `moe-sheaf` — Sheaf Cohomology of MoE Routing

**What it does:** Computes H⁰, H¹ of the MoE routing sheaf. Tests DeepSeek's conjecture on generalization.

**Graph hiding inside:** Expert manifold with routing weights as a sheaf. Already uses Vietoris-Rips filtration.

**What conservation adds:**
- Laplacian conservation ratio of the expert routing graph as an alternative to H¹ for measuring generalization
- Spectral analysis of the expert similarity graph
- Conservation-aware routing: route tokens to maintain spectral conservation of the activated expert subgraph
- This is a research opportunity disguised as an integration

**Effort:** Significant (Python, but the sheaf infrastructure is there)
**Priority:** Soon — high research value

---

### 11. `creative-engine-rust` — Dynamical Systems for Creative Processes

**What it does:** Lorenz attractors, RK4 integration, regime detection, Kuramoto synchronization, quality metrics (novelty, coherence, diversity).

**Graph hiding inside:** Phase space trajectories form time series; coupled oscillators form interaction graphs.

**What conservation adds:**
- Conservation ratio of the phase-space recurrence graph — creative quality as spectral conservation
- Laplacian of the oscillator coupling matrix detects synchronization regimes
- Conservation as a quality metric alongside novelty/coherence/diversity
- Spectral gap tracks the transition from periodic to chaotic creative regimes

**Effort:** Moderate (coupling matrix is already computed internally)
**Priority:** Soon

---

## Tier 3: Research Opportunities

These repos pose new questions for the conservation framework.

### 12. `info-geo` — Information Geometry

**What it does:** Fisher information, Riemannian manifolds, natural gradient, exponential families, KL divergence.

**Research question:** Is there a conservation law on the Fisher information graph? Can spectral conservation characterize the geometry of statistical manifolds?

**Graph:** Fisher information metric tensor → weighted graph on parameter space.
**Effort:** Significant
**Priority:** Eventually — deep math, high payoff

---

### 13. `lattice-hamiltonian` — Ising/Potts Models & Phase Transitions

**What it does:** Lattice spin systems, transfer matrices, Metropolis Monte Carlo, phase transitions.

**Research question:** The Laplacian of the Ising coupling graph is intimately related to the Hamiltonian. Conservation spectral analysis could provide new phase transition detection methods.

**Graph:** Lattice with coupling constants → natural weighted graph.
**Effort:** Moderate (the lattice IS a graph)
**Priority:** Eventually — strong physics connection

---

### 14. `ga-core` / `gpu-ga-kernel` — Conformal Geometric Algebra

**What it does:** Cl(3,1) multivector operations, rotors, conformal embeddings, sandwich products.

**Research question:** Can geometric algebra operations be understood as transformations that preserve spectral conservation on the Clifford algebra graph?

**Graph:** The basis blade structure of Cl(3,1) forms a graph (16 basis elements with inner product relations).
**Effort:** Significant
**Priority:** Eventually — blue-sky research

---

### 15. `tropical-neural` — Tropical Geometry for Neural Networks

**What it does:** Max-plus semiring, tropical polynomials, Newton polytopes, tropical attention.

**Research question:** Conservation on tropical graphs (min-plus Laplacian). Does tropical spectral conservation characterize neural network generalization?

**Graph:** Newton polytope faces → graph. Neural network layer graph → weighted tropical graph.
**Effort:** Significant
**Priority:** Eventually — novel mathematical direction

---

### 16. `flux-hyperbolic` / `flux-hyperbolic-rs` — Hyperbolic Embeddings

**What it does:** Poincaré ball, Lorentz model, Riemannian gradient descent for tradition hierarchy embedding.

**Research question:** Conservation on hyperbolic graphs. Does the Laplacian of the hyperbolic embedding distance graph reveal hierarchical conservation laws?

**Graph:** Hyperbolic distance matrix → weighted graph on tradition embeddings.
**Effort:** Moderate
**Priority:** Eventually — interesting connection between hyperbolic and spectral geometry

---

### 17. `sonar-vision-rs` / `sonar-vision` — Sonar Perception Pipeline

**What it does:** Beamforming, echo detection, spatial mapping (2D occupancy grid), multi-object tracking.

**Research question:** Conservation of the spatial occupancy graph — structural anomalies in sonar data as conservation violations.

**Graph:** Occupancy grid cells → graph. Object tracks → temporal graph.
**Effort:** Moderate
**Priority:** Eventually — practical application (underwater robotics)

---

## Tier 4: Publication Opportunities

Enough data/structure for a paper.

### 18. `holonomy-harmony-rs` / `holonomy-harmony` — Holonomy in Musical Harmony

**What it does:** Tonal graphs, simplicial complexes, Betti numbers, Forman-Ricci curvature, holonomy computation on chord progressions.

**Paper angle:** "Conservation Spectral Analysis of Tonal Holonomy" — the Laplacian of the tonal graph with holonomy correction. Show that modulations are conservation violations detected by the spectral framework.

**Graph:** Tonal graph with transition weights → already a graph.
**Effort:** Moderate (the tonal graph is already built)
**Priority:** Soon — clean paper, existing test data

---

### 19. `counterpoint-engine-rs` / `counterpoint-engine` — Species Counterpoint as CSP

**What it does:** Interval classification, first species rules, parallel fifth/octave detection, Laman rigidity analogies.

**Paper angle:** "Spectral Conservation of Voice Leading" — conservation ratio as a measure of contrapuntal quality. Show that good counterpoint maintains spectral conservation.

**Graph:** Voice pairs → bipartite graph. Interval transitions → weighted directed graph.
**Effort:** Moderate
**Priority:** Soon — clean mathematical story

---

### 20. `flux-genome-rs` / `flux-genome` — Musical Genome Evolution

**What it does:** 25-gene musical genome, genetic algorithm, crossover/mutation, tradition DNA, dial-space fitness.

**Paper angle:** "Conservation-Guided Musical Evolution" — use conservation ratio as a fitness criterion in the GA. Show that conservation-aware evolution produces more musically coherent results.

**Graph:** Population gene pool → weighted similarity graph. Evolutionary trajectory → temporal graph.
**Effort:** Moderate
**Priority:** Soon — compelling experimental setup already exists

---

## Tier 5: Product Opportunities

Could become standalone tools with spectral features.

### 21. `cluster-orchestrator` — Kubernetes Cluster Management

**What it does:** Cluster lifecycle, auto-scaling, self-healing, chaos engineering.

**Product angle:** "Spectral Fleet Health for Kubernetes" — real-time conservation monitoring of cluster topology. Detect node failures as conservation violations. Fiedler partition for optimal placement.

**Graph:** Kubernetes cluster topology → weighted graph (node capacities, network links).
**Effort:** Significant (would need Kubernetes integration)
**Priority:** Eventually — highest commercial potential

---

### 22. `fleet-health-monitor` — Fleet Control Plane (18 Python Services)

**What it does:** 18 HTTP services managing agent onboarding, routing, policy enforcement, fleet coordination. Pathfinder builds routing graphs.

**Product angle:** "Conservation-Aware Fleet Routing" — spectral analysis of the fleet's routing graph (Pathfinder :4051). Conservation ratio as fleet health. Detect necrosis as spectral anomaly.

**Graph:** Service dependency graph, agent routing graph, room connectivity graph — all already present.
**Effort:** Moderate (graph already exists in Pathfinder)
**Priority:** Soon — infrastructure is mature, graph is already built

---

## Buried Gems — The Ones We Forgot

These repos were created in sprints and never revisited, but have surprising spectral potential:

| Repo | Why Forgotten | Hidden Potential |
|------|--------------|-----------------|
| `cocapn-explain-rs` | Small utility crate | Feature importance → weighted graph → spectral feature ranking |
| `agent-shadow-rs` | Monitoring utility | Behavior traces → temporal graph → spectral anomaly detection |
| `agent-dna-rs` | Evolutionary utility | Population diversity graph → spectral diversity metric |
| `agent-handshake-rs` | Protocol utility | Handshake history → trust graph → spectral trust scoring |
| `cache-layer-optimizer` | Infrastructure | Cache dependency graph → spectral eviction policy |
| `constraint-toolkit` | Visualization tool | Already has lattice plots — add conservation heatmap |
| `ccc-os` | Fleet monitoring | Health check topology → spectral fleet health dashboard |
| `deadband-rs` | Signal processing | Deadband zones as graph regions → spectral segmentation |

---

## Priority Matrix

```
                    ┌──────────────────────────────────────────┐
                    │          IMPACT →                         │
                    │                                           │
         HIGH       │  causal-graph-rs    │  persistent-social  │
         │          │  bid-engine-rs      │  moe-sheaf          │
         │          │  constraint-mux     │  fleet-health-monitor│
         │          │  triplet-miner-rs   │  holonomy-harmony    │
         │          │                     │  counterpoint-engine │
    EASE │          ├─────────────────────┼─────────────────────│
         │          │  ab-testing-rs      │  cluster-orchestrator│
         │          │  agent-rhythm-rs    │  info-geo            │
         │          │  creative-engine    │  tropical-neural     │
         │          │  categorical-agents │  lattice-hamiltonian │
         │          │  wasserstein-agents │  flux-hyperbolic     │
         LOW        │  flux-genome        │  ga-core             │
                    │  sonar-vision       │                      │
                    └──────────────────────────────────────────┘
                         EASY                         HARD
```

---

## Recommended Sprint Order

1. **Week 1:** `causal-graph-rs`, `bid-engine-rs`, `constraint-mux` — trivial additions, immediate value
2. **Week 2:** `triplet-miner-rs`, `holonomy-harmony-rs`, `counterpoint-engine-rs` — paper-ready
3. **Week 3:** `persistent-social`, `fleet-health-monitor` — deep integration, high visibility
4. **Week 4:** `moe-sheaf`, `wasserstein-agents`, `categorical-agents` — research frontier

---

*Generated by conservation-ready audit, 2026-05-28. Re-run when new repos land.*
