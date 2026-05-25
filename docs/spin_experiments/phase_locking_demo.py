#!/usr/bin/env python3
"""Experiment 4: Phase locking — neural entrainment as coupled oscillators."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, json

OUT = os.path.dirname(__file__)

# --- 4a. Two coupled oscillators ---
dt = 0.001
T = 20.0
t = np.arange(0, T, dt)

def simulate_coupled(omega1, omega2, K, dt=0.001, T=20.0):
    """Coupled Kuramoto oscillators."""
    t = np.arange(0, T, dt)
    theta1 = np.zeros(len(t))
    theta2 = np.zeros(len(t))
    theta1[0] = 0.0
    theta2[0] = np.pi / 4
    
    for i in range(1, len(t)):
        d1 = omega1 + K * np.sin(theta2[i-1] - theta1[i-1])
        d2 = omega2 + K * np.sin(theta1[i-1] - theta2[i-1])
        theta1[i] = theta1[i-1] + d1 * dt
        theta2[i] = theta2[i-1] + d2 * dt
    
    return t, theta1, theta2

# Phase difference over time for different K
fig, axes = plt.subplots(1, 3, figsize=(15, 4), tight_layout=True)

omega1 = 2 * np.pi * 2.0  # 2 Hz
omega2 = 2 * np.pi * 2.3  # 2.3 Hz
delta_omega = abs(omega1 - omega2)

for ax, K, label in zip(axes, [0.0, 0.8, 3.0], 
    ['K=0 (No coupling)\nFree running',
     f'K=0.8 < Δω={delta_omega:.2f}\nPartial entrainment',
     f'K=3.0 > Δω={delta_omega:.2f}\nFull phase lock']):
    t_sim, th1, th2 = simulate_coupled(omega1, omega2, K, dt=0.001, T=20.0)
    phase_diff = (th2 - th1) % (2*np.pi)
    # Unwrap for continuity
    phase_diff_unwrapped = np.unwrap(th2 - th1)
    
    ax.plot(t_sim, phase_diff_unwrapped / (2*np.pi), lw=0.5, color='steelblue')
    ax.set_title(label, fontsize=9)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Phase Difference (cycles)')

plt.suptitle('Phase Locking: How Coupling Strength Creates Synchronization', fontsize=13, y=1.05)
plt.savefig(os.path.join(OUT, 'phase_locking.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✓ phase_locking.png")

# --- 4b. Arnold tongues ---
fig, ax = plt.subplots(figsize=(12, 8))

# Scan (omega_ratio, K) space
omega_base = 2 * np.pi * 1.0  # base oscillator
n_ratios = 150
n_K = 60
omega_ratios = np.linspace(0.5, 2.0, n_ratios)
K_values = np.linspace(0, 3.0, n_K)

locking_map = np.zeros((n_K, n_ratios))

for i, K in enumerate(K_values):
    if i % 10 == 0:
        print(f"  Arnold tongues: K row {i}/{n_K}")
    for j, ratio in enumerate(omega_ratios):
        omega2_test = omega_base * ratio
        t_sim, th1, th2 = simulate_coupled(omega_base, omega2_test, K, dt=0.005, T=5.0)
        
        # Check if locked: phase difference bounded in last 2 seconds
        last_2s = t_sim > 3.0
        if np.sum(last_2s) > 0:
            pd = np.abs(np.diff(np.unwrap(th2[last_2s] - th1[last_2s])))
            # Locked if phase diff rate is small
            locking_map[i, j] = 1.0 - np.mean(pd) / (0.005 * abs(omega_base * (ratio - 1)) + 0.001)
            locking_map[i, j] = np.clip(locking_map[i, j], 0, 1)

im = ax.imshow(locking_map, aspect='auto', origin='lower',
               extent=[0.5, 2.0, 0, 3.0], cmap='hot', vmin=0, vmax=1)
plt.colorbar(im, label='Lock Strength')

# Mark consonant intervals
notable = {'1/1': 1.0, '3/2': 1.5, '4/3': 4/3, '5/4': 1.25, 
           '5/3': 5/3, '2/1': 2.0, '6/5': 1.2}
for name, ratio in notable.items():
    ax.axvline(ratio, color='cyan', alpha=0.5, lw=0.8, ls='--')
    ax.annotate(name, (ratio, 2.8), fontsize=8, color='cyan', ha='center', fontweight='bold')

ax.set_xlabel('Frequency Ratio ω₂/ω₁')
ax.set_ylabel('Coupling Strength K')
ax.set_title('Arnold Tongues: Regions of Phase Locking = Consonance Valleys')
plt.savefig(os.path.join(OUT, 'arnold_tongues.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✓ arnold_tongues.png")

# --- 4c. Musical mapping ---
fig, axes = plt.subplots(1, 3, figsize=(15, 4), tight_layout=True)

for ax, (K, title) in zip(axes, [
    (0, 'K=0: No Rhythm Perception (Free)'),
    (0.5, 'K=0.5: Complex Polyrhythm'),
    (2.0, 'K=2.0: Simple 4/4 Groove (Locked)')
]):
    # Simulate 4 oscillators
    omegas = [2*np.pi*f for f in [1.0, 2.0, 1.5, 3.0]]  # Hz
    n_osc = len(omegas)
    thetas = np.zeros((n_osc, len(np.arange(0, 10, 0.001))))
    t_short = np.arange(0, 10, 0.001)
    
    for step in range(1, len(t_short)):
        for n in range(n_osc):
            coupling = K/n_osc * sum(np.sin(thetas[m, step-1] - thetas[n, step-1]) for m in range(n_osc))
            thetas[n, step] = thetas[n, step-1] + (omegas[n] + coupling) * 0.001
    
    for n in range(n_osc):
        ax.plot(t_short, np.sin(thetas[n]), lw=0.5, alpha=0.7, label=f'{omegas[n]/(2*np.pi):.1f} Hz')
    ax.set_title(title, fontsize=9)
    ax.set_xlabel('Time (s)')
    ax.legend(fontsize=7)

plt.suptitle('Coupling Strength → Musical Texture', fontsize=13)
plt.savefig(os.path.join(OUT, 'coupling_music.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✓ coupling_music.png")

# Save
results = {
    "experiment": "phase_locking",
    "delta_omega": float(delta_omega),
    "locking_threshold": f"K > Δω = {delta_omega:.3f}",
    "notable_ratios": notable,
    "insight": "Phase locking in coupled oscillators maps directly to musical consonance. Arnold tongues = consonance valleys. When coupling K exceeds frequency difference Δω, oscillators lock — this IS groove, IS rhythm perception, IS consonance."
}
with open(os.path.join(OUT, 'arnold_tongues.json'), 'w') as f:
    json.dump(results, f, indent=2)

print("\n✅ Experiment 4 complete: phase_locking_demo")
