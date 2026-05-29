# MULTI-SCALE LAPLACIAN: Conservation Hierarchies and Automatic Scale Detection

**Draft — May 2026**
**Status:** Theoretical framework with concrete predictions

---

## Abstract

The Tension-Graph Laplacian measures conservation at a single scale — the granularity of the state space. But real systems exhibit conservation at multiple, hierarchically nested scales: phonemes form words form sentences form paragraphs; notes form chords form phrases form movements; tokens form statements form functions form modules. This document extends the spectral alignment principle to multiple scales. We define a family of coarsening operators, construct Laplacians at each scale, prove inter-scale conservation bounds, and derive an algorithm for automatic scale detection. The multi-scale framework reveals the *intrinsic hierarchy* of any system with dynamics and attributes — without prior knowledge of its structure. We present concrete predictions for music (phrase structure recovery), code (function boundary detection), and Mixture-of-Experts (expert cluster discovery), and prove that "deep conservation" — conservation across all scales simultaneously — is equivalent to the system being a nested hierarchy of coherent structures.

---

## 1. Motivation: The Single-Scale Blindspot

### 1.1 What We Miss at One Scale

The single-scale Tension-Graph Laplacian $L = D - W$ with $W_{ij} = P(i \to j) \cdot K(i,j)$ decomposes a system into aligned and misaligned modes. It tells us *whether* the dynamics respect the attribute geometry. But it cannot tell us *at what scale* this alignment operates.

Consider a simple music example. A 12-bar blues progression in C:

$$C_7 \to F_7 \to C_7 \to C_7 \to F_7 \to F_7 \to C_7 \to C_7 \to G_7 \to F_7 \to C_7 \to G_7$$

At the note-scale, the Tension-Graph Laplacian sees individual chord transitions. It detects that $C_7 \to F_7$ (up a fourth) is a low-tension move, while $C_7 \to G_7$ (dominant) has higher tension. The conservation ratio is moderate.

But there's *more* structure at higher scales:

| Scale | What's happening | Conservation signal |
|-------|-----------------|-------------------|
| Note (1 chord) | $C_7 \to F_7 \to C_7 \ldots$ | Weak-moderate |
| Bar (1-2 chords) | I-IV-I-I-IV-IV-I-I-V-IV-I-V | Strong — the harmonic rhythm is conserved |
| Phrase (4 bars) | Tonic-Subdominant-Tonic-Dominant | Very strong — the arc repeats |
| Section (12 bars) | Full blues cycle | Perfect — the cycle is exactly conserved |

A single-scale Laplacian at note resolution *averages* these into a single CR value. It misses the hierarchy.

### 1.2 What Multi-Scale Reveals

The multi-scale Laplacian will:

1. **Automatically recover** the 4-bar phrase structure and 12-bar section structure from raw note transitions
2. **Quantify** conservation at each scale separately
3. **Detect** the *scale hierarchy* as the set of scales where conservation is locally maximized
4. **Prove** that scales are coupled: conservation at fine scales constrains conservation at coarse scales

This transforms the Laplacian from a flat measure into a *spectral microscope* — we can zoom in and out, examining structure at every resolution simultaneously.

---

## 2. Mathematical Framework

### 2.1 Notation and Setup

Let $X = \{x_1, \ldots, x_n\}$ be a finite set of **states** with:
- A **transition matrix** $P \in \mathbb{R}^{n \times n}$, where $P_{ij} = \Pr(x_i \to x_j)$, satisfying $\sum_j P_{ij} = 1$
- An **attribute function** $a: X \to \mathbb{R}^d$, where $a(x_i)$ is the attribute vector (tension, entropy, embedding, etc.)
- An **attribute kernel** $K \in \mathbb{R}^{n \times n}$, where $K_{ij} = \kappa(a(x_i), a(x_j))$ for some similarity function $\kappa$ (e.g., $\kappa(u,v) = e^{-\|u-v\|^2 / \sigma^2}$)

The single-scale Tension-Graph Laplacian is:

$$W = P \odot K \quad \text{(element-wise product)}$$
$$D = \operatorname{diag}(W \mathbf{1})$$
$$L = D - W$$

with conservation ratio $\operatorname{CR}(k) = \frac{\langle \phi_k, L \phi_k \rangle}{\langle \phi_k, \phi_k \rangle}$ where $\phi_k$ is the $k$-th eigenvector of $L$ or equivalently of the dynamics-transition matrix.

### 2.2 Coarsening Operators

**Definition 2.1 (Partition).** A *coarsening* of $X$ at scale $i$ is a partition $\mathcal{P}_i = \{C_{i,1}, \ldots, C_{i,m_i}\}$ of $X$ into $m_i$ disjoint clusters, where each cluster $C_{i,j} \subseteq X$ and $\bigcup_j C_{i,j} = X$.

**Definition 2.2 (Scale Hierarchy).** A *scale hierarchy* is a sequence of partitions $\mathcal{P}_1, \mathcal{P}_2, \ldots, \mathcal{P}_S$ such that $\mathcal{P}_{i+1}$ is a *refinement* of $\mathcal{P}_i$: every cluster in $\mathcal{P}_i$ is a union of clusters in $\mathcal{P}_{i+1}$. Equivalently, $\mathcal{P}_{i+1}$ is obtained by merging clusters of $\mathcal{P}_i$.

**Definition 2.3 (Coarsening Operator).** For a partition $\mathcal{P}_i$ with $m_i$ clusters, the *coarsening operator* $C_i \in \mathbb{R}^{m_i \times n}$ maps fine-grained states to coarse clusters:

$$(C_i)_{k,\ell} = \begin{cases} 1 & \text{if } x_\ell \in C_{i,k} \\ 0 & \text{otherwise} \end{cases}$$

The *normalized coarsening operator* is $\tilde{C}_i = \operatorname{diag}(n_1^{-1}, \ldots, n_{m_i}^{-1}) C_i$ where $n_k = |C_{i,k}|$, giving row-stochastic maps that average within each cluster.

### 2.3 Constructing Partitions

The partitions $\mathcal{P}_i$ must be constructed from the data. We consider three approaches:

**Approach 1: Attribute-Based (A-priori).** Cluster states by attribute similarity using $K$-means, spectral clustering, or DBSCAN on the attribute vectors $a(x_i)$. This gives partitions based purely on geometry, independent of dynamics.

**Approach 2: Dynamics-Based (A-posteriori).** Cluster states by transition similarity using the eigenvectors of $L$ (spectral clustering on the Laplacian). This gives partitions based on how the dynamics actually organize the state space.

**Approach 3: Joint (Recommended).** Use the leading eigenvectors of $L$ to define a *spectral embedding* of the state space, then hierarchically cluster in this embedding. This respects both dynamics and geometry simultaneously.

**Definition 2.4 (Hierarchical Spectral Clustering).** Given the single-scale Laplacian $L$ with eigenvectors $\phi_1, \ldots, \phi_n$, define the spectral embedding:

$$y_i = (\phi_1(x_i), \phi_2(x_i), \ldots, \phi_k(x_i)) \in \mathbb{R}^k$$

where $\phi_j(x_i)$ is the $i$-th component of the $j$-th eigenvector. Apply agglomerative hierarchical clustering to $\{y_i\}$ using Ward's method. The partitions $\mathcal{P}_1, \ldots, \mathcal{P}_S$ are the dendrogram levels at $S$ selected cut points.

### 2.4 Multi-Scale Laplacians

**Definition 2.5 (Coarsened Transition Matrix).** At scale $i$, the coarsened transition matrix $P^{(i)} \in \mathbb{R}^{m_i \times m_i}$ is:

$$P^{(i)} = C_i P \tilde{C}_i^T$$

where $C_i$ is the coarsening operator and $\tilde{C}_i$ is its normalized version. Component-wise:

$$P^{(i)}_{ab} = \frac{1}{|C_{i,a}|} \sum_{x_\ell \in C_{i,a}} \sum_{x_j \in C_{i,b}} P_{\ell j}$$

This is the average transition probability from cluster $a$ to cluster $b$.

**Definition 2.6 (Coarsened Attribute Kernel).** At scale $i$, let $\bar{a}^{(i)}_k$ be the average attribute of cluster $C_{i,k}$:

$$\bar{a}^{(i)}_k = \frac{1}{|C_{i,k}|} \sum_{x_j \in C_{i,k}} a(x_j)$$

The coarsened kernel $K^{(i)} \in \mathbb{R}^{m_i \times m_i}$ is:

$$K^{(i)}_{ab} = \kappa(\bar{a}^{(i)}_a, \bar{a}^{(i)}_b)$$

**Definition 2.7 (Scale-i Laplacian).** At scale $i$, the multi-scale Tension-Graph Laplacian is:

$$W^{(i)} = P^{(i)} \odot K^{(i)}$$
$$D^{(i)} = \operatorname{diag}(W^{(i)} \mathbf{1})$$
$$L^{(i)} = D^{(i)} - W^{(i)}$$

**Definition 2.8 (Scale-i Conservation Ratio).** For the $k$-th eigenvector $\phi^{(i)}_k$ of $L^{(i)}$:

$$\operatorname{CR}_i(k) = \frac{\langle \phi^{(i)}_k, L^{(i)} \phi^{(i)}_k \rangle}{\langle \phi^{(i)}_k, \phi^{(i)}_k \rangle}$$

And the *aggregate* conservation at scale $i$ is:

$$\overline{\operatorname{CR}}_i = \frac{1}{K} \sum_{k=1}^K \operatorname{CR}_i(k)$$

for some small $K$ (typically $K = 3$ or $K = 5$).

---

## 3. Deep Conservation

### 3.1 Definition

**Definition 3.1 (Deep Conservation).** A system exhibits *deep conservation* of attribute $a$ with threshold $\varepsilon$ if:

$$\forall i \in \{1, \ldots, S\}, \forall k \in \{1, \ldots, K\}: \operatorname{CR}_i(k) < \varepsilon$$

That is, conservation holds at *every* scale simultaneously.

This is strictly stronger than single-scale conservation. A system might conserve tension at the note level (smooth chord transitions) but break it at the phrase level (abrupt modulations). Deep conservation requires coherence at all resolutions.

**Proposition 3.1 (Deep Conservation Implies Single-Scale).** If the fine scale $i=1$ is the original state space ($m_1 = n$), then deep conservation at scale 1 implies single-scale conservation. The converse is false: single-scale conservation does not imply deep conservation.

*Proof sketch.* Scale 1 with $m_1 = n$ is the original Laplacian $L$. Deep conservation includes this scale. For the converse, construct a system with smooth micro-transitions but abrupt macro-structure (e.g., a Markov chain that moves smoothly within each of two disjoint clusters but jumps randomly between them). The micro scale conserves; the macro scale does not. $\square$

### 3.2 The Deep Conservation Theorem

**Theorem 3.1 (Deep Conservation ⇔ Nested Hierarchy).** For a stationary Markov chain with attribute $a$, deep conservation (with threshold $\varepsilon \to 0$) is equivalent to the state space being a *nested hierarchy of coherent structures*, defined as:

1. The state space partitions into clusters $\mathcal{P}_1$ where within-cluster transitions conserve $a$
2. Each cluster in $\mathcal{P}_i$ partitions into subclusters $\mathcal{P}_{i+1}$ where within-subcluster transitions conserve $a$  
3. This nesting extends to the finest granularity

*Proof sketch.* ($\Rightarrow$) Deep conservation at scale $i$ means $L^{(i)}$ has near-zero spectral gap, implying the coarsened transition matrix $P^{(i)}$ is approximately a block matrix with near-constant attributes within blocks. The blocks of $P^{(i)}$ are the clusters of $\mathcal{P}_i$. Deep conservation at scale $i+1$ further partitions each block. By induction, this gives a nested hierarchy.

($\Leftarrow$) Given a nested hierarchy, at each level $i$, the transitions within each $\mathcal{P}_i$ cluster are approximately stationary within a region of constant attribute. The coarsened Laplacian $L^{(i)}$ then has eigenvectors close to the indicator vectors of clusters (by the Cheeger inequality for the quotient graph), and attribute variation along these eigenvectors is small by construction, giving low $\operatorname{CR}_i(k)$. $\square$

### 3.3 Empirical Consequences

Deep conservation is a *very* strong condition. In practice, most real systems exhibit:

1. **Shallow conservation**: conservation at 1-2 scales only
2. **Hierarchical conservation**: conservation at well-separated scales, with gaps in between
3. **Deep conservation**: all scales, extremely rare

We predict:

| System type | Depth | Expected pattern |
|-------------|-------|-----------------|
| Well-composed tonal music | 3-4 scales | Notes → beats → phrases → sections |
| Well-structured code | 3-5 scales | Tokens → statements → functions → modules → packages |
| Natural language | 2-3 scales | Words → sentences → paragraphs |
| Random walk on a graph | 0-1 scales | Single scale at best |
| Protein folding | 2-3 scales | Residues → secondary structure → domains |
| MoE routing (good) | 2-3 scales | Tokens → expert groups → layers |

---

## 4. Inter-Scale Coupling: The Conservation Cascade

### 4.1 How Coarsening Transfers Conservation

Deep conservation is not just a conjunction — the scales are coupled. Conservation at a fine scale *constrains* what's possible at coarser scales.

**Theorem 4.1 (Conservation Cascade Bound).** Let $\operatorname{CR}_i(k)$ be the conservation ratio at scale $i$ in the $k$-th eigenmode. Then for any coarsening from scale $i$ to scale $i+1$ (where each cluster at scale $i+1$ merges at most $M$ clusters from scale $i$):

$$\operatorname{CR}_{i+1}(1) \leq M \cdot \max_{k \leq M} \operatorname{CR}_i(k) + \mathcal{O}(\delta_{\text{merge}})$$

where $\delta_{\text{merge}}$ measures the attribute variation *between* merged clusters:

$$\delta_{\text{merge}} = \max_{a,b \text{ merged}} \|\bar{a}^{(i)}_a - \bar{a}^{(i)}_b\|$$

*Proof sketch.* Consider a coarse eigenvector $\phi$ at scale $i+1$. Lift it to scale $i$ by assigning the same value to all fine states within each coarse cluster. This lifted vector is a piecewise-constant approximation at scale $i$. Its Rayleigh quotient on $L^{(i)}$ involves two terms: (1) transitions *within* fine clusters (bounded by $\max_k \operatorname{CR}_i(k)$) and (2) transitions *between* merged clusters (bounded by $\delta_{\text{merge}}$ times a mixing coefficient). The factor $M$ appears because each coarse cluster contains up to $M$ fine clusters, amplifying cross-cluster transitions. The $\mathcal{O}(\delta_{\text{merge}})$ term accounts for attribute mismatch between merged groups.

By the min-max theorem, the smallest eigenvalue of $L^{(i+1)}$ is at most the Rayleigh quotient of any lifted vector, giving the bound. $\square$

### 4.2 The Cascade Function

**Definition 4.1 (Cascade Function).** The *conservation cascade function* $f_{i \to i+1}: \mathbb{R}^+ \to \mathbb{R}^+$ maps the maximum conservation at scale $i$ to an upper bound on conservation at scale $i+1$:

$$f_{i \to i+1}(\varepsilon) = \inf_{\text{coarsenings}} \sup \{\operatorname{CR}_{i+1}(1) : \max_k \operatorname{CR}_i(k) \leq \varepsilon\}$$

where the infimum is over all coarsenings that respect the partition structure.

**Theorem 4.2 (Cascade Function Properties).** The cascade function satisfies:

1. **Monotonicity**: $\varepsilon_1 \leq \varepsilon_2 \implies f(\varepsilon_1) \leq f(\varepsilon_2)$
2. **Sublinearity**: $f(\varepsilon) \leq \alpha \varepsilon + \beta$ for some $\alpha, \beta > 0$ depending on the merging topology
3. **Fixed point**: If $\varepsilon^*$ satisfies $f(\varepsilon^*) < \varepsilon^*$, then scales with conservation $\varepsilon^*$ will have *strictly weaker* conservation at coarser scales — conservation decays upward
4. **Contraction**: If $f(\varepsilon) < \varepsilon$ for all $\varepsilon > 0$, then deep conservation is impossible: conservation always degrades at coarser scales

*Proof sketch.* (1) and (2) follow directly from Theorem 4.1. For (3), the cascade bound means coarse-scale conservation is bounded above by a function of fine-scale conservation. If this function lies below the identity, conservation degrades. For (4), iterating $f$ gives a sequence converging to 0, so any fixed $\varepsilon > 0$ is violated at sufficiently coarse scales. $\square$

### 4.3 Practical Implication: Conservation Decay Length

**Definition 4.2 (Conservation Decay Length).** Given a cascade function $f$, the *conservation decay length* $\ell(\varepsilon_0)$ is the smallest $S$ such that iterating $f$ $S$ times from initial conservation $\varepsilon_0$ yields $\overline{\operatorname{CR}}_S > \varepsilon_{\text{threshold}}$.

This is the number of scales before conservation is lost. For well-structured systems, $\ell$ is large (3-5 scales). For poorly structured systems, $\ell = 1$ (conservation disappears immediately upon coarsening).

**Prediction 4.1.** For a random walk on the 12-tone chromatic scale with uniform transition probabilities, $\ell = 1$: no conservation at any scale. For a well-composed fugue, $\ell \geq 4$: conservation persists from notes through sections.

---

## 5. Automatic Scale Detection

### 5.1 The Conservation Profile

**Definition 5.1 (Conservation Profile).** Let $m$ be the number of clusters at a given scale. The *conservation profile* of a system is the function:

$$\Gamma(m) = \overline{\operatorname{CR}}(m)$$

mapping the number of clusters to the aggregate conservation ratio at that scale (using the optimal partition with $m$ clusters, e.g., from hierarchical spectral clustering).

**Definition 5.2 (Natural Scale).** A *natural scale* of the system is a value $m^*$ where $\Gamma(m)$ has a *local minimum*:

$$\Gamma(m^*) < \Gamma(m^* - \Delta) \quad \text{and} \quad \Gamma(m^*) < \Gamma(m^* + \Delta)$$

for some window $\Delta$ (typically $\Delta = \max(1, m^*/10)$).

### 5.2 Why Local Minima Are Natural Scales

The intuition: as we coarsen the state space (fewer clusters), we lose information. This *increases* the alignment of dynamics with averaged attributes, because averaging smooths out fine-scale mismatches. Conversely, at very fine scales (many clusters), noise dominates and conservation drops.

But *between* these extremes, local minima of $\Gamma(m)$ occur precisely when the partition aligns with the system's intrinsic structure. At these scales:

1. **Transitions within clusters are smooth** (dynamics ≈ geometry within cluster)
2. **Transitions between clusters are disruptive** (dynamics ≠ geometry between clusters)
3. **The boundary between clusters is meaningful** — it corresponds to a "phase transition" in the system

**Proposition 5.1 (Natural Scales Are Structural Transitions).** Local minima of $\Gamma(m)$ correspond to scale boundaries where the spectral embedding changes abruptly — these are the Cheeger cuts of the quotient graph.

*Proof sketch.* At a natural scale $m^*$, the $m^*$ clusters form a partition where each cluster is a "coherent region" — transitions within each cluster are dynamics-geometry aligned, and transitions between clusters are not. This is precisely the condition for the quotient graph's Cheeger cut: the partition minimizes the ratio of inter-cluster to intra-cluster Laplacian energy. The spectral embedding $y_i$ separates into $m^*$ well-separated clusters at this scale. $\square$

### 5.3 The Scale Detection Algorithm

We now present the full algorithm for automatic scale detection.

```
Algorithm: Multi-Scale Conservation Detection
===============================================
Input:  State set X = {x_1, ..., x_n}
        Transition matrix P ∈ ℝ^{n×n}
        Attribute function a: X → ℝ^d
        Kernel function κ: ℝ^d × ℝ^d → ℝ^+
        Parameters: K (top eigenvectors), ε (convergence)

Output: Scale hierarchy {P_1, ..., P_S}
        Conservation profile Γ(m) for m = 1..n
        Natural scales {m*_1, ..., m*_S}


1. BUILD SINGLE-SCALE LAPLACIAN
   ────────────────────────────
   For i,j = 1..n:
     K_ij ← κ(a(x_i), a(x_j))
     W_ij ← P_ij · K_ij
   D ← diag(W · 1_n)
   L ← D - W

2. SPECTRAL EMBEDDING
   ──────────────────
   Compute K smallest eigenvectors of L: φ_1, ..., φ_K
   For i = 1..n:
     y_i ← (φ_1(x_i), ..., φ_K(x_i)) ∈ ℝ^K

3. HIERARCHICAL CLUSTERING
   ────────────────────────
   T ← agglomerative_clustering(y_i, method="ward")
   This gives a dendrogram D with n leaves

4. CONSERVATION PROFILE
   ────────────────────
   For m = n down to 1:        (reverse: coarse to fine)
     P_m ← cut_dendrogram(T, m clusters)
     C_m ← coarsening_operator(P_m)
     
     P_coarse ← C_m · P · C_m^†      (coarsened transition)
     a_bar_k ← mean {a(x_j) : x_j ∈ cluster k}
     K_coarse_ab ← κ(a_bar_a, a_bar_b)
     
     W_coarse ← P_coarse ⊙ K_coarse
     D_coarse ← diag(W_coarse · 1_m)
     L_coarse ← D_coarse - W_coarse
     
     Compute eigenvectors ψ_1, ..., ψ_K of L_coarse
     CR_m(k) ← ⟨ψ_k, L_coarse ψ_k⟩ / ⟨ψ_k, ψ_k⟩
     Γ(m) ← mean(CR_m(k) for k = 1..K)

5. NATURAL SCALE DETECTION
   ────────────────────────
   S ← []
   For m = 2..n-1:
     Δ ← max(1, m/10)
     if is_local_min(Γ, m, Δ):
       S.append(m)
   
   Sort S by Γ(m) (ascending: strongest conservation first)
   
   If len(S) == 0:
     // No natural scales found
     Return: {leaf partition}, Γ, []
   Else:
     // Build partition sequence from natural scales
     P_1 ← cut_dendrogram(T, S[0])    // finest
     P_S ← cut_dendrogram(T, S[-1])   // coarsest
     Return: {P_1, ..., P_S}, Γ, S

6. (OPTIONAL) DEEP CONSERVATION CHECK
   ──────────────────────────────────
   deep ← True
   For each natural scale m* in S:
     if Γ(m*) > threshold:
       deep ← False
   Return: deep_ok ← deep
```

### 5.4 Computational Complexity

- **Step 1**: $O(n^2)$ for full Laplacian construction (sparse approximation: $O(|E|)$ where $|E|$ is the number of nonzero transitions)
- **Step 2**: $O(Kn^2)$ or $O(K|E|)$ for sparse eigen-decomposition (Lanczos/ARPACK)
- **Step 3**: $O(n^2)$ for agglomerative clustering (or $O(n \log n)$ for approximate methods like HDBSCAN)
- **Step 4**: $O(n^2)$ total if we recompute per scale naively; $O(S(n + |E|))$ with incremental updates

**Practical scaling**: For $n = 10^4$ states: ~1 second for sparse Laplacian, ~5 seconds for eigenvectors, ~10 seconds for full profile. For $n = 10^6$, use subsampling or Nyström approximation.

---

## 6. Wavelet Laplacian: Continuous Multi-Scale

### 6.1 Motivation

The partition-based approach above is discrete: it jumps between scales defined by cluster counts. An alternative is to use a *wavelet basis* on the graph, which gives a continuous resolution parameter $s$ (scale).

### 6.2 Graph Wavelets

**Definition 6.1 (Spectral Graph Wavelets).** Following Hammond, Vandergheynst, and Gribonval (2011), define a wavelet operator at scale $s$:

$$T_g^s = g(s L) = U g(s \Lambda) U^T$$

where $L = U \Lambda U^T$ is the eigenvalue decomposition of the single-scale Laplacian, and $g: \mathbb{R}^+ \to \mathbb{R}^+$ is a band-pass filter (e.g., $g(x) = x e^{-x}$).

The wavelet coefficients at scale $s$ for a function $f: X \to \mathbb{R}$ are:

$$\mathcal{W}_s f = T_g^s f$$

### 6.3 Wavelet Conservation

**Definition 6.2 (Wavelet Conservation Ratio).** At wavelet scale $s$, the *wavelet conservation ratio* for attribute $a$ is:

$$\operatorname{CR}_{\text{wav}}(s) = \frac{\|\mathcal{W}_s \nabla a\|^2}{\|\mathcal{W}_s a\|^2}$$

where $\nabla a$ is the gradient of the attribute on the graph (the vector of edge-wise differences).

**Proposition 6.1 (Wavelet Conservation ⇔ Scale Conservation).** For a partition-based coarsening where each cluster has diameter $\sim s$ in the diffusion distance, $\operatorname{CR}_{\text{wav}}(s)$ is approximately proportional to $\overline{\operatorname{CR}}(m(s))$, where $m(s)$ is the number of clusters at scale $s$.

*Proof sketch.* The wavelet operator $g(sL)$ acts as a band-pass filter, amplifying modes with eigenvalues $\lambda \sim 1/s$ and attenuating others. The energy of $\nabla a$ in this band corresponds to attribute variation at scale $s$. The partition-based $\overline{\operatorname{CR}}(m)$ measures the same quantity — attribute variation in the $m$-cluster quotient graph — by the Rayleigh quotient. The conversion between $s$ and $m$ follows from the Weyl law for graph Laplacians: $\lambda \sim 1/s^2$ for $m \sim n^{1/2} s^{-1/2}$ on a 1D graph, with dimension-dependent exponents in general. $\square$

### 6.4 Advantages of the Wavelet Approach

1. **Continuous resolution**: No need to choose discrete scales; examine $\operatorname{CR}_{\text{wav}}(s)$ for all $s > 0$
2. **Natural multi-resolution**: The scaling function $\phi = g(0 L) f$ gives the DC component; wavelets give detail at each scale
3. **Efficient computation**: Using Chebyshev polynomial approximation, $T_g^s f$ can be computed in $O(|E|)$ without full eigen-decomposition
4. **Frame-theoretic guarantees**: The wavelet family forms a frame, enabling perfect reconstruction and energy conservation across scales

**Definition 6.3 (Conservation Spectrum).** The *conservation spectrum* is the function $\operatorname{CR}_{\text{wav}}(s)$ for $s \in (0, s_{\max})$. Its *scale signature* is the set of $s$ where $\operatorname{CR}_{\text{wav}}(s)$ has local minima — these correspond to natural scales.

---

## 7. The Inverse Problem: Scale Detection from Conservation Alone

### 7.1 Motivation

In many real settings, we cannot observe the full transition matrix $P$ or state space $X$. We can only observe a *conservation signal* — a time series of attribute values. Can we infer the scale hierarchy from conservation measurements alone?

### 7.2 Problem Statement

**Definition 7.1 (Conservation Tomography).** Given:
- A time series of attribute values $a(t_1), a(t_2), \ldots, a(t_T)$
- (Optional) A partial observation of transitions
- The ability to compute single-scale CR on any subset of states

Reconstruct the most likely scale hierarchy $\mathcal{P}_1, \ldots, \mathcal{P}_S$ and transition structure $P$ that would produce the observed conservation profile $\Gamma(m)$.

### 7.3 Spectral Signature of Hierarchies

**Theorem 7.1 (Hierarchy Imprints on Conservation Profile).** If a system has $S$ natural scales at cluster counts $m_1^* < m_2^* < \cdots < m_S^*$, then the conservation profile $\Gamma(m)$ has the form:

$$\Gamma(m) = \sum_{i=1}^S \gamma_i \cdot \delta_k(\log m, \log m_i^*) + \Gamma_{\text{noise}}(m)$$

where $\delta_k$ is a kernel function peaked at $\log m_i^*$ (representing the scale transition) and $\gamma_i$ is the conservation depth at scale $i$.

*Proof sketch.* At a natural scale $m_i^*$, the partition aligns with the system's intrinsic structure. Transitions within clusters are smooth; transitions between clusters are disruptive. This makes the coarsened Laplacian $L^{(i)}$ have small eigenvalues (good conservation). At scales *between* natural scales, the partition cuts through coherent structure, mixing smooth and disruptive transitions, degrading conservation. The profile $\Gamma(m)$ therefore has dips at $\log m_i^*$. The kernel width depends on the spectral gap of the quotient graph at each scale. $\square$

### 7.4 Inference Algorithm

```
Algorithm: Conservation Tomography (Sketch)
=============================================
Input:  Attribute time series a(t_1), ..., a(t_T)
        (Optional) Partial transition observations
Output: Estimated scale hierarchy {m*_1, ..., m*_S}

1. For each window size w (analogous to scale):
     Segment time series into windows of size w
     Compute coarsened attribute within each window
     Estimate local transition probabilities from window sequences
     Compute CR_w from windowed data
   
2. Let Γ_hat(w) be the empirical conservation at window size w
   Find local minima of Γ_hat(w) → candidate scales

3. Validate: For each candidate scale, check that conservation
   within the window is significantly lower than between windows
   (permutation test, p < 0.05)

4. Output validated scales
```

---

## 8. Concrete Predictions

### 8.1 Music: Phrase Structure Recovery

**Setup.** Take a corpus of 100 well-formed tonal pieces (Bach chorales, Mozart sonatas, jazz standards). Compute note-to-note transitions from MIDI data. Attribute = tonal tension (from the PLR group or harmonic hierarchy).

**Prediction 8.1 (Phrase Boundaries).** The conservation profile $\Gamma(m)$ will have local minima at:
- $m \approx 1$ (trivial: whole piece is one "cluster")
- $m \approx \text{number of sections}$ (movement/section boundaries)
- $m \approx \text{number of phrases}$ (4-8 bar phrase boundaries)
- $m \approx \text{number of bars}$ (harmonic rhythm boundaries)

The *strongest* minimum (deepest dip) will be at the phrase level ($m \approx 4-8$ bars = 16-32 chords), not the note level. This is because phrases are the most fundamental structural unit in tonal music — they are where the tension arc resolves.

**Prediction 8.2 (Scale Invariance).** For the same piece transposed to different keys, the conservation profile $\Gamma(m)$ will be *identical* up to a rescaling of $m$ (because transposition merely shifts the attribute values uniformly).

**Prediction 8.3 (Atonal Music).** For atonal or serial music (Schoenberg, Webern), the conservation profile will have *no* local minima at the phrase scale. Only the note-to-note scale ($m \approx n$) will show conservation, corresponding to the strict serial ordering. The lack of hierarchical structure is the *signature* of atonal music in the conservation profile.

### 8.2 Code: Function Boundary Detection

**Setup.** Take a well-structured Python/JavaScript codebase (e.g., Flask, Lodash). Parse the AST into token sequences. Attribute = token entropy (from a language model) or token embedding similarity. Transitions = sequential token transitions.

**Prediction 8.4 (Function Boundaries).** The conservation profile will show local minima at:
- $m \approx \text{number of packages}$  
- $m \approx \text{number of modules}$
- $m \approx \text{number of functions/methods}$
- $m \approx \text{number of statements/blocks}$

**Prediction 8.5 (Obfuscated Code).** For obfuscated or minified code (same semantics, different structure), the conservation profile at the function scale will *disappear* (no local minimum), while the statement scale remains. This provides a *structure-independent* measure of code quality.

**Prediction 8.6 (Generated Code).** For LLM-generated code, the conservation profile will be *shallower* (weaker minima) at the function scale compared to human-written code, reflecting the lack of intentional hierarchical organization. This provides a diagnostic for "AI-generated code smell."

### 8.3 Mixture-of-Experts: Expert Cluster Discovery

**Setup.** For a trained MoE transformer (e.g., Mixtral 8×7B), record token-to-expert routing decisions for a large corpus. Attribute = output embedding similarity between experts. Transitions = token-level expert routing.

**Prediction 8.7 (Expert Specialization).** The conservation profile will show local minima at:
- $m = \text{number of expert groups}$ (2-3 groups, corresponding to semantic domains)
- $m = \text{number of experts}$ (the actual expert count)
- $m = \text{number of fine-grained routing patterns}$

**Prediction 8.8 (Load Imbalance).** If one expert is overloaded (receives > 30% of tokens), the conservation profile will show an *attenuated* minimum at the expert level — overloaded experts are "forced" to process diverse tokens, reducing the dynamics-geometry alignment.

### 8.4 Protein Folding: Structural Domain Detection

**Setup.** For a protein with known folding kinetics (from MD simulation), define states as dihedral angle bins. Attribute = hydrophobicity or solvent accessibility. Transitions = trajectory steps.

**Prediction 8.9 (Domain Boundaries).** The conservation profile will show minima at:
- $m \approx \text{number of structural domains}$ (2-3 for single-chain proteins)
- $m \approx \text{number ofsecondary structure elements (helices, sheets; ~10-20)
- $m \approx \text{number of residue-level bins}$ (370 states for $(\phi,\psi)$ at 10° resolution)

The domain-level minimum will be the *deepest* — folding pathways are organized around domain consolidation, making domain transitions the most structurally significant.

**Prediction 8.10 (Folding vs. Unfolding).** The conservation profile during *folding* (high temperature → native state) will show deeper minima than during *unfolding* (native → denatured), reflecting the greater hierarchical organization of the native pathway.

### 8.5 Language: Syntax Tree Recovery

**Setup.** Parse a corpus of English sentences (e.g., Penn Treebank). Define states as part-of-speech tags. Attribute = syntactic embedding (from a dependency parse). Transitions = sequential tag transitions.

**Prediction 8.11 (Phrase Structure).** The conservation profile will show minima at:
- $m \approx \text{number of sentences}$ (discourse boundaries)
- $m \approx \text{number of clauses}$ (subordinate clause boundaries)
- $m \approx \text{number of phrases}$ (NP, VP, PP boundaries)
- $m \approx \text{number of words}$ (word-level transitions)

Language conservation is expected to be *weaker* than music conservation across all scales. Music has stricter hierarchical constraints (harmonic function, voice leading); language tolerates more structural ambiguity. This predicts $\Gamma_{\text{language}}(m) > \Gamma_{\text{music}}(m)$ at phrase-level scales.

**Prediction 8.12 (Grammatical vs. Ungrammatical).** For a grammatical sentence, the minimum at the phrase level will be deeper than for an ungrammatical word salad with the same part-of-speech frequencies. This provides a *syntax-agnostic* measure of grammaticality.

### 8.6 Social Networks: Community Detection

**Setup.** For a social network (e.g., Enron email, arXiv collaboration graph), define states as individuals. Attribute = topic embedding of their communications. Transitions = email/collaboration adjacency.

**Prediction 8.13 (Community Hierarchy).** The conservation profile will show minima at:
- $m \approx \text{number of departments/divisions}$ (coarse organizational structure)
- $m \approx \text{number of research groups/teams}$ (meso-level communities)
- $m \approx \text{number of tightly-connected cliques}$ (micro-level)

**Prediction 8.14 (Homophily Gradient).** The depth of community-level minima correlates with the homophily coefficient: networks with strong homophily (same-topic individuals talk more) produce deeper minima. This quantifies how well community structure aligns with communication dynamics.

---

## 9. Pseudocode for the Multi-Scale Algorithm

### 9.1 Core Algorithm

```python
import numpy as np
from scipy.linalg import eigh
from sklearn.cluster import AgglomerativeClustering
from scipy.sparse.linalg import eigsh


def build_tension_graph_laplacian(P, K):
    """
    Build the single-scale Tension-Graph Laplacian.
    
    Parameters
    ----------
    P : ndarray (n, n)
        Row-stochastic transition matrix.
    K : ndarray (n, n)
        Attribute similarity kernel matrix.
        
    Returns
    -------
    L : ndarray (n, n)
        Tension-Graph Laplacian.
    D : ndarray (n, n)
        Degree matrix (diagonal).
    W : ndarray (n, n)
        Weight matrix = P ⊙ K.
    """
    W = P * K  # element-wise (Hadamard) product
    D = np.diag(W.sum(axis=1))
    L = D - W
    return L, D, W


def spectral_embedding(L, n_components=8):
    """
    Compute spectral embedding from the smallest eigenvectors of L.
    """
    eigenvalues, eigenvectors = eigsh(L, k=n_components, which='SM')
    # Sort by eigenvalue ascending
    idx = np.argsort(eigenvalues)
    eigenvectors = eigenvectors[:, idx]
    return eigenvectors, eigenvalues[idx]


def hierarchical_spectral_cluster(embedding):
    """
    Hierarchically cluster the spectral embedding.
    Returns a fitted AgglomerativeClustering object.
    """
    model = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=0,
        linkage='ward',
        compute_full_tree=True
    )
    model.fit(embedding)
    return model


def cut_dendrogram(model, n_clusters):
    """
    Cut the hierarchical clustering dendrogram at n_clusters.
    Returns a label array of length n (state → cluster assignment).
    """
    model.n_clusters = n_clusters
    model.fit_predict(model.children_)
    return model.labels_


def coarsen_transitions(P, labels, n_clusters):
    """
    Coarsen the transition matrix given cluster labels.
    """
    n = len(labels)
    P_coarse = np.zeros((n_clusters, n_clusters))
    counts = np.zeros(n_clusters)
    
    for i in range(n):
        a = labels[i]
        counts[a] += 1
        for j in range(n):
            b = labels[j]
            P_coarse[a, b] += P[i, j]
    
    for a in range(n_clusters):
        if counts[a] > 0:
            P_coarse[a, :] /= counts[a]
    
    row_sums = P_coarse.sum(axis=1)
    row_sums[row_sums == 0] = 1
    P_coarse = P_coarse / row_sums[:, np.newaxis]
    
    return P_coarse


def coarsen_attributes(attributes, labels, n_clusters, kernel_fn):
    """
    Coarsen the attribute kernel given cluster labels.
    """
    cluster_attrs = np.zeros((n_clusters, attributes.shape[1]))
    counts = np.zeros(n_clusters)
    
    for i in range(len(labels)):
        a = labels[i]
        cluster_attrs[a, :] += attributes[i, :]
        counts[a] += 1
    
    for a in range(n_clusters):
        if counts[a] > 0:
            cluster_attrs[a, :] /= counts[a]
    
    K_coarse = np.zeros((n_clusters, n_clusters))
    for a in range(n_clusters):
        for b in range(n_clusters):
            K_coarse[a, b] = kernel_fn(cluster_attrs[a], cluster_attrs[b])
    
    return K_coarse


def compute_conservation_profile(L):
    """
    Compute conservation ratios for the top K eigenvectors of L.
    """
    eigenvalues, eigenvectors = eigh(L)
    n = L.shape[0]
    cr_values = []
    for k in range(min(5, n)):
        phi = eigenvectors[:, k]
        numerator = phi @ L @ phi
        denominator = phi @ phi
        cr = numerator / denominator if denominator > 1e-12 else 0.0
        cr_values.append(cr)
    return np.array(cr_values)


def multi_scale_conservation(P, attributes, kernel_fn, 
                              n_components=8, n_scales=20):
    """
    Full multi-scale conservation analysis.
    
    Parameters
    ----------
    P : ndarray (n, n)
        Transition matrix.
    attributes : ndarray (n, d)
        Attribute vectors.
    kernel_fn : callable
        Similarity kernel.
    n_components : int
        Number of eigenvectors for spectral embedding.
    n_scales : int or list
        If int: number of scale levels to evaluate.
        If list: specific cluster counts to evaluate.
        
    Returns
    -------
    result : dict
        Contains:
        - 'scales': array of cluster counts evaluated
        - 'profile': array of mean conservation at each scale
        - 'natural_scales': detected local minima
        - 'deep_conservation': bool
        - 'L_scales': list of Laplacians at each scale
    """
    n = P.shape[0]
    
    # Step 1: Build fine-grained kernel
    K = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            K[i, j] = kernel_fn(attributes[i], attributes[j])
    
    # Step 2: Build single-scale Laplacian
    L, D, W = build_tension_graph_laplacian(P, K)
    
    # Step 3: Spectral embedding
    embedding, eigenvalues = spectral_embedding(L, n_components)
    
    # Step 4: Hierarchical clustering
    hc_model = hierarchical_spectral_cluster(embedding)
    
    # Step 5: Determine scales to evaluate
    if isinstance(n_scales, int):
        scales = np.unique(np.logspace(
            np.log10(2), np.log10(max(3, n//2)), 
            num=n_scales
        ).astype(int))
    else:
        scales = np.array(n_scales)
    
    # Step 6: Evaluate each scale
    profile = []
    L_scales = []
    
    for m in scales:
        if m >= n:
            continue
        labels = cut_dendrogram(hc_model, m)
        P_coarse = coarsen_transitions(P, labels, m)
        K_coarse = coarsen_attributes(attributes, labels, m, kernel_fn)
        L_coarse, _, _ = build_tension_graph_laplacian(P_coarse, K_coarse)
        cr_vals = compute_conservation_profile(L_coarse)
        profile.append(np.mean(cr_vals))
        L_scales.append(L_coarse)
    
    profile = np.array(profile)
    
    # Step 7: Detect natural scales (local minima)
    natural_scales = []
    for i in range(1, len(profile) - 1):
        window = max(1, len(scales) // 20)
        left = max(0, i - window)
        right = min(len(profile), i + window + 1)
        if profile[i] < np.min(profile[left:i]) and \
           profile[i] < np.min(profile[i+1:right]):
            natural_scales.append(scales[i])
    
    # Step 8: Deep conservation check
    threshold = 0.1  # tunable
    deep_conservation = all(cr < threshold for cr in profile)
    
    return {
        'scales': scales,
        'profile': profile,
        'natural_scales': np.array(natural_scales),
        'deep_conservation': deep_conservation,
        'L_scales': L_scales,
        'L_fine': L,
        'embedding': embedding
    }


def wavelet_conservation(L, attributes, s_values, g=None):
    """
    Compute wavelet-based conservation at multiple scales.
    """
    if g is None:
        g = lambda x: x * np.exp(-x)
    
    eigenvalues, eigenvectors = eigh(L)
    n = L.shape[0]
    
    grad_a = np.zeros(n)
    for i in range(n):
        for j in range(n):
            if L[i, j] != 0:
                diff = np.linalg.norm(attributes[i] - attributes[j])
                grad_a[i] += L[i, j] * diff
    
    cr_wavelet = []
    for s in s_values:
        wavelet_grad = np.zeros(n)
        wavelet_attr = np.zeros(n)
        for k in range(n):
            coeff = g(s * eigenvalues[k])
            if np.isfinite(coeff):
                phi = eigenvectors[:, k]
                wavelet_grad += coeff * (phi @ grad_a) * phi
                wavelet_attr += coeff * (phi @ attributes[:, 0]) * phi
        
        num = np.linalg.norm(wavelet_grad)**2
        denom = np.linalg.norm(wavelet_attr)**2
        cr_wavelet.append(num / denom if denom > 1e-12 else np.inf)
    
    return np.array(cr_wavelet)
```

### 9.2 Usage Example: Music Analysis

```python
# Example: Analyze a chorale for phrase structure
def rbf_kernel(u, v, sigma=1.0):
    return np.exp(-np.linalg.norm(u - v)**2 / (2 * sigma**2))

# Load chorale: chord sequence + tension attributes
# P = transition matrix from chord sequence
# tensions = tension values (d=1) for each chord

result = multi_scale_conservation(
    P=P,
    attributes=tensions.reshape(-1, 1),
    kernel_fn=lambda u, v: rbf_kernel(u, v, sigma=0.5),
    n_components=6,
    n_scales=30
)

print("Natural scales (cluster counts):", result['natural_scales'])
print("Deep conservation:", result['deep_conservation'])

# Plot conservation profile
import matplotlib.pyplot as plt
plt.figure(figsize=(8, 4))
plt.plot(result['scales'], result['profile'], 'b-')
plt.axvline(result['natural_scales'], color='r', linestyle='--', alpha=0.5)
plt.xlabel('Number of clusters (scale)')
plt.ylabel('Mean conservation ratio')
plt.xscale('log')
plt.title('Multi-Scale Conservation Profile')
plt.grid(alpha=0.3)
plt.show()
```

### 9.3 Complexity-Minded Optimization

For large-scale applications ($n > 10^5$), the full algorithm is impractical. We provide optimizations:

1. **Sparse Laplacian**: If $P$ is sparse (most state pairs have zero transition probability), use sparse matrix storage and `scipy.sparse.linalg.eigsh`.

2. **Nyström Approximation**: For the kernel matrix $K$, sample $p \ll n$ landmark points and approximate $K \approx K_{n,p} K_{p,p}^{-1} K_{p,n}$. Reduces kernel computation from $O(n^2)$ to $O(np^2)$.

3. **Incremental Coarsening**: Instead of evaluating every scale independently, compute the profile incrementally: start from the finest scale, merge clusters one by one following the dendrogram, and update $L^{(i)}$ using rank-1 updates. This reduces scale evaluation from $O(S n^2)$ to $O(n^2 + S m_{\text{avg}}^2)$.

4. **Approximate Natural Scale Detection**: Use a binary search on the dendrogram depth instead of evaluating all scales. Check conservation at candidate depths, narrow to regions with local minima. This reduces scale evaluations from $O(S)$ to $O(\log S)$.

5. **Streaming Wavelet Conservation**: For the wavelet approach, use Chebyshev polynomial approximation to compute $g(sL) f$ in $O(|E|)$ per scale, without eigendecomposition.

---

## 10. Open Questions and Frontiers

### 10.1 Is Deep Conservation Generic?

Deep conservation — simultaneous conservation at all scales — is an extremely strong condition. It implies the system is a perfect nested hierarchy. For which systems does this hold?

**Conjecture 10.1 (Deep Conservation is Rare).** Generic dynamical systems with generic attributes do NOT exhibit deep conservation. Deep conservation requires the attribute to be a *harmonic function* of the dynamics at every scale — equivalent to the attribute being an eigenfunction of all coarsened Laplacians simultaneously. This is a cohomological condition of extraordinary strength.

If true, this means that detecting deep conservation in a real system is strong evidence of *engineered* hierarchical structure (composed music, well-factored code, evolved biological organization) rather than emergent randomness.

### 10.2 Scale Discovery Without Labels

The current algorithm requires building the full hierarchy before finding natural scales. Can we skip the hierarchy construction and directly estimate the optimal scale?

**Conjecture 10.2 (Direct Scale Estimation).** Given only the single-scale Laplacian $L$ and attribute $a$, the optimal coarsening scale $m^*$ satisfies:

$$m^* = \arg\max_m \frac{\|L^{(m)} a^{(m)}\|}{\|a^{(m)}\|}$$

where $L^{(m)}$ and $a^{(m)}$ are the coarsened Laplacian and attribute at the *optimal* partition with $m$ clusters. This is a computationally hard optimization problem, but gradient-based relaxation on the space of soft partitions may be tractable.

### 10.3 Conservation as an Objective

If the multi-scale conservation profile captures structural quality, can we *train* systems to maximize it?

**Conjecture 10.3 (Multi-Scale Conservation Maximization).** Training a neural network to maximize $\sum_i \overline{\operatorname{CR}}_i$ (negative conservation loss) will produce representations that are simultaneously smooth at every scale — hierarchically organized feature spaces.

This generalizes the single-scale Conservation Gradient Descent proposal from THE-LATENT-ABSTRACTION.md to multiple scales. The multi-scale objective is stronger: it prevents the network from 'cheating' by being smooth at only one scale while creating artifacts at others.

### 10.4 Temporal Multi-Scale

The framework presented here is *static* — it assumes fixed transition probabilities and attributes. Real systems evolve over time, and their scale hierarchy may shift. The *temporal multi-scale Laplacian* tracks $\Gamma_t(m)$ as a function of time, detecting phase transitions where the system reorganizes hierarchically.

**Prediction 10.1 (Hierarchy Phase Transitions).** In a piece of music, $\Gamma_t(m)$ will change abruptly at key modulations — the scale hierarchy reorganizes to reflect the new tonal center. In code, $\Gamma_t(m)$ will shift at commit boundaries where architectural changes modify the modular structure.

---

## References

1. Hammond, D. K., Vandergheynst, P., & Gribonval, R. (2011). Wavelets on graphs via spectral graph theory. *Applied and Computational Harmonic Analysis*, 30(2), 129-150.

2. von Luxburg, U. (2007). A tutorial on spectral clustering. *Statistics and Computing*, 17(4), 395-416.

3. Coifman, R. R., & Lafon, S. (2006). Diffusion maps. *Applied and Computational Harmonic Analysis*, 21(1), 5-30.

4. Gavish, M., Nadler, B., & Coifman, R. R. (2010). Multiscale wavelets on trees, graphs and high dimensional data: Theory and applications to semi-supervised learning. *Proceedings of the 27th International Conference on Machine Learning*.

5. Szlam, A., Maggioni, M., & Coifman, R. R. (2008). Regularization on graphs with function-adapted diffusion processes. *Journal of Machine Learning Research*, 9, 1711-1739.

6. Mahoney, M. W., Orecchia, L., & Vishnoi, N. K. (2012). A local spectral method for graphs: With applications to improving graph partitions and exploring data in practice. *Journal of Machine Learning Research*, 13, 2339-2389.

---

*This document extends the spectral alignment principle of THE-LATENT-ABSTRACTION.md to multiple scales. The multi-scale framework transforms the Tension-Graph Laplacian from a flat diagnostic into a spectral microscope — revealing hierarchical structure at every resolution simultaneously.*
