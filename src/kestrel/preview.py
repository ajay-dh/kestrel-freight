"""Print a Markdown rate preview for the GitHub Actions job summary.

Usage in CI:  python -m kestrel.preview >> "$GITHUB_STEP_SUMMARY"
"""

import sys
from pathlib import Path

from kestrel.lanes import LANES, WEIGHTS_KG
from kestrel.quote import quote


def money(x: float) -> str:
    return f"-${abs(x):,.2f}" if x < 0 else f"${x:,.2f}"


def render() -> str:
    header = "| Lane | " + " | ".join(f"{w:,} kg" for w in WEIGHTS_KG) + " |"
    divider = "|---|" + "---:|" * len(WEIGHTS_KG)
    rows = []
    problems = 0
    for lane, km in LANES:
        cells = []
        for w in WEIGHTS_KG:
            price = quote(w, km)
            if price <= 0:
                problems += 1
                cells.append(f"❌ **{money(price)}**")
            else:
                cells.append(money(price))
        rows.append(f"| {lane} ({km:,} km) | " + " | ".join(cells) + " |")

    status = (
        f"> ❌ **{problems} quotes are zero or negative.** Do not ship this."
        if problems
        else "> ✅ All sample quotes are positive."
    )
    return "\n".join(["## 📦 Rate card preview (standard service)", "", status, "", header, divider, *rows, ""])


def annotations() -> list[str]:
    """GitHub annotations for bad prices, pinned to the line that applies the discount."""
    src = Path(__file__).with_name("quote.py").read_text(encoding="utf-8").splitlines()
    line = next((i for i, t in enumerate(src, 1) if "cost" in t and "DISCOUNT" in t), 1)
    out = []
    for lane, km in LANES:
        for w in WEIGHTS_KG:
            price = quote(w, km)
            if price <= 0:
                out.append(
                    f"::error file=src/kestrel/quote.py,line={line},title=Negative price on the rate card::"
                    f"{lane}, {w:,} kg would be quoted {money(price)}"
                )
    return out


if __name__ == "__main__":
    if "--annotate" in sys.argv:
        print("\n".join(annotations()))
    else:
        print(render())
