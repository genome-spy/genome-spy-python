"""Render static gallery thumbnails with a headless browser.

GenomeSpy renders to a WebGL/canvas surface, so there is no pure-Python way to
rasterize a chart; a headless browser is the correct tool. For each gallery
example this mounts the live chart with the pinned GenomeSpy bundle and
screenshots it to a PNG thumbnail. Examples use different natural heights, so
the renderer scales each chart to fit inside a fixed gallery card instead of
cropping taller compositions.

Network is required (the browser imports the ``@genome-spy/core`` CDN bundle), so
this runs in CI rather than as part of every local build. When no PNG exists,
``docs_gallery.py`` falls back to a generated SVG poster.

Usage:
    uv run --with playwright playwright install --with-deps chromium
    uv run --with playwright python tools/render_thumbnails.py
"""

from __future__ import annotations

import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent

# Capture-box size; the sizeless charts fill it, giving a consistent card image.
CARD_WIDTH = 720
CARD_HEIGHT = 405
CARD_PADDING = 12
READY_TIMEOUT_MS = 45_000
SETTLE_DELAY_MS = 6_000


@dataclass(frozen=True, slots=True)
class ThumbnailLayout:
    """Geometry for one rendered thumbnail card."""

    stage_width: int
    min_stage_height: int


def thumbnail_layout(example: object) -> ThumbnailLayout:
    """Return the natural render size for an example before card scaling."""
    max_width = getattr(example, "max_width", None)
    height = getattr(example, "height", CARD_HEIGHT)
    return ThumbnailLayout(
        stage_width=int(max_width) if max_width is not None else CARD_WIDTH,
        min_stage_height=int(height),
    )


def _load_gallery():
    spec = importlib.util.spec_from_file_location(
        "_gs_docs_gallery", _TOOLS / "docs_gallery.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_PAGE_TEMPLATE = """<!doctype html>
<html><head><meta charset="utf-8">
<style>
html,body{{margin:0;height:100%;background:#fff}}
body{{font-family:Lato,system-ui,sans-serif}}
#frame{{display:flex;align-items:center;justify-content:center;box-sizing:border-box;width:{card_width}px;height:{card_height}px;padding:{card_padding}px;overflow:hidden;background:#fff}}
#fit{{flex:0 0 auto;width:{stage_width}px;transform-origin:center center}}
#c{{width:{stage_width}px;min-height:{min_stage_height}px}}
</style>
</head><body><div id="frame"><div id="fit"><div id="c"></div></div></div>
<script type="module">
import {{ embed }} from "{bundle}";
const spec = {spec};
const frame = document.getElementById("frame");
const fit = document.getElementById("fit");
const container = document.getElementById("c");
const cardPadding = {card_padding};

function applyScale() {{
  const scale = Math.min(
    (frame.clientWidth - cardPadding * 2) / fit.offsetWidth,
    (frame.clientHeight - cardPadding * 2) / fit.offsetHeight,
    1
  );
  fit.style.transform = `scale(${{scale}})`;
}}

try {{
  await embed(container, spec, {{ bare: true }});
  applyScale();
  window.__gsMounted = true;
}} catch (e) {{
  window.__gsError = String(e);
}}
</script></body></html>"""


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "playwright is not installed. Run with:\n"
            "  uv run --with playwright playwright install --with-deps chromium\n"
            "  uv run --with playwright python tools/render_thumbnails.py",
            file=sys.stderr,
        )
        return 1

    gallery = _load_gallery()
    bundle_url = gallery.default_bundle_url()
    examples = gallery.collect_examples()
    gallery.THUMBS_DIR.mkdir(parents=True, exist_ok=True)

    rendered = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(
            viewport={"width": CARD_WIDTH, "height": CARD_HEIGHT},
            device_scale_factor=2,
        )
        for example in examples:
            layout = thumbnail_layout(example)
            html = _PAGE_TEMPLATE.format(
                card_width=CARD_WIDTH,
                card_height=CARD_HEIGHT,
                card_padding=CARD_PADDING,
                stage_width=layout.stage_width,
                min_stage_height=layout.min_stage_height,
                bundle=bundle_url,
                spec=json.dumps(example.spec),
            )
            page.set_content(html, wait_until="load")
            try:
                page.wait_for_function(
                    "window.__gsMounted === true || window.__gsError",
                    timeout=READY_TIMEOUT_MS + 5_000,
                )
            except Exception:  # noqa: BLE001 - report and skip a single example
                err = page.evaluate("window.__gsError || 'timed out'")
                print(f"[thumb] {example.name}: render failed ({err})", file=sys.stderr)
                continue
            error = page.evaluate("window.__gsError || null")
            if error is not None:
                print(
                    f"[thumb] {example.name}: render failed ({error})", file=sys.stderr
                )
                continue
            page.locator("#c canvas").first.wait_for(timeout=READY_TIMEOUT_MS)
            try:
                page.wait_for_load_state("networkidle", timeout=READY_TIMEOUT_MS)
            except Exception:
                pass
            page.wait_for_timeout(SETTLE_DELAY_MS)
            page.evaluate(
                f"""
                () => {{
                  const frame = document.getElementById("frame");
                  const fit = document.getElementById("fit");
                  const container = document.getElementById("c");
                  const rect = container.getBoundingClientRect();
                  fit.style.height = `${{Math.ceil(rect.height)}}px`;
                  const scale = Math.min(
                    (frame.clientWidth - {CARD_PADDING * 2}) / rect.width,
                    (frame.clientHeight - {CARD_PADDING * 2}) / rect.height,
                    1
                  );
                  fit.style.transform = `scale(${{scale}})`;
                }}
                """
            )
            page.screenshot(path=str(gallery.THUMBS_DIR / f"{example.name}.png"))
            print(f"[thumb] {example.name}")
            rendered += 1
        browser.close()

    print(f"Rendered {rendered}/{len(examples)} thumbnail(s).")
    return 0 if rendered else 1


if __name__ == "__main__":
    raise SystemExit(main())
