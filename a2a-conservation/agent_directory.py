"""
Agent Directory — agents register by publishing their spectral fingerprint.

The directory supports alignment queries: given an agent's fingerprint,
find all registered agents with alignment above a threshold.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from conservation_agent import ConservationAgent, SpectralFingerprint


@dataclass
class DirectoryEntry:
    """A registered agent in the directory."""
    agent_id: str
    fingerprint: SpectralFingerprint
    metadata: Dict = field(default_factory=dict)


class AgentDirectory:
    """
    Spectral fingerprint directory for agent discovery.
    
    Agents register by publishing their spectral fingerprint (not their API).
    Discovery happens through alignment computation.
    """

    def __init__(self):
        self._registry: Dict[str, DirectoryEntry] = {}

    def register(self, agent: ConservationAgent, metadata: Dict = None) -> None:
        """Register an agent by its spectral fingerprint."""
        self._registry[agent.name] = DirectoryEntry(
            agent_id=agent.name,
            fingerprint=agent.spectral_fingerprint,
            metadata=metadata or {},
        )

    def unregister(self, agent_id: str) -> None:
        """Remove an agent from the directory."""
        self._registry.pop(agent_id, None)

    def get(self, agent_id: str) -> Optional[DirectoryEntry]:
        """Get a specific agent's entry."""
        return self._registry.get(agent_id)

    def list_agents(self) -> List[str]:
        """List all registered agent IDs."""
        return list(self._registry.keys())

    def compute_alignment(self, fp_a: SpectralFingerprint,
                          fp_b: SpectralFingerprint) -> float:
        """
        Compute spectral alignment between two fingerprints.
        Cosine similarity of eigenvalue spectra.
        """
        ev_a = np.array(fp_a.eigenvalues)
        ev_b = np.array(fp_b.eigenvalues)

        # Pad to same length
        max_len = max(len(ev_a), len(ev_b))
        ev_a = np.pad(ev_a, (0, max_len - len(ev_a)))
        ev_b = np.pad(ev_b, (0, max_len - len(ev_b)))

        dot = np.dot(ev_a, ev_b)
        norm_a = np.linalg.norm(ev_a)
        norm_b = np.linalg.norm(ev_b)

        if norm_a < 1e-10 or norm_b < 1e-10:
            return 0.0

        return float(dot / (norm_a * norm_b))

    def find_collaborators(self, agent: ConservationAgent,
                           min_alignment: float = 0.15,
                           exclude_self: bool = True) -> List[Tuple[str, float]]:
        """
        Find agents with alignment above threshold.
        Returns list of (agent_id, alignment) sorted by alignment descending.
        """
        results = []
        for agent_id, entry in self._registry.items():
            if exclude_self and agent_id == agent.name:
                continue
            alignment = self.compute_alignment(
                agent.spectral_fingerprint, entry.fingerprint
            )
            if alignment >= min_alignment:
                results.append((agent_id, alignment))

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def find_best_collaborator(self, agent: ConservationAgent) -> Optional[Tuple[str, float]]:
        """Find the single best collaborator for an agent."""
        results = self.find_collaborators(agent, min_alignment=-1.0)
        return results[0] if results else None

    def alignment_matrix(self) -> Tuple[np.ndarray, List[str]]:
        """
        Compute the full pairwise alignment matrix.
        Returns (matrix, agent_ids).
        """
        agents = list(self._registry.keys())
        n = len(agents)
        matrix = np.eye(n)

        for i in range(n):
            for j in range(i + 1, n):
                fp_i = self._registry[agents[i]].fingerprint
                fp_j = self._registry[agents[j]].fingerprint
                alpha = self.compute_alignment(fp_i, fp_j)
                matrix[i, j] = alpha
                matrix[j, i] = alpha

        return matrix, agents

    def summary(self) -> str:
        """Human-readable summary of the directory."""
        lines = ["Agent Directory", "=" * 50]
        for agent_id, entry in self._registry.items():
            fp = entry.fingerprint
            lines.append(f"\n  {agent_id}:")
            lines.append(f"    Capabilities: {fp.capability_count}")
            lines.append(f"    Spectral gap: {fp.spectral_gap:.4f}")
            lines.append(f"    Cheeger constant: {fp.cheeger_constant:.4f}")
            lines.append(f"    Spectral entropy: {fp.spectral_entropy:.4f}")
            lines.append(f"    Graph density: {fp.graph_density:.4f}")

        if len(self._registry) > 1:
            matrix, agents = self.alignment_matrix()
            lines.append(f"\n  Alignment Matrix:")
            header = "         " + "  ".join(f"{a[:8]:>8}" for a in agents)
            lines.append(f"  {header}")
            for i, agent in enumerate(agents):
                row = "  ".join(f"{matrix[i, j]:8.3f}" for j in range(len(agents)))
                lines.append(f"  {agent[:8]:>8}  {row}")

        return "\n".join(lines)
