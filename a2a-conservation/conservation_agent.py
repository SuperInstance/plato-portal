"""
ConservationAgent — An agent whose identity IS its spectral fingerprint.

Each agent builds a capability graph (nodes = capabilities, edges = composability),
computes the graph Laplacian, and derives a spectral fingerprint. Two agents can
assess their structural compatibility through a single dot product.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import json


@dataclass
class SpectralFingerprint:
    """The compressed structural identity of an agent."""
    agent_id: str
    eigenvalues: List[float]
    spectral_gap: float
    cheeger_constant: float
    spectral_entropy: float
    fiedler_vector: List[float]
    capability_count: int
    graph_density: float
    alignment_threshold: float = 0.15

    def to_dict(self) -> dict:
        return {
            'agent_id': self.agent_id,
            'eigenvalues': self.eigenvalues,
            'spectral_gap': self.spectral_gap,
            'cheeger_constant': self.cheeger_constant,
            'spectral_entropy': self.spectral_entropy,
            'fiedler_vector': self.fiedler_vector,
            'capability_count': self.capability_count,
            'graph_density': self.graph_density,
            'alignment_threshold': self.alignment_threshold,
        }

    @classmethod
    def from_dict(cls, d: dict) -> 'SpectralFingerprint':
        return cls(**d)


class ConservationAgent:
    """
    An agent that communicates through spectral structure.
    Its 'language' IS its tension graph.
    """

    def __init__(self, name: str, capabilities: List[str],
                 compatibility_fn: Optional[callable] = None):
        self.name = name
        self.capabilities = capabilities
        self.compatibility_fn = compatibility_fn or self._default_compatibility
        self.tension_graph = self._build_capability_graph(capabilities)
        self.spectral_fingerprint = self._compute_fingerprint()

    def _default_compatibility(self, cap_a: str, cap_b: str) -> float:
        """
        Default compatibility: related capabilities get higher weights.
        Uses simple keyword overlap heuristic.
        """
        # Shared word stems indicate related capabilities
        words_a = set(cap_a.lower().replace('-', ' ').replace('_', ' ').split())
        words_b = set(cap_b.lower().replace('-', ' ').replace('_', ' ').split())
        overlap = len(words_a & words_b)
        # Base weight + overlap bonus
        base = 0.1
        return min(base + overlap * 0.3, 1.0)

    def _build_capability_graph(self, capabilities: List[str]) -> Dict:
        """
        Each capability is a node.
        Edges = how capabilities relate (can compose, can chain, can substitute).
        Weights = compatibility (how well they work together).
        """
        n = len(capabilities)
        graph = {
            'nodes': capabilities,
            'adjacency': np.zeros((n, n)),
            'n': n,
        }

        for i in range(n):
            for j in range(i + 1, n):
                w = self.compatibility_fn(capabilities[i], capabilities[j])
                graph['adjacency'][i][j] = w
                graph['adjacency'][j][i] = w

        return graph

    def _build_laplacian(self, graph: Dict) -> np.ndarray:
        """Build the graph Laplacian L = D - W."""
        W = graph['adjacency']
        D = np.diag(W.sum(axis=1))
        L = D - W
        return L

    def _cheeger(self, fiedler: np.ndarray) -> float:
        """
        Approximate Cheeger constant from the Fiedler vector.
        h(G) ≈ min_S |∂S| / min(vol(S), vol(V\S))
        where S is defined by the Fiedler partition.
        """
        n = len(fiedler)
        W = self.tension_graph['adjacency']
        median = np.median(fiedler)
        S = fiedler > median
        S_bar = ~S

        if S.sum() == 0 or S_bar.sum() == 0:
            return 0.0

        # Edge cut weight
        cut = W[np.ix_(S, S_bar)].sum()

        # Volumes
        vol_S = W[S].sum()
        vol_Sbar = W[S_bar].sum()

        if vol_S == 0 or vol_Sbar == 0:
            return 0.0

        return float(cut / min(vol_S, vol_Sbar))

    def _compute_fingerprint(self) -> SpectralFingerprint:
        """
        Spectral fingerprint = the agent's identity in conservation space.
        Two agents with similar fingerprints can collaborate efficiently.
        """
        L = self._build_laplacian(self.tension_graph)
        eigenvalues, eigenvectors = np.linalg.eigh(L)

        # Fiedler vector (second eigenvector)
        fiedler = eigenvectors[:, 1] if eigenvectors.shape[1] > 1 else np.zeros(eigenvectors.shape[0])

        # Spectral gap
        spectral_gap = float(eigenvalues[1] - eigenvalues[0]) if len(eigenvalues) > 1 else 0.0

        # Cheeger constant approximation
        cheeger = self._cheeger(fiedler)

        # Spectral entropy (measures how spread out the spectrum is)
        ev_pos = eigenvalues[eigenvalues > 0]
        if len(ev_pos) > 0 and ev_pos.sum() > 0:
            probs = ev_pos / ev_pos.sum()
            entropy = float(-np.sum(probs * np.log(probs + 1e-10)))
        else:
            entropy = 0.0

        # Graph density
        n = self.tension_graph['n']
        max_edges = n * (n - 1) / 2 if n > 1 else 1
        actual_edges = (self.tension_graph['adjacency'] > 0).sum() / 2
        density = actual_edges / max_edges if max_edges > 0 else 0

        return SpectralFingerprint(
            agent_id=self.name,
            eigenvalues=eigenvalues.tolist(),
            spectral_gap=spectral_gap,
            cheeger_constant=cheeger,
            spectral_entropy=entropy,
            fiedler_vector=fiedler.tolist(),
            capability_count=n,
            graph_density=float(density),
        )

    def can_collaborate_with(self, other: 'ConservationAgent') -> float:
        """
        Conservation alignment between two agents.
        High alignment = agents understand each other's structure.
        Returns alignment coefficient α ∈ [0, 1] (or negative for anti-alignment).
        """
        fp_self = np.array(self.spectral_fingerprint.eigenvalues)
        fp_other = np.array(other.spectral_fingerprint.eigenvalues)

        # Pad to same length
        max_len = max(len(fp_self), len(fp_other))
        fp_self = np.pad(fp_self, (0, max_len - len(fp_self)))
        fp_other = np.pad(fp_other, (0, max_len - len(fp_other)))

        # Cosine similarity of eigenvalue spectra
        dot = np.dot(fp_self, fp_other)
        norm_self = np.linalg.norm(fp_self)
        norm_other = np.linalg.norm(fp_other)

        if norm_self < 1e-10 or norm_other < 1e-10:
            return 0.0

        alignment = dot / (norm_self * norm_other)
        return float(alignment)

    def compose_with(self, other: 'ConservationAgent',
                     cross_weight: float = 0.5) -> Dict:
        """
        Compose two agents. The composition graph is the union of both
        agents' capability graphs plus cross-edges.
        """
        composed_graph = self._merge_graphs(other, cross_weight)
        L = self._build_laplacian(composed_graph)
        eigenvalues, eigenvectors = np.linalg.eigh(L)

        # Conservation ratio of the composition (using uniform attribute)
        n = composed_graph['n']
        a = np.ones(n) / np.sqrt(n)
        a = a - a.mean()  # Center
        if np.linalg.norm(a) > 1e-10:
            a = a / np.linalg.norm(a)
        cr = float(a @ L @ a)

        # Fiedler routing
        fiedler = eigenvectors[:, 1] if eigenvectors.shape[1] > 1 else np.zeros(n)

        # Partition: positive fiedler → self, negative → other
        n_self = self.tension_graph['n']
        partition_self = [i for i in range(n_self) if fiedler[i] >= 0]
        partition_other = [i for i in range(n_self, n) if fiedler[i] < 0]

        # If Fiedler doesn't split well, assign by capability count
        if len(partition_self) == 0:
            partition_self = list(range(n_self))
        if len(partition_other) == 0:
            partition_other = list(range(n_self, n))

        return {
            'composed_graph': composed_graph,
            'eigenvalues': eigenvalues.tolist(),
            'eigenvectors': eigenvectors.tolist(),
            'conservation_ratio': cr,
            'fiedler_vector': fiedler.tolist(),
            'alignment': self.can_collaborate_with(other),
            'partition_self': partition_self,
            'partition_other': partition_other,
        }

    def _merge_graphs(self, other: 'ConservationAgent',
                      cross_weight: float) -> Dict:
        """Merge two capability graphs with cross-edges."""
        n_self = self.tension_graph['n']
        n_other = other.tension_graph['n']
        n_total = n_self + n_other

        W = np.zeros((n_total, n_total))

        # Self graph
        W[:n_self, :n_self] = self.tension_graph['adjacency']

        # Other graph
        W[n_self:, n_self:] = other.tension_graph['adjacency']

        # Cross-edges: compatibility between self and other capabilities
        for i in range(n_self):
            for j in range(n_other):
                # Use cross-weight scaled by compatibility
                w = cross_weight * self._cross_compatibility(
                    self.capabilities[i], other.capabilities[j]
                )
                W[i, n_self + j] = w
                W[n_self + j, i] = w

        nodes = self.capabilities + other.capabilities
        return {'nodes': nodes, 'adjacency': W, 'n': n_total}

    def _cross_compatibility(self, cap_a: str, cap_b: str) -> float:
        """Compute compatibility between capabilities of different agents."""
        return self.compatibility_fn(cap_a, cap_b)

    def __repr__(self) -> str:
        return (f"ConservationAgent({self.name!r}, "
                f"capabilities={self.capabilities}, "
                f"spectral_gap={self.spectral_fingerprint.spectral_gap:.3f})")
