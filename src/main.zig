const std = @import("std");

// ============================================================
// Deadband Filter Library — Zig Implementation
// ============================================================
//
// A deadband filter suppresses small changes around a reference
// value (baseline). Essential in control systems, sensor readings,
// joystick input, and anywhere noise produces meaningless jitter.
//
// Three filter types:
//   1. Basic      — suppress values within ±threshold of baseline
//   2. RateLimit  — cap how fast the output can change per sample
//   3. Persistence— require N consecutive out-of-band samples
// ============================================================

// ------------------------------------------------------------
// DeadbandFilter — basic configurable deadband
// ------------------------------------------------------------

pub const DeadbandFilter = struct {
    threshold: f64,
    baseline: f64,
    last_output: f64,
    suppressed_count: u64,

    pub fn init(threshold: f64) DeadbandFilter {
        std.debug.assert(threshold >= 0);
        return .{
            .threshold = threshold,
            .baseline = 0.0,
            .last_output = 0.0,
            .suppressed_count = 0,
        };
    }

    pub fn initWithBaseline(threshold: f64, baseline: f64) DeadbandFilter {
        std.debug.assert(threshold >= 0);
        return .{
            .threshold = threshold,
            .baseline = baseline,
            .last_output = baseline,
            .suppressed_count = 0,
        };
    }

    pub fn setThreshold(self: *DeadbandFilter, threshold: f64) void {
        std.debug.assert(threshold >= 0);
        self.threshold = threshold;
    }

    pub fn setBaseline(self: *DeadbandFilter, baseline: f64) void {
        self.baseline = baseline;
    }

    /// Apply basic deadband: values within ±threshold of baseline are suppressed.
    pub fn apply(self: *DeadbandFilter, value: f64) f64 {
        if (@abs(value - self.baseline) <= self.threshold) {
            self.suppressed_count += 1;
            return self.last_output;
        }
        self.last_output = value;
        return value;
    }

    /// Apply deadband with linear rescale. Maps the transition at
    /// ±threshold to 0.0 output, then linearly to full range.
    /// Requires baseline = 0 and threshold < max_value.
    pub fn applyRescale(self: *DeadbandFilter, value: f64, max_value: f64) f64 {
        std.debug.assert(self.threshold < max_value);
        const relative = value - self.baseline;
        if (@abs(relative) <= self.threshold) {
            self.suppressed_count += 1;
            return self.baseline;
        }
        const sign: f64 = if (relative > 0) 1.0 else -1.0;
        const rescaled = self.baseline + sign * (@abs(relative) - self.threshold) / (max_value - self.threshold);
        self.last_output = rescaled;
        return rescaled;
    }

    /// Process a batch of samples, writing outputs into the provided slice.
    pub fn applyBatch(self: *DeadbandFilter, inputs: []const f64, outputs: []f64) void {
        std.debug.assert(inputs.len == outputs.len);
        for (inputs, outputs) |inp, *out| {
            out.* = self.apply(inp);
        }
    }

    pub fn reset(self: *DeadbandFilter) void {
        self.baseline = 0.0;
        self.last_output = 0.0;
        self.suppressed_count = 0;
    }
};

// ------------------------------------------------------------
// RateLimitFilter — cap rate of change
// ------------------------------------------------------------

pub const RateLimitFilter = struct {
    max_rate: f64, // max change per sample
    last_output: f64,
    initialized: bool,

    pub fn init(max_rate: f64) RateLimitFilter {
        std.debug.assert(max_rate >= 0);
        return .{
            .max_rate = max_rate,
            .last_output = 0.0,
            .initialized = false,
        };
    }

    pub fn apply(self: *RateLimitFilter, value: f64) f64 {
        if (!self.initialized) {
            self.last_output = value;
            self.initialized = true;
            return value;
        }
        const delta = value - self.last_output;
        if (@abs(delta) <= self.max_rate) {
            self.last_output = value;
            return value;
        }
        const clamped = self.last_output + if (delta > 0) self.max_rate else -self.max_rate;
        self.last_output = clamped;
        return clamped;
    }

    pub fn applyBatch(self: *RateLimitFilter, inputs: []const f64, outputs: []f64) void {
        std.debug.assert(inputs.len == outputs.len);
        for (inputs, outputs) |inp, *out| {
            out.* = self.apply(inp);
        }
    }

    pub fn reset(self: *RateLimitFilter) void {
        self.last_output = 0.0;
        self.initialized = false;
    }
};

// ------------------------------------------------------------
// PersistenceFilter — require N consecutive exceedances
// ------------------------------------------------------------

pub const PersistenceFilter = struct {
    threshold: f64,
    baseline: f64,
    required_count: u32,
    consecutive_count: u32,
    last_output: f64,
    pending_value: f64,

    pub fn init(threshold: f64, required_count: u32) PersistenceFilter {
        std.debug.assert(threshold >= 0);
        std.debug.assert(required_count > 0);
        return .{
            .threshold = threshold,
            .baseline = 0.0,
            .required_count = required_count,
            .consecutive_count = 0,
            .last_output = 0.0,
            .pending_value = 0.0,
        };
    }

    pub fn setThreshold(self: *PersistenceFilter, threshold: f64) void {
        std.debug.assert(threshold >= 0);
        self.threshold = threshold;
    }

    /// Apply persistence filter. Value must exceed deadband for
    /// `required_count` consecutive samples before output changes.
    pub fn apply(self: *PersistenceFilter, value: f64) f64 {
        if (@abs(value - self.baseline) <= self.threshold) {
            // Back inside deadband — reset counter
            self.consecutive_count = 0;
            return self.last_output;
        }
        // Outside deadband
        self.consecutive_count += 1;
        self.pending_value = value;
        if (self.consecutive_count >= self.required_count) {
            self.last_output = value;
            return value;
        }
        return self.last_output;
    }

    pub fn applyBatch(self: *PersistenceFilter, inputs: []const f64, outputs: []f64) void {
        std.debug.assert(inputs.len == outputs.len);
        for (inputs, outputs) |inp, *out| {
            out.* = self.apply(inp);
        }
    }

    pub fn reset(self: *PersistenceFilter) void {
        self.consecutive_count = 0;
        self.last_output = 0.0;
        self.pending_value = 0.0;
    }
};

// ------------------------------------------------------------
// Free functions (original API preserved)
// ------------------------------------------------------------

/// Apply a deadband filter: values within ±threshold are treated as zero.
pub fn apply(value: f64, threshold: f64) f64 {
    std.debug.assert(threshold >= 0);
    if (@abs(value) <= threshold) return 0.0;
    return value;
}

/// Apply deadband with rescale: output is linearly mapped so the transition
/// at ±threshold maps to 0.0 and the full-range maps linearly beyond.
pub fn apply_rescale(value: f64, threshold: f64) f64 {
    std.debug.assert(threshold >= 0);
    std.debug.assert(threshold < 1.0);
    if (@abs(value) <= threshold) return 0.0;
    const sign: f64 = if (value > 0) 1.0 else -1.0;
    return sign * (@abs(value) - threshold) / (1.0 - threshold);
}

// ============================================================
// Demo
// ============================================================

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();

    try stdout.print("=== Deadband Filter Demo ===\n\n", .{});

    // --- Basic deadband ---
    const test_values = [_]f64{ -2.0, -0.8, -0.05, 0.0, 0.03, 0.5, 1.5 };
    const threshold: f64 = 0.1;

    try stdout.print("Basic Deadband (threshold={d:.2})\n", .{threshold});
    try stdout.print("{s:>10} | {s:>10} | {s:>10}\n", .{ "Input", "Output", "Rescaled" });
    try stdout.print("{s:>10}-+-{s:>10}-+-{s:>10}\n", .{ "----------", "----------", "----------" });

    for (test_values) |v| {
        try stdout.print("{d:>10.3} | {d:>10.3} | {d:>10.3}\n", .{
            v,
            apply(v, threshold),
            apply_rescale(v, threshold),
        });
    }
    try stdout.print("\n", .{});

    // --- Struct-based filter with tracking ---
    try stdout.print("Struct-based filter with signal tracking:\n", .{});
    var filter = DeadbandFilter.init(0.5);
    const samples = [_]f64{ 0.1, 0.2, 0.3, 1.0, 0.4, 0.6 };
    for (samples) |s| {
        const out = filter.apply(s);
        try stdout.print("  input={d:.2} -> output={d:.2}\n", .{ s, out });
    }
    try stdout.print("  suppressed: {d} / {d} samples\n\n", .{ filter.suppressed_count, samples.len });

    // --- Rate-of-change limiter ---
    try stdout.print("Rate-of-change limiter (max_rate=1.0):\n", .{});
    var rl = RateLimitFilter.init(1.0);
    const rl_samples = [_]f64{ 0.0, 0.5, 2.5, 5.0, 3.0 };
    for (rl_samples) |s| {
        try stdout.print("  input={d:.2} -> output={d:.2}\n", .{ s, rl.apply(s) });
    }
    try stdout.print("\n", .{});

    // --- Persistence filter ---
    try stdout.print("Persistence filter (threshold=0.5, require=3):\n", .{});
    var pf = PersistenceFilter.init(0.5, 3);
    const pf_samples = [_]f64{ 0.1, 1.0, 1.0, 1.0, 0.2, 1.0 };
    for (pf_samples) |s| {
        try stdout.print("  input={d:.2} -> output={d:.2}\n", .{ s, pf.apply(s) });
    }
    try stdout.print("\n", .{});
}

// ============================================================
// Tests
// ============================================================

test "basic deadband - zero within threshold" {
    try std.testing.expect(apply(0.0, 0.1) == 0.0);
    try std.testing.expect(apply(0.05, 0.1) == 0.0);
    try std.testing.expect(apply(-0.1, 0.1) == 0.0);
}

test "basic deadband - passes values outside threshold" {
    try std.testing.expect(apply(0.11, 0.1) == 0.11);
    try std.testing.expect(apply(-0.5, 0.1) == -0.5);
    try std.testing.expect(apply(100.0, 0.1) == 100.0);
}

test "basic deadband - zero threshold passes everything" {
    try std.testing.expect(apply(0.0, 0.0) == 0.0);
    try std.testing.expect(apply(0.001, 0.0) == 0.001);
    try std.testing.expect(apply(-42.0, 0.0) == -42.0);
}

test "rescale deadband" {
    // At threshold boundary -> 0.0
    try std.testing.expect(apply_rescale(0.1, 0.1) == 0.0);
    // At 1.0 (full range) -> 1.0
    try std.testing.expectApproxEqAbs(apply_rescale(1.0, 0.1), 1.0, 1e-10);
    // At 0.55 with threshold 0.1 -> (0.55-0.1)/(1.0-0.1) = 0.5
    try std.testing.expectApproxEqAbs(apply_rescale(0.55, 0.1), 0.5, 1e-10);
    // Negative side
    try std.testing.expectApproxEqAbs(apply_rescale(-0.55, 0.1), -0.5, 1e-10);
}

test "DeadbandFilter struct - suppresses within threshold" {
    var f = DeadbandFilter.init(0.5);
    // Within threshold: returns last_output (which starts at 0.0)
    try std.testing.expect(f.apply(0.3) == 0.0);
    try std.testing.expect(f.suppressed_count == 1);
    try std.testing.expect(f.apply(-0.4) == 0.0);
    try std.testing.expect(f.suppressed_count == 2);
}

test "DeadbandFilter struct - passes outside threshold" {
    var f = DeadbandFilter.init(0.5);
    const result = f.apply(1.0);
    try std.testing.expect(result == 1.0);
    try std.testing.expect(f.last_output == 1.0);
    try std.testing.expect(f.suppressed_count == 0);
}

test "DeadbandFilter struct - setThreshold at runtime" {
    var f = DeadbandFilter.init(0.1);
    try std.testing.expect(f.apply(0.15) == 0.15); // outside 0.1
    f.setThreshold(0.5);
    try std.testing.expect(f.apply(0.15) == 0.15); // now within 0.5, returns last_output
}

test "DeadbandFilter struct - initWithBaseline" {
    var f = DeadbandFilter.initWithBaseline(0.5, 10.0);
    // Value 10.3 is within ±0.5 of baseline 10.0
    try std.testing.expect(f.apply(10.3) == 10.0); // returns last_output = baseline
    try std.testing.expect(f.suppressed_count == 1);
    // Value 11.0 is outside
    try std.testing.expect(f.apply(11.0) == 11.0);
}

test "DeadbandFilter struct - batch processing" {
    var f = DeadbandFilter.init(0.5);
    const inputs = [_]f64{ 0.1, 0.3, 1.0, 0.4, 2.0 };
    var outputs: [5]f64 = undefined;
    f.applyBatch(&inputs, &outputs);
    // 0.1 -> suppressed (last=0), 0.3 -> suppressed, 1.0 -> pass, 0.4 -> suppressed (last=1.0), 2.0 -> pass
    try std.testing.expect(outputs[0] == 0.0);
    try std.testing.expect(outputs[1] == 0.0);
    try std.testing.expect(outputs[2] == 1.0);
    try std.testing.expect(outputs[3] == 1.0); // returns last_output since suppressed
    try std.testing.expect(outputs[4] == 2.0);
    try std.testing.expect(f.suppressed_count == 3);
}

test "RateLimitFilter - passes small changes" {
    var f = RateLimitFilter.init(1.0);
    // First sample initializes
    try std.testing.expect(f.apply(5.0) == 5.0);
    try std.testing.expect(f.apply(5.5) == 5.5);
    try std.testing.expect(f.apply(6.0) == 6.0);
}

test "RateLimitFilter - clamps large jumps" {
    var f = RateLimitFilter.init(1.0);
    _ = f.apply(0.0);
    // Jump from 0 to 5 -> clamped to 1.0
    try std.testing.expect(f.apply(5.0) == 1.0);
    // Jump from 1 to -3 -> delta = -4, clamped to 0.0
    try std.testing.expect(f.apply(-3.0) == 0.0);
}

test "RateLimitFilter - batch processing" {
    var f = RateLimitFilter.init(2.0);
    const inputs = [_]f64{ 0.0, 1.0, 10.0, 8.0 };
    var outputs: [4]f64 = undefined;
    f.applyBatch(&inputs, &outputs);
    try std.testing.expect(outputs[0] == 0.0); // init
    try std.testing.expect(outputs[1] == 1.0); // within rate
    try std.testing.expect(outputs[2] == 3.0); // 1.0 + 2.0 (clamped)
    try std.testing.expect(outputs[3] == 5.0); // 3.0 -> 8.0 delta=5, clamped to 3.0+2.0=5.0
}

test "PersistenceFilter - requires consecutive samples" {
    var f = PersistenceFilter.init(0.5, 3);
    // Below threshold -> no change
    try std.testing.expect(f.apply(0.1) == 0.0);
    // Outside threshold, count=1
    try std.testing.expect(f.apply(1.0) == 0.0);
    // count=2
    try std.testing.expect(f.apply(1.0) == 0.0);
    // count=3 -> passes!
    try std.testing.expect(f.apply(1.0) == 1.0);
}

test "PersistenceFilter - resets on return to band" {
    var f = PersistenceFilter.init(0.5, 3);
    _ = f.apply(1.0); // count=1
    _ = f.apply(0.1); // back inside -> reset
    try std.testing.expect(f.consecutive_count == 0);
    // Need 3 more
    _ = f.apply(1.0);
    _ = f.apply(1.0);
    try std.testing.expect(f.apply(1.0) == 1.0);
}

test "DeadbandFilter - rescale via struct" {
    var f = DeadbandFilter.init(0.2);
    const result = f.applyRescale(0.6, 1.0);
    // (0.6 - 0.2) / (1.0 - 0.2) = 0.4 / 0.8 = 0.5
    try std.testing.expectApproxEqAbs(result, 0.5, 1e-10);
}

test "DeadbandFilter - reset clears state" {
    var f = DeadbandFilter.init(0.5);
    _ = f.apply(1.0);
    _ = f.apply(0.1);
    try std.testing.expect(f.suppressed_count == 1);
    f.reset();
    try std.testing.expect(f.last_output == 0.0);
    try std.testing.expect(f.suppressed_count == 0);
    try std.testing.expect(f.baseline == 0.0);
}
