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

This development preview implements shared categorical/continuous 2D embeddings
(UMAP, t-SNE, diffusion maps, saved graph layouts, PCA and custom bases), cell/gene scatter plots, plain dotplots
and matrixplots, individual-cell heatmaps, supplied numeric matrices, clustermaps,
standalone dendrograms, correlation matrices, stored rank/score panels and ranked
dotplot/matrixplot/heatmap wrappers.
Full public Scanpy plotting coverage is the destination; the inventory below
records remaining work. Stored PCA loadings and variance ratios share the ranking panels;
PCA overview composes these with the existing embedding chart. Native
plot builders remain planned.

## Shared 2D embeddings

UMAP, t-SNE, diffusion maps, saved graph layouts and PCA use the same preparation,
point rendering and native interactions. Generic `embedding` reads any stored
`obsm` basis. Named wrappers expose the same shared keyword defaults as Scanpy;
`pca_scatter` is an alias of `pca`.

```python
pca = gsc.pl.pca(
    pbmc, color=["louvain", "CD79A"], annotate_var_explained=True,
    width=280, height=280, zoom=True, show=False,
)
custom = gsc.pl.embedding(pbmc, "pca", dimensions=(1, 2), show=False)

sc.tl.tsne(pbmc, use_rep="X_pca", random_state=0, n_jobs=1)  # Explicit analysis.
tsne = gsc.pl.tsne(pbmc, color="louvain", zoom=True, show=False)
```

A basis resolves its exact `obsm` name first, then `X_<basis>`. Components use
Scanpy's one-based strings; `dimensions` uses zero-based pairs. Supplied columns,
precision, observation IDs, masks, color order and raw/layer lookup share the UMAP
path. No coordinates, neighbors or PCA metadata are fitted by plotting.

`diffmap` preserves pinned Scanpy 1.11.5's first-two-column default (`DC1`, `DC2`);
use `components="2,3"` explicitly for other columns. `draw_graph(layout=None)`
reads `uns["draw_graph"]["params"]["layout"]`; an explicit layout selects its
stored `X_draw_graph_<layout>` coordinates. Missing coordinates or metadata error.
PCA's optional variance labels read `uns["pca"]["variance_ratio"]` for the displayed
components and appear consistently in axes and hover. For Python brush retrieval,
use the same basis and pair: `gsc.selection_mask(adata, snapshot, basis="pca",
dimensions=(0, 1))`. The default remains UMAP.

The supported controls and visual limits below apply to all these embeddings.
3D, other graph forms/arrows and remaining marker/normalization options stay in M07.d/M14.
The UMAP notebook now includes packaged PCA and explicitly prepared t-SNE examples.

## Stored embedding density

Compute density explicitly with Scanpy on an existing embedding, then plot its
stored result. Plotting never runs KDE, recomputes coordinates, reads expression
or adds temporary observation columns.

```python
sc.tl.embedding_density(pbmc, basis="umap", groupby="phase")
density = gsc.pl.embedding_density(
    pbmc, groupby="phase", bg_dotsize=8, fg_dotsize=20,
    width=150, height=240, wspace=0.05, zoom=True, show=False,
)
density.display(inline=True, controls=False)
```

The adapter reuses the embedding coordinate, identity, size, color-bound,
point-rendering and interaction helpers. Its small preparation module only
resolves density-specific stored metadata and foreground/background groups.

| Parameters | Current behavior |
| --- | --- |
| `basis`, `key`, `groupby` | Basis is lowercased; `fa` selects `draw_graph_fa`. Pinned Scanpy 1.11.5 always defaults to `umap_density`, even for another basis; groupby appends its suffix. Pass key or groupby, not both. Require matching obs values and uns key_params. |
| Coordinates | Require the named X_ embedding, then retain the shared direct-name-before-X_ lookup used by Scanpy plotting. The two one-based stored components are authoritative. components/dimensions kwargs reject rather than overriding them. |
| `group` | All stored categorical levels by default, including unused categories; select one string or a list/tuple in supplied order, including repeats. None requires an ungrouped result. Explicit groups for an ungrouped result error rather than being silently ignored. Numeric categories are outside this preview. |
| `bg_dotsize`, `fg_dotsize` | Original defaults 80 and 180 squared points; finite nonnegative scalars. A zero size hides that point. Smaller values in the notebook are explicit customization. |
| `color_map`, bounds | YlOrRd selects the native yelloworangered scheme, whose stops differ from Matplotlib. Other supported GenomeSpy scheme names work; colormap objects and unsupported names error. Default bounds remain 0–1. Shared numeric/percentile/callable bounds and vcenter retain the background sentinel in their inputs, as Scanpy does. |
| Under/over colors and order | Native filtered point layers paint lightgray below the lower bound, the continuous scheme within the bounds, and black above the upper bound. They share data, styling and the prepared sort. sort_order=False errors when values span multiple color ranges, because layering would change overlaps; it works within one range. |
| Style | Shared frame, one supported marker (including a one-element list), scalar alpha/edge/linewidth styles, four colorbar sides/None, titles, ncols, hspace and wspace. norm objects, multiple markers and unknown kwargs reject clearly. |
| Native delivery | hover=True reports stable cell ID, original stored density and coordinates, including for background cells. zoom=False by default; True links x/y navigation. Width/height default to 300 pixels per panel. show/save follow the common native contract; no ax/return_fig or Matplotlib objects. |

Stored densities must be finite numeric values in [0, 1], with a categorical
covariate and valid stored component pair. Views and backed AnnData work when
their observation metadata and embedding are resident. Results are detached
snapshots; callers must explicitly recompute density after changing its analysis
inputs. Missing or malformed results never trigger automatic analysis.

Complete reference comparisons use viridis to separate geometry, bounds and draw
order from differing native palette stops. The default native palette and its
under/over colors are checked separately. Fonts, outer layout and guide tick
spacing retain the shared native rendering boundary.

## PCA loadings

`pca_loadings` reads stored `varm["PCs"]` and `var_names`. It reuses the same
preparation and native text panels as `ranking`, just as Scanpy delegates this
plot to its ranking function. No PCA, expression access or source mutation runs.

```python
# This packaged dataset stores loadings only for its highly variable genes.
pca_genes = pbmc[:, pbmc.var["highly_variable"]]
loadings = gsc.pl.pca_loadings(
    pca_genes, components="1,2", n_points=20,
    width=280, height=280, show=False,
)
loadings.display(inline=True, controls=False)
```

Components are one-based strings or integer sequences, in display order; the
default is the first three. Repeated components and variable labels are retained.
`n_points=None` selects min(30, n_vars); explicit counts cannot exceed n_vars.
`include_lowest=True` splits that count between high and low loadings, with a gap
when ranks are omitted. It requires at least two ranks. Top-only mode preserves
Scanpy's extra label when available. Sorting, signed scores and ties use the
existing NumPy ranking path.

Selected loadings must be finite resident NumPy data. Sparse expression, views
and backed AnnData work when their selected loadings are resident; sparse/lazy
loadings reject without densification. Missing loadings require explicit Scanpy
PCA first. Select valid genes explicitly when a stored array has missing rows;
the packaged PBMC example selects its 309 highly variable genes. Scanpy 1.11.5
also errors on that full array. A single component renders normally here despite
an indexing error in the pinned upstream plotting function.

Native `hover` shows gene, loading score and displayed rank; `hover=False`
disables it. `width`/`height` size each plot area. Native fonts, ticks and outer
spacing retain the ranking renderer's documented differences. Rotated ASCII dots
render the omitted-rank marker because the native font lacks vertical ellipsis.
`show`/`save` use the common native delivery contract.

## PCA variance ratios

`pca_variance_ratio` reads `uns["pca"]["variance_ratio"]` and uses the existing
ranking preparation and native text panels. It never runs PCA, reads expression,
renormalizes ratios or changes stored results.

```python
variance = gsc.pl.pca_variance_ratio(
    pbmc, n_pcs=10, log=True, width=360, height=240, show=False,
)
variance.display(inline=True, controls=False)
```

Defaults match Scanpy: `n_pcs=30`, `log=False`. NumPy sorts the supplied scores;
original one-based PC labels stay attached, including ties. Scanpy's top-only
ranking convention includes the next PC when available, so `n_pcs=10` displays
eleven labels. Short results keep the requested rank-axis extent.

`log=True` takes the **natural logarithm of scores before ranking**, rather than
using a logarithmic axis. Hover shows the plotted score, original PC label and
zero-based displayed rank. `hover=False` disables it; native `width`/`height`
set the plot area. Common show/save rules and ranking typography limits apply.

The stored vector must be nonempty, real and finite; NumPy arrays and resident
sequences are supported. Log mode requires all stored ratios to be positive.
Sparse/lazy vectors reject without materialization. Sparse expression, views and
backed AnnData work with resident stored ratios, without needing PCA coordinates
or loadings. Missing ratios error and ask for explicit Scanpy PCA. Supplied
finite linear scores are plotted as given, with no added range or sum constraint.

## PCA overview

`pca_overview` reuses `pca`, `pca_loadings` and `pca_variance_ratio`, in that order.
Scanpy opens three plots; the native result arranges their charts vertically and
displays once. Each row keeps its data, axes and independent scales and guides.

```python
pca_genes = pbmc[:, pbmc.var["highly_variable"]]
overview = gsc.pl.pca_overview(
    pca_genes, color="louvain", zoom=True, width=280, height=280, show=False,
)
overview.display(inline=True, controls=False)
```

As in Scanpy, forwarded plotting options affect **only the PCA embedding**.
This includes component choices and the native `hover`, `zoom`, `width` and
`height` controls. Loadings keep their first-three-component and extreme-rank
defaults; variance ratios keep `n_pcs=30, log=False`. To customize diagnostics,
call them separately and compose the resulting charts with native operators.

All three plots use supplied results. Plotting never fits PCA or filters genes;
the packaged-data example explicitly selects genes with stored finite loadings.
Missing or unsupported results retain their parent's named error. All children
are constructed before displaying, so an error cannot leave a partial overview.
Common show/save rules apply to the whole result, including standalone HTML.

## Scatter cells or genes

`scatter` retains its own Scanpy signature and lookup rules while reusing the
embedding point renderer, color helpers, sizing, guides, native hover and x/y zoom.

```python
cells = gsc.pl.scatter(
    pbmc, x="n_counts", y="n_genes", color=["louvain", "percent_mito"],
    width=280, height=280, zoom=True, show=False,
)
genes = gsc.pl.scatter(
    pbmc, x="means", y="dispersions", color="dispersions_norm",
    use_raw=False, zoom=True, show=False,
)
expression = gsc.pl.scatter(pbmc, "CD79A", "MS4A1", use_raw=True, show=False)
```

All x/y/color annotation keys must agree on an orientation. Observation
annotations and gene-expression keys plot cells; variable annotations and
observation-expression keys plot genes. Observation orientation wins when both
match. The adapter calls public AnnData vector accessors and never transposes the
full object or densifies the full expression matrix. It reads repeated keys once
per source and retains duplicate point labels with distinct positional IDs.
The UMAP notebook includes both packaged cell and gene annotation examples.

Use native chart methods to collect guides below the panels and make them compact:

```python
cells = cells.resolve_legend(default="collected").configure_legend(
    orient="bottom", direction="horizontal", columns=6,
    symbolSize=64, gradientLength=140, gradientThickness=10, tickCount=3,
    layout={"anchor": "middle", "wrap": True},
)
```

These methods also work on shared embedding plots. Color scales stay independent;
compatible guides are collected in one place. Ordinary calls preserve Scanpy's
scatter legend symbol area of 300 points² (about 24 pixels across). Native
`symbolSize` uses logical pixel area, so 64 gives smaller symbols without changing
the plotted points. Panel `height` sizes the plot area; external guides add height.

Core 1.2 clips later columns of vertical categorical legends. Large scatter
symbols can also overflow a short single-column guide. The compact horizontal
configuration above avoids these cases. Automatic default-guide fitting remains
open under C11 in the integration status ledger; point data and hover are unaffected.

| Parameters | Current behavior |
| --- | --- |
| `x`, `y`, `color` | Numeric coordinates, categorical/numeric annotation or expression colors, opaque CSS names/hex, or multiple color panels. Default color is gray. Annotation fields take precedence over expression and literal colors. Variable hover identifies genes. |
| `basis`, `components` | Exact `obsm["X_" + basis]` lookup; one one-based component pair. Unlike `embedding`, scatter's diffusion-map basis skips the first stored column. Supplied basis takes priority over x/y. Missing coordinates error without analysis. |
| `use_raw`, `layers` | Cell expression defaults to raw if present. One layer or an x/y/color triple; None/`"X"` chooses X. When raw is present, nondefault layers require explicit `use_raw=False`. Variable orientation drops automatic raw as Scanpy's transpose does; no physical transpose is used here. |
| `groups`, `palette` | Saved category order and CSS palettes; gray background for missing/excluded groups without an NA legend. Explicit group order controls painting and the legend. Nested palettes follow categorical panels, even after numeric panels. For several categorical panels, use nested palettes; a flat list currently errors because pinned Scanpy applies it only to the first. |
| `sort_order` | Pinned 1.11.5 does not forward this flag: numeric colors use NumPy's ascending sort for both values. Categories paint gray background first, then groups; source order is preserved within a group. |
| `size`, `marker`, `alpha` | Scalar area, default 120000 / point count; dot, circle, square or diamond, once or per panel; scalar opacity. Same native point units as UMAP. |
| `frameon`, `title` | x/y plots retain numeric axes/frame, as in Scanpy; basis frames follow the setting/request. Default titles replace key underscores with spaces; flat colors have no title. All color panels occupy one row. |
| `legend_loc`, `legend_fontsize`, `legend_fontweight`, `color_map` | Right-margin or no legend; native font sizing and continuous scheme. Font weight has no effect on these external legends upstream. On-data label positions/weight and other legend locations remain M07.d/M14. |
| `hover`, `zoom`, `width`, `height` | Four keyword-only native additions. Hover defaults True, zoom False; panel size defaults to 300 × 300 logical pixels. Scatter does not yet expose linked brushing or Python membership retrieval. |
| `show`, `save`, `ax` | Same native display/export rules as other plots; `ax` is omitted and fails if passed. No image saving or Matplotlib return objects. |
| `projection`, `legend_fontoutline`, `left_margin`, `right_margin`, stored `uns["highlights"]` | Only 2D and ordinary defaults are supported. Nondefault forms fail with the option named; native guides own layout. |

Only finite numeric coordinates and resident selected expression are supported;
backed metadata works, backed/lazy expression errors. Missing numeric colors are
omitted from painting and coordinate limits, matching scatter rather than UMAP's
gray missing-value layer. Native schemes can differ from Matplotlib's palette
bins. Native axes/guide ticks and layout are not pixel-identical to Matplotlib;
explicit opaque palettes preserve category paints. Other color forms, 3D, marker,
margin, label and storage limits retain M07.d/M14 owners.

## Scrublet score distributions

```python
counts = sc.datasets.pbmc3k()
sc.pp.scrublet(counts, threshold=0.25, random_state=0, use_approx_neighbors=False)
chart = gsc.pl.scrublet_score_distribution(counts, zoom=True, show=False)
chart.display(inline=True, controls=False)
```

The threshold above is a demonstration setting; use your chosen analysis
threshold. Plotting only reads `obs["doublet_score"]` and stored `uns["scrublet"]`
results. It never runs Scrublet, reads expression or modifies the supplied data.
Metadata-only AnnData views and backed objects are supported.

Each batch gets an observed/simulated pair. Histograms use NumPy with Scanpy's
fixed **50 edges / 49 bins** from 0 to 1. Each density divides by its own number
of scores falling in that range and by bin width. Missing and finite out-of-range
scores are excluded; 1 belongs to the final bin. A score vector with no in-range
values fails clearly. Native gray bars and a black stored-threshold rule retain
their initial score/density limits, including thresholds outside [0, 1].

| Option/storage | Supported behavior |
| --- | --- |
| `scale_hist_obs`, `scale_hist_sim` | Defaults `"log"` / `"linear"`; either panel accepts either scale. Density values stay unchanged. Other Matplotlib scale names, including symlog/logit, fail explicitly. |
| Single result | Read `uns["scrublet"]["doublet_scores_sim"]` and optional `threshold`. |
| Batched result | Read `batched_by`, the named obs column and each `batches[batch]` result. Preserve categorical order, or Scanpy's category conversion for other labels; missing batch labels are omitted. No pooling. |
| `figsize=(8, 3)` | Approximate per-batch figure dimensions at 100 logical pixels/inch, reserving space for axes/titles. Native layout controls fonts/ticks; physical export DPI is independent. |
| Native additions | Keyword-only `hover=True`, `zoom=False`, `width=None`, `height=None`. Width/height set plot area per panel (default 340 × 210); they cannot be mixed with a nondefault figsize. |
| Hover/zoom | Populated-bin hover shows batch, sample, boundaries, count and density. Optional score-axis zoom is independent per panel, with thresholds following the same score scale. Bins stay fixed. |
| Display | Scanpy's `show=True` default is retained; False returns one native chart for the full layout. Common native save/HTML rules apply; `return_fig`/`ax` are omitted. |

Scores must be resident one-dimensional numeric vectors. Infinity, malformed
results and unused batch categories fail clearly. Unused categories can be
removed explicitly before plotting; they are not silently pooled or discarded.
Histograms are aggregate marks, so hover describes bins rather than cell IDs.

## Highest-expression genes

```python
counts = sc.datasets.pbmc3k()  # Count data; downloads on first use.
chart = gsc.pl.highest_expr_genes(counts, n_top=20, zoom=True, show=False)
chart.display(inline=True, controls=False)
```

The adapter calls public `sc.pp.normalize_total` on a detached AnnData shell to
calculate each gene's percentage of each cell's **total across all genes**.
It ranks genes by mean percentage, including zero-total cells, and preserves
Scanpy's reverse-argsort tie order. X is used unless `layer` is given; `raw` is
ignored. Counts, metadata and views stay unchanged. Sparse counts stay sparse
except for one selected gene column at a time.

Native boxes show the 25th/50th/75th percentiles, 1.5-IQR whiskers and individual
outliers. `log=True` changes the percentage axis after computing linear summaries.
Hover reports box statistics or outlier cell IDs and percentages; `zoom=True`
enables navigation along the percentage axis. The returned native chart supports
notebook rendering and standalone HTML through the common display/save contract.

The Scanpy defaults are retained (`n_top=30`, `layer=None`, `gene_symbols=None`,
`log=False`). Native keyword-only additions are `hover=True`, `zoom=False`,
`width=None`, `height=None`. Default width is 387.5 logical pixels; height follows
Scanpy's requested gene count. `gene_symbols` reads a var column; selected labels
must be unique and nonmissing. Counts must be finite, nonnegative and resident;
zero-total cells produce Scanpy's warning and remain zero. An all-zero log plot
errors clearly. Backed/lazy counts, duplicate/missing selected labels and all
forwarded Seaborn styling options fail explicitly. Matplotlib `ax`/`return_fig`
are omitted. Native boxes use the built-in category10 palette (repeating after ten genes),
without Seaborn saturation adjustments. Fonts/ticks do not follow Matplotlib
global settings.

## Variable-gene diagnostics

```python
pbmc = sc.datasets.pbmc68k_reduced()
chart = gsc.pl.highly_variable_genes(
    pbmc.var, zoom=True, width=280, height=240, show=False
)
```

This plots the stored normalized and raw dispersion against mean expression.
Black points are selected genes; gray points are other genes. Native tooltips
show gene identity and original values, and `zoom=True` enables independent x/y
navigation in each panel. One native legend is collected below the pair.

Pass AnnData after explicitly running `sc.pp.highly_variable_genes` in your
analysis workflow, or supply its result DataFrame/record array. The packaged PBMC
table already has statistics but predates `uns["hvg"]` metadata, so this example
passes `pbmc.var` directly. Plotting never computes a new selection or reads
expression. Repeated gene labels retain separate point identities.

| Input/option | Supported behavior |
| --- | --- |
| AnnData | Read `var` and stored `uns["hvg"]["flavor"]`; views and backed metadata are supported without reading X/raw/layers. Missing analysis errors clearly. |
| DataFrame | Read supplied columns; `variances_norm` selects variance fields, otherwise dispersion fields, as in Scanpy. |
| Record array | Use supplied dispersion fields and positional gene identities, preserving the pinned legacy behavior. |
| `highly_variable_genes` | True reads the boolean `highly_variable` column; False reads `gene_subset`. Selected genes draw first, then other genes. |
| `log` | Use log axes without transforming stored values. As in 1.11.5, both panels use raw-statistic y limits. Means must be finite and positive; raw statistics must be finite with positive increasing limits. Other forms fail explicitly. |
| Missing values | Omit missing coordinate pairs independently per panel; retain their stored values. Infinity, ambiguous columns and missing/nonboolean selection flags error. |
| `show`, `save` | Common native display behavior; save only None/False, with HTML/JSON available through the chart. |
| Native additions | Keyword-only `hover=True`, `zoom=False`, `width=None`, `height=None`; default plot areas are 300 × 300 logical pixels. |

`filter_genes_dispersion(result, ...)` delegates to the same implementation with
`highly_variable_genes=False` and preserves the upstream deprecation warning.
Its `show=False` returns a native chart, rather than the old wrapper's None.
AnnData flavor detection follows Scanpy 1.11.5 exactly: only `seurat_v3` selects
variance columns; a supplied DataFrame selects them by the column's presence.
No cached statistics or caller data are changed.

Native fonts, ticks and the collected bottom guide use GenomeSpy layout. The
plotting data, draw order, point units and axis limits are checked independently
against Scanpy; this does not claim identical Matplotlib guide placement.

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
| 2D embeddings | Existing `obsm` coordinates; public AnnData `obs_vector`/`raw.obs_vector`; Scanpy's public palette lists | Masks, draw order, component selection, stable IDs and native color/size/guide mapping. No embedding computation. |
| Scatter | Public AnnData `obs_vector`/`raw.obs_vector`/`var_vector` and stored X_ coordinates; existing embedding color/style/point helpers | Distinct orientation, per-axis layers, legacy component labels and paint order; no full transpose or analysis. |
| PCA loadings | Stored `varm["PCs"]` and `var_names`; existing ranking preparation and chart builder | One-based component/count validation; no PCA or expression access. |
| PCA variance ratios | Stored `uns["pca"]["variance_ratio"]`; existing ranking preparation, NumPy sorting/log and chart builder | Named result/count checks; original PC labels stay attached. No PCA, renormalization or expression access. |
| PCA overview | Existing PCA scatter, loadings and variance-ratio entry points | Native vertical composition displays once, with independent scales/guides and unchanged diagnostic defaults. |
| Dotplot | Public `sc.get.obs_df`, including selected raw/layer/symbol lookup; AnnData categorization on the detached table | Shared pandas means, strict-cutoff fractions and plotting min–max scaling. Native marks and guides use those results. |
| Matrixplot | The same getter, categorization and shared grouped means/scaling; supplied `values_df` uses only group rows and zero-row feature lookup validation | Plot ordering, repeated slots and native tile/guide mapping. No expression-fraction computation. |
| Heatmap | The same getter, categorization, min–max operation, native palettes, marker ordering and tree branches | Cell values and original row positions, category spans and shared annotation alignment. No group means or downsampling. |
| Dendrograms | Stored `sc.tl.dendrogram` results, or that public method for a missing tree | Structural checks, shared leaf permutations and native branch rendering. |
| Clustermap | Public SciPy `linkage`/`dendrogram(no_plot=True)`, as used by Scanpy/Seaborn, or supplied linkage | Detached pandas normalization, bounded source access, color-track alignment and shared numeric tiles/tree rendering. No group-profile tree is substituted for cell/gene clustering. |
| Ranked summaries | Public `sc.get.rank_genes_groups_df` and stored ranking metadata; existing dotplot, matrixplot and heatmap entry points | One detached result shared by marker selection and statistic colors, ordered marker slots, strict stored fold-change filtering and clear missing-result errors. No ranking is run or cached data repaired. |

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
| cmap, color_map, vmin, vmax | GenomeSpy scheme names (default viridis) and numeric, percentile or callable bounds, including per-panel lists. Callables receive a copy of the masked numeric colors in painting order, including missing values, and must return a finite real number. Conflicting aliases error. GenomeSpy maps the retained measurements and draws the numeric guide. Unsupported names such as coolwarm and Matplotlib colormap objects error. |
| sort_order | Scanpy's continuous sort, including reversed equal-value ties; missing points draw first. Categorical source order is retained apart from moving missing points behind other points. |
| size, s, marker | Scalar or observation-length sizes in points squared; dot (`"."`), circle (`"o"`), square (`"s"`) and diamond (`"D"`) markers, once or per panel. Conversion accounts for marker path width, using a fixed 100/72 logical pixels per point. As in 1.11.5, an observation-size vector is carried in its reordered form between panels; reference tests cover this version-specific behavior. |
| mask_obs, groups | Recolor observations without dropping coordinates. Masks can be boolean arrays or an observation-column key. Groups and masks are mutually exclusive. |
| components, dimensions | One-based component pairs or zero-based dimension pairs; broadcasting follows Scanpy. Both cannot be supplied together. |
| frameon, title, ncols, hspace, wspace | Frame defaults to Scanpy's frame setting; panel layout uses explicit native defaults. Titles and guides remain per panel; guides are not automatically collected. |
| width, height (GenomeSpy additions) | Plot-area dimensions per panel in logical pixels. None uses 300 by 300 logical pixels. Explicit dimensions size each panel and its guide directly; axes and legends add space. Marker and font sizes are unchanged. |
| legend_loc, legend_fontsize, legend_fontweight | Centered right-margin legend, on-data median labels, or no legend; point font sizes use the fixed native conversion. On-data labels currently require legend_fontweight="normal" (or 400); the upstream bold default errors for that location because its glyph atlas is not bundled. |
| alpha, edgecolor/edgecolors, linewidth/linewidths | Scalar opacity and edge styling; conflicting aliases error. Matplotlib color shorthands, numeric RGB(A) tuples, cyclers, and per-entry alpha are rejected. Use opaque CSS names/hex and scalar alpha. |
| show | False returns a native chart; True displays once through anywidget and returns None. None uses Scanpy settings.autoshow. |
| save | None/False are supported when no automatic image save is requested. Image formats and automatic save currently error; native chart.save supports HTML/JSON. |
| ax, return_fig | Omitted. Passing either, even ax=None, raises a targeted error. Use show=False and native chart composition/configuration. |
| edges, edges_width, edges_color, neighbors_key | Optional stored undirected neighbor edges beneath the points and outlines. Width defaults to 0.1 points; color defaults to grey and accepts one opaque CSS color. The graph is read once, with native endpoint lookups into the shared cell table. Requires the first two components and a graph without self-loops. |
| projection, arrows, scale_factor | Only the ordinary 2D/no-arrow defaults are supported yet; nondefault scale_factor remains unsupported. |
| vcenter | None keeps a linear color scale. A number, percentile string or callable places that value at the native scheme midpoint; singleton/per-panel lists are supported. Automatic bounds expand if needed to enclose the center. Explicit bounds must strictly enclose it. |
| norm | Matplotlib normalization objects remain unsupported and raise an error. |
| add_outline, outline_width, outline_color | Optional two opaque outline layers behind the foreground, matching Scanpy’s relative widths and draw order. Widths are nonnegative pairs; colors are pairs of opaque CSS names/hex. Foreground opacity defaults to 0.7 only when outlines are enabled; explicit alpha (including None) retains its usual meaning. Foreground edges are disabled, while outline edges use the supplied scalar edge/linewidth options. |
| legend_fontoutline | Not implemented yet; unsupported values fail by name. |
| colorbar_loc | `"right"` (default), `"left"`, `"top"`, `"bottom"`, or None to hide continuous colorbars. Categorical legends retain `legend_loc`. |
| Arbitrary scatter kwargs, other markers/legend locations | Error with the unsupported argument named. |

```python
chart = gsc.pl.umap(
    pbmc, color=["louvain", "CD79A"], add_outline=True,
    outline_width=(0.3, 0.05), outline_color=("black", "white"),
    zoom=True, show=False,
)
```

Square and diamond markers use native `square` and `diamond` shape encodings,
including missing-value points and outlines. They reuse the same colors, hover,
navigation and selection paths, without extra data or layers. For example,
`gsc.pl.umap(pbmc, color=["louvain", "CD79A"], marker=["s", "D"], size=20, show=False)`
uses a square in the first panel and a diamond in the second. Scanpy's diamond
is a rotated square: its horizontal/vertical width is √2 times the square's at
the same size. The native size encoding accounts for this without changing the
supplied sizes. Thin diamond (`"d"`) and other unsupported markers still error.

Triangle markers (`"^"`, `"v"`, `"<"`, `">"`) remain unsupported: Core 1.2.0's
native triangles are equilateral, while Scanpy's triangles have equal width and
height. Uniform sizing cannot match both dimensions; the adapter does not
approximate this geometry.

Category keys follow each panel's marker shape through native legend inheritance.
This deliberately differs from Scanpy 1.11.5's circular embedding keys; scatter
keys already follow their points upstream. Diamond keys include their converted
size on the color legend; customize that legend's
`symbolSize` directly to override it. Other native legend defaults remain
available through chart configuration.

Outlines reuse the same observation records, sorted sizes and coordinate scales;
they add no data extraction or analysis. Outer outlines draw first, inner outlines
second, and colored/missing points last. Only foreground points provide tooltips.
Linked brushing dims all three layers and retains the same stable IDs and count.
Category legends stay opaque, as in Scanpy. Thin edges can differ at the pixel
level between WebGL, browser scaling and Matplotlib exports. Outline settings
have no visual effect while `add_outline` is False or None. All shared embedding
functions, including PCA overview's embedding panel, inherit this path; `scatter`
keeps its own Scanpy signature and does not add outline arguments.

`edges=True` reads the existing default neighbor connectivities from
`obsp["connectivities"]`, requiring `uns["neighbors"]`. A custom `neighbors_key`
uses that metadata's `connectivities_key`. Current storage takes precedence over
the legacy matrix in the neighbors metadata. NetworkX supplies the same
undirected edge order as Scanpy, including asymmetric entries and explicitly
stored sparse zeros; weights do not change edge width or color. No neighbors,
embedding or expression matrix is computed or densified. Missing, nonfinite,
wrong-shaped or unsupported graph storage raises a named error.

Edges share point navigation, use Scanpy's extra endpoint padding and remain
unpickable behind the points. Cell hover, linked counts and Python retrieval
still describe cells; brushing does not recolor graph edges. This increment
supports `dimensions=(0, 1)` only. Additional stored coordinate columns are
left intact and the first pair is used; Scanpy 1.11.5's edge renderer assumes its
stored positions are already two dimensional and ignores requested component
pairs. Other pairs, self-loops and per-edge/numeric colors currently error.
Empty graphs render the ordinary point chart. Edge style/key options have no
effect while `edges=False`, as in Scanpy.

Callable `vmin`/`vmax`/`vcenter` run once per numeric panel when creating the chart. Use
missing-aware functions such as `np.nanmin` or
`lambda values: np.nanpercentile(values, 99)`. Callbacks receive copied values
after masking and sorting; `sort_order=False` keeps source order. They can also
appear in singleton or per-panel lists mixed with numeric/percentile bounds and
None. Categorical panels skip bounds. Invalid results raise a named error;
exceptions from the callback propagate. Hover, zoom and HTML delivery use the
resolved numeric limits without calling Python again.

For example, `vcenter=0, cmap="redblue"` assigns half the color scheme to each
side of zero, preserving unequal observed limits. The existing measurements
stay in the chart; a native three-value domain, equivalent to `domainMid`,
controls interpolation and guide positions. This applies to all shared embedding
functions and PCA overview's embedding panel; scatter keeps its own signature.
For constant values equal to the center, a visible colorbar expands and uses
the midpoint color; without a colorbar Scanpy 1.11.5 uses the last scheme color.

Continuous colorbars span the plot height on the left/right and the plot width
on the top/bottom, including non-square panels. These are native guide defaults,
so `.resolve_legend(default="collected")` and `.configure_legend(...)` can still
collect and restyle numeric colorbars. When moving colorbars, categorical legends
remain explicitly on the right in vertical order.

```python
chart = gsc.pl.umap(
    adata, color=["n_counts", "percent_mito"], colorbar_loc="top", show=False
)
chart.resolve_legend(default="collected").configure_legend(
    gradientLength=140, gradientThickness=8
)
```

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
| `title`, `colorbar_title`, `size_title`, `var_group_*` | Native labels, bracket rules and size/color guides. Mapping features supply brackets directly. Scalar `linewidth` styles dot edges. The matrix viewport has a black 1.5-point frame; side tracks remain unframed. |
| `width`, `height` | Plot-area logical pixels; defaults are 37 pixels per feature column and 35 per group row, exchanged with the axes. Labels and guides add space. |
| `zoom`, `highlight` | Both default False. `zoom=True` enables y-only navigation; `zoom="xy"` enables both axes. Zoom/panning retain aligned labels and tree branches; highlighting uses a native crosshair ruler at the row and column centers under the pointer, including gaps between dots. Dot sizes and both guides keep their original mapping. Repeated labels retain separate integer slots. |
| `hover` | Enabled by default. Tooltips show gene, group, displayed mean/color value and actual expressing-cell percentage, before dot-size clipping. Use `hover=False` to disable them. Scaled means and supplied color values are labeled explicitly. |
| `figsize` | Explicit native layout budget at 100 logical pixels/inch: subtract a fixed 150-pixel guide allowance from width; height sizes the plot area. Labels and renderer padding add space, so this does not fix the outer canvas dimensions. Conflicts with `width`/`height` error. |
| `show`, `save`, `ax`, `return_fig` | Same native return/display/export boundary as UMAP. No Axes dictionaries or fake builders. |
| `dendrogram`, `norm`, `vcenter`, other forwarded kwargs | Trees accept True or a stored key; see the tree contract below. Nondefault norm/vcenter and other kwargs error; `DotPlot`, supplied `dot_size_df`, and builder styling are M13. Only scalar `linewidth` is accepted from scatter kwargs. |

Rows and columns use integer index-scale slots with padding that preserves the
initial Scanpy spacing. Marker blocks that partition the genes have four-pixel
gaps, fixed under zoom. Labels, brackets and trees use aligned `gs.surround`
side tracks; native guides sit outside the whole chart. Repeated gene labels
retain separate slots. Hover describes group/feature summaries; these dots do not identify individual cells.
Brushes and individual-cell selection remain deferred.

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
| `title`, `colorbar_title`, `var_group_*`, `width`, `height`, `figsize` | Shared native grouped layout and horizontal color guide. Index slots have no outer padding or group gaps; tiles remain adjacent across marker blocks. Default cells are 37 × 35 logical pixels, exchanged when axes swap. The outer frame is omitted. |
| `edgecolor`, `linewidth` in kwargs | Scalar opaque CSS edge color and nonnegative width in points; defaults are gray and 0.1. `edgecolor="none"` disables edges. Plural aliases error: Scanpy 1.11.5 overwrites those forwarded forms with its defaults; use the singular forms explicitly. Other pcolor kwargs error. |
| `zoom`, `show_values` | Both default False. `zoom=True` enables y-only navigation; `zoom="xy"` enables both axes. Enable fitted two-decimal plotted values; see [shared grid interactions](#shared-grid-interactions). |
| `hover` | Enabled by default; show gene, group and displayed mean/scaled mean or supplied value. `hover=False` disables picking without changing tile geometry. Summary tiles do not identify individual cells. |
| `show`, `save`, `ax`, `return_fig`, `dendrogram`, `norm`, `vcenter` | Same native delivery boundary as dotplot. Trees accept True or a stored key; norm/vcenter error. The MatrixPlot builder and its styling methods are M13. Brushes remain deferred. |

Native palette interpolation, fonts and guide layout have the same documented
fidelity boundaries as dotplot. Complete-chart checks cover labels, brackets,
plot and guide placement; registered tile comparisons use 150 export DPI and
DPR 1.5. The production adapter never imports upstream plotting or Matplotlib.

(shared-grid-interactions)=
## Shared grid interactions

Dotplots retain a black frame around the matrix viewport, including across group
gaps; labels, brackets and trees remain unframed. Heatmaps and matrix plots omit
the outer frame, a deliberate visual difference from Scanpy. Dot outlines and
tile-edge options are preserved. Native
`chart.configure_view(stroke="black", strokeWidth=1)` can add a frame to unframed
plots. Ranked variants inherit the same defaults.

Grid interactions are optional additions to the Scanpy signatures:

```python
heatmap = gsc.pl.heatmap(pbmc, markers, "bulk_labels", zoom=True, show_values=True, show=False)
matrixplot = gsc.pl.matrixplot(pbmc, markers, "bulk_labels", zoom=True, show_values=True, show=False)
matrix = gsc.pl.matrix(values, zoom=True, show_values=True, show=False)
clustermap = gsc.pl.clustermap(cells, zoom=True, show_values=True, show=False)
dotplot = gsc.pl.dotplot(pbmc, markers, "bulk_labels", zoom=True, highlight=True, show=False)
```

Use the mouse wheel inside the plot to zoom y and drag to pan y with
`zoom=True`; x stays fixed. Set `zoom="xy"` to enable zooming and panning both
axes. Native axis-margin gestures can then zoom one axis. Row/column labels and
dendrograms follow the visible slots; outside labels and partially visible gene brackets are hidden.
Heatmap category bands and group gaps follow individual cells. Clustermap's
two trees and annotation tracks follow the live row/column positions; automatic
tick labels reveal more names as slots grow. Defaults remain
`zoom=False`, `show_values=False` and `highlight=False`.

Category-strip tooltips use the native default handler and the same `hover` flag
as tiles. They work with the bundled Core 1.2.0 runtime, including after zoom and
pan. All expression grids use native `gs.surround` side tracks with shared
index scales for labels, brackets, trees and color tracks. Supplied matrices
and correlation matrices use the same track helpers. There is no patched bundle or custom hover listener
in the integration.

`show_values` uses native `fitToBand` text, shared tile records and the plotted
value after any log transform/scaling. Values fade in as cells become large
enough and show two decimals; tooltips retain more precision. Missing cells have
no text. Black/white contrast uses the native palette sampled at 256 bins,
clamped color bounds and tile opacity over white. Sampling runs in GenomeSpy;
there is no Python colormap implementation.

`highlight` uses a native two-axis ruler to mark the row and column centers under
the pointer, including gaps between dots, and clears on leaving the plot. Its
crosshair stays inside the plot and adds no background datasets or hover selections.
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
IDs, category bands, group gaps and branches follow it. Scanpy's category
sorting includes its within-group tie order. The adapter never substitutes group
means or changes AnnData.

| Parameters | Current behavior |
| --- | --- |
| `var_names`, `groupby`, `use_raw`, `layer`, `gene_symbols`, `num_categories` | Grouped access rules and resident NumPy/CSR/CSC storage limits apply. Repeated gene slots and views are supported. Missing group labels and unused categories fail explicitly; single-group data retains cell order without a category strip or tree. |
| `log`, `standard_scale` | Apply log1p before min–max scaling of individual cell values: `"var"` scales each gene across cells; `"obs"` scales each cell across requested genes. Constant ranges become zero. These are not matrixplot's scaled group means. |
| `dendrogram` | False, True or a stored-result key. Reuse Scanpy's stored result or the guarded public computation. Heatmap supports two-group trees. Interpolate stored branches to the centers of unequal cell-group spans; native link endpoints keep them connected across gaps. Group labels share those centers, correcting the old half-row offset. Matching marker blocks follow tree order too. |
| `swap_axes`, `show_gene_labels`, `var_group_*` | Ordinary heatmaps use gene brackets above the matrix; swapped heatmaps use a colored gene-group strip on the right, as Scanpy does. Show gene labels by default for at most 50 slots. `var_group_rotation` affects ordinary brackets. |
| `cmap`, `vmin`, `vmax`, `alpha`, `interpolation` | Native scheme (default viridis), numeric bounds, scalar opacity and nearest-neighbor tiles. Missing values keep their positions but are unpainted; all-missing colors error. Other interpolation, norm/vcenter, Matplotlib colormaps and unsupported imshow kwargs error by name. |
| Group gaps/layout | Native surround side tracks share the tile index scales. Cell groups have 4 CSS-pixel gaps that stay fixed under zoom and DPR changes; marker blocks also have gaps when their spans partition the genes. A single group has no internal gap. Arbitrary/overlapping brackets do not invent groups. Native scale settings can customize gaps. |
| Category colors | Reuse saved AnnData colors or the shared Scanpy default palettes without writing them back. Numeric and multi-key strips use native category20, currently limited to 20 groups. |
| `width`, `height`, `figsize` | Width/height control the tile area in logical pixels. Defaults follow Scanpy's gene-label size rules; figsize uses 100 pixels per inch with space reserved for strips/trees. Native text and outer layout differ from Matplotlib. The vertical color guide uses at most 400 pixels. |
| `zoom` | Defaults False. `True` enables y-only wheel zoom and drag panning; `"xy"` enables both index axes. Bands, gaps, tree leaves and gene labels follow the visible cells/genes. Clip branches and strips at the plot extent; hide offscreen labels and gene brackets whose whole span is not visible. |
| `show_values` | Default False. Reveal the plotted cell values to two decimals when the tiles have enough room; missing cells remain empty. |
| `hover`, delivery | Default hover shows original cell ID/name, gene, group and displayed expression. Category-band tooltips show the group in its own native track. `hover=False` disables both. Duplicate names use stable original-row IDs. Brushing is not offered. Existing show/save/native-return rules apply; Matplotlib axes and figure-return options error. |

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
match the axis length; repeated names retain separate index slots. Explicit
labels and their titles occupy native side tracks and follow the same index
scales during navigation; numeric defaults remain native axes.

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
apply. Optional `zoom=True` enables y-only wheel zoom and drag panning, with aligned tick labels. Use `zoom="xy"` for both axes. `show_values=True` adds fitted two-decimal values. Nonlinear normalization is unsupported.

Eight frozen Scanpy figures retain values, color bounds, labels, complete charts
and registered crops at 100 display / 150 export DPI. Native DPR 1.5 checks cover
tile footprints, missing paint and palette-bin differences; separate checks
exercise hover after resizing and offline HTML delivery. A resident 200 × 1,000
float32 resource check retained all 200,000 values: warm preparation took 0.14 s,
default formatted/validated JSON was 28.1 MB and took 12.0 s with allocation tracing, and tracked peak
allocation including serialization was 344 MB. Browser first paint including
dispatch took 10.3 s; paused hover was 113 ms. These local observations expose
the current serialization cost; larger/chunked transport remains M05.d.

## Clustermap compatibility

```python
genes = ["CD79A", "MS4A1", "CD3D", "NKG7"]
cells = pbmc.raw[:, genes].to_adata()
chart = gsc.pl.clustermap(
    cells, obs_keys="bulk_labels", use_raw=False, cmap="viridis",
    yticklabels=False, zoom=True, show_values=True, width=400, height=450, show=False,
)
```

Clustermap retains individual cells and clusters both rows and columns by default.
It does not reuse the group-profile tree from dotplot/matrixplot: its distances
describe the supplied cell/gene values. Scanpy delegates this plot to Seaborn;
the adapter uses the same public SciPy calculations without constructing a figure.
Plotting-only linkage is local and never written to AnnData.

| Option | Supported preview |
| --- | --- |
| `use_raw` | Defaults to raw when present. The entire supplied matrix is requested, so subset AnnData first. Scanpy 1.11.5 labels raw columns with `adata.var_names`; differing raw/X variable counts raise a clear error. No layer/symbol extensions are added. |
| `method`, `metric`, `row_cluster`, `col_cluster` | SciPy string names, default average linkage and Euclidean distance. Disabling an axis keeps its supplied order. No embedding, group analysis or ranking runs. |
| `row_linkage`, `col_linkage` | Finite valid linkage with the matching leaf count. Supplied trees are authoritative and are not recomputed; each axis can use a different method/metric. |
| `z_score`, `standard_scale` | None, 0 (rows), or 1 (columns); mutually exclusive. Scaling precedes linkage. Z-scores use sample standard deviation, matching Seaborn; constant ranges become missing rather than the zero convention of grouped expression plots. Missing distances fail. |
| `mask` | Matching boolean array or identically indexed DataFrame. Masks affect display and color bounds, never linkage. Missing values may be displayed blank when clustering is disabled or valid linkage is supplied. At least one unmasked finite value is required. |
| `obs_keys`, `row_colors`, `col_colors` | One categorical observation key, or explicit CSS color tracks. `obs_keys` gives the strip a native category legend using saved order and palette, independent of the expression colorbar. Pandas Series/DataFrames align by index; lists are positional, with nested lists representing tracks. Missing annotations are white and omitted from the legend. Explicit CSS tracks have no category labels or legend. Saved category palettes/order are reused without mutation. `obs_keys` conflicts with explicit row colors. |
| `xticklabels`, `yticklabels` | Auto spacing, True/False, positive stride, or a complete label list. Repeated labels retain distinct index slots. The matrix, labels, strips and branches follow the same permutation. |
| Layout/colors | Native scheme names, numeric `vmin`/`vmax`, `linewidths`, CSS `linecolor`, tree/track ratios and native matrix dimensions. `figsize` uses 100 logical pixels/inch and conflicts with width/height. `cbar_pos=None` hides the guide; `cbar_kws` supports its label. |
| `zoom`, `show_values` | Opt-in shared grid navigation and fitted plotted values. `zoom=True` navigates y only; `zoom="xy"` navigates both axes. Trees, strips and visible labels follow the same ordered slots. Both options default False. |
| Delivery | Default native hover reports original cell name, gene and plotted value. Native `obs_keys` strip tooltips show the observation category. `hover=False` disables both. `show`, `save` and chart HTML/JSON delivery follow the shared contract. The result is a native chart, not Seaborn's ClusterGrid; its artist attributes/chains are unavailable. |

The default native palette is magma rather
than Seaborn's rocket, and the native color guide is on the right rather than in
Seaborn's upper-left inset. Explicit viridis references isolate layout/value fidelity
from this palette difference. Custom `cbar_pos`, `pivot_kws`, `tree_kws`, `annot`,
`center`, `robust`, `norm`, artist options and unknown kwargs reject by name.

The preview accepts resident dense/CSR/CSC inputs and views, with at most **250,000
matrix values** and **1,000,000 pairwise distances per automatically clustered
axis**. Both guards run before expression access. Supplying linkage avoids the
distance allocation, but not the tile limit. Backed/lazy matrices reject before
reading expression; no silent sampling, aggregation or full unrelated matrix
densification occurs. The expression notebook uses all 700 packaged PBMC cells
and the same ten marker genes. Clustermap rows and columns remain contiguous.
Native surround tracks keep branches and color strips adjacent with zero track
spacing.

## Stored rankings and ranked expression plots

Scanpy owns differential-expression analysis. The packaged PBMC object already
has a `rank_genes_groups` result; plotting reads it directly:

```python
pbmc = sc.datasets.pbmc68k_reduced()
scores = gsc.pl.rank_genes_groups(pbmc, n_genes=5, show=False)
dots = gsc.pl.rank_genes_groups_dotplot(pbmc, n_genes=3, zoom=True, show=False)
means = gsc.pl.rank_genes_groups_matrixplot(
    pbmc, n_genes=3, standard_scale="var", show_values=True, show=False,
)
cells = gsc.pl.rank_genes_groups_heatmap(
    pbmc, n_genes=3, standard_scale="var", zoom=True, show_values=True, show=False,
)
```

For new data, run `sc.tl.rank_genes_groups(...)` explicitly during analysis first.
Missing or malformed results fail without running analysis or overwriting `uns`.
Ranked expression wrappers select through the public
[`sc.get.rank_genes_groups_df`](https://scanpy.readthedocs.io/en/1.11.x/generated/scanpy.get.rank_genes_groups_df.html)
and call the existing native plot. They inherit its source selection, summaries,
normalization order, trees, hover, limits and opt-in interactions.

| Surface | Current behavior |
| --- | --- |
| Stored marker selection | Default `n_genes=None` selects ten per list. A positive count takes the first ranks; a negative count takes the stored tail without reversing it. Filtered missing names are dropped before slicing. Repeated genes retain their slots and group brackets. |
| `groups`, `groupby`, `key` | Preserve requested rank-list order; a string selects one group. `groups` selects gene lists, not observation subsets. Expression grouping defaults to stored params; `groupby` overrides it. `key=None` uses `rank_genes_groups`. |
| `var_names`, symbols and threshold | Explicit lists/dictionaries replace automatic selection and conflict with explicit `n_genes`. Symbols for ranked marker selection use the getter's `adata.var` lookup. `min_logfoldchange` applies a strict `>` filter only when selecting automatic lists; it needs stored fold changes. As in Scanpy, explicit markers bypass that filter. |
| Raw/layer and trees | Expression uses the parent plot's raw/layer defaults and explicit kwargs; it does not automatically switch to a ranking's stored layer. `dendrogram` defaults True and can be disabled. Reading a rank list never computes a tree; the parent plot owns its normal tree policy. |
| Metric colors | Dotplot/matrixplot accept `scores`, `logfoldchanges`, `pvals`, `pvals_adj`, `log10_pvals` and `log10_pvals_adj`. The log options use **−log10(p)**. Colors read all stored ranking groups; `groups` selects marker lists only. Dot sizes still use expression fractions. Matrix statistics bypass `standard_scale`; dotplot retains its parent scaling order. Heatmaps keep individual-cell expression. |
| `rank_genes_groups` panels | Stored order and scores, requested groups, native label sizing, shared/separate score bounds and `n_panels_per_row` alias. Symbol labels use raw/var according to the ranking's stored `use_raw`. No expression matrix is read, including for backed data and views. Nonfinite scores or missing names error; filtered lists remain available through the expression wrappers. |
| `ranking` | Supplied var/obs/uns/varm/obsm score columns or a nested dictionary. Dense array `indices`, label lists/prefixes, natural-log scores and `include_lowest` are supported. Sorting follows Scanpy, including its extra top label when `include_lowest=False`. Sparse/backed array-column selection errors. This function has no save argument and does not use autosave, as in Scanpy. |
| Native rendering and delivery | Rank panels use rotated labels and native axes; width/height default to 300 pixels per panel. Fonts, automatic tick density and outer layout differ from Matplotlib. Expression wrappers return their parent chart type and accept its options; Matplotlib objects and unknown kwargs error. Notebook and offline HTML delivery use the existing chart/widget. |

The repository's `integrations/scanpy/notebooks/scanpy_expression.ipynb` shows
packaged stored scores, all three ranked expression variants, and explicit Scanpy preparation followed by statistic-colored summaries.

Statistic colors require complete stored rankings, as in Scanpy. The packaged
logreg cache contains only 100 ranks per group; prepare a new result explicitly:

```python
sc.tl.rank_genes_groups(
    pbmc, "bulk_labels", method="wilcoxon", use_raw=True,
    n_genes=pbmc.n_vars, key_added="rank_stats",
)
dots = gsc.pl.rank_genes_groups_dotplot(
    pbmc, key="rank_stats", n_genes=3, values_to_plot="logfoldchanges",
    cmap="redblue", vmin=-4, vmax=4, show=False,
)
tiles = gsc.pl.rank_genes_groups_matrixplot(
    pbmc, key="rank_stats", n_genes=3, values_to_plot="log10_pvals_adj",
    cmap="viridis", zoom=True, show_values=True, show=False,
)
```

Rank colors match genes by label in each stored group, including repeated plot
slots and gene symbols. Without a tree or explicit category order, matrixplot
retains the statistic table’s alphabetic group order; dotplot restores observation
category order, matching Scanpy. A `groupby` override must have the same group labels.
Expression raw/layer defaults and explicit options remain independent of ranking
params; saved statistics are never recomputed from the selected expression source.
The metric supplies the default colorbar title; `colorbar_title` overrides it.

Missing metrics, incomplete rankings, ambiguous labels, absent gene/group pairs,
and nonfinite selected values fail clearly. Unlike Scanpy’s missing-value fill,
this preview does not substitute `1` for missing statistics. Raw p-values may be
zero; log-transformed p-values must be positive because zero yields infinity.
No clipping or replacement analysis occurs. These cases remain compatibility
limits tracked in M14.

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
with native orthogonal links; it does not calculate profiles, correlations or linkage.
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
| `correlation_matrix` | Cached or locally computed group correlations. None/True draws a left tree and orders both axes by leaves; a string selects the cache. False keeps current category order without drawing a tree. Optional two-decimal numbers and default summary hover are native marks. Native side tracks hold vertical column labels, right row labels and the optional left tree; the colorbar stays beneath the matrix. |
| Correlation colors/style | Default native redblue with reversed scheme extent gives blue negatives and red positives; the guide increases from -1 to 1. Native cmap names, scalar edgecolors and linewidth are supported kwargs. Other kwargs, norm/vcenter and Matplotlib colormaps error. Native interpolation differs from Scanpy's default bwr. |
| Correlation size/delivery | Default tile area is 60 pixels per group in each direction; width/height override it. Figsize uses a 100-pixels/inch budget, subtracting 180 pixels for a tree and 20 for the guide. Labels and padding add space. Existing show/save/native-return rules apply; ax is omitted. |

Dotplot/matrixplot trees reserve an 80-pixel branch region; heatmaps use 100 pixels
on the right or 80 above, and correlation trees use 180.
Zero-distance leaves meet the matrix edge without a gap or distance-axis padding.
Attached trees share native viewport-based height fitting: after zooming or panning,
`gs.ViewportDomainRef(mode="contain")` fits the height scale to branches whose
endpoints lie in the visible slots. This expands local tree detail without
recomputing heights or clusters. The full overview retains its original root margin.
Entirely zero-height trees keep a fixed nonzero range. A released Core limitation
remains when only a zero-height subtree is visible inside a larger tree: its
degenerate height range centers the branches (C13 in the integration ledger).
All dendrograms share native orthogonal links, as in the
[GenomeSpy clustered-heatmap example](https://genomespy.app/docs/examples/generic/clustered-heatmap/).
Each stored merge becomes two parent-to-child links; the native vertical or
horizontal elbow preserves its merge height. Python still computes the trees.
Complete SVG paths, WebGL and inline HTML are verified across the four standalone
orientations and attached trees. Core's separate straight-link SVG issue (C12 in
the integration ledger) does not affect these orthogonal trees.
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
  customization with subsets, titles/frames, categorical order/palettes, square
  and diamond markers, outlines, stored neighbor edges, an explicit Scanpy gene score and
  the eight-panel marker overview, followed by
  stored PCA with variance labels/loadings, variance ratios and the composed overview,
  explicitly prepared t-SNE and cell/gene scatter.
- {download}`Expression plots <../../../integrations/scanpy/notebooks/scanpy_expression.ipynb>`:
  marker dotplot, per-gene scaled matrixplot, zoomable individual-cell heatmap and supplied matrix on
  `bulk_labels`, clustermap, stored score panels and ranked expression variants,
  with aligned dendrograms and value hover.
  QC sections inspect the packaged variable-gene statistics and load PBMC3k counts for highest-expression percentages.

These adapt supported UMAP, dotplot, matrixplot and heatmap sections of Scanpy's
[core](https://scanpy.scverse.org/en/stable/tutorials/plotting/core.html) and
[advanced](https://scanpy.scverse.org/en/stable/tutorials/plotting/advanced.html)
plotting tutorials. Grouped examples reuse a tree explicitly computed in Python
with `sc.tl.dendrogram`; clustermap computes separate cell/gene linkage. Ranked
examples read the packaged stored results; statistic-color examples explicitly
prepare a separate complete ranking with Scanpy. Remaining tutorial plots and
Matplotlib artist styling are not implemented yet.

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
| Available as partial previews | umap, dotplot, matrixplot, heatmap, matrix, clustermap, dendrogram, correlation_matrix, ranking, rank_genes_groups, rank_genes_groups_dotplot, rank_genes_groups_matrixplot, rank_genes_groups_heatmap, embedding, tsne, diffmap, draw_graph, pca, pca_scatter, scatter, pca_loadings, pca_variance_ratio, pca_overview, highest_expr_genes, highly_variable_genes, filter_genes_dispersion, scrublet_score_distribution, embedding_density |
| Distributions and tracks | violin, stacked_violin, tracksplot, rank_genes_groups_violin, rank_genes_groups_stacked_violin, rank_genes_groups_tracksplot |
| Simulation | sim |
| Trajectories and graphs | dpt_groups_pseudotime, dpt_timeseries, paga, paga_adjacency, paga_compare, paga_path, timeseries, timeseries_as_heatmap, timeseries_subplot |
| Spatial | spatial |
| Plot builders and useful semantic methods | DotPlot, MatrixPlot, StackedViolin |
| Settings helpers retained in Scanpy | set_rcParams_defaults, set_rcParams_scanpy |

All entries except the available plotting previews and settings helpers remain required future integration
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

.. autofunction:: genome_spy.integrations.scanpy.pl.clustermap

.. autofunction:: genome_spy.integrations.scanpy.pl.dendrogram

.. autofunction:: genome_spy.integrations.scanpy.pl.correlation_matrix

.. autofunction:: genome_spy.integrations.scanpy.pl.scrublet_score_distribution

.. autofunction:: genome_spy.integrations.scanpy.pl.highest_expr_genes

.. autofunction:: genome_spy.integrations.scanpy.pl.highly_variable_genes

.. autofunction:: genome_spy.integrations.scanpy.pl.filter_genes_dispersion

.. autofunction:: genome_spy.integrations.scanpy.selection_mask
```
