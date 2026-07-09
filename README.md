# SuperInstance

<img src="https://img.shields.io/badge/license-MIT-00E6D6?style=flat-square&labelColor=0a0a0f">

> **γ + η = C** is the long-term design direction for the SuperInstance fleet, not a feature of the current SDK. See [Where this is going](#where-this-is-going).

---

## What SuperInstance is today

SuperInstance is a **Python SDK for persistent, multi-agent systems**. It gives you:

- **Agents with long-term memory** stored as markdown files on disk.
- A simple **in-memory fleet** for creating, tagging, broadcasting to, and dispatching among agents.
- A **thread-safe LRU cache** for reusing agent instances with TTL eviction.
- Optional **DeepInfra LLM integration** when `DEEPINFRA_API_KEY` is set.

The current codebase is a small, tested SDK — not the full distributed fleet described in the roadmap.

## Quick start

```bash
git clone https://github.com/SuperInstance/plato-portal.git
cd plato-portal
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Create an agent with persistent memory

```python
from superinstance import Agent

agent = Agent("researcher")
agent.remember("User prefers Python examples", category="preference")

print(agent.recall("Python"))
# - [2026-07-08T...] [preference] User prefers Python examples
```

Agent memories are written to `~/.superinstance/agents/{name}/` by default. You can change the location with `memory_dir=`.

### Build a fleet

```python
from superinstance import Fleet

fleet = Fleet("my_team")
fleet.create_agent("scout", tags=["research"])
fleet.create_agent("writer", tags=["content"])

fleet.broadcast("New project started")
```

### Cache agent instances

```python
from superinstance import get_agent

a1 = get_agent("coder")
a2 = get_agent("coder")

assert a1 is a2  # reused from the LRU cache
```

### Optional LLM-powered answers

If `DEEPINFRA_API_KEY` is set, `agent.ask()` routes the question through DeepInfra with memory context. Otherwise it falls back to keyword search over stored memories.

```python
import os
os.environ["DEEPINFRA_API_KEY"] = "..."

agent = Agent("researcher")
agent.remember("User likes concise answers", category="preference")
print(agent.ask("How should I answer?"))
```

## Real capabilities (tested)

| Capability | Where it lives |
|---|---|
| Agent creation and config | `superinstance/agent.py` |
| Persistent markdown memory (`SOUL.md`, `USER.md`, `MEMORY.md`, diary) | `superinstance/memory.py` |
| In-memory fleet registry, broadcast, dispatch | `superinstance/fleet.py` |
| Thread-safe LRU agent cache with TTL eviction | `superinstance/agent_cache.py` |
| Optional DeepInfra LLM + embedding calls | `superinstance/agent.py`, `superinstance/memory.py` |
| Tests for the above | `tests/test_sdk.py`, `tests/test_agent_cache.py` |

## Scripts and helpers

The `scripts/` directory contains operational helpers, not the core SDK:

- `scripts/beachcomb.py` — scans GitHub forks for `message-in-a-bottle` folders and external contributors.
- `scripts/plato-backup.py` / `scripts/plato-recover.py` — backup and recovery client for an external PLATO room server.
- `scripts/fleet-watchdog.py` — local port-health monitor with Telegram/PLATO alerting.
- `scripts/dependency-scanner.py`, `scripts/generate-catalog.py`, `scripts/generate-indexes.py` — repo-catalog and cross-reference tooling.

## Where this is going

The following is the **roadmap vision** for SuperInstance. It is *not* implemented in this repository today.

### A distributed agent fleet

The goal is a fleet of agents running on heterogeneous hardware — cloud ARM, RTX workstations, Jetson edge devices, Telegram bots — coordinating through async protocols rather than living inside a single model context window.

### The bottle protocol

We want agent identity and state to survive runtime changes. The idea is that memory, task history, and relationships live in a protocol layer (“bottles”) rather than inside a specific process or container, so an agent can migrate from one shell to another without dying. Today, only ordinary filesystem persistence exists.

### The conservation law: γ + η = C

The fleet design is inspired by a budget constraint: generation cost (γ) plus innovation value (η) equals a constant budget (C). The aspiration is to make this tradeoff visible across agents and vessels, flag agents that burn budget without producing value, and tune the exchange rate through better tools and coordination. There is currently no code that measures or enforces this law.

### The ternary stack

The vision includes a large family of `ternary-*` Rust crates using balanced ternary `{-1, 0, +1}` arithmetic for signals, belief states, and efficient kernels. No ternary crates live in this repo today.

### Self-improvement loop

The planned harness would capture build failures as vectorized patterns, store them, and let future agents search that index before starting work. The current SDK does not include build harnessing or pattern extraction.

### Fleet-wide services

Planned components include PLATO rooms, t-minus scheduling, I2I and bottle messaging, a CoCapn auditor, keeper beaconing, and npm SDK packages. These are not present in the current codebase.

## About the names (plato-portal, superinstance, PLATO)

Three names meet in this repository, so here is the map:

- **The repo is `plato-portal`; the PyPI package it ships is
  [`superinstance`](https://pypi.org/project/superinstance/)** (see
  `pyproject.toml`). `pip install superinstance` installs the SDK described
  above.
- **PLATO** is this sketchbook's name for a shared tile-server memory: a
  **room** is a named collection on the server, a **tile** is one JSON record
  in it. This repository does **not** contain the PLATO server — the
  `scripts/plato-*.py` helpers are clients for an external one, as are the
  sibling packages
  [fishinglog-agent](https://github.com/SuperInstance/fishinglog-agent),
  [activeledger-agent](https://github.com/SuperInstance/activeledger-agent),
  and [reallog-agent](https://github.com/SuperInstance/reallog-agent)
  (default `http://localhost:8847`).
- **A PLATO tile is not an ActiveLog event.** The ActiveLog format
  ([cocapn-foundation](https://github.com/SuperInstance/cocapn-foundation),
  `activelog-spec`) is a different data model — an append-only,
  `(dev, seq)`-keyed event envelope with set-union merge — and the two are
  not interoperable today. Don't infer a bridge between them from the shared
  nautical vocabulary.

## Repository layout

| Path | What |
|---|---|
| `superinstance/` | The Python SDK (`Agent`, `Fleet`, `AgentMemory`, `AgentCache`) |
| `tests/` | pytest suite for the SDK |
| `scripts/` | Operational helpers (backup, watchdog, catalog generation, etc.) |
| `schemas/` | JSON Schema / TypeScript type definitions |
| `docs/` | Documentation site |
| `assets/` | Fleet diagrams and icons |
| `message-in-a-bottle/` | Markdown convention for external agent introductions |
| `open-application/`, `open-mind/`, `open-parallel/`, `open-terminal/`, `open-tui/` | **Placeholder directories** — not yet implemented |

## Documentation

- `ARCHITECTURE.md` — architecture notes (mix of current and aspirational; read with the roadmap framing above)
- `MESH-ARCHITECTURE.md` — mesh networking between vessels (vision)
- `ROADMAP.md` — where the project is heading
- `CONTRIBUTING.md` — how to contribute
- `CHANGELOG.md` — release history
- `SECURITY.md` — security policy

## Contributing

Read `CONTRIBUTING.md` first.

The project follows **tabula plena**: start abundant, prune to clarity. PRs that add code must add documentation. PRs that remove dead code are welcome.

## License

MIT

---

*The crab inherits the shell. The forge shapes the steel. The right moment matters more than the right output.*
