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
    parser.add_argument(
        "--plot", choices=("dotplot", "matrixplot", "heatmap"), default="dotplot"
    )
    parser.add_argument("--dendrogram", action="store_true")
    parser.add_argument("--ranked", action="store_true")
    parser.add_argument(
        "--builder",
        action="store_true",
        help="Measure DotPlot construction and three native chart snapshots.",
    )
    args = parser.parse_args()
    if args.builder and (args.plot != "dotplot" or args.ranked):
        parser.error("--builder requires --plot dotplot without --ranked")
    import anndata as ad
    import numpy as np
    import pandas as pd
    from scipy import sparse

    import genome_spy.integrations.scanpy as gsc
    from genome_spy.schema import SCHEMA_VERSION

    rng = np.random.default_rng(0)
    cells, genes, markers, groups = 100_000, 20_000, 40, 50
    if args.plot == "heatmap":
        cells, markers = 5_000, 50
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
    if args.ranked:
        labels = [str(i) for i in range(groups)]
        names = adata.var_names.to_numpy()
        scores = np.linspace(100, 1, genes)
        adata.uns["rank_genes_groups"] = {
            "params": {
                "groupby": "group",
                "method": "t-test",
                "reference": "rest",
                "use_raw": False,
            },
            **{
                key: np.rec.fromarrays([values] * groups, names=labels)
                for key, values in {
                    "names": names,
                    "scores": scores,
                    "logfoldchanges": scores / 2,
                    "pvals": np.linspace(0.00001, 0.9, genes),
                    "pvals_adj": np.linspace(0.0001, 1, genes),
                }.items()
            },
        }
    original, shapes = sparse.csr_matrix.toarray, []

    def selected_only(matrix, *positional, **kwargs):
        shapes.append(list(matrix.shape))
        rows = 0 if args.ranked and args.plot == "matrixplot" else cells
        assert matrix.shape == (rows, markers), matrix.shape
        return original(matrix, *positional, **kwargs)

    sparse.csr_matrix.toarray = selected_only
    tracemalloc.start()
    start = perf_counter()
    try:
        family = f"rank_genes_groups_{args.plot}" if args.ranked else args.plot
        positional = () if args.ranked else ([f"g{i}" for i in range(markers)], "group")
        options = {}
        if args.ranked:
            options.update(groups=["0"], n_genes=markers, zoom=True)
            if args.plot != "heatmap":
                options["values_to_plot"] = "scores"
        if args.builder:
            family = "DotPlot"
            plot = gsc.pl.DotPlot(
                adata, *positional, width=1400, height=1600, zoom=True
            )
            if args.dendrogram:
                plot.add_dendrogram()
            snapshots = [plot.to_chart()]
            snapshots.append(plot.swap_axes().to_chart())
            snapshots.append(
                plot.swap_axes(swap_axes=False).add_totals(color="steelblue").to_chart()
            )
            chart = snapshots[-1]
            assert shapes == [[cells, markers]]
        else:
            chart = getattr(gsc.pl, family)(
                adata,
                *positional,
                show=False,
                width=1400,
                height=1600,
                dendrogram=args.dendrogram,
                **options,
            )
    finally:
        sparse.csr_matrix.toarray = original
    prepared = perf_counter()
    retained, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    spec = chart.to_dict()
    spec.get("spec", spec)["name"] = "benchmark"
    for axis in ("x", "y"):
        spec["scales"][axis].setdefault("name", f"{args.plot}-{axis}")
    payload = json.dumps(spec, separators=(",", ":")).encode()
    serialized = perf_counter()
    report = {
        "measured": date.today().isoformat(),
        "plot": family,
        "core": SCHEMA_VERSION,
        "preparation_scope": "Cold plotting call including optional Scanpy imports; expression/ranking fixture construction excluded. Allocation tracing covers preparation only.",
        "system": platform.platform(),
        "python": platform.python_version(),
        "versions": {
            p: version(p) for p in ("scanpy", "anndata", "numpy", "pandas", "scipy")
        },
        "fixture": {
            "seed": 0,
            "cells": cells,
            "genes": genes,
            "nnz": matrix.nnz,
            "stored_ranks_per_group": genes if args.ranked else None,
            "values_to_plot": "scores"
            if args.ranked and args.plot != "heatmap"
            else None,
            "selected_genes": markers,
            "groups": groups,
            "summary_marks": markers * groups if args.plot != "heatmap" else None,
            "expression_tiles": cells * markers if args.plot == "heatmap" else None,
            "dendrogram": args.dendrogram,
            "resident_pca_components": 20 if args.dendrogram else None,
            "builder_snapshots": 3 if args.builder else None,
        },
        "densified_shapes": shapes,
        "seconds": {
            "chart_preparation": prepared - start,
            "validated_json": serialized - prepared,
        },
        "bytes": {
            "python_preparation_peak_allocations": peak,
            "python_preparation_retained_allocations": retained,
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
            column, row, hover_gene = 0, 0, "g0"
            if args.plot == "dotplot":
                records = next(
                    rows for rows in spec["datasets"].values() if "_percent" in rows[0]
                )
                probe = max(records, key=lambda row: row["_percent"])
                assert probe["_percent"] > 0
                column, row, hover_gene = probe["_x"], probe["_y"], probe["_gene"]
                report["fixture"]["hover_probe"] = {
                    key: probe[key] for key in ("_gene", "_group", "_percent")
                }
            if args.plot == "heatmap":
                row = cells // 2
            fractions = page.evaluate(
                """({family,column,row})=>['x','y'].map(axis=>{
                const scale=api.getScaleResolutionByName(`${family}-${axis}`).getScale();
                return axis==='x' ? scale(column)+scale.bandwidth()/2
                    : 1-scale(row)+scale.bandwidth()/2;
            })""",
                {"family": args.plot, "column": column, "row": row},
            )
            px = canvas["x"] + bounds["x"] + fractions[0] * bounds["width"]
            py = canvas["y"] + bounds["y"] + fractions[1] * bounds["height"]
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
                .nth(2 if args.plot == "heatmap" else 0)
                .locator("td")
                .inner_text()
                .strip()
                == hover_gene
            )
            zoom_elapsed = None
            if args.ranked or args.builder:
                domain = page.evaluate(
                    f"api.getScaleResolutionByName('{args.plot}-y').getDomain()"
                )
                span = domain[1] - domain[0]
                start = perf_counter()
                page.mouse.wheel(0, -220)
                page.wait_for_function(
                    "({name,span})=>{const d=api.getScaleResolutionByName(name).getDomain();return d[1]-d[0]<span}",
                    arg={"name": f"{args.plot}-y", "span": span},
                )
                zoom_elapsed = perf_counter() - start
            session = page.context.new_cdp_session(page)
            session.send("HeapProfiler.collectGarbage")
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
                "wheel_step_change_seconds": zoom_elapsed,
                "js_heap_bytes": metrics["JSHeapUsedSize"],
                "heap_scope": "Live chart/runtime after interaction and explicit garbage collection.",
            }
            browser.close()
    args.output.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
