# Claude Code Usage Patterns — Failure Analysis

## The Core Problem
Claude Code is expensive ($$$), slow, and rate-limited. We've wasted multiple expensive sessions getting SIGKILL'd or producing descriptions instead of code. This document captures the higher-level patterns so we stop repeating the same TYPE of mistake.

## Failure Catalog

### Failure Type 1: "Kitchen Sink Prompt" ❌
**What happened**: Asked Claude Code to do PolyBLEP + biquad filter + reverb + stereo output + playground fixes in ONE prompt.
**Result**: SIGKILL (timeout). Zero output.
**Root cause**: Too many features = too many file reads + edits = exceeds context/time budget.

### Failure Type 2: "Retry Same Task" ❌
**What happened**: Retried the kitchen sink prompt with longer timeout.
**Result**: SIGKILL again. Zero output.
**Root cause**: Same problem, more time doesn't fix scope.

### Failure Type 3: "Break Into 3 Tasks, Still Too Big" ❌
**What happened**: Broke into PolyBLEP, biquad+reverb, playground — 3 separate Claude Code sessions.
**Result**: Biquad described the design but didn't write code. PolyBLEP produced nothing (exited 0, no output). Playground hit rate limit.
**Root cause**: Even "one feature" is too big if it requires reading + understanding + designing + implementing + testing a file.

### Failure Type 4: "Big Data Processing" ❌
**What happened**: Asked Claude Code to process 130 repos, scan files, audit code.
**Result**: Timeouts, partial output.
**Root cause**: Claude Code is NOT a data processor. It's an architect.

### Failure Type 5: "Architecture Analysis" ✅
**What happened**: Asked Claude Code to READ code and WRITE a design document.
**Result**: Brilliant output — "enemy is Python overhead", Rust+PyO3 recommendation, identified _pebble_game() as stub.
**Why it worked**: Read-only input, text output, no file modifications, scoped analysis.

## The Higher Structure

### Claude Code's Sweet Spot
- **READ** existing code → **THINK** → **WRITE** a design/architecture/analysis document
- **READ** a single file → **EDIT** it with a precise, small change (< 50 lines)
- **DESIGN** an API, then hand implementation to cheaper models

### Claude Code's Kill Zone
- Implementing multiple features
- Reading many files to make changes
- Any task involving "and then test it"
- Data processing / scanning / bulk operations
- Tasks that require > 3 file edits

### The Right Pipeline

```
1. CHEAP MODEL (z.ai subagent, $0.001/1K tokens)
   → Scan codebase, gather context, summarize files
   → Create focused briefs with EXACT file paths, line numbers, and specs

2. CLAUDE CODE ($$$, slow but brilliant)
   → Receive a crafted brief: "Here's the file, here's what to change, here's the math"
   → Output: precise edit OR design document
   → ONE task per session, ONE file change maximum

3. CHEAP MODEL (z.ai subagent)
   → Take Claude's design and implement it
   → Run tests, fix errors, iterate
   → Report results back
```

## Concrete Rules

### Rule 1: Never send Claude Code more than ONE file to edit
If you need changes to oscillator.py, the prompt should be:
"Read oscillator.py. Change the sawtooth generator to use PolyBLEP. Here's the algorithm: [exact pseudocode]. Only modify the sawtooth() method."
NOT: "Add PolyBLEP to oscillator.py, also add a filter, also add reverb."

### Rule 2: Pre-digest the context
Before calling Claude Code, a cheap model should:
- Read the target file
- Extract the relevant section
- Identify exact line numbers
- Write the algorithm spec
Claude Code should receive a surgical brief, not a research task.

### Rule 3: Claude Code = Architect, Not Builder
- ✅ "Design the biquad filter coefficients for a lowpass at cutoff X with resonance Y"
- ✅ "Review this algorithm for correctness"  
- ✅ "Write the mathematical spec for Schroeder reverb delay lengths"
- ❌ "Implement PolyBLEP and test it and render a WAV"
- ❌ "Fix the synth and the playground and add stereo"

### Rule 4: If the output is CODE, cheaper models can do it
Claude Code's advantage is REASONING about code, not WRITING code. If you already know exactly what code to write (algorithm is specified), any model can write it. Use Claude Code when you DON'T know what to write and need architectural judgment.

### Rule 5: Rate limits are real
Claude Code hit "You've hit your limit" after 3 concurrent sessions. NEVER run multiple Claude Code sessions in parallel. Serialize them.

## What Should Have Happened

For the synth improvements, the correct workflow:

```
1. z.ai subagent: Read oscillator.py, summarize sawtooth/square generators, 
   write PolyBLEP algorithm spec with exact line numbers

2. z.ai subagent: Implement PolyBLEP from the spec, write to file, test

3. If stuck: Ask Claude Code ONE question: "Why is my PolyBLEP implementation 
   producing artifacts at 8kHz?" with the specific code snippet

4. z.ai subagent: Read synth.py, identify where to add filter, implement 
   biquad from RBJ cookbook formulas (well-known, no architectural judgment needed)

5. z.ai subagent: Implement reverb from Schroeder topology (well-known algorithm)

6. z.ai subagent: Test all three, render WAV, report artifacts remaining
```

This would have cost ~$0.05 in z.ai tokens instead of ~$5+ in Claude Code tokens, and would have actually PRODUCED the code instead of timing out.

## Meta-Pattern
**The mistake is treating Claude Code like a senior developer who can handle a sprint's worth of work. It's not. It's an expert consultant who gives brilliant 15-minute opinions. Use it for opinions, not implementation.**
