#!/usr/bin/env python3
"""Python quality benchmark — uses mpmath for high-precision reference values."""

import json
import math
import struct
import sys
import os
import hashlib
import random
import cmath
import wave
import numpy as np
from collections import Counter
from mpmath import mp, mpf, atan, sin as mpsin, log as mplog, cos as mpcos, pi as mppi, sqrt as mpsqrt, linspace

RESULTS = {}

def bits_of_agreement(computed, reference_str):
    """Count bits of agreement between computed float and reference string."""
    ref = float(reference_str)
    if computed == ref:
        return 53  # max for double
    err = abs(computed - ref)
    if err == 0:
        return 53
    bits = -math.log2(err)
    return max(0, min(53, bits))

def q1_precision():
    """Q1: Compute π via Machin's formula."""
    pi_computed = 16.0 * math.atan(1.0/5.0) - 4.0 * math.atan(1.0/239.0)
    ground_truth = "3.14159265358979323846264338327950288419716939937510"
    bits = bits_of_agreement(pi_computed, ground_truth)
    RESULTS["Q1_precision"] = {"pi": pi_computed, "bits_of_agreement": round(bits, 2)}

def q2_consistency():
    """Q2: sin(1.0) 10000 times, measure variance."""
    vals = [math.sin(1.0) for _ in range(10000)]
    mean = sum(vals) / len(vals)
    variance = sum((v - mean)**2 for v in vals) / len(vals)
    RESULTS["Q2_consistency"] = {"variance": variance, "should_be_zero": variance < 1e-30}

def q3_linearity():
    """Q3: log(x) at different scales, measure relative error."""
    xs = [1e-10, 1e-5, 1.0, 1e5, 1e10]
    mp.dps = 50
    errors = []
    for x in xs:
        computed = math.log(x)
        reference = float(mplog(mpf(x)))
        if reference != 0:
            rel_err = abs((computed - reference) / reference)
        else:
            rel_err = abs(computed - reference)
        errors.append({"x": x, "rel_error": rel_err})
    RESULTS["Q3_linearity"] = {"errors": errors}

def q4_smoothness():
    """Q4: sin(1.0) vs sin(1.0+eps), compare with |cos(1.0)|."""
    eps = sys.float_info.epsilon
    s1 = math.sin(1.0)
    s2 = math.sin(1.0 + eps)
    delta = abs(s2 - s1)
    expected = abs(math.cos(1.0)) * eps
    ratio = delta / expected if expected != 0 else float('inf')
    RESULTS["Q4_smoothness"] = {"delta": delta, "expected": expected, "ratio": ratio}

def q5_spectral():
    """Q5: Generate 440Hz sine, FFT, measure spurious harmonics."""
    sample_rate = 44100
    duration = 1.0
    freq = 440.0
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * freq * t)
    
    # Save WAV
    wav_path = os.path.join(os.path.dirname(__file__), "python_440hz.wav")
    signal_int = (signal * 32767).astype(np.int16)
    with wave.open(wav_path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(signal_int.tobytes())
    
    # FFT
    fft = np.fft.rfft(signal)
    magnitudes = np.abs(fft)
    fundamental_bin = int(freq * len(signal) / sample_rate)
    fundamental_mag = magnitudes[fundamental_bin]
    
    # Find spurious harmonics (exclude bins near fundamental ±5)
    spurious_mags = []
    for i, m in enumerate(magnitudes):
        if abs(i - fundamental_bin) > 5 and m > 0:
            spurious_mags.append(m)
    
    if spurious_mags:
        max_spurious = max(spurious_mags)
        spur_dB = 20 * np.log10(max_spurious / fundamental_mag) if fundamental_mag > 0 else -999
    else:
        spur_dB = -999
    
    RESULTS["Q5_spectral"] = {"spurious_dB": round(float(spur_dB), 2), "wav_file": wav_path}

def q6_temporal_drift():
    """Q6: Logistic map, compare with Decimal reference."""
    from decimal import Decimal, getcontext
    getcontext().prec = 50
    
    r = Decimal('3.9')
    x = Decimal('0.4')
    iterations = 1000000
    
    # Reference in Decimal
    ref_vals = []
    for _ in range(iterations):
        x = r * x * (1 - x)
        ref_vals.append(float(x))
    
    # Float version
    r_f = 3.9
    x_f = 0.4
    first_diverge = -1
    for i in range(iterations):
        x_f = r_f * x_f * (1 - x_f)
        if first_diverge == -1 and x_f != ref_vals[i]:
            first_diverge = i
    
    RESULTS["Q6_temporal_drift"] = {"first_divergence_iteration": first_diverge}

def q7_accumulation():
    """Q7: Sum 10^6 random numbers, naive vs Kahan."""
    random.seed(42)
    nums = [random.uniform(-1, 1) for _ in range(1000000)]
    
    naive = sum(nums)
    
    # Kahan summation
    kahan = 0.0
    c = 0.0
    for x in nums:
        y = x - c
        t = kahan + y
        c = (t - kahan) - y
        kahan = t
    
    # Reference with mpmath
    mp.dps = 50
    ref = float(sum(mpf(str(x)) for x in nums))
    
    naive_err = abs(naive - ref) / abs(ref) if ref != 0 else 0
    kahan_err = abs(kahan - ref) / abs(ref) if ref != 0 else 0
    improvement = naive_err / kahan_err if kahan_err != 0 else float('inf')
    
    RESULTS["Q7_accumulation"] = {
        "naive_sum": naive,
        "kahan_sum": kahan,
        "reference": ref,
        "naive_rel_error": naive_err,
        "kahan_rel_error": kahan_err,
        "improvement_ratio": improvement
    }

def q8_edge_cases():
    """Q8: IEEE 754 edge case compliance."""
    score = 0
    total = 6
    details = {}
    
    # 0/0 should be NaN
    try:
        r = 0.0 / 0.0
        details["zero_div_zero"] = math.isnan(r)
        if math.isnan(r): score += 1
    except:
        details["zero_div_zero"] = False
    
    # 1/0 should be inf
    try:
        r = 1.0 / 0.0
        details["one_div_zero"] = math.isinf(r)
        if math.isinf(r): score += 1
    except:
        details["one_div_zero"] = False
    
    # sqrt(-1) should be NaN
    try:
        r = math.sqrt(-1.0)
        details["sqrt_neg1"] = math.isnan(r)
        if math.isnan(r): score += 1
    except:
        # Exception is also acceptable
        details["sqrt_neg1"] = "exception"
        score += 1
    
    # -0 == 0 should be True
    neg_zero = -0.0
    pos_zero = 0.0
    details["neg_zero_eq_pos_zero"] = (neg_zero == pos_zero)
    if neg_zero == pos_zero: score += 1
    
    # NaN == NaN should be False
    details["nan_eq_nan"] = not (float('nan') == float('nan'))
    if not (float('nan') == float('nan')): score += 1
    
    # inf - inf should be NaN
    try:
        r = float('inf') - float('inf')
        details["inf_minus_inf"] = math.isnan(r)
        if math.isnan(r): score += 1
    except:
        details["inf_minus_inf"] = False
    
    RESULTS["Q8_edge_cases"] = {"score": f"{score}/{total}", "details": details, "percent": round(score/total*100, 1)}

def q9_cross_config():
    """Q9: Cross-optimization comparison — Python has no compiler flags, report N/A."""
    # Python doesn't have optimization flags like C
    # We run the same computation and report it as baseline
    val = math.sin(1.0) + math.cos(1.0) + math.log(2.0) + math.exp(1.0)
    RESULTS["Q9_cross_config"] = {"note": "Python has no optimization levels", "reference_value": val}

def q10_error_entropy():
    """Q10: Shannon entropy of sin(x) error distribution."""
    mp.dps = 30
    N = 10000
    errors = []
    for i in range(N):
        x = 2 * math.pi * i / N
        computed = math.sin(x)
        reference = float(mpsin(mpf(x)))
        errors.append(computed - reference)
    
    # Bin the errors
    num_bins = 100
    min_e = min(errors)
    max_e = max(errors)
    if max_e == min_e:
        entropy = 0.0
    else:
        bin_width = (max_e - min_e) / num_bins
        counts = [0] * num_bins
        for e in errors:
            b = int((e - min_e) / bin_width)
            if b >= num_bins: b = num_bins - 1
            counts[b] += 1
        
        total = sum(counts)
        entropy = 0.0
        for c in counts:
            if c > 0:
                p = c / total
                entropy -= p * math.log2(p)
    
    RESULTS["Q10_error_entropy"] = {"shannon_entropy_bits": round(entropy, 4), "num_samples": N}

if __name__ == "__main__":
    print("=== Python Quality Benchmark ===")
    for i, fn in enumerate([q1_precision, q2_consistency, q3_linearity, q4_smoothness,
                            q5_spectral, q6_temporal_drift, q7_accumulation, q8_edge_cases,
                            q9_cross_config, q10_error_entropy], 1):
        print(f"  Running Q{i}: {fn.__doc__.strip()}")
        try:
            fn()
        except Exception as e:
            RESULTS[f"Q{i}_error"] = str(e)
            print(f"    ERROR: {e}")
    
    out_path = os.path.join(os.path.dirname(__file__), "results_python.json")
    with open(out_path, 'w') as f:
        json.dump(RESULTS, f, indent=2)
    print(f"\nResults written to {out_path}")
    print(json.dumps(RESULTS, indent=2))
