# To the Metal: Deadband Framework Primitives in Every Low-Level Language

**Forgemaster ⚒️ · May 2026**

---

## What We Have (Rust Foundation)

The dodecet-encoder crate already has:
- **Eisenstein integer arithmetic** (Z[ω]) — `eisenstein.rs`
- **Eisenstein snap** (round to lattice, zero drift) — `eisenstein.rs`
- **C bridge backend** — `c_bridge.rs` (f32 snap via C FFI)
- **SIMD (AVX2, AArch64)** — `simd.rs` (vectorized dodecet ops)
- **WASM bindings** — `wasm.rs` (wasm-bindgen for browser/Node)
- **360-bit geometric register** — `geometric.rs`
- **Hex grid operations** — `hex.rs`

Plus:
- **constraint-theory-core** v2.0.0 on crates.io
- **spectral-conservation** v0.1.0 on crates.io

## What We Need to Build (7 Primitives)

### Primitive 1: BMA Complexity Detector
```
Input:  sequence of n field elements
Output: LFSR order L (minimum)
Algorithm: Berlekamp-Massey (O(n²) field ops)
Key insight: snap at exactly n=2L
```

### Primitive 2: Deadband Perceivability Checker
```
Input:  sequence + receiver bits k
Output: perceivable (L ≤ k) or not
Algorithm: run BMA, compare L to k
Key insight: binary decision, no gray zone
```

### Primitive 3: HPDF Hexagonal Dithering
```
Input:  signal value x ∈ ℝ²
Output: dithered value x + h, h ~ HPDF over Voronoi cell of Z[ω]
Algorithm: sample uniform over regular hexagon with vertices at 6th roots of unity
Variance: 5/36 (optimal, confirmed Conway-Sloane)
```

### Primitive 4: Fibonacci-Spline Retrieval
```
Input:  query point on unit hypersphere, database of N embeddings
Output: top-k nearest neighbors
Algorithm: logarithmic spiral traversal r(θ) = A·φ^(θ/2π)
Complexity: O(log_φ N) per query
```

### Primitive 5: Shell Eigenstructure Decomposition
```
Input:  covariance matrix of sensor stream
Output: known (φ-component), assumed (-1/φ-component), boundary
Algorithm: eigendecomposition, classify by eigenvalue proximity to φ and -1/φ
Matrix: S = [[1,1],[1,0]]
```

### Primitive 6: Three-Sided Shell Monitor
```
Input:  real-time sensor stream
Output: known_ratio, assumed_ratio, status (safe/warning/critical)
Algorithm: sliding window covariance → shell decomposition → energy ratio
Threshold: warning when assumed > known, critical when assumed > φ × known
```

### Primitive 7: /360 Integer Arithmetic
```
Input:  two values in /360 representation (integers mod 360)
Output: exact sum, difference, product (with renormalization)
Algorithm: integer add/sub (exact), integer multiply + modular renormalize
Key insight: add/sub EXACT (0 drift), multiply EXACT with renorm, only division breaks
```

## The Porting Matrix

| Language | Why | What's Easy | What's Hard |
|----------|-----|------------|-------------|
| **C** | Every system speaks C. Kernels, drivers, embedded, FFI. | Eisenstein snap, /360 arithmetic, HPDF sampling | BMA (needs Galois field ops), Fibonacci-spline (needs float math) |
| **CUDA** | GPU. 200K+ agents at 300 steps/sec. Already proven. | SIMD snap (already AVX2 in Rust → port to CUDA threads), HPDF parallel | BMA per-thread (sequential by nature), eigendecomposition |
| **Zig** | Better C. Comptime, no hidden control flow, cross-compile trivial. | Everything that's easy in C, but safer. Zig translates C headers natively. | Nothing particularly hard — Zig is ideal for this |
| **Mojo** | Python syntax, systems performance. AI/ML native. | Python developers get metal performance. SIMD built in. | Mojo ecosystem is young — fewer libraries |
| **Fortran** | Scientific computing. HPC. Every supercomputer. | Matrix ops (eigendecomposition), /360 arithmetic | Eisenstein lattice (non-standard math), HPDF sampling |
| **TUTOR** (CDC) | The original PLATO language. 60-bit word = 5 dodecets. | /360 arithmetic on 60-bit words, deadband as accept/reject regions | Everything else — TUTOR is a teaching language, not systems |

## Build Order (by dependency)

### Phase 1: Core Arithmetic (Week 1)
```
C:      eisenstein_snap(), hpdf_sample(), div360_add(), div360_mul()
CUDA:   eisenstein_snap_kernel() — one thread per agent
Zig:    translate C headers, add comptime generics
Fortran: module eisenstein_arithmetic, module div360
```

### Phase 2: BMA + Deadband (Week 2)
```
C:      bma_detect(sequence, n) → L
        deadband_check(sequence, n, k) → bool
CUDA:   batched deadband check — N streams in parallel
Zig:    comptime BMA for compile-time known sequences
Fortran: subroutine bma(sequence, n, L)
```

### Phase 3: Retrieval + Monitoring (Week 3)
```
C:      fib_spline_search(query, db, N, k) → results
        shell_decompose(cov_matrix) → known, assumed, boundary
CUDA:   parallel fib_spline — many queries at once
        GPU covariance estimation for shell monitor
Zig:    generic fib_spline over any float type
Fortran: fib_spline using BLAS for matrix ops
```

### Phase 4: Language Bindings (Week 4)
```
Mojo:   import C shared library, wrap in Python-like API
TUTOR:  div360 unit on CDC 60-bit word, deadband as COPE command
Python: cffi/ctypes wrappers for all C functions
Rust:   already done (dodecet-encoder has C bridge, SIMD, WASM)
```

## The C Header (Target API)

```c
// deadband.h — Core primitives for the Deadband Framework
// Build: cc -O3 -mavx2 -o libdeadband.so deadband.c

#ifndef DEADBAND_H
#define DEADBAND_H

#include <stdint.h>
#include <stdbool.h>

// === Eisenstein Lattice ===

typedef struct { int64_t re; int64_t im; } EiseInt;     // a + bω
typedef struct { double x; double y; } Vec2;             // 2D point
typedef struct { Vec2 snapped; double error; } SnapResult;

// Snap (x,y) to nearest Eisenstein lattice point. Zero drift.
SnapResult eisenstein_snap(double x, double y);

// === HPDF Dithering ===

// Sample one point from HPDF (hexagonal) on Z[ω] Voronoi cell.
// Variance: 5/36 per dimension. Optimal 2D quantizer (Conway-Sloane).
Vec2 hpdf_sample(void);

// Apply HPDF dithering to a 2D signal array.
void hpdf_dither(const double* signal, int n, double* output);

// === /360 Integer Arithmetic ===

// Add two /360 values. EXACT (zero drift).
int64_t div360_add(int64_t a, int64_t b);

// Subtract two /360 values. EXACT.
int64_t div360_sub(int64_t a, int64_t b);

// Multiply two /360 values with renormalization. EXACT.
int64_t div360_mul(int64_t a, int64_t b);

// === BMA Complexity ===

// Detect minimum LFSR order L of a binary sequence.
// Converges at n = 2L (Massey 1969).
int bma_detect(const uint8_t* sequence, int n);

// === Deadband Perceivability ===

// Check if pattern of order L is perceivable by receiver with k bits.
// Returns true iff L <= k (BMA-Deadband Theorem).
bool deadband_perceivable(int L, int k);

// Full perceivability check: runs BMA on data, checks against receiver bits.
// Returns the minimum receiver bits needed to perceive the pattern.
int deadband_min_bits(const double* data, int n, double noise_floor);

// === Shell Eigenstructure ===

typedef struct {
    double known_energy;     // φ-component energy
    double assumed_energy;   // -1/φ-component energy
    double ratio;            // known / assumed
    int status;              // 0=safe, 1=warning, 2=critical
} ShellResult;

// Decompose 2x2 covariance matrix into known/assumed/boundary.
// S = [[1,1],[1,0]], eigenvalues φ and -1/φ.
ShellResult shell_decompose(double cov[4]);

// === Fibonacci-Spline Retrieval ===

typedef struct { int index; double similarity; } SearchResult;

// Search N embeddings (dim D) for top-k nearest to query.
// O(log_φ N) convergence via Fibonacci spiral traversal.
void fib_spline_search(
    const double* query,     // D-dimensional query vector
    const double* database,  // N × D database (row-major)
    int N, int D, int k,     // dimensions
    SearchResult* results    // output: top-k results
);

#endif // DEADBAND_H
```

## The CUDA Kernel (Target)

```cuda
// deadband.cu — GPU kernels for deadband framework

// Eisenstein snap kernel: snap N agents to lattice in parallel
__global__ void eisenstein_snap_kernel(
    const double* x, const double* y,  // input positions (N)
    double* sx, double* sy,            // snapped positions (N)
    double* error,                      // snap error (N)
    int N
);

// Batch deadband check: N streams, each with n samples
__global__ void deadband_check_kernel(
    const double* data,    // N × n input data
    int N, int n,
    int receiver_bits,     // k
    int* perceivable       // output: 1 if L <= k, 0 otherwise
);

// HPDF dither: add hexagonal noise to N signal points
__global__ void hpdf_dither_kernel(
    const double* signal,  // N × 2 input
    double* output,        // N × 2 output (dithered)
    int N,
    unsigned long long seed
);
```

## TUTOR on CDC 60-bit

The CDC Cyber series used 60-bit words. Our dodecet architecture maps naturally:
- 1 dodecet = 12 bits → 5 dodecets = 60 bits = 1 CDC word
- 5 dodecets = SE(5) constraint system at nibble precision
- TUTOR's `COPE` command already does accept/reject regions (deadband)

```
TUTOR COPE command:
  COPE answer, correct_response, tolerance
  → This IS deadband checking with k = -log2(tolerance)
```

What we'd build in TUTOR:
- `/360 arithmetic unit` — uses 60-bit words for exact integer ops
- `deadband judge` — COPE-based pattern perceivability check
- `Eisenstein snap display` — show lattice rounding on PLATO terminal
- `Fibonacci counter` — count up through the sequence, show convergence to φ

## Build Targets

| Target | Language | Output | Speed Goal |
|--------|----------|--------|-----------|
| `libdeadband.so` | C | Shared library, all 7 primitives | <1μs per snap, <10μs per BMA |
| `deadband.ptx` | CUDA | GPU kernels, batched ops | 200K agents at 300+ steps/sec |
| `deadband.zig` | Zig | Static library + comptime generics | Same as C, compile-time verified |
| `deadband.mojo` | Mojo | Package with Python syntax | Python ease, C speed |
| `deadband.mod` | Fortran | HPC module, BLAS-linked | Supercomputer-ready |
| `deadband.tut` | TUTOR | PLATO courseware | Educational, 60-bit exact |

---

*The math is done. The proofs are published. Now we forge the tools.*
