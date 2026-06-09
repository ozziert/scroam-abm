from dataclasses import replace

import pytest

from scroam.config import SimulationConfig
from scroam.model import SCROAMModel, SUPPORTED_SCENARIOS


@pytest.mark.parametrize("scenario", SUPPORTED_SCENARIOS)
def test_model_runs_ten_steps_for_each_scenario(scenario: str) -> None:
    config = replace(SimulationConfig(), n_steps=10, n_agents=3)
    model = SCROAMModel(config=config, scenario=scenario, seed=7)

    summary = model.run()

    assert summary["scenario"] == scenario
    assert len(model.market_history) == 10
    assert len(model.agent_results) == 3
    assert 0.0 <= summary["stockout_rate"] <= 1.0
    assert 0.0 <= summary["average_service_level"] <= 1.0
