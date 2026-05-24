#!/usr/bin/env python3
"""
GPU-Accelerated Constraint Audio Engine
========================================
PyTorch/CUDA port of the constraint-audio-rs crate's core algorithms.

Modules:
  1. CUDA Lattice Oscillator — hundreds of partials in parallel
  2. CUDA RBJ Biquad Bank — 64 parallel biquad filters (one per voice)
  3. CUDA Consonance Filter — score all extensions in one GPU pass
  4. Benchmark suite — CPU vs GPU timing
  5. Real-time audio render test — 30s piece, 64 voices, save as WAV

Based on the Rust crate at /tmp/constraint-audio-rs/.
Requires: torch >= 2.0 with CUDA support
"""

import math
import time
import struct
import wave
from typing import List, Tuple, Optional
from enum import Enum

import torch
import torch.nn.functional as F

# ---------------------------------------------------------------------------
# Device helpers
# ---------------------------------------------------------------------------
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Harmonic lattice primes: just intonation ratios 2^a * 3^b * 5^c
LATTICE_PRIMES = [2.0, 3.0, 5.0]


# ===================================================================
# 1. CUDA LATTICE OSCILLATOR
# ===================================================================

class WaveformShape(Enum):
    Sine = 0
    Square = 1
    Saw = 2
    Triangle = 3
    Eisenstein = 4


class CudaLatticeOscillator:
    """
    GPU-accelerated lattice oscillator.

    Generates waveforms from harmonic lattice coordinates (2^a × 3^b × 5^c).
    The GPU computes hundreds of partials simultaneously for polyphonic synthesis.

    Vectorised over (num_voices, num_samples) tensors on GPU.
    """

    def __init__(self, device: torch.device = DEVICE):
        self.device = device

    # ---- waveform kernels (vectorised, no per-sample loops) ----

    def _sine(self, phase: torch.Tensor) -> torch.Tensor:
        return torch.sin(2.0 * math.pi * phase)

    def _square_polyblep(self, phase: torch.Tensor, dt: torch.Tensor) -> torch.Tensor:
        val = torch.where(phase < 0.5, torch.ones_like(phase), -torch.ones_like(phase))
        val = val + self._polyblep(phase, dt)
        val = val - self._polyblep((phase + 0.5) % 1.0, dt)
        return val

    def _saw_polyblep(self, phase: torch.Tensor, dt: torch.Tensor) -> torch.Tensor:
        return 2.0 * phase - 1.0 - self._polyblep(phase, dt)

    def _triangle(self, phase: torch.Tensor, dt: torch.Tensor) -> torch.Tensor:
        saw = 2.0 * phase - 1.0
        return 2.0 * (saw.abs() - 0.5)

    def _eisenstein(self, phase: torch.Tensor) -> torch.Tensor:
        """Eisenstein integer (A2 lattice) phase mapping."""
        omega_angle = 2.0 * math.pi / 3.0
        a = phase
        b = (phase * 1.5).frac()
        # Project onto Eisenstein plane
        re = a + b * math.cos(omega_angle)
        im = b * math.sin(omega_angle)
        mag = (re * re + im * im).sqrt().clamp(min=1e-3)
        return (re / mag * torch.sin(2.0 * math.pi * phase)).tanh()

    def _polyblep(self, t: torch.Tensor, dt: torch.Tensor) -> torch.Tensor:
        """Vectorised 2-point PolyBLEP correction kernel."""
        x_lo = t / dt
        corr_lo = x_lo + x_lo - x_lo * x_lo - 1.0
        x_hi = (t - 1.0) / dt
        corr_hi = x_hi * x_hi + x_hi + x_hi + 1.0
        return torch.where(t < dt, corr_lo,
                           torch.where(t > 1.0 - dt, corr_hi,
                                       torch.zeros_like(t)))

    # ---- partial generation from lattice coordinates ----

    def generate_partials(
        self,
        base_freqs: torch.Tensor,       # (V,) voice fundamental frequencies
        lattice_coords: torch.Tensor,    # (P, 3) int tuples (a, b, c)
        amplitudes: torch.Tensor,        # (P,) partial amplitudes
        num_samples: int,
        sample_rate: float,
        shape: WaveformShape = WaveformShape.Sine,
        stretch: float = 1.0,
    ) -> torch.Tensor:
        """
        Generate P partials for V voices simultaneously.

        Returns: (V, num_samples) tensor on GPU.
        """
        V = base_freqs.shape[0]
        P = lattice_coords.shape[0]

        # Compute partial frequencies: f_base * 2^a * 3^b * 5^c
        # lattice_coords: (P, 3) -> ratios (P,)
        ratios = (LATTICE_PRIMES[0] ** lattice_coords[:, 0].float() *
                  LATTICE_PRIMES[1] ** lattice_coords[:, 1].float() *
                  LATTICE_PRIMES[2] ** lattice_coords[:, 2].float())

        # partial_freqs: (V, P)
        partial_freqs = base_freqs.unsqueeze(1) * ratios.unsqueeze(0)

        # phase_inc: (V, P)
        phase_inc = partial_freqs / sample_rate * stretch

        # Cumulative phase: (V, P, T)
        t = torch.arange(num_samples, device=self.device, dtype=torch.float32)
        phase = (phase_inc.unsqueeze(2) * t.unsqueeze(0).unsqueeze(0)) % 1.0

        # Generate waveform samples
        dt = phase_inc.unsqueeze(2).expand_as(phase)

        if shape == WaveformShape.Sine:
            samples = torch.sin(2.0 * math.pi * phase)
        elif shape == WaveformShape.Square:
            samples = self._square_polyblep(phase, dt)
        elif shape == WaveformShape.Saw:
            samples = self._saw_polyblep(phase, dt)
        elif shape == WaveformShape.Triangle:
            samples = self._triangle(phase, dt)
        elif shape == WaveformShape.Eisenstein:
            samples = self._eisenstein(phase)
        else:
            samples = torch.sin(2.0 * math.pi * phase)

        # Apply amplitudes: (P,) -> (1, P, 1)
        samples = samples * amplitudes.view(1, P, 1)

        # Sum partials -> (V, T)
        output = samples.sum(dim=1)

        # Normalise so peak is [-1, 1] ish
        peak = output.abs().amax(dim=1, keepdim=True).clamp(min=1e-6)
        output = output / peak * 0.8

        return output

    def generate_voices(
        self,
        freqs: torch.Tensor,       # (V,)
        num_samples: int,
        sample_rate: float,
        shape: WaveformShape = WaveformShape.Sine,
        stretch: float = 1.0,
    ) -> torch.Tensor:
        """
        Generate simple (single-partial) waveforms for V voices.
        Returns: (V, num_samples).
        """
        V = freqs.shape[0]
        phase_inc = freqs / sample_rate * stretch
        t = torch.arange(num_samples, device=self.device, dtype=torch.float32)
        # (V, T)
        phase = (phase_inc.unsqueeze(1) * t.unsqueeze(0)) % 1.0
        dt = phase_inc.unsqueeze(1).expand_as(phase)

        if shape == WaveformShape.Sine:
            return torch.sin(2.0 * math.pi * phase)
        elif shape == WaveformShape.Square:
            return self._square_polyblep(phase, dt)
        elif shape == WaveformShape.Saw:
            return self._saw_polyblep(phase, dt)
        elif shape == WaveformShape.Triangle:
            return self._triangle(phase, dt)
        elif shape == WaveformShape.Eisenstein:
            return self._eisenstein(phase)
        return torch.sin(2.0 * math.pi * phase)


# ===================================================================
# 2. CUDA RBJ BIQUAD BANK
# ===================================================================

class CudaBiquadBank:
    """
    Process N parallel biquad filters on GPU using Direct Form II Transposed.

    Each filter can have different coefficients (e.g. one per voice).
    Processes (N, T) signal tensor through N independent filters.

    This is the main bottleneck in real-time polyphonic synthesis —
    each voice needs its own filter with separate state.
    """

    def __init__(self, device: torch.device = DEVICE):
        self.device = device

    @staticmethod
    def rbj_coefficients(
        filter_type: str,   # 'lowpass', 'highpass', 'bandpass'
        cutoffs: torch.Tensor,  # (N,) cutoff frequencies
        qs: torch.Tensor,       # (N,) Q values
        sample_rate: float,
    ) -> Tuple[torch.Tensor, ...]:
        """
        Compute RBJ Audio EQ Cookbook coefficients for N filters.

        Returns: (b0, b1, b2, a1, a2) each of shape (N,).
        """
        w0 = 2.0 * math.pi * cutoffs / sample_rate
        cos_w0 = torch.cos(w0)
        sin_w0 = torch.sin(w0)
        alpha = sin_w0 / (2.0 * qs)

        if filter_type == "lowpass":
            b1 = 1.0 - cos_w0
            b0 = b1 / 2.0
            b2 = b0
        elif filter_type == "highpass":
            b0 = (1.0 + cos_w0) / 2.0
            b1 = -(1.0 + cos_w0)
            b2 = b0
        elif filter_type == "bandpass":
            b0 = qs * alpha
            b1 = torch.zeros_like(cutoffs)
            b2 = -b0
        else:
            raise ValueError(f"Unknown filter type: {filter_type}")

        a0 = 1.0 + alpha
        a1 = -2.0 * cos_w0
        a2 = 1.0 - alpha

        # Normalise
        return b0 / a0, b1 / a0, b2 / a0, a1 / a0, a2 / a0

    def process(
        self,
        signal: torch.Tensor,       # (N, T) N voices, T samples
        b0: torch.Tensor,            # (N,)
        b1: torch.Tensor,
        b2: torch.Tensor,
        a1: torch.Tensor,
        a2: torch.Tensor,
    ) -> torch.Tensor:
        """
        Apply N parallel biquad filters in Direct Form II Transposed.

        Processed sequentially sample-by-sample on GPU (necessary for IIR state).
        The computation is vectorised across N filters at each time step.

        Returns: (N, T) filtered signal.
        """
        N, T = signal.shape
        # State variables
        z1 = torch.zeros(N, device=self.device, dtype=signal.dtype)
        z2 = torch.zeros(N, device=self.device, dtype=signal.dtype)

        # Pre-allocate output
        output = torch.empty_like(signal)

        for t in range(T):
            x = signal[:, t]
            y = b0 * x + z1
            z1 = b1 * x - a1 * y + z2
            z2 = b2 * x - a2 * y
            output[:, t] = y

        return output

    def create_filter_bank(
        self,
        filter_type: str,
        cutoffs: torch.Tensor,  # (N,)
        qs: torch.Tensor,       # (N,)
        sample_rate: float,
    ) -> Tuple[torch.Tensor, ...]:
        """Convenience: compute coefficients and return them."""
        return self.rbj_coefficients(filter_type, cutoffs, qs, sample_rate)


# ===================================================================
# 3. CUDA CONSONANCE FILTER / SCORER
# ===================================================================

# Consonant intervals in semitones (matching Rust crate)
CONSONANT_SEMITONES = [0, 3, 4, 5, 7, 9, 12]

# Extended consonance mapping: interval semitones -> consonance weight
# Based on harmonic series proximity
INTERVAL_WEIGHTS = {
    0:  1.0,   # unison
    1:  0.05,  # minor 2nd
    2:  0.15,  # major 2nd
    3:  0.75,  # minor 3rd
    4:  0.85,  # major 3rd
    5:  0.95,  # perfect 4th
    6:  0.30,  # tritone
    7:  1.0,   # perfect 5th
    8:  0.25,  # minor 6th
    9:  0.70,  # major 6th
    10: 0.20,  # minor 7th
    11: 0.55,  # major 7th
    12: 1.0,   # octave
}


class CudaConsonanceScorer:
    """
    Score the consonance of all possible chord extensions in ONE GPU pass.

    Given a chord (set of MIDI pitches), computes a consonance score for
    every possible additional note (0-127). This enables real-time
    "consonance-maximizing" play-along systems.

    The scoring considers:
    - Pairwise interval consonance (all intervals against all chord tones)
    - Harmonic lattice proximity (just intonation ratios)
    - Octave equivalence
    """

    def __init__(self, device: torch.device = DEVICE):
        self.device = device
        # Build weight tensor: (128, 128) pairwise consonance matrix
        weights = torch.zeros(128, 128, device=device)
        for i in range(128):
            for j in range(128):
                interval = abs(i - j) % 12
                # Weight by both interval quality and octave distance
                octave_dist = abs(i - j) // 12
                w = INTERVAL_WEIGHTS.get(interval, 0.1)
                # Diminish with octave distance
                w *= max(0.2, 1.0 - octave_dist * 0.15)
                weights[i, j] = w
        self.weights = weights

        # Lattice consonance: ratios close to 2^a * 3^b * 5^c are more consonant
        # Pre-compute just intonation ratios for intervals 0-24 semitones
        self.lattice_ratios = self._build_lattice_ratio_table()

    def _build_lattice_ratio_table(self) -> torch.Tensor:
        """Build a table of just-intonation ratios for scoring."""
        # Generate lattice coordinates up to reasonable limits
        coords = []
        for a in range(-2, 5):
            for b in range(-2, 4):
                for c in range(-1, 3):
                    ratio = (2.0 ** a) * (3.0 ** b) * (5.0 ** c)
                    if 0.5 <= ratio <= 8.0:
                        # Convert ratio to semitones
                        semitones = 12.0 * math.log2(ratio)
                        coords.append((semitones, ratio))
        return coords

    def score_extensions(
        self,
        chord_pitches: List[int],
        candidate_range: Tuple[int, int] = (36, 96),
    ) -> torch.Tensor:
        """
        Score all possible note additions to a chord in one GPU pass.

        Args:
            chord_pitches: MIDI pitches of the current chord.
            candidate_range: (low, high) MIDI range to score.

        Returns:
            Tensor of shape (num_candidates,) with consonance scores.
        """
        lo, hi = candidate_range
        candidates = torch.arange(lo, hi + 1, device=self.device)
        num_cand = candidates.shape[0]
        chord = torch.tensor(chord_pitches, device=self.device, dtype=torch.long)

        # Expand: (num_chord, num_candidates) interval matrix
        intervals = (chord.unsqueeze(1) - candidates.unsqueeze(0)).abs()

        # Map intervals to weights via the pre-built matrix
        # Clamp to valid range
        interval_mod = intervals % 12
        octave_dist = intervals // 12
        chord_weights = torch.zeros_like(intervals, dtype=torch.float32)
        for sem, w in INTERVAL_WEIGHTS.items():
            chord_weights = torch.where(interval_mod == sem, chord_weights + w, chord_weights)

        # Penalise large intervals
        chord_weights = chord_weights * torch.clamp(1.0 - octave_dist.float() * 0.1, min=0.1)

        # Score = sum of pairwise consonance, inverse to prefer candidates
        # that are consonant with ALL chord tones
        scores = chord_weights.sum(dim=0)  # sum over chord tones

        # Bonus: lattice proximity — candidates that form near-just ratios
        # with the chord root get a bonus
        if len(chord_pitches) > 0:
            root = chord_pitches[0]
            root_diff = (candidates.float() - root).abs()
            for semitones, ratio in self.lattice_ratios:
                near_lattice = (root_diff - abs(semitones)).abs() < 0.5
                scores = scores + near_lattice.float() * 0.3

        # Penalty for notes already in the chord
        for p in chord_pitches:
            in_chord = (candidates == p)
            scores = scores - in_chord.float() * 2.0

        return scores

    def consonance_filter_gpu(
        self,
        signal: torch.Tensor,    # (1, T) or (T,)
        root_freq: float,
        sample_rate: float,
        bandwidth: float = 0.5,
        blend: float = 0.5,
    ) -> torch.Tensor:
        """
        GPU consonance filter: emphasise consonant harmonics of root_freq.

        Applies parallel bandpass filters at consonant intervals of root.
        """
        if signal.dim() == 1:
            signal = signal.unsqueeze(0)

        T = signal.shape[1]
        original = signal.clone()

        # Build bandpass filters at consonant intervals
        harmonic_freqs = []
        for interval in CONSONANT_SEMITONES:
            f = root_freq * (2.0 ** (interval / 12.0))
            if f < sample_rate / 2.0:
                harmonic_freqs.append(f)

        num_filters = len(harmonic_freqs)
        cutoffs = torch.tensor(harmonic_freqs, device=self.device)
        qs = (cutoffs / max(bandwidth * root_freq, 1.0)).clamp(min=0.1)

        bank = CudaBiquadBank(device=self.device)

        # Process each filter and accumulate
        # Replicate signal for N filters: (N, T)
        sig_n = signal.expand(num_filters, T).clone()
        b0, b1, b2, a1, a2 = bank.rbj_coefficients("bandpass", cutoffs, qs, sample_rate)
        filtered = bank.process(sig_n, b0, b1, b2, a1, a2)

        # Average across filters
        avg_filtered = filtered.mean(dim=0, keepdim=True)

        # Blend
        output = original * (1.0 - blend) + avg_filtered * blend
        return output.squeeze(0)


# ===================================================================
# 4. BENCHMARK SUITE
# ===================================================================

class Benchmark:
    """CPU vs GPU timing comparison with torch.cuda.Event for accurate GPU timing."""

    def __init__(self, device: torch.device = DEVICE):
        self.device = device
        self.results: List[dict] = []

    def _gpu_timer(self):
        """Return start/stop cuda events for accurate GPU timing."""
        start = torch.cuda.Event(enable_timing=True)
        end = torch.cuda.Event(enable_timing=True)
        return start, end

    def bench_lattice_oscillator(self, num_voices: int = 100, duration: float = 5.0,
                                  sample_rate: float = 44100.0, num_partials: int = 16):
        """Benchmark lattice oscillator: CPU vs GPU for N-voice polyphony."""
        num_samples = int(duration * sample_rate)
        print(f"\n{'='*60}")
        print(f"  LATTICE OSCILLATOR BENCHMARK — {num_voices} voices, "
              f"{num_partials} partials, {duration}s @ {sample_rate}Hz")
        print(f"{'='*60}")

        # Generate random voice frequencies (MIDI range 36-96)
        freqs = 440.0 * 2.0 ** ((torch.randint(36, 97, (num_voices,)) - 69) / 12.0)
        freqs_cpu = freqs.clone()
        freqs_gpu = freqs.to(self.device)

        # Lattice coordinates for partials (a, b, c) with small ranges
        coords_list = []
        for a in range(0, 4):
            for b in range(0, 3):
                for c in range(0, 2):
                    coords_list.append([a, b, c])
                    if len(coords_list) >= num_partials:
                        break
                if len(coords_list) >= num_partials:
                    break
            if len(coords_list) >= num_partials:
                break
        lattice_coords = torch.tensor(coords_list[:num_partials], dtype=torch.long)
        # Amplitudes decrease with partial number
        amplitudes = 1.0 / (torch.arange(num_partials, dtype=torch.float32) + 1.0)

        # --- CPU benchmark ---
        osc = CudaLatticeOscillator(device=torch.device("cpu"))
        t0 = time.perf_counter()
        cpu_out = osc.generate_partials(
            freqs_cpu, lattice_coords, amplitudes,
            num_samples, sample_rate, WaveformShape.Sine
        )
        cpu_time = time.perf_counter() - t0

        # --- GPU benchmark ---
        osc_gpu = CudaLatticeOscillator(device=self.device)
        lattice_coords_gpu = lattice_coords.to(self.device)
        amplitudes_gpu = amplitudes.to(self.device)

        # Warmup
        _ = osc_gpu.generate_partials(
            freqs_gpu, lattice_coords_gpu, amplitudes_gpu,
            num_samples, sample_rate, WaveformShape.Sine
        )
        torch.cuda.synchronize()

        start_event, end_event = self._gpu_timer()
        start_event.record()
        gpu_out = osc_gpu.generate_partials(
            freqs_gpu, lattice_coords_gpu, amplitudes_gpu,
            num_samples, sample_rate, WaveformShape.Sine
        )
        end_event.record()
        torch.cuda.synchronize()
        gpu_time = start_event.elapsed_time(end_event) / 1000.0  # ms -> s

        speedup = cpu_time / gpu_time if gpu_time > 0 else float("inf")
        self.results.append({
            "test": "Lattice Oscillator",
            "voices": num_voices,
            "partials": num_partials,
            "cpu_time": cpu_time,
            "gpu_time": gpu_time,
            "speedup": speedup,
        })
        print(f"  CPU time: {cpu_time:.4f}s")
        print(f"  GPU time: {gpu_time:.4f}s")
        print(f"  Speedup:  {speedup:.2f}x")
        print(f"  Output shape: {gpu_out.shape}")

    def bench_biquad_bank(self, num_voices: int = 64, duration: float = 5.0,
                           sample_rate: float = 44100.0):
        """Benchmark parallel biquad filter bank: CPU vs GPU."""
        num_samples = int(duration * sample_rate)
        print(f"\n{'='*60}")
        print(f"  BIQUAD FILTER BANK BENCHMARK — {num_voices} voices, "
              f"{duration}s @ {sample_rate}Hz")
        print(f"{'='*60}")

        # Generate test signal: white noise for each voice
        torch.manual_seed(42)
        signal_cpu = torch.randn(num_voices, num_samples)
        signal_gpu = signal_cpu.to(self.device)

        # Random cutoffs and Q values
        cutoffs = torch.rand(num_voices) * 4000 + 200   # 200-4200 Hz
        qs = torch.rand(num_voices) * 4 + 0.5            # 0.5-4.5

        # --- CPU benchmark ---
        bank_cpu = CudaBiquadBank(device=torch.device("cpu"))
        b0, b1, b2, a1, a2 = bank_cpu.rbj_coefficients("lowpass", cutoffs, qs, sample_rate)
        t0 = time.perf_counter()
        cpu_out = bank_cpu.process(signal_cpu, b0, b1, b2, a1, a2)
        cpu_time = time.perf_counter() - t0

        # --- GPU benchmark ---
        bank_gpu = CudaBiquadBank(device=self.device)
        cutoffs_g = cutoffs.to(self.device)
        qs_g = qs.to(self.device)
        b0g, b1g, b2g, a1g, a2g = bank_gpu.rbj_coefficients("lowpass", cutoffs_g, qs_g, sample_rate)

        # Warmup
        _ = bank_gpu.process(signal_gpu.clone(), b0g, b1g, b2g, a1g, a2g)
        torch.cuda.synchronize()

        start_event, end_event = self._gpu_timer()
        start_event.record()
        gpu_out = bank_gpu.process(signal_gpu.clone(), b0g, b1g, b2g, a1g, a2g)
        end_event.record()
        torch.cuda.synchronize()
        gpu_time = start_event.elapsed_time(end_event) / 1000.0

        speedup = cpu_time / gpu_time if gpu_time > 0 else float("inf")
        self.results.append({
            "test": "RBJ Biquad Bank",
            "voices": num_voices,
            "cpu_time": cpu_time,
            "gpu_time": gpu_time,
            "speedup": speedup,
        })
        print(f"  CPU time: {cpu_time:.4f}s")
        print(f"  GPU time: {gpu_time:.4f}s")
        print(f"  Speedup:  {speedup:.2f}x")

    def bench_consonance_scorer(self, chord_size: int = 5):
        """Benchmark consonance scoring: CPU vs GPU."""
        print(f"\n{'='*60}")
        print(f"  CONSONANCE SCORER BENCHMARK — {chord_size}-note chord")
        print(f"{'='*60}")

        chord = [60, 64, 67, 72, 76]  # Cmaj7-ish

        # CPU
        scorer_cpu = CudaConsonanceScorer(device=torch.device("cpu"))
        t0 = time.perf_counter()
        for _ in range(1000):
            scores_cpu = scorer_cpu.score_extensions(chord)
        cpu_time = time.perf_counter() - t0

        # GPU
        scorer_gpu = CudaConsonanceScorer(device=self.device)
        # Warmup
        _ = scorer_gpu.score_extensions(chord)
        torch.cuda.synchronize()

        start_event, end_event = self._gpu_timer()
        start_event.record()
        for _ in range(1000):
            scores_gpu = scorer_gpu.score_extensions(chord)
        end_event.record()
        torch.cuda.synchronize()
        gpu_time = start_event.elapsed_time(end_event) / 1000.0

        speedup = cpu_time / gpu_time if gpu_time > 0 else float("inf")
        best_note = scores_gpu.argmax().item() + 36
        self.results.append({
            "test": "Consonance Scorer",
            "iterations": 1000,
            "cpu_time": cpu_time,
            "gpu_time": gpu_time,
            "speedup": speedup,
            "best_extension": best_note,
        })
        print(f"  CPU time (1000 iterations): {cpu_time:.4f}s")
        print(f"  GPU time (1000 iterations): {gpu_time:.4f}s")
        print(f"  Speedup:  {speedup:.2f}x")
        print(f"  Best consonant extension: MIDI {best_note} "
              f"({440 * 2 ** ((best_note - 69) / 12):.1f} Hz)")

    def run_all(self):
        """Run all benchmarks."""
        print(f"\n{'#'*60}")
        print(f"  GPU Audio Engine Benchmark Suite")
        print(f"  Device: {self.device}")
        if self.device.type == "cuda":
            print(f"  GPU: {torch.cuda.get_device_name(0)}")
            print(f"  VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        print(f"{'#'*60}")

        self.bench_lattice_oscillator(num_voices=100, duration=5.0, num_partials=16)
        self.bench_biquad_bank(num_voices=64, duration=5.0)
        self.bench_consonance_scorer()

        print(f"\n{'='*60}")
        print(f"  SUMMARY")
        print(f"{'='*60}")
        for r in self.results:
            print(f"  {r['test']:25s} — Speedup: {r['speedup']:.2f}x  "
                  f"(CPU {r['cpu_time']:.4f}s → GPU {r['gpu_time']:.4f}s)")

        return self.results


# ===================================================================
# 5. REAL-TIME AUDIO RENDER — 30s piece, 64 voices, save as WAV
# ===================================================================

def midi_to_freq(pitch: int) -> float:
    return 440.0 * 2.0 ** ((pitch - 69) / 12.0)


def generate_adsr_envelope(
    num_samples: int,
    attack: float, decay: float, sustain: float, release: float,
    sample_rate: float,
    device: torch.device = DEVICE,
) -> torch.Tensor:
    """Generate ADSR envelope on GPU."""
    attack_n = int(attack * sample_rate)
    decay_n = int(decay * sample_rate)
    release_n = int(release * sample_rate)

    t = torch.arange(num_samples, device=device, dtype=torch.float32)
    env = torch.zeros(num_samples, device=device)

    # Attack
    if attack_n > 0:
        env[:attack_n] = t[:attack_n].float() / attack_n
    # Decay
    decay_start = attack_n
    decay_end = attack_n + decay_n
    if decay_n > 0 and decay_end <= num_samples:
        env[decay_start:decay_end] = 1.0 - (t[decay_start:decay_end].float() - decay_start) / decay_n * (1.0 - sustain)
    # Sustain
    sus_start = decay_end
    sus_end = num_samples - release_n
    if sus_end > sus_start:
        env[sus_start:sus_end] = sustain
    # Release
    if release_n > 0:
        rel_start = num_samples - release_n
        env[rel_start:] = sustain * (1.0 - (t[rel_start:].float() - rel_start) / release_n)

    return env.clamp(0.0, 1.0)


def render_piece(
    duration: float = 30.0,
    num_voices: int = 64,
    sample_rate: float = 44100.0,
    output_path: str = "gpu_render_30s.wav",
    device: torch.device = DEVICE,
) -> str:
    """
    Render a 30-second piece with 64 voices using GPU-accelerated synthesis.

    Uses:
    - CUDA lattice oscillator for waveform generation
    - CUDA biquad bank for per-voice filtering
    - ADSR envelopes

    Returns path to saved WAV file.
    """
    print(f"\n{'#'*60}")
    print(f"  RENDERING {duration}s PIECE — {num_voices} voices @ {sample_rate}Hz")
    print(f"  Device: {device}")
    print(f"{'#'*60}")

    total_samples = int(duration * sample_rate)
    output = torch.zeros(total_samples, device=device, dtype=torch.float32)

    osc = CudaLatticeOscillator(device=device)
    bank = CudaBiquadBank(device=device)

    # Define a musical structure: chord progression with voice allocation
    # 4-bar pattern repeating (each bar ≈ 2s at 120 BPM)
    chord_progression = [
        [60, 64, 67],          # C major
        [62, 65, 69],          # Dm
        [64, 67, 71],          # Em
        [60, 65, 69, 72],      # C(add9)
    ]

    bar_duration = 2.0
    bar_samples = int(bar_duration * sample_rate)
    num_bars = int(duration / bar_duration)
    voices_per_chord = num_voices // len(chord_progression[0])

    # Spread voices across octaves for richness
    octave_offsets = [0, 12, -12, 24, -24, 7]

    start_event = torch.cuda.Event(enable_timing=True)
    end_event = torch.cuda.Event(enable_timing=True)
    start_event.record()

    for bar in range(num_bars):
        chord = chord_progression[bar % len(chord_progression)]
        bar_start = bar * bar_samples

        # For each chord tone, allocate voices
        all_freqs = []
        for i, tone in enumerate(chord):
            for v in range(voices_per_chord):
                oct_off = octave_offsets[v % len(octave_offsets)]
                detune = (v - voices_per_chord // 2) * 0.5  # slight detune for richness
                freq = midi_to_freq(tone + oct_off) * (1.0 + detune / 1000.0)
                all_freqs.append(freq)

        n_active = len(all_freqs)
        freqs_tensor = torch.tensor(all_freqs, device=device, dtype=torch.float32)

        # Generate waveforms (mix of shapes for texture)
        # First half: saw, second half: sine (leads vs pads)
        half = n_active // 2
        saw_freqs = freqs_tensor[:half]
        sin_freqs = freqs_tensor[half:]

        saw_signal = osc.generate_voices(saw_freqs, bar_samples, sample_rate, WaveformShape.Saw)
        sin_signal = osc.generate_voices(sin_freqs, bar_samples, sample_rate, WaveformShape.Sine)

        signal = torch.cat([saw_signal, sin_signal], dim=0)  # (n_active, bar_samples)

        # Apply per-voice biquad lowpass (different cutoffs for timbral variety)
        cutoffs = torch.linspace(800, 4000, n_active, device=device)
        qs = torch.full((n_active,), 1.5, device=device)
        b0, b1, b2, a1, a2 = bank.rbj_coefficients("lowpass", cutoffs, qs, sample_rate)
        filtered = bank.process(signal, b0, b1, b2, a1, a2)

        # ADSR envelope per voice
        env = generate_adsr_envelope(
            bar_samples, attack=0.05, decay=0.2, sustain=0.6, release=0.3,
            sample_rate=sample_rate, device=device
        )
        filtered = filtered * env.unsqueeze(0)  # broadcast

        # Mix down: simple sum with amplitude scaling
        mixed = filtered.sum(dim=0) / n_active * 0.8

        # Overwrite bar in output
        end_idx = min(bar_start + bar_samples, total_samples)
        actual_len = end_idx - bar_start
        output[bar_start:end_idx] = mixed[:actual_len]

        if (bar + 1) % 5 == 0:
            print(f"  Bar {bar+1}/{num_bars} rendered...")

    end_event.record()
    torch.cuda.synchronize()
    render_time = start_event.elapsed_time(end_event) / 1000.0

    print(f"  Render time: {render_time:.2f}s (real-time factor: {duration/render_time:.1f}x)")

    # Normalise to prevent clipping
    peak = output.abs().max()
    if peak > 0:
        output = output / peak * 0.9

    # Convert to 16-bit PCM and save WAV
    output_cpu = output.cpu()
    # Apply soft fade-out at end
    fade_samples = min(int(0.5 * sample_rate), total_samples)
    fade = torch.linspace(1.0, 0.0, fade_samples)
    output_cpu[-fade_samples:] *= fade

    pcm_data = (output_cpu * 32767).clamp(-32768, 32767).to(torch.int16).numpy()

    # Write WAV
    with wave.open(output_path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(int(sample_rate))
        wf.writeframes(pcm_data.tobytes())

    file_size = len(pcm_data) * 2
    print(f"  Saved: {output_path} ({file_size / 1e6:.1f} MB)")
    print(f"  Duration: {duration}s, Sample rate: {sample_rate}Hz, Voices: {num_voices}")

    return output_path


# ===================================================================
# MAIN
# ===================================================================

if __name__ == "__main__":
    import os

    print("GPU-Accelerated Constraint Audio Engine")
    print(f"PyTorch {torch.__version__}, CUDA {'available' if torch.cuda.is_available() else 'NOT available'}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    print()

    # Run benchmarks
    bench = Benchmark(device=DEVICE)
    results = bench.run_all()

    # Render 30-second piece
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gpu_render_30s.wav")
    render_piece(duration=30.0, num_voices=64, output_path=output_path, device=DEVICE)

    print("\n✅ All done!")
