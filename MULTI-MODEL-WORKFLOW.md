# Multi-Model Workflow

## Available Models & Their Roles

### z.ai subagents (glm-5.1) — THE WORKHORSE
- **Cost**: ~$0.01-0.05 per task
- **Best for**: Implementation, testing, scanning, bulk work, well-specified tasks
- **Use for**: 90% of all work
- **Limit**: 5 concurrent subagents per session

### kimi-cli (kimi-for-coding) — CREATIVE CODING
- **Cost**: Free (own API key)
- **Best for**: Creative coding, refactoring, code review, finding clever solutions
- **How**: Via tmux session (interactive TTY required)
- **Setup**: `tmux new-session -d -s kimi` → `kimi` → send-keys with task
- **Strength**: Good at exploring codebases, finding patterns, creative refactors

### Claude Code — EXPERT CONSULTANT (USE SPARINGLY)
- **Cost**: $2-5 per session, rate limited (resets 2:30 AM AKDT)
- **Best for**: Architecture decisions, code review, ONE precise edit
- **Rules**: See HARD-RULES.md and CLAUDE-CODE-LESSONS.md
- **NEVER**: Multi-file changes, implementation of known algorithms, data processing

### DeepSeek — TECHNICAL ANALYSIS
- **Cost**: Cheap
- **Best for**: Mathematical proofs, algorithm analysis, technical writing
- **How**: Via z.ai subagent with model="deepseek/deepseek-chat"

### OpenRouter — MODEL ROUTER
- **Cost**: Varies by model
- **How**: Via z.ai subagent with model="openrouter/auto"
- **Use for**: Accessing Seed mini, Nemotron, and other models

## Model Roles by Task Type

| Task | Model | Why |
|------|-------|-----|
| Implement well-known algorithm | z.ai glm-5.1 | Cheap, fast, algorithm is spec'd |
| Creative refactoring | kimi-cli via tmux | Creative, good at finding patterns |
| Architecture decision | Claude Code | Expensive but brilliant opinions |
| Scan 100 repos | z.ai glm-5.1 | Bulk data processing |
| Write research paper | z.ai + DeepSeek | Technical writing, math |
| Beta test | z.ai glm-5.1 | Structured evaluation |
| Creative ideation | Seed mini via OpenRouter | Divergent thinking |
| Reality check | Nemotron via OpenRouter | Grounded, practical thinking |
| Code review (deep) | Claude Code | ONE file, ONE review |
| Code review (quick) | kimi-cli | Fast, creative feedback |
| Fix bug (known cause) | z.ai glm-5.1 | Spec'd fix, just implement |
| Fix bug (mystery) | Claude Code | Needs architectural judgment |

## Kimi-cli via tmux — Standard Pattern

```bash
# 1. Create or reuse a tmux session
tmux new-session -d -s kimi 2>/dev/null || true

# 2. Start kimi if not running
tmux capture-pane -t kimi -p | tail -5 | grep -q "input" || {
  tmux send-keys -t kimi "kimi" Enter
  sleep 3  # wait for startup
}

# 3. Send task
tmux send-keys -t kimi -l -- "Read constraint-synth/constraint_synth/oscillator.py and add PolyBLEP anti-aliasing to sawtooth and square waves"
sleep 0.1
tmux send-keys -t kimi Enter

# 4. Wait for completion (poll every 30s)
sleep 30
tmux capture-pane -t kimi -p | tail -20

# 5. Check if done
tmux capture-pane -t kimi -p | tail -5 | grep -q "input" && echo "DONE" || echo "STILL WORKING"
```

## Seed Mini & Nemotron via subagents

```python
# Seed mini for creative ideation
sessions_spawn(model="openrouter/auto", task="Creative brainstorm: ...")

# Nemotron for realistic thinking  
sessions_spawn(model="openrouter/auto", task="Be brutally realistic: ...")
```

Note: Need to verify OpenRouter access to these specific models. If not available via openrouter/auto, check if z.ai has them or if we need a direct API key.

## Model Fleet (Updated 2026-05-23)

### Tier 1: Workhorse (90% of work)
- **z.ai glm-5.1** — default subagent model. Fast, cheap, solid implementation.
- **deepseek/deepseek-chat** — alternative perspective, good for debugging.

### Tier 2: Creative / Diverse
- **openrouter/auto** — routes to cheapest capable model, good for volume testing
- **kimi-cli** (via tmux) — creative coding, interactive TTY work
- **google/gemma-4-31B-it** — experimental, different training data = different insights

### Tier 3: Heavy Reasoning (sparingly)
- **Claude Code** — architecture opinions only. ONE file per session. Max 1/day.
- **NousResearch/Hermes-3-Llama-3.1-405B** — massive context window. Use when:
  - Need to digest the ENTIRE codebase and reason about cross-cutting concerns
  - Abstract scaling ideas (how does this grow from 1 user to 10,000?)
  - Synthesis across multiple research papers
  - Finding deep patterns that require holding 100K+ tokens in mind

### Flywheel Pattern
```
[Cheap model tests as user] → [finds bugs] → [cheap model fixes] → [different cheap model tests]
         ↑                                                                    ↓
         ←←←←←←←←← [Hermes 405B synthesizes findings] ←←←←←←←←←←←←←←←←←←←←
```

The wheel never stops. Every tester teaches. Every fix teaches. Every synthesis teaches.
