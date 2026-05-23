# SANA-WM Hardware Compatibility Report

**Date:** 2026-05-17  
**Author:** Forgemaster ⚒️  
**Paper:** [arXiv:2605.15178](https://arxiv.org/abs/2605.15178)  
**Repo:** [github.com/NVlabs/Sana](https://github.com/NVlabs/Sana) (cloned to `sana-wm/`)  
**Project page:** [nvlabs.github.io/Sana/WM/](https://nvlabs.github.io/Sana/WM/)

---

## Executive Summary

**SANA-WM cannot run on our current hardware.** The model requires CUDA GPU with ≥24GB VRAM for the autoregressive variant or ≥80GB (H100) for bidirectional inference. Our WSL2 environment has no GPU passthrough, 16GB RAM, and CPU-only PyTorch. The code isn't even in the repo yet — the WM variant is listed as "coming soon" in the to-do.

**Verdict by variant:**

| Variant | Can We Run It? | Minimum Hardware |
|---------|:--------------:|-----------------|
| Bidirectional (full quality) | ❌ No | Single H100 (80GB VRAM) |
| Chunk-causal autoregressive | ❌ No | Single high-VRAM GPU (~24-48GB) |
| Distilled NVFP4 (4-bit) | ❌ No | Single RTX 5090 (32GB VRAM) |
| CPU inference (any variant) | ❌ No | Would need 32GB+ RAM, impractically slow |
| Cloud inference | ✅ Yes | Via Replicate, RunPod, Vast.ai |

---

## 1. Our Hardware Profile

| Resource | Value | Notes |
|----------|-------|-------|
| **Platform** | WSL2 on Windows (eileen) | Linux 6.6.87.2-microsoft-standard-WSL2 |
| **RAM** | 16GB total, 11GB available | 4GB swap |
| **GPU (Windows host)** | NVIDIA RTX 4050 | Laptop GPU, 6GB VRAM |
| **GPU passthrough** | ❌ None | `/dev/dxg` exists but `nvidia-smi` not found, `torch.cuda=False` |
| **CUDA toolkit** | 11.5 (WSL2) | Stale version; PyTorch 2.12.0+cpu only |
| **PyTorch** | 2.12.0+cpu | CPU-only build, no CUDA |
| **Disk** | 851GB free | Sufficient for model weights |

### WSL2 GPU Passthrough Status

WSL2 has the driver stubs at `/usr/lib/wsl/lib/` (libcuda.so exists) and `/dev/dxg` is present, but:
- `nvidia-smi` not found — no driver mapped
- `nvcc` reports CUDA 11.5 (ancient)
- PyTorch built as CPU-only (`+cpu` suffix)
- Even if passthrough worked, the RTX 4050 only has **6GB VRAM** — far below any SANA-WM requirement

**To enable WSL2 GPU passthrough would require:**
1. Update NVIDIA driver on Windows host
2. Install CUDA toolkit 12.x in WSL2
3. Reinstall PyTorch with CUDA support
4. Even then: 6GB VRAM is insufficient for any SANA-WM variant

---

## 2. SANA-WM Model Specifications

### Architecture

- **Parameters:** 2.6B
- **Backbone:** Hybrid Linear DiT (Gated DeltaNet + softmax attention)
- **Tokenizer:** LTX2 VAE (32× spatial, 8× temporal compression)
- **Output:** 720p, 60-second video with 6-DoF camera control
- **Training:** 15 days on 64× H100 GPUs, ~213K video clips
- **License:** Apache 2.0

### Three Inference Variants

1. **Bidirectional** — Highest quality, full attention over entire minute. Fits on single H100 (80GB).
2. **Chunk-causal autoregressive** — Sequential rollout, constant-memory KV cache. Fits on single GPU (est. 24-48GB VRAM).
3. **Distilled NVFP4** — Few-step distilled, 4-bit quantized. Fits on single RTX 5090 (32GB). Generates 60s 720p video in **34 seconds**.

### Memory Estimates

| Component | bf16 Size | NVFP4 Size |
|-----------|----------|-----------|
| Model weights (2.6B params) | ~5.2GB | ~1.3GB |
| LTX2 VAE | ~1-2GB | ~1-2GB |
| Text encoder | ~1-2GB | ~1-2GB |
| KV cache / activations (60s video) | **40-60GB+** | **20-30GB+** |
| **Total for 60s generation** | **~80GB** | **~32GB** |

The model *weights* are modest (5.2GB), but the **activation memory for minute-long video** is the bottleneck. The LTX2 VAE compresses 32× spatially, but 60 seconds of 720p video still generates enormous activation tensors during the denoising process.

---

## 3. Code Availability Status

⚠️ **SANA-WM code is NOT yet in the repo.**

The [NVlabs/Sana](https://github.com/NVlabs/Sana) repo (cloned to `sana-wm/`) contains:
- ✅ SANA (image generation) — full code + weights
- ✅ SANA-1.5 — full code + weights
- ✅ SANA-Sprint — full code + weights
- ✅ SANA-Video — full code + weights
- ❌ **SANA-WM — NOT in the repo**

The README to-do list shows: `[] SANA World Model` (unchecked). The paper was published May 14, 2026, and the project page exists, but the actual WM inference/training code hasn't been merged yet. The `configs/` directory has no WM-specific configs.

---

## 4. Could CPU Inference Work?

**Short answer: No, not meaningfully.**

### Why not:
- **Activation memory for 60s video** exceeds our 11GB available RAM even at 4-bit
- **CPU-only PyTorch** lacks FlashAttention, CUDA kernels, and fused operations that SANA relies on
- The hybrid GDN/softmax attention architecture uses custom CUDA kernels
- **Estimated speed:** Even if it could load, we'd be looking at **hours per frame**, not seconds. A 60-second video at 16fps = 960 frames. Even at 1 minute per frame (extremely optimistic for CPU), that's 16 hours per video.

### Aggressive quantization (int8/int4) won't help enough:
- SANA-Video's 4-bit image model needs 8GB VRAM — our *total RAM* is only 16GB
- The distilled NVFP4 variant needs an RTX 5090 (32GB VRAM) — we don't have the GPU at all
- No amount of quantization solves the activation memory problem for minute-long video

---

## 5. Cloud Inference Options

### Option A: Wait for Replicate / HuggingFace API
- SANA (image) is already on Replicate
- SANA-WM will likely appear on Replicate once code is released
- **Estimated cost:** $0.10-0.50 per 60s video (based on similar video gen pricing)

### Option B: RunPod / Vast.ai (BYO Model)
| Provider | GPU | Cost/hr | Notes |
|----------|-----|---------|-------|
| RunPod | H100 80GB | ~$3.69 | Best for bidirectional variant |
| RunPod | A100 80GB | ~$2.21 | Should work for bidirectional |
| Vast.ai | RTX 4090 24GB | ~$0.30-0.50 | May work for autoregressive variant |
| Lambda | H100 80GB | ~$3.49 | Reliable, fast |
| Google Colab | A100 40GB | ~$10.49/mo (Pro) | May not be enough VRAM |

**Cost per 60s video (estimated):**
- H100 bidirectional: ~$0.05-0.15 per video (3-15 min generation)
- RTX 5090 distilled: ~$0.02-0.05 per video (34s generation)
- **Budget for 100 videos:** $5-15

### Option C: DeepInfra
- DeepInfra has Wan models but NOT SANA-WM (too new, code not released)
- Worth monitoring once the code drops

---

## 6. Hardware Upgrade Path

### Minimum to run SANA-WM locally:

| Target | Hardware | Cost (used) | Variant |
|--------|----------|------------|---------|
| **Budget** | RTX 3090 24GB | ~$700-900 | Autoregressive only, may need model offloading |
| **Recommended** | RTX 4090 24GB | ~$1,400-1,600 | Autoregressive, borderline for distilled |
| **Ideal** | RTX 5090 32GB | ~$2,000+ | Distilled NVFP4 variant (34s generation) |
| **Overkill** | H100 80GB | $25,000+ | Bidirectional (full quality) |

**But:** We're on a laptop (RTX 4050 is mobile). Upgrading GPU means either:
1. Desktop build with RTX 4090/5090
2. External GPU enclosure (eGPU) — expensive, bandwidth-limited
3. Cloud-only approach

---

## 7. Can We Use the Architecture Ideas Without Running the Model?

**Yes — this is the most practical path.** SANA-WM's contributions are architectural, and the ideas can inform our PLATO work:

### Directly Applicable Ideas:

1. **Gated DeltaNet (GDN) for long-context** — Linear-time recurrence with constant memory state. Could inspire lightweight PLATO room attention mechanisms for long conversation histories.

2. **LTX2 VAE (32× spatial compression)** — Extreme compression maintaining quality. The compression ratio is relevant to our SplineLinear work on drift-detect.

3. **Block Causal Linear Attention** — Already in SANA-Video. The block-wise processing with constant-memory KV cache is exactly the pattern for streaming PLATO room updates.

4. **Dual-branch camera control (UCPE + Plücker)** — Multi-rate conditioning. Could inspire multi-resolution conditioning in our micro models (e.g., coarse intent + fine features).

5. **Progressive training strategy** — 4-stage training from short to minute-scale. Our PLATO training pipeline could use a similar progressive approach (short → long sequences).

6. **NVFP4 quantization** — 4-bit inference with minimal quality loss. Relevant to our NPU quantization work in plato-training.

### What We Can Do NOW:

- ✅ Read the paper and code (when released) for architecture insights
- ✅ Study the LTX2 VAE compression approach
- ✅ Implement GDN-style attention in our micro models
- ✅ Use progressive training for our video understanding models
- ✅ Run SANA-WM on cloud GPUs for specific experiments (~$0.05-0.15/video)

---

## 8. Recommended Action Plan

1. **Short-term:** Monitor the NVlabs/Sana repo for WM code release (check weekly). Paper was published May 14, code typically follows within 2-4 weeks.

2. **Medium-term:** When code drops, test on RunPod with RTX 4090 ($0.50/hr). Use the autoregressive variant with model offloading.

3. **Architecture study:** Extract the GDN attention and LTX2 compression patterns for PLATO room improvements. These ideas are independent of running the full model.

4. **Cloud budget:** Allocate ~$20-50/month for SANA-WM cloud inference experiments once code is available.

5. **Skip local GPU upgrade** unless there are other use cases. Cloud is cheaper for intermittent experiments.

---

## 9. Key Numbers Summary

| Metric | Value |
|--------|-------|
| Model parameters | 2.6B |
| Model weight memory (bf16) | ~5.2GB |
| Model weight memory (NVFP4) | ~1.3GB |
| Minimum VRAM (bidirectional) | 80GB (single H100) |
| Minimum VRAM (autoregressive) | ~24-48GB |
| Minimum VRAM (distilled NVFP4) | 32GB (single RTX 5090) |
| Generation time (H100, bidirectional) | ~3-5 min per 60s video |
| Generation time (RTX 5090, NVFP4) | 34s per 60s video |
| Training cost | 15 days × 64 × H100 |
| Our available RAM | 11GB |
| Our available VRAM | 0GB (no GPU passthrough) |
| Disk space for model | ~10-15GB |
| Cloud cost per video (est.) | $0.02-0.15 |

---

*Report generated by Forgemaster ⚒️ — SANA-WM repo cloned to `sana-wm/`, paper archived at arXiv:2605.15178*