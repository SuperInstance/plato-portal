# constraint-toolkit

Python analysis toolkit for constraint space visualization, tradition clustering, and lattice exploration.

## What This Gives You

- **Lattice plots** — Visualize partially-ordered constraint lattices as ASCII diagrams
- **Dial positions** — Represent and compare circular constraint values (angle + radius)
- **Tradition clusters** — Group musical traditions by constraint similarity with Euclidean distance
- **Export** — Dump analysis results to JSON, CSV, or Markdown reports
- **Zero dependencies** — Pure Python, no external packages required

## Quick Start

```python
from constraint_toolkit import (
    ConstraintLattice, LatticeNode,
    DialSpace, DialPosition,
    TraditionCluster, Tradition,
)

# Build a constraint lattice
lattice = ConstraintLattice("Harmonic")
lattice.add_node(LatticeNode("root", level=0))
lattice.add_node(LatticeNode("major", level=1, coordinates=(1, 0)))
lattice.add_node(LatticeNode("minor", level=1, coordinates=(0, 1)))

# Compare traditions
jazz = Tradition("Jazz", scores={"tension": 0.8, "complexity": 0.9})
blues = Tradition("Blues", scores={"tension": 0.7, "complexity": 0.5})
print(f"Distance: {jazz.distance_to(blues):.3f}")

# Cluster and export
cluster = TraditionCluster(traditions=[jazz, blues])
cluster.find_clusters(threshold=0.5)
```

## API Reference

### `constraint_toolkit.lattice`

| Class | Description |
|-------|-------------|
| `LatticeNode` | Frozen dataclass: name, level, coordinates, metadata |
| `ConstraintLattice` | Named lattice with add/lookup/query operations |

### `constraint_toolkit.dial`

| Class | Description |
|-------|-------------|
| `DialPosition` | Circular position (angle in radians, normalized to [0, 2π)) |
| `DialSpace` | Collection of dial positions with distance computation |

### `constraint_toolkit.tradition`

| Class | Description |
|-------|-------------|
| `Tradition` | Named tradition with constraint scores dict |
| `TraditionCluster` | Group traditions by similarity, find clusters |

### `constraint_toolkit.visualization`

ASCII rendering of lattices, dial spaces, and tradition clusters.

### `constraint_toolkit.export`

Export to JSON, CSV, and Markdown formats.

## How It Fits

Part of the [SuperInstance](https://github.com/SuperInstance) constraint theory ecosystem. This toolkit sits between the core math ([constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core)) and higher-level tools, providing human-readable analysis and export of constraint structures.

## Testing

```bash
pip install -e ".[dev]"
pytest
```

## Installation

```bash
pip install -e .
```

Requires Python ≥ 3.10. No external dependencies.

## License

MIT
