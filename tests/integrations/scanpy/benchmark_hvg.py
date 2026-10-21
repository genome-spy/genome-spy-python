"""Measure metadata-only variable-gene panels over a large sparse AnnData shape.

Run ``uv run --no-sync python -m tests.integrations.scanpy.benchmark_hvg --output /tmp/hvg.json``.
The benchmark never computes variable genes or reads expression.
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

    cells, genes = 100_000, 20_000
    rng = np.random.default_rng(17)
    a = ad.AnnData(sparse.csr_matrix((cells, genes), dtype=np.float32))
    a.var_names = [f"gene-{i}" for i in range(genes)]
    for name in ("means", "dispersions", "dispersions_norm"):
        a.var[name] = rng.lognormal(size=genes).astype(np.float32)
    a.var["highly_variable"] = rng.random(genes) > 0.7
    a.uns["hvg"] = {"flavor": "seurat"}
    original = ad.AnnData.X

    def unread(*args, **kwargs):
        raise AssertionError("QC diagnostics must not access expression")

    ad.AnnData.X = property(unread)
    tracemalloc.start()
    start = perf_counter()
    try:
        chart = gsc.pl.highly_variable_genes(a, zoom=True, show=False)
        prepared = perf_counter()
        spec = chart.to_dict()
        payload = json.dumps(spec, separators=(",", ":")).encode()
        serialized = perf_counter()
    finally:
        ad.AnnData.X = original
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert len(spec["datasets"]) == 1
    assert len(next(iter(spec["datasets"].values()))) == genes
    report = {
        "system": platform.platform(),
        "python": platform.python_version(),
        "core": SCHEMA_VERSION,
        "fixture": {"seed": 17, "cells": cells, "genes": genes, "panels": 2},
        "scope": "Imports/fixture excluded; validated JSON includes allocation tracing. Expression access raises. Browser timing excludes JSON validation.",
        "seconds": {
            "prepare": prepared - start,
            "validated_json": serialized - prepared,
        },
        "bytes": {"json": len(payload), "python_peak": peak},
    }
    with sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        page = browser.new_page(viewport={"width": 1400, "height": 1000})
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
