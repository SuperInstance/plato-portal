"""
Quality DSP Effect Processor
=============================
Each programming language has a unique "sound" — a characteristic pattern of
numerical errors, rounding behaviors, and computational artifacts. This module
ISOLATES those characteristics and applies them as controllable audio effects.

Analog tape saturation is the "sound" of magnetic hysteresis.
These are the sounds of floating-point arithmetic.
"""

import numpy as np
import struct
import wave
import os


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def _to_float(audio):
    """Ensure audio is float64 in [-1, 1]."""
    a = np.asarray(audio, dtype=np.float64)
    return a


def _clamp(audio):
    """Soft-clamp to [-1, 1]."""
    return np.clip(audio, -1.0, 1.0)


# ---------------------------------------------------------------------------
# Effect 1: Depth — Bit Depth Control (Q1)
# ---------------------------------------------------------------------------

class DepthEffect:
    """
    Simulates f64 (clean), f32 (warm), f16 (lo-fi), f8 (crunchy), f4 (destroyed).
    Quantize: round(x * 2^N) / 2^N
    """

    def apply(self, audio, params=None):
        params = params or {}
        bits = params.get('bits', 64)
        bits = max(4, min(64, int(bits)))
        if bits >= 64:
            return audio.copy()
        audio = _to_float(audio)
        levels = 2 ** bits
        quantized = np.round(audio * levels) / levels
        return _clamp(quantized)


# ---------------------------------------------------------------------------
# Effect 2: Jitter — Consistency Jitter (Q2)
# ---------------------------------------------------------------------------

class JitterEffect:
    """
    Non-deterministic variance from parallel computation.
    CUDA mode: warp-aligned (groups of 32 get same offset)
    CPU mode: sample-by-sample
    fortran_parallel: groups of 128
    """

    def apply(self, audio, params=None):
        params = params or {}
        amount = params.get('amount', 0.0)
        mode = params.get('mode', 'cpu')
        if amount <= 0:
            return audio.copy()
        audio = _to_float(audio).copy()
        n = len(audio)
        rng = np.random.default_rng()

        if mode == 'cuda':
            warp = 32
            n_warps = (n + warp - 1) // warp
            offsets = rng.normal(0, amount * 1e-3, n_warps)
            jitter = np.repeat(offsets, warp)[:n]
        elif mode == 'fortran_parallel':
            block = 128
            n_blocks = (n + block - 1) // block
            offsets = rng.normal(0, amount * 1e-3, n_blocks)
            jitter = np.repeat(offsets, block)[:n]
        else:  # cpu
            jitter = rng.normal(0, amount * 1e-3, n)

        return _clamp(audio + jitter)


# ---------------------------------------------------------------------------
# Effect 3: Compander — Numerical Nonlinearity (Q3)
# ---------------------------------------------------------------------------

class CompanderEffect:
    """
    Float has more precision near 0, less near ±max.
    sign(x) * |x|^α
    α=1: linear (f64), α=1.1: mild (f32), α=1.5: heavy (f16)
    """

    def apply(self, audio, params=None):
        params = params or {}
        alpha = params.get('alpha', 1.0)
        if alpha == 1.0:
            return audio.copy()
        audio = _to_float(audio)
        out = np.sign(audio) * np.power(np.abs(audio) + 1e-12, alpha)
        # normalize to preserve approximate loudness
        peak = np.max(np.abs(out))
        if peak > 0:
            orig_peak = np.max(np.abs(audio))
            out = out * (orig_peak / peak)
        return _clamp(out)


# ---------------------------------------------------------------------------
# Effect 4: Alias — Discontinuity Injection (Q4)
# ---------------------------------------------------------------------------

class AliasEffect:
    """
    Simulates non-smooth behavior from -ffast-math optimizations.
    Injects small step discontinuities at random intervals.
    """

    def apply(self, audio, params=None):
        params = params or {}
        step_size = params.get('step_size', 0.0)
        density = params.get('density', 0.001)  # probability per sample
        if step_size <= 0:
            return audio.copy()
        audio = _to_float(audio).copy()
        n = len(audio)
        rng = np.random.default_rng()
        mask = rng.random(n) < density
        steps = rng.choice([-1, 1], size=n) * step_size * mask
        # accumulate steps so they form discontinuities, then add
        return _clamp(audio + np.cumsum(steps) * 0.01)


# ---------------------------------------------------------------------------
# Effect 5: Purity — Spectral Contamination (Q5)
# ---------------------------------------------------------------------------

class PurityEffect:
    """
    Spurious harmonics from imprecise sin() implementations.
    Mix signal with sin(N·2π·f·t) where N is a spurious harmonic.
    """

    PRESETS = {
        'clean': -120,
        'warm': -80,
        'dirty': -60,
        'crunchy': -40,
        'destroyed': -20,
    }

    def apply(self, audio, params=None):
        params = params or {}
        sr = params.get('sr', 44100)
        level_name = params.get('level', 'warm')
        if isinstance(level_name, (int, float)):
            db = float(level_name)
        else:
            db = self.PRESETS.get(level_name, -80)
        if db <= -120:
            return audio.copy()
        audio = _to_float(audio)
        n = len(audio)
        t = np.arange(n, dtype=np.float64) / sr
        amplitude = 10 ** (db / 20.0)
        # add 2nd and 3rd harmonics of a reference freq
        # detect fundamental from autocorrelation of first 4096 samples
        ref_freq = 440.0  # default A4
        segment = audio[:min(4096, n)]
        corr = np.correlate(segment, segment, mode='full')
        corr = corr[len(corr) // 2:]
        # find first peak after zero crossing
        if len(corr) > sr // 80:
            start = int(sr / 2000)
            peak_idx = start + np.argmax(corr[start:])
            if peak_idx > 0:
                ref_freq = sr / peak_idx

        spur2 = amplitude * np.sin(2 * 2 * np.pi * ref_freq * t)
        spur3 = amplitude * 0.5 * np.sin(3 * 2 * np.pi * ref_freq * t)
        return _clamp(audio + spur2 + spur3)


# ---------------------------------------------------------------------------
# Effect 6: Drift — Temporal Drift (Q6)
# ---------------------------------------------------------------------------

class DriftEffect:
    """
    Drift from repeated numerical operations.
    f(t) = f₀ + A·sin(2π·d·t)
    """

    def apply(self, audio, params=None):
        params = params or {}
        sr = params.get('sr', 44100)
        amount = params.get('amount', 0.0)
        rate = params.get('rate', 0.01)
        if amount <= 0:
            return audio.copy()
        audio = _to_float(audio).copy()
        n = len(audio)
        t = np.arange(n, dtype=np.float64) / sr
        # apply as subtle phase modulation (FM)
        modulation = amount * np.sin(2 * np.pi * rate * t)
        # integrate modulation into phase shift
        phase = np.cumsum(modulation) / sr
        # apply as amplitude modulation for simplicity
        mod_signal = 1.0 + modulation * 0.1
        return _clamp(audio * mod_signal)


# ---------------------------------------------------------------------------
# Effect 7: Saturation — Accumulation Saturation (Q7)
# ---------------------------------------------------------------------------

class SaturationEffect:
    """
    Error accumulation from repeated operations.
    y[n] = tanh(α·x[n] + β·y[n-1])
    """

    def apply(self, audio, params=None):
        params = params or {}
        alpha = params.get('alpha', 1.0)
        beta = params.get('beta', 0.0)
        if beta == 0.0 and alpha == 1.0:
            return audio.copy()
        audio = _to_float(audio)
        n = len(audio)
        out = np.zeros(n, dtype=np.float64)
        prev = 0.0
        for i in range(n):
            out[i] = np.tanh(alpha * audio[i] + beta * prev)
            prev = out[i]
        return _clamp(out)


# ---------------------------------------------------------------------------
# Effect 8: Glitch — Edge Case Artifacts (Q8)
# ---------------------------------------------------------------------------

class GlitchEffect:
    """
    Artifacts from edge-case numerical failures.
    NaN→silence, Inf→clip, -0→phase flip, denorm→dropout
    """

    def apply(self, audio, params=None):
        params = params or {}
        prob_nan = params.get('prob_nan', 0.0)
        prob_inf = params.get('prob_inf', 0.0)
        prob_negzero = params.get('prob_negzero', 0.0)
        prob_denorm = params.get('prob_denorm', 0.0)
        total = prob_nan + prob_inf + prob_negzero + prob_denorm
        if total <= 0:
            return audio.copy()
        audio = _to_float(audio).copy()
        n = len(audio)
        rng = np.random.default_rng()
        r = rng.random(n)

        # NaN → silence
        mask_nan = r < prob_nan
        audio[mask_nan] = 0.0

        # Inf → clip to ±1
        mask_inf = (r >= prob_nan) & (r < prob_nan + prob_inf)
        audio[mask_inf] = np.sign(audio[mask_inf]) * 1.0

        # -0 → phase flip
        mask_nz = (r >= prob_nan + prob_inf) & (r < prob_nan + prob_inf + prob_negzero)
        audio[mask_nz] = -audio[mask_nz]

        # denorm → dropout (fade to zero)
        mask_dn = r >= prob_nan + prob_inf + prob_negzero
        audio[mask_dn] *= 0.01

        return _clamp(audio)


# ---------------------------------------------------------------------------
# Effect 9: Stereo — Cross-Platform Spread (Q9)
# ---------------------------------------------------------------------------

class StereoEffect:
    """
    Simulates -O0 vs -O2 vs -Ofast differences.
    Left: clean, Right: clean + artifact.
    Stereo width = cross-platform disagreement.
    """

    def apply(self, audio, params=None):
        params = params or {}
        width = params.get('width', 0.0)
        sr = params.get('sr', 44100)
        if width <= 0:
            # return mono duplicated
            return np.column_stack([audio, audio])
        audio = _to_float(audio)
        n = len(audio)
        rng = np.random.default_rng()
        # artifact channel: add quantization + noise
        artifact = audio.copy()
        levels = 2 ** 23  # ~f32 mantissa
        artifact = np.round(artifact * levels) / levels
        artifact += rng.normal(0, width * 1e-4, n)
        right = audio * (1 - width) + artifact * width
        return _clamp(np.column_stack([audio, right]))


# ---------------------------------------------------------------------------
# Effect 10: Noise — Error Character / Entropy (Q10)
# ---------------------------------------------------------------------------

class NoiseEffect:
    """
    STRUCTURE of numerical error.
    Low entropy: correlated noise (filtered, warm, analog hiss)
    High entropy: white noise (flat, digital dithering)
    """

    def apply(self, audio, params=None):
        params = params or {}
        amount = params.get('amount', 0.0)
        entropy = params.get('entropy', 0.5)  # 0=correlated, 1=white
        sr = params.get('sr', 44100)
        if amount <= 0:
            return audio.copy()
        audio = _to_float(audio)
        n = len(audio)
        rng = np.random.default_rng()
        noise = rng.normal(0, amount * 0.01, n)
        # filter: low cutoff = correlated, high cutoff = white
        cutoff = max(100, entropy * sr / 2)
        # simple one-pole lowpass
        if cutoff < sr / 2:
            rc = 1.0 / (2 * np.pi * cutoff)
            dt = 1.0 / sr
            alpha_f = dt / (rc + dt)
            filtered = np.zeros(n)
            filtered[0] = noise[0] * alpha_f
            for i in range(1, n):
                filtered[i] = filtered[i - 1] + alpha_f * (noise[i] - filtered[i - 1])
            noise = filtered
        return _clamp(audio + noise)


# ---------------------------------------------------------------------------
# Effect Chain
# ---------------------------------------------------------------------------

class QualityEffectChain:
    def __init__(self, sr=44100):
        self.sr = sr
        self.effects = {
            'depth': DepthEffect(),
            'jitter': JitterEffect(),
            'compander': CompanderEffect(),
            'alias': AliasEffect(),
            'purity': PurityEffect(),
            'drift': DriftEffect(),
            'saturation': SaturationEffect(),
            'glitch': GlitchEffect(),
            'stereo': StereoEffect(),
            'noise': NoiseEffect(),
        }

    def process(self, audio, **params):
        """Run enabled effects in order. Each param key maps to an effect."""
        audio = _to_float(audio)
        is_stereo = False
        for name, effect in self.effects.items():
            if name in params:
                p = dict(params[name])
                p['sr'] = self.sr
                result = effect.apply(audio, p)
                if result.ndim == 2:
                    is_stereo = True
                audio = result
        return audio

    # --- Language / Hardware Presets ---

    def preset_cuda_f32(self, audio):
        """NVIDIA CUDA f32: reduced precision, warp-aligned jitter, warm saturation."""
        return self.process(audio,
            depth={'bits': 24},
            jitter={'amount': 0.3, 'mode': 'cuda'},
            purity={'level': 'dirty'},
            saturation={'alpha': 1.0, 'beta': 0.02},
        )

    def preset_fortran_o2(self, audio):
        """FORTRAN -O2: good precision, slight parallel jitter, very clean."""
        return self.process(audio,
            jitter={'amount': 0.1, 'mode': 'fortran_parallel'},
            purity={'level': 'warm'},
            drift={'amount': 0.2, 'rate': 0.005},
        )

    def preset_rust_release(self, audio):
        """Rust --release: clean, deterministic, tight."""
        return self.process(audio,
            depth={'bits': 48},
            compander={'alpha': 1.01},
            purity={'level': 'clean'},
        )

    def preset_c_ffast_math(self, audio):
        """C -ffast-math: aggressive optimizations, discontinuities, dirty."""
        return self.process(audio,
            alias={'step_size': 0.3, 'density': 0.002},
            purity={'level': 'crunchy'},
            depth={'bits': 32},
            saturation={'alpha': 1.05, 'beta': 0.01},
        )

    def preset_python_numpy_f64(self, audio):
        """Python NumPy f64: reference clean, minimal artifacts."""
        return self.process(audio,
            depth={'bits': 53},
            purity={'level': 'clean'},
        )

    def preset_julia_f64(self, audio):
        """Julia f64: very clean, LLVM-optimized."""
        return self.process(audio,
            depth={'bits': 50},
            purity={'level': 'clean'},
            compander={'alpha': 1.005},
        )

    def preset_go_float64(self, audio):
        """Go float64: clean but deterministic rounding."""
        return self.process(audio,
            depth={'bits': 48},
            noise={'amount': 0.05, 'entropy': 0.3},
        )

    def preset_javascript_f64(self, audio):
        """JavaScript (all numbers are f64): clean, V8-optimized."""
        return self.process(audio,
            depth={'bits': 52},
            compander={'alpha': 1.002},
        )

    def preset_matlab_f64(self, audio):
        """MATLAB f64: clean, BLAS-optimized."""
        return self.process(audio,
            purity={'level': 'warm'},
            jitter={'amount': 0.05, 'mode': 'cpu'},
        )

    def preset_arm_neon_f16(self, audio):
        """ARM NEON f16: half-precision, warm and crunchy."""
        return self.process(audio,
            depth={'bits': 11},
            jitter={'amount': 0.2, 'mode': 'cpu'},
            purity={'level': 'dirty'},
            compander={'alpha': 1.15},
        )

    def preset_gpu_thermal(self, audio):
        """GPU under thermal throttling: drift, jitter, degradation."""
        return self.process(audio,
            depth={'bits': 20},
            jitter={'amount': 0.5, 'mode': 'cuda'},
            drift={'amount': 1.0, 'rate': 0.1},
            saturation={'alpha': 1.1, 'beta': 0.03},
            purity={'level': 'dirty'},
        )

    # --- Creative Presets ---

    def preset_analog_tape(self, audio):
        """Warm analog tape saturation with hiss."""
        return self.process(audio,
            saturation={'alpha': 1.5, 'beta': 0.05},
            noise={'amount': 0.8, 'entropy': 0.2},
            compander={'alpha': 1.12},
            drift={'amount': 0.5, 'rate': 0.01},
            depth={'bits': 40},
        )

    def preset_vinyl(self, audio):
        """Vinyl record: warm, crackly, slight wow."""
        return self.process(audio,
            noise={'amount': 1.0, 'entropy': 0.15},
            drift={'amount': 0.8, 'rate': 0.005},
            depth={'bits': 36},
            saturation={'alpha': 1.2, 'beta': 0.02},
            purity={'level': 'warm'},
        )

    def preset_8bit_chip(self, audio):
        """8-bit chiptune: crunchy, quantized, retro."""
        return self.process(audio,
            depth={'bits': 8},
            compander={'alpha': 1.3},
            purity={'level': 'crunchy'},
            alias={'step_size': 0.5, 'density': 0.005},
        )

    def preset_broken_dac(self, audio):
        """Broken DAC: glitchy, dropping bits, artifacts."""
        return self.process(audio,
            depth={'bits': 12},
            glitch={'prob_nan': 0.001, 'prob_inf': 0.002, 'prob_negzero': 0.005, 'prob_denorm': 0.01},
            alias={'step_size': 0.8, 'density': 0.01},
            purity={'level': 'destroyed'},
        )

    def preset_gpu_thermal_creative(self, audio):
        """Creative: GPU thermal throttling as musical effect."""
        return self.process(audio,
            drift={'amount': 2.0, 'rate': 0.15},
            jitter={'amount': 0.7, 'mode': 'cuda'},
            depth={'bits': 18},
            saturation={'alpha': 1.3, 'beta': 0.05},
            purity={'level': 'crunchy'},
        )

    def preset_interstellar(self, audio):
        """Interstellar: extreme drift, lo-fi, haunting."""
        return self.process(audio,
            depth={'bits': 14},
            drift={'amount': 3.0, 'rate': 0.003},
            noise={'amount': 1.5, 'entropy': 0.1},
            purity={'level': 'dirty'},
            saturation={'alpha': 1.8, 'beta': 0.08},
        )

    def preset_hologram(self, audio):
        """Hologram: digital shimmer, spectral artifacts, ethereal."""
        return self.process(audio,
            purity={'level': 'dirty'},
            jitter={'amount': 0.15, 'mode': 'cpu'},
            depth={'bits': 28},
            compander={'alpha': 1.08},
            stereo={'width': 0.6},
        )

    def preset_magnetic(self, audio):
        """Magnetic: warm saturation with memory/feedback."""
        return self.process(audio,
            saturation={'alpha': 1.4, 'beta': 0.1},
            noise={'amount': 0.6, 'entropy': 0.25},
            compander={'alpha': 1.15},
            depth={'bits': 32},
        )

    def preset_quantum(self, audio):
        """Quantum: glitchy, probabilistic, unpredictable."""
        return self.process(audio,
            glitch={'prob_nan': 0.003, 'prob_inf': 0.001, 'prob_negzero': 0.01, 'prob_denorm': 0.005},
            jitter={'amount': 0.8, 'mode': 'cuda'},
            depth={'bits': 16},
            purity={'level': 'destroyed'},
            alias={'step_size': 1.0, 'density': 0.008},
        )

    def preset_deep_ocean(self, audio):
        """Deep Ocean: filtered, muffled, vast, slow drift."""
        return self.process(audio,
            noise={'amount': 2.0, 'entropy': 0.05},
            depth={'bits': 24},
            drift={'amount': 1.5, 'rate': 0.001},
            saturation={'alpha': 0.8, 'beta': 0.15},
            compander={'alpha': 1.2},
        )

    def preset_chip_8bit(self, audio):
        """8-bit chip: depth=8, purity=dirty, alias=high."""
        return self.process(audio,
            depth={'bits': 8},
            purity={'level': 'dirty'},
            alias={'step_size': 0.6, 'density': 0.008},
            compander={'alpha': 1.2},
        )

    def preset_broken_dac(self, audio):
        """Broken DAC: glitch=high, jitter=high, stereo=wide."""
        return self.process(audio,
            depth={'bits': 12},
            glitch={'prob_nan': 0.002, 'prob_inf': 0.003, 'prob_negzero': 0.008, 'prob_denorm': 0.015},
            jitter={'amount': 0.8, 'mode': 'cpu'},
            alias={'step_size': 0.8, 'density': 0.01},
            purity={'level': 'destroyed'},
            stereo={'width': 0.8},
        )

    def preset_vinyl_crackle(self, audio):
        """Vinyl crackle: glitch + noise + depth reduction."""
        return self.process(audio,
            noise={'amount': 1.2, 'entropy': 0.15},
            drift={'amount': 0.6, 'rate': 0.005},
            depth={'bits': 36},
            saturation={'alpha': 1.15, 'beta': 0.02},
            glitch={'prob_nan': 0.0005, 'prob_inf': 0.0, 'prob_negzero': 0.0, 'prob_denorm': 0.008},
            purity={'level': 'warm'},
        )

    def preset_mainframe_fortran(self, audio):
        """Mainframe FORTRAN: depth=32, very clean, ultra-low jitter."""
        return self.process(audio,
            depth={'bits': 32},
            jitter={'amount': 0.02, 'mode': 'fortran_parallel'},
            purity={'level': 'warm'},
        )

    def preset_teen_engine(self, audio):
        """Teen engine: depth=4, alias=high, purity=destroyed."""
        return self.process(audio,
            depth={'bits': 4},
            alias={'step_size': 1.0, 'density': 0.015},
            purity={'level': 'destroyed'},
            compander={'alpha': 1.5},
            noise={'amount': 0.5, 'entropy': 0.8},
        )

    def preset_radio_shortwave(self, audio):
        """Shortwave radio: noisy, fading, drifting."""
        return self.process(audio,
            noise={'amount': 3.0, 'entropy': 0.6},
            drift={'amount': 2.0, 'rate': 0.05},
            depth={'bits': 20},
            purity={'level': 'crunchy'},
            alias={'step_size': 0.4, 'density': 0.003},
            glitch={'prob_nan': 0.002, 'prob_inf': 0.0, 'prob_negzero': 0.0, 'prob_denorm': 0.003},
        )

    # --- Get all presets ---

    def get_presets(self):
        """Return dict of all preset name -> callable."""
        presets = {}
        for name in dir(self):
            if name.startswith('preset_'):
                presets[name.replace('preset_', '')] = getattr(self, name)
        return presets


# ---------------------------------------------------------------------------
# WAV I/O
# ---------------------------------------------------------------------------

def write_wav(filename, audio, sr=44100):
    """Write mono or stereo float audio to 16-bit WAV."""
    audio = np.asarray(audio)
    if audio.ndim == 1:
        audio = audio.reshape(-1, 1)
    n_channels = audio.shape[1]
    # normalize
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak * 0.95
    # convert to int16
    pcm = np.int16(audio * 32767)
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())


def read_wav(filename):
    """Read WAV file, return (audio_float64, sr)."""
    with wave.open(filename, 'r') as wf:
        sr = wf.getframerate()
        n_channels = wf.getnchannels()
        n_frames = wf.getnframes()
        raw = wf.readframes(n_frames)
    pcm = np.frombuffer(raw, dtype=np.int16).reshape(-1, n_channels)
    return pcm.astype(np.float64) / 32767.0, sr


# ---------------------------------------------------------------------------
# Demo signal generators
# ---------------------------------------------------------------------------

def generate_test_signal(sr=44100, duration=3.0):
    """Generate a rich test signal: chord (A3, C#4, E4) with harmonics."""
    t = np.arange(int(sr * duration), dtype=np.float64) / sr
    freqs = [220.0, 277.18, 329.63]  # A3, C#4, E4
    signal = np.zeros_like(t)
    for f in freqs:
        signal += np.sin(2 * np.pi * f * t)
        signal += 0.3 * np.sin(2 * np.pi * f * 2 * t)  # 2nd harmonic
        signal += 0.1 * np.sin(2 * np.pi * f * 3 * t)  # 3rd harmonic
    # envelope
    env = np.ones_like(t)
    fade = int(0.05 * sr)
    env[:fade] = np.linspace(0, 1, fade)
    env[-fade:] = np.linspace(1, 0, fade)
    signal *= env
    # normalize
    signal = signal / np.max(np.abs(signal)) * 0.8
    return signal


if __name__ == '__main__':
    print("🎵 Quality DSP Effect Processor")
    print("=" * 50)

    sr = 44100
    chain = QualityEffectChain(sr=sr)
    signal = generate_test_signal(sr=sr, duration=3.0)
    presets = chain.get_presets()

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
    os.makedirs(out_dir, exist_ok=True)

    # Write clean reference
    write_wav(os.path.join(out_dir, '00_reference_clean.wav'), signal, sr)
    print(f"  ✓ 00_reference_clean.wav")

    for i, (name, func) in enumerate(sorted(presets.items()), 1):
        try:
            result = func(signal)
            fname = f"{i:02d}_{name}.wav"
            write_wav(os.path.join(out_dir, fname), result, sr)
            channels = "stereo" if result.ndim == 2 else "mono"
            print(f"  ✓ {fname} ({channels})")
        except Exception as e:
            print(f"  ✗ {name}: {e}")

    print(f"\n✅ Generated {len(presets) + 1} WAV files in {out_dir}")
