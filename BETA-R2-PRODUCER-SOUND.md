# BETA-R2-PRODUCER-SOUND: Audio Quality Re-Test

**Tester:** Audio Quality Re-Tester (Round 2)  
**Date:** 2026-05-22  
**Previous score:** 4/10  
**Verdict:** The imports are fixed. The pipeline runs. The audio is technically valid. The sound design is still a **tutorial oscillator**.

---

## 1. Pipeline Status: ✅ WORKS

All components render without errors:

- **Full pipeline demo** → 8.0s WAV, counterpoint → harmony → groove → smoothing → rooms → style → audio
- **5 synth presets** → each 1.6s WAV
- **Jazz voicing engine** → Autumn Leaves arrangement, 8 bars, walking bass + comping
- **Fugue (existing)** → 28.7s D minor fugue, 4 voices

No crashes. No import errors. The flux_tensor_midi imports are fixed. ✅

---

## 2. Honest Preset Evaluation

### "Bach Organ" — Score: 2/10
- **Waveform:** Triangle wave. That's it. A single triangle oscillator.
- **Does it sound like an organ?** No. An organ has sustained tone with multiple harmonic ranks (mixtures), percussion, and a gradual swell. This is a triangle wave with a sustain envelope.
- **What's missing:** Drawbar simulation (multiple sine/triangle layers at harmonic intervals), rotary speaker effect (slow LFO modulation), key click, percussive attack transient, reverb.

### "Joplin Piano" — Score: 3/10
- **Waveform:** Eisenstein snap (7-level quantization) + stretch=1.002. 
- **Does it sound like a piano?** Barely recognizable. The inharmonicity parameter is a nice touch (piano strings ARE inharmonic), but a single quantized oscillator at 7 levels sounds like a broken kazoo, not a piano.
- **What's missing:** Multi-strike samples or at minimum a complex harmonic series, hammer noise transient, string resonance (sympathetic vibrations from undamped strings), sustain pedal simulation, damper release noise.

### "Debussy Pad" — Score: 4/10
- **Waveform:** Sine + stretch=1.001 + slow ADSR (attack=0.8s, release=1.2s).
- **Does it sound like a pad?** Sort of! This is the most successful preset because pads are the most forgiving — a slow-attacking sine wave is actually pad-like. The consonance filter adds subtle movement.
- **What's missing:** Chorus (detuned copies), multiple oscillator layers, LFO modulation (PWM, filter sweep), reverb tail, stereo width.
- **Note:** This preset clips (18 samples at full scale). The slow attack means the peak detection in the envelope math can create near-full-scale samples.

### "Coltrane Sax" — Score: 2/10
- **Waveform:** Sawtooth + noise_floor=0.15.
- **Does it sound like a sax?** No. A sawtooth with noise is the universal "beginner synth brass" sound. 475 detected click artifacts — the sawtooth discontinuity is not band-limited, causing audible clicks at the waveform reset point.
- **What's missing:** Formant filtering (the spectral envelope of a sax is its signature), breath noise modulated by dynamics, growl (subharmonic modulation), microtonal pitch inflections, dynamic timbral change (brighter at louder dynamics).

### "Aphex Glitch" — Score: 3/10
- **Waveform:** Eisenstein + noise=0.4 + short envelope.
- **Does it sound like glitch?** It sounds like noise bursts, which is in the neighborhood. The eisenstein quantization adds some digital artifacts. But glitch music is about *rhythmic* complexity, not just noise.
- **What's missing:** Granular synthesis, beat-synced parameter changes, bitcrushing, ring modulation, stutter/repeat, rhythmic gating, sample mangling.

### Overall preset average: **2.8/10**

---

## 3. Jazz Rendering Evaluation

The jazz voicing engine produces correct MIDI:
- Voice-led rootless voicings ✓
- Walking bass lines ✓
- Bill Evans-style comping with varied velocity and syncopation ✓

When rendered through constraint-synth with a triangle oscillator, it sounds like a **music theory textbook played through a cheap Casio**. The *notes* are right. The *sound* is wrong.

A real jazz piano has warmth, resonance, and a percussive-but-singing quality. This has none of that.

---

## 4. Technical Audio Quality Issues

### Good:
- **No aliasing** — high-frequency energy ratio is effectively zero for all presets. The built-in waveforms (sine, triangle, saw) are generated naively but at 44.1kHz the aliasing isn't severe for these simple shapes.
- **No DC offset** — all files have DC < 0.001.
- **No clipping** — except debussy_pad (18 samples at ±1.0).
- **Clean note boundaries** — no clicks at note boundaries for most presets (the envelope handles attack/release smoothly).

### Bad:
- **Coltrane Sax has 475 click artifacts** — the sawtooth wave's discontinuity creates sample-to-sample jumps >0.3. This is audible as a harsh buzz. A band-limited sawtooth (polyBLEP or additive) would fix this.
- **No oversampling** — the sawtooth and square waves will alias at higher frequencies. Currently inaudible because the demo melody stays in C4-C5 range, but play a C7 and you'll hear it.
- **16-bit output only** — modern production uses 24-bit or 32-bit float. The `to_wav` method hardcodes 16-bit.
- **Mono only** — no stereo field, no panning, no width.

### Ugly:
- **The "Consonance Filter" is barely functional.** It operates in the frequency domain by comparing spectral bins to harmonic ratios, but with short FFT windows (512-4096 samples), the frequency resolution is poor. The difference between filter ON and filter OFF is negligible in practice (RMS: 0.255 vs 0.265 for a sawtooth note). This is not a real synthesizer filter.
- **No anti-aliasing on waveform resets.** The sawtooth, square, and eisenstein snap all have discontinuities that should be smoothed (polyBLEP).

---

## 5. What's ACTUALLY Missing for Production Use

### Effects (Critical)
| Effect | Priority | Why |
|--------|----------|-----|
| **Reverb** | 🔴 Critical | Every preset sounds bone-dry. Even a simple Schroeder reverb would transform the output from "tinny" to "listenable." |
| **Chorus** | 🔴 Critical | The pad preset needs detuned copies. Without chorus, pads are flat and lifeless. |
| **Delay** | 🟡 Important | Even a simple tempo-synced delay adds movement and depth. |
| **Compression** | 🟡 Important | Dynamic range is wild (5.8:1 on full pipeline output). A compressor would glue things together. |
| **EQ** | 🟡 Important | No way to shape the tone beyond the crude "consonance filter." |

### Synthesis Techniques (Critical)
| Technique | Priority | Why |
|-----------|----------|-----|
| **Subtractive** | 🔴 Critical | Every professional synth starts with a harmonically rich oscillator then *filters* it down. This synth has no real filter — the "consonance filter" doesn't work as a lowpass/bandpass. |
| **FM** | 🔴 Critical | Frequency modulation synthesis is how you get bells, brass, electric pianos, and complex timbres from simple oscillators. Without it, the timbral palette is extremely limited. |
| **Wavetable** | 🟡 Important | Scanning through wavetables creates evolving timbres. The current "lattice shapes" are just static waveforms. |
| **Granular** | 🟢 Nice-to-have | For glitch/ambient textures. Not essential for basics. |
| **Additive** | 🟡 Important | The synth is already halfway there (it can layer oscillators). Formalize it with explicit harmonic controls. |
| **Band-limited oscillators** | 🔴 Critical | PolyBLEP or BLIT oscillators to prevent aliasing and clicks. |

### Quality of Life
- **Stereo output** — mandatory for production
- **24-bit/32-bit float WAV** — 16-bit is limiting
- **Real filter** — a proper biquad lowpass/highpass/bandpass with cutoff and resonance
- **LFOs** — for vibrato, tremolo, filter sweeps, PWM
- **MIDI CC support** — continuous controllers for expression
- **Polyphony management** — voice stealing, note priority

---

## 6. My Better Preset Attempt

I built `better_preset.py` that pushes the synth to its actual limits using only available tools:

### Strategy
Since the synth only has sine, triangle, square, saw, and eisenstein waveforms + a basic ADSR + a weak "consonance filter", I focused on what it CAN do:
- **Layered oscillators** — multiple instances summed for richer timbres
- **Slow envelopes** — the FunnelEnvelope is actually well-implemented; pads are the synth's strength
- **Crossfading segments** — simulating parameter automation by stitching short segments
- **Octave layering** — fundamental + sub-octave for body, + octave for shimmer

### Results
| Preset | Duration | Technical Quality | Listenability |
|--------|----------|-------------------|---------------|
| `ambient_progression.wav` | 11.0s | Clean (0 clicks, 0 clips) | 5/10 — actually pad-like! |
| `evolving_tone.wav` | 8.9s | Clean | 4/10 — subtle filter sweep, interesting |
| `shimmer_bells.wav` | 16.1s | Clean | 4/10 — the eisenstein quantization actually works for bells |
| `combined_arrangement.wav` | 11.0s | Clean | 5/10 — pads + bells, the best this synth can do |

### Honest Assessment of My Own Work
These presets are the ceiling of what constraint-synth can produce without adding new synthesis methods. They're listenable — you could put `ambient_progression.wav` in a meditation app and nobody would complain. But you couldn't put any of this in a track and have it sound professional.

The fundamental problem: **this is an oscillator, not a synthesizer.** A real synth has at minimum:
1. Multiple oscillator types with proper aliasing prevention
2. A real resonant filter (biquad, not FFT-based "consonance")
3. Effects (reverb, chorus, delay at minimum)
4. LFOs for modulation
5. Proper stereo output

---

## 7. Scoring

| Criteria | R1 Score | R2 Score | Notes |
|----------|----------|----------|-------|
| Pipeline runs | 3/10 | 9/10 | All components work, no import errors |
| Audio renders | 4/10 | 8/10 | Clean WAV output, correct sample rate |
| Preset fidelity | 2/10 | 3/10 | Debussy pad slightly improved; others unchanged |
| Audio quality | 3/10 | 4/10 | Coltrane Sax still clicks; debussy clips |
| Production viability | 1/10 | 2/10 | Still not usable in production without major additions |
| **OVERALL** | **4/10** | **5/10** | One point for working pipeline; sound design unchanged |

### What would move this to 7/10:
1. **Real biquad filter** with cutoff, resonance, and envelope modulation (2 days of work)
2. **Band-limited oscillators** via polyBLEP (1 day)
3. **Built-in reverb** — even a simple Schroeder reverb (1 day)
4. **Chorus** — 3 detuned copies with slow LFO (half a day)
5. **Stereo output** — trivial to add

### What would move this to 8/10:
6. **FM synthesis operator** — 2-op FM creates bells, brass, EPs
7. **24-bit WAV output**
8. **Proper anti-aliasing** at high frequencies
9. **LFO system** — assignable to pitch, filter, amplitude

---

## 8. Bottom Line

The constraint-theory *math* is solid — the lattice shapes, snap thresholds, and funnel envelopes are interesting abstractions. But the mapping from math to audio is too thin. Right now:

> **"Lattice geometry determines waveshape"** means you pick sine/triangle/saw/square and rename them.

The eisenstein snap (7-level quantization) is the only genuinely novel synthesis technique, and it produces a usable (if limited) stepped waveform. That's not nothing, but it's not enough for a product.

The pipeline WORKS now. The sound doesn't. A producer would open this, hear the presets, close it, and open Vital or Serum instead. The gap isn't theoretical — it's practical. Add a real filter, reverb, chorus, and band-limited oscillators, and you have something worth demoing. Without those, you have a math paper with audio output.

**Score: 5/10** — up from 4/10 because the pipeline runs clean and the audio is technically valid. Still not production-ready.
