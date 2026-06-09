"""Matplotlib visualizations for scenario comparison."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DEFAULT_PLOT_KPIS = [
    "stockout_rate",
    "average_service_level",
    "total_aicow",
    "total_insurance_payout",
    "total_p2p_payout",
    "residual_loss",
    "total_system_cost",
    "pool_remaining_capital",
]


def plot_scenario_bar(
    results_df: pd.DataFrame,
    kpi: str,
    output_path: str | Path | None = None,
) -> plt.Figure:
    """Plot mean KPI values by scenario with one-standard-deviation error bars."""
    if kpi not in results_df.columns:
        raise ValueError(f"Unknown KPI column: {kpi}")

    grouped = results_df.groupby("scenario")[kpi].agg(["mean", "std"])
    grouped["std"] = grouped["std"].fillna(0.0)

    figure, axis = plt.subplots(figsize=(9, 5))
    grouped["mean"].plot(
        kind="bar",
        yerr=grouped["std"],
        capsize=4,
        color="#3A6EA5",
        edgecolor="black",
        ax=axis,
    )
    axis.set_title(f"SCROAM scenario comparison: {kpi.replace('_', ' ').title()}")
    axis.set_xlabel("Scenario")
    axis.set_ylabel(kpi.replace("_", " ").title())
    axis.tick_params(axis="x", rotation=25)
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()

    if output_path is not None:
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(destination, dpi=150, bbox_inches="tight")

    return figure


def plot_all_kpis(
    results_df: pd.DataFrame,
    output_dir: str | Path = "outputs/figures",
) -> list[Path]:
    """Generate and save one scenario bar chart for each major KPI."""
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    saved_paths = []

    for kpi in DEFAULT_PLOT_KPIS:
        output_path = destination / f"{kpi}.png"
        figure = plot_scenario_bar(results_df, kpi, output_path)
        plt.close(figure)
        saved_paths.append(output_path)

    return saved_paths
