"""Guardrail tests for the quote engine.

These run on every pull request. Branch protection blocks the merge if any fail.
"""

import pytest

from kestrel.quote import QuoteError, quote

WEIGHTS = [1, 50, 999, 1000, 5000, 20000]
DISTANCES = [1, 70, 600, 3400]


def test_known_price():
    # 25 + 100 kg * 500 km * 0.0004 = 45.00, plus 8% fuel = 48.60
    assert quote(100, 500) == 48.60


def test_express_costs_more():
    assert quote(100, 500, express=True) > quote(100, 500)


@pytest.mark.parametrize("weight", WEIGHTS)
@pytest.mark.parametrize("distance", DISTANCES)
@pytest.mark.parametrize("express", [False, True])
def test_price_is_always_positive(weight, distance, express):
    """Revenue guardrail: we never quote zero or a negative price."""
    assert quote(weight, distance, express) > 0


@pytest.mark.parametrize("weight", WEIGHTS)
def test_longer_trips_cost_more(weight):
    assert quote(weight, 1000) > quote(weight, 100)


@pytest.mark.parametrize("weight, distance", [(0, 100), (-5, 100), (10, 0), (10, -1)])
def test_rejects_invalid_input(weight, distance):
    with pytest.raises(QuoteError):
        quote(weight, distance)
