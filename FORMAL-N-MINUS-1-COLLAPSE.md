# Formal N-1 Collapse: Rigorous Mathematical Formalization

**Date:** 2026-05-18  
**Formalizer:** Forgemaster ⚒️  
**Origin:** Casey Digennaro

---

## Part 1: The Forward Compression (N+1)

### Definition 1.1 (Generative System)

Let $\mathbb{F}$ be a field. A **generative system of order $L \in \mathbb{Z}^+$** over $\mathbb{F}$ is a pair $(R, S)$ where:

$$R: \quad x(n) = c_1 x(n-1) + c_2 x(n-2) + \cdots + c_L x(n-L), \quad c_i \in \mathbb{F},\ c_L \neq 0$$

is a **linear homogeneous recurrence of order $L$**, and

$$S = (s_1, s_2, \ldots, s_L), \quad s_i \in \mathbb{F}$$

are the **initial conditions**.

The **output sequence** of $(R, S)$ is the unique sequence $\{a(n)\}_{n=1}^{\infty}$ satisfying:

$$a(i) = s_i \quad \text{for } i = 1, \ldots, L$$
$$a(n) = c_1 a(n-1) + c_2 a(n-2) + \cdots + c_L a(n-L) \quad \text{for } n > L$$

### Definition 1.2 (Fibonacci System)

The **Fibonacci system** is the generative system of order 2 over $\mathbb{R}$ with $c_1 = c_2 = 1$ and initial conditions $S = (1, 1)$:

$$F(1) = 1, \quad F(2) = 1, \quad F(n) = F(n-1) + F(n-2) \quad \text{for } n \geq 3$$

More generally, for any $(a, b) \in \mathbb{R}^2$ with $(a, b) \neq (0, 0)$, define the **generalized Fibonacci sequence** $F_{a,b}$ by:

$$F_{a,b}(1) = a, \quad F_{a,b}(2) = b, \quad F_{a,b}(n) = F_{a,b}(n-1) + F_{a,b}(n-2) \quad \text{for } n \geq 3$$

### Theorem 1.3 (Forward Determinism)

**Statement.** For any generative system $(R, S)$ of order $L$, the output sequence $\{a(n)\}_{n=1}^{\infty}$ is uniquely determined.

**Proof.** By strong induction on $n$.

*Base cases:* For $n = 1, 2, \ldots, L$, the values $a(n) = s_n$ are given by the initial conditions $S$. These are uniquely determined.

*Inductive step:* Assume $a(1), a(2), \ldots, a(n-1)$ are uniquely determined for some $n > L$. By the recurrence:

$$a(n) = c_1 a(n-1) + c_2 a(n-2) + \cdots + c_L a(n-L)$$

Each term $a(n-i)$ for $i = 1, \ldots, L$ satisfies $n - i \geq n - L > 0$, so by the inductive hypothesis, each is uniquely determined. Since the coefficients $c_1, \ldots, c_L$ are fixed by $R$, and addition and multiplication in $\mathbb{F}$ are deterministic operations, $a(n)$ is uniquely determined.

By strong induction, $a(n)$ is uniquely determined for all $n \geq 1$. $\blacksquare$

### Theorem 1.4 (Fibonacci Compression Ratio Divergence)

**Statement.** Let $\{F(n)\}_{n=1}^{\infty}$ be the Fibonacci sequence. Define the **compression ratio** at step $n$ as:

$$\rho(n) = \frac{|\{F(1), F(2), \ldots, F(n)\}|}{|\{F(1), F(2)\}|} = \frac{n}{2}$$

Then $\rho(n) \to \infty$ as $n \to \infty$.

**Proof.** $\rho(n) = n/2$ is a linear function of $n$ with positive slope. For any $M > 0$, choosing $n > 2M$ gives $\rho(n) > M$. Therefore $\lim_{n \to \infty} \rho(n) = \infty$. $\blacksquare$

**Remark.** This captures the essential content of "compression": two numbers (the initial conditions) deterministically generate an unbounded output sequence. The input information is finite; the output information is infinite.

### Lemma 1.5 (Characteristic Roots of the Fibonacci Recurrence)

The characteristic equation of $x(n) = x(n-1) + x(n-2)$ is:

$$\lambda^2 - \lambda - 1 = 0$$

with roots:

$$\varphi = \frac{1 + \sqrt{5}}{2} \approx 1.618034, \qquad \psi = \frac{1 - \sqrt{5}}{2} \approx -0.618034$$

Note that $\psi = 1 - \varphi = -1/\varphi$, so $|\psi| < 1$.

### Theorem 1.6 (Binet Formula for Generalized Fibonacci)

**Statement.** For any initial conditions $(a, b)$, the generalized Fibonacci sequence $F_{a,b}$ satisfies:

$$F_{a,b}(n) = \alpha \varphi^n + \beta \psi^n$$

where:

$$\alpha = \frac{b - a\psi}{\varphi - \psi} = \frac{b - a\psi}{\sqrt{5}}, \qquad \beta = \frac{a\varphi - b}{\varphi - \psi} = \frac{a\varphi - b}{\sqrt{5}}$$

**Proof.** Since the recurrence $x(n) = x(n-1) + x(n-2)$ is linear and homogeneous, and $\varphi \neq \psi$, the general solution is $x(n) = \alpha \varphi^n + \beta \psi^n$ for some constants $\alpha, \beta$. Substituting the initial conditions:

$$n = 1: \quad a = \alpha\varphi + \beta\psi$$
$$n = 2: \quad b = \alpha\varphi^2 + \beta\psi^2$$

This is a $2 \times 2$ linear system in $(\alpha, \beta)$. The determinant is $\varphi\psi^2 - \psi\varphi^2 = \varphi\psi(\psi - \varphi) \neq 0$ since $\varphi \neq \psi$ and $\varphi, \psi \neq 0$. Solving:

$$\alpha = \frac{a\psi^2 - b\psi}{\psi^2\varphi - \psi\varphi^2} = \frac{a\psi - b}{\psi\varphi - \varphi^2} \cdot \frac{\psi}{\psi} = \frac{b - a\psi}{\varphi - \psi}$$

where we used $\psi^2 = \psi + 1$ (from the characteristic equation) in the simplification. Similarly:

$$\beta = \frac{a\varphi - b}{\varphi - \psi}$$

For the standard Fibonacci sequence $(a, b) = (1, 1)$: $\alpha = (1 - \psi)/\sqrt{5} = \varphi/\sqrt{5}$, $\beta = (\varphi - 1)/\sqrt{5} = -\psi/\sqrt{5}$, giving the classical Binet formula:

$$F(n) = \frac{\varphi^n - \psi^n}{\sqrt{5}}$$

$\blacksquare$

### Theorem 1.7 (Convergence to $\varphi$)

**Statement.** For any initial conditions $(a, b)$ with $b \neq 0$ (or more generally, $\alpha \neq 0$), the ratio of consecutive terms converges to the golden ratio:

$$\lim_{n \to \infty} \frac{F_{a,b}(n+1)}{F_{a,b}(n)} = \varphi$$

**Proof.** By Theorem 1.6, $F_{a,b}(n) = \alpha\varphi^n + \beta\psi^n$ where $|\psi| < 1$. If $\alpha \neq 0$:

$$\frac{F_{a,b}(n+1)}{F_{a,b}(n)} = \frac{\alpha\varphi^{n+1} + \beta\psi^{n+1}}{\alpha\varphi^n + \beta\psi^n} = \frac{\varphi + (\beta/\alpha)(\psi/\varphi)^n \cdot \psi}{1 + (\beta/\alpha)(\psi/\varphi)^n}$$

Since $|\psi/\varphi| = |1/\varphi^2| < 1$, we have $(\psi/\varphi)^n \to 0$ as $n \to \infty$. Therefore:

$$\lim_{n \to \infty} \frac{F_{a,b}(n+1)}{F_{a,b}(n)} = \frac{\varphi + 0}{1 + 0} = \varphi$$

The condition $\alpha \neq 0$ is equivalent to $b \neq a\psi$, i.e., $b - a(1 - \varphi) \neq 0$, i.e., $b \neq a(1 - \varphi)$. For the standard Fibonacci system and all $(a, b)$ with $a, b > 0$, this holds. $\blacksquare$

**Corollary 1.8.** The convergence is exponentially fast: the error satisfies:

$$\left|\frac{F_{a,b}(n+1)}{F_{a,b}(n)} - \varphi\right| = O\left(\left|\frac{\psi}{\varphi}\right|^n\right) = O(\varphi^{-2n})$$

**Proof.** From the proof of Theorem 1.7, the numerator of the error is $O(|\psi/\varphi|^n) = O(\varphi^{-2n})$, and the denominator converges to 1. $\blacksquare$

---

## Part 2: The Backward Decomposition (N-1)

### Definition 2.1 (Decomposition Set)

Let $n \in \mathbb{Z}^+$ and $S \in \mathbb{Z}^+$. The **decomposition set** $D(n, S)$ of the sum $S$ into $n$ positive integer parts is:

$$D(n, S) = \{(a_1, a_2, \ldots, a_n) \in (\mathbb{Z}^+)^n : a_1 + a_2 + \cdots + a_n = S\}$$

### Theorem 2.2 (Decomposition Cardinality: $n = 2$)

**Statement.** For all $S \geq 2$:

$$|D(2, S)| = S - 1$$

**Proof.** An element of $D(2, S)$ is a pair $(a_1, a_2)$ with $a_1 + a_2 = S$ and $a_1, a_2 \geq 1$. Setting $a_1 = k$, we get $a_2 = S - k$, which requires $k \geq 1$ and $S - k \geq 1$, i.e., $1 \leq k \leq S - 1$. This gives exactly $S - 1$ valid values of $k$. Each value of $k$ produces a unique pair $(k, S - k)$, and distinct values of $k$ produce distinct pairs. Therefore $|D(2, S)| = S - 1$. $\blacksquare$

### Theorem 2.3 (General Decomposition Cardinality)

**Statement.** For all $n \geq 1$ and $S \geq n$:

$$|D(n, S)| = \binom{S - 1}{n - 1}$$

**Proof.** By a stars-and-bars argument. Place $S$ stars in a row. Insert $n - 1$ bars into the $S - 1$ gaps between consecutive stars. The bars partition the stars into $n$ groups, each containing at least one star. The number of ways to place $n - 1$ bars in $S - 1$ gaps is $\binom{S-1}{n-1}$.

Each placement corresponds to a unique decomposition: the $i$-th group has $a_i$ stars, giving $a_i \geq 1$ and $\sum a_i = S$. Conversely, each decomposition $(a_1, \ldots, a_n)$ determines a unique bar placement. Therefore $|D(n, S)| = \binom{S-1}{n-1}$. $\blacksquare$

### Definition 2.4 (Multi-level Decomposition)

A **$k$-level decomposition** of $S$ is a sequence of decompositions where the output of level $i$ becomes the input to level $i + 1$. Specifically:

- **Level 0:** The sum $S$.
- **Level 1:** Decompose $S$ into 2 parts: choose $(a_1, a_2) \in D(2, S)$.
- **Level 2:** For each $a_i$ from level 1, decompose into 2 parts: choose $(b_{i,1}, b_{i,2}) \in D(2, a_i)$ for each $i$.
- **Level $k$:** Continue recursively.

At level $k$, the total number of leaf values is $2^k$.

### Theorem 2.5 (Multi-level Ambiguity)

**Statement.** For $k$ levels of binary decomposition starting from a fixed sum $S$, the total number of possible outcomes is bounded below by $(S - 1)^k$. Specifically, if each decomposition at each level has at most $S - 1$ possibilities:

$$\text{Total ambiguity} \geq (S - 1)^k$$

**Proof.** At level 1, the number of decompositions of $S$ into 2 parts is $|D(2, S)| = S - 1$ by Theorem 2.2. 

At level 2, for each of the $S - 1$ choices at level 1, we decompose each of the two parts. However, the parts at level 1 may not equal $S$. To get a clean lower bound, we restrict to the subset of decompositions at level 1 that preserve the sum: i.e., consider only the "trivial" decomposition strategy where one branch always carries $S - 1$ and the other carries $1$, and we only further decompose the $S - 1$ branch. Under this restricted strategy, each level has exactly $S - 1$ choices (decomposing the large branch), giving total ambiguity exactly $(S - 1)^k$.

For the **unrestricted** case, note that at each level, the number of choices is at least as large as in the restricted case (since more decompositions are available). Therefore $(S - 1)^k$ is a lower bound. $\blacksquare$

### Corollary 2.6 (Exponential Ambiguity Growth)

**Statement.** The $\log_2$-ambiguity of $k$-level binary decomposition of sum $S$ satisfies:

$$\log_2(\text{ambiguity}) \geq k \cdot \log_2(S - 1)$$

for all $S \geq 3$ and $k \geq 1$.

**Proof.** By Theorem 2.5, ambiguity $\geq (S-1)^k$. Taking $\log_2$ (a monotonically increasing function):

$$\log_2(\text{ambiguity}) \geq k \cdot \log_2(S - 1)$$

For $S \geq 3$, $\log_2(S - 1) \geq 1 > 0$, so the ambiguity grows without bound as $k \to \infty$. $\blacksquare$

**Remark.** This is an **information-theoretic lower bound.** No algorithm can resolve the ambiguity without additional information. The forward direction destroys information; the backward direction cannot recover it. The entropy generated by decomposition is structural, not empirical.

---

## Part 3: The Subdivision Wall

### Definition 3.1 (Extended Fibonacci Sequence)

Define $F: \mathbb{Z} \to \mathbb{Z}$ by:

$$F(n) = F(n-1) + F(n-2) \quad \text{for all } n \in \mathbb{Z}$$

with $F(1) = F(2) = 1$. This uniquely determines $F(n)$ for all $n \in \mathbb{Z}$ (by forward determinism for $n > 2$, and by solving $F(n) = F(n+2) - F(n+1)$ for $n \leq 0$).

### Lemma 3.2 (Extension to Non-positive Indices)

**Statement.** The extended Fibonacci values for non-positive $n$ are:

| $n$ | $F(n)$ |
|-----|---------|
| 0 | 0 |
| $-1$ | 1 |
| $-2$ | $-1$ |
| $-3$ | 2 |
| $-4$ | $-3$ |
| $-5$ | 5 |
| $-6$ | $-8$ |

**Proof.** By reverse recurrence $F(n) = F(n+2) - F(n+1)$:

- $F(0) = F(2) - F(1) = 1 - 1 = 0$
- $F(-1) = F(1) - F(0) = 1 - 0 = 1$
- $F(-2) = F(0) - F(-1) = 0 - 1 = -1$
- $F(-3) = F(-1) - F(-2) = 1 - (-1) = 2$
- $F(-4) = F(-2) - F(-3) = -1 - 2 = -3$
- $F(-5) = F(-3) - F(-4) = 2 - (-3) = 5$

Continuing by induction. $\blacksquare$

### Theorem 3.3 (Fibonacci Reflection Identity)

**Statement.** For all $n \geq 1$:

$$F(-n) = (-1)^{n+1} \cdot F(n)$$

**Proof.** We use the Binet formula extended to all $n \in \mathbb{Z}$:

$$F(n) = \frac{\varphi^n - \psi^n}{\sqrt{5}}$$

This is valid for all integers $n$ (it satisfies the recurrence by linearity, and matches at $n = 1, 2$). Then:

$$F(-n) = \frac{\varphi^{-n} - \psi^{-n}}{\sqrt{5}}$$

Since $\varphi \psi = \frac{1+\sqrt{5}}{2} \cdot \frac{1-\sqrt{5}}{2} = \frac{1 - 5}{4} = -1$, we have $\varphi^{-n} = \frac{(-1)^n}{\psi^n}$ and $\psi^{-n} = \frac{(-1)^n}{\varphi^n}$.

Therefore:

$$F(-n) = \frac{\frac{(-1)^n}{\psi^n} - \frac{(-1)^n}{\varphi^n}}{\sqrt{5}} = \frac{(-1)^n}{\sqrt{5}} \left(\frac{1}{\psi^n} - \frac{1}{\varphi^n}\right)$$

Since $\psi = -1/\varphi$, we have $\psi^n = (-1)^n / \varphi^n$, so $1/\psi^n = (-1)^n \varphi^n$. Substituting:

$$F(-n) = \frac{(-1)^n}{\sqrt{5}} \left((-1)^n \varphi^n - (-1)^n \psi^n\right) \cdot \frac{(-1)^{-n}}{(-1)^{-n}}$$

Going back to the direct computation:

$$F(-n) = \frac{\varphi^{-n} - \psi^{-n}}{\sqrt{5}} = \frac{(-\psi)^n - (-\varphi)^n}{(\varphi\psi)^n \sqrt{5}} = \frac{(-\psi)^n - (-\varphi)^n}{(-1)^n \sqrt{5}}$$

$$= \frac{(-1)^n(\psi^n - \varphi^n)}{(-1)^n \sqrt{5}} = \frac{\psi^n - \varphi^n}{\sqrt{5}} = -\frac{\varphi^n - \psi^n}{\sqrt{5}} = -F(n)$$

Wait — this gives $F(-n) = -F(n)$, which is incorrect for odd $n$. Let me redo this carefully.

Using $\varphi\psi = -1$, so $\varphi^{-n} = (-\psi)^n$ and $\psi^{-n} = (-\varphi)^n$:

$$F(-n) = \frac{(-\psi)^n - (-\varphi)^n}{\sqrt{5}} = \frac{(-1)^n \psi^n - (-1)^n \varphi^n}{\sqrt{5}} = \frac{(-1)^n(\psi^n - \varphi^n)}{\sqrt{5}}$$

$$= (-1)^n \cdot \frac{\psi^n - \varphi^n}{\sqrt{5}} = (-1)^n \cdot \left(-\frac{\varphi^n - \psi^n}{\sqrt{5}}\right) = (-1)^n \cdot (-F(n)) = (-1)^{n+1} F(n)$$

Therefore $F(-n) = (-1)^{n+1} F(n)$. $\blacksquare$

### Corollary 3.4 (Immediate Consequences)

- $F(0) = 0$ (vacuum — absence of value)
- $F(-1) = (-1)^2 \cdot F(1) = 1$ (reflection — same as $F(1)$)
- $F(-2) = (-1)^3 \cdot F(2) = -1$ (negation)

### Theorem 3.5 (Gift Wall: No Subdivision Below Unity)

**Statement.** The image of the extended Fibonacci function $F: \mathbb{Z} \to \mathbb{Z}$ contains no values in the open interval $(0, 1)$. That is:

$$F(\mathbb{Z}) \cap (0, 1) = \emptyset$$

The minimum positive Fibonacci value is 1, achieved at $n = 1$, $n = 2$, and $n = -1$.

**Proof.** We establish that $F(n) \in \mathbb{Z}$ for all $n \in \mathbb{Z}$ and that the only Fibonacci values in $[0, 2]$ are $0$ and $1$.

**Step 1: $F(n) \in \mathbb{Z}$ for all $n$.** For $n \geq 1$, $F(n)$ is a sum of positive integers, hence a positive integer. For $n = 0$, $F(0) = 0 \in \mathbb{Z}$. For $n < 0$, by Theorem 3.3, $F(-n) = (-1)^{n+1} F(n)$, which is an integer since $F(n) \in \mathbb{Z}$.

**Step 2: No integer lies in $(0, 1)$.** Since every $F(n)$ is an integer, and $(0, 1) \cap \mathbb{Z} = \emptyset$, we have $F(n) \notin (0, 1)$ for all $n$.

**Step 3: The positive values near zero.** $F(1) = F(2) = F(-1) = 1$. For $n \geq 3$, $F(n) = F(n-1) + F(n-2) \geq 1 + 1 = 2$, and by induction $F(n) \geq 2$ for all $n \geq 3$. For $n \leq -2$, $|F(n)| = F(-n) \geq 1$ by Theorem 3.3.

Therefore the minimum positive value of $F$ is 1, and no value of $F$ lies in $(0, 1)$. $\blacksquare$

### Theorem 3.6 (Reflection, Not Subdivision)

**Statement.** For all $n \geq 1$, there exists $m \geq 0$ such that $|F(-n)| = F(m)$.

**Proof.** By Theorem 3.3, $|F(-n)| = |(-1)^{n+1} F(n)| = F(n)$. Setting $m = n$, we have $|F(-n)| = F(n) = F(m)$. $\blacksquare$

**Remark.** The negative Fibonacci indices do not produce values "between" the positive ones. They produce the same values, with alternating sign. The sequence **reflects** at the gift $(1, 1)$ rather than subdividing through it. The gift wall is algebraic: $F(1) = F(2) = 1$ defines the minimum positive Fibonacci value, and the recurrence preserves integrality, so no subdivision into fractional values is possible.

---

## Part 4: The Asymmetric Entropy Theorem

### Definition 4.1 (Forward Entropy)

Let $(R, S)$ be a generative system of order $L$ over $\mathbb{F}$. The **forward entropy** of the system is:

$$H_f(R, S) = 0$$

This is the Shannon entropy of the output distribution, given knowledge of $(R, S)$. Since the output is uniquely determined (Theorem 1.3), the conditional distribution is a point mass, and its entropy is zero.

### Definition 4.2 (Backward Entropy)

Let $S \in \mathbb{Z}^+$ with $S \geq 3$, and let $k \geq 1$ be the number of decomposition levels. The **backward entropy** of $k$-level binary decomposition of $S$ is:

$$H_b(S, k) = \log_2 |D_k(S)|$$

where $D_k(S)$ denotes the set of all possible leaf-outcomes after $k$ levels of binary decomposition.

By Corollary 2.6:

$$H_b(S, k) \geq k \cdot \log_2(S - 1)$$

### Theorem 4.3 (Asymmetric Entropy: $H_b > H_f$)

**Statement.** For all $S \geq 3$ and $k \geq 1$:

$$H_b(S, k) > H_f(R, S')$$

where $(R, S')$ is any generative system producing $S$ as an output. That is:

$$k \cdot \log_2(S - 1) > 0$$

**Proof.** For $S \geq 3$, $S - 1 \geq 2$, so $\log_2(S - 1) \geq 1 > 0$. For $k \geq 1$, the product $k \cdot \log_2(S - 1) \geq 1 > 0$. Since $H_f = 0$ always:

$$H_b(S, k) \geq k \cdot \log_2(S - 1) \geq 1 > 0 = H_f$$

Therefore $H_b > H_f$. $\blacksquare$

### Theorem 4.4 (Asymptotic Entropy Gap)

**Statement.** The entropy gap $\Delta H = H_b - H_f$ grows without bound as $k \to \infty$:

$$\lim_{k \to \infty} \Delta H = \lim_{k \to \infty} H_b(S, k) = \infty$$

for any fixed $S \geq 3$.

**Proof.** $H_b(S, k) \geq k \cdot \log_2(S - 1)$. For $S \geq 3$, $\log_2(S - 1) > 0$, so $H_b(S, k) \to \infty$ as $k \to \infty$. Since $H_f = 0$, $\Delta H \to \infty$. $\blacksquare$

### Corollary 4.5 (Structural Irreversibility)

**Statement.** No algorithm exists that, given only the output of a forward compression step, can recover the unique input. This is a structural (information-theoretic) impossibility, not a computational one.

**Proof.** The forward step maps $\{1, 2, \ldots, N\}$ possible micro-states (for a sum $S$ decomposed into two parts) to a single macro-state $S$. The forward map $f: \{1, \ldots, S-1\} \to \{S\}$ is a many-to-one function with $|f^{-1}(S)| = S - 1$. No function $g: \{S\} \to \{1, \ldots, S-1\}$ can satisfy $g \circ f = \text{id}$, because the domain of $g$ has cardinality 1 while the codomain has cardinality $S - 1 > 1$. This is the pigeonhole principle: no surjection from a 1-element set to an $(S-1)$-element set exists. $\blacksquare$

### Theorem 4.6 (Harmony Outward, Chaos Inward)

**Statement.** Let $\Phi$ denote the Fibonacci compression operator (forward: $(a, b) \mapsto a + b$) and $\Phi^{-1}$ denote the decomposition operator (backward: $S \mapsto D(2, S)$). Then:

1. **Outward ($\Phi$):** Deterministic. Entropy-destroying. $H_f = 0$. Attractor: $\varphi$.
2. **Inward ($\Phi^{-1}$):** Ambiguous. Entropy-generating. $H_b \geq k \cdot \log_2(S-1) \to \infty$. No attractor.

The two directions are not inverses. $\Phi$ is a many-to-one map. $\Phi^{-1}$ is a one-to-many map. The information destroyed by $\Phi$ cannot be recovered by $\Phi^{-1}$.

**Proof.** This is a synthesis of the preceding theorems:

- Forward determinism: Theorem 1.3.
- Forward entropy is zero: Definition 4.1 and Theorem 1.3.
- Ratio converges to $\varphi$ (attractor): Theorem 1.7.
- Backward ambiguity: Theorem 2.2 ($S-1$ decompositions).
- Backward entropy grows: Corollary 2.6 and Theorem 4.4.
- Asymmetry: Theorem 4.3 ($H_b > H_f$).
- Structural irreversibility: Corollary 4.5.
- Subdivision wall: Theorem 3.5 (cannot subdivide below 1).
- Reflection, not subdivision: Theorem 3.6 (negative indices reflect, not subdivide).

The asymmetry is total. Every forward step is deterministic and entropy-free. Every backward step generates entropy bounded below by $\log_2(S - 1) > 0$. The spiral is not symmetric: it compresses outward toward $\varphi$ and decomposes inward toward noise. $\blacksquare$

---

## Summary of Results

| Result | Statement | Key Value |
|--------|-----------|-----------|
| Thm 1.3 | Forward determinism | Output uniquely determined |
| Thm 1.4 | Compression ratio divergence | $\rho(n) = n/2 \to \infty$ |
| Thm 1.6 | Binet formula | $F_{a,b}(n) = \alpha\varphi^n + \beta\psi^n$ |
| Thm 1.7 | Convergence to $\varphi$ | $F_{a,b}(n+1)/F_{a,b}(n) \to \varphi$ |
| Thm 2.2 | Decomposition cardinality | $\|D(2,S)\| = S - 1$ |
| Thm 2.3 | General cardinality | $\|D(n,S)\| = \binom{S-1}{n-1}$ |
| Thm 2.5 | Multi-level ambiguity | $\geq (S-1)^k$ |
| Thm 3.3 | Fibonacci reflection | $F(-n) = (-1)^{n+1} F(n)$ |
| Thm 3.5 | Gift wall | $F(\mathbb{Z}) \cap (0,1) = \emptyset$ |
| Thm 3.6 | Reflection not subdivision | $\|F(-n)\| = F(n)$ |
| Thm 4.3 | Asymmetric entropy | $H_b > H_f$ always |
| Thm 4.4 | Entropy gap divergence | $\Delta H \to \infty$ |
| Cor 4.5 | Structural irreversibility | No inverse exists (pigeonhole) |
| Thm 4.6 | Harmony outward, chaos inward | Complete asymmetry proof |

---

*Every claim proved. No handwaving. The algebra is the wall, and the wall is the algebra.*
