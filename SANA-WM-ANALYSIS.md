# SANA-WM: Deep Technical Analysis

**NVIDIA's 2.6B Open-Source World Model for Minute-Scale 720p Video Generation**

*Analysis date: 2026-05-17*
*Paper: arXiv 2605.15178 (May 14, 2026)*
*Code: [github.com/NVlabs/Sana](https://github.com/NVlabs/Sana)*
*Project: [nvlabs.github.io/Sana/WM/](https://nvlabs.github.io/Sana/WM/)*

---

## 1. Executive Summary

SANA-WM is NVIDIA's open-source, 2.6B-parameter world model that generates 720p, one-minute videos with precise 6-DoF camera control. It represents a significant efficiency milestone: trained on only ~213K public video clips in 15 days on 64 H100 GPUs, it achieves visual quality comparable to industrial-scale systems like LingBot-World and HY-WorldPlay while delivering **36× higher throughput**. The distilled variant generates a 60-second 720p clip on a single RTX 5090 in just 34 seconds using NVFP4 quantization.

What makes this notable isn't the parameter count or the resolution — it's the *native* minute-scale training combined with aggressive architectural efficiency. SANA-WM doesn't distill from a short-video teacher; it trains end-to-end for 60-second generation, which gives it better scene persistence and trajectory adherence than shortcut approaches.

Licensed under Apache 2.0.

---

## 2. Architecture Deep Dive

### 2.1 Hybrid Linear Diffusion Transformer

The backbone is a DiT (Diffusion Transformer) that alternates between two attention mechanisms:

**Frame-wise Gated DeltaNet (GDN) blocks** — the workhorse. These replace the cumulative linear attention from SANA-Video with a gated recurrent state. Each GDN block processes one latent *frame* (not one token) per recurrent step:

```
S_t = S_{t-1} · M_t + U_t
M_t = γ_t(I − K̂_t · β_t · K̂_t^T)
U_t = V_t · β_t · K̂_t^T
O_t = S_t · Q̂_t
```

Where:
- `S_t ∈ ℝ^{D×D}` is the recurrent state matrix (constant size regardless of video length)
- `γ_t ∈ (0,1]` is a learned **decay gate** that forgets stale content
- `β_t ∈ [0,1]` is a per-token **update gate** (delta-rule correction)
- The correction term `(v_i − γ_i · S_{i-1} · k̂_i) · β_i · k̂_i^T` updates only the residual between target and prediction

This is the key innovation over SANA-Video's ReLU-based cumulative linear attention. The original approach had no decay mechanism — stale features accumulated with the same weight as recent ones, causing drift at minute-scale. GDN's decay gate (`γ`) and delta-rule correction solve this cleanly.

**Periodic softmax attention blocks** — interspersed among GDN blocks for exact long-range recall. The hybrid pattern: most layers use efficient GDN, with occasional softmax layers for precision retrieval. This mirrors trends in efficient LLM architectures (Jamba, etc.) that mix SSM/linear layers with sparse exact attention.

### 2.2 LTX2-VAE Tokenizer

SANA-WM replaces the baseline ST-DC-AE with **LTX2-VAE** for superior spatiotemporal compression:

- **2.0× smaller** latent representation than ST-DC-AE
- **8.0× smaller** than Wan2.1-VAE
- This compression is what makes minute-scale generation computationally feasible at all

The VAE adaptation required discarding the original patchify layer and output projection, re-initializing them from scratch to align with LTX2's different channel dimensions. Full-model fine-tuning with 50k steps adapts to the new latent distribution.

### 2.3 Dual-Branch Camera Control

This is where SANA-WM gets precise 6-DoF trajectory adherence despite aggressive video compression. Two complementary conditioning branches:

**Branch 1: Latent-rate UCPE (Unified Camera Positional Encoding)**
- Operates at the latent frame rate (compressed temporal resolution)
- Captures global trajectory structure — the coarse "where is the camera going" signal
- Based on the UCPE encoding scheme from prior work

**Branch 2: Raw-frame Plücker mixing**
- Operates at the raw (uncompressed) frame rate
- Restores fine camera motion *within* each temporal VAE stride
- Plücker coordinates represent camera rays as 6D vectors (origin + direction)
- Mixed directly into the generation process at full temporal resolution

The dual-rate design is necessary because VAE compression collapses multiple frames into single latent frames. UCPE provides trajectory guidance at the latent level, while Plücker mixing recovers the sub-stride motion detail that would otherwise be lost. Without this, camera control degrades as compression ratio increases.

### 2.4 Two-Stage Generation Pipeline

Stage 1: Base SANA-WM generator produces the minute-long video.
Stage 2: An independent **long-video refiner** operates on the full 60-second output, correcting structural artifacts and sharpening details.

The refiner is adapted to handle SANA-WM's specific output characteristics and operates as a quality-improvement pass. This separation of concerns (generation vs. refinement) is architecturally clean — the base model focuses on trajectory adherence and temporal consistency, while the refiner focuses on visual fidelity.

### 2.5 Key Stabilization: Frame-wise GDN Details

The transition from token-wise to frame-wise GDN is more nuanced than just changing the scan unit. When scanning one latent frame (containing S = H_ℓ × W_ℓ spatial tokens) per step instead of one token, the update gate β becomes a diagonal matrix β_t = diag(β_{t,1}, ..., β_{t,S}), allowing per-spatial-position selectivity in what gets written to the recurrent state.

The frame-wise state update:
```
S_t = S_{t-1} · M_t + U_t
M_t = γ_t(I − K̂_t · β_t · K̂_t^T)    // decay + selective erase
U_t = V_t · β_t · K̂_t^T              // write new content
O_t = S_t · Q̂_t                      // read from state
```

This is structurally similar to how LSTM/GRU gates work, but at the level of an entire spatial frame's D×D state matrix. The `M_t` term implements a selective erase (the K̂_t · β_t · K̂_t^T product identifies which subspaces to clear), while `U_t` writes fresh content. The decay gate γ_t provides global temporal forgetting.

For numerical stability, the paper adds key scaling and normalization to prevent gradient explosion in the recurrent state over thousands of frame steps. This is the kind of engineering detail that separates a working implementation from a theoretical contribution — training stability over 213K clips at minute scale requires careful attention to the numerical behavior of the recurrent state.

### 2.6 Chunk-Causal Deployment Design

The chunk-causal and distilled variants add two critical engineering features for practical deployment:

1. **Attention-sink tokens** — special learnable tokens prepended to each chunk that absorb attention from the actual content tokens, preventing attention degeneration at chunk boundaries. This is borrowed from streaming LLM literature.

2. **Local temporal windows** — softmax attention is restricted to a fixed-size window around the current position, so memory and compute per chunk stay constant regardless of total rollout length. The GDN recurrent state still carries information across chunks.

Together these mean the model can generate arbitrarily long rollouts (beyond 60s) with constant per-chunk resource usage. The paper only evaluates at 60s, but the architecture doesn't have a hard length limit.

### 2.7 Three Inference Variants

1. **Bidirectional generator** — highest quality, sees the full minute context. Fits on a single H100.
2. **Chunk-causal autoregressive** — sequential rollout, generates chunks in order. Uses attention-sink tokens and local temporal windows to keep softmax memory constant regardless of rollout length.
3. **Few-step distilled autoregressive** — self-forcing distillation reduces sampling to just 4 denoising steps. This is the RTX 5090 variant.

---

## 3. What Makes It Efficient

### 3.1 Linear Attention at Scale

The frame-wise GDN is the primary efficiency driver. The recurrent state `S_t ∈ ℝ^{D×D}` is:
- **Constant memory** — doesn't grow with video length (unlike softmax attention's O(n²) KV cache)
- **O(1) update per frame** — just matrix multiply and addition
- **Decay-gated** — avoids the stale-feature accumulation that killed naive linear attention at minute scale

For a 720p, 60-second video, softmax attention over the full token sequence would be prohibitively expensive. GDN handles this in constant memory per layer.

### 3.2 Latent Compression

The LTX2-VAE compression ratio directly reduces the number of tokens the transformer must process:

| Tokenizer | Relative Size |
|-----------|:------------:|
| Wan2.1-VAE | 8.0× |
| ST-DC-AE | 2.0× |
| LTX2-VAE | 1.0× (baseline) |

Fewer tokens = fewer FLOPs in every transformer layer. The 8× improvement over Wan2.1-VAE is substantial.

### 3.3 Few-Step Distillation

Self-forcing distillation compresses the denoising process from the standard 20-50 steps down to **4 steps**. Combined with NVFP4 quantization (4-bit floating point) on RTX 5090 hardware, this achieves the 34-second generation time for a full 60s clip.

The distillation uses self-forcing — the model teaches itself to denoise in fewer steps by training on its own intermediate outputs. No separate teacher model required.

### 3.4 Progressive Training

The four-stage training strategy avoids training instability:

1. **Stage 1** (50k steps): VAE adaptation on short clips
2. **Stage 2**: Architecture change to hybrid GDN/softmax, still on short clips (cheaper, easier to debug)
3. **Stage 3**: Scale to minute-length + add camera conditioning
4. **Stage 4**: Chunk-causal fine-tuning + distillation

This avoids the common failure mode of training on long sequences from scratch. Each stage builds on a stable foundation.

### 3.5 Data Annotation Pipeline

The pose annotation pipeline is worth examining in detail because it's what makes the 213K-clip budget work without proprietary data:

1. **Source**: Public video clips (internet-scale)
2. **Pose estimation**: VIPE + Pi3/Pi3X for camera pose recovery
3. **Depth estimation**: MoGe-2 for metric-scale geometry
4. **Filtering**: Quality thresholds on pose consistency, motion diversity, and scene coverage
5. **Output**: ~213K clips with metric-scale 6-DoF annotations

The key insight is that modern pose/depth estimators are good enough to produce training-quality labels from unannotated video. The annotations won't be perfect, but diffusion models are robust to moderate label noise — the volume and diversity of the data matter more than per-sample precision.

This pipeline is fully reproducible using open tools, which is significant for the field. Previous camera-controlled world models typically relied on synthetic environments (games, 3D renders) or proprietary data pipelines for action labels.

---

## 4. Training Details

| Parameter | Value |
|-----------|-------|
| Parameters | 2.6B |
| Training data | ~213K public video clips |
| Training duration | 15 days |
| Hardware | 64× NVIDIA H100 GPUs |
| Data annotation | Metric-scale 6-DoF camera poses from public videos via VIPE/Pi3/MoGe-2 |
| Output resolution | 720p |
| Output duration | 60 seconds |
| License | Apache 2.0 |

The data pipeline is worth noting. Rather than using proprietary action labels, SANA-WM builds a robust annotation pipeline that extracts metric-scale camera poses from public videos using pose and geometry estimators (VIPE, Pi3/Pi3X, MoGe-2). After filtering, this yields ~213K clips with precise annotations. This is the accessibility story — you don't need a private data moat.

### Evaluation Benchmark

The paper introduces a new one-minute world-model benchmark:
- 80 initial scenes generated by Nano Banana Pro
- Four scene types
- Each paired with two revisit trajectories
- Evaluates: action following, visual quality, efficiency

---

## 5. Hardware Requirements for Inference

### 5.1 Confirmed Configurations

| Variant | GPU | Time | Notes |
|---------|-----|------|-------|
| Bidirectional | 1× H100 (80GB) | Minutes | Highest quality, full context |
| Chunk-causal | 1× H100 (80GB) | Minutes | Sequential rollout, constant memory |
| Distilled + NVFP4 | 1× RTX 5090 | **34s** | 4-step denoising, 4-bit quantization |

### 5.2 Inferred Minimum Requirements

- **RTX 5090 (32GB)**: Confirmed for distilled variant with NVFP4. This is the consumer-grade target.
- **RTX 4090 (24GB)**: Likely feasible for distilled variant with aggressive quantization, but not confirmed in the paper.
- **H100 (80GB)**: Required for bidirectional and chunk-causal variants at full precision.
- **CPU-only**: Not supported — diffusion transformer inference at this scale requires GPU acceleration. No CPU fallback is mentioned.

The 34-second generation time on a single RTX 5090 is remarkable. For context, many competing world models require multi-GPU inference setups even for shorter clips.

### 5.3 Memory Profile

The frame-wise GDN's constant-size recurrent state (`S_t ∈ ℝ^{D×D}`) means memory doesn't scale with video length. The softmax attention layers use attention-sink tokens and local temporal windows in the chunk-causal and distilled variants, keeping their memory footprint constant as well. This is what enables single-GPU inference for minute-long videos.

---

## 6. Comparison with Other World Models

### 6.1 Direct Competitors

| Model | Params | Resolution | Duration | Control | Training | Open Source |
|-------|--------|-----------|----------|---------|----------|:-----------:|
| **SANA-WM** | 2.6B | 720p | 60s | 6-DoF camera | 213K clips, 64 H100s, 15 days | ✅ Apache 2.0 |
| **Cosmos (NVIDIA)** | ~7B+ | 720p | Variable | Multiple | Large-scale, proprietary data | ❌ |
| **GameNGen (Decart)** | Unknown | Variable | Real-time | Keyboard/gamepad | Game-specific | ❌ |
| **LingBot-World** | Unknown | 720p | 60s+ | Camera | Industrial-scale | ❌ |
| **HY-WorldPlay** | Unknown | 720p | 60s+ | Camera | Industrial-scale | ❌ |
| **Oasis (Etched)** | Unknown | Variable | Real-time | Keyboard | Minecraft-specific | Partial |
| **Genie 2 (DeepMind)** | Unknown | Variable | 10s+ | Keyboard | Large-scale | ❌ |

### 6.2 Key Differentiators

**Efficiency-first design philosophy.** The most striking comparison is training cost. SANA-WM's total training budget (213K clips × 15 days × 64 H100s) is orders of magnitude below what industrial systems use. Cosmos, for example, was trained on proprietary NVIDIA data infrastructure with presumably vastly larger compute. LingBot-World and HY-WorldPlay are both described as "large-scale industrial baselines" in the paper. SANA-WM achieves comparable quality with academic-scale resources.

**Native minute-scale training.** Many competing approaches start with short-video generators (5-10s) and attempt to extend them to longer durations via autoregressive rollout or sliding windows. SANA-WM trains natively on 60-second sequences from Stage 3 onward. This gives it better scene persistence — objects and structures don't drift or hallucinate over the minute because the model has actually seen minute-scale sequences during training.

**Open-source accessibility.** Apache 2.0 license, public code, public weights. This is rare in the world model space where most competitive systems are either closed-source (Genie 2, Cosmos) or have restrictive licenses.

**vs. Cosmos**: Cosmos is NVIDIA's larger-scale world model with broader ambitions. SANA-WM is more focused — specifically camera-controlled, minute-scale generation — and dramatically more efficient. SANA-WM achieves comparable visual quality at 36× higher throughput.

**vs. GameNGen/Oasis**: These target real-time interactive gameplay with keyboard/gamepad control. SANA-WM targets offline video generation with precise camera trajectories — different use case entirely. SANA-WM produces much higher quality output but isn't real-time interactive.

**vs. LingBot-World / HY-WorldPlay**: These are industrial baselines with presumably much larger training budgets and proprietary data. SANA-WM matches their visual quality with 213K clips and 15 days of training. That's the efficiency story in one comparison.

**vs. Genie 2**: Genie 2 generates shorter clips (10s range) with keyboard control. SANA-WM's minute-scale native training and 6-DoF camera control is a different capability class.

### 6.3 Efficiency Comparison

SANA-WM's 36× throughput advantage over open-source baselines comes from:
1. LTX2-VAE's 8× compression advantage over Wan2.1-VAE
2. Frame-wise GDN's constant-memory recurrence vs. growing KV caches
3. 4-step distilled inference vs. standard 20-50 step sampling
4. NVFP4 quantization reducing memory bandwidth requirements

---

## 7. Limitations and Open Questions

### 7.1 Known Limitations

1. **Camera control only** — SANA-WM controls camera motion but not object dynamics, physics, or agent actions. It's a visual navigation simulator, not a full interactive world model.

2. **720p resolution ceiling** — The paper targets 720p exclusively. No results at 1080p or higher. The LTX2-VAE compression that enables efficiency may also limit resolution scaling.

3. **Single-scene generation** — No evidence of multi-scene transitions or scene composition. Each generation is a single continuous camera path through one environment.

4. **Refiner dependency** — The two-stage pipeline means the base model's output quality isn't sufficient alone. The refiner is required for acceptable visual quality, adding inference overhead.

5. **Evaluated on synthetic benchmark** — The evaluation benchmark uses scenes generated by Nano Banana Pro, not real-world footage. Generalization to real camera trajectories is an open question.

6. **Pose estimation quality ceiling** — Training data quality depends on the pose estimation pipeline (VIPE, Pi3, MoGe-2). Errors in pose estimation propagate directly into training signal quality.

### 7.2 Open Questions

1. **Can it handle dynamic scenes?** The paper emphasizes camera control through static/near-static environments. How well does it handle scenes with significant object motion, people, or physics interactions?

2. **What's the maximum rollout length?** The GDN's constant-memory recurrence theoretically supports arbitrary lengths, but quality degradation over very long rollouts (>2 minutes) isn't tested.

3. **Fine-tuning for specific domains?** Can the model be fine-tuned for specific environments (indoor navigation, driving simulation, game environments)? The Apache 2.0 license enables this, but no fine-tuning results are published.

4. **Interaction beyond camera?** The architecture could potentially be extended to other control modalities (robot actions, keyboard input), but this isn't demonstrated.

5. **Real-time generation?** The 34-second generation time for a 60-second clip means ~1.76× real-time. With further optimization, real-time or near-real-time generation might be possible, but the chunk-causal variant's sequential nature is a bottleneck.

6. **Scaling behavior** — Would a 7B or 15B variant trained on the same pipeline show linear quality improvements, or does the architecture have diminishing returns?

---

## 8. Architecture Significance

SANA-WM represents an important proof point: **world models don't require industrial-scale resources**. The combination of:

1. High-compression latent spaces (LTX2-VAE)
2. Efficient recurrent attention (frame-wise GDN)
3. Hybrid exact-approximate attention patterns
4. Progressive training from short to long sequences
5. Two-stage generation with dedicated refinement

...creates a recipe that could be replicated by academic labs or smaller companies. The 213K clip training budget and 15-day, 64-GPU schedule is accessible to many research groups.

The frame-wise GDN innovation is the most transferable contribution. Applying delta-rule recurrent mechanisms at the *frame* level rather than the token level is a natural fit for video generation that other architectures could adopt. The delta rule's correction term `(v − S_{t-1}·k̂) · β · k̂^T` is essentially a "learn to correct your own predictions" mechanism — the state doesn't just accumulate features, it actively corrects its representation based on prediction error. This is a more principled approach than simple gating.

The dual-branch camera control design is also worth highlighting as a general pattern. Any time you have aggressive temporal compression but need high-frequency control signals, the dual-rate approach (coarse signal at latent rate + fine signal at raw rate) is applicable beyond just camera control.

### 8.1 Reproducibility Assessment

SANA-WM scores high on reproducibility:
- ✅ Open-source code (Apache 2.0)
- ✅ Open weights (HuggingFace)
- ✅ Training data from public sources with described pipeline
- ✅ Progressive training strategy fully documented
- ⚠️ Training compute (64 H100s for 15 days) is expensive but not unreasonable
- ⚠️ Pose annotation pipeline requires specific estimator models (VIPE, Pi3, MoGe-2) that must be sourced separately
- ❌ No training code released yet (only inference as of May 2026)

The main gap is training code — the repo currently provides inference only, with training recipes presumably coming later based on the SANA ecosystem's pattern of progressive releases.

SANA-WM represents an important proof point: **world models don't require industrial-scale resources**. The combination of:

1. High-compression latent spaces (LTX2-VAE)
2. Efficient recurrent attention (frame-wise GDN)
3. Hybrid exact-approximate attention patterns
4. Progressive training from short to long sequences
5. Two-stage generation with dedicated refinement

...creates a recipe that could be replicated by academic labs or smaller companies. The 213K clip training budget and 15-day, 64-GPU schedule is accessible to many research groups.

The frame-wise GDN innovation is the most transferable contribution. Applying delta-rule recurrent mechanisms at the *frame* level rather than the token level is a natural fit for video generation that other architectures could adopt.

---

## 9. Links

| Resource | URL |
|----------|-----|
| Paper | [arxiv.org/abs/2605.15178](https://arxiv.org/abs/2605.15178) |
| HTML Paper | [arxiv.org/html/2605.15178v1](https://arxiv.org/html/2605.15178v1) |
| Code | [github.com/NVlabs/Sana](https://github.com/NVlabs/Sana) |
| Project Page | [nvlabs.github.io/Sana/WM/](https://nvlabs.github.io/Sana/WM/) |
| Weights | HuggingFace (via Sana model zoo) |
| License | Apache 2.0 |
| SANA Ecosystem | [nvlabs.github.io/Sana/docs/](https://nvlabs.github.io/Sana/docs/) |

---

## 10. Potential Applications

Given the capabilities and limitations:

1. **Embodied AI simulation** — Generate training environments for navigation agents by sweeping camera trajectories through synthetic scenes. Cheaper than building 3D environments.

2. **Film/creative pre-visualization** — Camera path planning through virtual sets. Generate a rough preview of what a camera move will look like before committing to full rendering.

3. **Real estate / architectural visualization** — Virtual walkthroughs from a single image. The 6-DoF camera control maps naturally to spatial navigation.

4. **Data augmentation** — Generate diverse camera trajectories through scenes for training downstream models (SLAM, depth estimation, novel view synthesis).

5. **Game prototyping** — Rapidly visualize how camera systems would work in a game environment before building the actual game world.

Applications that are *not* well-served: interactive real-time simulation (too slow), physics-based scenarios (no physics modeling), multi-agent environments (single-camera perspective only).

---

## 11. Bottom Line

SANA-WM is the most efficient open-source world model for minute-scale video generation as of May 2026. Its architecture choices — frame-wise GDN, LTX2 compression, dual-branch camera control, progressive training — form a coherent efficiency story that's actually reproducible. The 34-second, single-RTX-5090 generation is a practical headline number that matters for deployment.

The main limitation is scope: it's a camera navigation model, not a general world simulator. But within that scope, it's an impressively tight design. The Apache 2.0 license makes it a genuine baseline for the field — expect to see this architecture pattern (frame-wise gated recurrence + sparse softmax + high-compression latents) replicated and extended throughout 2026.

**Key numbers to remember:**
- 2.6B parameters, 213K training clips, 15 days on 64 H100s
- 720p × 60 seconds, 6-DoF camera control
- 34 seconds on single RTX 5090 (distilled, NVFP4)
- 36× throughput advantage over open-source baselines
- Comparable visual quality to LingBot-World and HY-WorldPlay
- Apache 2.0 license
