# BETA-TASK-STYLE: Musical Style Analysis & Morphing Report

## Task Summary
Analyze MIDI files in the workspace, extract their musical style, compare to famous composers, and morph one toward Bach's style using the `style-dna` tool.

---

## Step-by-Step Log

### Step 1: Find MIDI files
- Ran `ls *.mid` → Found **1 file**: `autumn_leaves.mid` (1,594 bytes)
- ✅ Trivial, no friction

### Step 2: Find style tools
- Searched for directories with "style" or "dna" in the name
- Found `/home/phoenix/.openclaw/workspace/style-dna/` — a full Python package
- Also spotted related music tools: `flux-tensor-midi`, `groove-analyzer`, `plato-room-musician`, `jazz-voicing-engine`, `counterpoint-engine`, `holonomy-harmony`, `spline-midi-smooth`
- ✅ Easy to find, clear naming

### Step 3: Figure out the API
- Read `README.md` — **excellent** documentation with quick start code, API reference, and invariant explanations
- API surface: `StyleExtractor.extract()`, `StyleTile.similarity()`, `StyleMorpher.morph()`, pre-built `PERSONALITIES` dict
- Source code in 5 clean files: `tile.py`, `extract.py`, `morph.py`, `personalities.py`, `__init__.py`
- Pre-built composer profiles: Bach, Chopin, Joplin, Debussy, Coltrane
- ✅ README was clear enough to use immediately without reading source. I read source anyway to understand morphing behavior.

### Step 4: Install dependencies
- `pip install -e .` failed: `setuptools.backends._legacy` import error (Python 3.10 + old setuptools)
- Workaround: `sys.path.insert(0, 'style-dna')` and install `mido` + `numpy` separately
- ⚠️ **Friction point**: Package doesn't install cleanly on this Python 3.10 environment. The `pyproject.toml` backend needs updating.

### Step 5: Extract style profile from `autumn_leaves.mid`
Results:
| Metric | Value |
|--------|-------|
| Pitch center | 44.5 (low, bass-heavy) |
| Pitch range | 28–69 (41 semitones) |
| Mean interval | 10.29 semitones (very leap-y) |
| Step/leap ratio | 0.19 (mostly leaps) |
| Consonance rate | 0.476 |
| Syncopation rate | 0.091 |
| Notes per bar | 2.8 (sparse) |
| Betti numbers | (6, 2) — 6 components, 2 loops |
| Lyapunov exponent | -0.0235 (convergent) |
| Entropy ratio | 1.0 (maximum surface variety) |
| Liubai rate | 0.387 (lots of silence) |

The MIDI appears to be a simple/bare arrangement — very sparse, bass-register, lots of leaps and silences. Not a rich multi-track recording.

### Step 6: Compare to composer presets
| Composer | Similarity | Era |
|----------|-----------|-----|
| Debussy | **0.7649** | Impressionist |
| Chopin | 0.7395 | Romantic |
| Coltrane | 0.7234 | Jazz |
| Joplin | 0.7015 | Ragtime |
| Bach | 0.6744 | Baroque |

Interesting: Autumn Leaves is *least* similar to Bach, most similar to Debussy. The high entropy ratio (1.0), low consonance (0.476), and high liubai (silence) drive the Debussy similarity.

### Step 7: Morph toward Bach (blend=0.7)
- Morphing applied register shift, rhythm, timing, and harmony adjustments
- Output: `autumn_leaves_bach_morph.mid`

| Metric | Original | Morphed | Bach Target |
|--------|----------|---------|-------------|
| Pitch center | 44.5 | 54.2 | 60.0 |
| Consonance | 0.476 | 0.476 | 0.93 |
| Syncopation | 0.091 | 0.136 | 0.05 |
| Lyapunov | -0.0235 | 0.0423 | 0.01 |
| Entropy ratio | 1.0 | 1.0 | 0.29 |
| → Bach similarity | 0.6744 | **0.6413** | 1.0 |

**⚠️ The morphing actually DECREASED Bach similarity by 0.033!** The register shift helped (moved pitch center up), but the morphing introduced more syncopation (wrong direction) and didn't address the core structural differences (entropy ratio, consonance).

### Step 8: Export
- Morphed file saved to `autumn_leaves_bach_morph.mid`
- ✅ File written successfully

---

## Friction Score: 4/10

| Aspect | Score | Notes |
|--------|-------|-------|
| Finding MIDI files | 0/10 | Trivial, right there |
| Finding the tool | 0/10 | `style-dna` directory, obvious name |
| Understanding the API | 1/10 | README is excellent, quick start works |
| Installation | 7/10 | `pip install -e .` failed, had to workaround |
| Extraction | 1/10 | Clean API, worked first try |
| Comparison | 0/10 | `PERSONALITIES` dict + `.similarity()`, dead simple |
| Morphing | 6/10 | API works, but **results are poor/wrong direction** |
| Export | 0/10 | Auto-generates output path, just works |

**Average: ~4/10 friction** — mostly from install issues and the morphing quality problem.

---

## What Worked
- **README is top-tier**: Clear API, quick start code that actually runs, invariant explanations with typical values
- **StyleTile design**: Frozen dataclass with `.similarity()`, `.diff()`, `.to_json()` — feels professional
- **PERSONALITIES pre-built profiles**: Instant comparison to 5 composers, no setup needed
- **Extraction quality**: The extracted profile seems reasonable and captures meaningful musical features
- **Code organization**: 5 clean files, each with a clear responsibility
- **`.diff()` method**: Incredibly useful for understanding *why* two styles differ

## What Didn't Work
- **`pip install -e .` fails**: setuptools backend issue on Python 3.10
- **Morphing quality is poor**: The morphed file moved *away* from Bach similarity. Root causes:
  - Register morphing only does a blunt pitch shift (helps somewhat)
  - Rhythm morphing tries to add syncopation but Bach needs *less* syncopation — it goes the wrong direction
  - Harmony morphing randomly chromatic-alters notes (increase/decrease dissonance), but doesn't actually reharmonize
  - No morphing of interval structure or melodic contour (the biggest gaps vs Bach)
  - Entropy ratio (1.0 vs 0.29) is completely untouched
- **Single MIDI file is sparse**: Autumn Leaves MIDI is bare (2.8 notes/bar, bass-heavy), which limits the extraction quality

## Would I Use This Again?

**For extraction and comparison: Absolutely yes.** The `StyleExtractor` + `StyleTile.similarity()` pipeline is genuinely useful for understanding musical DNA. The deep invariants (Betti numbers, Lyapunov exponent, entropy ratio) are creative and meaningful. I'd use this to profile my MIDI collection and understand composer relationships.

**For morphing: Not yet.** The morpher needs significant work — it treats symptoms (pitch center, timing jitter) rather than structural causes (interval distribution, consonance patterns, entropy). A good morph toward Bach would need to: smooth interval leaps into steps, add consonant intervals, increase note density, add counterpoint, and reduce entropy ratio.

**Overall: 7/10 tool.** The analysis/extraction side is genuinely impressive. The morphing side is a proof-of-concept that needs real algorithmic work.
