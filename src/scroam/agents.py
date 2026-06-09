"""Manufacturing agent and operational resilience logic."""

from __future__ import annotations

from scroam.insurance import ParametricNDBIContract
from scroam.p2p_pool import P2PLiquidityPool


PARAMETRIC_SCENARIOS = {"parametric_ndbi", "parametric_ndbi_p2p"}


class ManufacturerAgent:
    """A manufacturer exposed to electricity-price-driven AICOW."""

    def __init__(
        self,
        agent_id: int,
        inventory: float,
        baseline_capacity: float,
        daily_demand: float,
        normal_price: float,
        energy_intensity: float,
        scenario: str,
        insurance_contract: ParametricNDBIContract,
        p2p_pool: P2PLiquidityPool,
        safety_stock_capacity_factor: float,
        traditional_bi_capacity_factor: float,
    ) -> None:
        self.agent_id = agent_id
        self.inventory = float(inventory)
        self.baseline_capacity = float(baseline_capacity)
        self.daily_demand = float(daily_demand)
        self.normal_price = float(normal_price)
        self.energy_intensity = float(energy_intensity)
        self.scenario = scenario
        self.insurance_contract = insurance_contract
        self.p2p_pool = p2p_pool
        self.safety_stock_capacity_factor = safety_stock_capacity_factor
        self.traditional_bi_capacity_factor = traditional_bi_capacity_factor

        self.total_aicow = 0.0
        self.total_insurance_payout = 0.0
        self.total_p2p_payout = 0.0
        self.total_residual_loss = 0.0
        self.stockout_days = 0
        self.total_demand = 0.0
        self.total_fulfilled = 0.0
        self.total_production = 0.0
        self.steps_completed = 0

    def step(self, market_state: dict[str, float | bool]) -> None:
        """Advance the manufacturer's inventory and financial state by one day."""
        wind_index = float(market_state["wind_index"])
        spot_price = float(market_state["spot_price"])
        planned_production = self.baseline_capacity

        aicow = (
            max(spot_price - self.normal_price, 0.0)
            * self.energy_intensity
            * planned_production
        )

        insurance_payout = 0.0
        if self.scenario in PARAMETRIC_SCENARIOS:
            insurance_payout, _ = self.insurance_contract.evaluate(
                wind_index=wind_index,
                spot_price=spot_price,
                estimated_aicow=aicow,
            )

        residual_after_insurance = max(aicow - insurance_payout, 0.0)
        p2p_payout = 0.0
        if self.scenario == "parametric_ndbi_p2p":
            p2p_payout = self.p2p_pool.cover(residual_after_insurance)

        residual_loss = max(
            aicow - insurance_payout - p2p_payout,
            0.0,
        )
        funded_amount = insurance_payout + p2p_payout

        effective_capacity = self.baseline_capacity
        if aicow > 0:
            funded_ratio = min(funded_amount / aicow, 1.0)
            effective_capacity = self.baseline_capacity * funded_ratio

            # Comparator scenarios approximate non-parametric coping capacity.
            if self.scenario == "safety_stock_only":
                effective_capacity = (
                    self.baseline_capacity
                    * self.safety_stock_capacity_factor
                )
            elif self.scenario == "traditional_bi":
                effective_capacity = (
                    self.baseline_capacity
                    * self.traditional_bi_capacity_factor
                )

        production = effective_capacity
        self.inventory += production
        fulfilled = min(self.daily_demand, self.inventory)
        self.inventory -= fulfilled

        if fulfilled < self.daily_demand:
            self.stockout_days += 1

        self.total_aicow += aicow
        self.total_insurance_payout += insurance_payout
        self.total_p2p_payout += p2p_payout
        self.total_residual_loss += residual_loss
        self.total_demand += self.daily_demand
        self.total_fulfilled += fulfilled
        self.total_production += production
        self.steps_completed += 1

    def metrics(self) -> dict[str, float | int]:
        """Return thesis KPIs for this manufacturer."""
        stockout_rate = (
            self.stockout_days / self.steps_completed
            if self.steps_completed
            else 0.0
        )
        service_level = (
            self.total_fulfilled / self.total_demand
            if self.total_demand
            else 1.0
        )
        return {
            "agent_id": self.agent_id,
            "stockout_rate": stockout_rate,
            "service_level": service_level,
            "total_aicow": self.total_aicow,
            "total_insurance_payout": self.total_insurance_payout,
            "total_p2p_payout": self.total_p2p_payout,
            "residual_loss": self.total_residual_loss,
            "total_production": self.total_production,
            "ending_inventory": self.inventory,
        }
