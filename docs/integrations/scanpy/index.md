# Scanpy integration

Keep your existing Scanpy analysis and replace supported plotting calls:

```python
import scanpy as sc
import genome_spy.scanpy as gsc

# Scanpy analysis: after your usual preprocessing, compute the embedding once.
sc.pp.neighbors(adata, random_state=0)
sc.tl.umap(adata, random_state=0)  # Writes adata.obsm["X_umap"].

# GenomeSpy plotting: reads those coordinates and returns an interactive chart.
chart = gsc.pl.umap(
    adata, color=["cell_type", "MS4A1"], vmax="p99",
    show=False, hover=True, zoom=True,
)
chart.save("umap.html", inline=True)
```

**Scanpy computes UMAP; GenomeSpy renders it.** If your workflow already has
`adata.obsm["X_umap"]`, go straight to `gsc.pl.umap`. The plotting adapter never
runs neighbors or UMAP analysis. A missing embedding produces an error asking
you to compute it explicitly first.

This development preview implements categorical and continuous 2D UMAP.
Full public Scanpy plotting coverage is the destination; the inventory below
records remaining work. No other plotting family is implemented yet.

## Installation and version contract

```sh
pip install "genome-spy-python[scanpy]"
```

The integration currently supports **Scanpy 1.11.5 only**. Other versions raise
an actionable error at the plotting call. Importing either genome_spy or
genome_spy.scanpy does not import Scanpy, AnnData, NumPy, pandas, SciPy,
Matplotlib, or PyArrow. The scientific dependencies load when plotting.

The optional arrow extra speeds notebook transport. It is not required for
JSON or interactive HTML. The reproducible reference environment is the
scanpy-test dependency group and uv.lock; exact scientific-stack versions are
also recorded in the reference manifest.

## UMAP compatibility

The native function retains the effective Scanpy UMAP parameter names and
defaults, with the explicit renderer-object exceptions below. A parameter
present in the signature can be reserved for later support: unsupported values
raise an error instead of being ignored.

| Parameters | Current behavior |
| --- | --- |
| color | None, one key, or multiple observation/gene keys. Each panel retains its original numeric measurements and supplied coordinates. |
| use_raw, layer, gene_symbols | raw.X by default if available; a layer overrides the automatic raw choice. Explicit use_raw=True plus a layer is an error. Symbol lookup follows UMAP's adata.var lookup before selected expression extraction. |
| palette, na_color, na_in_legend | Explicit sequences/mappings/color cyclers, named Matplotlib palettes, stored category colors, or Scanpy defaults. Preserve categorical order and unused categories; missing points retain a distinct color. |
| cmap, color_map, vmin, vmax | Named/public Matplotlib colormaps and numeric or percentile bounds, including per-panel bounds. Conflicting aliases error. Lookup-table fills preserve source precision and the chart has a native numeric color guide. |
| sort_order | Scanpy's continuous sort, including reversed equal-value ties; missing points draw first. Categorical source order is retained apart from moving missing points behind other points. |
| size, s, marker | Scalar or observation-length sizes in points squared; dot and circle markers. Conversion accounts for marker path width and figure DPI. As in 1.11.5, an observation-size vector is carried in its reordered form between panels; reference tests cover this version-specific behavior. |
| mask_obs, groups | Recolor observations without dropping coordinates. Masks can be boolean arrays or an observation-column key. Groups and masks are mutually exclusive. |
| components, dimensions | One-based component pairs or zero-based dimension pairs; broadcasting follows Scanpy. Both cannot be supplied together. |
| frameon, title, ncols, hspace, wspace | Frame and panel layout from the supported Scanpy/Matplotlib settings. Titles and guides remain per panel; guides are not automatically collected. |
| legend_loc, legend_fontsize, legend_fontweight | Centered right-margin legend, on-data median labels, or no legend; font sizes follow the configured figure DPI. On-data labels currently require legend_fontweight="normal" (or 400); the upstream bold default errors for that location because its glyph atlas is not bundled. |
| alpha, edgecolor/edgecolors, linewidth/linewidths | Scalar opacity and edge styling; conflicting aliases error. Transparent palette/cmap/NA entries require scalar alpha or a disabled guide; per-entry guide transparency is not supported yet. |
| show | False returns a native chart; True displays once through anywidget and returns None. None uses Scanpy settings.autoshow. |
| save | None/False are supported when no automatic image save is requested. Image formats and automatic save currently error; native chart.save supports HTML/JSON. |
| ax, return_fig | Omitted. Passing either, even ax=None, raises a targeted error. Use show=False and native chart composition/configuration. |
| projection, edges/arrows, scale_factor | Only the ordinary 2D/no-graph defaults are supported yet. |
| norm, vcenter, callable color bounds | Not implemented yet. Their nondefault forms raise errors. |
| add_outline, legend_fontoutline, nondefault outline settings | Not implemented yet; no silent approximation with unoutlined points/text. |
| colorbar_loc | Right or None. Other positions are not implemented yet. |
| Arbitrary scatter kwargs, other markers/legend locations | Error with the unsupported argument named. |

Supported input arrays are NumPy and SciPy CSR/CSC matrices/arrays. Views preserve
positional correspondence. Only requested unique expression columns are
densified; AnnData can materialize dense views through its public array access.
Metadata and resident embeddings also work with backed AnnData;
requested backed/lazy expression is not supported yet. Coordinates must be
finite. Continuous values can be missing but must include a finite value;
infinities and ambiguous variable/symbol labels fail clearly.
Category labels must remain distinct when serialized as strings. A category
named "NA" alongside missing values currently errors because the native guide
cannot distinguish those two labels faithfully.

Plot preparation does not mutate AnnData, write palettes, run Scanpy plotting
functions, construct Matplotlib artists, or perform analysis. Charts contain
detached snapshots: later AnnData edits do not change an existing chart.

### Visual fidelity boundaries

Supported defaults retain source coordinate domains, plot dimensions, palette
bins, color normalization, point footprints, draw order, titles, axis labels,
and right-side guide meaning. Numeric guide ticks use public Matplotlib locator
arithmetic. Each panel retains its own guide. Row and column spacing are authored
separately.

The native runtime embeds **Lato Regular**, while the default reference font is
DejaVu Sans. This preview uses bundled Lato to make the default chart portable
offline. Font shape, text measurement, guide padding, and browser antialiasing
therefore differ from Matplotlib. Native panel edges round to backing pixels;
registered plot comparisons allow that rounding and renderer antialiasing.
This is not a claim of pixel-identical complete figures or support for arbitrary
Matplotlib rcParams/style sheets. Exact typography and per-entry transparent
guides need native runtime work; unsupported bold/outlined on-data styling errors
instead of fetching a remote font or silently changing the requested style.

## Interaction and native results

hover=True adds observation ID, original observation name, value/source, and
coordinate tooltips without changing the initial marks. hover=False disables
record hover. zoom=True enables coordinate navigation; it is off by default.
The selection argument is reserved for the linked-selection phase and currently
rejects non-None values.

obs_id selects an existing unique, nonmissing observation-column key. Without it,
unique obs_names supply IDs. Duplicate names receive distinct snapshot-local row
keys, preserving every observation even when coordinates repeat. Those local
keys are not cross-AnnData identity; supply explicit IDs for future linking.

Use normal native chart composition and configuration:

```python
cells = gsc.pl.umap(adata, color="cell_type", show=False)
expression = gsc.pl.umap(adata, color="MS4A1", show=False)
combined = cells | expression
combined.save("cells.html", inline=True)
```

Interactive HTML works without Python when data and runtime are embedded.
Python callbacks require a live notebook kernel. HTML bundling does not make
external URL datasets offline. Native results do not emulate Matplotlib Axes,
Figure attributes, or artist styling methods.

## Full plotting coverage inventory

The tracked API snapshot contains 50 public callables, including aliases,
three builders, and two rcParams helpers. It records callable targets so aliases
remain visible. Function coverage and parameter coverage are separate.

| Delivery | Public entries |
| --- | --- |
| Available | umap |
| Group summaries and trees | dotplot, matrixplot, dendrogram, correlation_matrix |
| Cell heatmaps and ranked summaries | heatmap, matrix, rank_genes_groups_dotplot, rank_genes_groups_matrixplot, rank_genes_groups_heatmap |
| Other embeddings and PCA | scatter, embedding, tsne, pca, pca_scatter, diffmap, draw_graph, pca_loadings, pca_overview, pca_variance_ratio |
| Distributions and tracks | violin, stacked_violin, tracksplot, rank_genes_groups_violin, rank_genes_groups_stacked_violin, rank_genes_groups_tracksplot |
| Diagnostics, ranking, matrices, simulation | clustermap, rank_genes_groups, ranking, highest_expr_genes, highly_variable_genes, filter_genes_dispersion, scrublet_score_distribution, sim |
| Trajectories and graphs | dpt_groups_pseudotime, dpt_timeseries, paga, paga_adjacency, paga_compare, paga_path, timeseries, timeseries_as_heatmap, timeseries_subplot |
| Spatial and density | spatial, embedding_density |
| Plot builders and useful semantic methods | DotPlot, MatrixPlot, StackedViolin |
| Settings helpers retained in Scanpy | set_rcParams_defaults, set_rcParams_scanpy |

All entries except UMAP and settings helpers remain required future integration
work. Settings remain owned by Scanpy. The external.pl namespace is separate
from this core inventory.

Dendrograms belong with grouped-plot coverage. Reuse existing compatible results
or compute missing profiles, distances, linkage and branch coordinates in Python,
then render native rule marks. A dedicated tree mark is unnecessary. This does
not authorize rerunning the user's UMAP or differential-expression analysis.
Violin densities and track envelopes can likewise be prepared in Python, while
their filled geometry needs appropriate native rendering support.

## Reference preparation and validation

Reference assets use original, synthetic test data under the project's MIT
license. They contain duplicate observation names and coordinates, different
raw/X variable vocabularies, unequal category order, missing values, and ties.
No benchmark scripts or real datasets were promoted. Upstream source describes
the contract; the adapter does not vendor Scanpy plotting implementations or
read rendered artists.

Developers can reproduce the pinned API metadata and full reference figures:

```sh
uv sync --dev --extra scanpy --group scanpy-test
uv run --no-sync python -m tools.scanpy_reference
uv run --no-sync pytest tests/test_scanpy_reference.py tests/test_scanpy_contract.py tests/test_scanpy_umap.py
uv run --no-sync python -m playwright install chromium
uv run --no-sync pytest tests/browser/test_scanpy_umap.py
```

Reference generation is explicit and separate from ordinary tests and runtime.
It renders Scanpy figures and records their observed geometry, colors, and
ordering; independent tests also check hand-calculated values, source identities,
sparse allocation, and mutation behavior. PNG checksums, export/display DPI, and
versions are retained under tests/fixtures/scanpy. Browser tests measure actual
marker footprints, retain registered overlays and complete-chart captures, and
exercise hover, navigation, and offline delivery.

### Resource baseline

The explicit benchmark is reproducible without local research directories:

```sh
uv run --no-sync python -m tools.scanpy_performance --cells 100000 --panels 8 --output /tmp/umap-memory.json
uv run --no-sync python -m tools.scanpy_performance --cells 10000 --panels 8 --browser --output /tmp/umap-browser.json
```

The tracked performance-baseline.json records versions, source dimensions,
payloads, hardware, viewport, DPI/DPR, and timing definitions. On an Apple M5
with 32 GiB RAM, the seeded 100,000-cell × 20,000-gene sparse fixture used about
16.4 MB for expression; its dense float32 equivalent would use 8 GB. Preparation
read one selected gene column for one panel and four unique columns for eight
panels. No full matrix was densified.

| Workload | Chart preparation | Arrow transport preparation | Validated JSON export | Arrow / JSON payload | Peak Python RSS |
| --- | --- | --- | --- | --- | --- |
| 100,000 cells, 1 panel | 0.26 s | 0.27 s | 2.49 s | 8.1 / 25.9 MB | 660 MB |
| 100,000 cells, 8 panels | 1.64 s | 1.33 s | 69.95 s | 40.1 / 122.5 MB | 1.67 GB |

In Chromium 156, a separate 10,000-cell eight-panel WebGL run at 2800 × 1800,
DPR 1, took 6.55 seconds to first paint including spec dispatch. All 16 known-ID
hover probes succeeded; median/p95 observed response was 79/181 ms after native
tooltip dwell, including the one-pixel pointer approach and assertion. A wheel
event changed the coordinate domain in 220 ms. Browser JS heap was 148 MB.
These single-run observations are not portable timing limits. In particular,
large validated JSON export remains expensive; Arrow is the preferred notebook
transport for that workload. Peak RSS includes imports, fixture construction,
and serialization, rather than measuring expression extraction alone.

The [self-contained notebook](https://github.com/genome-spy/genome-spy-python/blob/main/notebooks/scanpy_umap.ipynb)
demonstrates the native widget and its live Python connection. CI runs semantic
and browser checks with the pinned stack on Python 3.11, 3.12, and 3.13, and
renders the notebook through JupyterLab. Local validation used Python 3.11.

## API

```{eval-rst}
.. autofunction:: genome_spy.scanpy.pl.umap
```
