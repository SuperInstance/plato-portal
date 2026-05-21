# deadband-zig

A deadband filter library in Zig — because sometimes the best thing a signal can do is *nothing*.

## Why does your thermostat wait 2 degrees before turning on?

You set it to 70°F. The room hits 69.5°F. The heater doesn't kick in. It waits until 68°F.

That's a deadband. And it's not a bug — it's the entire point.

Without it, your heater would cycle on and off every few seconds as the temperature wiggles by 0.1°F around the setpoint. That constant switching wastes energy, wears out the compressor, and shortens the life of the equipment. The deadband says: *ignore small changes. Only react when it matters.*

This pattern shows up everywhere:

- **Joysticks** — the stick never reads exactly 0.0. A deadband ignores the resting noise so your character doesn't slowly drift.
- **Sensor filtering** — an ADC reading 4096 might fluctuate between 4094 and 4098. A deadband treats those as the same value.
- **Motor control** — prevents oscillation around a target position by ignoring tiny positioning errors.
- **Audio** — noise gates are deadbands in disguise. Silence anything below a threshold.

## The math

A deadband filter defines a zone around a reference (baseline). Any value inside that zone is treated as "no change." Values outside the zone pass through.

```
         passed through
        /
       /
---[---|---]---  →  baseline ± threshold
       \
        \
         passed through
```

With rescaling, the output is linearly mapped so the transition at the threshold boundary maps to zero output:

```
output = sign × (|input| - threshold) / (max - threshold)
```

This removes the "jump" at the boundary — useful for smooth joystick curves.

## Filter types

### Basic Deadband

Suppress values within ±threshold. Simple and fast.

```zig
var f = DeadbandFilter.init(0.5);
f.apply(0.3);  // → 0.0  (suppressed, within ±0.5)
f.apply(1.2);  // → 1.2  (passed, outside ±0.5)
```

### Rate-of-Change Limit

Cap how fast the output can change per sample. Prevents sudden jumps.

```zig
var f = RateLimitFilter.init(1.0);  // max change of 1.0 per sample
f.apply(0.0);  // → 0.0  (initialization)
f.apply(5.0);  // → 1.0  (clamped: would have jumped 5.0, limited to 1.0)
f.apply(2.5);  // → 2.0  (clamped: delta 1.5, limited to 1.0)
```

### Persistence Filter

The signal must exceed the threshold for N *consecutive* samples before the output changes. Eliminates transient spikes.

```zig
var f = PersistenceFilter.init(0.5, 3);  // threshold=0.5, require 3 samples
f.apply(1.0);  // → 0.0  (count=1, need 3)
f.apply(1.0);  // → 0.0  (count=2, need 3)
f.apply(0.1);  // → 0.0  (back inside band, counter reset)
f.apply(1.0);  // → 0.0  (count=1 again)
f.apply(1.0);  // → 0.0  (count=2)
f.apply(1.0);  // → 1.0  (count=3, passes!)
```

## Usage

```zig
const deadband = @import("deadband-zig");

// Basic
var f = deadband.DeadbandFilter.init(0.1);
const result = f.apply(0.05);  // 0.0 (suppressed)

// Change threshold at runtime
f.setThreshold(0.5);

// Track state
const suppressed = f.suppressed_count;
const baseline = f.baseline;
const last = f.last_output;

// Batch process
const inputs = [_]f64{ 0.1, 0.3, 1.0, 0.4, 2.0 };
var outputs: [5]f64 = undefined;
f.applyBatch(&inputs, &outputs);

// Rate limiting
var rl = deadband.RateLimitFilter.init(0.5);

// Persistence
var pf = deadband.PersistenceFilter.init(0.5, 3);
```

## Building

```bash
zig build              # build the demo
zig build run          # run the demo
zig build test         # run tests (16 tests)
```

## API

| Type | Method | Description |
|------|--------|-------------|
| `DeadbandFilter` | `init(threshold)` | Create with threshold |
| | `initWithBaseline(threshold, baseline)` | Create with non-zero baseline |
| | `apply(value) → f64` | Filter single value |
| | `applyRescale(value, max) → f64` | Filter with linear rescale |
| | `applyBatch(inputs, outputs)` | Process array of samples |
| | `setThreshold(t)` | Change threshold at runtime |
| | `setBaseline(b)` | Change baseline |
| | `reset()` | Clear all state |
| `RateLimitFilter` | `init(max_rate)` | Create with max rate of change |
| | `apply(value) → f64` | Filter single value |
| | `applyBatch(inputs, outputs)` | Process array |
| | `reset()` | Clear state |
| `PersistenceFilter` | `init(threshold, count)` | Create with threshold and required consecutive samples |
| | `apply(value) → f64` | Filter single value |
| | `applyBatch(inputs, outputs)` | Process array |
| | `setThreshold(t)` | Change threshold |
| | `reset()` | Clear state |

## Why Zig?

Zero-cost abstractions, comptime, no hidden allocations. Deadband filters run in embedded systems and hot loops — Zig's performance characteristics make it a natural fit.

## License

MIT
