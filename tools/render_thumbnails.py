"""Render static gallery thumbnails with a headless browser.

GenomeSpy renders to a WebGL/canvas surface, so there is no pure-Python way to
rasterize a chart; a headless browser is the correct tool. For each gallery
example this mounts the live chart with the pinned GenomeSpy bundle and
screenshots it to a PNG thumbnail. Examples use different natural heights, so
the renderer scales each chart to fit inside a fixed gallery card instead of
cropping taller compositions.

Network is required (the browser imports the ``@genome-spy/core`` CDN bundle).
The generated PNGs are visual review artifacts and should be checked in after
they have been inspected.

Usage:
    uv run --with playwright playwright install --with-deps chromium
    uv run --with playwright python tools/render_thumbnails.py
    uv run --with playwright python tools/render_thumbnails.py manhattan_plot
    uv run --with playwright python tools/render_thumbnails.py --overwrite
"""

from __future__ import annotations

import argparse
import base64
import copy
import importlib.util
import json
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent

# Capture-box size; the sizeless charts fill it, giving a consistent card image.
CARD_WIDTH = 720
CARD_HEIGHT = 405
CARD_PADDING = 12
DEVICE_SCALE_FACTOR = 2
INK_THRESHOLD = 248
STAGE_WIDTH_BUFFER = 240
READY_TIMEOUT_MS = 45_000
SETTLE_DELAY_MS = 6_000
# `embed()` resolves before lazy sources finish loading and drawing, so the
# settle delay alone can capture a half-drawn chart. Keep polling until two
# consecutive frames are identical.
STABLE_POLL_MS = 2_000
STABLE_ATTEMPTS = 6


def wait_until_stable(
    capture: Callable[[], bytes],
    wait: Callable[[], None],
    *,
    attempts: int = STABLE_ATTEMPTS,
) -> bytes:
    """Capture until two consecutive frames match, or until attempts run out.

    Args:
        capture: Takes one screenshot and returns its bytes.
        wait: Pauses between captures.
        attempts: Maximum number of captures.

    Returns:
        The first repeated frame, or the last one taken.

    Raises:
        ValueError: If ``attempts`` is less than one.

    Example:
        >>> wait_until_stable(next_frame, pause)
    """
    if attempts < 1:
        raise ValueError("attempts must be at least one.")

    previous: bytes | None = None
    for _ in range(attempts):
        current = capture()
        if current == previous:
            return current
        previous = current
        wait()
    return previous if previous is not None else capture()


@dataclass(frozen=True, slots=True)
class ThumbnailLayout:
    """Geometry for one rendered thumbnail card."""

    stage_width: int
    min_stage_height: int


@dataclass(frozen=True, slots=True)
class PaintBounds:
    """Bounding box of non-background pixels in a rendered screenshot."""

    left: int
    top: int
    right: int
    bottom: int


def center_translation(
    bounds: PaintBounds,
    *,
    device_scale_factor: float = DEVICE_SCALE_FACTOR,
) -> tuple[float, float]:
    """Return a padding-safe translation that centers rendered chart ink."""
    left = bounds.left / device_scale_factor
    top = bounds.top / device_scale_factor
    right = bounds.right / device_scale_factor
    bottom = bounds.bottom / device_scale_factor

    desired_x = CARD_WIDTH / 2 - (left + right) / 2
    desired_y = CARD_HEIGHT / 2 - (top + bottom) / 2
    min_x = CARD_PADDING - left
    max_x = CARD_WIDTH - CARD_PADDING - right
    min_y = CARD_PADDING - top
    max_y = CARD_HEIGHT - CARD_PADDING - bottom
    dx = min(max(desired_x, min_x), max_x)
    dy = min(max(desired_y, min_y), max_y)
    return dx, dy


def thumbnail_layout(example: object) -> ThumbnailLayout:
    """Return the natural render size for an example before card scaling."""
    max_width = getattr(example, "max_width", None)
    height = getattr(example, "height", CARD_HEIGHT)
    stage_width = CARD_WIDTH
    if max_width is not None:
        stage_width = int(max_width)
        if stage_width <= 1200:
            stage_width += STAGE_WIDTH_BUFFER
    return ThumbnailLayout(
        stage_width=stage_width,
        min_stage_height=int(height),
    )


def thumbnail_spec(spec: dict[str, object]) -> dict[str, object]:
    """Return a copy with transient zoom guidance removed from thumbnails."""
    result = copy.deepcopy(spec)

    drop = object()

    def clean(value: object, *, root: bool = False) -> object:
        if isinstance(value, dict):
            if value.get("name") == "zoom-message":
                return drop
            layers = value.get("layer")
            if (
                not root
                and isinstance(layers, list)
                and any(
                    isinstance(layer, dict) and layer.get("name") == "zoom-message"
                    for layer in layers
                )
            ):
                return drop
            for key, child in list(value.items()):
                cleaned = clean(child)
                if cleaned is drop:
                    value.pop(key)
                else:
                    value[key] = cleaned
            return value
        if isinstance(value, list):
            cleaned_items = []
            for child in value:
                cleaned = clean(child)
                if cleaned is not drop:
                    cleaned_items.append(cleaned)
            return cleaned_items
        return value

    cleaned = clean(result, root=True)
    assert isinstance(cleaned, dict)
    return cleaned


def _load_gallery():
    spec = importlib.util.spec_from_file_location(
        "_gs_docs_gallery", _TOOLS / "docs_gallery.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture missing GenomeSpy documentation gallery thumbnails."
    )
    parser.add_argument(
        "examples",
        nargs="*",
        metavar="EXAMPLE",
        help="Example names to capture; defaults to every documentation example.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Recapture thumbnails that already exist.",
    )
    parser.add_argument(
        "--settle-ms",
        type=int,
        default=SETTLE_DELAY_MS,
        help=(
            "Milliseconds to wait after a chart mounts before capturing. "
            "Raise it for examples that keep loading data. "
            f"Defaults to {SETTLE_DELAY_MS}."
        ),
    )
    return parser.parse_args(argv)


def _select_examples(gallery: object, names: list[str]) -> list[object]:
    examples = gallery.collect_examples()
    if not names:
        return examples

    by_name = {example.name: example for example in examples}
    missing = [name for name in names if name not in by_name]
    if missing:
        available = ", ".join(sorted(by_name))
        raise ValueError(
            f"Unknown example name(s): {', '.join(missing)}. Available examples: {available}"
        )
    return [by_name[name] for name in names]


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
const container = document.getElementById("c");

try {{
  await embed(container, spec, {{ bare: true }});
  window.__gsMounted = true;
}} catch (e) {{
  window.__gsError = String(e);
}}
</script></body></html>"""


_FIND_PAINT_BOUNDS = """
async ({ url, threshold }) => {
  const image = new Image();
  image.src = url;
  await image.decode();
  const canvas = document.createElement("canvas");
  canvas.width = image.width;
  canvas.height = image.height;
  const context = canvas.getContext("2d", { willReadFrequently: true });
  context.drawImage(image, 0, 0);
  const pixels = context.getImageData(0, 0, image.width, image.height).data;
  let left = image.width;
  let top = image.height;
  let right = -1;
  let bottom = -1;
  for (let y = 0; y < image.height; y++) {
    for (let x = 0; x < image.width; x++) {
      const offset = (y * image.width + x) * 4;
      if (
        pixels[offset + 3] > 0 &&
        (pixels[offset] < threshold ||
          pixels[offset + 1] < threshold ||
          pixels[offset + 2] < threshold)
      ) {
        left = Math.min(left, x);
        top = Math.min(top, y);
        right = Math.max(right, x + 1);
        bottom = Math.max(bottom, y + 1);
      }
    }
  }
  return right < 0 ? null : { left, top, right, bottom };
}
"""


def main() -> int:
    args = _parse_args()
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
    try:
        examples = _select_examples(gallery, args.examples)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2
    gallery.THUMBS_DIR.mkdir(parents=True, exist_ok=True)

    explicit_selection = bool(args.examples)
    pending = [
        example
        for example in examples
        if args.overwrite
        or explicit_selection
        or not (gallery.THUMBS_DIR / f"{example.name}.png").exists()
    ]
    if not pending:
        print(
            "No thumbnails captured because all selected outputs already exist. "
            "Use --overwrite to refresh them."
        )
        return 0

    rendered = 0
    settle_delay_ms = args.settle_ms
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(
            viewport={"width": CARD_WIDTH, "height": CARD_HEIGHT},
            device_scale_factor=DEVICE_SCALE_FACTOR,
        )
        for example in pending:
            layout = thumbnail_layout(example)
            html = _PAGE_TEMPLATE.format(
                card_width=CARD_WIDTH,
                card_height=CARD_HEIGHT,
                card_padding=CARD_PADDING,
                stage_width=layout.stage_width,
                min_stage_height=layout.min_stage_height,
                bundle=bundle_url,
                spec=json.dumps(thumbnail_spec(example.spec)),
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
            page.wait_for_timeout(settle_delay_ms)
            wait_until_stable(
                page.screenshot,
                lambda: page.wait_for_timeout(STABLE_POLL_MS),
            )
            runtime_error = page.locator("#c").inner_text().strip()
            if runtime_error.startswith("Error:"):
                print(
                    f"[thumb] {example.name}: render failed ({runtime_error})",
                    file=sys.stderr,
                )
                continue
            page.evaluate(
                """
                () => {
                  const frame = document.getElementById("frame");
                  const fit = document.getElementById("fit");
                  const container = document.getElementById("c");
                  fit.style.transform = "none";
                  const canvas = container.querySelector("canvas");
                  const canvasRect = canvas.getBoundingClientRect();
                  container.style.width = `${Math.ceil(canvasRect.width)}px`;
                  container.style.minHeight = "0px";
                  fit.style.width = `${Math.ceil(canvasRect.width)}px`;
                  const rect = container.getBoundingClientRect();
                  fit.style.height = `${Math.ceil(rect.height)}px`;
                  const scale = Math.min(
                    (frame.clientWidth - 24) / rect.width,
                    (frame.clientHeight - 24) / rect.height,
                    1
                  );
                  fit.dataset.scale = String(scale);
                  fit.style.transform = `scale(${scale})`;
                }
                """
            )
            preview = page.screenshot()
            bounds_data = None
            for _ in range(4):
                bounds_data = page.evaluate(
                    _FIND_PAINT_BOUNDS,
                    {
                        "url": (
                            "data:image/png;base64,"
                            + base64.b64encode(preview).decode("ascii")
                        ),
                        "threshold": INK_THRESHOLD,
                    },
                )
                if bounds_data is None:
                    break
                edge = DEVICE_SCALE_FACTOR * CARD_PADDING
                if (
                    bounds_data["left"] > edge
                    and bounds_data["top"] > edge
                    and bounds_data["right"] < CARD_WIDTH * DEVICE_SCALE_FACTOR - edge
                    and bounds_data["bottom"] < CARD_HEIGHT * DEVICE_SCALE_FACTOR - edge
                ):
                    break
                scale = float(page.locator("#fit").get_attribute("data-scale") or 1)
                scale *= 0.75
                page.evaluate(
                    "(scale) => { const fit = document.getElementById('fit'); "
                    "fit.dataset.scale = String(scale); "
                    "fit.style.transform = `scale(${scale})`; }",
                    scale,
                )
                preview = page.screenshot()
            if bounds_data is not None:
                dx, dy = center_translation(PaintBounds(**bounds_data))
                page.evaluate(
                    """
                    ([dx, dy]) => {
                      const fit = document.getElementById("fit");
                      fit.style.transform =
                        `translate(${dx}px, ${dy}px) scale(${fit.dataset.scale})`;
                    }
                    """,
                    [dx, dy],
                )
            page.screenshot(path=str(gallery.THUMBS_DIR / f"{example.name}.png"))
            print(f"[thumb] {example.name}")
            rendered += 1
        browser.close()

    print(f"Rendered {rendered}/{len(pending)} thumbnail(s).")
    return 0 if rendered == len(pending) else 1


if __name__ == "__main__":
    raise SystemExit(main())
