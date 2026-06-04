# The Harness — Production-Grade Pipeline v0.1

## The Problem
We can build 20 modules in a day. They all compile, tests pass, READMEs look good. But they're all 3.0-3.5/5. None are production-ready.

## The Insight
The bottleneck isn't building. It's the last 20% — the same 20% every time:
1. Configurable thresholds (not hardcoded)
2. Real data source adapters
3. Persistence/export
4. Error handling (not silent failures)
5. Integration examples with real output
6. Unhappy-path testing
7. Trend analysis (not just snapshots)

## The Harness: A Repeatable Pipeline

### Phase 1: Build (what we're good at)
- Budget → Profile → Detect → Report architecture
- Unit tests on happy path
- Show-don't-sell README
- Push to GitHub branch

### Phase 2: Bug Fix (what we just started doing)
- Run thorough QA with adversarial tester
- Fix every found bug
- Add tests for each bug fix
- Re-verify all tests pass

### Phase 3: Production Hardening (the missing piece)
For each module, apply this checklist:

| Check | Status | Notes |
|-------|--------|-------|
| All thresholds configurable | ☐ | Named constants → constructor params |
| Real data source adapter | ☐ | API client / callback hook / stdin parser |
| Persistence layer | ☐ | JSON save/load, SQLite optional |
| Export formats | ☐ | JSON, Markdown, Prometheus metrics |
| Error handling | ☐ | No silent failures. Log or surface everything. |
| Unhappy-path tests | ☐ | Empty input, corrupted data, edge cases |
| Integration example | ☐ | Full end-to-end with real-looking output |
| Alerting/action | ☐ | Not just detect — help fix |
| Trend analysis | ☐ | Compare current to historical |
| Version bump + republish | ☐ | Semantic versioning |
| CI pipeline | ☐ | Automated test on push |
| Changelog | ☐ | What changed, why |

### Phase 4: Validate
- Install from registry (pip/npm/cargo)
- Run through the integration example
- Verify output matches README claims
- Test with real-ish data (not just unit test fixtures)

### Phase 5: Document the Process
- What took longer than expected?
- What was mechanical vs required thinking?
- What can be templatized for next module?
- What did we learn that changes the Build phase?

## The Meta-Goal

Each module we take through this harness makes the harness better. The first one (conservation-guardian) will take effort. The second should be 50% faster because we have templates. The third 50% faster again. By module 5, the harness IS the product — and anyone can use it.

## Champion Module: conservation-guardian (Python)

- Best API design (3.5/5)
- Already on PyPI
- Widest potential audience
- DAG analyzer is genuinely novel
- Easiest path to real users

## Champion Run: conservation-guardian v0.1.0 → v0.2.0

### Time: ~20 minutes total

### What Was Mechanical (template-worthy):
- Custom exception hierarchy
- CI/CD (ruff + mypy + pytest, 3 Python versions)
- CHANGELOG / CONTRIBUTING boilerplate
- Example scripts
- Export format serialization (Prometheus, Slack)

### What Required Thinking:
- Adapter `extract_samples()` API design
- GenericAdapter dot-notation field resolution
- Profiler.compare() trend thresholds
- Thread safety decisions

### Key Lessons for Next Module:
1. Start with .gitignore (clean tree from the start)
2. Design adapter interface before writing adapters (base class saves repetition)
3. Check PyPI for existing version before re-publishing
4. Trend analysis should be its own module, not on Profiler
5. Thread safety needs explicit design, not just GIL reliance

### Acceleration Curve (predicted):
- Module 1 (conservation-guardian): 20 min
- Module 2: ~12 min (templates save mechanical work)
- Module 3: ~8 min (patterns are dialed in)
- Module 5+: ~5 min (harness IS the product)

---

## Success Metric
A module is production-grade when:
1. A stranger can pip/npm/cargo install it
2. Import it, feed it real data
3. Get actionable output in < 5 minutes
4. Trust the output enough to act on it

---

*This document IS the product. Every module we ship is evidence that it works.*
