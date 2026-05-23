# BETA-R2: Constraint Substrate Math Rigor Re-Test

**Date:** 2026-05-22  
**Scope:** Verify Round 1 fixes, find new issues, cross-language validation

---

## Executive Summary

**Python fixes are correct.** All 5 reported fixes are mathematically sound in the Python reference implementation. 34/34 Python tests pass.

**Critical finding: Rust and C implementations were NOT updated to match the Python fixes.** They retain the Round 1 bugs and add new cross-language divergence issues. Tests pass only because Rust/C tests use loose tolerances that don't detect the discrepancies.

| Module | Python | Rust | C | Cross-Language Match |
|--------|--------|------|---|---------------------|
| is_laman | ✅ Fixed | ❌ Broken | ❌ Broken | ❌ Diverges |
| Funnel | ✅ Fixed | ❌ Broken | ❌ Broken | ❌ Diverges |
| Snap | ✅ Fixed | ❌ Wrong lattice | ❌ Wrong lattice | ❌ Diverges |
| Consensus | ✅ Fixed | ❌ No circular mean | ❌ No circular mean | ❌ Diverges |
| Holonomy | ✅ OK | ✅ OK | ✅ OK | ✅ Match |
| Covering radius | ✅ Correct | ✅ Correct | N/A | ✅ Match |

---

## Part 1: Fix Verification

### 1.1 is_laman — VERIFIED ✅

The Python fix adds full Laman subgraph condition checking via subset enumeration (n ≤ 10) or probabilistic sampling (n > 10).

**Test case that would FAIL without the fix:**

```python
# 5 vertices, 7 edges (= 2*5-3, passes edge count), but K4 subgraph on {0,1,2,3}
# has 6 > 2*4-3=5 edges → NOT Laman
edges = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3),(3,4)]
assert not is_laman(5, edges)  # Passes with fix, would fail without
```

**Mathematical correctness:**
- n < 2 → False ✅ (single vertex cannot be rigid)
- n == 2 → len(edges) ≥ 1 ✅ (one edge is minimally rigid in 2D)
- Edge count check: `len(edges) < 2n-3 → False` ✅
- Subgraph check: every k-subset has ≤ 2k-3 edges ✅ (exact enumeration for n ≤ 10)
- Over-constrained detection: since the full vertex set (k=n) is checked, any graph with |E| > 2n-3 is correctly rejected. So `>=` in condition 1 effectively means `==`. ✅

**Edge cases verified:**
- `is_laman(0, [])` → False ✅
- `is_laman(1, [])` → False ✅  
- `is_laman(2, [])` → False ✅
- `is_laman(2, [(0,1)])` → True ✅
- K4 (6 edges on 4 vertices) → False ✅ (6 > 2*4-3=5, caught by full-graph subset check)

**Note on disconnected graphs:** A disconnected graph cannot have 2n-3 edges (proven by counting: two components with n₁+n₂=n need 2n₁-3+2n₂-3 = 2n-6 < 2n-3 edges). So the edge count check alone rules out disconnectedness. No separate check needed. ✅

### 1.2 Funnel — VERIFIED ✅ (Python only)

**Test case: exponential vs linear decay**
```python
# With fix (exponential): new_eps = 1.0 * exp(-0.1) ≈ 0.9048
# Without fix (linear):    new_eps = 1.0 * (1 - 0.1) = 0.9
_, eps = funnel_step(1.0, 2.0, 1.0, 0.1)
assert abs(eps - math.exp(-0.1)) < 1e-12  # Passes only with exponential
```

**Mathematical properties verified:**
- Epsilon decays as ε₀ · e^(-k·rate), strictly positive for all k ✅
- After 10,000 steps with rate=0.5, epsilon = 2.47e-323 > 0 (hits subnormal floor) ✅
- Convergence: exponential decay gives geometric series with finite sum = ε₀/(1-e^(-rate)). For ε₀=1, rate=0.1, max reachable distance ≈ 10.5. ✅
- Within deadband correction: `diff * (1 - exp(-rate))` — moves fraction of remaining distance, consistent with exponential approach ✅

### 1.3 Snap — VERIFIED ✅ (Python only)

**Hand computation for snap(0.6, 0.8, 3):**
- Axial coordinates: b ≈ 2·0.8/√3 ≈ 0.9238, a ≈ 0.6 + 0.8/√3 ≈ 1.0619
- Floor: a_lo=1, b_lo=0
- Check 9 candidates; best is (a=1, b=1) → Cartesian (0.5, 0.866) with error 0.1198
- Python output: `(0.500000, 0.866025, 0.119831)` ✅ matches hand calculation

**Nearest-neighbor verification:** The 3×3 candidate grid centered on the floored coordinates always contains the true nearest lattice point for a hexagonal lattice, because the Voronoi cell is bounded by distance 1/√3 < 1 from any lattice point, and the candidate grid spans ±1 in both axial directions. ✅

### 1.4 Consensus — VERIFIED ✅ (Python only)

**Circular mean wrap-around test:**
```python
# values=[0.1, 0.9], modulus=1.0
# Arithmetic mean = 0.5 (WRONG — halfway around the circle)
# Circular mean: sin(0.2π)+sin(1.8π) ≈ 0, cos(0.2π)+cos(1.8π) ≈ 0
# → atan2 → ~0.0 or ~1.0 (near zero on the circle) ✅
```

**Convergence verified:** `[0.1, 0.9] mod 1.0` converges in 2 iterations to `[0.025, 0.025]`. ✅

**Antipodal degeneracy:** `[0.0, 0.5] mod 1.0` — sin_sum=0, cos_sum=0. Python's `atan2(0, 0)` returns 0.0, giving circular_mean=0.0. This is a degenerate case (any value on the circle is equidistant), but the algorithm still converges (to 0.25 after 5 iterations). The behavior is acceptable but should be documented.

### 1.5 Covering Radius — VERIFIED ✅

The covering radius of the A₂ lattice with unit spacing is 1/√3 ≈ 0.5774.

```
COVERING_RADIUS = 1/sqrt(3) = 1/(2·sin(π/3)) ≈ 0.5773502692
```

This is correct. Note: `1/(2·sin(π/n))` and `1/√3` are identical for n=3. The "fix" description claimed correction from `1/(2sin(π/n))` to `sin(π/n)`, but the actual code still uses `1/√3` which equals `1/(2sin(π/3))` — the supposed "old" value. **The code is correct; the fix description may be misleading.** Using `sin(π/3) = √3/2 ≈ 0.866` would be WRONG (that's the nearest-neighbor distance, not the covering radius).

---

## Part 2: NEW Issues Found

### 🔴 CRITICAL: Rust/C Not Updated — Cross-Language Divergence

The Round 1 fixes were applied **only to Python**. Rust and C retain the old, buggy algorithms. This violates the project's core promise: *"All three implementations produce identical results."*

#### Issue 2.1: Funnel — Linear vs Exponential Decay (Rust/C)

**Rust** (`src/lib.rs` line ~55):
```rust
let new_eps = epsilon * (1.0 - decay_rate);  // WRONG: linear
```

**C** (`src/funnel.c`):
```c
double new_eps = epsilon * (1.0 - decay);  // WRONG: linear
```

**Should be:**
```rust
let new_eps = epsilon * (-decay_rate).exp();  // exponential
```

**Impact:** For decay_rate=0.1, Python gives ε=0.9048, Rust/C give ε=0.9000. The divergence compounds: after 100 steps, Python's ε is 0.0000454 vs Rust/C's 2.66e-5 — a 71% relative error.

#### Issue 2.2: Lattice Snap — Different Lattice! (Rust/C)

**Python** snaps to Eisenstein integers Z[ω] with basis:
- e₁ = (1, 0)
- e₂ = (-1/2, √3/2)

**Rust/C** use a completely different coordinate system:
- Projects (x,y) → (q=2x/√3, r=y)
- Rounds q,r to integers
- Converts back: (sx=a·√3/2, sy=b)

This corresponds to basis vectors:
- e₁ = (√3/2, 0)  
- e₂ = (0, 1)

These are NOT the same lattice! The Python lattice has nearest-neighbor distance 1.0; the Rust lattice has nearest-neighbor distance ≈0.866.

**Empirical proof of divergence:**

| Input | Python snaps to | Rust/C snaps to |
|-------|----------------|-----------------|
| (1.0, 0.0) | (1.0, 0.0) | (0.866, 0.0) |
| (0.5, 0.866) | (0.5, 0.866) | (0.866, 1.0) |
| (0.01, 0.99) | (0.5, 0.866) | (0.0, 1.0) |
| (-0.5, 0.866) | (-0.5, 0.866) | (-0.866, 1.0) |

Only (0,0) produces the same result. **Every other lattice point diverges.**

#### Issue 2.3: Rigidity — No Subgraph Check (Rust/C)

**Rust** (`src/lib.rs`) and **C** (`src/rigidity.c`):
```rust
pub fn is_laman(n: u32, edges: &[(u32, u32)]) -> bool {
    if n < 2 { return false; }
    if n == 2 { return edges.len() >= 1; }
    edges.len() >= (2 * n as usize - 3)  // ONLY edge count check!
}
```

No Laman subgraph condition. Incorrectly returns `True` for:
- K4 (4 vertices, 6 edges): Python says False, Rust/C say True
- Dense subgraph (5 vertices with K4 subgraph): Python says False, Rust/C say True

#### Issue 2.4: Consensus — No Circular Mean (Rust/C)

**Rust** and **C** consensus functions only compute arithmetic mean. The `modulus` parameter for circular mean is entirely absent from both implementations and their APIs (`cs_consensus` and `consensus::round`).

The C header:
```c
CsConsensusResult cs_consensus(const double* values, uint32_t count, double epsilon);
// No modulus parameter!
```

### 🟡 MODERATE: Test Vector Coverage Gaps

#### Issue 2.5: vectors.json Missing Circular Mean Cases

The consensus vectors in `tests/vectors.json` have **no test cases with the `modulus` parameter**. All three cases use arithmetic mean only. This means:
- Circular mean code path is untested in cross-language validation
- The `modulus` parameter was added to Python but never added to the shared vectors

#### Issue 2.6: Funnel Vectors Use Exponential Values, Rust/C Can't Match

All funnel test vector epsilon values match `exp(-decay)` (exponential decay):
- `0.9048374180359595` = `1.0 * exp(-0.1)` ✅ exponential
- Rust/C would compute `0.9` (linear) and fail vector validation

Since Rust/C don't run against `vectors.json`, this doesn't cause test failures, but it proves the cross-language contract is broken.

#### Issue 2.7: Lattice Vectors Match Python Lattice Only

The lattice snap vectors use the Python Eisenstein lattice. Rust/C snap to a different lattice and would produce different (x, y) outputs for the same inputs. The vectors are not portable.

### 🟢 MINOR: Python-Specific Issues

#### Issue 2.8: Shadowing `round` Builtin

`consensus.py` defines `def round(...)` which shadows the Python builtin `round`. This is safe within the module (the function is renamed to `consensus_round` in `__init__.py`), but it's a code smell. If anyone calls `round()` inside `consensus.py` expecting the builtin, they'd get the wrong function.

#### Issue 2.9: Antipodal Degeneracy Undocumented

When all input values are perfectly evenly spaced around the circle (e.g., `[0.0, 0.5]` mod 1.0), the circular mean is mathematically undefined (sin_sum = cos_sum = 0). Python's `atan2(0, 0)` returns 0.0, which picks an arbitrary direction. The algorithm still converges but the intermediate behavior is implementation-dependent. This edge case should be documented.

#### Issue 2.10: Rigidity Probabilistic Check for n > 10

For large graphs (n > 10), the Python Laman check uses random sampling instead of exact enumeration. While the seed is fixed for reproducibility, a graph with a subtle Laman violation in a specific subgraph might not be caught. The comment mentions "A full pebble game algorithm would be better" — this is correct. The current implementation is a heuristic for n > 10.

---

## Part 3: Test Results

### Python (34/34 passed)
```
34 passed in 0.09s
```
All tests pass including new tests for circular mean wrap-around, Laman subgraph rejection, and exponential funnel decay.

### Rust (19/19 passed)
```
19 passed; 0 failed
```
Tests pass because they use loose tolerances (0.1, 0.5) that don't detect the mathematical errors. The Rust tests don't validate against `vectors.json`.

### C (28/28 passed)
```
28 passed, 0 failed
```
Same situation as Rust — loose tolerances mask the bugs.

---

## Summary of Action Items

### Must Fix (Cross-Language Correctness)
1. **Rust/C funnel**: Change `1.0 - decay_rate` → `(-decay_rate).exp()` / `exp(-decay)`
2. **Rust/C snap**: Rewrite to use Python's Eisenstein Z[ω] lattice with basis (1,0) and (-1/2, √3/2)
3. **Rust/C rigidity**: Add Laman subgraph condition (exact for n ≤ 10, probabilistic for n > 10)
4. **Rust/C consensus**: Add `modulus` parameter and circular mean (atan2-based) implementation

### Should Fix (Test Coverage)
5. Add circular mean test cases to `vectors.json`
6. Add cross-language vector validation to Rust/C test suites
7. Tighten test tolerances to detect drift

### Nice to Have
8. Rename `consensus.py::round()` to `consensus_round()` to avoid builtin shadowing
9. Document antipodal degeneracy in circular mean
10. Implement pebble game algorithm for exact Laman check at any scale
