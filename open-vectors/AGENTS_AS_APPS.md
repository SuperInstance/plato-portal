# Agents as Applications: open-vectors

## The Agent IS the Search Engine

In traditional vector databases, you write a search query and get cosine-similar results back. In open-vectors, **the agent itself is the search engine**. It doesn't write search queries — it computes Wasserstein distances between meaning distributions and eigenvalue similarities between document structures.

### How It Works

1. **Spectral Search**: Instead of comparing vectors directly, we compute the eigenvalue profile of each document's embedding. The eigenvalue profile captures the "energy distribution" of the vector — how concentrated vs. spread out the semantic content is. Results are ranked by how well their eigenvalue profile matches the query's.

2. **Wasserstein Search**: Each document's embedding is converted to a probability distribution. The Wasserstein distance (Earth Mover's Distance) measures the minimum cost to transform one distribution into another. This captures structural shifts that cosine similarity misses — a document about "machine learning" and one about "deep learning" have similar but shifted distributions.

3. **Beyond Cosine**: Cosine similarity treats vectors as points in space. But embeddings carry distributional information. Two documents with the same cosine similarity to a query can have very different structural relationships. Wasserstein and spectral metrics capture these differences.

### Architecture

```
┌──────────────────────────────────────────┐
│  open-vectors (Weaviate fork)            │
│                                          │
│  ┌──────────────────────────────────────┐│
│  │ si_integration/                      ││
│  │                                      ││
│  │  SpectralSearchEngine                ││
│  │  ├── index(documents)                ││
│  │  ├── search(query_vector) → results  ││
│  │  └── eigenvalue profile comparison   ││
│  │                                      ││
│  │  WassersteinSearchEngine             ││
│  │  ├── index(documents)                ││
│  │  ├── search(query_vector) → results  ││
│  │  └── distribution distance           ││
│  └──────────────────────────────────────┘│
└──────────────────────────────────────────┘
```

### Why Wasserstein?

Cosine similarity is a point metric — it measures the angle between two vectors. But embeddings represent distributions over semantic space. The Wasserstein distance respects the geometry of this space:

- **Shift invariance**: A distribution shifted by one topic dimension has small Wasserstein distance but potentially large cosine distance.
- **Spread sensitivity**: A broad topic distribution vs. a narrow one are clearly distinguished.
- **Transport interpretation**: The distance has a physical meaning — how much "semantic mass" must be moved to transform one document into another.

### Files

- `si_integration/spectral_search.py` — Eigenvalue profile search engine
- `si_integration/wasserstein_search.py` — Wasserstein distance search engine
