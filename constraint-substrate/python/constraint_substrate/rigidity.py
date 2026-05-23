"""Laman rigidity checking."""

from itertools import combinations
from typing import List, Tuple


def _edge_count_in_subgraph(
    edges: List[Tuple[int, int]], vertex_subset: Tuple[int, ...]
) -> int:
    """Count edges where both endpoints lie in the vertex subset."""
    vertex_set = set(vertex_subset)
    count = 0
    for u, v in edges:
        if u in vertex_set and v in vertex_set:
            count += 1
    return count


def is_laman(n: int, edges: List[Tuple[int, int]]) -> bool:
    """Check if a graph with n vertices and given edges satisfies
    Laman's condition for generic rigidity in 2D.

    Laman's theorem: a graph G = (V, E) is generically minimally rigid
    in 2D if and only if:
      1. |E| = 2|V| - 3  (for |V| >= 2)
      2. For every subset of k >= 2 vertices, the induced subgraph
         has at most 2k - 3 edges.

    We also accept graphs with |E| >= 2|V| - 3 as rigid (they may be
    over-constrained but are still rigid).

    For the subgraph condition, we check that no subgraph on k vertices
    has more than 2k - 3 edges. This is necessary for generic rigidity.
    """
    if n < 2:
        return False
    if n == 2:
        return len(edges) >= 1

    # Condition 1: must have exactly 2n-3 edges (minimally rigid)
    # or more (rigid but over-constrained). Having fewer means not rigid.
    if len(edges) < 2 * n - 3:
        return False

    # Condition 2: Laman subgraph condition — every subset of k vertices
    # must span at most 2k - 3 edges.
    # Check all subsets of size 2..n (skip k=1 since 2*1-3 = -1, trivially ok).
    # For large n this is exponential; we cap at n <= 10 for exact check,
    # otherwise use a sampling heuristic.
    vertices = list(range(n))

    if n <= 10:
        # Exact check via enumeration
        for k in range(2, n + 1):
            limit = 2 * k - 3
            for subset in combinations(vertices, k):
                if _edge_count_in_subgraph(edges, subset) > limit:
                    return False
    else:
        # For large graphs, check random subsets as a probabilistic check.
        # A full pebble game algorithm would be better but this is a
        # reference implementation.
        import random
        random.seed(42)  # deterministic for reproducibility
        for _ in range(min(1000, n * n)):
            k = random.randint(2, n)
            subset = tuple(random.sample(vertices, k))
            limit = 2 * k - 3
            if _edge_count_in_subgraph(edges, subset) > limit:
                return False

    return True
