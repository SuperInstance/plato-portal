# constraint-substrate — The Irreducible Core

**Date:** 2026-05-22  
**Status:** Design Document  
**Premise:** Five primitives. Zero dependencies. Every language. The math that music, physics, distributed systems, robotics, and signal processing all share.

---

## Table of Contents

1. [Philosophy](#1-philosophy)
2. [The Five Primitives](#2-the-five-primitives)
3. [API Contract — Identical in All Languages](#3-api-contract--identical-in-all-languages)
4. [Mathematical Specification](#4-mathematical-specification)
5. [Cross-Language Test Vectors](#5-cross-language-test-vectors)
6. [Build System & Directory Layout](#6-build-system--directory-layout)
7. [Implementation Notes Per Language](#7-implementation-notes-per-language)
8. [Relationship to the Music Ecosystem](#8-relationship-to-the-music-ecosystem)
9. [Implementation Priority & Phases](#9-implementation-priority--phases)

---

## 1. Philosophy

`constraint-substrate` is **not** a music library. It is not a DSP library. It is not tied to any domain.

It is the mathematical substrate shared by:
- **Music theory** — scales are lattice quantizations, envelopes are funnels, rhythm is consensus
- **Crystallography** — lattice structures, covering radii, Weyl groups
- **Distributed systems** — consensus protocols, deadband convergence, fault detection
- **Robotics** — rigidity theory, formation control, phase synchronization
- **Signal processing** — quantization noise bounds, phase-locked loops, holonomy verification
- **Quantum computing** — lattice error correction codes, topological invariants

The library provides five functions so fundamental that rederiving them would take any mathematician an afternoon and any engineer a week. They are:

1. **snap** — Quantize to a lattice
2. **funnel** — Converge through a deadband
3. **holonomy** — Accumulate phase around a loop
4. **rigidity** — Check graph independence
5. **consensus** — Synchronize multiple agents

Everything else — the 85 sound dials, the assembly-first synth, the PLATO architecture — builds on these five. This is the foundation stone.

---

## 2. The Five Primitives

### 2.1 snap — Lattice Quantization

**What:** Map any point in continuous space to the nearest point on a discrete lattice.  
**Why:** Every digital system quantizes. The A₂ (Eisenstein) lattice is the densest 2D packing, giving the tightest error bound by construction.  
**Guarantee:** Maximum quantization error ≤ ρ = 1/√3 ≈ 0.577 (covering radius).  
**Generalization:** Configurable cyclic group Z/nZ for arbitrary lattice geometries (12-TET, pentatonic, continuous).

### 2.2 funnel — Deadband Convergence

**What:** Exponentially narrow a tolerance band from permissive to precise.  
**Why:** Every adaptive system needs to converge — oscillators lock, envelopes decay, predictions tighten.  
**Guarantee:** ε(t) = ε₀ · e^(−λt) monotonically decreases. Anomaly detection when error exceeds δ.

### 2.3 holonomy — Phase Accumulation

**What:** Compute the winding number / holonomy around a closed cycle.  
**Why:** Every cyclic system needs consistency verification — does the loop close?  
**Guarantee:** Holonomy = 0 ⟺ cycle is consistent. O(log N) fault isolation.

### 2.4 rigidity — Graph Independence

**What:** Check whether a graph of N vertices and E edges is minimally rigid (Laman conditions).  
**Why:** Every multi-agent system needs the minimum communication topology for reliable coordination.  
**Guarantee:** Laman ⟹ exactly 2N−3 edges, every edge load-bearing, ≥2 independent paths between any vertices.

### 2.5 consensus — Multi-Agent Synchronization

**What:** One round of metronome convergence among N agents with coupling strength α.  
**Why:** Every distributed system needs agreement — clock sync, tempo lock, formation keeping.  
**Guarantee:** With optimal α* = 2/(λ₂ + λₙ), convergence is fastest without oscillation.

---

## 3. API Contract — Identical in All Languages

### Type Conventions

All languages use these universal types:
- `f64` — IEEE 754 double-precision float
- `f32` — IEEE 754 single-precision float (batch variants)
- `i32` / `u32` — signed/unsigned 32-bit integer
- `bool` — boolean
- `[]T` — contiguous array of type T (pointer + length)
- `Edge` — pair of `(u32, u32)` vertex indices

### Scalar Functions

```
// snap — quantize a value to the nearest lattice point
//
// Parameters:
//   value        — the input value to quantize
//   lattice_group — cyclic group order (0 = continuous, 12 = chromatic, etc.)
//
// Returns: (snapped_value, error)
//   snapped_value — the quantized output
//   error         — |value - snapped_value|, guaranteed ≤ covering_radius(lattice_group)
//
snap(value: f64, lattice_group: u32) -> (f64, f64)
```

```
// funnel — one step of deadband convergence
//
// Parameters:
//   current — current value
//   target  — target value
//   epsilon — current deadband width
//   decay   — exponential decay rate λ
//
// Returns: (new_value, new_epsilon)
//   new_value   — value moved toward target by ε-proportional step
//   new_epsilon — epsilon decayed: epsilon * exp(-decay)
//
// If |current - target| > epsilon: anomaly detected, epsilon resets to initial.
funnel(current: f64, target: f64, epsilon: f64, decay: f64) -> (f64, f64)
```

```
// holonomy — compute winding number around a cycle
//
// Parameters:
//   values  — array of accumulated phase values around the cycle
//   modulus — the modulus (e.g., 2π for angles, 48 for direction indices)
//
// Returns: winding number (holonomy). 0 means consistent cycle.
//
holonomy(values: []f64, modulus: f64) -> f64
```

```
// is_rigid — check Laman rigidity conditions
//
// Parameters:
//   n_vertices — number of vertices in the graph
//   edges      — array of Edge (u32, u32) pairs
//
// Returns: true if graph is Laman rigid (2n-3 edges, all subsets ≤ 2k-3)
//
is_rigid(n_vertices: u32, edges: []Edge) -> bool
```

```
// consensus — one round of metronome synchronization
//
// Parameters:
//   values  — current values of all N agents
//   epsilon — convergence threshold
//
// Returns: (new_values, converged)
//   new_values — values after one consensus round (circular mean correction)
//   converged  — true if max pairwise difference ≤ epsilon
//
consensus(values: []f64, epsilon: f64) -> ([]f64, bool)
```

### Batch Functions

```
// snap_batch — vectorized snap for N values
snap_batch(values: []f64, lattice_group: u32) -> ([]f64, []f64)
// Returns: (snapped_values[], errors[])

// funnel_batch — N agents converging independently
funnel_batch(currents: []f64, targets: []f64, epsilons: []f64, decay: f64) -> ([]f64, []f64)
// Returns: (new_values[], new_epsilons[])

// holonomy_batch — compute holonomy for M cycles
holonomy_batch(cycles: [][]f64, modulus: f64) -> []f64
// Returns: winding_numbers[]
```

### Utility Functions

```
// covering_radius — maximum snap error for a given lattice group
covering_radius(lattice_group: u32) -> f64

// optimal_coupling — compute α* = 2/(λ₂ + λₙ) for a graph
optimal_coupling(n_vertices: u32, edges: []Edge) -> f64

// henneberg_construct — build a Laman graph with N vertices
 henneberg_construct(n: u32, seed: u32) -> []Edge
```

---

## 4. Mathematical Specification

### 4.1 snap — Lattice Quantization

**Domain:** ℝ × ℕ → ℝ × ℝ  
**Lattice:** The A₂ (Eisenstein) lattice generated by {1, ω} where ω = e^{2πi/3} = −½ + i√3/2.

**Algorithm:**

Given input (x, y) and group order n:

1. If `n = 0`: return (x, 0.0) — no quantization, continuous mode.
2. Compute step size: `step = 1.0 / n`.
3. Quantize: `snapped = round(value / step) * step`.
4. Compute error: `err = |value - snapped|`.
5. Return `(snapped, err)`.

**A₂ mode (n = 12, the default):**

Given input (x, y) on the complex plane:

1. Convert Cartesian → lattice coordinates:
   - b_f = y / (√3/2) = 2y/√3
   - a_f = x + b_f/2
2. Round: a = ⌊a_f + ½⌋, b = ⌊b_f + ½⌋
3. Check 7 candidates: (a,b) and its 6 neighbors in the A₂ lattice
4. Select the candidate minimizing Euclidean distance
5. Return (snapped point, distance)

**Error bound:** For A₂, max error ≤ ρ = 1/√3 ≈ 0.57735.  
**Instruction count:** ~30 FP operations, ~10ns scalar on modern CPU.

### 4.2 funnel — Deadband Convergence

**Domain:** ℝ × ℝ × ℝ × ℝ → ℝ × ℝ  
**Law:** ε(t) = ε₀ · e^(−λt)

**Algorithm:**

```
funnel(current, target, epsilon, decay):
    diff = |current - target|
    new_epsilon = epsilon * exp(-decay)
    
    if diff > delta:        # anomaly (delta = initial epsilon_0)
        new_epsilon = epsilon_0
        return (current, new_epsilon)  # no movement, widen funnel
    else:
        # Move proportionally toward target within deadband
        step = min(1.0, epsilon / max(diff, 1e-15))
        new_value = current + (target - current) * step
        return (new_value, new_epsilon)
```

**Properties:**
- Monotonic: epsilon only decreases (or resets on anomaly)
- Bounded: |new_value - target| ≤ new_epsilon after convergence
- Smooth: exponential decay, no discontinuities

### 4.3 holonomy — Phase Accumulation

**Domain:** ℝᴺ × ℝ → ℝ  
**Law:** H = (Σᵢ vᵢ) mod M

**Algorithm:**

```
holonomy(values, modulus):
    sum = 0
    for v in values:
        sum = sum + v
    return sum mod modulus
```

**Properties:**
- H = 0 ⟺ the cycle closes exactly (consistent)
- H ≠ 0 ⟺ the cycle has a gap (faulty)
- Fault isolation in O(log N) via bisection

**Topological interpretation:** The holonomy is the winding number — how many times the accumulated phase wraps around the modulus. This is a topological invariant of the cycle.

### 4.4 rigidity — Laman Graph Check

**Domain:** ℕ × Edgeᴹ → Boolean  
**Law:** G is Laman rigid ⟺ |E| = 2|V| − 3 ∧ ∀S ⊂ V : |E(S)| ≤ 2|S| − 3

**Algorithm (small graphs, n ≤ 15):** Brute-force subset enumeration.  
**Algorithm (large graphs, n > 15):** Pebble game (Jacobs & Hendrickson, 1997).

**Complexity:**
- Edge count check: O(1)
- Subset check: O(2ⁿ · n) for brute force, O(n · m) for pebble game
- Algebraic connectivity: O(k · n²) via power iteration (k iterations)

**Construction:** Henneberg type-I:
1. Start with K₂ (2 vertices, 1 edge)
2. For each new vertex v, connect to 2 existing vertices
3. Result: exactly 2n − 3 edges, guaranteed Laman

### 4.5 consensus — Multi-Agent Synchronization

**Domain:** ℝᴺ × ℝ → ℝᴺ × Boolean  
**Law:** Kuramoto consensus with optimal coupling

**Algorithm:**

```
consensus(values, epsilon):
    n = length(values)
    mean = circular_mean(values)
    
    new_values = []
    for i in 0..n:
        diff = mean - values[i]
        # Normalize to [-modulus/2, modulus/2]
        while diff > π: diff -= 2π
        while diff < -π: diff += 2π
        new_values[i] = values[i] + alpha * diff
    
    # Check convergence
    max_diff = max pairwise difference in new_values
    converged = (max_diff <= epsilon)
    
    return (new_values, converged)
```

**Optimal coupling:** α* = 2/(λ₂ + λₙ) where λ₂ is the algebraic connectivity (2nd smallest Laplacian eigenvalue) and λₙ is the largest.

**Convergence rate:** Determined by λ₂. For Laman graphs: λ₂ ≈ O(1/n).

---

## 5. Cross-Language Test Vectors

The file `tests/vectors.json` contains known-input/known-output pairs. Every implementation must produce bit-identical results within floating-point tolerance (ε_fp = 10⁻⁶ for f64, 10⁻³ for f32).

### 5.1 snap vectors

```json
{
  "snap": [
    {
      "id": "snap_001",
      "description": "Origin snaps to origin",
      "input": {"value": 0.0, "lattice_group": 12},
      "expected": {"snapped": 0.0, "error": 0.0},
      "tolerance": 1e-15
    },
    {
      "id": "snap_002",
      "description": "0.5 snaps to nearest 1/12 = 0.0833",
      "input": {"value": 0.5, "lattice_group": 12},
      "expected": {"snapped": 0.5, "error": 0.0},
      "tolerance": 1e-10
    },
    {
      "id": "snap_003",
      "description": "0.6 snaps to 0.5833 (7/12)",
      "input": {"value": 0.6, "lattice_group": 12},
      "expected": {"snapped": 0.5833333333333334, "error": 0.016666666666666606},
      "tolerance": 1e-10
    },
    {
      "id": "snap_004",
      "description": "1.0 snaps to 1.0",
      "input": {"value": 1.0, "lattice_group": 12},
      "expected": {"snapped": 1.0, "error": 0.0},
      "tolerance": 1e-15
    },
    {
      "id": "snap_005",
      "description": "Continuous mode (group=0), identity",
      "input": {"value": 3.14159, "lattice_group": 0},
      "expected": {"snapped": 3.14159, "error": 0.0},
      "tolerance": 1e-15
    },
    {
      "id": "snap_006",
      "description": "Pentatonic (group=5)",
      "input": {"value": 0.5, "lattice_group": 5},
      "expected": {"snapped": 0.4, "error": 0.1},
      "tolerance": 1e-10
    },
    {
      "id": "snap_007",
      "description": "Negative value",
      "input": {"value": -0.3, "lattice_group": 12},
      "expected": {"snapped": -0.3333333333333333, "error": 0.03333333333333333},
      "tolerance": 1e-10
    },
    {
      "id": "snap_008",
      "description": "Large value",
      "input": {"value": 100.7, "lattice_group": 12},
      "expected": {"snapped": 100.66666666666667, "error": 0.03333333333333333},
      "tolerance": 1e-8
    },
    {
      "id": "snap_009",
      "description": "Diatonic (group=7)",
      "input": {"value": 0.5, "lattice_group": 7},
      "expected": {"snapped": 0.42857142857142855, "error": 0.07142857142857144},
      "tolerance": 1e-10
    },
    {
      "id": "snap_010",
      "description": "Group=1 — everything snaps to integer",
      "input": {"value": 0.7, "lattice_group": 1},
      "expected": {"snapped": 1.0, "error": 0.30000000000000004},
      "tolerance": 1e-10
    }
  ]
}
```

### 5.2 funnel vectors

```json
{
  "funnel": [
    {
      "id": "funnel_001",
      "description": "Already at target",
      "input": {"current": 1.0, "target": 1.0, "epsilon": 0.1, "decay": 0.05},
      "expected": {"new_value": 1.0, "new_epsilon": 0.09512294249971396},
      "tolerance": 1e-10
    },
    {
      "id": "funnel_002",
      "description": "Small step toward target",
      "input": {"current": 0.5, "target": 1.0, "epsilon": 0.1, "decay": 0.05},
      "expected": {"new_value": 0.6, "new_epsilon": 0.09512294249971396},
      "tolerance": 1e-10
    },
    {
      "id": "funnel_003",
      "description": "Zero decay — epsilon stays same",
      "input": {"current": 0.5, "target": 1.0, "epsilon": 0.1, "decay": 0.0},
      "expected": {"new_value": 0.6, "new_epsilon": 0.1},
      "tolerance": 1e-10
    },
    {
      "id": "funnel_004",
      "description": "Large decay — epsilon shrinks fast",
      "input": {"current": 1.0, "target": 1.0, "epsilon": 1.0, "decay": 1.0},
      "expected": {"new_value": 1.0, "new_epsilon": 0.36787944117144233},
      "tolerance": 1e-10
    },
    {
      "id": "funnel_005",
      "description": "Anomaly — error exceeds delta",
      "input": {"current": 0.0, "target": 10.0, "epsilon": 0.1, "decay": 0.1},
      "expected": {"new_value": 0.01, "new_epsilon": 0.09048374180359596},
      "tolerance": 1e-10
    },
    {
      "id": "funnel_006",
      "description": "Tiny epsilon, near target",
      "input": {"current": 0.999, "target": 1.0, "epsilon": 0.001, "decay": 0.0},
      "expected": {"new_value": 1.0, "new_epsilon": 0.001},
      "tolerance": 1e-10
    }
  ]
}
```

### 5.3 holonomy vectors

```json
{
  "holonomy": [
    {
      "id": "holonomy_001",
      "description": "Empty cycle — trivially consistent",
      "input": {"values": [], "modulus": 48.0},
      "expected": 0.0,
      "tolerance": 1e-15
    },
    {
      "id": "holonomy_002",
      "description": "Balanced cycle — zero holonomy",
      "input": {"values": [12.0, 12.0, 12.0, 12.0], "modulus": 48.0},
      "expected": 0.0,
      "tolerance": 1e-15
    },
    {
      "id": "holonomy_003",
      "description": "Unbalanced cycle — nonzero holonomy",
      "input": {"values": [10.0, 10.0, 10.0, 10.0], "modulus": 48.0},
      "expected": 40.0,
      "tolerance": 1e-15
    },
    {
      "id": "holonomy_004",
      "description": "Full wrap — 48 total, mod 48 = 0",
      "input": {"values": [16.0, 16.0, 16.0], "modulus": 48.0},
      "expected": 0.0,
      "tolerance": 1e-15
    },
    {
      "id": "holonomy_005",
      "description": "Angular holonomy — 2π total",
      "input": {"values": [1.5707963267948966, 1.5707963267948966, 1.5707963267948966, 1.5707963267948966], "modulus": 6.283185307179586},
      "expected": 0.0,
      "tolerance": 1e-10
    },
    {
      "id": "holonomy_006",
      "description": "Single value",
      "input": {"values": [25.0], "modulus": 48.0},
      "expected": 25.0,
      "tolerance": 1e-15
    }
  ]
}
```

### 5.4 rigidity vectors

```json
{
  "rigidity": [
    {
      "id": "rigid_001",
      "description": "K2 — minimal rigid graph",
      "input": {"n_vertices": 2, "edges": [[0, 1]]},
      "expected": true
    },
    {
      "id": "rigid_002",
      "description": "Triangle — 3 vertices, 3 edges (2*3-3=3)",
      "input": {"n_vertices": 3, "edges": [[0, 1], [1, 2], [2, 0]]},
      "expected": true
    },
    {
      "id": "rigid_003",
      "description": "Too few edges — not rigid",
      "input": {"n_vertices": 3, "edges": [[0, 1], [1, 2]]},
      "expected": false
    },
    {
      "id": "rigid_004",
      "description": "Too many edges",
      "input": {"n_vertices": 3, "edges": [[0, 1], [1, 2], [2, 0], [0, 1]]},
      "expected": false
    },
    {
      "id": "rigid_005",
      "description": "4 vertices, 5 edges (2*4-3=5), Henneberg construction",
      "input": {"n_vertices": 4, "edges": [[0, 1], [2, 0], [2, 1], [3, 0], [3, 1]]},
      "expected": true
    },
    {
      "id": "rigid_006",
      "description": "Single vertex — trivially rigid (0 edges)",
      "input": {"n_vertices": 1, "edges": []},
      "expected": true
    },
    {
      "id": "rigid_007",
      "description": "5 vertices, 7 edges (2*5-3=7), Laman",
      "input": {"n_vertices": 5, "edges": [[0,1],[1,2],[2,0],[2,3],[3,0],[3,4],[4,1]]},
      "expected": true
    },
    {
      "id": "rigid_008",
      "description": "Disconnected graph",
      "input": {"n_vertices": 4, "edges": [[0, 1], [2, 3]]},
      "expected": false
    }
  ]
}
```

### 5.5 consensus vectors

```json
{
  "consensus": [
    {
      "id": "consensus_001",
      "description": "Already converged — all same",
      "input": {"values": [1.0, 1.0, 1.0], "epsilon": 0.1},
      "expected": {"new_values": [1.0, 1.0, 1.0], "converged": true},
      "tolerance": 1e-10
    },
    {
      "id": "consensus_002",
      "description": "Small spread — converges in one step",
      "input": {"values": [0.1, 0.2, 0.3], "epsilon": 0.5},
      "expected": {"new_values": [0.2, 0.2, 0.2], "converged": true},
      "tolerance": 1e-10
    },
    {
      "id": "consensus_003",
      "description": "Large spread — not converged yet",
      "input": {"values": [0.0, 1.0, 2.0], "epsilon": 0.1},
      "expected": {"new_values": [0.6666666666666666, 1.0, 1.3333333333333333], "converged": false},
      "tolerance": 1e-8
    },
    {
      "id": "consensus_004",
      "description": "Single agent — trivially converged",
      "input": {"values": [3.14], "epsilon": 0.01},
      "expected": {"new_values": [3.14], "converged": true},
      "tolerance": 1e-15
    },
    {
      "id": "consensus_005",
      "description": "Two agents — symmetric convergence",
      "input": {"values": [0.0, 1.0], "epsilon": 0.5},
      "expected": {"new_values": [0.5, 0.5], "converged": true},
      "tolerance": 1e-10
    },
    {
      "id": "consensus_006",
      "description": "Negative values",
      "input": {"values": [-1.0, 0.0, 1.0], "epsilon": 0.5},
      "expected": {"new_values": [0.0, 0.0, 0.0], "converged": true},
      "tolerance": 1e-10
    }
  ]
}
```

---

## 6. Build System & Directory Layout

```
constraint-substrate/
│
├── python/                      # Phase 1 — Reference implementation
│   ├── pyproject.toml           # pip install constraint-substrate
│   ├── src/
│   │   └── constraint_substrate/
│   │       ├── __init__.py
│   │       ├── snap.py          # snap, snap_batch, covering_radius
│   │       ├── funnel.py        # funnel, funnel_batch
│   │       ├── holonomy.py      # holonomy, holonomy_batch
│   │       ├── rigidity.py      # is_rigid, henneberg_construct, optimal_coupling
│   │       └── consensus.py     # consensus
│   └── tests/
│       ├── test_vectors.py      # Runs against tests/vectors.json
│       └── test_properties.py   # Property-based tests (hypothesis)
│
├── rust/                        # Phase 1 — Performance reference
│   ├── Cargo.toml               # cargo add constraint-substrate
│   ├── src/
│   │   ├── lib.rs               # Re-exports
│   │   ├── snap.rs              # no_std compatible
│   │   ├── funnel.rs
│   │   ├── holonomy.rs
│   │   ├── rigidity.rs
│   │   └── consensus.rs
│   ├── benches/                 # criterion benchmarks
│   └── tests/
│       └── test_vectors.rs
│
├── c/                           # Phase 1 — Portability reference
│   ├── Makefile
│   ├── include/
│   │   └── constraint_substrate.h
│   ├── src/
│   │   ├── snap.c
│   │   ├── funnel.c
│   │   ├── holonomy.c
│   │   ├── rigidity.c
│   │   └── consensus.c
│   └── tests/
│       └── test_vectors.c
│
├── cpp/                         # Phase 2 — Header-only
│   ├── include/
│   │   └── constraint_substrate/
│   │       ├── snap.hpp
│   │       ├── funnel.hpp
│   │       ├── holonomy.hpp
│   │       ├── rigidity.hpp
│   │       └── consensus.hpp
│   └── tests/
│
├── cuda/                        # Phase 2 — GPU kernels
│   ├── include/
│   │   └── constraint_substrate.cuh
│   ├── src/
│   │   ├── snap.cu              # batch kernels
│   │   ├── funnel.cu
│   │   └── consensus.cu
│   └── tests/
│
├── zig/                         # Phase 2 — Modern systems
│   ├── build.zig
│   ├── src/
│   │   ├── snap.zig             # comptime generics for group order
│   │   ├── funnel.zig
│   │   ├── holonomy.zig
│   │   ├── rigidity.zig
│   │   └── consensus.zig
│   └── tests/
│
├── julia/                       # Phase 3 — Scientific
│   ├── Project.toml
│   ├── src/
│   │   ├── ConstraintSubstrate.jl
│   │   ├── snap.jl
│   │   ├── funnel.jl
│   │   ├── holonomy.jl
│   │   ├── rigidity.jl
│   │   └── consensus.jl
│   └── test/
│
├── fortran/                     # Phase 3 — HPC
│   ├── fpm.toml
│   ├── src/
│   │   ├── constraint_substrate.f90
│   │   ├── snap.f90
│   │   ├── funnel.f90
│   │   ├── holonomy.f90
│   │   ├── rigidity.f90
│   │   └── consensus.f90
│   └── test/
│
├── chapel/                      # Phase 3 — Parallel
│   ├── src/
│   │   ├── ConstraintSubstrate.chpl
│   │   ├── Snap.chpl            # locale-aware batch
│   │   ├── Funnel.chpl
│   │   ├── Holonomy.chpl
│   │   ├── Rigidity.chpl
│   │   └── Consensus.chpl
│   └── test/
│
├── mojo/                        # Phase 3 — AI/ML
│   ├── src/
│   │   ├── constraint_substrate.mojo
│   │   ├── snap.mojo            # SIMD-native, Python-compatible
│   │   ├── funnel.mojo
│   │   ├── holonomy.mojo
│   │   ├── rigidity.mojo
│   │   └── consensus.mojo
│   └── test/
│
├── go/                          # Phase 4 — Cloud
│   ├── go.mod
│   ├── snap.go
│   ├── funnel.go
│   ├── holonomy.go
│   ├── rigidity.go
│   ├── consensus.go
│   └── snap_test.go
│
├── ts/                          # Phase 4 — Web
│   ├── package.json
│   ├── src/
│   │   ├── index.ts
│   │   ├── snap.ts
│   │   ├── funnel.ts
│   │   ├── holonomy.ts
│   │   ├── rigidity.ts
│   │   └── consensus.ts
│   └── tests/
│
├── wasm/                        # Phase 4 — Universal
│   ├── Cargo.toml               # wasm-pack, compiled from Rust
│   ├── src/
│   │   └── lib.rs
│   └── pkg/                     # Generated .wasm + JS bindings
│
├── j/                           # Phase 5 — Array
│   ├── constraint_substrate.ijs
│   └── test.ijs
│
├── apl/                         # Phase 5 — Array
│   ├── CONSTRAINT_SUBSTRATE.apl
│   └── TEST.apl
│
├── tests/                       # Shared test infrastructure
│   ├── vectors.json             # The canonical test vectors (above)
│   ├── generate_vectors.py      # Generate vectors from reference impl
│   └── compare.py               # Compare two implementations' output
│
├── benches/                     # Cross-language benchmarks
│   ├── BENCHMARK.md             # Results table
│   └── bench.py                 # Runner
│
├── docs/
│   ├── README.md                # Overview, quick start
│   ├── API.md                   # Full API reference (this section 3)
│   ├── MATH.md                  # Mathematical foundations (this section 4)
│   └── LANGUAGES.md             # Per-language notes (this section 7)
│
├── .github/
│   └── workflows/
│       ├── ci.yml               # Test all languages
│       └── bench.yml            # Run benchmarks
│
├── LICENSE                      # MIT or Apache 2.0 dual
└── README.md
```

---

## 7. Implementation Notes Per Language

### Python (Reference)

**Style:** Pure Python with optional numpy for batch operations.  
**Idioms:** Type hints, docstrings, `@dataclass`, `@overload` for scalar vs batch.  
**Tricky parts:**
- `snap` with A₂ mode needs the 7-candidate search (round then check neighbors)
- `is_rigid` subset enumeration is O(2ⁿ) — use pebble game for n > 15
- `consensus` must handle circular mean correctly (atan2 of sin/cos sums)

```python
def snap(value: float, lattice_group: int = 12) -> tuple[float, float]:
    if lattice_group == 0:
        return (value, 0.0)
    step = 1.0 / lattice_group
    snapped = round(value / step) * step
    err = abs(value - snapped)
    return (snapped, err)
```

### Rust (Performance Reference)

**Style:** `no_std` + `alloc`, generic over `f32`/`f64`.  
**Idioms:** Traits (`Snap`, `Funnel`, etc.), `#[inline(always)]`, `Simd<f64, LANES>`.  
**Tricky parts:**
- `no_std` means no `exp()` in `core` — use `libm` or inline approximation
- `is_rigid` pebble game needs `alloc::vec::Vec`
- WASM target: compile from this crate with `wasm32-unknown-unknown`

```rust
pub fn snap(value: f64, lattice_group: u32) -> (f64, f64) {
    if lattice_group == 0 {
        return (value, 0.0);
    }
    let step = 1.0 / (lattice_group as f64);
    let snapped = (value / step).round() * step;
    let err = (value - snapped).abs();
    (snapped, err)
}
```

### C (Portability Reference)

**Style:** C99, no libc dependencies for core math (use custom `cs_exp`, `cs_sqrt`).  
**Idioms:** Header-only option via `#define CS_HEADER_ONLY`, opaque structs, error codes.  
**Tricky parts:**
- Custom transcendental functions (`cs_exp`, `cs_log`, `cs_sqrt`) for no-libc builds
- Edge array passed as `const uint32_t edges[][2]` with length
- Thread safety: all functions pure, no global state

```c
typedef struct { double snapped; double error; } CsSnapResult;
typedef struct { uint32_t u; uint32_t v; } CsEdge;

CsSnapResult cs_snap(double value, uint32_t lattice_group);
void cs_snap_batch(const double* values, uint32_t n, uint32_t lattice_group,
                   double* snapped_out, double* errors_out);
```

### C++ (Header-Only)

**Style:** C++17, header-only, `<algorithm>` + `<cmath>`.  
**Idioms:** Templates, `constexpr` where possible, `std::span` for arrays, concepts for type constraints.  
**Tricky parts:**
- `constexpr snap` is straightforward; `constexpr funnel` needs `constexpr exp`
- Batch variants use `std::valarray` or raw pointers for game-engine compatibility

```cpp
template<typename T = double>
struct SnapResult { T snapped, error; };

template<typename T = double>
constexpr SnapResult<T> snap(T value, uint32_t lattice_group = 12) noexcept;
```

### CUDA (GPU Kernels)

**Style:** `__global__` kernels, `__device__` helpers, coalesced memory access.  
**Idioms:** Block/grid sizing, shared memory for consensus reduction, warp-level primitives.  
**Tricky parts:**
- `snap_batch` is embarrassingly parallel — one thread per value
- `consensus` needs all-reduce within a block — use warp shuffle or shared memory
- `is_rigid` is inherently serial for subset check — offload only for massive batch

```cuda
__global__ void cs_snap_batch_kernel(
    const double* __restrict__ values,
    uint32_t n, uint32_t lattice_group,
    double* __restrict__ snapped_out,
    double* __restrict__ errors_out
);
```

### Zig (Modern Systems)

**Style:** Comptime generics, `pub fn`, explicit allocator passing.  
**Idioms:** `comptime lattice_group: u32` for compile-time specialization. Vector types `@Vector(N, f64)`.  
**Tricky parts:**
- `comptime` lattice_group means `snap` is monomorphized per group — zero-cost abstraction
- Allocator required for `is_rigid` (pebble game) and `consensus` (array allocation)

```zig
pub fn snap(comptime value: f64, comptime lattice_group: u32) struct { f64, f64 } {
    if (lattice_group == 0) return .{ value, 0.0 };
    const step = 1.0 / @as(f64, @floatFromInt(lattice_group));
    const snapped = @round(value / step) * step;
    return .{ snapped, @abs(value - snapped) };
}
```

### Julia (Scientific)

**Style:** Type-stable, multiple dispatch, `@inline`, SIMD via `LoopVectorization.jl`.  
**Idioms:** `snap(::Float64, ::Int) = ...` dispatches on types. `@simd` for batch.  
**Tricky parts:**
- Multiple dispatch makes the API natural: `snap(0.5, 12)` just works
- `is_rigid` can use `LightGraphs.jl` internally (optional dep)
- Array operations are already SIMD-friendly in Julia

```julia
snap(value::AbstractFloat, lattice_group::Integer=12) = 
    lattice_group == 0 ? (value, zero(value)) : 
    let s = 1.0/lattice_group; 
        n = round(value/s)*s; 
        (n, abs(value-n)) 
    end
```

### Fortran (HPC)

**Style:** F2008, modules, assumed-shape arrays, pure functions.  
**Idioms:** `pure function`, `intent(in)`, array syntax `snapped = nint(values/step)*step`.  
**Tricky parts:**
- Module system for encapsulation
- Array ops are Fortran's superpower — batch variants are trivially one-liners
- `is_rigid` needs careful memory management for the pebble game

```fortran
module constraint_substrate
  implicit none
  private
  public :: cs_snap, cs_funnel, cs_holonomy, cs_is_rigid, cs_consensus
contains
  pure function cs_snap(value, lattice_group) result(r)
    real(8), intent(in) :: value
    integer, intent(in) :: lattice_group
    real(8) :: r(2)  ! (snapped, error)
    real(8) :: step, snapped
    if (lattice_group == 0) then
      r = [value, 0.0d0]
    else
      step = 1.0d0 / lattice_group
      snapped = nint(value / step) * step
      r = [snapped, abs(value - snapped)]
    end if
  end function
end module
```

### Chapel (Parallel)

**Style:** Locale-aware parallel, `coforall`, `ReduceScanIntent`.  
**Idioms:** Domain maps for distributed arrays, `forall` for parallel iteration.  
**Tricky parts:**
- `snap_batch` parallelizes trivially with `forall`
- `consensus` needs a global reduction across locales — use `reduce` intent
- `is_rigid` pebble game is serial per graph, but can check many graphs in parallel

```chapel
proc snap(value: real, lattice_group: int = 12): (real, real) {
  if lattice_group == 0 then return (value, 0.0);
  const step = 1.0 / lattice_group;
  const snapped = round(value / step) * step;
  return (snapped, abs(value - snapped));
}

proc snap_batch(values: [] real, lattice_group: int = 12): ([] real, [] real) {
  const n = values.domain.size;
  var snapped: [0..#n] real;
  var errors: [0..#n] real;
  forall i in 0..#n {
    (snapped[i], errors[i]) = snap(values[i], lattice_group);
  }
  return (snapped, errors);
}
```

### Mojo (AI/ML)

**Style:** Python-compatible syntax, SIMD-native, `@parameter` for compile-time.  
**Idioms:** `SIMD[f64, N]` for vectorized ops, `@parameter` for compile-time group order.  
**Tricky parts:**
- Very young language — API may need adjustment as Mojo evolves
- Python compat means the interface looks identical to the Python version
- SIMD vectorization is built-in and explicit

```mojo
fn snap(value: Float64, lattice_group: Int = 12) -> (Float64, Float64):
    if lattice_group == 0:
        return (value, 0.0)
    let step = 1.0 / Float64(lattice_group)
    let snapped = round(value / step) * step
    return (snapped, abs(value - snapped))
```

### Go (Cloud)

**Style:** Goroutine-safe, `package constraintsubstrate`, interface-based generics.  
**Idioms:** `func Snap(value float64, latticeGroup uint32) (float64, float64)`.  
**Tricky parts:**
- No generics for numeric types pre-1.18; post-1.18 use type constraints
- `is_rigid` needs slice-based edge representation
- Batch operations: use goroutines + channels for parallelism, or just loops for simplicity

```go
func Snap(value float64, latticeGroup uint32) (float64, float64) {
    if latticeGroup == 0 {
        return value, 0.0
    }
    step := 1.0 / float64(latticeGroup)
    snapped := math.Round(value/step) * step
    err := math.Abs(value - snapped)
    return snapped, err
}
```

### TypeScript/JavaScript (Web)

**Style:** ES2020, typed, tree-shakeable.  
**Idioms:** `export function snap(value: number, latticeGroup: number = 12): [number, number]`.  
**Tricky parts:**
- `Math.round` in JS rounds half-to-even in some engines — use custom round-half-up
- `is_rigid` subset check needs careful typing for edge arrays
- SIMD via `Float64Array` + manual loop unrolling for batch

```typescript
export function snap(value: number, latticeGroup: number = 12): [number, number] {
  if (latticeGroup === 0) return [value, 0.0];
  const step = 1.0 / latticeGroup;
  const snapped = Math.round(value / step) * step;
  const err = Math.abs(value - snapped);
  return [snapped, err];
}
```

### WebAssembly (Universal)

**Style:** Compiled from Rust via `wasm-pack`. Linear memory for arrays.  
**Idioms:** Export functions via `#[wasm_bindgen]`. Memory management via `wasm_bindgen` allocator.  
**Tricky parts:**
- Array passing: write to WASM linear memory, return pointers
- Single-threaded (for now) — batch operations are sequential
- `is_rigid` is fine; `consensus` needs careful memory layout

### J (Array Programming)

**Style:** Tacit, rank-polymorphic, every operation is array-native.  
**Idioms:** `snap =: 3 : 0` or tacit: `(] -~ ] * [: -.@零 [: <. [: %&1&12)` etc.  
**Tricky parts:**
- J's power is that batch is the default — no separate batch function needed
- `snap"0` applies element-wise automatically
- `is_rigid` needs careful matrix construction

```j
NB. snap: quantize to lattice
snap =: dyad define
  'value group' =. y
  if. group = 0 do. value , 0 return. end.
  step =. % group
  snapped =. [: <. step %~ ]
  snapped , |@(-~ value)
)
```

### APL (Array Programming)

**Style:** Glyphic, concourse, everything is an array.  
**Idioms:** `⌊` for floor, `○` for pi, `|` for absolute value.  
**Tricky parts:**
- APL's entire philosophy is array-first — batch is free
- `is_rigid` translates to matrix rank checks
- Debugging glyphs is an art form

```apl
∇ R ← V SNAP G
  →(G=0)/ZERO
  S ← ÷G
  SN ← (⌊(V÷S)+0.5)×S
  R ← SN, (|V-SN)
  →0
ZERO:
  R ← V, 0
∇
```

---

## 8. Relationship to the Music Ecosystem

### Independent But Foundational

`constraint-substrate` is mathematically independent of music. It knows nothing about:
- MIDI, notes, scales, chords
- Audio sample rates, buffers, DSP
- Instruments, performers, scores

It IS the math that music shares with everything else:

| Music Concept | Substrate Primitive | What Music Adds |
|---|---|---|
| Scale quantization | `snap` | Musical meaning of lattice points (note names) |
| ADSR envelope | `funnel` | Mapping to amplitude, timbre evolution |
| Chord consistency | `holonomy` | Harmonic function, voice leading |
| Voice independence | `rigidity` | Contrapuntal rules, species counterpoint |
| Ensemble timing | `consensus` | Groove, swing, rubato, microtiming |

### The 85 Dials Map to 5 Primitives

The Sound Parameter Atlas's 85 parameters all decompose into compositions of the 5 primitives:

- **Layer 1 (Timbre, 12 params):** `snap` (lattice geometry) + `funnel` (spectral convergence)
- **Layer 2 (Envelope, 10 params):** `funnel` (the entire ADSR lifecycle IS a funnel)
- **Layer 3 (Dynamics, 9 params):** `funnel` (epsilon modulation) + `consensus` (compression)
- **Layer 4 (Pitch, ~10 params):** `snap` (lattice point selection) + `holonomy` (tuning consistency)
- **Layer 5 (Rhythm, ~10 params):** `consensus` (tempo sync) + `snap` (grid quantization)
- **Layer 6 (Harmony, ~10 params):** `holonomy` (voice leading) + `rigidity` (voice independence)
- **Layer 7 (Space, ~10 params):** `funnel` (reverb decay) + `consensus` (spatial coherence)
- **Layer 8 (Personality, ~14 params):** All five, orchestrated together

### The Dependency Direction

```
constraint-substrate          ← You are here (pure math)
    │
    ├── constraint-theory-core ← Python research library (imports substrate)
    │       │
    │       ├── lattice.py     → substrate.snap
    │       ├── temporal.py    → substrate.funnel
    │       ├── holonomy.py    → substrate.holonomy
    │       ├── rigidity.py    → substrate.rigidity
    │       └── metronome.py   → substrate.consensus
    │
    ├── assembly-first-synth   ← Audio engine (links substrate Rust/C)
    │
    ├── PLATO-tiles            ← Constraint verification (uses substrate.holonomy)
    │
    └── DAW plugins            ← JUCE/VST (links substrate C++)
```

The substrate has **no imports from the music ecosystem**. The music ecosystem imports the substrate. This is the foundation stone.

---

## 9. Implementation Priority & Phases

### Phase 1 — Reference Implementations (Week 1-2)
These three define the contract. All other implementations test against them.

| Language | Role | Key Deliverables |
|---|---|---|
| **Python** | Reference, docs, education | Full API, test vectors, property tests |
| **Rust** | Performance, no_std, WASM | Benchmarks, SIMD, FFI to C |
| **C** | Portability, FFI base | C99 header, every language can bind to it |

### Phase 2 — Performance Languages (Week 3-4)
| Language | Role | Key Notes |
|---|---|---|
| **CUDA** | GPU batch | snap_batch and consensus kernels |
| **C++** | Game engines, plugins | Header-only, C++17 |
| **Zig** | Modern systems, cross-compile | Comptime lattice_group specialization |

### Phase 3 — Scientific Languages (Week 5-6)
| Language | Role | Key Notes |
|---|---|---|
| **Julia** | Math research, SIMD | Multiple dispatch makes API natural |
| **Fortran** | Legacy HPC | Array-native, pure functions |
| **Chapel** | Parallel, exascale | Locale-aware distributed consensus |
| **Mojo** | AI/ML acceleration | SIMD-native, Python-compatible |

### Phase 4 — Web & Cloud (Week 7)
| Language | Role | Key Notes |
|---|---|---|
| **TypeScript** | Browser DAWs | Tree-shakeable, typed |
| **WebAssembly** | Universal deploy | Compiled from Rust |
| **Go** | Microservices | Goroutine-safe |

### Phase 5 — Array Languages (Week 8)
| Language | Role | Key Notes |
|---|---|---|
| **J** | Finance, research | Tacit, batch is default |
| **APL** | Research, education | Glyphic, concourse |

### Validation Pipeline

Every implementation must:
1. Pass all test vectors from `tests/vectors.json` within tolerance
2. Pass property-based tests (snap always within covering radius, funnel epsilon monotonically decreases, etc.)
3. Report benchmark numbers for the standard benchmark suite

### Benchmark Suite

Standard benchmarks run on all implementations:

| Benchmark | Description | Metric |
|---|---|---|
| `snap_scalar` | 1M single snap operations | ns/op |
| `snap_batch_1k` | Batch snap 1024 values | ns/op |
| `snap_batch_1m` | Batch snap 1M values | ms |
| `funnel_converge` | Funnel to convergence | iterations |
| `holonomy_100` | Holonomy of 100-element cycle | ns/op |
| `is_rigid_10` | Rigidity check, 10 vertices | μs/op |
| `is_rigid_100` | Rigidity check, 100 vertices | μs/op |
| `consensus_10` | Consensus round, 10 agents | μs/op |
| `consensus_1000` | Consensus round, 1000 agents | μs/op |

---

*This is the foundation stone. Everything else builds on these five functions. Get these right, and every domain — music, physics, robotics, distributed systems — gets the same math for free.*
