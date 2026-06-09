"""Experiment runners for single simulations and Monte Carlo analysis."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

from scroam.config import SimulationConfig
from scroam.model import SCROAMModel


def run_single_simulation(
    scenario: str,
    config: SimulationConfig,
    seed: int,
) -> dict[str, float | int | str | bool]:
    """Run one reproducible SCROAM simulation."""
    model = SCROAMModel(config=config, scenario=scenario, seed=seed)
    return model.run()


def run_monte_carlo(
    config: SimulationConfig,
    scenarios: Iterable[str],
    n_runs: int,
) -> pd.DataFrame:
    """Return one result row for every scenario and Monte Carlo seed."""
    if n_runs <= 0:
        raise ValueError("n_runs must be positive")

    rows = [
        run_single_simulation(scenario=scenario, config=config, seed=seed)
        for scenario in scenarios
        for seed in range(n_runs)
    ]
    return pd.DataFrame(rows)
