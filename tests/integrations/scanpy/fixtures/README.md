# Scanpy reference fixtures

Generated explicitly with `uv run --group scanpy-test python -m tests.integrations.scanpy.generate_references`.
The environment is locked in `uv.lock`; `umap.json` records exact scientific
versions, export/display DPI, checksums, source positions and rendered values.
`api.json` records the complete pinned public callable inventory and defaults.

`grouped.json` freezes 17 data/statistic cases from Scanpy 1.11.5's `DotPlot`
constructor, without creating/rendering a figure or inspecting artists. Generate
it explicitly with:

```sh
uv run --no-sync python -m tests.integrations.scanpy.generate_grouped_references
```

Its original MIT input is `tests/integrations/scanpy/grouped_fixture.py`; the
manifest records that file's checksum and scientific-stack versions. Cases cover
raw/layers/symbols, numeric bins, multi-key groups, repeated slots/brackets, source
order, thresholds, missing values, log-before-aggregation and min–max scaling.
Ordinary tests read frozen results alongside hand-calculated checks; production
does not import fixture/generation modules or upstream plotting classes.

The original synthetic input lives in `tests/integrations/scanpy/fixture_data.py` and is covered
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
