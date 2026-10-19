# Scanpy implementation plan

The destination is the full public `scanpy.pl` plotting surface at the supported
Scanpy version. This is a delivery roadmap, not a claim that those plots already
exist. Read [STATUS.md](STATUS.md) for implemented behavior, the next slice,
blockers, the 50-entry inventory, validation evidence, and clearance decisions.
The [shared lifecycle](../README.md#plan-lifecycle) defines milestone states and
when working plans can be cleared. Update the status ledger with each slice.

This tracked plan supersedes ignored `plans/scanpy_integration_plan.md` as the
active roadmap. Research findings still need reconciliation before local plans
or prototype artifacts can be removed. No runtime or required test may depend on
those files being present.

## Product contract

Keep the analysis in Scanpy and replace supported plotting calls:

```python
import scanpy as sc
import genome_spy.integrations.scanpy as gsc

pbmc = sc.datasets.pbmc68k_reduced()  # Includes stored UMAP coordinates.
chart = gsc.pl.umap(pbmc, color=["louvain", "CD79A"], show=False)
chart.display(inline=True)
```

For new data, users explicitly run their preprocessing, neighbors, `sc.tl.umap`,
clustering, density estimation, and differential expression before plotting.
Missing analysis results produce actionable errors; plotting must never silently
rerun them. Plotting statistics, dendrogram linkage/layout, graph layout from an
existing graph, and violin density geometry are separate Python responsibilities,
with their own tested semantics and computation policies below.

The pinned [signature inventory](../../tests/integrations/scanpy/fixtures/api.json)
is Scanpy **1.11.5**: 45 plotting functions (including aliases), three builders,
and two Matplotlib settings helpers. Those two settings helpers remain in Scanpy;
they are explicit renderer-specific exceptions, not native plots to implement.
`scanpy.external.pl` is a separate future inventory, not counted as completed by
this core roadmap. Changes in the upstream public surface require a new inventory
and a version review rather than silently changing the denominator.

For supported cases, preserve names, argument names/kinds/defaults, aliases,
ordering, statistical meaning, and supplied results. Add keyword-only GenomeSpy
controls. Track meaningful unsupported parameters until implemented or explicitly
resolved as a renderer boundary. Signature presence alone is not support.
Scanpy 1.11.5 is the only accepted version today; broaden the optional dependency
range only after the version checks in M14 pass. Keep base and namespace imports
free of the scientific stack.

### Rendering boundary

- Omit `ax`, `cax`, and `return_fig`; detect them in forwarded kwargs and explain
  native composition/returns. Do not return fake Matplotlib figures or axes.
- Preserve `show`: false returns a native chart, true displays once, and none uses
  Scanpy's autoshow setting. Native builders are handled separately in M13.
- `save` is currently limited to its inactive form; image/automatic-save requests
  fail clearly. Native chart HTML/JSON saving works now. M14 resolves image export,
  suffix/autosave behavior, and explicitly documents any remaining boundary.
- Native chart configuration replaces artist/Axes method chaining. Preserve useful
  Scanpy builder methods that express plotting semantics (M13), without an artist
  emulation layer.
- Accept only GenomeSpy-supported color schemes and opaque CSS colors. Reject
  unsupported Matplotlib names/objects, cyclers, numeric color tuples, and entry
  alpha. Do not sample Matplotlib colormaps or read rcParams. Per-plot scalar alpha
  remains supported where implemented.
- Grouped `figsize` is a native layout budget at 100 logical pixels/inch. Dotplot
  width includes a fixed 150-pixel guide allowance; matrixplot uses the same budget.
  Height sizes the plot area.
  Labels and renderer padding add space, so it does not fix the outer canvas.
  Reject conflicts with native panel `width`/`height`; test resulting panel and
  guide sizes. Do not consult global Matplotlib settings.
- No ignored kwargs: supported aliases/conflicts have tests; unsupported values
  name the function, option, and usable alternative or missing capability.

Initial appearance stays faithful to the data, order, marks, and guides.
Interactivity is opt-in and follows plain-chart review. Current native defaults
use 300 by 300 logical pixels per UMAP panel and 100/72 pixels per point.
Typography and native continuous palette interpolation are documented differences,
not reasons to skip complete-chart validation.

## Code and data ownership

Installable implementation: `src/genome_spy/integrations/scanpy/`. The
[workspace source map](README.md) explains current modules. This is the sole
public Scanpy integration namespace; do not add parallel import aliases.
Workflows stay here, validation under `tests/integrations/scanpy/`, and user docs
under `docs/integrations/scanpy/`. Generic `tools/` has no integration code.

A public plotting function validates its contract, calls pure data/statistic
functions, and passes detached results to its family's chart module. Chart
construction does not read AnnData. The existing chart/widget handles notebook,
JSON, and HTML delivery. Preserve ordinary anywidget parameter synchronization;
notebooks must not set up asyncio tasks or a custom ipywidgets connection layer.

Each family gets a focused chart module. Reuse common data access, category/color
handling, identities, group summaries, and trees wherever their semantics match.
Extract shared helpers when useful now; a second-family prerequisite would be
artificial. A family-specific data module is optional. Avoid a universal preparer
with many switches, a registry, or a general adapter framework.
Prefer public Scanpy computations over reproducing their algorithms; guard
unwanted analysis/mutation at the call boundary and honor their stored results.
The [source map](README.md#scanpy-integration-workspace) identifies shared owners:
data validation/source selection in `_data`, native presentation in `_style`,
grouped extraction/statistics and layout in `_grouped_data`/`_grouped_chart`,
and tree preparation/rendering in the dendrogram modules. Common display/options
handling remains alongside the public functions in `pl.py`. Add capabilities
to these helpers when semantics match; keep genuine plot-specific differences
local rather than introducing a universal preparer or per-plot copies.

| Concern | Reuse first | Independently implement/test where needed |
| --- | --- | --- |
| Observation/embedding projection | Existing `genome_spy.anndata` and public AnnData vector/indexing APIs | raw/layer choice, symbol resolution, selected columns, per-call order/identity |
| Grouped expression tables | `sc.get.obs_df` when its lookup/duplicate semantics match | numeric bins, multi-key groups, repeated display slots, masks and exact permutations |
| Group summaries | Shared pandas summaries over `sc.get.obs_df` output, as in Scanpy's documented recipe | aggregate mean/count_nonzero and pp.scale are not equivalent to plotting means/fractions/min–max scaling; retain the small tested operations |
| Stored gene rankings | `sc.get.rank_genes_groups_df` and stored params | strict filters, group/feature slots, rank-metric colors, expression-size statistics |
| Trees | Stored `sc.tl.dendrogram` results; the same public method for missing trees | structural validation, no-hidden-PCA guard, shared permutations, orientation and alignment |
| Distributions/graphs | Suitable public SciPy/Scanpy numerical functions | pinned KDE normalization, graph layout inputs, native chart geometry and order |

UMAP uses public AnnData `obs_vector`, because `sc.get.obs_df` has different
raw-symbol and duplicate-label behavior. Do not force a single accessor onto
families with different lookup semantics. Do not call upstream plotting, inspect
rendered artists, import benchmark scripts, or promote prototype geometry as
runtime preparation. Source and dataset provenance are reviewed before reuse.
The [Scanpy 1.11.5 reuse audit](../../docs/integrations/scanpy/index.md#reusing-scanpy-computations)
and [delegation/counterexample tests](../../tests/integrations/scanpy/test_upstream_reuse.py)
make these boundaries explicit. Recheck them when adding support for a version
that exposes suitable public plotting-preparation methods.

### Shared semantic requirements

Every applicable family checks these cases, independently of rendering:

- Source selection: raw default, explicit `use_raw`, layer precedence/conflicts,
  different raw/X variable vocabularies, symbol lookup and ambiguity. Preserve
  the family's actual rules rather than assuming UMAP rules apply everywhere.
- Group/feature identity: category order including unused levels, supplied
  palettes, missing values/groups, numeric bins, multiple grouping columns,
  duplicate names, repeated display slots and nonstring-label collisions.
- Row identity: preserve original observation positions through masking/sorting;
  attach stable unique IDs when a mark represents observations. Group-summary
  marks identify group/feature membership rather than inventing a cell ID.
- Storage: dense, CSR/CSC matrices and arrays, implicit zeros, views and backed
  data. Read selected columns in batches/chunks as needed; do not densify the
  full matrix. A full heatmap requests many values but must still have a tested
  resource policy. Current backed-expression limitations remain explicit until
  supported, not silently materialized.
- Mutation/cache: charts are detached snapshots. Do not write palettes, reorder
  AnnData, or cache by object identity across calls. Reuse extraction within a
  call; validate stored results against available grouping/shape metadata.
  Honor explicit Scanpy snapshots without repeating their computation to check
  freshness. Users recompute trees after changing data/group membership;
  malformed or incompatible results fail without being overwritten.
- Computation: no automatic embedding, ranking, density analysis, or clustering
  rerun. Automatic plot-derived tree computation can use an available matching
  representation, return a local result, and avoid cache writes. A missing
  representation that would trigger hidden PCA requires explicit Scanpy
  preparation first; record this compatibility restriction in M04/M14.

## Completion gates for every slice

A slice can close only for its stated supported subset. Full-family completion
also requires all remaining parameter and method rows to be resolved.

1. **Contract/data:** signature and alias tests plus hand-calculated semantic
   cases; instrument analysis calls, mutations, and allocations. Frozen upstream
   outputs are a second oracle, not the only oracle.
2. **Complete chart:** axes, titles, ticks, label slots, legends, annotations,
   footprints, ordering, trees, and clipping. Register reference/native plot
   areas; keep image exports and overlays in temporary local/CI artifacts and
   metadata in Git. Never commit or push generated test images. Record export DPI,
   logical dimensions,
   DPR, palette bins/interpolation, fonts and browser rasterization. Set measured
   case-specific tolerances; an aggregate image-error score alone is insufficient.
3. **Interactions offered by the slice:** observe gestures, hover contents,
   selection ownership/clearing, zoom, linking, counts, Python membership, widget
   reruns/disposal, and offline HTML. Noninteractive defaults must retain the
   reviewed appearance. Only add interactions after basic reproduction passes.
4. **Resources:** sparse preparation allocations, payload size, render latency,
   interaction latency, and retained memory with recorded machine/browser/runtime.
   Include selected-column workloads and a realistic multi-panel or tile workload;
   publish a tested envelope rather than promising hardware-independent timing.
5. **Workflow/handoff:** real packaged Scanpy data and relevant official tutorial
   calls, provenance, support docs, tests, Ruff, and typing. Fresh-clone validation
   cannot import ignored local research. Update STATUS and clearance decisions.

## Milestone order

Current states and evidence live only in [STATUS.md](STATUS.md#milestones).
The order below favors verified native capabilities and reuse; blocked filled
geometry does not stop diagnostics or graph work.

| ID | Deliverable | Depends on |
| --- | --- | --- |
| M00 | Contract, optional dependency, source layout and progress management | Existing Core/widget |
| M01 | Categorical/continuous UMAP and linked-brush preview | M00 |
| M02 | Shared grouped access and dotplot | M00; reuse M01 access/colors |
| M03 | Matrixplot | M02 shared summaries |
| M04 | Dendrograms and correlation, standalone and attached | Grouped tables from M02/M03 |
| M05 | Heatmap, matrix, clustermap | M02 grouping, M04 trees |
| M06 | Ranking and ranked dot/matrix/heatmap | M02–M05 |
| M07 | Other embeddings, PCA and outstanding UMAP options | M01 |
| M08 | Violin, stacked violin, ranked forms | Grouped access; released filled geometry |
| M09 | Tracksplot and ranked tracks | Grouped access; released filled geometry |
| M10 | Quality-control diagnostics | M00; reusable distributions/scatter |
| M11 | DPT, PAGA, time series and simulation | M05/M07 and native graph/layout checks |
| M12 | Spatial and embedding density | M07; released image support for full spatial |
| M13 | Three native builders and semantic method chains | Each underlying family; can ship incrementally |
| M14 | Parameter closure, exports, versions, docs publication and release | All required families and capability work |

### M00 — foundation and layout

- M00.a: freeze effective signatures/defaults/aliases and the version guard;
  distinguish plotting, builder, and renderer-only entries.
- M00.b: keep optional dependencies lazy, explicit reference generation separate
  from ordinary tests, and synthetic edge fixtures independently interpretable.
- M00.c: place implementation and public imports under
  `genome_spy.integrations.scanpy`, without a compatibility namespace. Test
  base/namespace import isolation and wheel packaging.
- M00.d: maintain the full inventory, milestone/next-work ledger, evidence links,
  and clearance decisions under the shared lifecycle.

Acceptance: a fresh clone locates and validates implementation without ignored
artifacts; no runtime duplication, integration code in `tools/`, or integration
workflows in generic `notebooks/`. This milestone is infrastructure, not full API.

### M01 — UMAP preview and linked selection

Categorical/continuous 2D UMAP reads stored coordinates, raw/layer values,
metadata, masks, components and original identities. Native axes/color guides,
size/order semantics, optional hover/zoom, and native sizing are implemented.
One first-panel interval owner supports linked highlighting, a native count, and
Python `selection_mask` through the ordinary widget. Use the dedicated PBMC
UMAP notebook and frozen semantic/complete-chart/browser/resource checks as
evidence. Its order is basic plotting, linked selection, then customization.

Acceptance: preserve supplied coordinates and independent per-panel color scales;
plain-drag brush example, clear, coincident cells and half-open membership agree
in the chart and Python. No local Core patch or notebook connection task.
This closes a preview only. Remaining normalization, overlays, fonts, 3D,
backed expression, and broader selection modes stay in M07/M14.

### M02 — grouped access and dotplot (plain-chart preview closed)

M02.a–d are verified for the plain-chart preview; see [data evidence](STATUS.md#m02ab-preparation-and-statistics)
and [chart evidence and limits](STATUS.md#m02cd-plain-dotplot-preview).
The public dotplot function includes index-scaled slots and optional summary hover.
Trees, builders and summary selections remain in their named later slices.

- M02.a: reuse compatible accessors for selected expression, grouping keys,
  category order and palettes. Support scalar/list/mapping `var_names`, repeated
  slots and group brackets, `categories_order`, `num_categories`, gene symbols,
  raw/layer and view/sparse cases. Preserve numeric-bin edges and multi-key group
  ordering. Document differing duplicate-label behavior from UMAP.
- M02.b: pure grouped summaries. Apply `log=True` as `log1p` to selected
  observations before thresholding/means. Fraction uses strict
  `value > expression_cutoff` with Scanpy's comparison/count denominator, including
  implicit zeros. Ordinary NaN compares false and remains in that denominator;
  pandas nullable NA follows the pinned nullable-count exclusion. Do not substitute
  `count_nonzero`. `mean_only_expressed`
  changes the mean's denominator, not the fraction's. Check missing-value rules,
  signed values, exact-cutoff values, empty/constant groups and unequal sizes.
  Apply `standard_scale` to means on the specified axis after aggregation,
  preserving constant-row/column behavior.
- M02.c: `_dotplot_chart.py` authors native dot area, color/size guides, group and
  feature axes, brackets, title, `swap_axes`, padding and sizing. Use integer index
  slots and band positions for brackets, retaining Scanpy spacing and repeated labels.
  Offer optional summary hover without changing the initial marks. Check clipped
  `dot_min`/`dot_max`, inferred limits, size exponent and `smallest_dot`, including
  zero/all-equal fractions. Respect supplied `dot_color_df`/builder `dot_size_df`
  labels/order without silently recomputing or rescaling supplied values.
- M02.d: freeze default, reordered, log, scaled, supplied-statistic and repeated-
  slot references; reproduce the core tutorial marker dotplot on PBMC.
  Keep dotplot, matrixplot and heatmap examples in the expression notebook,
  sharing its data/marker setup as those families arrive. Measure
  selected-gene preparation for 100k cells × 20k sparse genes and group×feature
  chart costs. Observe summary hover in both orientations, including clipped dot
  sizes and single-slot axes. Review plain charts before adding summary selection.

Plain-chart preview call (current limits and evidence in STATUS):

```python
chart = gsc.pl.dotplot(
    pbmc, ["CD79A", "MS4A1", "CD3D"], groupby="louvain",
    expression_cutoff=0.0, mean_only_expressed=False, show=False,
)
```

Acceptance: exact summary tables match hand calculations and pinned Scanpy,
size/color legends express the retained statistics, and repeated labels occupy
distinct slots. The first preview may explicitly reject `dendrogram=True` until
M04; it does not close full dotplot coverage or the DotPlot builder.

### M03 — matrixplot

- M03.a: reuse selected expression/group order and mean statistics; do not copy
  dotplot's fraction-specific code. Preserve `log` before aggregation,
  `standard_scale="var"/"group"` min–max order and zero-range behavior.
- M03.b: `values_df` is an authoritative labeled table; test reindexing,
  mismatch/duplicate errors and the distinct supplied-table scaling path.
  In 1.11.5 supplied values bypass log/scaling, keep column and row order, and
  only explicit `categories_order` reindexes rows. Repeated feature multiplicities
  must match the plotted slots; duplicate group labels fail clearly.
- M03.c: `_matrixplot_chart.py` uses native rectangles, actual color scales,
  swapped axes, brackets and per-panel guides. Preserve color bounds and edge
  styling; compare complete charts on the same grouped PBMC marker workflow.
  Reuse native index slots/labels/brackets with zero outer padding, a horizontal
  color guide and optional summary hover. Accept singular scalar `edgecolor` and
  `linewidth`; reject plural aliases that upstream overwrites with defaults.

Target: `gsc.pl.matrixplot(pbmc, markers, "louvain", standard_scale="var", show=False)`.
Acceptance: shared access/mean code is used, table values and ordering are exact,
and tile/guide geometry matches measured references. Trees complete in M04;
builder styling completes in M13.

### M04 — dendrogram and correlation (preview closed)

M04.a–d are verified for standalone trees/correlation and dotplot/matrixplot
attachments; see [scope and evidence](STATUS.md#m04ad-dendrogram-and-correlation-preview).
Later-family attachments remain with M05/M08/M09. Normalization, kwargs and
export compatibility remain in M14.

- M04.a: validate supplied `uns[dendrogram_key]` grouping, linkage, category order,
  correlations and leaf order. Cover multi-key groups, missing/constant profiles,
  ties, reordered categories, malformed/incompatible caches and one/two-group
  limits. Honor cached component/method choices without recomputing profiles.
- M04.b: compute missing group profiles, correlations/distances, linkage and branch
  coordinates in Python. Reuse public upstream computation only when it avoids
  hidden analysis/mutation. `inplace=False` alone is insufficient if Scanpy's
  representation resolver would fit missing PCA. Require an existing matching
  representation or explicit upstream preparation; no silent PCA/embedding fit.
  Keep automatic plot-derived results local, with no new AnnData cache writes.
  The delivered implementation delegates to public sc.tl.dendrogram with
  inplace=False and an explicit existing representation, preventing hidden PCA.
  Automatic computation currently requires resident dense X or X_pca, following
  Scanpy 1.11.5's limits. Never densify expression to bypass those limits.
  Stored trees need no expression/representation access and work with sparse or
  backed AnnData. Read their correlations and geometry directly, including
  nondefault n_pcs/var_names/method results. Do not reimplement group profiles,
  correlations, linkage, layout or freshness detection in the adapter.
- M04.c: a focused tree layout helper feeds native rule marks for top/right/left/
  bottom orientation. Use the same group permutation for dots, tiles, labels,
  brackets, totals and leaf centers. Implement standalone `dendrogram` labels and
  `remove_labels`, plus `correlation_matrix` numbers, bounds and attached tree.
- M04.d: attach to dotplot/matrixplot and later heatmap/tracks/stacked violin;
  supplied coordinates/order are retained. Compare all orientations, ties, swaps
  and resize behavior. Pan/zoom cannot detach a tree from its rows/columns.
  Dot/matrix trees now use native rule geometry projected into fixed index slots,
  with excluded scales/axes. Grouped navigation is optional in M05.e; summary hover
  and resize alignment are verified. No Core changes or prototype geometry are
  required. Reuse these helpers when each later family is implemented.

Targets: `gsc.pl.dotplot(pbmc, markers, "louvain", dendrogram=True, show=False)`
and `gsc.pl.dendrogram(pbmc, "louvain", show=False)`.
Acceptance: Python linkage/leaf geometry independently verified, released native
rules suffice, exact cached results are honored, no analysis rerun or mutation.
Tree fallback requiring missing PCA remains an explicit contract limit to resolve
in M14, not an excuse to declare full automatic compatibility.

### M05 — heatmap, matrix and clustermap

Heatmap M05.a/b is delivered as a bounded preview; see the
[status record](STATUS.md#m05ab-cell-heatmap-preview) and maintained
[heatmap contract](../../docs/integrations/scanpy/index.md#heatmap-compatibility).
It adds one chart module and small functions in the existing grouped data/tree
modules, reusing access, scaling, palettes, feature ordering, labels and branches.
The 250,000-value limit is checked before extraction; the 100k × 50 case tests
rejection without data reads. Larger/chunked transport remains M05.d.
The standalone `matrix` part of M05.b is delivered as a numeric-array preview,
reusing numeric validation, linear color bounds, index slots and labels. Heatmap
adds optional zoom with aligned cell annotations and clipped tree branches;
y-only by default, with both axes explicitly available.
Shared grid interactions are M05.e below. M05.c has a bounded clustermap preview
with public SciPy or supplied linkage, ordered annotation tracks and shared
tiles/branches; see its [status evidence](STATUS.md#m05c--clustermap-preview).
Larger transport remains M05.d; M06 stored ranking and ranked summaries are next.

- M05.a: observation-level heatmap reuses source/group/slot access. Carry one
  explicit observation permutation through values, IDs, category strips, group
  intervals, labels and trees. Test category ties, missing groups, repeated gene
  slots, `show_gene_labels`, swapped axes, `log`, and `standard_scale="obs"/"var"`
  before rendering; grouped means are not a substitute for cell values.
- M05.b: `_heatmap_chart.py` composes tiles, strips, brackets, guides and M04 trees.
  `matrix` accepts the supplied numeric matrix directly with explicit ticks,
  labels, title, finite-range linear normalization and colorbar sizing. This
  preview accepts resident numeric arrays/tables, preserves missing/masked cells
  and rejects color objects, images, sparse/lazy data and mismatched tick counts.
  Heatmap zoom defaults off; explicit zoom keeps strips, boundaries and tree leaves
  aligned, hides offscreen labels, and hides partially visible gene brackets.
- M05.c: `clustermap` computes requested row/column clustering in Python, honors
  supplied linkage and annotation colors, and routes supported clustering kwargs
  explicitly. Do not silently cluster a supplied ordering or densify an unrelated
  expression matrix. Reject unsupported Seaborn/Matplotlib options by name.
  The delivered preview bounds tiles and pairwise distances before expression
  access. Z-score/sample-SD and min–max scaling follow Seaborn, including missing
  constant ranges; display masks do not change distances. Native palette/guide
  differences, unsupported kwargs and fixed navigation remain explicit in the
  maintained contract, with broader options assigned to M14. Do not claim the
  full clustermap family closed from this preview.
- M05.d: test chunked selected-column access and a 100k-cell × 50-marker heatmap;
  record payload/render/memory limits and an explicit over-budget policy. Compare
  complete PBMC tutorial heatmaps with registered strips/tree/label alignment.

- M05.e (verified interaction preview; [evidence](STATUS.md#m05e-shared-grid-interactions)):
  share index navigation and live annotation projection across heatmap,
  matrixplot, matrix and dotplot. Offer opt-in fitted two-decimal values on the
  three tile families and a native row/column crosshair ruler on dotplot. Preserve plotted
  values, repeated slots, color limits, dot sizes, guides and default appearance.
  `zoom=True` uses y-only navigation; explicit `zoom="xy"` enables both axes,
  and `zoom=False` disables navigation. Test locked x domains during y zoom/pan.
  Reuse the prepared tables; interactions must not call Scanpy or extract data.
  Observe dense overview/zoomed text, native contrast including opacity/clipping,
  tooltip access, normal/swapped tree alignment while panning, duplicate-slot
  highlighting, gaps between dots, clearing on plot leave and standalone HTML.
  Run the packaged-PBMC expression notebook and record
  a realistic allocation/payload/browser observation. Keep native API limitations
  and remaining large-data transport debt explicit.

Targets: `gsc.pl.heatmap(pbmc, markers, "louvain", dendrogram=True, show=False)`
and `gsc.pl.matrix(values, xticks=genes, yticks=groups, show=False)`.
Acceptance: value order and all annotations agree on the same permutation;
large inputs have a measured policy without hidden downsampling/aggregation.

### M06 — ranking and ranked summary plots

- M06.a: read the requested stored `rank_genes_groups` key and params, validate
  groups/method/source fields and filtered results, then use public
  `sc.get.rank_genes_groups_df` where equivalent. Never run ranking to fill gaps.
- M06.b: preserve group order, positive/negative rank ordering, `n_genes`, explicit
  `var_names`, symbols, repeated genes across group slots and strict
  `min_logfoldchange` filtering. Validate available scores, log-fold changes and
  adjusted/raw p-values; missing metrics error rather than silently changing them.
- M06.c: implement `ranking` for supplied attributes/dictionaries and
  `rank_genes_groups` rank/score panels. Add ranked dotplot/matrixplot/heatmap by
  delegating to the implemented family charts, not by copying them.
- M06.d: for `values_to_plot`, metric colors and expression fractions remain
  distinct data sources. Verify raw/layer precedence from stored ranking params,
  supplied selected groups and missing/nonfinite statistics.

Target: `gsc.pl.rank_genes_groups_dotplot(pbmc, key="rank_genes_groups", n_genes=3, show=False)`.
Acceptance: frozen stored ranks produce identical slots and labels; hand-checked
rank-statistic colors do not alter expression denominators. Ranked violin/tracks
are deliberately assigned to M08/M09 until their parent chart exists.

### M07 — embeddings, scatter and PCA

- M07.a: extract reusable embedding authoring/access from UMAP for `embedding`,
  `tsne`, `diffmap`, `draw_graph`, `pca` and alias `pca_scatter`. Resolve basis/layout
  names, components/dimensions and explained-variance labels from stored results.
  Missing coordinates error; no neighbors, PCA, t-SNE or force layout rerun.
- M07.b: implement `scatter` x/y/basis selection, observation versus variable
  orientation, per-axis `layers`, labels, palettes and multiple colors. Share
  point/color code while preserving its distinct signature/lookup behavior.
- M07.c: PCA loadings/variance/overview consume stored loadings and variance data;
  preserve component order, `include_lowest`, `n_points`, `n_pcs`, logarithmic
  axes, labels and overview panel composition. Verify the pca_scatter alias target.
- M07.d: complete 2D options currently rejected by UMAP: graph/arrow overlays,
  scale factor, supported marker/style forms, outlines, colorbar positions,
  numeric normalization/center/callable bounds and missing-category schemes.
  Recheck native primitives and add focused tests per option; do not sample
  Matplotlib colors or accept its normalization objects.

Targets: `gsc.pl.embedding(adata, basis="tsne", color="cell_type", show=False)`
and `gsc.pl.pca_overview(adata, show=False)` after explicit Scanpy PCA.
Acceptance: shared points retain source precision, IDs and draw order; PCA
metadata is never fitted implicitly. Track 3D/native typography gaps in M14.

### M08 — violin distributions and stacked violin

- M08.a: shared grouping/expression access feeds Python density estimation with
  pinned bandwidth/kernel/grid, cut/clip, support range, constant/empty groups and
  `density_norm` (plus deprecated `scale`) semantics. Distinguish value-axis
  `log=True` from transforming values before KDE; test upstream behavior.
- M08.b: `_violin_chart.py` renders native filled densities, outlines, inner
  summaries and strip/jitter points. Preserve `order`, group palettes, split/
  multi-panel behavior, widths, legends and axes. Deterministic random tests
  check jitter bounds/identity; do not require upstream random draws to coincide.
- M08.c: `_stacked_violin_chart.py` reuses densities with row colors/scales,
  `standard_scale`, `row_palette`, swaps, y ticks, brackets, totals and M04 trees.
  Ranked violin/stacked wrappers reuse M06 result selection.

Acceptance: densities/integrals/normalization and full chart references pass,
hover identifies actual observations where points represent them, and filled
shapes use a released native capability. Custom sampled-rectangle/polygon trial
recipes are not the production solution. Numeric work may proceed while filled
rendering is blocked.

### M09 — tracksplot and ranked tracks

- M09.a: prepare selected gene tracks in category/observation order, apply the
  correct log/value scaling and baselines, and retain category intervals, palettes,
  tree permutation, feature slots and original IDs.
- M09.b: `_tracksplot_chart.py` authors filled profiles using a released native
  area capability, with brackets, axes and trees. Ranked tracks reuse M06 slots.
  Test isolated peaks, zero/negative values where accepted, uneven groups, repeated
  genes and swapped/unsupported options explicitly.

Acceptance: profiles, baselines and panel extents match references; native zoom
keeps annotations aligned, realistic cell×track costs are measured. Python
preparation alone does not close rendering; experimental filled rectangles are
not an accepted replacement.

### M10 — quality-control diagnostics

- M10.a: `highest_expr_genes` preserves source/layer/symbol rules, per-cell total
  denominators, zero totals, percentage summaries, top-n selection and log axes.
  Reuse distribution authoring after verifying its needed geometry.
- M10.b: `highly_variable_genes` and legacy `filter_genes_dispersion` consume
  supplied result/var fields, preserve selected versus other genes, normalized
  versus raw dispersions/variance, flavor-dependent labels and logarithmic axes.
  No variable-gene selection is rerun for missing results.
- M10.c: `scrublet_score_distribution` reads observed/simulated scores, thresholds
  and batch keys; verify histogram bins, count/density normalization and axis-scale
  aliases. Do not rerun Scrublet or silently pool batches.

Acceptance: hand-checked denominators/bins/ranks plus complete references on real
QC workflows. Upstream deprecated aliases remain visible in the version contract;
upstream deprecation is not a reason to silently drop a pinned public entry.

### M11 — trajectories, graph layouts, time series and simulation

- M11.a: `timeseries`, `timeseries_subplot`, `timeseries_as_heatmap` accept supplied
  matrices/time values, variable order, highlights, labels, color maps, limits and
  markers. Use shared heatmap or dedicated line/time authoring as appropriate;
  verify a supported released path primitive rather than disconnected point
  approximations. `sim` reads supplied simulation outputs and preserves time
  truncation, `shuffle`, markers and heatmap choice without rerunning simulation.
- M11.b: `dpt_groups_pseudotime` and `dpt_timeseries` consume stored DPT groups,
  order, pseudotime and highlights, with heatmap/series modes and exact alignment.
  Missing DPT analysis errors; no trajectory inference in plotting.
- M11.c: `paga` consumes stored connectivities/transitions; Python graph layouts
  may be computed for plotting only when positions were not supplied. Preserve
  `pos`, threshold inclusion, roots, components, node-size powers, normalization,
  solid/dashed/directed edges, labels and scales. Explicitly handle `plot`,
  `add_pos` and `export_to_gexf` side effects; user-requested writes only.
- M11.d: `paga_adjacency`, `paga_compare` and `paga_path` reuse matrix/embedding/
  graph authoring. Preserve supplied adjacency/tree/positions, panel alignment,
  ordered paths, `n_avg` window/end behavior, annotations, source selection and
  `normalize_to_zero_one`. Specify native return shapes for `return_data` and
  no-plot modes instead of returning fake axes.

Acceptance: hand-sized graphs/path arrays cover thresholds, direction, duplicate
edges, gaps and smoothing; saved coordinates/arrays are honored. No hidden PAGA
or DPT recomputation. Observe graph hover/zoom and verify cell selection only
where marks represent cells; nodes/edges carry group/edge IDs instead.

### M12 — spatial and embedding density

- M12.a: `embedding_density` reads the explicitly prepared `obs` density key and
  `uns` params for basis/group; preserve supplied groups, background/foreground
  dots, coordinate choice, bounds, color scales and multiple panels. Never rerun
  `sc.tl.embedding_density` on missing/stale input.
- M12.b: `spatial` reuses point/color access but resolves library/image keys,
  spot diameter, scale factors, crop, coordinate origin/aspect, background image,
  alpha and black/white image behavior. Image decode/coordinates are independently
  tested; use a released native raster capability for the actual background.
- M12.c: validate a reproducible Scanpy spatial workflow with licensed small
  imagery and metadata; do not vendor tutorial datasets before provenance review.

Acceptance: image pixels, spot centers/diameters and crop register together at
multiple zoom levels; library ambiguity errors clearly. Scatter-only spatial
support is a preview, not completed spatial compatibility. Density can ship
independently of the image capability blocker.

### M13 — native plot builders and useful chains

Implement `DotPlot`, `MatrixPlot`, `StackedViolin` incrementally with their existing
family data and chart code. Builders need small explicit state only for actual
upstream methods; no placeholder base class or generic method dispatcher.

| Method group | Native contract and validation |
| --- | --- |
| `add_dendrogram`, `add_totals`, `swap_axes` | Preserve arguments/defaults, return self where upstream chains, and alter the shared ordering/layout consistently. Test totals sorting/colors and incompatible decorations. |
| `style` | Dot color-on-dot/square, dot limits/exponent/edges/grid/padding; matrix colors/edges; stacked strip/jitter/row palettes/density/limits. Preserve method names/aliases, clearly reject unsupported forms. |
| `legend` | Preserve semantic guide visibility, titles, sizes and widths with native scales/guides; compare after a chain, not just each setter separately. |
| Native delivery | Document chart extraction/display/HTML/JSON methods and mutation versus snapshot timing; test repeated rendering and further chaining. |
| Matplotlib-only methods/attributes | `get_axes`, figure/Axes attributes and artist styling fail with guidance. Decide `make_figure`, `show(return_axes=...)` and `savefig` boundaries explicitly; do not make empty no-op methods. |

Target shape (future): `gsc.pl.DotPlot(pbmc, markers, "louvain").add_dendrogram().swap_axes().style(dot_edge_color="black")`.
Acceptance: chained and equivalent functional plots share statistics/chart code,
identical supported semantics, and explicit renderer boundaries. Record method
coverage separately from the three constructor entries in STATUS.

### M14 — compatibility closure and released capabilities

Recheck the installed schema/runtime at the start of each affected slice and each
Core upgrade. As audited here, Core **1.0.0** exposes `rect`, `point`, `rule`,
`tick`, `text`, `link`, and `arrow`, with no filled-area, raster-image, or 3D
projection primitive in the bundled schema. See the status capability ledger.
Python linkage/KDE/graph computation cannot supply a missing renderer primitive.

- M14.a: adopt released Core capabilities for filled densities/tracks, paths,
  images and 3D as required; review tree/axis alignment, typography, outlines,
  missing colors and numeric normalization individually. No local bundle patches.
  Real Core bugs need an upstream reproducer and observed evidence.
- M14.b: adopt improved faceting after release. Isolate composition changes;
  recheck axes/gap/plot zoom routing, guides, sizing, brush owner/scope, counts,
  reruns/disposal and snapshots. Do not promise an unreleased API shape.
- M14.c: close backed/lazy selected-expression access, aliases/kwargs, supported
  marker/legend forms, return modes, tree fallback, save/export and every meaningful
  parameter limit. Maintain a per-family parameter/method matrix as each family
  is added; unexplained omissions block full compatibility claims.
- M14.d: test the oldest/newest declared Scanpy versions plus pinned scientific
  dependencies, signatures/defaults, fresh installs, wheel/namespace imports,
  semantic/reference/browser/resource suites and deprecation behavior.
  Only then widen `scanpy==1.11.5` to the tested range.

Acceptance: every inventory entry is verified or an explicit renderer-specific
exception; parameter and method debt is resolved, not hidden by a function count.
If native capability gaps remain, publish a precisely scoped preview rather than
calling the integration a complete drop-in replacement.

## Documentation and release

M14.e designs the integrations landing page and one workflow page before choosing
and implementing notebook rendering. Keep the general visualization skill and
focused agent guides general; Scanpy policy/tutorials belong in this integration.

```text
Integrations
  Overview: actual libraries, status, tested versions
  Scanpy
    Start here: analysis ownership, install, first replacement
    Compatibility: plots, parameters, methods, returns, exports, limits
    UMAP workflow: basics, linked selection, customization
    Expression workflow: dotplot, matrixplot, heatmap
    API reference
```

Review navigation, status/version labels, code visibility, chart placement,
download/run links, narrow-screen/large-chart behavior and Python-only retrieval.
No empty library cards. Use the dedicated UMAP notebook and a shared expression
notebook for dotplot, matrixplot and heatmap examples under this workspace. Each
notebook runs independently with explicit pinned preparation and reusable native
chart artifacts. Add examples only when their plotting APIs are implemented. The
ordinary Sphinx build must not run unbounded analysis or downloads. A static page
can run hover/brush/count; Python subset retrieval requires a live kernel.

Adapt the official [core plotting tutorial](https://scanpy.scverse.org/en/stable/tutorials/plotting/core.html)
and [customization tutorial](https://scanpy.scverse.org/en/stable/tutorials/plotting/advanced.html)
as families arrive. Keep upstream analysis steps explicit; replace the supported
plotting calls. The tracked pinned signature inventory and installed 1.11.5 source
remain authoritative where the moving stable tutorials differ.

Release acceptance: one rendered real tutorial page and working notebook download,
observed native interactions, offline delivery, reproducible artifacts and reviewed
provenance; full core API and parameter/method coverage evidence; tested resource
limits and version range. Update STATUS with the release and residual scope before
clearing any completed working plans. Another library starts with its own small
contract, inventory and workflow, reusing this layout without assuming Scanpy's
AnnData semantics apply to it.
