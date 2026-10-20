"""Measure seeded sparse embedding/scatter workloads in a fresh process.

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
import tracemalloc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells", type=int, default=100_000)
    parser.add_argument("--panels", type=int, choices=[1, 8], default=1)
    parser.add_argument(
        "--plot", choices=["umap", "pca", "scatter", "scatter-genes"], default="umap"
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--browser", action="store_true")
    args = parser.parse_args()
    if args.cells < 16:
        parser.error("--cells must be at least 16 for the isolated hover probes")
    import anndata as ad
    import numpy as np
    import pandas as pd
    import scanpy as sc
    from scipy import sparse

    import genome_spy.integrations.scanpy as gsc
    from genome_spy.schema import SCHEMA_VERSION

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
    coordinates = a.obsm["X_umap"]
    labels = a.obs_names[:16].tolist()
    if args.plot == "pca":
        a.obsm["X_pca"] = rng.standard_normal((n, 50)).astype(np.float32)
        a.uns["pca"] = {"variance_ratio": np.full(50, 0.02)}
        coordinates = a.obsm["X_pca"][:, [1, 49]]
    elif args.plot == "scatter-genes":
        a.var["group"] = pd.Categorical(rng.integers(0, 12, genes).astype(str))
        a.var["score"] = rng.standard_normal(genes).astype(np.float32)
        coordinates = rng.standard_normal((genes, 2)).astype(np.float32)
        labels = a.var_names[:16].tolist()
    if args.browser:
        # Exposed points let the interaction oracle name exact source IDs.
        coordinates[:16] = [[6 + i % 4 * 0.4, 6 + i // 4 * 0.4] for i in range(16)]
        if args.plot == "pca":
            a.obsm["X_pca"][:, [1, 49]] = coordinates
    if args.plot.startswith("scatter"):
        axis_table = a.var if args.plot == "scatter-genes" else a.obs
        axis_table["x"], axis_table["y"] = coordinates.T
    # Fail on a dense allocation larger than a single requested gene column.
    original = sparse.csr_matrix.toarray
    shapes = []

    def selected_only(matrix, *positional, **kwargs):
        shapes.append(list(matrix.shape))
        expected = (1, genes) if args.plot == "scatter-genes" else (n, 1)
        assert matrix.shape == expected, matrix.shape
        return original(matrix, *positional, **kwargs)

    sparse.csr_matrix.toarray = selected_only
    keys = ["group", "score", "g0", "g1", "g2", "g3", "group", "score"]
    options = {}
    if args.plot == "pca":
        options["components"] = "2,50"
    elif args.plot.startswith("scatter"):
        options.update(x="x", y="y")
        if args.plot == "scatter-genes":
            keys[2:6] = a.obs_names[:4].tolist()
    tracemalloc.start()
    start = perf_counter()
    try:
        chart = getattr(gsc.pl, args.plot.split("-")[0])(
            a,
            color=keys if args.panels == 8 else keys[2],
            zoom=args.browser,
            size=36 if args.browser else None,
            show=False,
            **options,
        )
    finally:
        sparse.csr_matrix.toarray = original
    prepared_at = perf_counter()
    transport = chart._prepare_render()
    serialized_at = perf_counter()
    spec = chart.to_dict()
    encoded = json.dumps(spec, separators=(",", ":")).encode()
    json_at = perf_counter()
    retained, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    report = {
        "plot": args.plot,
        "preparation_scope": "Imports and fixture construction excluded; includes plotting setup, Arrow and validated JSON with allocation tracing enabled.",
        "hardware": {
            "system": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "python": platform.python_version(),
        "core": SCHEMA_VERSION,
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
            "displayed_rows": len(coordinates),
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
            "python_peak_allocations": peak,
            "python_retained_with_arrow_and_json": retained,
            "peak_process_rss": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            * (1 if sys.platform == "darwin" else 1024),
        },
        "densified_shapes": shapes,
        "render_settings": {
            "panel_logical_pixels": [300, 300],
            "logical_pixels_per_point": 100 / 72,
            "native_font": "Lato",
            "reference_font": "DejaVu Sans",
        },
    }
    if args.browser:
        report["browser"] = _measure_browser(
            spec, coordinates[:16], args.output, labels
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")


def _measure_browser(spec, coordinates, output, labels):
    import numpy as np
    from playwright.sync_api import sync_playwright
    from genome_spy._embed import bundled_module_url
    from tests.integrations.scanpy.helpers import points, units

    for i, unit in enumerate(units(spec)):
        unit["name"] = f"panel-{i}"
    with sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        viewport = [max(2800, len(spec.get("hconcat", [])) * 500), 1800]
        page = browser.new_page(
            viewport={"width": viewport[0], "height": viewport[1]},
            device_scale_factor=1,
        )
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
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
        assert not errors, errors
        page.wait_for_timeout(800)
        size = page.evaluate("api.getLogicalCanvasSize()")
        assert size["width"] <= viewport[0] and size["height"] <= viewport[1], size
        for i in range(len(units(spec))):
            panel = page.evaluate(
                "i=>api.views.getLayoutBounds({scope:[],view:'panel-'+i})", i
            )
            assert 0 <= panel["x"] and panel["x"] + panel["width"] <= size["width"] + 1
            assert (
                0 <= panel["y"] and panel["y"] + panel["height"] <= size["height"] + 1
            )
        bounds = page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-0'})")
        unit = units(spec)[0]
        encoding = points(unit)["encoding"]
        xd, yd = [encoding[d]["scale"]["domain"] for d in ("x", "y")]
        names = [encoding[d]["scale"]["name"] for d in ("x", "y")]
        observed = page.evaluate(
            "names=>names.map(n=>api.getScaleResolutionByName(n).getDomain())", names
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
                if page.get_by_text(labels[i], exact=True).first.is_visible():
                    break
            page.get_by_text(labels[i], exact=True).first.wait_for(
                state="visible", timeout=2000
            )
            hover.append(perf_counter() - started)
        started = perf_counter()
        page.mouse.wheel(0, -300)
        page.wait_for_function(
            "({name,low})=>api.getScaleResolutionByName(name).getDomain()[0]>low",
            arg={"name": names[0], "low": xd[0]},
        )
        zoom_time = perf_counter() - started
        session = page.context.new_cdp_session(page)
        session.send("HeapProfiler.collectGarbage")
        session.send("Performance.enable")
        metrics = {
            item["name"]: item["value"]
            for item in session.send("Performance.getMetrics")["metrics"]
        }
        report = {
            "chromium": browser.version,
            "viewport": viewport,
            "dpr": 1,
            "isolated_probe_points": 16,
            "first_paint_seconds_including_spec_dispatch": first_paint,
            "hover_median_seconds_after_native_dwell": statistics.median(hover),
            "hover_p95_seconds_after_native_dwell": float(np.percentile(hover, 95)),
            "wheel_domain_change_seconds": zoom_time,
            "js_heap_bytes": metrics["JSHeapUsedSize"],
            "heap_scope": "After hover/zoom and explicit garbage collection; includes the live chart/runtime.",
        }
        assert not errors, errors
        browser.close()
        return report


if __name__ == "__main__":
    main()
