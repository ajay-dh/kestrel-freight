"""Staging smoke test: check the built site before it can reach production.

Usage:  python -m kestrel.smoke _site
"""

import re
import sys
from pathlib import Path


def check(site_dir: str) -> list[str]:
    page = Path(site_dir) / "index.html"
    if not page.exists():
        return [f"{page} is missing"]
    text = page.read_text(encoding="utf-8")
    errors = []
    if "Kestrel Freight" not in text:
        errors.append("brand title missing")
    if re.search(r"-\$\d", text):
        errors.append("negative price on rate card")
    if "<td>" not in text:
        errors.append("rate table is empty")
    return errors


if __name__ == "__main__":
    problems = check(sys.argv[1] if len(sys.argv) > 1 else "_site")
    for p in problems:
        print(f"::error::Smoke test failed: {p}")
    if problems:
        sys.exit(1)
    print("✅ Staging smoke test passed")
