import pytest

from scroam.agents import ManufacturerAgent
from scroam.insurance import ParametricNDBIContract
from scroam.p2p_pool import P2PLiquidityPool


def make_parametric_agent(
    insurance_contract: ParametricNDBIContract,
) -> ManufacturerAgent:
    return ManufacturerAgent(
        agent_id=0,
        inventory=0,
        baseline_capacity=100,
        daily_demand=100,
        normal_price=80,
        energy_intensity=1,
        scenario="parametric_ndbi",
        insurance_contract=insurance_contract,
        p2p_pool=P2PLiquidityPool(
            initial_capital=0,
            coverage_ratio=0.60,
        ),
        safety_stock_capacity_factor=0.65,
        traditional_bi_capacity_factor=0.65,
        parametric_base_capacity_factor=0.65,
    )


def test_parametric_capacity_keeps_minimum_without_funding() -> None:
    agent = make_parametric_agent(
        ParametricNDBIContract(
            deductible=0,
            policy_limit=100_000,
            wind_trigger=0.10,
            price_trigger=150,
        )
    )

    agent.step({"wind_index": 0.50, "spot_price": 200})

    assert agent.total_aicow > 0
    assert agent.total_insurance_payout == 0
    assert agent.total_production == pytest.approx(65)


def test_parametric_capacity_reaches_baseline_with_full_funding() -> None:
    agent = make_parametric_agent(
        ParametricNDBIContract(
            deductible=0,
            policy_limit=100_000,
            wind_trigger=0.10,
            price_trigger=150,
        )
    )

    agent.step({"wind_index": 0.05, "spot_price": 200})

    assert agent.total_aicow > 0
    assert agent.total_insurance_payout == pytest.approx(
        agent.total_aicow
    )
    assert agent.total_production == pytest.approx(
        agent.baseline_capacity
    )


def test_parametric_capacity_recovers_gradually_with_partial_funding() -> None:
    agent = make_parametric_agent(
        ParametricNDBIContract(
            deductible=6_000,
            policy_limit=100_000,
            wind_trigger=0.10,
            price_trigger=150,
        )
    )

    agent.step({"wind_index": 0.05, "spot_price": 200})

    assert agent.total_aicow == pytest.approx(12_000)
    assert agent.total_insurance_payout == pytest.approx(6_000)
    assert agent.total_production == pytest.approx(82.5)
