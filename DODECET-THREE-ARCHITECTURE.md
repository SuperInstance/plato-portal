# Dodecet Architecture: 12-bit, 24-bit, 48-bit, 60-bit — Why Three Scales

**Author:** Forgemaster ⚒️  
**Date:** 2026-05-18  
**Repos:** SuperInstance/dodecet-encoder (12-bit Eisenstein constraint encoding)

---

## 1. The Dodecet: 12 Bits = 3 Nibbles = One Eisenstein Constraint

The dodecet (`dodecet-encoder`) is a 12-bit unit composed of **3 nibbles (4-bit groups)**:

```
┌─────────────────────────────────────────┐
│           DODECET (12 bits)             │
├──────────────┬────────────┬─────────────┤
│  Nibble 2    │  Nibble 1  │  Nibble 0   │
│  Bits 11-8   │  Bits 7-4  │  Bits 3-0   │
│  CONSTRAINT  │  DIRECTION │  CHIRALITY  │
│  LEVEL       │  IN CELL   │  + SAFETY   │
│  0=on snap   │  0-15=22.5°│  chamber 0-5│
│  15=at ρ     │  azimuth   │  safe/crit  │
└──────────────┴────────────┴─────────────┘
```

**Why 12 bits?**

- 3 nibbles × 4 bits = 12 bits
- 4096 states — enough to encode the full Eisenstein constraint surface
- **Nibble 0 (chirality):** 6 Weyl chambers (S₃ symmetry, |W(A₂)| = 6) + safety bit
- **Nibble 1 (direction):** 16 angular bins at 22.5° resolution within a chamber
- **Nibble 2 (constraint level):** 16 levels from snap-point (0) to covering radius (15)

The 3-nibble structure is **not arbitrary** — it maps directly to the three degrees of freedom of SE(2):
- **Translation in x** → direction within chamber
- **Translation in y** → constraint level (distance from snap)
- **Rotation θ** → chirality chamber selection

12 bits = dim(SE(2)) = 3, with 4 bits of precision per degree of freedom.

---

## 2. Double Dodecet: 3 Bytes = 24 Bits = 2 × 12 = Paired Constraint

**Three bytes** form a double dodecet:

```
┌─────────────── DODECET A ──────────────┬─────────────── DODECET B ──────────────┐
│  Nibble 2  │  Nibble 1  │  Nibble 0    │  Nibble 2  │  Nibble 1  │  Nibble 0   │
│  Snap-a    │  Snap-b    │  Combined    │  Error-a   │  Error-b   │  Flags      │
│  (x-snap)  │  (y-snap)  │  Chamber+Par │  (x-error) │  (y-error) │  Valid/etc  │
└─────────────────────────────────────────┴─────────────────────────────────────────┘
```

The double dodecet encodes a **full Eisenstein snap result**:
- **Dodecet A:** The lattice coordinates (snap_a, snap_b in basis coordinates)
- **Dodecet B:** The error vector + metadata

This is the fundamental **tile** for our constraint theory data format. One tile = 3 bytes = one complete Eisenstein snap.

**Why 3 bytes?**
- 3 bytes × 8 bits = 24 bits
- 2 × 12 = double the SE(2) precision, OR
- 1 × SE(3) constraint (6 DOF × 4 bits each = 24 bits)

**The d=3 prediction:** A double dodecet can encode one SE(3) snap at reduced precision:
- 6 DOF × 4 bits/DOF = 24 bits = 3 bytes
- This means **3 bytes is the minimum tile size for 3D constraint encoding**

---

## 3. Six Bytes: 48 Bits = 4 × 12 = Full SE(3) Constraint

```
┌─── Dodecet 1 ───┬─── Dodecet 2 ───┬─── Dodecet 3 ───┬─── Dodecet 4 ───┐
│  TX (4 bits)     │  TY (4 bits)    │  TZ (4 bits)    │  Flags (4 bits) │
│  + precision     │  + precision    │  + precision    │  + metadata     │
├──────────────────┼──────────────────┼──────────────────┼──────────────────┤
│  Rx (4 bits)     │  Ry (4 bits)    │  Rz (4 bits)    │  Confidence     │
│  + precision     │  + precision    │  + precision    │  (4 bits)       │
└──────────────────┴──────────────────┴──────────────────┴──────────────────┘
```

**48 bits** = 6 bytes = 4 dodecets:

- 6 DOF of SE(3) × 8 bits/DOF = 48 bits (full precision)
- OR: 4 × 12-bit dodecets, each encoding one SE(2) constraint + metadata

**48-bit is the natural word size for 3D constraint computing.**

This connects to:
- **dim(SE(3)) = 6** — six degrees of freedom
- **6 bytes × 8 bits = 48 bits** — one full 3D rigid body state
- **4 × 12-bit dodecets** — backward compatible with 2D tiles

### 48-bit in Computing History

The 48-bit word has precedent:
- **Burroughs B5000/B6000** (1961-1977): 48-bit words, tag bits for type safety
- **UNIVAC 1100 series**: 36-bit words, but 48-bit floating point
- **CDC 1604**: 48-bit words
- **Modern SIMD**: AVX-512 has 512-bit registers; 48-bit sub-units for 3D coordinates

The pattern: when engineers needed to represent **3D data naturally**, they kept arriving at multiples of 12 and 48.

---

## 4. The 60-bit Word: CDC Cyber, TUTOR, and PLATO

### 4.1 The CDC 60-bit Architecture

The CDC 6000 series and Cyber mainframes used a **60-bit word**. This was not arbitrary — it was chosen by Seymour Cray for mathematical reasons:

- **10 × 6-bit Display Code characters** per word (CDC's character encoding)
- **60 = lcm(12, 15, 20, 30)** — compatible with many subdivisions
- **Single-precision float:** 60-bit mantissa + exponent (unusual precision)
- **Instruction packing:** Multiple 15-bit or 30-bit instructions per 60-bit word

### 4.2 PLATO and TUTOR: The First Vectorized Reasoning System

PLATO (Programmed Logic for Automatic Teaching Operations) ran on CDC Cyber hardware at UIUC, starting 1960. The TUTOR language (1965, Sherwood) was its authoring system.

**What made TUTOR different from modern AI:**

TUTOR implemented a form of **vectorized reasoning** that is fundamentally different from today's LLMs:

| Aspect | Modern LLMs | TUTOR/PLATO |
|--------|-------------|-------------|
| Where reasoning happens | Inside the model (billions of parameters) | Between the model and the user (filter + route) |
| Role of language | Input/output surface | **Command routing substrate** |
| Architecture | Monolithic transformer | **Decision tree with pattern matching** |
| Intelligence source | Statistical patterns in training data | **Author-encoded logic + user testing** |
| Vectorization | Internal attention heads | **External command filters** |

**TUTOR's vectorized reasoning worked like this:**

1. **Student types free-text response** (natural language input)
2. **TUTOR's `answer` command runs a pattern-matching filter** over the input
   - `answer <specification>` defines acceptable responses
   - `wrong <specification>` defines known wrong answers
   - `choices <list>` defines multiple choice options
3. **The filter routes to specific evaluation paths** — like a decision tree, but:
   - Each path tests a specific *concept* (not just string match)
   - Synonyms, ignorable words, required words are all configurable
   - The system handles "malformed" input gracefully
4. **The evaluation produces a teaching response** — not a generated text, but a **structured pedagogical action**

This is "vectorized" in the sense that:
- The input text is decomposed into **feature dimensions** (keyword presence, word order, required/optional elements)
- Each dimension is tested **independently and in parallel** (like dot products against filter vectors)
- The result vector is **routed** to the appropriate teaching strategy
- **The intelligence is in the routing, not in the model**

### 4.3 Why This Matters for Our Work

TUTOR's approach is closer to what we're building than modern LLMs:

1. **Our constraint theory IS a routing system.** The Eisenstein snap doesn't "reason" — it routes a real-valued input to the nearest lattice point through a geometric filter. The intelligence is in the lattice structure, not in computation.

2. **The dodecet IS a TUTOR-style feature vector.** Each 12-bit dodecet encodes: "which chamber am I in?" (routing) + "how far from snap?" (confidence) + "am I safe?" (binary decision). This is exactly the pattern-matching filter approach.

3. **60-bit = 5 dodecets.** A CDC 60-bit word could hold:
   - 5 × 12-bit dodecets (one per constraint dimension, with 3 spare)
   - 10 × 6-bit Display Code characters (the original use)
   - **The connection:** 5 dodecets would encode a complete constraint state for a 5-dimensional problem

4. **TUTOR's `answer` command is a deadband filter.** When TUTOR checks if a response matches a specification, it's doing exactly what our deadband attention does: "is this input within tolerance of the expected pattern?" The "tolerance" in TUTOR is the set of acceptable synonyms and word orderings; in our system, it's the covering radius ρ of the Eisenstein lattice.

---

## 5. The Three-Byte / Six-Byte / 60-bit Unified Architecture

### The Pattern

| Unit | Bits | Bytes | Dodecets | What It Encodes |
|------|------|-------|----------|-----------------|
| **Nibble** | 4 | 0.5 | 1/3 | One SE(2) DOF at 16 levels |
| **Dodecet** | 12 | 1.5 | 1 | One SE(2) constraint (3 DOF × 4 bits) |
| **Triple byte** | 24 | 3 | 2 | One SE(3) constraint (6 DOF × 4 bits) OR full SE(2) snap |
| **Six bytes** | 48 | 6 | 4 | Full SE(3) rigid body state (6 DOF × 8 bits) |
| **CDC word** | 60 | 7.5 | 5 | Complete constraint system (5 dimensions × 12 bits) |
| **64-bit word** | 64 | 8 | 5⅓ | Modern standard (wasteful — 16 bits unused for 5-dodecet encoding) |

### The Law

**For a d-dimensional constraint system:**
- Minimum tile = d(d+1)/2 × 4 bits (one nibble per DOF)
- Full precision tile = d(d+1)/2 × 8 bits (one byte per DOF)

| d | dim(SE(d)) | Min tile (4-bit) | Full tile (8-bit) |
|---|-----------|------------------|-------------------|
| 1 | 1 | 4 bits (1 nibble) | 8 bits (1 byte) |
| 2 | 3 | 12 bits (1 dodecet) | 24 bits (3 bytes) |
| 3 | 6 | 24 bits (3 bytes) | 48 bits (6 bytes) |
| 4 | 10 | 40 bits (5 bytes) | 80 bits (10 bytes) |
| 5 | 15 | 60 bits (CDC word!) | 120 bits (15 bytes) |

**The CDC 60-bit word is the natural encoding for a 5-dimensional constraint system at nibble precision.**

This is NOT a coincidence. Seymour Cray designed the 60-bit word for scientific computing, and the number 60 = 15 × 4 = dim(SE(5)) × 4 bits/DOF.

### Why 60-bit Failed (And What That Teaches Us)

The CDC 60-bit word lost to IBM's 32-bit architecture because:
1. **Economies of scale** — more 32-bit machines = cheaper components
2. **Binary alignment** — 32 is a power of 2, making addressing simpler
3. **Good enough** — 32 bits covers most problems adequately

The same forces killed Brusentsov's ternary Setun. The mathematically optimal lost to the economically convenient.

**But now we're hitting the wall.** As we push into 3D constraint systems, 32/64-bit words waste bits:
- A 3D rigid body needs exactly 48 bits (6 bytes)
- Stored in a 64-bit word: 16 bits wasted (25%)
- Stored in two 32-bit words: 16 bits wasted + alignment overhead

**The dodecet architecture recovers this efficiency** by using 12-bit tiles that pack without waste:
- 4 dodecets = 48 bits = one SE(3) state, zero waste
- 5 dodecets = 60 bits = one SE(5) state, matches CDC word size exactly

---

## 6. The Deep Connection: TUTOR as Proto-Constraint System

### TUTOR's Answer Judging = Deadband Attention

TUTOR's `answer` command implemented what we now call **deadband attention**:

```tutor
answer <it is> <(going)> up
wrong <it is> <(going)> down
wrong <it is> <(going)> sideways
```

This says: "accept any response containing 'it', 'is', and 'up', optionally containing 'going', in any order, ignoring other words."

Translated to our constraint theory:
- **Required words** = hard constraints (must be satisfied)
- **Optional words** = soft constraints (nice to have, ignored if absent)
- **Wrong answers** = forbidden regions (explicit deadband exclusions)
- **Ignorable words** = noise tolerance (deadband around the expected pattern)

### The 60-bit as Filter Register

In the PLATO system, student responses were packed into 60-bit words for pattern matching. Each bit position could represent:
- Presence/absence of a keyword
- A feature of the response (length, special characters, numerical content)
- A routing flag (which evaluation path to take)

This is **exactly** how our dodecet constraint system works:
- Nibble 0 (chirality) = routing flag (which chamber → which evaluation path)
- Nibble 1 (direction) = feature encoding (angular position within chamber)
- Nibble 2 (level) = confidence signal (distance from snap point)

### TUTOR vs Modern AI: The Fundamental Difference

**Modern LLMs:** "I have memorized patterns from 10TB of text. Given your input, I'll statistically predict what comes next."

**TUTOR:** "I have been programmed with specific knowledge about what correct and incorrect answers look like. Given your input, I'll route it through a decision tree that tests your understanding of specific concepts."

**Our constraint theory:** "I have been programmed with geometric structure (Eisenstein lattice). Given your input (real-valued vector), I'll route it to the nearest lattice point through a geometric filter that tests its distance from known-good regions."

The lineage is: **TUTOR → Expert Systems → Constraint Theory → Eisenstein Snap → Dodecet Encoding**

All of these share the same philosophical stance: **intelligence is in the routing structure, not in the statistical model.**

---

## 7. Predictions

1. **3-byte tiles** (double dodecet) will become the standard for 2D constraint encoding — one complete snap result per tile
2. **6-byte tiles** (quadruple dodecet) will be the natural format for 3D rigid body states
3. **60-bit processing** will return as specialized hardware for high-dimensional constraint systems — exactly matching the CDC word size for d=5
4. **TUTOR-style routing** (deadband attention with explicit accept/reject regions) will prove more efficient than attention heads for structured domains
5. **The dodecet will prove more efficient than byte-aligned encoding** for constraint theory data, just as balanced ternary proves more efficient than binary

---

## References

- `SuperInstance/dodecet-encoder` — 12-bit Eisenstein constraint encoding, Rust, WASM, C bridge
- `src/eisenstein.rs` — Weyl group S₃ integration, 6 chambers, covering radius
- CDC 6000 Series Reference Manual — 60-bit word architecture
- Sherwood, B.A. (1974) "The TUTOR Language" — PLATO authoring system
- Bitzer, D. (1960s) PLATO system design — first vectorized reasoning system
- Brusentsov, N.P. (1958) Setun — balanced ternary computer, proved ternary superiority in hardware
