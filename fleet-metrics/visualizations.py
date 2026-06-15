"""
SVG chart generators using only xml.etree.ElementTree.

Produces two charts:
  - scaling_curve.svg     — delta(n) vs agent count
  - cancellation_plot.svg — coupling_cancellation_rate(n) vs agent count
"""

import os
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def _tag(name: str) -> str:
    return f"{{{SVG_NS}}}{name}"


def _svg_root(width: int, height: int, title: str) -> ET.Element:
    root = ET.Element(_tag("svg"), {
        "width": str(width),
        "height": str(height),
        "viewBox": f"0 0 {width} {height}",
        "xmlns": SVG_NS,
    })
    t = ET.SubElement(root, _tag("title"))
    t.text = title
    # White background
    ET.SubElement(root, _tag("rect"), {
        "width": str(width), "height": str(height),
        "fill": "#0f1117",
    })
    return root


def _make_chart(
    root: ET.Element,
    xs: list,
    ys: list,
    *,
    margin_left: int = 70,
    margin_right: int = 30,
    margin_top: int = 50,
    margin_bottom: int = 60,
    width: int,
    height: int,
    line_color: str,
    fill_color: str,
    title: str,
    x_label: str,
    y_label: str,
    highlight_n: int = 50,
    y_format: str = "{:.3f}",
) -> None:
    pw = width - margin_left - margin_right
    ph = height - margin_top - margin_bottom

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    y_range = y_max - y_min or 1.0
    # Add 10% padding on y
    y_pad = y_range * 0.1
    y_lo = y_min - y_pad
    y_hi = y_max + y_pad

    def tx(x):
        return margin_left + (x - x_min) / (x_max - x_min) * pw

    def ty(y):
        return margin_top + ph - (y - y_lo) / (y_hi - y_lo) * ph

    # --- Title ---
    t = ET.SubElement(root, _tag("text"), {
        "x": str(width // 2),
        "y": str(margin_top - 18),
        "text-anchor": "middle",
        "font-family": "monospace",
        "font-size": "14",
        "font-weight": "bold",
        "fill": "#e2e8f0",
    })
    t.text = title

    # --- Area fill (polygon under curve) ---
    baseline_y = ty(max(y_lo, 0.0))
    poly_pts = (
        [f"{tx(xs[0])},{baseline_y}"]
        + [f"{tx(x)},{ty(y)}" for x, y in zip(xs, ys)]
        + [f"{tx(xs[-1])},{baseline_y}"]
    )
    ET.SubElement(root, _tag("polygon"), {
        "points": " ".join(poly_pts),
        "fill": fill_color,
        "opacity": "0.25",
    })

    # --- Curve ---
    pts = " ".join(f"{tx(x)},{ty(y)}" for x, y in zip(xs, ys))
    ET.SubElement(root, _tag("polyline"), {
        "points": pts,
        "fill": "none",
        "stroke": line_color,
        "stroke-width": "2.2",
        "stroke-linejoin": "round",
        "stroke-linecap": "round",
    })

    # --- Axes ---
    # X axis
    y_zero = max(margin_top, min(margin_top + ph, ty(0.0)))
    ET.SubElement(root, _tag("line"), {
        "x1": str(margin_left), "y1": str(y_zero),
        "x2": str(margin_left + pw), "y2": str(y_zero),
        "stroke": "#4a5568", "stroke-width": "1",
    })
    # Y axis
    ET.SubElement(root, _tag("line"), {
        "x1": str(margin_left), "y1": str(margin_top),
        "x2": str(margin_left), "y2": str(margin_top + ph),
        "stroke": "#4a5568", "stroke-width": "1",
    })

    # --- X ticks ---
    tick_ns = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    for n in tick_ns:
        if n < x_min or n > x_max:
            continue
        xp = tx(n)
        ET.SubElement(root, _tag("line"), {
            "x1": str(xp), "y1": str(margin_top + ph),
            "x2": str(xp), "y2": str(margin_top + ph + 5),
            "stroke": "#718096", "stroke-width": "1",
        })
        lbl = ET.SubElement(root, _tag("text"), {
            "x": str(xp),
            "y": str(margin_top + ph + 18),
            "text-anchor": "middle",
            "font-family": "monospace",
            "font-size": "10",
            "fill": "#a0aec0",
        })
        lbl.text = str(n)

    # --- Y ticks (5 evenly spaced) ---
    for i in range(6):
        yv = y_lo + i * (y_hi - y_lo) / 5.0
        yp = ty(yv)
        ET.SubElement(root, _tag("line"), {
            "x1": str(margin_left - 5), "y1": str(yp),
            "x2": str(margin_left), "y2": str(yp),
            "stroke": "#718096", "stroke-width": "1",
        })
        # Gridline
        ET.SubElement(root, _tag("line"), {
            "x1": str(margin_left), "y1": str(yp),
            "x2": str(margin_left + pw), "y2": str(yp),
            "stroke": "#2d3748", "stroke-width": "1",
            "stroke-dasharray": "4,4",
        })
        lbl = ET.SubElement(root, _tag("text"), {
            "x": str(margin_left - 8),
            "y": str(yp + 4),
            "text-anchor": "end",
            "font-family": "monospace",
            "font-size": "10",
            "fill": "#a0aec0",
        })
        lbl.text = y_format.format(yv)

    # --- Axis labels ---
    xl = ET.SubElement(root, _tag("text"), {
        "x": str(margin_left + pw // 2),
        "y": str(margin_top + ph + 45),
        "text-anchor": "middle",
        "font-family": "monospace",
        "font-size": "12",
        "fill": "#cbd5e0",
    })
    xl.text = x_label

    yl = ET.SubElement(root, _tag("text"), {
        "x": str(-(margin_top + ph // 2)),
        "y": "16",
        "text-anchor": "middle",
        "font-family": "monospace",
        "font-size": "12",
        "fill": "#cbd5e0",
        "transform": "rotate(-90)",
    })
    yl.text = y_label

    # --- Highlight point at n=50 ---
    if x_min <= highlight_n <= x_max:
        hi = xs.index(highlight_n)
        hx, hy_val = tx(highlight_n), ty(ys[hi])
        ET.SubElement(root, _tag("circle"), {
            "cx": str(hx), "cy": str(hy_val), "r": "5",
            "fill": "#f6ad55", "stroke": "#fff", "stroke-width": "1.5",
        })
        ET.SubElement(root, _tag("line"), {
            "x1": str(hx), "y1": str(hy_val),
            "x2": str(hx), "y2": str(margin_top + ph),
            "stroke": "#f6ad55", "stroke-width": "1",
            "stroke-dasharray": "3,3",
        })
        ann = ET.SubElement(root, _tag("text"), {
            "x": str(hx + 7),
            "y": str(hy_val - 8),
            "font-family": "monospace",
            "font-size": "10",
            "fill": "#f6ad55",
        })
        ann.text = f"n=50: {y_format.format(ys[hi])}"


def _write_svg(root: ET.Element, path: str) -> None:
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    with open(path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write(ET.tostring(root, encoding="unicode"))
        f.write("\n")


def scaling_curve_svg(
    metrics: dict,
    output_dir: str = "fleet-metrics/visualizations",
) -> str:
    """Write scaling_curve.svg — delta(n) vs agent count."""
    os.makedirs(output_dir, exist_ok=True)

    agents = metrics["agents"]
    xs = [e["n"] for e in agents]
    ys = [e["delta"] for e in agents]

    W, H = 820, 480
    root = _svg_root(W, H, "CLT Coupling Correction: delta(n) vs Agent Count")
    _make_chart(
        root, xs, ys,
        width=W, height=H,
        line_color="#63b3ed",
        fill_color="#63b3ed",
        title="CLT Scaling Curve: δ(n) = (1/√n)(1 − 3/2n)",
        x_label="Agent Count (n)",
        y_label="δ(n)  [coupling correction]",
        highlight_n=50,
        y_format="{:.4f}",
    )

    path = os.path.join(output_dir, "scaling_curve.svg")
    _write_svg(root, path)
    return path


def cancellation_plot_svg(
    metrics: dict,
    output_dir: str = "fleet-metrics/visualizations",
) -> str:
    """Write cancellation_plot.svg — coupling_cancellation_rate(n) vs agent count."""
    os.makedirs(output_dir, exist_ok=True)

    agents = metrics["agents"]
    xs = [e["n"] for e in agents]
    ys = [e["coupling_cancellation_rate"] for e in agents]

    W, H = 820, 480
    root = _svg_root(W, H, "Coupling Cancellation Rate vs Agent Count")
    _make_chart(
        root, xs, ys,
        width=W, height=H,
        line_color="#68d391",
        fill_color="#68d391",
        title="Coupling Cancellation Rate: 1 − δ(n)   [target 86.4% @ n=50]",
        x_label="Agent Count (n)",
        y_label="Cancellation Rate",
        highlight_n=50,
        y_format="{:.3f}",
    )

    # Target line at 86.4%
    target_y = 0.864
    margin_left, margin_right, margin_top, margin_bottom = 70, 30, 50, 60
    pw = W - margin_left - margin_right
    ph = H - margin_top - margin_bottom
    all_ys = ys
    y_lo = min(all_ys) - (max(all_ys) - min(all_ys)) * 0.1
    y_hi = max(all_ys) + (max(all_ys) - min(all_ys)) * 0.1
    ty_target = margin_top + ph - (target_y - y_lo) / (y_hi - y_lo) * ph
    ET.SubElement(root, _tag("line"), {
        "x1": str(margin_left), "y1": str(ty_target),
        "x2": str(margin_left + pw), "y2": str(ty_target),
        "stroke": "#fc8181", "stroke-width": "1.5",
        "stroke-dasharray": "6,3",
    })
    lbl = ET.SubElement(root, _tag("text"), {
        "x": str(margin_left + pw - 4),
        "y": str(ty_target - 5),
        "text-anchor": "end",
        "font-family": "monospace",
        "font-size": "10",
        "fill": "#fc8181",
    })
    lbl.text = "target 86.4%"

    path = os.path.join(output_dir, "cancellation_plot.svg")
    _write_svg(root, path)
    return path
