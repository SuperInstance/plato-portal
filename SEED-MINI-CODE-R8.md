# Seed Mini Code Innovation Round 8

## 1. TextureAutomation Class (BUILD THIS)
```python
class TextureAutomation:
    """Generate parameter curves for build→drop→breakdown structure."""
    def __init__(self, bars=16, bpm=130):
        self.curves = {
            'filter_cutoff': [],  # 0-1 over bars
            'reverb_wet': [],     # 0-1
            'note_density': [],   # notes/bar
            'velocity': [],       # 0-127
        }
    
    def build_drop_breakdown(self):
        """Classic techno: sparse → build → DROP → sparse"""
        # Breakdown: low everything
        # Build: exponential ramp up filter/density
        # Drop: peak filter, peak density, low reverb (punch)
        # After: sustain at medium
```
Key insight: techno texture follows a predictable TENSION ARC. The curves are predictable enough to generate algorithmically.

## 2. SeedManager (BUILD THIS — math educator requested it)
```python
class SeedManager:
    """Single master seed → deterministic random streams per subsystem."""
    def __init__(self, master_seed=42):
        self.master = random.Random(master_seed)
        self.subsystems = {}
    
    def get_rng(self, name: str) -> random.Random:
        """Get a deterministic RNG for a named subsystem."""
        if name not in self.subsystems:
            self.subsystems[name] = random.Random(self.master.randint(0, 2**32))
        return self.subsystems[name]
    
    # Usage:
    # terrain_rng = seed_mgr.get_rng('terrain')
    # note_rng = seed_mgr.get_rng('notes')
    # humanize_rng = seed_mgr.get_rng('humanize')
    # Same seed → same output, every time.
```

## 3. ChordProgression Module (BUILD THIS — top user request)
- Takes key + constraint settings
- Generates I-vi-ii-V type progressions
- Feeds chord changes to melody generators so they follow harmony
- Time-aligned: each chord knows when it starts/ends

## 4. Minimal Viable Constraint Instrument (21 lines)
```python
import random
scale_notes = ["C4", "D4", "E4", "G4", "A4"]
terrain_height = 2  # start at middle
melody = []
for step in range(16):
    terrain_height += random.uniform(-0.5, 0.5)
    terrain_height = max(0, min(len(scale_notes)-1, terrain_height))
    nearest = round(terrain_height)
    melody.append(scale_notes[nearest])
print(" → ".join(melody))
```
The terrain is a drifting heightmap. The snap pulls notes to the nearest scale degree. This IS the concept in 10 lines.

## 5. REST API (FastAPI)
- POST /generate → WAV + diagnostic + MIDI
- POST /analyze → uploaded MIDI → diagnostic
- GET /terrains → list all 17
- Full FastAPI implementation sketched out with pydantic validation

## 6. ASCII Terrain Visualization
delta_blues: sparse, low, irregular dots
bebop: dense, wide range, packed middle
electronic_techno: dense bottom (kick+bass), sparse top, grid-aligned
Good for terminal output and docs.
