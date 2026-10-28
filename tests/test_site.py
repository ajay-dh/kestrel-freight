from kestrel.preview import render
from kestrel.site import build_html
from kestrel.smoke import check


def test_site_builds_and_passes_smoke(tmp_path):
    (tmp_path / "index.html").write_text(build_html(), encoding="utf-8")
    assert check(str(tmp_path)) == []


def test_preview_is_markdown_table():
    md = render()
    assert "| Lane |" in md
    assert "✅" in md
