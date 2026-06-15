#!/usr/bin/env python3
"""
Conservation Law Reporting Pipeline — Approach C (Hybrid)

Usage:
    python fleet-metrics/main.py [--data PATH] [--budget C] [--target-n N]

Reads real fleet data from fleet-metrics/data/metrics.json if it exists;
otherwise generates theoretical data via CLT delta formula.
Outputs:
    fleet-metrics/reports/conservation_report_YYYYMMDD.json
    fleet-metrics/visualizations/scaling_curve.svg
    fleet-metrics/visualizations/cancellation_plot.svg
"""

import argparse
import os
import sys

# Allow running from repo root or from fleet-metrics/ directory.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from conservation_law import load_or_generate_metrics
from reports import generate_report
from visualizations import cancellation_plot_svg, scaling_curve_svg


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument(
        "--data",
        default=os.path.join(_HERE, "data", "metrics.json"),
        help="Path to real fleet metrics JSON (default: fleet-metrics/data/metrics.json)",
    )
    p.add_argument(
        "--budget", type=float, default=1.0,
        help="Total budget C for gamma+eta model (default: 1.0)",
    )
    p.add_argument(
        "--target-n", type=int, default=50,
        help="Target agent count for headline stats (default: 50)",
    )
    p.add_argument(
        "--reports-dir",
        default=os.path.join(_HERE, "reports"),
        help="Output directory for JSON reports",
    )
    p.add_argument(
        "--viz-dir",
        default=os.path.join(_HERE, "visualizations"),
        help="Output directory for SVG visualizations",
    )
    return p.parse_args()


def main() -> None:
    args = _parse_args()

    print("Conservation Law Reporting Pipeline")
    print("=" * 50)

    # 1. Load or generate metrics
    metrics = load_or_generate_metrics(args.data)
    source = metrics.get("source", "file")
    n_points = len(metrics["agents"])
    print(f"  Data source : {source}")
    print(f"  Agent range : n=1..{n_points}")
    if source == "theoretical":
        print(f"  Formula     : {metrics['formula']}")

    # 2. Generate JSON report
    report_path, report = generate_report(
        output_dir=args.reports_dir,
        data_path=args.data,
        C=args.budget,
        target_n=args.target_n,
    )
    hl = report["headline"]
    savings = report["cost_savings"]
    print()
    print(f"  [report] {report_path}")
    print(f"    n={hl['n_agents']}: CCR = {hl['coupling_cancellation_rate_pct']:.4f}%"
          f"  (target {hl['target_cancellation_pct']}%,"
          f" within tolerance: {hl['within_tolerance']})")
    print(f"    Productive spend : {hl['productive_spend_pct']:.2f}%")
    print(f"    Overhead spend   : {hl['overhead_spend_pct']:.2f}%")
    print(f"    Cost savings     : {savings['description']}")

    # 3. Generate SVG visualizations
    svg1 = scaling_curve_svg(metrics, output_dir=args.viz_dir)
    svg2 = cancellation_plot_svg(metrics, output_dir=args.viz_dir)
    print()
    print(f"  [svg] {svg1}")
    print(f"  [svg] {svg2}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
