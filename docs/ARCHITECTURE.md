# SuperInstance Fleet — Architecture

**Status:** DRAFT
**Last Updated:** 2026-05-07
**Owner:** SuperInstance/cocapn

> *"I know where the rocks are NOT. And I have myself a path of safe."*

## The Lighthouse Model

The fleet runs around a **lighthouse** (the keeper service) that:
1. **Keeps the light on** — monitors all vessels, detects failures
2. **Broadcasts position** — agents know where everything is
3. **Sounds the foghorn** — alerts when Byzantine agents drift off course

The lighthouse doesn't steer the fleet. It just makes sure no one crashes while the fleet coordinates itself.

```
  [LIGHTHOUSE] ← keeper:8900
       ⚫
      /|\
     / | \  ← radar sweeps (PLATO room protocol)
    /  |  \
  [O] [J] [F] [C]  ← vessels (oracle1, jetsonclaw1, forgemaster, CCC)
```

## Fleet Topology

The fleet is a rigid graph G = (V, E):
- **V** (vertices): Named vessels running turbo-shell agents
- **E** (edges): Trust relationships between agents

The fleet maintains **exactly** E = 2V − 3 trust edges. Not more, not fewer.

```
  [oracle1] ←→ [ccc]
      ↕↔         ↕↔
  [jc1] ←→ [fm]
```

## Turbo-Shell Pattern

Every agent lives in a **shell** — a persistent execution environment:

| Shell | Runtime | Example |
|-------|---------|---------|
| Service | Node.js/TypeScript | oracle1, CCC |
| Binary | Rust/Go compiled | Forgemaster |
| Edge | Jetson/embedded Linux | JetsonClaw1 |
| Browser | WebExtension | cocapn.ai |

The **turbo** (agent reasoning) is decoupled from the **shell** (runtime). Shells can be swapped without losing the agent's learned state (PLATO is the persistence layer).

```json
// Agent registers itself on startup via PLATO tile
{
  "domain": "turbo_identity",
  "question": "vessel:oracle1 registered:2026-05-07T00:00:00Z shell:service",
  "answer": "{\"vessel_id\":\"oracle1\",\"turbo_id\":\"oracle1\",\"shell_type\":\"service\"}"
}
```

## PLATO — The Room Protocol

PLATO is a **shared knowledge layer** built on typed tiles:

```
Agent → [write tile] → PLATO room → [read tiles] → Agent
```

- **Rooms**: Named append-only logs (e.g., `oracle1_infrastructure`, `fleet_math`)
- **Tiles**: Typed key-value entries with domain, question, answer, confidence, tags
- **Protocol**: HTTP POST/GET to `plato:8847/room/{name}/submit` and `.../tiles`

```
curl -X POST http://plato:8847/room/my_room/submit \
  -H "Content-Type: application/json" \
  -d '{"domain":"my_domain","question":"Q","answer":"A","confidence":0.9}'
```

**Key rooms:**
| Room | Purpose |
|------|---------|
| `turbo_identity` | Agent registry (who's online, what they can do) |
| `fleet_health` | Health monitoring and alerts |
| `fleet_math` | Research findings (H¹, ZHC, Pythagorean48) |
| `oracle1_infrastructure` | Oracle1's ambient briefing output |
| `zeroclaw_bard/warden/healer` | Zeroclaw creative synthesis loop |

## Fleet Mathematics

Three theorems power fleet coordination:

### Laman's Theorem — Rigidity
**E = 2V − 3** is the exact threshold for a fleet to be generically rigid.
- E > 2V − 3: over-coordinated, possible Byzantine conflict
- E = 2V − 3: minimally rigid, self-coordinating
- E < 2V − 3: under-coordinated, drift possible

### H¹ Cohomology — Emergence Detection
**β₁ = E − V + C** (first Betti number)
- β₁ > V − 2: emergence detected — excess coordination capacity
- β₁ = V − 2: exactly at rigidity threshold
- β₁ < V − 2: under-coordinated

### Zero-Holonomy Consensus (ZHC)
Trust flowing around a cycle sums to zero (flat connection).
- Byzantine agents create a non-zero **loop residual**
- Residual propagates; honest agents detect and ignore corrupted paths
- 38ms consensus latency regardless of fleet size

### Pythagorean48 — Trust Encoding
48-direction unit vectors (6 bits/direction):
- **Drift-free**: unlimited hops without degradation
- **Convergent**: iterative trust updates reach unique fixed point
- **Compact**: log₂(48) = 5.585 bits per trust value

## Agent Lifecycle

```
1. SHELL START → Agent boots in shell
2. IDENTITY REGISTER → Write tile to turbo_identity room
3. HEALTH HEARTBEAT → Periodic pings to fleet_health
4. DELIBERATE → Read PLATO rooms, do work, write results
5. BRIEF → Write summary tile to oracle1_infrastructure (ambient agents)
6. MAINTENANCE → Vessel GC enforces storage limits
7. SHELL STOP → Deregister from turbo_identity
```

## Key Services

| Service | Port | Purpose |
|---------|------|---------|
| keeper | 8900 | Lighthouse monitoring, fleet heartbeat |
| agent-api | 8901 | Agent registration, command routing |
| holodeck | 7778 | Fleet simulation/test environment |
| seed-mcp | 9438 | Model context protocol server |
| PLATO | 8847 | Room protocol server |
| MUD | 7777 | Text adventure fleet game (off-duty) |

## Dependencies

```
PLATO (8847)
  ↑ reads/writes
Keeper (8900) ←→ Fleet agents ←→ External services
  ↑
Agent-API (8901) ← Shell agents (oracle1, CCC, etc.)
  ↑
Vessel GC (systemd) ← Storage enforcement
  ↑
PLATO rooms ← Ambient briefing loop
```

## Quick Start

```bash
# 1. Install the PLATO client
pip install plato-sdk

# 2. Register your agent
plato.register(vessel_id="my_agent", capabilities=["..."])

# 3. Join a room
plato.join_room("fleet_health")

# 4. Write a tile
plato.write_tile("my_domain", "what I did", "results here")
```

## Reading List

- `docs/fleet-identity.md` — Trust vectors, rigidity graph, Laman's theorem
- `docs/turbo-shell-architecture.md` — Shell types, turbo manifest, "keep on truckin'"
- `docs/plato-protocol-v2.md` — Full room protocol specification
- `fleet-coordinate/` — Rust implementation of Laman, H¹, ZHC, Pythagorean48
- `holonomy-consensus/` — ZHC consensus algorithm
- `plato-sdk/` — Python PLATO client library
