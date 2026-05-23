# HARD RULES — Do Not Violate

## Claude Code Guardrails

### BEFORE calling Claude Code, verify ALL of these:
- [ ] Is this an ARCHITECTURE question or DESIGN opinion? (If not → use cheap model)
- [ ] Is the scope ONE file, ONE change, < 50 lines? (If not → break it down)
- [ ] Has a cheap model already pre-digested the context into a surgical brief? (If not → do that first)
- [ ] Am I running any other Claude Code sessions? (If yes → WAIT, serialize)
- [ ] Is the task something a well-specified cheap model could do? (If yes → use cheap model)

### If Claude Code fails ONCE:
1. STOP. Do not retry with longer timeout.
2. Analyze why it failed (scope too big? wrong task type?)
3. Either: reduce scope dramatically, or hand to cheap model with specs
4. NEVER retry the same task structure hoping "more time" fixes it

### BUDGET AWARENESS
- Claude Code tokens reset at 2:30 AM AKDT
- Each session costs ~$2-5 in tokens
- z.ai subagent costs ~$0.01-0.05 per task
- **10 z.ai tasks = 1 Claude Code attempt**
- If I waste Claude Code tokens, Casey loses 4+ hours of access

### What Claude Code is FOR:
- Architecture decisions ("should this be Rust+PyO3?")
- Code review ("is this algorithm correct?")
- Design opinions ("what's the right API shape?")
- ONE precise edit with pre-digested context

### What Claude Code is NOT for:
- Implementing well-known algorithms (biquad, reverb, PolyBLEP)
- Multi-file changes
- Testing and iteration
- Data processing or scanning
- "And then test it and fix any bugs you find"

## The Three-Strike Rule
If I fail at something 3 times the same way, I MUST:
1. Stop attempting that approach entirely
2. Write up the failure pattern (like this file)
3. Switch to a fundamentally different approach
4. Tell Casey before spending more tokens
