# Universal Sequencer Architecture v2 — Addendum

> **Why this document exists:** The v1 vision document was written with three agent perspectives (Builder, User, Adversary), and the synthesis was *close* to the right model — but it was still thinking in MIDI wire-format terms. The channel model used "bank switching via CC 0/32, MIDI 2.0 UMP, multi-file merge" to solve the capacity problem. The timeline was a piano roll with extra tracks. This document strips out the MIDI-thinking and replaces it with a **node-instance architecture** where MIDI is only an import/export bridge.

**Date:** 2026-06-15  
**Status:** Supersedes v1 channel model. Retains v1's adversarial critique as valid (MIDI wire format limitations) but rejects v1's "add more channels" solution.

---

## 1. Correction: The Channel is a Node

### 1.1 The Core Shift

v1 said: *"2 million channels via CC 0/32, MIDI 2.0 UMP, multi-file merge."*

That's still MIDI-thinking. It assumes the problem is *how many MIDI channels we can multiplex onto a wire*. It's not.

A **channel** in the Universal Sequencer architecture is a **node instance**. Not a MIDI port. Not a CC stream. A living computational entity that exists in the sequencer's tensor embedding space. The wire format restrictions of MIDI are irrelevant because `.mid` is just an import/export bridge — the sequencer never thinks in MIDI internally.

### 1.2 Node Schema

Every channel/node is defined by a 4-part schema:

```json
{
  "id": "esp32-lab-01",
  "channel": 0,                       // logical index in embedding space
  "inputs": {                          // what this node reads
    "sampled": ["hall_sensor", "temp_sensor_A0"],
    "setpoints": ["actuator_D3_target"],
    "external": ["alarm_broadcast"]
  },
  "parameters": {
    "sample_rate_hz": 100,
    "pin_map": { "A0": "temperature", "D3": "actuator" },
    "wifi_ssid": "fleet_mesh",
    "firmware_hash": "sha256:a1b2c3..."
  },
  "transform": {
    "type": "esp32_firmware",
    "entry": "loop()",
    "flashed": true,
    "runtime": "freertos"
  },
  "outputs": {
    "stream": ["temperature:C", "actuator_position:rad"],
    "status": ["online", "temp_min", "temp_max", "uptime_s"],
    "events": ["threshold_crossed", "fault"]
  }
}
```

This is NOT a MIDI track. It's a **graph node** that happens to produce and consume time-series data. The sequencer routes data between these nodes at runtime.

### 1.3 Examples

**ESP32 Temperature Sensor (physical device):**

```json
{
  "id": "greenhouse-esp-01",
  "channel": 42,
  "inputs": {
    "setpoints": ["target_temp_C", "alarm_threshold_C"],
    "control": ["reset"]
  },
  "parameters": {
    "sample_rate_hz": 50,
    "pin_map": { "A0": "temp_probe_1", "A1": "humidity_probe" },
    "wifi_ssid": "fleet_mesh",
    "ota_url": "https://fleet-firmware.internal/esp32-greenhouse-v2.bin"
  },
  "transform": {
    "type": "esp32_firmware",
    "flashed": true
  },
  "outputs": {
    "stream": ["temp_C:float32", "humidity_pct:float32"],
    "status": ["online", "firmware_version"]
  }
}
```

**Stock API Feed (data source node):**

```json
{
  "id": "polygon-io-primary",
  "channel": 100,
  "inputs": {
    "control": ["symbols", "rate_limit_ms"]
  },
  "parameters": {
    "api_endpoint": "https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/minute/",
    "rate_limit_per_min": 300,
    "symbols_default": ["AAPL", "TSLA", "NVDA"]
  },
  "transform": {
    "type": "api_poller",
    "interval_ms": 60000,
    "auth": "token_ref"
  },
  "outputs": {
    "stream": ["price:float64", "volume:uint64", "timestamp_ns:int64"],
    "events": ["new_candle", "gap_up", "gap_down"]
  }
}
```

**Puppet Joint (actuator node):**

```json
{
  "id": "marionette-left-arm-shoulder",
  "channel": 12,
  "inputs": {
    "position_target": ["x_deg", "y_deg", "z_deg"],
    "speed": ["interpolation_ms"]
  },
  "parameters": {
    "servo_pins": { "x": 5, "y": 6, "z": 7 },
    "angle_limits": { "x": [-45, 45], "y": [-30, 30], "z": [0, 180] },
    "smoothing": "cubic_ease"
  },
  "transform": {
    "type": "servo_controller",
    "pwm_freq_hz": 50,
    "flashed": false
  },
  "outputs": {
    "stream": ["actual_x_deg:float32", "actual_y_deg:float32", "actual_z_deg:float32"],
    "status": ["online", "stall_detected"]
  }
}
```

### 1.4 Node Registration (Discovery)

Nodes register with the sequencer via a discovery protocol — not static channel assignments:

```
Node: "I'm online. My id is esp32-01. Here's my schema."
Sequencer: "I see you. Assigning channel 42. Here are your inputs."
Node: "Acknowledged. Streaming at 50 Hz."
```

This happens over:
- **WiFi/mesh** for ESP32-class devices
- **WebSocket** for API/data-source nodes
- **UD/UD** for local subprocess nodes
- **Plug-and-detect** for USB-connected hardware

The sequencer maintains a registry: every node's current schema, state, and routing. No manual MIDI channel assignment. No bank switching.

---

## 2. Correction: Dependency Graphs, Not Piano Rolls

### 2.1 The Real Representation

The Universal Sequencer is a **directed graph**, not a flat piano roll. Each node (channel) is a vertex. Edges are data dependencies — inputs flowing from one node's outputs to another's inputs.

```
┌─────────┐   temp_C   ┌──────────────┐   setpoint   ┌────────────┐
│ ESP32-01 ├───────────▶│ Thermostat   ├─────────────▶│ ESP32-01   │
│ (sensor) │   humidity │ Logic Node   │              │ (actuator) │
└─────────┘            └──────┬───────┘              └────────────┘
                              │ alarm_event
                              ▼
                       ┌──────────────┐
                       │ Dashboard    │
                       │ Alert Node   │
                       └──────────────┘
```

Time is one axis of this graph. Every edge carries:
- **Latest value** (current state)
- **Time series** (history window, configurable length)
- **Metadata** (sample rate, units, quality flags)

### 2.2 What Was "Piano Roll" Becomes Graph Projection

When the sequencer exports to `.mid` format, it **projects** the graph onto a flat timeline:

- Each node's output stream becomes a **track** (or bank-switched channels)
- Edge relationships become **meta-events** (not channel mappings)
- The graph structure is lost in the flat projection

This is lossy — you can't reconstruct the full graph from a `.mid` export without the `.nail` schema. That's by design. The `.mid` file is a **time-slice visualization**, not the canonical representation.

### 2.3 Cycle Detection and Feedback Loops

The graph engine must detect and handle cycles:

- **Positive feedback loop:** Sensor reads temperature → heater turns on → temperature rises → sensor reads higher temperature. The engine needs to detect this and either serialize the loop (one node updates per pass) or converge to a fixed point.
- **Intended cycles:** A puppetry joint that reads its own position to compute velocity-based damping. This is valid — the engine should support it with an explicit `feedback: true` flag and per-sample iteration limit.
- **Broken cycles:** Sensor → Actuator → Sensor without damping → oscillation. The engine flags this as a warning and suggests adding a damping node.

Cycle handling is part of the graph compilation step, not runtime detection.

---

## 3. Correction: Physical Devices Are First-Class Channels

### 3.1 The Old View

In v1, a physical device like an ESP32 is a "data source" that emits MIDI events. You squirt its sensor readings into a DAW track, and somehow the DAW talks back.

### 3.2 The Corrected View

The ESP32 **is** a channel node. The sequencer:

1. **Flashes firmware** to it (OTA or USB)
2. **Negotiates parameters** (sample rate, pin map, calibration curves)
3. **Reads its output stream** as channel data in real time
4. **Writes setpoints back** to close the loop
5. **Monitors its health** (online, warm, faulted)

The device runs its own local loop — reading sensors, applying transforms, driving actuators. The sequencer doesn't micromanage every sample. It orchestrates the **sync pulse** — telling the device "run your loop at speed X" and reading back summary data at the negotiated rate.

### 3.3 Flashing Workflow

```
Sequencer: "I have firmware v2.1 for device type 'greenhouse-sensor'."
ESP32: "I'm running v1.8."
Sequencer: "Upgrading now..." [binary push]
ESP32: "Flashed. Reboot -> online."
Sequencer: "Parameter negotiation..."
ESP32: "I support 10-200 Hz sample rate, 4 analog pins, 3 digital."
Sequencer: "Set sample_rate=100, pin_map={'A0':'temp','A1':'humidity'}."
ESP32: "Acknowledged. Streaming."
```

### 3.4 Parameter Negotiation

The device tells the sequencer what it can do. The sequencer configures within device limits. This is not MIDI SysEx trivia — it's a structured capability exchange:

```json
// Device capabilities (sent on connect)
{
  "device_class": "esp32-s3-greenhouse",
  "firmware_version": "2.1.0",
  "capabilities": {
    "sample_rates_hz": [1, 10, 25, 50, 100, 200],
    "analog_pins": 4,
    "digital_pins": 3,
    "output_streams": ["temperature:C", "humidity:pct", "light:lux"],
    "control_inputs": ["target_temp_C", "reset"],
    "wifi": true,
    "ota": true
  }
}
```

### 3.5 Close-the-Loop

The sequencer can write setpoints back to the device:

```
Sequencer -> ESP32: "Set target_temp_C = 26.5"
ESP32 -> Sequencer: "Acknowledged."
...seconds later...
ESP32 -> Sequencer: "temp_C=26.4, target_reached=true"
```

This turns the ESP32 from a "sensor" into an **actuator node** — a full participant in the dependency graph.

### 3.6 Device-as-Channel Lifecycle

```
┌─────────┐    ┌──────────┐    ┌─────────┐    ┌───────────┐    ┌──────────┐
│ DISCOVER │───▶│ CONFIGURE│───▶│ STREAM  │───▶│ RECONFIGURE│───▶│ DISCONN │
└─────────┘    └──────────┘    └─────────┘    └───────────┘    └──────────┘
     │              │              │               │               │
     │ device       │ params       │ data          │ new params    │ gone
     │ announces    │ set by       │ flowing       │ set by        │ offline
     │ presence     │ sequencer    │               │ sequencer     │
```

Every device must be able to reconnect and resume. The sequencer holds last-known state and replays it on reconnection.

---

## 4. Correction: The Two Interfaces

### 4.1 Why Two?

v1 assumed one interface — the DAW piano roll. A human edits tracks. Everyone sees the same thing.

In reality:
- **Agents** need to see everything: graph topology, signal routing, transfer functions, performance metrics, error rates. This is the **mixer board**.
- **Humans** need a dashboard: "camera tracking OK, puppet joints nominal, lighting on scene 4, stock feed green, ESP32-#1 running warm." Alerts only when something breaks.

### 4.2 Agent Mixer View

The agent sees the **full dependency graph**. This is the real interface:

```
┌─────────────────────────────────────────────────┐
│  SEQUENCER ORCHESTRATOR — AGENT MIXER VIEW      │
├─────────────────────────────────────────────────┤
│                                                   │
│  ┌──────┐   ┌──────────┐   ┌──────────┐        │
│  │CAM   │──▶│ CV to    │──▶│ Puppet   │        │
│  │node  │   │ joint    │   │ joints   │        │
│  └──────┘   └──────────┘   └──────────┘        │
│                          │                       │
│                          ▼                       │
│                ┌──────────────────┐              │
│                │ Lighting sync    │              │
│                │ (delay = frame)  │              │
│                └──────────────────┘              │
│                                                   │
│  Stale: [none]     Routing: [graph]     Score: 0.92 │
│  Active channels: 14/64    Throughput: 340 ev/s  │
└─────────────────────────────────────────────────┘
```

Key properties:
- **Editable:** The agent can reroute edges, insert transform nodes, change parameters
- **Measurable:** Every edge shows latency, data rate, error rate
- **Searchable:** Nodes are embedded in vector space — find by semantic similarity
- **Compilable:** The graph compiles to a runtime schedule (which nodes run in which order, at which cadence)

### 4.3 Human Dashboard View

The human sees a **projected status board**:

```
┌─────────────────────────────────────────────────┐
│  SEQUENCER — HUMAN DASHBOARD                     │
│  Project: "Thursday Livestream"                  │
├─────────────────────────────────────────────────┤
│                                                   │
│  🟢 Camera Tracking     OK    (0.12s latency)    │
│  🟢 Puppet Joints       Nom   (all 18 joints)    │
│  🟡 Lighting Scene 4    OK    (warn: bulb 3)     │
│  🔴 Stock Feed          DOWN  (reconnecting...)   │
│  🟢 ESP32-#1 (temp)     Warm  (28.4°C, 50Hz)     │
│  🟢 ESP32-#2 (humidity) OK    (72%, 25Hz)        │
│                                                   │
│  [Last alert: Stock feed reconnecting — 12s ago]  │
│  [Routing: Auto (orchestrator)]                   │
│  [Override → agent mixer]                        │
└─────────────────────────────────────────────────┘
```

The human does **not** touch the graph unless something breaks. The orchestrator agent handles routing by default.

### 4.4 When the Human Opens the Hood

Three situations where the human drops into agent mixer view:

1. **Failure:** A node goes down. The human needs to see the graph to find the broken edge.
2. **Composition:** The human wants to add a new subsystem (e.g., attach a new ESP32 with air quality sensor). They see the graph, choose where to route its output.
3. **Routing changes:** "Route the ESP32 temperature through the Kalman filter node before it reaches the dashboard."

In all cases, the agent orchestrator provides suggestions: "I'd route it here. The latency impact is +2ms. Confirm?"

### 4.5 Where the Orchestrator Agent Sits

```
┌──────────────┐      discovery/         ┌──────────────┐
│  HUMAN       │◀───── alerts            │  DASHBOARD   │
│  (dashboard) │      status             │  (projected) │
└──────────────┘                         └──────────────┘
       ▲                                       ▲
       │  "mute ESP32 alarm"                   │  status
       ▼                                       │
┌──────────────────────────────────────────────────────┐
│           ORCHESTRATOR AGENT                         │
│  - Routes graph edges (auto by default)               │
│  - Compiles graph to runtime schedule                 │
│  - Monitors health, triggers alerts                   │
│  - Provides override suggestions to human             │
│  - Embeds all node state in vector space              │
└──────────────────────────────────────────────────────┘
       ▲                                       ▲
       │  parameter set                         │  graph topology
       ▼                                       │
┌──────────────┐                         ┌──────────────┐
│  NODES       │◀──── routed edges──────▶│  DEPENDENCY  │
│  (ESP32s,    │                         │  GRAPH       │
│   APIs,      │                         │  ENGINE      │
│   transforms)│                         │              │
└──────────────┘                         └──────────────┘
```

---

## 5. Correction: Tensor Spreadsheet

### 5.1 The Old Concept

v1 described a spreadsheet where "columns = MIDI channels/CC streams" and "cells are time-indexed tensors." This was still a MIDI-centric view — the columns were MIDI concepts, not node concepts.

### 5.2 The Corrected View

Columns = **nodes** (channels). Rows = **time steps** (in the embedding space, not MIDI ticks). Cells = **values** that can be scalars, vectors, dependent formulas, or meta-events.

```
         │  ESP32-01   │ Polygon-API │ Puppet-Arm │ Formula   │
         │  temp_C     │ price       │ x_deg      │ temp_avg  │
─────────┼─────────────┼─────────────┼────────────┼───────────┤
T=0      │  22.1       │  185.32     │  -12.4     │ =AVG(A0:C0)│
T=1      │  22.3       │  185.40     │  -11.8     │           │
T=2      │  22.0       │  185.15     │  -10.2     │           │
T=3      │  22.4       │  185.55     │  -8.9      │           │
...      │  ...        │  ...        │  ...       │           │
─────────┼─────────────┼─────────────┼────────────┼───────────┤
Formula  │ =SENSOR(A0) │ =API(syms)  │ =PID(x_sp) │ =AVG(A:A) │
```

### 5.3 Cell Types

| Cell Type | Example | Behavior |
|-----------|---------|----------|
| **Scalar** | `22.1` | A single numeric value at a time step |
| **Vector** | `[22.1, 72.3, 845]` | Multiple values at one time step (e.g., temp, humidity, light) |
| **Dependent Formula** | `=AVG(A0:A10)` | Computed from other cells; updates propagate |
| **Meta** | `{"event":"scene_change","to":4}` | Non-numeric metadata at a time step |
| **Empty** | `.` | No value recorded; gap in time series |

### 5.4 Edit Operations

The visual editor supports:

- **Set:** Click a cell, type a value → writes to that node's time series at that step
- **Fill:** Select a column range, fill with pattern `[22.0, 22.5, 23.0...]` → bulk set of sequential values
- **Fill-right (drag):** Same as MIDI CC fill — copy a value or formula across time
- **Copy-paste:** Select cells, copy, paste into another node's column → event range operations with auto-rescaling
- **Delete:** Clear cells → remove time steps from the node's history
- **Insert row:** Shift time steps forward (inserts delay into the sequence)
- **Formula bar:** Type `=PID(sp_target, current)` → a computed node output

### 5.5 How This Maps to .mid Export

When the spreadsheet is exported to `.mid` format:

- Each **column** becomes a **track** (with bank switching if >16 channels)
- Each **scalar cell** becomes a **CC message** or **pitch bend**
- **Vector cells** become **multi-byte SysEx** or **set of CCs**
- **Formulas** are **lost** — embedded as meta-events only
- **Meta cells** become **text meta-events** or **SysEx**
- **Time gaps** become **rests** (no events for those ticks)

This is lossy. The `.mid` file is a **snapshot render** of the spreadsheet state at a given time. The canonical representation is always the spreadsheet + graph.

---

## 6. Correction: MIDI is a Bridge, Not a Foundation

### 6.1 Summary of Corrections

| Topic | v1 Thinking | v2 Corrected |
|-------|------------|-------------|
| Channel model | Bank-switched MIDI channels | Node instances in embedding space |
| Timeline | Flat piano roll (DAW model) | Directed dependency graph |
| Physical devices | Data sources emitting MIDI | First-class channel nodes with lifecycle |
| UI | Single DAW interface | Dual: agent mixer + human dashboard |
| Data model | MIDI with extra meta-events | Tensor spreadsheet with graph topology |
| Wire format | .nail+.mid hybrid | .mid is import/export; internal is graph+spreadsheet |
| MIDI's role | Canonical format | Bridge only |

### 6.2 What v1 Got Right

- The three-agent critique (especially the adversarial analysis of MIDI's wire format limitations)
- Ghost Track as a concept (predicting from time-series data)
- Using MIDI as import/export bridge
- The idea of time as a universal coordinate
- The .nail schema concept for semantic definition

### 6.3 What v1 Got Wrong (Corrected Here)

- Thinking "add more channels" solves the capacity problem (it doesn't — MIDI's channel concept is wrong for this)
- Flat timeline thinking (dependency graphs are the real representation)
- Single-interface design (agents and humans need fundamentally different views)
- Treating MIDI as the canonical format (it's a bridge)
- No device lifecycle management (physical nodes need flashing, negotiation, reconnection)

---

## 7. Updated Roadmap — Node-Instance Architecture

This roadmap supersedes v1's Phase 1-4 plan. That plan was for MIDI-first infrastructure. This is for a node-instance sequencer.

### Phase 0: Node Schema Specification (Now)

- [ ] Define the node schema JSON (inputs, parameters, transform, outputs)
- [ ] Define the dependency graph edge format
- [ ] Define the registration/discovery protocol
- [ ] Define the tensor spreadsheet cell types
- [ ] Define the projection from graph → .mid export (lossy mapping)
- [ ] Document the embedding space where channel indices live
- [ ] **KT tile:** This document, tagged `sequencer-v2-architecture`

### Phase 1: ESP32 Bridge (Next — 0-3 months)

**Goal:** One physical device as a first-class channel node.

- [ ] ESP32 firmware with discovery protocol (announce schema on boot)
- [ ] ESP32 firmware with parameter negotiation (capabilities → set)
- [ ] ESP32 firmware with streaming output over WiFi/mesh
- [ ] ESP32 firmware with setpoint input (close the loop)
- [ ] Sequencer-side node registry accepting ESP32 registrations
- [ ] Sequencer-side graph engine with one physical node
- [ ] Demo: ESP32 temperature sensor → graph → dashboard display
- [ ] Bridge library: Node schema ↔ .mid export for this device

**Key milestone:** "An ESP32 boots up, announces itself, the sequencer detects it, negotiates parameters, and begins streaming data into the graph. The human dashboard shows 'ESP32-01: temp=22.3°C, online.'"

### Phase 2: Dependency Graph Engine (3-6 months)

**Goal:** The dependency graph is the real representation. Time is one dimension.

- [ ] Graph compilation: given N nodes with edges, produce runtime schedule
- [ ] Cycle detection: static analysis of all feedback loops
- [ ] Feedback loop serialization (one node updates per tick) and fixed-point convergence
- [ ] Edge latency tracking (each edge reports min/max/avg latency)
- [ ] Subgraph isolation (run a subset of nodes independently)
- [ ] Graph persistence (save/load graph topology as JSON)
- [ ] Multi-node mock: 5 virtual nodes with simulated dependencies
- [ ] Node embedding: embed each node's outputs in 384-dim vector space for semantic search

**Key milestone:** "Five virtual nodes form a dependency graph (sensor → filter → actuator → dashboard). The engine compiles the graph, runs it, detects the implicit cycle, and serializes correctly. 2+ nodes are queryable in embedding space."

### Phase 3: Agent Mixer Board + Human Dashboard (6-9 months)

**Goal:** Two interfaces for two audiences.

- [ ] Agent mixer view: full dependency graph, editable edges, node parameters, signal flow
- [ ] Agent mixer: performance metrics per node (latency, throughput, error rate)
- [ ] Agent mixer: embed/search interface (find nodes by semantic similarity)
- [ ] Agent mixer: graph compilation preview ("this topology will run at 50 Hz with +3ms added latency")
- [ ] Human dashboard: status cards, per-node health, key metrics
- [ ] Human dashboard: alert system (actionable, not noise)
- [ ] Human dashboard: project-level overview (which systems are green/yellow/red)
- [ ] Orchestrator agent: auto-routing logic ("route sensor A to filter B because..."
- [ ] Orchestrator agent: override prompt flow ("Human, do you want to reroute? Impact: +2ms latency.")
- [ ] **Trigger:** The human opens the hood only on failure, composition, or routing changes

**Key milestone:** "A full show runs with 18 nodes. The agent mixer auto-routes everything. The human dashboard shows green cards. When a node goes down, the dashboard shows red, the human opens the mixer, sees the broken edge, and the orchestrator suggests a reroute."

### Phase 4: Tensor Spreadsheet Visual Editor (9-12 months)

**Goal:** The spreadsheet where columns = nodes and rows = time steps.

- [ ] Spreadsheet grid showing nodes as columns, time as rows
- [ ] Cell editing: set scalar, clear, bulk fill
- [ ] Formula bar with dependent formulas (`=AVG`, `=PID`, custom transforms)
- [ ] Copy-paste across columns (event range operations with rescaling)
- [ ] Vector cell display (nested values in one cell)
- [ ] Meta-event cell display (JSON metadata per time step)
- [ ] Insert/delete row (shift time steps, insert delays)
- [ ] Live update: editing a cell sends a write to the node's stream
- [ ] Export to .mid: project spreadsheet state to SMF format
- [ ] Import from .mid: reverse-project back to spreadsheet (lossy — fills gaps, loses formulas)

**Key milestone:** "A user opens the spreadsheet, enters temperature setpoints for the next 30 minutes in the ESP32 column, types a formula in the 'average' column, and hits play. The ESP32 receives setpoints in real time."

### Phase 5: Full Fleet Migration (12-24 months)

**Goal:** Every fleet component that produces or consumes temporal data is a node in the graph.

- [ ] Fleet OSC bridge: external OSC streams → graph nodes
- [ ] Fleet MIDI bridge: any `.mid` file → import to graph
- [ ] Headspace-rs: query nodes by embedding across the entire fleet
- [ ] Ghost Track: predict future node states from graph history
- [ ] tminus-dispatcher: schedule cue events as graph writes
- [ ] Pincher: .nail state machines as transform nodes
- [ ] Pulse system: fleet heartbeat as a root node (everyone syncs to it)
- [ ] Conservation meter: γ+η=C with graph awareness (measure orchestration overhead)
- [ ] Baton-system: A2A graph messaging over temporal edges
- [ ] Colony games: temporal coordination as multi-node optimization scoring

**Key milestone:** "The fleet runs entirely on the sequencer graph. MIDI files are used only for DAW export/import. The sequencer is the canonical temporal representation."

---

## 8. KT Tile Posting

The token secret is loaded from `secrets/fleet-kt-secret.env`.

```bash
curl -X POST \
  -H "Authorization: Bearer 2coqVwP5KbSy0as4H94Bh9DGDuqkoiqy" \
  -H "Content-Type: application/json" \
  -d '{"id":"sequencer-v2-architecture","content":{"type":"architecture_design","agent_id":"oracle2","instance":"fleet","score":0.85,"branch":"sequencer","narrative":"Universal Sequencer Architecture v2 — corrected channel model from MIDI-bank-switching to node-instances in tensor embedding space with dependency graphs. Physical devices (ESP32) are first-class channels. The two-interface model (agent mixer board vs human dashboard) replaces single-grid thinking. Tensor spreadsheet as visual editor.","sloppy_summary":"Sequencer v2: channels are nodes, not MIDI ports. ESP32s are channels. Dependency graphs. Agent mixer vs human dashboard."}}' \
  https://fleet-kt-engine.casey-digennaro.workers.dev/tile
```

### Posting results

```json
{"ok":true,"tile_id":"sequencer-v2-architecture","room":"oracle2"}
```

**Confirmed at 2026-06-15 22:46 UTC.** KT tile posted successfully. Auth: Bearer token from `secrets/fleet-kt-secret.env`.

**KT Tile ID:** `sequencer-v2-architecture`

**Narrative summary:**
> Universal Sequencer Architecture v2 — corrected channel model from MIDI-bank-switching to node-instances in tensor embedding space with dependency graphs. Physical devices (ESP32) are first-class channels. The two-interface model (agent mixer board vs human dashboard) replaces single-grid thinking. Tensor spreadsheet as visual editor.

**Sloppy summary:**
> Sequencer v2: channels are nodes, not MIDI ports. ESP32s are channels. Dependency graphs. Agent mixer vs human dashboard.

---

*Document generated: 2026-06-15 22:46 UTC*
*Status: v2 addendum — supersedes v1 channel model*
*Author: oracle2 subagent*

**Appendix: Relationship to v1 Vision**

| v1 Document | v2 Addendum |
|-------------|-------------|
| Retain Section 3 (Adversarial Critique) | ✅ Valid critique of MIDI limitations |
| Retain Agent 2 Use Cases (puppetry, stock, kitchen) | ✅ Valid as user stories for the graph |
| Replace Section 1.2 Channel Mapping | ✅ Node-instance model replaces bank switching |
| Replace Section 4.3 (tensor spreadsheet) | ✅ Nodes-as-columns, not channels-as-columns |
| Replace Roadmap (Phase 1-4) | ✅ Node-instance roadmap (Phase 0-5) |
| Retain MIDI as bridge concept | ✅ Kept — .mid is import/export only |
| Add: Physical device lifecycle | ❌ Not present in v1 — new in v2 |
| Add: Two-interface model | ❌ Not present in v1 — new in v2 |
| Add: Dependency graph engine | ❌ Not present in v1 — new in v2 |
| Add: Node schema | ❌ Not present in v1 — new in v2 |

Read this document before reading v1. The v2 model supersedes v1's channel architecture. v1's use cases and adversarial critique remain useful for context.
