"""Tests for the export module."""

import json
import math
import os
import tempfile
import pytest
from constraint_toolkit.lattice import ConstraintLattice, LatticeNode
from constraint_toolkit.dial import DialPosition, DialSpace
from constraint_toolkit.tradition import Tradition, TraditionCluster
from constraint_toolkit.export import (
    export_lattice_json,
    export_dial_json,
    export_traditions_json,
    export_traditions_csv,
    export_lattice_csv,
    generate_report,
    export_report_file,
)


def _make_lattice():
    lat = ConstraintLattice()
    lat.add_node(LatticeNode("top", 2, coordinates=(0.0, 1.0), metadata={"type": "root"}))
    lat.add_node(LatticeNode("mid", 1))
    lat.add_node(LatticeNode("bot", 0))
    lat.add_edge("top", "mid")
    lat.add_edge("mid", "bot")
    return lat


def _make_dial():
    return DialSpace([
        DialPosition("a", 0),
        DialPosition("b", math.pi / 2),
    ])


def _make_traditions():
    return TraditionCluster([
        Tradition("jazz", {"harmony": 8.0, "rhythm": 9.0}, "music"),
        Tradition("blues", {"harmony": 7.0, "rhythm": 7.0}, "music"),
    ])


# ---- JSON exports ----

class TestExportLatticeJson:
    def test_valid_json(self):
        data = json.loads(export_lattice_json(_make_lattice()))
        assert "nodes" in data
        assert "edges" in data

    def test_node_fields(self):
        data = json.loads(export_lattice_json(_make_lattice()))
        top = [n for n in data["nodes"] if n["name"] == "top"][0]
        assert top["level"] == 2
        assert top["coordinates"] == [0.0, 1.0]
        assert top["metadata"]["type"] == "root"

    def test_edge_fields(self):
        data = json.loads(export_lattice_json(_make_lattice()))
        assert {"parent": "top", "child": "mid"} in data["edges"]

    def test_empty(self):
        data = json.loads(export_lattice_json(ConstraintLattice()))
        assert data["nodes"] == []
        assert data["edges"] == []


class TestExportDialJson:
    def test_valid_json(self):
        data = json.loads(export_dial_json(_make_dial()))
        assert "positions" in data
        assert len(data["positions"]) == 2

    def test_position_fields(self):
        data = json.loads(export_dial_json(_make_dial()))
        a = data["positions"][0]
        assert a["name"] == "a"
        assert a["angle"] == 0
        assert "angle_degrees" in a
        assert a["radius"] == 1.0

    def test_angle_degrees(self):
        ds = DialSpace([DialPosition("quarter", math.pi / 2)])
        data = json.loads(export_dial_json(ds))
        assert abs(data["positions"][0]["angle_degrees"] - 90.0) < 0.01


class TestExportTraditionsJson:
    def test_valid_json(self):
        data = json.loads(export_traditions_json(_make_traditions()))
        assert "traditions" in data
        assert len(data["traditions"]) == 2

    def test_tradition_fields(self):
        data = json.loads(export_traditions_json(_make_traditions()))
        jazz = [t for t in data["traditions"] if t["name"] == "jazz"][0]
        assert jazz["scores"]["harmony"] == 8.0
        assert jazz["category"] == "music"


# ---- CSV exports ----

class TestExportTraditionsCsv:
    def test_has_header(self):
        csv_str = export_traditions_csv(_make_traditions())
        lines = csv_str.strip().split("\n")
        assert "name" in lines[0]
        assert "category" in lines[0]
        assert "harmony" in lines[0]
        assert "rhythm" in lines[0]

    def test_data_rows(self):
        csv_str = export_traditions_csv(_make_traditions())
        lines = csv_str.strip().split("\n")
        assert len(lines) == 3  # header + 2 rows
        assert "jazz" in lines[1]
        assert "blues" in lines[2]

    def test_empty(self):
        assert export_traditions_csv(TraditionCluster()) == ""


class TestExportLatticeCsv:
    def test_has_header(self):
        csv_str = export_lattice_csv(_make_lattice())
        lines = csv_str.strip().split("\n")
        assert "name" in lines[0]
        assert "level" in lines[0]

    def test_data_rows(self):
        csv_str = export_lattice_csv(_make_lattice())
        lines = csv_str.strip().split("\n")
        assert len(lines) == 4  # header + 3 nodes

    def test_edge_info(self):
        csv_str = export_lattice_csv(_make_lattice())
        # top should have mid as child
        assert "mid" in csv_str


# ---- Markdown report ----

class TestGenerateReport:
    def test_full_report(self):
        report = generate_report(
            lattice=_make_lattice(),
            dial=_make_dial(),
            traditions=_make_traditions(),
            title="Test Report",
        )
        assert "# Test Report" in report
        assert "Lattice Structure" in report
        assert "Dial Positions" in report
        assert "Traditions" in report
        assert "constraint-toolkit" in report

    def test_lattice_only(self):
        report = generate_report(lattice=_make_lattice())
        assert "Lattice Structure" in report
        assert "Dial Positions" not in report
        assert "Traditions" not in report

    def test_dial_only(self):
        report = generate_report(dial=_make_dial())
        assert "Dial Positions" in report
        assert "Mean angle" in report
        assert "Diameter" in report

    def test_traditions_only(self):
        report = generate_report(traditions=_make_traditions())
        assert "Traditions" in report
        assert "Score Heatmap" in report
        assert "Cluster Summary" in report

    def test_empty_report(self):
        report = generate_report()
        assert "# Constraint Analysis Report" in report
        assert "Generated" in report

    def test_custom_title(self):
        report = generate_report(title="My Custom Title")
        assert "# My Custom Title" in report


class TestExportReportFile:
    def test_writes_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            path = f.name
        try:
            export_report_file(path, title="File Test")
            with open(path) as f:
                content = f.read()
            assert "# File Test" in content
        finally:
            os.unlink(path)

    def test_file_with_all_data(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            path = f.name
        try:
            export_report_file(
                path,
                lattice=_make_lattice(),
                dial=_make_dial(),
                traditions=_make_traditions(),
            )
            with open(path) as f:
                content = f.read()
            assert "Lattice Structure" in content
            assert "Dial Positions" in content
            assert "Traditions" in content
        finally:
            os.unlink(path)
