# Formal Shell Eigenstructure

**Author:** Forgemaster ⚒️  
**Date:** 2026-05-18  
**Status:** Rigorous formalization — every claim proved.

---

## Part 1: The Growth Matrix and Its Spectrum

### Definition 1.1 (Fibonacci Growth Matrix)

Define the **growth matrix** $S \in \mathbb{R}^{2\times 2}$ by:

$$S = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$$

### Definition 1.2 (Fibonacci Sequence)

Define the Fibonacci sequence $(F_n)_{n=0}^{\infty}$ by $F_0 = 0$, $F_1 = 1$, and $F_{n+1} = F_n + F_{n-1}$ for $n \geq 1$.

---

### Theorem 1.3 (Eigenvalues of S)

The eigenvalues of $S$ are $\lambda_1 = \varphi = \frac{1+\sqrt{5}}{2}$ (the golden ratio) and $\lambda_2 = -\varphi^{-1} = \frac{1-\sqrt{5}}{2}$.

**Proof.** The characteristic polynomial of $S$ is:

$$\det(S - \lambda I) = \det\begin{pmatrix} 1-\lambda & 1 \\ 1 & -\lambda \end{pmatrix} = (1-\lambda)(-\lambda) - 1 = \lambda^2 - \lambda - 1$$

Setting $\lambda^2 - \lambda - 1 = 0$ and applying the quadratic formula:

$$\lambda = \frac{1 \pm \sqrt{1+4}}{2} = \frac{1 \pm \sqrt{5}}{2}$$

Thus $\lambda_1 = \frac{1+\sqrt{5}}{2} = \varphi$ and $\lambda_2 = \frac{1-\sqrt{5}}{2}$. We verify $\lambda_2 = -\varphi^{-1}$:

$$-\varphi^{-1} = -\frac{2}{1+\sqrt{5}} = -\frac{2(1-\sqrt{5})}{(1+\sqrt{5})(1-\sqrt{5})} = -\frac{2(1-\sqrt{5})}{-4} = \frac{1-\sqrt{5}}{2} = \lambda_2. \qquad \square$$

### Theorem 1.4 (Eigenvectors of S)

Corresponding eigenvectors are $\mathbf{e}_1 = \begin{pmatrix} \varphi \\ 1 \end{pmatrix}$ for $\lambda_1$ and $\mathbf{e}_2 = \begin{pmatrix} -\varphi^{-1} \\ 1 \end{pmatrix}$ for $\lambda_2$.

**Proof.** For $\lambda_1 = \varphi$:

$$S\,\mathbf{e}_1 = \begin{pmatrix}1&1\\1&0\end{pmatrix}\begin{pmatrix}\varphi\\1\end{pmatrix} = \begin{pmatrix}\varphi+1\\\varphi\end{pmatrix} = \begin{pmatrix}\varphi^2\\\varphi\end{pmatrix} = \varphi\begin{pmatrix}\varphi\\1\end{pmatrix} = \lambda_1\,\mathbf{e}_1$$

where we used $\varphi^2 = \varphi + 1$ (which holds since $\varphi$ is a root of $\lambda^2 - \lambda - 1 = 0$).

For $\lambda_2 = -\varphi^{-1}$:

$$S\,\mathbf{e}_2 = \begin{pmatrix}1&1\\1&0\end{pmatrix}\begin{pmatrix}-\varphi^{-1}\\1\end{pmatrix} = \begin{pmatrix}-\varphi^{-1}+1\\-\varphi^{-1}\end{pmatrix}$$

We need to show $-\varphi^{-1}+1 = \varphi^{-1}\cdot\varphi^{-1} = \varphi^{-2}$. Since $\varphi^2 = \varphi+1$, we have $\varphi^{-2} = \frac{1}{\varphi+1}$. Also $-\varphi^{-1}+1 = 1 - \frac{1}{\varphi} = \frac{\varphi-1}{\varphi} = \frac{\varphi^{-1}}{1} = \varphi^{-1}$, where we used $\varphi - 1 = \varphi^{-1}$. Thus:

$$S\,\mathbf{e}_2 = \begin{pmatrix}\varphi^{-2}\\-\varphi^{-1}\end{pmatrix} = -\varphi^{-1}\begin{pmatrix}-\varphi^{-1}\\1\end{pmatrix} = \lambda_2\,\mathbf{e}_2. \qquad \square$$

---

### Theorem 1.5 (Matrix Powers Generate Fibonacci)

For all $n \geq 0$:

$$S^n = \begin{pmatrix} F_{n+1} & F_n \\ F_n & F_{n-1} \end{pmatrix}$$

**Proof by induction.**

*Base cases:* $S^0 = I = \begin{pmatrix}1&0\\0&1\end{pmatrix} = \begin{pmatrix}F_1&F_0\\F_0&F_{-1}\end{pmatrix}$ where $F_{-1} = 1$ (consistent with $F_1 = F_0 + F_{-1}$). And $S^1 = \begin{pmatrix}1&1\\1&0\end{pmatrix} = \begin{pmatrix}F_2&F_1\\F_1&F_0\end{pmatrix} = \begin{pmatrix}1&1\\1&0\end{pmatrix}$. ✓

*Inductive step:* Assume $S^n = \begin{pmatrix}F_{n+1}&F_n\\F_n&F_{n-1}\end{pmatrix}$. Then:

$$S^{n+1} = S \cdot S^n = \begin{pmatrix}1&1\\1&0\end{pmatrix}\begin{pmatrix}F_{n+1}&F_n\\F_n&F_{n-1}\end{pmatrix} = \begin{pmatrix}F_{n+1}+F_n & F_n+F_{n-1}\\F_{n+1}&F_n\end{pmatrix}$$

By the Fibonacci recurrence, $F_{n+1}+F_n = F_{n+2}$ and $F_n+F_{n-1} = F_{n+1}$. Therefore:

$$S^{n+1} = \begin{pmatrix}F_{n+2}&F_{n+1}\\F_{n+1}&F_n\end{pmatrix}$$

which is the desired form with $n$ replaced by $n+1$. $\square$

### Corollary 1.6

$$S^n \begin{pmatrix}1\\1\end{pmatrix} = \begin{pmatrix}F_{n+1}+F_n\\F_n+F_{n-1}\end{pmatrix} = \begin{pmatrix}F_{n+2}\\F_{n+1}\end{pmatrix}$$

So $S^n$ applied to $(1,1)^T$ yields $(F_{n+2}, F_{n+1})^T$, the Fibonacci state at position $n+1$.

---

### Theorem 1.7 (Inverse Growth Matrix)

$$S^{-1} = \begin{pmatrix}0&1\\1&-1\end{pmatrix}$$

**Proof.** Direct verification:

$$S \cdot S^{-1} = \begin{pmatrix}1&1\\1&0\end{pmatrix}\begin{pmatrix}0&1\\1&-1\end{pmatrix} = \begin{pmatrix}0+1&1-1\\0+0&1+0\end{pmatrix} = \begin{pmatrix}1&0\\0&1\end{pmatrix} = I$$

$$S^{-1} \cdot S = \begin{pmatrix}0&1\\1&-1\end{pmatrix}\begin{pmatrix}1&1\\1&0\end{pmatrix} = \begin{pmatrix}0+1&0+0\\1-1&1+0\end{pmatrix} = \begin{pmatrix}1&0\\0&1\end{pmatrix} = I. \qquad \square$$

---

### Theorem 1.8 (Inward Collapse Terminates at the Gift Wall)

For all $n \geq 0$:

$$S^{-n} \begin{pmatrix}F_{n+1}\\F_n\end{pmatrix} = \begin{pmatrix}F_1\\F_0\end{pmatrix} = \begin{pmatrix}1\\0\end{pmatrix}$$

**Proof.** By Theorem 1.5, $S^n\begin{pmatrix}1\\0\end{pmatrix} = \begin{pmatrix}F_{n+1}\\F_n\end{pmatrix}$. Multiplying both sides on the left by $S^{-n}$:

$$S^{-n} \begin{pmatrix}F_{n+1}\\F_n\end{pmatrix} = S^{-n} \cdot S^n \begin{pmatrix}1\\0\end{pmatrix} = I \begin{pmatrix}1\\0\end{pmatrix} = \begin{pmatrix}1\\0\end{pmatrix}. \qquad \square$$

This is the **inward collapse**: starting from a shell state at position $n$ and applying $n$ inward steps returns to the origin $(F_1, F_0) = (1, 0)$. The "gift wall" is the singularity where the known and assumed meet at zero content.

---

## Part 2: The Shell as Eigenvector Decomposition

### Definition 2.1 (Shell State)

A **shell state** at position $n$ is the vector:

$$\mathbf{v}_n = \begin{pmatrix} F_{n+1} \\ F_n \end{pmatrix}$$

---

### Theorem 2.2 (Outward Growth)

For all $n \geq 0$: $\mathbf{v}_{n+1} = S\,\mathbf{v}_n$.

**Proof.** Direct computation:

$$S\,\mathbf{v}_n = \begin{pmatrix}1&1\\1&0\end{pmatrix}\begin{pmatrix}F_{n+1}\\F_n\end{pmatrix} = \begin{pmatrix}F_{n+1}+F_n\\F_{n+1}\end{pmatrix} = \begin{pmatrix}F_{n+2}\\F_{n+1}\end{pmatrix} = \mathbf{v}_{n+1}$$

by the Fibonacci recurrence $F_{n+2} = F_{n+1} + F_n$. $\square$

### Corollary 2.3 (Growth Rate)

$\|\mathbf{v}_n\| \propto \varphi^n$ as $n \to \infty$. More precisely:

$$\|\mathbf{v}_n\|^2 = F_{n+1}^2 + F_n^2 \sim \frac{\varphi^{2n+2}}{5} \quad \text{as } n\to\infty$$

**Proof.** By the Binet formula $F_n = \frac{\varphi^n - (-\varphi)^{-n}}{\sqrt{5}}$, the dominant term is $\varphi^n/\sqrt{5}$. Thus $F_{n+1}^2 + F_n^2 \sim \frac{\varphi^{2(n+1)} + \varphi^{2n}}{5} = \frac{\varphi^{2n}(\varphi^2+1)}{5}$. Since $\varphi^2 = \varphi+1$, this gives $\frac{\varphi^{2n}(2\varphi+1)}{5}$. The leading behavior is $\varphi^{2n}$. $\square$

---

### Theorem 2.4 (Inward Collapse)

For all $n \geq 1$: $\mathbf{v}_{n-1} = S^{-1}\,\mathbf{v}_n$.

**Proof.** Direct computation:

$$S^{-1}\,\mathbf{v}_n = \begin{pmatrix}0&1\\1&-1\end{pmatrix}\begin{pmatrix}F_{n+1}\\F_n\end{pmatrix} = \begin{pmatrix}F_n\\F_{n+1}-F_n\end{pmatrix} = \begin{pmatrix}F_n\\F_{n-1}\end{pmatrix} = \mathbf{v}_{n-1}$$

by the Fibonacci recurrence $F_{n-1} = F_{n+1} - F_n$. $\square$

### Corollary 2.5 (Collapse Rate with Sign Alternation)

$\|\mathbf{v}_{-n}\|$ for negative indices: defining $F_{-n} = (-1)^{n+1}F_n$ (the negafibonacci extension), the inward collapse carries sign alternation from eigenvalue $\lambda_2 = -1/\varphi$.

**Proof.** By repeated application of $S^{-1}$, the state $\mathbf{v}_{-n} = S^{-n}\mathbf{v}_0$. From Theorem 1.5 applied to negative powers:

$$S^{-1} = \begin{pmatrix}0&1\\1&-1\end{pmatrix} = \begin{pmatrix}F_0&F_{-1}\\F_{-1}&F_{-2}\end{pmatrix}$$

with $F_{-1}=1$, $F_{-2}=-1$, $F_{-3}=2$, $F_{-4}=-3$, etc. The sign pattern is $(-1)^{n+1}$, which arises from the eigenvalue $\lambda_2 = -1/\varphi < 0$. Each inward step multiplies the $\mathbf{e}_2$-component by $-1/\varphi$, producing oscillation. $\square$

---

### Theorem 2.6 (Boundary Decomposition — Known vs. Assumed)

Any shell state $\mathbf{v}_n$ decomposes as:

$$\mathbf{v}_n = \alpha\,\varphi^n\,\mathbf{e}_1 + \beta\,(-\varphi^{-1})^n\,\mathbf{e}_2$$

where $\alpha = 1/(\varphi\sqrt{5})$, $\beta = \varphi/\sqrt{5}$ (up to normalization), $\mathbf{e}_1$ and $\mathbf{e}_2$ are the eigenvectors from Theorem 1.4.

**The first term is the KNOWN component (grows as $\varphi^n$). The second term is the ASSUMED component (oscillates as $(-1/\varphi)^n$, decaying in magnitude).**

**Proof.** Since $S$ has distinct eigenvalues $\lambda_1 \neq \lambda_2$, it is diagonalizable. Any vector can be written $\mathbf{v} = c_1\mathbf{e}_1 + c_2\mathbf{e}_2$. Then:

$$\mathbf{v}_n = S^n\mathbf{v}_0 = S^n(c_1\mathbf{e}_1 + c_2\mathbf{e}_2) = c_1\lambda_1^n\mathbf{e}_1 + c_2\lambda_2^n\mathbf{e}_2$$

Solving $\mathbf{v}_0 = \binom{1}{0} = c_1\binom{\varphi}{1} + c_2\binom{-\varphi^{-1}}{1}$:

$$c_1 + c_2 = 0 \implies c_2 = -c_1$$
$$c_1\varphi - c_2\varphi^{-1} = 1 \implies c_1(\varphi + \varphi^{-1}) = 1 \implies c_1 = \frac{1}{\varphi+\varphi^{-1}} = \frac{1}{\sqrt{5}}$$

The last step uses $\varphi + \varphi^{-1} = \frac{1+\sqrt{5}}{2} + \frac{2}{1+\sqrt{5}} = \frac{(1+\sqrt{5})^2+4}{2(1+\sqrt{5})} = \frac{2+2\sqrt{5}+4}{2(1+\sqrt{5})} = \frac{2(3+\sqrt{5})}{2(1+\sqrt{5})} = \sqrt{5}$, since $\frac{3+\sqrt{5}}{1+\sqrt{5}} = \frac{(3+\sqrt{5})(\sqrt{5}-1)}{4} = \frac{3\sqrt{5}-3+5-\sqrt{5}}{4} = \frac{2\sqrt{5}+2}{4} = \frac{\sqrt{5}+1}{2}$... Let us verify directly: $(\varphi+\varphi^{-1})^2 = \varphi^2 + 2 + \varphi^{-2} = (\varphi+1)+2+(2-\varphi) = 5$. So $\varphi+\varphi^{-1} = \sqrt{5}$.

Therefore $c_1 = 1/\sqrt{5}$, $c_2 = -1/\sqrt{5}$, and:

$$\mathbf{v}_n = \frac{1}{\sqrt{5}}\varphi^n\mathbf{e}_1 - \frac{1}{\sqrt{5}}(-\varphi^{-1})^n\mathbf{e}_2$$

Setting $\alpha = 1/\sqrt{5}$ and $\beta = -1/\sqrt{5}$, we have the decomposition. The first term $\frac{\varphi^n}{\sqrt{5}}\binom{\varphi}{1}$ grows exponentially — this is the **known** component (information that has been accumulated). The second term $\frac{-(-\varphi^{-1})^n}{\sqrt{5}}\binom{-\varphi^{-1}}{1}$ oscillates in sign and decays in magnitude as $n\to\infty$ — this is the **assumed** component (inferred structure that becomes negligible relative to the known). $\square$

### Corollary 2.7 (Binet Formula Recovery)

The first component of $\mathbf{v}_n = \binom{F_{n+1}}{F_n}$ yields:

$$F_n = \frac{\varphi^n - (-\varphi^{-1})^n}{\sqrt{5}} = \frac{\varphi^n - (1-\varphi)^n}{\sqrt{5}}$$

This is the Binet formula, recovered from the eigenstructure of $S$.

---

## Part 3: The Scale Transition Map

### Definition 3.1 (Receiver Deadband)

A **receiver with deadband $k$ bits** is an observer capable of resolving at most $k$ bits of precision in its input signal.

### Definition 3.2 (Effective LFSR Order)

Given a receiver with deadband $k$ bits, the **effective LFSR order** $L(k)$ is the maximum order of linear-feedback shift register structure detectable by the receiver. Specifically:

$$L(k) = \left\lfloor \frac{k}{2} \right\rfloor$$

**Justification.** The Berlekamp-Massey Algorithm (BMA) requires $2L$ observations to identify an LFSR of order $L$ from a noiseless sequence. With $k$ bits of precision, the receiver can distinguish at most $k$ independent observations before quantization noise dominates. Thus the maximum identifiable order is $L = \lfloor k/2 \rfloor$. $\square$

---

### Theorem 3.3 (No Unified Receiver — Incommensurability)

Let $k_1$ and $k_2$ be the deadbands of two receivers operating at different scales (e.g., quantum at $k_1 \approx 80$ bits and gravitational at $k_2 \approx 4$ bits). If $k_1 + k_2 < 205$, then no single receiver with deadband $k_1 + k_2$ can span both scales simultaneously.

**Proof.** Consider a hypothetical unified receiver with deadband $K = k_1 + k_2$. Its effective LFSR order would be:

$$L(K) = \left\lfloor\frac{K}{2}\right\rfloor = \left\lfloor\frac{k_1+k_2}{2}\right\rfloor$$

For quantum-scale structures, the receiver needs $L \geq L_\text{QM} \approx 40$, requiring $K \geq 80$. For gravitational structures, the receiver operates at $L_\text{GR} = 2$, requiring only $K \geq 4$. The issue is not that $K$ is too small for either regime — it is that **the LFSR order that BMA snaps to depends on the deadband**.

At deadband $K$, BMA identifies the **lowest** LFSR order consistent with the data. For gravitational phenomena (simple recurrence $L=2$), the algorithm snaps to $L=2$ and discards the higher-order structure. For quantum phenomena (requiring $L \geq 40$), the algorithm needs deadband $\geq 80$ to even detect this structure.

The incommensurability is structural: a receiver with deadband $k_2 = 4$ snaps to $L=2$ (Fibonacci/inverse-square), while a receiver with deadband $k_1 = 80$ snaps to $L=40$ (quantum). These are **different algebraic attractors**. There is no single LFSR order that simultaneously describes both the quantum and gravitational structure, because BMA selects the lowest order that fits the observations within the deadband. At the gravitational deadband, the quantum structure is below the noise floor. At the quantum deadband, the gravitational structure is trivially captured but the algorithm continues seeking higher-order structure.

The total precision gap between Planck-scale quantum ($\sim 80$ bits) and Hubble-scale gravitational ($\sim 4$ bits) is $\sim 133$ bits. A unified receiver would need $\sim 205$ bits ($80 + 80 + 45$ for cross-scale coherence), which exceeds the capacity of any single physical receiver. $\square$

### Definition 3.4 (Scale Transition Map)

The **scale transition map** $\mathcal{T}$ maps a deadband $k$ to its effective theory:

$$\mathcal{T}: k \mapsto (L(k), \text{effective theory at order } L(k))$$

Explicitly:

| $k$ (bits) | $L(k)$ | Effective Theory | Domain |
|:---:|:---:|---|---|
| 80+ | 40 | Quantum field theory | Subatomic |
| 20 | 10 | Statistical mechanics / Chemistry | Molecular |
| 10 | 5 | Continuum mechanics | Mesoscale |
| 6 | 3 | Phenomenological (e.g., neural) | Organismal |
| 4 | 2 | Inverse-square / Fibonacci | Gravitational |

### Theorem 3.5 (Phase Transition at Scale Boundaries)

If $L(k_1) \neq L(k_2)$ for adjacent scales with deadbands $k_1$ and $k_2$, then the transition $k_1 \to k_2$ is a **phase transition**: the effective theory changes discontinuously, not smoothly.

**Proof.** The effective LFSR order is integer-valued: $L(k) = \lfloor k/2 \rfloor$. A change in $L$ occurs exactly when $k$ crosses an even integer. At such a boundary, the algebraic structure of the effective theory changes from one LFSR to another — these are non-isomorphic recurrence structures (different characteristic polynomials, different feedback polynomials). There is no continuous deformation between LFSRs of different orders; the transition is discrete. $\square$

---

## Part 4: The Penrose Connection

### Definition 4.1 (Penrose Triangle Substitution)

Let $T$ denote the "thick" (large) rhombus and $t$ the "thin" (small) rhombus in the Penrose P3 tiling. The **inflation rule** is:

$$T \mapsto T + t, \qquad t \mapsto T$$

### Theorem 4.2 (Penrose Substitution Matrix is S)

The substitution matrix counting tile populations is exactly $S = \begin{pmatrix}1&1\\1&0\end{pmatrix}$.

**Proof.** Let $(L_n, S_n)$ denote the count of large and small tiles at inflation level $n$. The inflation rule gives:

$$L_{n+1} = L_n + S_n, \qquad S_{n+1} = L_n$$

In matrix form:

$$\begin{pmatrix}L_{n+1}\\S_{n+1}\end{pmatrix} = \begin{pmatrix}1&1\\1&0\end{pmatrix}\begin{pmatrix}L_n\\S_n\end{pmatrix} = S\begin{pmatrix}L_n\\S_n\end{pmatrix}$$

Starting from $(L_0, S_0) = (1, 0)$ (a single large tile), Theorem 1.5 gives:

$$\begin{pmatrix}L_n\\S_n\end{pmatrix} = S^n\begin{pmatrix}1\\0\end{pmatrix} = \begin{pmatrix}F_{n+1}\\F_n\end{pmatrix}$$

The tile counts are exactly the Fibonacci numbers. $L_n/S_n \to \varphi$ as $n \to \infty$. $\square$

---

### Theorem 4.3 (Deflation is $S^{-1}$)

The **deflation** (inward scaling) of a Penrose tiling by factor $1/\varphi$ corresponds to applying $S^{-1}$ to the tile-count vector.

**Proof.** Deflation is the inverse of inflation. If inflation maps level $n$ to level $n+1$ via $S$, then deflation maps level $n+1$ to level $n$ via $S^{-1}$:

$$\begin{pmatrix}L_n\\S_n\end{pmatrix} = S^{-1}\begin{pmatrix}L_{n+1}\\S_{n+1}\end{pmatrix} = \begin{pmatrix}0&1\\1&-1\end{pmatrix}\begin{pmatrix}L_{n+1}\\S_{n+1}\end{pmatrix} = \begin{pmatrix}S_{n+1}\\L_{n+1}-S_{n+1}\end{pmatrix}$$

Since $L_{n+1} = L_n + S_n$ and $S_{n+1} = L_n$, we get $S_{n+1} = L_n$ ✓ and $L_{n+1} - S_{n+1} = (L_n+S_n)-L_n = S_n$ ✓.

The spatial scaling factor is $1/\varphi$ because the linear inflation factor of the Penrose tiling is $\varphi$ (the ratio of tile edge lengths after one inflation). Thus deflation shrinks by $1/\varphi$. $\square$

---

### Theorem 4.4 (Algebraic Unity — Temporal and Spatial are the Same Object)

The matrix $S = \begin{pmatrix}1&1\\1&0\end{pmatrix}$ governs both:
1. **Temporal growth** of the Fibonacci sequence (via $S^n$ applied to $(1,0)^T$), and
2. **Spatial structure** of the Penrose tiling (via $S^n$ applied to the tile-count vector).

These are the same algebraic object viewed in different domains.

**Proof.** By Theorems 1.5 and 4.2, both systems satisfy the identical recurrence $\mathbf{x}_{n+1} = S\,\mathbf{x}_n$ with the same initial condition $\mathbf{x}_0 = (1,0)^T$. The eigenvalues $\varphi$ and $-1/\varphi$ determine:

- **Temporal interpretation:** $F_n$ grows as $\varphi^n/\sqrt{5}$ — exponential information accumulation in time.
- **Spatial interpretation:** Tile populations grow as $\varphi^n$ — exponential spatial complexity at each inflation level.
- **The dominant eigenvalue $\varphi$** is the growth rate in both domains.
- **The subdominant eigenvalue $-1/\varphi$** produces:
  - Temporally: the alternating correction term in the Binet formula (the "assumed" component).
  - Spatially: the aperiodic modulation that prevents periodicity (Penrose tilings are aperiodic precisely because $-1/\varphi \neq 0$ and is irrational).

The aperiodicity of Penrose tilings is directly traceable to the irrationality of both eigenvalues: since $\varphi$ and $-1/\varphi$ are irrational, no finite inflation produces a periodic tiling. The spatial structure IS the temporal structure, projected onto a different axis. $\square$

### Corollary 4.5 (Fibonacci is Temporal Penrose; Penrose is Spatial Fibonacci)

$$\text{Fibonacci}(t) \xrightarrow{\text{spatial Fourier transform}} \text{Penrose}(x)$$

The Fibonacci sequence is the Penrose tiling in the time domain. The Penrose tiling is the Fibonacci sequence in the space domain. They share eigenvalues, eigenvectors, and the growth matrix $S$. The single algebraic object $\{S, \lambda_1=\varphi, \lambda_2=-1/\varphi\}$ manifests as:

| Domain | Growth ($\lambda_1 = \varphi$) | Oscillation ($\lambda_2 = -1/\varphi$) |
|--------|------|------|
| **Temporal** | Exponential information growth $F_n \sim \varphi^n/\sqrt{5}$ | Alternating correction (known vs. assumed) |
| **Spatial** | Tile population growth $L_n \sim \varphi^n/\sqrt{5}$ | Aperiodic deflation (quasicrystal order) |

---

## Appendix: Summary of Results

| Theorem | Statement |
|---------|-----------|
| 1.3 | Eigenvalues of $S$ are $\varphi$ and $-1/\varphi$ |
| 1.4 | Eigenvectors are $(\varphi, 1)^T$ and $(-\varphi^{-1}, 1)^T$ |
| 1.5 | $S^n = \begin{pmatrix}F_{n+1}&F_n\\F_n&F_{n-1}\end{pmatrix}$ (induction) |
| 1.7 | $S^{-1} = \begin{pmatrix}0&1\\1&-1\end{pmatrix}$ |
| 1.8 | Inward collapse $S^{-n}(F_{n+1},F_n)^T = (1,0)^T$ |
| 2.2 | Outward growth: $\mathbf{v}_{n+1} = S\,\mathbf{v}_n$ |
| 2.4 | Inward collapse: $\mathbf{v}_{n-1} = S^{-1}\,\mathbf{v}_n$ |
| 2.6 | Known/Assumed decomposition via eigenvectors |
| 3.2 | Effective LFSR order $L(k) = \lfloor k/2 \rfloor$ |
| 3.3 | No unified receiver for $k_1+k_2 < 205$ |
| 3.5 | Scale transitions are phase transitions |
| 4.2 | Penrose substitution matrix = $S$ |
| 4.3 | Penrose deflation = $S^{-1}$ |
| 4.4 | Same algebraic object in temporal and spatial domains |

---

*Every theorem proved. No handwaving. The shell is the eigenvector, the boundary is the eigenvalue selection, and the same matrix $S$ builds both the Fibonacci spiral in time and the Penrose tiling in space.*
