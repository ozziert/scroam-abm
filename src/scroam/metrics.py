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

CLEAN_SUMMARY_COLUMNS = [
    "scenario",
    "stockout_rate_mean",
    "average_service_level_mean",
    "residual_loss_mean",
    "total_system_cost_mean",
    "total_insurance_payout_mean",
    "total_p2p_payout_mean",
    "pool_remaining_capital_mean",
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


def create_clean_summary(summary_df: pd.DataFrame) -> pd.DataFrame:
    """Return the thesis-facing scenario comparison columns."""
    missing_columns = set(CLEAN_SUMMARY_COLUMNS) - set(summary_df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"summary_df is missing required columns: {missing}")

    return summary_df[CLEAN_SUMMARY_COLUMNS].copy()
