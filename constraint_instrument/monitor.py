"""
The Monitor — the invisible engineer.

Like a monitor engineer at a concert who rides the faders so
smoothly nobody notices, the Monitor wraps any Instrument mode
and provides adaptive, invisible assistance.

When the performer is in flow, the monitor goes silent.
When they're struggling, it offers the gentlest possible nudge —
not a correction, but a reshaping of possibilities so the
next choice naturally lands better.

"The depth sounder you stop looking at."
"""

import math
import random
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Deque, Dict, List, Optional, Tuple

from .instrument import Instrument


# ── Data Classes ──────────────────────────────────────────────────────

@dataclass
class PerformerSnapshot:
    """A snapshot of the performer's state at a moment in time."""
    timestamp: float
    notes: List[dict]
    error_rate: float          # 0=perfect, 1=disastrous
    consistency: float         # 0=chaotic, 1=rock-solid
    exploration_velocity: float  # how fast they're exploring new territory
    register: Tuple[float, float]  # current pitch range (low, high)
    mean_interval: float       # average interval between notes
    rhythmic_stability: float  # 0=erratic, 1=steady


@dataclass
class FlowAssessment:
    """The monitor's assessment of the performer's flow state."""
    flow_score: float          # 0.0 = struggling, 1.0 = deep flow
    confidence: float          # how confident the assessment is
    should_intervene: bool     # whether the monitor should act
    intervention_type: Optional[str]  # kind of nudge, if any
    reason: str                # human-readable explanation


@dataclass
class LearnedTendencies:
    """What the monitor has learned about the performer."""
    favorite_intervals: Dict[int, float] = field(default_factory=dict)
    register_preference: Tuple[float, float] = (55.0, 79.0)
    rhythmic_patterns: List[List[float]] = field(default_factory=list)
    average_velocity: float = 80.0
    phrase_length_preference: float = 8.0
    temporal_density: float = 0.5   # notes per second
    exploration_style: str = "moderate"  # "cautious", "moderate", "adventurous"
    sample_count: int = 0


@dataclass
class MonitorReport:
    """A report from the monitor — mostly for debugging/insight."""
    flow_state: float
    sensitivity: float
    snapshots_analyzed: int
    interventions_total: int
    tendencies: LearnedTendencies
    is_vanished: bool
    assessment: FlowAssessment


# ── Flow Detection ────────────────────────────────────────────────────

def _compute_error_rate(notes: List[dict], terrain) -> float:
    """
    Estimate error rate from note data.
    Errors = out-of-range pitches, velocity spikes, timing irregularities.
    """
    if not notes:
        return 0.0

    errors = 0
    total = len(notes)

    # Check register bounds (soft)
    low, high = terrain.register_tendency
    for n in notes:
        pitch = n.get("pitch", 60)
        if pitch < low - 12 or pitch > high + 12:
            errors += 1

    # Check velocity consistency
    velocities = [n.get("velocity", 80) for n in notes]
    if velocities:
        vel_std = _std(velocities)
        if vel_std > 30:
            errors += total * 0.1

    # Check timing regularity
    starts = sorted([n.get("start", 0) for n in notes])
    if len(starts) > 2:
        gaps = [starts[i+1] - starts[i] for i in range(len(starts) - 1)]
        gap_std = _std(gaps)
        mean_gap = _mean(gaps) if gaps else 1.0
        if mean_gap > 0:
            cv = gap_std / mean_gap  # coefficient of variation
            if cv > 1.0:
                errors += total * 0.15

    return min(1.0, errors / max(1, total))


def _compute_consistency(notes: List[dict]) -> float:
    """
    Consistency: how regular and coherent the playing is.
    High consistency = repeating patterns, steady tempo, even dynamics.
    """
    if len(notes) < 3:
        return 0.5

    # Timing consistency
    starts = sorted([n.get("start", 0) for n in notes])
    gaps = [starts[i+1] - starts[i] for i in range(len(starts) - 1) if starts[i+1] - starts[i] > 0]
    if not gaps:
        return 0.5

    mean_gap = _mean(gaps)
    gap_cv = _std(gaps) / mean_gap if mean_gap > 0 else 1.0
    timing_score = max(0, 1.0 - gap_cv)

    # Dynamic consistency
    velocities = [n.get("velocity", 80) for n in notes]
    vel_cv = _std(velocities) / _mean(velocities) if _mean(velocities) > 0 else 1.0
    dynamic_score = max(0, 1.0 - vel_cv)

    # Interval consistency (repeating patterns)
    pitches = [n.get("pitch", 60) for n in notes]
    intervals = [pitches[i+1] - pitches[i] for i in range(len(pitches) - 1)]
    if len(intervals) >= 4:
        # Check for repeating 3-note interval patterns
        pattern_match = 0
        pattern_total = 0
        for i in range(len(intervals) - 3):
            pattern = intervals[i:i+3]
            for j in range(i + 3, min(i + 12, len(intervals) - 2)):
                candidate = intervals[j:j+3]
                if pattern == candidate:
                    pattern_match += 1
                pattern_total += 1
        pattern_score = pattern_match / max(1, pattern_total) * 5  # scale up
        pattern_score = min(1.0, pattern_score)
    else:
        pattern_score = 0.5

    return (timing_score * 0.4 + dynamic_score * 0.3 + pattern_score * 0.3)


def _compute_exploration_velocity(notes: List[dict], history: List[List[dict]]) -> float:
    """
    How fast is the performer exploring new territory?
    Compares current notes against history to find novelty.
    """
    if not notes or not history:
        return 0.5

    current_pitches = set(n.get("pitch", 60) for n in notes)

    # Collect historical pitches
    historical_pitches = set()
    for past_notes in history[-10:]:  # last 10 performances
        for n in past_notes:
            historical_pitches.add(n.get("pitch", 60))

    # Novelty = fraction of current pitches not in history
    if not current_pitches:
        return 0.0

    novel = current_pitches - historical_pitches
    novelty_ratio = len(novel) / len(current_pitches)

    # Also consider interval novelty
    current_intervals = set()
    pitches = sorted([n.get("pitch", 60) for n in notes])
    for i in range(len(pitches) - 1):
        current_intervals.add(abs(pitches[i+1] - pitches[i]))

    historical_intervals = set()
    for past_notes in history[-10:]:
        pp = sorted([n.get("pitch", 60) for n in past_notes])
        for i in range(len(pp) - 1):
            historical_intervals.add(abs(pp[i+1] - pp[i]))

    if current_intervals:
        novel_intervals = current_intervals - historical_intervals
        interval_novelty = len(novel_intervals) / len(current_intervals)
    else:
        interval_novelty = 0.0

    return min(1.0, novelty_ratio * 0.6 + interval_novelty * 0.4)


# ── Helpers ───────────────────────────────────────────────────────────

def _mean(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _std(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = _mean(values)
    variance = sum((v - m) ** 2 for v in values) / len(values)
    return math.sqrt(variance)


# ── The Monitor ───────────────────────────────────────────────────────

class Monitor:
    """
    The invisible engineer. Wraps any Instrument mode.

    Tracks the performer's state and provides minimal,
    adaptive assistance. When the performer is in flow,
    the monitor goes silent. When they're struggling,
    it offers the gentlest possible correction.
    """

    def __init__(self, instrument: Instrument, sensitivity: float = 0.5):
        """
        Args:
            instrument: The Instrument to wrap and monitor.
            sensitivity: How quickly the monitor reacts. 0=hands-off, 1=very responsive.
        """
        self.instrument = instrument
        self.sensitivity = max(0.0, min(1.0, sensitivity))

        # State
        self.flow_state: float = 0.5  # start neutral
        self.error_history: Deque[float] = deque(maxlen=50)
        self.consistency_history: Deque[float] = deque(maxlen=50)
        self.exploration_history: Deque[float] = deque(maxlen=50)
        self.flow_history: Deque[float] = deque(maxlen=100)

        # Learning
        self.learned_tendencies = LearnedTendencies()
        self._performance_history: List[List[dict]] = []
        self._snapshots: List[PerformerSnapshot] = []

        # Intervention tracking
        self.intervention_count: int = 0
        self._last_intervention_time: float = 0.0
        self._intervention_cooldown: float = 5.0  # seconds between interventions

        # Vanishing
        self._vanished: bool = False
        self._high_flow_streak: int = 0  # consecutive high-flow performances
        self._vanishing_threshold: int = 10  # performances above 0.9 flow to vanish

        # Adaptive parameters (shaped by the monitor)
        self._register_nudge: float = 0.0
        self._tempo_nudge: float = 0.0
        self._interval_bias: Dict[int, float] = {}

    # ── Main Interface ────────────────────────────────────────────────

    def perform(self, **kwargs) -> dict:
        """
        Perform through the monitor. The monitor observes the result,
        assesses flow, learns tendencies, and optionally nudges the
        instrument for the next performance.
        """
        # If vanished, just pass through
        if self._vanished:
            return self.instrument.perform(**kwargs)

        # Apply any gentle nudges from prior monitoring
        self._apply_nudges(kwargs)

        # Perform
        result = self.instrument.perform(**kwargs)
        notes = result.get("notes", [])

        # Observe and assess
        snapshot = self._take_snapshot(notes)
        assessment = self._assess_flow(snapshot)

        # Update state
        self._update_state(snapshot, assessment)

        # Learn from this performance
        self._learn(notes)

        # Decide whether to nudge for next time
        if assessment.should_intervene:
            self._plan_intervention(assessment)

        # Check vanishing condition
        self._check_vanishing()

        return result

    def report(self) -> MonitorReport:
        """Get a report on the monitor's state and the performer's tendencies."""
        assessment = self._current_assessment()
        return MonitorReport(
            flow_state=self.flow_state,
            sensitivity=self.sensitivity,
            snapshots_analyzed=len(self._snapshots),
            interventions_total=self.intervention_count,
            tendencies=self.learned_tendencies,
            is_vanished=self._vanished,
            assessment=assessment,
        )

    def reset(self):
        """Reset the monitor to initial state (but keep learned tendencies)."""
        self.flow_state = 0.5
        self.error_history.clear()
        self.consistency_history.clear()
        self.exploration_history.clear()
        self.flow_history.clear()
        self._snapshots.clear()
        self._vanished = False
        self._high_flow_streak = 0
        self._register_nudge = 0.0
        self._tempo_nudge = 0.0
        self._interval_bias.clear()

    @property
    def is_vanished(self) -> bool:
        """Whether the monitor has detected full internalization and gone silent."""
        return self._vanished

    # ── Flow Detection ────────────────────────────────────────────────

    def _take_snapshot(self, notes: List[dict]) -> PerformerSnapshot:
        """Capture a snapshot of the performer's current state."""
        terrain = self.instrument._terrain

        error_rate = _compute_error_rate(notes, terrain)
        consistency = _compute_consistency(notes)
        exploration = _compute_exploration_velocity(notes, self._performance_history)

        pitches = [n.get("pitch", 60) for n in notes]
        register = (min(pitches), max(pitches)) if pitches else (60, 60)

        intervals = [abs(pitches[i+1] - pitches[i]) for i in range(len(pitches) - 1)] if len(pitches) > 1 else []
        mean_interval = _mean(intervals) if intervals else 0.0

        starts = sorted([n.get("start", 0) for n in notes])
        gaps = [starts[i+1] - starts[i] for i in range(len(starts) - 1)] if len(starts) > 1 else []
        rhythmic_stability = max(0, 1.0 - _std(gaps) / _mean(gaps)) if gaps and _mean(gaps) > 0 else 0.5

        snapshot = PerformerSnapshot(
            timestamp=time.time(),
            notes=notes,
            error_rate=error_rate,
            consistency=consistency,
            exploration_velocity=exploration,
            register=register,
            mean_interval=mean_interval,
            rhythmic_stability=rhythmic_stability,
        )
        self._snapshots.append(snapshot)
        return snapshot

    def _assess_flow(self, snapshot: PerformerSnapshot) -> FlowAssessment:
        """
        Assess the performer's flow state from a snapshot.

        Flow = high consistency + low errors + moderate exploration.
        Struggling = high errors + low consistency.
        Wandering = high exploration + low consistency (exploring, not lost).
        """
        # Weighted combination
        # Consistency is the strongest signal (0.4)
        # Error rate is inverted (0.3)
        # Exploration is sweet-spot (0.15) — too low = stagnant, too high = lost
        # Rhythmic stability (0.15)

        consistency_signal = snapshot.consistency
        error_signal = 1.0 - snapshot.error_rate

        # Exploration: sweet spot around 0.3-0.6
        exp = snapshot.exploration_velocity
        exploration_signal = 1.0 - abs(exp - 0.45) * 2.0
        exploration_signal = max(0, min(1, exploration_signal))

        rhythmic_signal = snapshot.rhythmic_stability

        raw_flow = (
            consistency_signal * 0.4 +
            error_signal * 0.3 +
            exploration_signal * 0.15 +
            rhythmic_signal * 0.15
        )

        # Smooth with history
        self.flow_state = 0.7 * self.flow_state + 0.3 * raw_flow
        self.flow_history.append(self.flow_state)

        # Confidence: how much data do we have?
        confidence = min(1.0, len(self._snapshots) / 10.0)

        # Should we intervene?
        should_intervene = False
        intervention_type = None
        reason = "Flow is good"

        if self.flow_state < 0.3:
            should_intervene = True
            intervention_type = "support"
            reason = "Low flow: high error rate and inconsistency detected"
        elif self.flow_state < 0.5:
            # Only intervene if sensitivity is high enough
            if self.sensitivity > 0.3:
                should_intervene = True
                intervention_type = "nudge"
                reason = "Moderate flow: gentle course correction available"
        elif self.flow_state > 0.8:
            reason = "Deep flow: monitor is silent"

        # Cooldown check
        now = time.time()
        if should_intervene and (now - self._last_intervention_time) < self._intervention_cooldown:
            should_intervene = False
            reason += " (cooldown active)"

        return FlowAssessment(
            flow_score=self.flow_state,
            confidence=confidence,
            should_intervene=should_intervene,
            intervention_type=intervention_type,
            reason=reason,
        )

    def _current_assessment(self) -> FlowAssessment:
        """Get assessment from current state without a new snapshot."""
        return FlowAssessment(
            flow_score=self.flow_state,
            confidence=min(1.0, len(self._snapshots) / 10.0),
            should_intervene=False,
            intervention_type=None,
            reason="Current state assessment",
        )

    # ── Learning ──────────────────────────────────────────────────────

    def _learn(self, notes: List[dict]):
        """Learn the performer's tendencies from this performance."""
        if not notes:
            return

        self._performance_history.append(notes)
        t = self.learned_tendencies
        t.sample_count += 1

        # Learn favorite intervals
        pitches = [n.get("pitch", 60) for n in notes]
        intervals = [abs(pitches[i+1] - pitches[i]) for i in range(len(pitches) - 1)]

        for interval in intervals:
            if interval == 0:
                continue
            if interval not in t.favorite_intervals:
                t.favorite_intervals[interval] = 0.0
            # Exponential moving average
            t.favorite_intervals[interval] = 0.9 * t.favorite_intervals[interval] + 0.1

        # Normalize favorites
        total_weight = sum(t.favorite_intervals.values())
        if total_weight > 0:
            for k in t.favorite_intervals:
                t.favorite_intervals[k] /= total_weight

        # Learn register preference
        if pitches:
            low, high = min(pitches), max(pitches)
            alpha = min(0.3, 1.0 / t.sample_count)
            old_low, old_high = t.register_preference
            t.register_preference = (
                (1 - alpha) * old_low + alpha * low,
                (1 - alpha) * old_high + alpha * high,
            )

        # Learn velocity preference
        velocities = [n.get("velocity", 80) for n in notes]
        if velocities:
            alpha = min(0.3, 1.0 / t.sample_count)
            t.average_velocity = (1 - alpha) * t.average_velocity + alpha * _mean(velocities)

        # Learn phrase length preference
        phrase_lengths = self._detect_phrases(notes)
        if phrase_lengths:
            alpha = min(0.3, 1.0 / t.sample_count)
            t.phrase_length_preference = (1 - alpha) * t.phrase_length_preference + alpha * _mean(phrase_lengths)

        # Learn temporal density
        if notes:
            total_dur = max(n.get("start", 0) + n.get("duration", 0) for n in notes)
            if total_dur > 0:
                density = len(notes) / total_dur
                alpha = min(0.3, 1.0 / t.sample_count)
                t.temporal_density = (1 - alpha) * t.temporal_density + alpha * density

        # Classify exploration style
        if len(self.exploration_history) >= 5:
            avg_exploration = _mean(list(self.exploration_history)[-10:])
            if avg_exploration < 0.2:
                t.exploration_style = "cautious"
            elif avg_exploration > 0.6:
                t.exploration_style = "adventurous"
            else:
                t.exploration_style = "moderate"

        # Store exploration in history
        if self._snapshots:
            self.exploration_history.append(self._snapshots[-1].exploration_velocity)

    def _detect_phrases(self, notes: List[dict]) -> List[int]:
        """Detect phrase boundaries (gaps longer than average)."""
        if len(notes) < 4:
            return [len(notes)]

        starts = sorted([(n.get("start", 0), n.get("duration", 0)) for n in notes])
        gaps = []
        for i in range(len(starts) - 1):
            gap = starts[i+1][0] - (starts[i][0] + starts[i][1])
            gaps.append(max(0, gap))

        if not gaps:
            return [len(notes)]

        mean_gap = _mean(gaps)
        threshold = mean_gap * 2.5  # phrase boundary = 2.5x average gap

        phrases = []
        current_len = 1
        for gap in gaps:
            if gap > threshold:
                phrases.append(current_len)
                current_len = 1
            else:
                current_len += 1
        phrases.append(current_len)

        return phrases

    # ── Intervention ──────────────────────────────────────────────────

    def _plan_intervention(self, assessment: FlowAssessment):
        """
        Plan the gentlest possible intervention.
        We don't correct — we reshape the landscape.
        """
        if not self._snapshots:
            return

        latest = self._snapshots[-1]
        t = self.learned_tendencies

        if assessment.intervention_type == "support":
            # Strong nudge: bias toward learned preferences
            # Nudge register toward their comfort zone
            low, high = latest.register
            pref_low, pref_high = t.register_preference
            center = (low + high) / 2
            pref_center = (pref_low + pref_high) / 2
            self._register_nudge = (pref_center - center) * 0.1 * self.sensitivity

            # Nudge intervals toward favorites
            self._interval_bias = {}
            for interval, weight in sorted(t.favorite_intervals.items(), key=lambda x: -x[1])[:5]:
                self._interval_bias[interval] = weight * 0.3 * self.sensitivity

            self.intervention_count += 1
            self._last_intervention_time = time.time()

        elif assessment.intervention_type == "nudge":
            # Subtle nudge
            if latest.rhythmic_stability < 0.3:
                # Suggest steadier rhythm
                self._tempo_nudge = 0.05 * self.sensitivity

            self.intervention_count += 1
            self._last_intervention_time = time.time()

    def _apply_nudges(self, kwargs: dict):
        """Apply gentle nudges to performance parameters."""
        # These are hints that modes can optionally use.
        # The key insight: we don't force. We suggest.
        if self._register_nudge != 0:
            kwargs.setdefault("_monitor_register_nudge", self._register_nudge)
        if self._tempo_nudge != 0:
            kwargs.setdefault("_monitor_tempo_nudge", self._tempo_nudge)
        if self._interval_bias:
            kwargs.setdefault("_monitor_interval_bias", dict(self._interval_bias))

        # Decay nudges
        self._register_nudge *= 0.8
        self._tempo_nudge *= 0.8
        self._interval_bias = {k: v * 0.8 for k, v in self._interval_bias.items()}

    # ── Vanishing ─────────────────────────────────────────────────────

    def _check_vanishing(self):
        """
        Check if the performer has fully internalized the constraints.
        If they've been in deep flow for enough consecutive performances,
        the monitor vanishes — becomes a pure passthrough.
        """
        if self.flow_state >= 0.9:
            self._high_flow_streak += 1
        else:
            self._high_flow_streak = max(0, self._high_flow_streak - 2)

        if self._high_flow_streak >= self._vanishing_threshold:
            self._vanished = True

    def revive(self):
        """
        Bring the monitor back after vanishing.
        Useful if the performer changes terrain or mode.
        """
        self._vanished = False
        self._high_flow_streak = 0

    # ── Adaptive Constraint Surface ───────────────────────────────────

    def get_adaptive_surface(self) -> dict:
        """
        Return a shaped constraint surface based on learned tendencies.
        Other systems can use this to adjust their constraints.
        """
        t = self.learned_tendencies
        return {
            "register": t.register_preference,
            "favorite_intervals": dict(sorted(
                t.favorite_intervals.items(), key=lambda x: -x[1]
            )[:8]),
            "temporal_density": t.temporal_density,
            "average_velocity": t.average_velocity,
            "phrase_length": t.phrase_length_preference,
            "exploration_style": t.exploration_style,
            "flow_state": self.flow_state,
            "recommended_sensitivity": self.sensitivity * (1.0 - self.flow_state),
        }

    # ── Representations ───────────────────────────────────────────────

    def __repr__(self) -> str:
        state = "VANISHED" if self._vanished else f"flow={self.flow_state:.2f}"
        return f"Monitor({self.instrument}, {state})"

    def __str__(self) -> str:
        if self._vanished:
            return "🔇 Monitor: vanished (performer has internalized constraints)"
        return (
            f"🎛️ Monitor: flow={self.flow_state:.1%}, "
            f"interventions={self.intervention_count}, "
            f"style={self.learned_tendencies.exploration_style}"
        )
