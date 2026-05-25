#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const results = {};

// Q1: Precision - Machin's formula for pi
function q1_precision() {
    const pi = 16.0 * Math.atan(1.0/5.0) - 4.0 * Math.atan(1.0/239.0);
    const ref = 3.14159265358979323846;
    const err = Math.abs(pi - ref);
    const bits = err > 0 ? Math.min(53, Math.max(0, -Math.log2(err))) : 53;
    results.Q1_precision = { pi, bits_of_agreement: Math.round(bits * 100) / 100 };
    console.log(`  Q1: bits_of_agreement = ${bits.toFixed(2)}`);
}

// Q2: Consistency
function q2_consistency() {
    const vals = Array.from({length: 10000}, () => Math.sin(1.0));
    const mean = vals.reduce((a, b) => a + b, 0) / 10000;
    const variance = vals.reduce((a, v) => a + (v - mean) ** 2, 0) / 10000;
    results.Q2_consistency = { variance };
    console.log(`  Q2: variance = ${variance}`);
}

// Q3: Linearity
function q3_linearity() {
    const xs = [1e-10, 1e-5, 1.0, 1e5, 1e10];
    const refs = [-23.025850929940457, -11.512925464970229, 0.0, 11.512925464970229, 23.025850929940457];
    const errors = xs.map((x, i) => {
        const c = Math.log(x);
        const r = refs[i];
        const rel = r !== 0 ? Math.abs((c - r) / r) : Math.abs(c);
        return { x, rel_error: rel };
    });
    results.Q3_linearity = { errors };
    console.log(`  Q3: done`);
}

// Q4: Smoothness
function q4_smoothness() {
    const eps = Number.EPSILON;
    const s1 = Math.sin(1.0);
    const s2 = Math.sin(1.0 + eps);
    const delta = Math.abs(s2 - s1);
    const expected = Math.abs(Math.cos(1.0)) * eps;
    const ratio = delta / expected;
    results.Q4_smoothness = { delta, expected, ratio };
    console.log(`  Q4: ratio = ${ratio.toFixed(6)}`);
}

// Q5: Spectral - generate WAV and check harmonics
function q5_spectral() {
    const sr = 44100, n = 44100, freq = 440;
    const signal = new Float64Array(n);
    for (let i = 0; i < n; i++) {
        signal[i] = Math.sin(2 * Math.PI * freq * i / sr);
    }
    
    // Write WAV
    const bufSize = 44 + n * 2;
    const buf = Buffer.alloc(bufSize);
    buf.write('RIFF', 0);
    buf.writeUInt32LE(bufSize - 8, 4);
    buf.write('WAVE', 8);
    buf.write('fmt ', 12);
    buf.writeUInt32LE(16, 16);
    buf.writeUInt16LE(1, 20); // PCM
    buf.writeUInt16LE(1, 22); // mono
    buf.writeUInt32LE(sr, 24);
    buf.writeUInt32LE(sr * 2, 28);
    buf.writeUInt16LE(2, 32);
    buf.writeUInt16LE(16, 34);
    buf.write('data', 36);
    buf.writeUInt32LE(n * 2, 40);
    for (let i = 0; i < n; i++) {
        const s = Math.max(-32768, Math.min(32767, Math.round(signal[i] * 32767)));
        buf.writeInt16LE(s, 44 + i * 2);
    }
    fs.writeFileSync(path.join(__dirname, 'node_440hz.wav'), buf);
    
    // Simple DFT at fundamental
    const fundBin = Math.floor(freq * n / sr);
    let fundRe = 0, fundIm = 0;
    for (let i = 0; i < n; i++) {
        const t = 2 * Math.PI * fundBin * i / n;
        fundRe += signal[i] * Math.cos(t);
        fundIm -= signal[i] * Math.sin(t);
    }
    const fundMag = Math.sqrt(fundRe*fundRe + fundIm*fundIm) / n * 2;
    
    // Check harmonics
    const checkBins = [2*440, 3*440, 5*440, 7*440, 100, 1000, 5000, 10000, 20000];
    let maxSpur = 0;
    for (const b of checkBins) {
        if (b >= n/2) continue;
        let re = 0, im = 0;
        for (let i = 0; i < n; i++) {
            const t = 2 * Math.PI * b * i / n;
            re += signal[i] * Math.cos(t);
            im -= signal[i] * Math.sin(t);
        }
        const mag = Math.sqrt(re*re + im*im) / n * 2;
        if (mag > maxSpur) maxSpur = mag;
    }
    const spurDB = fundMag > 0 ? 20 * Math.log10(maxSpur / fundMag) : -999;
    results.Q5_spectral = { spurious_dB: Math.round(spurDB * 100) / 100 };
    console.log(`  Q5: spurious_dB = ${spurDB.toFixed(2)}`);
}

// Q6: Temporal drift
function q6_temporal_drift() {
    // JS doesn't have float32 natively, use Float32Array
    let xf_arr = new Float32Array([0.4]);
    let xd = 0.4;
    const r = 3.9;
    let firstDiv = -1;
    for (let i = 0; i < 1000000; i++) {
        xf_arr[0] = r * xf_arr[0] * (1.0 - xf_arr[0]);
        xd = r * xd * (1.0 - xd);
        if (firstDiv === -1 && xf_arr[0] !== xd) firstDiv = i;
    }
    results.Q6_temporal_drift = { f32_vs_f64_diverge: firstDiv };
    console.log(`  Q6: f32 vs f64 diverge at ${firstDiv}`);
}

// Q7: Accumulation
function q7_accumulation() {
    // Simple LCG
    let state = 42n;
    const nums = [];
    for (let i = 0; i < 1000000; i++) {
        state = (state * 6364136223846793005n + 1442695040888963407n) & ((1n << 64n) - 1n);
        const x = Number(state >> 33n) / (1 << 31) * 2 - 1;
        nums.push(x);
    }
    const naive = nums.reduce((a, b) => a + b, 0);
    let kahan = 0, c = 0;
    for (const x of nums) {
        const y = x - c;
        const t = kahan + y;
        c = (t - kahan) - y;
        kahan = t;
    }
    const diff = Math.abs(naive - kahan) / Math.max(Math.abs(kahan), 1e-30);
    results.Q7_accumulation = { naive, kahan, relative_diff: diff };
    console.log(`  Q7: rel_diff = ${diff.toExponential(6)}`);
}

// Q8: Edge cases
function q8_edge_cases() {
    let score = 0;
    const details = {};
    
    // 0/0
    const r1 = 0/0;
    details.zero_div_zero = Number.isNaN(r1);
    if (Number.isNaN(r1)) score++;
    
    // 1/0
    const r2 = 1/0;
    details.one_div_zero = Number.isFinite(r2) === false && !Number.isNaN(r2);
    if (details.one_div_zero) score++;
    
    // sqrt(-1) - JS returns NaN
    const r3 = Math.sqrt(-1);
    details.sqrt_neg1 = Number.isNaN(r3);
    if (Number.isNaN(r3)) score++;
    
    // -0 == 0
    details.neg_zero_eq = (-0 === 0);
    if (-0 === 0) score++;
    
    // NaN == NaN
    details.nan_eq_nan_false = (NaN !== NaN);
    if (NaN !== NaN) score++;
    
    // inf - inf
    const r6 = Infinity - Infinity;
    details.inf_minus_inf = Number.isNaN(r6);
    if (Number.isNaN(r6)) score++;
    
    results.Q8_edge_cases = { score: `${score}/6`, details, percent: Math.round(score/6*1000)/10 };
    console.log(`  Q8: score = ${score}/6`);
}

// Q9: Cross config (no compiler flags for JS)
function q9_cross_config() {
    const val = Math.sin(1) + Math.cos(1) + Math.log(2) + Math.exp(1);
    results.Q9_cross_config = { note: "JS has no optimization levels", reference_value: val };
    console.log(`  Q9: reference value = ${val}`);
}

// Q10: Error entropy
function q10_error_entropy() {
    const N = 10000;
    const errors = new Float64Array(N);
    let maxErr = 0;
    for (let i = 0; i < N; i++) {
        const x = 2 * Math.PI * i / N;
        const xf = Math.fround(x); // force float32
        errors[i] = Math.sin(x) - Math.fround(Math.sin(xf));
        if (Math.abs(errors[i]) > maxErr) maxErr = Math.abs(errors[i]);
    }
    const numBins = 100;
    const counts = new Uint32Array(numBins);
    const bw = 2 * maxErr / numBins;
    for (let i = 0; i < N; i++) {
        let b = Math.floor((errors[i] + maxErr) / bw);
        b = Math.min(b, numBins - 1);
        counts[b]++;
    }
    let entropy = 0;
    for (let i = 0; i < numBins; i++) {
        if (counts[i] > 0) {
            const p = counts[i] / N;
            entropy -= p * Math.log2(p);
        }
    }
    results.Q10_error_entropy = { shannon_entropy_bits: Math.round(entropy * 10000) / 10000, num_samples: N };
    console.log(`  Q10: entropy = ${entropy.toFixed(4)} bits`);
}

console.log('=== Node.js Quality Benchmark ===');
q1_precision();
q2_consistency();
q3_linearity();
q4_smoothness();
q5_spectral();
q6_temporal_drift();
q7_accumulation();
q8_edge_cases();
q9_cross_config();
q10_error_entropy();

const outPath = path.join(__dirname, 'results_node.json');
fs.writeFileSync(outPath, JSON.stringify(results, null, 2));
console.log(`\nResults written to ${outPath}`);
