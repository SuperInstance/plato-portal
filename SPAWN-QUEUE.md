# SPAWN QUEUE — Priority order
# Updated: 2026-06-03 23:15 AKDT

## P0 — Spawn immediately when slot opens
1. kimi-ecosynthesis (GLM-5.1 262K) — Read GPU paradigms + architecture + topology, produce GRAND-INTEGRATION.md with thesis, contradictions, experiment sequence
2. claude-hardest — Claude Sonnet for the toughest integration challenge: make all layers (C/CUDA/Rust/WASM/Python) pass the same test vectors using the cross-language schema

## P1 — After P0
3. lever-runner-integration-test — End-to-end test: teach command → search → export → import → verify round-trip
4. pincherOS-nail-bridge — Test .nail export from lever-runner → import into pincherOS, verify compatibility
5. GPU factory experiment — Run 24 parallel game variants on GPU, compile policies, benchmark the full factory loop

## P2 — After P1  
6. Browser demo integration — Wire WASM carapace + Pyodide demo into lever-runner/browser/
7. OpenCL on real hardware — If OpenCL runtime available, benchmark tile-opencl kernels
8. ARM cross-compile — Build compiled-policy-c and tile-neon for aarch64, verify on QEMU
