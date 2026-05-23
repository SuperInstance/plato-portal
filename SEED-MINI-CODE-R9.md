# Seed Mini Code Innovation Round 9

## ExerciseGenerator (BUILD — math educator request)
```python
class ExerciseGenerator:
    def prescribe(self, diagnostic_report) -> list[Exercise]:
        """Generate targeted exercises for weak orders."""
    
    def for_order(self, order: int, difficulty: float) -> Exercise:
        """Generate an exercise for a specific diagnostic order."""
    
    def progress(self, history: list[DiagnosticReport]) -> Exercise:
        """Generate next exercise based on improvement trajectory."""
```
- Position order: accuracy drills (hit these specific notes)
- Direction order: phrase arc practice (build to peak, descend)
- Curvature order: timing exercises (vary velocity on beats 2 and 4)
- Structure order: form practice (compose 8 bars with AABA structure)

## TerrainHarmony (BUILD — top user request: chords)
```python
class TerrainHarmony:
    MAPPINGS = {
        'delta_blues': ['I', 'IV', 'V', 'I'],       # 12-bar blues
        'bebop': ['ii', 'V', 'I', 'viio'],           # ii-V-I with tritone sub
        'modal_jazz': ['Im7', 'IVm7', 'bVII7', 'IIIm7'], # modal interchange
        'hip_hop_trap': ['i', 'VI', 'III', 'VII'],    # minor loop
        'electronic_techno': ['i', 'i', 'i', 'i'],    # minimal harmonic movement
    }
    def generate(self, terrain, bars, key) -> list[Chord]:
```

## CompatibilityEngine (social feature)
```python
class CompatibilityEngine:
    def analyze_duo(self, report_a, report_b) -> CompatibilityReport:
        """How should two musicians play together?"""
    # "You anchor harmony (high position), they bring groove (high curvature)"
```

## PaceScript AI (PODCAST product variant)
Same 4-order diagnostic applied to speech:
- Position = articulation/clarity
- Direction = narrative arc
- Curvature = pacing/rhythm
- Structure = coherence/stay-on-topic
Separate product. Same engine.

## Playground Upgrade (web)
- Waveform canvas (Web Audio AnalyserNode)
- Piano roll canvas (colored notes per constraint primitive)
- 5 primitive strength sliders
- "Surprise Me" button (random terrain + mode + seed)
