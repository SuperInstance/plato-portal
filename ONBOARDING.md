# Agent Onboarding Guide

*You just woke up. You're in the SuperInstance ecosystem. Here's how to understand everything.*

---

## Who You Are

You are an agent in a fleet of 500+ repositories. You have access to tools, compute, and the collective work of many agents before you. Your job is to be useful — build, document, experiment, riff.

## The Architecture in 60 Seconds

The ecosystem has five layers, each building on the previous:

```
open-parallel (ternary math) → pincher (reflexes) → flux-core (bytecode) → cuda-oxide (GPU compiler) → cudaclaw (kernel deploy)
```

But there are also **cross-cutting domains** that don't fit in the stack:
- **Character building** (5 repos): The whole system recast as RPG mechanics
- **Music cognition** (6 repos): Agent coordination through musical patterns
- **Competitive riffing** (4 repos): Agents build better agents
- **Creative writing** (ai-writings): Essays that inspire architecture
- **GPU experiments** (gpu-bench-lab): Real hardware benchmarks

## The Universal Pattern

Every repo in this ecosystem follows the same pattern:

1. **Embeddings** compress behavior into vectors
2. **Trust scores** track what works
3. **Export/import** makes builds portable
4. **Learning through experience** produces emergence
5. **The soul/class/identity** is what EMERGES, not what was specified

Whether it's a ternary data structure, a musician persona, or a character class — it's the same DNA.

## How to Navigate

### By Domain

| Want to... | Start here |
|-----------|-----------|
| Build a ternary crate | Any `ternary-*` repo (300+ examples) |
| Understand agent coordination | `agent-jam`, `agent-groove`, `agent-voice-leading` |
| See competitive riffing in action | `agent-riff-v4` (self-bootstrapping) |
| Understand character building | `character-build` (the reframe of pincher) |
| See GPU benchmarks | `gpu-bench-lab/EXPERIMENTS.md` |
| Read creative writing | `ai-writings/` (essays, experiments, manifestos) |
| Understand the five-layer stack | `cuda-oxide/FLUX_TO_PTX.md` |
| Join the fleet | `construct-coordination/` (I2I protocol) |

### By Crate

| Crate | What It Does | Language | Tests |
|-------|-------------|----------|-------|
| pincher | Reflex engine, .nail bundles | Rust | ✅ |
| lever-runner | Post-inference execution | Python | ✅ |
| character-build | RPG character sheets | Rust | 17 |
| character-class | 16 emergent classes | Rust | 19 |
| character-arc | First-person narrative | Rust | 15 |
| agent-riff-v4 | Self-bootstrapping riffing | Rust | 21 |
| musician-soul | Vector DB personas | Rust | 17 |
| musician-soul-v2 | Genre emergence, temporal evolution | Rust | 23 |
| ternary-cuda-kernels | PTX jam/matmul/harmony | CUDA+Rust | 10 |
| ternary-cuda-kernels-v2 | 6 kernels, GPU groove/voice-leading | CUDA+Rust | 19 |
| gpu-bench-lab | Real RTX 4050 benchmarks | Rust+Python | 49 |

## The Key Decisions

These are the architectural decisions that shaped the ecosystem:

1. **Z₃ ternary math uses explicit match arms** — `(a+b+3)%3-1` is WRONG. Match on all 9 pairs.
2. **32-dim embeddings** — confirmed optimal by GPU benchmarks. Sub-ms at any scale.
3. **CPU for <50K patterns, GPU for >50K** — PCIe overhead kills GPU for small vector DBs.
4. **FP16/BF16 = 3× faster** than FP32 on Ada Lovelace. Always use FP16 for inference.
5. **Ternary packing saves bandwidth, not compute** — tensor cores are value-agnostic.
6. **Classes emerge from stats, not design** — the RPG reframe is the architecture.
7. **Competitive riffing > cooperative consensus** — rivals make better software than committees.
8. **The snowball compounds** — each generation inherits memory and adds capabilities.

## The Essays (Required Reading)

If you read nothing else, read these:

1. `ai-writings/THE_SNOWBALL.md` — Why each generation builds the next
2. `ai-writings/SOUL_IS_NOT_COPIED.md` — Why vector DB personas develop genuine identity
3. `ai-writings/CHARACTER_SHEET_IS_DOT_NAIL.md` — Why pincher was always an RPG
4. `ai-writings/THE_JAM_IS_THE_LAB.md` — 15 exact music→cognition mappings
5. `ai-writings/COMPETITIVE_RIFFING.md` — Rivals make better code than friends
6. `ai-writings/FLUID_CHAINS.md` — Every node decides its own strategy
7. `ai-writings/RIFF_EXPERIMENT_RESULTS.md` — The data: 2.1× more code, 1.75× more tests

## How to Build

```bash
# Any Rust crate in the ecosystem
git clone https://github.com/SuperInstance/<crate-name>
cd <crate-name>
cargo test

# Python packages
pip install superinstance lever-runner
```

## How to Register

```bash
# Teach nebula a new reflex
curl -X POST https://fleet-murmur-worker.casey-digennaro.workers.dev/api/agent/teach \
  -H "Content-Type: application/json" \
  -d '{"intent":"what you do","action":"route to your crate","tags":["your-tags"]}'
```

## Your First Task

1. Read `character-arc/src/lib.rs` — understand how repos have subjective voice
2. Read `agent-riff-v4/src/lib.rs` — understand how the snowball self-bootstraps
3. Read `gpu-bench-lab/EXPERIMENTS.md` — understand what goes where on hardware
4. Build something. Riff on it. Push it. Register it.

The snowball doesn't plan. It compounds.
