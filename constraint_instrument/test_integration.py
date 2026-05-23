#!/usr/bin/env python3
"""
Integration test for the Constraint Instrument.

Tests every mode, every terrain, Goodman diagnostics, Monitor wrapping,
and WAV rendering. Run from workspace root:

    python3 constraint_instrument/test_integration.py
"""

import os
import sys
import random
import traceback

# Ensure we can import from workspace
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constraint_instrument.terrain import TERRAINS, Terrain
from constraint_instrument.instrument import Instrument, _render_to_wav
from constraint_instrument.goodman import GoodmanEngine, DiagnosticReport
from constraint_instrument.monitor import Monitor

# ── Test Tracking ────────────────────────────────────────────────────

results = []


def test(name, func):
    """Run a test and track results."""
    try:
        func()
        results.append((name, "PASS", ""))
        print(f"  ✅ {name}")
    except Exception as e:
        tb = traceback.format_exc().splitlines()[-1]
        results.append((name, "FAIL", str(e)))
        print(f"  ❌ {name}: {e}")
        print(f"     {tb}")


# ── Tests ────────────────────────────────────────────────────────────

def test_all_terrains_load():
    """All 17 terrains load and have required attributes."""
    assert len(TERRAINS) == 17, f"Expected 17 terrains, got {len(TERRAINS)}"
    for name, terrain in TERRAINS.items():
        assert isinstance(terrain, Terrain), f"{name} is not a Terrain"
        assert len(terrain.scale_degrees) > 0, f"{name} has no scale degrees"
        assert terrain.register_tendency[0] < terrain.register_tendency[1], \
            f"{name} has invalid register range"


def test_parker_mode():
    """Parker mode: practice, trajectory, perform."""
    inst = Instrument(mode="parker", terrain="bebop")
    sessions = inst.practice(focus="bebop", sessions=3)
    assert len(sessions) == 3
    assert all(s.accuracy >= 0 for s in sessions)
    traj = inst.feel_trajectory("ii-V-I")
    assert len(traj.path) > 0
    result = inst.perform(minutes=0.1)
    assert "notes" in result and len(result["notes"]) > 0


def test_miles_mode():
    """Miles mode: frontier, originality, perform."""
    inst = Instrument(mode="miles", terrain="modal")
    frontiers = inst.frontier(5)
    assert len(frontiers) == 5
    result = inst.perform(minutes=0.1)
    assert "notes" in result and len(result["notes"]) > 0
    orig = inst.originality()
    assert "score" in orig


def test_ellington_mode():
    """Ellington mode: compose, render."""
    inst = Instrument(mode="ellington", terrain="blues")
    chart = inst.compose(
        sections=["intro: sparse piano, rubato", "head: ensemble tight",
                   "sax solo: open sax, sparse", "outro: ensemble full"],
        constraints=["blues form", "call and response"],
        title="Integration Test Suite",
    )
    chart.assign("sax", "angular, dense, ahead")
    chart.assign("piano", "lyrical, sparse, behind")
    result = inst.perform(chart=chart)
    assert "notes" in result and len(result["notes"]) > 0


def test_basie_mode():
    """Basie mode: jam session, consensus, perform."""
    inst = Instrument(mode="basie", terrain="blues")
    session = inst.join_jam(players=4, tempo=140, style="swing")
    result = inst.perform(session=session)
    assert "notes" in result
    groove = session.consensus()
    assert 0.0 <= groove.pocket <= 1.0
    # Play a few rounds and watch consensus tighten
    for _ in range(3):
        session.play(listen=True)
    groove2 = session.consensus()
    assert groove2.pocket >= groove.pocket or groove.locked


def test_goodman_mode():
    """Goodman mode: diagnose notes."""
    inst = Instrument(mode="goodman", terrain="blues")
    # Generate some test notes manually
    notes = []
    t = 0.0
    for i in range(40):
        pitch = 60 + random.choice([0, 3, 5, 6, 7, 10])
        dur = random.choice([0.25, 0.5, 0.5, 1.0])
        notes.append({
            "pitch": pitch,
            "velocity": random.randint(60, 100),
            "start": round(t, 3),
            "duration": dur,
        })
        t += dur
    report = inst.diagnose(notes)
    assert isinstance(report, DiagnosticReport)
    assert len(report.orders) == 4
    assert report.overall_score >= 0
    summary = report.summary()
    assert "GOODMAN" in summary


def test_armstrong_mode():
    """Armstrong mode: load, remove/keep constraints, perform."""
    inst = Instrument(mode="armstrong", terrain="blues")
    inst.load("what_a_wonderful_world")
    assert inst.remove_constraint("pitch_grid")
    assert inst.keep_constraint("emotional_trajectory")
    result = inst.perform(minutes=0.1)
    assert "notes" in result and len(result["notes"]) > 0
    assert "pitch_grid" in result["removed_constraints"]


def test_ella_mode():
    """Ella mode: perform with no parameters."""
    inst = Instrument(mode="ella", terrain="blues")
    result = inst.perform()
    assert "notes" in result and len(result["notes"]) > 0
    assert result["mode"] == "ella"


def test_goodman_diagnose_external():
    """Goodman engine can diagnose notes from any source."""
    engine = GoodmanEngine(terrain=TERRAINS["modal"])
    # Generate a modal solo
    notes = []
    t = 0.0
    scale = [0, 2, 4, 5, 7, 9]
    for i in range(60):
        pitch = 60 + random.choice(scale) + random.choice([0, 12])
        dur = random.choice([0.5, 1.0, 1.0, 2.0])
        notes.append({
            "pitch": pitch,
            "velocity": random.randint(50, 110),
            "start": round(t, 3),
            "duration": dur,
        })
        t += dur
    report = engine.diagnose(notes)
    assert isinstance(report, DiagnosticReport)
    assert report.overall_score > 0


def test_monitor_wrapping():
    """Monitor wraps an instrument and adapts over multiple performances."""
    inst = Instrument(mode="miles", terrain="modal")
    mon = Monitor(inst, sensitivity=0.7)
    assert not mon.is_vanished

    # Run multiple performances through monitor
    for i in range(5):
        result = mon.perform(minutes=0.05)
        assert "notes" in result

    report = mon.report()
    assert report.flow_state >= 0
    assert report.snapshots_analyzed > 0
    surface = mon.get_adaptive_surface()
    assert "flow_state" in surface


def test_render_wav_parker():
    """Parker mode renders to WAV."""
    inst = Instrument(mode="parker", terrain="bebop")
    inst.perform(minutes=0.1)
    path = inst.render("constraint_instrument/test_parker.wav")
    assert os.path.exists(path)
    size = os.path.getsize(path)
    assert size > 1000, f"WAV too small: {size} bytes"
    os.unlink(path)


def test_render_wav_ella():
    """Ella mode renders to WAV."""
    inst = Instrument(mode="ella", terrain="blues")
    inst.perform(seed=42)
    path = inst.render("constraint_instrument/test_ella.wav")
    assert os.path.exists(path)
    size = os.path.getsize(path)
    assert size > 1000, f"WAV too small: {size} bytes"
    os.unlink(path)


def test_all_terrains_through_modes():
    """Every terrain runs through at least one mode."""
    modes_for_terrain = [
        "parker", "miles", "ella", "armstrong", "ellington", "basie"
    ]
    terrain_names = list(TERRAINS.keys())
    failures = []
    for i, tname in enumerate(terrain_names):
        mode = modes_for_terrain[i % len(modes_for_terrain)]
        try:
            inst = Instrument(mode=mode, terrain=tname)
            if mode == "ellington":
                chart = inst.compose(
                    sections=["head: ensemble", "solo: open sax"],
                    constraints=["test"],
                )
                result = inst.perform(chart=chart)
            elif mode == "basie":
                session = inst.join_jam(players=3)
                result = inst.perform(session=session)
            else:
                result = inst.perform(minutes=0.05)
            assert "notes" in result and len(result["notes"]) > 0, \
                f"{mode}/{tname}: no notes generated"
        except Exception as e:
            failures.append(f"{mode}/{tname}: {e}")
    assert not failures, "Terrain failures:\n" + "\n".join(failures)


def test_demo_output_wav():
    """Generate the demo WAV file (4+ bars)."""
    inst = Instrument(mode="ella", terrain="blues")
    inst.perform(seed=123)
    path = inst.render("constraint_instrument/demo_output.wav")
    assert os.path.exists(path)
    size = os.path.getsize(path)
    assert size > 5000, f"Demo WAV too small: {size} bytes"
    print(f"     → demo_output.wav: {size:,} bytes")


def test_all_modes_produce_valid_notes():
    """Every mode produces notes with required fields."""
    configs = [
        ("parker", "bebop", {}),
        ("miles", "modal", {}),
        ("ella", "blues", {}),
        ("armstrong", "delta_blues", {}),
    ]
    for mode, terrain, kwargs in configs:
        inst = Instrument(mode=mode, terrain=terrain)
        result = inst.perform(minutes=0.05, **kwargs)
        notes = result["notes"]
        assert len(notes) > 0, f"{mode} produced no notes"
        for n in notes:
            assert "pitch" in n, f"{mode}: note missing pitch"
            assert "velocity" in n, f"{mode}: note missing velocity"
            assert "start" in n, f"{mode}: note missing start"
            assert "duration" in n, f"{mode}: note missing duration"
            assert n["duration"] > 0, f"{mode}: zero duration"
            assert 21 <= n["pitch"] <= 108, f"{mode}: pitch out of range: {n['pitch']}"


# ── Run ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    random.seed(42)
    print("\n🔬 Constraint Instrument — Integration Tests\n")

    test("All 17 terrains load", test_all_terrains_load)
    test("Parker mode", test_parker_mode)
    test("Miles mode", test_miles_mode)
    test("Ellington mode", test_ellington_mode)
    test("Basie mode", test_basie_mode)
    test("Goodman mode", test_goodman_mode)
    test("Armstrong mode", test_armstrong_mode)
    test("Ella mode", test_ella_mode)
    test("Goodman external diagnosis", test_goodman_diagnose_external)
    test("Monitor wrapping", test_monitor_wrapping)
    test("WAV render (Parker)", test_render_wav_parker)
    test("WAV render (Ella)", test_render_wav_ella)
    test("All terrains through modes", test_all_terrains_through_modes)
    test("All modes produce valid notes", test_all_modes_produce_valid_notes)
    test("Demo WAV output", test_demo_output_wav)

    # Summary table
    passed = sum(1 for _, status, _ in results if status == "PASS")
    failed = sum(1 for _, status, _ in results if status == "FAIL")
    print(f"\n{'─' * 60}")
    print(f"  Results: {passed} passed, {failed} failed, {len(results)} total")
    print(f"{'─' * 60}")

    if failed:
        print(f"\n  FAILURES:")
        for name, status, err in results:
            if status == "FAIL":
                print(f"    ❌ {name}: {err}")
        sys.exit(1)
    else:
        print(f"\n  🎉 All tests passed!\n")
        sys.exit(0)
