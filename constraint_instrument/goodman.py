"""
Goodman Mode — The Diagnostic Engine.

Benny Goodman had the notes but not always the feel.
This engine DIAGNOSES what order of constraint you're missing,
with clinical precision, from raw MIDI/performance data.

Order hierarchy (analogous to Taylor expansion of motion):
  0th — POSITION:     Do you know where you are?    (pitch selection, scale adherence)
  1st — DIRECTION:    Do you know where you're going? (melodic direction, voice leading)
  2nd — CURVATURE:    Do you know how direction changes? (rhythm, dynamics, microtiming)
  3rd — STRUCTURE:    Does the whole thing hold together? (form, motifs, arc)

Each order scores 0.0–1.0 and maps to ★☆☆☆☆ through ★★★★★.
"""

import math
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# ── Data types ──────────────────────────────────────────────────────────────

Note = Dict[str, Any]  # {"pitch": int, "velocity": int, "start": float, "duration": float}


@dataclass
class OrderScore:
    """Score and breakdown for a single order of constraint."""
    order: int
    name: str
    score: float            # 0.0 – 1.0
    stars: str              # "★★★☆☆"
    components: Dict[str, float]  # sub-metric name -> score
    detail: str             # human-readable breakdown
    diagnosis: str          # what's wrong, in plain language


@dataclass
class DiagnosticReport:
    """Full diagnostic report across all four orders."""
    orders: List[OrderScore]
    overall_score: float
    weakest: OrderScore
    strongest: OrderScore
    recommendation: str
    prescriptions: List["Prescription"]

    def summary(self) -> str:
        lines = ["═" * 60, "  GOODMAN DIAGNOSTIC REPORT", "═" * 60]
        for o in self.orders:
            lines.append(f"\n  {o.name} (Order {o.order})  {o.stars}  {o.score:.0%}")
            for k, v in o.components.items():
                bar = "█" * int(v * 10) + "░" * (10 - int(v * 10))
                lines.append(f"    {k:25s} [{bar}] {v:.0%}")
            lines.append(f"    → {o.diagnosis}")
        lines.append(f"\n{'─' * 60}")
        lines.append(f"  Weakest:  {self.weakest.name} ({self.weakest.score:.0%})")
        lines.append(f"  Strongest: {self.strongest.name} ({self.strongest.score:.0%})")
        lines.append(f"\n  RECOMMENDATION: {self.recommendation}")
        lines.append("═" * 60)
        return "\n".join(lines)

    @property
    def stars(self) -> dict:
        """Map order names to their star ratings."""
        return {o.name: o.stars for o in self.orders}


@dataclass
class Prescription:
    """Targeted exercises for a missing order."""
    order: int
    order_name: str
    focus: str
    exercises: List[str]
    rationale: str


# ── Constants ───────────────────────────────────────────────────────────────

ORDER_NAMES = {0: "POSITION", 1: "DIRECTION", 2: "CURVATURE", 3: "STRUCTURE"}

# Standard tendency-tone resolutions (semitone classes within an octave)
# Maps tendency tone -> its expected resolution (offset in semitones)
TENDENCY_RESOLUTIONS = {
    11: 0,   # leading tone → tonic (7→1)
    5: 7,    # 4→5 (in dominant context)
    6: 5,    # #4/b5 → 5 or 4
}

# Common scale patterns (interval sets from root, in semitones)
SCALES = {
    "major":       {0, 2, 4, 5, 7, 9, 11},
    "minor":       {0, 2, 3, 5, 7, 8, 10},
    "blues":       {0, 3, 5, 6, 7, 10},
    "pentatonic":  {0, 2, 4, 7, 9},
    "chromatic":   set(range(12)),
}

# ── Helpers ─────────────────────────────────────────────────────────────────

def _stars(score: float) -> str:
    n = max(0, min(5, round(score * 5)))
    return "★" * n + "☆" * (5 - n)


def _pitch_class(pitch: int, key: int) -> int:
    """Pitch class relative to key, 0–11."""
    return (pitch - key) % 12


def _detect_scale(pitches: List[int], key: int) -> Tuple[str, float]:
    """Best-guess scale from pitch distribution. Returns (name, fitness)."""
    pcs = {_pitch_class(p, key) for p in pitches}
    best_name, best_fit = "chromatic", 0.0
    for name, intervals in SCALES.items():
        if len(intervals) == 0:
            continue
        overlap = len(pcs & intervals)
        fitness = overlap / max(1, len(pcs))
        if fitness > best_fit:
            best_fit = fitness
            best_name = name
    return best_name, best_fit


def _quantize_to_grid(start: float, grid: float = 0.25) -> float:
    """Quantize a timestamp to the nearest grid point."""
    return round(start / grid) * grid


def _wrap_angle(angle: float) -> float:
    """Wrap angle to [-180, 180]."""
    while angle > 180:
        angle -= 360
    while angle <= -180:
        angle += 360
    return angle


def _normalize_notes(source: list) -> List[Note]:
    """
    Normalize any supported note format to Goodman's internal dict format.
    
    Accepts:
      - List of dicts:  [{'pitch': 60, 'velocity': 80, ...}, ...]
      - List of objects: [Note(pitch=60, ...), ...]  (any object with .pitch)
      - List of ints:   [60, 64, 67, 72]
    
    Returns list of dicts with keys: pitch, velocity, start, duration
    """
    if not source:
        return []

    normalized = []
    for i, item in enumerate(source):
        if isinstance(item, int):
            # Raw pitch int — assign sensible defaults
            normalized.append({
                "pitch": item,
                "velocity": 80,
                "start": float(i) * 0.5,
                "duration": 0.4,
            })
        elif isinstance(item, dict):
            n = {
                "pitch": item.get("pitch", 60),
                "velocity": item.get("velocity", 80),
                "start": item.get("start", item.get("start_time", float(i) * 0.5)),
                "duration": item.get("duration", 0.5),
            }
            normalized.append(n)
        elif hasattr(item, "pitch"):
            # Object with .pitch attribute (e.g. Note dataclass)
            normalized.append({
                "pitch": getattr(item, "pitch", 60),
                "velocity": getattr(item, "velocity", 80),
                "start": getattr(item, "start", getattr(item, "start_time", float(i) * 0.5)),
                "duration": getattr(item, "duration", 0.5),
            })
        else:
            raise TypeError(
                f"Cannot normalize note at index {i}: {item!r}. "
                "Expected int, dict, or note object with .pitch attribute."
            )
    return normalized


# ── The Engine ──────────────────────────────────────────────────────────────

class GoodmanEngine:
    """
    The diagnostic engine: feed it notes, get a clinical breakdown.
    
    Usage:
        engine = GoodmanEngine(key=60, scale="blues", bpm=120)
        report = engine.diagnose(notes)
        print(report.summary())
    """

    def __init__(self, key: int = 60, scale: str = "blues", bpm: float = 120.0,
                 terrain=None):
        """
        Args:
            key:      MIDI note number of the tonic (default C4=60).
            scale:    Scale name from SCALES keys (default "blues").
            bpm:      Tempo in beats per minute (for timing analysis).
            terrain:  Optional Terrain object — if provided, overrides scale.
        """
        self.key = key
        self.bpm = bpm
        self.beat_duration = 60.0 / bpm
        self.terrain = terrain

        if terrain is not None:
            # Derive scale degrees from terrain
            self.scale_pcs = {d.degree for d in terrain.scale_degrees}
            self.degree_weights = {d.degree: d.weight for d in terrain.scale_degrees}
        else:
            self.scale_pcs = SCALES.get(scale, SCALES["blues"])
            # Default weights: all equal
            self.degree_weights = {pc: 1.0 / len(self.scale_pcs) for pc in self.scale_pcs}
            # Boost roots, thirds, fifths
            for pc in [0, 4, 7]:
                if pc in self.degree_weights:
                    self.degree_weights[pc] = 0.2

    def diagnose(self, notes) -> DiagnosticReport:
        """
        Analyze a performance and return a full DiagnosticReport.
        
        Accepts any supported note format:
          - List of dicts:  [{'pitch': 60, 'velocity': 80, 'start': 0.0, 'duration': 0.5}, ...]
          - List of objects: [Note(pitch=60, ...), ...]
          - List of ints:   [60, 64, 67, 72]
        """
        notes = _normalize_notes(notes)
        if len(notes) < 4:
            return self._trivial_report("Need at least 4 notes for diagnosis.")

        # Sort by start time
        notes = sorted(notes, key=lambda n: n.get("start", 0))

        # Run all four diagnostics
        o0 = self._score_position(notes)
        o1 = self._score_direction(notes)
        o2 = self._score_curvature(notes)
        o3 = self._score_structure(notes)

        orders = [o0, o1, o2, o3]
        weakest = min(orders, key=lambda o: o.score)
        strongest = max(orders, key=lambda o: o.score)
        overall = sum(o.score for o in orders) / 4

        recommendation = self._make_recommendation(weakest)
        prescriptions = self._prescribe_all(orders)

        return DiagnosticReport(
            orders=orders,
            overall_score=overall,
            weakest=weakest,
            strongest=strongest,
            recommendation=recommendation,
            prescriptions=prescriptions,
        )

    def diagnose_midi_file(self, filepath: str) -> DiagnosticReport:
        """Load and analyze a MIDI file."""
        notes = self._load_midi(filepath)
        return self.diagnose(notes)

    # ── 0th Order: POSITION ────────────────────────────────────────────

    def _score_position(self, notes: List[Note]) -> OrderScore:
        """
        POSITION: Do you know where you are?
        
        Metrics:
          - Scale adherence:  % of notes in the correct scale
          - Strong-degree hit: % of notes on weighted degrees (roots, 3rds, 5ths)
          - Range usage:      how much of the available range is used
          - Pitch entropy:    is pitch distribution focused or scattered
        """
        pitches = [n["pitch"] for n in notes]
        pcs = [_pitch_class(p, self.key) for p in pitches]
        total = len(pitches)

        # 1. Scale adherence
        on_scale = sum(1 for pc in pcs if pc in self.scale_pcs)
        scale_adherence = on_scale / total if total else 0

        # 2. Strong-degree hit rate
        strong_threshold = 0.15
        strong_degrees = {pc for pc, w in self.degree_weights.items() if w >= strong_threshold}
        on_strong = sum(1 for pc in pcs if pc in strong_degrees)
        strong_hit = on_strong / total if total else 0

        # 3. Range usage (0.0 = one note, 1.0 = full practical range)
        min_p, max_p = min(pitches), max(pitches)
        actual_range = max_p - min_p
        practical_range = 24  # 2 octaves is "full usage"
        range_usage = min(1.0, actual_range / practical_range) if practical_range else 0

        # 4. Pitch-class entropy (normalized; higher = more spread)
        pc_counts = Counter(pcs)
        entropy = 0.0
        for count in pc_counts.values():
            p = count / total
            entropy -= p * math.log2(p) if p > 0 else 0
        max_entropy = math.log2(12)
        pitch_entropy = entropy / max_entropy if max_entropy else 0
        # We want moderate entropy (not all one note, not perfectly even)
        # Ideal: ~0.7–0.9 of max entropy (focused but not monotonous)
        entropy_score = 1.0 - abs(pitch_entropy - 0.8) / 0.8
        entropy_score = max(0.0, min(1.0, entropy_score))

        # Composite
        score = (
            scale_adherence * 0.40 +
            strong_hit * 0.25 +
            range_usage * 0.20 +
            entropy_score * 0.15
        )

        # Diagnosis
        if scale_adherence < 0.6:
            diagnosis = ("You're playing notes that don't belong to this tradition. "
                         "Learn the scale first.")
        elif strong_hit < 0.3:
            diagnosis = ("You're in the scale but missing the landing points. "
                         "Aim for roots, 3rds, and 5ths on strong beats.")
        elif range_usage < 0.3:
            diagnosis = ("You're camping in one register. Explore the full range.")
        else:
            diagnosis = "Solid note choices for this terrain."

        components = {
            "Scale adherence": round(scale_adherence, 3),
            "Strong degree hit": round(strong_hit, 3),
            "Range usage": round(range_usage, 3),
            "Pitch distribution": round(entropy_score, 3),
        }

        return OrderScore(
            order=0, name="POSITION", score=round(score, 3),
            stars=_stars(score), components=components,
            detail=f"{scale_adherence:.0%} on scale, {strong_hit:.0%} on strong degrees, "
                   f"range: {actual_range} semitones",
            diagnosis=diagnosis,
        )

    # ── 1st Order: DIRECTION ────────────────────────────────────────────

    def _score_direction(self, notes: List[Note]) -> OrderScore:
        """
        DIRECTION: Do you know where you're going?
        
        Metrics:
          - Interval coherence: are intervals musically sensible?
          - Voice leading:      are transitions smooth?
          - Tendency resolution: do tendency tones resolve?
          - Phrase shape:       do phrases have arcs (rise → peak → fall)?
        """
        if len(notes) < 3:
            return self._order_score(1, 0.5, {}, "Not enough notes.", "Insufficient data.")

        pitches = [n["pitch"] for n in notes]
        starts = [n.get("start", 0) for n in notes]
        durations = [n.get("duration", 0.5) for n in notes]

        # 1. Interval coherence: penalize jumps > 9 semitones, reward steps
        intervals = [pitches[i+1] - pitches[i] for i in range(len(pitches) - 1)]
        if not intervals:
            return self._order_score(1, 0.5, {}, "No intervals.", "Insufficient data.")

        step_count = sum(1 for iv in intervals if abs(iv) <= 2)   # steps
        leap_count = sum(1 for iv in intervals if abs(iv) >= 7)   # large leaps
        step_ratio = step_count / len(intervals)
        leap_ratio = leap_count / len(intervals)
        interval_coherence = step_ratio * 0.7 + (1.0 - leap_ratio) * 0.3
        interval_coherence = max(0.0, min(1.0, interval_coherence))

        # 2. Voice leading: average interval size (smaller = smoother)
        avg_interval = sum(abs(iv) for iv in intervals) / len(intervals)
        # Ideal: 2–3 semitones average
        voice_leading = 1.0 - abs(avg_interval - 2.5) / 8.0
        voice_leading = max(0.0, min(1.0, voice_leading))

        # 3. Tendency tone resolution
        pcs = [_pitch_class(p, self.key) for p in pitches]
        tendency_opportunities = 0
        tendency_resolved = 0
        for i in range(len(pcs) - 1):
            pc = pcs[i]
            next_pc = pcs[i + 1]
            if pc in TENDENCY_RESOLUTIONS:
                expected = TENDENCY_RESOLUTIONS[pc]
                tendency_opportunities += 1
                # Check if the next note resolves by step in the expected direction
                actual_motion = (next_pc - pc) % 12
                if actual_motion == expected % 12 or abs(next_pc - pc) <= 2:
                    tendency_resolved += 1

        tendency_score = tendency_resolved / tendency_opportunities if tendency_opportunities else 0.7  # neutral if no opportunities

        # 4. Phrase shape: detect phrases and check for arcs
        phrases = self._detect_phrases(notes)
        arc_count = 0
        for phrase in phrases:
            if len(phrase) < 4:
                continue
            pp = [n["pitch"] for n in phrase]
            mid = len(pp) // 2
            # Check if there's a peak roughly in the middle third
            peak_idx = pp.index(max(pp))
            third = len(pp) // 3
            if third <= peak_idx <= len(pp) - third:
                arc_count += 1

        phrase_arc = arc_count / len(phrases) if phrases else 0.5

        # Composite
        score = (
            interval_coherence * 0.25 +
            voice_leading * 0.25 +
            tendency_score * 0.25 +
            phrase_arc * 0.25
        )

        # Diagnosis
        if interval_coherence < 0.4:
            diagnosis = ("Your lines jump around randomly. Practice stepwise motion "
                         "and connecting intervals logically.")
        elif tendency_score < 0.4:
            diagnosis = ("You're not resolving tendency tones. The 7th wants to go to 1, "
                         "the 4th wants to go to 3. Honor the gravity.")
        elif phrase_arc < 0.3:
            diagnosis = ("Your phrases don't have clear shape — no rise, peak, and fall. "
                         "Think about where each phrase is heading.")
        else:
            diagnosis = "Melodic lines have good direction and shape."

        components = {
            "Interval coherence": round(interval_coherence, 3),
            "Voice leading": round(voice_leading, 3),
            "Tendency resolution": round(tendency_score, 3),
            "Phrase shape": round(phrase_arc, 3),
        }

        return OrderScore(
            order=1, name="DIRECTION", score=round(score, 3),
            stars=_stars(score), components=components,
            detail=f"Avg interval: {avg_interval:.1f} semitones, "
                   f"phrases: {len(phrases)}, arcs: {arc_count}/{len(phrases)}",
            diagnosis=diagnosis,
        )

    # ── 2nd Order: CURVATURE ────────────────────────────────────────────

    def _score_curvature(self, notes: List[Note]) -> OrderScore:
        """
        CURVATURE: Do you know how the direction is changing?
        
        Metrics:
          - Rhythmic variety:  are durations varied or monotonous?
          - Dynamic shape:     do velocity changes create emotional arcs?
          - Microtiming:       are you ahead/behind/on the beat? Consistent?
          - Tonal weight:      do important notes get more emphasis?
        """
        if len(notes) < 4:
            return self._order_score(2, 0.5, {}, "Not enough notes.", "Insufficient data.")

        velocities = [n.get("velocity", 80) for n in notes]
        durations = [n.get("duration", 0.5) for n in notes]
        starts = [n.get("start", 0) for n in notes]
        pitches = [n["pitch"] for n in notes]

        # 1. Rhythmic variety (entropy of duration values, quantized)
        grid = self.beat_duration / 4  # 16th note grid
        quant_durs = [round(d / grid) * grid for d in durations]
        dur_counts = Counter(quant_durs)
        dur_entropy = 0.0
        total = len(quant_durs)
        for count in dur_counts.values():
            p = count / total
            dur_entropy -= p * math.log2(p) if p > 0 else 0
        max_dur_entropy = math.log2(min(8, total))  # cap at 8 distinct durations
        rhythmic_variety = dur_entropy / max_dur_entropy if max_dur_entropy else 0
        rhythmic_variety = min(1.0, rhythmic_variety)

        # 2. Dynamic shape (velocity arc over the performance)
        vel_range = max(velocities) - min(velocities)
        dynamic_range_score = min(1.0, vel_range / 50.0)  # 50+ = full score

        # Check if there's a dynamic arc (louder in middle/end)
        third = len(velocities) // 3
        if third > 0:
            avg_start = sum(velocities[:third]) / third
            avg_mid = sum(velocities[third:third*2]) / third
            avg_end = sum(velocities[third*2:]) / max(1, len(velocities) - third*2)
            # Good: some section is louder (creates arc)
            has_arc = (avg_mid > avg_start or avg_end > avg_start)
            dynamic_arc = 0.7 if has_arc else 0.3
            # Bonus for climax
            climax_third = velocities.index(max(velocities)) // max(1, third)
            if climax_third == 1 or climax_third == 2:  # climax in middle or late
                dynamic_arc = min(1.0, dynamic_arc + 0.2)
        else:
            dynamic_arc = 0.5

        dynamic_shape = dynamic_range_score * 0.5 + dynamic_arc * 0.5

        # 3. Microtiming: consistency of placement relative to grid
        microtimings = []
        for i, start in enumerate(starts):
            grid_pos = _quantize_to_grid(start, grid)
            offset = start - grid_pos  # positive = late, negative = early
            microtimings.append(offset)

        if microtimings:
            avg_offset = sum(microtimings) / len(microtimings)
            offset_std = math.sqrt(
                sum((m - avg_offset) ** 2 for m in microtimings) / len(microtimings)
            )
            # Good microtiming: consistent placement (low std)
            # std < 0.05 beats = very tight, 0.1 = decent, 0.2+ = sloppy
            consistency = 1.0 - min(1.0, offset_std / (self.beat_duration * 0.15))
            consistency = max(0.0, consistency)

            # Is the average offset deliberate? (consistent laid-back or pushed)
            deliberate = 1.0 if abs(avg_offset) > 0.01 and consistency > 0.5 else 0.5
            microtiming_score = consistency * 0.7 + deliberate * 0.3
        else:
            microtiming_score = 0.5
            avg_offset = 0
            offset_std = 0

        # 4. Tonal weight: important notes (strong degrees, peaks) get emphasis
        pcs = [_pitch_class(p, self.key) for p in pitches]
        on_strong = [i for i, pc in enumerate(pcs) if pc in {0, 4, 7}]
        if on_strong:
            avg_vel_strong = sum(velocities[i] for i in on_strong) / len(on_strong)
            avg_vel_all = sum(velocities) / len(velocities)
            vel_diff = avg_vel_strong - avg_vel_all
            # Strong degrees should be slightly louder (+5 to +15 is ideal)
            tonal_weight = 0.5 + min(0.5, max(-0.5, vel_diff / 20.0))
        else:
            tonal_weight = 0.5

        # Composite
        score = (
            rhythmic_variety * 0.25 +
            dynamic_shape * 0.25 +
            microtiming_score * 0.30 +
            tonal_weight * 0.20
        )

        # Diagnosis
        if rhythmic_variety < 0.3:
            diagnosis = ("You're playing with robotic rhythm — all the same durations. "
                         "Mix long notes with short, add syncopation.")
        elif dynamic_shape < 0.3:
            diagnosis = ("Everything's the same volume. Music needs loud and soft — "
                         "shape your phrases with dynamics.")
        elif microtiming_score < 0.4:
            diagnosis = ("Your time feel is inconsistent. You're not locked into the groove. "
                         "Play along with records until your timing is solid.")
        else:
            diagnosis = "Good feel and dynamics."

        components = {
            "Rhythmic variety": round(rhythmic_variety, 3),
            "Dynamic shape": round(dynamic_shape, 3),
            "Microtiming": round(microtiming_score, 3),
            "Tonal weight": round(tonal_weight, 3),
        }

        placement = "behind" if avg_offset > 0.02 else ("ahead" if avg_offset < -0.02 else "on")
        return OrderScore(
            order=2, name="CURVATURE", score=round(score, 3),
            stars=_stars(score), components=components,
            detail=f"Timing: {placement} the beat (avg {avg_offset*1000:.0f}ms), "
                   f"consistency σ={offset_std*1000:.0f}ms, "
                   f"dynamic range: {vel_range}",
            diagnosis=diagnosis,
        )

    # ── 3rd Order: STRUCTURE ────────────────────────────────────────────

    def _score_structure(self, notes: List[Note]) -> OrderScore:
        """
        STRUCTURE: Is the whole thing holding together?
        
        Metrics:
          - Phrase count:      enough phrases to form a narrative?
          - Motivic development: do you develop ideas or just play new ones?
          - Repetition ratio:   balance of repeated vs novel material
          - Overall arc:        does the full performance have a climax shape?
        """
        if len(notes) < 8:
            return self._order_score(3, 0.5, {}, "Not enough notes.", "Insufficient data.")

        pitches = [n["pitch"] for n in notes]
        starts = [n.get("start", 0) for n in notes]
        durations = [n.get("duration", 0.5) for n in notes]
        velocities = [n.get("velocity", 80) for n in notes]
        total_dur = sum(durations)

        # 1. Phrase count (groups separated by gaps)
        phrases = self._detect_phrases(notes)
        phrase_count = len(phrases)

        # Ideal: 4–12 phrases for a solo
        if 4 <= phrase_count <= 12:
            phrase_count_score = 1.0
        elif 2 <= phrase_count <= 16:
            phrase_count_score = 0.6
        else:
            phrase_count_score = 0.3

        # 2. Motivic development: compare pitch sequences across phrases
        # Use pitch-class contours as motif signatures
        if phrase_count >= 2:
            motifs = []
            for phrase in phrases:
                pp = [n["pitch"] for n in phrase]
                # Interval contour (direction only: +, -, =)
                contour = tuple(
                    "+" if pp[i+1] > pp[i] else ("-" if pp[i+1] < pp[i] else "=")
                    for i in range(len(pp) - 1)
                )
                motifs.append(contour)

            # Count how many motifs are similar (share prefix of length 3+)
            similar_pairs = 0
            total_pairs = 0
            for i in range(len(motifs)):
                for j in range(i + 1, len(motifs)):
                    total_pairs += 1
                    # Compare first 3 intervals
                    prefix_len = min(3, len(motifs[i]), len(motifs[j]))
                    if prefix_len >= 2:
                        shared = sum(
                            1 for k in range(prefix_len)
                            if motifs[i][k] == motifs[j][k]
                        )
                        if shared >= prefix_len * 0.6:
                            similar_pairs += 1

            motivic_score = similar_pairs / total_pairs if total_pairs else 0.5
            # Ideal: 30–60% similarity (enough development, not repetition)
            motivic_dev = 1.0 - abs(motivic_score - 0.45) / 0.55
            motivic_dev = max(0.0, min(1.0, motivic_dev))
        else:
            motivic_dev = 0.3
            motivic_score = 0.0

        # 3. Repetition vs novelty
        # Look at pitch-class trigrams
        pcs = [_pitch_class(p, self.key) for p in pitches]
        trigrams = [tuple(pcs[i:i+3]) for i in range(len(pcs) - 2)]
        if trigrams:
            unique_trigrams = len(set(trigrams))
            repetition_ratio = 1.0 - (unique_trigrams / len(trigrams))
            # Ideal: 20–50% repetition
            rep_score = 1.0 - abs(repetition_ratio - 0.35) / 0.65
            rep_score = max(0.0, min(1.0, rep_score))
        else:
            rep_score = 0.5
            repetition_ratio = 0.0

        # 4. Overall arc: pitch + velocity across the whole performance
        quarters = 4
        seg_len = max(1, len(pitches) // quarters)
        segments_pitch = []
        segments_vel = []
        for q in range(quarters):
            start_i = q * seg_len
            end_i = min((q + 1) * seg_len, len(pitches))
            if start_i < end_i:
                segments_pitch.append(sum(pitches[start_i:end_i]) / (end_i - start_i))
                segments_vel.append(sum(velocities[start_i:end_i]) / (end_i - start_i))
            else:
                segments_pitch.append(pitches[-1])
                segments_vel.append(velocities[-1])

        # Good arc: rises then falls, or builds to a climax
        has_pitch_arc = False
        has_vel_arc = False
        if len(segments_pitch) >= 3:
            # Peak in middle or late-middle
            peak_q = segments_pitch.index(max(segments_pitch))
            has_pitch_arc = 0 < peak_q < len(segments_pitch) - 1

            peak_vq = segments_vel.index(max(segments_vel))
            has_vel_arc = 0 < peak_vq < len(segments_vel) - 1

        arc_score = (
            (0.6 if has_pitch_arc else 0.2) +
            (0.4 if has_vel_arc else 0.1)
        )

        # Composite
        score = (
            phrase_count_score * 0.15 +
            motivic_dev * 0.30 +
            rep_score * 0.25 +
            arc_score * 0.30
        )

        # Diagnosis
        if motivic_dev < 0.3:
            diagnosis = ("You're not developing ideas — every phrase is completely new. "
                         "Try repeating and varying a motif across phrases.")
        elif rep_score < 0.2:
            diagnosis = ("Almost no repetition. A solo needs callbacks — things the "
                         "listener can recognize. Play something, then bring it back.")
        elif arc_score < 0.3:
            diagnosis = ("The solo doesn't have a shape. Think beginning → development → "
                         "climax → resolution. The whole thing is one flat line.")
        else:
            diagnosis = "Good structural shape and motivic development."

        components = {
            "Phrase count": round(phrase_count_score, 3),
            "Motivic development": round(motivic_dev, 3),
            "Repetition/novelty": round(rep_score, 3),
            "Overall arc": round(arc_score, 3),
        }

        return OrderScore(
            order=3, name="STRUCTURE", score=round(score, 3),
            stars=_stars(score), components=components,
            detail=f"Phrases: {phrase_count}, motif similarity: {motivic_score:.0%}, "
                   f"repetition: {repetition_ratio:.0%}, arc: {'yes' if arc_score > 0.5 else 'flat'}",
            diagnosis=diagnosis,
        )

    # ── Phrase Detection ────────────────────────────────────────────────

    def _detect_phrases(self, notes: List[Note]) -> List[List[Note]]:
        """
        Split notes into phrases based on gaps (rests).
        A gap > 1 beat duration = phrase boundary.
        """
        if not notes:
            return []

        threshold = self.beat_duration * 0.75  # 3/4 of a beat = phrase break
        phrases = []
        current = [notes[0]]

        for i in range(1, len(notes)):
            prev_end = notes[i-1].get("start", 0) + notes[i-1].get("duration", 0.5)
            curr_start = notes[i].get("start", 0)
            gap = curr_start - prev_end

            if gap > threshold:
                if current:
                    phrases.append(current)
                current = [notes[i]]
            else:
                current.append(notes[i])

        if current:
            phrases.append(current)

        return phrases

    # ── Recommendation Engine ───────────────────────────────────────────

    def _make_recommendation(self, weakest: OrderScore) -> str:
        """Generate targeted recommendation based on weakest order."""
        recs = {
            0: ("You're missing 0th order — POSITION. You don't have the notes yet. "
                "Learn the scale cold. Practice scale-degree drills until hitting the "
                "right pitches is automatic. Everything else is built on this."),
            1: ("You have the notes but you're missing 1st order — DIRECTION. "
                "Your lines wander instead of going somewhere. Practice call-and-response: "
                "sing a phrase, then play it. Think about where each phrase is heading "
                "before you play it."),
            2: ("You have the notes and the direction, but you're missing 2nd order — "
                "CURVATURE. It doesn't FEEL right. Play along with records. Focus purely "
                "on matching the time feel — are you ahead, behind, or on? Practice "
                "laying back on the beat, pushing forward, playing rubato. Dynamics too: "
                "shape every phrase with loud and soft."),
            3: ("Everything sounds good in the moment but you're missing 3rd order — "
                "STRUCTURE. The solo doesn't tell a story. Study great solos: where's the "
                "climax? What gets repeated? Practice playing a motif, then varying it "
                "across a solo. Think about the whole journey, not just the next note."),
        }
        return recs.get(weakest.order, "Keep practicing!")

    # ── Prescription Engine ─────────────────────────────────────────────

    def prescribe(self, missing_order: int, **kwargs) -> Prescription:
        """Get exercises for a specific missing order."""
        # Build placeholder orders
        names = ["POSITION", "DIRECTION", "CURVATURE", "STRUCTURE"]
        if missing_order < 0 or missing_order >= 4:
            raise ValueError(f"missing_order must be 0-3")
        o = OrderScore(
            order=missing_order,
            name=names[missing_order],
            score=0.0,
            stars="☆☆☆☆☆",
            components={},
            detail="(prescription for specific order)",
            diagnosis="Targeted practice recommended",
        )
        return self._prescribe(o)

    def _prescribe_all(self, orders: List[OrderScore]) -> List[Prescription]:
        """Generate prescriptions, prioritizing weakest orders."""
        # Sort by score ascending (weakest first)
        sorted_orders = sorted(orders, key=lambda o: o.score)
        prescriptions = []

        for o in sorted_orders:
            if o.score >= 0.7:
                continue  # Don't prescribe for strong areas
            prescriptions.append(self._prescribe(o))

        # If all strong, give one maintenance prescription
        if not prescriptions:
            prescriptions.append(Prescription(
                order=-1,
                order_name="MAINTENANCE",
                focus="General",
                exercises=[
                    "Transcribe a solo by ear",
                    "Play along with a recording you've never heard",
                    "Record yourself and listen back critically",
                ],
                rationale="All orders are strong. Focus on expanding vocabulary and staying honest."
            ))

        return prescriptions

    def _prescribe(self, order: OrderScore) -> Prescription:
        """Generate specific exercises for a weak order."""
        # Pick exercises based on which sub-component is weakest
        if order.components:
            weakest_component = min(order.components, key=order.components.get)
        else:
            weakest_component = "general"

        exercise_map = {
            0: {
                "default": [
                    "Play the scale ascending and descending, 5 minutes daily",
                    "Random scale-degree drill: call out a degree, find it instantly",
                    "Play only on strong degrees (1, 3, 5) for a full chorus",
                    "Target note practice: pick 3 notes, solo using ONLY those 3",
                ],
                "Scale adherence": [
                    "Write out the scale. Play it in all 12 keys.",
                    "Play a chord tone on every strong beat, fill with passing tones",
                    "Record yourself playing freely, then count how many notes are out of scale",
                ],
                "Range usage": [
                    "Play the scale in each octave you can reach",
                    "Practice wide interval jumps within the scale",
                    "Solo with the rule: each phrase must go higher than the last",
                ],
            },
            1: {
                "default": [
                    "Sing a melodic phrase, then play it on your instrument",
                    "Call-and-response with a recording: echo what you hear",
                    "Melodic dictation: listen to a phrase, write it out, play it",
                    "Play phrases that start low and end high, then reverse",
                ],
                "Tendency resolution": [
                    "Practice resolving the 7th to the root, 4th to the 3rd",
                    "Play a tendency tone and HOLD it — feel the tension — then resolve",
                    "Solo where every phrase ends on a resolution, not a tension note",
                ],
                "Phrase shape": [
                    "Play phrases with exactly 4, 8, and 12 notes",
                    "Each phrase must have a clear peak note (highest or loudest)",
                    "Practice phrases that rise for 3 notes then fall for 3 notes",
                ],
            },
            2: {
                "default": [
                    "Play along with a recording and match the soloist's time feel exactly",
                    "Set a metronome to 60bpm, play ONLY on beats 2 and 4",
                    "Practice laying back (play 30ms behind the beat) consistently",
                    "Play a simple phrase 10 times, each time with different dynamics",
                ],
                "Rhythmic variety": [
                    "Tap a rhythm, then play it. Vary: quarter, eighth, triplet, sixteenth",
                    "Practice playing in 3 against a 4/4 backing track",
                    "Solo using only 2 distinct rhythm patterns, alternate between them",
                ],
                "Dynamic shape": [
                    "Play a scale pp, then mf, then ff — feel each level",
                    "Practice crescendo through a phrase, decrescendo through the next",
                    "Play with extreme dynamics: whisper-quiet to full blast",
                ],
                "Microtiming": [
                    "Record yourself with a click. Are you ahead or behind? By how much?",
                    "Practice playing exactly ON the beat (with metronome) for 5 minutes",
                    "Then practice laying back 50ms behind for 5 minutes",
                    "Then practice pushing 50ms ahead for 5 minutes",
                ],
            },
            3: {
                "default": [
                    "Analyze a great solo: map out phrases, motifs, climax",
                    "Play a 3-chorus solo where chorus 1 = simple, chorus 2 = develop, chorus 3 = peak",
                    "Compose a solo beforehand, then play it from memory",
                    "Record a solo, transcribe your best ideas, build on them next time",
                ],
                "Motivic development": [
                    "Play a 3-note motif. Now play it 5 different ways (transpose, invert, retrograde)",
                    "Solo where you MUST reference your opening idea at least 3 times",
                    "Take a classic lick and develop it across 4 bars",
                ],
                "Overall arc": [
                    "Plan your solo: write 'quiet → building → climax → resolution' and follow it",
                    "Practice 2-chorus solos where the energy MUST increase each chorus",
                    "Listen to Coltrane's 'Giant Steps' solo — notice the arc",
                ],
            },
        }

        order_exercises = exercise_map.get(order.order, {})
        exercises = order_exercises.get(weakest_component, order_exercises.get("default", []))

        component_pct = order.components.get(weakest_component, 0)

        rationale = {
            0: f"Your weakest area is '{weakest_component}' ({component_pct:.0%}). "
               "These exercises will build automatic pitch selection.",
            1: f"Your weakest area is '{weakest_component}' ({component_pct:.0%}). "
               "These exercises will build directional awareness in your lines.",
            2: f"Your weakest area is '{weakest_component}' ({component_pct:.0%}). "
               "These exercises will develop your time feel and dynamic control.",
            3: f"Your weakest area is '{weakest_component}' ({component_pct:.0%}). "
               "These exercises will build your structural and architectural awareness.",
        }.get(order.order, "Practice these exercises to improve.")

        return Prescription(
            order=order.order,
            order_name=order.name,
            focus=weakest_component,
            exercises=exercises,
            rationale=rationale,
        )

    # ── Utility ─────────────────────────────────────────────────────────

    def _order_score(self, order: int, score: float,
                     components: Dict[str, float],
                     detail: str, diagnosis: str) -> OrderScore:
        return OrderScore(
            order=order, name=ORDER_NAMES[order], score=score,
            stars=_stars(score), components=components,
            detail=detail, diagnosis=diagnosis,
        )

    def _trivial_report(self, reason: str) -> DiagnosticReport:
        o = OrderScore(order=-1, name="N/A", score=0, stars="☆☆☆☆☆",
                       components={}, detail=reason, diagnosis=reason)
        return DiagnosticReport(
            orders=[o], overall_score=0, weakest=o, strongest=o,
            recommendation=reason, prescriptions=[],
        )

    def _load_midi(self, filepath: str) -> List[Note]:
        """Load notes from a MIDI file."""
        try:
            import mido
            mid = mido.MidiFile(filepath)
            notes: List[Note] = []
            active: Dict[int, Tuple[float, int]] = {}  # note -> (start_time, velocity)
            t = 0.0

            for track in mid.tracks:
                t = 0.0
                for msg in track:
                    t += msg.time / mid.ticks_per_beat
                    if msg.type == 'note_on' and msg.velocity > 0:
                        active[msg.note] = (round(t, 4), msg.velocity)
                    elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                        if msg.note in active:
                            start, vel = active.pop(msg.note)
                            dur = round(t - start, 4)
                            if dur > 0:
                                notes.append({
                                    "pitch": msg.note,
                                    "velocity": vel,
                                    "start": start,
                                    "duration": dur,
                                })

            notes.sort(key=lambda n: n["start"])
            return notes
        except ImportError:
            raise ImportError("Install mido for MIDI support: pip install mido")
        except Exception as e:
            raise ValueError(f"Could not parse MIDI file: {e}")


# ── Standalone / Quick Test ─────────────────────────────────────────────────

if __name__ == "__main__":
    import random

    # Generate a test performance: blues scale, varying quality
    random.seed(42)
    key = 60  # C

    # Build a plausible blues solo
    blues_scale = [0, 3, 5, 6, 7, 10]  # relative to key
    notes = []
    t = 0.0
    for i in range(80):
        # Mostly scale notes with occasional "wrong" notes
        if random.random() < 0.15:
            pitch = key + random.randint(0, 24)
        else:
            octave = random.choice([0, 12])
            pitch = key + octave + random.choice(blues_scale)

        vel = 60 + int(30 * math.sin(i / 10.0) + random.randint(-10, 10))
        vel = max(30, min(127, vel))
        dur = random.choice([0.25, 0.5, 0.5, 0.5, 1.0])

        notes.append({
            "pitch": pitch,
            "velocity": vel,
            "start": round(t, 3),
            "duration": dur,
        })
        t += dur

    engine = GoodmanEngine(key=key, scale="blues", bpm=120)
    report = engine.diagnose(notes)
    print(report.summary())

    print("\n\n📋 PRESCRIPTIONS:")
    for p in report.prescriptions:
        print(f"\n  [{p.order_name}] Focus: {p.focus}")
        print(f"  {p.rationale}")
        for ex in p.exercises:
            print(f"    • {ex}")
