# Queued GPU Tasks (waiting for subagent slots)

## Priority 1: PTX Native Kernels
- Direct PTX assembly for conservation operations
- Warp-level reductions, bank conflict avoidance
- Cycle-level GPU control
- Repo: conservation-spectral-ptx

## Priority 2: GPU Benchmark Framework  
- Compare CPU vs CUDA vs PTX vs Thrust vs cuBLAS
- Auto-detect GPU capabilities
- Generate performance plots
- Repo: conservation-gpu-bench

## Priority 3: OpenCL (cross-vendor GPU)
- Runs on NVIDIA, AMD, Intel, Apple Silicon, mobile
- The universal GPU compute standard
- Repo: conservation-spectral-opencl

## Priority 4: WebGPU Compute (browser)
- Runs in ANY browser on ANY device
- Single HTML file, zero install
- Most accessible version possible
- Repo: conservation-spectral-webgpu

## Priority 5: Vulkan Compute
- Lowest-level cross-platform GPU API
- SPIR-V shaders, minimal overhead
- Repo: conservation-spectral-vulkan

## After GPU wave: Modern Hyper-Optimized
- Take best insights from FORTRAN IV (cache), Forth (composition), APL (vectorization), ASM (registers), Ada (safety)
- Forge new Rust/Zig/Mojo versions incorporating ALL lessons
- Target: 10x faster than current implementations
