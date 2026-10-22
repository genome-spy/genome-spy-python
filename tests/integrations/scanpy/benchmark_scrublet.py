"""Measure stored Scrublet histograms without accessing expression.

Run ``uv run --no-sync python -m tests.integrations.scanpy.benchmark_scrublet --output /tmp/scrublet.json``.
The benchmark reads stored scores only; it never runs Scrublet or reads expression.
"""

import argparse
import json
from pathlib import Path
import platform
from time import perf_counter
import tracemalloc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    import anndata as ad
    import numpy as np
    from scipy import sparse
    from playwright.sync_api import sync_playwright

    import genome_spy.integrations.scanpy as gsc
    from genome_spy.schema import SCHEMA_VERSION
    from tests.integrations.scanpy.browser.test_umap import render

    cells, genes, batches = 100_000, 20_000, 4
    rng = np.random.default_rng(17)
    a = ad.AnnData(sparse.csr_matrix((cells, genes), dtype=np.float32))
    a.obs["doublet_score"] = rng.beta(2, 20, cells)
    a.obs["batch"] = [f"B{i // 25000}" for i in range(cells)]
    a.uns["scrublet"] = {
        "batched_by": "batch",
        "batches": {
            f"B{i}": {"doublet_scores_sim": rng.beta(3, 8, 50_000), "threshold": 0.25}
            for i in range(batches)
        },
    }
    gsc.pl.scrublet_score_distribution(a[:25000], show=False).to_dict()
    original = ad.AnnData.X

    def unread(*args, **kwargs):
        raise AssertionError("Scrublet plotting must not access expression")

    ad.AnnData.X = property(unread)
    tracemalloc.start()
    start = perf_counter()
    try:
        chart = gsc.pl.scrublet_score_distribution(
            a, zoom=True, width=300, height=220, show=False
        )
        prepared = perf_counter()
        spec = chart.to_dict()
        payload = json.dumps(spec, separators=(",", ":")).encode()
        serialized = perf_counter()
    finally:
        ad.AnnData.X = original
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert any(
        len(rows) == batches * 98 and "density" in rows[0]
        for rows in spec["datasets"].values()
    )
    report = {
        "system": platform.platform(),
        "python": platform.python_version(),
        "core": SCHEMA_VERSION,
        "fixture": {
            "seed": 17,
            "cells": cells,
            "genes": genes,
            "batches": batches,
            "simulated_scores": 200_000,
            "panels": 2 * batches,
        },
        "scope": "Imports/fixture excluded; validated JSON includes allocation tracing. Expression access raises. Browser timing excludes JSON validation.",
        "seconds": {
            "prepare": prepared - start,
            "validated_json": serialized - prepared,
        },
        "bytes": {"json": len(payload), "python_peak": peak},
    }
    with sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        page = browser.new_page(viewport={"width": 1400, "height": 1500})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        start = perf_counter()
        render(page, spec)
        report["seconds"]["browser_first_paint"] = perf_counter() - start
        report["bytes"]["reported_js_heap"] = page.evaluate(
            "performance.memory.usedJSHeapSize"
        )
        assert not errors, errors
        browser.close()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
