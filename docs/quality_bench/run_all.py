#!/usr/bin/env python3
"""Master benchmark orchestrator — compile, run, collect, plot."""

import json
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path

DIR = Path(__file__).parent
os.chdir(DIR)

ALL_RESULTS = {}

def run(cmd, label, timeout=300):
    """Run a command, return stdout."""
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"  cmd: {cmd}")
    print(f"{'='*60}")
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        print(r.stdout[-3000:] if len(r.stdout) > 3000 else r.stdout)
        if r.stderr:
            print("STDERR:", r.stderr[-1000:] if len(r.stderr) > 1000 else r.stderr)
        if r.returncode != 0:
            print(f"  ⚠ Return code: {r.returncode}")
        return r
    except subprocess.TimeoutExpired:
        print(f"  ⚠ TIMEOUT ({timeout}s)")
        return None
    except Exception as e:
        print(f"  ⚠ ERROR: {e}")
        return None

def load_json(path, label):
    """Load results JSON from file."""
    try:
        with open(path) as f:
            data = json.load(f)
        ALL_RESULTS[label] = data
        print(f"  ✓ Loaded {path}")
        return data
    except Exception as e:
        print(f"  ✗ Failed to load {path}: {e}")
        ALL_RESULTS[label] = {"error": str(e)}
        return None

# ============================================================
# 1. Python (reference)
# ============================================================
print("\n" + "█"*60)
print("  PYTHON BENCHMARK")
print("█"*60)
run("python3 benchmark_python.py", "Python")
load_json("results_python.json", "python")

# ============================================================
# 2. C — multiple optimization levels
# ============================================================
print("\n" + "█"*60)
print("  C BENCHMARK")
print("█"*60)

c_flags = ["-O0", "-O2", "-Ofast", "-ffast-math"]
c_results = {}

for flag in c_flags:
    exe = f"benchmark_c_{flag.replace('-','')}"
    r = run(f"gcc {flag} -o {exe} benchmark_c.c -lm", f"C compile {flag}")
    if r and r.returncode == 0:
        run(f"./{exe}", f"C run {flag}")
        # Q9 cross-config value
        r9 = run(f"./{exe} --q9", f"C Q9 {flag}")
        if r9 and r9.stdout.strip():
            try:
                q9data = json.loads(r9.stdout.strip())
                c_results[flag] = q9data.get("q9_value", "N/A")
            except:
                c_results[flag] = r9.stdout.strip()

# Load main C results (from -O2 run)
load_json("results_c.json", "c")

# Add cross-config to C results
if "c" in ALL_RESULTS and isinstance(ALL_RESULTS["c"], dict) and "Q9_cross_config" in ALL_RESULTS["c"]:
    ALL_RESULTS["c"]["Q9_cross_config"]["optimization_values"] = c_results

# ============================================================
# 3. Fortran
# ============================================================
print("\n" + "█"*60)
print("  FORTRAN BENCHMARK")
print("█"*60)

fortran_flags = ["-O0", "-O2", "-Ofast", "-ffast-math"]
fortran_q9 = {}

for flag in fortran_flags:
    exe = f"benchmark_fortran_{flag.replace('-','')}"
    r = run(f"gfortran {flag} -o {exe} benchmark_fortran.f90", f"Fortran compile {flag}")
    if r and r.returncode == 0:
        run(f"./{exe}", f"Fortran run {flag}")

# Fortran outputs to stdout, parse it into results
ALL_RESULTS["fortran"] = {"note": "Results printed to stdout above (no JSON writer in Fortran stdlib)"}

# ============================================================
# 4. Rust
# ============================================================
print("\n" + "█"*60)
print("  RUST BENCHMARK")
print("█"*60)

# Check if serde_json is available
serde_check = run("ls ~/.cargo/registry/cache/*/serde_json-* 2>/dev/null | head -1", "Check serde_json")
if serde_check and serde_check.stdout.strip():
    # Has serde_json crate cached
    rust_code = open("benchmark_rust.rs").read()
    # Check if Cargo.toml exists, if not create a simple project
    if not os.path.exists("Cargo.toml"):
        run("cargo init --name bench_temp .", "Rust init")
    # Write Cargo.toml with serde_json
    with open("Cargo.toml", "w") as f:
        f.write('[package]\nname = "bench_temp"\nversion = "0.1.0"\nedition = "2021"\n\n[dependencies]\nserde_json = "1"\n')
    # Copy rust source to src/main.rs
    os.makedirs("src", exist_ok=True)
    import shutil
    shutil.copy("benchmark_rust.rs", "src/main.rs")
    run("cargo build --release 2>&1 | tail -5", "Rust build")
    run("./target/release/bench_temp", "Rust run")
    load_json("results_rust.json", "rust")
else:
    # Try without serde_json - rewrite a simpler version
    print("  No serde_json available, running simplified Rust benchmark...")
    simple_rust = '''
use std::f64::consts::PI;
use std::io::Write;

fn main() {
    println!("=== Rust Quality Benchmark (simplified) ===");
    
    // Q1
    let pi = 16.0_f64 * (1.0_f64/5.0_f64).atan() - 4.0_f64 * (1.0_f64/239.0_f64).atan();
    println!("  Q1: pi = {:.20}", pi);
    
    // Q2
    let s = 1.0_f64.sin();
    println!("  Q2: sin(1.0) = {:.20} (constant)", s);
    
    // Q3
    for x in [1e-10_f64, 1e-5, 1.0, 1e5, 1e10] {
        println!("      ln({:.1e}) = {:.15}", x, x.ln());
    }
    
    // Q4
    let eps = f64::EPSILON;
    let ratio = ((1.0 + eps).sin() - 1.0_f64.sin()).abs() / (1.0_f64.cos().abs() * eps);
    println!("  Q4: smoothness ratio = {:.6}", ratio);
    
    // Q6
    let mut xf: f32 = 0.4;
    let mut xd: f64 = 0.4;
    let r: f64 = 3.9;
    let mut fd = -1i64;
    for i in 0..1_000_000 {
        xf = (r as f32) * xf * (1.0 - xf);
        xd = r * xd * (1.0 - xd);
        if fd == -1 && (xf as f64) != xd { fd = i; }
    }
    println!("  Q6: f32 vs f64 diverge at {}", fd);
    
    // Q8
    let mut score = 0;
    if (0.0_f64 / 0.0).is_nan() { score += 1; }
    // Rust may panic on 1.0/0.0 in debug
    let inf_ok = std::panic::catch_unwind(|| 1.0_f64 / 0.0);
    if inf_ok.map(|v| v.is_infinite()).unwrap_or(false) { score += 1; }
    if (-1.0_f64).sqrt().is_nan() { score += 1; }
    if -0.0_f64 == 0.0_f64 { score += 1; }
    if !(f64::NAN == f64::NAN) { score += 1; }
    if (f64::INFINITY - f64::INFINITY).is_nan() { score += 1; }
    println!("  Q8: IEEE score = {}/6", score);
    
    println!("\\n=== Rust done ===");
}
'''
    with open("/tmp/bench_rust_simple.rs", "w") as f:
        f.write(simple_rust)
    run("rustc -O -o benchmark_rust_simple /tmp/bench_rust_simple.rs", "Rust compile")
    run("./benchmark_rust_simple", "Rust run")
    ALL_RESULTS["rust"] = {"note": "Simplified benchmark (no serde_json), see stdout above"}

# ============================================================
# 5. CUDA
# ============================================================
print("\n" + "█"*60)
print("  CUDA BENCHMARK")
print("█"*60)

r = run("nvcc -O2 -o benchmark_cuda benchmark_cuda.cu -lm 2>&1", "CUDA compile")
if r and r.returncode == 0:
    run("./benchmark_cuda", "CUDA run")
    ALL_RESULTS["cuda"] = {"note": "Results printed to stdout above"}
else:
    print("  ⚠ CUDA compilation failed — skipping")
    ALL_RESULTS["cuda"] = {"error": "Compilation failed (likely no GPU available)"}

# ============================================================
# 6. Node.js
# ============================================================
print("\n" + "█"*60)
print("  NODE.JS BENCHMARK")
print("█"*60)
run("node benchmark_node.js", "Node.js")
load_json("results_node.json", "node")

# ============================================================
# Save combined results
# ============================================================
with open("quality_results.json", "w") as f:
    json.dump(ALL_RESULTS, f, indent=2)
print(f"\n✓ All results saved to quality_results.json")

# ============================================================
# Generate plots
# ============================================================
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    
    # --- Radar plot per language ---
    categories = ['Q1\nPrecision', 'Q2\nConsistency', 'Q3\nLinearity', 
                   'Q4\nSmoothness', 'Q5\nSpectral', 'Q6\nDrift',
                   'Q7\nAccum.', 'Q8\nIEEE', 'Q10\nEntropy']
    
    def extract_scores(data, label):
        """Extract normalized 0-10 scores from results."""
        scores = [5.0] * 9  # default
        
        if not isinstance(data, dict):
            return scores
            
        # Q1: bits of agreement (53 max → 10)
        q1 = data.get("Q1_precision", {})
        if "bits_of_agreement" in q1:
            scores[0] = min(10, q1["bits_of_agreement"] / 5.3)
        
        # Q2: variance (0 → 10, 1e-20 → ~5)
        q2 = data.get("Q2_consistency", {})
        if "variance" in q2:
            v = q2["variance"]
            scores[1] = 10 if v == 0 else max(0, 10 + np.log10(max(v, 1e-100)))
        
        # Q3: average relative error
        q3 = data.get("Q3_linearity", {})
        if "errors" in q3:
            avg_err = np.mean([e["rel_error"] for e in q3["errors"]])
            scores[2] = 10 if avg_err == 0 else max(0, min(10, -np.log10(max(avg_err, 1e-20))))
        
        # Q4: ratio (1.0 → 10)
        q4 = data.get("Q4_smoothness", {})
        if "ratio" in q4:
            scores[3] = max(0, 10 - abs(q4["ratio"] - 1.0) * 10)
        
        # Q5: spurious dB (more negative = better)
        q5 = data.get("Q5_spectral", {})
        if "spurious_dB" in q5:
            scores[4] = min(10, max(0, (-q5["spurious_dB"]) / 30 * 10))
        
        # Q6: drift iteration (higher = better, normalize to 10 at 1M)
        q6 = data.get("Q6_temporal_drift", {})
        drift_key = [k for k in q6 if "diverge" in k.lower()] if isinstance(q6, dict) else []
        if drift_key:
            dv = q6[drift_key[0]]
            scores[5] = min(10, max(0, dv / 100000))  # 100k iterations = 10
        
        # Q7: relative diff (smaller = better)
        q7 = data.get("Q7_accumulation", {})
        if "relative_diff" in q7:
            rd = q7["relative_diff"]
            scores[6] = 10 if rd == 0 else max(0, min(10, -np.log10(max(rd, 1e-30)) * 2))
        
        # Q8: IEEE percent
        q8 = data.get("Q8_edge_cases", {})
        if "percent" in q8:
            scores[7] = q8["percent"] / 10
        
        # Q10: entropy (higher = more uniform error = better for well-behaved)
        q10 = data.get("Q10_error_entropy", {})
        if "shannon_entropy_bits" in q10:
            scores[8] = min(10, q10["shannon_entropy_bits"] / 6.5 * 10)
        
        return scores
    
    lang_colors = {
        'python': '#3776AB', 'c': '#555555', 'node': '#68A063',
        'rust': '#DEA584', 'fortran': '#734F96', 'cuda': '#76B900'
    }
    
    for lang, data in ALL_RESULTS.items():
        if lang == "error": continue
        scores = extract_scores(data, lang)
        
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        scores_plot = scores + [scores[0]]
        angles += [angles[0]]
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        ax.fill(angles, scores_plot, alpha=0.25, color=lang_colors.get(lang, 'gray'))
        ax.plot(angles, scores_plot, 'o-', linewidth=2, color=lang_colors.get(lang, 'gray'), label=lang)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=9)
        ax.set_ylim(0, 10)
        ax.set_yticks([2, 4, 6, 8, 10])
        ax.set_title(f'Quality Benchmark: {lang.upper()}', size=14, pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        plt.tight_layout()
        plt.savefig(f'radar_{lang}.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Saved radar_{lang}.png")
    
    # --- Cross-language heatmap ---
    lang_labels = []
    all_scores = []
    for lang, data in ALL_RESULTS.items():
        if isinstance(data, dict) and "error" not in data:
            lang_labels.append(lang.upper())
            all_scores.append(extract_scores(data, lang))
    
    if all_scores:
        fig, ax = plt.subplots(figsize=(10, 6))
        scores_arr = np.array(all_scores)
        im = ax.imshow(scores_arr, cmap='RdYlGn', aspect='auto', vmin=0, vmax=10)
        ax.set_xticks(range(len(categories)))
        ax.set_xticklabels([c.replace('\n', ' ') for c in categories], rotation=45, ha='right')
        ax.set_yticks(range(len(lang_labels)))
        ax.set_yticklabels(lang_labels)
        
        for i in range(len(lang_labels)):
            for j in range(len(categories)):
                ax.text(j, i, f'{scores_arr[i,j]:.1f}', ha='center', va='center', fontsize=8,
                       color='white' if scores_arr[i,j] < 3 or scores_arr[i,j] > 7 else 'black')
        
        plt.colorbar(im, label='Score (0-10)')
        ax.set_title('Cross-Language Quality Comparison', size=14)
        plt.tight_layout()
        plt.savefig('heatmap_cross_language.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("  ✓ Saved heatmap_cross_language.png")

except ImportError:
    print("  ⚠ matplotlib not available, skipping plots")

# ============================================================
# Summary
# ============================================================
print("\n" + "█"*60)
print("  SUMMARY")
print("█"*60)
for lang, data in ALL_RESULTS.items():
    if isinstance(data, dict):
        q8 = data.get("Q8_edge_cases", {})
        q1 = data.get("Q1_precision", {})
        print(f"  {lang:10s} | Q1 bits: {q1.get('bits_of_agreement', 'N/A'):>6} | Q8 IEEE: {q8.get('score', 'N/A'):>5}")
    else:
        print(f"  {lang:10s} | (no structured data)")

print("\n✓ Benchmark suite complete!")
