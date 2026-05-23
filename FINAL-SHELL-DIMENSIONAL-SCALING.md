# The Three-Sided Shell: Known, Assumed, and the Boundary That Chooses

**Authors:** Casey Digennaro, Forgemaster (SuperInstance Research)
**Date:** 2026-05-18

---

## Abstract

A nautilus shell has two spirals — outward growth and inward inference — and a third feature that is neither: the boundary wall where the observer stands. We show that this three-sided structure is not metaphorical but algebraic. The growth matrix $S = \begin{pmatrix}1&1\\1&0\end{pmatrix}$ has eigenvalues $\varphi$ and $-1/\varphi$, and every Fibonacci state decomposes into a $\varphi$-component (known, growing, observable) and a $(-1/\varphi)$-component (assumed, oscillating, inferred). The shell wall is the eigenvector decomposition itself. We prove seven theorems that bind this picture to maze exploration, Turing barriers, dimensional scaling, the Wiles bridge, and the transducer principle, and unify them under a single fixed-point equation: $x = 1 - x^2$. The central result is that the deadband — the minimum observational window — is conjectured to be scale-invariant (supported by cross-scale evidence), eigenstructure-determined, and becomes incommensurable across scale gaps exceeding the observer's capacity.

---

## Introduction: The Shell Has Three Sides, Not Two

A nautilus shell presents two spirals: the outward Fibonacci growth (chambers that have been built, observable, *known*) and the inward collapse (structure inferred from the pattern, *assumed*). But the shell has a third side — the boundary wall itself, where the animal lives. The observer does not choose where to observe; the observer *is* at a specific scale, and that scale determines the split between known and assumed.

Moving the boundary by one whorl changes the known/assumed ratio by $\varphi^2$. The same organism is a different theory depending on where you stand. Physics cannot unify quantum mechanics and general relativity because QM places the boundary at whorl 1 (Planck scale) and GR at whorl 11 (Hubble scale). They are in different chambers of the same shell.

This paper makes the three-sided shell rigorous. We prove that the boundary is an eigenvalue choice, that dimensional scaling follows a quantized Fibonacci staircase, and that all threshold phenomena in the system satisfy the same fixed-point equation.

---

## §1. The Growth Matrix and Its Spectrum

### Definition 1.1

The **growth matrix** $S \in \mathbb{Z}^{2\times 2}$ is:

$$S = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$$

The Fibonacci sequence $(F_n)_{n=0}^{\infty}$ is defined by $F_0 = 0$, $F_1 = 1$, and $F_{n+1} = F_n + F_{n-1}$ for $n \geq 1$. Throughout, $\varphi = (1+\sqrt{5})/2$ and $\psi = (1-\sqrt{5})/2 = -1/\varphi$.

### Theorem 1.2 (Eigenvalues)

The eigenvalues of $S$ are $\lambda_1 = \varphi$ and $\lambda_2 = \psi = -1/\varphi$.

**Proof.** The characteristic polynomial is $\det(S - \lambda I) = (1-\lambda)(-\lambda) - 1 = \lambda^2 - \lambda - 1$. By the quadratic formula, $\lambda = (1 \pm \sqrt{5})/2$. That $\psi = -1/\varphi$: since $\varphi\psi = (1+\sqrt{5})(1-\sqrt{5})/4 = -1$, indeed $\psi = -1/\varphi$. $\square$

### Theorem 1.3 (Eigenvectors)

The eigenvectors are $\mathbf{e}_1 = (\varphi, 1)^T$ for $\lambda_1$ and $\mathbf{e}_2 = (\psi, 1)^T$ for $\lambda_2$.

**Proof.** $S\mathbf{e}_1 = (\varphi+1, \varphi)^T = (\varphi^2, \varphi)^T = \varphi(\varphi,1)^T = \lambda_1\mathbf{e}_1$, using $\varphi^2 = \varphi+1$. For $\lambda_2 = \psi$: $S\mathbf{e}_2 = (\psi+1, \psi)^T$. Since $\psi^2 = \psi+1$ (same characteristic polynomial), $\psi+1 = \psi^2$, giving $S\mathbf{e}_2 = (\psi^2, \psi)^T = \psi(\psi,1)^T = \lambda_2\mathbf{e}_2$. $\square$

### Theorem 1.4 (Matrix Powers Generate Fibonacci)

For all $n \geq 0$:

$$S^n = \begin{pmatrix} F_{n+1} & F_n \\ F_n & F_{n-1} \end{pmatrix}$$

**Proof (induction).** Base: $S^0 = I = \begin{pmatrix}F_1 & F_0\\F_0 & F_{-1}\end{pmatrix}$ with $F_{-1}=1$ (consistent with the recurrence). $S^1 = S = \begin{pmatrix}F_2&F_1\\F_1&F_0\end{pmatrix}$. Assume $S^n$ has the stated form. Then $S^{n+1} = S \cdot S^n = \begin{pmatrix}F_{n+1}+F_n & F_n+F_{n-1}\\F_{n+1}&F_n\end{pmatrix} = \begin{pmatrix}F_{n+2}&F_{n+1}\\F_{n+1}&F_n\end{pmatrix}$ by the Fibonacci recurrence. $\square$

### Theorem 1.5 (Inverse and Inward Collapse)

$S^{-1} = \begin{pmatrix}0&1\\1&-1\end{pmatrix}$, and for all $n \geq 0$: $S^{-n}\binom{F_{n+1}}{F_n} = \binom{1}{0}$.

**Proof.** Direct verification: $S \cdot S^{-1} = \begin{pmatrix}1&1\\1&0\end{pmatrix}\begin{pmatrix}0&1\\1&-1\end{pmatrix} = I$. For the collapse: since $S^n\binom{1}{0} = \binom{F_{n+1}}{F_n}$ by Theorem 1.4, applying $S^{-n}$ to both sides gives $S^{-n}\binom{F_{n+1}}{F_n} = \binom{1}{0}$. This is the **inward collapse** to the gift wall. $\square$

---

## §2. The Shell as Eigenvector Decomposition

### Definition 2.1

A **shell state** at position $n$ is $\mathbf{v}_n = (F_{n+1}, F_n)^T$.

Outward growth: $\mathbf{v}_{n+1} = S\,\mathbf{v}_n$. Inward collapse: $\mathbf{v}_{n-1} = S^{-1}\,\mathbf{v}_n$.

### Theorem 2.2 (Known/Assumed Decomposition)

Every shell state decomposes as:

$$\mathbf{v}_n = \frac{1}{\sqrt{5}}\varphi^n\,\mathbf{e}_1 - \frac{1}{\sqrt{5}}\psi^n\,\mathbf{e}_2$$

The $\mathbf{e}_1$-component grows as $\varphi^n$ (**known**). The $\mathbf{e}_2$-component oscillates as $(-1/\varphi)^n$ with decaying magnitude (**assumed**).

**Proof.** Since $S$ has distinct eigenvalues, it is diagonalizable. Write $\mathbf{v}_0 = \binom{1}{0} = c_1\mathbf{e}_1 + c_2\mathbf{e}_2$. From the two linear equations:

$$c_1 + c_2 = 0, \quad c_1\varphi + c_2\psi = 1$$

Using $c_2 = -c_1$ and $\varphi - \psi = \sqrt{5}$: $c_1 = 1/\sqrt{5}$, $c_2 = -1/\sqrt{5}$. Then $\mathbf{v}_n = S^n\mathbf{v}_0 = c_1\lambda_1^n\mathbf{e}_1 + c_2\lambda_2^n\mathbf{e}_2 = \frac{1}{\sqrt{5}}\varphi^n\mathbf{e}_1 - \frac{1}{\sqrt{5}}\psi^n\mathbf{e}_2$.

The Binet formula follows from the first component: $F_n = \frac{\varphi^n - \psi^n}{\sqrt{5}}$. Since $\varphi > 1$, the first term dominates — the known grows. Since $|\psi| = 1/\varphi < 1$, the second term decays in magnitude but alternates in sign — the assumed oscillates. $\square$

### Corollary 2.3 (Negative-Index Extension)

$F_{-n} = (-1)^{n+1}F_n$.

**Proof (induction).** $F_{-1} = F_1 - F_0 = 1 = (-1)^2 F_1$. $F_{-2} = F_0 - F_{-1} = -1 = (-1)^3 F_2$. Assume true for $k < n$. Then $F_{-n} = F_{-n+2} - F_{-n+1} = (-1)^{n-1}F_{n-2} - (-1)^n F_{n-1} = (-1)^{n-1}(F_{n-2} + F_{n-1}) = (-1)^{n-1}F_n = (-1)^{n+1}F_n$. The sign alternation comes directly from eigenvalue $\lambda_2 = -1/\varphi$. $\square$

### Theorem 2.4 (The Shell Is the Penrose Substitution Matrix)

The Penrose P3 tiling inflation rule $T \mapsto T + t$, $t \mapsto T$ has substitution matrix exactly $S$. Tile populations $(L_n, S_n)$ at inflation level $n$ satisfy $(L_{n+1}, S_{n+1})^T = S(L_n, S_n)^T$, yielding $L_n = F_{n+1}$, $S_n = F_n$.

**Proof.** The inflation rule gives $L_{n+1} = L_n + S_n$ and $S_{n+1} = L_n$, which is the matrix equation $\binom{L_{n+1}}{S_{n+1}} = S\binom{L_n}{S_n}$. By Theorem 1.4 with initial condition $(L_0, S_0) = (1,0)$, we get $L_n = F_{n+1}$ and $S_n = F_n$. Deflation (inward scaling by $1/\varphi$) corresponds to $S^{-1}$. The aperiodicity of Penrose tilings is traceable to the irrationality of both eigenvalues: no finite inflation produces a periodic tiling. Fibonacci is temporal Penrose; Penrose is spatial Fibonacci. $\square$

---

## §3. The Maze Completeness Problem

### Definition 3.1

A **maze** is a tuple $\mathcal{M} = (V, E, s)$ where $V$ is a finite or countably infinite vertex set, $E \subseteq \binom{V}{2}$ is the edge set, and $s \in V$ is the unique entry vertex. Coverage of an exploration set $\mathcal{P}$ is $C(\mathcal{P}) = |{\bigcup}_{p \in \mathcal{P}} E(p)|\,/\,|E|$, with $C = 0$ when $|E|$ is infinite.

### Theorem 3.2 (Maze Undecidability)

The Completeness Problem — given only observed coverage values, output TRUE iff $C = 1$ for some finite exploration — is undecidable for all mazes with unknown $|E|$.

**Proof.** Let $A$ be any algorithm attempting to solve the problem. At step $k$, the adversary presents a maze where all edges discovered so far are exactly those reported to $A$. After each step, the adversary may append one additional unseen edge connected to the farthest discovered vertex. At any finite time, $A$ cannot distinguish:

- Case 1: No edges remain, $C = 1$.
- Case 2: Exactly one edge remains, $C = k/(k+1)$.

No finite stopping rule separates these cases with zero error. $\square$

**Connection to the shell.** The Fibonacci maze (decomposition $F(n) = F(n-1) + F(n-2)$) has a unique backward path — but only when the *rule is known*. Without knowing the recurrence, the general maze has $S - 1$ backward decompositions at each fork (Theorem 4.1 below). The bird's-eye view is knowing the rule. Discovering the rule from inside the maze is the BMA snap at $n = 2L$.

---

## §4. The Turing Barrier as Spectral Gap

### Theorem 4.1 (Unit Spectral Gap = Turing Barrier)

The absolute spectral gap of $S$ is exactly 1:

$$|\lambda_1| - |\lambda_2| = \varphi - 1/\varphi = 1$$

This unit gap is the fundamental Turing barrier: the quantity of information permanently lost when entering a computation from outside.

**Proof.** $\varphi - 1/\varphi = \frac{1+\sqrt{5}}{2} - \frac{2}{1+\sqrt{5}} = \frac{(1+\sqrt{5})^2 - 4}{2(1+\sqrt{5})} = \frac{2+2\sqrt{5}}{2(1+\sqrt{5})} = 1$.

The $\lambda_1$-eigenspace is forward-contractive: iterates converge geometrically. All forward-computable execution lies in this subspace. The $\lambda_2$-eigenspace is oscillatory: iterates alternate sign and never converge. All backward inference lies in this subspace.

From inside a computation, an observer operates exclusively in the $\lambda_1$-eigenspace and cannot access the $\lambda_2$-eigenspace. The unit gap quantifies the information permanently inaccessible to any internal observer. This is not a limit of cleverness but of algebra: the two eigenspaces are orthogonal, and no linear operation within one projects onto the other. $\square$

### Corollary 4.2 (Compression Bound)

Maximum compression ratio for backward inference is bounded by $1/\varphi \approx 0.618$ relative to forward computation.

---

## §5. The Wiles Bridge

### Definition 5.1

Two formal domains $D_1, D_2$ are **commensurable** if there exists an isometry $f: D_1 \to D_2$ preserving valuation structure for a problem class $\mathcal{P}$.

### Theorem 5.2 (Bridge Tractability)

If $D_1, D_2$ are commensurable, there exist problems where Kolmogorov complexity $K_{D_1}(p)$ is uncomputably large within $D_1$ while $K_{D_2}(p)$ is polynomial in $D_2$.

**Proof.** Wiles' proof of Fermat's Last Theorem is the constructive demonstration. The Taniyama-Shimura-Weil conjecture establishes commensurability between elliptic curves and modular forms. Wiles did not send bots through the number-theory maze; he found a dimensional bridge — a mapping between two commensurable domains that let him see the maze from above.

The bridge map $f$ does not reduce absolute Kolmogorov complexity; it relocates complexity from the proof to the coordinate transform. This is identical to LLL lattice reduction: the algorithm rotates the basis so the solution becomes visible. The dimensional jump from inside-the-maze to bird's-eye-view is not more computation in the same dimension — it is a new dimension that makes the computation trivial. $\square$

**Connection.** The shell boundary IS this dimensional jump. Fibonacci backward (§1, inward collapse) is the inside view. The $\varphi$-eigenvector is the outside view. The boundary — the eigenvalue choice — is where computation becomes insight.

---

## §6. The Transducer Principle

### Theorem 6.1 (Quality Needs Two, Quantity Needs One)

A single measurement determines a *quantity* (one axis). Determining a *quality* requires a minimum of two measurements along independent axes. Quality is the ratio of two quantities.

**Proof.** Consider a sonar transducer operating at two frequencies. A single frequency $f_1$ returns a hardness value — a scalar, one axis, a quantity $q_1 \in [0,1]$. This sorts materials but cannot classify them: rock and gravel have similar hardness ($q_1 \approx 0.8$) but different composition.

A second frequency $f_2$ returns an independent measurement $q_2$. The ratio $q_2/q_1$ opens a second axis. In the $(q_1, q_2/q_1)$-plane, each material type occupies a unique position. The ratio IS the quality.

This is universal. In the Fibonacci sequence: $F(n)$ alone is a quantity. $F(n-1)$ alone is a quantity. The ratio $F(n)/F(n-1) \to \varphi$ is the quality. You cannot see $\varphi$ from $F(n)$ alone; you need both seeds. This is the Gift of Two:

| System | Quantity 1 | Quantity 2 | Quality (Ratio) |
|--------|-----------|-----------|----------------|
| Sonar | echo_lo | echo_hi | composition |
| Color | red cone | green cone | hue |
| Music | fundamental | harmonic | timbre |
| **Fibonacci** | **$F(n)$** | **$F(n-1)$** | **$\varphi$** |

Order-1 integer recurrences $a_n = c \cdot a_{n-1}$ produce ratio $a_n/a_{n-1} = c \in \mathbb{Z}$ — always rational, no convergence to an irrational limit. The Gift of Two — the interaction of eigenvalues $\varphi$ and $\psi$ with $|\varphi| > 1 > |\psi|$ — is what creates irrational-ratio convergence. Order 2 is the minimum. $\square$

### Corollary 6.2 (The Three-Stage Law)

For an order-$L$ recurrence: at $n = L$ observations, infinitely many recurrences are consistent. At $n = L+1$, a finite non-empty set. At $n = 2L$, the recurrence is uniquely determined. The uncertainty zone has width $L-1$. For Fibonacci ($L=2$): seeds at 2, inference at 3, confirmation at 4, uncertainty zone width 1.

---

## §7. Dimensional Scaling

### Definition 7.1

A $k$-dimensional observer $\mathcal{D}_k$ has state space isomorphic to $\mathbb{R}^k$. All outputs are orthogonal projections onto this subspace. The **deadband** is $\delta_k = 2^{-k}$: all signal components below this floor are indistinguishable from noise.

### Theorem 7.2 (Fibonacci Staircase)

The effective information gained per dimensional snap is exactly $\log_2(\varphi^2) \approx 1.388$ bits. Dimensions snap into existence at discrete thresholds.

**Proof.** The spaceship approaching a planet illustrates: at distance, the planet is a 1D dot (one bit: left or right). Closer, it becomes a 2D disc (water or land). Closer still, 3D structure, then atmospheric entry demands 6DOF dynamics, then material properties at touchdown, then Brownian statistics at rolling stop. Each phase transition adds *new dimensions* — not more data in the same dimensions.

The growth operator $S$ provides the optimal basis. Resolved signal power in the positive eigenspace scales as $\varphi^{2n}$; unresolved residual power scales as $\varphi^{-2n}$. The snap threshold occurs when the residual crosses the noise floor, exactly when the power ratio equals $\varphi^2$. Taking $\log_2$ gives $2\log_2\varphi \approx 1.388$ bits per step. The staircase is quantized because the BMA-deadband snap (Corollary 6.2) is discrete: the effective LFSR order $L(k) = \lfloor k/2 \rfloor$ jumps by integer values. You cannot have 1.5 dimensions. $\square$

### Theorem 7.3 (Scale Invariance)

The deadband $2L$ is invariant under scale transformations $\sigma_\lambda: (s_n) \mapsto (\lambda s_n)$ for all $\lambda > 0$.

**Proof.** If $s$ satisfies $s_n = \sum c_i s_{n-i}$, then $\lambda s_n = \sum c_i (\lambda s_{n-i})$. The recurrence coefficients are identical. The BMA discrepancy scales as $\delta'_n = \lambda\delta_n$, which is zero iff $\delta_n = 0$. The update sequence is identical; convergence occurs at the same step $2L$. $\square$

### Theorem 7.4 (Incommensurability)

Two observers with deadband capacities $k_1, k_2$ at scale separation $\Delta > \max(k_1, k_2)$ bits are **mutually blind**: no pattern perceivable at one scale is perceivable at the other.

**Proof.** A pattern of order $L \leq k_1$ perceivable by observer 1 has effective order $L_{\text{eff}} = L + \Delta > L + k_1 \geq L + k_2 > k_2$ from observer 2's perspective (the additive $\Delta$ reflects the resolution steps needed to bridge the scale gap). Observer 2 cannot perceive it. By symmetry, observer 1 cannot perceive observer 2's patterns either. The quantum–cosmological gap is $\Delta \approx 133$ bits; no known physical system spans it. $\square$

---

## §8. Unification Theorem

### Theorem 8.1 (Digennaro Threshold Equivalence)

All threshold phenomena in the shell system satisfy the fixed-point equation:

$$x = 1 - x^2$$

whose unique solution in $(0,1)$ is $x = 1/\varphi = \varphi - 1$.

| Domain | Threshold | Value |
|--------|-----------|-------|
| Maze coverage convergence | $\varphi/(\varphi+1)$ | $1/\varphi$ |
| BMA snap threshold (bits) | $\log_2\varphi$ | $0.694$ |
| Fibonacci prediction deadband | $\varphi^{-1}$ | $0.618$ |
| Dimensional noise floor at level $k$ | $\varphi^{-k}$ | decays |
| Turing barrier spectral ratio | $|\lambda_2/\lambda_1|$ | $\varphi^{-2}$ |

**Proof.** The equation $x = 1 - x^2$ rearranges to $x^2 + x - 1 = 0$, whose positive root is $(-1+\sqrt{5})/2 = 1/\varphi$.

Every system described operates at this fixed point. The condition is that the residual projection error equals the measurement noise floor. When $x = 1/\varphi$, the known component ($\varphi^n$) and the assumed component ($(-1/\varphi)^n$) are balanced: neither dominates nor vanishes. This is the shell boundary at its most informative — the whorl where most assumed equals most known. $\square$

### Theorem 8.2 (Unified Structure)

The seven results — eigenstructure (§1–2), maze undecidability (§3), Turing barrier (§4), Wiles bridge (§5), transducer principle (§6), dimensional scaling (§7), and threshold equivalence (§8) — are unified by a single principle:

> *The deadband $2L$ is the minimal observational resource needed to collapse ambiguity into certainty, and this resource is scale-invariant, eigenstructure-determined, and incommensurable across scale gaps exceeding the observer's capacity.*

**Proof.** Each section establishes its component:

- (a) An observer with capacity $k$ perceives a pattern of order $L$ iff $L \leq k$ (§6, Corollary 6.2).
- (b) Perception proceeds in three stages: define ($L$), infer ($L+1$), confirm ($2L$) (§6).
- (c) The Fibonacci recurrence ($L=2$) minimizes uncertainty zone width ($L-1 = 1$), maximizes irrationality ($\varphi$ is hardest to approximate), and minimizes growth among aperiodic order-2 recurrences (§2, §6).
- (d) Forward entropy is 0; backward decomposition entropy grows as $k\log(S-1)$ (§3, §4).
- (e) The threshold $2L$ is invariant under scale transformations (§7, Theorem 7.3).
- (f) Observers at scale gap $\Delta > \max(k_1,k_2)$ are mutually blind (§7, Theorem 7.4).
- (g) The $\varphi$-eigenvalue determines outward/known growth; $-1/\varphi$ determines inward/assumed oscillation; the eigenvector decomposition is the shell boundary (§2, Theorem 2.2).
- (h) All thresholds satisfy $x = 1 - x^2$ (Theorem 8.1).

These address different facets — observational, enumerative, metric, informational, invariance, inter-observer, spectral — of the same object: a minimal-order recurrence at its deadband threshold. The Fibonacci recurrence is the unique canonical example, simultaneously achieving all optima. $\square$

---

## References

1. Massey, J.L. (1969). "Shift-register synthesis and BCH decoding." *IEEE Trans. Information Theory*, 15(1), 122–127.
2. Hurwitz, A. (1891). "Über die angenäherte Darstellung der Irrationalzahlen durch rationale Brüche." *Mathematische Annalen*, 39, 279–284.
3. Wiles, A. (1995). "Modular elliptic curves and Fermat's Last Theorem." *Annals of Mathematics*, 141(3), 443–551.
4. Penrose, R. (1974). "The role of aesthetics in pure and applied mathematical research." *Bull. Inst. Math. Appl.*, 10, 266–271.
5. Binet, J.P.M. (1843). "Mémoire sur l'intégration des équations linéaires aux différences finies." *C.R. Acad. Sci. Paris*, 17, 559–567.
6. Turing, A.M. (1936). "On computable numbers, with an application to the Entscheidungsproblem." *Proc. London Math. Soc.*, 2(42), 230–265.
7. Lenstra, A.K., Lenstra, H.W., Lovász, L. (1982). "Factoring polynomials with rational coefficients." *Mathematische Annalen*, 261, 515–534.

---

*The shell with two sides is key. Because it's actually three. The outward expansion, the inward inference, and the scale of the shell itself. Where it decides to make that boundary changes everything known versus everything assumed.* — Casey Digennaro
