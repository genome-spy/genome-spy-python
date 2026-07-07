"""Render real static thumbnails of gallery examples with a headless browser.

GenomeSpy renders to a WebGL/canvas surface, so there is no pure-Python way to
rasterize a chart; a headless browser is the correct tool (the same approach
Altair uses via vl-convert for its own renderer). This script mounts each
example's live chart with the pinned GenomeSpy bundle and screenshots it to
``docs/assets/generated/thumbs/<name>.png``.

Network is required (the browser imports the ``@genome-spy/core`` CDN bundle),
so this runs in CI rather than as part of every local build. When no PNG exists,
``docs_gallery.py`` falls back to a generated SVG poster, so the site still
builds offline.

Usage (CI):
    uv run --with playwright playwright install --with-deps chromium
    uv run --with playwright python tools/render_thumbnails.py
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent


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
<style>html,body{{margin:0;background:#fff}}#c{{display:inline-block}}</style>
</head><body><div id="c"></div>
<script type="module">
import {{ embed }} from "{bundle}";
const spec = {spec};
try {{
  await embed(document.getElementById("c"), spec);
  window.__gsReady = true;
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
            viewport={"width": 900, "height": 520}, device_scale_factor=2
        )
        for example in examples:
            html = _PAGE_TEMPLATE.format(
                bundle=bundle_url, spec=json.dumps(example.spec)
            )
            page.set_content(html, wait_until="load")
            try:
                page.wait_for_function("window.__gsReady === true", timeout=30_000)
            except Exception:  # noqa: BLE001 - report and skip a single example
                err = page.evaluate("window.__gsError || 'timed out'")
                print(f"[thumb] {example.name}: render failed ({err})", file=sys.stderr)
                continue
            page.wait_for_timeout(600)  # let the first frame settle
            out = gallery.THUMBS_DIR / f"{example.name}.png"
            page.locator("#c").screenshot(path=str(out))
            print(f"[thumb] {example.name} -> {out.name}")
            rendered += 1
        browser.close()

    print(f"Rendered {rendered}/{len(examples)} thumbnail(s).")
    return 0 if rendered else 1


if __name__ == "__main__":
    raise SystemExit(main())
