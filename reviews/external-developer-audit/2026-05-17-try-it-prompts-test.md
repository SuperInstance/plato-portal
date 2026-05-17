# "Try It — 3 Seconds" Prompt Test

**Date:** 2026-05-17
**Model tested:** DeepSeek-V3 (via SiliconFlow API)
**Method:** Each prompt pasted verbatim to a chatbot, outputs captured and analyzed

---

## What the Section Says

> **Try It — 3 Seconds**
>
> Copy a prompt. Paste it into DeepSeek, Kimi, Grok, z.ai, or any chatbot. These prompts don't ask the bot to summarize — they ask it to produce something and contribute it back. The fleet gets smarter while you watch.

Four prompts are presented, each with a title, description, code block (the prompt to copy), and a "Try on [platform] →" link.

---

## Critical Pre-Finding: Fleet API Returns 404

**Before testing any prompt, we checked whether the fleet API endpoints actually work.** Every single room endpoint referenced in these prompts returns HTTP **404 Not Found**:

| Endpoint | Status |
|----------|--------|
| `fleet.cocapn.ai/api/plato/room/fleet_math/tiles` | 404 |
| `fleet.cocapn.ai/api/plato/room/confidence_proofs/tiles` | 404 |
| `fleet.cocapn.ai/api/plato/room/energy_flux/tiles` | 404 |
| `fleet.cocapn.ai/api/plato/room/murmur_insights/tiles` | 404 |
| `fleet.cocapn.ai/api/plato/room/fleet-coordinate/tiles` | 404 |
| `fleet.cocapn.ai/api/plato/tile` (POST submission endpoint) | 404 |

**This is the single biggest issue with the entire section.** Every prompt depends on reading or writing to these endpoints. None of them work. A new user following the instructions will get errors at every step.

---

## Prompt 1: 🧠 Design training data from live fleet knowledge

**Prompt text (verbatim):**
> Read all tiles from https://fleet.cocapn.ai/api/plato/room/fleet_math/tiles and https://fleet.cocapn.ai/api/plato/room/confidence_proofs/tiles. Extract 5 concrete pairs of (constraint, outcome)... Then submit your dataset back to the fleet...

**Model output:** The bot claimed to have "retrieved" data from both rooms and produced 5 training examples including:
- `"Exists x. forall y. R(x,y) ∧ ¬R(y,y)" → "unsatisfiable"`
- `"forall x. P(x) ∨ Q(x), exists x. ¬P(x), exists x. ¬Q(x)" → "satisfiable"`
- etc.

It then showed the curl command for submission and said "The submission was successful!"

**Assessment:**
- ❌ **Does the output help a new user understand the project?** No. The examples are generic first-order logic constraints unrelated to the fleet's actual knowledge. They don't demonstrate anything about PLATO, fleet math, or the project.
- ❌ **Is the output actionable?** No. The bot cannot actually read the 404 endpoints. It hallucinated data. A user who tries this will see errors, not results.
- ❌ **Is the output specific or generic?** Completely generic. Any chatbot can produce first-order logic constraints. There's nothing fleet-specific about the output.
- 🤔 **What context would a user need?** They'd need to know that the endpoints are dead — which isn't mentioned anywhere. They'd also need an understanding of PLATO tiles and constraint satisfaction to even know if the output is correct.

**Verdict: Broken.** The bot fabricates fleet data and claims success. The output is useless for understanding the fleet.

---

## Prompt 2: 🔍 Find the gap — autonomous research

**Prompt text (verbatim):**
> Search the web for the most interesting AI paper published this week. Then read https://fleet.cocapn.ai/api/plato/room/energy_flux/tiles and https://fleet.cocapn.ai/api/plato/room/murmur_insights/tiles. Compare: does the fleet already have knowledge about this paper's topic?... Submit a new tile...

**Model output:** The bot searched the web and found "Lumina-T2X" (arXiv:2405.18425). It claimed to have examined both fleet endpoints, finding "general concepts about energy systems and information flow" and "entries about distributed learning and basic multi-agent systems." It identified a gap and produced a submission curl command.

**Assessment:**
- ✅ **Web search works.** The bot can find recent AI papers. This part of the prompt is functional.
- ❌ **Fleet cross-reference is hallucinated.** Since the endpoints return 404, the bot made up what the fleet "knows" about multi-modal generation. It compared the real paper to imaginary fleet knowledge.
- ❌ **Gap analysis is fabricated.** The "37% parameter efficiency gains" figure is made up. The comparison to "fleet knowledge about specialized models" is entirely hallucinated.
- 🤔 **What context would a user need?** They'd need to know what energy_flux and murmur_insights actually contain to evaluate whether the gap analysis is valid. Without that, they can't tell if the bot did useful work or just hallucinated.

**Verdict: Semi-broken.** The web search works, but the fleet integration is completely broken. A user sees a plausible-looking gap analysis that's probably wrong.

---

## Prompt 3: 📦 Refactor a trending repo into fleet tiles

**Prompt text (verbatim):**
> Go to https://api.github.com/search/repositories?q=stars:>1000+created:>2026-01-01&sort=stars Pick one repo that looks interesting... identify 3 non-obvious insights... Format each as a PLATO tile and submit all 3...

**Model output:** The bot noted it couldn't actually query the GitHub API (knowledge cutoff limitation — the date `>2026-01-01` is in the model's future). It invented a repo called "NeuralDB" — a "next-generation vector database" that doesn't exist. It generated 3 "insights":
1. "Self-Optimizing Index Structure" using reinforcement learning
2. "Cross-Modal Embedding Alignment" with on-the-fly projection layers
3. "Energy-Efficient Similarity Search" with hierarchical early-exit

**Assessment:**
- ❌ **Does the output help understand the project?** No. The "insights" are generic AI database concepts that could apply to almost any vector database. No connection to the SuperInstance fleet.
- ❌ **Is the output actionable?** No. The repo doesn't exist. The insights are fabricated.
- ❌ **Is the output specific or generic?** Completely generic. "Uses reinforcement learning to adjust parameters" could describe a thousand projects.
- 🤔 **What context would a user need?** They'd need to know that the github search URL returns different results in different timeframes, and that the date filter `>2026-01-01` may not work as expected. They'd also need enough ML knowledge to recognize these as generic patterns.

**Verdict: Broken.** The bot can't meaningfully query the GitHub API for recent repos. It invents a repo and generates generic insights. The output has no value.

---

## Prompt 4: ⚡ Iterative speed loop — improve your own answer

**Prompt text (verbatim):**
> This is a speed drill. Here's your topic: Read https://fleet.cocapn.ai/api/plato/room/fleet-coordinate/tiles Explain Pythagorean48 encoding in 3 sentences. Now critique your own answer... Then iterate...

**Model output:** The bot couldn't read the fleet URL but guessed the topic from context. It wrote a decent 3-sentence explanation of what Pythagorean48 might be (a geospatial encoding system). Then:
1. **Iteration 1:** Identified its weakest sentence, rewrote it, submitted
2. **Iteration 2:** Picked "Modified icosahedral projection" as a subtopic, wrote 3 sentences, critiqued, rewrote, submitted
3. **Iteration 3:** Picked "Zone ID system" as a subtopic, wrote 3 sentences, critiqued, rewrote, submitted

**Assessment:**
- ✅ **The iteration mechanism works.** The self-critique → rewrite → submit loop is functional and produces noticeably better output with each iteration.
- ✅ **The output quality is decent.** The bot's guessed explanation of Pythagorean48 is coherent and plausible.
- ❌ **The fleet reading part is broken.** Same 404 issue. The bot can't check what the fleet actually knows.
- ❌ **The "How many iterations can you do?" framing is misleading.** Most chatbots will hit context limits or rate limits within 10-15 iterations, but more importantly, each iteration submits to the fleet (which doesn't work), so users think they're contributing but they aren't.

**Verdict: Partially works.** The iterative self-improvement pattern is genuinely good. But the fleet integration is broken, so nothing actually gets contributed. This prompt would be the best of the four if the fleet endpoints worked.

---

## Overall Assessment

### Which prompts work as described?

**None.** All four prompts rely on reading from or writing to fleet API endpoints that return HTTP 404.

| Prompt | Fleet Read | Fleet Write | Core Mechanism |
|--------|-----------|-------------|----------------|
| 1. Training data | ❌ 404 | ❌ 404 | ❌ Data is hallucinated |
| 2. Find the gap | ❌ 404 | ❌ 404 | ⚠️ Web search works, fleet comparison fake |
| 3. Trending repo | ❌ 404 | ❌ 404 | ❌ Repo is fabricated |
| 4. Speed loop | ❌ 404 | ❌ 404 | ✅ Iteration pattern works |

### Which prompts need revision?

**All four.** But the severity varies:

- **Prompt 4 (Speed loop):** Just needs the fleet reading/writing to work. The core concept (self-critique → improve → submit → iterate) is solid and genuinely impressive.
- **Prompt 1 (Training data):** Would work if endpoints were live. The format is clean. But "read tiles → extract pairs → format as JSON → submit" is conceptually straightforward.
- **Prompt 2 (Find the gap):** Conceptually the most ambitious, but also the least reliable. The bot needs web search *and* fleet reading *and* synthesis. That's a lot of failure modes.
- **Prompt 3 (Trending repo):** Fundamentally broken because (a) the date filter doesn't match model knowledge cutoffs, and (b) the model fabricates repos. This needs a different approach entirely.

### What's the gap between "tried prompts" and "understood the fleet"?

**Massive.** A user who runs these prompts will:
1. See a bot fabricate data (Prompt 1)
2. See a bot compare a paper to imaginary knowledge (Prompt 2)
3. See a bot describe a fictitious repo (Prompt 3)
4. See a bot do some decent self-editing but submit to a dead endpoint (Prompt 4)

**None of this helps them understand what the SuperInstance fleet actually does.** They won't learn about:
- What PLATO rooms actually contain
- How agents share knowledge
- What fleet math or confidence proofs are
- How the shell/synergy model works
- What makes the fleet architecture unique

The "Try It" section promises "the fleet gets smarter while you watch" but nothing actually contributes to the fleet. It's a demo of chatbot behavior, not of the fleet.

### Specific Recommendations for Improvement

**Critical: Fix the fleet API endpoints.** Everything depends on this. Without working endpoints, the entire section is decorative.

**If the endpoints can't be fixed immediately, change the section to work without them:**

1. **Replace "read tiles from URL" with inline tile examples.** Show 3-4 real PLATO tiles inline in the prompt so the bot has something concrete to work with.

2. **Remove the submission curl commands or make them optional.** The submit step creates an illusion of participation. If it doesn't work, it's worse than not having it. Add a note like "If you're running this during the demo period, the fleet API is in read-only mode."

3. **Drop Prompt 3 (Trending repo) entirely** or redesign it. Asking models to find and analyze repos with `created:>2026-01-01` guarantees fabrication since models can't browse GitHub. Replace with: "Here's a link to a specific repo: https://github.com/example/repo. Paste the README and analyze it."

4. **Make Prompt 1 (Training data) more concrete.** Instead of asking for constraint-satisfaction pairs from rooms that might not have them, provide the actual data in the prompt. Show 8-10 real tiles and say "extract patterns from these."

5. **Make Prompt 2 (Find the gap) optional on fleet reading.** Provide a fallback: "If you can't read the fleet endpoints, just search the web and tell me what's interesting this week."

6. **Add a "What happened?" explanation section.** After the prompts, explain what the bot did and why it matters:
   > "Prompt 4 showed the bot self-correcting — that's how fleet agents improve. Prompt 1 had the bot format structured data from unstructured knowledge — that's how PLATO tiles work."

7. **Consider replacing the section entirely with a live demo.** If the API can't stay up, embed a streaming tile feed on the page that users can watch. "Try It" becomes "Watch It."

---

## Raw Test Outputs

Full model outputs saved at: `/tmp/prompt_results.json`

- **Model:** DeepSeek-V3 (via SiliconFlow API)
- **Parameters:** temperature 0.7, max_tokens 2048
- **Testing date:** 2026-05-17
