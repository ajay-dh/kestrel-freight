"""Turns failing price guardrails into one plain-English annotation on the GitHub run page.

Only active inside GitHub Actions. Locally, pytest output is unchanged.
"""

import os

import pytest

from kestrel.preview import money
from kestrel.quote import quote

ON_GITHUB = os.environ.get("GITHUB_ACTIONS") == "true"
_bad_quotes: list[tuple[float, float, bool, float]] = []


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if not ON_GITHUB or report.when != "call" or not report.failed:
        return
    if item.originalname == "test_price_is_always_positive":
        args = item.funcargs
        w, d, x = args["weight"], args["distance"], args["express"]
        _bad_quotes.append((w, d, x, quote(w, d, x)))


def pytest_sessionfinish(session):
    if not ON_GITHUB:
        return
    if _bad_quotes:
        w, d, x, price = min(_bad_quotes, key=lambda q: q[3])
        service = "express" if x else "standard"
        print(
            "\n::error file=tests/test_quote.py,title=Revenue guardrail: negative prices::"
            f"{len(_bad_quotes)} quotes came out at $0 or below. "
            f"Worst: {w:,} kg, {d:,} km, {service} = {money(price)}. Prices must always be positive."
        )
