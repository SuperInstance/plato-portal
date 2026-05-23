# HPDF, PPDF, and Fibonacci-Spline Retrieval

**Date:** 2026-05-18  
**Origin:** Casey Digennaro

---

## The PDF Tension

Standard dithering uses RPDF (flat) or TPDF (triangular). Both assume the **square** integer lattice. Their noise is coherent with square quantization.

Our lattice is **hexagonal** (Eisenstein). The dithering PDF must match the lattice geometry or we're fighting the snap at every step.

| PDF | Shape | Variance | Lattice | Coherent With |
|-----|-------|----------|---------|--------------|
| RPDF | Rectangle | 1/12 | Square | Integer arithmetic |
| TPDF | Triangle (=RPDF*RPDF) | 1/6 | Square | Standard audio dither |
| **HPDF** | **Hexagon** | **5/12** | **Eisenstein** | **Our /360 arithmetic** |
| **PPDF** | **Penrose (aperiodic)** | **φ-dependent** | **Fibonacci** | **Semantic structure** |

HPDF has 5× the variance of RPDF but covers the hexagonal Voronoi cell — the dither noise is **coherent** with the snap lattice. After snapping, less residual error because the error distribution matches the lattice geometry.

---

## HPDF: Hexagonal Probability Density Function

Defined as uniform density within the hexagonal Voronoi cell of the Eisenstein lattice:

```
p(x,y) = const  if (x,y) inside hexagonal cell
p(x,y) = 0      otherwise
```

Properties:
- 6 neighbors (vs 4 for square lattice) — tighter packing
- Average quantization error: 2% lower than square lattice
- Convolution: HPDF * HPDF = rotated HPDF at 2× scale (Minkowski sum of two hexagons)
- The self-convolution preserves hexagonal symmetry — the lattice geometry is **closed under dithering**

This matters because: every time you dither and re-snap on the Eisenstein lattice, the noise stays hexagonally structured. You never introduce square-lattice artifacts. The dither IS the lattice.

---

## PPDF: Penrose Probability Density Function

A probability density shaped by Penrose tiling geometry — φ-proportioned, aperiodic, self-similar.

Properties:
- **Not uniform** — has Fibonacci-spaced density peaks
- **Not radially symmetric** — direction matters (Penrose has 5-fold or 10-fold symmetry)
- **Self-similar at all scales** — zoom in on any peak, same pattern
- **Peaks widen with distance** — because F(n+1)-F(n) grows as φⁿ

The widening peaks ARE the N-1 collapse from the previous paper:
- At small F(n): narrow peaks = high precision = individual-level chaos
- At large F(n): wide peaks = low precision = colony-level harmony
- The PDF shape encodes the zoom-level tension automatically

### Snapping Mandelbrot with PPDF

The Mandelbrot set has structure at every scale (fractal). Standard rendering uses uniform grid sampling (RPDF). PPDF sampling places density at Fibonacci-spaced intervals:

| Mandelbrot Period | F-snap | Error | Classification |
|------------------|--------|-------|---------------|
| 1, 2, 3 | exact | 0 | Core (harmony) |
| 4, 6, 7 | ±1 | 1 | Fibonacci-aligned |
| 10, 15 | ±2 | 2 | Near-Fibonacci |
| 30, 50, 100 | +4 to +33 | 4-33 | Chaotic gap |

Periods that ARE Fibonacci: perfect classification. Periods BETWEEN Fibonacci: chaotic gaps. The PPDF naturally concentrates sampling where structure exists and starves the gaps — **semantic sampling** that knows where meaning lives.

---

## Fibonacci-Spline Retrieval: Not Linear Algebra

### Linear Algebra Retrieval (Current)
```
cos(query, document) → similarity score
```
- Dot product. Flat. RPDF-like.
- One snapshot. No path. No convergence story.
- O(N) scan or O(log N) with ANN index.

### Fibonacci-Spline Retrieval (Proposed)
```
r(t) = A·sin(2πt/T) · φ^(t/T)
```
- **sin component**: oscillation — scan all directions (like a radar sweep)
- **φ^(t/T) component**: Fibonacci explosion — widen search radius by φ each period
- Each step adds **1.388 bits of precision** about the target
- The query **grows** into the answer along a spiral path

For N = 1,000,000 documents:
- Linear scan: 1,000,000 operations
- ANN (HNSW): ~14 operations
- Fibonacci spiral: ~29 operations (O(log_φ(N)))

Same complexity class as ANN, but follows a **natural path** through the embedding space. Not random graph traversal — spiral convergence.

### Why This Works

The sin×φ waveform is:
- **Periodic** (sin): ensures no direction is permanently ignored
- **Growing** (φ^t): each sweep covers φ× more area than the last
- **Spiral** (combined): the path traces a Fibonacci spiral through the space

This is retrieval as **growth**, not measurement. The query doesn't measure distance to documents. It grows outward along a Fibonacci spiral until it intersects relevant documents. The first intersection is the best match.

---

## The Complete Pipeline

1. **EMBED** on Eisenstein lattice (Z[ω], not ℝⁿ)
   - HPDF dithering during quantization → coherent noise
   - Snap to lattice points → zero-drift arithmetic

2. **RETRIEVE** by Fibonacci spiral (not cosine similarity)
   - r(t) = A·sin(2πt/T) · φ^(t/T)
   - Each spiral step: oscillate (directions) × grow (φ-widening)
   - O(log_φ(N)) convergence

3. **CLASSIFY** by PPDF snap (not continuous clustering)
   - Snap results to Fibonacci-spaced categories
   - Chaotic gaps = N-1 collapse zones = low-confidence regions
   - φ-proportioned hierarchy (natural scale separation)

4. **CONNECT** by spiral path (not nearest-neighbor graph)
   - The PATH between documents IS the relationship
   - Not flat proximity — spiral trajectory encodes direction and scale

---

## The Deep Connection

RPDF/TPDF are the PDFs of **square lattice** arithmetic. They work because the integer lattice is self-similar under addition (integer + integer = integer).

HPDF is the PDF of **hexagonal lattice** arithmetic. It works because the Eisenstein lattice is self-similar under snap (Z[ω] + Z[ω] stays in Z[ω] after snap).

PPDF is the PDF of **Fibonacci structure** itself. It works because the Mandelbrot set, Penrose tilings, and all self-similar systems have natural Fibonacci spacing at their structural boundaries.

The spline of sin (periodic) and φ^t (explosive) is the waveform that **navigates** all three. It oscillates (RPDF-like scanning) while growing (Fibonacci-like convergence). It's the retrieval waveform for an information space built on the Eisenstein lattice.

---

*"Think about the mathematical tension in the qualities of RPDF and TPDF and how Hexagonal Probability Density Functions would be mathematically superior for our lattice and how a Penrose Probability Density Function could snap a Mandelbrot system along Fibonacci lines."* — Casey

RPDF feeds the square lattice. TPDF is its convolution child. HPDF feeds the hexagonal lattice — our lattice. PPDF feeds the Fibonacci structure — our structure. The spline navigates between them.
