"""Kestrel Freight quote engine.

Prices a single shipment from weight, distance and service level.
Every customer-facing price on kestrelfreight.example comes from quote().
"""

BASE_FEE = 25.00  # USD per shipment
RATE_PER_KG_KM = 0.0004  # USD per kg per km
EXPRESS_MULTIPLIER = 1.5
FUEL_SURCHARGE = 0.08  # 8% on top of everything


class QuoteError(ValueError):
    """Raised when a quote request is invalid."""


def quote(weight_kg: float, distance_km: float, express: bool = False) -> float:
    """Return the shipment price in USD, rounded to cents."""
    if weight_kg <= 0:
        raise QuoteError("weight_kg must be positive")
    if distance_km <= 0:
        raise QuoteError("distance_km must be positive")

    cost = BASE_FEE + weight_kg * distance_km * RATE_PER_KG_KM

    if express:
        cost *= EXPRESS_MULTIPLIER

    cost *= 1 + FUEL_SURCHARGE
    return round(cost, 2)
