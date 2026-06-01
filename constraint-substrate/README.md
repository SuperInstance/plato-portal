# constraint-substrate

Five constraint primitives verified across Python, Rust, and C — snap, funnel, is_laman, consensus, and holonomy with identical semantics in every language.

## What This Gives You

- **5 core primitives** — snap, funnel, is_laman, consensus, holonomy
- **3-language parity** — identical behavior in Python, Rust, and C
- **Cross-language verification** — test suite validates all implementations agree
- **Minimal API** — each primitive is one function call
- **No external dependencies** — each language implementation is self-contained

## Quick Start

### Python

```python
from constraint_substrate import snap, funnel, is_laman, consensus, holonomy

# Snap to Eisenstein A₂ lattice
point, error = snap(0.5, 0.3)

# Deadband funnel
result = funnel(error, decay=0.1, tolerance=0.001)

# Check Laman rigidity
edges = [(0,1), (1,2), (2,3), (3,0), (0,2)]
print(is_laman(4, edges))  # True: |E|=5 = 2·4-3

# Distributed consensus
phases = consensus(n_agents=9, edges=henneberg(9))

# Cycle verification
print(holonomy(tiles, mod_val=48))
```

### Rust

```rust
use constraint_substrate::{snap, funnel, is_laman};

let (point, error) = snap(0.5, 0.3);
let settled = funnel(error, 0.1, 0.001);
let rigid = is_laman(4, &edges);
```

### C

```c
#include "constraint_substrate.h"

SnapResult r = cs_snap(0.5, 0.3);
bool settled = cs_funnel(r.error, 0.1, 0.001);
bool rigid = cs_is_laman(4, edges, edge_count);
```

## API Reference

| Primitive | Python | Rust | C | Description |
|---|---|---|---|---|
| Snap | `snap(x, y)` | `snap(x, y)` | `cs_snap(x, y)` | Nearest A₂ lattice point |
| Funnel | `funnel(err, decay, tol)` | `funnel(err, decay, tol)` | `cs_funnel(err, decay, tol)` | Deadband settling check |
| Laman | `is_laman(n, edges)` | `is_laman(n, edges)` | `cs_is_laman(n, edges, count)` | Rigidity verification |
| Consensus | `consensus(n, edges)` | `consensus(n, edges)` | `cs_consensus(n, edges, count)` | Distributed agreement |
| Holonomy | `holonomy(tiles, mod)` | `holonomy(tiles, m)` | `cs_holonomy(tiles, n, m)` | Cycle consistency |

## How It Fits

The **cross-language foundation** of the constraint theory ecosystem:

- [constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core) — full theory library built on these primitives
- [conservation-conformance](https://github.com/SuperInstance/conservation-conformance) — conformance tests for all implementations
- [constraint-dialect](https://github.com/SuperInstance/constraint-dialect) — MLIR dialect using these primitives

## Testing

```bash
# Python
pytest tests/

# Rust
cargo test

# C
gcc test_substrate.c src/substrate.c -lm -o test_substrate && ./test_substrate

# Cross-language conformance
python tests/test_cross_language.py
```

## Installation

```bash
# Python
pip install constraint-substrate

# Rust
cargo add constraint-substrate

# C
cp include/constraint_substrate.h src/constraint_substrate.c /your/project
```

## License

MIT
