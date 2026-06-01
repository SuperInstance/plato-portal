"""ASCII visualization of constraint spaces — lattice plots, dial positions, tradition clusters."""

from __future__ import annotations

import math
from typing import Sequence

from constraint_toolkit.lattice import ConstraintLattice, LatticeNode
from constraint_toolkit.dial import DialPosition, DialSpace
from constraint_toolkit.tradition import Tradition, TraditionCluster


def _pad(s: str, width: int) -> str:
    return s[:width].ljust(width)


# ---------------------------------------------------------------------------
# Lattice visualization
# ---------------------------------------------------------------------------

def render_lattice(lattice: ConstraintLattice, width: int = 60, height: int = 20) -> str:
    """Render a constraint lattice as an ASCII art diagram.

    Nodes are arranged by level (bottom-up). Edges shown with pipes and dashes.
    """
    if not lattice.nodes:
        return "(empty lattice)"

    # Group nodes by level
    levels: dict[int, list[LatticeNode]] = {}
    for node in lattice.nodes:
        levels.setdefault(node.level, []).append(node)

    if not levels:
        return "(empty lattice)"

    min_level = min(levels)
    max_level = max(levels)
    num_levels = max_level - min_level + 1

    lines: list[str] = []
    edge_set = set(lattice.edges)

    for lvl in range(max_level, min_level - 1, -1):
        nodes_at = levels.get(lvl, [])
        # Render node row
        if not nodes_at:
            continue
        max_name_len = max(len(nd.name) + 2 for nd in nodes_at) if nodes_at else 4
        spacing = max(width // (len(nodes_at) + 1), max_name_len)
        positions = [spacing * (i + 1) for i in range(len(nodes_at))]
        row = [" "] * (max(positions) + max_name_len + 2) if positions else []
        for i, nd in enumerate(nodes_at):
            label = f"[{nd.name}]"
            start = positions[i] - len(label) // 2
            for ci, ch in enumerate(label):
                idx = start + ci
                if 0 <= idx < len(row):
                    row[idx] = ch
        lines.append("".join(row).rstrip())

        # Render edges to next level down
        next_lvl = lvl - 1
        next_nodes = levels.get(next_lvl, [])
        if next_nodes and edge_set:
            edge_lines = _render_lattice_edges(
                nodes_at, next_nodes, edge_set, positions, width
            )
            lines.extend(edge_lines)

    return "\n".join(lines)


def _render_lattice_edges(
    upper: list[LatticeNode],
    lower: list[LatticeNode],
    edge_set: set[tuple[str, str]],
    upper_positions: list[int],
    width: int,
) -> list[str]:
    """Render edge connections between two levels."""
    max_name_len = max((len(nd.name) + 2 for nd in lower), default=4)
    spacing = max(width // (len(lower) + 1), max_name_len)
    lower_positions = [spacing * (i + 1) for i in range(len(lower))]

    conn_line = [" "] * (max(max(upper_positions), max(lower_positions)) + 10)

    for ui, unode in enumerate(upper):
        for li, lnode in enumerate(lower):
            if (unode.name, lnode.name) in edge_set:
                start = min(upper_positions[ui], lower_positions[li])
                end = max(upper_positions[ui], lower_positions[li])
                mid = (start + end) // 2
                if 0 <= mid < len(conn_line):
                    conn_line[mid] = "|"

    rendered = "".join(conn_line).rstrip()
    return [rendered] if rendered.strip() else []


# ---------------------------------------------------------------------------
# Dial visualization
# ---------------------------------------------------------------------------

def render_dial(space: DialSpace, radius: int = 8) -> str:
    """Render a dial space as an ASCII circular plot.

    Positions are plotted on a circle. The center is marked with '+'.
    """
    if not space.positions:
        return "(empty dial)"

    size = 2 * radius + 3
    grid: list[list[str]] = [[" "] * size for _ in range(size)]
    cx, cy = size // 2, size // 2
    grid[cy][cx] = "+"

    # Draw circle outline
    for deg in range(0, 360, 10):
        rad = math.radians(deg)
        x = cx + int(radius * math.cos(rad))
        y = cy - int(radius * math.sin(rad))
        if 0 <= y < size and 0 <= x < size:
            grid[y][x] = "·"

    # Plot positions
    for pos in space.positions:
        x = cx + int(radius * pos.angle / (2 * math.pi) * 2 * math.pi / (2 * math.pi) * radius * 0.9)
        # Proper cartesian mapping
        px = cx + int((radius - 1) * math.cos(pos.angle))
        py = cy - int((radius - 1) * math.sin(pos.angle))
        if 0 <= py < size and 0 <= px < size:
            # Use first char of name or '*'
            ch = pos.name[0] if pos.name else "*"
            grid[py][px] = ch

    # Legend
    lines = ["".join(row).rstrip() for row in grid]
    lines.append("")
    for pos in space.positions:
        deg = math.degrees(pos.angle)
        lines.append(f"  {pos.name}: {deg:.1f}° (r={pos.radius:.2f})")

    return "\n".join(lines)


def render_dial_histogram(space: DialSpace, bins: int = 12) -> str:
    """Render an ASCII histogram of dial positions binned by angle."""
    if not space.positions:
        return "(empty dial)"

    bin_width = 2 * math.pi / bins
    counts = [0] * bins
    for pos in space.positions:
        idx = int(pos.angle / bin_width) % bins
        counts[idx] += 1

    max_count = max(counts) if counts else 1
    max_bar = 30
    lines: list[str] = []
    for i in range(bins):
        deg_start = math.degrees(i * bin_width)
        deg_end = math.degrees((i + 1) * bin_width)
        bar_len = int(counts[i] / max_count * max_bar) if max_count else 0
        bar = "█" * bar_len
        lines.append(f"{deg_start:6.1f}°-{deg_end:6.1f}° |{bar} ({counts[i]})")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Tradition cluster visualization
# ---------------------------------------------------------------------------

def render_tradition_heatmap(
    cluster: TraditionCluster, keys: Sequence[str] | None = None, width: int = 40
) -> str:
    """Render tradition scores as an ASCII heatmap.

    Each row is a tradition, columns are score dimensions.
    """
    traditions = cluster.traditions
    if not traditions:
        return "(empty traditions)"

    all_keys = list(keys or sorted({k for t in traditions for k in t.scores}))
    if not all_keys:
        return "(no scores)"

    max_name = max(len(t.name) for t in traditions)
    heat_chars = " ░▒▓█"

    lines: list[str] = []
    # Header
    header = _pad("Tradition", max_name + 2)
    for key in all_keys:
        header += _pad(key, max(len(key) + 1, 6))
    lines.append(header)
    lines.append("-" * len(header))

    for t in traditions:
        row = _pad(t.name, max_name + 2)
        for key in all_keys:
            val = t.scores.get(key, 0.0)
            # Map 0-10 scale to heat chars
            normalized = max(0.0, min(val / 10.0, 1.0)) if val else 0.0
            idx = int(normalized * (len(heat_chars) - 1))
            idx = min(idx, len(heat_chars) - 1)
            cell = f"{heat_chars[idx]}{val:.1f}"
            row += _pad(cell, max(len(key) + 1, 6))
        lines.append(row)

    return "\n".join(lines)


def render_cluster_summary(
    tc: TraditionCluster, threshold: float = 1.0
) -> str:
    """Render a summary of tradition clusters."""
    clusters = tc.cluster_by_distance(threshold)
    if not clusters:
        return "(no traditions to cluster)"

    lines: list[str] = []
    for i, group in enumerate(clusters):
        centroid = tc.centroid_scores(group)
        lines.append(f"Cluster {i + 1} ({len(group)} traditions):")
        for t in group:
            lines.append(f"  • {t.name} [{t.category}]")
        if centroid:
            scores_str = ", ".join(f"{k}={v:.2f}" for k, v in sorted(centroid.items()))
            lines.append(f"  centroid: {scores_str}")
        lines.append("")

    return "\n".join(lines).rstrip()
