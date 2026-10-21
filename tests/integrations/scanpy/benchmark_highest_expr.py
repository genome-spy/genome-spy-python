"""Measure count normalization, top-gene summaries and native boxes on sparse counts.

Run ``uv run --no-sync python -m tests.integrations.scanpy.benchmark_highest_expr --output /tmp/highest-expression.json``.
Only selected columns may be densified; no preprocessing or analysis is run.
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

    cells, genes = 50_000, 20_000
    rng = np.random.default_rng(17)
    matrix = sparse.random(
        cells,
        genes,
        density=0.001,
        format="csr",
        rng=rng,
        data_rvs=lambda count: rng.integers(1, 20, count).astype(np.float32),
        dtype=np.float32,
    )
    a = ad.AnnData(matrix)
    original = sparse.csr_matrix.toarray
    shapes = []

    def selected_only(matrix, *args, **kwargs):
        """Record dense column accesses and reject full-matrix conversion."""
        shapes.append(matrix.shape)
        assert matrix.shape == (cells, 1)
        return original(matrix, *args, **kwargs)

    # Exclude one-time schema/import/JIT work from steady-state chart preparation.
    gsc.pl.highest_expr_genes(ad.AnnData(np.ones((2, 2))), show=False).to_dict()
    sparse.csr_matrix.toarray = selected_only
    tracemalloc.start()
    start = perf_counter()
    try:
        chart = gsc.pl.highest_expr_genes(
            a, n_top=20, zoom=True, height=450, show=False
        )
        prepared = perf_counter()
        spec = chart.to_dict()
        payload = json.dumps(spec, separators=(",", ":")).encode()
        serialized = perf_counter()
    finally:
        sparse.csr_matrix.toarray = original
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert shapes == [(cells, 1)] * 20
    assert a.X is matrix
    assert any(
        len(rows) == 20 and "q1" in rows[0] for rows in spec["datasets"].values()
    )
    report = {
        "system": platform.platform(),
        "python": platform.python_version(),
        "core": SCHEMA_VERSION,
        "fixture": {
            "seed": 17,
            "cells": cells,
            "genes": genes,
            "top_genes": 20,
            "nonzero_counts": matrix.nnz,
        },
        "scope": "Imports/fixture excluded; validated JSON includes allocation tracing. Sparse normalization included; one-column densification enforced. Browser timing excludes JSON validation.",
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
