# lau-constellation

> The research monorepo for the PLATO/LAU ecosystem — 350+ project directories spanning deadband signal processing, constraint substrates, spectral analysis, agent architectures, music synthesis, quantum spin languages, and beyond.

**765 markdown documents · Zig + Rust + C + Fortran · 16 Zig tests**

---

## What This Does

`lau-constellation` is the central research and development hub for the PLATO/LAU ecosystem. It contains experiments, proofs-of-concept, formal specifications, research notes, agent architectures, and production code across dozens of domains.

The monorepo is organised as a constellation of semi-independent project directories, each exploring a different facet of the ecosystem.

### The Zig Deadband Library

The root-level Zig project (`src/main.zig`, `build.zig`) implements a **deadband filter library** — because sometimes the best thing a signal can do is *nothing*.

A deadband filter suppresses small changes around a reference value. This pattern appears in:

- **Thermostats** — wait for a 2°F swing before cycling the HVAC
- **Joysticks** — ignore resting noise so your character doesn't drift
- **Sensor filtering** — treat ADC jitter (4094–4098) as the same reading
- **Motor control** — prevent oscillation around a target position
- **Audio** — noise gates are deadbands in disguise

**16 Zig tests** covering all three filter types.

---

## The Key Idea

### Deadband Filters

A deadband defines a zone around a baseline. Values inside the zone are "no change." Values outside pass through:

```
         passed through
        /
       /
---[---|---]---  →  baseline ± threshold
       \
        \
         passed through
```

With rescaling, the output is linearly mapped so the transition at the threshold boundary maps to zero:

```
output = sign × (|input| - threshold) / (max - threshold)
```

### The Broader Constellation

Beyond the deadband library, the repo contains 350+ directories spanning:

| Area | Example directories |
|---|---|
| **Signal processing** | `spectral-conservation`, `analog-spectral`, `flux-research`, `warp-flux-poc` |
| **Agent architectures** | `agent-field`, `zeroclaw-agent`, `zeroclaw-plato`, `agent-native-language` |
| **Music synthesis** | `spline-instrument`, `spline-midi-smooth`, `plato-room-musician`, `groove-analyzer` |
| **Compiler/PL research** | `flux-lang`, `flux-isa-mini`, `zerolang`, `agentic-compiler` |
| **Mathematical physics** | `constraint-substrate`, `eisenstein`, `eisenstein-vs-z2-c`, `tensor-penrose`, `tensor-spline` |
| **Quantum computing** | `quantum_spin_lang`, `berry_phase`, `entanglement`, `spin_statistics` |
| **Graphics/visualisation** | `voxel-engine`, `spectral-graphing-calculator`, `a2ui-render`, `snapkit-rs` |
| **Infrastructure** | `superinstance-cli`, `superinstance-runtime`, `superinstance-ffi`, `autoclaw` |
| **Research notes** | `RESEARCH/`, `AI-Writings/`, `captains-log/`, `blog-posts/` |
| **MIDI/audio** | 8 `.mid` files, `better_preset_output`, `style-dna` |
| **Testing/quality** | `docs/quality_bench/`, `constraint-substrate/rust/tests/`, `audits/` |

---

## Install (Zig Deadband Library)

### Prerequisites

- [Zig](https://ziglang.org/) 0.13+

### Build

```bash
git clone https://github.com/SuperInstance/lau-constellation.git
cd lau-constellation

zig build              # build the demo
zig build run          # run the deadband filter demo
zig build test         # run 16 unit tests
```

---

## Quick Start (Zig Deadband)

```zig
const deadband = @import("deadband-zig");

// Basic deadband: suppress values within ±0.5
var f = deadband.DeadbandFilter.init(0.5);
f.apply(0.3);   // → 0.0  (suppressed)
f.apply(1.2);   // → 1.2  (passed)

// With baseline: centre the deadband around a non-zero value
var fb = deadband.DeadbandFilter.initWithBaseline(0.5, 10.0);
fb.apply(10.3);  // → 10.0  (within ±0.5 of baseline)
fb.apply(11.0);  // → 11.0  (outside band)

// Rate-of-change limiter: cap output to ±1.0 per sample
var rl = deadband.RateLimitFilter.init(1.0);
rl.apply(0.0);   // → 0.0  (initialisation)
rl.apply(5.0);   // → 1.0  (clamped from delta=5 to max_rate=1)

// Persistence filter: require 3 consecutive out-of-band samples
var pf = deadband.PersistenceFilter.init(0.5, 3);
pf.apply(1.0);   // → 0.0  (count=1)
pf.apply(1.0);   // → 0.0  (count=2)
pf.apply(0.1);   // → 0.0  (reset — back inside band)
pf.apply(1.0);   // → 0.0  (count=1)
pf.apply(1.0);   // → 0.0  (count=2)
pf.apply(1.0);   // → 1.0  (count=3 — passes!)

// Batch processing
const inputs = [_]f64{ 0.1, 0.3, 1.0, 0.4, 2.0 };
var outputs: [5]f64 = undefined;
f.applyBatch(&inputs, &outputs);
```

---

## API Reference

### `DeadbandFilter` — Basic deadband

| Method | Description |
|---|---|
| `init(threshold)` | Create with threshold, baseline = 0 |
| `initWithBaseline(threshold, baseline)` | Create with non-zero baseline |
| `apply(value) → f64` | Suppress within ±threshold of baseline; returns `last_output` if suppressed |
| `applyRescale(value, max_value) → f64` | Deadband with linear rescale (smooth transition at boundary) |
| `applyBatch(inputs, outputs)` | Process array of samples |
| `setThreshold(t)` | Change threshold at runtime |
| `setBaseline(b)` | Change baseline |
| `reset()` | Clear all state |

**Fields:** `threshold`, `baseline`, `last_output`, `suppressed_count`

### `RateLimitFilter` — Rate-of-change cap

| Method | Description |
|---|---|
| `init(max_rate)` | Create with maximum change per sample |
| `apply(value) → f64` | Clamp output to ±max_rate from previous |
| `applyBatch(inputs, outputs)` | Process array |
| `reset()` | Clear state |

### `PersistenceFilter` — Consecutive-sample requirement

| Method | Description |
|---|---|
| `init(threshold, required_count)` | Require N consecutive out-of-band samples |
| `apply(value) → f64` | Only passes after N consecutive exceedances |
| `applyBatch(inputs, outputs)` | Process array |
| `setThreshold(t)` | Change threshold |
| `reset()` | Clear counter |

### Free functions

```zig
deadband.apply(value, threshold) → f64          // stateless basic deadband
deadband.apply_rescale(value, threshold) → f64   // stateless with rescale (max=1.0)
```

---

## How It Works

### Basic Deadband

```
output = value            if |value - baseline| > threshold
output = last_output      if |value - baseline| ≤ threshold
```

Values inside the deadband zone are suppressed — the output holds at `last_output` (or baseline for the first sample). This prevents chattering in control loops.

### Linear Rescale

The basic deadband has a discontinuity at the boundary — the output jumps from suppressed to the raw value. For smooth joystick curves, `applyRescale` maps the transition:

$$\text{output} = \text{baseline} + \text{sign}(v) \cdot \frac{|v - \text{baseline}| - \text{threshold}}{\text{max\_value} - \text{threshold}}$$

This makes the output continuous: it's 0 at the threshold boundary and reaches ±1.0 at `max_value`.

### Rate Limiting

Cap the per-sample change: `output = last + clamp(value - last, -max_rate, +max_rate)`. Useful for motor controllers where sudden setpoint changes cause mechanical stress.

### Persistence Filtering

Count consecutive samples outside the deadband. Only update the output when the counter reaches `required_count`. A single transient spike is ignored. The counter resets to zero when any sample falls back inside the band.

---

## The Math

### Deadband as a Nonlinearity

A deadband is a memoryless nonlinearity $f: \mathbb{R} \to \mathbb{R}$:

$$f(x) = \begin{cases} x - d & x > d \\ 0 & |x| \leq d \\ x + d & x < -d \end{cases}$$

With rescaling, it becomes:

$$f(x) = \begin{cases} \text{sgn}(x) \cdot \frac{|x| - d}{m - d} & |x| > d \\ 0 & |x| \leq d \end{cases}$$

where $d$ is the threshold and $m$ is the maximum input value.

### Energy Conservation

A deadband filter does not conserve signal energy — it removes it deliberately. The energy removed is exactly the energy of the suppressed band. This makes deadband filters useful in energy-aware control systems where actuator cycling has a real energy cost.

---

## Testing

**16 Zig tests** covering:

- Basic deadband: zero within threshold, passes outside, zero threshold passes everything
- Rescale: boundary mapping, full-range mapping, negative side, midpoint
- Struct-based filter: suppression counting, baseline mode, batch processing, runtime threshold change, reset
- Rate limiter: passes small changes, clamps large jumps, batch processing
- Persistence: requires consecutive samples, resets on return to band

```bash
zig build test
```

---

## Repository Structure

```
lau-constellation/
├── src/main.zig          # Zig deadband library + demo + tests
├── build.zig             # Zig build configuration
├── RESEARCH/             # Experiment results and research notes
├── AI-Writings/          # AI-generated essays and analyses
├── constraint-substrate/ # Rust constraint-checking system
├── spectral-conservation/# Spectral energy conservation experiments
├── flux-lang/            # Flux programming language experiments
├── eisenstein/           # Eisenstein integer research
├── voxel-engine/         # 3D voxel rendering
├── snapkit-rs/           # Rust snap kit
├── turbovec/             # Vector operations
├── plato-room-musician/  # AI music generation
├── ... 350+ more project directories
└── *.mid                 # MIDI files for music experiments
```

---

## Why Zig?

Zero-cost abstractions, comptime, no hidden allocations. Deadband filters run in embedded systems and hot loops — Zig's performance characteristics make it a natural fit. The broader constellation uses whatever language fits the problem: Rust for systems code, C for interop, Fortran for numerics, Zig for embedded/signal processing.

---

## License

MIT
