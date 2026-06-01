#!/bin/bash
# Publish remaining lau-* crates to crates.io
# Run after rate limit resets
# Rate limit: ~5 new crates per period, then cooldown

CRATES=(
  lau-galois-agents
  lau-sheaf-neural
  lau-quantum-topology-agents
  lau-morse-homology-agents
  lau-mean-field-agents
  lau-agent-topology
  lau-mirror-control
  lau-ricci-curvature-agents
  lau-stochastic-homotopy
  lau-categorical-mechanics
  lau-persistence-experiment
  lau-agent-organism
  lau-closure
  lau-glue
  lau-resolvent-leverage
  lau-self-aware-agent
  lau-conservation-experiment
  lau-spectral-zeta
  lau-eigenfunction-policy
  lau-calm-noether
  lau-landauer-meter
  lau-leverage-singularity
  lau-hardware-abstract
  lau-noether-agents
  lau-observation-control
  lau-self-modeling
  lau-sheaf-automata
  lau-spectral-agent
  lau-kalman-hodge
  lau-thermal-rl
  lau-dirichlet-space
  lau-ergodic-gradient
  lau-trace-monoid
  lau-conservation-laws
  lau-gradient-ricci
  lau-constitutive-compute
  lau-penrose-growth
  lau-geometric-growth
  lau-naturality-boundary
  lau-spectral-gap-experiment
  lau-witten-reward
  lau-connes-spectral-triple
  lau-calm-crdt
  lau-reward-hacking-detector
  lau-teleomorphic
  lau-sheaf-learning
  lau-symplectic-agent
  lau-tropical-agent
  lau-index-theorem
  lau-automata-theory
  lau-concurrent-systems
  lau-linear-systems
  lau-conservation-spectral
  lau-functional-programming
  lau-cudaclaw-bridge
  lau-reinforcement-learning-advanced
  lau-homotopy-type
  lau-symplectic-geometry
  lau-agent-lifecycle
  lau-gpu-compute
  lau-ffi-bindings
  lau-hardware-simd
  lau-cuda-kernels
)

for crate in "${CRATES[@]}"; do
  cd /tmp/$crate 2>/dev/null || continue
  [ -f Cargo.toml ] || continue
  
  # Ensure required fields
  grep -q '^description = ' Cargo.toml || sed -i "/^\[package\]/a description = \"$crate - Lau ecosystem\"" Cargo.toml
  grep -q '^repository = ' Cargo.toml || sed -i "/^\[package\]/a repository = \"https://github.com/SuperInstance/$crate\"" Cargo.toml
  grep -q '^license = ' Cargo.toml || sed -i "/^\[package\]/a license = \"MIT\"" Cargo.toml
  
  echo "Publishing $crate..."
  cargo publish --allow-dirty 2>&1 | tail -2
  echo "---"
  sleep 5
done
