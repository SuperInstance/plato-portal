# R&D Evaluation: DawDreamer for VST Hosting & Constraint-Theory Audio Integration

**Date:** 2026-05-22  
**Status:** ✅ Proof-of-concept working  
**Verdict:** Strong fit — recommend integration

---

## Executive Summary

DawDreamer (v0.8.3) installs cleanly on our WSL2 Linux environment, hosts VST2/VST3 plugins via JUCE, supports audio-rate and PPQN-based parameter automation, and includes a built-in Faust DSP compiler. We successfully built a constraint-theory audio demo using Faust synthesizers with lattice-snap, funnel-envelope, and holonomy-modulation parameter automation — all without needing external VST plugins.

**Bottom line:** DawDreamer solves the "no VST/AU = not production ready" problem. It's the right bridge between our constraint-theory substrate and real producer workflows.

---

## 1. DawDreamer Capabilities Confirmed

### Installation
```
pip install dawdreamer  # 40.7 MB wheel, installed in ~10s
```
- ✅ Python 3.10 compatible
- ✅ Linux (WSL2) support
- ✅ No external dependencies beyond numpy

### Core API (tested)
| Feature | Status | Notes |
|---------|--------|-------|
| RenderEngine | ✅ Working | `RenderEngine(44100, 512)` |
| Faust Processor | ✅ Working | Real-time DSP compilation |
| Parameter Automation | ✅ Working | PPQN and audio-rate modes |
| Built-in Oscillator | ✅ Working | `make_oscillator_processor()` |
| MIDI Support | ✅ Available | Note-by-note or file import |
| VST Plugin Host | ⚠️ Requires VST files | API works, no VSTs on system |
| WAV Output | ✅ Working | Via `get_audio()` + wave module |

### Built-in Processors
```
make_faust_processor      # Faust DSP (no VST needed!)
make_plugin_processor     # VST2/VST3 host
make_oscillator_processor # Basic oscillator
make_playback_processor   # Audio file playback
make_playbackwarp_processor # Ableton-style warp
make_compressor_processor
make_delay_processor
make_filter_processor
make_panner_processor
make_reverb_processor
make_sampler_processor
make_add_processor        # Mix multiple signals
```

### Key API Details
- **Automation** uses parameter *names* (strings like `/dawdreamer/freq`), not indices
- **PPQN mode** = musically-synced automation (960 pulses per quarter note standard)
- **Parameters** are always normalized to [0, 1] regardless of display range
- **Graph** is DAG-based: `engine.load_graph([(proc, [inputs])])`

---

## 2. Proof-of-Concept: Constraint-Theory → Audio

**File:** `examples/constraint_demo.wav` (8 seconds, 705KB)

### Architecture Demonstrated

```
constraint-substrate
    ↓
┌─────────────────────────────────────────┐
│  Parameter Mapping Layer                │
│                                         │
│  Lattice Snap → frequency quantization  │
│    (pentatonic scale snapping)          │
│                                         │
│  Funnel → gain envelope shape           │
│    (attack/sustain/release)             │
│                                         │
│  Holonomy → modulation depth (LFO)      │
│    (sinusoidal gain modulation)         │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  DawDreamer Faust Synth                 │
│  freq = hslider("freq", 440, 100, 2000) │
│  gain = hslider("gain", 0.5, 0, 1)      │
│  process = os.osc(freq) * gain           │
└─────────────┬───────────────────────────┘
              ↓
         WAV output (rendered)
```

### What Each Constraint Does in Audio

| Constraint | Audio Parameter | Effect |
|-----------|----------------|--------|
| **Lattice Snap** | Frequency | Quantizes continuous pitch to discrete scale degrees (pentatonic demo) |
| **Funnel** | Gain envelope | Shapes attack/sustain/release — constrains energy flow over time |
| **Holonomy** | Modulation depth | LFO depth on gain — topological winding creates vibrato/tremolo patterns |

### Code Pattern
```python
import dawdreamer as daw
import numpy as np

engine = daw.RenderEngine(44100, 512)
engine.set_bpm(120)

synth = engine.make_faust_processor('synth')
synth.set_dsp_string('''
freq = hslider("freq", 440, 100, 2000, 1);
gain = hslider("gain", 0.5, 0, 1, 0.01);
process = os.osc(freq) * gain;
''')

# Lattice snap: quantize to pentatonic
pentatonic = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25]
ppqn, beats = 960, 16
pulses = beats * ppqn

# Generate snapped automation curve
freq_automation = build_snapped_curve(pentatonic, pulses)  # normalized [0,1]
gain_automation = build_funnel_envelope(pulses)             # with holonomy LFO

synth.set_automation('/dawdreamer/freq', freq_automation, ppqn=ppqn)
synth.set_automation('/dawdreamer/gain', gain_automation, ppqn=ppqn)

engine.load_graph([(synth, [])])
engine.render(8.0)
audio = engine.get_audio()  # numpy array ready for WAV
```

---

## 3. Full Integration Architecture

### Phase 1: Constraint-Theory → Faust Synth (NOW)
The PoC already works. Next steps:
- Replace simple oscillator with richer Faust synth (subtractive, FM, wavetable)
- Map all constraint types to audio parameters
- Build `constraint_audio.py` module that bridges substrate → DawDreamer

### Phase 2: Constraint-Theory → Any VST (NEAR TERM)
```python
# Load any VST synth
surge = engine.make_plugin_processor('surge', '/path/to/Surge.vst3')
# Apply constraint automation to VST parameters
surge.set_automation('filter_cutoff', lattice_snap_curve, ppqn=960)
surge.set_automation('osc1_pitch', quantized_pitch_curve, ppqn=960)
surge.set_automation('amp_env_attack', funnel_curve, ppqn=960)
surge.set_automation('lfo_depth', holonomy_curve, ppqn=960)
```

### Phase 3: Constraint-VST Plugin (MEDIUM TERM)
Build a JUCE-based VST that wraps constraint-substrate:
- VST parameters = constraint parameters (lattice size, funnel shape, holonomy order)
- Audio thread reads from constraint solver running in background
- Producers use it in Ableton/FL Studio like any other synth
- DawDreamer's JUCE foundation means we understand the framework

### Phase 4: Real-time / DAW Integration (LONG TERM)
Options for getting into producers' hands:
1. **Offline render** (now): constraint-substrate → DawDreamer → WAV → import into DAW
2. **Standalone app**: JUCE app with real-time constraint controls + audio output
3. **VST plugin**: Wrap everything in a VST3/AU that runs inside Ableton
4. **REPL/Notebook**: Jupyter + DawDreamer for experimental workflows

---

## 4. Recommended VSTs for Constraint-Music

| VST | License | Why | Automation Support |
|-----|---------|-----|--------------------|
| **Surge XT** | GPL-3.0 | Best free synth, massive parameter set, FM/wavetable/unison | Excellent (500+ params) |
| **Vital** | Free tier | Spectral warping wavetable, visual modulation system | Good |
| **Helm** | GPL-3.0 | Simple subtractive, good for learning | Good |
| **Dexed** | GPL-3.0 | DX7 FM synth, 144 parameters, algorithmic music friendly | Excellent |
| **Pianoteq** | Commercial | Physical modeling (constraint-theory meets physics!) | Excellent |
| **TAL-NoiseMaker** | Free | Juno-style subtractive, 80 params | Good |
| **ZynAddSubFX** | GPL-2.0 | Additive + subtractive + PAD synth | Good |

**Top pick: Surge XT** — open source, massive parameter space, deep modulation, and runs on all platforms including Linux.

---

## 5. Path from Python Library → Producer in Ableton

### Realistic Timeline

| Phase | Time | Deliverable |
|-------|------|-------------|
| 1. Faust synth + constraint automation | 1-2 weeks | `constraint_audio.py` module |
| 2. VST hosting with Surge | 2-3 weeks | Render pipeline with any VST |
| 3. MIDI export | 1 week | Constraint → MIDI file → any DAW |
| 4. Standalone JUCE app | 1-2 months | GUI app with real-time audio |
| 5. VST3/AU plugin | 2-3 months | Plugin that runs inside Ableton |

### The Pragmatic Path (What Gets Producers Using It)

**Fastest:** Constraint → MIDI export. Producers can:
1. Generate constraint-parameterized MIDI in Python
2. Import MIDI into Ableton with any synth
3. Tweak synth settings manually

This requires zero new code — DawDreamer supports MIDI export, and constraint parameters can drive MIDI note selection (lattice snap = quantize, funnel = velocity, holonomy = CC automation).

**Most impressive:** Constraint → Surge XT via DawDreamer → rendered audio. This shows the full pipeline working with a real VST.

---

## 6. Technical Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| GPLv3 license (DawDreamer) | Medium | Our wrapper can be MIT; only distribution of combined work triggers GPL |
| No real-time audio in DawDreamer | Low | Render mode is fine for offline; real-time needs JUCE app or VST plugin |
| VST path management | Low | Docker image with pre-installed free VSTs |
| JUCE complexity for VST plugin | Medium | Start with JUCE's audio plugin template; DawDreamer proves JUCE works |
| WSL2 audio latency | Low | Use offline render; for real-time, native Linux or macOS |

---

## 7. Conclusion & Recommendation

**DawDreamer is a strong fit.** It gives us:
- ✅ VST hosting today (just need to install VSTs)
- ✅ Parameter automation that maps cleanly to constraint theory
- ✅ Faust DSP for custom synthesis without external plugins
- ✅ MIDI support for DAW integration
- ✅ Python-native (fits our stack)

**Recommended next steps:**
1. Install Surge XT VST3 on this machine
2. Build `constraint_audio.py` module abstracting the DawDreamer bridge
3. Create a richer Faust synth (multi-oscillator, filter, effects chain)
4. Demo: constraint-theory parameters → Surge XT → rendered WAV
5. That demo is what we show the producer beta tester

The "no VST/AU = not production ready" feedback is valid. DawDreamer is the answer. The PoC proves the concept works — now we just need to make it polished.
