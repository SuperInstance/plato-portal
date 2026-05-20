# SuperInstance

Micro-model ecosystem: distill LLM knowledge into deployable micro-models.

## Packages

| Package | PyPI | npm | crates.io | Description |
|---------|------|-----|-----------|-------------|
| **plato-core** | `pip install plato-core` | `@superinstance/plato-core` | — | Base types + mesh registry |
| **tensor-spline** | `pip install tensor-spline` | `@superinstance/tensor-spline` | — | SplineLinear layers, 5-20x compression |
| **eisenstein-embed** | `pip install eisenstein-embed` | `@superinstance/eisenstein-embed` | — | 5-layer matching cascade |
| **plato-training** | `pip install plato-training` | — | — | Training framework (monolith) |
| **plato-deadband** | — | — | `plato-deadband` | Deadband caching (Rust) |
| **constraint-theory-core** | — | — | `constraint-theory-core` | Constraint solving (Rust) |
| **spectral-conservation** | — | — | `spectral-conservation` | Spectral analysis (Rust) |

## Architecture

Each package is standalone — install only what you need. When co-installed, packages auto-discover and mesh via entry_points.

See [MESH-ARCHITECTURE.md](./MESH-ARCHITECTURE.md) for the full specification.

## Key Results

- **Eisenstein encoder**: 71.2% hit rate, 653x smaller than Model2Vec
- **SplineLinear**: 16,384:1 compression ratio on 512×512 layers
- **Bitvector matching**: 93.8% typo accuracy, zero ML dependencies
- **ONNX inference**: 58,648 qps on CPU (700x faster than PyTorch)
- **Heterogeneous compute**: CUDA (training) + CPU/ONNX (inference) + iGPU (overflow) + NPU (pending)
