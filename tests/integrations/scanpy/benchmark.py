"""Measure a seeded sparse UMAP workload in a fresh process.

Run each size/panel count separately, for example:
``uv run --no-sync python -m tests.integrations.scanpy.benchmark --cells 100000 --panels 8``.
This is an explicit local benchmark, not a hardware-independent CI time limit.
The source matrix has 20,000 genes but only selected columns may be densified.
"""

from __future__ import annotations

import argparse
from importlib.metadata import version
import json
from pathlib import Path
import platform
import resource
import statistics
import sys
from time import perf_counter


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells", type=int, default=100_000)
    parser.add_argument("--panels", type=int, choices=[1, 8], default=1)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--browser", action="store_true")
    args = parser.parse_args()
    import anndata as ad
    import matplotlib as mpl
    import numpy as np
    import pandas as pd
    import scanpy as sc
    from scipy import sparse

    import genome_spy.scanpy as gsc

    sc.settings.autoshow = False

    rng = np.random.default_rng(0)
    n = args.cells
    genes = 20_000
    # Exactly 20 sparse entries per observation, including four requested genes.
    positions = np.concatenate(
        [np.tile(np.arange(4), (n, 1)), rng.integers(4, genes, size=(n, 16))], axis=1
    )
    x = sparse.coo_matrix(
        (
            rng.random(n * 20, dtype=np.float32),
            (np.repeat(np.arange(n), 20), positions.ravel()),
        ),
        shape=(n, genes),
    ).tocsr()
    a = ad.AnnData(x, obs=pd.DataFrame(index=[f"cell-{i}" for i in range(n)]))
    a.var_names = [f"g{i}" for i in range(genes)]
    a.obs["group"] = pd.Categorical(rng.integers(0, 12, n).astype(str))
    a.obs["score"] = rng.standard_normal(n).astype(np.float32)
    a.obsm["X_umap"] = rng.standard_normal((n, 2)).astype(np.float32)
    if args.browser:
        # Exposed points let the interaction oracle name exact source IDs.
        a.obsm["X_umap"][:16] = [[6 + i % 4 * 0.4, 6 + i // 4 * 0.4] for i in range(16)]
    # Fail on a dense allocation larger than a single requested gene column.
    original = sparse.csr_matrix.toarray
    shapes = []

    def selected_only(matrix, *positional, **kwargs):
        shapes.append(list(matrix.shape))
        assert matrix.shape == (n, 1), matrix.shape
        return original(matrix, *positional, **kwargs)

    sparse.csr_matrix.toarray = selected_only
    start = perf_counter()
    keys = ["group", "score", "g0", "g1", "g2", "g3", "group", "score"]
    with mpl.rc_context({"figure.figsize": (3, 3), "figure.dpi": 100}):
        chart = gsc.pl.umap(
            a,
            color=keys if args.panels == 8 else "g0",
            zoom=args.browser,
            size=36 if args.browser else None,
            show=False,
        )
    prepared_at = perf_counter()
    transport = chart._prepare_render()
    serialized_at = perf_counter()
    spec = chart.to_dict()
    encoded = json.dumps(spec, separators=(",", ":")).encode()
    json_at = perf_counter()
    report = {
        "hardware": {
            "system": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "python": platform.python_version(),
        "versions": {
            p: version(p)
            for p in [
                "scanpy",
                "anndata",
                "numpy",
                "pandas",
                "scipy",
                "matplotlib",
                "pyarrow",
            ]
        },
        "fixture": {
            "seed": 0,
            "cells": n,
            "genes": genes,
            "nnz": x.nnz,
            "panels": args.panels,
            "sparse_bytes": x.data.nbytes + x.indices.nbytes + x.indptr.nbytes,
            "equivalent_dense_float32_bytes": n * genes * 4,
        },
        "seconds": {
            "prepare_chart": prepared_at - start,
            "arrow_transport": serialized_at - prepared_at,
            "json_with_validation": json_at - serialized_at,
        },
        "bytes": {
            "arrow": sum(len(b) for b in transport.buffers.values()),
            "json": len(encoded),
            "peak_process_rss": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            * (1 if sys.platform == "darwin" else 1024),
        },
        "densified_shapes": shapes,
        "render_settings": {
            "figure_inches": [3, 3],
            "display_dpi": 100,
            "native_font": "Lato",
            "reference_font": "DejaVu Sans",
        },
    }
    if args.browser:
        report["browser"] = _measure_browser(spec, a.obsm["X_umap"][:16], args.output)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")


def _measure_browser(spec, coordinates, output):
    import numpy as np
    from playwright.sync_api import sync_playwright
    from genome_spy._embed import bundled_module_url
    from tests.integrations.scanpy.helpers import units

    for i, unit in enumerate(units(spec)):
        unit["name"] = f"panel-{i}"
    with sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        page = browser.new_page(
            viewport={"width": 2800, "height": 1800}, device_scale_factor=1
        )
        page.set_content('<style>body{margin:0}</style><div id="chart"></div>')
        started = perf_counter()
        page.evaluate(
            """async ({url,spec})=>{
            const {embed}=await import(url);
            window.api=await embed(document.querySelector('#chart'),spec);
            await new Promise(requestAnimationFrame);
            await new Promise(requestAnimationFrame);
        }""",
            {"url": bundled_module_url("embed"), "spec": spec},
        )
        first_paint = perf_counter() - started
        assert not page.locator(".message-box").count()
        page.wait_for_timeout(800)
        bounds = page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-0'})")
        unit = units(spec)[0]
        encoding = unit.get("layer", [unit])[0]["encoding"]
        xd, yd = [encoding[d]["scale"]["domain"] for d in ("x", "y")]
        observed = page.evaluate(
            "[api.getScaleResolutionByName('umap-x-0').getDomain(), api.getScaleResolutionByName('umap-y-1').getDomain()]"
        )
        np.testing.assert_allclose(observed, [xd, yd])
        canvas = page.locator("canvas").first.bounding_box()
        output.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(output.with_suffix(".png")), full_page=True)
        hover = []
        for i, (x, y) in enumerate(coordinates):
            px = (
                canvas["x"]
                + bounds["x"]
                + bounds["width"] * float((x - xd[0]) / (xd[1] - xd[0]))
            )
            py = (
                canvas["y"]
                + bounds["y"]
                + bounds["height"] * float(1 - (y - yd[0]) / (yd[1] - yd[0]))
            )
            page.mouse.move(px - 2, py - 2)
            page.wait_for_timeout(450)
            started = perf_counter()
            page.mouse.move(px, py)
            # Approach the small marker through a one-pixel neighborhood, as a
            # real pointer does; quantized picking pixels can straddle its edge.
            for dx, dy in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
                page.mouse.move(px + dx, py + dy)
                page.wait_for_timeout(50)
                if page.get_by_text(f"cell-{i}", exact=True).first.is_visible():
                    break
            page.get_by_text(f"cell-{i}", exact=True).first.wait_for(
                state="visible", timeout=2000
            )
            hover.append(perf_counter() - started)
        started = perf_counter()
        page.mouse.wheel(0, -300)
        page.wait_for_function(
            "low=>api.getScaleResolutionByName('umap-x-0').getDomain()[0]>low",
            arg=xd[0],
        )
        zoom_time = perf_counter() - started
        session = page.context.new_cdp_session(page)
        session.send("Performance.enable")
        metrics = {
            item["name"]: item["value"]
            for item in session.send("Performance.getMetrics")["metrics"]
        }
        report = {
            "chromium": browser.version,
            "viewport": [2800, 1800],
            "dpr": 1,
            "isolated_probe_points": 16,
            "first_paint_seconds_including_spec_dispatch": first_paint,
            "hover_median_seconds_after_native_dwell": statistics.median(hover),
            "hover_p95_seconds_after_native_dwell": float(np.percentile(hover, 95)),
            "wheel_domain_change_seconds": zoom_time,
            "js_heap_bytes": metrics["JSHeapUsedSize"],
        }
        browser.close()
        return report


if __name__ == "__main__":
    main()
