from __future__ import annotations

from pathlib import Path


def test_gos_defaults_to_text_html_renderer() -> None:
    gos_display = Path("tmp/gos/gosling/display.py").read_text(encoding="utf-8")

    assert 'return {"text/html": html}' in gos_display
    assert 'renderers.register("default", HTMLRenderer())' in gos_display


def test_altair_exposes_separate_html_and_jupyter_renderers() -> None:
    altair_display = Path("tmp/altair/altair/vegalite/v6/display.py").read_text(
        encoding="utf-8"
    )

    assert 'renderers.register("default", html_renderer)' in altair_display
    assert 'renderers.register("jupyter", jupyter_renderer)' in altair_display
    assert "application/vnd.jupyter.widget-view+json" in Path(
        "tmp/altair/tests/vegalite/v6/test_renderers.py"
    ).read_text(encoding="utf-8")


def test_our_default_chart_display_remains_html_first() -> None:
    chart_source = Path("src/genome_spy/chart.py").read_text(encoding="utf-8")

    assert 'return {"text/html": self.to_html()}' in chart_source
    assert "def widget(" in chart_source
