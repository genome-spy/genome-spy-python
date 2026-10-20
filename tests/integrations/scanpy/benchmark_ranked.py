"""Measure stored rank preparation and six native label panels.

Run ``uv run --no-sync python -m tests.integrations.scanpy.benchmark_ranked --output /tmp/ranked.json``.
This local observation includes no differential-expression analysis.
"""

import argparse
from importlib.metadata import version
import json
from pathlib import Path
import platform
from time import perf_counter
import tracemalloc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    import anndata as ad
    import numpy as np
    import pandas as pd
    from scipy import sparse
    from playwright.sync_api import sync_playwright

    import genome_spy.integrations.scanpy as gsc
    from genome_spy._embed import bundled_module_url
    from genome_spy.schema import SCHEMA_VERSION
    from tests.integrations.scanpy.helpers import units

    cells, genes, groups = 100_000, 20_000, [str(i) for i in range(6)]
    rng = np.random.default_rng(17)
    adata = ad.AnnData(sparse.csr_matrix((cells, genes), dtype=np.float32))
    adata.var_names = [f"gene-{i}" for i in range(genes)]
    adata.obs["group"] = pd.Categorical(np.arange(cells) % len(groups))
    adata.uns["rank_genes_groups"] = {
        "params": {
            "groupby": "group",
            "method": "logreg",
            "use_raw": False,
            "reference": "rest",
        },
        "names": np.rec.fromarrays(
            [rng.permutation(adata.var_names.to_numpy()) for _ in groups], names=groups
        ),
        "scores": np.rec.fromarrays(
            [np.sort(rng.standard_normal(genes))[::-1] for _ in groups], names=groups
        ),
    }
    original = sparse.csr_matrix.toarray

    def unread(*args, **kwargs):
        raise AssertionError("Rank labels must not densify expression")

    sparse.csr_matrix.toarray = unread
    tracemalloc.start()
    start = perf_counter()
    try:
        chart = gsc.pl.rank_genes_groups(
            adata, n_genes=30, ncols=3, width=300, height=300, show=False
        )
        prepared = perf_counter()
        spec = chart.to_dict()
        payload = json.dumps(spec, separators=(",", ":")).encode()
        serialized = perf_counter()
    finally:
        sparse.csr_matrix.toarray = original
    retained, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    panels = units(spec)
    assert len(panels) == 6
    assert sum(len(rows) for rows in spec["datasets"].values()) == 180
    for index, panel in enumerate(panels):
        panel["name"] = f"panel-{index}"
    report = {
        "system": platform.platform(),
        "python": platform.python_version(),
        "versions": {
            p: version(p) for p in ("scanpy", "anndata", "numpy", "pandas", "scipy")
        },
        "core": SCHEMA_VERSION,
        "fixture": {
            "seed": 17,
            "cells": cells,
            "genes": genes,
            "panels": 6,
            "labels": 180,
        },
        "scope": "Imports and fixture excluded; includes plotting setup and validated compact JSON with allocation tracing enabled. Sparse expression is unread.",
        "seconds": {
            "prepare": prepared - start,
            "validated_json": serialized - prepared,
        },
        "bytes": {
            "json": len(payload),
            "python_peak": peak,
            "python_retained": retained,
        },
    }
    with sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        page = browser.new_page(viewport={"width": 1400, "height": 1000})
        page.set_content('<div id="chart"></div>')
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        start = perf_counter()
        page.evaluate(
            """async ({url,spec})=>{
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
        render = perf_counter() - start
        assert not page.locator(".message-box").count()
        hover = []
        canvas = page.locator("canvas").first.bounding_box()
        for index, panel in enumerate(panels):
            bounds = page.evaluate(
                "i=>api.views.getLayoutBounds({scope:[],view:'panel-'+i})", index
            )
            row = spec["datasets"][panel["data"]["name"]][1]
            x0, x1 = panel["encoding"]["x"]["scale"]["domain"]
            y0, y1 = panel["encoding"]["y"]["scale"]["domain"]
            px = (
                canvas["x"]
                + bounds["x"]
                + (row["_rank"] - x0) / (x1 - x0) * bounds["width"]
            )
            py = (
                canvas["y"]
                + bounds["y"]
                + (y1 - row["_score"]) / (y1 - y0) * bounds["height"]
            )
            start = perf_counter()
            for dx, dy in [(0, -4), (0, -8), (2, -4)]:
                page.mouse.move(px + dx, py + dy)
                page.wait_for_timeout(450)
                page.mouse.move(px + dx + 0.2, py + dy + 0.2)
                page.wait_for_timeout(100)
                if page.get_by_text(row["_label"], exact=True).is_visible():
                    break
            page.get_by_text(row["_label"], exact=True).wait_for(
                state="visible", timeout=2000
            )
            hover.append(perf_counter() - start)
        session = page.context.new_cdp_session(page)
        session.send("HeapProfiler.collectGarbage")
        heap = session.send("Runtime.getHeapUsage")["usedSize"]
        report["browser"] = {
            "chromium": browser.version,
            "viewport": [1400, 1000],
            "dpr": 1,
            "render_seconds_including_dispatch_and_enter_animation": render,
            "hover_seconds_including_pointer_pause": hover,
            "retained_js_heap_after_gc": heap,
        }
        assert not errors, errors
        page.screenshot(path=str(args.output.with_suffix(".png")), full_page=True)
        browser.close()
    args.output.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
