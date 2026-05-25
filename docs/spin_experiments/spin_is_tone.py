#!/usr/bin/env python3
"""Experiment 1: Prove that a spin IS a tone."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, json

OUT = os.path.join(os.path.dirname(__file__), 'spin_portraits')
os.makedirs(OUT, exist_ok=True)

# --- Parameters ---
SR = 44100
DUR = 0.01  # 10ms window for display
t = np.linspace(0, DUR, int(SR*DUR), endpoint=False)

# --- 1a. Pure tone as complex exponential ---
freq = 440.0
z = np.exp(1j * 2 * np.pi * freq * t)

fig, axes = plt.subplots(3, 1, figsize=(12, 10), tight_layout=True)
axes[0].plot(t*1000, z.real, label='Real (what we hear)', color='steelblue')
axes[0].set_title('440 Hz Tone — Real Part (Audible Component)')
axes[0].set_xlabel('Time (ms)')
axes[0].set_ylabel('Amplitude')
axes[0].legend()

axes[1].plot(t*1000, z.imag, label='Imaginary (hidden spin)', color='coral')
axes[1].set_title('440 Hz Tone — Imaginary Part (Spin Component)')
axes[1].set_xlabel('Time (ms)')
axes[1].set_ylabel('Amplitude')
axes[1].legend()

# Complex plane: show several snapshots
n_cycles = 3
t_short = np.linspace(0, n_cycles/freq, 500)
z_short = np.exp(1j * 2 * np.pi * freq * t_short)
axes[2].plot(z_short.real, z_short.imag, color='purple', lw=2)
axes[2].set_title('Complex Plane: The Spin (Perfect Circle)')
axes[2].set_xlabel('Real')
axes[2].set_ylabel('Imaginary')
axes[2].set_aspect('equal')
axes[2].axhline(0, color='gray', lw=0.5)
axes[2].axvline(0, color='gray', lw=0.5)

plt.savefig(os.path.join(OUT, '01_pure_tone_spin.png'), dpi=150)
plt.close()
print("✓ 01_pure_tone_spin.png")

# --- 1b. Harmonics = faster spins ---
fig, axes = plt.subplots(2, 2, figsize=(12, 10), tight_layout=True)
t_short = np.linspace(0, 3/freq, 1000)

for i, (n, ax) in enumerate(zip([1, 2, 3, 4], axes.flat)):
    z_h = np.exp(1j * 2 * np.pi * freq * n * t_short)
    ax.plot(z_h.real, z_h.imag, lw=1.5)
    ax.set_title(f'Harmonic {n}: {freq*n} Hz ({n}× spin speed)')
    ax.set_aspect('equal')
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)

plt.suptitle('Harmonics = Faster Spins (Same Circle, n× Speed)', fontsize=14)
plt.savefig(os.path.join(OUT, '02_harmonics_as_spins.png'), dpi=150)
plt.close()
print("✓ 02_harmonics_as_spins.png")

# --- 1c. Adding harmonics together ---
t_long = np.linspace(0, 4/freq, 2000)
fig, axes = plt.subplots(2, 2, figsize=(12, 10), tight_layout=True)

# Sine: just fundamental
z_sine = np.exp(1j * 2 * np.pi * freq * t_long)
axes[0,0].plot(z_sine.real, z_sine.imag, lw=1, color='blue')
axes[0,0].set_title('Pure Sine — Perfect Circle')
axes[0,0].set_aspect('equal')

# Sawtooth: sum of 1/n harmonics
z_saw = np.zeros_like(t_long, dtype=complex)
for n in range(1, 20):
    z_saw += (1/n) * np.exp(1j * 2 * np.pi * freq * n * t_long)
axes[0,1].plot(z_saw.real, z_saw.imag, lw=0.5, color='red')
axes[0,1].set_title('Sawtooth — Spirograph Pattern')
axes[0,1].set_aspect('equal')

# Square wave: sum of 1/(2n-1) odd harmonics
z_sq = np.zeros_like(t_long, dtype=complex)
for n in range(1, 20):
    h = 2*n - 1
    z_sq += (1/h) * np.exp(1j * 2 * np.pi * freq * h * t_long)
axes[1,0].plot(z_sq.real, z_sq.imag, lw=0.5, color='green')
axes[1,0].set_title('Square Wave — Diamond Pattern')
axes[1,0].set_aspect('equal')

# Triangle: sum of 1/(2n-1)^2 odd harmonics
z_tri = np.zeros_like(t_long, dtype=complex)
for n in range(1, 20):
    h = 2*n - 1
    z_tri += (1/h**2) * ((-1)**(n-1)) * np.exp(1j * 2 * np.pi * freq * h * t_long)
axes[1,1].plot(z_tri.real, z_tri.imag, lw=0.5, color='orange')
axes[1,1].set_title('Triangle Wave — Rounded Diamond')
axes[1,1].set_aspect('equal')

plt.suptitle('Spin Portraits: Each Wave Shape = Unique Orbital Pattern', fontsize=14)
plt.savefig(os.path.join(OUT, '03_spin_portraits.png'), dpi=150)
plt.close()
print("✓ 03_spin_portraits.png")

# --- 1d. Full waveform reconstruction ---
fig, axes = plt.subplots(2, 2, figsize=(12, 10), tight_layout=True)

# Show real part of each
for ax, (z, name, color) in zip(axes.flat, [
    (z_sine, 'Sine', 'blue'),
    (z_saw / np.max(np.abs(z_saw)), 'Sawtooth', 'red'),
    (z_sq / np.max(np.abs(z_sq)), 'Square', 'green'),
    (z_tri / np.max(np.abs(z_tri)), 'Triangle', 'orange'),
]):
    sig = z.real
    ax.plot(t_long*1000, sig, color=color, lw=1)
    ax.set_title(f'{name} — Real Part (Audible Waveform)')
    ax.set_xlabel('Time (ms)')

plt.suptitle('Waveforms = Real Projections of Complex Spins', fontsize=14)
plt.savefig(os.path.join(OUT, '04_waveforms_from_spins.png'), dpi=150)
plt.close()
print("✓ 04_waveforms_from_spins.png")

# --- Save metadata ---
meta = {
    "experiment": "spin_is_tone",
    "frequencies": [440],
    "harmonics_used": list(range(1, 20)),
    "insight": "Every tone is a complex exponential e^(iωt). The real part is what we hear. The imaginary part is the spin component. Adding harmonics = adding faster spins. Different timbres produce different orbital patterns in the complex plane."
}
with open(os.path.join(os.path.dirname(__file__), 'spin_portraits', 'metadata.json'), 'w') as f:
    json.dump(meta, f, indent=2)

print("\n✅ Experiment 1 complete: spin_is_tone")
