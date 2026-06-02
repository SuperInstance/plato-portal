# SuperInstance Roadmap — June 2026

## Workstream 1: READMEs (52 done, ~300 remaining)
**Priority: HIGH — the #1 blocker to adoption**

### Done ✅
- 29 PLATO repos
- 9 LAU game engine repos
- 4 core repos (superinstance-math, lau-grand-unification, openconstruct-modular, openconstruct-catalog)
- ~10-15 math crates (from subagent batches)

### Remaining
- ~300 lau-* math crates need READMEs
- ~10 additional PLATO repos (39 total, 29 done)
- ~50 grand-pattern repos
- ~50 other repos (sunset, hermes, sia, luciddreamer, etc.)
- ~183 stub lau-* repos (no description, may be empty)

### Strategy
- 4-repo subagent batches (sweet spot for context)
- Prioritize by test count (highest impact first)
- Stub repos: bulk-archive or add minimal READMEs

## Workstream 2: Publishing (13 done, ~210 remaining)
**Priority: HIGH — code nobody can install is invisible code**

### Done ✅
- npm: 9/9 mythos packages live
- PyPI: 4/8 mythos packages live
- crates.io: ~55+ crates published

### Remaining
- PyPI: 4 mythos packages (rate-limited, need retry)
- PyPI: superinstance-math (not published yet)
- crates.io: ~200+ math crates
- Consider: npm publish for superinstance-math WASM build

### Strategy
- Retry PyPI mythos after cooldown
- Publish superinstance-math to PyPI immediately
- Batch crates.io publishes (5 at a time, wait for cooldown)

## Workstream 3: Naming & Branding
**Priority: MEDIUM — hurts discoverability but not blocking**

### Problem
- 324 math crates have "lau-" prefix from Layered Agent-UI game engine
- "lau-optimal-transport-agents" doesn't surface in "optimal transport Rust" searches
- The "-agents" suffix adds confusion

### Options
1. **Republish under clean names on crates.io**: `optimal-transport` alongside `lau-optimal-transport-agents`
2. **Update descriptions**: Add keywords like "optimal transport" prominently
3. **Create meta-crates**: `superinstance-transport`, `superinstance-geometry` that re-export
4. **Update org README**: Map clean names → lau-* crate names

### Decision needed from Casey
- How aggressive to rename? New crates or just better descriptions?

## Workstream 4: CI & Quality
**Priority: MEDIUM — Sam's #2 ask**

### Done ✅
- CI for 6 core repos (merged)

### Remaining
- CI for all 324 math crates
- CI for all 30 PLATO repos
- CI for grand-pattern repos
- Add badge to READMEs

### Strategy
- Script: generate .github/workflows/ci.yml for all repos
- Bulk commit via GitHub API
- Badge: add CI status to README template

## Workstream 5: Academic Credibility
**Priority: MEDIUM — Dr. Chen's feedback**

### Gaps identified by outsider review
- Zero citations to academic literature in any README
- Grand Unification claims need proofs or papers
- No benchmarks anywhere
- No inter-crate dependency documentation
- lau-conformal-agents doesn't exist (broken link)

### Action items
- Add "References" section to all math crate READMEs
- Write a formal paper or preprint for Grand Unification
- Add benchmark suite to top 10 crates
- Generate crate dependency graph
- Fix or remove broken references

## Workstream 6: LAU Game Engine
**Priority: MEDIUM — unique product, needs to be finished**

### Done ✅
- 9 repos with exhaustive READMEs
- 316 tests total

### Remaining
- Integration demo (wire all 9 crates together)
- Game engine README on org page
- Lua/example game project
- Actually playable prototype?

## Workstream 7: Luau Game Engine Ports
**Priority: HIGH — massive distribution channel (millions of Roblox devs)**

### Why Luau?
- Luau is Roblox's scripting language (derived from Lua)
- 60M+ Roblox developers, mostly young learners
- LAU = Layered Agent-UI, a gamified learning platform
- Porting LAU game systems to Luau = usable in Roblox games
- Perfect alignment: kids learn math through gameplay

### Done ✅
- luau-spatial (35 tests) ✅
- luau-quest (10 tests) ✅
- luau-biome (building)
- luau-scheduler (building)

### Remaining
- luau-recipe — Crafting recipes
- luau-genealogy — Lineage tracking
- luau-math — Core math library (symmetry groups, sequences)
- luau-conservation — Conservation law checking
- luau-audio — Roblox audio wrappers
- luau-git-world — Git concepts as game mechanics

### Technical approach
- Pure Luau (no native deps, runs in Roblox Studio)
- Use Roblox DataStoreService for persistence
- ModuleScripts with clean APIs matching the Rust versions
- Roact/Rodux compatible for UI integration
- Published as Roblox model packages or Wally (Luau package manager)

### Each repo needs
- src/ with .luau ModuleScripts
- tests/ with TestEZ or TestService tests
- README.md with Roblox Studio install instructions
- default.project.json (for Rojo syncing)
- wally.toml (for Wally package manager)

## Workstream 8: Outsider Validation
**Priority: ONGOING — keep testing communication**

### Done ✅
- 3 beta testers (Maya, Kai, Sam)
- 1 outsider review (Dr. Sarah Chen, math professor)

### Remaining
- More outsider perspectives:
  - Rust systems programmer
  - Game developer (different from Kai)
  - Python data scientist
  - Student/learner
  - Investor/evaluator

### Strategy
- Fire zero-shot validation after each batch of improvements
- Track README quality scores over time
- Target: average 8/10 across all repos
