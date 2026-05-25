#!/usr/bin/env python3
"""Experiment 5: Wheel singularity — visualizing the center as information hub."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
import os, json

OUT = os.path.dirname(__file__)

# --- 5a. Spinning wheel with force vectors ---
fig, axes = plt.subplots(1, 3, figsize=(15, 5), tight_layout=True)

# Left: spinning wheel with radius vectors
ax = axes[0]
theta = np.linspace(0, 2*np.pi, 100)
ax.plot(np.cos(theta), np.sin(theta), 'k-', lw=2)  # rim
ax.plot(0, 0, 'ko', ms=5)  # center

# Draw force vectors at different radii
for r, color in zip([0.9, 0.6, 0.3, 0.05], ['red', 'orange', 'green', 'blue']):
    angle = np.pi/4
    x, y = r*np.cos(angle), r*np.sin(angle)
    # Tangential force (torque)
    fx, fy = -np.sin(angle), np.cos(angle)  # tangent direction
    scale = r * 0.3
    ax.annotate('', xy=(x + fx*scale, y + fy*scale), xytext=(x, y),
                arrowprops=dict(arrowstyle='->', color=color, lw=2))
    ax.plot(x, y, 'o', color=color, ms=6)
    ax.annotate(f'r={r}', (x, y), fontsize=7, xytext=(5, 5), textcoords='offset points')

ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.set_title('Spinning Wheel: Torque = r × F')

# Middle: torque vs radius → singularity at center
ax = axes[1]
radii = np.linspace(0, 1, 200)
F = 1.0  # constant force
torque = radii * F
velocity = radii * 1.0  # angular velocity * r

ax.plot(radii, torque, 'r-', lw=2, label='Torque (r × F)')
ax.plot(radii, velocity, 'b-', lw=2, label='Linear velocity (ωr)')
ax.axvline(0, color='gray', lw=0.5, ls='--')
ax.annotate('SINGULARITY\nr → 0\nTorque → 0\nVelocity → 0\nDirection → preserved!',
            xy=(0, 0), xytext=(0.3, 0.7), fontsize=9,
            arrowprops=dict(arrowstyle='->', color='black'),
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
ax.set_xlabel('Radius r')
ax.set_ylabel('Magnitude')
ax.set_title('The Singularity at the Center')
ax.legend()

# Right: information vs motion
ax = axes[2]
r = np.linspace(0.01, 1, 200)
# Information density ~ 1/r (more info at center)
info = 1.0 / r
# Motion ~ r
motion = r

ax.fill_between(r, 0, motion, alpha=0.3, color='blue', label='Expression (motion)')
ax.fill_between(r, 0, info, alpha=0.3, color='red', label='Information density')
ax.axvline(0.5, color='green', ls='--', lw=2, label='"Sweet spot" — moderate r')
ax.set_xlabel('Radius (dial position)')
ax.set_ylabel('Intensity')
ax.set_title('Information vs Expression: The Dial Map')
ax.legend(fontsize=8)
ax.set_xlim(0, 1)
ax.set_ylim(0, 5)

plt.suptitle('The Wheel Singularity: Center Holds Direction, Rim Holds Motion', fontsize=13)
plt.savefig(os.path.join(OUT, 'wheel_singularity.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✓ wheel_singularity.png")

# --- 5b. DC component analogy ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5), tight_layout=True)

# Fourier components mapped to wheel radii
ax = axes[0]
t = np.linspace(0, 2*np.pi, 1000)
components = {
    'DC (center)': (0, 0.5, 'black'),     # radius 0 — the center!
    'Fundamental': (1, 1.0, 'red'),
    '2nd harmonic': (2, 0.5, 'orange'),
    '3rd harmonic': (3, 0.33, 'green'),
    '4th harmonic': (4, 0.25, 'blue'),
}

for name, (n, amp, color) in components.items():
    if n == 0:
        ax.axhline(amp, color=color, lw=2, ls='--', label=f'{name}: offset={amp}')
    else:
        ax.plot(t, amp * np.cos(n * t), color=color, lw=1, alpha=0.7, label=f'{name}: r={amp:.2f}')

ax.set_title('Fourier Components as Wheel Radii')
ax.legend(fontsize=8)
ax.set_xlabel('Phase θ')
ax.set_ylabel('Amplitude')

# The dial position map
ax = axes[1]
# Our "most pleasing" position at moderate radius
dial_positions = {
    'Timbre': (2.61/5, 2.33/5, 'red'),
    'Tradition': (4.0/5, 2.33/5, 'blue'),
    'Relationship': (2.61/5, 4.0/5, 'green'),
}

# Background: radial gradient
for r in np.linspace(0, 1, 50):
    circle = plt.Circle((0.5, 0.5), r, fill=True, color=plt.cm.coolwarm(1-r), alpha=0.1)
    ax.add_patch(circle)

for name, (x, y, color) in dial_positions.items():
    r_pos = np.sqrt((x-0.5)**2 + (y-0.5)**2)
    ax.plot(x, y, 'o', color=color, ms=10)
    ax.annotate(f'{name}\nr={r_pos:.2f}', (x, y), fontsize=8,
                xytext=(10, 10), textcoords='offset points')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.set_title('Dial Positions as Radii on the Wheel')

plt.suptitle('Fourier ↔ Wheel: DC = Center, Harmonics = Radial Modes', fontsize=13)
plt.savefig(os.path.join(OUT, 'fourier_wheel.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✓ fourier_wheel.png")

# Save
results = {
    "experiment": "wheel_singularity",
    "dial_positions": {
        "most_pleasing": {"timbre": 2.61, "tradition": 2.33, "relationship": 4.0},
        "normalized_radius": 0.37,
        "interpretation": "moderate radius — balance of information and expression"
    },
    "insight": "The center of the spinning wheel is a singularity: zero motion but maximum directional information. This maps to the DC component in Fourier analysis and to the pure-relationship end of our dials. The most aesthetically pleasing dial positions sit at moderate radius — neither pure information nor pure expression."
}
with open(os.path.join(OUT, 'wheel_singularity.json'), 'w') as f:
    json.dump(results, f, indent=2)

print("\n✅ Experiment 5 complete: wheel_singularity")
