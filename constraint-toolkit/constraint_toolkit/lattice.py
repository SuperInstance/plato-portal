"""Constraint lattice — nodes arranged in a partially-ordered lattice structure."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class LatticeNode:
    """A single node in a constraint lattice."""

    name: str
    level: int
    coordinates: tuple[float, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict, hash=False)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LatticeNode):
            return NotImplemented
        return self.name == other.name and self.level == other.level

    def __hash__(self) -> int:
        return hash((self.name, self.level))


class ConstraintLattice:
    """Partially-ordered lattice of constraint nodes with join/meet operations."""

    def __init__(self) -> None:
        self._nodes: dict[str, LatticeNode] = {}
        self._edges: list[tuple[str, str]] = []
        self._order: dict[str, set[str]] = {}  # node -> nodes it is <= than

    def add_node(self, node: LatticeNode) -> None:
        self._nodes[node.name] = node
        if node.name not in self._order:
            self._order[node.name] = {node.name}

    def add_edge(self, parent: str, child: str) -> None:
        if parent not in self._nodes or child not in self._nodes:
            raise ValueError(f"Both nodes must exist: {parent}, {child}")
        self._edges.append((parent, child))
        # Transitive closure for partial order
        self._rebuild_order()

    def _rebuild_order(self) -> None:
        # _order[x] = {y : x <= y}  (everything x is below-or-equal to)
        # Edge (parent, child) means child <= parent
        for name in self._nodes:
            self._order[name] = {name}
        changed = True
        while changed:
            changed = False
            for parent, child in self._edges:
                # child <= parent, so parent is in child's upper set
                # Also transitively, everything parent <= child also <=
                new_for_child = self._order[parent] | self._order.get(parent, {parent})
                before = len(self._order[child])
                self._order[child] |= self._order[parent]
                if len(self._order[child]) > before:
                    changed = True

    @property
    def nodes(self) -> list[LatticeNode]:
        return list(self._nodes.values())

    @property
    def edges(self) -> list[tuple[str, str]]:
        return list(self._edges)

    def leq(self, a: str, b: str) -> bool:
        """Check if node a <= node b in the partial order."""
        return b in self._order.get(a, {a})

    def join(self, a: str, b: str) -> str | None:
        """Find the least upper bound (join) of two nodes."""
        upper_a = {n for n in self._nodes if self.leq(a, n)}
        upper_b = {n for n in self._nodes if self.leq(b, n)}
        candidates = upper_a & upper_b
        if not candidates:
            return None
        # Return candidate with minimum level that no other candidate is below
        min_level = min(self._nodes[n].level for n in candidates)
        joins = [n for n in candidates if self._nodes[n].level == min_level]
        return joins[0] if len(joins) == 1 else None

    def meet(self, a: str, b: str) -> str | None:
        """Find the greatest lower bound (meet) of two nodes."""
        lower_a = {n for n in self._nodes if self.leq(n, a)}
        lower_b = {n for n in self._nodes if self.leq(n, b)}
        candidates = lower_a & lower_b
        if not candidates:
            return None
        max_level = max(self._nodes[n].level for n in candidates)
        meets = [n for n in candidates if self._nodes[n].level == max_level]
        return meets[0] if len(meets) == 1 else None

    def ancestors(self, name: str) -> set[str]:
        return {n for n in self._nodes if self.leq(name, n) and n != name}

    def descendants(self, name: str) -> set[str]:
        return {n for n in self._nodes if self.leq(n, name) and n != name}
