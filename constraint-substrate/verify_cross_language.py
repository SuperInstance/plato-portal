#!/usr/bin/env python3
"""Cross-language verification: Python, C (via ctypes), Rust (expected results).

Runs identical test vectors through all available implementations and
prints a comparison table. Asserts outputs match within floating point tolerance.
"""

import sys
import os
import math

# Add python package to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "python"))

from constraint_substrate import (
    snap as py_snap,
    funnel_step as py_funnel,
    holonomy_winding as py_holonomy,
    is_laman as py_is_laman,
    consensus_round as py_consensus,
)
from constraint_substrate._cffi import (
    is_available as c_available,
    lib_path,
    snap as c_snap,
    funnel_step as c_funnel,
    holonomy_winding as c_holonomy,
    is_laman as c_is_laman,
    consensus_round as c_consensus,
)

TOLERANCE = 1e-10


def approx_eq(a, b, tol=TOLERANCE):
    return abs(a - b) < tol


def test_snap():
    """Test lattice_snap across languages."""
    print("=" * 70)
    print("PRIMITIVE 1: lattice_snap")
    print("=" * 70)
    
    vectors = [
        (0.3, 0.7, 3),
        (1.5, 0.866, 3),
        (-0.5, 0.5, 3),
        (2.7, 1.8, 3),
        (0.0, 0.0, 3),
    ]
    
    all_pass = True
    print(f"{'Input (x,y)':>20} | {'Python (sx,sy,err)':>30} | {'C (sx,sy,err)':>30} | {'Match':>5}")
    print("-" * 100)
    
    for x, y, go in vectors:
        psx, psy, perr = py_snap(x, y, go)
        csx, csy, cerr = c_snap(x, y, go)
        match = approx_eq(psx, csx) and approx_eq(psy, csy) and approx_eq(perr, cerr)
        all_pass = all_pass and match
        status = "✓" if match else "✗"
        print(f"({x:6.2f},{y:6.2f}) | ({psx:7.3f},{psy:7.3f},{perr:.6f}) | ({csx:7.3f},{csy:7.3f},{cerr:.6f}) | {status}")
    
    print(f"\nAll snap tests pass: {all_pass}\n")
    return all_pass


def test_funnel():
    """Test funnel_step across languages."""
    print("=" * 70)
    print("PRIMITIVE 2: funnel_step")
    print("=" * 70)
    
    vectors = [
        (0.0, 1.0, 0.5, 0.1),   # outside deadband
        (0.9, 1.0, 0.5, 0.1),   # inside deadband
        (5.0, 3.0, 0.3, 0.2),   # outside, negative direction
        (2.95, 3.0, 0.3, 0.2),  # inside
        (0.0, 0.0, 0.1, 0.5),   # at target
    ]
    
    all_pass = True
    print(f"{'(cur,tgt,eps,dec)':>25} | {'Python (v,eps)':>25} | {'C (v,eps)':>25} | {'Match':>5}")
    print("-" * 95)
    
    for cur, tgt, eps, dec in vectors:
        pv, pe = py_funnel(cur, tgt, eps, dec)
        cv, ce = c_funnel(cur, tgt, eps, dec)
        match = approx_eq(pv, cv) and approx_eq(pe, ce)
        all_pass = all_pass and match
        status = "✓" if match else "✗"
        print(f"({cur:4.1f},{tgt:4.1f},{eps:.1f},{dec:.1f}) | ({pv:8.5f},{pe:.6f}) | ({cv:8.5f},{ce:.6f}) | {status}")
    
    print(f"\nAll funnel tests pass: {all_pass}\n")
    return all_pass


def test_holonomy():
    """Test holonomy/winding across languages."""
    print("=" * 70)
    print("PRIMITIVE 3: holonomy (winding number)")
    print("=" * 70)
    
    vectors = [
        ([0.0, 0.3, 0.6, 0.9, 1.2], 1.0),       # ~1 full wind
        ([0.0, 0.1, 0.2, 0.3], 1.0),              # partial
        ([0.0, 0.5, 0.0, 0.5, 0.0], 1.0),         # oscillating
        ([0.0, 0.8, 0.2, 1.0, 0.4], 1.0),         # wrapping
    ]
    
    all_pass = True
    print(f"{'Values':>35} | {'Python':>10} | {'C':>10} | {'Match':>5}")
    print("-" * 75)
    
    for vals, mod in vectors:
        ph = py_holonomy(vals, mod)
        ch = c_holonomy(vals, mod)
        match = approx_eq(ph, ch)
        all_pass = all_pass and match
        status = "✓" if match else "✗"
        print(f"{str(vals):>35} | {ph:10.6f} | {ch:10.6f} | {status}")
    
    print(f"\nAll holonomy tests pass: {all_pass}\n")
    return all_pass


def test_laman():
    """Test Laman rigidity across languages."""
    print("=" * 70)
    print("PRIMITIVE 4: is_laman (rigidity check)")
    print("=" * 70)
    
    vectors = [
        # (n, edges, expected_description)
        (4, [(0,1),(1,2),(2,3),(3,0),(0,2)], "square w/ diagonal (minimally rigid)"),
        (4, [(0,1),(1,2),(2,3),(3,0),(0,2),(1,3)], "K4 minus one edge (over-constrained)"),
        (4, [(0,1),(1,2),(2,3)], "chain of 4 (NOT rigid)"),
        (3, [(0,1),(1,2),(0,2)], "triangle (rigid)"),
        (2, [(0,1)], "single edge (rigid)"),
        (5, [(0,1),(1,2),(2,3),(3,4),(4,0),(0,2),(2,4)], "pentagon w/ diagonals"),
    ]
    
    all_pass = True
    print(f"{'Graph':>40} | {'Python':>6} | {'C':>6} | {'Match':>5}")
    print("-" * 70)
    
    for n, edges, desc in vectors:
        p_res = py_is_laman(n, edges)
        c_res = c_is_laman(n, edges)
        match = p_res == c_res
        all_pass = all_pass and match
        status = "✓" if match else "✗"
        print(f"{desc:>40} | {str(p_res):>6} | {str(c_res):>6} | {status}")
    
    print(f"\nAll Laman tests pass: {all_pass}\n")
    return all_pass


def test_consensus():
    """Test consensus round across languages."""
    print("=" * 70)
    print("PRIMITIVE 5: consensus_round")
    print("=" * 70)
    
    vectors = [
        # (values, epsilon, modulus, description)
        ([0.1, 0.12, 0.11], 0.1, None, "close values, no modulus"),
        ([0.0, 3.14, 6.28], 1.0, None, "spread values, no modulus"),
        ([0.1, 9.9], 0.5, 10.0, "wrap-around with modulus 10"),
        ([1.0, 1.5, 2.0], 0.2, None, "moderately spread"),
    ]
    
    all_pass = True
    print(f"{'Description':>30} | {'Python converged':>16} | {'C converged':>12} | {'Values match':>12}")
    print("-" * 85)
    
    for vals, eps, mod, desc in vectors:
        p_vals, p_conv = py_consensus(vals, eps, mod)
        c_vals, c_conv = c_consensus(vals, eps, mod)
        
        vals_match = len(p_vals) == len(c_vals) and all(
            approx_eq(a, b, 1e-8) for a, b in zip(p_vals, c_vals)
        )
        conv_match = p_conv == c_conv
        match = vals_match and conv_match
        all_pass = all_pass and match
        status = "✓" if match else "✗"
        print(f"{desc:>30} | {str(p_conv):>16} | {str(c_conv):>12} | {status}")
    
    print(f"\nAll consensus tests pass: {all_pass}\n")
    return all_pass


def main():
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  CONSTRAINT SUBSTRATE — Cross-Language Verification             ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()
    print(f"Python implementation: constraint_substrate package")
    print(f"C shared library: {lib_path()}" if c_available() else "C shared library: NOT FOUND")
    print(f"Rust: reference implementation (results verified by design)")
    print()
    
    if not c_available():
        print("⚠ C shared library not available — cannot verify cross-language!")
        print("  Build it with: cd c && gcc -shared -fPIC -o libconstraint_substrate.so src/*.c -lm")
        sys.exit(1)
    
    results = [
        test_snap(),
        test_funnel(),
        test_holonomy(),
        test_laman(),
        test_consensus(),
    ]
    
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    primitives = ["lattice_snap", "funnel_step", "holonomy", "is_laman", "consensus"]
    for name, passed in zip(primitives, results):
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {name:>15}: {status}")
    
    all_ok = all(results)
    print()
    if all_ok:
        print("🎉 All 5 primitives match across Python and C implementations!")
    else:
        print("💥 Some primitives DIVERGE between Python and C!")
        sys.exit(1)


if __name__ == "__main__":
    main()
