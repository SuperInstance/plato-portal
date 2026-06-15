# The Universal Temporal Sequencer — User Guide

## For Humans Who Compose Reality

---

## What Is This Thing?

Imagine a DAW — Ableton Live, Logic, Cubase — but instead of synthesizers and drum machines, the tracks are *real things*. An ESP32 temperature sensor on track 1. A stock price feed on track 2. A puppet's left arm joint on track 3. A kitchen oven on track 4.

The sequencer doesn't make sound. It makes *time* — time that carries data, events, dependencies, and actions across any number of channels, from any number of devices, all scrolling left to right in one unified timeline.

You're the composer. The sequencer is your instrument. The orchestra is everything you've plugged into it.

### The Two Views

| You are... | Use this view | It shows you |
|-----------|--------------|--------------|
| Checking in | **Dashboard** | Summary cards, status lights, alerts, key metrics |
| Composing or debugging | **Mixer** | The full dependency graph, signal routing, every channel |

The dashboard is the stage. The mixer is the backstage. You live on the stage. You only go backstage when something needs your hands.

---

## Channels: The Tracks of Reality

A **channel** is one node instance. Think of it as a track in a DAW — but instead of audio or MIDI, it carries a stream of time-domain data from a single source.

### What can be a channel?

| Source | Example | Shows up as |
|--------|---------|------------|
| Physical device | ESP32 with temp sensor | A channel named "Oven Probe" with a live temperature curve |
| Stock API | Polygon.io feed for $SPX | A channel named "SPX" with price as pitch bend, volume as velocity |
| Camera + Tensor CAM | Webcam pointed at a puppet | A channel named "Puppet A" with 31 CC streams for joints |
| Neural net output | Mood classifier | A channel named "Mood" with float values 0.0–1.0 |
| Virtual channel | Formula that reads two others | A channel named "Blend" that averages two sensor feeds |
| DMX lighting rig | USB-to-DMX dongle | A channel named "Stage Lights" with RGBW values |
| Another sequencer instance | Network-connected | A channel named "Kitchen Sync" mirroring remote data |

### Adding a channel

**Plug in a physical device:** Connect it via USB, WiFi, or serial. The sequencer discovers it automatically. Within seconds, a new channel appears on your dashboard with a name, type, and current readings. No configuration. No drivers.

**Connect an API:** Paste a URL and credentials. The sequencer negotiates the schema, sets up a polling or websocket connection, and creates the channel. Stock feeds, weather APIs, calendar data — if it has a time dimension, it lands as a timeline.

**Define a virtual channel:** Click "New Channel → Virtual." Give it a name. Pick its input channels. Select or write a transform function (add, average, threshold, FFT, whatever). The sequencer creates a dependency edge and handles the data flow automatically.

### Channel anatomy

Every channel has four parts:

```
┌─────────────────────────────────────────┐
│  Channel: "Oven Probe"                   │
│  Type:   ESP32-S3 / SHT40               │
├─────────────────────────────────────────┤
│  Inputs:     ⬜ (none — this is a source)│
│  Parameters:  500ms sample interval      │
│  Transform:  °C conversion               │
│  Output:     temp_readings → timeline    │
└─────────────────────────────────────────┘
```

- **Inputs:** What this channel reads from (empty for source devices)
- **Parameters:** Settings that control behavior (sample rate, calibration, API key, thresholds)
- **Transform:** A function applied to incoming data (scale, map, filter, composite)
- **Output:** Where the data goes (the timeline, another channel's input, an actuator, a file export)

---

## How Channels Talk to Each Other

A channel doesn't live in isolation. Any channel can read from any other channel. That's the whole point.

### Dependency graphs — the invisible wiring

When you tell a channel to read from another, the sequencer creates a directed edge. Channel B reads Channel A's output, applies its transform, and produces its own output. Channel C reads both A and B. The sequencer maintains the graph, resolves evaluation order, and streams data along the edges in real time.

This is how a lighting channel reads a scene description channel and maps it to DMX values. This is how a mood blender reads a stock feed and a camera channel and produces a gesture amplitude. This is how a kitchen oven reads a recipe timeline and adjusts its temperature setpoint.

**You never need to see the graph if you don't want to.** In the dashboard, it's invisible. You just see "Lighting: Scene 3 → Warm wash" and "Mood: Market up → Puppet energetic." The mixer view shows you the full graph if you open it.

**To wire channels together:**

1. Open a channel's properties
2. In the "Inputs" section, click "Add Input"
3. Select the source channel from the list
4. Choose what data to read (raw, filtered, specific parameter, the whole output stream)
5. Done

The sequencer handles evaluation order, circular dependency detection, and data synchronization. If you create a loop, it flags it immediately and refuses to close the circuit.

### Data types flowing through the graph

| Shape | Example | Shows in timeline as |
|-------|---------|---------------------|
| Scalar | 73.4°C | A single value curve |
| Vector | [x, y, z] joint position | Multi-line curve |
| Event | "door opened" | A note on the timeline |
| Formula | `A * 0.7 + B * 0.3` | Computed curve |
| Meta-event | "Scene change to 4" | Label on the timeline |

---

## The Dashboard View

The dashboard is what you see when you open the sequencer. It's designed to answer one question: *Is everything okay?*

### Layout

```
┌──────────┬──────────┬──────────┬──────────┐
│ Oven     │ Puppet A │ SPX      │ Mood     │
│ Probe    │          │          │          │
│ 73.4°C   │ 🟢 Idle  │ ▴ 5,421  │ 0.72     │
│ ───────  │          │ ───────  │ ───────  │
│  ▁▂▃▄▅▆▇ │  ▁▃▅▇▅▃▁ │  ▄▅▆▇▆▅▄ │  ▃▄▆▇▆▄▃ │
├──────────┴──────────┴──────────┴──────────┤
│ Alert: Puppet B left arm joint            │
│ exceeded range at 22:41:03.               │
│ → Agent reset to safe position.           │
└───────────────────────────────────────────┘
```

### Summary cards

Each channel gets a card showing:
- Channel name and type icon
- Current value (big, readable)
- Mini sparkline of recent activity
- Status indicator (green = nominal, yellow = attention, red = critical)
- Quick-action buttons (mute, inspect, zoom to timeline)

### Alert bar

Beneath the cards, a scrolling alert bar. It shows:
- Recent threshold violations ("Temp > 80°C at 22:40:12")
- Connection drops ("ESP32 Kitchen Probe disconnected at 22:38")
- Automatic recoveries ("Agent rerouted feed to backup sensor")
- Pending confirmations ("Recipe step 4: 'Add salt' — waiting for human OK")

Each alert is clickable. Clicking opens the relevant channel in the mixer with the problem highlighted.

### When to use the dashboard

- Morning check: "Did everything survive the night?"
- Mid-run glance: "Is the puppet still tracking?"
- Service monitoring: "Are all stations nominal?"
- You're not actively composing — you're supervising

---

## The Mixer View

The mixer is the backstage. Open it when you need to understand, compose, or fix something.

### What the mixer shows

```
┌─────────────────────────────────────────────────┐
│  Dependency Graph                                │
│                                                  │
│  ┌──────┐    ┌──────────┐    ┌──────────┐      │
│  │ Temp │───▶│ Threshold │───▶│ Alert    │      │
│  │Probe │    │ Detector  │    │ Channel  │      │
│  └──────┘    └──────────┘    └──────────┘      │
│                     │                            │
│                     ▼                            │
│              ┌──────────┐                        │
│              │  Fan     │                        │
│              │ Actuator │                        │
│              └──────────┘                        │
│                                                  │
│  ┌──────┐    ┌──────────┐    ┌──────────┐      │
│  │Stock │───▶│  Mood    │───▶│ Gesture  │      │
│  │ Feed │    │  Blend   │    │  Map     │      │
│  └──────┘    └──────────┘    └──────────┘      │
│        │                                         │
│        └──────────┐                              │
│                   ▼                              │
│            ┌──────────┐                          │
│            │Volume    │                          │
│            │ Map      │                          │
│            └──────────┘                          │
└─────────────────────────────────────────────────┘
```

Each node is a channel. Edges show data flow. Colors indicate status. You can:
- Drag to rearrange
- Click a node to open its full properties
- Click an edge to see the transform function
- Double-click to open the timeline for that channel
- Pinch/zoom to navigate large graphs

### When to use the mixer

- You're composing a new dependency chain
- Something broke and you need to see why
- You want to understand what's connected to what
- You're optimizing signal flow

---

## Editing the Timeline

The timeline is where everything lives. Temperature curves, stock prices, puppet motion, lighting cues, recipe steps — all of it scrolls left to right, and all of it is editable.

### Three Modes

The sequencer has three modes, exactly like a DAW:

#### Record Mode 🔴

Hit record. Everything happening right now gets written to the timeline. Every channel's output at every time step. Running a puppet show? Record it. Running a kitchen service? Record it. The result is a .mid file that captures the entire session.

- **What it's for:** Capturing live performance, sensor data, or any real-time stream
- **What you get:** A dense timeline with every channel's data at full resolution
- **Pro tip:** You can trim, slice, and edit the recording afterward. Record is just capture.

#### Overdub Mode 🟡

Record mode, but it doesn't erase what's already there. New data layers on top. Existing data that isn't overwritten stays in place.

- **What it's for:** Adding a new channel's data to an existing session, layering sensor streams, patching in new data
- **What you get:** A merged timeline with both old and new data
- **Pro tip:** Great for combining multiple recording sessions. Record the stock feed once, then overdub the puppet performance later.

#### Program Mode 🟢

No real-time input. You manually place data on the timeline — set values at specific times, draw curves, insert events, define ranges.

- **What it's for:** Authoring a sequence from scratch
- **What you get:** A precisely crafted timeline with no noise
- **Pro tip:** This is where you compose a recipe, script a lighting show, or program a puppet performance

### The Piano Roll (but for everything)

The main editing area looks like a DAW's piano roll. The vertical axis is channel data (values, events, ranges). The horizontal axis is time.

- **Scalar channels** show as automation curves — draw, smooth, quantize
- **Event channels** show as note blocks — place, stretch, move
- **Vector channels** show as multi-line curves — edit individual components
- **Meta channels** show as labeled markers — edit text, timing, duration

### Editing actions

| Action | How | What happens |
|--------|-----|-------------|
| Draw a value | Click and drag on the curve | Sets that channel's output at those times |
| Place an event | Click on the timeline | Inserts a timestamped action |
| Stretch a range | Drag the edge of a note block | Extends or shortens the event duration |
| Quantize | Select, hit Q | Snaps events to nearest grid line |
| Smooth | Select curve, hit S | Applies smoothing to noisy data |
| Copy/paste | Ctrl+C, Ctrl+V on time selection | Duplicates events and curves |
| Time shift | Select + drag left/right | Moves everything earlier or later |
| Tempo map | Set BPM per section | Controls the grid density (60 BPM = relaxed kitchen; 180 BPM = frantic) |

---

## What Happens When Something Breaks

Things will break. Sensors drift. ESP32s lose WiFi. API rate limits hit. The sequencer has a recovery hierarchy.

### Level 1: Automatic Fallback

The orchestrator agent detects the failure and tries to recover without you. It might:
- Reconnect a dropped device
- Switch to a backup sensor
- Retry a failed API call with exponential backoff
- Use the last known good value for a channel until it recovers
- Reroute data through an alternative path in the dependency graph

You see a notification in the alert bar: "ESP32 Kitchen Probe reconnected after 3s dropout. No data loss."

### Level 2: Orchestrator Intervention

The orchestrator agent takes active measures. It might:
- Create a new channel to compensate (e.g., if a temperature sensor fails, it creates a virtual channel that estimates temperature from a nearby sensor)
- Adjust parameters on related channels (e.g., if a puppet joint drifts, it recalibrates the IK solver)
- Shift the timeline (e.g., if a kitchen step is delayed, it shifts all downstream steps)
- Request confirmation from you ("Oven temperature suspected incorrect. Approve fallback estimation?")

You see a notification with an action button: ⚠️ "Puppet B arm joint drifting. Agent recalibrated. [Inspect] [Dismiss]"

### Level 3: Human Required

This is where the orchestrator gives up and calls you. It only does this for things it can't fix:
- Physical hardware failure ("ESP32 not responding after 5 reconnect attempts. Needs physical check.")
- Semantic ambiguity ("Recipe says 'fold gently' — unclear duration and intensity. Please define.")
- Safety-critical decisions ("Kitchen oven at 250°C with no sensor feedback. Request human override.")
- Structural changes ("Cannot resolve circular dependency between Mood Blend and Gesture Map.")

You get a prominent alert with a "View in Mixer" button. The mixer opens with the problem highlighted. You fix it, the sequencer resumes.

### The agent handles most things

The orchestrator agent is the default operator. It's always running. It watches every channel, every connection, every dependency. When something breaks, it tries Level 1 first, Level 2 second, and only calls you at Level 3.

This means most of the time, you don't see failures. You see the system handle them and move on. You only intervene when the system can't solve it alone.

---

## Saving, Sharing, and Replaying

### The .mid file is your save state

Every session — whether recorded, programmed, or a mix of both — saves as a single .mid file. This is your universal temporal document. It contains:

- Every channel's data (scalars, vectors, events, meta-events)
- Every dependency edge (what reads from what)
- Every parameter setting (sample rates, thresholds, calibration values)
- .nail schema references (what everything means)
- Timestamp anchors (absolute wall-clock time for each section)

**Open any past session** and it looks exactly like it did when you saved it. Scrub through it. Tweak parameters. Replay it. Your kitchen service from last week is a file you can remix.

### Export options

| Format | What it's for | Size (typical) |
|--------|--------------|----------------|
| .mid | Save/open/load, universal temporal document | 50–500 KB for most sessions |
| .mid + .nail | Full semantic + temporal data | 60–600 KB |
| MIDI file (SMF) | Import into DAWs (Ableton, Logic, Reaper) | 50–500 KB |
| Live stream | Send to another sequencer instance in real time | Network |
| CSV/JSON | Extract data for analysis | Variable |

### Sharing

Share a .mid file like you'd share any document. The recipient opens it in their sequencer (or DAW, if exported as SMF). They see your timeline, your channels, your data. They can scrub through it, tweak it, and replay it.

Send your stock market sonification to a friend: "Listen to the divergence at 10:47 AM." Send your kitchen service to a consultant: "Find the bottleneck." Send your puppet show to a collaborator: "Add lighting cues to track 4."

---

## What This Can Do — The Big Picture

The Universal Temporal Sequencer is a tool for gluing any time-domain thing to any other time-domain thing.

### Application patterns

**Unify disparate systems into one timeline.**

A temperature sensor, a stock feed, a camera, a mood classifier, a DMX controller — five different things with five different protocols, all appearing as adjacent channels in the same timeline. You can scroll from the temperature spike at 10:47 AM to the stock price reaction at 10:48 AM without leaving the view.

**Create autonomous behaviors from simple parts.**

A camera channel feeds pose data into a mood blender channel that reads a stock feed channel. No code. No scripts. Just "this reads from this reads from this." The puppet reacts to the market because you connected three channels.

**Capture anything as a replayable document.**

A two-hour kitchen service becomes a 150 KB file. Rewind to the moment the oven failed. See exactly when it happened, what the temperature curve looked like, how the system responded. Edit it. Replay it. Remix it.

**Program complex sequences with DAW-level precision.**

A ten-course tasting menu with timed temperature profiles, ingredient addition cues, and human confirmation points — all in program mode. Draw the temperature curves, place the cue markers, set the durations. The sequencer executes with metronomic precision.

**Live-stream between instances.**

One sequencer instance in the kitchen, another in the dining room, a third in the back office. They're all in sync. The kitchen sequencer drives the ovens. The dining room sequencer displays course timing. The back office sequencer logs everything. One change propagates everywhere.

### What it's not

It's not a sensor data logger (though it can be used as one). It's not an automation system (though it can trigger automation). It's not a protocol converter (though it routes between protocols). It's not a DAW (though it looks and acts like one).

It's a *temporal composition tool* — a way to think about, capture, edit, and replay time-domain data across any number of sources and destinations, with a DAW-like interface that makes time feel tangible.

---

## Quick Reference

| Concept | What it is |
|---------|-----------|
| Channel | One node instance — a device, API, virtual, or agent |
| Dashboard | The stage view — summary cards, alerts, key metrics |
| Mixer | The backstage view — full dependency graph and signal routing |
| Record mode | Capture live data to the timeline |
| Overdub mode | Layer new data on existing timeline |
| Program mode | Manually author data on the timeline |
| Dependency edge | One channel reads another's output |
| Orchestrator agent | Default operator — routes, transforms, recovers |
| .mid file | Universal temporal document — save, share, replay |
| .nail schema | Semantic definition — what each channel means |

### If in doubt

Open the dashboard. Check the cards. Read the alert bar. If everything's green, you're good. If something's yellow, the agent is handling it. If something's red, click the alert and go to the mixer. The system tells you what it needs.

You're the composer. You don't tune the violins. You write the music.
