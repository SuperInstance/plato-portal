# BETA-R2: Style Morpher Fix

## Problem
The morpher was cosmetic — it only shifted pitch register and added random jitter. Bach similarity actually *decreased* from 0.674 to 0.641 when morphing toward Bach.

## Root Cause
The old morpher (`_morph_harmony`, `_morph_rhythm`, etc.) operated on raw MIDI messages in-place:
- **Register**: crude pitch shift (only thing that worked)
- **Rhythm**: the syncopation code had `pass` — literally did nothing
- **Harmony**: randomly shifted notes by ±1 semitone without tracking note_off pairs
- **No structural changes**: didn't touch intervals, step/leap ratio, or note density

## Fix: Structural Morphing via Note Extraction → Transform → Rebuild

Rewrote `morph.py` to:
1. **Extract all notes** into structured data (onset, pitch, duration, velocity, track)
2. **Apply 8 structural transformations** in sequence:
   - `_morph_interval_distribution` — rescales intervals toward target mean_interval
   - `_morph_consonance` — shifts simultaneous notes toward/away from consonant intervals
   - `_morph_step_leap` — inserts passing tones to break up leaps (Bach), or creates leaps (jazz)
   - `_morph_durations` — reshapes note duration distribution
   - `_morph_syncopation` — quantizes to beat grid (Bach) or shifts off-beat (jazz)
   - `_morph_density` — adds/removes notes to match target notes_per_bar
   - `_morph_register` — shifts pitch center
   - `_morph_velocity_curve` — reshapes dynamics
3. **Rebuild MIDI** from transformed note data with proper note_on/note_off pairing

## Results

```
Before: Bach similarity = 0.674
After:  Bach similarity = 0.854
Improvement: +0.180
```

Key field movements (Autumn Leaves → Bach, blend=0.7):
| Field | Before | After | Target |
|-------|--------|-------|--------|
| mean_interval | 10.29 | 4.97 | 2.80 |
| step_vs_leap | 0.190 | 0.400 | 0.850 |
| consonance | 0.476 | 0.543 | 0.930 |
| notes_per_bar | 2.80 | 4.60 | 8.00 |

All fields move in the correct direction. The output is a valid MIDI file with 37 notes.

## File
`style-dna/style_dna/morph.py` — complete rewrite (~570 lines)
