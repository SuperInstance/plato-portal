"""Tests for the constraint-instrument package."""

import sys
import os
import tempfile
import unittest

from constraint_instrument import Instrument, TERRAINS
from constraint_instrument.terrain import Terrain, BLUES, BEBOP, MODAL
from constraint_instrument.parker import ParkerEngine
from constraint_instrument.miles import MilesEngine
from constraint_instrument.ellington import EllingtonEngine
from constraint_instrument.basie import BasieEngine
from constraint_instrument.goodman import GoodmanEngine
from constraint_instrument.armstrong import ArmstrongEngine
from constraint_instrument.ella import EllaEngine


class TestTerrain(unittest.TestCase):
    def test_terrains_exist(self):
        self.assertIn("blues", TERRAINS)
        self.assertIn("bebop", TERRAINS)
        self.assertIn("modal", TERRAINS)
        self.assertIn("classical", TERRAINS)
        self.assertIn("free_jazz", TERRAINS)

    def test_blues_has_blue_notes(self):
        blue_notes = [d for d in BLUES.scale_degrees if d.blues_note]
        self.assertTrue(len(blue_notes) >= 3)

    def test_terrain_attributes(self):
        self.assertEqual(BEBOP.name, "bebop")
        self.assertTrue(len(BEBOP.scale_degrees) >= 7)
        self.assertTrue(BEBOP.chromatic_density > 0.5)


class TestInstrument(unittest.TestCase):
    def test_create_all_modes(self):
        for mode in Instrument.MODES:
            inst = Instrument(mode=mode, terrain="blues")
            self.assertEqual(inst.mode, mode)

    def test_invalid_mode(self):
        with self.assertRaises(ValueError):
            Instrument(mode="coltrane")

    def test_invalid_terrain(self):
        with self.assertRaises(ValueError):
            Instrument(terrain="polka")

    def test_info(self):
        inst = Instrument(mode="ella", voice="piano", terrain="modal")
        info = inst.info
        self.assertEqual(info["mode"], "ella")
        self.assertEqual(info["voice"], "piano")
        self.assertEqual(info["terrain"], "modal")
        self.assertFalse(info["has_performance"])


class TestParkerMode(unittest.TestCase):
    def setUp(self):
        self.inst = Instrument(mode="parker", terrain="bebop")

    def test_practice(self):
        sessions = self.inst.practice(focus="chromatic_enclosure", sessions=3)
        self.assertEqual(len(sessions), 3)
        for s in sessions:
            self.assertGreaterEqual(s.accuracy, 0.0)
            self.assertLessEqual(s.accuracy, 1.0)

    def test_feel_trajectory(self):
        traj = self.inst.feel_trajectory("ii-V-I")
        self.assertIn(0, traj.path)  # starts or ends on root

    def test_perform(self):
        result = self.inst.perform(minutes=0.5)
        self.assertIn("notes", result)
        self.assertGreater(len(result["notes"]), 0)
        self.assertIn("tempo", result)
        self.assertIn("internalization", result)

    def test_perform_notes_have_required_fields(self):
        result = self.inst.perform(minutes=0.2)
        for note in result["notes"]:
            self.assertIn("pitch", note)
            self.assertIn("velocity", note)
            self.assertIn("start", note)
            self.assertIn("duration", note)


class TestMilesMode(unittest.TestCase):
    def setUp(self):
        self.inst = Instrument(mode="miles", terrain="modal")

    def test_frontier(self):
        frontier = self.inst.frontier(n=3)
        self.assertLessEqual(len(frontier), 3)
        for f in frontier:
            self.assertGreater(f.distance, 0)

    def test_perform(self):
        result = self.inst.perform(explore=True, risk=0.5, minutes=0.5)
        self.assertIn("notes", result)
        self.assertGreater(len(result["notes"]), 0)

    def test_originality(self):
        self.inst.perform(minutes=0.3)
        orig = self.inst.originality()
        self.assertIn("score", orig)
        self.assertGreaterEqual(orig["score"], 0.0)
        self.assertLessEqual(orig["score"], 1.0)


class TestEllingtonMode(unittest.TestCase):
    def setUp(self):
        self.inst = Instrument(mode="ellington", terrain="blues")

    def test_compose(self):
        chart = self.inst.compose(
            sections=[
                "intro: full ensemble, statement of theme",
                "sax solo: open, just rhythm section",
                "outro: full ensemble, recapitulation",
            ],
            constraints=["theme must establish the motif"],
            title="Test Chart",
        )
        self.assertEqual(chart.title, "Test Chart")
        self.assertEqual(len(chart.sections), 3)

    def test_assign_and_render(self):
        chart = self.inst.compose(
            sections=["sax solo: open section"],
            constraints=[],
        )
        chart.assign("trumpet", personality="bold, angular, likes upper register")
        chart.assign("sax", personality="smooth, lyrical, blues-influenced")
        result = self.inst.perform(chart=chart)
        self.assertIn("notes", result)
        self.assertGreater(len(result["notes"]), 0)


class TestBasieMode(unittest.TestCase):
    def setUp(self):
        self.inst = Instrument(mode="basie", terrain="blues")

    def test_join_jam(self):
        from constraint_instrument.basie import JamSession
        session = self.inst.join_jam(players=4, tempo=140, key=60)
        self.assertIsInstance(session, JamSession)
        self.assertEqual(len(session.players), 4)

    def test_play_and_consensus(self):
        session = self.inst.join_jam(players=3, tempo=120)
        result = self.inst.perform(session=session, my_role="piano", listen=True)
        self.assertIn("groove", result)
        self.assertIn("notes", result)

    def test_lock(self):
        session = self.inst.join_jam(players=3, tempo=120)
        # Play a few rounds first
        for _ in range(5):
            session.play(listen=True)
        groove = session.lock()
        self.assertTrue(groove.pocket >= 0.9)


class TestGoodmanMode(unittest.TestCase):
    def setUp(self):
        self.inst = Instrument(mode="goodman", terrain="blues")

    def test_diagnose_notes(self):
        # Generate some test notes
        notes = [
            {"pitch": 60, "velocity": 80, "start": 0.0, "duration": 0.5},
            {"pitch": 63, "velocity": 85, "start": 0.5, "duration": 0.5},
            {"pitch": 65, "velocity": 70, "start": 1.0, "duration": 0.5},
            {"pitch": 67, "velocity": 90, "start": 1.5, "duration": 1.0},
            {"pitch": 70, "velocity": 75, "start": 2.5, "duration": 0.5},
            {"pitch": 65, "velocity": 80, "start": 3.0, "duration": 0.5},
            {"pitch": 60, "velocity": 85, "start": 3.5, "duration": 1.0},
        ]
        report = self.inst.diagnose(notes)
        self.assertIn("POSITION", report.stars)
        self.assertIn("DIRECTION", report.stars)
        self.assertIn("CURVATURE", report.stars)
        self.assertIn("STRUCTURE", report.stars)
        self.assertIsNotNone(report.recommendation)

    def test_prescribe(self):
        rx = self.inst.prescribe(missing_order=2, focus="blues_curvature")
        self.assertEqual(rx.order, 2)
        self.assertGreater(len(rx.exercises), 0)


class TestArmstrongMode(unittest.TestCase):
    def setUp(self):
        self.inst = Instrument(mode="armstrong", terrain="blues")

    def test_load_and_perform(self):
        self.inst.load("what_a_wonderful_world")
        result = self.inst.perform(forget_lyrics=True, minutes=0.5)
        self.assertIn("notes", result)
        self.assertIn("removed_constraints", result)

    def test_constraint_removal(self):
        self.inst.remove_constraint("pitch_grid")
        self.inst.remove_constraint("time_grid")
        self.inst.keep_constraint("emotional_trajectory")
        result = self.inst.perform(minutes=0.3)
        self.assertIn("pitch_grid", result["removed_constraints"])
        self.assertIn("emotional_trajectory", result["active_constraints"])


class TestEllaMode(unittest.TestCase):
    def setUp(self):
        self.inst = Instrument(mode="ella", terrain="blues")

    def test_perform_no_params(self):
        result = self.inst.perform()
        self.assertIn("notes", result)
        self.assertGreater(len(result["notes"]), 0)
        self.assertEqual(result["mode"], "ella")

    def test_perform_with_seed(self):
        result = self.inst.perform(seed=42)
        self.assertIn("notes", result)

    def test_notes_in_range(self):
        result = self.inst.perform(seed=42)
        terrain_low, terrain_high = self.inst._terrain.register_tendency
        # Allow soft clamp margin
        for note in result["notes"]:
            self.assertGreaterEqual(note["pitch"], terrain_low - 10)
            self.assertLessEqual(note["pitch"], terrain_high + 10)


class TestRender(unittest.TestCase):
    def test_render_wav(self):
        inst = Instrument(mode="ella", terrain="blues")
        inst.perform(seed=42)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            path = inst.render(f.name)
        self.assertTrue(os.path.exists(path))
        self.assertGreater(os.path.getsize(path), 100)
        os.unlink(path)

    def test_render_json_fallback(self):
        inst = Instrument(mode="parker", terrain="bebop")
        inst.perform(minutes=0.1)
        with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as f:
            path = inst.render(f.name)
        self.assertTrue(os.path.exists(path))
        os.unlink(path)


if __name__ == "__main__":
    unittest.main()
