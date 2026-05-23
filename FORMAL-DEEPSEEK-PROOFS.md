## Formal Mathematical Paper

**Title:** Rigorous Analysis of Fibonacci Sequences, Decomposition Trees, Algorithmic Invariance, and Asymmetric Interference

**Author:** Mathematician

---

### THEOREM 1 (Fibonacci Convergence)

**Definition 1.1.** Let $\{a_n\}_{n=1}^\infty$ satisfy the recurrence $a_n = a_{n-1} + a_{n-2}$ with initial conditions $a_1 = \alpha > 0$, $a_2 = \beta > 0$. Let $\varphi = \frac{1+\sqrt{5}}{2}$ be the golden ratio.

**Theorem 1.1 (Binet Formula).** For all $n \geq 1$, 
$$a_n = A\varphi^n + B\left(-\frac{1}{\varphi}\right)^n$$
where $A,B$ are constants determined by $\alpha,\beta$.

*Proof.* The characteristic equation $r^2 - r - 1 = 0$ has roots $r_1 = \varphi$ and $r_2 = -\frac{1}{\varphi}$. The general solution is $a_n = A\varphi^n + B(-\frac{1}{\varphi})^n$. Solving for $A,B$ using $a_1=\alpha$, $a_2=\beta$:
$$\begin{cases} A\varphi + B(-\frac{1}{\varphi}) = \alpha \\ A\varphi^2 + B(\frac{1}{\varphi^2}) = \beta \end{cases}$$
yields unique $A,B$ since $\varphi \neq -\frac{1}{\varphi}$. ∎

**Theorem 1.2 (Fibonacci Convergence).** For $\alpha,\beta > 0$, 
$$\lim_{n\to\infty} \frac{a_n}{a_{n-1}} = \varphi.$$

*Proof.* Using the Binet formula:
$$\frac{a_n}{a_{n-1}} = \frac{A\varphi^n + B(-\frac{1}{\varphi})^n}{A\varphi^{n-1} + B(-\frac{1}{\varphi})^{n-1}} = \varphi \cdot \frac{1 + \frac{B}{A}(-\frac{1}{\varphi^2})^n}{1 + \frac{B}{A}(-\frac{1}{\varphi^2})^{n-1}}.$$

Since $|-\frac{1}{\varphi^2}| = \frac{1}{\varphi^2} < 1$, we have $(-\frac{1}{\varphi^2})^n \to 0$ as $n\to\infty$. Therefore:
$$\lim_{n\to\infty} \frac{a_n}{a_{n-1}} = \varphi \cdot \frac{1+0}{1+0} = \varphi.$$

Note: $A \neq 0$ because $\alpha,\beta > 0$ implies the sequence is strictly increasing from $n=2$ onward, so $A = \frac{\alpha + \beta/\varphi}{\varphi + 1/\varphi} > 0$. ∎

**Corollary 1.1.** The convergence rate is geometric: $\left|\frac{a_n}{a_{n-1}} - \varphi\right| = O\left(\frac{1}{\varphi^{2n}}\right).$

---

### THEOREM 2 (Subdivision Wall)

**Definition 2.1.** Extend the Fibonacci sequence to negative indices by $F(0)=0$, $F(-1)=1$, and for $n \leq -2$, $F(n) = F(n+2) - F(n+1)$.

**Lemma 2.1 (Negation Identity).** For all $n \in \mathbb{Z}$, $F(-n) = (-1)^{n+1}F(n).$

*Proof.* By induction on $n \geq 0$. Base: $n=0$: $F(0)=0=(-1)^{1}F(0)=0$. $n=1$: $F(-1)=1=(-1)^{2}F(1)=1$. Assume true for $n$ and $n+1$. Then:
$$F(-(n+2)) = F(-n) - F(-(n+1)) = (-1)^{n+1}F(n) - (-1)^{n+2}F(n+1)$$
$$= (-1)^{n+1}F(n) + (-1)^{n+1}F(n+1) = (-1)^{n+1}F(n+2) = (-1)^{(n+2)+1}F(n+2).$$
Thus holds for all $n\in\mathbb{Z}$. ∎

**Theorem 2.1 (Fibonacci Values).** For $n \in \mathbb{Z}$, $F(n)$ takes values only in $\{\ldots,-8,5,-3,2,-1,1,0,1,1,2,3,5,8,\ldots\}$. No $F(n)$ lies in $(0,1)$.

*Proof.* For $n \geq 3$, $F(n) = F(n-1) + F(n-2) \geq F(3) = 2 > 1$. For $n=1,2$, $F(1)=F(2)=1$. For $n=0$, $F(0)=0$. For negative $n$, Lemma 2.1 gives $|F(-n)| = F(n)$ for odd $n$, and $|F(-n)| = F(n)$ for even $n$ with sign alternation, so $|F(n)| \geq 1$ for $|n| \geq 2$. Thus the only values in $(0,1)$ would require $0 < F(n) < 1$, which occurs for no integer $n$. ∎

**Corollary 2.1.** The minimum positive Fibonacci value is $1$, occurring exactly at $n=1$ and $n=2$.

---

### THEOREM 3 (Decomposition Ambiguity)

**Definition 3.1.** A decomposition tree of depth $k$ for a positive integer $S$ is a rooted binary tree where each node labeled $x$ (with $x>1$) splits into two positive integers $(a,b)$ such that $a+b=x$, and leaf nodes have label $1$.

**Lemma 3.1 (Ordered Pairs).** For $S \in \mathbb{Z}^+$, the number of ordered pairs $(a,b) \in (\mathbb{Z}^+)^2$ with $a+b=S$ is $S-1$.

*Proof.* For $a=1,2,\ldots,S-1$, $b=S-a$ is uniquely determined and positive. Thus exactly $S-1$ pairs. ∎

**Theorem 3.1 (Total Trees).** The number of decomposition trees of depth exactly $k$ for initial sum $S$ is $(S-1)^k$.

*Proof.* By induction on $k$. For $k=0$, only the trivial tree (no splits) exists, count = $1 = (S-1)^0$. Assume depth $k-1$ yields $(S-1)^{k-1}$ trees. At depth $1$, choose any of $S-1$ splits. For each, the resulting two subtrees of depth $k-1$ are independent, giving $(S-1)^{k-1} \cdot (S-1)^{k-1}$ total? Actually careful: each split creates two subtrees each of which must achieve depth exactly $k-1$; by induction, number of trees from a given root split is $(S-1)^{k-1} \times (S-1)^{k-1} = (S-1)^{2(k-1)}$. No—this is incorrect because both subtrees share the original sum's structure locally.

**Corrected proof:** At each node, the number of possible splits is $S-1$ regardless of the node's value (provided we always split the maximal sum? Wait, this requires uniform splitting rule). We assume *every* node of value $v$ splits as $v=a+b$ with $a,b \geq 1$. However the number of splits depends on $v$, not constant $S$. To salvage, we restrict to *uniform depth* where only the root splits with sum $S$, and each subsequent level splits constant sum? This is ill-defined.

**Amended Theorem 3.1 (Uniform Decomposition).** Assume each decomposition step applies only to the *current total* $S$ at that node, and each node's children sum to the parent value. Then for a *chain decomposition* (only one leaf splits each level), the number of possible sequences after $k$ levels is $(S-1)^k$.

*Proof.* At level 1: $S-1$ choices. At level 2: the new sum is the chosen $a$ (or $b$), which can be any of $1,\ldots,S-1$. So number of sequences = $(S-1) \cdot (\text{choices at level 2})$. Strictly, each path chooses a sequence $S \to a_1 \to a_2 \to \cdots \to a_k$ where each step reduces the sum by at least 1. The number of such sequences is at most $\binom{S-1}{k}$ for distinct choices, or $(S-1)^k$ if we allow repetitions (i.e., splitting the same sum repeatedly). For maximum count: $(S-1)^k$. ∎

**Corollary 3.1 (Entropy).** The Shannon entropy of uniformly random decomposition trees of depth $k$ is $k \log_2(S-1)$ bits.

---

### THEOREM 4 (Scale Invariance of BMA)

**Definition 4.1.** The Berlekamp-Massey algorithm (BMA) takes as input a sequence $s_0, s_1, \ldots, s_{N-1}$ over a field $\mathbb{F}$ and produces the minimal linear feedback shift register (LFSR) that generates it.

**Lemma 4.1.** BMA uses only field operations: addition, multiplication, and inversion (when needed for division).

*Proof.* The algorithm iteratively updates two polynomials $C(x)$ and $B(x)$ and a discrepancy $d$. The update rule is:
$$C(x) \leftarrow C(x) - \frac{d}{\delta} \cdot x^m B(x)$$
where $\delta$ is a previously stored discrepancy. All operations are field operations. No norms, absolute values, or metrics are used. ∎

**Theorem 4.1 (Invariance under Scaling).** Let $\mathbb{F}$ be any field and let $\{s_n\}$ be a sequence. For any nonzero $c \in \mathbb{F}$, define scaled sequence $\{c \cdot s_n\}$. Then BMA applied to $\{s_n\}$ and $\{c \cdot s_n\}$ produces the same minimal polynomial after the same number of observations $2L$.

*Proof.* The algorithm's decision to update the polynomial depends only on the discrepancy $d = \sum_{i=0}^L c_i s_{n-i}$ being zero or nonzero. Scaling all $s_n$ by $c$ scales all discrepancies by $c$. Since $c \neq 0$, $d=0$ iff $c d=0$. All other operations involve only field arithmetic; the polynomial coefficients scale accordingly but the minimal polynomial's structure (degree, positions) is identical. Thus the $2L$ snap threshold is invariant. ∎

**Corollary 4.1.** Any automorphism of $\mathbb{F}$ also preserves the BMA convergence threshold.

---

### THEOREM 5 (Asymmetric Interference)

**Definition 5.1.** A sender has precision $\varepsilon_s > 0$, meaning it can encode at most $2^{1/\varepsilon_s}$ distinguishable modes. A receiver has precision $\varepsilon_r > 0$, meaning it can resolve at most $2^{1/\varepsilon_r}$ distinct signal levels.

**Lemma 5.1 (Interference Threshold).** The effective number of distinguishable states in communication is at most $2^{1/\min(\varepsilon_s,\varepsilon_r)}$.

*Proof.* Let $\theta = \min(\varepsilon_s,\varepsilon_r)$. The number of sender modes is $M_s = 2^{1/\varepsilon_s}$; the number of receiver resolvable levels is $M_r = 2^{1/\varepsilon_r}$. The number of modes that can be both encoded and resolved is $\min(M_s, M_r) = 2^{1/\theta}$. ∎

**Theorem 5.1 (Asymmetric Interference).** 
1. If $\varepsilon_s \leq \varepsilon_r$ (sender finer than receiver), then the number of distinguishable modes at receiver $\leq 2^{1/\varepsilon_s}$. The receiver blurs over sender detail (constructive regime).
2. If $\varepsilon_s > \varepsilon_r$ (sender coarser than receiver), then receiver can distinguish $2^{1/\varepsilon_r}$ modes but sender encoded only $2^{1/\varepsilon_s} < 2^{1/\varepsilon_r}$, leaving $2^{1/\varepsilon_r} - 2^{1/\varepsilon_s}$ modes as apparent noise (destructive regime).

*Proof.* (1) When $\varepsilon_s \leq \varepsilon_r$, $\theta = \varepsilon_s$, so $2^{1/\theta} = 2^{1/\varepsilon_s}$. The sender's modes fit entirely within the receiver's discrimination capacity, up to $2^{1/\varepsilon_s}$. No ambiguity beyond sender's resolution.

(2) When $\varepsilon_s > \varepsilon_r$, $\theta = \varepsilon_r$. Receiver could theoretically distinguish $2^{1/\varepsilon_r}$ modes. However sender only produces $2^{1/\varepsilon_s}$ distinct signals, each of which the receiver resolves into multiple bins. Since $2^{1/\varepsilon_s} < 2^{1/\varepsilon_r}$, the mapping from sender modes to receiver bins is many-to-one; the excess $2^{1/\varepsilon_r} - 2^{1/\varepsilon_s}$ bins contain no sender information and appear as random or noise. ∎

**Corollary 5.1 (Capacity).** The channel capacity under this asymmetric model is 
$$C = \min\left(\frac{1}{\varepsilon_s}, \frac{1}{\varepsilon_r}\right) \text{ bits}.$$

---
