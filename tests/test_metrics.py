import pandas as pd
import pytest

from scroam.metrics import CLEAN_SUMMARY_COLUMNS, create_clean_summary


def test_create_clean_summary_selects_thesis_comparison_columns() -> None:
    summary = pd.DataFrame(
        {
            "scenario": ["parametric_ndbi"],
            "stockout_rate_mean": [0.25],
            "average_service_level_mean": [0.75],
            "residual_loss_mean": [100.0],
            "total_system_cost_mean": [150.0],
            "total_insurance_payout_mean": [50.0],
            "total_p2p_payout_mean": [0.0],
            "pool_remaining_capital_mean": [300_000.0],
            "total_aicow_mean": [150.0],
        }
    )

    clean_summary = create_clean_summary(summary)

    assert clean_summary.columns.tolist() == CLEAN_SUMMARY_COLUMNS
    assert clean_summary.loc[0, "scenario"] == "parametric_ndbi"
    assert "total_aicow_mean" not in clean_summary.columns


def test_create_clean_summary_rejects_missing_columns() -> None:
    with pytest.raises(
        ValueError,
        match="summary_df is missing required columns",
    ):
        create_clean_summary(pd.DataFrame({"scenario": ["traditional_bi"]}))
