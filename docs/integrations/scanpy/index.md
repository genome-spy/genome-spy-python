# Scanpy integration

Keep your existing Scanpy analysis and replace supported plotting calls:

```python
import scanpy as sc
import genome_spy.integrations.scanpy as gsc

# Scanpy analysis: after your usual preprocessing, compute the embedding once.
sc.pp.neighbors(adata, random_state=0)
sc.tl.umap(adata, random_state=0)  # Writes adata.obsm["X_umap"].

# GenomeSpy plotting: reads those coordinates and returns an interactive chart.
chart = gsc.pl.umap(
    adata, color=["cell_type", "MS4A1"], vmax="p99",
    width=300, height=300, ncols=2,
    show=False, hover=True, zoom=True,
)
chart.save("umap.html", inline=True)
```

**Scanpy computes UMAP; GenomeSpy renders it.** If your workflow already has
`adata.obsm["X_umap"]`, go straight to `gsc.pl.umap`. The plotting adapter never
runs neighbors or UMAP analysis. A missing embedding produces an error asking
you to compute it explicitly first.

This development preview implements categorical/continuous 2D UMAP, plain dotplots
and matrixplots.
Full public Scanpy plotting coverage is the destination; the inventory below
records remaining work. Dendrograms and plot builders remain planned.

## Installation and version contract

```sh
pip install "genome-spy-python[scanpy]"
```

The integration currently supports **Scanpy 1.11.5 only**. Other versions raise
an actionable error at the plotting call. Importing either genome_spy or
genome_spy.integrations.scanpy does not import Scanpy, AnnData, NumPy, pandas, SciPy,
Matplotlib, or PyArrow. The scientific dependencies load when plotting.

The optional arrow extra speeds notebook transport. It is not required for
JSON or interactive HTML. The reproducible reference environment is the
scanpy-test dependency group and uv.lock; exact scientific-stack versions are
also recorded in the reference manifest.

## UMAP compatibility

The native function retains the effective Scanpy UMAP parameter names and
defaults, within the explicit native rendering boundaries below. A parameter
present in the signature can be reserved for later support: unsupported values
raise an error instead of being ignored.

| Parameters | Current behavior |
| --- | --- |
| color | None, one key, or multiple observation/gene keys. Each panel retains its original numeric measurements and supplied coordinates. |
| use_raw, layer, gene_symbols | raw.X by default if available; a layer overrides the automatic raw choice. Explicit use_raw=True plus a layer is an error. Symbol lookup follows UMAP's adata.var lookup before selected expression extraction. |
| palette, na_color, na_in_legend | Opaque CSS color sequences/mappings, GenomeSpy scheme names, stored CSS category colors, or Scanpy default palette values. Preserve categorical order and unused categories. Named schemes with missing values require na_in_legend=False; use an explicit CSS palette for an NA legend. |
| cmap, color_map, vmin, vmax | GenomeSpy scheme names (default viridis) and numeric or percentile bounds, including per-panel bounds. Conflicting aliases error. GenomeSpy maps the retained measurements and draws the numeric guide. Unsupported names such as coolwarm and Matplotlib colormap objects error. |
| sort_order | Scanpy's continuous sort, including reversed equal-value ties; missing points draw first. Categorical source order is retained apart from moving missing points behind other points. |
| size, s, marker | Scalar or observation-length sizes in points squared; dot and circle markers. Conversion accounts for marker path width, using a fixed 100/72 logical pixels per point. As in 1.11.5, an observation-size vector is carried in its reordered form between panels; reference tests cover this version-specific behavior. |
| mask_obs, groups | Recolor observations without dropping coordinates. Masks can be boolean arrays or an observation-column key. Groups and masks are mutually exclusive. |
| components, dimensions | One-based component pairs or zero-based dimension pairs; broadcasting follows Scanpy. Both cannot be supplied together. |
| frameon, title, ncols, hspace, wspace | Frame defaults to Scanpy's frame setting; panel layout uses explicit native defaults. Titles and guides remain per panel; guides are not automatically collected. |
| width, height (GenomeSpy additions) | Plot-area dimensions per panel in logical pixels. None uses 300 by 300 logical pixels. Explicit dimensions size each panel and its guide directly; axes and legends add space. Marker and font sizes are unchanged. |
| legend_loc, legend_fontsize, legend_fontweight | Centered right-margin legend, on-data median labels, or no legend; point font sizes use the fixed native conversion. On-data labels currently require legend_fontweight="normal" (or 400); the upstream bold default errors for that location because its glyph atlas is not bundled. |
| alpha, edgecolor/edgecolors, linewidth/linewidths | Scalar opacity and edge styling; conflicting aliases error. Matplotlib color shorthands, numeric RGB(A) tuples, cyclers, and per-entry alpha are rejected. Use opaque CSS names/hex and scalar alpha. |
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
functions, import Matplotlib directly, construct artists, or perform analysis. Scanpy itself
depends on Matplotlib; the plotting adapter does not call it. Charts contain
detached snapshots: later AnnData edits do not change an existing chart.

### Visual fidelity boundaries

The adapter retains source coordinates/domains, numeric color bounds, categorical
order and explicit palette values, point footprints, draw order, titles, axis
labels, and per-panel guide meaning. GenomeSpy owns numeric color mapping and
guide ticks. Its scheme interpolation can differ from Matplotlib's lookup-table
bins. Named categorical schemes also use native color ordering/sampling; use
explicit CSS colors when category colors must match exactly. There are no Python color-conversion utilities or hidden guide marks.

Native defaults use 300 by 300 logical pixels, fixed typography, and fixed
point-unit conversion. Matplotlib rcParams and style sheets do not affect the
result. Reference comparisons explicitly match known plot-area sizes and export
DPI rather than recreating Matplotlib's subplot layout in production.

The native runtime embeds **Lato Regular**, while the default reference font is
DejaVu Sans. This preview uses bundled Lato to make the default chart portable
offline. Font shape, text measurement, guide padding, and browser antialiasing
therefore differ from Matplotlib. Native panel edges round to backing pixels;
registered plot comparisons allow that rounding and renderer antialiasing.
This is not a claim of pixel-identical complete figures or support for arbitrary
Matplotlib rcParams/style sheets. Exact typography and per-entry transparent
guides need native runtime work; unsupported bold/outlined on-data styling errors
instead of fetching a remote font or silently changing the requested style.

## Dotplot compatibility

```python
pbmc = sc.datasets.pbmc68k_reduced()
chart = gsc.pl.dotplot(
    pbmc, {"B-cell": ["CD79A", "MS4A1"], "T-cell": ["CD3D"]},
    groupby="bulk_labels", show=False,
)
chart.display(inline=True, controls=False)
```

Dot color represents group mean expression and dot area represents the fraction
strictly above `expression_cutoff`. Only selected unique columns are read through
public `sc.get.obs_df`. Chart construction receives detached summary tables;
it does not read AnnData or call Scanpy plotting. No embedding, clustering,
ranking, palette write, or cached-result mutation occurs.

| Parameters | Current behavior |
| --- | --- |
| `var_names`, `groupby` | String/list/mapping features, repeated slots and labeled brackets; categorical, string, numeric-bin or multiple categorical string groups. Missing single-key groups are excluded. Unused categories error; remove them explicitly or pre-bin numeric data. Missing multi-key groups and joined-label collisions error. |
| `use_raw`, `layer`, `gene_symbols` | Scanpy public getter lookup, including raw symbol annotations. Raw is automatic when available, a layer overrides that default, explicit raw+layer conflicts error. Dense NumPy and CSR/CSC matrices and views work; backed/lazy expression and sparse arrays error before extraction. |
| `categories_order`, `num_categories` | Full category order and Scanpy numeric-bin edges. Repeated feature labels retain distinct slots. Ambiguous variable names error. |
| `log`, `expression_cutoff`, `mean_only_expressed` | `log1p` before comparison/aggregation; strict `>` threshold. Fractions use comparison/count denominators, including implicit zeros. Ordinary NaN compares false; nullable NA follows upstream count exclusion. Expressed-only means use their own denominator and fill empty means with zero. |
| `standard_scale`, `swap_axes` | Preserve 1.11.5's constructor scaling and second render-time scaling after optional transpose. Constant ranges become zero. |
| `dot_color_df` | Labeled authoritative table, aligned by group/feature. Repeated feature slots use its first matching column. No means are substituted. As upstream, supplied colors skip constructor scaling but receive render-time scaling. Missing/extra labels, duplicate group labels and nonnumeric values error. |
| `dot_min`, `dot_max`, `smallest_dot` | Clip fractions, normalize to the specified interval, raise to 1.5, then map area from `smallest_dot` to 200 points squared. Default upper limit rounds the observed maximum up to 0.1. Exact native area lookup also drives the percentage guide. Degenerate/inverted limits error; for all-zero fractions pass `dot_max=1` to retain invisible zero-area dots. |
| `cmap`, `vmin`, `vmax` | Native schemes (default `Reds` selects Vega `reds`) and finite numeric bounds. Constant bounds paint the first palette color; the guide expands by 10%, or ±0.1 at zero, matching Scanpy's precomputed dot colors. Missing values are omitted from painting without removing their slots; infinities and all-missing colors error. |
| `title`, `colorbar_title`, `size_title`, `var_group_*` | Native labels, bracket rules and size/color guides. Mapping features supply brackets directly. Scalar `linewidth` styles dot edges. |
| `width`, `height` | Plot-area logical pixels; defaults are 37 pixels per feature column and 35 per group row, exchanged with the axes. Labels and guides add space. |
| `hover` | Enabled by default. Tooltips show gene, group, displayed mean/color value and actual expressing-cell percentage, before dot-size clipping. Use `hover=False` to disable them. Scaled means and supplied color values are labeled explicitly. |
| `figsize` | Explicit native layout budget at 100 logical pixels/inch: subtract a fixed 150-pixel guide allowance from width; height sizes the plot area. Labels and renderer padding add space, so this does not fix the outer canvas dimensions. Conflicts with `width`/`height` error. |
| `show`, `save`, `ax`, `return_fig` | Same native return/display/export boundary as UMAP. No Axes dictionaries or fake builders. |
| `dendrogram`, `norm`, `vcenter`, other forwarded kwargs | Nondefault/reserved forms error. Tree attachment is M04; `DotPlot`, supplied `dot_size_df`, and builder styling are M13. Only scalar `linewidth` is accepted from scatter kwargs. |

Rows and columns use integer index-scale slots with padding that preserves the
initial Scanpy spacing. Repeated gene labels retain separate slots. Hover
describes group/feature summaries; these dots do not identify individual cells.
Brushes, cell selection and coordinate navigation remain deferred.

Native labels use portable Lato Regular and native guides. Line breaks in guide
titles become spaces; fractional percentage ticks retain native numeric precision
instead of Scanpy's integer label rounding. Guide sizing/padding and rotated text alignment
differ from Matplotlib. Vega `reds` has different stops from Matplotlib `Reds`,
including a darker low end; no Matplotlib colors are sampled or imported. Use
`cmap="viridis"` for the shared-palette reference comparisons. Browser tests
register plot areas at the recorded export DPI and check positions, sizes and
paint with renderer-specific tolerances; they do not claim identical full figures.

## Matrixplot compatibility

```python
chart = gsc.pl.matrixplot(
    pbmc, marker_genes, "bulk_labels", standard_scale="var",
    cmap="Blues", colorbar_title="column scaled\nexpression", show=False,
)
chart.display(inline=True, controls=False)
```

Each tile represents a group/feature mean. Matrixplot shares dotplot's selected
expression access, category/feature handling, native labels, brackets and sizing.
It uses its own tile chart and statistical path; expression fractions are not
computed. It performs no analysis or AnnData/cache writes.

| Parameters | Current behavior |
| --- | --- |
| `var_names`, `groupby`, `use_raw`, `layer`, `gene_symbols`, `num_categories`, `categories_order` | Same grouped access and storage limits as dotplot. Repeated feature slots remain distinct. Computed means require observed categories; unused categories error explicitly. |
| `log`, `standard_scale`, `swap_axes` | Apply log1p to selected observations, aggregate means, then min–max scale per gene (`"var"`) or group (`"group"`) once before an optional transpose. Constant ranges become zero. Matrixplot does not use dotplot's second scaling pass. |
| `values_df` | Authoritative real numeric table. Preserve supplied values and row/column order; only explicit `categories_order` reindexes its rows. `log` and `standard_scale` do not transform the supplied table. Require exactly the plotted groups and feature multiplicities, with unique group labels. Repeated supplied feature columns retain their own slot values. Missing/extra labels, unexpected duplicates, infinities and nonnumeric entries error. |
| `cmap`, `vmin`, `vmax` | Native scheme (default viridis) with finite numeric bounds and clipping. Constant bounds expand the guide by 10%, or ±0.1 at zero; tiles map against that expanded domain, unlike dotplot's frozen constant colors. Missing tiles are unpainted but retain their slots; all-missing values error. |
| `title`, `colorbar_title`, `var_group_*`, `width`, `height`, `figsize` | Shared native grouped layout and horizontal color guide. Index slots have no outer padding, so adjacent tiles fill the matrix. Default cells are 37 × 35 logical pixels, exchanged when axes swap. Frame width follows matrixplot's 1.5-point default. |
| `edgecolor`, `linewidth` in kwargs | Scalar opaque CSS edge color and nonnegative width in points; defaults are gray and 0.1. `edgecolor="none"` disables edges. Plural aliases error: Scanpy 1.11.5 overwrites those forwarded forms with its defaults; use the singular forms explicitly. Other pcolor kwargs error. |
| `hover` | Enabled by default; show gene, group and displayed mean/scaled mean or supplied value. `hover=False` disables picking without changing tile geometry. Summary tiles do not identify individual cells. |
| `show`, `save`, `ax`, `return_fig`, `dendrogram`, `norm`, `vcenter` | Same native delivery and unsupported-option boundary as dotplot. Trees are M04; the MatrixPlot builder and its styling methods are M13. Brushes and tile navigation remain deferred. |

Native palette interpolation, fonts and guide layout have the same documented
fidelity boundaries as dotplot. Complete-chart checks cover labels, brackets,
frame and guide placement; registered tile comparisons use 150 export DPI and
DPR 1.5. The production adapter never imports upstream plotting or Matplotlib.

## Interaction and native results

hover=True adds observation ID, original observation name, value/source, and
coordinate tooltips without changing the initial marks. hover=False disables
record hover. zoom=True enables coordinate navigation; it is off by default.
The selection argument supports an x/y interval brush, owned by the first panel,
with linked highlighting across panels showing the same dimension pair. Point
selection, initial brush values, and caller-supplied push scopes currently error.

obs_id selects an existing unique, nonmissing observation-column key. Without it,
unique obs_names supply IDs. Duplicate names receive distinct snapshot-local row
keys, preserving every observation even when coordinates repeat. Those local
keys are not cross-AnnData identity; supply explicit IDs when matching selections
back to an AnnData object that may have been reordered or sliced.

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

### Linked UMAP brushing

Use Scanpy’s packaged PBMC data, which already contains UMAP coordinates:

```python
import scanpy as sc
import genome_spy as gs
import genome_spy.integrations.scanpy as gsc

pbmc = sc.datasets.pbmc68k_reduced()
brush = gs.selection_interval("cells", encodings=["x", "y"], on="mousedown", zoom=False)
chart = gsc.pl.umap(
    pbmc, color=["louvain", "CD79A"], selection=brush,
    zoom=False, width=280, height=280, show=False,
)
view = chart.widget(parameter_names=[brush.name], inline=True, controls=False)
view
```

**Drag in the first panel without holding any keys.** Both panels highlight the
same observations and a native text mark below them shows the selected-cell
count. Double-click in the first panel to clear. Navigation is disabled in this
example so ordinary dragging always brushes. The second panel displays the
selection but does not start a brush.

The count and highlighting run entirely in GenomeSpy, including in exported
interactive HTML. An empty rectangle reports zero selected cells while retaining
the initial point appearance. Unselected fills and outlines dim to 20% of their
original opacity. Per-entry transparency requires an explicit scalar `alpha`
when brushing. All panels must use the same dimension pair; their color scales,
palettes, guides, and draw orders remain independent.

The existing JupyterChart synchronizes the named parameter through
`parameter_values`. After brushing, run an ordinary Python cell:

```python
mask = gsc.selection_mask(pbmc, view.parameter_values.get(brush.name))
selected_ids = pbmc.obs_names[mask]
selected_adata = pbmc[mask].copy()
```

No asynchronous setup, callback registration, or separate widget controls are
needed. Rerun the retrieval cell after changing the brush to refresh the subset.
Only interval bounds cross to Python; expression data is copied only when you
explicitly request the AnnData subset. Python retrieval requires a live kernel.

`selection_mask` reads the unchanged plotted embedding and returns membership in
the supplied AnnData's current row order, preserving distinct coincident rows.
It uses the same lower-inclusive, upper-exclusive bounds as highlighting and the
native count. It supports reordered/sliced observations that retain their
coordinates. Do not recompute or edit UMAP between plotting and retrieval.
Pass `dimensions=(i, j)` if you plotted a nondefault component pair.

The linked-brushing section of the
{download}`UMAP notebook <../../../integrations/scanpy/notebooks/scanpy_umap.ipynb>`
uses this normal widget path. For navigation and brushing together, use
`zoom=True` and the default interval gesture: Shift-drag brushes, ordinary
dragging pans. Custom `on`, `clear`, and brush-zoom settings follow the native
interval parameter. Command-drag is not the default brush gesture.

### Examples adapted from Scanpy tutorials

The examples load `sc.datasets.pbmc68k_reduced()` through Scanpy's public API:
700 real PBMC observations, 765 genes, annotations, and stored UMAP coordinates.
The plotting adapter does not recompute the embedding or differential expression.
No dataset copy is vendored here.

Two notebooks run independently:

- {download}`UMAP <../../../integrations/scanpy/notebooks/scanpy_umap.ipynb>`:
  basic categorical/continuous UMAP, linked brushing/count/Python retrieval, then
  customization with subsets, titles/frames, categorical order/palettes, an
  explicit Scanpy gene score and the eight-panel marker overview.
- {download}`Expression plots <../../../integrations/scanpy/notebooks/scanpy_expression.ipynb>`:
  marker dotplot and per-gene scaled matrixplot on `bulk_labels`, with summary
  hover. Heatmap examples will extend this workflow when implemented.

These adapt supported UMAP, dotplot and matrixplot sections of Scanpy's
[core](https://scanpy.scverse.org/en/stable/tutorials/plotting/core.html) and
[advanced](https://scanpy.scverse.org/en/stable/tutorials/plotting/advanced.html)
plotting tutorials. The next tutorial coverage is Python-computed dendrograms,
then heatmaps and ranked-gene variants. The
remaining tutorial plots and Matplotlib artist styling are not implemented yet.

### Native plot sizing

Set panel dimensions through GenomeSpy without importing or configuring
Matplotlib:

```python
chart = gsc.pl.umap(
    adata, color=["cell_type", "MS4A1"],
    width=300, height=300, ncols=2, show=False,
)
```

`width` and `height` are keyword-only GenomeSpy controls in logical pixels, not
figure inches or marker areas. They apply to each plot area; titles, axes,
spacing, and legends take additional space. Numeric guides use the requested
height. An omitted dimension retains its Scanpy-compatible default, and plotting
does not change global settings. Use `ncols` to arrange the panels, `wspace` and
`hspace` for relative gaps, and `size` for marker area.

For a multi-panel result, setting dimensions on the outer composition with
`.properties()` does not resize its fixed child panels. Pass `width`/`height`
at the plotting call to size the panels and guides together.

## Full plotting coverage inventory

The tracked API snapshot contains 50 public callables, including aliases,
three builders, and two rcParams helpers. It records callable targets so aliases
remain visible. Function coverage and parameter coverage are separate.

| Delivery | Public entries |
| --- | --- |
| Available as partial previews | umap, dotplot, matrixplot |
| Trees and correlation | dendrogram, correlation_matrix |
| Cell heatmaps and ranked summaries | heatmap, matrix, rank_genes_groups_dotplot, rank_genes_groups_matrixplot, rank_genes_groups_heatmap |
| Other embeddings and PCA | scatter, embedding, tsne, pca, pca_scatter, diffmap, draw_graph, pca_loadings, pca_overview, pca_variance_ratio |
| Distributions and tracks | violin, stacked_violin, tracksplot, rank_genes_groups_violin, rank_genes_groups_stacked_violin, rank_genes_groups_tracksplot |
| Diagnostics, ranking, matrices, simulation | clustermap, rank_genes_groups, ranking, highest_expr_genes, highly_variable_genes, filter_genes_dispersion, scrublet_score_distribution, sim |
| Trajectories and graphs | dpt_groups_pseudotime, dpt_timeseries, paga, paga_adjacency, paga_compare, paga_path, timeseries, timeseries_as_heatmap, timeseries_subplot |
| Spatial and density | spatial, embedding_density |
| Plot builders and useful semantic methods | DotPlot, MatrixPlot, StackedViolin |
| Settings helpers retained in Scanpy | set_rcParams_defaults, set_rcParams_scanpy |

All entries except the UMAP/dotplot/matrixplot previews and settings helpers remain required future integration
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
uv run --no-sync python -m tests.integrations.scanpy.generate_references
uv run --no-sync pytest tests/integrations/scanpy --ignore=tests/integrations/scanpy/browser
uv run --no-sync python -m playwright install chromium
uv run --no-sync pytest tests/integrations/scanpy/browser
```

Reference generation is explicit and separate from ordinary tests and runtime.
It renders Scanpy figures and records their observed geometry, colors, and
ordering; independent tests also check hand-calculated values, source identities,
sparse allocation, and mutation behavior. PNG checksums, export/display DPI, and
versions are retained under tests/integrations/scanpy/fixtures. Browser tests measure actual
marker footprints, retain registered overlays and complete-chart captures, and
exercise hover, navigation, and offline delivery.

### Resource baseline

The explicit benchmark is reproducible without local research directories:

```sh
uv run --no-sync python -m tests.integrations.scanpy.benchmark --cells 100000 --panels 8 --output /tmp/umap-memory.json
uv run --no-sync python -m tests.integrations.scanpy.benchmark --cells 10000 --panels 8 --browser --output /tmp/umap-browser.json
```

The tracked performance-baseline.json records versions, source dimensions,
payloads, hardware, viewport, DPI/DPR, and timing definitions. On an Apple M5
with 32 GiB RAM, the seeded 100,000-cell × 20,000-gene sparse fixture used about
16.4 MB for expression; its dense float32 equivalent would use 8 GB. Preparation
read one selected gene column for one panel and four unique columns for eight
panels. No full matrix was densified. The table below records the October 17
native renderer at 300 by 300 logical pixels per panel; the tracked manifest also
retains the previous renderer's October 16 measurements as historical evidence.

| Workload | Chart preparation | Arrow transport preparation | Validated JSON export | Arrow / JSON payload | Peak Python RSS |
| --- | --- | --- | --- | --- | --- |
| 100,000 cells, 1 panel | 0.01 s | 0.25 s | 1.33 s | 6.0 / 20.3 MB | 591 MB |
| 100,000 cells, 8 panels | 0.09 s | 1.13 s | 25.25 s | 23.3 / 78.5 MB | 1.20 GB |

In Chromium 156, a separate 10,000-cell eight-panel WebGL run at 2800 × 1800,
DPR 1, took 5.35 seconds to first paint including spec dispatch. All 16 known-ID
hover probes succeeded; median/p95 observed response was 79/118 ms after native
tooltip dwell, including the one-pixel pointer approach and assertion. A wheel
event changed the coordinate domain in 203 ms. Browser JS heap was 104 MB.
These single-run observations are not portable timing limits. In particular,
large validated JSON export remains expensive; Arrow is the preferred notebook
transport for that workload. Peak RSS includes imports, fixture construction,
and serialization, rather than measuring expression extraction alone.

The {download}`self-contained UMAP notebook <../../../integrations/scanpy/notebooks/scanpy_umap.ipynb>`
demonstrates the native widget and its live Python connection. CI runs semantic
and browser checks with the pinned stack on Python 3.11, 3.12, and 3.13, and
renders both workflow notebooks through JupyterLab. Local validation used Python 3.11.

## API

```{eval-rst}
.. autofunction:: genome_spy.integrations.scanpy.pl.umap

.. autofunction:: genome_spy.integrations.scanpy.pl.dotplot

.. autofunction:: genome_spy.integrations.scanpy.pl.matrixplot

.. autofunction:: genome_spy.integrations.scanpy.selection_mask
```
