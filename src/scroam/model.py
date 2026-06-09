"""Core SCROAM simulation model."""

from __future__ import annotations

import numpy as np

from scroam.agents import ManufacturerAgent
from scroam.config import SimulationConfig
from scroam.insurance import ParametricNDBIContract
from scroam.p2p_pool import P2PLiquidityPool
from scroam.weather_price import WeatherPriceGenerator


SUPPORTED_SCENARIOS = (
    "safety_stock_only",
    "traditional_bi",
    "parametric_ndbi",
    "parametric_ndbi_p2p",
)


class SCROAMModel:
    """Plain-Python agent-based prototype for operational resilience analysis."""

    def __init__(
        self,
        config: SimulationConfig,
        scenario: str,
        seed: int,
    ) -> None:
        if scenario not in SUPPORTED_SCENARIOS:
            raise ValueError(
                f"Unsupported scenario {scenario!r}. "
                f"Choose from {SUPPORTED_SCENARIOS}."
            )

        self.config = config
        self.scenario = scenario
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.weather_price_generator = WeatherPriceGenerator(config, self.rng)
        self.insurance_contract = ParametricNDBIContract(
            deductible=config.insurance_deductible,
            policy_limit=config.insurance_limit,
            wind_trigger=config.wind_p10,
            price_trigger=config.price_trigger,
        )
        self.p2p_pool = P2PLiquidityPool(
            initial_capital=config.p2p_initial_capital,
            coverage_ratio=config.p2p_coverage_ratio,
        )
        self.agents = self._create_agents()
        self.market_history: list[dict[str, float | bool | int]] = []
        self.agent_results: list[dict[str, float | int]] = []
        self.summary: dict[str, float | int | str | bool] = {}

    def _create_agents(self) -> list[ManufacturerAgent]:
        energy_intensities = self.rng.normal(
            self.config.energy_intensity_mean,
            self.config.energy_intensity_std,
            self.config.n_agents,
        )
        energy_intensities = np.clip(energy_intensities, 0.01, None)

        return [
            ManufacturerAgent(
                agent_id=agent_id,
                inventory=self.config.initial_inventory,
                baseline_capacity=self.config.baseline_capacity,
                daily_demand=self.config.daily_demand,
                normal_price=self.config.normal_price,
                energy_intensity=float(energy_intensity),
                scenario=self.scenario,
                insurance_contract=self.insurance_contract,
                p2p_pool=self.p2p_pool,
                safety_stock_capacity_factor=(
                    self.config.safety_stock_capacity_factor
                ),
                traditional_bi_capacity_factor=(
                    self.config.traditional_bi_capacity_factor
                ),
            )
            for agent_id, energy_intensity in enumerate(energy_intensities)
        ]

    def run(self) -> dict[str, float | int | str | bool]:
        """Run all model steps and return the model-level KPI summary."""
        for step in range(self.config.n_steps):
            market_state = self.weather_price_generator.generate()
            self.market_history.append({"step": step, **market_state})
            for agent in self.agents:
                agent.step(market_state)

        self.agent_results = [agent.metrics() for agent in self.agents]
        self.summary = self._build_summary()
        return self.summary

    def _build_summary(self) -> dict[str, float | int | str | bool]:
        n_agents = len(self.agent_results)
        total_stockout_rate = sum(
            float(result["stockout_rate"]) for result in self.agent_results
        )
        total_service_level = sum(
            float(result["service_level"]) for result in self.agent_results
        )
        total_aicow = sum(
            float(result["total_aicow"]) for result in self.agent_results
        )
        total_insurance_payout = sum(
            float(result["total_insurance_payout"])
            for result in self.agent_results
        )
        total_p2p_payout = sum(
            float(result["total_p2p_payout"])
            for result in self.agent_results
        )
        residual_loss = sum(
            float(result["residual_loss"]) for result in self.agent_results
        )

        # Simplified v0.1 proxy; later versions can separate transfer costs,
        # premiums, pool contributions, and uncovered operational loss.
        total_system_cost = (
            residual_loss + total_insurance_payout + total_p2p_payout
        )

        return {
            "scenario": self.scenario,
            "seed": self.seed,
            "stockout_rate": total_stockout_rate / n_agents,
            "average_service_level": total_service_level / n_agents,
            "total_aicow": total_aicow,
            "total_insurance_payout": total_insurance_payout,
            "total_p2p_payout": total_p2p_payout,
            "residual_loss": residual_loss,
            "total_system_cost": total_system_cost,
            "pool_depleted": self.p2p_pool.depleted,
            "pool_remaining_capital": self.p2p_pool.remaining_capital,
        }
