"""Build the public rate card page (static HTML) into an output folder.

Usage:  python -m kestrel.site --out _site
"""

import argparse
import html
import os
from datetime import UTC, datetime
from pathlib import Path

from kestrel import __version__
from kestrel import quote as quote_module
from kestrel.lanes import LANES, WEIGHTS_KG
from kestrel.preview import money
from kestrel.quote import quote


def build_html() -> str:
    sha = os.environ.get("GITHUB_SHA", "local")[:7]
    run = os.environ.get("GITHUB_RUN_NUMBER", "-")
    built = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    discount = getattr(quote_module, "VOLUME_DISCOUNT_RATE", None)
    threshold = getattr(quote_module, "VOLUME_DISCOUNT_THRESHOLD_KG", None)
    banner = (
        f'<p class="banner">New: {discount:.0%} volume discount on shipments of {threshold:,} kg or more</p>'
        if discount and threshold
        else ""
    )

    head = "".join(f"<th>{w:,} kg</th>" for w in WEIGHTS_KG)
    body = ""
    for lane, km in LANES:
        cells = "".join(f"<td>{money(quote(w, km))}</td>" for w in WEIGHTS_KG)
        body += f"<tr><th>{html.escape(lane)} <span>{km:,} km</span></th>{cells}</tr>"

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kestrel Freight Rates</title>
<style>
:root {{ --ink:#14213d; --muted:#5c677d; --line:#e3e7ee; --accent:#0a7d55; --bg:#f7f8fa; }}
body {{ margin:0; font-family: system-ui, -apple-system, sans-serif; color:var(--ink); background:var(--bg); }}
main {{ max-width: 860px; margin: 48px auto; padding: 0 16px; }}
h1 {{ margin:0 0 4px; font-size: 28px; }}
.sub {{ color:var(--muted); margin:0 0 24px; }}
.banner {{ background:var(--accent); color:#fff; padding:10px 14px; border-radius:8px; font-weight:600; }}
table {{ width:100%; border-collapse:collapse; background:#fff; border:1px solid var(--line); border-radius:8px; }}
th, td {{ padding:12px; border-bottom:1px solid var(--line); text-align:right; font-variant-numeric: tabular-nums; }}
tbody th, thead th:first-child {{ text-align:left; }}
tbody th span {{ display:block; color:var(--muted); font-weight:400; font-size:13px; }}
footer {{ margin-top:20px; color:var(--muted); font-size:13px; }}
code {{ background:#fff; border:1px solid var(--line); padding:2px 6px; border-radius:4px; }}
</style></head>
<body><main>
<h1>Kestrel Freight · Standard rates</h1>
<p class="sub">Door-to-door pricing, fuel surcharge included.</p>
{banner}
<table><thead><tr><th>Lane</th>{head}</tr></thead><tbody>{body}</tbody></table>
<footer>v{__version__} · commit <code>{sha}</code> · pipeline run #{run} · built {built}</footer>
</main></body></html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="_site")
    out = Path(parser.parse_args().out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(build_html(), encoding="utf-8")
    print(f"Wrote {out / 'index.html'}")


if __name__ == "__main__":
    main()
