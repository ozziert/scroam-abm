import numpy as np

from scroam.config import SimulationConfig
from scroam.weather_price import WeatherPriceGenerator


def test_weather_generator_returns_valid_market_state() -> None:
    generator = WeatherPriceGenerator(
        SimulationConfig(),
        rng=np.random.default_rng(42),
    )

    for _ in range(100):
        state = generator.generate()
        assert 0.0 <= state["wind_index"] <= 1.0
        assert state["spot_price"] >= 0.0
        assert isinstance(state["low_wind_event"], bool)
