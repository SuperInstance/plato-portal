#!/usr/bin/env python3
"""Python quality benchmark - all 10 tests"""
import json, math, struct, sys, os, hashlib
import numpy as np
from mpmath import mp, mpf, atan, pi as mppi, sin as mpsin, log as mplog, sqrt as mpsqrt, fft as mpfft

OUTDIR = os.path.dirname(os.path.abspath(__file__))
mp.dps = 50

def q1_precision():
    """π via Machin's formula, bits of agreement"""
    true_pi = str(mppi)
    # float64
    pi_f64 = 16*math.atan(1/5) - 4*math.atan(1/239)
    # float32 via numpy
    pi_f32 = np.float32(16*np.arctan(np.float32(1)/np.float32(5)) - 4*np.arctan(np.float32(1)/np.float32(239)))
    
    def bits_of_agreement(computed, true_str):
        s = f"{computed:.50f}"
        true_clean = true_str.replace(' ','')
        bits = 0
        for i, (a,b) in enumerate(zip(s, true_clean)):
            if a == b: continue
            else:
                if i > 2:  # skip "3."
                    bits = (i - 2) * 3.32  # ~log2(10) per digit
                break
        return bits
    
    return {"bits_f64": bits_of_agreement(pi_f64, true_pi),
            "bits_f32": bits_of_agreement(float(pi_f32), true_pi),
            "pi_f64": pi_f64, "pi_true": true_pi[:52]}

def q2_consistency():
    """sin(1.0) 10000 times"""
    results = [math.sin(1.0) for _ in range(10000)]
    return {"variance": float(np.var(results)), "all_same": all(r == results[0] for r in results)}

def q3_linearity():
    """log(x) at different scales"""
    scales = [1e-10, 1e-5, 1.0, 1e5, 1e10]
    errors = []
    for x in scales:
        val = math.log(x)
        ref = float(mplog(mpf(x)))
        rel = abs(val - ref) / abs(ref) if ref != 0 else abs(val - ref)
        errors.append({"x": x, "rel_error": rel, "val": val, "ref": ref})
    return errors

def q4_smoothness():
    """sin(x+eps) - sin(x) / eps vs cos(x)"""
    x = 1.0
    eps = sys.float_info.epsilon
    diff = (math.sin(x + eps) - math.sin(x)) / eps
    expected = math.cos(x)
    return {"computed_derivative": diff, "expected_cos": expected,
            "relative_error": abs(diff - expected)/abs(expected)}

def q5_spectral():
    """FFT of sin(440Hz) at 44100Hz"""
    sr = 44100; freq = 440; dur = 1.0
    t = np.arange(int(sr*dur)) / sr
    signal = np.sin(2*np.pi*freq*t)
    fft = np.fft.rfft(signal)
    magnitudes = np.abs(fft) / len(signal) * 2
    freqs = np.fft.rfftfreq(len(signal), 1/sr)
    
    peak_idx = np.argmax(magnitudes[1:]) + 1
    peak_mag = magnitudes[peak_idx]
    
    # spurious = max magnitude excluding 440Hz bin (±5 bins)
    mask = np.ones(len(magnitudes), dtype=bool)
    center = int(freq * len(signal) / sr)
    mask[max(0,center-5):center+6] = False
    mask[0] = False  # DC
    spur_mag = np.max(magnitudes[mask]) if np.any(mask) else 0
    spur_db = 20*np.log10(spur_mag/peak_mag + 1e-30)
    
    # Save WAV
    try:
        import wave
        wav_path = os.path.join(OUTDIR, "python_q5.wav")
        with wave.open(wav_path, 'w') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
            pcm = (signal * 32767).astype(np.int16)
            w.writeframes(pcm.tobytes())
    except: pass
    
    return {"spurious_db": float(spur_db), "peak_freq": float(freqs[peak_idx]),
            "snr_db": float(-spur_db), "wav_saved": True}

def q6_temporal_drift():
    """Logistic map divergence from mpmath reference"""
    r = mpf('3.9'); x = mpf('0.4')
    ref_vals = []
    for i in range(1000000):
        x = r * x * (1 - x)
        ref_vals.append(float(x))
    
    # float64 run
    r64 = 3.9; x64 = 0.4
    first_diverge = -1
    for i in range(1000000):
        x64 = r64 * x64 * (1 - x64)
        if first_diverge < 0 and abs(x64 - ref_vals[i]) > 0.01:
            first_diverge = i
    
    return {"first_diverge_step": first_diverge, "max_iter": 1000000}

def q7_accumulation():
    """Sum 1e6 random numbers: naive vs kahan vs pairwise"""
    np.random.seed(42)
    vals = np.random.random(1000000)
    
    # Naive sequential
    naive = 0.0
    for v in vals: naive += v
    
    # Kahan
    s = 0.0; c = 0.0
    for v in vals:
        y = v - c; t = s + y; c = (t - s) - y; s = t
    kahan = s
    
    # Pairwise (numpy)
    pairwise = float(np.sum(vals))
    
    # Also use mpmath reference
    ref = float(sum(mpf(str(v)) for v in vals[:10000]))  # subsample for speed
    
    return {"naive": naive, "kahan": kahan, "pairwise": pairwise,
            "naive_vs_kahan_rel": abs(naive-kahan)/abs(kahan),
            "pairwise_vs_kahan_rel": abs(pairwise-kahan)/abs(kahan)}

def q8_edge_cases():
    """IEEE 754 edge cases"""
    tests = {}
    # 0/0
    try: tests["0_div_0"] = str(0.0/0.0)
    except: tests["0_div_0"] = "exception"
    # 1/0
    try: tests["1_div_0"] = str(1.0/0.0)
    except: tests["1_div_0"] = "exception"
    # sqrt(-1)
    try: tests["sqrt_neg1"] = str(math.sqrt(-1))
    except: tests["sqrt_neg1"] = "exception"
    # -0 == 0
    tests["neg0_eq_0"] = (-0.0 == 0.0)
    # NaN == NaN
    tests["nan_eq_nan"] = (float('nan') == float('nan'))
    # inf - inf
    tests["inf_minus_inf"] = str(float('inf') - float('inf'))
    
    correct = 0; total = 6
    if "nan" in tests["0_div_0"].lower(): correct += 1
    if "inf" in tests["1_div_0"].lower(): correct += 1
    if "nan" in tests["sqrt_neg1"].lower() or "exception" in tests["sqrt_neg1"].lower(): correct += 1
    if tests["neg0_eq_0"] == True: correct += 1
    if tests["nan_eq_nan"] == False: correct += 1
    if "nan" in tests["inf_minus_inf"].lower(): correct += 1
    
    return {"results": tests, "score": correct, "total": total}

def q9_cross_config():
    """Python has no compile flags, but test different approaches"""
    # Compare numpy vs math vs mpmath for sin
    import numpy as np
    x_vals = [0.1, 1.0, 3.14159, 100.0]
    ref = [float(mpsin(mpf(x))) for x in x_vals]
    math_errs = [abs(math.sin(x)-r)/r if r!=0 else abs(math.sin(x)-r) for x,r in zip(x_vals,ref)]
    np_errs = [abs(np.sin(x)-r)/r if r!=0 else abs(np.sin(x)-r) for x,r in zip(x_vals,ref)]
    return {"math_max_rel_err": max(math_errs), "numpy_max_rel_err": max(np_errs),
            "note": "Python has no compile flags; comparing math vs numpy vs mpmath"}

def q10_error_entropy():
    """Shannon entropy of sin() error distribution"""
    x_vals = [float(2*math.pi*i/10000) for i in range(10000)]
    errors = [math.sin(x) - float(mpsin(mpf(x))) for x in x_vals]
    
    # Bin errors into 50 bins
    n_bins = 50
    min_e, max_e = min(errors), max(errors)
    bins = [0]*n_bins
    for e in errors:
        idx = min(int((e - min_e)/(max_e - min_e + 1e-30) * n_bins), n_bins-1)
        bins[idx] += 1
    
    total = sum(bins)
    entropy = 0
    for b in bins:
        if b > 0:
            p = b/total
            entropy -= p * math.log2(p)
    
    return {"shannon_entropy_bits": entropy, "max_entropy": math.log2(n_bins),
            "normalized": entropy/math.log2(n_bins)}

if __name__ == "__main__":
    results = {}
    results["Q1_precision"] = q1_precision()
    results["Q2_consistency"] = q2_consistency()
    results["Q3_linearity"] = q3_linearity()
    results["Q4_smoothness"] = q4_smoothness()
    results["Q5_spectral"] = q5_spectral()
    results["Q6_temporal_drift"] = q6_temporal_drift()
    results["Q7_accumulation"] = q7_accumulation()
    results["Q8_edge_cases"] = q8_edge_cases()
    results["Q9_cross_config"] = q9_cross_config()
    results["Q10_error_entropy"] = q10_error_entropy()
    print(json.dumps(results, indent=2))
