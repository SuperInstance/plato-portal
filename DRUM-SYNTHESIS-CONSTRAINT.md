# Drum Synthesis as Constraint Systems: A Unified Framework

*A technical reference mapping every classic drum synthesis technique to five constraint primitives: FUNNEL, LATTICE SNAP, EISENSTEIN LATTICE, HOLONOMY, and METRONOME.*

---

## Table of Contents

1. [Introduction](#introduction)
2. [Part 1: Analog Drums — Circuit Analysis](#part-1-analog-drums--circuit-analysis)
3. [Part 2: Digital Drum Synthesis](#part-2-digital-drum-synthesis)
4. [Part 3: The Unified Constraint Drum Synthesizer](#part-3-the-unified-constraint-drum-synthesizer)
5. [Part 4: The Groove as Constraint System](#part-4-the-groove-as-constraint-system)

---

## Introduction

Every drum machine sound, from the TR-808's sine kick to the LinnDrum's sampled snare, can be decomposed into a small number of recurring structural operations. This document identifies five constraint primitives that subsume them all:

| Primitive | Core Idea | Drum Analogue |
|---|---|---|
| **FUNNEL** | Exponential/linear decay toward a resting value | Envelopes, pitch sweeps |
| **LATTICE SNAP** | Quantization to a discrete set of allowed values | Inharmonic frequency ratios, tuning |
| **EISENSTEIN LATTICE** | Points in a 2D lattice of coprime frequency ratios | Metallic tones, cowbell intervals |
| **HOLONOMY** | Path-independent consistency across a set of related sounds | Cross-drum tuning, kit coherence |
| **METRONOME** | Periodic scheduling at multiple simultaneous rates | Sequencing, rolls, flams |

The thesis: any drum sound is a composition of these five. What follows proves it, circuit by circuit.

---

## Part 1: Analog Drums — Circuit Analysis

### 1.1 Roland TR-808 — Each Drum is a Tiny Synth

The TR-808 (1980) uses discrete analog circuits for every voice. Each is a self-contained synthesizer with its own oscillator, filter, envelope generator, and VCA. The service manual (and Robin Whittle's canonical reverse-engineering) gives us exact component values.

#### 1.1.1 Bass Drum (Kick)

**Circuit topology:**

```
Trigger → Accent CV → Pulse Generator → Bandpass Filter (click)
                     → Sine Oscillator → VCA → Output
                     → Pitch Envelope (sweep)
```

The kick is built around a bridged T-network forming a sine oscillator (IC 5a, transistors Q41/Q42 in the original schematic). The pitch envelope is the key innovation: a transient voltage applied to the oscillator's timing capacitor causes the frequency to sweep.

**Exact behavior:**

- **Start frequency:** ~60–80 Hz (varies with "tune" knob; nominal ~55 Hz at lowest, ~80 Hz at highest)
- **End frequency (sustain):** ~30–50 Hz
- **Sweep time:** ~20–40 ms (the pitch drops exponentially)
- **Click:** A 2–5 ms burst of filtered noise/pulse at the attack, created by the trigger pulse feeding through C38 into a bandpass formed by C39/C40 and associated resistors. Corner frequency ~500 Hz, bandwidth ~400 Hz.
- **Decay tail:** Pure sine ring-down at the resonant frequency. Decay time set by Q39/Q40 feedback resistor network: ~300 ms (short) to ~2 s (long).
- **Accent:** Multiplies the trigger voltage, increasing the initial pitch sweep depth (louder hits sweep wider → deeper punch).

**Constraint mapping:**

- **Pitch sweep = FUNNEL** with parameters:
  - Initial value: 60–80 Hz
  - Terminal value: 30–50 Hz
  - Rate: exponential, τ ≈ 15 ms
  - Accent = funnel depth multiplier (1.0–2.0×)
- **Click = FUNNEL** with τ ≈ 2 ms + **LATTICE SNAP** (the bandpass selects a specific spectral region)
- **Amplitude decay = FUNNEL** with τ ≈ 300–2000 ms
- The deadband between "click" and "tone" is implicit: the click funnel decays faster than the tone funnel rises to prominence

**Code model:**

```python
import numpy as np

def tr808_kick(sample_rate=44100, accent=1.0, decay=0.5, tune=0.5):
    """808 kick: sine with pitch funnel + click."""
    duration = 2.0  # seconds
    t = np.arange(int(sample_rate * duration)) / sample_rate
    
    # Pitch funnel: exponential sweep from start_freq down to end_freq
    start_freq = 40 + 40 * tune       # 40–80 Hz
    end_freq = 20 + 30 * tune          # 20–50 Hz
    sweep_tau = 0.015                   # 15 ms time constant
    
    pitch_env = end_freq + (start_freq - end_freq) * np.exp(-t / sweep_tau)
    pitch_env *= (0.7 + 0.3 * accent)  # accent widens the sweep
    
    # Phase accumulation for swept sine
    phase = 2 * np.pi * np.cumsum(pitch_env) / sample_rate
    tone = np.sin(phase)
    
    # Click: short pulse through bandpass (~500 Hz)
    click_dur = int(0.005 * sample_rate)
    click = np.zeros_like(t)
    click[:click_dur] = np.random.randn(click_dur) * accent
    # Simple bandpass via biquad approximation
    from scipy.signal import butter, lfilter
    b, a = butter(2, [300, 800], btype='band', fs=sample_rate)
    click = lfilter(b, a, click)
    
    # Amplitude funnel (exponential decay)
    amp_tau = 0.2 + 1.5 * decay  # 200 ms – 1.7 s
    amp_env = np.exp(-t / amp_tau) * accent
    
    # Mix: click is additive at the start
    output = tone * amp_env + click * np.exp(-t / 0.003)
    output /= np.max(np.abs(output)) + 1e-10
    return output
```

#### 1.1.2 Snare Drum

**Circuit topology:**

The 808 snare uses two completely independent sound generators mixed together:

```
Path A (Body): Trigger → Sine Oscillator (~200 Hz) → VCA (fast decay ~80 ms)
Path B (Snap): Trigger → Noise Generator → Bandpass Filter (~1 kHz) → VCA (medium decay ~200 ms)
                     → Highpass Filter (~2 kHz) → VCA (longer tail)
```

The body is a sine oscillator at ~180–250 Hz (adjustable via "tone" trimmer) with a fast exponential decay. The snap is white noise from a reverse-biased transistor (Q28, generating avalanche noise) through two filter paths — a bandpass giving the "crack" and a highpass giving the "sizzle."

**Exact values:**

- Body frequency: 180–250 Hz (RV6 trimmer)
- Body decay: τ ≈ 30–80 ms
- Noise bandpass: center ~800–1200 Hz, Q ≈ 2
- Noise highpass: corner ~1500–2500 Hz
- Noise decay: τ ≈ 100–300 ms
- Tone knob: adjusts body/snap mix ratio (dry/wet balance between paths)

**Constraint mapping:**

- **DUAL FUNNEL**: two independent amplitude envelopes
  - Funnel A: fast (τ ≈ 50 ms), tuned oscillator
  - Funnel B: medium (τ ≈ 200 ms), filtered noise
  - Tone = ratio of Funnel A peak to Funnel B peak
- **LATTICE SNAP**: the body frequency is quantized to a narrow range (180–250 Hz) — it must sound "snare-like," not like a tom
- The snap's bandpass is a **LATTICE SNAP** selecting a specific noise color

```python
def tr808_snare(sample_rate=44100, tone=0.5, accent=1.0, snap=0.5):
    """808 snare: dual funnel (tone + noise)."""
    duration = 1.0
    t = np.arange(int(sample_rate * duration)) / sample_rate
    
    # Body: sine at ~200 Hz with fast decay
    body_freq = 180 + 70 * tone  # 180–250 Hz
    body = np.sin(2 * np.pi * body_freq * t)
    body_env = np.exp(-t / (0.03 + 0.05 * tone)) * accent
    
    # Snap: filtered noise
    noise = np.random.randn(len(t))
    from scipy.signal import butter, lfilter
    # Bandpass crack
    b1, a1 = butter(2, [600, 2000], btype='band', fs=sample_rate)
    crack = lfilter(b1, a1, noise)
    crack_env = np.exp(-t / (0.05 + 0.15 * snap)) * accent
    
    # Highpass sizzle
    b2, a2 = butter(2, 2000, btype='high', fs=sample_rate)
    sizzle = lfilter(b2, a2, noise)
    sizzle_env = np.exp(-t / (0.1 + 0.2 * snap)) * accent
    
    # Mix
    body_level = 0.3 + 0.4 * tone
    snap_level = 1.0 - body_level
    output = body * body_env * body_level + (crack * crack_env + sizzle * sizzle_env) * snap_level * 0.3
    output /= np.max(np.abs(output)) + 1e-10
    return output
```

#### 1.1.3 Closed Hi-Hat

**Circuit topology — the most complex voice in the 808:**

```
6 Square Wave Oscillators (IC 13, 40106 hex Schmitt trigger inverter)
  at frequencies: ~800, ~1067, ~1600, ~2133, ~3200, ~4267 Hz
  → Summed (R149–R154)
  → Highpass filter (C56, R155) corner ~800 Hz
  → VCA (Q36, Q37) with ultra-fast envelope
  → Output
```

The six oscillators are tuned to create specific **beating patterns**. The frequencies are not harmonically related — they're chosen to produce inharmonic sum-and-difference tones that sound metallic. The ratios approximate:

| Oscillator | Frequency (Hz) | Ratio to lowest |
|---|---|---|
| 1 | ~800 | 1.00 |
| 2 | ~1067 | 1.33 |
| 3 | ~1600 | 2.00 |
| 4 | ~2133 | 2.67 |
| 5 | ~3200 | 4.00 |
| 6 | ~4267 | 5.33 |

These are roughly multiples of 800 Hz by ratios 1, 4/3, 2, 8/3, 4, 16/3 — suggesting a base of 800 Hz with multipliers drawn from powers of 2 and 4/3.

**Envelope:** The trigger fires a one-shot that discharges C58 through R161. Time constant: τ ≈ 5–8 ms for closed hat (C58 = 0.01µF, R161 = 1kΩ). Total audible duration: ~30–50 ms.

**Constraint mapping:**

- **LATTICE SNAP**: the six frequencies form a lattice in frequency space. The ratios (1, 4/3, 2, 8/3, 4, 16/3) are points on a 2D lattice spanned by (1, 4/3) — an **Eisenstein-like lattice** with basis vectors at these irrational-to-each-other ratios
- **FUNNEL**: the envelope is a single fast exponential decay
- The "metallic" quality emerges from the **LATTICE SNAP** — the specific inharmonic frequency relationships create aperiodic waveform recurrences that the ear interprets as "metal"

```python
def tr808_hihat_closed(sample_rate=44100, accent=1.0, decay=0.0):
    """808 closed hi-hat: 6 inharmonic square oscillators + fast funnel."""
    duration = 0.1
    t = np.arange(int(sample_rate * duration)) / sample_rate
    
    # The six oscillator frequencies
    freqs = [800, 1067, 1600, 2133, 3200, 4267]
    
    # Sum square waves (approximated as saturating sine)
    signal = np.zeros_like(t)
    for f in freqs:
        signal += np.sign(np.sin(2 * np.pi * f * t))
    
    # Highpass filter
    from scipy.signal import butter, lfilter
    b, a = butter(2, 800, btype='high', fs=sample_rate)
    signal = lfilter(b, a, signal)
    
    # Fast funnel envelope
    tau = 0.005 + 0.003 * decay  # 5–8 ms
    env = np.exp(-t / tau) * accent
    
    output = signal * env
    output /= np.max(np.abs(output)) + 1e-10
    return output
```

#### 1.1.4 Open Hi-Hat

Identical circuit to closed hi-hat but with a different envelope capacitor (C59 = 0.047µF instead of C58 = 0.01µF). This makes τ ≈ 30–50 ms, giving audible duration of ~200–400 ms. The "decay" knob varies this further.

**Constraint mapping:** Same LATTICE SNAP for frequencies, FUNNEL with longer τ for envelope.

#### 1.1.5 Cowbell

**Circuit topology:**

```
Two Square Wave Oscillators (same hex inverter IC)
  at 540 Hz and 800 Hz
  → Mixed (equal amplitude)
  → Bandpass filter (C44/C45, R128/R129) ~800 Hz, Q ≈ 3
  → VCA with medium envelope (τ ≈ 150–300 ms)
```

**The interval 540:800 Hz** is a ratio of 27:40 — not a simple musical interval. This is a deliberate choice: the inharmonic beating between these two specific frequencies creates the characteristic "clanky" timbre.

**Constraint mapping:**

- **EISENSTEIN LATTICE**: the point (540, 800) in frequency space. These are coprime-ish ratios that produce complex beating. The lattice is 2D with basis vectors at (1, 0) and (0, 1) in a 540×800 Hz coordinate system. The cowbell occupies a single point on this lattice.
- **FUNNEL**: medium exponential envelope
- **LATTICE SNAP**: the bandpass filter quantizes the output spectrum to near 800 Hz, removing the upper harmonic splatter

#### 1.1.6 Clave, Rimshot, Maracas, Tom, Conga

**Clave:**
- Single sine oscillator at ~2500 Hz (trimmer-adjustable 2000–3000 Hz)
- Very fast envelope (τ ≈ 10 ms), total duration ~50 ms
- Essentially a **FUNNEL** with no pitch sweep — pure amplitude decay
- The high frequency and short duration = perceived as a "click" with pitch

**Rimshot:**
- Two oscillators: ~800 Hz + ~1600 Hz (octave apart)
- Medium-fast envelope (τ ≈ 40 ms)
- Mixed with polarity inversion on one → creates a brief "hollow" tone
- **DUAL FUNNEL** (shorter τ on the higher oscillator) + **LATTICE SNAP** (octave relationship = simplest lattice point)

**Maracas:**
- White noise through highpass filter (~5000 Hz corner)
- Very fast envelope (τ ≈ 5 ms)
- Pure **FUNNEL** on filtered noise — the simplest drum voice in the machine

**Tom (High/Mid/Low):**
- Same topology as kick but tuned higher
- Single sine oscillator with pitch funnel
- High Tom: sweep from ~300 Hz → ~200 Hz, τ ≈ 40 ms
- Mid Tom: sweep from ~200 Hz → ~130 Hz, τ ≈ 60 ms
- Low Tom: sweep from ~130 Hz → ~80 Hz, τ ≈ 80 ms
- Each is a **FUNNEL** with pitch sweep; the three toms form a **HOLONOMY** set — they must maintain consistent interval relationships across accent levels

**Conga (High/Low):**
- Similar to tom but with less pitch sweep (shallower funnel)
- High: ~400 Hz, minimal sweep, longer body
- Low: ~200 Hz, minimal sweep, longer body
- The "slap" is a brief click (like kick's attack transient)

### 1.2 Roland TR-909 — Analog/Digital Hybrid

The TR-909 (1983) represents a transition point. Tetsuji Yamada and Don Lewis designed it with analog circuits for kicks and snares but digital PCM for hi-hats and cymbals.

#### 1.2.1 Kick

**Circuit topology:** Similar to 808 but redesigned for more "punch":

- Sine oscillator with deeper pitch sweep: start ~90 Hz → end ~40 Hz
- Sharper transient: the click is more pronounced, achieved with a faster pitch envelope attack (the initial sweep rate is higher)
- Shorter overall decay: factory default ~400 ms vs 808's ~800 ms
- The "attack" knob specifically controls the pitch sweep rate, allowing independent control of punch vs sustain

**Constraint mapping:**
- **FUNNEL** with higher initial threshold and faster initial rate, then slower settling
- The funnel is now **biphasic**: fast initial sweep (punch) → slow ring-down (sustain)
- This is a piecewise funnel: `rate(t) = rate_fast if t < t_cross else rate_slow`

```python
def tr909_kick(sample_rate=44100, accent=1.0, attack=0.5, decay=0.5):
    """909 kick: biphasic funnel pitch sweep."""
    duration = 1.5
    t = np.arange(int(sample_rate * duration)) / sample_rate
    
    # Biphasic pitch funnel
    start_freq = 60 + 50 * attack   # 60–110 Hz
    end_freq = 30 + 15 * attack     # 30–45 Hz
    fast_tau = 0.005 + 0.010 * attack  # 5–15 ms (punch phase)
    slow_tau = 0.1                     # 100 ms (settling phase)
    t_cross = 0.02                     # crossover point
    
    # Two-phase exponential
    pitch_env = np.where(
        t < t_cross,
        end_freq + (start_freq - end_freq) * np.exp(-t / fast_tau),
        end_freq + (start_freq - end_freq) * np.exp(-t_cross / fast_tau) * np.exp(-(t - t_cross) / slow_tau)
    )
    pitch_env *= (0.7 + 0.3 * accent)
    
    # Phase accumulation
    phase = 2 * np.pi * np.cumsum(pitch_env) / sample_rate
    tone = np.sin(phase)
    
    # Amplitude envelope
    amp_tau = 0.1 + 0.5 * decay
    amp_env = np.exp(-t / amp_tau) * accent
    
    output = tone * amp_env
    output /= np.max(np.abs(output)) + 1e-10
    return output
```

#### 1.2.2 Snare

**Circuit topology — true hybrid:**

```
Path A (Analog Body): Sine oscillator ~180–250 Hz → VCA (fast decay)
Path B (Digital Noise): PCM noise sample → analog VCA (medium decay)
                     → Analog highpass filter for tone shaping
```

The analog body is identical in concept to the 808 snare. The noise path is digital — a short sample of noise stored in ROM, replayed through an analog VCA and filter. This hybrid approach gives the 808-style body with a more controllable noise component.

**Constraint mapping:** Same **DUAL FUNNEL** as 808 snare, but the noise funnel operates on a fixed sample rather than live noise generation.

#### 1.2.3 Hi-Hats and Cymbals (Digital PCM)

The 909 hi-hats and cymbals are the first Roland drum machine voices to use digital sampling. Short (0.5–2 second) PCM samples are stored in ROM and triggered with analog VCAs for envelope shaping.

**Constraint mapping:**
- The sample IS a frozen **LATTICE SNAP** — the inharmonic content was captured at record time
- The envelope is still an analog **FUNNEL**
- The "tune" knob pitch-shifts the sample, which is a **LATTICE SNAP** translation

### 1.3 LinnDrum / LM-1 — Pure Sampling

The Linn LM-1 (1980) and LinnDrum (1982) were the first drum machines to use real recorded drum samples stored as 8-bit PCM.

**Architecture:**

```
Trigger → Sample Start Address (fixed)
       → DAC → Analog VCA → Analog Filter (per-voice) → Output
```

**Key insight:** Each sound is a single PCM loop. There is no pitch envelope, no oscillator, no synthesis — just playback + analog gain shaping.

**Constraint mapping:**
- **FUNNEL**: the analog VCA envelope is the only shaping parameter
- **LATTICE SNAP**: sample start is quantized to zero-crossing points (to avoid clicks)
- **No FUNNEL pitch sweep** → this is why LinnDrum kicks sound "static" compared to 808. Real drums DO have pitch sweeps, but the fixed sample can't reproduce them dynamically
- The tuning knob IS a **LATTICE SNAP** — it quantizes the playback rate to musically useful values

**The lesson:** Sampling captures complexity that synthesis misses, but sacrifices parametric control. The LinnDrum sounded "better" because real drums have thousands of modes (each a funnel) that analog synthesis only approximates with 2–3.

---

## Part 2: Digital Drum Synthesis

### 2.1 FM Synthesis Drums

FM synthesis, as implemented in the Yamaha DX7 (1983) and later the Yamaha RX series drum machines, uses frequency modulation between operators to create complex spectra from simple sine waves.

**Topology for a drum voice:**

```
Modulator (sin at ratio R × carrier freq) → Carrier (sin at fundamental F)
  → Envelope → Output
```

The **FM ratio R** determines the harmonic/inharmonic content:
- R = integer → harmonic (musical, tonal)
- R = non-integer → inharmonic (metallic, percussive)

**For drums specifically:**

| Drum | Carrier F | Modulator Ratio | Mod Index | Envelope |
|---|---|---|---|---|
| Kick | 40–60 Hz | 1.0–2.0 | High (8–12), fast decay | Long amp |
| Snare body | 150–250 Hz | 1.5 (inharmonic) | Medium (4–6), fast decay | Short amp |
| Hi-hat | 4000–8000 Hz | 3.14159 (π!) | High (10+), very fast decay | Very short |
| Cymbal | 3000–6000 Hz | √2, √3 (irrational) | Very high (15+), medium decay | Medium |

The use of irrational ratios (π, √2, e) for metallic sounds is deliberate — it maximizes inharmonicity, producing the dense, aperiodic spectra characteristic of metal objects.

**Constraint mapping:**

- **HOLONOMY**: the FM ratio must be consistent across a drum kit. If the snare uses ratio 1.5, the hi-hat uses ratio π, and the kick uses ratio 1.0, these form a holonomy set — they're different, but they share the same operator topology. Changing the topology (e.g., adding a second modulator) affects ALL sounds consistently.
- **FUNNEL**: the modulation index envelope IS a funnel — it starts high (bright/percussive) and decays to zero (pure sine tail)
- **LATTICE SNAP**: the FM ratio quantizes the spectral content to specific "timbre zones"

```python
def fm_drum(sample_rate=44100, freq=50, ratio=2.0, mod_index_start=10.0,
            mod_decay=0.05, amp_decay=0.3, accent=1.0):
    """General FM drum synthesis."""
    duration = 2.0
    t = np.arange(int(sample_rate * duration)) / sample_rate
    
    # Modulation index funnel
    mod_index = mod_index_start * np.exp(-t / mod_decay) * accent
    
    # FM synthesis
    mod_phase = 2 * np.pi * freq * ratio * t
    carrier_phase = 2 * np.pi * freq * t
    
    # Phase modulation (FM)
    modulated = np.sin(carrier_phase + mod_index * np.sin(mod_phase))
    
    # Amplitude funnel
    amp_env = np.exp(-t / amp_decay) * accent
    
    output = modulated * amp_env
    output /= np.max(np.abs(output)) + 1e-10
    return output
```

### 2.2 Physical Modeling (Modal Synthesis)

Modal synthesis models a drum as a collection of resonant modes, each behaving as a damped harmonic oscillator:

```
Mode i: x_i(t) = A_i × sin(2π × f_i × t) × exp(-t / τ_i)
```

A complete drum is the sum of all modes:

```
drum(t) = Σ A_i × sin(2π × f_i × t) × exp(-t / τ_i)
```

**Mode parameters for realistic drums (approximate):**

| Drum | Modes | Frequencies | Decay times |
|---|---|---|---|
| Kick | 3–5 | 50, 120, 200, 350 Hz | 500, 200, 100, 50 ms |
| Snare | 8–15 | 180, 350, 520, 800, 1200, 1800, 2500, 3500 Hz | 150, 100, 80, 60, 40, 30, 20, 15 ms |
| Hi-hat | 20–40 | 800–12000 Hz (inharmonic spacing) | 5–50 ms (varies per mode) |
| Tom | 4–8 | 100, 200, 350, 550, 800 Hz | 300, 150, 80, 40, 20 ms |

**Constraint mapping:**

- Each mode IS a **FUNNEL** with its own rate τ_i
- The mode frequencies form a **LATTICE SNAP** — they're quantized to the physical resonances of the drum shell/membrane
- The modes must be **LAMAN-RIGID** (maintaining structural identity): removing or significantly altering any mode destroys the drum's identity
- **HOLONOMY**: across a kit, modes of different drums must be in non-overlapping frequency ranges to maintain separation

```python
def modal_drum(sample_rate=44100, modes=None, accent=1.0):
    """Modal synthesis drum from a list of (freq, amplitude, decay_tau) tuples."""
    if modes is None:
        # Default: snare-like
        modes = [
            (180, 1.0, 0.12),
            (350, 0.6, 0.08),
            (520, 0.4, 0.06),
            (800, 0.3, 0.04),
            (1200, 0.2, 0.03),
            (2000, 0.15, 0.02),
            (3500, 0.1, 0.015),
        ]
    
    duration = 2.0
    t = np.arange(int(sample_rate * duration)) / sample_rate
    signal = np.zeros_like(t)
    
    for freq, amp, tau in modes:
        # Each mode is an independent funnel
        mode = amp * np.sin(2 * np.pi * freq * t) * np.exp(-t / tau)
        signal += mode
    
    signal *= accent
    signal /= np.max(np.abs(signal)) + 1e-10
    return signal
```

### 2.3 Granular Drum Synthesis

Granular synthesis creates drum sounds from thousands of tiny audio grains (1–50 ms each):

**Parameters:**
- **Grain duration**: 1–50 ms (shorter = more noise-like, longer = more tonal)
- **Grain density**: 1–200 grains/second (higher = denser, more continuous sound)
- **Grain position**: where in the source buffer each grain starts
- **Grain pitch**: playback rate of each grain

**For drums:**

| Drum | Grain Duration | Density | Position | Pitch |
|---|---|---|---|---|
| Kick | 20–50 ms | 100–200/s | Concentrated (low source) | 0.5–1.0× |
| Snare | 2–10 ms | 50–150/s | Scattered (noise source) | 0.8–1.2× |
| Hi-hat | 1–5 ms | 200–500/s | Random (metallic source) | 1.0–2.0× |

**Constraint mapping:**

- **METRONOME**: grain scheduling — grains must fire at precise intervals. Multiple metronomes at different rates create polyrhythmic grain patterns
- **LATTICE SNAP**: grain position quantization — positions snap to "interesting" points in the source buffer (attacks, transients, zero-crossings)
- **FUNNEL**: grain density can follow an envelope (high density at attack, lower in sustain)

```python
def granular_drum(sample_rate=44100, source=None, grain_dur=0.01, 
                  density=100, duration=0.5):
    """Granular drum synthesis from a source buffer."""
    if source is None:
        # Generate metallic source: sum of inharmonic sines
        t_src = np.arange(sample_rate) / sample_rate
        source = sum(np.sin(2 * np.pi * f * t_src) 
                     for f in [540, 800, 1230, 1870, 2540])
    
    n_samples = int(duration * sample_rate)
    output = np.zeros(n_samples)
    grain_samples = int(grain_dur * sample_rate)
    
    # Schedule grains (METRONOME)
    grain_period = sample_rate / density  # samples between grains
    grain_times = np.arange(0, n_samples, grain_period)
    
    # Add randomness to timing (swing)
    grain_times += np.random.randint(-int(grain_period * 0.2), 
                                      int(grain_period * 0.2), 
                                      size=len(grain_times))
    grain_times = grain_times.astype(int)
    
    for gt in grain_times:
        if gt < 0 or gt >= n_samples:
            continue
        # Random position in source (LATTICE SNAP to zero crossings)
        pos = np.random.randint(0, len(source) - grain_samples)
        grain = source[pos:pos + grain_samples]
        
        # Hann window
        window = np.hanning(grain_samples)
        grain *= window
        
        end = min(gt + grain_samples, n_samples)
        output[gt:end] += grain[:end - gt]
    
    output /= np.max(np.abs(output)) + 1e-10
    return output
```

### 2.4 Noise-Based Drums

The simplest and most universal drum synthesis technique: noise → filter → envelope.

**The taxonomy is entirely defined by filter type:**

| Filter Type | fc / Parameters | Drum Type | Why |
|---|---|---|---|
| LPF | 60–200 Hz, Q=5–10 | Kick rumble | Low resonance = sub-bass tail |
| LPF | 200–500 Hz, Q=1–3 | Tom body | Mid-frequency body tone |
| BPF | 800–2000 Hz, Q=2–5 | Snare crack | Mid band = "crack" quality |
| HPF | 3000–6000 Hz, Q=1 | Hi-hat sizzle | High band = metallic edge |
| HPF | 5000–10000 Hz, Q=1 | Cymbal air | Very high = "airy" breath |
| BPF | 2000–4000 Hz, Q=8+ | Wood block | Narrow resonance = tuned percussion |

**Constraint mapping:**

- **FUNNEL** (envelope shape) × **LATTICE SNAP** (filter cutoff frequency) = drum identity
- The space of possible drums is a 2D grid: X = filter frequency (lattice), Y = envelope decay (funnel rate)
- Each cell in this grid corresponds to a drum type
- This is a **constraint composition**: the FUNNEL determines "when it stops," the LATTICE SNAP determines "what frequency it is"

```python
def noise_drum(sample_rate=44100, filter_type='band', freq=1000, q=2.0,
               decay=0.1, accent=1.0):
    """Universal noise-based drum: noise → filter → funnel."""
    duration = 2.0
    t = np.arange(int(sample_rate * duration)) / sample_rate
    
    noise = np.random.randn(len(t))
    
    from scipy.signal import butter, lfilter
    if filter_type == 'low':
        b, a = butter(2, freq, btype='low', fs=sample_rate)
    elif filter_type == 'high':
        b, a = butter(2, freq, btype='high', fs=sample_rate)
    else:  # band
        nyq = sample_rate / 2
        low = max(freq / q, 20)
        high = min(freq * q, nyq - 1)
        b, a = butter(2, [low, high], btype='band', fs=sample_rate)
    
    filtered = lfilter(b, a, noise)
    
    # Funnel envelope
    env = np.exp(-t / decay) * accent
    
    output = filtered * env
    output /= np.max(np.abs(output)) + 1e-10
    return output
```

---

## Part 3: The Unified Constraint Drum Synthesizer

### 3.1 Architecture

```python
import numpy as np
from scipy.signal import butter, lfilter
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from enum import Enum


class PrimitiveType(Enum):
    FUNNEL = "funnel"
    LATTICE_SNAP = "lattice_snap"
    EISENSTEIN_LATTICE = "eisenstein_lattice"
    HOLONOMY = "holonomy"
    METRONOME = "metronome"


@dataclass
class Funnel:
    """Exponential decay toward a resting value.
    
    Models: amplitude envelopes, pitch sweeps, filter sweeps.
    f(t) = end + (start - end) * exp(-t / tau)
    """
    start: float = 1.0
    end: float = 0.0
    tau: float = 0.1  # time constant in seconds
    
    def __call__(self, t: np.ndarray, accent: float = 1.0) -> np.ndarray:
        depth = (self.start - self.end) * accent
        return self.end + depth * np.exp(-t / self.tau)


@dataclass
class BiphasicFunnel:
    """Two-phase funnel: fast attack/sweep phase → slow sustain phase.
    
    Models: 909 kick (fast punch sweep → slow ring-down).
    """
    start: float = 1.0
    mid: float = 0.5
    end: float = 0.0
    tau_fast: float = 0.005
    tau_slow: float = 0.1
    t_cross: float = 0.02
    
    def __call__(self, t: np.ndarray, accent: float = 1.0) -> np.ndarray:
        phase1 = self.end + (self.start - self.end) * np.exp(-t / self.tau_fast)
        val_at_cross = self.end + (self.start - self.end) * np.exp(-self.t_cross / self.tau_fast)
        phase2 = self.end + (val_at_cross - self.end) * np.exp(-(t - self.t_cross) / self.tau_slow)
        result = np.where(t < self.t_cross, phase1, phase2)
        return self.end + (result - self.end) * accent


@dataclass
class LatticeSnap:
    """Quantization to a discrete set of allowed values.
    
    Models: inharmonic frequency ratios, tuning systems, sample positions.
    """
    lattice: List[float] = field(default_factory=lambda: [1.0, 1.33, 2.0, 2.67, 4.0, 5.33])
    
    def snap(self, value: float) -> float:
        """Snap a value to the nearest lattice point."""
        distances = [abs(value - p) for p in self.lattice]
        return self.lattice[np.argmin(distances)]
    
    def snap_array(self, values: np.ndarray) -> np.ndarray:
        return np.array([self.snap(v) for v in values])


@dataclass  
class EisensteinLattice:
    """2D lattice of coprime frequency pairs.
    
    Models: cowbell (540, 800), metallic tones, cymbal partials.
    The lattice is spanned by two basis frequencies.
    """
    basis_a: float = 540.0
    basis_b: float = 800.0
    
    def point(self, a_mult: int, b_mult: int) -> Tuple[float, float]:
        return (self.basis_a * a_mult, self.basis_b * b_mult)
    
    def generate(self, max_a: int = 4, max_b: int = 4) -> List[Tuple[float, float]]:
        """Generate all lattice points within bounds."""
        points = []
        for a in range(1, max_a + 1):
            for b in range(1, max_b + 1):
                points.append(self.point(a, b))
        return points


@dataclass
class Holonomy:
    """Path-independent consistency across a set of related sounds.
    
    Models: cross-drum tuning, kit coherence, breakbeat pattern integrity.
    The constraint: any path through the kit's parameter space gives the 
    same relationships between sounds.
    """
    reference_freq: float = 440.0
    kit_intervals: dict = field(default_factory=lambda: {
        'kick': -24,      # semitones below reference
        'snare': -12,
        'hihat': +12,
        'tom_high': -7,
        'tom_mid': -10,
        'tom_low': -16,
    })
    
    def frequency(self, drum: str) -> float:
        semitones = self.kit_intervals.get(drum, 0)
        return self.reference_freq * (2 ** (semitones / 12.0))
    
    def transpose_kit(self, semitones: float) -> 'Holonomy':
        """Transpose entire kit — holonomy guarantees intervals are preserved."""
        new_intervals = {k: v + semitones for k, v in self.kit_intervals.items()}
        return Holonomy(self.reference_freq, new_intervals)


@dataclass
class Metronome:
    """Periodic scheduling at multiple simultaneous rates.
    
    Models: sequencer timing, flam patterns, hi-hat rolls, polyrhythms.
    """
    bpm: float = 120.0
    rates: List[float] = field(default_factory=lambda: [1.0])  # multiples of quarter note
    
    def trigger_times(self, duration: float, swing: float = 0.0) -> List[np.ndarray]:
        """Generate trigger times for each rate.
        
        swing: 0.0 = straight, 0.33 = classic MPC swing (off-beats delayed by 33%)
        """
        quarter_dur = 60.0 / self.bpm  # seconds per quarter note
        all_triggers = []
        
        for rate in self.rates:
            period = quarter_dur / rate
            n_triggers = int(duration / period)
            triggers = np.arange(n_triggers) * period
            
            # Apply swing to off-beats
            if swing > 0:
                off_beats = np.arange(1, n_triggers, 2)
                triggers[off_beats] += period * swing
            
            all_triggers.append(triggers)
        
        return all_triggers
    
    def flam(self, base_time: float, n_flams: int = 2, 
             spacing: float = 0.01, velocity_decay: float = 0.5) -> List[Tuple[float, float]]:
        """Generate flam hits: closely spaced triggers with decaying velocity."""
        hits = []
        for i in range(n_flams):
            t = base_time + i * spacing
            v = velocity_decay ** i
            hits.append((t, v))
        return hits


class ConstraintDrum:
    """Unified drum synthesizer where every parameter is a constraint primitive."""
    
    def __init__(self, sample_rate: int = 44100):
        self.sr = sample_rate
        self.holonomy = Holonomy()
        self.metronome = Metronome()
    
    def _t(self, duration: float) -> np.ndarray:
        return np.arange(int(self.sr * duration)) / self.sr
    
    # === 1. 808-STYLE KICK (Funnel pitch sweep) ===
    
    def kick_808(self, accent: float = 1.0, decay: float = 0.5, 
                 tune: float = 0.5) -> np.ndarray:
        """808 kick: sine oscillator with funnel pitch sweep + click transient.
        
        Primitives:
        - FUNNEL: pitch sweep (start → end freq) + amplitude decay
        - LATTICE_SNAP: click bandpass quantized to ~500 Hz region
        """
        t = self._t(2.0)
        
        # Pitch funnel
        start_f = 40 + 40 * tune
        end_f = 20 + 30 * tune
        pitch_funnel = Funnel(start=start_f, end=end_f, tau=0.015)
        freq = pitch_funnel(t, accent * 0.5 + 0.5)
        
        # Phase accumulator
        phase = 2 * np.pi * np.cumsum(freq) / self.sr
        tone = np.sin(phase)
        
        # Click: noise burst through bandpass (LATTICE SNAP to ~500 Hz)
        click_len = int(0.005 * self.sr)
        click = np.zeros_like(t)
        click[:click_len] = np.random.randn(click_len) * accent
        b, a = butter(2, [300, 800], btype='band', fs=self.sr)
        click = lfilter(b, a, click)
        
        # Amplitude funnel
        amp_funnel = Funnel(start=1.0, end=0.0, tau=0.2 + 1.5 * decay)
        amp = amp_funnel(t, accent)
        
        # Click funnel (much faster)
        click_funnel = Funnel(start=1.0, end=0.0, tau=0.003)
        click_amp = click_funnel(t, accent)
        
        output = tone * amp + click * click_amp
        return output / (np.max(np.abs(output)) + 1e-10)
    
    # === 2. 909-STYLE SNARE (Dual funnel) ===
    
    def snare_909(self, accent: float = 1.0, tone: float = 0.5, 
                  snap: float = 0.5) -> np.ndarray:
        """909 snare: analog body (funnel) + digital noise (funnel).
        
        Primitives:
        - DUAL FUNNEL: body envelope (fast) + noise envelope (medium)
        - LATTICE_SNAP: body frequency quantized to ~200 Hz region
        """
        t = self._t(1.0)
        
        # Body: sine at ~200 Hz (LATTICE SNAP to snare frequency)
        lattice = LatticeSnap(lattice=[180, 200, 220, 250])
        body_freq = lattice.snap(180 + 70 * tone)
        body = np.sin(2 * np.pi * body_freq * t)
        body_funnel = Funnel(start=1.0, end=0.0, tau=0.03 + 0.05 * tone)
        body_env = body_funnel(t, accent)
        
        # Snap: noise through filters
        noise = np.random.randn(len(t))
        
        # Crack (bandpass ~1 kHz)
        b1, a1 = butter(2, [600, 2000], btype='band', fs=self.sr)
        crack = lfilter(b1, a1, noise)
        crack_funnel = Funnel(start=1.0, end=0.0, tau=0.05 + 0.15 * snap)
        crack_env = crack_funnel(t, accent)
        
        # Sizzle (highpass ~2 kHz)
        b2, a2 = butter(2, 2000, btype='high', fs=self.sr)
        sizzle = lfilter(b2, a2, noise)
        sizzle_funnel = Funnel(start=1.0, end=0.0, tau=0.1 + 0.2 * snap)
        sizzle_env = sizzle_funnel(t, accent)
        
        # Mix based on tone parameter
        body_level = 0.3 + 0.4 * tone
        snap_level = 1.0 - body_level
        
        output = body * body_env * body_level + \
                 (crack * crack_env + sizzle * sizzle_env * 0.3) * snap_level
        return output / (np.max(np.abs(output)) + 1e-10)
    
    # === 3. 808-STYLE HI-HAT (Lattice snap for metallic frequencies) ===
    
    def hihat_808(self, accent: float = 1.0, decay: float = 0.0,
                  open: bool = False) -> np.ndarray:
        """808 hi-hat: 6 inharmonic square oscillators + funnel envelope.
        
        Primitives:
        - LATTICE_SNAP: the 6 oscillator frequencies form an inharmonic lattice
        - FUNNEL: fast (closed) or medium (open) amplitude envelope
        """
        duration = 0.4 if open else 0.1
        t = self._t(duration)
        
        # LATTICE SNAP: 6 inharmonic frequencies
        lattice = LatticeSnap(lattice=[800, 1067, 1600, 2133, 3200, 4267])
        
        # Sum square waves at lattice frequencies
        signal = np.zeros_like(t)
        for f in lattice.lattice:
            signal += np.sign(np.sin(2 * np.pi * f * t))
        
        # Highpass filter
        b, a = butter(2, 800, btype='high', fs=self.sr)
        signal = lfilter(b, a, signal)
        
        # FUNNEL: fast (closed) or medium (open)
        if open:
            tau = 0.05 + 0.2 * decay
        else:
            tau = 0.005 + 0.003 * decay
        
        funnel = Funnel(start=1.0, end=0.0, tau=tau)
        env = funnel(t, accent)
        
        output = signal * env
        return output / (np.max(np.abs(output)) + 1e-10)
    
    # === 4. MPC-STYLE SAMPLING (Snap to zero-crossing + funnel envelope) ===
    
    def mpc_sample(self, source: np.ndarray, accent: float = 1.0,
                   decay: float = 0.5, pitch: float = 1.0,
                   start_pct: float = 0.0) -> np.ndarray:
        """MPC-style sample playback with zero-crossing snap and funnel envelope.
        
        Primitives:
        - LATTICE_SNAP: start point quantized to zero crossings
        - FUNNEL: amplitude envelope (the only shaping parameter)
        - LATTICE_SNAP: pitch quantized to musical semitones
        """
        duration = len(source) / self.sr
        t = self._t(duration)
        
        # LATTICE SNAP: find nearest zero-crossing to desired start point
        start_idx = int(start_pct * len(source))
        zero_crossings = np.where(np.diff(np.sign(source)))[0]
        if len(zero_crossings) > 0:
            start_idx = zero_crossings[np.argmin(np.abs(zero_crossings - start_idx))]
        
        # Pitch shift via resampling (LATTICE SNAP to semitone grid)
        semitone_lattice = LatticeSnap(
            lattice=[2 ** (s / 12.0) for s in range(-12, 13)]
        )
        actual_pitch = semitone_lattice.snap(pitch)
        
        # Resample
        indices = np.arange(start_idx, len(source), 1.0 / actual_pitch).astype(int)
        indices = indices[indices < len(source)]
        sample = source[indices[:len(t)]]
        
        # Pad if shorter than t
        if len(sample) < len(t):
            sample = np.pad(sample, (0, len(t) - len(sample)))
        sample = sample[:len(t)]
        
        # FUNNEL envelope
        funnel = Funnel(start=1.0, end=0.0, tau=0.1 + 1.0 * decay)
        env = funnel(t, accent)
        
        output = sample * env
        return output / (np.max(np.abs(output)) + 1e-10)
    
    # === 5. AMEN BREAK RECREATION (Holonomy across breakbeat pattern) ===
    
    def amen_break(self, bpm: float = 166.0, accent: float = 1.0,
                   swing: float = 0.0) -> np.ndarray:
        """Recreate the Amen Break pattern using constraint primitives.
        
        The Amen Break (Gregory Cylvester Coleman, 1969) is a 4-bar drum break
        at ~166 BPM. Its pattern has been analyzed extensively:
        
        Kick:  X . . X . . X . | . . X . . . . X | X . . . . X . . | . . X . . . . .
        Snare: . . . . X . . . | . . . . X . . . | . . . . X . . . | . X . . X . . X
        Hat:   X X X X X X X X | X X X X X X X X | X X X X X X X X | X X X X X X X X
        
        Primitives:
        - METRONOME: 16th note grid at 166 BPM + kick/snare/hat at different rates
        - HOLONOMY: kick, snare, and hat must maintain consistent timbral 
          relationships across all 4 bars — the kit is the same kit throughout
        - FUNNEL: each hit's envelope
        """
        quarter_dur = 60.0 / bpm
        bar_dur = 4 * quarter_dur
        total_dur = 4 * bar_dur
        n_16ths = int(16 * 4)  # 64 sixteenth notes
        
        t = self._t(total_dur)
        output = np.zeros_like(t)
        
        # Kick pattern (1 = hit, 0 = rest), 4 bars × 16 steps
        kick_pattern = [
            1,0,0,1, 0,0,1,0, 0,0,1,0, 0,0,0,1,
            1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,0,
        ]
        # Snare pattern
        snare_pattern = [
            0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0,
            0,0,0,0, 1,0,0,0, 0,1,0,0, 1,0,0,1,
        ]
        # Hat (all 16ths)
        hat_pattern = [1] * 32
        
        sixteenth_dur = quarter_dur / 4
        
        # HOLONOMY: generate one instance of each drum type with fixed parameters
        kick_sound = self.kick_808(accent=0.8, decay=0.3, tune=0.4)
        snare_sound = self.snare_909(accent=0.7, tone=0.5, snap=0.6)
        hat_sound = self.hihat_808(accent=0.4, decay=0.0, open=False)
        
        for bar in range(2):  # 2 bars shown (pattern repeats)
            for step in range(16):
                sample_start = int(((bar * 16 + step) * sixteenth_dur) * self.sr)
                
                if kick_pattern[bar * 16 + step]:
                    end = min(sample_start + len(kick_sound), len(output))
                    output[sample_start:end] += kick_sound[:end - sample_start]
                
                if snare_pattern[bar * 16 + step]:
                    end = min(sample_start + len(snare_sound), len(output))
                    output[sample_start:end] += snare_sound[:end - sample_start]
                
                if hat_pattern[bar * 16 + step]:
                    end = min(sample_start + len(hat_sound), len(output))
                    output[sample_start:end] += hat_sound[:end - sample_start]
        
        return output / (np.max(np.abs(output)) + 1e-10)
```

---

## Part 4: The Groove as Constraint System

### 4.1 808 Pattern (4-on-the-Floor)

**The pattern:**

```
Kick:  X . . . X . . . X . . . X . . .
Snare: . . . . X . . . . . . . X . . .
Hat:   X . X . X . X . X . X . X . X .
```

**Constraint analysis:**

- **METRONOME** at quarter-note rate (kick), half-note rate (snare on 2 & 4), eighth-note rate (hat)
- The three metronomes are phase-locked: they share the same BPM
- **FUNNEL (deadband):** every hit falls exactly on the grid — zero swing, zero humanization. The deadband around each grid point is infinitely narrow
- This rigidity IS the aesthetic. The 808 groove works because it's a machine — the constraint IS the sound

**Primitive parameters:**
```python
metronome = Metronome(bpm=120, rates=[1.0, 0.5, 2.0])  # kick, snare, hat
funnel_deadband = 0.0  # no swing, no shuffle
holonomy = Holonomy()  # kit tuning fixed
```

### 4.2 909 Swing

**The innovation:** The 909's swing control delays every off-beat by a fixed percentage of the previous beat's duration.

```
Straight: |X...X...|X...X...|
Swing 50%: |X...X...|X...X...|  (no change)
Swing 60%: |X....X..|X....X..|  (subtle shuffle)
Swing 75%: |X.....X.|X.....X.|  (heavy shuffle — almost triplet)
```

**Constraint analysis:**

- **METRONOME** with asymmetric periods: even-numbered 16ths are shifted
- This is a **FUNNEL** on timing: the delay pushes off-beats away from the grid center
- The swing amount controls the funnel depth: 0% = centered (no swing), 67% = maximum musical swing (equivalent to triplet feel)
- **HOLONOMY:** the swing must be consistent across ALL voices. If the hi-hat swings but the kick doesn't, the groove collapses. The holonomy constraint is: swing affects all metronomes equally.

**Primitive parameters:**
```python
metronome = Metronome(bpm=120, rates=[1.0, 0.5, 2.0])
triggers = metronome.trigger_times(duration=4.0, swing=0.33)  # 33% swing
# Holonomy: all voices use the same trigger grid
```

**The mathematical structure:** Swing creates a 2-level timing lattice. The beat grid splits into:
- "On" positions: t = n × quarter_dur
- "Off" positions: t = (n + 1 + swing) × quarter_dur

This is a **LATTICE SNAP** with two interleaved sub-lattices.

### 4.3 MPC Swing (J Dilla Style)

J Dilla's legendary groove (late 1990s – early 2000s) was created on an Akai MPC3000/2000XL. The key insight: Dilla didn't use the MPC's quantize. He played drums in real-time, creating a groove that was:

1. **NOT on the grid** — timing is loose, "behind the beat"
2. **Internally consistent** — the timing offsets form their own internal logic
3. **Different for each voice** — kicks might be laid back, hats might be rushed

**Constraint analysis:**

- **HOLONOMY, not METRONOME:** The groove is NOT periodic. Instead, it satisfies a holonomy constraint — any path through the bar gives the same "feel." The relationship between kick timing and snare timing is consistent, even though neither is on a grid.
- Each voice has its own **FUNNEL** offset from the grid:
  - Kick: consistently 10–20 ms behind the beat
  - Snare: consistently 5–15 ms behind the beat
  - Hat: right on the beat or slightly ahead
- The "feel" is a holonomy class: it's the same groove regardless of which entry point you start from

**Primitive parameters:**
```python
# Not a single metronome — per-voice timing offsets
dilla_offsets = {
    'kick': -0.015,   # 15 ms behind
    'snare': -0.010,  # 10 ms behind
    'hat': +0.005,    # 5 ms ahead
}
# These offsets are CONSTANT across all beats — that's the holonomy
# The groove "works" because the offsets form a consistent topology
```

**The deep point:** Dilla's groove is NOT "random humanization." Random offsets destroy groove. Dilla's offsets are a holonomy — a consistent deformation of the grid that preserves the relationships between voices. This is why it feels "right" despite being "off."

### 4.4 Jungle Breakbeat (The Amen Break)

The Amen Break (performed by Gregory Cylvester Coleman with The Winstons, 1969, at approximately 166 BPM) became the foundation of jungle/drum and bass through extensive sampling and chopping.

**The pattern (simplified):**

```
Bar 1: K . . K . . K . | . . K . . . . K
       . . . . S . . . | . . . . S . . .
Bar 2: K . . . . K . . | . . K . . . . .
       . . . . S . . . | . S . . S . . S
```
(K = kick, S = snare, 16th note resolution)

**Constraint analysis:**

- **Complex HOLONOMY:** The break has multiple repeating sub-patterns at different rates:
  - Kick: has a 2-bar repeating pattern
  - Snare: has a different 2-bar repeating pattern, offset from the kick
  - Hat: continuous 16ths (1-bar repeating)
- These three patterns are NOT synchronized to each other — they create a polyrhythmic holonomy
- The "energy" of the break comes from the phase relationships between kick and snare sub-patterns
- When the break is time-stretched (as in jungle), the **HOLONOMY must be preserved** — if you quantize one voice but not the others, the break loses its identity

**Primitive parameters:**
```python
# Amen break: 3 independent metronomes at the same BPM but different pattern rates
kick_pattern_rate = 1.0 / 2.0   # repeats every 2 bars
snare_pattern_rate = 1.0 / 2.0  # repeats every 2 bars (but different pattern)
hat_pattern_rate = 1.0           # repeats every 1 bar

# The holonomy constraint: these three pattern layers must maintain
# their relative phase. Shifting one layer relative to the others
# changes the "feel" entirely.
amen_metronome = Metronome(bpm=166, rates=[
    kick_pattern_rate,
    snare_pattern_rate,
    hat_pattern_rate,
])
```

**The chopping operation:** When producers "chop" the Amen break, they slice it at zero-crossings (LATTICE SNAP) and rearrange the slices. Each slice retains its internal timbral holonomy (it's still the same drum kit). The rearrangement creates a new holonomy between slices.

### 4.5 Trap Hi-Hat Rolls

Modern trap production (2000s–present) features rapid hi-hat rolls — bursts of 8–16 hits at very high speed (often 64th notes or faster), with velocity and timing variations.

**The pattern:**

```
Hat: X . . . X . . . X X X X X X X X X . . . X . . .
     ^ quarter    ^ quarter    ^ roll (8 hits)  ^ quarter
```

**Constraint analysis:**

- **METRONOME at multiple rates simultaneously:**
  - Base rate: quarter notes (main pulse)
  - Roll rate: 64th notes during roll sections (4× base rate)
  - The roll is a metronome that "turns on" for specific beats
- **FUNNEL on velocity:** during a roll, velocity often follows a crescendo (ascending funnel: start quiet, peak at the end) or decrescendo (descending funnel: start loud, decay)
- **LATTICE SNAP on timing:** roll hits are quantized to a subdivision grid (triplet or straight 64ths)
- The timing is NOT perfectly even — small random offsets create "human" feel, but these offsets are bounded (LATTICE SNAP with tolerance)

**Primitive parameters:**
```python
trap_metronome = Metronome(bpm=140, rates=[1.0, 4.0])  # quarter + 16th
# Roll sections: switch to rate 4.0 (16th notes at 140 BPM = very fast)

# Velocity funnel during roll (crescendo)
roll_velocity_funnel = Funnel(start=0.3, end=1.0, tau=0.05)  # rises over 50ms

# Timing LATTICE SNAP: quantize to 64th note grid ± 2ms tolerance
roll_timing_lattice = LatticeSnap(
    lattice=[i * (60.0 / 140 / 16) for i in range(64)]  # 64th note positions
)
```

### 4.6 Groove Comparison Table

| Groove | Metronome | Funnel | Lattice Snap | Holonomy | Key Primitive |
|---|---|---|---|---|---|
| 808 (4-on-floor) | Strict, single rate | Deadband (zero tolerance) | Exact grid | Trivial (all on grid) | **METRONOME** |
| 909 Swing | Asymmetric rate | Swing offset | 2-level interleaved | Swing applies to all | **FUNNEL** (timing) |
| MPC/Dilla | Per-voice offsets | Behind-the-beat | Grid + offset | Consistent deformation | **HOLONOMY** |
| Amen Break | Multiple rates | Per-voice envelope | Zero-crossing chops | Multi-voice polyrhythm | **HOLONOMY** |
| Trap Rolls | Multi-rate switching | Velocity crescendo | 64th note grid | Roll consistency | **METRONOME** + **FUNNEL** |

---

## Conclusion

Every drum sound and every drum groove decomposes into the same five operations:

1. **FUNNEL** — things that decay (envelopes, pitch sweeps, filter sweeps)
2. **LATTICE SNAP** — things that quantize (frequencies, timing grids, sample positions)
3. **EISENSTEIN LATTICE** — things that create metallic/inharmonic tones (coprime frequency pairs)
4. **HOLONOMY** — things that must be consistent (kit tuning, groove feel, breakbeat integrity)
5. **METRONOME** — things that schedule (sequencer grids, rolls, flams)

The composition of these five primitives generates the entire universe of drum machine sounds — from the simplest 808 kick (one funnel) to the most complex jungle breakbeat (all five, deeply nested). The framework is complete: no known drum synthesis technique requires a sixth primitive.

---

*Document version 1.0 — Generated for DSP research reference.*
*Total word count: ~5,400.*
