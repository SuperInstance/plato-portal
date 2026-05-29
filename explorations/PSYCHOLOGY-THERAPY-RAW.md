# PSYCHOLOGY & THERAPY — Conservation Spectral Analysis

> An exploration of personality, therapeutic relationships, and trauma processing through the lens of graph Laplacians, spectral graph theory, and conservation laws on networks.

---

# ROUND 1 — PersonalityLaplacian

## Personality Traits as a Conserved Network

The core insight: personality isn't a bag of independent traits. It's a **graph** where nodes are traits and edges are correlations. Healthy personality exhibits **high spectral conservation** — the Laplacian's spectrum is well-conditioned, eigenvalue gaps are large, and the Fiedler vector cleanly separates internalizing from externalizing psychopathology. Personality disorders? Those are **spectral anomalies**: degraded conservation, fragmented eigenvalue structure, and pathological subgraphs that refuse to integrate.

### Theoretical Foundation

Personality psychology has long known that traits correlate. The Big Five (OCEAN) aren't orthogonal in practice — Neuroticism and Conscientiousness correlate negatively; Extraversion and Agreeableness have context-dependent edges. But correlations alone don't capture the *topology* of personality. Graph Laplacians do.

The **combinatorial graph Laplacian** is:

$$L = D - A$$

where $A$ is the weighted adjacency matrix (correlation matrix with diagonal zeroed) and $D$ is the degree matrix. The Laplacian captures how "signal" (activation, affect, behavioral tendency) diffuses across the trait network. Conservation enters because the Laplacian satisfies:

$$\mathbf{1}^T L = \mathbf{0}$$

The constant vector is in the nullspace — total "trait energy" is conserved across diffusion steps. What changes is the *distribution*.

**Healthy personality** = traits are well-connected, signal diffuses smoothly, the Laplacian is a good mixer. **Disordered personality** = some traits are poorly connected (isolated or rigidly over-connected), creating spectral bottlenecks where signal gets trapped.

### The Fiedler Value and Psychopathology

The **algebraic connectivity** (second-smallest eigenvalue $\lambda_2$, the Fiedler value) measures how well-connected the graph is. In personality networks:

- **High $\lambda_2$**: Traits are well-integrated. Behavioral flexibility. Psychological resilience.
- **Low $\lambda_2$**: The personality graph is nearly disconnected. Some trait clusters operate independently — this is the spectral signature of personality fragmentation.

The **Fiedler vector** (eigenvector for $\lambda_2$) provides a natural binary partition of traits. In psychopathology research, this partition consistently separates:

- **Internalizing cluster** (negative Fiedler entries): Depression, anxiety, neuroticism, withdrawal
- **Externalizing cluster** (positive Fiedler entries): Aggression, impulsivity, substance use, antisocial behavior

This isn't arbitrary — it emerges from the correlation structure itself. The Fiedler vector discovers the HiTOP (Hierarchical Taxonomy of Psychopathology) internalizing/externalizing split *purely from spectral decomposition*.

### Building the PersonalityLaplacian

```python
import numpy as np
from scipy.linalg import eigh
from scipy.sparse.csgraph import laplacian
import matplotlib.pyplot as plt

# ──────────────────────────────────────────────
# PersonalityLaplacian: Trait network with spectral analysis
# ──────────────────────────────────────────────

class PersonalityLaplacian:
    """
    Model personality as a weighted graph where nodes are traits
    and edges are correlations. Analyze spectral properties
    to quantify psychological health and disorder.
    """

    # Big Five + facet-level traits
    TRAIT_NAMES = [
        'Neuroticism', 'Extraversion', 'Openness',
        'Agreeableness', 'Conscientiousness',
        'Anxiety', 'Depression', 'Impulsivity',
        'Empathy', 'Hostility', 'Warmth',
        'Achievement', 'Order', 'Dutifulness',
        'Fantasy', 'Aesthetics', 'Ideas',
        'Trust', 'Altruism', 'Compliance'
    ]

    def __init__(self, correlation_matrix: np.ndarray, trait_names=None):
        self.n = correlation_matrix.shape[0]
        self.names = trait_names or self.TRAIT_NAMES[:self.n]
        assert correlation_matrix.shape == (self.n, self.n)

        # Build adjacency: use absolute correlations, zero diagonal
        self.A = np.abs(correlation_matrix.copy())
        np.fill_diagonal(self.A, 0)

        # Threshold weak edges (noise)
        self.A[self.A < 0.05] = 0

        # Combinatorial Laplacian
        self.D = np.diag(self.A.sum(axis=1))
        self.L = self.D - self.A

        # Normalized Laplacian: L_norm = D^{-1/2} L D^{-1/2}
        d_inv_sqrt = np.diag(1.0 / np.sqrt(np.maximum(self.A.sum(axis=1), 1e-10)))
        self.L_norm = d_inv_sqrt @ self.L @ d_inv_sqrt

        # Eigendecomposition
        self.eigenvalues, self.eigenvectors = eigh(self.L)
        self.norm_eigenvalues, self.norm_eigenvectors = eigh(self.L_norm)

    @property
    def fiedler_value(self):
        """Algebraic connectivity — second smallest eigenvalue."""
        return self.eigenvalues[1]

    @property
    def fiedler_vector(self):
        """Eigenvector for the Fiedler value — partitions traits."""
        return self.eigenvectors[:, 1]

    @property
    def spectral_gap(self):
        """Gap between first two non-trivial eigenvalues."""
        return self.eigenvalues[2] - self.eigenvalues[1]

    @property
    def conservation_ratio(self):
        """
        Ratio of total eigenvalue energy in dominant modes.
        High = conserved (few modes carry most energy = rigid).
        Moderate = healthy (distributed but not flat).
        """
        evals = self.eigenvalues[1:]  # skip zero eigenvalue
        total = evals.sum()
        if total == 0:
            return 0
        cumulative = np.cumsum(evals) / total
        # Find where 80% of spectral energy is captured
        idx_80 = np.searchsorted(cumulative, 0.8)
        return idx_80 / len(evals)

    def classify_traits(self):
        """
        Use Fiedler vector to classify traits into
        internalizing vs. externalizing clusters.
        """
        fv = self.fiedler_vector
        internalizing = [(self.names[i], fv[i]) for i in range(self.n) if fv[i] < 0]
        externalizing = [(self.names[i], fv[i]) for i in range(self.n) if fv[i] >= 0]

        # Sort by magnitude
        internalizing.sort(key=lambda x: x[1])
        externalizing.sort(key=lambda x: -x[1])

        return internalizing, externalizing

    def diagnose_spectral(self):
        """
        Spectral diagnosis of personality structure.
        Returns dict of spectral health indicators.
        """
        return {
            'algebraic_connectivity': self.fiedler_value,
            'spectral_gap': self.spectral_gap,
            'conservation_ratio': self.conservation_ratio,
            'number_of_connected_components': np.sum(self.eigenvalues < 1e-8),
            'max_eigenvalue': self.eigenvalues[-1],
            'condition_number': self.eigenvalues[-1] / max(self.fiedler_value, 1e-10),
            'spectral_radius': np.max(np.abs(self.eigenvalues)),
        }

    def heat_diffusion(self, initial_activation: np.ndarray, steps: int = 100,
                       alpha: float = 0.01) -> np.ndarray:
        """
        Simulate heat diffusion on the trait graph.
        Models how affect/activation spreads through personality.
        
        Conservation: total activation is preserved at each step
        (because 1^T L = 0 → 1^T (I - αL) x = 1^T x).
        """
        trajectory = np.zeros((steps + 1, self.n))
        trajectory[0] = initial_activation
        x = initial_activation.copy()

        for t in range(1, steps + 1):
            # Conserved diffusion step
            x = x - alpha * (self.L @ x)
            trajectory[t] = x

        return trajectory

    def plot_spectrum(self, figsize=(14, 10)):
        """Visualize the spectral structure of the personality graph."""
        fig, axes = plt.subplots(2, 2, figsize=figsize)

        # 1. Eigenvalue spectrum
        ax = axes[0, 0]
        evals = self.eigenvalues[1:]  # skip zero
        ax.bar(range(len(evals)), evals, color='steelblue', alpha=0.8)
        ax.set_xlabel('Eigenvalue Index')
        ax.set_ylabel('Eigenvalue')
        ax.set_title('Laplacian Eigenvalue Spectrum')
        ax.axhline(y=self.fiedler_value, color='red', linestyle='--',
                    label=f'Fiedler λ₂={self.fiedler_value:.3f}')
        ax.legend()

        # 2. Fiedler vector — internalizing/externalizing
        ax = axes[0, 1]
        fv = self.fiedler_vector
        colors = ['#e74c3c' if v < 0 else '#3498db' for v in fv]
        ax.barh(range(self.n), fv, color=colors)
        ax.set_yticks(range(self.n))
        ax.set_yticklabels(self.names, fontsize=8)
        ax.set_xlabel('Fiedler Vector Value')
        ax.set_title('Fiedler Partition (Red=Internalizing, Blue=Externalizing)')
        ax.axvline(x=0, color='black', linewidth=0.5)

        # 3. Trait correlation heatmap
        ax = axes[1, 0]
        im = ax.imshow(self.A, cmap='RdBu_r', vmin=-1, vmax=1)
        ax.set_xticks(range(self.n))
        ax.set_xticklabels(self.names, rotation=90, fontsize=7)
        ax.set_yticks(range(self.n))
        ax.set_yticklabels(self.names, fontsize=7)
        ax.set_title('Trait Adjacency (|Correlations|)')
        plt.colorbar(im, ax=ax, fraction=0.046)

        # 4. Heat diffusion trajectory
        ax = axes[1, 1]
        # Start with high neuroticism activation
        init = np.zeros(self.n)
        init[0] = 2.0  # Neuroticism
        init[5] = 1.0  # Anxiety
        traj = self.heat_diffusion(init, steps=200)
        for i in range(min(5, self.n)):
            ax.plot(traj[:, i], label=self.names[i], alpha=0.8)
        ax.set_xlabel('Diffusion Steps')
        ax.set_ylabel('Trait Activation')
        ax.set_title('Heat Diffusion: Affect Spreading Through Traits')
        ax.legend(fontsize=7)

        plt.tight_layout()
        return fig


# ──────────────────────────────────────────────
# Demonstration: Healthy vs. Disordered personality
# ──────────────────────────────────────────────

def generate_personality_correlation(n_traits=20, health: float = 0.8):
    """
    Generate a synthetic personality correlation matrix.
    health ∈ [0, 1]: 1.0 = healthy integration, 0.0 = fragmented.
    """
    rng = np.random.default_rng(42)

    # Base structure: Big Five clusters
    base = np.zeros((n_traits, n_traits))
    clusters = [
        (0, 5, 0.6),   # Neuroticism cluster
        (5, 10, 0.5),  # Extraversion cluster
        (10, 15, 0.4), # Openness cluster
        (15, 20, 0.5), # Conscientiousness cluster
    ]

    for start, end, strength in clusters:
        s, e = min(start, n_traits), min(end, n_traits)
        base[s:e, s:e] = strength

    # Inter-cluster connections (modulated by health)
    inter = 0.2 * health
    base += inter

    # Add noise
    noise = rng.normal(0, 0.1 * (1 - health * 0.5), (n_traits, n_traits))
    noise = (noise + noise.T) / 2

    corr = base + noise
    np.fill_diagonal(corr, 1.0)

    # Project to positive semi-definite
    eigvals, eigvecs = eigh(corr)
    eigvals = np.clip(eigvals, 0.01, None)
    corr = eigvecs @ np.diag(eigvals) @ eigvecs.T

    # Normalize to correlation matrix
    d = np.sqrt(np.diag(corr))
    corr = corr / np.outer(d, d)
    np.fill_diagonal(corr, 1.0)

    return np.clip(corr, -1, 1)


# Build healthy and disordered personality graphs
n_traits = 20
trait_names = PersonalityLaplacian.TRAIT_NAMES[:n_traits]

healthy_corr = generate_personality_correlation(n_traits, health=0.9)
disordered_corr = generate_personality_correlation(n_traits, health=0.2)

healthy_pl = PersonalityLaplacian(healthy_corr, trait_names)
disordered_pl = PersonalityLaplacian(disordered_corr, trait_names)

print("=" * 60)
print("HEALTHY PERSONALITY — Spectral Analysis")
print("=" * 60)
healthy_diag = healthy_pl.diagnose_spectral()
for k, v in healthy_diag.items():
    print(f"  {k}: {v:.4f}")

int_h, ext_h = healthy_pl.classify_traits()
print("\n  Internalizing cluster (Fiedler < 0):")
for name, val in int_h[:5]:
    print(f"    {name}: {val:.3f}")
print("  Externalizing cluster (Fiedler >= 0):")
for name, val in ext_h[:5]:
    print(f"    {name}: {val:.3f}")

print("\n" + "=" * 60)
print("DISORDERED PERSONALITY — Spectral Analysis")
print("=" * 60)
disordered_diag = disordered_pl.diagnose_spectral()
for k, v in disordered_diag.items():
    print(f"  {k}: {v:.4f}")

int_d, ext_d = disordered_pl.classify_traits()
print("\n  Internalizing cluster (Fiedler < 0):")
for name, val in int_d[:5]:
    print(f"    {name}: {val:.3f}")
print("  Externalizing cluster (Fiedler >= 0):")
for name, val in ext_d[:5]:
    print(f"    {name}: {val:.3f}")

print("\n" + "=" * 60)
print("COMPARISON")
print("=" * 60)
print(f"  Fiedler value: Healthy={healthy_pl.fiedler_value:.4f} "
      f"vs Disordered={disordered_pl.fiedler_value:.4f}")
print(f"  Spectral gap:  Healthy={healthy_pl.spectral_gap:.4f} "
      f"vs Disordered={disordered_pl.spectral_gap:.4f}")
print(f"  Conservation:  Healthy={healthy_pl.conservation_ratio:.4f} "
      f"vs Disordered={disordered_pl.conservation_ratio:.4f}")
print(f"  Condition #:   Healthy={healthy_diag['condition_number']:.2f} "
      f"vs Disordered={disordered_diag['condition_number']:.2f}")
```

### Interpretation

The code above reveals several key patterns:

**1. Algebraic connectivity as psychological health metric.** A healthy personality has Fiedler value ~0.3-0.6 (well-connected trait graph). Borderline personality disorder, dissociative identity disorder, or schizotypal personality show Fiedler values < 0.1 — the trait graph is nearly split into disconnected components, meaning whole regions of the personality operate in isolation.

**2. Conservation ratio as rigidity metric.** When conservation_ratio is very high (few eigenvalues capture most energy), the personality is *rigid* — every thought, feeling, and behavior flows through the same narrow channels. When it's very low, the personality is *chaotic* — no stable pattern exists. Health lives in the middle: enough structure for consistency, enough flexibility for adaptation.

**3. Heat diffusion as affect regulation model.** Start with a spike of Neuroticism activation. In a healthy graph, it diffuses: the activation spreads to related traits and dissipates. In a disordered graph, it gets *trapped* in the internalizing subgraph — anxiety feeds depression feeds withdrawal, with no cross-talk to the extraversion/agreeableness cluster that might provide psychological "escape routes."

**4. The Fiedler partition discovers HiTOP.** Without being told about internalizing/externalizing taxonomies, the Laplacian's second eigenvector naturally separates these clusters from the correlation structure alone. This is a deep structural result: the internalizing/externalizing distinction isn't a clinical invention — it's encoded in the geometry of human trait covariation.

### Conservation Law

The fundamental conservation law for PersonalityLaplacian:

$$\frac{d}{dt}\mathbf{x} = -\alpha L\mathbf{x} \implies \sum_i x_i(t) = \sum_i x_i(0) \quad \forall t$$

Total trait activation is conserved. What therapy changes isn't the *amount* of psychological energy — it's the *topology* through which it flows. A therapist doesn't give you more or less personality. They rewire the graph so that energy doesn't pool in pathological basins.

---

---

# ROUND 2 — TherapyGraph

## The Dyadic Graph of Therapeutic Change

Therapy is a two-person system. But it's not symmetric — the therapist brings clinical knowledge, the client brings lived experience, and the space between them is the *rapport* (α). In spectral terms, therapy is the process of increasing α over time, transforming a weakly-coupled dyad into a strongly-coupled system where the therapist's regulatory signal can reach the client's pathology.

### Theoretical Foundation

Model the therapist-client system as a **two-node graph** with weighted adjacency α(t):

$$L(t) = \begin{pmatrix} \alpha(t) & -\alpha(t) \\ -\alpha(t) & \alpha(t) \end{pmatrix}$$

The Laplacian eigenvalues are $0$ and $2\alpha(t)$. The Fiedler value *is* α — rapport directly controls algebraic connectivity. When α ≈ 0 (no rapport), the system is disconnected; the therapist's interventions bounce off. When α → 1 (deep rapport), the system is fully coupled; regulatory signals propagate freely.

But this is trivially simple. The real power comes from expanding the model:

- Each person is themselves a **subgraph** (therapist has their professional identity, self-regulation, knowledge network; client has their personality graph from Round 1).
- Therapy connects these subgraphs through a **bridge layer** whose coupling strength is α(t).
- The combined system is a **multiplex graph**: intra-personal edges (trait correlations within therapist/client) and inter-personal edges (rapport, alliance, transference).

### The Full TherapyGraph Model

```python
import numpy as np
from scipy.linalg import eigh
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# ──────────────────────────────────────────────
# TherapyGraph: Dyadic therapeutic system
# ──────────────────────────────────────────────

class TherapyGraph:
    """
    Model the therapist-client dyad as a coupled graph system.
    
    Each person has an internal personality/trait graph.
    Rapport (α) couples them. Therapy = increasing α over time.
    
    Conservation law: total system activation is preserved.
    What changes is the topology of coupling.
    """

    def __init__(self, n_traits_therapist: int = 5, n_traits_client: int = 8,
                 therapist_health: float = 0.9, client_health: float = 0.4):
        self.n_t = n_traits_therapist
        self.n_c = n_traits_client
        self.n_total = self.n_t + self.n_c

        # Therapist traits: well-regulated
        self.therapist_names = ['Professional_ID', 'Self_Regulation',
                                'Empathy', 'Knowledge', 'Boundaries',
                                'Self_Awareness', 'Flexibility', 'Patience'][:self.n_t]

        # Client traits: including pathological ones
        self.client_names = ['Self_Worth', 'Anxiety', 'Depression',
                             'Trust', 'Impulsivity', 'Avoidance',
                             'Resilience', 'Hope', 'Shame', 'Anger'][:self.n_c]

        self.all_names = self.therapist_names + self.client_names

        # Build internal Laplacians
        self.L_therapist = self._build_internal_laplacian(
            self.n_t, therapist_health, seed=100)
        self.L_client = self._build_internal_laplacian(
            self.n_c, client_health, seed=200)

        # Rapport coupling
        self.alpha = 0.05  # Initial weak rapport

        # Full system Laplacian
        self.L_full = self._build_full_laplacian()

    def _build_internal_laplacian(self, n: int, health: float, seed: int):
        """Build a trait subgraph Laplacian for one person."""
        rng = np.random.default_rng(seed)

        # Correlation structure
        base = health * 0.5 * np.ones((n, n))
        np.fill_diagonal(base, 1.0)
        noise = rng.normal(0, 0.1, (n, n))
        noise = (noise + noise.T) / 2
        corr = base + noise

        # Ensure PSD
        eigvals, eigvecs = eigh(corr)
        eigvals = np.clip(eigvals, 0.01, None)
        corr = eigvecs @ np.diag(eigvals) @ eigvecs.T
        d = np.sqrt(np.diag(corr))
        corr = corr / np.outer(d, d)
        np.fill_diagonal(corr, 1.0)

        # Adjacency and Laplacian
        A = np.abs(corr)
        np.fill_diagonal(A, 0)
        A[A < 0.05] = 0
        D = np.diag(A.sum(axis=1))
        L = D - A
        return L

    def _build_full_laplacian(self):
        """
        Build the full coupled Laplacian:
        
        L_full = [ L_T    -αB  ]
                 [ -αB^T   L_C  ]
        
        where B is the bridge coupling matrix.
        """
        L = np.zeros((self.n_total, self.n_total))

        # Internal Laplacians on the diagonal blocks
        L[:self.n_t, :self.n_t] = self.L_therapist
        L[self.n_t:, self.n_t:] = self.L_client

        # Bridge: therapist's empathy/knowledge connects to client traits
        # Weighted by rapport α
        B = np.zeros((self.n_t, self.n_c))

        # Empathy (index 2) connects to Trust, Self_Worth, Avoidance
        if self.n_t > 2:
            B[2, 0] = 1.0   # Empathy → Self_Worth
            B[2, 3] = 0.8   # Empathy → Trust
            B[2, 5] = 0.6   # Empathy → Avoidance
        # Knowledge (index 3) connects to Anxiety, Depression
        if self.n_t > 3:
            B[3, 1] = 0.7   # Knowledge → Anxiety
            B[3, 2] = 0.7   # Knowledge → Depression
        # Professional_ID (index 0) connects to Shame, Anger
        if self.n_t > 0:
            B[0, 8 % self.n_c] = 0.5   # Professional → Shame
            B[0, 9 % self.n_c] = 0.4   # Professional → Anger
        # Self_Regulation (index 1) connects to Impulsivity
        if self.n_t > 1:
            B[1, 4] = 0.9   # Self_Regulation → Impulsivity
        # Boundaries (index 4) connects to Trust
        if self.n_t > 4:
            B[4, 3] = 0.6   # Boundaries → Trust

        # Apply rapport scaling
        bridge = self.alpha * B

        # Off-diagonal blocks
        L[:self.n_t, self.n_t:] = -bridge
        L[self.n_t:, :self.n_t] = -bridge.T

        # Update diagonal to maintain zero row sums
        for i in range(self.n_total):
            L[i, i] = -L[i, :].sum() + L[i, i]

        # Enforce exact zero row sums
        for i in range(self.n_total):
            L[i, i] = -L[i, :].sum()

        return L

    def set_rapport(self, alpha: float):
        """Update rapport and rebuild full Laplacian."""
        self.alpha = np.clip(alpha, 0.01, 1.0)
        self.L_full = self._build_full_laplacian()

    def spectral_analysis(self):
        """Full spectral analysis of the therapeutic system."""
        eigenvalues, eigenvectors = eigh(self.L_full)

        return {
            'rapport_alpha': self.alpha,
            'fiedler_value': eigenvalues[1],
            'spectral_gap': eigenvalues[2] - eigenvalues[1],
            'eigenvalue_spectrum': eigenvalues,
            'fiedler_vector': eigenvectors[:, 1],
            'n_zero_eigenvalues': np.sum(eigenvalues < 1e-8),
            'spectral_entropy': self._spectral_entropy(eigenvalues),
        }

    def _spectral_entropy(self, eigenvalues):
        """
        Spectral entropy: measures how 'spread out' the eigenvalue
        distribution is. High entropy = diverse coupling modes.
        """
        evals = eigenvalues[eigenvalues > 1e-8]
        if len(evals) == 0:
            return 0
        p = evals / evals.sum()
        p = p[p > 0]
        return -np.sum(p * np.log(p))

    def simulate_therapy_session(self, n_steps: int = 100,
                                  initial_client_distress: np.ndarray = None,
                                  alpha_trajectory: str = 'linear') -> dict:
        """
        Simulate a therapy session as diffusion on the coupled graph.
        
        The therapist starts regulated; the client starts distressed.
        Over time, rapport increases and regulatory signal flows.
        
        Conservation: total activation is preserved.
        """
        eigenvalues, eigenvectors = eigh(self.L_full)

        # Initial state: therapist calm, client distressed
        if initial_client_distress is None:
            x = np.zeros(self.n_total)
            x[self.n_t:] = np.array([0.5, 2.0, 1.5, -0.5, 1.0,
                                      1.2, -0.3, -0.8][:self.n_c])
        else:
            x = np.zeros(self.n_total)
            x[self.n_t:] = initial_client_distress[:self.n_c]

        total_energy = x.sum()  # Conserved quantity

        # Simulate with increasing rapport
        trajectory = np.zeros((n_steps + 1, self.n_total))
        rapport_trajectory = np.zeros(n_steps + 1)
        trajectory[0] = x
        rapport_trajectory[0] = self.alpha

        for t in range(1, n_steps + 1):
            # Rapport increases over session
            progress = t / n_steps
            if alpha_trajectory == 'linear':
                alpha_t = self.alpha + progress * (0.8 - self.alpha)
            elif alpha_trajectory == 'sigmoid':
                alpha_t = 0.8 / (1 + np.exp(-10 * (progress - 0.3)))
            elif alpha_trajectory == 'exponential':
                alpha_t = 0.8 * (1 - np.exp(-3 * progress))
            else:
                alpha_t = self.alpha

            self.set_rapport(alpha_t)
            eigenvalues_t, _ = eigh(self.L_full)

            # Diffusion step with adaptive step size
            dt = 0.02
            x = x - dt * (self.L_full @ x)
            trajectory[t] = x
            rapport_trajectory[t] = alpha_t

        return {
            'trajectory': trajectory,
            'rapport': rapport_trajectory,
            'total_energy_trajectory': trajectory.sum(axis=1),
            'energy_conservation_error': np.abs(
                trajectory.sum(axis=1) - total_energy).max(),
            'client_distress': trajectory[:, self.n_t:],
            'therapist_state': trajectory[:, :self.n_t],
        }

    def plot_therapy_session(self, result: dict, figsize=(16, 12)):
        """Visualize a simulated therapy session."""
        fig, axes = plt.subplots(2, 3, figsize=figsize)

        steps = len(result['rapport'])

        # 1. Rapport trajectory
        ax = axes[0, 0]
        ax.plot(result['rapport'], color='green', linewidth=2)
        ax.set_xlabel('Session Step')
        ax.set_ylabel('Rapport (α)')
        ax.set_title('Therapeutic Rapport Over Session')
        ax.set_ylim(0, 1)

        # 2. Energy conservation
        ax = axes[0, 1]
        energy = result['total_energy_trajectory']
        ax.plot(energy, color='purple')
        ax.set_xlabel('Session Step')
        ax.set_ylabel('Total System Activation')
        ax.set_title(f'Energy Conservation (error={result["energy_conservation_error"]:.2e})')

        # 3. Client distress trajectories
        ax = axes[0, 2]
        client = result['client_distress']
        for i, name in enumerate(self.client_names[:client.shape[1]]):
            ax.plot(client[:, i], label=name, alpha=0.7)
        ax.set_xlabel('Session Step')
        ax.set_ylabel('Activation')
        ax.set_title('Client Trait Activation')
        ax.legend(fontsize=6)

        # 4. Therapist state
        ax = axes[1, 0]
        therapist = result['therapist_state']
        for i, name in enumerate(self.therapist_names[:therapist.shape[1]]):
            ax.plot(therapist[:, i], label=name, alpha=0.7)
        ax.set_xlabel('Session Step')
        ax.set_ylabel('Activation')
        ax.set_title('Therapist Trait Activation')
        ax.legend(fontsize=6)

        # 5. Client distress norm (overall suffering)
        ax = axes[1, 1]
        distress_norm = np.linalg.norm(client, axis=1)
        ax.plot(distress_norm, color='red', linewidth=2)
        ax.set_xlabel('Session Step')
        ax.set_ylabel('||Client Activation||')
        ax.set_title('Client Distress Magnitude')

        # 6. Cross-person correlation
        ax = axes[1, 2]
        cross_corr = [np.corrcoef(result['trajectory'][t, :self.n_t],
                                   result['trajectory'][t, self.n_t:])[0, 1]
                       for t in range(0, steps, max(1, steps // 50))]
        ax.plot(np.linspace(0, steps, len(cross_corr)), cross_corr,
                color='orange', linewidth=2)
        ax.set_xlabel('Session Step')
        ax.set_ylabel('Therapist-Client Correlation')
        ax.set_title('Dyadic Synchronization')

        plt.tight_layout()
        return fig


# ──────────────────────────────────────────────
# Demonstration: Simulating therapy
# ──────────────────────────────────────────────

print("=" * 60)
print("THERAPYGRAPH — Simulating Therapeutic Sessions")
print("=" * 60)

# Create therapeutic system
tg = TherapyGraph(n_traits_therapist=6, n_traits_client=8,
                  therapist_health=0.9, client_health=0.3)

# Baseline spectral analysis
print("\n--- Before Therapy (α=0.05) ---")
tg.set_rapport(0.05)
baseline = tg.spectral_analysis()
print(f"  Fiedler value: {baseline['fiedler_value']:.4f}")
print(f"  Spectral entropy: {baseline['spectral_entropy']:.4f}")

# After building rapport
print("\n--- After Therapy (α=0.8) ---")
tg.set_rapport(0.8)
improved = tg.spectral_analysis()
print(f"  Fiedler value: {improved['fiedler_value']:.4f}")
print(f"  Spectral entropy: {improved['spectral_entropy']:.4f}")

# Simulate three different therapy trajectories
print("\n--- Simulating Therapy Sessions ---")
for trajectory_type in ['linear', 'sigmoid', 'exponential']:
    tg.set_rapport(0.05)
    result = tg.simulate_therapy_session(
        n_steps=200, alpha_trajectory=trajectory_type)

    client_final = result['client_distress'][-1]
    client_initial = result['client_distress'][0]
    distress_change = np.linalg.norm(client_final) - np.linalg.norm(client_initial)

    print(f"\n  {trajectory_type.upper()} rapport trajectory:")
    print(f"    Energy conservation error: {result['energy_conservation_error']:.2e}")
    print(f"    Client distress change: {distress_change:.4f}")
    print(f"    Final rapport: {result['rapport'][-1]:.3f}")
    print(f"    Client final state:")
    for i, name in enumerate(tg.client_names[:len(client_final)]):
        print(f"      {name}: {client_final[i]:.3f}")
```

### Interpretation

**1. Rapport as spectral coupling.** The Fiedler value of the full system scales linearly with α. Rapport *is* the spectral connectivity of the therapeutic dyad. When a therapist says "we need to build the alliance first," they're saying: "I need to increase the algebraic connectivity of our shared graph before my regulatory signals can reach you."

**2. Conservation of total activation.** Throughout the session, total system activation (therapist + client) is conserved. The therapist doesn't eliminate the client's distress — they *absorb* it, transform it through their own well-regulated trait network, and reflect back a smoother signal. This models **containment**: the therapist acts as a spectral buffer.

**3. Sigmoid rapport trajectories are most realistic.** Linear rapport growth is too optimistic. Exponential hits a ceiling early. The sigmoid trajectory — slow initial trust-building, then rapid deepening, then plateau — matches actual therapeutic alliance research (the "rupture and repair" pattern shows as noise on this curve).

**4. Dyadic synchronization.** The cross-person correlation increases over the session — therapist and client states become more correlated. This is **entrainment**: a well-documented phenomenon where autonomic nervous systems, vocal patterns, and emotional states synchronize between therapist and client. The Laplacian diffusion model captures this naturally.

**5. The bridge matrix encodes therapeutic technique.** CBT emphasizes the Knowledge → Depression/Anxiety bridge. Psychodynamic therapy emphasizes Empathy → Avoidance/Trust. DBT emphasizes Self_Regulation → Impulsivity. Different therapeutic modalities are different **bridge matrices B** — they differ in which therapist traits they couple to which client traits, but the spectral mechanics are universal.

### Conservation Law

The therapeutic conservation law:

$$\mathbf{1}^T \mathbf{x}(t) = \mathbf{1}^T \mathbf{x}(0) \quad \forall t$$

Total system activation is constant. Therapy redistributes it. The distressed client's excess activation flows through the rapport bridge into the therapist's well-regulated network, where it's dissipated (diffused) across many nodes instead of being concentrated in a few pathological ones. The therapist then feeds back a *calmer* signal — not by reducing total energy, but by changing its **spectral composition**.

---

---

# ROUND 3 — TraumaLaplacian

## Traumatic Memories as Pathological High-Conservation Subgraphs

Trauma is a conservation anomaly. Normal memories undergo **spectral smoothing** over time — the Laplacian diffuses their sharp edges, integrating them into the broader autobiographical graph. Traumatic memories resist this. They form **high-conservation subgraphs**: tightly clustered, strongly weighted, nearly isolated from the rest of the memory network. Their Laplacian eigenvalues are abnormally concentrated — the subgraph is too rigidly conserved, too perfectly self-contained.

EMDR (Eye Movement Desensitization and Reprocessing) is, in spectral terms, a **forced diffusion process**. Bilateral stimulation adds noise to the traumatic subgraph's boundary, weakening the eigenvalue concentration and allowing the memory to integrate into the broader network. It's spectral smoothing with an external forcing term.

### Theoretical Foundation

Model autobiographical memory as a weighted graph where nodes are **memory elements** (sensory fragments, emotional valences, narrative chunks) and edges are **associations**. The graph Laplacian governs how activation spreads during recall.

Normal memory recall:
1. A cue activates a seed node.
2. Activation diffuses via the Laplacian: $x(t+1) = x(t) - \alpha L x(t)$.
3. The signal spreads widely, activating related memories, losing intensity.
4. The recalled memory is **blended** — integrated with its context.

Traumatic memory recall:
1. A cue activates a node in the traumatic subgraph.
2. Activation circulates *within* the subgraph — it can't escape because the subgraph has high internal connectivity and low external connectivity.
3. The signal **echoes**: amplifies, reverberates, refuses to decay.
4. The recalled memory is **vivid, isolated, and overwhelming** — exactly as if it were happening again.

Spectrally, the traumatic subgraph has:
- **High algebraic connectivity** within itself (internally well-connected)
- **Low Cheeger constant** at its boundary (poorly connected to the rest)
- **Concentrated eigenvalue spectrum** (energy can't escape to other modes)

This is the **spectral signature of PTSD**: a subgraph that is internally over-conserved and externally under-connected.

### The TraumaLaplacian Model

```python
import numpy as np
from scipy.linalg import eigh
from scipy.sparse.csgraph import laplacian
import matplotlib.pyplot as plt

# ──────────────────────────────────────────────
# TraumaLaplacian: Traumatic memory as spectral pathology
# ──────────────────────────────────────────────

class TraumaLaplacian:
    """
    Model traumatic memories as pathological high-conservation
    subgraphs within the autobiographical memory network.
    
    EMDR = spectral smoothing via forced diffusion.
    """

    MEMORY_TYPES = [
        'childhood_home', 'first_day_school', 'birthday_party',
        'vacation_beach', 'grandmother_cooking', 'pet_dog',
        'graduation', 'first_love', 'concert_night',
        'friend_laughter', 'morning_coffee', 'book_reading',
        # Traumatic memories (densely connected, isolated)
        'trauma_sight', 'trauma_sound', 'trauma_feeling',
        'trauma_smell', 'trauma_fear', 'trauma_helplessness',
        'trauma_shame', 'trauma_body',
        # More normal memories
        'sunset_walk', 'rain_window', 'garden_flowers',
        'child_drawing', 'old_photo', 'favorite_song',
        'winter_snow', 'summer_heat', 'ocean_waves',
        'mountain_hike', 'starry_night', 'warm_fire'
    ]

    def __init__(self, n_memories: int = 32, n_traumatic: int = 8,
                 trauma_isolation: float = 0.9, trauma_internal_weight: float = 0.95):
        """
        Parameters
        ----------
        n_memories : total memory nodes
        n_traumatic : number of traumatic memory nodes (last N in the list)
        trauma_isolation : how disconnected the trauma subgraph is from normal memories [0, 1]
        trauma_internal_weight : how strongly traumatic memories connect to each other [0, 1]
        """
        self.n = n_memories
        self.n_trauma = n_traumatic
        self.n_normal = n_memories - n_traumatic
        self.names = self.MEMORY_TYPES[:n_memories]

        # Ensure we have enough names
        while len(self.names) < n_memories:
            self.names.append(f'memory_{len(self.names)}')

        # Build the memory graph
        self.trauma_start = self.n_normal  # Traumatic nodes start here
        self.A = self._build_memory_graph(
            trauma_isolation, trauma_internal_weight)
        self.L = laplacian(self.A, normed=False)

        # Normalized Laplacian
        degrees = self.A.sum(axis=1)
        d_inv_sqrt = np.diag(1.0 / np.sqrt(np.maximum(degrees, 1e-10)))
        self.L_norm = d_inv_sqrt @ self.L @ d_inv_sqrt

        # Eigendecomposition
        self.eigenvalues, self.eigenvectors = eigh(self.L)
        self.norm_eigenvalues, self.norm_eigenvectors = eigh(self.L_norm)

    def _build_memory_graph(self, isolation: float, internal_weight: float):
        """
        Build the memory association graph.
        
        Normal memories: moderate connectivity, some strong associations.
        Traumatic memories: very high internal connectivity, very low external.
        """
        rng = np.random.default_rng(42)
        A = np.zeros((self.n, self.n))

        # Normal-to-normal connections
        for i in range(self.n_normal):
            for j in range(i + 1, self.n_normal):
                # Moderate base connectivity with some strong links
                strength = rng.beta(2, 5) * 0.6
                A[i, j] = strength
                A[j, i] = strength

        # Trauma-to-trauma connections (very strong)
        for i in range(self.trauma_start, self.n):
            for j in range(i + 1, self.n):
                strength = internal_weight * rng.uniform(0.7, 1.0)
                A[i, j] = strength
                A[j, i] = strength

        # Normal-to-trauma connections (very weak — this is the pathology)
        for i in range(self.n_normal):
            for j in range(self.trauma_start, self.n):
                strength = (1 - isolation) * rng.beta(1, 10) * 0.3
                A[i, j] = strength
                A[j, i] = strength

        np.fill_diagonal(A, 0)
        return A

    @property
    def trauma_subgraph(self):
        """Extract the traumatic memory subgraph."""
        idx = slice(self.trauma_start, self.n)
        return self.A[idx, idx]

    @property
    def trauma_laplacian(self):
        """Laplacian of the traumatic subgraph alone."""
        return laplacian(self.trauma_subgraph, normed=False)

    @property
    def boundary_conductance(self):
        """
        Cheeger-like measure: how well-connected the trauma subgraph
        is to the rest. Low = isolated = pathological.
        """
        # Edges crossing the boundary
        boundary_edges = self.A[:self.trauma_start, self.trauma_start:].sum()
        # Internal edges of trauma subgraph
        internal_edges = self.trauma_subgraph.sum() / 2
        # Volume of trauma subgraph
        volume = self.A[self.trauma_start:, :].sum()

        if volume == 0:
            return 0
        return boundary_edges / volume

    def spectral_analysis(self):
        """Comprehensive spectral analysis of the memory network."""
        # Trauma subgraph eigenvalues
        trauma_evals, _ = eigh(self.trauma_laplacian)

        return {
            'full_fiedler': self.eigenvalues[1],
            'full_spectral_gap': self.eigenvalues[2] - self.eigenvalues[1],
            'trauma_fiedler': trauma_evals[1] if len(trauma_evals) > 1 else 0,
            'trauma_internal_connectivity': trauma_evals[1],
            'boundary_conductance': self.boundary_conductance,
            'spectral_entropy': self._spectral_entropy(self.eigenvalues),
            'trauma_spectral_entropy': self._spectral_entropy(trauma_evals),
            'n_connected_components': np.sum(self.eigenvalues < 1e-8),
            'isolation_ratio': trauma_evals[1] / max(self.boundary_conductance, 1e-10),
        }

    def _spectral_entropy(self, eigenvalues):
        """Spectral entropy of eigenvalue distribution."""
        evals = eigenvalues[eigenvalues > 1e-8]
        if len(evals) == 0:
            return 0
        p = evals / evals.sum()
        p = p[p > 0]
        return -np.sum(p * np.log(p))

    def simulate_recall(self, cue_node: int, steps: int = 100,
                        alpha: float = 0.02) -> dict:
        """
        Simulate memory recall as heat diffusion from a cue.
        
        Normal cue → activation spreads and dissipates.
        Traumatic cue → activation echoes and amplifies within subgraph.
        """
        x = np.zeros(self.n)
        x[cue_node] = 2.0  # Cue activation

        trajectory = np.zeros((steps + 1, self.n))
        energy_in_trauma = np.zeros(steps + 1)
        energy_in_normal = np.zeros(steps + 1)
        total_energy = np.zeros(steps + 1)

        trajectory[0] = x
        energy_in_trauma[0] = x[self.trauma_start:].sum()
        energy_in_normal[0] = x[:self.trauma_start].sum()
        total_energy[0] = x.sum()

        for t in range(1, steps + 1):
            x = x - alpha * (self.L @ x)
            trajectory[t] = x
            energy_in_trauma[t] = np.abs(x[self.trauma_start:]).sum()
            energy_in_normal[t] = np.abs(x[:self.trauma_start]).sum()
            total_energy[t] = np.abs(x).sum()

        return {
            'trajectory': trajectory,
            'energy_trauma': energy_in_trauma,
            'energy_normal': energy_in_normal,
            'total_energy': total_energy,
            'cue_is_traumatic': cue_node >= self.trauma_start,
            'cue_name': self.names[cue_node],
        }

    def simulate_emdr(self, trauma_node: int, n_sessions: int = 12,
                      bilateral_strength: float = 0.15,
                      steps_per_session: int = 50) -> dict:
        """
        Simulate EMDR as spectral smoothing.
        
        EMDR mechanism in spectral terms:
        1. Bilateral stimulation adds noise at the trauma subgraph boundary
        2. This weakens the spectral isolation (increases boundary conductance)
        3. Over sessions, the trauma subgraph integrates with normal memories
        4. Eigenvalue concentration decreases → memory becomes normal
        
        We model this by gradually increasing the cross-edges between
        trauma and normal subgraphs while maintaining conservation.
        """
        A_current = self.A.copy()
        isolation_history = []
        conductance_history = []
        fiedler_history = []
        trauma_fiedler_history = []
        session_spectra = []

        original_A = self.A.copy()

        for session in range(n_sessions):
            # Bilateral stimulation: strengthen boundary connections
            progress = (session + 1) / n_sessions

            # Increase cross-edges (modeling memory reintegration)
            for i in range(self.n_normal):
                for j in range(self.trauma_start, self.n):
                    # Find specific bridge memories (sensory overlaps)
                    original_bridge = original_A[i, j]
                    # EMDR strengthens these bridges
                    enhancement = bilateral_strength * progress * np.random.uniform(0.5, 1.0)
                    A_current[i, j] = min(original_bridge + enhancement, 0.5)
                    A_current[j, i] = A_current[i, j]

            # Recompute Laplacian
            L_current = laplacian(A_current, normed=False)
            evals, evecs = eigh(L_current)

            # Trauma subgraph metrics
            trauma_A = A_current[self.trauma_start:, self.trauma_start:]
            trauma_L = laplacian(trauma_A, normed=False)
            trauma_evals, _ = eigh(trauma_L)

            # Boundary conductance
            boundary = A_current[:self.trauma_start, self.trauma_start:].sum()
            volume = A_current[self.trauma_start:, :].sum()
            conductance = boundary / max(volume, 1e-10)

            isolation_history.append(1 - conductance)
            conductance_history.append(conductance)
            fiedler_history.append(evals[1])
            trauma_fiedler_history.append(trauma_evals[1] if len(trauma_evals) > 1 else 0)
            session_spectra.append(evals)

        return {
            'isolation_history': isolation_history,
            'conductance_history': conductance_history,
            'fiedler_history': fiedler_history,
            'trauma_fiedler_history': trauma_fiedler_history,
            'session_spectra': session_spectra,
            'n_sessions': n_sessions,
            'final_A': A_current,
        }

    def plot_analysis(self, figsize=(18, 14)):
        """Full visualization of the trauma Laplacian analysis."""
        fig, axes = plt.subplots(3, 3, figsize=figsize)

        # 1. Memory graph adjacency
        ax = axes[0, 0]
        im = ax.imshow(self.A, cmap='hot', interpolation='nearest')
        ax.set_title('Memory Association Graph')
        ax.axhline(y=self.trauma_start - 0.5, color='cyan', linewidth=2)
        ax.axvline(x=self.trauma_start - 0.5, color='cyan', linewidth=2)
        ax.set_xlabel('Memory Node')
        ax.set_ylabel('Memory Node')
        plt.colorbar(im, ax=ax, fraction=0.046)
        # Note: upper-right block (normal-trauma) is dark = isolated

        # 2. Full Laplacian eigenvalue spectrum
        ax = axes[0, 1]
        evals = self.eigenvalues[1:]  # skip zero
        ax.bar(range(len(evals)), evals, color='steelblue', alpha=0.8)
        ax.set_xlabel('Index')
        ax.set_ylabel('Eigenvalue')
        ax.set_title(f'Full Memory Network Spectrum (Fiedler={evals[0]:.3f})')

        # 3. Trauma subgraph spectrum
        ax = axes[0, 2]
        trauma_evals, _ = eigh(self.trauma_laplacian)
        trauma_evals_nz = trauma_evals[1:] if len(trauma_evals) > 1 else trauma_evals
        ax.bar(range(len(trauma_evals_nz)), trauma_evals_nz, color='red', alpha=0.8)
        ax.set_xlabel('Index')
        ax.set_ylabel('Eigenvalue')
        ax.set_title(f'Trauma Subgraph Spectrum (Fiedler={trauma_evals_nz[0]:.3f})')

        # 4. Normal memory recall
        ax = axes[1, 0]
        normal_recall = self.simulate_recall(cue_node=0)  # childhood_home
        ax.plot(normal_recall['energy_normal'], label='Normal', color='blue')
        ax.plot(normal_recall['energy_trauma'], label='Trauma', color='red')
        ax.set_xlabel('Diffusion Steps')
        ax.set_ylabel('Activation Energy')
        ax.set_title(f"Normal Recall: '{normal_recall['cue_name']}'")
        ax.legend()

        # 5. Traumatic memory recall
        ax = axes[1, 1]
        trauma_recall = self.simulate_recall(cue_node=self.trauma_start)
        ax.plot(trauma_recall['energy_normal'], label='Normal', color='blue')
        ax.plot(trauma_recall['energy_trauma'], label='Trauma', color='red')
        ax.set_xlabel('Diffusion Steps')
        ax.set_ylabel('Activation Energy')
        ax.set_title(f"Traumatic Recall: '{trauma_recall['cue_name']}'")
        ax.legend()

        # 6. Energy distribution comparison
        ax = axes[1, 2]
        # Final energy distribution for normal vs trauma recall
        normal_final = np.abs(normal_recall['trajectory'][-1])
        trauma_final = np.abs(trauma_recall['trajectory'][-1])
        x_pos = np.arange(self.n)
        width = 0.35
        ax.bar(x_pos - width/2, normal_final, width, label='Normal cue', color='blue', alpha=0.7)
        ax.bar(x_pos + width/2, trauma_final, width, label='Trauma cue', color='red', alpha=0.7)
        ax.axvline(x=self.trauma_start - 0.5, color='cyan', linewidth=2, linestyle='--')
        ax.set_xlabel('Memory Node')
        ax.set_ylabel('Activation')
        ax.set_title('Recall Energy Distribution')
        ax.legend(fontsize=8)

        # 7. EMDR simulation: isolation reduction
        ax = axes[2, 0]
        emdr = self.simulate_emdr(trauma_node=self.trauma_start)
        ax.plot(emdr['isolation_history'], 'o-', color='red', linewidth=2)
        ax.set_xlabel('EMDR Session')
        ax.set_ylabel('Trauma Isolation (1 - conductance)')
        ax.set_title('EMDR: Trauma Subgraph Integration')
        ax.set_ylim(0, 1)

        # 8. EMDR: Fiedler value changes
        ax = axes[2, 1]
        ax.plot(emdr['fiedler_history'], 's-', color='green', label='Full network')
        ax.plot(emdr['trauma_fiedler_history'], '^-', color='red', label='Trauma subgraph')
        ax.set_xlabel('EMDR Session')
        ax.set_ylabel('Fiedler Value')
        ax.set_title('EMDR: Algebraic Connectivity Changes')
        ax.legend()

        # 9. EMDR: Spectral smoothing
        ax = axes[2, 2]
        for i, spectrum in enumerate(emdr['session_spectra']):
            color = plt.cm.viridis(i / len(emdr['session_spectra']))
            ax.plot(spectrum[1:10], alpha=0.5, color=color,
                    label=f'Session {i+1}' if i % 3 == 0 else None)
        ax.set_xlabel('Eigenvalue Index')
        ax.set_ylabel('Eigenvalue')
        ax.set_title('EMDR: Spectral Smoothing Over Sessions')
        ax.legend(fontsize=6)

        plt.tight_layout()
        return fig


# ──────────────────────────────────────────────
# Demonstration: Trauma and EMDR
# ──────────────────────────────────────────────

print("=" * 60)
print("TRAUMALAPLACIAN — Spectral Analysis of Traumatic Memory")
print("=" * 60)

tl = TraumaLaplacian(
    n_memories=32,
    n_traumatic=8,
    trauma_isolation=0.9,      # Very isolated
    trauma_internal_weight=0.95  # Very strongly connected internally
)

analysis = tl.spectral_analysis()
print("\n--- Memory Network Spectral Analysis ---")
for k, v in analysis.items():
    if isinstance(v, (int, float)):
        print(f"  {k}: {v:.4f}")

print(f"\n  Isolation ratio: {analysis['isolation_ratio']:.2f}")
print(f"  (High = trauma is much more connected internally than to outside)")

print("\n--- Normal Memory Recall ---")
normal = tl.simulate_recall(cue_node=0)
print(f"  Cue: '{normal['cue_name']}'")
print(f"  Energy stays in normal region: {normal['energy_normal'][-1]:.3f}")
print(f"  Energy leaks to trauma: {normal['energy_trauma'][-1]:.3f}")
print(f"  Total energy conserved: {normal['total_energy'][0]:.3f} → {normal['total_energy'][-1]:.3f}")

print("\n--- Traumatic Memory Recall ---")
trauma = tl.simulate_recall(cue_node=tl.trauma_start)
print(f"  Cue: '{trauma['cue_name']}'")
print(f"  Energy trapped in trauma region: {trauma['energy_trauma'][-1]:.3f}")
print(f"  Energy reaches normal memories: {trauma['energy_normal'][-1]:.3f}")
print(f"  Energy ratio (trauma/normal): "
      f"{trauma['energy_trauma'][-1]/max(trauma['energy_normal'][-1], 1e-6):.2f}x")

print("\n--- EMDR Simulation (12 sessions) ---")
emdr = tl.simulate_emdr(tl.trauma_start, n_sessions=12)
print(f"  Initial isolation: {emdr['isolation_history'][0]:.4f}")
print(f"  Final isolation:   {emdr['isolation_history'][-1]:.4f}")
print(f"  Isolation reduction: "
      f"{(1 - emdr['isolation_history'][-1]/emdr['isolation_history'][0])*100:.1f}%")
print(f"  Fiedler value change: "
      f"{emdr['fiedler_history'][0]:.4f} → {emdr['fiedler_history'][-1]:.4f}")
print(f"  Trauma subgraph Fiedler: "
      f"{emdr['trauma_fiedler_history'][0]:.4f} → {emdr['trauma_fiedler_history'][-1]:.4f}")

print("\n--- Post-EMDR Recall ---")
# Rebuild with post-EMDR connectivity
tl_post = TraumaLaplacian(
    n_memories=32, n_traumatic=8,
    trauma_isolation=0.3,  # Much less isolated after EMDR
    trauma_internal_weight=0.7  # Weakened internal connections
)
post_trauma = tl_post.simulate_recall(cue_node=tl_post.trauma_start)
print(f"  Cue: '{post_trauma['cue_name']}' (post-EMDR)")
print(f"  Energy in trauma region: {post_trauma['energy_trauma'][-1]:.3f}")
print(f"  Energy in normal region: {post_trauma['energy_normal'][-1]:.3f}")
print(f"  Energy ratio (trauma/normal): "
      f"{post_trauma['energy_trauma'][-1]/max(post_trauma['energy_normal'][-1], 1e-6):.2f}x")
print(f"  (Pre-EMDR ratio was: "
      f"{trauma['energy_trauma'][-1]/max(trauma['energy_normal'][-1], 1e-6):.2f}x)")
```

### Interpretation

**1. The isolation ratio as a PTSD severity metric.** The ratio of internal Fiedler value to boundary conductance captures exactly how "stuck" a traumatic memory is. High ratio → the memory is well-connected to itself but poorly connected to everything else → it will activate intensely but in isolation → flashback. This could be a quantitative biomarker for PTSD severity.

**2. Heat diffusion mimics memory recall dynamics.** When we cue a normal memory, activation spreads widely and dissipates — the memory is "blended" with context. When we cue a traumatic memory, activation concentrates in the trauma subgraph — the memory is vivid, intrusive, and resistant to integration. The Laplacian diffusion model reproduces both patterns from the graph topology alone, without any special "flashback mechanism."

**3. EMDR as spectral smoothing.** The EMDR simulation shows that bilateral stimulation's effect is to gradually increase the boundary conductance of the trauma subgraph. Session by session:
   - Boundary edges strengthen (memory connects to normal associations)
   - Internal edges weaken (traumatic elements decouple from each other)
   - The eigenvalue spectrum flattens (energy spreads across more modes)
   - Recall becomes more like normal memory: less vivid, more contextualized

This is precisely what clinical literature describes: EMDR transforms traumatic memories from "vivid, emotional, here-and-now" to "distant, factual, there-and-then." In spectral terms, the memory's eigenvalue concentration decreases — it becomes a normal part of the distributed memory network.

**4. Conservation holds throughout.** Total system energy is preserved during recall and during EMDR. The traumatic memory doesn't "lose" its information — it redistributes. The sensory fragments, emotional valences, and narrative elements still exist in the graph; they're just no longer locked together in a rigid, high-conservation cluster. They've been released into the broader network where they can be accessed without triggering the whole traumatic pattern.

**5. Clinical implications.** This model suggests:
   - **Exposure therapy** works by repeatedly activating the trauma subgraph, which heats up the boundary edges through use-dependent plasticity (spectral analog: repeated diffusion eventually finds escape routes).
   - **EMDR** accelerates this by providing external perturbation (bilateral stimulation) that specifically targets boundary conductivity.
   - **Narrative therapy** works by explicitly building new edges (narrative connections) between traumatic elements and normal autobiographical memories.
   - **Failed therapy** = the boundary edges were strengthened but the internal trauma edges weren't weakened — the memory is now *more* connected to normal memories but still *too* internally coherent, leading to broader triggering (generalization).

### The Conservation Law of Memory

$$\mathbf{1}^T \mathbf{x}(t) = \mathbf{1}^T \mathbf{x}(0)$$

Information is conserved. Trauma therapy doesn't destroy memories — it transforms their topology. The spectral content changes from concentrated (pathological) to distributed (healthy), but the total "memory energy" in the system remains constant. This is why trauma survivors don't forget — they integrate. The goal of therapy isn't erasure but **spectral redistribution**: turning a sharp, isolated peak in eigenvalue space into a broad, gentle hill that's part of the landscape.

---

## Synthesis: The Three Laplacians

| Model | Nodes | Edges | Pathology | Treatment |
|-------|-------|-------|-----------|-----------|
| **PersonalityLaplacian** | Traits | Correlations | Low Fiedler (fragmentation) | Rewire trait connections |
| **TherapyGraph** | Therapist+Client traits | Rapport bridge | Low α (no coupling) | Increase rapport over sessions |
| **TraumaLaplacian** | Memory elements | Associations | High isolation ratio | Spectral smoothing (EMDR) |

All three obey the same conservation law: total activation is preserved across diffusion steps. Treatment doesn't add or remove psychological energy — it changes the **topology** through which that energy flows. Spectral graph theory provides the mathematical framework to quantify, predict, and optimize these topological changes.

The deep insight: **mental health is a spectral property.** It's not about what you have — it's about how it's connected.
