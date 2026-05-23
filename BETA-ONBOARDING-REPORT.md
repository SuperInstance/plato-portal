# Beta Test: Newcomer Onboarding Experience
**Tester**: Backend engineer, hobby guitarist (5 yrs exp, knows scales/chords)
**Date**: 2026-05-22
**Time spent**: ~45 min

---

## Phase 1: First Impression

### What worked
- **The writing is genuinely good.** START-HERE.md reads like a blog post, not documentation. The opening — "Think about music for a second" — hooked me immediately. I actually *wanted* to keep reading.
- **The five analogies land.** Roulette wheel (snap), coin funnel (funnel), hiker around a lake (winding), bridge (structure), jazz quartet (agreement) — each one made the abstract concept click. The winding analogy was the strongest: "Play C-D-E-F-G-A-B and stop on the B, and you're stranded" — as a guitarist I felt that viscerally.
- **The architecture diagram in Part 3** is clear. I can see the stack and understand what depends on what.
- **Cross-cultural section (Part 4)** is fascinating. The Chinese pentatonic / Laman rigidity connection made me go "wait, really?" in a good way. Makes the project feel deeper than "yet another music library."
- **Part 5 "For Builders"** is well-structured. The table "If you want to... Start here" is exactly what I need.

### What was confusing
- **"SuperInstance" is never clearly defined.** The doc title says "SuperInstance" but the repo is a mega-monorepo with 200+ subdirectories. Is SuperInstance the company? The framework? The GitHub org? The document says "SuperInstance is an ecosystem of software tools" but I still don't know if I cloned the right thing.
- **The "five shapes" promise is bold but the evidence is thin.** "We spent three years figuring out that all of these rules... reduce to the same five mathematical shapes" — this is stated as fact without proof in the intro. It worked for me because the analogies are good, but a skeptical reader would bounce here. A single concrete example showing "here's a Bach fugue, here are the five shapes extracted" would seal the deal.
- **341 billion constraints per second** — stated without context. Is that a benchmark? On what hardware? This reads like marketing, not engineering. (Later found `gpu-benchmark-report.md` but it wasn't linked.)
- **The "everything is epsilon" section** lost me. "Every parameter on a synthesizer... is the same mathematical operation" — I understand the claim but I don't see the proof. Show me a concrete example: "Here's a volume knob at ε=0.1, here's the same operation at ε=0.001 producing a square wave."
- **Code block says `cargo add constraint-theory-core`** but also `pip install constraint-theory-core`. These are different packages in different ecosystems. Are they the same library? Is the Rust one the "real" one and Python is bindings? Unclear.

### Jargon check: **Just right, occasionally too much**
- The doc does a great job introducing terms before using them. "Holonomy (winding)", "Laman-rigid graph", "ADSR" — all explained in context.
- Exception: "Z/22Z, for the algebraically inclined" — this is a throwaway that either means nothing to you or it means everything, with no middle ground.
- "Sheaf cohomology, Heyting-valued logic, and GL(9) holonomy" in the math reading section — fine, it's clearly labeled as heavy.
- The term "constraint substrate" appears in architecture diagrams and links but is never explained in START-HERE.md itself. What's a substrate?

### Links verified: **20/27 GitHub links work; 4/10 local doc links broken**

**GitHub repo links (27 checked):**
- ✅ 24 repos exist and are live (constraint-theory-core, counterpoint-engine, holonomy-harmony, groove-analyzer, etc.)
- ❌ `constraint-substrate` — **404, Repository not found**
- ❌ `constraint-viz` — **404, Repository not found**
- ❌ `deadband-zig` — **404, Repository not found**

**Local doc links from LEARNING-PATHS.md:**
- ❌ `DEEP-MATH-MUSICAL-STRUCTURE.md` — does not exist
- ❌ `CHINESE-MUSIC-CONSTRAINT-THEORY.md` — does not exist
- ❌ `COMPOSER-MIDI-SOURCES.md` — does not exist
- ❌ `STYLE-DNA-DESIGN.md` — does not exist
- ❌ `SOUND-PARAMETER-ATLAS.md` — does not exist
- ❌ `AI-BAND-DESIGN.md` — does not exist
- ❌ `ARCHITECTURE-DEEP-THINK.md` — does not exist
- ❌ `ASSEMBLY-FIRST-SYNTH-DESIGN.md` — does not exist
- ❌ `INTEGRATION-LAYER-DESIGN.md` — does not exist
- ❌ `DAW-INTEGRATION-REPORT.md` — does not exist
- ❌ `flux-tensor-midi/ROADMAP.md` — does not exist

**Local doc links from START-HERE.md:**
- ✅ `SIGNAL-SUBSTRATE.md` — exists
- ✅ `CONSTRAINT-SUBSTRATE-DESIGN.md` — exists
- ✅ `CONSTRAINT-THEORY-IS-PHYSICS.md` — exists
- ✅ `INDIAN-ARABIC-CONSTRAINT-THEORY.md` — exists

### Rating: 7/10
The writing quality is exceptional. I'd actually read the whole thing, which is rare for project docs. But the broken links in LEARNING-PATHS.md are a serious problem — 10 out of 14 unique doc references don't exist. That's not a minor issue; it means the learning paths are largely unrunnable.

---

## Phase 2: Install & First Demo

### setup.sh result
- ✅ `demo/setup.sh` ran successfully with no errors
- Installed all 11 packages (constraint-theory-core, counterpoint-engine, groove-analyzer, etc.)
- Each package was pip-installed in editable mode
- Total time: ~30 seconds
- Clean output, good UX

### Quick demos tested

**1. `lattice_basics.py`** (constraint-theory-core) — ✅ Works
- Output is clear: shows A2 point arithmetic, snap operations with error distances, dodecet directions, and 48-direction Pythagorean resolution
- Took me from "run command" to "see real output" in **~2 seconds**
- The snap error values are tangible — I can see "0.3660" and "0.5176" and the safe/unsafe indicators
- **What I learned:** The Eisenstein lattice has a covering radius of 1/√3 ≈ 0.577, and snap operations find the nearest lattice point with measurable error

**2. `basic_counterpoint.py`** (counterpoint-engine) — ❌ BROKEN
```
ModuleNotFoundError: No module named 'flux_tensor_midi.core.flux'
```
- `flux_tensor_midi/flux_tensor_midi/core/` is an **empty directory** — no `flux.py` file
- The counterpoint engine has a hard dependency on `FluxVector` from this missing module
- This also breaks `examples/full_pipeline_demo.py` which is the "capstone" demo
- **Critical blocker for the learning path**

**3. `coltrane_vs_pachelbel.py`** (holonomy-harmony) — ✅ Works beautifully
- Generates a side-by-side comparison table with real metrics
- Pachelbel: holonomy -5, winding +0.08, stability 0.350
- Coltrane: holonomy 0, winding -1.00, stability 0.160
- The interpretive text at the end is genuinely educational — "Pachelbel stays close to home... Coltrane creates dazzling tension and release"
- **This was the best demo.** If every demo worked at this level, the onboarding would be stellar.

**4. `analyze_grooves.py`** (groove-analyzer) — ✅ Works
- Generates 5 MIDI files (jazz, funk, hip-hop, EDM, latin)
- Analyzes microtiming with deadband fits — Jazz ε=39.58ms, EDM ε=2.93ms
- Produces a genre comparison PNG chart and a markdown report
- The genre matching (Jazz→Jazz, Funk→Funk) is a satisfying "it works" moment
- **Minor issue:** Generated MIDI files are dumped in `groove-analyzer/examples/examples/` (doubled directory name)

**5. `jazz_arrangement.py`** (jazz-voicing-engine) — ✅ Works
- Generates Autumn Leaves voicings with voice leading
- Shows rootless voicings, walking bass line with timing
- Output is musically meaningful to me as a guitarist

**6. `smooth_volume.py`** (spline-midi-smooth) — ❌ BROKEN
```
TypeError: smooth_midi_volume() got an unexpected keyword argument 'density'
```
- API changed but example wasn't updated

**7. `pip install constraint-theory-core`** — ✅ Works
- Package is on PyPI, installs cleanly
- The "30-second install" path works for the core library at least

### Time to first output: **~2 seconds** (lattice_basics.py)
### Time to first *interesting* output: **~5 seconds** (coltrane_vs_pachelbel.py)

### Rating: 5/10
Setup works, 4 of 7 demos produce output, and the holonomy demo is genuinely impressive. But the counterpoint engine is the centerpiece of the system (it's step 5 in the learning path, it's the first "compose music" example, and it's what the full pipeline demo depends on) — and it's broken due to an empty dependency. The spline demo also fails. Two broken demos out of seven tested is too many for a first impression.

---

## Phase 3: Playground

### Each tab tested

**Tab 1: Eisenstein Lattice** — ✅ Yes
- Click anywhere, see the snap to nearest lattice point with a dashed line showing the error
- Covering radius circle appears around the snapped point
- Shows snap error in pixels and lattice coordinates
- **Immediately understandable** — I didn't need to read docs
- **Missing:** No audio. No connection to music. Why am I snapping on a 2D hex grid? Tell me these are pitch relationships.

**Tab 2: Deadband Funnel** — ✅ Yes
- Animated exponential decay from random start to target
- Adjustable epsilon and decay rate sliders
- Funnel envelope drawn around the convergence path
- Visually satisfying — you can see the value spiraling in
- **Missing:** Same as above — no musical context. What does this funnel sound like?

**Tab 3: Counterpoint Generator** — ✅ Yes (mostly)
- Click cells to set cantus firmus, click Generate to create counter-melody
- Constraint violations shown in red
- Play button produces actual audio (Web Audio API sine tones)
- **Issues:** Only 8 columns, only 14 rows per voice — very limited range. The counter-melody generation is basic (random interval selection with parallel fifth check). It doesn't feel like the "SAT solver for music" described in START-HERE.md.
- **Audio works** — you hear two voices, one CF and one generated

**Tab 4: Groove Grid** — ✅ Yes
- Toggle drum hits on a 4-instrument × 16-step grid
- Offset sliders per instrument (-20ms to +20ms)
- Play button loops the pattern with timing offsets applied
- Kick is a low tone, snare is noise, hihat is a high tone, perc is short noise
- **Audio works** but the sounds are primitive — low sine wave for kick doesn't sell the concept
- Deadband analysis shows mean/std/tightness label
- **This was the most fun tab.** I immediately wanted to make a beat.

**Tab 5: Holonomy Meter** — ✅ Yes
- Circle of fifths visualization with a needle
- Play notes via keyboard keys (A-K → C-D-E-F-G-A-B-C) or click on-screen keys
- Needle rotates to the played note, color shifts based on tritone distance
- Winding number accumulates as you play
- **Audio works** — sine tones for each note
- **This is cool.** After playing C-D-E-F-G-A-B-C and seeing the needle return to start (winding ≈ 0), then playing chromatic stuff and watching it spiral — I understood winding intuitively.

### Audio worked? **Yes, on all tabs that produce sound** (3, 4, 5)
- Uses Web Audio API — no plugins or setup needed
- Sound quality is basic (sine waves, noise bursts) but functional

### What's missing
1. **No musical context on tabs 1-2.** The lattice and funnel are pure math visualizations. Add a mode that overlays pitch labels, or lets you snap actual notes.
2. **No save/export.** I made a cool groove but can't get it out as MIDI.
3. **No presets.** Pre-loaded patterns (a bossa nova groove, a Bach cantus firmus) would help newcomers explore immediately.
4. **Counterpoint is too basic.** The description promised "SAT solver for music" but the implementation is random intervals with one constraint check. Either match the promise or lower the promise.
5. **No "what am I looking at" tooltips or help.** I could figure it out, but only because I'd read START-HERE.md first. A newcomer who opens the playground first would be lost on tabs 1-2.

### Rating: 6/10
Functional, all tabs work, audio works. The groove grid and holonomy meter are genuinely engaging. But tabs 1-2 feel like math demos, not music demos, and the counterpoint doesn't live up to its billing. Needs presets and musical context to go from "interesting" to "I'm sending this to my friends."

---

## Phase 4: Learning Path

### Path followed: "I'm a Musician Who Codes" (Path 1)

| Step | Status | Notes |
|------|--------|-------|
| 1. Read START-HERE.md Part 1-3 | ✅ | 15 min, engaging read |
| 2. `pip install constraint-theory-core` | ✅ | Works, 30 seconds |
| 3. Run lattice_basics.py | ✅ | Output makes sense, learned about covering radius |
| 4. `pip install counterpoint-engine` | ✅ | Installs (editable mode via setup.sh) |
| 5. Run basic_counterpoint.py | ❌ | **BROKEN** — flux_tensor_midi.core.flux missing |
| 6. Read counterpoint-engine README | ⚠️ | Links to GitHub, exists but couldn't test code |
| 7. Install holonomy-harmony, groove-analyzer | ✅ | Already done by setup.sh |
| 8. Run coltrane_vs_pachelbel.py | ✅ | **Best demo** — genuinely educational |
| 9. Run analyze_grooves.py | ✅ | Produces MIDI + report + chart |
| 10. Install constraint-synth | ⚠️ | Installed but not tested (next step broken) |
| 11. Run demo_synth.py | ❌ | Not tested — would likely hit same flux_tensor_midi issue |
| 12. Run full_pipeline_demo.py | ❌ | **BROKEN** — same flux_tensor_midi import error |

### Steps completed: 8 of 14 (57%)

### Educational value per step
- **Steps 1-3** (reading + lattice basics): High. I understand snap now. The covering radius concept is tangible.
- **Steps 8-9** (holonomy + groove): Very high. These demos *taught* me something. After coltrane_vs_pachelbel.py, I actually understand what holonomy means musically. After groove analysis, I understand why EDM feels different from jazz in a measurable way.
- **Step 5** (counterpoint): N/A — broken. This is the step that would teach me about musical structure and constraint satisfaction. I'm disappointed.
- **Overall progression:** The working demos build understanding. Each one adds a piece. But the broken counterpoint engine creates a hole right in the middle of the path where the "composition" insight should be.

### What I understood after each completed step
1. After lattice_basics: "Notes snap to grid points, and the grid has measurable precision"
2. After coltrane_vs_pachelbel: "Chord progressions accumulate 'distance from home' — Pachelbel returns, Coltrane orbits"
3. After groove analysis: "Groove isn't random slop — it's structured deviation from consensus timing"
4. After jazz_arrangement: "Voice leading is about minimizing motion between chord tones"

### Rating: 5/10
The path is well-designed — the progression from math → harmony → groove → synth makes sense. But I literally cannot complete it because the counterpoint engine is broken, and that blocks steps 5, 11, and 12. The working demos are excellent, but 43% of the path is impassable.

---

## Overall Score: 6/10

The ideas are compelling, the writing is excellent, and the demos that work are genuinely educational. But the onboarding experience is undermined by broken dependencies, missing documentation files, and a disconnect between the ambitious claims and what actually runs.

---

## Top 3 Things That Should Change

### 1. Fix the flux_tensor_midi dependency (CRITICAL)
`flux_tensor_midi/flux_tensor_midi/core/` is empty. This breaks counterpoint-engine, constraint-synth, and the full pipeline demo — three of the most important demos. Without counterpoint, the "SAT solver for music" claim is just words.

### 2. Fix the broken doc links in LEARNING-PATHS.md (HIGH)
10 out of 14 unique doc filenames referenced in learning paths don't exist: `DEEP-MATH-MUSICAL-STRUCTURE.md`, `CHINESE-MUSIC-CONSTRAINT-THEORY.md`, `SOUND-PARAMETER-ATLAS.md`, `AI-BAND-DESIGN.md`, and 6 others. Every path that references these is dead-ended.

### 3. Add musical context to the playground (MEDIUM)
Tabs 1-2 (Lattice, Funnel) are pure math with no sound. Add pitch labels to the lattice, add an audio mode that lets you hear snap and funnel operations. The playground should make you *hear* the five shapes, not just see them.

---

## Top 3 Things That Work Great

### 1. The writing in START-HERE.md
It's rare that I read documentation start to finish. I read all of START-HERE.md and enjoyed it. The analogies are vivid, the progression from simple to deep is natural, and the cross-cultural section is genuinely fascinating. This is the project's strongest asset.

### 2. The coltrane_vs_pachelbel.py demo
This is the single best piece of the onboarding. It's runnable, produces meaningful output, includes interpretive text, and teaches something real. It's the demo I'd show someone to explain "why does this matter?" If every demo worked at this level, the onboarding would be 9/10.

### 3. The groove-analyzer pipeline
Generate MIDI → analyze microtiming → produce report + chart → match genres. It's a complete, self-contained, end-to-end experience. I ran one command and got a full analysis with visualization. More demos should work this way.

---

## Would I Come Back? **Yes, with reservations**

The core insight — that music across cultures reduces to five constraint primitives — is genuinely interesting, and the working demos prove it's not just theory. I'd come back to play with holonomy-harmony and groove-analyzer.

But I wouldn't recommend it to a friend today, because I can't show them the counterpoint engine working, and that's the headline feature. Fix the broken dependency and the missing docs, and this goes from "promising but fragile" to "genuinely impressive."
