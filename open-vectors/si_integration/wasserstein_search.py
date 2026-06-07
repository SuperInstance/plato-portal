"""
Wasserstein Search — Search using Wasserstein distance between document distributions.

More robust than cosine similarity for distributional similarity. The Wasserstein
distance (Earth Mover's Distance) measures the minimum "cost" to transform one
distribution into another, capturing structural differences that point metrics miss.

The agent IS the search engine. It doesn't write search queries — it computes
Wasserstein distances between meaning distributions.

Example usage:
    >>> from wasserstein_search import WassersteinSearchEngine, Document
    >>> engine = WassersteinSearchEngine(top_k=3)
    >>> engine.index([
    ...     Document(id="d1", vector=[0.5, 0.3, 0.2], metadata={"title": "Doc 1"}),
    ...     Document(id="d2", vector=[0.4, 0.4, 0.2], metadata={"title": "Doc 2"}),
    ...     Document(id="d3", vector=[0.1, 0.1, 0.8], metadata={"title": "Doc 3"}),
    ... ])
    >>> results = engine.search([0.5, 0.3, 0.2], top_k=2)
    >>> len(results)
    2
    >>> results[0].document.id
    'd1'
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class Document:
    """A document with an embedding vector and metadata."""
    id: str
    vector: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WassersteinSearchResult:
    """A search result with Wasserstein distance score."""
    document: Document
    score: float  # Higher = more similar (converted from distance)
    wasserstein_distance: float
    cosine_similarity: float


def _to_distribution(vector: List[float]) -> List[float]:
    """
    Convert a vector to a probability distribution (sums to 1).

    Takes the absolute values and normalizes so that all components
    sum to 1.0, making it a valid probability distribution for
    Wasserstein distance computation.

    Args:
        vector: Input vector.

    Returns:
        Probability distribution (non-negative, sums to 1).
    """
    abs_vec = [abs(x) for x in vector]
    total = sum(abs_vec)
    if total < 1e-15:
        n = len(vector)
        return [1.0 / n] * n if n > 0 else []
    return [x / total for x in abs_vec]


def wasserstein_distance_1d(p: List[float], q: List[float]) -> float:
    """
    Compute the 1D Wasserstein distance (Earth Mover's Distance) between
    two discrete distributions.

    Uses the cumulative distribution function (CDF) method:
    W_1(P, Q) = sum |CDF_P(i) - CDF_Q(i)|

    This is the optimal transport cost for moving mass from distribution P
    to distribution Q on a 1D grid.

    Args:
        p: First probability distribution (must sum to 1).
        q: Second probability distribution (must sum to 1).

    Returns:
        Wasserstein-1 distance (non-negative).
    """
    n = max(len(p), len(q))

    # Pad with zeros if different lengths
    p = p + [0.0] * (n - len(p))
    q = q + [0.0] * (n - len(q))

    # Compute CDF difference
    cdf_p = 0.0
    cdf_q = 0.0
    distance = 0.0

    for i in range(n):
        cdf_p += p[i]
        cdf_q += q[i]
        distance += abs(cdf_p - cdf_q)

    return distance


def wasserstein_distance_sorted(
    p_values: List[float],
    q_values: List[float],
    p_weights: List[float],
    q_weights: List[float],
) -> float:
    """
    Compute the 1D Wasserstein distance between weighted point sets.

    More general version that handles arbitrary weighted samples.
    The points are sorted, and the distance is computed as the integral
    of the absolute difference of the CDFs.

    Args:
        p_values: Positions of points in distribution P.
        q_values: Positions of points in distribution Q.
        p_weights: Weights of points in P (sum to 1).
        q_weights: Weights of points in Q (sum to 1).

    Returns:
        Wasserstein-1 distance.
    """
    # Merge all positions
    all_positions = sorted(set(p_values + q_values))

    if not all_positions:
        return 0.0

    # Build CDFs
    def build_cdf(values: List[float], weights: List[float]) -> List[float]:
        """Build CDF at the merged positions."""
        cdf = []
        cumulative = 0.0
        v_idx = 0
        for pos in all_positions:
            while v_idx < len(values) and values[v_idx] <= pos:
                cumulative += weights[v_idx]
                v_idx += 1
            cdf.append(cumulative)
        return cdf

    # Sort p and q by value
    p_sorted = sorted(zip(p_values, p_weights))
    q_sorted = sorted(zip(q_values, q_weights))

    p_vals = [v for v, _ in p_sorted]
    p_wts = [w for _, w in p_sorted]
    q_vals = [v for v, _ in q_sorted]
    q_wts = [w for _, w in q_sorted]

    cdf_p = build_cdf(p_vals, p_wts)
    cdf_q = build_cdf(q_vals, q_wts)

    # Integrate |CDF_P - CDF_Q| * dx
    distance = 0.0
    for i in range(1, len(all_positions)):
        dx = all_positions[i] - all_positions[i - 1]
        mid_cdf_diff = abs(
            (cdf_p[i] + cdf_p[i - 1]) / 2 - (cdf_q[i] + cdf_q[i - 1]) / 2
        )
        distance += mid_cdf_diff * dx

    return distance


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na < 1e-15 or nb < 1e-15:
        return 0.0
    return dot / (na * nb)


class WassersteinSearchEngine:
    """
    Search engine that ranks results by Wasserstein distance between
    document distributions.

    Each document's embedding vector is converted to a probability distribution.
    The Wasserstein distance measures how much "work" is needed to transform
    one distribution into another, capturing structural similarity.

    More robust than cosine similarity for:
    - Documents with shifted topic distributions
    - Comparing documents of different "spread" (specificity)
    - Capturing ordering relationships between dimensions

    Args:
        top_k: Default number of results to return.
        wasserstein_weight: Weight for Wasserstein similarity (0-1).
            0 = pure cosine, 1 = pure Wasserstein. Default 0.7.
    """

    def __init__(
        self,
        top_k: int = 10,
        wasserstein_weight: float = 0.7,
    ):
        self.top_k = top_k
        self.wasserstein_weight = wasserstein_weight
        self._documents: List[Document] = []
        self._distributions: Dict[str, List[float]] = {}

    def index(self, documents: List[Document]) -> None:
        """
        Index a list of documents.

        Converts each document's vector to a probability distribution
        and caches it for fast distance computation.

        Args:
            documents: List of Document objects to index.
        """
        for doc in documents:
            self._documents.append(doc)
            self._distributions[doc.id] = _to_distribution(doc.vector)

    def search(
        self,
        query_vector: List[float],
        top_k: Optional[int] = None,
    ) -> List[WassersteinSearchResult]:
        """
        Search for documents similar to the query vector.

        Ranks results by a combination of cosine similarity and inverse
        Wasserstein distance.

        Args:
            query_vector: Query embedding vector.
            top_k: Number of results to return. Uses default if None.

        Returns:
            List of WassersteinSearchResult objects, sorted by combined
            score descending.
        """
        k = top_k or self.top_k
        query_dist = _to_distribution(query_vector)

        results: List[WassersteinSearchResult] = []

        for doc in self._documents:
            doc_dist = self._distributions[doc.id]

            # Compute Wasserstein distance
            w_dist = wasserstein_distance_1d(query_dist, doc_dist)

            # Convert distance to similarity: exp(-distance)
            # This maps [0, inf) -> (0, 1]
            w_sim = math.exp(-w_dist)

            # Cosine similarity
            cos_sim = cosine_similarity(query_vector, doc.vector)

            # Combined score
            combined = (
                (1 - self.wasserstein_weight) * cos_sim
                + self.wasserstein_weight * w_sim
            )

            results.append(
                WassersteinSearchResult(
                    document=doc,
                    score=combined,
                    wasserstein_distance=w_dist,
                    cosine_similarity=cos_sim,
                )
            )

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:k]

    def remove(self, doc_id: str) -> bool:
        """
        Remove a document from the index.

        Args:
            doc_id: ID of the document to remove.

        Returns:
            True if the document was found and removed.
        """
        self._distributions.pop(doc_id, None)
        before = len(self._documents)
        self._documents = [d for d in self._documents if d.id != doc_id]
        return len(self._documents) < before

    @property
    def document_count(self) -> int:
        """Number of indexed documents."""
        return len(self._documents)

    def get_distribution(self, doc_id: str) -> Optional[List[float]]:
        """Get the probability distribution for a document."""
        return self._distributions.get(doc_id)


if __name__ == "__main__":
    # Example usage
    engine = WassersteinSearchEngine(top_k=3, wasserstein_weight=0.7)

    docs = [
        Document(id="d1", vector=[0.5, 0.3, 0.2], metadata={"title": "Machine Learning"}),
        Document(id="d2", vector=[0.4, 0.4, 0.2], metadata={"title": "Deep Learning"}),
        Document(id="d3", vector=[0.1, 0.1, 0.8], metadata={"title": "Cooking"}),
        Document(id="d4", vector=[0.45, 0.35, 0.2], metadata={"title": "Neural Networks"}),
        Document(id="d5", vector=[0.2, 0.7, 0.1], metadata={"title": "Python Programming"}),
    ]
    engine.index(docs)

    query = [0.5, 0.3, 0.2]
    results = engine.search(query, top_k=3)

    print("Wasserstein Search Results:")
    for r in results:
        print(
            f"  {r.document.id}: {r.document.metadata['title']} "
            f"(combined={r.score:.3f}, w_dist={r.wasserstein_distance:.3f}, "
            f"cosine={r.cosine_similarity:.3f})"
        )
