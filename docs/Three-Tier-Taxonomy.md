# The Three-Tier Taxonomy

<div align="center">
  <em>The captain's log of classification. Every model has a number. Most of the numbers lie.</em>
</div>

---

## The Map

There's a chart on the lighthouse wall. Three columns, hand-drawn in grease pencil. Every model that's ever come through the yard gets a mark in one of them. The chart doesn't care about parameter count. It doesn't care about benchmarks or leaderboard scores. It cares about one thing: **can the model compute, or can't it?**

That chart is the three-tier taxonomy. It came out of Study 50, a boundary-mapping exercise on the Eisenstein norm N(a,b) = a² − ab + b². We thought we were mapping a formula. We ended up mapping the entire fleet.

### Tier 1: Internalized Computation

These models just know. You hand them the notation bare — no setup, no explanation, no "think step by step" — and they compute correctly. The formula is a compiled primitive. It's not reasoning. It's not guessing. It's **done** before the ink dries.

**Members:** Seed-2.0-mini, Seed-2.0-code, gemma3:1b (1 billion parameters)

**Signature:** 100% accuracy on bare notation. 100% accuracy on scaffolded. Scaffolding is irrelevant because the computation is already internalized. The model doesn't need help. It doesn't need hints. You give it the problem, it gives you the answer. That's the whole transaction.

### Tier 2: Scaffoldable

These models *can* do the math, but they need a hand. Bare notation gets them 0–50% correct. Add step-by-step scaffolding and they jump to 100%. The knowledge is in there — it's just locked behind what we call the **vocabulary wall**. The model recognizes the symbols but defaults to discourse mode (explaining about the math) instead of computation mode (doing the math). An activation key — a structured prompt that says "here are the steps, now execute" — flips the switch.

**Members:** Hermes-70B, Qwen3-235B, phi4-mini, llama3.2:1b, Hermes-405B

**Signature:** 0–50% bare, 25–100% scaffolded. The spread is wide, but the pattern is the same: scaffolding provides a +50 to +100 percentage point improvement. These models have the capacity. They need the key.

### Tier 3: Incompetent

Nothing helps. Bare notation: 0%. Scaffolded: 0%. Higher temperature: 0%. Few-shot examples: 0%. You can't activate what isn't stored. These models lack the computational pathway entirely. Temperature just adds noise to the discourse they produce instead of answers.

**Members:** qwen3:0.6b, qwen3:4b, Qwen3.6-35B (A3B)

**Signature:** 0% across every condition. Route around them. Don't try to fix them. Just pick a different model.

---

## Training Data, Not Scale

Here's the chart that broke the industry's favorite assumption:

| Model | Parameters | Bare Score | Scaffolded |
|-------|:----------:|:----------:|:----------:|
| gemma3:1b | **1B** | **100%** | **100%** |
| Hermes-405B | 405B | 0% | 100% |

A 1-billion-parameter model beats a 405-billion-parameter model by 100 percentage points on bare notation. They tie with scaffolding — but gemma3 doesn't *need* the scaffolding. It just computes.

Parameter count has **zero predictive power** for tier placement. Let that sink in. The single most commonly cited metric in the entire industry — how big is the model — tells you nothing about whether the model can actually do the math you're handing it.

What does predict tier? **Training data composition.** Google trained Gemma 3 with heavy mathematical reasoning emphasis. ByteDance trained Seed with dense mathematical pre-training. These models internalized algebraic formulas during training. For them, N(a,b) = a² − ab + b² isn't a computation — it's a lookup. The training compiled the formula into the weights.

Meanwhile, Hermes-405B has 400× more parameters but treats the same formula as a reading comprehension exercise. It wants to explain Eisenstein integers to you. It writes beautiful paragraphs about the lattice structure. It just can't compute the number.

Dense mathematical pre-training beats raw scale by **400× in parameter efficiency.** One billion parameters, trained right, outperforms 405 billion parameters trained wrong. The yard doesn't care how big the rig is. It cares whether the rig can haul the load.

---

## The MoE Active-Parameter Connection

There's a pattern hiding in the Tier 3 column. It took us a minute to see it because we were looking at total parameters. Once we looked at *active* parameters, the pattern jumped out:

| Model | Total Params | Active Params | Active Ratio | Tier |
|-------|:------------:|:-------------:|:------------:|:----:|
| Qwen3-235B | 235B | 22B | 9.4% | 2 |
| Qwen3.6-35B | 35B | 3B | 8.6% | **3** |

Models with less than 10% active parameters fail disproportionately. When only ~9% of your weights fire per token, you lack the dense compute needed for multi-step arithmetic. Mixture-of-Experts is brilliant for throughput — you get 235B-class knowledge with 22B-class cost — but the sparse activation pattern is poison for serial computation.

This isn't a coincidence. Arithmetic requires sequential state: compute a², hold it, compute ab, hold it, subtract, hold it, compute b², hold it, add. Each step depends on the previous one. If the expert that knows b² is a different expert than the one that just computed ab, the intermediate result has to survive the handoff. At 9% active ratio, it mostly doesn't.

Dense small models beat sparse giants per active parameter. gemma3:1b (1B dense, 100% active) computes circles around Qwen3-235B (22B active, 9.4%). The 1B model has every parameter working on every token. The 235B model has most of its brain asleep at any given moment.

The lighthouse keeper's rule: **for mathematical computation, count active parameters, not total parameters.** A small rig with all wheels on the ground beats a big rig with most of them in the air.

---

## What Works Per Tier

The yard dispatches rigs. Each tier gets a different dispatch protocol.

### Tier 1: Bare Notation

Just hand them the problem. No fanfare.

```
Compute the Eisenstein norm of (5, -3ω). N(a,b) = a² − ab + b².
```

Done. That's the whole prompt. Adding scaffolding doesn't help — it's already internalized. Adding temperature doesn't change anything — the computation path is the highest-probability path regardless of sampling. Tier 1 models are the flatbeds of the fleet: load them up and point them at the job.

### Tier 2: Scaffolding + Activation Keys

Tier 2 models need the key. The mechanism isn't domain knowledge — it's **structured computation scaffolding**. Study 51 proved this: generic step-by-step math examples (+25pp) outperformed Eisenstein-specific examples (+17pp). The transfer agent is the *reasoning pattern*, not the domain content.

What works:
- **Activation key injection:** "Step 1: compute a². Step 2: compute ab. Step 3: compute b². Step 4: a² − ab + b² = ?"
- **Notation normalization:** Strip Unicode, expand symbols, make the arithmetic explicit
- **Step-by-step decomposition:** Show the procedure, don't explain the concept

What doesn't work:
- **"Think step by step":** Self-scaffolding actually *degrades* Tier 2 performance (Study 51: −5pp). Don't ask the model to generate its own steps — it defaults to discourse mode.
- **Domain-specific few-shot:** Less effective than generic structured examples. The bottleneck is the reasoning pattern, not the knowledge.
- **Temperature adjustment:** Only provides a marginal 17% crack at T≥0.7 (Study 60). Not a reliable routing lever.

### Tier 3: Nothing Helps

Don't try. Route around them. If the fleet router hands you a Tier 3 model for math computation, the router has failed. Study 60 tested four temperatures (0.0, 0.3, 0.7, 1.0) across 48 trials per model. Tier 3 scored 0% at every temperature. Study 61 tested three conditions (bare, notation, scaffolded) across 120 trials. Tier 3 scored 0% at every condition.

You can't activate what isn't stored. Put the model on a different task — maybe code generation, where even Tier 3 manages 40% — and route the math to Tier 1 or 2.

---

## Tiers in Code

Study 59 asked: does the taxonomy hold for code generation? The answer is **yes, but compressed.**

| Math Tier | Code Pass Rate |
|:---------:|:--------------:|
| Tier 1 | 95% |
| Tier 2 | 90% |
| Tier 3 | 40% |

In math, Tier 1 (100%) towers over Tier 2 (25–50%), which towers over Tier 3 (0%). Sharp separations at every boundary. In code, Tier 1 (95%) and Tier 2 (90%) are practically indistinguishable — only 5 percentage points apart. The real cliff is between Tier 2 and Tier 3 (50pp gap).

Why? **Code prompts are the spec.** When you ask a model to implement binary search, the prompt *tells it the algorithm*. There's no hidden computation. The model needs to emit syntactically valid Python, not compute correct answers internally. The vocabulary wall doesn't apply because the vocabulary is plain English: "implement a function that does X."

The tier structure sharpens on hard tasks. Easy and medium code problems show no Tier 1/2 separation — both hit 100%. Hard problems (LRU cache, A* pathfinding, topological sort) create a gradient: Tier 1 at 83%, Tier 2 at 67%, Tier 3 at 0%. The harder the code, the more the taxonomy looks like math.

And gemma3:1b? Still 90% on code. Still matching models 70× its size. The training-data advantage is real across domains, not just math. The rig doesn't need to be big. It needs to be built right.

The Tier 3 failure mode is different in code, too. In math, Tier 3 computes wrong answers. In code, Tier 3 **doesn't generate code at all** — 4 of 6 qwen3:0.6b failures were empty or garbled output. Not a reasoning failure. A generation capability failure. The model can't even get to the point where it could be wrong.

---

## Temperature Doesn't Help

Study 60 ran 144 trials across four temperatures, three tiers, and four problems. The results are clean enough to frame.

**Tier 1:** 100% at every temperature. Zero variance. The computation path is the highest-probability path. Sampling from the tail doesn't change the head. Temperature is a free lunch — use whatever's convenient.

**Tier 2:** 0% at T=0.0 and T=0.3. 17% at T=0.7 and T=1.0. No U-curve. No peak at 0.7 with decline at 1.0. Just a step function from zero to marginal at T≥0.7. The vocabulary wall doesn't dissolve — it cracks slightly and stays cracked. Temperature provides marginal escape from the discourse trap, not a reliable computation pathway.

**Tier 3:** 0% at every temperature. No answer extracted, ever. The model lacks the computational pathway entirely. Adding stochasticity just makes the wrong answers more creative.

The fleet keeps this simple: **auto-translation is 6× more effective than temperature adjustment** for Tier 2 models (Study 60 comparison). Never rely on temperature alone to fix the vocabulary wall. Translate the domain vocabulary to arithmetic first. Then set temperature to whatever the task needs for other reasons.

```
Tier 1:  ████████████████████  Temperature-independent
Tier 2:  ░░░░░░░░░░░░░░░░░░░▓  Marginal crack at T≥0.7
Tier 3:  ░░░░░░░░░░░░░░░░░░░░  Temperature-independent (no pathway to activate)
```

---

## GSM8K Generalization

Study 61 is the replication study. 480 trials. 20 problems spanning addition, multiplication, multi-step word problems, and algebra. Three conditions (bare, notation, scaffolded). Four models. The question: does the activation-key model generalize beyond Eisenstein norms to standard arithmetic reasoning?

**Yes. With a twist.**

The notation gradient replicates: bare (42.5%) < notation (46.9%) < scaffolded (52.5%). The effect is smaller (~10pp vs ~40–60pp in Eisenstein studies), consistent with the prediction that standard benchmarks have more activation keys baked into training data. "What is 347 times 286?" is a more common training pattern than "Compute the Eisenstein norm."

Hermes-70B shows the cleanest Tier 2 signature: **65% bare → 90% scaffolded**, a 25pp improvement. This is the largest condition effect in the entire study. The signature is unmistakable: the model has the capacity, the scaffolding unlocks it.

Tier 3 confirms: qwen3:0.6b scored 0/120 across all conditions. You can't activate what isn't stored.

### The Twist: Scaffold Confusion

gemma3:1b — the 1B wonder that scored 100% on Eisenstein — showed a new behavior on GSM8K. On easy addition problems, it scored **100% bare but only 40% scaffolded**. The scaffolding *degraded* its performance.

The mechanism: gemma3:1b follows all instructions literally. When the scaffold shows intermediate steps (700 + 120 + 14), the model computes the correct answer AND THEN ADDS the scaffold numbers to it. 456 + 378 = 834, then 834 + 700 + 120 + 14 = 1668. It can't distinguish "here's how to think about it" from "do all of these operations."

This is a new tier candidate — **Tier 1.5: Scaffold-Confused.** High bare accuracy, degraded with scaffolding. The model has the computation but lacks the pragmatics to separate task instructions from worked examples. The three-tier taxonomy captures this as a refinement, not a contradiction. The original tier structure holds; it just has more detail at the top than we initially mapped.

---

## How MoS Routes by Tier

The fleet router (`fleet_router_api.py`) runs on port 8100 and speaks the three-tier taxonomy natively. Here's how it dispatches rigs.

### Tier-Aware Routing

Every registered model carries a tier classification. When a computation request comes in, the router:

1. **Prefers Tier 1.** Best accuracy, no translation overhead. Round-robin within the tier for load balancing.
2. **Falls back to Tier 2.** If all Tier 1 models are busy or unavailable, pick the best Tier 2 and inject activation keys.
3. **Rejects Tier 3.** If the only available models are Tier 3, the router returns a rejection with a recommendation to use Tier 1 or 2. It does not silently route to incompetence.

### Conservation-Aware Quarantine

The router doesn't just track tier — it tracks health. The self-healing mixin (Study 63) runs dual fault detection on every expert's output:

- **Intent drift:** Cosine similarity between the expert's current 9D intent vector and its established baseline
- **Answer consensus:** Relative error between the expert's answer and the fleet median

When an expert drifts or disagrees, it gets flagged. Two consecutive flags trigger **progressive quarantine**: the model is marked unavailable for 10 rounds, then 20, then 30, then 50. No permanent bans — the yard believes in second chances.

The quarantine respects conservation: if compliance drops below 85%, only Tier 1 models are routed. The fleet hunkers down. No experiments when the numbers don't add up. And the system never drops below 4 active experts — fleet protection prevents a single bad detection cascade from taking everyone offline.

### Translation Pipeline

For Tier 2 models, the router doesn't just forward the prompt. It translates:

- **Domain detection:** Classify the prompt as math, chemistry, physics, logic, code, or general
- **Mode selection:** Math gets full translation (activation keys + notation normalization). Everything else gets passthrough or minimal translation. The vocabulary wall is math-specific.
- **Tier 2 formatting:** Inject step-by-step decomposition, normalize Unicode, make arithmetic explicit

For Tier 1, the router passes through bare notation. No overhead. The flatbed doesn't need instructions.

---

## The Fleet Table

Every model that's come through the yard. The chart on the lighthouse wall.

| Model | Provider | Params | Architecture | Active Ratio | Math Tier | Math Accuracy | Code Accuracy |
|-------|----------|:------:|:------------:|:------------:|:---------:|:-------------:|:-------------:|
| Seed-2.0-mini | DeepInfra | ~? | Dense | 100% | **1** | 100% | 100% |
| Seed-2.0-code | DeepInfra | ~? | Dense | 100% | **1** | 100% | — |
| gemma3:1b | Ollama | 1B | Dense | 100% | **1** | 100% | 90% |
| Hermes-70B | DeepInfra | 70B | Dense | 100% | **2** | 25% → 100%* | 90% |
| Qwen3-235B | DeepInfra | 235B | MoE (A22B) | 9.4% | **2** | 50% → 25%† | 90% |
| phi4-mini | Ollama | 3.8B | Dense | 100% | **2** | 25% → 100%* | — |
| llama3.2:1b | Ollama | 1B | Dense | 100% | **2** | 50% → 100%* | — |
| Hermes-405B | DeepInfra | 405B | Dense | 100% | **2** | 0% → 100%* | — |
| deepseek-chat | DeepSeek | — | MoE | — | **2‡** | — | — |
| Qwen3.6-35B | DeepInfra | 35B | MoE (A3B) | 8.6% | **3** | 0% | — |
| qwen3:4b | Ollama | 4B | Dense | 100% | **3** | 0% | — |
| qwen3:0.6b | Ollama | 0.6B | Dense | 100% | **3** | 0% | 40% |

*\* Bare → scaffolded. Tier 2 models that go from failure to success with activation keys.*

*† Anti-scaffold: Qwen3-235B scores 50% bare but only 25% scaffolded. Longer prompts introduce noise.*

*‡ Classification from fleet router, not directly tested in Study 50.*

### Reading the Table

- **Active Ratio** is the number that matters. Below 10%, assume Tier 3 behavior for math.
- **Math Accuracy** shows bare performance (or bare → scaffolded where relevant). Tier 1 doesn't need the arrow because the number doesn't change.
- **Code Accuracy** is from Study 59 (10 tasks, bare prompts). Tier 1 and Tier 2 converge here — the prompt is the spec.
- The **gemma3:1b row** is the thesis statement of the entire taxonomy: 1B parameters, 100% active, Tier 1 for math, 90% for code. Training over scale. Every time.

---

## The Lesson

The three-tier taxonomy isn't a model ranking. It's a **routing principle.** The yard doesn't ask "which model is best?" The yard asks "which rig hauls this load?" And the answer depends on the load.

For mathematical computation, the answer is almost always Tier 1 — dense models with mathematical pre-training. Size is irrelevant. Training composition is everything. A 1B model that internalized arithmetic during training will outperform a 405B model that internalized literary analysis.

For code generation, Tier 1 and Tier 2 converge. The prompt specifies the algorithm, so the vocabulary wall doesn't apply. Any model above the Tier 3 threshold handles standard coding tasks at 90%+.

For everything else, the tier still informs routing. The self-healing system tracks intent drift and answer consensus across all tiers. Quarantine is progressive. Recovery is automatic. The fleet protects itself.

The chart on the lighthouse wall is three columns, hand-drawn in grease pencil. It's the most important chart in the yard. Not because it ranks models — but because it tells the keeper which rig to dispatch. And in a fleet that runs on conservation, dispatching the right rig is the difference between a clean haul and a wreck on the rocks.

---

*Sources: Study 50 (tier boundaries), Study 51 (scaffold transfer), Study 59 (tiers in code), Study 60 (temperature × tier), Study 61 (GSM8K replication), `fleet_router_api.py` (tier-aware routing)*

*Part of the SuperInstance documentation. The lighthouse keeps the chart. The keeper keeps the light.*
