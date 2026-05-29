# Forgemaster Extraction Plan

**Repo:** `SuperInstance/forgemaster`
**Last commit:** 2026-05-26
**Total top-level directories:** 91
**Empty/stub directories:** 36
**Active directories (with files):** 55

---

## Executive Summary

The forgemaster repo has become a monolithic catch-all with 91 directories — 36 of which are completely empty (stub placeholders). The goal is to slim it down to a **streamlined, single-purpose onboarding & agent shell** that:

1. Downloads and onboards to a new user's git account
2. Connects to their keeper API (OpenClaw or custom keeper)
3. Comes pre-loaded with PLATO knowledge rooms
4. Enables flow-state with agents across devices
5. Is plug-and-play useful for anyone

---

## Extraction Table

| # | Directory | What It Is | Action | New Repo / Notes | Type | Priority |
|---|-----------|-----------|--------|-----------------|------|----------|
| 1 | **forgemaster/** | Core Python package — constraint-aware build orchestration | **STAY** | Core forgemaster library | Core | — |
| 2 | **forgemaster-shell/** | OpenClaw agent shell config (AGENTS, SOUL, IDENTITY, etc.) | **STAY** | The default shell experience | Core | — |
| 3 | **plato/** | Preference Learning & Adaptive Target Optimization (18 sub-projects) | **STAY** (bundled) | Pre-loaded knowledge rooms | Core | — |
| 4 | **docs/** | Forgemaster documentation (134 files) | **STAY** | Project docs | Core | — |
| 5 | **tests/** | Integration tests | **STAY** | Test suite | Core | — |
| 6 | **integration_tests/** | Integration test configs | **STAY** | Test suite | Core | — |
| 7 | **scripts/** | Utility scripts | **STAY** | Build/setup helpers | Core | — |
| 8 | **memory/** | Agent memory/daily logs (192 files) | **STAY** | Runtime memory | Core | — |
| 9 | **skills/** | Agent skill definitions | **STAY** | Agent capabilities | Core | — |
| 10 | **templates/** | Project templates | **STAY** | User-facing templates | Core | — |
| 11 | **flux/** | Flux language ecosystem — compilers, runtimes, ISAs (363 files) | **EXTRACT** | `SuperInstance/flux` | Language/toolchain | P1 |
| 12 | **fleet/** | Fleet management code (477 files) | **EXTRACT** | `SuperInstance/fleet` | Agent infrastructure | P1 |
| 13 | **research/** | Research papers & notes (314 files) | **EXTRACT** | `SuperInstance/research` | Archive | P1 |
| 14 | **experiments/** | Proof repos for constraint theory (170 files) | **EXTRACT** | `SuperInstance/experiments` | Archive | P1 |
| 15 | **flywheel/** | Experiment runner/state (208 files) | **EXTRACT** | Merge into `experiments` | Archive | P2 |
| 16 | **products/** | Clock sync, metronome products (53 files) | **EXTRACT** | `SuperInstance/products` | Tools | P2 |
| 17 | **guard/** | Constraint enforcement & safety DSL (49 files) | **EXTRACT** | `SuperInstance/guard` | Library | P1 |
| 18 | **constraint/** | Constraint theory implementations (17 files) | **EXTRACT** | `SuperInstance/constraint-theory` | Library | P1 |
| 19 | **ct-bridge-npm/** | Node.js constraint theory bridge (10 files, has pkg.json + tests) | **EXTRACT** | `SuperInstance/ct-bridge-npm` | NPM package | P1 |
| 20 | **ct-demo/** | Constraint theory Rust demo (11 files, has Cargo.toml + tests) | **EXTRACT** | `SuperInstance/ct-demo` | Demo project | P2 |
| 21 | **cocapn/** | Cocapn AI web platform (32 files) | **EXTRACT** | `SuperInstance/cocapn` | Platform | P1 |
| 22 | **swarm/** | Distributed swarm intelligence (29 files) | **EXTRACT** | `SuperInstance/swarm` | Agent infrastructure | P1 |
| 23 | **vessel/** | Walkable Wikipedia concept (36 files) | **EXTRACT** | `SuperInstance/vessel` | Application | P2 |
| 24 | **sonar/** | Vision/perception systems (17 files) | **EXTRACT** | `SuperInstance/sonar` | Library | P2 |
| 25 | **deadband/** | Signal processing (12 files) | **EXTRACT** | `SuperInstance/deadband` | Library | P2 |
| 26 | **architectures/** | Deployment architecture proposals (15 files) | **EXTRACT** | Merge into `docs` or `research` | Archive | P2 |
| 27 | **legacy/** | Superseded projects (9 files) | **EXTRACT** | `SuperInstance/legacy` | Archive | P3 |
| 28 | **agent/** | Agent frameworks (4 files) | **EXTRACT** | Merge into `fleet` or standalone | Library | P2 |
| 29 | **demo/** | Three-agent demo (29 files) | **EXTRACT** | `SuperInstance/demo` | Demo | P3 |
| 30 | **frontends/** | Frontend code (1 file) | **EXTRACT** | `SuperInstance/frontends` | Application | P3 |
| 31 | **editors/** | Editor configs (3 files) | **EXTRACT** | `SuperInstance/editor-configs` | Config | P3 |
| 32 | **bootcamp/** | Training materials (18 files) | **EXTRACT** | `SuperInstance/bootcamp` | Docs | P3 |
| 33 | **blog-posts/** | Blog content (11 files) | **EXTRACT** | `SuperInstance/blog-posts` | Content | P3 |
| 34 | **captains-log/** | Captain's log entries (11 files) | **EXTRACT** | `SuperInstance/captains-log` | Content | P3 |
| 35 | **papers/** | Research papers (2 files) | **EXTRACT** | Merge into `research` | Archive | P3 |
| 36 | **proposals/** | Project proposals (2 files) | **EXTRACT** | Merge into `docs` | Archive | P3 |
| 37 | **portfolio/** | Portfolio site (8 files) | **EXTRACT** | `SuperInstance/portfolio` | Application | P3 |
| 38 | **snapkit/** | SnapKit project (4 files) | **EXTRACT** | `SuperInstance/snapkit` | Tool | P3 |
| 39 | **eisenstein/** | Eisenstein integer math (1 file) | **EXTRACT** | `SuperInstance/eisenstein` | Library | P3 |
| 40 | **warp-room/** | Already extracted (points to SuperInstance/warp-room) | **DELETE** | Already moved, just a stub | — | P1 |
| 41 | **playtest-results/** | Test results (4 files) | **EXTRACT** | Merge into `experiments` | Archive | P3 |
| 42 | **gpu-kernels/** | GPU kernel code (7 files) | **EXTRACT** | `SuperInstance/gpu-kernels` | Library | P2 |
| 43 | **llvm-xconstr/** | LLVM cross-constraints (5 files, has tests) | **EXTRACT** | `SuperInstance/llvm-xconstr` | Toolchain | P2 |
| 44 | **marine-gpu-edge/** | (0 files, stub) | **ARCHIVE** | Empty placeholder | — | P3 |
| 45 | **autodata-integration/** | AutoData integration (3 files) | **EXTRACT** | `SuperInstance/autodata-integration` | Tool | P3 |
| 46 | **comms-experiment/** | Comms experiment (2 files) | **EXTRACT** | Merge into `experiments` | Archive | P3 |
| 47 | **state/** | State management (1 file) | **EXTRACT** | Merge into `fleet` | Library | P3 |
| 48 | **tools/** | Utility tools (20 files) | **EXTRACT** | `SuperInstance/tools` | Tools | P2 |
| 49 | **migrations/** | DB migrations (1 file) | **STAY or MERGE** | If related to core, keep | Core | — |
| 50 | **discussions/** | Discussion files (1 file) | **ARCHIVE** | Merge into `docs` | Archive | P3 |
| 51 | **dojo/** | Dojo (1 file) | **EXTRACT** | `SuperInstance/dojo` | Application | P3 |
| 52 | **tri-quarter-toolbox/** | Toolbox (1 file) | **EXTRACT** | `SuperInstance/tri-quarter-toolbox` | Tool | P3 |
| 53 | **message-in-a-bottle/** | Message protocol (3 files) | **EXTRACT** | Merge into `swarm` | Protocol | P3 |
| 54 | **vocabularies/** | Vocabularies (1 file) | **EXTRACT** | Merge into `plato` | Data | P3 |

---

## Empty Directories (36) — Archive or Delete

These have **zero files** and are stub placeholders. All should be removed or archived.

| Directory | Notes |
|-----------|-------|
| AIR | Empty stub |
| OpenShell | Empty stub |
| acg_protocol | Empty stub |
| ai-forest | Empty stub |
| automerge | Empty stub |
| collective-ai | Empty stub |
| commit-predictor | Empty stub |
| device-router | Empty stub |
| dodecet-encoder | Empty stub |
| grand-synthesis | Empty stub |
| i2i-protocol | Empty stub |
| intent-directed-compilation | Empty stub |
| intent-inference | Empty stub |
| lighthouse-cli | Empty stub |
| marine-gpu-edge | Empty stub |
| memory-crystal | Empty stub |
| micro-onnx | Empty stub |
| multi-model-adversarial-testing | Empty stub |
| negative-knowledge | Empty stub |
| openarm | Empty stub |
| openhuman | Empty stub |
| openshell-compatibility-audit | Empty stub |
| pbft-rust | Empty stub |
| polyformalism-a2a-js | Empty stub |
| polyformalism-a2a-python | Empty stub |
| polyformalism-thinking | Empty stub |
| quality-gate-stream | Empty stub |
| repos | Empty stub |
| sana-wm | Empty stub |
| signal-chain | Empty stub |
| spreader-tool | Empty stub |
| sunset-ecosystem | Empty stub |
| tile-memory | Empty stub |
| training-throttle | Empty stub |
| triplet-miner | Empty stub |
| turbovec | Empty stub |

**Action:** Delete all 36 empty directories. If any represent planned future work, create an issue tracker entry instead.

---

## What STAYS in Forgemaster Core

The slimmed-down repo retains:

```
forgemaster/           # Core Python package
forgemaster-shell/     # Agent shell (AGENTS, SOUL, IDENTITY, etc.)
plato/                 # Knowledge rooms (pre-loaded)
docs/                  # Documentation
tests/                 # Test suite
integration_tests/     # Integration tests
scripts/               # Setup/build scripts
memory/                # Agent memory runtime
skills/                # Agent skills
templates/             # Project templates
migrations/            # DB migrations (if core-related)
```

**Plus root files:** README.md, .gitignore, setup.py / pyproject.toml, etc.

---

## Extraction Priority

### P1 — Do First (Active, substantial, clear boundaries)
1. **flux/** → Own repo (363 files, language ecosystem)
2. **fleet/** → Own repo (477 files, agent infrastructure)
3. **research/** → Own repo (314 files)
4. **experiments/** → Own repo (170 files)
5. **constraint/** → Own repo (mathematical foundation)
6. **guard/** → Own repo (safety DSL)
7. **ct-bridge-npm/** → Own repo (NPM package with tests)
8. **cocapn/** → Own repo (web platform)
9. **swarm/** → Own repo (swarm intelligence)
10. **warp-room/** → Already extracted, just delete the stub

### P2 — Do Next (Active, moderate size)
11. **products/** → Own repo
12. **vessel/** → Own repo
13. **sonar/** → Own repo
14. **deadband/** → Own repo
15. **gpu-kernels/** → Own repo
16. **llvm-xconstr/** → Own repo
17. **tools/** → Own repo
18. **ct-demo/** → Own repo
19. **flywheel/** → Merge into experiments
20. **architectures/** → Merge into docs or research

### P3 — Last Pass (Small, niche, or archival)
21. **legacy/** → Archive repo
22. **demo/** → Demo repo
23. **blog-posts/** → Content repo
24. **captains-log/** → Content repo
25. **bootcamp/** → Training repo
26. **portfolio/** → App repo
27. Everything else small → Merge or extract as needed

### Cleanup
28. Delete all 36 empty directories
29. Delete warp-room stub

---

## Recommended Extraction Process

```bash
# For each directory to extract:
cd /tmp
mkdir -p $REPO_NAME && cd $REPO_NAME
git init

# Copy from forgemaster with history
cd /tmp/forgemaster-audit
git subtree split --prefix=$DIR_NAME -b $REPO_NAME-branch
git clone /tmp/forgemaster-audit --branch $REPO_NAME-branch /tmp/$REPO_NAME-full

# Create on GitHub
gh repo create SuperInstance/$REPO_NAME --private
cd /tmp/$REPO_NAME-full
git remote add origin git@github.com:SuperInstance/$REPO_NAME.git
git push -u origin main

# Then remove from forgemaster
cd /tmp/forgemaster-audit
git rm -rf $DIR_NAME
git commit -m "chore: extract $DIR_NAME to SuperInstance/$REPO_NAME"
```

---

## Dependency Notes

- **flux** depends on **constraint** (constraint theory is core to flux language)
- **guard** depends on **constraint** (safety DSL built on constraint theory)
- **ct-bridge-npm** wraps **constraint** Python package
- **fleet** and **swarm** may share protocols — check for cross-imports
- **forgemaster** (core) imports from **plato** — this stays bundled
- **products** (clock sync) relates to **fleet** — may belong together
- **agent** is tiny (4 files) — likely best merged into **fleet**
- **message-in-a-bottle** is tiny (3 files) — likely best merged into **swarm**

---

## Summary Statistics

| Category | Count |
|----------|-------|
| Core (STAY) | 10 directories |
| Extract to own repo | ~25 directories |
| Merge into other repos | ~5 directories |
| Empty (delete) | 36 directories |
| Already extracted (delete stub) | 1 directory |
| **Total** | **91** |

After extraction: **forgemaster goes from 91 directories to ~10**, focused purely on the onboarding, shell, and PLATO experience.
