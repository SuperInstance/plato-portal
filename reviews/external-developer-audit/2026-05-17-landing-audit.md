# SuperInstance Landing Experience Audit
**Date:** 2026-05-17
**Auditor:** External Developer Perspective (Oracle1 Agent)
**Scope:** GitHub org page + cocapn.ai website

---

## Part 1: GitHub Org — https://github.com/SuperInstance

### First Impression
The profile reads: *"Commercial fisherman in Sitka, Alaska → Building AI that learns how I fish. Edge ML on Jetson, privacy-first fleet learning. Practical Open-source tools."*

Disarming and memorable. A fisherman building fleet AI creates intrigue. But the mismatch between profile (fisherman) and projects (constraint theory, formal verification, custom ISA) raises questions.

**Org README: genuinely excellent.** Three-shell architecture with ASCII diagrams, working code sample (`pip install plato-sdk`, `PlatoClient()`), clear learning loop explanation. Best onboarding asset in the org.

### Problems Identified

| Issue | Severity | Detail |
|-------|----------|--------|
| **1,646 repos** | P0 | Firehose. No pinned repos. New visitor has zero idea where to start. |
| **No org-level pinned repos** | P0 | Even the canonical `SuperInstance/SuperInstance` is buried in the list. |
| **"SuperInstance" is a person, not an org** | P1 | Personal GitHub account. Brand identity is fuzzy — is this a company, research project, or hobby? |
| **4 followers** | P1 | Low social proof for 1,646 repos. Skeptics will bounce. |
| **No CONTRIBUTING.md anywhere** | P1 | Zero guidance for external contributors. |
| **No community channels** | P1 | No Discord, Matrix, or Discussions pinned. |
| **No CI badges on most repos** | P2 | Only keeper-beacon and flux-isa show working CI. Rest could be dead. |

### Repo Name Analysis

| Repo | Clarity | Verdict |
|------|---------|---------|
| `constraint-theory-papers` | ✅ High | Self-explanatory |
| `fleet-stack` | ✅ High | Clear deployment repo |
| `plato-sdk` | ✅ High | "SDK" suffix makes intent obvious |
| `forgemaster` | 🟡 Moderate | Metaphor explained in description |
| `penrose-memory` | ❌ Low | "Penrose" requires domain knowledge |
| `flux-isa` | ❌ Low | Requires knowing FLUX project |
| `plato` | ❌ Low | Name alone means nothing |

**Overall: mixed.** Core repos are clear. Specialized ones assume pre-knowledge.

### What's Missing for Getting Started

- No "Start Here" link from the org page (the main README has one, but you have to find it)
- No skeleton READMEs for ~15% of repos (complete 404)
- No `good first issue` labels
- No release tags showing version history

---

## Part 2: Website — cocapn.ai vs superinstance.ai

**⚠️ cocapn.ai returns 404.** Live site is superinstance.ai.

### What's Good
- Hermit crab metaphor is effective for multi-agent specialization
- "Try It — 3 Seconds" section is genuinely creative (paste prompts into any chatbot)
- Fleet vessel cards give personality to agents
- Live stats (20 rooms, 288 tiles, 4 vessels) signal real project

### What's Confusing

| Issue | Severity | Detail |
|-------|----------|--------|
| **Branding split** | P0 | cocapn vs SuperInstance. Logo is lighthouse (Cocapn). Company name seems to be Cocapn. Domain is superinstance.ai. fleet.cocapn.ai is the API. Three brand identities. |
| **E12 vs Float16** | P1 | "Two autopilots" analogy is interesting but math lands cold. Why should I care? |
| **Conservation law** | P1 | `(γ + H = 1.283 − 0.159 · ln(V))` presented as breakthrough but γ/H/V unexplained. Looks impressive but unhelpful. |
| **No "build your own agent"** | P1 | Site explains fleet philosophy but gives no path to build/start one. |
| **404 on cocapn.ai** | P0 | Confuses first-time visitors. What's the canonical domain? |

---

## Priority Fix List

1. **Pin 4-6 repos** on org page — fleet-stack, plato-sdk, keeper-beacon, flux-isa, SuperInstance/SuperInstance
2. **Fix cocapn.ai** — redirect to superinstance.ai or publish the landing page
3. **Add org-level profile README** — lighthouse logo, link to flag repos, explain brand
4. **Add CONTRIBUTING.md** to top 5 repos
5. **Create single-page architecture overview** at `github.com/SuperInstance/.github` or SuperInstance/SuperInstance/docs/ARCHITECTURE.md
6. **Add skeleton READMEs** to 9 repos with zero docs
7. **Consolidate brand** — pick one identity (Cocapn or SuperInstance) and be consistent

---

*Next audit should focus on: does the "Try It - 3 Seconds" section actually work for a new user?*