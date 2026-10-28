# Scanpy reference fixtures

These JSON files are test inputs and expected results, not run reports. Python
and browser tests read their numeric values, API contracts, labels, domains,
geometry and provenance. Keep them when cleaning generated artifacts.

Tracked fixtures: `api.json`, `clustermap.json`, `dendrogram.json`, `dotplot.json`, `embedding.json`, `grouped.json`, `heatmap.json`, `matrix.json`, `matrixplot.json`, `ranked.json`, `scatter.json`, `umap.json`.

Reference generation uses the pinned Scanpy/scientific stack in `pyproject.toml`
and `uv.lock`. The original inputs and explicit `generate_*_references.py` scripts
live in the parent directory. Run generators deliberately; tests never refresh
tracked references. Inspect changes against upstream behavior before accepting them.

Generators may inspect Matplotlib artists for the independent Scanpy reference.
Production preparation does not. Source hashes, version metadata and display/export
DPI in these fixtures make comparisons reproducible. Native palette bins, text
metrics and rasterization differences are checked with explicit test tolerances;
registered overlays must not resize or fit images to hide discrepancies.

Generated reference images, screenshots, overlays, HTML/PDF exports, recordings
and logs must stay in temporary directories or ignored local caches. Browser
tests write through pytest's temporary paths. Allocation behavior is covered by
small deterministic regression tests; the former manual benchmark scripts have
been removed.

The fixtures use original small synthetic inputs under this project's MIT license.
Keep applicable source/data attribution when adding references. No downloaded
analysis dataset or upstream tutorial image belongs in this directory.
