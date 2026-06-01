"""
Visualization of spectral fingerprints and alignment structures.
Generates ASCII art plots (no matplotlib dependency).
"""

import numpy as np
from typing import List


def ascii_bar(values: List[float], labels: List[str], width: int = 50,
              title: str = "") -> str:
    """Generate an ASCII bar chart."""
    lines = []
    if title:
        lines.append(f"  {title}")
        lines.append(f"  {'─' * (width + 20)}")

    max_val = max(abs(v) for v in values) if values else 1
    for label, val in zip(labels, values):
        bar_len = int(abs(val) / max_val * width)
        bar = "█" * bar_len
        sign = "+" if val >= 0 else "-"
        lines.append(f"  {label:>15} │{sign}{bar} {val:+.4f}")

    return "\n".join(lines)


def ascii_eigenvalue_spectrum(eigenvalues: List[float],
                              agent_name: str = "") -> str:
    """Visualize eigenvalue spectrum as a spectral fingerprint."""
    lines = []
    lines.append(f"  Spectral Fingerprint: {agent_name}")
    lines.append(f"  {'─' * 60}")

    ev = eigenvalues
    if not ev:
        return "\n".join(lines) + "\n  (no eigenvalues)"

    max_ev = max(abs(e) for e in ev) if ev else 1
    max_ev = max(max_ev, 0.001)

    for i, e in enumerate(ev):
        bar_len = int(abs(e) / max_ev * 40)
        bar = "▓" * bar_len + "░" * (40 - bar_len)
        label = "λ₀" if i == 0 else f"λ{i}"
        lines.append(f"  {label:>3} │{bar}│ {e:.4f}")

    # Spectral gap
    if len(ev) > 1:
        gap = ev[1] - ev[0]
        lines.append(f"")
        lines.append(f"  Spectral gap (λ₁ - λ₀) = {gap:.4f}")

    return "\n".join(lines)


def ascii_alignment_heatmap(matrix: np.ndarray,
                            names: List[str]) -> str:
    """Generate an ASCII alignment heatmap."""
    lines = []
    lines.append("  Alignment Heatmap")
    lines.append(f"  {'─' * (len(names) * 8 + 12)}")

    n = len(names)

    # Color scale
    def heat_char(val: float) -> str:
        if val > 0.8:
            return "█"
        elif val > 0.6:
            return "▓"
        elif val > 0.4:
            return "▒"
        elif val > 0.2:
            return "░"
        elif val > 0:
            return "·"
        else:
            return " "

    header = "            " + "".join(f"{nm[:7]:>8}" for nm in names)
    lines.append(f"  {header}")

    for i in range(n):
        row_str = "".join(
            f" {matrix[i,j]:7.4f}" for j in range(n)
        )
        lines.append(f"  {names[i][:10]:>10} {row_str}")

    lines.append(f"")
    lines.append(f"  Scale: █ > 0.8  ▓ > 0.6  ▒ > 0.4  ░ > 0.2  · > 0  (blank ≤ 0)")

    return "\n".join(lines)


def ascii_fiedler_partition(fiedler: List[float],
                            agent_a_name: str, agent_b_name: str,
                            n_a: int, capabilities: List[str]) -> str:
    """Visualize Fiedler partition for task routing."""
    lines = []
    lines.append(f"  Fiedler Partition: {agent_a_name} ⊕ {agent_b_name}")
    lines.append(f"  {'─' * 60}")

    f = np.array(fiedler)
    median = np.median(f)

    # Sort by Fiedler value
    order = np.argsort(f)

    for idx in order:
        if idx < n_a:
            agent = agent_a_name
        else:
            agent = agent_b_name
        cap = capabilities[idx] if idx < len(capabilities) else f"cap-{idx}"
        val = f[idx]
        side = "←" if val < median else "→"
        bar_len = int(abs(val) / (max(abs(f)) + 1e-10) * 25)
        bar = "━" * bar_len

        lines.append(f"  {side} {cap[:15]:>15} [{agent[:12]:>12}] │{bar} {val:+.4f}")

    lines.append(f"")
    lines.append(f"  ← assigned to one agent  → assigned to other agent")

    return "\n".join(lines)
