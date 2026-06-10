"""Run the complete SCROAM v0.1.1 Monte Carlo demonstration."""

from pathlib import Path

from scroam.config import SimulationConfig
from scroam.experiments import run_monte_carlo
from scroam.metrics import create_clean_summary, summarize_results
from scroam.model import SUPPORTED_SCENARIOS
from scroam.visualization import plot_all_kpis


def format_clean_summary(clean_summary):
    """Format the scenario comparison for readable console output."""
    rate_columns = {
        "stockout_rate_mean",
        "average_service_level_mean",
    }
    formatters = {
        column: (
            (lambda value: f"{value:.4f}")
            if column in rate_columns
            else (lambda value: f"{value:,.2f}")
        )
        for column in clean_summary.columns
        if column != "scenario"
    }
    return clean_summary.to_string(index=False, formatters=formatters)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    results_dir = project_root / "outputs" / "results"
    figures_dir = project_root / "outputs" / "figures"
    results_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    config = SimulationConfig()
    results = run_monte_carlo(
        config=config,
        scenarios=SUPPORTED_SCENARIOS,
        n_runs=100,
    )
    summary = summarize_results(results)
    clean_summary = create_clean_summary(summary)

    results.to_csv(results_dir / "scroam_v01_results.csv", index=False)
    summary.to_csv(results_dir / "scroam_v01_summary.csv", index=False)
    clean_summary.to_csv(
        results_dir / "scroam_v01_clean_summary.csv",
        index=False,
    )
    plot_all_kpis(results, figures_dir)

    print("\nSCROAM v0.1.1 Scenario Comparison\n")
    print(format_clean_summary(clean_summary))


if __name__ == "__main__":
    main()
