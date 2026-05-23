# Indian & Arabic Music as Constraint Systems

**A deep mathematical investigation of raga, maqam, śruti, quarter tones, tala, and the universal lattice that unites the world's microtonal traditions.**

---

## Table of Contents

1. [The 22 Śruti — India's Microtonal Substrate](#1-the-22-śruti--indias-microtonal-substrate)
2. [Raga as Constraint Profile](#2-raga-as-constraint-profile)
3. [Tala as Rhythmic Lattice](#3-tala-as-rhythmic-lattice)
4. [Arabic Quarter Tones & Z/24Z](#4-arabic-quarter-tones--z24z)
5. [Maqam as Lattice Journey](#5-maqam-as-lattice-journey)
6. [Taqsim — Improvisation Without Clock](#6-taqsim--improvisation-without-clock)
7. [Cross-Cultural Synthesis — The Universal Lattice](#7-cross-cultural-synthesis--the-universal-lattice)
8. [The Grand Synthesis — UniversalMusicTile](#8-the-grand-synthesis--universalmusictile)
9. [References](#9-references)

---

## 0. Motivation

In `CHINESE-MUSIC-CONSTRAINT-THEORY.md` we established that Chinese 五音 maps cleanly to Z/5Z embedded in Z/12Z via the fifth-chain homomorphism, and that the pentatonic's larger covering radius (ρ₅ ≈ 0.588 vs ρ₁₂ ≈ 0.259) corresponds to its greater pitch ambiguity. In `DEEP-MATH-MUSICAL-STRUCTURE.md` we developed the general theory of scales as coset structures, the Eisenstein lattice over arbitrary cyclic groups, and the resolution-perplexity tradeoff.

Now we complete the triangle. Indian classical music operates on 22 microtonal divisions with *asymmetric* scales and *continuous* ornamentation. Arabic music operates on 24-TET with quarter tones and prescribed tonal journeys. Both systems are far richer than Western 12-TET in their constraint profiles — and both offer profound insights for our unified theory.

---

## 1. The 22 Śruti — India's Microtonal Substrate

### 1.1 Z/22Z: Group Structure

The cyclic group Z/22Z = Z/(2·11)Z. By the Chinese Remainder Theorem:

$$\mathbb{Z}/22\mathbb{Z} \cong \mathbb{Z}/2\mathbb{Z} \times \mathbb{Z}/11\mathbb{Z}$$

This is a **fundamentally different structure** from Z/12Z ≅ Z/4Z × Z/3Z. The factorization 22 = 2 × 11 (product of two primes) means:

**Subgroups of Z/22Z:**

| Subgroup | Order | Generator | Musical Interpretation |
|----------|-------|-----------|----------------------|
| {0} | 1 | 0 | Silence / single pitch |
| ⟨11⟩ = {0, 11} | 2 | 11 | Octave equivalence (tritone in śruti-space) |
| ⟨2⟩ = {0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20} | 11 | 2 | Whole-śruti scale (11 equal divisions) |
| Z/22Z itself | 22 | 1 or any coprime | Full śruti space |

There are exactly **4 subgroups** (compared to 6 for Z/12Z). The paucity comes from 22 being a product of two primes — fewer divisors = fewer subgroups.

**Key insight:** The subgroup ⟨2⟩ of order 11 is particularly interesting. It divides the octave into 11 equal parts — which has *no Western analogue*. This is an entirely new pitch universe. The 11-tone equal division is non-existent in Western theory but emerges naturally from the śruti framework.

### 1.2 The Śruti Are NOT Equally Spaced

Crucially, the 22 śruti are **not** equally spaced — they cluster around the 12 semitone positions of 12-TET. The mapping is:

| Semitone (12-TET) | Śruti positions | Cluster size |
|--------------------|----------------|-------------|
| C (Sa) | 0, 1, 2 | 3 |
| C♯/D♭ | 3, 4 | 2 |
| D (Re) | 5, 6 | 2 |
| D♯/E♭ | 7, 8 | 2 |
| E (Ga) | 9, 10 | 2 |
| F (Ma) | 11, 12 | 2 |
| F♯/G♭ | 13, 14 | 2 |
| G (Pa) | 15, 16 | 2 |
| G♯/A♭ | 17, 18 | 2 |
| A (Dha) | 19, 20 | 2 |
| A♯/B♭ | 21 | 1 |
| B (Ni) | — (wrapped to next octave) | — |

Wait — that's only 22 from positions 0–21. The clustering pattern is actually:

The 12 semitones each have either 1 or 2 śruti, with some having 3 (particularly Sa and Pa, the drone notes, which get more microtonal resolution). The exact mapping follows from the **just intonation ratios** of the 22 śruti:

| Śruti # | Ratio to Sa | Cents | Nearest semitone |
|---------|-------------|-------|-----------------|
| 0 | 1/1 | 0 | C |
| 1 | 256/243 | 90 | C (flat) |
| 2 | 16/15 | 112 | C (sharp) |
| 3 | 10/9 | 182 | D (flat) |
| 4 | 9/8 | 204 | D (natural) |
| 5 | 32/27 | 294 | E♭ (flat) |
| 6 | 6/5 | 316 | E♭ (natural) |
| 7 | 5/4 | 386 | E (natural) |
| 8 | 81/64 | 408 | E (sharp) |
| 9 | 4/3 | 498 | F |
| 10 | 27/20 | 520 | F (sharp) |
| 11 | 45/32 | 590 | F♯ |
| 12 | 729/512 | 612 | F♯ (sharp) |
| 13 | 3/2 | 702 | G |
| 14 | 128/81 | 792 | A♭ (flat) |
| 15 | 8/5 | 814 | A♭ |
| 16 | 5/3 | 884 | A (natural) |
| 17 | 27/16 | 906 | A (sharp) |
| 18 | 16/9 | 996 | B♭ |
| 19 | 9/5 | 1018 | B♭ (sharp) |
| 20 | 15/8 | 1088 | B |
| 21 | 243/128 | 1110 | B (sharp) |

**This is NOT a uniform lattice.** The spacing varies from ~22 cents (between śruti 5 and 6) to ~90 cents (between śruti 0 and 1). The śruti system is a **non-uniform quantization** of pitch space.

### 1.3 The 22/12 Relationship: A Refinement, Not a Replacement

The relationship between 22-śruti and 12-TET is not a simple "finer grid." The 22 śruti can be modeled as a **partition refinement**:

$$\mathcal{P}_{12} = \{[0), [1), \ldots, [11)\} \quad \text{(12-TET partition)}$$
$$\mathcal{P}_{22} \succ \mathcal{P}_{12} \quad \text{(22-śruti is a refinement)}$$

Each of the 12 semitone bins is further divided into 1–3 śruti bins. The refinement is **non-uniform** — notes that are harmonically important (Sa, Pa, major third) get more resolution.

**In lattice terms:** The 22-śruti system is not a sublattice or superlattice of 12-TET. It's a **non-uniform quantization** where the Voronoi cells have different sizes. This is closer to vector quantization (as in speech coding) than to lattice theory proper.

### 1.4 Covering Radius Comparison

From `DEEP-MATH-MUSICAL-STRUCTURE.md`, the covering radius for n equally-spaced points on the unit circle is:

$$\rho_n = \frac{1}{2\sin(\pi/n)}$$

But the śruti are *not* equally spaced. For a non-uniform set, the covering radius is determined by the **maximum gap** between consecutive points:

| System | n | Max gap (cents) | Effective ρ (cents) |
|--------|---|----------------|---------------------|
| 12-TET | 12 | 100 | 50 |
| 22-śruti | 22 | ~112 (between clusters) | ~56 |
| 24-TET (Arabic) | 24 | 50 | 25 |
| 53-TET (Turkish) | 53 | ~22.6 | ~11.3 |

**Surprising result:** The 22-śruti system has a *worse* covering radius than 12-TET in the worst case, because the clustering creates gaps of up to ~112 cents between some adjacent śruti (e.g., between the sharp end of one cluster and the flat end of the next). But **within** each cluster, the resolution is much finer (~22 cents).

This means the śruti system is **locally precise but globally coarse** — it invests its resolution where it matters most (around consonant intervals) and saves resolution at dissonant zones. This is *optimal* from an information-theoretic perspective: it maximizes the perceptual utility of each bit of resolution.

### 1.5 The Eisenstein Lattice Over Z/22Z

If we treat the 22 śruti as Z/22Z (ignoring the non-uniform spacing for the algebraic structure), the Eisenstein lattice on intervals becomes:

$$\Lambda_{22} = \{(k_1, k_2) \in \mathbb{Z}^2 : k_1 + k_2 \equiv 0 \pmod{22}\}$$

This is a sublattice of Z² of index 22. Its covering radius in the Eisenstein norm scales as:

$$\rho_{A_2}^{(22)} = \frac{\sqrt{22}}{\sqrt{3}} \approx 2.714$$

vs.

$$\rho_{A_2}^{(12)} = \frac{\sqrt{12}}{\sqrt{3}} \approx 2.000$$

The 22-śruti interval lattice has a **36% larger covering radius** than the 12-TET interval lattice. More possible intervals = more space to navigate = more freedom AND more potential for error.

But with the **non-uniform** spacing, the effective lattice is distorted — the Voronoi cells around commonly-used intervals (fifths, fourths, major thirds) are *smaller* (tighter snap) while cells around dissonant intervals are *larger* (looser snap). This is a **weighted lattice** where the weight function is determined by harmonic salience.

---

## 2. Raga as Constraint Profile

### 2.1 Raga ≠ Scale

A Western scale is a subset of pitch classes. A raga is a **complete musical personality** — a highly constrained system that specifies:

| Property | Sanskrit | Constraint Type | Formal Analogue |
|----------|----------|----------------|-----------------|
| Ascending scale | ārohaṇa | Ordered pitch set (up) | Sequence S↑ ⊂ Z/22Z |
| Descending scale | avarohaṇa | Ordered pitch set (down) | Sequence S↓ ⊂ Z/22Z |
| King note | vādī | Primary constraint anchor | Weighted node in lattice |
| Prime minister note | saṃvādī | Secondary anchor | Second-weighted node |
| Enemy note | vivādī | Forbidden / hard constraint | Excluded node |
| Melodic movement | gamaka | Continuous ornamentation | Non-discrete path in lattice |
| Time of day | samay | Environmental constraint | Boolean gate on raga activation |
| Season | ṛtu | Environmental constraint | Seasonal gate |
| Emotional state | rasa | Affective constraint | FluxVector target |
| Phrase seed | pakad | Melodic fingerprint | Identity function on motif space |

This is **far richer** than a StyleTile. A raga is essentially a **constraint program** — a collection of hard constraints, soft constraints, environmental guards, and continuous dynamics that together define a musical universe.

### 2.2 Asymmetric Scales: Ārohaṇa ≠ Avarohaṇa

Some ragas have different notes ascending vs. descending. For example:

**Raga Bhimpalasi:**
- Ārohaṇa (ascending): Sa - Ga - Ma - Pa - Ni - Ṡa  (n Ga, ṫ Ma, P, ko Ni) → {0, 3, 5, 7, 10, 12}
- Avarohaṇa (descending): Ṡa - Ni - Dha - Pa - Ma - Ga - Re - Sa → {12, 10, 9, 7, 5, 3, 2, 0}

Note: Dha (9) and Re (2) appear in the descent but NOT the ascent. The ascending and descending sets are **different subsets of Z/22Z**:

$$S_\uparrow = \{0, 3, 5, 7, 10\} \subsetneq S_\downarrow = \{0, 2, 3, 5, 7, 9, 10\}$$

**Formal model:** A raga is a pair (S↑, S↓) of ordered subsets of Z/22Z with S↑ ⊆ S↓ typically (or occasionally S↓ ⊆ S↑). The **effective constraint set** at any moment depends on the direction of melodic motion:

$$\text{ValidPitch}(t) = \begin{cases} S_\uparrow & \text{if } \dot{p}(t) > 0 \text{ (ascending)} \\ S_\downarrow & \text{if } \dot{p}(t) < 0 \text{ (descending)} \end{cases}$$

This is a **direction-dependent constraint** — the first time we've encountered a constraint that depends on the *sign of the first derivative* of pitch. In lattice terms, the snap target set *changes* depending on whether you're moving up or down.

**Deadband implication:** The deadband funnel must be **anisotropic** — its width depends on the direction of approach. When ascending, you snap to S↑; when descending, you snap to S↓. At turning points (where $\dot{p} = 0$), the snap target is the intersection S↑ ∩ S↓, which may be a strict subset of both.

### 2.3 Vādī and Saṃvādī: Weighted Constraint Anchors

The vādī (king) and saṃvādī (prime minister) notes are not just "important" — they function as **attractor basins** in the pitch lattice. They're typically a fourth or fifth apart (consonant interval), creating a dual-center gravity:

$$\text{Gravitational pull of note } n = w_v \cdot \delta(n, v) + w_s \cdot \delta(n, s)$$

where $v$ = vādī, $s$ = saṃvādī, $\delta$ is an inverse-distance function, and $w_v > w_s > 0$.

This creates a **potential field** over the lattice. Melodies tend to oscillate around the vādī and resolve toward it, with the saṃvādī serving as a secondary resting point. The potential field is:

$$V(n) = -\frac{w_v}{d(n, v) + \epsilon} - \frac{w_s}{d(n, s) + \epsilon}$$

where $d$ is interval distance and $\epsilon$ prevents singularities. Melodic motion can be modeled as **gradient descent** on this potential, modulated by the raga's sequential constraints.

### 2.4 Vivādī: Hard Constraints as Forbidden Zones

The vivādī (enemy) note is a **hard exclusion**. If a raga omits a note, that note is not just "not preferred" — it's *forbidden*. In constraint-theory terms:

$$\text{vivādī note } v^* \notin S_\uparrow \cup S_\downarrow$$

More strongly, the performance should *avoid even approaching* $v^*$ — it creates a **repulsive potential**:

$$V(n) = +\frac{w_{\text{repel}}}{d(n, v^*) + \epsilon}$$

The total potential field for a raga is:

$$V_{\text{raga}}(n) = -\sum_{\text{vādī, saṃvādī}} \frac{w_i}{d(n, n_i) + \epsilon} + \sum_{\text{vivādī}} \frac{w_j}{d(n, n_j) + \epsilon}$$

This is a **Lenard-Jones-like potential** — attractive to anchor notes, repulsive from forbidden notes. Melody navigates this landscape like a particle in a force field.

### 2.5 Gamakas: Continuous Oscillation, Not Discrete Snap

This is perhaps the most radical departure from Western lattice theory. In Indian music, notes are **not** discrete points. A single "note" like Ga might be rendered as a continuous oscillation spanning several śruti:

$$\text{Ga}_{\text{gamaka}}(t) = G_0 + A \sin(2\pi f_g t)$$

where $G_0$ is the nominal pitch, $A$ is the gamaka amplitude (potentially several śruti), and $f_g$ is the gamaka frequency (typically 5–8 Hz, creating the characteristic "shake").

**In lattice terms:** A gamaka is not a snap to a lattice point — it's an **oscillation around** a lattice point. The snap is not:

$$\text{pitch} \to \text{nearest lattice point}$$

but rather:

$$\text{pitch} \to \text{oscillation around nearest lattice point with prescribed amplitude and frequency}$$

This requires a fundamentally different model. Instead of:

```
snap(p) = argmin_{s ∈ Scale} |p - s|
```

we need:

```
gamaka_snap(p) = oscillate(argmin_{s ∈ Scale} |p - s|, 
                            amplitude=gamaka_table[s].A,
                            frequency=gamaka_table[s].f)
```

The gamaka parameters are **note-dependent** — different notes in the same raga have different gamakas. Some notes are rendered "straight" (A=0), others with heavy oscillation (A ≈ 3–5 śruti). This is encoded in a **gamaka table** specific to each raga.

**Continuous vs. discrete lattice:** The gamaka system suggests a model where the lattice points are not zero-dimensional but have **finite extent** — each note occupies a *region* of pitch space, not a point. The snap is to a *region*, and within that region, prescribed oscillatory motion occurs.

Formally, instead of snapping to $s \in S$, we snap to a **tubular neighborhood**:

$$T_\epsilon(s) = \{p \in \mathbb{R} : |p - s| < \epsilon(s)\}$$

where $\epsilon(s)$ is the gamaka amplitude for note $s$ in the current raga. The deadband funnel's terminal region is not a point but a **tube**.

### 2.6 Time of Day as Environmental Constraint

Ragas are associated with specific times:

| Time | Raga examples | Rasa |
|------|-------------|------|
| Dawn (6–9 AM) | Bhairav, Todi | Devotional, contemplative |
| Morning (9–12) | Bhimpalasi, Deshkar | Longing, romantic |
| Afternoon (12–3) | Bhimpalasi, Bageshri | Peaceful, romantic |
| Evening (3–6) | Yaman, Bhairavi | Peaceful, romantic |
| Night (9–12 AM) | Darbari, Malkauns | Majestic, mysterious |
| Late night (12–3) | Bageshri, Abhogi | Deep, meditative |

In constraint-theory terms, this is an **environmental guard** — a boolean condition that gates whether a raga's constraint set is active:

```python
def raga_active(raga, current_time):
    return raga.time_range.contains(current_time)
```

This is the first time we've encountered a constraint system where **wall-clock time** is a constraint variable. In the deadband funnel model, this means:

$$\text{Funnel}(t, \text{pitch}, \text{time\_of\_day}) = \begin{cases}
\text{RagaFunnel}_r & \text{if time\_of\_day ∈ samay}(r) \\
\emptyset & \text{otherwise}
\end{cases}$$

The "correct" constraint set depends on the external world state. This is a **context-dependent constraint system** — the rules change based on environmental conditions.

### 2.7 Rasa as FluxVector Mapping

The nine rasas (emotional essences) map to our FluxVector concept:

| Rasa | Emotion | FluxVector characteristics |
|------|---------|---------------------------|
| Śṛṅgāra | Love/Romance | Slow rate, moderate energy, upward bias |
| Hāsya | Joy/Mirth | Fast rate, high energy, random direction |
| Karuṇa | Sadness/Compassion | Slow rate, low energy, downward bias |
| Raudra | Anger | Fast rate, high energy, angular/discontinuous |
| Vīra | Heroism | Moderate rate, high energy, upward+forward |
| Bhayānaka | Fear | Variable rate, low energy, tremulous |
| Bībhatsa | Disgust | Angular, irregular, low coherence |
| Adbhuta | Wonder | Wide pitch range, moderate energy, exploratory |
| Śānta | Peace | Minimal rate, low energy, centered |

Each raga targets one (sometimes two) rasas. This is a mapping from the **raga constraint set** to a **target region in FluxVector space**. The mapping is:

$$\text{Raga}(r) \xrightarrow{\text{encode}} \text{FluxVector}_{\text{target}} \in \mathbb{R}^4$$

where the 4 dimensions are: {rate, energy, direction, coherence}.

### 2.8 Formal Raga Model

Putting it all together, a raga is a tuple:

$$\mathcal{R} = (S_\uparrow, S_\downarrow, v, s, V_{\text{forbidden}}, G, T_{\text{samay}}, r_{\text{rasa}}, P_{\text{pakad}})$$

where:
- $S_\uparrow, S_\downarrow \subset \mathbb{Z}/22\mathbb{Z}$: ascending/descending pitch sets
- $v$: vādī (primary attractor)
- $s$: saṃvādī (secondary attractor)
- $V_{\text{forbidden}}$: vivādī exclusion set
- $G: S_\uparrow \cup S_\downarrow \to \mathbb{R}^2$: gamaka function mapping each note to (amplitude, frequency)
- $T_{\text{samay}}$: time-of-day interval
- $r_{\text{rasa}}$: target emotional state
- $P_{\text{pakad}}$: characteristic melodic phrase (identity motif)

This is a **constraint program**, not a scale. The total number of theoretically possible ragas in the Hindustani system is estimated at:

- 12 swara positions × 2 variants for some (śuddha/komal) ≈ 16 effective pitches
- Thāṭ system: 32 parent scales × ornamental variants × time restrictions
- Practically: ~500 named ragas, theoretically: thousands

The constraint space is **vast but structured**. Each raga carves out a specific region of musical possibility.

---

## 3. Tala as Rhythmic Lattice

### 3.1 Tala as Hierarchical Group Product

Indian tala (rhythmic cycles) are **not** simple cyclic groups. They have internal structure — beats are grouped into unequal segments, and each segment has a different accentual weight.

**Common talas:**

| Tala | Structure | Total beats | Group decomposition |
|------|-----------|-------------|---------------------|
| Teental | 4+4+4+4 | 16 | Z/4 × Z/4 |
| Jhaptal | 2+3+2+3 | 10 | Z/5 × Z/2 (with permutation) |
| Rupak | 3+2+2 | 7 | Z/7 (prime, indecomposable) |
| Ektal | 2+2+2+2+2+2 | 12 | Z/6 × Z/2 |
| Keherwa | 4+4 | 8 | Z/4 × Z/2 |
| Dadra | 3+3 | 6 | Z/3 × Z/2 |

**Group-theoretic analysis:**

**Teental (4+4+4+4 = 16):**
- The cyclic group Z/16Z has the decomposition Z/16Z ≅ Z/16Z (since 16 = 2⁴, no further CRT decomposition).
- But the *metrical structure* 4+4+4+4 suggests the product Z/4 × Z/4 (4 groups of 4), which is NOT Z/16Z — it's Z/4 × Z/4 of order 16.
- The difference: Z/16Z is cyclic (single generator), while Z/4 × Z/4 requires two generators. Musically, this means the first beat of each 4-beat group (sam, tal, khali) serves as a **secondary time reference** — a second "clock."
- **The tala has two levels of synchronization:** the global cycle (16 beats) and the local cycle (4 beats within each segment).

**Jhaptal (2+3+2+3 = 10):**
- Z/10Z ≅ Z/5 × Z/2 by CRT.
- The metrical structure 2+3+2+3 is NOT isomorphic to 5×2 — it's a specific permutation of the product.
- The asymmetry (2≠3) creates a **non-isochronous** grouping — this is fundamentally different from Western meter, where all beats at the same level have equal duration.

**Rupak (3+2+2 = 7):**
- Z/7Z is a prime-order cyclic group — it has NO nontrivial subgroups and NO CRT decomposition.
- The metrical structure 3+2+2 cannot be expressed as a group product — it's a single irreducible cycle.
- **This makes Rupak "metrically prime"** — there's no simpler metrical unit to subdivide into. Every performance of Rupak has an irreducible "7-ness."

### 3.2 The Tala Lattice

For a tala with structure $n_1 + n_2 + \ldots + n_k = N$, we can define a **metrical lattice**:

$$\Lambda_{\text{tala}} = \{(i, j) : 0 \leq i < k, 0 \leq j < n_i\}$$

where $i$ indexes the segment (vibhāg) and $j$ indexes the beat within the segment. This is a **non-rectangular lattice** — different segments have different numbers of beats.

The lattice has:
- **Strong beats** (tālī): first beats of segments 1, 2, 3, ... (marked by hand clap)
- **Weak beats** (khālī): first beat of a specific segment (marked by wave)
- **The sam**: beat 1 of segment 1 (the "reset" point, equivalent to downbeat)

In constraint-theory terms:
- Strong beats are **attractor points** in the time lattice — there's a gravitational pull toward landing on them
- The sam is the **strongest attractor** — the point of maximum resolution
- Between attractors, rhythmic freedom is permitted (fill patterns, variations)

### 3.3 Deadband Funnel with Non-Isochronous Cycles

The deadband funnel model assumes a regular grid of time points. But Indian tala is **non-isochronous** — the segments have unequal lengths. How does the funnel work?

The key insight: the funnel operates on **metrical time**, not clock time. The time axis is warped so that each segment occupies equal "metrical space" regardless of its beat count:

```
Clock time:    |---3---|---2---|---2---|   (Rupak: 3+2+2)
Metrical time: |---1---|---1---|---1---|   (3 equal metrical units)
```

The deadband funnel operates in metrical time, where the segments are equally spaced. The snap targets are the segment boundaries (strong beats), not individual beats.

**Implication:** The funnel has a **variable resolution** in clock time. For a 3-beat segment, the funnel approaches its target over 3 beats; for a 2-beat segment, over 2 beats. The funnel "width" in clock time varies with segment length:

$$\text{FunnelWidth}(t) = w_0 \cdot \left(1 - \frac{t \bmod n_{\text{segment}}}{n_{\text{segment}}}\right)$$

where $n_{\text{segment}}$ is the length of the current segment. Longer segments give a gentler, wider funnel; shorter segments give a steeper, narrower funnel.

### 3.4 The Theka as Rhythmic Constraint Profile

Each tala has a **theka** — a standard drum pattern that defines its identity. The theka is the rhythmic analogue of a raga's pakad:

$$\text{Theka}(t) = \text{drum_pattern}[\text{segment}(t)][\text{beat}(t)]$$

The theka provides a **constraint envelope** for rhythmic improvisation. Soloists can elaborate, subdivide, and syncopate, but the theka provides the invariant framework. In constraint-theory terms, it's the **identity function** for the rhythmic lattice — deviations from it are permitted but must resolve back.

---

## 4. Arabic Quarter Tones & Z/24Z

### 4.1 Z/24Z: The Quarter-Tone Group

The cyclic group Z/24Z decomposes as:

$$\mathbb{Z}/24\mathbb{Z} \cong \mathbb{Z}/8\mathbb{Z} \times \mathbb{Z}/3\mathbb{Z}$$

by CRT (since 24 = 8 × 3 and gcd(8,3) = 1). This is richer than Z/12Z ≅ Z/4Z × Z/3Z.

**Subgroups of Z/24Z:**

| Subgroup | Generator(s) | Order | Musical interpretation |
|----------|-------------|-------|----------------------|
| {0} | 0 | 1 | Single pitch |
| ⟨12⟩ | 12 | 2 | Octave/tritone equivalence |
| ⟨8⟩ | 8 | 3 | Augmented triad in quarter-tone space |
| ⟨6⟩ | 6 | 4 | Diminished 7th in quarter-tone space |
| ⟨4⟩ | 4 | 6 | Whole-tone scale + quarter tones |
| ⟨3⟩ | 3 | 8 | Minor-third chain (octatonic extended) |
| ⟨2⟩ | 2 | 12 | 12-TET embedded in 24-TET |
| ⟨1⟩ | 1 | 24 | Full quarter-tone space |

There are **8 subgroups** (compared to 6 for Z/12Z). The extra subgroups come from the additional divisors of 24: ⟨3⟩ of order 8 and ⟨4⟩ of order 6 have no analogue in Z/12Z.

**Key observation:** The subgroup ⟨2⟩ = {0, 2, 4, 6, ..., 22} is isomorphic to Z/12Z — this is 12-TET **embedded** in 24-TET. The Arabic system contains the Western system as a subgroup.

The subgroup ⟨3⟩ = {0, 3, 6, 9, 12, 15, 18, 21} is an 8-note scale of minor thirds — the **octatonic** scale, extended to quarter-tone space. This subgroup does NOT exist in Z/12Z (⟨3⟩ in Z/12Z has order 4, giving only the diminished seventh). In Z/24Z, we get a full 8-note scale built from minor thirds.

### 4.2 Maqam Scales: Quarter-Tone Scales That Don't Exist in 12-TET

The fundamental Arabic maqamat (singular: maqam) and their interval structures in 24-TET:

| Maqam | Intervals (in quarter-steps) | Scale degrees (from 24-TET) |
|-------|------------------------------|---------------------------|
| Rast | 4-3-4-4-4-3-4 | {0, 4, 7, 11, 15, 18, 22} |
| Bayati | 3-4-4-4-4-3-4 | {0, 3, 7, 11, 15, 19, 22} |
| Hijaz | 3-5-3-4-4-3-4 | {0, 3, 8, 11, 15, 19, 22} |
| Saba | 3-2-5-4-4-3-3 | {0, 3, 5, 10, 14, 18, 21} |
| Kurd | 2-5-3-4-4-3-4 | {0, 2, 7, 10, 14, 18, 22} |
| Nahawand | 4-3-4-4-3-4-4 | {0, 4, 7, 11, 15, 18, 22} |
| Ajam | 4-3-4-4-3-4-4 | {0, 4, 7, 11, 14, 18, 22} |
| Sikah | 3-4-4-3-4-3-5 | {0, 3, 7, 11, 14, 18, 21} |

**Critical observation:** The intervals include **odd numbers** (3, 5 quarter-steps) that correspond to **quarter tones** — intervals that fall between the cracks of 12-TET. For example:
- Rast starts with 4-3: a major second (200¢) followed by a "neutral third" (~350¢) — this 3-quarter-step interval is 150¢, a quarter tone.
- Hijaz has 3-5-3: a sequence of augmented-second-like intervals (150¢ + 250¢ + 150¢) creating the characteristic "Hijaz gap."

**These scales are NOT subsets of Z/12Z.** They contain elements not in ⟨2⟩ ⊂ Z/24Z. The Arabic maqam system is **irreducibly quarter-tonal** — it cannot be represented in 12-TET without loss of identity.

### 4.3 The Eisenstein Lattice Over Z/24Z

The interval lattice over Z/24Z:

$$\Lambda_{24} = \{(k_1, k_2) \in \mathbb{Z}^2 : k_1 + k_2 \equiv 0 \pmod{24}\}$$

Covering radius in Eisenstein norm:

$$\rho_{A_2}^{(24)} = \frac{\sqrt{24}}{\sqrt{3}} = \frac{2\sqrt{6}}{\sqrt{3}} = 2\sqrt{2} \approx 2.828$$

vs. $\rho_{A_2}^{(12)} \approx 2.000$ — a 41% increase. The interval space is larger, with more possible intervals, including the quarter-tone intervals that define Arabic identity.

The **covering radius on the unit circle** for n equally-spaced points is:

$$\rho_n = \sin(\pi/n)$$

For 24-TET: $\rho_{24} = \sin(\pi/24) \approx 0.131$
For 12-TET: $\rho_{12} = \sin(\pi/12) \approx 0.259$

The ratio $\rho_{24}/\rho_{12} \approx 0.504$, meaning quarter-tone resolution roughly halves the worst-case snap error.

### 4.4 Maqam as a Subset of Z/24Z

Each maqam selects 5–7 notes from the 24 available. In group-theoretic terms, a maqam is a **subset** of Z/24Z (not necessarily a subgroup or coset).

The maqam scales do NOT form subgroups — they're selected subsets. But they often have internal symmetry:

- **Rast** {0, 4, 7, 11, 15, 18, 22} has a near-symmetry: the upper tetrachord (15, 18, 22) + 24/2 = (3, 6, 10) is close to but not equal to the lower tetrachord shifted. The symmetry is approximate, not exact.
- **Hijaz** {0, 3, 8, 11, 15, 19, 22} has the characteristic augmented-second gap (3-5-3) that defines its identity. This gap of 5 quarter-steps (250¢) is larger than any interval in standard Western scales.

---

## 5. Maqam as Lattice Journey

### 5.1 The Sayr: A Prescribed Path Through Lattice Space

A maqam performance is not just a collection of allowed notes — it's a **journey** through specific tonal centers in a prescribed order. The *sayr* (path/journey) defines:

1. **Start:** Root (qarār) — the tonal center
2. **Ascend:** Move upward through specific scale degrees
3. **Upper dominant:** Reach the ghammaz (upper dominant, usually 5th or 4th)
4. **Explore:** Improvise around the ghammaz
5. **Descend:** Return downward through the scale
6. **Resolve:** Return to root (qarār)

**This is literally a PATH through the Eisenstein lattice.** In constraint-theory terms, the sayr is a **trajectory constraint** — not just *which* notes are allowed, but the *order* in which regions of pitch space should be visited.

### 5.2 Formal Sayr Model

Let the maqam scale be $M = \{m_0, m_1, \ldots, m_{k-1}\} \subset \mathbb{Z}/24\mathbb{Z}$ with $m_0 = 0$ (root). The sayr defines an ordering:

$$\text{Sayr} = (R_0, R_1, R_2, \ldots, R_n, \ldots, R_2, R_1, R_0)$$

where each $R_i$ is a **region** of the scale (typically a tetrachord or pentachord). The performance must visit these regions in order:

$$\forall i: \text{visit}(R_i) \text{ before } \text{visit}(R_{i+1})$$

This is a **precedence constraint** in addition to the pitch-class constraint.

**In lattice terms:** The sayr defines a **Hamiltonian path** (or near-Hamiltonian path) through the lattice points corresponding to the maqam's scale degrees. The path has a prescribed shape:
- Ascending arc from root to upper dominant
- Hovering/exploration at upper dominant
- Descending arc back to root

### 5.3 Modulation: Moving Between Maqam

Arabic music allows **modulation** between maqamat during a performance. The modulation rules are:

1. **Modulation to a related maqam:** Two maqamat are related if they share a tetrachord or have overlapping scale degrees. The modulation is smooth — the shared notes form a "bridge."
2. **Modulation up or down by a quarter tone:** Moving the root up or down by one step in Z/24Z. This is the Arabic equivalent of a half-step modulation in Western music, but at the quarter-tone level.
3. **Return:** After modulating, the performer must eventually return to the original maqam (unless transitioning to a new section).

**In group-theoretic terms,** a modulation from maqam $M_1$ to maqam $M_2$ is a **coset shift** in Z/24Z:

$$M_2 = M_1 + t \quad \text{for some transposition } t \in \mathbb{Z}/24\mathbb{Z}$$

The smoothest modulations minimize $|t|$ (small transposition = close key relationship). Quarter-tone modulations ($|t| = 1$) are the Arabic equivalent of the Western half-step shift — a small but significant color change.

### 5.4 The Maqam Journey as Constraint Satisfaction

The entire maqam performance can be modeled as a **constraint satisfaction problem (CSP):**

- **Variables:** Pitch at each time step $p(t) \in \mathbb{Z}/24\mathbb{Z}$
- **Domain:** The maqam scale $M \subset \mathbb{Z}/24\mathbb{Z}$
- **Constraints:**
  1. $p(0) = 0$ (start on root)
  2. Sayr ordering: visit regions in prescribed order
  3. Melodic coherence: $|p(t+1) - p(t)| \leq \Delta_{\max}$ (maximum leap)
  4. Gravity: tendency to return to root/qarār
  5. If modulation occurs: bridge constraint (shared notes)
  6. Return to root before ending

This is our constraint-theory framework **applied to melodic trajectories** rather than just pitch classes.

---

## 6. Taqsim — Improvisation Without Clock

### 6.1 Free Rhythm: ε = ∞

A taqsim is an **unmetered improvisation** in a maqam. There is no tala, no meter, no regular beat grid. In our deadband funnel model:

$$\text{Deadband temporal width} = \epsilon_t = \infty$$

The funnel has **no temporal constraint** — pitch is free to move at any speed, to pause for any duration, to rush forward or linger. The ONLY constraints are:
1. **Harmonic:** Stay within the maqam (or modulate following rules)
2. **Sayr:** Follow the prescribed tonal journey
3. **Aesthetic:** Maintain musical coherence

**What does the funnel look like with ε = ∞?**

The funnel collapses from a 2D structure (pitch × time) to a 1D structure (pitch only). The time axis disappears — there's no "deadline" to hit any particular pitch at any particular time. The only remaining structure is the **pitch ladder**:

```
Maqam pitch ladder (1D constraint):

    [Ghammaz] ---- target region
         |
         |  (free wandering within scale)
         |
    [Root] ---- target region
```

The performer navigates this ladder at their own pace. There's no clock — only the pitch constraint and the sayr ordering.

### 6.2 Free Rhythm in Deadband Terms

In the standard deadband model:

$$\text{Funnel}(t) = \{(p, \tau) : |p - p_{\text{target}}| < \epsilon_p(t), |\tau - \tau_{\text{target}}| < \epsilon_\tau(t)\}$$

For taqsim, $\epsilon_\tau(t) = \infty$ always. The funnel is:

$$\text{Funnel}_{\text{taqsim}}(t) = \{(p, \tau) : |p - p_{\text{target}}| < \epsilon_p(t)\}$$

This is a **vertical strip** in (pitch, time) space — infinite extent in time, bounded only in pitch. The performer is free to take as long as they want to reach any pitch target.

**The pitch constraint remains tight.** Even without temporal constraints, the maqam rules are strict — you can't play notes outside the scale, you can't skip the sayr ordering, you can't avoid the root. The constraint is purely **harmonic/spatial** with no temporal component.

### 6.3 Rubato as Variable ε

Western rubato (expressive timing) is a **finite** stretching of ε — the temporal deadband is wider than strict tempo but not infinite. Taqsim is the **limit** of rubato as ε → ∞.

This suggests a **spectrum of temporal freedom:**

| Mode | ε_τ | Musical practice |
|------|-----|-----------------|
| Strict tempo | ~50ms | Metronomic, dance music |
| Rubato | ~200-500ms | Classical Western, expressive |
| Free meter | ~1-5s | Chant, recitative |
| Taqsim | ∞ | Arabic unmetered improvisation |
| Alap | ∞ | Indian unmetered improvisation |

Both Indian alap (unmetered opening of raga performance) and Arabic taqsim operate at ε_τ = ∞ — they are the **same mathematical object** (unmetered pitch-constraint navigation) in different traditions.

---

## 7. Cross-Cultural Synthesis — The Universal Lattice

### 7.1 The Naïve Approach: LCM

The minimum cyclic group containing all traditions as subgroups:

$$n_{\min} = \text{lcm}(12, 22, 24, 53, 7, 5)$$

Let us compute:
- lcm(12, 24) = 24
- lcm(24, 22) = lcm(24, 2·11) = lcm(24, 22) = 24·11/gcd(24,22) = 24·11/2 = 132
- lcm(132, 53) = 132·53/gcd(132,53) = 132·53 = 6996 (53 is prime)
- lcm(6996, 7) = 6996·7/gcd(6996,7) = 6996·7 = 48972 (7 is prime)
- lcm(48972, 5) = 48972·5/gcd(48972,5) = 48972·5 = 244860 (5 is prime)

Wait, but gcd(24, 22) = 2, and we already accounted for that. Let me redo:

- 12 = 2² × 3
- 22 = 2 × 11
- 24 = 2³ × 3
- 53 = 53
- 7 = 7
- 5 = 5

LCM = 2³ × 3 × 5 × 7 × 11 × 53 = 8 × 3 × 5 × 7 × 11 × 53

= 8 × 3 = 24
× 5 = 120
× 7 = 840
× 11 = 9240
× 53 = **489,720**

Not 15960 as initially guessed — the 53 factor nearly doubles it. Z/489720Z is **absurd** as a practical music representation.

### 7.2 The Non-Uniform Alternative

The problem with the LCM approach is that it treats all traditions as **equal subdivisions** of the same circle. But traditions don't need the SAME grid — they need a grid that can **reproduce their distinctive intervals.**

The key insight: most traditions agree on the **perfect fifth** (ratio 3/2) and **octave** (ratio 2/1) as fundamental. They diverge on:
- How to divide the whole tone (2-TET? 4-TET? 9-TET?)
- Whether to allow quarter tones
- How to handle the Pythagorean comma

**A non-uniform universal lattice** could be built on the following principles:

1. **Common anchor points:** All traditions share the octave, fifth, and fourth
2. **Variable-density regions:** Dense around consonances, sparse around dissonances
3. **Tradition-specific overlays:** Each tradition adds its own fine structure

### 7.3 The Pythagorean Backbone

All five traditions are ultimately derived from the **Pythagorean spiral** — stacking perfect fifths (ratio 3/2) and reducing modulo octaves:

$$f_n = f_0 \cdot \left(\frac{3}{2}\right)^n \cdot 2^{-\lfloor n \cdot \log_2(3/2) \rfloor}$$

The spiral generates the following pitch sequence (in cents from root):
0, 702, 204, 906, 408, 1110, 612, 114, 816, 318, 1020, 522, 24, ...

This is the **universal backbone** — all traditions use it as a starting point and then diverge:
- **Western 12-TET:** Quantizes to 12 equal divisions (closes the spiral by distributing the comma evenly)
- **Chinese 12-lü:** Uses the raw Pythagorean spiral (12 fifths) without tempering
- **Indian 22-śruti:** Adds just-intonation microtones between the Pythagorean tones
- **Arabic 24-TET:** Subdivides each Pythagorean whole tone into quarters
- **Turkish 53-TET:** Uses 53 divisions (which gives an excellent approximation to the pure fifth: 31/53 ≈ 0.5849 vs 3/2 ratio ≈ 0.5850)

**The minimum group that captures all these Pythagorean-derived systems is determined by the resolution of the finest system (53-TET).** But we don't need all 53 steps — we need only the steps that correspond to intervals used in any tradition.

### 7.4 A Practical Universal Lattice: The 15960-Subgroup Tower

Instead of using the full LCM group, we can build a **tower of embeddings:**

```
Z/5Z  (slendro) 
  ↪ Z/7Z  (pelog, Thai)
    ↪ Z/12Z  (Western, Chinese)
      ↪ Z/22Z  (Indian śruti)
        ↪ Z/24Z  (Arabic quarter-tone)
          ↪ Z/53Z  (Turkish comma)
```

Each embedding is a **group homomorphism** Z/mZ → Z/nZ (for m | n or via CRT). The tower preserves the structure of each level while allowing communication between levels.

**But the embeddings don't all exist as subgroup relationships.** For example:
- 22 ∤ 24, so Z/22Z is NOT a subgroup of Z/24Z
- 12 ∤ 22, so Z/12Z is NOT a subgroup of Z/22Z
- 12 | 24, so Z/12Z IS a subgroup of Z/24Z ✓
- 53 is prime, so Z/53Z has no nontrivial subgroups

The only clean subgroup chains are:
- Z/5Z → Z/10Z → Z/20Z → Z/40Z → ... (multiples of 5)
- Z/7Z → Z/14Z → Z/28Z → Z/56Z → ... (multiples of 7)
- Z/12Z → Z/24Z (doubles, capturing Western → Arabic)
- Z/53Z (isolated)

**The traditions don't form a clean nested hierarchy.** They're partially overlapping circles of resolution.

### 7.5 The Fibre Bundle Model

A more elegant approach: treat the **universal pitch space** as a **fibre bundle:**

$$E = B \times F$$

where:
- **Base space** $B$ = the 12-tone chromatic (shared by Western, Chinese, Arabic's 12-tone subset)
- **Fibre** $F_n$ = the microtonal refinement specific to each tradition:
  - Western: $F_W = \{0\}$ (no refinement — the base IS the full pitch space)
  - Indian: $F_I = \{0, 1\}$ or $\{0, 1, 2\}$ (1–2 śruti per semitone)
  - Arabic: $F_A = \{0, 1\}$ (one quarter tone per semitone)
  - Turkish: $F_T = \{0, 1, 2, 3, 4\}$ (approximately 53/12 ≈ 4.4 divisions per semitone)

The total pitch space for each tradition is $B \times F_n$, which has the right cardinality:
- Western: 12 × 1 = 12 ✓
- Indian: 12 × ~2 = ~24 (close to 22) ✓
- Arabic: 12 × 2 = 24 ✓
- Turkish: 12 × ~4.4 = ~53 ✓

This model captures the intuition that **all traditions agree on the coarse structure** (the 12-semitone backbone) but diverge on the fine structure (how many divisions within each semitone).

**The covering radius of the fibre bundle model:**

$$\rho_{\text{bundle}} = \sqrt{\rho_B^2 + \rho_F^2}$$

where $\rho_B = \sin(\pi/12) \approx 0.259$ (covering radius of 12-TET on unit circle) and $\rho_F$ depends on the tradition:

| Tradition | $\rho_F$ | $\rho_{\text{bundle}}$ |
|-----------|---------|----------------------|
| Western | 0 (no fibre) | 0.259 |
| Arabic (24) | $\sin(\pi/2) = 1$ | ~1.03 |
| Turkish (53) | $\sin(\pi/\lfloor53/12\rfloor)$ | varies |

The base space dominates the covering radius! **Microtonal refinement doesn't significantly improve the worst-case snap error** — it only improves the *local* precision within each semitone bin. This matches the perceptual reality: listeners primarily perceive pitch at the semitone level, with microtonal differences as secondary coloration.

### 7.6 Indonesian Gamelan: The Outliers

Javanese and Balinese gamelan use two scale systems:
- **Slendro:** 5 roughly equal divisions of the octave (Z/5Z)
- **Pelog:** 7 unequal divisions (no clean group structure — the intervals are non-uniform)

Slendro maps to Z/5Z with generator 1, giving a 5-cycle. Its covering radius:

$$\rho_5 = \sin(\pi/5) \approx 0.588$$

This is the **largest covering radius** of any tradition we've examined — gamelan has the "loosest" pitch snap, which matches the ethnomusicological observation that gamelan tuning is highly variable between ensembles. The "same" slendro can differ by 30-50 cents between orchestras.

Pelog is harder to model because the intervals are non-uniform (roughly 120, 120, 150, 250, 120, 150, 250 cents). It's not well-described by any cyclic group — it's closer to a **custom subset** of Z/12Z or Z/24Z.

---

## 8. The Grand Synthesis — UniversalMusicTile

### 8.1 Specification

Drawing on all three traditions (Western, Chinese, Indian, Arabic) and the mathematical analysis above, we define a **UniversalMusicTile** that can represent ANY musical tradition:

```python
@dataclass
class UniversalMusicTile:
    # === Lattice Structure ===
    lattice_group: str           # "Z12", "Z22", "Z24", "Z53", "Z5", "Z7", "custom"
    lattice_size: int            # n for Z/nZ
    
    # === Scale Selection ===
    scale_coset: List[int]       # Which elements of Z/nZ are "in the scale"
    scale_name: str              # "major", "Bhairav", "Rast", "gōng-diào", etc.
    
    # === Asymmetry ===
    ascending_set: List[int]     # S↑ — notes allowed when ascending
    descending_set: List[int]    # S↓ — notes allowed when descending
    # If symmetric: ascending_set == descending_set
    
    # === Attractor Structure ===
    primary_attractor: int       # Vādī / root / tonic
    secondary_attractor: int     # Saṃvādī / dominant
    attractor_weights: Tuple[float, float]  # (w_primary, w_secondary)
    forbidden_notes: List[int]   # Vivādī / excluded pitches
    
    # === Ornamentation ===
    ornament_function: str       # "discrete", "continuous", "gamaka"
    ornament_params: Dict[int, Tuple[float, float]]  # note_id -> (amplitude, frequency)
    # For discrete: amplitude = 0 for all notes
    # For gamaka: amplitude and frequency per note
    
    # === Environmental Constraints ===
    time_of_day: Optional[Tuple[int, int]]  # (start_hour, end_hour) or None
    season: Optional[str]        # "spring", "summer", etc. or None
    context: Optional[str]       # "concert", "ritual", "dance", etc. or None
    
    # === Emotional State ===
    emotional_rasa: str          # "śṛṅgāra", "karuṇa", "vīra", etc.
    flux_vector_target: Tuple[float, float, float, float]
    # (rate, energy, direction, coherence)
    
    # === Rhythmic Structure ===
    rhythmic_cycle: Optional[List[int]]  # [4,4,4,4] for teental, [3,2,2] for rupak, None for free
    rhythmic_hierarchy: Optional[str]    # "isochronous", "non-isochronous", "free"
    total_beats: Optional[int]          # Sum of rhythmic_cycle, or None
    
    # === Tonal Journey ===
    journey_regions: Optional[List[List[int]]]  # Ordered regions to visit (sayr)
    modulation_targets: Optional[List[int]]     # Valid transpositions for modulation
    
    # === Identity ===
    tradition: str               # "western", "chinese", "indian", "arabic", "turkish", "gamelan"
    parent_scale: Optional[str]  # Thāṭ / maqam family / mode
    
    # === Snap Configuration ===
    snap_mode: str               # "point" (discrete) or "tube" (gamaka)
    snap_deadband: float         # Covering radius for snap
    temporal_freedom: float      # ε_τ: ∞ for alap/taqsim, small for strict tempo
```

### 8.2 Example Instantiations

#### Western Major Scale
```python
UniversalMusicTile(
    lattice_group="Z12",
    lattice_size=12,
    scale_coset=[0, 2, 4, 5, 7, 9, 11],
    scale_name="C major",
    ascending_set=[0, 2, 4, 5, 7, 9, 11],
    descending_set=[0, 2, 4, 5, 7, 9, 11],
    primary_attractor=0,
    secondary_attractor=7,
    attractor_weights=(1.0, 0.6),
    forbidden_notes=[1, 3, 6, 8, 10],
    ornament_function="discrete",
    ornament_params={},
    time_of_day=None,
    season=None,
    context=None,
    emotional_rasa="",
    flux_vector_target=(0.5, 0.5, 0.0, 0.8),
    rhythmic_cycle=[4, 4],  # 4/4 time
    rhythmic_hierarchy="isochronous",
    total_beats=4,
    journey_regions=None,  # No prescribed sayr
    modulation_targets=[2, 5, 7, 9, 10],  # Circle of fifths
    tradition="western",
    parent_scale="major",
    snap_mode="point",
    snap_deadband=0.259,  # sin(π/12) — 12-TET covering radius
    temporal_freedom=0.05,
)
```

#### Raga Bhairav (Indian, Dawn)
```python
UniversalMusicTile(
    lattice_group="Z22",
    lattice_size=22,
    scale_coset=[0, 2, 5, 9, 13, 15, 19],  # śuddha + komal Re, komal Dha
    scale_name="Bhairav",
    ascending_set=[0, 2, 5, 9, 13, 15, 19],
    descending_set=[0, 2, 5, 9, 13, 15, 19],
    primary_attractor=0,      # Sa
    secondary_attractor=13,   # Pa (śruti position for Pa)
    attractor_weights=(1.0, 0.7),
    forbidden_notes=[...],    # Depends on specific mapping
    ornament_function="gamaka",
    ornament_params={
        0: (0.0, 0.0),        # Sa: straight (drone)
        2: (3.0, 6.0),        # Re: heavy gamaka
        5: (2.0, 5.5),        # Ga: moderate gamaka
        13: (0.5, 4.0),       # Pa: light gamaka
    },
    time_of_day=(6, 9),       # Dawn raga
    season=None,
    context="morning meditation",
    emotional_rasa="śānta",   # Peace / devotional
    flux_vector_target=(0.3, 0.3, 0.0, 0.9),
    rhythmic_cycle=None,      # Alap section: free rhythm
    rhythmic_hierarchy="free",
    total_beats=None,
    journey_regions=[[0, 2, 5], [5, 9, 13], [13, 15, 19], [13, 9, 5], [0]],
    modulation_targets=None,  # No modulation in raga
    tradition="indian",
    parent_scale="Bhairav thāṭ",
    snap_mode="tube",         # Gamaka snap to regions, not points
    snap_deadband=0.510,
    temporal_freedom=float('inf'),  # Alap: no temporal constraint
)
```

#### Maqam Rast (Arabic)
```python
UniversalMusicTile(
    lattice_group="Z24",
    lattice_size=24,
    scale_coset=[0, 4, 7, 11, 15, 18, 22],
    scale_name="Rast",
    ascending_set=[0, 4, 7, 11, 15, 18, 22],
    descending_set=[0, 4, 7, 11, 15, 18, 22],
    primary_attractor=0,
    secondary_attractor=15,   # Ghammaz (5th degree)
    attractor_weights=(1.0, 0.7),
    forbidden_notes=[i for i in range(24) if i not in [0,4,7,11,15,18,22]],
    ornament_function="continuous",  # Arabic ornaments but less heavy than gamaka
    ornament_params={
        4: (1.5, 5.0),         # Neutral third with light shake
        7: (1.0, 4.0),         # Quarter-tone ornamentation
    },
    time_of_day=None,
    season=None,
    context=None,
    emotional_rasa="",
    flux_vector_target=(0.5, 0.5, 0.0, 0.7),
    rhythmic_cycle=[4, 4],     # Maqsum rhythm
    rhythmic_hierarchy="isochronous",
    total_beats=8,
    journey_regions=[[0, 4, 7], [7, 11, 15], [15, 18, 22], [15, 11, 7], [0]],
    modulation_targets=[4, 7, 11],  # Related maqamat
    tradition="arabic",
    parent_scale="Rast family",
    snap_mode="point",
    snap_deadband=0.131,  # sin(π/24) — 24-TET covering radius
    temporal_freedom=0.1,
)
```

### 8.3 The Universal Snap Algorithm

The generalized snap algorithm for a UniversalMusicTile:

```python
def universal_snap(pitch: float, direction: int, tile: UniversalMusicTile) -> float:
    """
    Snap a pitch to the nearest valid note, considering:
    - Direction-dependent scale (asymmetric raga)
    - Ornament function (discrete vs continuous)
    - Forbidden notes (vivādī)
    """
    # 1. Determine valid snap targets based on direction
    if direction > 0:
        targets = tile.ascending_set
    elif direction < 0:
        targets = tile.descending_set
    else:
        targets = set(tile.ascending_set) & set(tile.descending_set)
    
    # 2. Remove forbidden notes
    targets = [t for t in targets if t not in tile.forbidden_notes]
    
    # 3. Find nearest target
    nearest = min(targets, key=lambda t: abs(pitch - t))
    distance = abs(pitch - nearest)
    
    # 4. Apply snap mode
    if tile.snap_mode == "point":
        # Western/Arabic: snap to exact point
        return float(nearest)
    
    elif tile.snap_mode == "tube":
        # Indian: snap to tubular neighborhood with gamaka
        amp, freq = tile.ornament_params.get(nearest, (0.0, 0.0))
        if distance < tile.snap_deadband:
            # Within snap range: apply gamaka oscillation
            return nearest + amp * math.sin(2 * math.pi * freq * time.time())
        else:
            # Outside snap range: move toward nearest
            return pitch + (nearest - pitch) * 0.5
    
    elif tile.snap_mode == "continuous":
        # Arabic: snap with light ornamentation
        amp, freq = tile.ornament_params.get(nearest, (0.0, 0.0))
        return nearest + amp * math.sin(2 * math.pi * freq * time.time())
```

### 8.4 Covering Radius Hierarchy

The covering radii for all examined traditions:

| Tradition | Group | n | ρ = sin(π/n) | ρ(A₂ interval lattice) |
|-----------|-------|---|-----------------|----------------------|
| Gamelan slendro | Z/5Z | 5 | 0.588 | 1.291 |
| Gamelan pelog | ~Z/7Z | 7 | 0.434 | 1.528 |
| Chinese pentatonic | Z/5Z→Z/12Z | 5-of-12 | 0.588* | 2.000 |
| Western diatonic | Z/12Z | 7-of-12 | 0.434* | 2.000 |
| Western chromatic | Z/12Z | 12 | 0.259 | 2.000 |
| Indian 22-śruti | Z/22Z | 22 | 0.143 | 2.714 |
| Arabic 24-TET | Z/24Z | 24 | 0.131 | 2.828 |
| Turkish 53-TET | Z/53Z | 53 | 0.059 | 4.203 |

\* Effective covering radius for a subset, not full lattice

**The fundamental tradeoff:**
- **More tones → better pitch resolution** (ρ = sin(π/n) → 0 as n → ∞)
- **More tones → worse interval resolution** (ρ(A₂) → ∞)
- **More tones → more information per note** (log₂(n) bits)
- **More tones → more possible intervals** (n(n-1)/2 choices)

The optimal point depends on perceptual constraints. Human pitch discrimination is ~10 cents for trained musicians, suggesting an ideal n ≈ 120 cents / 10 cents = 12, with marginal benefit up to n ≈ 53 (22.6 cent resolution). Beyond 53-TET, perceptual returns diminish rapidly.

---

## 9. References

### Mathematical Music Theory
- Amiot, E. (2016). *Music Through Fourier Space*. Springer.
- Clough, J. & Douthett, J. (1991). "Maximally Even Sets." *Journal of Music Theory*, 35, 93-173.
- Tymoczko, D. (2011). *A Geometry of Music*. Oxford University Press.
- Callender, C., Quinn, I., & Tymoczko, D. (2008). "Generalized Voice-Leading Spaces." *Science*, 320, 346-348.

### Indian Music Theory
- Jairazbhoy, N.A. (1995). *The Rāgs of North Indian Music*. Popular Prakashan.
- Raghavan, V. (1975). "The 22 Śrutis of Indian Music." *Journal of the Indian Musicological Society*.
- Levy, M. (1982). *Intonation in North Indian Music*. Biblia Impex.
- Widdess, R. (1995). *The Rāgas of Early Indian Music*. Clarendon Press.
- Clayton, M. (2000). *Time in Indian Music*. Oxford University Press.

### Arabic Music Theory
- Marcus, S. (2007). "Arab Music Theory in the Modern Period." *The Garland Encyclopedia of World Music*.
- Farhat, H. (2004). *The Dastgāh Concept in Persian Music*. Cambridge University Press.
- Zonis, E. (1973). *Classical Persian Music: An Introduction*. Harvard University Press.
- Touma, H.H. (1996). *The Music of the Arabs*. Amadeus Press.

### Cross-Cultural & Computational
- Sethares, W.A. (2005). *Tuning, Timbre, Spectrum, Scale*. Springer.
- Chalmers, J. (1993). *Divisions of the Tetrachord*. Frog Peak Music.
- Carey, N. & Clampitt, D. (1989). "Aspects of Well-Formed Scales." *Music Theory Spectrum*, 11, 187-206.

---

*This document completes the triptych: Western 12-TET (DEEP-MATH-MUSICAL-STRUCTURE.md), Chinese 五音/十二律 (CHINESE-MUSIC-CONSTRAINT-THEORY.md), and now Indian raga & Arabic maqam. Together, they span the five great musical civilizations and their mathematical structures.*
