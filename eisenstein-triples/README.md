# eisenstein-triples

Eisenstein integer triples (a² − ab + b² = c²) — the hexagonal analog of Pythagorean triples, with Weyl orbit analysis and statistical comparison to Z².

## What This Gives You

- **Triple generation** — all Eisenstein triples (a, b, c) with c ≤ N using parametric formulas
- **Weyl orbits** — complete D₆ orbits under the symmetries of Z[ω]
- **Statistical analysis** — density, distribution, and comparison with Pythagorean triples
- **Proof verification** — automated checking of norm identities and orbit closure

## Quick Start

```python
from eisenstein_triples import generate_triples, is_eisenstein_triple, weyl_orbit

# Generate all triples with c ≤ 50
triples = generate_triples(50)
print(f"Found {len(triples)} triples")

# Check a specific triple
print(is_eisenstein_triple(3, 5, 7))  # True: 9-15+25 = 19... let the code tell you

# Full D₆ Weyl orbit
orbit = weyl_orbit(3, 5)
print(f"Orbit size: {len(orbit)}")
```

## API Reference

| Function | Description |
|---|---|
| `norm(a, b)` | Eisenstein norm: a² − ab + b² |
| `is_eisenstein_triple(a, b, c)` | Check if a² − ab + b² = c² |
| `is_primitive(a, b)` | Check gcd condition in Z[ω] |
| `weyl_orbit(a, b)` | All 12 D₆ symmetry images |
| `generate_triples(max_c)` | All triples with c ≤ max_c |

## How It Fits

Foundational number theory for:

- [eisenstein-vs-z2-rs](https://github.com/SuperInstance/eisenstein-vs-z2-rs) — Rust benchmark of hexagonal vs square lattice
- [eisenstein-embed](https://github.com/SuperInstance/eisenstein-embed) — Eisenstein integer embeddings for NLP/search
- [constraint-theory-core](https://github.com/SuperInstance/constraint-theory-core) — A₂ lattice operations

## License

MIT
