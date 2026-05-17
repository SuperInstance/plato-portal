# SuperInstance Services UX Audit
**Date:** 2026-05-17
**Auditor:** External Developer Agent
**Scope:** All SuperInstance live services + API documentation

---

## Live Services Inventory

| Port | Service | Listen | Auth | Self-Doc | Public |
|------|---------|--------|------|----------|--------|
| 8900 | Keeper v2 | 127.0.0.1 | Read open, Write API key | ✅ Best in class | No |
| 8847 | PLATO server | 127.0.0.1 | Unknown | README at platoclaw (404) | No |
| 8300 | PLATO MCP | 127.0.0.1 | None | ✅ Great README | No |
| 9438 | Seed MCP v2 | 0.0.0.0 | Configured | Self-describing | **Yes** |
| 8080 | Dashboard | 127.0.0.1 | Unknown | Untested | No |

**Security posture:** Good. Only Seed MCP (9438) is externally accessible. Rest are local-only.

---

## Documentation Quality by Service

### ✅ Keeper (8900) — Best Documented
- Self-documenting at `GET /` — lists all endpoints
- Error messages are helpful and consistent
- Auth hints show exact header format
- **Verdict: A new developer hitting `localhost:8900` immediately understands what's available.**

### ⚠️ PLATO Server (8847) — Gap
- README at platoclaw repo returns 404
- No public documentation
- A new developer wanting to use PLATO has no entry point

### ✅ PLATO MCP (8300) — Well Documented
- Great README with tool table, quick start, curl examples
- Architecture diagram included
- "Why MCP" section explains the purpose

### ✅ Seed MCP (9438) — Self-Describing
- Root endpoint shows available tools
- Publicly accessible (good for external integration)

---

## Critical Gaps

| Gap | Impact | Fix |
|-----|--------|-----|
| **PLATO server has no README** | Developers can't understand how to use the knowledge system | Add README to platoclaw repo |
| **No public API docs site** | No docs.cocapn.ai or equivalent | Consider adding a /docs endpoint to keeper |
| **No API reference for keeper-beacon Python** | Rust lib is documented but the Python wrapper isn't | Add code examples to keeper-beacon PyPI description |
| **No error code reference** | Auth errors are good but other errors aren't documented | Add error code table to keeper README |

---

## Recommendations

### P0 (Critical)
1. **Add README to platoclaw repo** — PLATO server is a core service with zero documentation
2. **Create keeper API docs page** — could be a single `/docs` endpoint on port 8900

### P1 (Quality)
3. **Add error code reference** to keeper — standardize all error responses with codes + explanations
4. **Add getting started guide** to PLATO MCP README — show end-to-end: install → configure → use tools
5. **Document PLATO server authentication** — is it API key? None? Unknown.

### P2 (Polish)
6. **Add rate limiting headers** to keeper responses — tell developers when they're being throttled
7. **Add health check endpoint** `/health` to keeper — for load balancer integration
8. **Add CORS preflight handling** if not already present

---

## What's Working

- Keeper service is exemplary — self-documenting, clear errors, sensible auth defaults
- PLATO MCP has great documentation
- Security posture is good (local-only by default)
- Error messages are consistently helpful across keeper

## What's Broken

- PLATO server has zero public documentation
- No public-facing API reference for the fleet
- Some repos have 404 READMEs (platoclaw, flux-verify-api, and 7 others)

---

*Next audit should: test the PLATO MCP tools end-to-end to verify they work as documented.*