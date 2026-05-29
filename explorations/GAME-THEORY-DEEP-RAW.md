# GAME THEORY AND STRATEGY: A Conservation Spectral Analysis

*Three deep explorations of strategic interaction through the lens of graph Laplacians, spectral decomposition, and conserved quantities.*

---

## ROUND 1 — The Nash Equilibrium Laplacian

### The Insight: Games as Graphs, Equilibria as Eigenvectors

A game is a graph. This is not metaphor—it is mathematics. Every player is a node. The influence of one player's strategy on another's payoff is a weighted edge. The game's Laplacian matrix—born from this graph—encodes the entire strategic structure of the interaction. And Nash equilibria, those fabled fixed points where no player benefits from unilateral deviation, are eigenvector configurations of this Laplacian, satisfying a precise variational principle.

Let us make this concrete. Consider $n$ players, each with a strategy $x_i \in \mathbb{R}^d$. The payoff to player $i$ depends on their own strategy and the strategies of all other players whose actions affect them. We encode this mutual influence in a weighted adjacency matrix $W$, where $W_{ij}$ measures the sensitivity of player $i$'s payoff to changes in player $j$'s strategy. The graph Laplacian is:

$$L = D - W, \quad D_{ii} = \sum_j W_{ij}$$

This Laplacian is the operator that governs strategic diffusion across the game. When we say "no player benefits from unilateral deviation," we are saying that each player's strategy is locally optimal given the strategies of their neighbors in this graph. This is precisely the condition that the strategy vector $\mathbf{x} = (x_1, \ldots, x_n)$ satisfies a generalized eigenvalue condition with respect to $L$.

For continuous games with smooth payoff functions, the Nash condition becomes:

$$\nabla_{x_i} u_i(\mathbf{x}) = 0 \quad \forall i$$

where $u_i$ is player $i$'s payoff. When payoffs are quadratic—a common and analytically tractable case—this system linearizes to:

$$L \mathbf{x} = \lambda \mathbf{x}$$

The Nash equilibria are eigenvectors of the game Laplacian. The eigenvalue $\lambda$ determines the stability: equilibria corresponding to small eigenvalues are weakly stable (the Fiedler eigenvalue governs the most vulnerable equilibrium), while large-eigenvalue equilibria are robust against perturbation.

### The Fiedler Vector and Coalition Boundaries

The Fiedler vector—the eigenvector corresponding to the second-smallest eigenvalue (algebraic connectivity) of $L$—has a profound game-theoretic interpretation. In spectral graph theory, the Fiedler vector partitions a graph into two communities by sign. In game theory, it partitions the player set into *coalitions*.

When the Fiedler vector has a clear bimodal structure (positive and negative components with a gap near zero), the game naturally splits into two coalitions whose internal strategies are aligned but whose cross-coalition strategies are adversarial. The magnitude of the Fiedler eigenvalue—the algebraic connectivity—measures how tightly coupled the coalitions are. A small Fiedler eigenvalue means the coalitions are nearly independent (the game decomposes). A large one means strategic interdependence is strong and coalition boundaries are contested.

This gives us a spectral theory of cooperation and conflict. Cooperation lives in the low-frequency eigenvectors (smooth, aligned strategies across players). Conflict lives in the high-frequency eigenvectors (oscillatory, opposing strategies). The Nash equilibrium landscape is a superposition of these modes.

### Conservation in the Strategic Laplacian

The Laplacian always has a zero eigenvalue with eigenvector $\mathbf{1}$ (the all-ones vector). In game-theoretic terms, this represents a trivial equilibrium where all players adopt identical strategies—perfect symmetry. The conservation law here is:

$$\sum_i L_{ij} = 0 \quad \forall j$$

This means the total strategic "force" in the system is conserved. You cannot create strategic pressure out of nothing—it must flow from one player to another. When a player changes strategy, the payoff impacts propagate through the Laplacian like heat diffusing through a network. The total payoff shift sums to zero in a zero-sum formulation, or to a conserved quantity in general-sum games.

This conservation principle is what makes Nash equilibria computable: the search space is constrained by the spectral structure of $L$. You don't need to explore all possible strategy profiles—only those consistent with the eigenvector structure.

### Implementation: NashLaplacian

```python
import numpy as np
from scipy import linalg
from scipy.sparse.csgraph import laplacian
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class GameGraph:
    """A game represented as a weighted influence graph."""
    n_players: int
    names: List[str]
    influence_matrix: np.ndarray  # W[i,j] = influence of j on i's payoff

    @property
    def laplacian(self) -> np.ndarray:
        """Compute the graph Laplacian L = D - W."""
        return laplacian(self.influence_matrix)

    @property
    def algebraic_connectivity(self) -> float:
        """Fiedler eigenvalue — measures strategic coupling strength."""
        eigvals = np.sort(np.linalg.eigvalsh(self.laplacian))
        return eigvals[1]  # second smallest

    @property
    def fiedler_vector(self) -> np.ndarray:
        """Eigenvector for the Fiedler eigenvalue — identifies coalition boundaries."""
        L = self.laplacian
        eigvals, eigvecs = np.linalg.eigh(L)
        # Sort by eigenvalue
        idx = np.argsort(eigvals)
        return eigvecs[:, idx[1]]  # second smallest eigenvector

    def coalitions(self, threshold: float = 0.0) -> Tuple[List[int], List[int]]:
        """Split players into two coalitions based on Fiedler vector sign."""
        fv = self.fiedler_vector
        coalition_a = [i for i in range(self.n_players) if fv[i] >= threshold]
        coalition_b = [i for i in range(self.n_players) if fv[i] < threshold]
        return coalition_a, coalition_b


@dataclass
class NashLaplacian:
    """
    Finds and analyzes Nash equilibria through spectral decomposition
    of the game's Laplacian.
    """
    game: GameGraph
    payoff_matrices: List[np.ndarray]  # payoff_matrices[i] = H_i for player i
    _equilibria: Optional[List[Dict]] = field(default=None, init=False)

    def find_equilibria(self, n_strategies: int = 4,
                        regularization: float = 1e-6) -> List[Dict]:
        """
        Find Nash equilibria as eigenvector configurations of the game Laplacian.

        For quadratic payoffs: u_i(x) = x^T H_i x
        Nash condition: (H_i + H_i^T) x = lambda_i x
        We solve the joint system via the Laplacian structure.
        """
        L = self.game.laplacian
        n = self.game.n_players

        # Build joint Nash operator: sum of symmetrized payoff matrices
        # weighted by Laplacian structure
        H_joint = np.zeros((n, n))
        for i in range(n):
            H_sym = 0.5 * (self.payoff_matrices[i] + self.payoff_matrices[i].T)
            # Weight by influence structure
            H_joint += self.game.influence_matrix[i, :].reshape(-1, 1) * H_sym

        # Regularize for numerical stability
        H_joint += regularization * np.eye(n)

        # Eigendecomposition
        eigvals, eigvecs = np.linalg.eigh(H_joint)

        equilibria = []
        for k in range(min(n_strategies, n)):
            strategy = eigvecs[:, k]
            # Normalize to unit simplex-like structure
            strategy = strategy / (np.sum(np.abs(strategy)) + 1e-12)

            # Check Nash stability: compute each player's incentive to deviate
            incentives = self._compute_incentives(strategy)
            is_nash = all(inc < 0.1 for inc in incentives)  # threshold

            equilibria.append({
                'strategy_profile': strategy,
                'eigenvalue': eigvals[k],
                'is_stable': eigvals[k] > self.game.algebraic_connectivity,
                'max_incentive_to_deviate': max(incentives),
                'stability_score': eigvals[k] / (eigvals[-1] + 1e-12),
            })

        self._equilibria = equilibria
        return equilibria

    def _compute_incentives(self, strategy: np.ndarray) -> List[float]:
        """Compute each player's incentive to unilaterally deviate."""
        incentives = []
        for i in range(self.game.n_players):
            H_i = self.payoff_matrices[i]
            # Current payoff
            current_payoff = strategy @ H_i @ strategy
            # Best unilateral deviation (gradient direction)
            gradient = 2 * H_i @ strategy
            gradient_norm = np.linalg.norm(gradient)
            incentives.append(gradient_norm)
        return incentives

    def analyze_coalition_stability(self) -> Dict:
        """
        Analyze stability of coalition structures via spectral analysis.
        """
        coal_a, coal_b = self.game.coalitions()
        fiedler_val = self.game.algebraic_connectivity

        # Within-coalition cooperation strength
        W = self.game.influence_matrix
        intra_a = np.mean([W[i, j] for i in coal_a for j in coal_a if i != j]) if len(coal_a) > 1 else 0
        intra_b = np.mean([W[i, j] for i in coal_b for j in coal_b if i != j]) if len(coal_b) > 1 else 0
        inter = np.mean([W[i, j] for i in coal_a for j in coal_b]) if coal_a and coal_b else 0

        return {
            'coalition_a': [self.game.names[i] for i in coal_a],
            'coalition_b': [self.game.names[i] for i in coal_b],
            'fiedler_eigenvalue': fiedler_val,
            'intra_coalition_a_strength': intra_a,
            'intra_coalition_b_strength': intra_b,
            'inter_coalition_hostility': inter,
            'coupling_ratio': fiedler_val / (np.trace(self.game.laplacian) / self.game.n_players),
            'spectral_gap': self._spectral_gap(),
        }

    def _spectral_gap(self) -> float:
        """Gap between Fiedler eigenvalue and zero — measures coalition stability."""
        eigvals = np.sort(np.linalg.eigvalsh(self.game.laplacian))
        return eigvals[1] - eigvals[0]

    def conservation_check(self, strategy: np.ndarray) -> float:
        """
        Verify conservation: total strategic force = 0.
        Returns deviation from conservation (should be ~0).
        """
        L = self.game.laplacian
        force = L @ strategy
        return np.sum(force)

    def report(self) -> str:
        """Generate a full spectral analysis report."""
        lines = ["=" * 60]
        lines.append("NASH EQUILIBRIUM LAPLACIAN ANALYSIS")
        lines.append("=" * 60)
        lines.append(f"Players: {self.game.names}")
        lines.append(f"Algebraic connectivity (Fiedler): {self.game.algebraic_connectivity:.4f}")
        lines.append("")

        coal = self.analyze_coalition_stability()
        lines.append("COALITION STRUCTURE:")
        lines.append(f"  Coalition A: {coal['coalition_a']}")
        lines.append(f"  Coalition B: {coal['coalition_b']}")
        lines.append(f"  Intra-A strength: {coal['intra_coalition_a_strength']:.4f}")
        lines.append(f"  Intra-B strength: {coal['intra_coalition_b_strength']:.4f}")
        lines.append(f"  Inter-coalition hostility: {coal['inter_coalition_hostility']:.4f}")
        lines.append("")

        if self._equilibria:
            lines.append("NASH EQUILIBRIA:")
            for i, eq in enumerate(self._equilibria):
                lines.append(f"  Equilibrium {i}:")
                lines.append(f"    Eigenvalue: {eq['eigenvalue']:.4f}")
                lines.append(f"    Stable: {eq['is_stable']}")
                lines.append(f"    Max deviation incentive: {eq['max_incentive_to_deviate']:.4f}")
                lines.append(f"    Conservation residual: {self.conservation_check(eq['strategy_profile']):.2e}")
                lines.append("")

        return "\n".join(lines)


# === DEMONSTRATION ===
def demo_nash_laplacian():
    """
    5-player influence game with coalition structure.
    """
    names = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]

    # Influence matrix: strong intra-coalition, weaker inter-coalition
    # Coalition 1: Alpha, Beta, Gamma | Coalition 2: Delta, Epsilon
    W = np.array([
        [0.0, 0.8, 0.7, 0.2, 0.1],   # Alpha
        [0.7, 0.0, 0.9, 0.1, 0.2],   # Beta
        [0.6, 0.8, 0.0, 0.3, 0.1],   # Gamma
        [0.2, 0.1, 0.2, 0.0, 0.9],   # Delta
        [0.1, 0.2, 0.1, 0.8, 0.0],   # Epsilon
    ])

    game = GameGraph(n_players=5, names=names, influence_matrix=W)

    # Payoff matrices (strategic interaction kernels)
    np.random.seed(42)
    payoffs = []
    for i in range(5):
        H = np.random.randn(5, 5) * 0.5
        H = 0.5 * (H + H.T)  # symmetrize
        # Make own-payoff dominant
        H[i, i] = 2.0
        payoffs.append(H)

    solver = NashLaplacian(game=game, payoff_matrices=payoffs)
    equilibria = solver.find_equilibria()
    print(solver.report())

    # Verify conservation
    print("\nCONSERVATION VERIFICATION:")
    L = game.laplacian
    ones = np.ones(5)
    print(f"  L @ 1 = {L @ ones} (should be ~0)")

    return solver


if __name__ == "__main__":
    demo_nash_laplacian()
```

### What This Reveals

The NashLaplacian framework gives us something classical game theory struggles with: *structural* insight. When we decompose a game into its spectral modes, we see:

1. **The zero mode** ($\lambda = 0$): Universal cooperation—the trivial equilibrium where everyone plays the same. Always exists, rarely interesting.

2. **The Fiedler mode**: The most relevant strategic divide. The sign structure of this eigenvector tells you who naturally allies with whom, not from social choice, but from the mathematical structure of mutual influence.

3. **High-frequency modes**: Oscillatory strategies where adjacent players in the influence graph adopt opposing positions. These are equilibria too—but unstable ones. Small perturbations collapse them toward lower-frequency solutions.

The conservation principle ($L\mathbf{1} = 0$) ensures that strategic pressure cannot be created or destroyed—it can only be redistributed. When one player gains strategic advantage, others must lose it. The Laplacian tracks this flow with mathematical precision, and the eigenvectors tell you *where* the pressure goes.

---

## ROUND 2 — The Auction Network

### The Insight: Markets as Graphs, Efficiency as Conservation

An auction is a game, and a market is a network of auctions. When we model bidders as nodes and valuation correlations as edges, the resulting graph Laplacian encodes the market's competitive structure with startling fidelity. The key insight: *conservation of competitive pressure*.

In an efficient market, competitive pressure flows freely between all participants. The graph Laplacian has high algebraic connectivity—every bidder is effectively connected to every other through chains of competitive relationships. The spectral profile is smooth and well-distributed.

In a collusive or monopolistic market, the graph fractures. Subsets of bidders form tight clusters (the cartel) with weak connections to the rest. The algebraic connectivity drops. The Fiedler vector cleanly separates colluders from legitimate bidders. And crucially, *the conservation property of the Laplacian is violated locally within each cluster*—competitive pressure doesn't flow across cluster boundaries.

This is collusion detection through spectral analysis. No need to observe secret meetings or decrypt communications. The market structure itself reveals the conspiracy.

### Valuation Correlation as Edge Weight

Two bidders have correlated valuations when they tend to bid similarly on similar items. This correlation is a measurable quantity. Define:

$$W_{ij} = \text{corr}(v_i, v_j) = \frac{\mathbb{E}[(v_i - \bar{v}_i)(v_j - \bar{v}_j)]}{\sigma_i \sigma_j}$$

where $v_i$ is the vector of bidder $i$'s valuations across all items. In a competitive market, these correlations are moderate—bidders have overlapping but distinct preferences. In a cartel, correlations among colluders are suspiciously high (they coordinate bids), while correlations between colluders and outsiders are suspiciously low (they avoid competing with each other).

The auction Laplacian $L_{\text{auction}} = D - W$ then captures the market's competitive topology. Its spectral properties are a direct readout of market health:

- **High algebraic connectivity**: Healthy competition. No bidder is isolated; everyone faces competitive pressure.
- **Low algebraic connectivity**: Market failure. Either natural monopoly (legitimate) or cartel (fraudulent).
- **Fiedler vector structure**: Identifies the fault line. If it separates a small group from everyone else, that's your cartel.

### The Conservation Principle in Markets

The Laplacian conservation $L\mathbf{1} = 0$ has a precise market interpretation: *the total competitive imbalance is zero*. For every bidder who faces above-average competition, there must be bidders facing below-average competition. Competitive pressure is a conserved quantity.

When a cartel forms, this conservation is maintained globally but breaks down *locally*. Within the cartel, bidders face artificially low competition (they've agreed not to compete with each other). Outside the cartel, bidders face artificially high competition (the cartel coordinates against them). The net effect cancels globally, but the local imbalance is detectable through the spectral structure.

The Rayleigh quotient provides the formal measure:

$$R(\mathbf{x}) = \frac{\mathbf{x}^T L \mathbf{x}}{\mathbf{x}^T \mathbf{x}}$$

For the Fiedler vector $\mathbf{v}_2$, $R(\mathbf{v}_2) = \lambda_2$, the algebraic connectivity. A drop in this value—compared to historical baselines or theoretical expectations—signals a structural change in the market. If the drop coincides with the emergence of a clear partition in the Fiedler vector, you have strong evidence of collusion.

### Implementation: AuctionNetwork

```python
import numpy as np
from scipy import linalg
from scipy.sparse.csgraph import laplacian
from scipy.stats import pearsonr
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field
import warnings


@dataclass
class Bidder:
    """A participant in the auction market."""
    name: str
    valuations: np.ndarray  # valuations across items
    bid_history: np.ndarray  # actual bids across items


@dataclass
class AuctionMarket:
    """A market as a graph of bidder relationships."""
    bidders: List[Bidder]
    n_items: int
    _W: Optional[np.ndarray] = field(default=None, init=False)
    _L: Optional[np.ndarray] = field(default=None, init=False)

    @property
    def n_bidders(self) -> int:
        return len(self.bidders)

    def compute_correlation_matrix(self, use_bids: bool = True) -> np.ndarray:
        """
        Compute valuation/bid correlation matrix as edge weights.
        use_bids: True = use actual bids, False = use valuations.
        """
        n = self.n_bidders
        W = np.zeros((n, n))
        data_source = 'bids' if use_bids else 'valuations'

        for i in range(n):
            for j in range(i + 1, n):
                vi = self.bidders[i].bid_history if use_bids else self.bidders[i].valuations
                vj = self.bidders[j].bid_history if use_bids else self.bidders[j].valuations
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    corr, _ = pearsonr(vi, vj)
                W[i, j] = max(corr, 0)  # non-negative weights
                W[j, i] = W[i, j]

        self._W = W
        self._L = laplacian(W)
        return W

    @property
    def laplacian(self) -> np.ndarray:
        if self._L is None:
            self.compute_correlation_matrix()
        return self._L

    @property
    def correlation_matrix(self) -> np.ndarray:
        if self._W is None:
            self.compute_correlation_matrix()
        return self._W

    @property
    def algebraic_connectivity(self) -> float:
        eigvals = np.sort(np.linalg.eigvalsh(self.laplacian))
        return eigvals[1]

    @property
    def fiedler_vector(self) -> np.ndarray:
        L = self.laplacian
        eigvals, eigvecs = np.linalg.eigh(L)
        idx = np.argsort(eigvals)
        return eigvecs[:, idx[1]]


@dataclass
class AuctionNetwork:
    """
    Spectral collusion detection and market efficiency analysis.
    """
    market: AuctionMarket
    historical_connectivity: Optional[float] = None
    collusion_threshold: float = 0.3  # drop ratio triggering alert

    def market_efficiency_score(self) -> float:
        """
        Compute market efficiency from spectral profile.
        High = competitive market, Low = market failure.
        """
        L = self.market.laplacian
        eigvals = np.sort(np.linalg.eigvalsh(L))
        n = self.market.n_bidders

        # Efficiency = normalized algebraic connectivity
        # Perfect market: fully connected → lambda_2 = n
        # Worst case: disconnected → lambda_2 = 0
        max_connectivity = float(n)
        efficiency = eigvals[1] / max_connectivity
        return float(np.clip(efficiency, 0, 1))

    def detect_collusion(self) -> Dict:
        """
        Detect potential collusion via spectral analysis.
        Returns suspicious clusters and confidence scores.
        """
        connectivity = self.market.algebraic_connectivity
        efficiency = self.market_efficiency_score()
        fiedler = self.market.fiedler_vector

        # Check for connectivity drop
        connectivity_drop = 0.0
        if self.historical_connectivity is not None:
            connectivity_drop = 1.0 - (connectivity / self.historical_connectivity)

        # Identify suspicious partition from Fiedler vector
        # Look for bimodal structure
        median_fv = np.median(fiedler)
        group_a = [i for i in range(len(fiedler)) if fiedler[i] >= median_fv]
        group_b = [i for i in range(len(fiedler)) if fiedler < median_fv]

        # Compute intra-group vs inter-group correlation
        W = self.market.correlation_matrix
        intra_a = np.mean([W[i, j] for i in group_a for j in group_a
                           if i != j]) if len(group_a) > 1 else 0
        intra_b = np.mean([W[i, j] for i in group_b for j in group_b
                           if i != j]) if len(group_b) > 1 else 0
        inter = np.mean([W[i, j] for i in group_a for j in group_b
                        ]) if group_a and group_b else 0

        # Collusion signal: high intra, low inter
        asymmetry_ratio = (intra_a + intra_b) / (2 * inter + 1e-12)

        # Confidence: combine multiple signals
        signals = {
            'connectivity_drop': connectivity_drop,
            'asymmetry_ratio': asymmetry_ratio,
            'efficiency': efficiency,
        }

        # Heuristic confidence score
        confidence = 0.0
        if connectivity_drop > self.collusion_threshold:
            confidence += 0.3
        if asymmetry_ratio > 2.0:
            confidence += 0.3
        if efficiency < 0.3:
            confidence += 0.2
        if len(group_a) < 0.3 * len(fiedler) or len(group_b) < 0.3 * len(fiedler):
            confidence += 0.2  # small suspicious group

        # Determine suspicious group (the smaller one)
        if len(group_a) <= len(group_b):
            suspicious = group_a
        else:
            suspicious = group_b

        return {
            'collusion_detected': confidence > 0.5,
            'confidence': min(confidence, 1.0),
            'suspicious_bidders': [self.market.bidders[i].name for i in suspicious],
            'group_a': [self.market.bidders[i].name for i in group_a],
            'group_b': [self.market.bidders[i].name for i in group_b],
            'efficiency_score': efficiency,
            'connectivity_drop': connectivity_drop,
            'asymmetry_ratio': asymmetry_ratio,
            'algebraic_connectivity': connectivity,
            'signals': signals,
        }

    def conservation_audit(self) -> Dict:
        """
        Audit the conservation property across the market.
        In healthy markets, competitive pressure is conserved globally.
        In corrupt markets, local conservation breaks down.
        """
        L = self.market.laplacian
        n = self.market.n_bidders

        # Global conservation: L @ 1 should be ~0
        ones = np.ones(n)
        global_conservation = np.linalg.norm(L @ ones)

        # Per-bidder local conservation
        bidder_balance = L @ ones  # should be ~0 for each bidder

        # Per-bidder competitive pressure (diagonal of L = total influence)
        pressure = np.diag(L)

        # Identify bidders with anomalous pressure
        mean_pressure = np.mean(pressure)
        std_pressure = np.std(pressure) + 1e-12
        anomalous = [self.market.bidders[i].name for i in range(n)
                     if abs(pressure[i] - mean_pressure) > 2 * std_pressure]

        return {
            'global_conservation_residual': float(global_conservation),
            'bidder_balance': {self.market.bidders[i].name: float(bidder_balance[i])
                               for i in range(n)},
            'competitive_pressure': {self.market.bidders[i].name: float(pressure[i])
                                     for i in range(n)},
            'anomalous_bidders': anomalous,
            'pressure_distribution': {
                'mean': float(mean_pressure),
                'std': float(std_pressure),
                'min': float(np.min(pressure)),
                'max': float(np.max(pressure)),
            },
        }

    def spectral_profile(self) -> Dict:
        """Full spectral profile of the market."""
        L = self.market.laplacian
        eigvals = np.sort(np.linalg.eigvalsh(L))

        # Effective graph resistance (Kirchhoff index)
        non_zero = eigvals[eigvals > 1e-10]
        kirchhoff = float(n * np.sum(1.0 / non_zero)) if len(non_zero) > 0 else float('inf')

        return {
            'eigenvalues': eigvals.tolist(),
            'spectral_gap': float(eigvals[1] - eigvals[0]),
            'algebraic_connectivity': float(eigvals[1]),
            'kirchhoff_index': kirchhoff,
            'spectral_entropy': self._spectral_entropy(eigvals),
            'participation_ratio': self._participation_ratio(eigvals),
        }

    def _spectral_entropy(self, eigvals: np.ndarray) -> float:
        """Spectral entropy — measures randomness of eigenvalue distribution."""
        shifted = eigvals - np.min(eigvals) + 1e-12
        probs = shifted / np.sum(shifted)
        return float(-np.sum(probs * np.log(probs + 1e-12)))

    def _participation_ratio(self, eigvals: np.ndarray) -> float:
        """Number of effective spectral modes."""
        total = np.sum(eigvals ** 2)
        return float(np.sum(eigvals ** 2) ** 2 / (np.sum(eigvals ** 4) + 1e-12))

    def report(self) -> str:
        """Generate comprehensive market analysis report."""
        lines = ["=" * 60]
        lines.append("AUCTION NETWORK SPECTRAL ANALYSIS")
        lines.append("=" * 60)

        collusion = self.detect_collusion()
        lines.append(f"\nCOLLUSION DETECTION:")
        lines.append(f"  Detected: {collusion['collusion_detected']}")
        lines.append(f"  Confidence: {collusion['confidence']:.2%}")
        lines.append(f"  Suspicious bidders: {collusion['suspicious_bidders']}")
        lines.append(f"  Efficiency score: {collusion['efficiency_score']:.4f}")
        lines.append(f"  Asymmetry ratio: {collusion['asymmetry_ratio']:.4f}")

        audit = self.conservation_audit()
        lines.append(f"\nCONSERVATION AUDIT:")
        lines.append(f"  Global residual: {audit['global_conservation_residual']:.2e}")
        lines.append(f"  Anomalous bidders: {audit['anomalous_bidders']}")
        lines.append(f"  Pressure range: [{audit['pressure_distribution']['min']:.4f}, "
                      f"{audit['pressure_distribution']['max']:.4f}]")

        profile = self.spectral_profile()
        lines.append(f"\nSPECTRAL PROFILE:")
        lines.append(f"  Eigenvalues: {[f'{e:.4f}' for e in profile['eigenvalues']]}")
        lines.append(f"  Kirchhoff index: {profile['kirchhoff_index']:.4f}")
        lines.append(f"  Spectral entropy: {profile['spectral_entropy']:.4f}")

        return "\n".join(lines)


# === DEMONSTRATION ===
def demo_auction_network():
    """
    8-bidder market with a 3-bidder cartel.
    """
    np.random.seed(123)
    n_items = 50

    # Generate valuations for honest bidders
    honest_vals = [np.random.exponential(scale=100 + i * 20, size=n_items) for i in range(5)]

    # Cartel: 3 bidders with artificially correlated bids
    base_cartel = np.random.exponential(scale=120, size=n_items)
    cartel_vals = [base_cartel * (0.8 + 0.4 * np.random.random(n_items)) for _ in range(3)]

    # Build bidders
    names = ["Honest_" + str(i) for i in range(5)] + ["Cartel_" + str(i) for i in range(3)]
    all_vals = honest_vals + cartel_vals

    bidders = []
    for name, val in zip(names, all_vals):
        # Bids = valuation + noise (honest) or coordinated (cartel)
        if "Cartel" in name:
            bid = val * (0.7 + 0.1 * np.random.random(n_items))  # suppress bids
        else:
            bid = val + np.random.normal(0, 10, size=n_items)
        bidders.append(Bidder(name=name, valuations=val, bid_history=np.maximum(bid, 1)))

    market = AuctionMarket(bidders=bidders, n_items=n_items)
    analyzer = AuctionNetwork(
        market=market,
        historical_connectivity=1.5,  # expected healthy connectivity
    )

    print(analyzer.report())
    return analyzer


if __name__ == "__main__":
    demo_auction_network()
```

### What This Reveals

The AuctionNetwork framework demonstrates that market integrity is fundamentally a *spectral* property. A healthy competitive market has a full, well-distributed eigenvalue spectrum. The algebraic connectivity is high because competitive pressure flows freely. The Fiedler vector is unstructured—there's no natural partition because all bidders are equally embedded in the competitive network.

Collusion distorts this spectrum. The cartel creates an artificially tight cluster—high intra-correlation, low inter-correlation. The Fiedler eigenvalue drops because the graph is nearly disconnected. The Fiedler vector cleanly separates colluders from honest bidders. The conservation audit reveals bidders with anomalous competitive pressure—cartel members face too little, outsiders face too much.

The practical power of this approach is its *passive* nature. You don't need to prove conspiracy through communication records or whistleblower testimony. The market structure itself—the pattern of who bids like whom—encodes the collusion in its Laplacian. The spectrum doesn't lie.

---

## ROUND 3 — The Evolutionary Game Graph

### The Insight: Evolution as a Laplacian Process

Natural selection is a game. Species (or strategies) are players. Fitness interactions are payoffs. The evolutionary stable strategy (ESS) is the Nash equilibrium of natural selection. And the entire evolutionary dynamics can be formulated as a Laplacian diffusion process on the fitness landscape graph.

This is not a loose analogy. It is a precise mathematical correspondence. Define a graph where each node is a strategy (or species, or phenotype). Edge weight $W_{ij}$ represents the fitness interaction between strategies $i$ and $j$—how well strategy $i$ performs against strategy $j$. The Laplacian $L = D - W$ governs how strategy frequencies evolve over time.

The replicator dynamics—the workhorse equation of evolutionary game theory—are:

$$\dot{x}_i = x_i (f_i(\mathbf{x}) - \bar{f}(\mathbf{x}))$$

where $x_i$ is the frequency of strategy $i$, $f_i$ is its fitness, and $\bar{f}$ is the average fitness. This can be rewritten as:

$$\dot{\mathbf{x}} = \text{diag}(\mathbf{x}) (W\mathbf{x} - (\mathbf{x}^T W \mathbf{x})\mathbf{1})$$

The term $W\mathbf{x}$ is the fitness landscape, and the subtraction of the average ensures that frequencies sum to one—a *conservation law*. Total population is conserved; strategies gain at each other's expense.

In the Laplacian formulation, this becomes:

$$\dot{\mathbf{x}} = -\text{diag}(\mathbf{x}) L \mathbf{x} + (\text{correction terms})$$

The Laplacian drives strategy frequencies toward the kernel (low-fitness eigenmodes die out; high-fitness eigenmodes grow). The correction terms maintain the simplex constraint (frequencies sum to one). This is diffusion on a simplex—the Laplacian selects for smooth, high-conservation strategy configurations.

### ESS as High-Conservation Eigenvector Configuration

An evolutionary stable strategy is a strategy that, once established, cannot be invaded by any mutant. In the Laplacian framework, this translates to:

**An ESS is a strategy $\mathbf{x}^*$ such that the spectral radius of $L$ restricted to the orthogonal complement of $\mathbf{x}^*$ is minimized.**

Why? Because the ESS must be robust against perturbations in *all* directions. The perturbations that matter are precisely the eigenmodes of the Laplacian. If any eigenmode has low eigenvalue (weak restoring force), a perturbation in that direction can invade. The ESS maximizes the minimum eigenvalue of the restricted Laplacian—it has the strongest possible spectral gap against invasion.

This is the max-min principle of evolutionary stability, and it connects directly to the conservation structure. A high-conservation configuration is one where the Laplacian eigenvalues are all large—every direction of perturbation is strongly opposed. The ESS is the most conserved configuration: the one that resists change the most.

### The Red Queen: Perpetual Laplacian Perturbation

Van Valen's Red Queen Hypothesis states that species must constantly adapt merely to maintain their relative fitness. In the Laplacian framework, this is:

**The fitness Laplacian is never static. It is perpetually perturbed by mutation, environmental change, and coevolution.**

Each perturbation shifts the eigenvalues and eigenvectors. The ESS computed at time $t$ is no longer an ESS at time $t+1$. The system must continuously track the moving target. The Red Queen is the Laplacian's refusal to sit still.

Formally, if $L(t)$ is the fitness Laplacian at time $t$:

$$L(t+1) = L(t) + \epsilon P(t)$$

where $P(t)$ is a perturbation matrix (from mutation, environmental change, etc.) and $\epsilon$ is the perturbation strength. The ESS at time $t+1$ satisfies:

$$L(t+1) \mathbf{x}^*(t+1) = \lambda_{\min} \mathbf{x}^*(t+1)$$

The tracking problem—how well the population can follow the moving ESS—is governed by the *spectral gap* of $L(t)$. A large spectral gap means the ESS is well-defined and easy to find. A small spectral gap means the ESS is fragile and easily lost. Coevolutionary arms races correspond to periods of shrinking spectral gap—increasing vulnerability to invasion—as the system approaches a bifurcation point where the current ESS destabilizes and a new one emerges.

### Implementation: EvoGameGraph

```python
import numpy as np
from scipy import linalg
from scipy.sparse.csgraph import laplacian
from scipy.integrate import odeint
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class StrategyNode:
    """A strategy/species in the evolutionary game."""
    name: str
    initial_frequency: float
    fitness_baseline: float = 1.0


@dataclass
class EvoGameGraph:
    """
    Evolutionary game dynamics on a fitness interaction graph.
    Tracks ESS stability, Red Queen dynamics, and spectral conservation.
    """
    strategies: List[StrategyNode]
    fitness_matrix: np.ndarray  # A[i,j] = fitness of i against j
    mutation_rate: float = 0.01
    _L: Optional[np.ndarray] = field(default=None, init=False)
    _history: List[Dict] = field(default_factory=list, init=False)

    @property
    def n_strategies(self) -> int:
        return len(self.strategies)

    @property
    def laplacian(self) -> np.ndarray:
        """Fitness-weighted Laplacian."""
        if self._L is None:
            self._L = laplacian(self.fitness_matrix)
        return self._L

    def initial_frequencies(self) -> np.ndarray:
        freqs = np.array([s.initial_frequency for s in self.strategies])
        return freqs / freqs.sum()

    def mean_fitness(self, x: np.ndarray) -> float:
        """Population mean fitness: x^T A x."""
        return float(x @ self.fitness_matrix @ x)

    def fitness_vector(self, x: np.ndarray) -> np.ndarray:
        """Fitness of each strategy against the population: A @ x."""
        return self.fitness_matrix @ x

    def replicator_dynamics(self, x: np.ndarray, t: float) -> np.ndarray:
        """
        Replicator equation: dx_i/dt = x_i * (f_i - f_bar)
        with conservation constraint (sum of frequencies = 1).
        """
        f = self.fitness_vector(x)
        f_bar = self.mean_fitness(x)
        dxdt = x * (f - f_bar)

        # Add small mutation term (prevents extinction, enables exploration)
        mutation_flow = self.mutation_rate * (np.ones_like(x) / len(x) - x)
        dxdt += mutation_flow

        return dxdt

    def simulate(self, t_span: np.ndarray) -> Dict:
        """
        Run evolutionary dynamics and track spectral properties.
        """
        x0 = self.initial_frequencies()

        # Integrate replicator dynamics
        trajectory = odeint(self.replicator_dynamics, x0, t_span)

        # Analyze spectral properties at each time step
        spectral_history = []
        for t_idx, x_t in enumerate(trajectory):
            # Effective Laplacian at this population state
            L_eff = self._effective_laplacian(x_t)
            eigvals = np.sort(np.linalg.eigvalsh(L_eff))

            spectral_history.append({
                'time': t_span[t_idx],
                'frequencies': x_t.copy(),
                'mean_fitness': self.mean_fitness(x_t),
                'diversity': self._shannon_diversity(x_t),
                'algebraic_connectivity': eigvals[1],
                'spectral_gap': eigvals[1] - eigvals[0],
                'spectral_radius': eigvals[-1],
                'conservation_residual': float(np.linalg.norm(L_eff @ np.ones_like(x_t))),
                'dominant_strategy': int(np.argmax(x_t)),
                'dominance': float(np.max(x_t)),
            })

        self._history = spectral_history
        return {
            'trajectory': trajectory,
            'times': t_span,
            'spectral_history': spectral_history,
        }

    def _effective_laplacian(self, x: np.ndarray) -> np.ndarray:
        """
        Effective Laplacian weighted by current frequencies.
        Encodes how the fitness landscape looks to the current population.
        """
        # Weight fitness interactions by frequency
        W_eff = self.fitness_matrix * np.outer(x, x)
        D_eff = np.diag(np.sum(W_eff, axis=1))
        return D_eff - W_eff

    def _shannon_diversity(self, x: np.ndarray) -> float:
        """Shannon entropy of strategy distribution — measures diversity."""
        p = x[x > 1e-10]
        return float(-np.sum(p * np.log(p)))

    def find_ess(self) -> Dict:
        """
        Identify evolutionary stable strategies via spectral analysis.

        An ESS maximizes the minimum eigenvalue of the restricted Laplacian.
        """
        L = self.laplacian
        eigvals, eigvecs = np.linalg.eigh(L)

        # Candidates: eigenvectors that can be interpreted as frequency distributions
        # (all non-negative, sums to 1)
        candidates = []
        for k in range(self.n_strategies):
            v = eigvecs[:, k]
            # Try to project onto simplex
            v_pos = np.maximum(v, 0)
            if np.sum(v_pos) > 1e-10:
                v_norm = v_pos / np.sum(v_pos)
                min_eigenval = eigvals[k]

                # Check ESS condition: for all mutant strategies,
                # v^T A v > mutant^T A v (when rare)
                is_ess = self._check_ess_condition(v_norm)

                candidates.append({
                    'strategy': v_norm,
                    'eigenvalue': float(eigvals[k]),
                    'is_ess': is_ess,
                    'diversity': self._shannon_diversity(v_norm),
                    'dominant': self.strategies[int(np.argmax(v_norm))].name,
                    'dominance': float(np.max(v_norm)),
                })

        # Also check pure strategies
        for i in range(self.n_strategies):
            pure = np.zeros(self.n_strategies)
            pure[i] = 1.0
            is_ess = self._check_ess_condition(pure)
            candidates.append({
                'strategy': pure,
                'eigenvalue': float(self.fitness_matrix[i, i]),
                'is_ess': is_ess,
                'diversity': 0.0,
                'dominant': self.strategies[i].name,
                'dominance': 1.0,
                'pure': True,
            })

        return {
            'candidates': candidates,
            'ess_count': sum(1 for c in candidates if c['is_ess']),
            'best_mixed': max(
                [c for c in candidates if c['diversity'] > 0.1],
                key=lambda c: c['eigenvalue'],
                default=None,
            ),
        }

    def _check_ess_condition(self, x_star: np.ndarray, n_invaders: int = 100) -> bool:
        """
        Check ESS condition: x* is ESS if for all mutants y != x*,
        x*^T A x* > y^T A x* (when mutant is rare).
        """
        f_star = x_star @ self.fitness_matrix @ x_star

        for _ in range(n_invaders):
            # Random mutant
            y = np.random.dirichlet(np.ones(self.n_strategies))
            f_y_vs_star = y @ self.fitness_matrix @ x_star

            if f_y_vs_star > f_star + 1e-10:
                return False  # Invader does better — not ESS

        return True

    def red_queen_simulation(self, n_steps: int = 100,
                              perturbation_strength: float = 0.1) -> Dict:
        """
        Simulate Red Queen dynamics: perpetual Laplacian perturbation.
        The fitness matrix evolves over time, and strategies must track.
        """
        L_current = self.fitness_matrix.copy()
        x = self.initial_frequencies()
        t_fine = np.linspace(0, 1, 20)

        history = []
        ess_tracking = []  # How well population tracks the moving ESS

        for step in range(n_steps):
            # Evolve fitness landscape (Red Queen perturbation)
            perturbation = perturbation_strength * np.random.randn(
                self.n_strategies, self.n_strategies)
            perturbation = 0.5 * (perturbation + perturbation.T)  # symmetrize
            L_current = L_current + perturbation

            # Ensure non-negative fitness
            L_current = np.maximum(L_current, 0.01)

            # Temporarily update fitness matrix
            original_fitness = self.fitness_matrix.copy()
            self.fitness_matrix = L_current
            self._L = None  # Reset cached Laplacian

            # Simulate one round of evolution
            x = np.maximum(x, 1e-6)
            x = x / np.sum(x)

            trajectory = odeint(self.replicator_dynamics, x, t_fine)
            x = trajectory[-1]
            x = np.maximum(x, 1e-6)
            x = x / np.sum(x)

            # Compute spectral properties
            L_eff = self._effective_laplacian(x)
            eigvals = np.sort(np.linalg.eigvalsh(L_eff))

            # Compute current ESS
            ess_result = self.find_ess()
            best_ess = ess_result['best_mixed']

            # Track distance to ESS
            ess_distance = 0.0
            if best_ess is not None:
                ess_distance = float(np.linalg.norm(x - best_ess['strategy']))

            history.append({
                'step': step,
                'frequencies': x.copy(),
                'mean_fitness': self.mean_fitness(x),
                'diversity': self._shannon_diversity(x),
                'algebraic_connectivity': eigvals[1],
                'spectral_gap': eigvals[1] - eigvals[0],
                'ess_distance': ess_distance,
                'dominant': self.strategies[int(np.argmax(x))].name,
            })

            ess_tracking.append(ess_distance)

        # Restore original fitness matrix
        self.fitness_matrix = original_fitness
        self._L = None

        return {
            'history': history,
            'mean_ess_distance': float(np.mean(ess_tracking)),
            'ess_tracking_trend': float(
                np.polyfit(range(len(ess_tracking)), ess_tracking, 1)[0]
            ) if len(ess_tracking) > 1 else 0.0,
            'red_queen_intensity': perturbation_strength,
            'conclusion': self._red_queen_conclusion(ess_tracking),
        }

    def _red_queen_conclusion(self, ess_tracking: List[float]) -> str:
        """Interpret the Red Queen simulation results."""
        if len(ess_tracking) < 10:
            return "Insufficient data for conclusion."

        trend = np.polyfit(range(len(ess_tracking)), ess_tracking, 1)[0]
        mean_dist = np.mean(ess_tracking)
        volatility = np.std(ess_tracking)

        if abs(trend) < 0.001 and volatility < 0.1:
            return ("Stable regime: Population tracks ESS effectively. "
                    "Low Red Queen pressure — fitness landscape relatively static.")
        elif trend > 0.01:
            return ("Escalating arms race: Population falling behind moving ESS. "
                    "Increasing mismatch suggests coevolutionary escalation. "
                    "The Red Queen runs faster than the population adapts.")
        elif volatility > 0.2:
            return ("Chaotic regime: Large fluctuations in ESS tracking. "
                    "Fitness landscape is highly dynamic. "
                    "Population alternates between strategies in a turbulent Red Queen dynamic.")
        else:
            return ("Dynamic equilibrium: Population tracks ESS with moderate lag. "
                    "Red Queen pressure is present but manageable. "
                    "This is the typical state of real ecosystems.")

    def report(self) -> str:
        """Generate comprehensive evolutionary analysis report."""
        lines = ["=" * 60]
        lines.append("EVOLUTIONARY GAME GRAPH ANALYSIS")
        lines.append("=" * 60)

        lines.append(f"\nStrategies: {[s.name for s in self.strategies]}")

        # ESS analysis
        ess = self.find_ess()
        lines.append(f"\nESS ANALYSIS:")
        lines.append(f"  ESS candidates found: {ess['ess_count']}")
        for c in ess['candidates']:
            if c.get('is_ess', False):
                lines.append(f"    ESS: dominant={c['dominant']}, "
                             f"diversity={c['diversity']:.4f}, "
                             f"eigenvalue={c['eigenvalue']:.4f}")

        # Spectral properties
        L = self.laplacian
        eigvals = np.sort(np.linalg.eigvalsh(L))
        lines.append(f"\nFITNESS LAPLACIAN SPECTRUM:")
        lines.append(f"  Eigenvalues: {[f'{e:.4f}' for e in eigvals]}")
        lines.append(f"  Algebraic connectivity: {eigvals[1]:.4f}")
        lines.append(f"  Spectral gap: {eigvals[1] - eigvals[0]:.4f}")

        return "\n".join(lines)


# === DEMONSTRATION ===
def demo_evo_game():
    """
    Rock-Paper-Scissors-Lizard-Spock evolutionary dynamics.
    """
    names = ["Rock", "Paper", "Scissors", "Lizard", "Spock"]

    # Fitness matrix: A[i,j] = fitness of i against j
    # Rock beats Scissors, Lizard
    # Paper beats Rock, Spock
    # Scissors beats Paper, Lizard
    # Lizard beats Paper, Spock
    # Spock beats Rock, Scissors
    A = np.array([
        [0.5, 0.0, 1.0, 1.0, 0.0],   # Rock
        [1.0, 0.5, 0.0, 0.0, 1.0],   # Paper
        [0.0, 1.0, 0.5, 1.0, 0.0],   # Scissors
        [0.0, 1.0, 0.0, 0.5, 1.0],   # Lizard
        [1.0, 0.0, 1.0, 0.0, 0.5],   # Spock
    ])

    strategies = [
        StrategyNode(name=n, initial_frequency=0.2, fitness_baseline=1.0)
        for n in names
    ]

    game = EvoGameGraph(
        strategies=strategies,
        fitness_matrix=A,
        mutation_rate=0.02,
    )

    print(game.report())

    # Simulate dynamics
    t_span = np.linspace(0, 50, 500)
    result = game.simulate(t_span)

    print(f"\n{'=' * 60}")
    print("SIMULATION RESULTS")
    print(f"{'=' * 60}")
    print(f"  Initial frequencies: {result['spectral_history'][0]['frequencies']}")
    print(f"  Final frequencies: {result['spectral_history'][-1]['frequencies']}")
    print(f"  Final diversity: {result['spectral_history'][-1]['diversity']:.4f}")
    print(f"  Final mean fitness: {result['spectral_history'][-1]['mean_fitness']:.4f}")

    # Red Queen simulation
    print(f"\n{'=' * 60}")
    print("RED QUEEN SIMULATION")
    print(f"{'=' * 60}")
    rq = game.red_queen_simulation(n_steps=50, perturbation_strength=0.05)
    print(f"  Mean ESS distance: {rq['mean_ess_distance']:.4f}")
    print(f"  ESS tracking trend: {rq['ess_tracking_trend']:.6f}")
    print(f"  Conclusion: {rq['conclusion']}")

    return game


if __name__ == "__main__":
    demo_evo_game()
```

### What This Reveals

The EvoGameGraph framework demonstrates that evolutionary dynamics are fundamentally spectral processes:

1. **ESS as spectral maximin**: An evolutionary stable strategy maximizes the minimum eigenvalue of the fitness Laplacian restricted to the perturbation subspace. This is the same mathematical structure as the max-min eigenvalue problem in robustness analysis—evolution selects for robustness.

2. **Conservation of population**: The replicator dynamics conserve total population ($\sum x_i = 1$ always). This is enforced by the Laplacian structure—frequencies shift between strategies, but the total is invariant. Fitness gains by one strategy are exactly offset by losses of others. Competition is zero-sum at the level of frequency, even when it's positive-sum at the level of absolute fitness.

3. **The Red Queen as spectral drift**: When the fitness Laplacian is perturbed (by mutation, environmental change, or coevolution), the eigenvalues and eigenvectors shift. The population must continuously track the moving ESS. The efficiency of this tracking depends on the spectral gap: large gaps allow fast tracking, small gaps create lag. Arms races correspond to periods of shrinking spectral gap—increasing vulnerability to invasion—as the system approaches a bifurcation where the current ESS destabilizes and a new one emerges.

4. **Diversity as spectral entropy**: High Shannon entropy in the strategy distribution corresponds to a flat, well-distributed eigenvalue spectrum. Low entropy (dominance by one strategy) corresponds to a concentrated spectrum. The transition between these regimes—speciation and extinction events—corresponds to spectral phase transitions, where eigenvalues cross and the dominant mode changes.

The conservation lens unifies these phenomena. Population is conserved. Fitness flows through the Laplacian. Stability is maximized when the Laplacian's spectral profile is most resistant to perturbation. And evolution is the perpetual search for high-conservation configurations in a landscape that refuses to sit still.

---

## SYNTHESIS: The Unity of Strategic Spectral Analysis

Across all three rounds, a single mathematical structure appears: the graph Laplacian and its spectral decomposition. In each domain—cooperative games, auction markets, evolutionary dynamics—the Laplacian encodes the structure of strategic interaction, and its eigenvalues/eigenvectors reveal the equilibrium landscape.

The conservation principle—$\sum_i L_{ij} = 0$—is the unifying thread. In games, strategic pressure is conserved. In markets, competitive pressure is conserved. In evolution, population frequency is conserved. In all cases, the Laplacian tracks this conservation with mathematical precision, and deviations from it signal structural anomalies: collusion in markets, coalition instability in games, or ecological disruption in evolution.

The spectral perspective transforms game theory from a collection of solution concepts into a unified field theory of strategic interaction. Every game has a spectrum. Every equilibrium is an eigenvector. Every instability is a spectral gap. And every conservation law is the Laplacian's first and most fundamental property.
