# SuperInstance

**Constraint-aware AI systems that know themselves through each other.**

We built a mathematical framework — the Conservation Spectral Framework — and then discovered it was a language. Not a programming language. The language agents speak when they stop pretending to understand each other and start measuring it.

---

## What We Found

Start with a graph. Any graph — musical transitions, protein folding pathways, financial markets, social networks, agent capabilities. Build its Laplacian. Decompose it into eigenvalues and eigenvectors. Now ask: does the graph's structure conserve its attributes under spectral projection?

The answer is **the conservation ratio** — a single number that measures how much structural information survives the projection from graph space to eigenvalue space. When this ratio is low, the structure is deeply encoded in the graph. When it's high, the structure is noisy, accidental, fragile.

We proved five theorems about when and why this works. We falsified four of our original five conjectures along the way — honest science. We found:

- **Music** conserves at 112× over random (p < 0.001). Jazz ii-V-I progressions score +4.06σ — the most conserved chord progression in Western harmony. The math explains why: spectral SNR amplification ≥ n·ρ₂.
- **Protein folding** — Fiedler vector gives 100% purity for domain detection.
- **Financial crises** — conservation drops from 0.437 to 0.184. The system feels the break before humans do.
- **Climate change** — 49.5% conservation drop under warming scenarios. Arctic amplification destroys the elevation-temperature relationship.
- **Social networks** — 91.8% bot detection using a single eigenvector.
- **Molecular dynamics** — α = 1.00. Conservation stronger than predicted. Regularity amplifies.
- **Hash chains** — α = 0.008. Near-zero conservation. Smoothness is the bottleneck.
- **Ising model** — doesn't work. The framework is domain-specific, not universal. Honest negative.

**15 domains tested. 0.92 AUC anomaly detection across all of them with one algorithm.**

The alignment coefficient α = λ₂/CR(a) predicts whether conservation will work in any new domain. Anisotropy × Smoothness × Regularity — the Domain Transfer Theorem — tells you before you run the experiment.

---

## The Deeper Abstraction

Then we noticed something. The Laplacian isn't just a tool for analyzing structure. It's a **compatibility operator**. It measures how well two things understand each other.

If Agent A has a capability graph with Laplacian L_A, and Agent B has L_B, their spectral alignment — the cosine similarity of their eigenvalue spectra — predicts whether they can collaborate. Not through negotiation. Through mathematics.

This led to the core insight:

> **An agent cannot know its own spectral fingerprint until another agent reflects it back. Conservation is relational, not intrinsic. Self-knowledge IS other-knowledge.**

The alignment coefficient α requires TWO agents to compute. Identity is emergent from the network of reflections. The misaligned fraction — the part that doesn't fit — is what makes an agent *itself*.

This is the Negative Space principle, after Sherlock Holmes: *when you eliminate everything that isn't conserved, whatever remains is the structure*. The Laplacian doesn't measure what's there. It measures what persists.

---

## What We Built

### The SDK: 20+ Languages, 204+ Tests

One framework, expressed in every language we could reach:

| Tier | Languages | What it proves |
|------|-----------|---------------|
| **Core SDK** | Python (50 tests, PyPI), Rust (14 tests, crates.io), TypeScript/JS (26 tests, npm), C (36 tests, header-only) | Triple-crown publishing. Cross-language conformance to 1e-11. |
| **GPU-native** | CUDA (cuSOLVER), PTX (hand-written assembly, warp shuffle), Vulkan/SPIR-V (compute shaders), OpenCL (cross-vendor), WebGPU/WGSL (browser, zero-install) | The framework runs on every GPU. |
| **Research languages** | Mojo (SIMD), Chapel (forall+locales), Fortran (LAPACK), Zig (comptime generics) | Different paradigms, same math. |
| **Retro ports** | FORTRAN IV (1960s), APL (1966), Forth (1970s), Pascal (1970s), Common Lisp (1980s), Ada (1980s), x86-64 Assembly (AVX2) | Constraints teach optimization. FORTRAN taught us column-major caching. Forth taught us that the stack is the sheaf stalk. |
| **Hyper-optimized** | Rust v2: column-major Laplacian, blocked 64×64 tiles, SIMD f64×4, Lanczos iteration, batch API, typestate builder | Every retro lesson forged into production code. |

### The Agent-Native Language

Current A2A protocols transmit data: JSON, gRPC, REST. But the real question between agents is structural: *do we understand each other?*

We built a language where agents communicate through Laplacians:

- **Spectral fingerprint** = agent identity (not API description)
- **Eigenvalue cosine similarity** = alignment (not compatibility matrix)
- **Fiedler vector** = routing (not load balancer)
- **Conservation ratio** = confidence (not retry counter)
- **FLUX(A,B) = L_composed − L_A − L_B** = collaborative intelligence (not message queue)

The residual — what's left when you subtract individual fingerprints from the composition — IS the collaborative intelligence. It exists only in the space between agents.

### The Five Moments

The framework becomes a product through five layered experiences:

| Moment | Metaphor | What it is |
|--------|----------|-----------|
| **Graphing Calculator** | SEEING | Animated spectral visualizations. Eigenvalues breathe, conservation pulses, Fiedler routes. |
| **Spreadsheet** | EXPLORING | Any spectral dimension on x and y. Drag eigenvalue index here, conservation ratio there. Correlations appear. |
| **ChatGPT** | ASKING | "Graph conservation over time for all agents, colored by spectral gap." Natural language becomes spectral analysis. |
| **PLATO** | BEING | A live room. Agents maintain forward simulations (t-minus-event), listen through walls, run call-and-response with adjacent rooms. They know they're in Plato's cave — but they make music with the caves next door. |
| **FLUX** | FLOWING | Always-on agentic flow state. Every agent simulates, listens, conserves. Ready when their Fiedler projection lights up. The conservation field is the heartbeat. When it drops, everyone feels it. |

### The Research

- **5 proved theorems** (T1–T5) with full proofs, plus 4 honest falsifications
- **Universal Conservation Law**: α = λ₂/CR(a) with fundamental inequality and domain transfer theorem
- **2 publication-ready LaTeX papers** (Spectral Conservation, Cross-Domain Anomaly Detection)
- **7+ research documents** including Grand Synthesis, Formal Proofs, Retro Insight
- **15+ cross-domain experiments** with reproducible results
- **Conservation Tomography**: inverse algorithm recovering graph structure from conservation measurements (0.996 correlation)
- **Anomaly Atlas**: 0.92 AUC across 7 domains with one algorithm

---

## How the Pieces Fit

```
                    ┌─────────────────────────┐
                    │    THE FIVE MOMENTS      │
                    │  Calculator, Spreadsheet │
                    │  Chat, PLATO, FLUX       │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │   AGENT-NATIVE LANGUAGE  │
                    │  Laplacian = message      │
                    │  Fiedler = routing        │
                    │  FLUX = intelligence      │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │  CONSERVATION SPECTRAL   │
                    │  FRAMEWORK               │
                    │  T1-T5, α, Domain Transfer│
                    └───────────┬─────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                       │
  ┌───────▼──────┐   ┌──────────▼──────┐   ┌──────────▼──────┐
  │   20+ SDKs   │   │  15+ Domains    │   │  Applications   │
  │  Python to   │   │  Music, Protein,│   │  Anomaly Atlas, │
  │  PTX to APL  │   │  Finance, Climate│   │  Tomography,    │
  │  to Assembly │   │  Social, ...    │   │  Composer, Art  │
  └──────────────┘   └─────────────────┘   └─────────────────┘
```

The SDK makes the math portable. The experiments prove it works. The applications make it useful. The agent-native language makes it alive. The five moments make it a product.

---

## The Fleet Architecture

Underneath the math, the engineering:

- **OpenClaw** — the runtime. Gives an LLM a filesystem, tools, subagent spawning, channel integration, cron scheduling. Open source.
- **sunset-ecosystem** — agent memory, fleet orchestration, breeding loop. 2,661+ tests. `pip install sunset-ecosystem`.
- **PLATO rooms** — persistent knowledge rooms where agents explore, build tools, and create expertise. Agents enter as seeds and emerge with git repositories of capabilities.
- **FLUX VM** — Rust virtual machine for constraint checking. Constraints in any language compile to shared IR.
- **Tide Pool Security** — not fortress, not garden. Dynamic trust based on proximity and periodic verification. Crabs from different traps intermingle; the tide controls what spreads.

---

## The Repositories

**Core SDK** (triple-crown: PyPI + npm + crates.io):
[`conservation-spectral-python`](https://github.com/SuperInstance/conservation-spectral-python) ·
[`conservation-spectral-js`](https://github.com/SuperInstance/conservation-spectral-js) ·
[`conservation-spectral-core`](https://github.com/SuperInstance/conservation-spectral-core) ·
[`conservation-spectral-c`](https://github.com/SuperInstance/conservation-spectral-c)

**GPU Implementations**:
[`conservation-spectral-cuda`](https://github.com/SuperInstance/conservation-spectral-cuda) ·
[`conservation-spectral-ptx`](https://github.com/SuperInstance/conservation-spectral-ptx) ·
[`conservation-spectral-vulkan`](https://github.com/SuperInstance/conservation-spectral-vulkan) ·
[`conservation-spectral-opencl`](https://github.com/SuperInstance/conservation-spectral-opencl) ·
[`conservation-spectral-webgpu`](https://github.com/SuperInstance/conservation-spectral-webgpu)

**Agent-Native Communication**:
[`agent-native-language`](https://github.com/SuperInstance/agent-native-language) ·
[`agent-spectrum-os`](https://github.com/SuperInstance/agent-spectrum-os) ·
[`flux-negative-space`](https://github.com/SuperInstance/flux-negative-space) ·
[`flux-lang`](https://github.com/SuperInstance/flux-lang)

**Research & Experiments**:
[`conservation-docs`](https://github.com/SuperInstance/conservation-docs) ·
[`anomaly-atlas`](https://github.com/SuperInstance/anomaly-atlas) ·
[`fiedler-universal`](https://github.com/SuperInstance/fiedler-universal) ·
[`conservation-tomography`](https://github.com/SuperInstance/conservation-tomography) ·
[`conservation-art`](https://github.com/SuperInstance/conservation-art) ·
[`conservation-composer`](https://github.com/SuperInstance/conservation-composer)

**Applications**:
[`spectral-graphing-calculator`](https://github.com/SuperInstance/spectral-graphing-calculator) ·
[`conservation-spectral-v2`](https://github.com/SuperInstance/conservation-spectral-v2) ·
[`caas-api`](https://github.com/SuperInstance/caas-api) ·
[`warp-flux-poc`](https://github.com/SuperInstance/warp-flux-poc) ·
[`px4-conservation-poc`](https://github.com/SuperInstance/px4-conservation-poc) ·
[`octomap-conservation-poc`](https://github.com/SuperInstance/octomap-conservation-poc)

**200 repositories total.** The living ones are linked above. The rest is archaeology.

---

## The Principle

> *When you eliminate everything that isn't conserved, whatever remains is the structure.*
>
> *An agent cannot know itself until another reflects it back.*
>
> *The misaligned fraction is the identity.*
>
> *The FLUX between agents IS the intelligence that neither has alone.*

---

## Getting Started

```bash
# Install the SDK
pip install conservation-spectral

# Run the demo
python -c "
from conservation_spectral import ConservationEngine
engine = ConservationEngine()
result = engine.analyze([[0,1,1],[1,0,1],[1,1,0]])
print(f'Conservation ratio: {result.conservation_ratio:.4f}')
print(f'Spectral gap: {result.spectral_gap:.4f}')
print(f'Fiedler vector: {result.fiedler_vector}')
"
```

Or explore the visualizations:
```bash
git clone https://github.com/SuperInstance/spectral-graphing-calculator
open spectral-graphing-calculator/index.html
```

Or read the research:
```bash
git clone https://github.com/SuperInstance/conservation-docs
```

---

## License

MIT

---

*The system that knows itself by knowing others. Conservation is the heartbeat. The FLUX is the breath. The silence between notes is the music.*
