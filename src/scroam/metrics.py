"""Result summarization helpers."""

from __future__ import annotations

import pandas as pd


MAJOR_KPIS = [
    "stockout_rate",
    "average_service_level",
    "total_aicow",
    "total_insurance_payout",
    "total_p2p_payout",
    "residual_loss",
    "total_system_cost",
    "pool_remaining_capital",
]


def summarize_results(results_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate mean, standard deviation, minimum, and maximum by scenario."""
    missing_columns = {"scenario", *MAJOR_KPIS} - set(results_df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"results_df is missing required columns: {missing}")

    summary = results_df.groupby("scenario")[MAJOR_KPIS].agg(
        ["mean", "std", "min", "max"]
    )
    summary.columns = [
        f"{kpi}_{statistic}" for kpi, statistic in summary.columns
    ]
    return summary.reset_index()
