"""Configuration for the SCROAM simulation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationConfig:
    """Transparent model parameters collected in one reproducible object."""

    n_steps: int = 365
    n_agents: int = 20
    daily_demand: float = 100
    baseline_capacity: float = 110
    initial_inventory: float = 300
    base_price: float = 80
    normal_price: float = 80
    alpha: float = 120
    noise_std: float = 15
    wind_p10: float = 0.10
    spike_intensity: float = 100
    energy_intensity_mean: float = 2.0
    energy_intensity_std: float = 0.25
    insurance_deductible: float = 5_000
    insurance_limit: float = 30_000
    price_trigger: float = 150
    p2p_initial_capital: float = 300_000
    p2p_coverage_ratio: float = 0.60
    safety_stock_capacity_factor: float = 0.65
    traditional_bi_capacity_factor: float = 0.65
    parametric_base_capacity_factor: float = 0.65
