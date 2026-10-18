"""Measure selected-column grouped-plot preparation, payload and native rendering.

Run ``uv run --no-sync python -m tests.integrations.scanpy.benchmark_grouped --output /tmp/dotplot.json``.
This is an explicit observation, not a portable CI timing limit.
"""

import argparse
from importlib.metadata import version
from datetime import date
import json
from pathlib import Path
import platform
import resource
import sys
from time import perf_counter
import tracemalloc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--browser", action="store_true")
    parser.add_argument("--plot", choices=("dotplot", "matrixplot"), default="dotplot")
    parser.add_argument("--dendrogram", action="store_true")
    args = parser.parse_args()
    import anndata as ad
    import numpy as np
    import pandas as pd
    from scipy import sparse

    import genome_spy.integrations.scanpy as gsc

    rng = np.random.default_rng(0)
    cells, genes, markers, groups = 100_000, 20_000, 40, 50
    matrix = sparse.coo_matrix(
        (
            rng.random(cells * 10, dtype=np.float32),
            (np.repeat(np.arange(cells), 10), rng.integers(0, genes, cells * 10)),
        ),
        shape=(cells, genes),
    ).tocsr()
    adata = ad.AnnData(
        matrix,
        obs=pd.DataFrame(
            {"group": pd.Categorical(rng.integers(groups, size=cells).astype(str))},
            index=[f"cell{i}" for i in range(cells)],
        ),
    )
    adata.var_names = [f"g{i}" for i in range(genes)]
    if args.dendrogram:
        adata.obsm["X_pca"] = rng.standard_normal((cells, 20), dtype=np.float32)
    original, shapes = sparse.csr_matrix.toarray, []

    def selected_only(matrix, *positional, **kwargs):
        shapes.append(list(matrix.shape))
        assert matrix.shape == (cells, markers)
        return original(matrix, *positional, **kwargs)

    sparse.csr_matrix.toarray = selected_only
    tracemalloc.start()
    start = perf_counter()
    try:
        chart = getattr(gsc.pl, args.plot)(
            adata,
            [f"g{i}" for i in range(markers)],
            "group",
            show=False,
            width=1400,
            height=1600,
            dendrogram=args.dendrogram,
        )
    finally:
        sparse.csr_matrix.toarray = original
    prepared = perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    spec = chart.to_dict()
    spec["name"] = "benchmark"
    payload = json.dumps(spec, separators=(",", ":")).encode()
    serialized = perf_counter()
    report = {
        "measured": date.today().isoformat(),
        "plot": args.plot,
        "preparation_scope": "Cold plotting call including optional Scanpy imports; matrix construction excluded.",
        "system": platform.platform(),
        "python": platform.python_version(),
        "versions": {
            p: version(p) for p in ("scanpy", "anndata", "numpy", "pandas", "scipy")
        },
        "fixture": {
            "seed": 0,
            "cells": cells,
            "genes": genes,
            "selected_genes": markers,
            "groups": groups,
            "summary_marks": markers * groups,
            "dendrogram": args.dendrogram,
            "resident_pca_components": 20 if args.dendrogram else None,
        },
        "densified_shapes": shapes,
        "seconds": {
            "chart_preparation": prepared - start,
            "validated_json": serialized - prepared,
        },
        "bytes": {
            "python_preparation_peak_allocations": peak,
            "json": len(payload),
            "peak_process_rss": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            * (1 if sys.platform == "darwin" else 1024),
        },
    }
    if args.browser:
        from playwright.sync_api import sync_playwright
        from genome_spy._embed import bundled_module_url

        with sync_playwright() as runtime:
            browser = runtime.chromium.launch()
            page = browser.new_page(
                viewport={"width": 2000, "height": 1900}, device_scale_factor=1
            )
            page.set_content('<div id="chart"></div>')
            start = perf_counter()
            page.evaluate(
                """async ({url,spec}) => {
                const {embed}=await import(url);
                window.api=await embed(document.querySelector('#chart'),spec);
                await new Promise(requestAnimationFrame);
                await new Promise(requestAnimationFrame);
            }""",
                {"url": bundled_module_url("embed"), "spec": spec},
            )
            page.wait_for_function("""() => Math.abs(
                document.querySelector('canvas').getBoundingClientRect().width
                - api.getLogicalCanvasSize().width) < 0.1""")
            elapsed = perf_counter() - start
            assert not page.locator(".message-box").count()
            bounds = page.evaluate(
                "api.views.getLayoutBounds({scope:[],view:'benchmark'})"
            )
            canvas = page.locator("canvas").first.bounding_box()
            xpad, ypad = (0.3, 0.5) if args.plot == "dotplot" else (0, 0)
            px = (
                canvas["x"]
                + bounds["x"]
                + (0.5 + xpad) / (markers + 2 * xpad) * bounds["width"]
            )
            py = (
                canvas["y"]
                + bounds["y"]
                + (0.5 + ypad) / (groups + 2 * ypad) * bounds["height"]
            )
            page.mouse.move(px - 2, py - 2)
            page.wait_for_timeout(450)
            start = perf_counter()
            for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
                page.mouse.move(px + dx, py + dy)
                page.wait_for_timeout(80)
                if page.locator("table.attributes").is_visible():
                    break
            page.locator("table.attributes").wait_for(state="visible")
            hover_elapsed = perf_counter() - start
            assert (
                page.locator("table.attributes tr")
                .first.locator("td")
                .inner_text()
                .strip()
                == "g0"
            )
            session = page.context.new_cdp_session(page)
            session.send("Performance.enable")
            metrics = {
                item["name"]: item["value"]
                for item in session.send("Performance.getMetrics")["metrics"]
            }
            report["browser"] = {
                "chromium": browser.version,
                "viewport": [2000, 1900],
                "dpr": 1,
                "plot_area": [1400, 1600],
                "first_paint_seconds_including_dispatch": elapsed,
                "hover_roundtrip_seconds_excluding_pointer_pause": hover_elapsed,
                "js_heap_bytes": metrics["JSHeapUsedSize"],
            }
            browser.close()
    args.output.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
