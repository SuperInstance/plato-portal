"""
si_integration package — Spectral Instance integration for open-vectors.

Provides search algorithms that go beyond cosine similarity:
- spectral_search: Eigenvalue profile similarity
- wasserstein_search: Wasserstein (Earth Mover's) distance
"""

from .spectral_search import SpectralSearchEngine
from .wasserstein_search import WassersteinSearchEngine

__all__ = ["SpectralSearchEngine", "WassersteinSearchEngine"]
