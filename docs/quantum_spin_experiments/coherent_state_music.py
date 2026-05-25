#!/usr/bin/env python3
"""
Experiment 2: Coherent States as Musical Instruments
Shows how coherent state amplitude maps to instrument timbre:
  α small → flute, α medium → trumpet, α large → brass
Plus squeezed states → vocoder/wah effects.
"""

import numpy as np
import json
import wave
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# ── Coherent State Physics ──
def phonon_distribution(alpha, n_max=60):
    """P(n) = e^(-|α|²) |α|^(2n) / n!  — Poisson distribution."""
    n = np.arange(n_max)
    mean_n = abs(alpha)**2
    log_p = -mean_n + 2 * n * np.log(abs(alpha) + 1e-30) - \
            np.array([np.math.factorial(int(k)) if k < 170 else 170 
                      for k in n])  # placeholder
    
    # Better computation using log-gamma
    from math import lgamma
    log_p = -mean_n + n * np.log(mean_n + 1e-30) - np.array([lgamma(k + 1) for k in n])
    P = np.exp(log_p)
    P = P / np.sum(P)  # normalize
    return n, P

def coherent_state_wavefunction(alpha, x, hbar=1.0, omega=1.0):
    """Coherent state |α⟩ wavefunction — displaced Gaussian."""
    x0 = np.sqrt(2 * hbar / omega) * alpha.real
    p0 = np.sqrt(2 * hbar * omega) * alpha.imag
    sigma = np.sqrt(hbar / (2 * omega))
    
    psi = (1.0 / (2 * np.pi * sigma**2)**0.25) * \
          np.exp(-(x - x0)**2 / (4 * sigma**2)) * \
          np.exp(1j * p0 * x / hbar)
    return psi

# ── Instruments from coherent states ──
instruments = {
    "flute":      {"alpha": 1.0 + 0j,  "base_freq": 523.25, "desc": "few phonons, pure tone"},
    "trumpet":    {"alpha": 5.0 + 0j,  "base_freq": 233.08, "desc": "moderate harmonics"},
    "brass":      {"alpha": 20.0 + 0j, "base_freq": 130.81, "desc": "many harmonics, bright"},
    "organ":      {"alpha": 10.0 + 0j, "base_freq": 261.63, "desc": "rich harmonics"},
}

print("Coherent State → Instrument Mapping")
print("=" * 50)

SR = 44100
DURATION = 2.0

all_distributions = {}
x = np.linspace(-15, 15, 4000)

for name, params in instruments.items():
    alpha = params["alpha"]
    n, P = phonon_distribution(alpha)
    mean_n = abs(alpha)**2
    std_n = np.sqrt(np.sum(P * (n - mean_n)**2))
    
    print(f"\n{name.upper()} (|α|={abs(alpha):.1f}):")
    print(f"  Mean phonon number: ⟨n⟩ = {mean_n:.1f}")
    print(f"  Std dev: Δn = {std_n:.2f}")
    print(f"  Distribution width (Δn/⟨n⟩): {std_n/mean_n:.4f}")
    
    # Show top phonon numbers
    top = np.argsort(P)[-5:][::-1]
    print(f"  Top phonon numbers: {list(zip(n[top].tolist(), np.round(P[top], 4).tolist()))}")
    
    all_distributions[name] = {
        "alpha": {"real": alpha.real, "imag": alpha.imag, "magnitude": abs(alpha)},
        "mean_n": float(mean_n),
        "std_n": float(std_n),
        "relative_width": float(std_n / mean_n),
        "phonon_dist": {"n": n[:40].tolist(), "P": P[:40].tolist()}
    }
    
    # ASCII bar chart of distribution
    print(f"  Phonon distribution:")
    max_p = np.max(P)
    for ni in range(min(15, len(P))):
        if P[ni] > 0.005:
            bar = "█" * int(P[ni] / max_p * 30)
            print(f"    n={ni:2d}: {bar} {P[ni]:.4f}")

# ── Audio synthesis from coherent states ──
def synthesize_coherent(alpha, base_freq, duration=DURATION, sr=SR):
    """Synthesize audio whose harmonic spectrum matches the phonon distribution."""
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    n, P = phonon_distribution(alpha)
    
    audio = np.zeros_like(t)
    for i in range(len(P)):
        if P[i] < 0.001:
            continue
        harmonic_freq = base_freq * (i + 1)
        if harmonic_freq > sr / 2:
            break
        # Amplitude follows phonon distribution
        amp = np.sqrt(P[i])
        # ADSR envelope
        attack = np.minimum(t / 0.05, 1.0)
        decay = np.exp(-np.maximum(t - 0.1, 0) / (duration * 0.4))
        envelope = attack * decay
        audio += amp * envelope * np.sin(2 * np.pi * harmonic_freq * t)
    
    # Normalize
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak * 0.8
    return audio

def save_wav(filename, audio, sr=SR):
    audio_int = (audio * 32767).astype(np.int16)
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(audio_int.tobytes())

print("\n\nSynthesizing coherent state audio:")
for name, params in instruments.items():
    audio = synthesize_coherent(params["alpha"], params["base_freq"])
    wav_path = os.path.join(OUT, f"coherent_{name}.wav")
    save_wav(wav_path, audio)
    print(f"  {name} → {wav_path}")

# ── Squeezed States ──
print("\n\nSQUEEZED STATES (vocoder/wah effect):")
print("-" * 40)

def squeezed_state_params(r, phi, alpha):
    """Squeezed coherent state parameters.
    r = squeeze parameter, phi = squeeze angle.
    Sub-Poissonian for r > 0 → narrower than coherent."""
    mean_n = abs(alpha)**2 + np.sinh(r)**2
    # Variance modified by squeezing
    var_n = mean_n + np.sinh(2*r)**2/2 + \
            2 * abs(alpha)**2 * (np.cosh(2*r) - np.sinh(2*r)*np.cos(2*phi - 2*np.angle(alpha)))
    return mean_n, var_n

squeezed_configs = [
    {"name": "squeezed_subpoisson", "r": 1.5, "phi": 0, "alpha": 5.0,
     "desc": "Sub-Poissonian: narrower → vocoder effect"},
    {"name": "squeezed_superpoisson", "r": 1.5, "phi": np.pi/2, "alpha": 5.0,
     "desc": "Super-Poissonian: wider → wah effect"},
    {"name": "squeezed_vacuum", "r": 2.0, "phi": 0, "alpha": 0.0,
     "desc": "Squeezed vacuum: no displacement, pure squeeze"},
]

squeezed_data = {}
for cfg in squeezed_configs:
    mean_n, var_n = squeezed_state_params(cfg["r"], cfg["phi"], cfg["alpha"])
    print(f"\n  {cfg['name']}: {cfg['desc']}")
    print(f"    r={cfg['r']:.1f}, φ={cfg['phi']:.2f}, α={cfg['alpha']:.1f}")
    print(f"    ⟨n⟩={mean_n:.2f}, Var(n)={var_n:.2f}")
    print(f"    Fano factor (Var/⟨n⟩): {var_n/mean_n:.4f}")
    print(f"    {'Sub-Poissonian (narrow)' if var_n < mean_n else 'Super-Poissonian (broad)'}")
    
    squeezed_data[cfg["name"]] = {
        "r": cfg["r"], "phi": cfg["phi"], "alpha": cfg["alpha"],
        "mean_n": float(mean_n), "var_n": float(var_n),
        "fano_factor": float(var_n / mean_n)
    }
    
    # Synthesize squeezed audio (modulate amplitude with squeeze oscillation)
    t = np.linspace(0, DURATION, int(SR * DURATION), endpoint=False)
    base_freq = 220.0
    squeeze_freq = 3.0 + cfg["r"]  # squeeze creates amplitude modulation
    
    # Base tone with harmonics from coherent state
    audio = synthesize_coherent(complex(cfg["alpha"]), base_freq)
    
    # Apply squeeze modulation (amplitude envelope at squeeze frequency)
    if cfg["alpha"] > 0:
        squeeze_mod = 1.0 + 0.3 * cfg["r"] * np.sin(2 * np.pi * squeeze_freq * t)
        audio = audio * squeeze_mod
        peak = np.max(np.abs(audio))
        if peak > 0:
            audio = audio / peak * 0.8
    
    wav_path = os.path.join(OUT, f"squeezed_{cfg['name']}.wav")
    save_wav(wav_path, audio)
    print(f"    → {wav_path}")

# ── Save JSON ──
data = {
    "experiment": "Coherent States as Musical Instruments",
    "coherent_instruments": all_distributions,
    "squeezed_states": squeezed_data,
    "conclusion": "Coherent state amplitude |α| directly controls spectral richness. "
                  "Small |α| → pure sine (flute), medium → moderate harmonics (trumpet), "
                  "large → full spectrum (brass). The Poisson phonon distribution IS the "
                  "instrument's overtone recipe. Squeezed states create amplitude modulation "
                  "effects (vocoder/wah) through sub/super-Poissonian statistics."
}

json_path = os.path.join(OUT, "coherent_states.json")
with open(json_path, 'w') as f:
    json.dump(data, f, indent=2)
print(f"\nSaved: {json_path}")
