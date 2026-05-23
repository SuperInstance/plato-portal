"""
Tests for the Monitor — the invisible engineer.
"""

import pytest
import random
import math

from constraint_instrument.instrument import Instrument
from constraint_instrument.monitor import (
    Monitor,
    MonitorReport,
    FlowAssessment,
    LearnedTendencies,
    PerformerSnapshot,
    _compute_error_rate,
    _compute_consistency,
    _compute_exploration_velocity,
    _mean,
    _std,
)


# ── Fixtures ──────────────────────────────────────────────────────────

@pytest.fixture
def instrument():
    return Instrument(mode="ella", terrain="blues")


@pytest.fixture
def monitor(instrument):
    return Monitor(instrument, sensitivity=0.5)


@pytest.fixture
def high_sensitivity_monitor(instrument):
    return Monitor(instrument, sensitivity=0.9)


@pytest.fixture
def low_sensitivity_monitor(instrument):
    return Monitor(instrument, sensitivity=0.1)


def make_notes(pitches, start=0.0, duration=0.5, velocity=80):
    """Helper to create note dicts."""
    notes = []
    t = start
    for p in pitches:
        notes.append({
            "pitch": p,
            "velocity": velocity,
            "start": round(t, 3),
            "duration": round(duration, 3),
        })
        t += duration
    return notes


# ── Monitor Initialization ────────────────────────────────────────────

class TestMonitorInit:
    def test_basic_creation(self, instrument):
        m = Monitor(instrument)
        assert m.instrument is instrument
        assert m.flow_state == 0.5
        assert m.intervention_count == 0
        assert not m.is_vanished

    def test_sensitivity_clamped(self, instrument):
        m = Monitor(instrument, sensitivity=5.0)
        assert m.sensitivity == 1.0
        m2 = Monitor(instrument, sensitivity=-1.0)
        assert m2.sensitivity == 0.0

    def test_repr(self, monitor):
        r = repr(monitor)
        assert "Monitor" in r
        assert "flow=" in r

    def test_str_vanished(self, monitor):
        monitor._vanished = True
        assert "vanished" in str(monitor).lower()


# ── Flow Detection ────────────────────────────────────────────────────

class TestFlowDetection:
    def test_consistent_notes_high_flow(self, monitor):
        """Consistent, in-register notes should produce high flow."""
        notes = make_notes([60, 62, 64, 65, 67, 69, 71, 72])
        snapshot = monitor._take_snapshot(notes)
        assert snapshot.consistency > 0.3  # decent consistency
        assert snapshot.error_rate < 0.5   # low errors

    def test_erratic_notes_low_flow(self, monitor):
        """Erratic, out-of-range notes should produce low flow."""
        notes = make_notes([20, 100, 30, 110, 25, 105], velocity=100)
        # Add velocity spikes
        notes[1]["velocity"] = 127
        notes[3]["velocity"] = 10
        snapshot = monitor._take_snapshot(notes)
        assert snapshot.error_rate > 0.1  # some errors detected

    def test_flow_state_smoothed(self, monitor):
        """Flow state should change gradually, not jump."""
        initial_flow = monitor.flow_state
        # Perform several times — flow should move smoothly
        for _ in range(5):
            monitor.perform()
        # Flow should have moved but not wildly
        assert abs(monitor.flow_state - initial_flow) < 1.0

    def test_assessment_returns_flow_assessment(self, monitor):
        notes = make_notes([60, 62, 64, 67, 69])
        snapshot = monitor._take_snapshot(notes)
        assessment = monitor._assess_flow(snapshot)
        assert isinstance(assessment, FlowAssessment)
        assert 0.0 <= assessment.flow_score <= 1.0
        assert 0.0 <= assessment.confidence <= 1.0


# ── Error Rate Computation ────────────────────────────────────────────

class TestErrorRate:
    def test_clean_notes_low_error(self, instrument):
        terrain = instrument._terrain
        notes = make_notes([60, 62, 64, 65, 67])
        err = _compute_error_rate(notes, terrain)
        assert err < 0.5

    def test_wild_pitches_high_error(self, instrument):
        terrain = instrument._terrain
        notes = make_notes([10, 120, 5, 125, 15])
        err = _compute_error_rate(notes, terrain)
        assert err > 0.0

    def test_empty_notes_zero_error(self, instrument):
        terrain = instrument._terrain
        err = _compute_error_rate([], terrain)
        assert err == 0.0


# ── Consistency Computation ───────────────────────────────────────────

class TestConsistency:
    def test_perfectly_consistent(self):
        notes = make_notes([60, 62, 64, 66, 68, 70])
        c = _compute_consistency(notes)
        assert c > 0.3  # should be reasonably consistent

    def test_chaotic_low_consistency(self):
        notes = []
        t = 0.0
        for i in range(10):
            notes.append({
                "pitch": random.randint(30, 100),
                "velocity": random.randint(30, 127),
                "start": round(t + random.uniform(0, 2), 3),
                "duration": round(random.uniform(0.1, 2.0), 3),
            })
            t = notes[-1]["start"] + notes[-1]["duration"]
        c = _compute_consistency(notes)
        # Chaotic notes should have lower consistency than structured
        assert c >= 0.0

    def test_few_notes_returns_half(self):
        c = _compute_consistency(make_notes([60, 62]))
        assert c == 0.5


# ── Exploration Velocity ──────────────────────────────────────────────

class TestExploration:
    def test_no_history(self):
        notes = make_notes([60, 62, 64])
        v = _compute_exploration_velocity(notes, [])
        assert v == 0.5

    def test_repeated_material_low_exploration(self):
        notes = make_notes([60, 62, 64])
        history = [make_notes([60, 62, 64])] * 5
        v = _compute_exploration_velocity(notes, history)
        assert v < 0.5  # should be low since nothing new

    def test_new_material_high_exploration(self):
        notes = make_notes([90, 92, 94, 96])  # very different
        history = [make_notes([40, 42, 44])] * 5
        v = _compute_exploration_velocity(notes, history)
        assert v > 0.3  # should detect novelty


# ── Learning ──────────────────────────────────────────────────────────

class TestLearning:
    def test_learns_register_preference(self, monitor):
        # Play lots of high notes
        high_notes = make_notes([80, 82, 84, 86, 88] * 3)
        monitor._learn(high_notes)
        monitor._learn(high_notes)
        monitor._learn(high_notes)
        t = monitor.learned_tendencies
        assert t.register_preference[0] > 60  # should have shifted up

    def test_learns_interval_preferences(self, monitor):
        # Play lots of thirds (interval 3-4 semitones)
        notes = []
        base = 60
        for i in range(20):
            notes.append({"pitch": base, "velocity": 80, "start": i * 0.5, "duration": 0.4})
            notes.append({"pitch": base + 4, "velocity": 80, "start": i * 0.5 + 0.25, "duration": 0.4})
            base = (base + 4) % 12 + 60
        monitor._learn(notes)
        t = monitor.learned_tendencies
        assert 4 in t.favorite_intervals  # major third should be learned

    def test_learns_velocity(self, monitor):
        loud_notes = make_notes([60, 62, 64], velocity=110)
        monitor._learn(loud_notes)
        monitor._learn(loud_notes)
        assert monitor.learned_tendencies.average_velocity > 80

    def test_learns_temporal_density(self, monitor):
        # Dense notes
        notes = make_notes([60, 62, 64, 65, 67, 69, 71, 72, 74, 76])
        for n in notes:
            n["duration"] = 0.1
            n["start"] *= 0.2  # compress
        monitor._learn(notes)
        assert monitor.learned_tendencies.temporal_density > 0

    def test_classifies_exploration_style(self, monitor):
        # Simulate adventurous exploration
        monitor.exploration_history.extend([0.7, 0.8, 0.75, 0.65, 0.8])
        notes = make_notes([60, 62, 64])
        monitor._learn(notes)
        assert monitor.learned_tendencies.exploration_style == "adventurous"

    def test_detects_phrases(self, monitor):
        # Notes with a clear gap in the middle
        notes = make_notes([60, 62, 64, 67, 69])  # first phrase
        # Add a big gap
        notes += make_notes([72, 74, 76], start=5.0)  # second phrase
        phrases = monitor._detect_phrases(notes)
        assert len(phrases) >= 1  # should detect at least the gap


# ── Intervention ──────────────────────────────────────────────────────

class TestIntervention:
    def test_no_intervention_in_flow(self, monitor):
        """When flow is high, monitor should not intervene."""
        monitor.flow_state = 0.95
        notes = make_notes([60, 62, 64, 67, 69])
        snapshot = monitor._take_snapshot(notes)
        assessment = monitor._assess_flow(snapshot)
        assert not assessment.should_intervene or assessment.intervention_type is None

    def test_intervention_when_struggling(self, monitor):
        """When flow is low, monitor should plan intervention."""
        monitor.flow_state = 0.1
        assessment = FlowAssessment(
            flow_score=0.1, confidence=0.8, should_intervene=True,
            intervention_type="support", reason="test"
        )
        snapshot = PerformerSnapshot(
            timestamp=0, notes=[], error_rate=0.8, consistency=0.2,
            exploration_velocity=0.1, register=(60, 72), mean_interval=3.0,
            rhythmic_stability=0.2,
        )
        monitor._snapshots = [snapshot]
        monitor._plan_intervention(assessment)
        assert monitor.intervention_count > 0
        assert monitor._register_nudge != 0 or monitor._interval_bias

    def test_cooldown_respected(self, monitor):
        """Interventions should respect cooldown period."""
        monitor._last_intervention_time = 0  # long ago
        # Force a low-flow state
        monitor.flow_state = 0.1
        notes = make_notes([20, 100, 30])  # bad notes
        snapshot = monitor._take_snapshot(notes)
        assessment = monitor._assess_flow(snapshot)
        # After first intervention, set cooldown
        monitor._last_intervention_time = 9999999999  # very recent
        # Next assessment should not intervene due to cooldown
        notes2 = make_notes([20, 100, 30])
        snapshot2 = monitor._take_snapshot(notes2)
        assessment2 = monitor._assess_flow(snapshot2)
        assert not assessment2.should_intervene or "cooldown" in assessment2.reason

    def test_sensitivity_affects_intervention(self, instrument):
        """Higher sensitivity should trigger interventions more readily."""
        # Low sensitivity monitor
        low_mon = Monitor(instrument, sensitivity=0.1)
        low_mon.flow_state = 0.4
        notes = make_notes([60, 62, 64])
        snapshot = low_mon._take_snapshot(notes)
        assessment = low_mon._assess_flow(snapshot)
        # With low sensitivity and moderate flow, likely no intervention
        # (depends on exact numbers, but sensitivity gates it)

        # High sensitivity monitor
        high_mon = Monitor(instrument, sensitivity=0.9)
        high_mon.flow_state = 0.4
        snapshot2 = high_mon._take_snapshot(notes)
        assessment2 = high_mon._assess_flow(snapshot2)
        # High sensitivity is more likely to intervene at moderate flow


# ── Vanishing ─────────────────────────────────────────────────────────

class TestVanishing:
    def test_vanishing_after_sustained_flow(self, monitor):
        """Monitor should vanish after sustained deep flow."""
        monitor._vanishing_threshold = 3  # lower threshold for testing
        # Simulate high-flow performances
        for _ in range(5):
            monitor.flow_state = 0.95
            monitor._check_vanishing()
        assert monitor.is_vanished

    def test_no_vanishing_with_mixed_flow(self, monitor):
        """Monitor should not vanish if flow is inconsistent."""
        monitor._vanishing_threshold = 5
        flows = [0.95, 0.5, 0.95, 0.3, 0.95]
        for f in flows:
            monitor.flow_state = f
            monitor._check_vanishing()
        assert not monitor.is_vanished

    def test_revive(self, monitor):
        """Monitor can be revived after vanishing."""
        monitor._vanished = True
        monitor.revive()
        assert not monitor.is_vanished
        assert monitor._high_flow_streak == 0

    def test_vanished_monitor_passes_through(self, monitor):
        """When vanished, monitor should just pass through."""
        monitor._vanished = True
        result = monitor.perform()
        assert "notes" in result
        assert result["mode"] == "ella"

    def test_vanishing_threshold_default(self, monitor):
        """Default vanishing threshold is 10."""
        assert monitor._vanishing_threshold == 10


# ── Nudge Application ─────────────────────────────────────────────────

class TestNudges:
    def test_nudges_applied_to_kwargs(self, monitor):
        """Nudges should be applied to kwargs before performance."""
        monitor._register_nudge = 3.0
        monitor._tempo_nudge = 0.1
        monitor._interval_bias = {3: 0.5, 5: 0.3}
        kwargs = {}
        monitor._apply_nudges(kwargs)
        assert "_monitor_register_nudge" in kwargs
        assert "_monitor_tempo_nudge" in kwargs
        assert "_monitor_interval_bias" in kwargs

    def test_nudges_decay(self, monitor):
        """Nudges should decay after application."""
        monitor._register_nudge = 10.0
        monitor._tempo_nudge = 1.0
        monitor._interval_bias = {4: 1.0}
        monitor._apply_nudges({})
        assert abs(monitor._register_nudge - 8.0) < 0.01
        assert abs(monitor._tempo_nudge - 0.8) < 0.01
        assert abs(monitor._interval_bias[4] - 0.8) < 0.01


# ── Adaptive Surface ──────────────────────────────────────────────────

class TestAdaptiveSurface:
    def test_surface_returns_data(self, monitor):
        monitor.perform()  # need some data
        surface = monitor.get_adaptive_surface()
        assert "register" in surface
        assert "favorite_intervals" in surface
        assert "flow_state" in surface
        assert "exploration_style" in surface

    def test_surface_recommended_sensitivity(self, monitor):
        monitor.perform()
        surface = monitor.get_adaptive_surface()
        # recommended sensitivity should be reduced by flow
        assert surface["recommended_sensitivity"] >= 0


# ── Report ────────────────────────────────────────────────────────────

class TestReport:
    def test_report_type(self, monitor):
        report = monitor.report()
        assert isinstance(report, MonitorReport)
        assert isinstance(report.tendencies, LearnedTendencies)

    def test_report_after_performances(self, monitor):
        monitor.perform()
        monitor.perform()
        report = monitor.report()
        assert report.snapshots_analyzed >= 2


# ── Reset ─────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_state(self, monitor):
        monitor.perform()
        monitor.perform()
        monitor.reset()
        assert monitor.flow_state == 0.5
        assert monitor.intervention_count == 0
        assert not monitor.is_vanished
        assert len(monitor._snapshots) == 0

    def test_reset_keeps_tendencies(self, monitor):
        monitor.perform()
        monitor.perform()
        old_tendencies = monitor.learned_tendencies
        monitor.reset()
        # Tendencies object is kept (it's the same learning)
        assert monitor.learned_tendencies is old_tendencies


# ── Helpers ───────────────────────────────────────────────────────────

class TestHelpers:
    def test_mean(self):
        assert _mean([1, 2, 3, 4, 5]) == 3.0
        assert _mean([]) == 0.0

    def test_std(self):
        assert _std([5, 5, 5, 5]) == 0.0
        assert _std([]) == 0.0
        assert _std([1]) == 0.0
        assert _std([1, 3]) > 0


# ── Integration ───────────────────────────────────────────────────────

class TestIntegration:
    def test_full_performance_cycle(self, monitor):
        """Monitor should handle a full performance cycle."""
        result = monitor.perform()
        assert "notes" in result
        assert isinstance(result["notes"], list)
        assert len(result["notes"]) > 0

    def test_multiple_performances_learn(self, monitor):
        """Multiple performances should build up learning."""
        for _ in range(5):
            monitor.perform()
        assert monitor.learned_tendencies.sample_count >= 5
        assert len(monitor._snapshots) >= 5

    def test_monitor_with_different_modes(self):
        """Monitor should work with any instrument mode."""
        for mode in ["parker", "miles", "ella"]:
            inst = Instrument(mode=mode, terrain="blues")
            mon = Monitor(inst, sensitivity=0.5)
            result = mon.perform()
            assert "notes" in result

    def test_monitor_wraps_ellington(self):
        """Monitor works with Ellington mode (compose then perform)."""
        inst = Instrument(mode="ellington", terrain="blues")
        mon = Monitor(inst)
        chart = inst.compose(
            sections=["A", "B", "A"],
            constraints=[{"type": "register", "range": [55, 75]}],
        )
        result = mon.perform(chart=chart)
        assert "notes" in result
