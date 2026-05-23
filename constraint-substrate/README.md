# constraint-substrate

**The 5 irreducible constraint primitives. Zero dependencies. Three languages.**

This is the extracted, standalone core of [constraint-theory-core](https://github.com/your-org/constraint-theory-core) — the mathematical substrate that everything else builds on.

## What It Is

Five primitives that form the irreducible core of constraint-based systems:

| Primitive | Module | What it does |
|---|---|---|
| **Lattice Snap** | `lattice` | Snap continuous values to the nearest Eisenstein A₂ lattice point |
| **Funnel** | `funnel` | Deadband convergence — pull values toward targets with shrinking tolerance |
| **Holonomy** | `holonomy` | Compute winding numbers (holonomy) of value sequences modulo N |
| **Rigidity** | `rigidity` | Check Laman's condition for structural rigidity of graphs |
| **Consensus** | `consensus` | Metronome consensus rounds — converge distributed values to agreement |

No external dependencies. No framework opinions. Just math.

## Why It Exists

These five operations show up *everywhere* in constraint systems:
- Phase alignment needs lattice snapping
- Error correction needs funnel convergence
- Gauge theory needs holonomy tracking
- Structural analysis needs rigidity checking
- Distributed agreement needs consensus

Rather than reimplementing them badly in every project, we extract them once, test them thoroughly, and ship them in whatever language you need.

## Language Matrix

| | Rust | C | Python |
|---|---|---|---|
| **Purpose** | Performance reference | Portable reference | Ergonomic reference |
| **Dependencies** | none (`no_std`) | none (C11) | none (stdlib only) |
| **Status** | ✅ Tested | ✅ Tested | ✅ Tested |

All three implementations produce **identical results** on the same test vectors.

## Quick Start

### Rust

```bash
cd rust
cargo test
```

```rust
use constraint_substrate::{lattice, funnel, holonomy, rigidity, consensus};

let (sx, sy, err) = lattice::snap(1.5, 0.3, 3);
let (val, eps) = funnel::step(0.0, 5.0, 1.0, 0.1);
let w = holonomy::winding(&[1.0, 3.0, 5.0], 10.0);
let rigid = rigidity::is_laman(3, &[(0,1), (1,2), (0,2)]);
let (vals, converged) = consensus::round(&[1.0, 2.0, 3.0], 0.5);
```

### C

```bash
cd c
make test
```

```c
#include "constraint_substrate.h"

CsSnapResult r = cs_snap(1.5, 0.3, 3);
CsFunnelResult f = cs_funnel_step(0.0, 5.0, 1.0, 0.1);
double w = cs_holonomy(values, count, 10.0);
int rigid = cs_is_laman(3, edges, 3);
CsConsensusResult c = cs_consensus(values, count, 0.5);
cs_consensus_free(c);  // remember to free!
```

### Python

```bash
cd python
pip install -e .
pytest tests/
```

```python
from constraint_substrate import (
    snap, snap_batch,
    funnel_step, funnel_batch,
    holonomy_winding,
    is_laman,
    consensus_round,
)

sx, sy, err = snap(1.5, 0.3)
val, eps = funnel_step(0.0, 5.0, 1.0, 0.1)
w = holonomy_winding([1.0, 3.0, 5.0], 10.0)
rigid = is_laman(3, [(0,1), (1,2), (0,2)])
vals, converged = consensus_round([1.0, 2.0, 3.0], 0.5)
```

## Cross-Language Test Vectors

`tests/vectors.json` contains known inputs and expected outputs for all 5 primitives. All three language implementations validate against these vectors.

To regenerate:
```bash
cd tests && python3 generate_vectors.py > vectors.json
```

## Project Structure

```
constraint-substrate/
├── rust/           # Rust reference (no_std, no deps)
│   ├── Cargo.toml
│   ├── src/lib.rs
│   └── tests/integration_tests.rs
├── c/              # C reference (C11, no deps)
│   ├── include/constraint_substrate.h
│   ├── src/{lattice,funnel,holonomy,rigidity,consensus}.c
│   ├── Makefile
│   └── tests/test_main.c
├── python/         # Python reference (stdlib only)
│   ├── pyproject.toml
│   ├── constraint_substrate/
│   │   ├── __init__.py
│   │   └── {lattice,funnel,holonomy,rigidity,consensus}.py
│   └── tests/test_all.py
├── tests/
│   └── vectors.json
└── README.md
```

## Relationship to constraint-theory-core

`constraint-substrate` is the **extract** — the minimal, zero-dependency mathematical core. `constraint-theory-core` builds higher-level abstractions (constraint graphs, propagation engines, solver infrastructure) *on top of* these primitives.

The substrate is designed to be:
- **Embedded anywhere** — no_std Rust, bare-metal C, any Python
- **Deterministic** — same inputs, same outputs, every language
- **Tested across boundaries** — shared test vectors prove cross-language correctness

## License

MIT
