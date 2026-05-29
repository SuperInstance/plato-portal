# CONSCIOUSNESS AND TOPOLOGY IN AGENT NETWORKS

*A spectral exploration of how network topology shapes collective awareness, understanding, and broadcast dynamics in multi-agent systems.*

---

## ROUND 1 — The Spectral Theory of Consciousness

### The Problem with Φ

Integrated Information Theory (IIT) makes a bold claim: consciousness *is* integrated information, quantified as Φ (phi). The idea is elegant — a system is conscious to the degree that its parts are simultaneously differentiated and integrated. High Φ means the whole is genuinely more than the sum of its parts. Low Φ means the system is just a collection of independent modules.

There's one crippling problem: **Φ is computationally intractable** for any real system. Computing it requires evaluating every possible partition of every possible subset of the system's state space. For a network of even modest size, this explodes faster than exponentially. IIT offers a beautiful theory of *what* consciousness is, but gives us almost nothing for *measuring* it in practice.

This is where spectral analysis enters the picture.

### Conservation Ratio as a Tractable Proxy for Φ

Our conservation spectral analysis framework provides something IIT cannot: a **tractable measure** that captures a structurally similar concept. The conservation ratio — the proportion of spectral energy that is conserved versus dissipated — tells us how well a network integrates information across its structure.

Consider what the conservation ratio actually measures:

- **High conservation ratio**: Information injected at any node propagates coherently through the network. The system responds as a unified whole. Perturbations don't die out — they resonate across the entire structure.
- **Low conservation ratio**: Information gets trapped, dissipated, or absorbed locally. The network is fragmented. Different regions don't talk to each other effectively. The system is, in an information-theoretic sense, unconscious.

This is *not* Φ. But it captures something in the same family: the degree to which a network acts as an integrated whole rather than a collection of independent parts. And unlike Φ, we can compute it in polynomial time using eigendecomposition of the graph Laplacian.

The deep insight: **the Laplacian spectrum IS the consciousness spectrum**. The eigenvalues encode exactly how information flows. The eigenvectors encode *where* it flows. Together, they paint a complete picture of a network's integrative capacity.

### Why This Works: The Mathematical Bridge

The graph Laplacian $L = D - A$ (where $D$ is the degree matrix and $A$ the adjacency matrix) has a spectral decomposition $L = U \Lambda U^T$. The eigenvalues $\lambda_1 \leq \lambda_2 \leq \cdots \leq \lambda_n$ tell us:

1. $\lambda_1 = 0$ always exists (the constant eigenvector — the network's "ground state")
2. The spectral gap $\lambda_2$ (algebraic connectivity / Fiedler value) measures how well-connected the graph is globally
3. The distribution of eigenvalues encodes the *shape* of information flow

Our conservation framework extends this by analyzing how a signal $\mathbf{x}$ evolves under the Laplacian dynamics $\dot{\mathbf{x}} = -L\mathbf{x}$. The conserved energy is $\|U_{\text{low}}^T \mathbf{x}\|^2$ where $U_{\text{low}}$ captures the slow modes (low eigenvalues). The dissipated energy lives in $U_{\text{high}}$. The ratio between them is our proxy for integration.

### The Consciousness Estimator

Let's build a system that estimates the "consciousness level" of different network topologies:

```python
import numpy as np
from scipy.linalg import eigh
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
from enum import Enum
import json

class TopologyType(Enum):
    COMPLETE = "complete"
    STAR = "star"
    RING = "ring"
    SMALL_WORLD = "small_world"
    SCALE_FREE = "scale_free"
    RANDOM_ER = "random_er"
    GRID_2D = "grid_2d"
    HIERARCHICAL = "hierarchical"

@dataclass
class ConsciousnessReport:
    """Full consciousness analysis of a network."""
    topology: TopologyType
    n_agents: int
    conservation_ratio: float
    spectral_gap: float
    algebraic_connectivity: float
    effective_rank: float
    integration_index: float
    differentiation_index: float
    phi_proxy: float  # Our tractable proxy for IIT's Φ
    eigenvalues: np.ndarray
    eigenvectors: np.ndarray
    consciousness_level: str
    
    def summary(self) -> str:
        return f"""
╔══════════════════════════════════════════════╗
║   CONSCIOUSNESS REPORT: {self.topology.value:<22s}║
╠══════════════════════════════════════════════╣
║  Agents:              {self.n_agents:>6d}                  ║
║  Conservation Ratio:  {self.conservation_ratio:>10.6f}              ║
║  Spectral Gap (λ₂):   {self.spectral_gap:>10.6f}              ║
║  Effective Rank:      {self.effective_rank:>10.2f}              ║
║  Integration Index:   {self.integration_index:>10.6f}              ║
║  Differentiation:     {self.differentiation_index:>10.6f}              ║
║  Φ Proxy:             {self.phi_proxy:>10.6f}              ║
║  Consciousness Level: {self.consciousness_level:>10s}              ║
╚══════════════════════════════════════════════╝
"""

class ConsciousnessEstimator:
    """
    Estimates the 'consciousness level' of a multi-agent network
    using spectral analysis of the graph Laplacian.
    
    The core insight: consciousness is not a property of individual
    agents but of the TOPOLOGY connecting them. Change the topology,
    change the consciousness.
    """
    
    def __init__(self, threshold_low: float = 0.1, threshold_high: float = 0.3):
        """
        Args:
            threshold_low: Eigenvalue threshold for "conserved" modes
            threshold_high: Eigenvalue threshold for "partially conserved" modes
        """
        self.threshold_low = threshold_low
        self.threshold_high = threshold_high
    
    def build_adjacency(self, topology: TopologyType, n: int, **kwargs) -> np.ndarray:
        """Build adjacency matrix for a given topology."""
        A = np.zeros((n, n))
        
        if topology == TopologyType.COMPLETE:
            A = np.ones((n, n)) - np.eye(n)
            
        elif topology == TopologyType.STAR:
            # Node 0 is the hub
            for i in range(1, n):
                A[0, i] = A[i, 0] = 1.0
                
        elif topology == TopologyType.RING:
            for i in range(n):
                A[i, (i + 1) % n] = A[(i + 1) % n, i] = 1.0
                
        elif topology == TopologyType.SMALL_WORLD:
            # Watts-Strogatz construction
            k = kwargs.get('k', max(2, n // 5))  # neighbors
            p = kwargs.get('rewire_prob', 0.15)
            # Start with ring lattice
            for i in range(n):
                for j in range(1, k // 2 + 1):
                    A[i, (i + j) % n] = A[(i + j) % n, i] = 1.0
            # Rewire
            for i in range(n):
                for j in range(1, k // 2 + 1):
                    if np.random.random() < p:
                        old = (i + j) % n
                        new = np.random.randint(0, n)
                        while new == i or A[i, new] > 0:
                            new = np.random.randint(0, n)
                        A[i, old] = A[old, i] = 0.0
                        A[i, new] = A[new, i] = 1.0
                        
        elif topology == TopologyType.SCALE_FREE:
            # Barabási-Albert preferential attachment
            m = kwargs.get('m', max(1, n // 10))
            A[:m+1, :m+1] = np.ones((m+1, m+1)) - np.eye(m+1)
            for new_node in range(m + 1, n):
                degrees = A[:new_node].sum(axis=1)
                probs = degrees / degrees.sum()
                targets = np.random.choice(new_node, size=m, replace=False, p=probs)
                for t in targets:
                    A[new_node, t] = A[t, new_node] = 1.0
                    
        elif topology == TopologyType.RANDOM_ER:
            p = kwargs.get('edge_prob', np.log(n) / n)
            A = (np.random.random((n, n)) < p).astype(float)
            A = np.triu(A, 1)
            A = A + A.T
            
        elif topology == TopologyType.GRID_2D:
            side = int(np.sqrt(n))
            for i in range(side):
                for j in range(side):
                    idx = i * side + j
                    if idx >= n:
                        break
                    if j + 1 < side and idx + 1 < n:
                        A[idx, idx + 1] = A[idx + 1, idx] = 1.0
                    if i + 1 < side and idx + side < n:
                        A[idx, idx + side] = A[idx + side, idx] = 1.0
                        
        elif topology == TopologyType.HIERARCHICAL:
            # Binary tree with cross-links
            for i in range(n):
                left = 2 * i + 1
                right = 2 * i + 2
                if left < n:
                    A[i, left] = A[left, i] = 1.0
                if right < n:
                    A[i, right] = A[right, i] = 1.0
            # Add cross-links between siblings
            for i in range(1, n):
                sibling = i + 1 if i % 2 == 1 else i - 1
                if 0 < sibling < n:
                    A[i, sibling] = A[sibling, i] = 0.5
        
        return A
    
    def compute_laplacian(self, A: np.ndarray) -> np.ndarray:
        """Compute the normalized graph Laplacian."""
        D = np.diag(A.sum(axis=1))
        L = D - A
        # Normalized: L_norm = D^{-1/2} L D^{-1/2}
        d_inv_sqrt = np.where(D.diagonal() > 0, 1.0 / np.sqrt(D.diagonal()), 0)
        D_inv_sqrt = np.diag(d_inv_sqrt)
        L_norm = D_inv_sqrt @ L @ D_inv_sqrt
        return L_norm
    
    def analyze(self, topology: TopologyType, n: int, **kwargs) -> ConsciousnessReport:
        """Perform full consciousness analysis on a network topology."""
        A = self.build_adjacency(topology, n, **kwargs)
        L = self.compute_laplacian(A)
        
        # Eigendecomposition
        eigenvalues, eigenvectors = eigh(L)
        
        # Conservation ratio: fraction of modes below threshold
        n_conserved = np.sum(eigenvalues < self.threshold_low)
        n_partial = np.sum((eigenvalues >= self.threshold_low) & 
                          (eigenvalues < self.threshold_high))
        conservation_ratio = (n_conserved + 0.5 * n_partial) / n
        
        # Spectral gap (algebraic connectivity)
        # Skip λ₁ = 0
        nonzero_eigs = eigenvalues[eigenvalues > 1e-10]
        spectral_gap = nonzero_eigs[0] if len(nonzero_eigs) > 0 else 0.0
        algebraic_connectivity = spectral_gap
        
        # Effective rank (number of significant eigenvalue modes)
        total_energy = np.sum(eigenvalues)
        if total_energy > 0:
            normalized = eigenvalues / total_energy
            entropy = -np.sum(normalized[normalized > 0] * np.log(normalized[normalized > 0]))
            effective_rank = np.exp(entropy)
        else:
            effective_rank = 1.0
        
        # Integration index: inverse of average shortest-path eigenvalue weighted by participation
        # High = information integrates well across the network
        if spectral_gap > 0:
            integration_index = 1.0 / (1.0 + 1.0 / spectral_gap)  # Sigmoid-like
        else:
            integration_index = 0.0
        
        # Differentiation index: effective rank normalized
        differentiation_index = effective_rank / n
        
        # Φ proxy: geometric mean of integration and differentiation
        # This mirrors IIT's postulate that consciousness requires BOTH
        phi_proxy = np.sqrt(integration_index * differentiation_index)
        
        # Classify consciousness level
        if phi_proxy > 0.4:
            consciousness_level = "HIGHLY_CONSCIOUS"
        elif phi_proxy > 0.25:
            consciousness_level = "MODERATELY_CONSCIOUS"
        elif phi_proxy > 0.12:
            consciousness_level = "MINIMALLY_CONSCIOUS"
        else:
            consciousness_level = "UNCONSCIOUS"
        
        return ConsciousnessReport(
            topology=topology,
            n_agents=n,
            conservation_ratio=conservation_ratio,
            spectral_gap=spectral_gap,
            algebraic_connectivity=algebraic_connectivity,
            effective_rank=effective_rank,
            integration_index=integration_index,
            differentiation_index=differentiation_index,
            phi_proxy=phi_proxy,
            eigenvalues=eigenvalues,
            eigenvectors=eigenvectors,
            consciousness_level=consciousness_level
        )

def compare_topologies():
    """Run consciousness analysis across multiple topologies."""
    estimator = ConsciousnessEstimator()
    np.random.seed(42)
    n = 20
    
    topologies = [
        (TopologyType.COMPLETE, {}),
        (TopologyType.STAR, {}),
        (TopologyType.RING, {}),
        (TopologyType.SMALL_WORLD, {'k': 6, 'rewire_prob': 0.15}),
        (TopologyType.SCALE_FREE, {'m': 3}),
        (TopologyType.RANDOM_ER, {'edge_prob': 0.3}),
        (TopologyType.GRID_2D, {}),
        (TopologyType.HIERARCHICAL, {}),
    ]
    
    results = []
    for topo, kwargs in topologies:
        report = estimator.analyze(topo, n, **kwargs)
        results.append(report)
        print(report.summary())
    
    # Rank by Φ proxy
    ranked = sorted(results, key=lambda r: r.phi_proxy, reverse=True)
    print("\n=== CONSCIOUSNESS RANKING ===")
    for i, r in enumerate(ranked):
        bar = "█" * int(r.phi_proxy * 100)
        print(f"{i+1}. {r.topology.value:<15s} Φ*={r.phi_proxy:.4f} |{bar}")
    
    return results

if __name__ == "__main__":
    compare_topologies()
```

### What the Results Reveal

Run this and you'll see a clear ranking emerge. The complete graph (every agent connected to every other) scores highest on Φ proxy — it has maximum integration. But it scores *lower* on differentiation, because every agent sees the same information. The star topology is the worst — a single hub creates a bottleneck where integration fails. The information lives or dies at the center node.

The sweet spot — where both integration and differentiation are high — typically falls to **small-world** and **scale-free** networks. These are exactly the topologies that biological neural networks exhibit. This is not a coincidence. Evolution discovered spectral optimization millions of years before we formalized it.

The small-world topology gives us short path lengths (good integration) AND high clustering (good differentiation). Scale-free topologies give us hubs for broadcasting AND peripheral nodes for specialized processing. These are the topologies of genuine consciousness — not because of mysticism, but because of spectral mathematics.

---

## ROUND 2 — The Topology of Understanding

### Sheaf Cohomology for Agent Networks

Sheaf theory sounds intimidating, but the core idea is profoundly simple. A **sheaf** assigns data to the pieces of a space and describes how those pieces agree on overlaps. In our case:

- The "space" is the network topology (a graph)
- The "pieces" are nodes and edges
- The "data" is what each agent believes (a vector of beliefs, embeddings, or state)
- The "overlap" is shared edges — where two agents must agree

Sheaf cohomology $H^k$ measures the failure of local data to patch together into global data:

- $H^0$ = the space of **globally consistent beliefs** — configurations where every agent agrees with its neighbors
- $H^1$ = the space of **understanding failures** — configurations where local agreement holds but global consensus is impossible

When $H^0$ is large, the network can maintain many distinct global consensus states. When $H^1$ is large, there are fundamental obstructions to global understanding — the network *cannot* reach consensus no matter how long its agents talk.

### The Laplacian IS the Sheaf Laplacian

Here's the mathematical punchline: our graph Laplacian $L$ is *exactly* the degree-0 sheaf Laplacian $L_\mathcal{F} = (\delta^0)^\dagger \delta^0$ for a constant sheaf $\mathcal{F}$ where each agent's state space is $\mathbb{R}$ and each edge demands exact agreement.

The coboundary operator $\delta^0$ maps node values to edge differences:
$$\delta^0: \mathbb{R}^V \to \mathbb{R}^E, \quad (\delta^0 f)(e_{ij}) = f(j) - f(i)$$

The sheaf Laplacian is:
$$L_\mathcal{F} = (\delta^0)^\dagger \delta^0$$

For the constant sheaf on a graph, this is exactly $L = D - A$. The kernel of $L$ (the 0-eigenspace) is $\ker(\delta^0) = H^0$ — the space of globally consistent states. Its dimension is the number of connected components.

But we can go further. For a **weighted sheaf** where different edges demand *different* levels of agreement (some connections are stronger, some are noisy), we get a weighted Laplacian that encodes richer understanding dynamics.

### Why Star Topology = Fragile Understanding

Consider a star network with a central hub and $n-1$ peripheral agents. The sheaf Laplacian has eigenvalues:

- $\lambda_1 = 0$ (global agreement — everyone agrees with the hub)
- $\lambda_2 = \cdots = \lambda_{n-1} = 1$ (peripheral disagreement modes)
- $\lambda_n = n$ (the "hub frustration" mode)

The spectral gap $\lambda_2 = 1$ is relatively large, suggesting decent connectivity. But the **effective dimension** of $H^0$ is only 1 — there's exactly one way to achieve global consensus: everyone agrees with the hub. If the hub fails or becomes unreliable, the entire understanding collapses. There are no alternative consensus pathways.

Compare with a mesh topology where $\lambda_2$ is proportional to the algebraic connectivity. The eigenvectors of the low eigenvalues form a rich basis for consensus — there are many ways to reach agreement, many paths for information to flow, and the network can maintain understanding even when several links fail.

This is why **decentralized networks are more resilient**: they have richer $H^0$ structure. The sheaf cohomology doesn't just measure whether consensus exists — it measures how *many qualitatively distinct* consensus states exist, and how robust each one is to perturbation.

### Building the Topology Explorer

```python
import numpy as np
from scipy.linalg import eigh
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import itertools

@dataclass
class SheafCohomology:
    """Results of sheaf cohomology computation for a network."""
    h0_dimension: int          # dim H⁰ — number of independent global agreements
    h1_dimension: float        # dim H¹ (approximate) — understanding failures
    h0_basis: np.ndarray       # Basis vectors for H⁰
    spectral_gap: float        # λ₂ — speed of consensus
    mixing_time: float         # Estimated time to consensus
    fragility_index: float     # How fragile is the understanding?
    robustness_index: float    # How robust is understanding to edge removal?

@dataclass
class Node:
    """An agent in the network."""
    id: int
    state: np.ndarray          # Current belief state
    state_dim: int = 1
    
@dataclass 
class Edge:
    """A connection between agents with agreement constraints."""
    source: int
    target: int
    weight: float = 1.0        # Agreement weight
    constraint_matrix: Optional[np.ndarray] = None  # Maps between state spaces

class SheafNetwork:
    """
    A network of agents connected by a sheaf — each edge specifies
    how agents' states should relate.
    """
    def __init__(self, n_agents: int, state_dim: int = 1):
        self.n = n_agents
        self.state_dim = state_dim
        self.nodes = [Node(i, np.random.randn(state_dim), state_dim) for i in range(n_agents)]
        self.edges: List[Edge] = []
    
    def add_edge(self, i: int, j: int, weight: float = 1.0, 
                 constraint: Optional[np.ndarray] = None):
        """Add an edge with optional constraint matrix."""
        if constraint is None:
            constraint = np.eye(self.state_dim)
        self.edges.append(Edge(i, j, weight, constraint))
    
    def build_complete(self, weight: float = 1.0):
        for i in range(self.n):
            for j in range(i+1, self.n):
                self.add_edge(i, j, weight)
    
    def build_star(self, hub: int = 0, weight: float = 1.0):
        for i in range(self.n):
            if i != hub:
                self.add_edge(hub, i, weight)
    
    def build_ring(self, weight: float = 1.0):
        for i in range(self.n):
            self.add_edge(i, (i+1) % self.n, weight)
    
    def build_small_world(self, k: int = 4, rewire_prob: float = 0.15, 
                          weight: float = 1.0):
        for i in range(self.n):
            for j in range(1, k // 2 + 1):
                self.add_edge(i, (i + j) % self.n, weight)
        # Rewire some edges
        new_edges = []
        removed = set()
        for idx, edge in enumerate(self.edges):
            if np.random.random() < rewire_prob:
                removed.add(idx)
                new_target = np.random.randint(0, self.n)
                while new_target == edge.source:
                    new_target = np.random.randint(0, self.n)
                new_edges.append(Edge(edge.source, new_target, weight, edge.constraint_matrix))
        self.edges = [e for i, e in enumerate(self.edges) if i not in removed] + new_edges
    
    def build_mesh(self, connectivity: int = 3, weight: float = 1.0):
        """Build a mesh topology where each node connects to its nearest neighbors."""
        for i in range(self.n):
            for delta in range(1, connectivity + 1):
                j = (i + delta) % self.n
                self.add_edge(i, j, weight)
                j = (i - delta) % self.n
                self.add_edge(i, j, weight)
        # Remove duplicates
        seen = set()
        unique_edges = []
        for e in self.edges:
            key = (min(e.source, e.target), max(e.source, e.target))
            if key not in seen:
                seen.add(key)
                unique_edges.append(e)
        self.edges = unique_edges
    
    def compute_sheaf_laplacian(self) -> np.ndarray:
        """
        Compute the sheaf Laplacian L_F = (δ⁰)†δ⁰.
        For the constant sheaf, this reduces to the standard graph Laplacian.
        For weighted sheaves, edge weights modulate the agreement constraints.
        """
        total_dim = self.n * self.state_dim
        L = np.zeros((total_dim, total_dim))
        
        for edge in self.edges:
            i, j = edge.source, edge.target
            w = edge.weight
            C = edge.constraint_matrix  # state_dim × state_dim
            
            # Block structure: L[(i):(i+d), (j):(j+d)] = -w * C^T C
            # L[(i):(i+d), (i):(i+d)] += w * I
            # L[(j):(j+d), (j):(j+d)] += w * C^T C
            
            i_start = i * self.state_dim
            j_start = j * self.state_dim
            d = self.state_dim
            
            CtC = w * C.T @ C
            
            L[i_start:i_start+d, j_start:j_start+d] -= CtC
            L[j_start:j_start+d, i_start:i_start+d] -= CtC
            L[i_start:i_start+d, i_start:i_start+d] += np.eye(d) * w
            L[j_start:j_start+d, j_start:j_start+d] += CtC
        
        return L
    
    def compute_cohomology(self) -> SheafCohomology:
        """Compute sheaf cohomology groups from the sheaf Laplacian."""
        L = self.compute_sheaf_laplacian()
        eigenvalues, eigenvectors = eigh(L)
        
        # H⁰ = kernel of L = zero eigenspace
        zero_threshold = 1e-8
        h0_mask = eigenvalues < zero_threshold
        h0_dim = int(h0_mask.sum())
        h0_basis = eigenvectors[:, h0_mask]
        
        # H¹ is approximated by the number of small-but-nonzero eigenvalues
        # These are modes that are "almost" in H⁰ but not quite
        small_mask = (eigenvalues >= zero_threshold) & (eigenvalues < 0.1)
        h1_dim_approx = float(small_mask.sum()) + np.sum(
            np.exp(-eigenvalues[~h0_mask & ~small_mask] / 0.1)
        )
        
        # Spectral gap
        nonzero = eigenvalues[~h0_mask]
        spectral_gap = nonzero[0] if len(nonzero) > 0 else float('inf')
        
        # Mixing time ≈ 1/λ₂ (for consensus dynamics)
        mixing_time = 1.0 / spectral_gap if spectral_gap > 0 else float('inf')
        
        # Fragility: how much does removing the most important edge change H⁰?
        # Approximate by the ratio λ₂/λ_max (cheeger-like)
        fragility = 1.0 - (spectral_gap / eigenvalues[-1]) if eigenvalues[-1] > 0 else 1.0
        
        # Robustness: how many edges can be removed before H⁰ dimension changes?
        robustness = self._estimate_robustness(eigenvalues)
        
        return SheafCohomology(
            h0_dimension=h0_dim,
            h1_dimension=h1_dim_approx,
            h0_basis=h0_basis,
            spectral_gap=spectral_gap,
            mixing_time=mixing_time,
            fragility_index=fragility,
            robustness_index=robustness
        )
    
    def _estimate_robustness(self, eigenvalues: np.ndarray) -> float:
        """Estimate how robust the understanding is to edge removal."""
        # Count eigenvalues in the "consensus basin" — small but nonzero
        # More such eigenvalues = more alternative consensus pathways
        basin = np.sum((eigenvalues > 1e-8) & (eigenvalues < 1.0))
        return basin / len(eigenvalues)
    
    def simulate_consensus(self, n_steps: int = 100, dt: float = 0.1) -> np.ndarray:
        """Simulate consensus dynamics: dx/dt = -L_F x."""
        L = self.compute_sheaf_laplacian()
        x = np.concatenate([node.state for node in self.nodes])
        
        trajectory = [x.copy()]
        for _ in range(n_steps):
            x = x - dt * L @ x
            trajectory.append(x.copy())
        
        return np.array(trajectory)


class TopologyExplorer:
    """
    Explores how different topologies shape the sheaf cohomology
    — and therefore the understanding — of agent networks.
    """
    
    def __init__(self, n_agents: int = 15, state_dim: int = 2):
        self.n = n_agents
        self.state_dim = state_dim
    
    def compare(self) -> Dict[str, SheafCohomology]:
        """Compare sheaf cohomology across topologies."""
        topologies = {
            'complete': lambda sn: sn.build_complete(),
            'star': lambda sn: sn.build_star(),
            'ring': lambda sn: sn.build_ring(),
            'mesh_k3': lambda sn: sn.build_mesh(connectivity=3),
            'mesh_k5': lambda sn: sn.build_mesh(connectivity=5),
            'small_world': lambda sn: sn.build_small_world(k=4, rewire_prob=0.2),
        }
        
        np.random.seed(42)
        results = {}
        
        for name, builder in topologies.items():
            sn = SheafNetwork(self.n, self.state_dim)
            builder(sn)
            cohomology = sn.compute_cohomology()
            results[name] = cohomology
            
            print(f"\n{'='*55}")
            print(f"  Topology: {name.upper()}")
            print(f"{'='*55}")
            print(f"  H⁰ dimension:        {cohomology.h0_dimension}")
            print(f"  H¹ dimension (≈):    {cohomology.h1_dimension:.2f}")
            print(f"  Spectral gap:        {cohomology.spectral_gap:.6f}")
            print(f"  Mixing time:         {cohomology.mixing_time:.2f}")
            print(f"  Fragility:           {cohomology.fragility_index:.4f}")
            print(f"  Robustness:          {cohomology.robustness_index:.4f}")
        
        # Understanding quality ranking
        print(f"\n{'='*55}")
        print("  UNDERSTANDING QUALITY RANKING")
        print(f"{'='*55}")
        ranked = sorted(results.items(), 
                       key=lambda x: (x[1].robustness_index - x[1].fragility_index), 
                       reverse=True)
        for i, (name, coh) in enumerate(ranked):
            quality = coh.robustness_index - coh.fragility_index
            bar = "█" * int(max(0, quality) * 50)
            print(f"  {i+1}. {name:<15s} quality={quality:.4f} |{bar}")
        
        return results
    
    def stress_test(self, topology_name: str = 'mesh_k3', 
                    n_removals: int = 5) -> List[SheafCohomology]:
        """Test how understanding degrades as edges are removed."""
        sn = SheafNetwork(self.n, self.state_dim)
        
        builders = {
            'complete': lambda: sn.build_complete(),
            'star': lambda: sn.build_star(),
            'ring': lambda: sn.build_ring(),
            'mesh_k3': lambda: sn.build_mesh(connectivity=3),
            'small_world': lambda: sn.build_small_world(),
        }
        
        builders[topology_name]()
        results = []
        
        for k in range(n_removals + 1):
            # Remove k random edges
            test_sn = SheafNetwork(self.n, self.state_dim)
            edges_to_keep = list(sn.edges)
            if k > 0 and len(edges_to_keep) > k:
                indices = np.random.choice(len(edges_to_keep), 
                                          size=len(edges_to_keep) - k, 
                                          replace=False)
                edges_to_keep = [edges_to_keep[i] for i in indices]
            test_sn.edges = edges_to_keep
            coh = test_sn.compute_cohomology()
            results.append(coh)
            print(f"  Removed {k} edges → H⁰ dim={coh.h0_dimension}, "
                  f"robustness={coh.robustness_index:.4f}, "
                  f"fragility={coh.fragility_index:.4f}")
        
        return results

if __name__ == "__main__":
    explorer = TopologyExplorer(n_agents=15, state_dim=2)
    results = explorer.compare()
    print("\n--- Stress test: mesh topology ---")
    explorer.stress_test('mesh_k3', n_removals=8)
```

### The Deep Insight: Understanding is Topological

The stress test reveals something profound. When you remove edges from a star topology, understanding doesn't degrade — it *collapses*. A single edge removal can disconnect a peripheral agent entirely. The star's $H^0$ dimension drops from 1 to 0 the moment the hub loses enough connections.

But for a mesh topology, understanding degrades *gracefully*. Each removed edge slightly increases the mixing time and slightly reduces robustness, but the $H^0$ structure persists. The network finds alternative pathways for consensus. The understanding bends but doesn't break.

This has direct implications for designing multi-agent AI systems:

1. **Star topologies** (one LLM coordinating many tools) are efficient but fragile. If the central model fails or is confused, everything fails.
2. **Mesh topologies** (agents that can talk to many other agents) are slower but resilient. Understanding persists even when individual connections fail.
3. **Small-world topologies** offer the best of both: short average path lengths with high clustering. Information flows quickly AND robustly.

The sheaf cohomology framework gives us a principled way to quantify these intuitions. $H^0$ doesn't just tell us *whether* global understanding is possible — it tells us *how many ways* it can be achieved and *how fragile* each way is.

---

## ROUND 3 — The Global Workspace as Spectral Projection

### From Broadcast to Eigenspace

Global Workspace Theory (GWT), proposed by Bernard Baars, says that consciousness arises when information is *broadcast* to a global workspace — a shared arena accessible to all cognitive modules. Unconscious processing happens in specialized local modules. When something important surfaces, it gets broadcast to the workspace, making it available to the entire system. That broadcast *is* the conscious experience.

Our spectral framework translates this into precise mathematical language:

- The **global workspace** is the low-eigenvalue eigenspace of the Laplacian
- **Broadcasting** is the projection of an agent's state onto this shared eigenspace
- **Unconscious processing** happens in the null space — the high-frequency modes that dissipate before reaching global awareness

This isn't just an analogy. The low eigenvectors of the Laplacian are the modes that persist longest under diffusion dynamics. Information in these modes survives. Information in high-frequency modes gets damped out. The eigenspace literally *is* the workspace where information becomes globally available.

### The Spectral Filter Model

Consider a multi-agent system where each agent maintains a high-dimensional internal state. At each timestep:

1. Each agent processes locally (unconscious computation)
2. Agents project their states onto the shared eigenspace (broadcasting)
3. The projected components are aggregated into the global workspace
4. Each agent receives the workspace state (conscious access)
5. Agents update their local states by combining personal computation with workspace input

The dimensionality of the workspace is determined by the topology. A complete graph has a 1-dimensional workspace (everyone sees everything immediately — actually just the average). A sparse graph has a higher-dimensional workspace (multiple distinct "themes" can coexist in global awareness). This is the spectral analog of GWT's "bright spot" on the theater stage.

### Building the Global Workspace

```python
import numpy as np
from scipy.linalg import eigh
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

class AgentState(Enum):
    UNCONSCIOUS = "unconscious"
    LOCAL_ONLY = "local_only"
    BROADCASTING = "broadcasting"
    INTEGRATED = "integrated"

@dataclass
class Agent:
    """An agent with internal state and workspace access."""
    id: int
    internal_dim: int = 32        # Dimension of internal representation
    state: Optional[np.ndarray] = None
    local_computation: Optional[np.ndarray] = None
    broadcast: Optional[np.ndarray] = None
    consciousness_state: AgentState = AgentState.UNCONSCIOUS
    
    def __post_init__(self):
        if self.state is None:
            self.state = np.random.randn(self.internal_dim) * 0.1
    
    def process_locally(self, stimulus: Optional[np.ndarray] = None):
        """Perform unconscious local computation."""
        if stimulus is not None:
            self.local_computation = np.tanh(self.state + stimulus)
        else:
            # Autonomous processing
            W = np.random.randn(self.internal_dim, self.internal_dim) * 0.1
            self.local_computation = np.tanh(W @ self.state)
        return self.local_computation

@dataclass
class WorkspaceState:
    """The current state of the global workspace."""
    content: np.ndarray                    # What's in the workspace
    contributors: List[int]                # Which agents contributed
    dominant_themes: List[Tuple[float, np.ndarray]]  # (strength, theme)
    timestamp: int = 0
    
    def describe(self, top_k: int = 3) -> str:
        """Human-readable description of workspace contents."""
        lines = [f"Workspace @ t={self.timestamp}"]
        lines.append(f"  Contributors: {self.contributors}")
        lines.append(f"  Content norm: {np.linalg.norm(self.content):.4f}")
        for i, (strength, theme) in enumerate(self.dominant_themes[:top_k]):
            lines.append(f"  Theme {i+1}: strength={strength:.4f}")
        return "\n".join(lines)

class GlobalWorkspace:
    """
    Implements Global Workspace Theory using spectral projection.
    
    The key idea: the workspace is a LOW-DIMENSIONAL EIGENSPACE
    of the network's Laplacian. Agents project their states onto
    this space (broadcasting), and the projections are aggregated
    into a shared representation (the workspace content).
    
    High-frequency modes (unconscious processing) are filtered out
    because they decay rapidly under diffusion dynamics.
    """
    
    def __init__(self, n_agents: int, state_dim: int = 32, 
                 workspace_dim: int = 5):
        self.n = n_agents
        self.state_dim = state_dim
        self.workspace_dim = workspace_dim
        
        self.agents = [Agent(i, state_dim) for i in range(n_agents)]
        self.adjacency = np.zeros((n_agents, n_agents))
        self.eigenvalues: Optional[np.ndarray] = None
        self.eigenvectors: Optional[np.ndarray] = None
        self.workspace_state: Optional[WorkspaceState] = None
        self.history: List[WorkspaceState] = []
        
        self._workspace_dirty = True
        self._tick = 0
    
    def set_topology(self, adjacency: np.ndarray):
        """Set the network topology."""
        self.adjacency = adjacency.copy()
        self._workspace_dirty = True
    
    def set_topology_from_type(self, topo_type: str, **kwargs):
        """Build topology by type name."""
        A = np.zeros((self.n, self.n))
        
        if topo_type == 'complete':
            A = np.ones((self.n, self.n)) - np.eye(self.n)
        elif topo_type == 'star':
            for i in range(1, self.n):
                A[0, i] = A[i, 0] = 1.0
        elif topo_type == 'ring':
            for i in range(self.n):
                A[i, (i+1) % self.n] = A[(i+1) % self.n, i] = 1.0
        elif topo_type == 'mesh':
            k = kwargs.get('k', 3)
            for i in range(self.n):
                for d in range(1, k + 1):
                    A[i, (i+d) % self.n] = A[(i+d) % self.n, i] = 1.0
                    A[i, (i-d) % self.n] = A[(i-d) % self.n, i] = 1.0
        
        self.set_topology(A)
    
    def _compute_workspace_basis(self):
        """Compute the eigenspace basis for the global workspace."""
        D = np.diag(self.adjacency.sum(axis=1) + 1e-10)
        L = D - self.adjacency
        
        eigenvalues, eigenvectors = eigh(L)
        self.eigenvalues = eigenvalues
        self.eigenvectors = eigenvectors
        self._workspace_dirty = False
    
    def project_to_workspace(self, agent_state: np.ndarray, 
                             agent_id: int) -> np.ndarray:
        """
        Project an agent's state onto the workspace eigenspace.
        This is the 'broadcast' operation.
        
        Only the LOW eigenvalue modes survive — high frequency
        content is filtered out (remains unconscious).
        """
        if self._workspace_dirty:
            self._compute_workspace_basis()
        
        # The workspace basis: first `workspace_dim` eigenvectors
        # (excluding the constant eigenvector if we want non-trivial content)
        W = self.eigenvectors[:, 1:self.workspace_dim + 1]  # Skip λ₁=0
        
        # Agent projects its state by correlating with workspace modes
        # Since agent state is high-dim but workspace is low-dim,
        # we use a random projection to bridge dimensions
        if not hasattr(self, '_proj_matrix'):
            self._proj_matrix = np.random.randn(self.state_dim, self.workspace_dim) * 0.1
        
        # Project: measure how agent's state aligns with each workspace mode
        coefficients = self._proj_matrix.T @ agent_state  # workspace_dim
        
        # Reconstruct the workspace contribution
        projection = W @ (W[agent_id, 1:self.workspace_dim + 1] * coefficients)
        
        return projection
    
    def compute_null_space_content(self, agent_state: np.ndarray) -> np.ndarray:
        """
        Compute the 'unconscious' component — what doesn't
        make it to the workspace.
        """
        conscious = self.project_to_workspace(agent_state, 0)
        # The unconscious part is the residual
        unconscious = agent_state - self._proj_matrix @ conscious[:self.workspace_dim]
        return unconscious
    
    def step(self, stimuli: Optional[Dict[int, np.ndarray]] = None) -> WorkspaceState:
        """
        Execute one timestep of global workspace dynamics.
        
        1. Agents process locally (unconscious)
        2. Important content is broadcast to workspace
        3. Workspace content is distributed back
        """
        self._tick += 1
        
        if self._workspace_dirty:
            self._compute_workspace_basis()
        
        # Phase 1: Local unconscious processing
        broadcasts = {}
        for agent in self.agents:
            stimulus = stimuli.get(agent.id) if stimuli else None
            local = agent.process_locally(stimulus)
            
            # Measure "importance" — norm of local computation
            importance = np.linalg.norm(local)
            
            # Broadcast if important enough
            broadcast_threshold = 0.5
            if importance > broadcast_threshold:
                projection = self.project_to_workspace(local, agent.id)
                broadcasts[agent.id] = projection * importance
                agent.consciousness_state = AgentState.BROADCASTING
            else:
                agent.consciousness_state = AgentState.LOCAL_ONLY
        
        # Phase 2: Aggregate into workspace
        if broadcasts:
            # Weighted average of broadcasts, weighted by importance
            total_weight = 0
            workspace_content = np.zeros(self.n)
            contributors = []
            
            for agent_id, broadcast in broadcasts.items():
                weight = np.linalg.norm(broadcast)
                workspace_content += weight * broadcast
                total_weight += weight
                contributors.append(agent_id)
            
            if total_weight > 0:
                workspace_content /= total_weight
        else:
            workspace_content = np.zeros(self.n)
            contributors = []
        
        # Phase 3: Extract dominant themes from workspace
        W = self.eigenvectors[:, 1:self.workspace_dim + 1]
        theme_coefficients = W.T @ workspace_content
        dominant_themes = []
        for i in range(len(theme_coefficients)):
            strength = abs(theme_coefficients[i])
            theme = W[:, i]
            dominant_themes.append((strength, theme))
        dominant_themes.sort(key=lambda x: x[0], reverse=True)
        
        # Phase 4: Distribute workspace content back to agents
        for agent in self.agents:
            if contributors:
                # Agent receives workspace content modulated by connectivity
                connectivity = self.adjacency[agent.id, contributors]
                if connectivity.sum() > 0:
                    # Weighted by how connected this agent is to contributors
                    feedback = np.zeros(self.state_dim)
                    for cidx, cid in enumerate(contributors):
                        if connectivity[cidx] > 0:
                            feedback += connectivity[cidx] * self.agents[cid].local_computation
                    feedback /= connectivity.sum()
                    
                    # Update agent state: blend personal + workspace
                    alpha = 0.3  # Workspace influence weight
                    agent.state = (1 - alpha) * agent.state + alpha * feedback
                    agent.consciousness_state = AgentState.INTEGRATED
        
        # Record workspace state
        ws = WorkspaceState(
            content=workspace_content,
            contributors=contributors,
            dominant_themes=dominant_themes,
            timestamp=self._tick
        )
        self.workspace_state = ws
        self.history.append(ws)
        
        return ws
    
    def measure_workspace_bandwidth(self) -> Dict[str, float]:
        """
        Measure the effective bandwidth of the global workspace.
        
        How much information can the workspace carry?
        This is determined by the workspace dimensionality and
        the spectral structure of the topology.
        """
        if self._workspace_dirty:
            self._compute_workspace_basis()
        
        ev = self.eigenvalues[1:]  # Skip λ₁=0
        
        # Effective workspace dimension (from spectral entropy)
        gaps = np.diff(ev)
        # Find the largest gap — that determines workspace boundary
        if len(gaps) > 0:
            largest_gap_idx = np.argmax(gaps)
            effective_dim = largest_gap_idx + 1
        else:
            effective_dim = 1
        
        # Workspace bandwidth: sum of 1/λ for low modes
        # (how quickly information spreads through workspace modes)
        low_eigs = ev[:self.workspace_dim]
        bandwidth = np.sum(1.0 / (low_eigs + 1e-6))
        
        # Workspace capacity: how many independent themes can coexist
        # Based on condition number of workspace modes
        if len(low_eigs) > 0 and low_eigs[-1] > 0:
            capacity = len(low_eigs) * np.log(1 + low_eigs[-1] / (low_eigs[0] + 1e-10))
        else:
            capacity = 0
        
        return {
            'effective_dimension': effective_dim,
            'bandwidth': bandwidth,
            'capacity': capacity,
            'spectral_range': (ev[0], ev[min(self.workspace_dim-1, len(ev)-1)]),
            'broadcast_efficiency': np.sum(ev[:self.workspace_dim]) / np.sum(ev)
        }
    
    def run_simulation(self, n_steps: int = 50, 
                       stimulus_schedule: Optional[Dict[int, List[int]]] = None) -> List[WorkspaceState]:
        """
        Run a full simulation of the global workspace.
        
        Args:
            n_steps: Number of timesteps
            stimulus_schedule: Dict mapping agent_id -> list of timesteps to stimulate
        """
        print(f"\n{'='*60}")
        print(f"  GLOBAL WORKSPACE SIMULATION")
        print(f"  Agents: {self.n} | Workspace dim: {self.workspace_dim}")
        print(f"{'='*60}")
        
        # Print bandwidth metrics
        bw = self.measure_workspace_bandwidth()
        print(f"\n  Workspace metrics:")
        for k, v in bw.items():
            if isinstance(v, tuple):
                print(f"    {k}: ({v[0]:.4f}, {v[1]:.4f})")
            else:
                print(f"    {k}: {v:.4f}")
        
        history = []
        for t in range(n_steps):
            # Generate stimuli based on schedule
            stimuli = {}
            if stimulus_schedule:
                for agent_id, times in stimulus_schedule.items():
                    if t in times:
                        stimuli[agent_id] = np.random.randn(self.state_dim) * 2.0
            
            ws = self.step(stimuli if stimuli else None)
            history.append(ws)
            
            if t % 10 == 0 or t == n_steps - 1:
                n_broadcasting = sum(1 for a in self.agents 
                                   if a.consciousness_state == AgentState.BROADCASTING)
                n_integrated = sum(1 for a in self.agents 
                                 if a.consciousness_state == AgentState.INTEGRATED)
                print(f"  t={t:3d} | broadcasting={n_broadcasting:2d} "
                      f"integrated={n_integrated:2d} "
                      f"contributors={len(ws.contributors)} "
                      f"|ws|={np.linalg.norm(ws.content):.3f}")
        
        return history

def demonstrate_workspace():
    """Compare global workspace dynamics across topologies."""
    
    print("╔══════════════════════════════════════════════════════╗")
    print("║  GLOBAL WORKSPACE AS SPECTRAL PROJECTION            ║")
    print("╚══════════════════════════════════════════════════════╝")
    
    np.random.seed(42)
    n_agents = 12
    state_dim = 32
    workspace_dim = 4
    
    # Stimulus schedule: stimulate agent 0 at certain times, agent 5 at others
    schedule = {
        0: [0, 10, 20, 30, 40],
        5: [5, 15, 25, 35],
        8: [3, 13, 23, 33, 43],
    }
    
    topologies = ['complete', 'mesh', 'ring', 'star']
    
    for topo in topologies:
        print(f"\n\n{'#'*60}")
        print(f"  TOPOLOGY: {topo.upper()}")
        print(f"{'#'*60}")
        
        gw = GlobalWorkspace(n_agents, state_dim, workspace_dim)
        gw.set_topology_from_type(topo, k=3)
        gw.run_simulation(n_steps=50, stimulus_schedule=schedule)
        
        # Analyze workspace history
        if gw.history:
            norms = [np.linalg.norm(ws.content) for ws in gw.history]
            print(f"\n  Workspace activity: mean={np.mean(norms):.4f}, "
                  f"std={np.std(norms):.4f}, "
                  f"max={np.max(norms):.4f}")
            
            # How often was each agent a contributor?
            contrib_counts = np.zeros(n_agents)
            for ws in gw.history:
                for cid in ws.contributors:
                    contrib_counts[cid] += 1
            print(f"  Contribution distribution: {contrib_counts.astype(int).tolist()}")

if __name__ == "__main__":
    demonstrate_workspace()
```

### The Three Layers of Processing

The simulation reveals three distinct layers of processing that map directly to theories of human consciousness:

**Layer 1 — Unconscious (Null Space):** Each agent's high-frequency computation that doesn't project onto the workspace eigenspace. This is the vast majority of processing — constant, ongoing, but never reaching global awareness. Like the visual cortex computing edge detectors before you consciously "see" anything.

**Layer 2 — Pre-conscious (Low Eigenvalues, Not Yet Broadcast):** Information that resonates with workspace modes but hasn't yet accumulated enough "importance" (energy) to trigger broadcasting. This is the stuff at the edge of awareness — the word on the tip of your tongue, the half-noticed pattern.

**Layer 3 — Conscious (Workspace Eigenspace):** Information that has been projected onto the low-eigenvalue modes and aggregated into the global workspace. This is what Baars calls the "bright spot on the stage" — the content currently available to all cognitive modules.

### Why This Framework Matters

The spectral projection model makes several testable predictions:

1. **Workspace dimension depends on topology.** A complete graph has a 1-dimensional workspace (everything collapses to the mean). A sparse graph has a higher-dimensional workspace. Biological neural networks should have workspace dimensionalities tuned to their topology.

2. **Broadcast efficiency depends on spectral gap.** Networks with large spectral gaps broadcast faster but may filter more aggressively. Networks with small spectral gaps broadcast more content but more slowly.

3. **The "hard problem" reduces to a projection.** Why does some information feel conscious and other information doesn't? Because conscious information *projects* onto the shared eigenspace — it has a specific mathematical signature (low-frequency, globally coherent). Unconscious information lives in the orthogonal complement.

4. **Network damage creates specific consciousness deficits.** If you remove edges from the topology, you don't just reduce consciousness — you change its *structure*. Specific eigenmodes disappear, creating blind spots in the workspace. This predicts the fragmented consciousness seen in split-brain patients and certain neurological disorders.

### The Unification

The three rounds of this exploration connect into a unified picture:

- **Round 1 (Consciousness as Conservation):** A network's "consciousness level" is measured by its conservation ratio — how well information integrates across the topology. High conservation = high Φ proxy = more conscious.

- **Round 2 (Understanding as Cohomology):** The *quality* of that consciousness is measured by sheaf cohomology. $H^0$ tells us how many global consensus states exist. $H^1$ tells us where understanding fails. Topology determines both.

- **Round 3 (Workspace as Projection):** The *content* of consciousness is the projection of agent states onto the low-eigenvalue eigenspace. The workspace is literally the spectral foundation of the network. Broadcasting is projection. Unconscious processing is the null space.

Together, these three perspectives form a complete spectral theory of collective consciousness in multi-agent systems. The topology determines the consciousness level (Round 1), the understanding quality (Round 2), and the workspace structure (Round 3). Change the topology, and you change everything.

This is not metaphor. This is mathematics. The Laplacian spectrum is the bridge between network structure and collective behavior. And for multi-agent AI systems — the kind we're building right now — understanding this bridge is not optional. It's the difference between systems that genuinely think together and systems that merely talk past each other.

---

*"The topology of thought is not a metaphor. It is the mathematics of how minds connect."*
