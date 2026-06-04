# QUEUED AGENTS — Waiting for slot availability
# Generated: 2026-06-03 22:30 AKDT
# Updated: 2026-06-03 22:35 AKDT

## Queue (spawn when slots open)

### 1. hermes-gpu-paradigms
- Model: hermes-3-llama-3.1-405b
- Task: High-level ideation on novel GPU/Ryzen paradigms
- Output: ~/repos/superinstance-ecosystem/research/GPU-PARADIGMS.md
- Focus: warp-level strategy, tensor core compression, async pipeline, CUDA graphs, shared memory tile fields

### 2. seedpro-architecture  
- Model: seed-2.0-mini
- Task: GPU-native tile field architecture design
- Output: ~/repos/superinstance-ecosystem/research/GPU-ARCHITECTURE.md
- Focus: memory layout, kernel pipeline, CPU-GPU sync, scalability, bottleneck analysis

### 3. deepseek-schemas
- Model: deepseek/deepseek-chat
- Task: Cross-language schemas and interfaces
- Output: ~/repos/superinstance-ecosystem/research/CROSS-LANGUAGE-SCHEMAS.md
- Focus: wire format, IPC protocol, WASM API, CUDA kernel interface, cross-platform test vectors, OpenCL backend

### 4. nemotron-systems
- Model: nvidia/nemotron-3-super-120b-a12b
- Task: Deployment topology across hardware
- Output: ~/repos/superinstance-ecosystem/research/DEPLOYMENT-TOPOLOGY.md
- Focus: per-platform strategy, three-gate tuning, tile sync, skill pack format, fallback chains

### 5. loom-arm-experiments
- Model: hermes-3-llama-3.1-405b
- Task: Design experiments Loom can run on Oracle ARM64 (4-core, 24GB RAM, NEON SIMD)
- Output: ~/repos/superinstance-ecosystem/research/LOOM-ARM-EXPERIMENTS.md
- Focus: NEON vs CUDA comparison, ARM-optimized tile fields, edge deployment validation, OpenCL on Mali, power efficiency benchmarks

### 6. opencl-backend-design
- Model: seed-2.0-mini
- Task: Design OpenCL backend for tile field operations (portable GPU compute)
- Output: ~/repos/superinstance-ecosystem/research/OPENCL-BACKEND.md
- Focus: OpenCL kernel design for tile ops, ARM Mali GPU support, CPU fallback via OpenCL, cross-vendor portability (NVIDIA/AMD/ARM/Intel)

### 7. kimicode-integration (after schemas land)
- Model: kimi via tmux
- Task: Low-level integration across C/CUDA/Rust/WASM/Python/OpenCL
- Focus: Make all layers talk to each other using the deepseek schemas
