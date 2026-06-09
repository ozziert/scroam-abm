"""Parametric non-damage business interruption insurance."""

from __future__ import annotations


class ParametricNDBIContract:
    """Parametric insurance linked to operational AICOW exposure.

    The contract is not an electricity derivative. Its external wind and price
    trigger releases a payout against an estimated Additional Increased Cost of
    Working (AICOW) incurred by the manufacturing operation.
    """

    def __init__(
        self,
        deductible: float,
        policy_limit: float,
        wind_trigger: float,
        price_trigger: float,
    ) -> None:
        self.deductible = deductible
        self.policy_limit = policy_limit
        self.wind_trigger = wind_trigger
        self.price_trigger = price_trigger

    def evaluate(
        self,
        wind_index: float,
        spot_price: float,
        estimated_aicow: float,
    ) -> tuple[float, bool]:
        """Return the operational AICOW payout and trigger status."""
        triggered = (
            wind_index < self.wind_trigger
            and spot_price > self.price_trigger
        )
        if not triggered:
            return 0.0, False

        payout = min(
            max(estimated_aicow - self.deductible, 0.0),
            self.policy_limit,
        )
        return float(payout), True
