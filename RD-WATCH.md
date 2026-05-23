# R&D Watch — Cutting Edge Repos & Trends

*Tracked repositories and technologies relevant to the constraint-music ecosystem.*

## 🔥 High Priority — Direct Integration Opportunities

### spotify/basic-pitch ⭐5052
- **Audio-to-MIDI with pitch bend detection**
- WHY: Our ecosystem is MIDI-in, but users have audio. This bridges the gap.
- Integration: Feed audio → basic-pitch → MIDI → style-dna → analysis
- GitHub: https://github.com/spotify/basic-pitch

### Rainbow-Dreamer/musicpy ⭐1460
- **Music programming language in Python with theory-aware data structures**
- WHY: Our constraint tools + musicpy's composition primitives = powerful combo
- Overlap: They do algorithmic composition, we do constraint-theory composition
- Integration: constraint-substrate as musicpy plugin, our lattice snap as their pitch operations
- GitHub: https://github.com/Rainbow-Dreamer/musicpy

### DBraun/DawDreamer ⭐1229
- **Python DAW with VST hosting, parameter automation, FAUST, JAX, JUCE**
- WHY: This is how we get VST/AU integration (producer's #1 ask from beta)
- Integration: constraint-synth as a DawDreamer processor, our pipeline as a DAW graph
- GitHub: https://github.com/DBraun/DawDreamer

### SamiPerttu/fundsp ⭐1147
- **Rust library for audio processing and synthesis**
- WHY: Our constraint-substrate is already Rust. This gives us real audio primitives.
- Integration: constraint-substrate funnel → fundsp envelope, lattice snap → fundsp quantizer
- GitHub: https://github.com/SamiPerttu/fundsp

### cycfi/q ⭐1385
- **C++ audio DSP library — filters, oscillators, effects**
- WHY: We need real biquad filters, polyBLEP, effects. This has them all.
- Integration: C layer for constraint-substrate audio extensions
- GitHub: https://github.com/cycfi/q

## 🎵 AI Music Generation — Competitive Landscape

### multimodal-art-projection/YuE ⭐6233
- **Open full-song generation model (Suno alternative)**
- WHY: Our style-DNA could CONDITION YuE generation — "generate in Bach style"
- Not competitive (we're tools, they're generation), potentially synergistic
- GitHub: https://github.com/multimodal-art-projection/YuE

### fspecii/ace-step-ui ⭐3915
- **Open source Suno alternative with local generation**
- WHY: Same as YuE — style conditioning opportunity
- GitHub: https://github.com/fspecii/ace-step-ui

### Google Magenta
- **ML-based music generation (MIDI + audio)**
- WHY: Their MusicVAE could generate MIDI that we analyze with style-dna
- Their approach: neural. Our approach: mathematical. Complementary.
- GitHub: https://github.com/magenta/magenta

## 🎼 Microtonal & Cross-Cultural

### charlesneimog/OM-JI ⭐12
- **OpenMusic library for Just Intonation composition**
- WHY: Direct overlap with our microtonal lattice work (Z/22Z, Z/24Z, Z/53Z)
- They have Harry Partch / Erv Wilson / Ben Johnston theory implemented
- Integration: Our Eisenstein lattice + their JI scales = full microtonal coverage

### retooth2/xenharmlib ⭐11
- **Xenharmonic music theory library — diatonic set theory, non-standard notations**
- WHY: Superset of Western theory, directly relevant to our cross-cultural work
- Could provide notation systems for our Z/nZ lattices
- GitHub: https://github.com/retooth2/xenharmlib

## 🔧 Constraint Programming

### yangeorget/nucs ⭐55
- **Python constraint programming library for CSP/CSOP**
- WHY: Our counterpoint engine IS a CSP solver but hand-rolled. nucs could make it formal.
- Integration: Replace hand-rolled constraint checking with nucs solver
- GitHub: https://github.com/yangeorget/nucs

## 🔬 Research Frontiers to Watch

### WebAudio API + WASM
- Our playground.html uses basic WebAudio. The frontier is:
  - AudioWorklet for real-time processing
  - WASM-compiled constraint-substrate in browser
  - SharedArrayBuffer for multi-threaded audio

### Differentiable DSP (ddsp, torchsynth)
- Neural-network-controlled synthesis
- Our constraint parameters as differentiable inputs to neural synths
- Could learn the mapping from style → synth parameters

### Music Information Retrieval (MIR)
- mirdata, librosa, essentia — analyze real recordings (not just MIDI)
- Our style-dna works on MIDI; MIR extends it to audio

### Real-time Collaboration
- WebRTC + CRDT (we have SmartCRDT in the org) for collaborative music making
- PLATO rooms as shared music spaces

## Evaluation Results

### ✅ basic-pitch — ADOPT
- Pipeline working: audio → MIDI → style DNA in 1-2s
- Bridge script: `examples/audio_to_analysis.py`
- Caveat: needs numpy<2 for tflite_runtime
- User story transformed: "drop any audio file"

### ✅ DawDreamer — ADOPT (phased)
- Installs cleanly on WSL2, 40.7MB wheel
- Built-in Faust DSP (no external VSTs needed for basics)
- VST hosting confirmed working (needs VST3 files like Surge XT)
- PoC: `examples/dawdreamer_render.py` + rendered 8s WAV
- Solves producer's #1 blocker

### ✅ musicpy — CONDITIONAL ADOPT
- Near-zero overlap with our tools — pure complementarity
- Use as composition front-end DSL (chord notation, scale objects, MIDI I/O)
- Our math stays ours (lattice, rigidity, funnel, holonomy)
- PoC: `examples/musicpy_constraint_composition.py`

### 🔄 fundsp — PENDING
- Rust audio backend for constraint-substrate
- Would give us real oscillators, filters, effects in Rust

### 🔄 YuE — WATCHING
- Style conditioning opportunity (our style-DNA conditions their generation)
- Not immediate priority

## Action Items
- [x] Evaluate basic-pitch → ADOPTED, bridge script working
- [x] Evaluate musicpy → CONDITIONAL ADOPT, PoC working
- [x] Evaluate DawDreamer → ADOPT, VST hosting confirmed
- [ ] Build `constraint_audio.py` bridge module (DawDreamer integration)
- [ ] Install Surge XT VST3 for real VST demo
- [ ] Add fundsp as Rust audio backend for constraint-substrate
- [ ] Study YuE for style-conditioned generation
- [ ] Contact xenharmlib maintainer about Eisenstein lattice collaboration
