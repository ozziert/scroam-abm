"""Shared peer-to-peer liquidity pool."""


class P2PLiquidityPool:
    """Finite shared capital used to fund residual AICOW after insurance."""

    def __init__(self, initial_capital: float, coverage_ratio: float) -> None:
        if initial_capital < 0:
            raise ValueError("initial_capital must be non-negative")
        if not 0 <= coverage_ratio <= 1:
            raise ValueError("coverage_ratio must be between 0 and 1")

        self.initial_capital = float(initial_capital)
        self.current_capital = float(initial_capital)
        self.coverage_ratio = float(coverage_ratio)
        self.total_paid = 0.0

    def cover(self, residual_loss: float) -> float:
        """Cover a share of residual loss, subject to remaining capital."""
        requested = max(float(residual_loss), 0.0) * self.coverage_ratio
        payout = min(requested, self.current_capital)
        self.current_capital -= payout
        self.total_paid += payout
        return float(payout)

    @property
    def depleted(self) -> bool:
        """Whether no usable capital remains."""
        return self.current_capital <= 0.0

    @property
    def remaining_capital(self) -> float:
        """Capital still available for future shocks."""
        return self.current_capital
