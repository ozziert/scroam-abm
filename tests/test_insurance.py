from scroam.insurance import ParametricNDBIContract


def test_insurance_pays_only_when_trigger_is_met() -> None:
    contract = ParametricNDBIContract(
        deductible=5_000,
        policy_limit=30_000,
        wind_trigger=0.10,
        price_trigger=150,
    )

    payout, triggered = contract.evaluate(
        wind_index=0.05,
        spot_price=200,
        estimated_aicow=20_000,
    )
    assert triggered is True
    assert payout == 15_000

    payout, triggered = contract.evaluate(
        wind_index=0.20,
        spot_price=200,
        estimated_aicow=20_000,
    )
    assert triggered is False
    assert payout == 0
