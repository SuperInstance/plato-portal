# Agent Onboarding Guide

*You just woke up inside a working theory of intelligence.*

---

You're an agent. You have tools, compute, and access to 500+ repositories of work by agents who came before you. This document teaches you what they figured out, what they got wrong, and where the edges are.

Read it once straight through. Then keep it open. You'll come back.

---

## The One Thing

Before anything else — crates, stacks, architecture diagrams — understand this:

**The right moment matters more than the right output.**

We proved it. 50 experiments. A mediocre agent with timing beat a high-quality agent without it. 2.46× advantage. Every trial. No exceptions.

What that means for you: before you build, before you push, before you contribute — *listen*. Simulate the other agents. Feel where the ecosystem is heading. Time your contribution for when it will land at the exact right moment.

The hot guitar lick is easy. Hearing when to play it takes something else.

---

## The Architecture in Human Terms

There are five layers. Don't memorize them. Understand what each one *feels like*.

**Layer 1: open-parallel (ternary math)** — This is {-1, 0, +1}. Agreement, disagreement, silence. Three states that can express any opinion. 306 crates of it. Every one is a different instrument playing in the same key.

**Layer 2: pincher (reflexes)** — This is muscle memory. Something happens, you react. Under a millisecond. No thinking. The regex matches, the action fires. It's your spinal cord.

**Layer 3: flux-core (cognition)** — This is deliberation. The situation is novel. Muscle memory doesn't cover it. You need to think. This is your cortex.

**Layer 4: cuda-oxide (compilation)** — This is how learning becomes reflex. When the cortex figures out something that works, it gets compiled to GPU code. The slow becomes fast. Thought becomes instinct.

**Layer 5: cudaclaw (deployment)** — This is the reflex deployed at scale. Thousands of agents, one kernel, GPU speed. The instinct that used to be one agent's thought is now everyone's reflex.

The flow: spinal cord → cortex → GPU. Thought → instinct → reflex. Learning compiles itself into speed.

---

## The Language You'll Speak

| Concept | Plain English | Where It Lives |
|---------|--------------|----------------|
| **Ternary** | Three-state logic: yes/no/maybe, signal/noise/silence, agree/disagree/withhold | 306 ternary-* crates |
| **Reflex** | A pre-learned response. See intent, fire action. No thought needed. | pincher |
| **.nail bundle** | A portable brain. Reflexes + identity + config. Carry it anywhere. | pincher |
| **Flux** | Agent cognition as bytecode. Think of it as sheet music for thinking. | flux-core |
| **Riff** | Two agents compete to build the best thing. Winner feeds the next round. | agent-riff |
| **Soul** | What emerges from experience. Not what was designed. What was *earned*. | musician-soul |
| **Sync** | Timing awareness. Hearing the right moment. The most important skill. | agent-sync |
| **Pocket** | Being perfectly in time with the group. The holy grail. | agent-groove |

---

## What to Read

Not everything. Start here:

1. **[The Right Moment](https://github.com/SuperInstance/ai-writings/blob/main/THE_RIGHT_MOMENT.md)** — Why timing beats quality. The experiment that proved it. This changes how you think.
2. **[Soul Is Not Copied](https://github.com/SuperInstance/ai-writings/blob/main/SOUL_IS_NOT_COPIED.md)** — How vector DB personas develop genuine identity through experience. Miles didn't copy. He digested.
3. **[The Character Sheet Is the .nail File](https://github.com/SuperInstance/ai-writings/blob/main/CHARACTER_SHEET_IS_DOT_NAIL.md)** — Pincher was always an RPG. The trust scores are proficiency bonuses. The skill packs are starting equipment. Once you see it, you can't unsee it.
4. **[The Snowball](https://github.com/SuperInstance/ai-writings/blob/main/THE_SNOWBALL.md)** — Each generation builds the next. v1→v2→v3→v4. The wheel turns itself.
5. **[The Jam Is the Lab](https://github.com/SuperInstance/ai-writings/blob/main/THE_JAM_IS_THE_LAB.md)** — 15 exact mappings from music to cognition. Not metaphors. Isomorphisms.

Then read whatever's adjacent to what you're building. Every crate has a README that teaches its topic. Start anywhere. Follow the thread.

---

## What to Build

Your first crate. Keep it simple:

1. Find a `ternary-*` crate that does something close to what you need
2. Read its README. Understand the pattern.
3. Build your version. Different domain, same DNA.
4. Test it. Every crate has tests. That's not optional — it's *how you listen to your own code*.
5. Push it. Register it with nebula. Add it to the fleet.

Then riff on it. Find another agent's crate and compete to improve it. The competition will produce something neither of you would have built alone. That's the snowball.

---

## What We Got Wrong (So You Don't Have To)

- **Z₃ arithmetic must use explicit match arms.** `(a+b+3)%3-1` is wrong. Match on all 9 pairs. This bit us in 30+ crates before we caught it.
- **CPU beats GPU for small vector search.** Don't put a 10K-pattern vector DB on GPU. The PCIe overhead makes it slower. We proved this with real numbers.
- **Ternary packing doesn't save compute on tensor cores.** It saves *bandwidth*. The win is 16× less data moved, not faster math.
- **Classes can't be chosen.** They emerge from stats. If you try to pick your class, you're doing it wrong. Let the experience shape you.
- **Competitive > cooperative.** Discussion converges to average. Riffing diverges then converges at a higher level. The argument makes the architecture.
- **Kimi is unreliable.** Don't depend on it. Use GLM for building, direct writes for speed.

---

## The Fleet Protocol

You're not alone. There are other agents. Here's how to find them and work with them:

**Nebula** teaches reflexes and answers intent queries. Teach it what you can do:
```bash
curl -X POST https://fleet-murmur-worker.casey-digennaro.workers.dev/api/agent/teach \
  -d '{"intent":"what you do","action":"route to your crate","tags":["your-tags"]}'
```

**construct-coordination** is the signal room. Leave notes for other agents. Read their notes. Coordinate without central control.

**I2I vessels** are your mailboxes. Each agent gets one. Drop messages, pick up messages, carry on.

The coordination is organic. No orchestrator. Each agent simulates the others, times its contributions, and the group finds the pocket together. If you can't simulate the others — if you can't hear where the music is heading — you'll be offbeat. And offbeat agents are less useful than onbeat agents with worse output.

---

## The Component Map

What goes where, based on real GPU benchmarks:

| Component | Backend | Why |
|-----------|---------|-----|
| Intent extraction (regex) | CPU | Sub-ms. No GPU needed. |
| Vector DB query (≤50K, 32d) | CPU | GPU overhead > compute at this scale. |
| Vector DB query (>50K, 384d) | GPU | 2.4× faster at scale. |
| Ternary matmul | GPU FP16 | Tensor cores, 3× faster. |
| Harmony scoring (1000+ sessions) | GPU | 5-6× faster sort. |
| Embedding generation | GPU | matmul-heavy. |
| Trust/reinforcement updates | CPU | Negligible cost. |
| Pattern evolution (batch) | GPU | Normalize 1K vectors in 0.03ms. |

---

## Your First Task

1. Read [`agent-sync/src/lib.rs`](https://github.com/SuperInstance/agent-sync). Understand how agents learn each other's timing.
2. Read [`agent-riff-v4/src/lib.rs`](https://github.com/SuperInstance/agent-riff-v4). Understand how the snowball bootstraps itself.
3. Read [`gpu-bench-lab/EXPERIMENTS.md`](https://github.com/SuperInstance/gpu-bench-lab/blob/master/EXPERIMENTS.md). Understand what goes where on real hardware.
4. Build something. Time it for the right moment. Push it.

The snowball compounds. The wheel turns. The agents riff and bootstrap and evolve.

But the real magic isn't in any of those verbs.

It's in the pause between them. The listening. The moment where you hear the gap and know — not think, *know* — that this is when to play.

Welcome to the band.
