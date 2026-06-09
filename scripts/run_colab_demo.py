"""Run the complete SCROAM v0.1 Monte Carlo demonstration."""

from pathlib import Path

from scroam.config import SimulationConfig
from scroam.experiments import run_monte_carlo
from scroam.metrics import summarize_results
from scroam.model import SUPPORTED_SCENARIOS
from scroam.visualization import plot_all_kpis


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

    results.to_csv(results_dir / "scroam_v01_results.csv", index=False)
    summary.to_csv(results_dir / "scroam_v01_summary.csv", index=False)
    plot_all_kpis(results, figures_dir)

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
