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

`dotplot.json` and `dotplot-*.png` retain eleven complete Scanpy dotplots and their
registered plot crops at 100 display / 150 export DPI. Cases cover default
statistics, ordering, log/expressed-only summaries, scaling (including after
swapping), authoritative/constant color tables, clipped areas and repeated feature slots.
The comparison calls explicitly use viridis, whose shared published palette
avoids conflating geometry/scaling checks with Vega reds' different stops.
The generator records rendered positions/areas/paint, tick labels, source hashes,
versions and full-image hashes. Native tests retain full captures and overlays
in the pytest output directory, at DPR 1.5, with no image fitting.

```sh
uv run --no-sync python -m tests.integrations.scanpy.generate_dotplot_references
```

`matrixplot.json` and `matrixplot-*.png` retain thirteen complete Scanpy
matrixplots and registered plot crops at the same 100/150 display/export DPI.
The original shared grouped input is extended by `matrixplot_fixture.py`.
Cases cover one-pass scaling before transpose, authoritative supplied values and
ordering, explicit row reindexing, log, repeated slots, missing tiles, constant
normalization and singular edge styling. Values, tile bounds/paint, color domain,
labels, edge widths/colors, input checksums and versions are frozen explicitly.
Native browser checks retain complete captures and registered overlays at DPR 1.5.

```sh
uv run --no-sync python -m tests.integrations.scanpy.generate_matrixplot_references
```

`dendrogram.json` freezes eight numerical tree computations and twelve complete
charts/crops from the original MIT `dendrogram_fixture.py` inputs. Numerical
cases cover default correlations/linkage, missing observations, multiple keys,
existing PCA, custom correlation/linkage, optimal ordering, ties and identical
profiles. Charts cover all standalone orientations, dot/matrix attachments in
both orientations, matching marker blocks and correlation trees/numbers.
The manifest retains source/image hashes, versions, 100/150 display/export DPI,
axes, labels, exact branch paths and correlation values. Registered native tests
compare branch paint and complete annotations at DPR 1.5; captures and overlays
are written to pytest output, with no image fitting.

```sh
uv run --no-sync python -m tests.integrations.scanpy.generate_dendrogram_references
```

`dotplot-performance.json` records the October 17 sparse 100,000-cell ×
20,000-gene check: only 40 requested columns densify; the chart carries 50 × 40
summary dots. Cold preparation includes optional imports; browser first paint
includes dispatch. Heap, Python allocation/RSS, payload and runtime metadata
are single-machine observations, not portable limits.
`dotplot-index-hover-performance.json` repeats that workload after the index-scale
and default-hover update, retaining the earlier observation for comparison.
Reproduce explicitly:

```sh
uv run --no-sync python -m tests.integrations.scanpy.benchmark_grouped --browser --output /tmp/dotplot.json
```

The same benchmark accepts `--plot matrixplot`, reusing the selected-column
workload for 2,000 summary tiles. `matrixplot-performance.json` records the
October 18 native tile observation, including preparation allocations, RSS,
payload, browser first paint, hover response and live JS heap. Timings are
single-machine observations; sparse densification remains restricted to the
100,000 × 40 selected columns.

`dendrogram-performance.json` adds a tree to that matrixplot workload using an
existing 100,000 × 20 float32 PCA representation. It records the same allocation,
payload, rendering, hover and heap measurements; tree computation does not
materialize the full expression matrix. The chart has 50 groups and 2,000 tiles.
The current observation delegates computation to public sc.tl.dendrogram;
stored Scanpy results are read without repeating that computation.
Correlation/linkage costs grow with group count; this is a tested workload,
not an arbitrary-group-count performance promise.

```sh
uv run --no-sync python -m tests.integrations.scanpy.benchmark_grouped --plot matrixplot --dendrogram --browser --output /tmp/trees.json
```

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
