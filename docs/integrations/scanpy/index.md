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
and matrixplots, individual-cell heatmaps, supplied numeric matrices, standalone dendrograms and correlation matrices.
Full public Scanpy plotting coverage is the destination; the inventory below
records remaining work. Native plot builders remain planned.

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

## Reusing Scanpy computations

The integration reuses public data access and computation methods where their
semantics match the plot:

| Plot | Reused methods/results | Native preparation retained |
| --- | --- | --- |
| UMAP | Existing `obsm` coordinates; public AnnData `obs_vector`/`raw.obs_vector`; Scanpy's public palette lists | Masks, draw order, component selection, stable IDs and native color/size/guide mapping. No embedding computation. |
| Dotplot | Public `sc.get.obs_df`, including selected raw/layer/symbol lookup; AnnData categorization on the detached table | Shared pandas means, strict-cutoff fractions and plotting min–max scaling. Native marks and guides use those results. |
| Matrixplot | The same getter, categorization and shared grouped means/scaling; supplied `values_df` remains authoritative | Plot ordering, repeated slots and native tile/guide mapping. No expression-fraction computation. |
| Heatmap | The same getter, categorization, min–max operation, native palettes, marker ordering and tree branches | Cell values and original row positions, category spans and shared annotation alignment. No group means or downsampling. |
| Dendrograms | Stored `sc.tl.dendrogram` results, or that public method for a missing tree | Structural checks, shared leaf permutations and native branch rendering. |

Scanpy 1.11.5 has no public standalone dotplot/matrixplot preparation method.
Their calculations live in the Matplotlib plotting classes; their common private
preparer also sanitizes the caller's AnnData. The adapter uses the documented
[`sc.get.obs_df` plus pandas grouping recipe](https://scanpy.readthedocs.io/en/1.11.x/generated/scanpy.get.obs_df.html)
without constructing those classes or calling private plotting helpers.

`sc.get.aggregate` is not equivalent to these plots: its means propagate NaN,
while the plotting means skip it. Its `count_nonzero` also counts negatives and
values below `expression_cutoff`. Likewise, `sc.pp.scale` computes z-scores,
whereas plotting's `standard_scale` is min–max scaling. Retain the small shared
pandas/NumPy operations rather than adding conversions or changing statistics.
Plot `log=True` applies NumPy `log1p` to the selected table, just as Scanpy's
grouped plotting preparer does; it does not preprocess or mutate AnnData.

UMAP uses AnnData vector access, as Scanpy's embedding code does. Forcing it
through `sc.get.obs_df` would change raw-symbol lookup and reject unrelated
duplicate variable labels, even for coordinate-only requests. Native color
mapping also avoids Scanpy's private Matplotlib color/palette mutation helpers.

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
| `zoom`, `highlight` | Both default False. Wheel zoom/drag panning retain aligned labels and tree branches; hovering a dot shades its row and column when highlighting is enabled. Dot sizes and both guides keep their original mapping. Repeated labels retain separate integer slots. |
| `hover` | Enabled by default. Tooltips show gene, group, displayed mean/color value and actual expressing-cell percentage, before dot-size clipping. Use `hover=False` to disable them. Scaled means and supplied color values are labeled explicitly. |
| `figsize` | Explicit native layout budget at 100 logical pixels/inch: subtract a fixed 150-pixel guide allowance from width; height sizes the plot area. Labels and renderer padding add space, so this does not fix the outer canvas dimensions. Conflicts with `width`/`height` error. |
| `show`, `save`, `ax`, `return_fig` | Same native return/display/export boundary as UMAP. No Axes dictionaries or fake builders. |
| `dendrogram`, `norm`, `vcenter`, other forwarded kwargs | Trees accept True or a stored key; see the tree contract below. Nondefault norm/vcenter and other kwargs error; `DotPlot`, supplied `dot_size_df`, and builder styling are M13. Only scalar `linewidth` is accepted from scatter kwargs. |

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
| `zoom`, `show_values` | Both default False. Enable aligned wheel zoom/drag panning and fitted two-decimal plotted values; see [shared grid interactions](#shared-grid-interactions). |
| `hover` | Enabled by default; show gene, group and displayed mean/scaled mean or supplied value. `hover=False` disables picking without changing tile geometry. Summary tiles do not identify individual cells. |
| `show`, `save`, `ax`, `return_fig`, `dendrogram`, `norm`, `vcenter` | Same native delivery boundary as dotplot. Trees accept True or a stored key; norm/vcenter error. The MatrixPlot builder and its styling methods are M13. Brushes and tile navigation remain deferred. |

Native palette interpolation, fonts and guide layout have the same documented
fidelity boundaries as dotplot. Complete-chart checks cover labels, brackets,
frame and guide placement; registered tile comparisons use 150 export DPI and
DPR 1.5. The production adapter never imports upstream plotting or Matplotlib.

## Shared grid interactions

Grid interactions are optional additions to the Scanpy signatures:

```python
heatmap = gsc.pl.heatmap(pbmc, markers, "bulk_labels", zoom=True, show_values=True, show=False)
matrixplot = gsc.pl.matrixplot(pbmc, markers, "bulk_labels", zoom=True, show_values=True, show=False)
matrix = gsc.pl.matrix(values, zoom=True, show_values=True, show=False)
dotplot = gsc.pl.dotplot(pbmc, markers, "bulk_labels", zoom=True, highlight=True, show=False)
```

Use the mouse wheel inside the plot to zoom both axes and drag to pan. Native
axis-margin gestures can zoom one axis. Row/column labels and dendrograms follow
the visible slots; outside labels and partially visible gene brackets are hidden.
Heatmap category strips and boundaries follow individual cells. Defaults remain
`zoom=False`, `show_values=False` and `highlight=False`.

`show_values` uses native `fitToBand` text, shared tile records and the plotted
value after any log transform/scaling. Values fade in as cells become large
enough and show two decimals; tooltips retain more precision. Missing cells have
no text. Black/white contrast uses the native palette sampled at 256 bins,
clamped color bounds and tile opacity over white. Sampling runs in GenomeSpy;
there is no Python colormap implementation.

`highlight` shades the hovered dot's row and column and clears on leaving the dot.
It works independently of `hover`; no brush or individual-cell selection is
implied by grouped summaries. Integer slots preserve repeated gene labels.
Zooming changes positions while keeping the dot percentage-to-area mapping,
color limits and guides fixed. These interactions run in the browser and never
read AnnData again or rerun Scanpy analysis. Notebook widgets and standalone HTML
use the same native specifications.

## Heatmap compatibility

```python
heatmap = gsc.pl.heatmap(
    pbmc, marker_genes, "bulk_labels", dendrogram=True,
    standard_scale="var", cmap="viridis", width=400, height=450, zoom=True, show=False,
)
heatmap.display(inline=True, controls=False)
```

Each tile represents one cell and one requested gene. Heatmap shares the grouped
getter, source/storage checks, palettes, scaling, labels, marker ordering and
native tree renderer. Preparation keeps one explicit cell permutation; values,
IDs, category strips, group boundaries and branches follow it. Scanpy's category
sorting includes its within-group tie order. The adapter never substitutes group
means or changes AnnData.

| Parameters | Current behavior |
| --- | --- |
| `var_names`, `groupby`, `use_raw`, `layer`, `gene_symbols`, `num_categories` | Grouped access rules and resident NumPy/CSR/CSC storage limits apply. Repeated gene slots and views are supported. Missing group labels and unused categories fail explicitly; single-group data retains cell order without a category strip or tree. |
| `log`, `standard_scale` | Apply log1p before min–max scaling of individual cell values: `"var"` scales each gene across cells; `"obs"` scales each cell across requested genes. Constant ranges become zero. These are not matrixplot's scaled group means. |
| `dendrogram` | False, True or a stored-result key. Reuse Scanpy's stored result or the guarded public computation. Heatmap supports two-group trees. Interpolate branches to unequal cell-group spans, retaining Scanpy's half-row strip-label/leaf placement. Matching marker blocks follow tree order too. |
| `swap_axes`, `show_gene_labels`, `var_group_*` | Ordinary heatmaps use gene brackets above the matrix; swapped heatmaps use a colored gene-group strip on the right, as Scanpy does. Show gene labels by default for at most 50 slots. `var_group_rotation` affects ordinary brackets. |
| `cmap`, `vmin`, `vmax`, `alpha`, `interpolation` | Native scheme (default viridis), numeric bounds, scalar opacity and nearest-neighbor tiles. Missing values keep their positions but are unpainted; all-missing colors error. Other interpolation, norm/vcenter, Matplotlib colormaps and unsupported imshow kwargs error by name. |
| Category colors | Reuse saved AnnData colors or the shared Scanpy default palettes without writing them back. Numeric and multi-key strips use native category20, currently limited to 20 groups. |
| `width`, `height`, `figsize` | Width/height control the tile area in logical pixels. Defaults follow Scanpy's gene-label size rules; figsize uses 100 pixels per inch with space reserved for strips/trees. Native text and outer layout differ from Matplotlib. The vertical color guide uses at most 400 pixels. |
| `zoom` | Defaults False. True enables wheel zoom and drag panning on both index axes. Strips, group boundaries, tree leaves and gene labels follow the visible cells/genes. Clip branches and strips at the plot extent; hide offscreen labels and gene brackets whose whole span is not visible. |
| `show_values` | Default False. Reveal the plotted cell values to two decimals when the tiles have enough room; missing cells remain empty. |
| `hover`, delivery | Default hover shows original cell ID/name, gene, group and displayed expression. Duplicate names use stable original-row IDs. Brushing is not offered. Existing show/save/native-return rules apply; Matplotlib axes and figure-return options error. |

This preview accepts **at most 250,000 cell–gene values**, counting repeated
slots. Larger requests fail before expression extraction and ask for an explicit
subset. No rows or columns are sampled, aggregated or silently truncated. The
selected-column getter materializes only requested genes; disk-backed/lazy
expression and sparse arrays remain explicit upstream access limits.

The retained resource observation uses 5,000 cells × 50 markers from a 20,000-gene
sparse matrix. Preparation peaked at 114 MB tracked Python allocations; the
250,000-tile JSON was 26.2 MB, browser first paint including dispatch took 16.2 s,
hover after a pointer pause took 96 ms and JS heap was 168 MB. These are local
Chromium observations, not portable limits. The 100,000-cell × 50-marker case
verifies early rejection without expression reads. Larger transport/chunking
work remains in M05.d.

Sixteen frozen Scanpy 1.11.5 figures retain complete labels/guides and registered
tile/tree references at 100 display / 150 export DPI. Native checks at DPR 1.5
allow 12/255 RGB paint differences for palette bins and browser rasterization;
they preserve positions, group spans and branch paths without fitting images.
Lato typography, native guide ticks and outer spacing are renderer differences.

## Supplied matrix compatibility

```python
chart = gsc.pl.matrix(
    values, xticks=genes, yticks=groups, xlabel="Genes", ylabel="Groups",
    title="Supplied values", color_map="viridis", show=False,
)
chart.display(inline=True, controls=False)
```

`matrix` displays the given resident 2D numeric NumPy/masked array, nested sequence
or DataFrame directly. It does not access AnnData, aggregate values, reorder axes,
or compute linkage. DataFrame index/column labels are used only when supplied as
`yticks`/`xticks`, matching Scanpy's array conversion. Explicit tick labels must
match the axis length; repeated names retain separate index slots.

Colors use linear normalization over finite values, including negative values.
Missing/masked entries stay blank; constant limits expand by 10% (or ±0.1 at
zero), matching Scanpy's colorbar normalization. All-missing or infinite values
fail clearly. `color_map=None` uses native viridis; native scheme names work,
while Matplotlib colormap/image/axes objects, sparse/lazy sources and RGB images
are unsupported. Unknown options fail rather than being ignored.

`colorbar_shrink=0.5` sets the vertical guide length relative to the native tile
area height. Default square cells fit inside a 400 × 400-pixel area; `width` and
`height` explicitly size that area. Native fonts, automatic numeric tick density,
outer layout and colorbar allocation differ from Matplotlib's figure layout.
Titles and axis labels are supported. Default hover shows row, column and value;
`hover=False` disables it. Existing `show`/`save` and native return/export rules
apply. Optional `zoom=True` enables x/y wheel zoom and drag panning, with aligned tick labels. `show_values=True` adds fitted two-decimal values. Nonlinear normalization is unsupported.

Eight frozen Scanpy figures retain values, color bounds, labels, complete charts
and registered crops at 100 display / 150 export DPI. Native DPR 1.5 checks cover
tile footprints, missing paint and palette-bin differences; separate checks
exercise hover after resizing and offline HTML delivery. A resident 200 × 1,000
float32 resource check retained all 200,000 values: warm preparation took 0.14 s,
default formatted/validated JSON was 28.1 MB and took 12.0 s with allocation tracing, and tracked peak
allocation including serialization was 344 MB. Browser first paint including
dispatch took 10.3 s; paused hover was 113 ms. These local observations expose
the current serialization cost; larger/chunked transport remains M05.d.

## Dendrograms and correlation matrices

Compute a tree explicitly in Python and reuse it across plots:

```python
sc.tl.dendrogram(pbmc, "bulk_labels")  # Uses the packaged X_pca representation.

dots = gsc.pl.dotplot(pbmc, marker_genes, "bulk_labels", dendrogram=True, show=False)
tiles = gsc.pl.matrixplot(pbmc, marker_genes, "bulk_labels", dendrogram=True, show=False)
tree = gsc.pl.dendrogram(pbmc, "bulk_labels", orientation="left", show=False)
correlations = gsc.pl.correlation_matrix(
    pbmc, "bulk_labels", show_correlation_numbers=True, show=False,
)
```

All computations run in Python. GenomeSpy renders supplied branch coordinates
with native rules; it does not calculate profiles, correlations or linkage.
A missing tree delegates to the public `sc.tl.dendrogram(..., inplace=False)`.
Scanpy computes group means, Pearson correlations, `1 - correlation` distances,
complete linkage and branch coordinates; the adapter does not implement these
computations. No result is written to `adata.uns` by plotting. For different
representations, components or methods, call `sc.tl.dendrogram` explicitly first.

Default profiles use resident `X` when `n_vars <= sc.settings.N_PCS`, otherwise
existing `obsm["X_pca"]`. Tree profiles do not use the selected marker genes,
`raw`, `layer`, plot `log`, or summary scaling. Missing PCA produces an error
asking for explicit preparation; no plotting function fits PCA, UMAP or gene
rankings. Automatic computation requires resident dense X or X_pca because of
Scanpy 1.11.5's input limits. It rejects sparse/backed/lazy computation clearly,
without densifying expression. Existing trees can be rendered with sparse or
backed data because reading a stored tree does not access X or its representation.

Stored trees are treated as Scanpy snapshots. The adapter checks their structure,
group labels, array shapes and finite values, then copies their correlations,
leaf order and branch coordinates. It does not recompute profiles, correlations,
linkage or layout to verify an existing result. Custom Scanpy computations such
as `n_pcs`, `var_names`, correlation/linkage methods and optimal ordering are
honored as stored. Reordered categories are aligned by labels. Malformed or
incompatible results fail without overwrite. As in Scanpy, recompute the tree
explicitly after changing the underlying data or group membership; the adapter
does not infer staleness from expression values.

| Surface | Current behavior |
| --- | --- |
| Grouped `dendrogram` | False retains the original plot; True uses `uns["dendrogram_<groupby>"]`, and a string selects another key. Missing results delegate to Scanpy. Tree order overrides explicit `categories_order`, as in Scanpy. Dotplot/matrixplot warn and omit attachments with at most two groups; heatmap supports two-group attachments. |
| Category and feature order | Carry the same leaf permutation through means, fractions, supplied tables and labels. When marker-block labels match the group categories, reorder their feature slots and brackets too; otherwise retain marker order. Multiple categorical string keys use Scanpy's lexically ordered joined tree groups. |
| Standalone `dendrogram` | All four orientations and `remove_labels`, including a two-group tree. At least two observed categories are required. Unused categories, ambiguous joined/string labels, and undefined constant/missing profiles error explicitly. Native width/height default to 300 × 300 logical pixels. |
| `correlation_matrix` | Cached or locally computed group correlations. None/True draws a left tree and orders both axes by leaves; a string selects the cache. False keeps current category order without drawing a tree. Optional two-decimal numbers and default summary hover are native marks. |
| Correlation colors/style | Default native redblue with reversed scheme extent gives blue negatives and red positives; the guide increases from -1 to 1. Native cmap names, scalar edgecolors and linewidth are supported kwargs. Other kwargs, norm/vcenter and Matplotlib colormaps error. Native interpolation differs from Scanpy's default bwr. |
| Correlation size/delivery | Default tile area is 60 pixels per group in each direction; width/height override it. Figsize uses a 100-pixels/inch budget, subtracting 180 pixels for a tree and 20 for the guide. Labels and padding add space. Existing show/save/native-return rules apply; ax is omitted. |

Dotplot/matrixplot trees reserve an 80-pixel branch region; heatmaps use 100 pixels
on the right or 80 above, and correlation trees use 180.
Zero-distance leaves meet the matrix edge without a gap or distance-axis padding.
Native dataflow projections follow the plot dimensions and fixed index-slot
padding. Optional grouped navigation uses the same live index projection for
branches and row/column labels. Summary hover remains available. Distances,
leaf positions and guide/label clearance are checked against frozen complete
Scanpy figures, including swapped axes and different plot sizes. These are native
font/layout comparisons, not a claim of identical Matplotlib outer figures.

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
  marker dotplot, per-gene scaled matrixplot, zoomable individual-cell heatmap and supplied matrix on
  `bulk_labels`, with aligned dendrograms and value hover.

These adapt supported UMAP, dotplot, matrixplot and heatmap sections of Scanpy's
[core](https://scanpy.scverse.org/en/stable/tutorials/plotting/core.html) and
[advanced](https://scanpy.scverse.org/en/stable/tutorials/plotting/advanced.html)
plotting tutorials. All expression examples reuse a tree explicitly computed in
Python with `sc.tl.dendrogram`. Clustermap is next; ranked-gene variants follow it. The
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
| Available as partial previews | umap, dotplot, matrixplot, heatmap, matrix, dendrogram, correlation_matrix |
| Ranked summaries | rank_genes_groups_dotplot, rank_genes_groups_matrixplot, rank_genes_groups_heatmap |
| Other embeddings and PCA | scatter, embedding, tsne, pca, pca_scatter, diffmap, draw_graph, pca_loadings, pca_overview, pca_variance_ratio |
| Distributions and tracks | violin, stacked_violin, tracksplot, rank_genes_groups_violin, rank_genes_groups_stacked_violin, rank_genes_groups_tracksplot |
| Diagnostics, ranking, matrices, simulation | clustermap, rank_genes_groups, ranking, highest_expr_genes, highly_variable_genes, filter_genes_dispersion, scrublet_score_distribution, sim |
| Trajectories and graphs | dpt_groups_pseudotime, dpt_timeseries, paga, paga_adjacency, paga_compare, paga_path, timeseries, timeseries_as_heatmap, timeseries_subplot |
| Spatial and density | spatial, embedding_density |
| Plot builders and useful semantic methods | DotPlot, MatrixPlot, StackedViolin |
| Settings helpers retained in Scanpy | set_rcParams_defaults, set_rcParams_scanpy |

All entries except the seven plotting previews and settings helpers remain required future integration
work. Settings remain owned by Scanpy. The external.pl namespace is separate
from this core inventory.

Dendrograms belong with grouped-plot coverage. Read stored Scanpy results or
delegate missing computation to `sc.tl.dendrogram`, then render native rule
marks. A dedicated tree mark is unnecessary. This does
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

Refreshing the frozen numerical/API metadata is explicit and separate from tests
and runtime. Browser tests use the pinned generators to render reference images
in pytest's temporary directory without changing that metadata. Generated PNGs,
screenshots and overlays are never committed or pushed. Explicit refresh commands
write images to ignored `tmp/scanpy-references/<family>/`; checksums, dimensions,
DPI and version metadata remain under `tests/integrations/scanpy/fixtures`.
Independent tests check hand-calculated values, source identities, sparse
allocation and mutation behavior. Browser checks measure actual marker footprints,
retain temporary registered overlays and complete-chart captures, and exercise
hover, navigation and offline delivery.

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

.. autofunction:: genome_spy.integrations.scanpy.pl.matrix

.. autofunction:: genome_spy.integrations.scanpy.pl.matrixplot

.. autofunction:: genome_spy.integrations.scanpy.pl.dendrogram

.. autofunction:: genome_spy.integrations.scanpy.pl.correlation_matrix

.. autofunction:: genome_spy.integrations.scanpy.selection_mask
```
