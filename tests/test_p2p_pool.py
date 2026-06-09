from scroam.p2p_pool import P2PLiquidityPool


def test_p2p_pool_never_pays_more_than_available_capital() -> None:
    pool = P2PLiquidityPool(initial_capital=1_000, coverage_ratio=0.60)

    payout = pool.cover(10_000)

    assert payout == 1_000
    assert pool.remaining_capital == 0
    assert pool.total_paid == 1_000
    assert pool.depleted is True
