"""Export constraint analysis results to JSON, CSV, and Markdown report formats."""

from __future__ import annotations

import csv
import io
import json
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Sequence

from constraint_toolkit.lattice import ConstraintLattice, LatticeNode
from constraint_toolkit.dial import DialPosition, DialSpace
from constraint_toolkit.tradition import Tradition, TraditionCluster


# ---------------------------------------------------------------------------
# JSON export
# ---------------------------------------------------------------------------

def export_lattice_json(lattice: ConstraintLattice) -> str:
    """Export a constraint lattice to a JSON string."""
    data = {
        "nodes": [
            {
                "name": n.name,
                "level": n.level,
                "coordinates": list(n.coordinates),
                "metadata": n.metadata,
            }
            for n in lattice.nodes
        ],
        "edges": [
            {"parent": p, "child": c}
            for p, c in lattice.edges
        ],
    }
    return json.dumps(data, indent=2)


def export_dial_json(space: DialSpace) -> str:
    """Export a dial space to a JSON string."""
    data = {
        "positions": [
            {
                "name": p.name,
                "angle": p.angle,
                "angle_degrees": round(__import__("math").degrees(p.angle), 4),
                "radius": p.radius,
            }
            for p in space.positions
        ]
    }
    return json.dumps(data, indent=2)


def export_traditions_json(tc: TraditionCluster) -> str:
    """Export traditions to a JSON string."""
    data = {
        "traditions": [
            {
                "name": t.name,
                "scores": t.scores,
                "category": t.category,
            }
            for t in tc.traditions
        ]
    }
    return json.dumps(data, indent=2)


# ---------------------------------------------------------------------------
# CSV export
# ---------------------------------------------------------------------------

def export_traditions_csv(tc: TraditionCluster) -> str:
    """Export traditions as CSV with score columns."""
    traditions = tc.traditions
    if not traditions:
        return ""

    all_keys = sorted({k for t in traditions for k in t.scores})
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["name", "category"] + all_keys)

    for t in traditions:
        row = [t.name, t.category] + [t.scores.get(k, 0.0) for k in all_keys]
        writer.writerow(row)

    return buf.getvalue()


def export_lattice_csv(lattice: ConstraintLattice) -> str:
    """Export lattice as CSV (nodes sheet)."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["name", "level", "coordinates", "parent_edges", "child_edges"])

    for n in lattice.nodes:
        parents = [p for p, c in lattice.edges if c == n.name]
        children = [c for p, c in lattice.edges if p == n.name]
        writer.writerow([
            n.name,
            n.level,
            ";".join(str(c) for c in n.coordinates),
            ";".join(parents),
            ";".join(children),
        ])

    return buf.getvalue()


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------

def generate_report(
    lattice: ConstraintLattice | None = None,
    dial: DialSpace | None = None,
    traditions: TraditionCluster | None = None,
    title: str = "Constraint Analysis Report",
) -> str:
    """Generate a Markdown report combining all analysis results."""
    from constraint_toolkit.visualization import (
        render_lattice,
        render_dial,
        render_tradition_heatmap,
        render_cluster_summary,
    )

    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"_Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_")
    lines.append("")

    if lattice is not None:
        lines.append("## Lattice Structure")
        lines.append("")
        lines.append(f"**Nodes:** {len(lattice.nodes)}  ")
        lines.append(f"**Edges:** {len(lattice.edges)}  ")
        lines.append("")
        lines.append("```")
        lines.append(render_lattice(lattice))
        lines.append("```")
        lines.append("")

    if dial is not None:
        lines.append("## Dial Positions")
        lines.append("")
        lines.append(f"**Positions:** {len(dial.positions)}  ")
        mean = dial.mean_angle()
        if mean is not None:
            import math
            lines.append(f"**Mean angle:** {math.degrees(mean):.1f}°  ")
        lines.append(f"**Diameter:** {math.degrees(dial.diameter()):.1f}°  ")
        lines.append("")
        lines.append("```")
        lines.append(render_dial(dial))
        lines.append("```")
        lines.append("")

    if traditions is not None:
        lines.append("## Traditions")
        lines.append("")
        lines.append(f"**Total:** {len(traditions.traditions)}  ")
        lines.append("")
        lines.append("### Score Heatmap")
        lines.append("")
        lines.append("```")
        lines.append(render_tradition_heatmap(traditions))
        lines.append("```")
        lines.append("")
        lines.append("### Cluster Summary")
        lines.append("")
        lines.append("```")
        lines.append(render_cluster_summary(traditions))
        lines.append("```")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Generated by constraint-toolkit*")
    return "\n".join(lines)


def export_report_file(
    path: str,
    lattice: ConstraintLattice | None = None,
    dial: DialSpace | None = None,
    traditions: TraditionCluster | None = None,
    title: str = "Constraint Analysis Report",
) -> None:
    """Write a Markdown report to a file."""
    report = generate_report(lattice=lattice, dial=dial, traditions=traditions, title=title)
    with open(path, "w") as f:
        f.write(report)
