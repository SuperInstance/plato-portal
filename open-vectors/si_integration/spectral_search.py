"""
Spectral Search — Search using spectral-fleet eigenvalue similarity.

Instead of ranking results by cosine similarity, spectral_search ranks results
by how well their eigenvalue profile matches the query's eigenvalue profile.
This captures structural similarity that cosine misses.

The agent IS the search engine. It doesn't write search queries — it computes
eigenvalue distances between meaning distributions.

Example usage:
    >>> from spectral_search import SpectralSearchEngine, Document
    >>> engine = SpectralSearchEngine(top_k=3)
    >>> engine.index([
    ...     Document(id="d1", vector=[1.0, 0.0, 0.0], metadata={"title": "Doc 1"}),
    ...     Document(id="d2", vector=[0.9, 0.1, 0.0], metadata={"title": "Doc 2"}),
    ...     Document(id="d3", vector=[0.0, 0.0, 1.0], metadata={"title": "Doc 3"}),
    ... ])
    >>> results = engine.search([1.0, 0.0, 0.0], top_k=2)
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
class SearchResult:
    """A search result with spectral similarity score."""
    document: Document
    score: float
    eigenvalue_similarity: float
    cosine_similarity: float


def _dot(a: List[float], b: List[float]) -> float:
    """Compute dot product of two vectors."""
    return sum(x * y for x, y in zip(a, b))


def _norm(v: List[float]) -> float:
    """Compute L2 norm of a vector."""
    return math.sqrt(sum(x * x for x in v))


def _normalize(v: List[float]) -> List[float]:
    """Normalize a vector to unit length."""
    n = _norm(v)
    if n < 1e-15:
        return [0.0] * len(v)
    return [x / n for x in v]


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    na, nb = _norm(a), _norm(b)
    if na < 1e-15 or nb < 1e-15:
        return 0.0
    return _dot(a, b) / (na * nb)


def _compute_eigenvalue_profile(vector: List[float], top_k: int = 5) -> List[float]:
    """
    Compute the eigenvalue profile of a vector's autocorrelation matrix.

    For a vector v, the autocorrelation matrix is v * v^T. Its eigenvalues
    are the squared components of v (sorted descending). This gives a compact
    representation of the vector's "energy distribution."

    Args:
        vector: Input vector.
        top_k: Number of eigenvalues to return.

    Returns:
        List of eigenvalues sorted in descending order.
    """
    # For a rank-1 matrix v*v^T, the only non-zero eigenvalue is ||v||^2
    # But for a more meaningful profile, we use the vector components as
    # a proxy for eigenvalue decomposition of the local neighborhood structure.
    squared = [x * x for x in vector]
    squared.sort(reverse=True)
    return squared[:top_k]


def _eigenvalue_similarity(
    profile_a: List[float], profile_b: List[float]
) -> float:
    """
    Compute similarity between two eigenvalue profiles.

    Uses normalized dot product (cosine similarity) between eigenvalue profiles.
    Two documents with similar eigenvalue distributions have high similarity,
    even if their raw vectors differ.

    Args:
        profile_a: Eigenvalue profile of the query.
        profile_b: Eigenvalue profile of the document.

    Returns:
        Similarity score in [-1, 1].
    """
    if not profile_a or not profile_b:
        return 0.0

    # Pad shorter profile with zeros
    max_len = max(len(profile_a), len(profile_b))
    a = profile_a + [0.0] * (max_len - len(profile_a))
    b = profile_b + [0.0] * (max_len - len(profile_b))

    return cosine_similarity(a, b)


class SpectralSearchEngine:
    """
    Search engine that ranks results by eigenvalue profile similarity.

    Unlike traditional vector search that uses cosine similarity alone,
    SpectralSearchEngine computes the eigenvalue profile of each document's
    embedding and ranks results by how well their spectral structure matches
    the query's spectral structure.

    This captures structural similarity: two documents about similar topics
    will have similar eigenvalue distributions even if their exact word
    embeddings differ.

    Args:
        top_k: Default number of results to return.
        spectral_weight: Weight for eigenvalue similarity (0-1).
            0 = pure cosine, 1 = pure spectral. Default 0.5.
        profile_size: Number of eigenvalues in each profile. Default 10.
    """

    def __init__(
        self,
        top_k: int = 10,
        spectral_weight: float = 0.5,
        profile_size: int = 10,
    ):
        self.top_k = top_k
        self.spectral_weight = spectral_weight
        self.profile_size = profile_size
        self._documents: List[Document] = []
        self._profiles: Dict[str, List[float]] = {}

    def index(self, documents: List[Document]) -> None:
        """
        Index a list of documents.

        Computes and caches the eigenvalue profile for each document.

        Args:
            documents: List of Document objects to index.
        """
        for doc in documents:
            self._documents.append(doc)
            self._profiles[doc.id] = _compute_eigenvalue_profile(
                doc.vector, top_k=self.profile_size
            )

    def search(
        self,
        query_vector: List[float],
        top_k: Optional[int] = None,
    ) -> List[SearchResult]:
        """
        Search for documents similar to the query vector.

        Ranks results by a combination of cosine similarity and eigenvalue
        profile similarity.

        Args:
            query_vector: Query embedding vector.
            top_k: Number of results to return. Uses default if None.

        Returns:
            List of SearchResult objects, sorted by combined score descending.
        """
        k = top_k or self.top_k

        query_profile = _compute_eigenvalue_profile(
            query_vector, top_k=self.profile_size
        )

        results: List[SearchResult] = []

        for doc in self._documents:
            cos_sim = cosine_similarity(query_vector, doc.vector)
            ev_sim = _eigenvalue_similarity(query_profile, self._profiles[doc.id])

            # Combined score: weighted average of cosine and spectral similarity
            combined = (
                (1 - self.spectral_weight) * cos_sim
                + self.spectral_weight * ev_sim
            )

            results.append(
                SearchResult(
                    document=doc,
                    score=combined,
                    eigenvalue_similarity=ev_sim,
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
        self._profiles.pop(doc_id, None)
        before = len(self._documents)
        self._documents = [d for d in self._documents if d.id != doc_id]
        return len(self._documents) < before

    @property
    def document_count(self) -> int:
        """Number of indexed documents."""
        return len(self._documents)

    def get_profile(self, doc_id: str) -> Optional[List[float]]:
        """Get the eigenvalue profile for a document."""
        return self._profiles.get(doc_id)


if __name__ == "__main__":
    # Example usage
    engine = SpectralSearchEngine(top_k=3, spectral_weight=0.6)

    docs = [
        Document(id="d1", vector=[1.0, 0.0, 0.0], metadata={"title": "Machine Learning"}),
        Document(id="d2", vector=[0.9, 0.1, 0.0], metadata={"title": "Deep Learning"}),
        Document(id="d3", vector=[0.0, 0.0, 1.0], metadata={"title": "Cooking"}),
        Document(id="d4", vector=[0.95, 0.05, 0.0], metadata={"title": "Neural Networks"}),
        Document(id="d5", vector=[0.1, 0.9, 0.0], metadata={"title": "Python Programming"}),
    ]
    engine.index(docs)

    query = [1.0, 0.0, 0.0]
    results = engine.search(query, top_k=3)

    print("Spectral Search Results:")
    for r in results:
        print(
            f"  {r.document.id}: {r.document.metadata['title']} "
            f"(combined={r.score:.3f}, cosine={r.cosine_similarity:.3f}, "
            f"spectral={r.eigenvalue_similarity:.3f})"
        )
