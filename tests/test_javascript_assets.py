from __future__ import annotations

import base64
from pathlib import Path
import re

import genome_spy as gs

from genome_spy._embed import bundled_module_url
from genome_spy.schema import SCHEMA_VERSION


def test_bundled_browser_modules_match_the_schema_version() -> None:
    sources = {
        name: base64.b64decode(bundled_module_url(name).split(",", 1)[1]).decode()
        for name in ("embed", "core", "inspector")
    }

    assert set(sources) == {"embed", "core", "inspector"}
    assert all(
        source.startswith(f"// Vendored from GenomeSpy {SCHEMA_VERSION}.")
        for source in sources.values()
    )


def test_inline_html_retains_the_complete_font_license() -> None:
    root = Path(__file__).resolve().parents[1]
    license_text = (root / "LICENSES/LATO-OFL-1.1.txt").read_text().strip()
    assert "Copyright (c) 2010-2014 by tyPoland Lukasz Dziedzic" in license_text
    assert "SIL OPEN FONT LICENSE Version 1.1" in license_text
    html = gs.Chart([{"x": 1}]).mark_point().to_html(inline=True)
    modules = re.findall(r"data:text/javascript;base64,([A-Za-z0-9+/=]+)", html)
    assert any(license_text in base64.b64decode(module).decode() for module in modules)
