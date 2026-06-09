"""Synthetic low-wind and electricity spot-price mechanism."""

from __future__ import annotations

import numpy as np

from scroam.config import SimulationConfig


class WeatherPriceGenerator:
    """Generate plausible market states without acting as a price forecast."""

    def __init__(
        self,
        config: SimulationConfig,
        rng: np.random.Generator | None = None,
    ) -> None:
        self.config = config
        self.rng = rng or np.random.default_rng()

    def generate(self) -> dict[str, float | bool]:
        """Return one synthetic daily wind and spot-price observation."""
        wind_index = float(self.rng.beta(2.0, 5.0))
        low_wind_event = wind_index < self.config.wind_p10
        noise = float(self.rng.normal(0.0, self.config.noise_std))

        spot_price = (
            self.config.base_price
            + self.config.alpha * (1.0 - wind_index)
            + noise
        )
        if low_wind_event:
            spot_price += self.config.spike_intensity

        return {
            "wind_index": wind_index,
            "spot_price": max(float(spot_price), 0.0),
            "low_wind_event": bool(low_wind_event),
        }
