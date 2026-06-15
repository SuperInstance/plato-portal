"""Generate JSON conservation law cost savings reports."""

import json
import os
from datetime import datetime

from budget import budget_summary, cost_savings_analysis
from conservation_law import load_or_generate_metrics


def generate_report(
    output_dir: str = "fleet-metrics/reports",
    data_path: str = "fleet-metrics/data/metrics.json",
    C: float = 1.0,
    target_n: int = 50,
) -> tuple:
    """
    Build and write the conservation report JSON.

    Returns (file_path, report_dict).
    """
    os.makedirs(output_dir, exist_ok=True)

    metrics = load_or_generate_metrics(data_path)
    budget = budget_summary(metrics, C=C)
    savings = cost_savings_analysis(budget, target_n=target_n)

    target_agent = next(e for e in metrics["agents"] if e["n"] == target_n)
    target_budget = next(r for r in budget if r["n"] == target_n)

    ccr_pct = round(target_agent["coupling_cancellation_rate"] * 100.0, 4)

    report = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "data_source": metrics.get("source", "file"),
        "formula": metrics.get("formula", ""),
        "budget_model": "gamma + eta = C",
        "headline": {
            "n_agents": target_n,
            "coupling_cancellation_rate_pct": ccr_pct,
            "target_cancellation_pct": 86.4,
            "within_tolerance": abs(ccr_pct - 86.4) < 1.0,
            "productive_spend_pct": target_budget["productive_pct"],
            "overhead_spend_pct": target_budget["overhead_pct"],
        },
        "cost_savings": savings,
        "agent_budget_table": budget,
    }

    date_str = datetime.utcnow().strftime("%Y%m%d")
    path = os.path.join(output_dir, f"conservation_report_{date_str}.json")
    with open(path, "w") as f:
        json.dump(report, f, indent=2)

    return path, report
