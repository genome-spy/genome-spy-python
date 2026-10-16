# Scanpy reference fixtures

Generated explicitly with `uv run --group scanpy-test python -m tools.scanpy_reference`.
The environment is locked in `uv.lock`; `umap.json` records exact scientific
versions, export/display DPI, checksums, source positions and rendered values.
`api.json` records the complete pinned public callable inventory and defaults.

The original synthetic input lives in `tests/scanpy_fixtures.py` and is covered
by this project's MIT license. No real datasets, benchmark implementations,
Scanpy source, or upstream tutorial images are redistributed here.

Reference generation may inspect Matplotlib artists. Production preparation
and ordinary tests never recover plot inputs from them. Duplicate coordinates
and names are not used to join observations. The UMAP compatibility guide
documents the observable 1.11.5 size-vector behavior across multiple panels.

Full figures retain axes, titles and legends. Isolated marker crops use a known
150/100 export/display ratio and supply an independent footprint oracle.
Browser tests retain measured captures/overlays in their pytest output directory;
they do not fit image alignment or alter source measurements.
