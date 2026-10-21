"""Measure a bounded clustermap of 700 packaged PBMC cells and 40 genes.

Run with --output /tmp/clustermap.json. Timings are observations, not CI limits.
"""

import argparse
from datetime import date
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
    import scanpy as sc
    from scipy.cluster.hierarchy import linkage
    from playwright.sync_api import sync_playwright

    import genome_spy.integrations.scanpy as gsc
    from tests.integrations.scanpy.browser.test_heatmap import render, hover_at

    # A transport/clustering workload, without interpreting the first genes as markers.
    data = sc.datasets.pbmc68k_reduced().raw[:, :40].to_adata()
    tracemalloc.start()
    start = perf_counter()
    values = data.X.toarray()
    row_linkage = linkage(values, method="average")
    col_linkage = linkage(values.T, method="average")
    chart = gsc.pl.clustermap(
        data,
        obs_keys="bulk_labels",
        use_raw=False,
        row_linkage=row_linkage,
        col_linkage=col_linkage,
        row_gap_threshold=0.9 * row_linkage[:, 2].max(),
        col_gap_threshold=0.9 * col_linkage[:, 2].max(),
        zoom="xy",
        show_values=True,
        yticklabels=False,
        width=550,
        height=550,
        show=False,
    )
    prepared = perf_counter()
    payload = chart.to_json()
    serialized = perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    spec = json.loads(payload)
    report = {
        "measured": date.today().isoformat(),
        "system": platform.platform(),
        "python": platform.python_version(),
        "versions": {
            name: version(name)
            for name in ("scanpy", "anndata", "numpy", "pandas", "scipy")
        },
        "fixture": {
            "dataset": "scanpy.datasets.pbmc68k_reduced",
            "source": "raw, first 40 genes",
            "shape": list(data.shape),
            "matrix_values": data.n_obs * data.n_vars,
            "row_distances": data.n_obs * (data.n_obs - 1) // 2,
        },
        "scope": "Dependencies loaded; linkage, chart preparation and validated JSON serialization measured; source construction excluded; tracemalloc active.",
        "gap_cut": "90% of each tree's maximum merge distance; linkage included in preparation.",
        "gap_counts": {
            axis: len(spec["scales"][axis]["gapPositions"]) for axis in ("x", "y")
        },
        "interactions": {"zoom": "xy", "show_values": True},
        "seconds": {
            "preparation": prepared - start,
            "serialization": serialized - prepared,
        },
        "bytes": {"peak_python_allocations": peak, "json": len(payload.encode())},
    }
    with sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        page = browser.new_page(viewport={"width": 1800, "height": 1400})
        start = perf_counter()
        bounds = render(page, chart)
        elapsed = perf_counter() - start
        fractions = page.evaluate("""() => ['x','y'].map(axis=>{
            const s=api.getScaleResolutionByName(`clustermap-${axis}`).getScale();
            const i=axis==='x'?20:350;
            return (axis==='x'?s(i):1-s(i))+s.bandwidth()/2;
        })""")
        start = perf_counter()
        hover_at(
            page,
            bounds["x"] + fractions[0] * bounds["width"],
            bounds["y"] + fractions[1] * bounds["height"],
        )
        page.locator("table.attributes").wait_for(state="visible")
        hover = perf_counter() - start
        report["browser"] = {
            "chromium": browser.version,
            "viewport": [1800, 1400],
            "dpr": 1,
            "first_paint_seconds_including_dispatch": elapsed,
            "hover_seconds_including_pointer_pause_and_probes": hover,
            "js_heap_bytes": page.evaluate("performance.memory.usedJSHeapSize"),
        }
        browser.close()
    args.output.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
