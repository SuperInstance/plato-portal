# Sequencer Tutorials

## Three Walkthroughs That Teach the System by Doing

---

# Tutorial 1: Your First Channel — Temperature from an ESP32

**What you'll learn:** Plug in a physical device, see its data on the timeline, set an alert, and watch the orchestrator agent respond.

**Time:** ~10 minutes start to finish.

---

### Step 1: Plug in the ESP32

Take the ESP32-S3 with the SHT40 temperature/humidity sensor. Connect it to your machine via USB.

That's it. The sequencer discovers it automatically.

Within about three seconds, a new card appears on your dashboard. It says:

```
┌──────────────────────────────────┐
│  ESP32 Kitchen Probe            │
│  73.4°C                           │
│  ▁▂▃▄▅▆▇                          │
│  🟢 Connected                     │
└──────────────────────────────────┘
```

The sequencer found the device, identified it (SHT40 sensor on ESP32-S3), established a serial connection, and started receiving temperature readings at the device's default sample rate.

**No configuration. No drivers. No "add device" wizard.** The device appears because it exists.

### Step 2: The Channel Opens

Click the card. The timeline opens, centered on this channel. You see:

- **Channel name:** "ESP32 Kitchen Probe" (auto-detected from device)
- **Channel type:** `ESP32-S3 / SHT40` (silkscreen name from the ESP32's firmware descriptor)
- **Current value:** 73.4°C (large, updating in real time)
- **Timeline:** A scrolling temperature curve, 60 seconds of history visible, updating every 500ms

The channel is already writing to the timeline. The curve you see is real data, captured since the moment of connection.

Hover over the curve. A tooltip shows the exact value at that timestamp: 73.2°C at 22:41:10, 73.5°C at 22:41:15, 73.4°C at 22:41:20.

This is already a .mid file being written in the background. Every data point is an event on the timeline.

### Step 3: Open the Dashboard (You're Already There)

Your first view of the sequencer *is* the dashboard. The temperature card is one of several — as you add more channels, more cards appear.

The dashboard shows you what matters:
- **Current value:** The most recent reading, always visible
- **Sparkline:** A mini-preview of recent activity
- **Status indicator:** Green while data flows normally

At this point, you have one card: the temperature probe. But notice the alert bar at the bottom is already showing something:

```
┌───────────────────────────────────────────┐
│  ✓ ESP32 Kitchen Probe connected at 22:40 │
└───────────────────────────────────────────┘

```

The system logged it. Everything is tracked.

### Step 4: Set a Threshold

You want to know if the temperature exceeds 80°C. (It's near an oven. It happens.)

On the temperature card, click the gear icon → "Alerts" → "Add Alert."

A dialog opens:

```
┌─── Add Alert ─────────────────────────────┐
│  Trigger when: Temperature     │  >  │ 80 │
│                                            │
│  Alert severity:  ● Warning  ○ Critical   │
│                                            │
│  Notify: [Dashboard alert bar] [Push]     │
│                                            │
│  [Cancel]  [Create Alert]                  │
└────────────────────────────────────────────┘
```

Fill it in:
- Trigger: Temperature > 80
- Severity: Warning (it's hot, not on fire)
- Notify: Dashboard alert bar

Click "Create Alert."

The sequencer registers the alert. Nothing changes visually — the card stays green. But there's now a threshold detector attached to this channel. When the value crosses 80°C, the sequencer will notice.

### Step 5: The Orchestrator Responds

Leave the probe running. Keep the dashboard open. Go make some tea.

When the temperature crosses 80°C, here's what happens:

**The dashboard updates immediately:**
- The temperature card turns yellow (warning)
- The alert bar shows: `⚠ ESP32 Kitchen Probe: Temperature 82.3°C exceeds threshold of 80°C`
- The current value flashes

**The orchestrator agent activates:**

Within seconds, the alert bar updates:

```
┌────────────────────────────────────────────┐
│  ⚠ ESP32 Kitchen Probe: Temp 82.3°C       │
│     exceeds threshold (80°C)               │
│  🤖 Agent: Created "Kitchen Fan" channel   │
│     (ESP32-PWM) — cooling actuator online  │
│  🤖 Agent: Wired Kitchen Fan → reads       │
│     Kitchen Probe temp; activates at >75°C │
└────────────────────────────────────────────┘
```

The orchestrator didn't just log the alert. It created a **new channel** — a cooling fan actuator — and wired it to the temperature probe. The dependency graph now looks like:

```
ESP32 Kitchen Probe ──(threshold: >75°C)──▶ Kitchen Fan (PWM on/off)
                        ↕
                  The alert you created
                  (notify at >80°C)
```

Check the dashboard now. There's a new card:

```
┌──────────────────────────────────┐
│  Kitchen Fan                     │
│  ● Active (PWM: 75%)            │
│  ───────                         │
│  ▁▁▁▁▁▁▁▇▇▇                      │
│  🟢 Active                        │
└──────────────────────────────────┘
```

The agent saw the threshold, identified a nearby ESP32 with a PWM output, instantiated a fan actuator channel with the correct pin mapping, set the activation threshold to 75°C (5 degrees before your alert), and turned it on.

You didn't write any code. You didn't configure any pins. You didn't tell the agent what to do. You just set one threshold on one channel, and the agent figured out the rest.

### What You Learned

- **Channels are devices.** Plug in a physical thing and it becomes a channel. No setup required.
- **The dashboard shows what matters.** One card per channel. Current value, recent history, status.
- **Alerts are triggers.** Setting a threshold tells the sequencer "watch this." What it does with that watch is the sequencer's job.
- **Agents handle the routing.** The orchestrator created a cooling channel, wired it in, and handled the dependency graph. You didn't know there was a fan-capable ESP32 nearby. The agent did.
- **You stay on the stage.** You set the composition rule ("don't exceed 80°C"). The agent built the backstage mechanism.

---

# Tutorial 2: A Puppet Learns from the Market

**What you'll learn:** How channels read from other channels, how dependency graphs create complex behavior from simple parts, and how the mixer view reveals the invisible wiring.

**Time:** ~15 minutes.

---

### Step 1: Start the Tensor CAM Channel

Point a webcam at a puppet. In the sequencer, go to "Add Channel" → "Camera" → select your webcam.

The sequencer starts Tensor CAM — a real-time pose estimation pipeline. Within a moment, a new channel appears:

```
┌──────────────────────────────────┐
│  Tensor CAM                      │
│  Puppet A — 31 landmarks         │
│  ▁▃▅▇▅▃▁                         │
│  🟢 Tracking                      │
└──────────────────────────────────┘
```

Click the card to see what's inside. Tensor CAM decomposes the camera feed into MIDI-compatible streams:

- **Head:** Pitch, yaw, roll → 3 CC channels
- **Left arm:** Shoulder, elbow, wrist X/Y/Z → 9 CC channels
- **Right arm:** Shoulder, elbow, wrist X/Y/Z → 9 CC channels
- **Torso:** Lean X/Y, twist → 3 CC channels
- **Face:** Eyebrow, eye, mouth openness → 7 CC channels

Each landmark position is a continuous controller stream. The puppet moves, the streams update, the timeline fills.

Move the puppet's arm. See the curve on the timeline rise. That's a real-time stream of x/y/z values, flowing into the sequencer.

### Step 2: Add a Stock Feed Channel

Go to "Add Channel" → "API" → "Polygon.io Stock Feed."

Paste your API key. Enter symbols: SPX, AAPL, NVDA.

The sequencer creates a channel:

```
┌──────────────────────────────────┐
│  Stock Feed                      │
│  SPX: 5,421 ▲  AAPL: 178 ▼      │
│  ▅▆▇▆▅▆▇▆▅                       │
│  🟢 Live                           │
└──────────────────────────────────┘
```

Each symbol has sub-streams:
- **Price** → mapped as pitch bend value (14-bit resolution for smooth curves)
- **Volume** → mapped as velocity
- **Change %** → mapped as continuous controller

The timeline shows three overlapping price curves. Stock data scrolls left to right just like the temperature data from Tutorial 1.

### Step 3: Create a Mood Blender Channel

Now the interesting part. You're going to create a channel that reads from both the stock feed and the puppet's camera feed, and produces a blended output.

Go to "Add Channel" → "Virtual."

Name it: **Mood Blender**

In the **Inputs** section, click "Add Input." A dropdown shows every available channel:

- [ ] Tensor CAM
- [✓] Stock Feed
- [ ] ...

Select Stock Feed. Then "Add Input" again and select Tensor CAM.

Now configure the transform. The sequencer shows a formula editor:

```
══ Read:  Stock Feed ──────────────────
  Stock Feed.SPX.change_percent → mood_in

══ Read:  Tensor CAM ─────────────────
  Tensor CAM.gesture_amplitude → amp_in
  (gesture_amplitude = mean joint displacement)

══ Transform: ─────────────────────────
  [mood_volatility = abs(mood_in) × 10]
  [output_amplitude = amp_in × (1 + mood_volatility)]
```

These are the defaults the sequencer suggests based on data types. You can edit them. For this tutorial, leave them:

- `mood_volatility = abs(mood_in) × 10` — more volatile stock movement = bigger mood impact
- `output_amplitude = amp_in × (1 + mood_volatility)` — scale the puppet's gesture amplitude by market mood

Click "Create Channel."

The sequencer validates the inputs, checks for circular dependencies, computes the evaluation order, and activates the channel.

### Step 4: Add the Lighting Channel

One more channel. This one reads the scene description from... well, you need a scene description channel.

Create another virtual channel called **Scene Descriptor**. For now, give it a simple transform: it reads Tensor CAM's face landmarks, and if mouth openness > 0.5, it outputs "Surprised." If eyebrow height < 0.2, "Neutral." If both eyes narrowed, "Angry."

```
══ Transform: ─────────────────────────
  if mouth_openness > 0.5 → "Surprised"
  elif eye_narrow > 0.6 → "Angry"
  else → "Neutral"
```

Now create the **Lighting** channel. It reads Scene Descriptor.

Set the transform to map scenes to DMX values:

```
══ Transform: ─────────────────────────
  "Neutral"    → { R: 128, G: 128, B: 128, W: 64 }
  "Surprised"  → { R: 255, G: 200, B: 100, W: 0 }
  "Angry"      → { R: 255, G: 50,  B: 50,  W: 0 }
```

The Lighting channel outputs DMX frames. If you have a DMX controller connected, it sends values to your stage lights. If not, it just writes to the timeline — you can see the lighting cues as colored blocks.

### Step 5: Open the Mixer View

Now open the mixer for the first time. Click "View" → "Mixer."

You see the full dependency graph:

```
┌──────────┐    ┌──────────────┐    ┌────────────┐
│ Tensor   │───▶│ Mood Blender │───▶│ (to pupil) │
│ CAM      │    └──────────────┘    │ gesture_amp │
└──────────┘         ▲              └────────────┘
     │               │
     │    ┌──────────┴───┐
     └───▶│ Stock Feed   │
          └──────────────┘

┌──────────┐    ┌──────────────┐    ┌────────────┐
│ Tensor   │───▶│ Scene        │───▶│ Lighting   │
│ CAM     │    │ Descriptor   │    │ (DMX out)  │
└──────────┘    └──────────────┘    └────────────┘
     │                                    │
     │                                    ▼
     └─── face landmarks              Physical
          → mouth/eye values          DMX controller
```

Each node is color-coded:
- 🟢 Active — data flowing
- 🟡 Idle — channel exists but no current activity
- 🔴 Error — something's wrong

Each edge shows a label if you hover: "reads: Tensor CAM.gesture_amplitude" or "maps: Surprised → DMX warm wash."

Drag nodes around to rearrange the graph. Click a node to open its properties. Click an edge to edit the transform function.

This is the backstage. Everything that happens automatically is visible here. You built two dependency chains without writing a line of code.

### Step 6: Watch It Run

Go back to the dashboard (click "View" → "Dashboard").

You see four cards now:

```
┌──────────┬──────────┬──────────┬──────────┐
│ Tensor   │ Stock    │ Mood     │ Lighting │
│ CAM      │ Feed     │ Blender  │          │
│ 🟢       │ 🟢       │ 🟢       │ 🟢       │
└──────────┴──────────┴──────────┴──────────┘
```

Watch what happens:

1. Move the puppet's arm up. The Tensor CAM curve rises.
2. Stock volume increases. The Mood Blender curve spikes.
3. The puppet's gesture amplitude changes — driven by market volatility.

Now make the puppet's mouth open. The Scene Descriptor outputs "Surprised." The Lighting channel sends warm wash DMX values. The timeline shows a lighting cue at that exact moment.

Move a puppet joint in a smooth arc. Watch the stock feed flicker. See the mood blend respond. See the lighting change when your puppet's expression shifts.

All of this is happening because:

- Tensor CAM → writes landmarks to the timeline
- Stock Feed → writes prices and volume to the timeline
- Mood Blender → reads both, computes blend
- Scene Descriptor → reads facial landmarks, classifies expression
- Lighting → reads scene descriptor, maps to DMX

No code. Five channels. Two dependency chains. Complex behavior from simple parts.

### What You Learned

- **Channels read from other channels.** That's the core interaction. A channel's input is another channel's output.
- **Dependency graphs make complex behavior from simple parts.** Each channel does one thing. Together, they create behavior that looks like intelligence.
- **The mixer shows the invisible wiring.** When something goes wrong — the lighting doesn't match the scene, the puppet doesn't react — you open the mixer to see the graph.
- **Virtual channels are where the logic lives.** They're the glue. No-code transforms that map, blend, and route data between real-world channels.
- **The dashboard is for watching.** The mixer is for understanding. You watch from the stage. You figure things out backstage.

---

# Tutorial 3: Script a Kitchen Service

**What you'll learn:** Program mode, timeline authoring, tempo maps, human-in-the-loop confirmation, and how a .mid file captures an entire session.

**Time:** ~20 minutes.

---

### Step 1: Define Stations

First, create the physical stations. If you have real devices, they auto-discover (Tutorial 1 style). For this tutorial, we'll define virtual stations that simulate the kitchen.

Go to "Add Channel" → "Virtual" for each station:

**Station: Oven**
- Inputs: (none — simulated for now)
- Parameters: target_temp = 180°C, actual_temp = 180°C (simulated)
- Output: temperature curve

**Station: Stove-Top**
- Inputs: (none — simulated)
- Parameters: burner_level = 0-100, pan_temp = tracked
- Output: burner level, pan temp

**Station: Prep Station**
- Inputs: (none — manual)
- Parameters: (none — human-driven)
- Output: step completion events

**Station: Plating Station**
- Inputs: (none — manual)
- Parameters: (none — human-driven)
- Output: step completion events

Your dashboard now shows four station cards. All green. Nothing happening.

### Step 2: Set the Recipe Timeline (Program Mode)

Switch to **Program Mode** — click the mode button until it turns green.

You now see an empty timeline. This is your canvas.

First task: **Set the tempo.** A tasting menu service moves at 60 BPM — one beat per minute, one minute per cooking step. Click the tempo field in the transport bar, set it to 60.

Now the timeline grid shows marks every one minute. Each mark is a beat. At 60 BPM, beat = minute.

**Add the recipe steps:**

The recipe is a five-course tasting menu:

| Step | Course | Duration | Notes |
|------|--------|----------|-------|
| 1 | Amuse-bouche | 2 minutes | Prep and plate |
| 2 | First course (cold) | 5 minutes | Assemble, no cooking |
| 3 | Second course (hot) | 12 minutes | Sear scallops, roast vegetables |
| 4 | Third course (meat) | 25 minutes | Sous-vide steak, sauce reduction |
| 5 | Fourth course (cheese) | 8 minutes | Plate cheese selection |
| 6 | Fifth course (dessert) | 10 minutes | Finale |

In Program Mode, you add events like placing notes on a piano roll:

1. On the **Prep Station** track, place a note block from Time 0 to Time 2. Label it "Amuse-bouche prep." Set the color to green (prep).
2. On the same track, place a block from Time 2 to Time 7. Label it "First course prep." Green.
3. On the **Stove-Top** track, place a block starting at Time 7, ending at Time 19 (12 minutes). Label it "Sear scallops."
4. Place another stove-top block from Time 8 to Time 19: "Roast vegetables" (they cook in parallel).
5. On the **Oven** track, place a block from Time 19 to Time 44 (25 minutes): "Steak sous-vide."
6. Add a parallel oven block: "Sauce reduction" same time range.

Each block is a MIDI note. Duration = note length. Label = note name.

Now **add the curves.** Temperature control:

1. On the **Oven** track, draw a temperature curve. Click to set points:
    - Time 0: 20°C (room temp)
    - Time 19: 55°C (sous-vide target)
    - Time 44: 55°C (hold)
    - Time 44+: drop to cooling

2. On the **Stove-Top** track, draw burner level:
    - Time 7: burner 0% → 80% over 30 seconds (preheat)
    - Time 7:30 to 19: burner 80% (searing heat)
    - Time 19: drop to 0%

Your timeline now looks like a DAW session:

```
   0       5      10      15      20      25      30      35      40      45
──────────────────────────────────────────────────────────────────────────────
Prep  [ Amuse-bouche  ][ First course  ]
Stove                                 [ Sear scallops  ]
                                      [ Roast veg      ]
Oven                               ══════════════════════════════[Sous-vide]══
                                    ~~~~temp curve rising~~~~55°C~~~~~~~~~~~~
```

### Step 3: Add Real Sensor Feedback

Now connect a real sensor to the Oven channel.

Plug in an ESP32 with a thermocouple probe. Place the probe in the oven. (Real oven. Real heat. Be careful.)

The sequencer discovers the probe (just like Tutorial 1). A new channel appears: **"Oven Probe"** with a live temperature reading.

Now go to the **Oven** channel's properties. In the Inputs section, click "Add Input" → select "Oven Probe."

A dialog asks: "Oven already has a temperature curve. Replace with real-time sensor, or blend?"

Select **"Use real sensor when available, fall back to programmed curve."**

The sequencer creates a dependency: Oven reads Oven Probe when connected, falls back to its internally programmed curve when disconnected. If the sensor disconnects mid-service, the programmed curve takes over — no interruption.

Open the **real-time display mode**:
- The programmed curve stays visible as a faint guide (semi-transparent)
- The actual sensor data draws on top as a solid line
- If they diverge, the area between them fills with a highlight color

Now when you run the service, you can see at a glance: "The oven is tracking the programmed curve perfectly" (no gap) or "The oven is 15°C below target" (big gap — trouble).

### Step 4: Add Confirmation Points

A kitchen is not fully automatic. Humans need to confirm steps before proceeding.

In Program Mode, right-click on the timeline at each transition point. Select "Add Marker" → "Confirmation."

For each confirmation, a dialog asks:

```
┌─ Add Confirmation Point ────────────┐
│  Time: 2:00                          │
│  Step: "Transition to First Course"  │
│                                       │
│  Prompt: "Plate amuse-bouche and     │
│           confirm ready for course 2"│
│                                       │
│  ⨁ Active pause                      │
│  Timeout: [ 5 ] minutes              │
│  Fallback: Continue without confirm  │
│                                       │
│  [Cancel]  [Add Confirmation]        │
└───────────────────────────────────────┘
```

Add confirmations at:
- 2:00 — before First Course
- 7:00 — before Second Course (stove-top prep)
- 19:00 — before Third Course (oven handoff)
- 44:00 — before Fourth Course (cheese)
- 52:00 — before Fifth Course (dessert)
- 62:00 — End of service (final plating)

New markers appear on the timeline as diamonds with labels:

```
Prep  [ Amuse  ][ First           ]
            ◆         ◆
     "Plate"  "Stove ready?"
```

When you run the service, the sequencer will pause at each ◆ and display a prompt. The timeline stops advancing until the human clicks "Confirm" — or until the timeout expires and the sequencer continues automatically.

### Step 5: Run the Service

Switch to **Performance Mode** — click the mode button until it turns red (Record Mode + playback).

Hit **Play.**

The sequencer starts executing the timeline. Time advances. Channels activate.

**Watch the timeline advance:**

At 0:00 — the Prep Station block starts. The dashboard shows "Amuse-bouche prep" highlighted.

At 2:00 — the timeline pauses. A confirmation dialog pops up on the dashboard:

```
┌─── Confirmation Required ───────────────────┐
│                                              │
│  "Plate amuse-bouche and confirm ready       │
│   for First Course"                          │
│                                              │
│  [Confirm]  [Hold (5 min)]  [Skip Step]      │
└──────────────────────────────────────────────┘
```

Click Confirm. The timeline resumes.

At 7:00 — another pause: "Prepare stove-top, confirm for Second Course." Confirm.

**Watch the temperature tracking:**

As the service progresses, the Oven card on the dashboard shows two curves — programmed (faint) and actual (solid). They track closely. The agent is logging deviations but none exceed the tolerance threshold.

**Watch time advance in real time:**
- The playhead moves left to right across the timeline
- Current step highlights
- Remaining time shows in the transport bar
- Tempo map shows current BPM (60)

At 19:00 — confirmation: "Hand off to oven for sous-vide. Confirm." Confirm.

The Stove-Top channel deactivates (its block ends). The Oven channel's burner curve begins its descent to sous-vide temperature.

### Step 6: Review the Playback

The service runs for about 62 minutes. When it's done, hit **Stop.**

You now have a .mid file that captures the entire service:

- **Every programmed step** — all the blocks on the timeline
- **Every temperature curve** — both programmed and actual
- **Every confirmation** — timestamp, who confirmed, how long the pause lasted
- **Every deviation** — when actual oven temp diverged from programmed, by how much, for how long
- **Every data point from every sensor** — full-resolution time series

Save the file: "tasting-menu-2026-06-15.mid"

**Now scrub backward.** Grab the playhead and drag it left.

- At Time 7:00, the confirmation pause is visible as a gap in the timeline.
- At Time 10:30, the stove burner curve climbs.
- At Time 12:15, there's a real temperature blip — someone opened the oven. The actual curve spikes, then recovers.

**This is a temporal document.** You can scroll through the entire service, second by second, and see exactly what happened at every moment.

**Now edit it:**
- Select the temperature blip at 12:15. Smooth it (press S).
- Move the "Sear scallops" block 30 seconds earlier.
- Add a new block on the Prep Station: "Warm plates" at 18:00.

**Hit Play again.** The service runs with your edits.

### What You Learned

- **Program mode is authoring.** You set notes, curves, markers, and tempo. The timeline is your score.
- **Performance mode is execution.** The sequencer reads the score and drives real devices. Time is real.
- **Confirmation points are MIDI markers.** They pause the timeline and wait. They're part of the sequence, not separate from it.
- **Real sensor feedback blends with programmed curves.** The programmed curve is the plan. The sensor is the reality. The sequencer shows both and uses the sensor when available.
- **The .mid file captures everything.** Steps, curves, confirmations, deviations — it's all in the file. Open it tomorrow, next week, next year. It's a full record.
- **The sequencer is a playback system.** You compose in program mode. You execute in performance mode. You review by scrubbing through the recording. The same file works for all three.
- **A kitchen service is a composition.** Like a symphony. Movements (courses), tempos (timing), dynamics (temperature), cues (confirmations). The DAW paradigm maps perfectly.

---

## Where to Go Next

You've learned the three core workflows:

1. **Plug and play** (Tutorial 1) — devices appear, data flows, agents respond
2. **Wire channels together** (Tutorial 2) — dependency graphs create complex behavior
3. **Compose and execute** (Tutorial 3) — program mode, performance mode, .mid as save state

These three patterns cover 90% of what the sequencer does. The rest is depth:
- Advanced transforms (FFT, convolution, machine learning)
- Recursive channels (a channel that reads its own past output)
- Multi-instance sync (multiple sequencers on the network)
- Custom .nail schemas for new device types
- Ghost Track integration (predict future values from past data)

But the fundamentals are always the same:

**Plug something in. See it on the timeline. Wire it to something else. Let the agent handle the routing. Compose. Execute. Save. Replay.**

You're not building infrastructure. You're composing time.
