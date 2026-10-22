# Scanpy implementation plan

The destination is the full public `scanpy.pl` plotting surface at the supported
Scanpy version. This is a delivery roadmap, not a claim that those plots already
exist. Read [STATUS.md](STATUS.md) for implemented behavior, the next slice,
blockers, the 50-entry inventory, validation evidence, and clearance decisions.
Its [current queue](STATUS.md#current-work-queue) is the sole next-work list;
this plan defines deliverables and acceptance criteria.
When multiple chats share the checkout, reconcile the current queue with recent
commits and uncommitted work before starting another slice. Record completion
and verification in STATUS rather than adding a second queue here.
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

Acceptance: preserve supplied coordinates and independent per-panel color scales.
With zoom enabled, Shift-drag brushing, clearing, coincident cells and half-open
membership agree in the chart and Python. No local Core patch or notebook connection task.
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
- M04.c: a focused tree layout helper feeds native orthogonal links for top/right/left/
  bottom orientation. Use the same group permutation for dots, tiles, labels,
  brackets, totals and leaf centers. Implement standalone `dendrogram` labels and
  `remove_labels`, plus `correlation_matrix` numbers, bounds and attached tree.
- M04.d: attach to dotplot/matrixplot and later heatmap/tracks/stacked violin;
  supplied coordinates/order are retained. Compare all orientations, ties, swaps
  and resize behavior. Pan/zoom cannot detach a tree from its rows/columns.
  All attached trees use the shared native orthogonal-link renderer and aligned
  surround tracks, with viewport height fitting. Grouped navigation is optional
  in M05.e; summary hover and resize alignment are verified. No Core changes or prototype geometry are
  required. Reuse these helpers when each later family is implemented.

Targets: `gsc.pl.dotplot(pbmc, markers, "louvain", dendrogram=True, show=False)`
and `gsc.pl.dendrogram(pbmc, "louvain", show=False)`.
Acceptance: Python linkage/leaf geometry independently verified, released native
orthogonal links suffice, exact cached results are honored, no analysis rerun or
mutation.
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
Larger transport remains M05.d; stored ranking and ranked summaries belong to M06.

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
  Native annotation-strip hover passes on Core 1.2; M05.f still owns placing the
  bands inside their own track viewports and verifying the migrated layout.
- M05.c: `clustermap` computes requested row/column clustering in Python, honors
  supplied linkage and annotation colors, and routes supported clustering kwargs
  explicitly. Do not silently cluster a supplied ordering or densify an unrelated
  expression matrix. Reject unsupported Seaborn/Matplotlib options by name.
  The delivered preview bounds tiles and pairwise distances before expression
  access. Z-score/sample-SD and min–max scaling follow Seaborn, including missing
  constant ranges; display masks do not change distances. Native palette/guide
  differences and unsupported kwargs remain explicit in the
  maintained contract, with broader options assigned to M14. Do not claim the
  full clustermap family closed from this preview.
  Observation category strips retain names/order/palettes and use their own native
  categorical legend. M05.f retains the native strip-viewport migration; legacy
  strip hover already passes on Core 1.2. Explicit CSS tracks do not invent
  category names.
- M05.d: test chunked selected-column access and a 100k-cell × 50-marker heatmap;
  record payload/render/memory limits and an explicit over-budget policy. Compare
  complete PBMC tutorial heatmaps with registered strips/tree/label alignment.

- M05.e (verified interaction preview; [evidence](STATUS.md#m05e-shared-grid-interactions)):
  share index navigation and live annotation projection across heatmap,
  matrixplot, matrix, clustermap and dotplot. Offer opt-in fitted two-decimal values on the
  tile families and a native row/column crosshair ruler on dotplot. Preserve plotted
  values, repeated slots, color limits, dot sizes, guides and default appearance.
  `zoom=True` uses y-only navigation; explicit `zoom="xy"` enables both axes,
  and `zoom=False` disables navigation. Test locked x domains during y zoom/pan.
  Reuse the prepared tables; interactions must not call Scanpy or extract data.
  Observe dense overview/zoomed text, native contrast including opacity/clipping,
  tooltip access, normal/swapped tree alignment while panning, duplicate-slot
  highlighting, gaps between dots, clearing on plot leave and standalone HTML.
  Clustermap's two trees, color tracks and visible ticks must remain aligned and
  clipped along the scrolling direction under both zoom modes and panning.
  Run the packaged-PBMC expression notebook and record
  a realistic allocation/payload/browser observation. Keep native API limitations
  and remaining large-data transport debt explicit.
- M05.f (released layout available through M14.b): move heatmap and clustermap
  category bands into their own aligned track viewports, then verify native hover.
  The current adapter draws these marks beyond the matrix viewport using offsets
  or coordinates outside 0–1 with clip="never". That layout choice is adapter debt;
  changing Core picking policy is not a prerequisite for an in-bounds heatmap.
  [PR #587](https://github.com/genome-spy/genome-spy/pull/587) reproduces that
  out-of-bounds interaction behavior, but is not a dependency of this slice.
  After migrating, observe both heatmap orientations and clustermap before/after
  zoom, pan and resize. Assert bands lie inside their own viewports, retained
  category identity/palettes and native legends, and normal tile/strip hover.
  Preserve the now-passing legacy hover coverage and add checks for the new
  viewport bounds and gapped layout. Remove obsolete layout helpers/notices only
  after observation. No patched bundle or custom hover listeners.

Targets: `gsc.pl.heatmap(pbmc, markers, "louvain", dendrogram=True, show=False)`
and `gsc.pl.matrix(values, xticks=genes, yticks=groups, show=False)`.
Acceptance: value order and all annotations agree on the same permutation;
large inputs have a measured policy without hidden downsampling/aggregation.

### M06 — ranking and ranked summary plots

M06.a–c now have a stored-result preview: ranking/score labels and expression-color
wrappers are implemented. M06.d adds stored statistic colors to the same dotplot
and matrixplot paths. Filtered marker lists
work; nonfinite/missing score-panel labels currently error. Track this limit and
native typography/guide differences in M14 rather than claiming full-family closure.

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
  supplied selected groups and missing/nonfinite statistics. Implemented preview:
  six metrics, repeated slots/symbols, all stored group rows and parent scaling.
  Missing pairs and nonfinite colors reject explicitly; M14 owns broader parity.

Target: `gsc.pl.rank_genes_groups_dotplot(pbmc, key="rank_genes_groups", n_genes=3, show=False)`.
Acceptance: frozen stored ranks produce identical slots and labels; hand-checked
rank-statistic colors do not alter expression denominators. Ranked violin/tracks
are deliberately assigned to M08/M09 until their parent chart exists.

### M07 — embeddings, scatter and PCA

Named embeddings, generic bases, PCA variance labels, selection retrieval and
scatter share the existing data/chart/style/interaction path. Slice states,
commit evidence and unmet verification gates live in the
[status ledger](STATUS.md#current-work-queue).

- M07.a: extract reusable embedding authoring/access from UMAP for `embedding`,
  `tsne`, `diffmap`, `draw_graph`, `pca` and alias `pca_scatter`. Resolve basis/layout
  names, components/dimensions and explained-variance labels from stored results.
  Missing coordinates error; no neighbors, PCA, t-SNE or force layout rerun.
- M07.b ([contract and evidence](STATUS.md#m07b-scatter)): `scatter` x/y/basis selection, observation versus variable
  orientation, per-axis `layers`, labels, palettes and multiple colors. Share
  point/color code while preserving its distinct signature/lookup behavior.
  Public AnnData vector access reads each selected source once without a full
  transpose. Four native controls expose hover, zoom and dimensions; numeric
  axes and variable hover use the shared renderer. Preserve exact X_ basis lookup,
  diffusion-column skipping, raw/layer rules and legacy painting order.
  Complete references cover both orientations, palettes, raw/layer and literal
  colors. Remaining margins, on-data labels, highlights, markers and storage
  options remain M07.d/M14; the preview does not close the whole family.
- M07.c: PCA loadings/variance/overview consume stored loadings and variance data;
  preserve component order, `include_lowest`, `n_points`, `n_pcs`, variance-score
  transformations, labels and overview panel composition. Start with a loadings increment:
  `gsc.pl.pca_loadings(pca_genes, components="1,2", include_lowest=True, n_points=20, show=False)`.
  For packaged PBMC, `pca_genes = pbmc[:, pbmc.var["highly_variable"]]` selects
  the genes with stored loadings; the other rows contain NaN and must not be
  silently dropped or replaced by analysis.
  Reuse the ranking renderer where equivalent. Test supplied `varm["PCs"]` and
  gene labels, reversed components, signed/tied loadings, omitted lower ranks,
  limits and missing results; never run PCA. Variance and overview now reuse these
  parents; their verified scope and remaining limits live in STATUS.
  Loadings acceptance: default components are 1–3 and default rank count is
  min(30, n_vars); preserve top-only's extra label, repeated components/labels,
  odd high/low splits and selected-column access. Test resident loadings on sparse
  expression, views and backed AnnData without reading X. Missing/nonfinite or
  unavailable results fail by name. Reuse rank chart references, hover/HTML and
  a realistic multi-panel resource workload; add a packaged-data notebook example.
  A single component should render normally despite pinned Scanpy's indexing bug.
  Variance acceptance: `gsc.pl.pca_variance_ratio(pbmc, n_pcs=10, log=True,
  show=False)` reads `uns["pca"]["variance_ratio"]`. Preserve `n_pcs=30`,
  `log=False`, numbered PC labels, NumPy sorting/ties and top-only's extra label.
  Scanpy applies a natural logarithm to scores before ranking; it does not use a
  logarithmic axis. Keep float32 log rounding before plotting conversion.
  Missing results and nonpositive log inputs need named errors,
  with no PCA computation. Test stored ordering, truncation, bounds, public
  delivery, references, hover/HTML, resources and the notebook. Overview composes
  both diagnostics with the existing PCA chart, without another data/chart module.
  Overview acceptance: `gsc.pl.pca_overview(pca_genes, color="louvain", show=False)`
  reuses `pca`, `pca_loadings` and `pca_variance_ratio` with their existing defaults.
  Scanpy opens the three plots in that order; compose the native results vertically
  and display once. Forward supported PCA plotting kwargs only to the embedding,
  keeping loadings/variance defaults; reject unsupported kwargs before any output.
  Test parent-chart equivalence, supplied coordinates/results, native scale/guide
  independence, nested data/configuration, show/save, hover and notebook/HTML
  delivery. Missing or nonfinite inputs retain each parent's explicit errors;
  never filter genes or run PCA silently. Complete resource gates for the composed
  workload before closing the overview increment.
  The pca_scatter alias belongs to M07.a's existing signature/identity evidence.
- M07.d: complete the remaining 2D options rejected by UMAP: graph/arrow overlays,
  scale factor, supported marker/style forms, outlines,
  numeric normalization/center/callable bounds and missing-category schemes.
  The outline increment retains `add_outline=False` (None also disables it),
  `outline_width=(0.3, 0.05)` and `outline_color=("black", "white")`. Render two
  opaque point layers behind the foreground, preserving relative area, marker
  geometry, supplied/reordered sizes, missing observations and draw order.
  With outlines, an omitted alpha becomes 0.7; explicit alpha, including None,
  keeps its upstream meaning. Reuse the existing point interactions; backgrounds
  have no tooltips, and all layers follow the same brush, count and stable IDs.
  Share one source/sort per panel; preparation and cached analysis stay unchanged.
  Verify Scanpy numerical geometry/opacity, registered isolated/overlapping
  marks, dot/circle markers, custom widths/colors/edges, native guides,
  hover/zoom/brush and offline HTML. Run the packaged UMAP notebook and measure
  a representative multi-panel payload/render/memory workload before closure.
  Recheck native primitives and add focused tests per option; do not sample
  Matplotlib colors or accept its normalization objects.
  The colorbar-placement contract covers `colorbar_loc=None` and all four sides
  through native guide orientation, preserving categorical guides, multi-panel
  bounds, collected/native configuration overrides, hover/zoom and transported
  records. Its [completed increment](STATUS.md#m07d-native-colorbar-placement)
  does not alter scatter's distinct signature or resolve C11's categorical
  multi-column extent bug.
  Callable-bound acceptance: `gsc.pl.umap(pbmc, color=["CD79A", "MS4A1"],
  vmin=np.nanmin, vmax=lambda values: np.nanpercentile(values, 99), show=False)`
  evaluates each numeric panel independently. Preserve scalar, singleton-list and
  per-panel-list forms, masks, missing values and `sort_order` in callback inputs.
  Evaluate once per bound/panel in Python; pass a copy so callbacks cannot change
  plotted measurements, other bounds or AnnData. Require finite real scalar
  results, retain callback exceptions and the existing lower/upper validation and
  constant-range behavior. Categorical panels skip callbacks. Compare inputs and
  limits against public Scanpy, reuse complete numeric charts and native
  interactions, run the packaged UMAP workflow and measure callback preparation
  overhead without full expression-matrix reads. The
  [delivery record](STATUS.md#m07d-callable-color-bounds) retains evidence;
  Centered-color acceptance: reuse this resolver for `vcenter=None`, numbers,
  percentiles, callables and singleton/per-panel lists. Match Scanpy's two linear
  slopes around the center through a native three-value domain (equivalent to
  `domainMid`), retaining source values. Automatic limits expand symmetrically
  when all values lie on one side; explicit limits must strictly enclose the
  center. Preserve constant colors with/without a guide, masks, callback inputs,
  clipping and numeric guide positions. Compare public Scanpy limits and painted
  points, including asymmetric ranges, and verify native hover/zoom/brush/HTML,
  packaged notebook execution and a realistic resource workload. The
  [centered-color record](STATUS.md#m07d-centered-embedding-colors) retains evidence.
  Matplotlib normalization objects remain outside the supported boundary.
  Stored-edge acceptance: `gsc.pl.umap(pbmc, color="louvain", edges=True,
  show=False)` reads stored connectivities, with default/custom neighbor keys
  and legacy/current storage precedence. Reuse NetworkX's undirected ordering
  rather than reimplementing sparse edge deduplication. Preserve asymmetric
  entries, sparse zeros, stable cell IDs and endpoint padding. Require resident
  NumPy/SciPy graph data, finite values and matching shape; never compute
  neighbors or a new embedding. Render native rules beneath points/outlines,
  using shared cell-coordinate lookups and native axes/navigation. The initial
  scope is the first two components, scalar CSS colors and finite nonnegative
  widths in points; other pairs, self-loops and per-edge/numeric colors must
  fail clearly. Test graph order/styles against public Scanpy on stored 2D
  positions, views/backed access without densification, inactive/empty graphs,
  complete-chart overlays, stroke coverage, hover/zoom/brush/HTML and resources.
  Keep explicit notebook sizes smaller while retaining the public size default.
  The [edge delivery record](STATUS.md#m07d-stored-neighbor-graph-edges) owns evidence;
  remaining edge forms retain M07.d/M14 owners.
  Square-marker acceptance: `marker="s"` maps to native square points in shared
  embeddings, PCA overview and scatter; existing scalar/per-panel broadcasting,
  size units, missing values, outlines and native legend symbols are retained.
  Verify occupied square corners as well as side lengths against Scanpy exports,
  then test hover, linked brushing, zoom and HTML through the shared helpers.
  Run the packaged notebook and a representative multi-panel resource comparison.
  The [square-marker record](STATUS.md#m07d-square-markers) owns delivery evidence.
  Diamond-marker acceptance: `marker="D"` uses native diamonds with Scanpy's
  √2 path-width conversion, including outlines and scalar/per-panel inputs.
  Share marker definitions across validation, points and guide sizing. Category
  keys follow each panel's marker shape through native legend inheritance;
  this deliberately differs from Scanpy's circular embedding keys. Compare sizes
  in Scanpy's units. Verify plain/stroked diamond bounds and
  occupied area, hover/brush/zoom/HTML, unchanged data, the packaged workflow
  and a representative resource workload. Do not enable thin diamonds or other
  markers merely because a similarly named native shape exists. The
  [diamond-marker record](STATUS.md#m07d-diamond-markers) owns delivery evidence.
  Triangle audit: compare `"^"`, `"v"`, `"<"`, `">"` with their native shapes,
  using Scanpy paths and rendered footprints with/without strokes. Enable them
  through the shared marker table only if both paths and paint match; scalar
  resizing must not hide different aspect ratios. The
  [audit record](STATUS.md#m07d-triangular-marker-audit) retains the native gap
  and a strict expected-failure check. Support stays blocked by C14 until a
  released native shape or aspect control preserves Scanpy's geometry.

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

Prioritize new plot families over remaining marker-shape details; those stay in
M14's compatibility backlog. Start M10.b with stored-statistic scatter panels,
then M10.a's highest-expression summaries and M10.c's histograms. M08/M09 keep
their native filled-geometry gate; this order does not close those milestones.

- M10.a: `highest_expr_genes` preserves source/layer/symbol rules, per-cell total
  denominators, zero totals, percentage summaries, top-n selection and log axes.
  Reuse public `sc.pp.normalize_total(target_sum=100, inplace=False)` on a
  metadata-free AnnData shell, preserving caller views. Reuse shared resident
  source checks; densify only one selected column at a time. Native rect/rule/
  point marks show quartiles, 1.5-IQR whiskers and outliers with gene band labels.
  Verify reverse-argsort ties, zero-cell denominators, source/layer precedence,
  linear summaries on log axes, complete registered charts and sparse resources.
  Keyword-only hover and percentage-axis zoom keep initial statistics unchanged.
  The PBMC3k workflow uses counts, not scaled PBMC68k expression. Ambiguous
  labels, backed/lazy counts and forwarded styling remain explicit M14 limits.
- M10.b: `highly_variable_genes` and legacy `filter_genes_dispersion` consume
  supplied result/var fields, preserve selected versus other genes, normalized
  versus raw dispersions/variance, flavor-dependent labels and logarithmic axes.
  No variable-gene selection is rerun for missing results.
  Accept AnnData.var with stored hvg flavor, supplied DataFrames and legacy record
  arrays. Preserve the exact flavor lookup and selection-field switch from
  Scanpy 1.11.5, group draw order and log limits (both panels use raw-statistic y
  limits). Keep one native collected bottom legend. Reuse existing numeric,
  identity and coordinate-limit helpers; a dedicated chart module owns the two
  point panels. Test metadata-only views/backed data, missing pairs, duplicate
  labels, native hover/per-panel zoom, complete references, the packaged notebook
  and a large gene-metadata workload. Reject unsupported log bounds explicitly.
- M10.c: `scrublet_score_distribution` reads observed/simulated scores, thresholds
  and batch keys; verify histogram bins, count/density normalization and axis-scale
  aliases. Reuse NumPy histogram counts and the shared numeric/coordinate-domain
  helpers; retain the 50 fixed edges and separate in-range density denominators.
  Read `batched_by`/`batches` in category order, including missing-label behavior;
  never pool batches or recompute Scrublet. Native rectangles and full-height
  threshold rules use independent density scales within each pair and across
  batches. Offer populated-bin hover and optional independent score-axis zoom.
  Verify linear/log modes, bin boundaries, missing/out-of-range scores, thresholds,
  constants, read-only views/backed metadata, registered geometry/overlays and a
  large stored-score workload with forbidden expression access. The PBMC3k
  notebook computes Scrublet explicitly before plotting. Other scale modes,
  unused batch categories and physical typography/export remain explicit M14
  limits. Do not silently map symlog/logit to a different native transform.

Acceptance: hand-checked denominators/bins/ranks plus complete references on real
QC workflows. Upstream deprecated aliases remain visible in the version contract;
upstream deprecation is not a reason to silently drop a pinned public entry.

### M11 — trajectories, graph layouts, time series and simulation

- M11.a heatmap increment: `timeseries_as_heatmap(X, *, var_names=(),
  highlights_x=(), color_map=None)` reuses supplied numeric matrix validation,
  native tiles/labels/color guide and shared zoom/value helpers. Preserve the
  transpose, first variable at the bottom, center-cropped limits, fractional
  highlight positions and singleton limits. No sorting, normalization, trajectory
  inference or simulation runs. Native defaults use viridis and a 372 × 616-pixel
  plot area; dash lengths round to native whole pixels. Resident 2D numeric arrays,
  sequences and tables are supported; sparse/lazy inputs, infinities, all-missing
  data and color objects error. Ordinary label sequences work in addition to the
  pinned helper's array form. Added show/save follow the native chart contract.
  Acceptance: independent data/limit tests, complete registered reference charts
  including singleton axes, observed hover/zoom/pan/fitted values/offline HTML,
  the packaged-PBMC expression workflow and a measured resident-array resource check.
  This increment does not close the point/subplot helpers or the full M11 milestone.
- M11.a point increment: the pinned `timeseries` and `timeseries_subplot` call
  scatter rather than line plotting. Preserve this behavior with native points;
  C04's connected-path review is not a dependency of these two helpers. Support
  multiple variables, categorical single-variable subsets and continuous single
  variables, preserving supplied time/order, point masks, sorted category order,
  finite color limits, labels, highlights, explicit x limits and y ticks. Default
  native colors use Scanpy's public Vega 10 palette; global Matplotlib settings
  are outside the rendering boundary. Use shared numeric, point-shape, color,
  navigation and native dashed-highlight helpers. Verify data separately from
  complete point footprints/guides, hover/zoom, the PBMC workflow and resources.
  Preserve the 6-point² default area and one-point face-colored edge. Native
  guides collect below the plot; fonts/ticks and global styles have the same
  explicit renderer boundary as other previews. Completion evidence is retained
  in [STATUS](STATUS.md#m11a-supplied-time-series-points).
  Per-subset marker differences, repeated legend labels and broader storage
  remain explicit M14 restrictions.
- M11.a subplot increment: expose `timeseries_subplot` with the pinned explicit
  plotting arguments/defaults, omitting Matplotlib `ax`. Reuse the same preparation,
  renderer and native delivery; errors name the requested entry. The default
  native subplot area is 496 × 369.6 pixels at 100 logical pixels/inch. Native
  `hconcat`/`vconcat` replaces current-figure mutation; explicit independent scale
  and guide resolution supports panels with different color modes. Acceptance:
  pinned signature/default and semantic comparisons, complete chart references,
  observed independent hover/zoom/pan and offline composition, a composed PBMC
  notebook example and a measured two-panel resource workload. This increment
  closes the subplot preview; simulation, DPT/PAGA and full M11 remain open.
- M11.a: `timeseries`, `timeseries_subplot`, `timeseries_as_heatmap` accept supplied
  matrices/time values, variable order, highlights, labels, color maps, limits and
  markers. Use shared heatmap or point authoring according to the pinned callable;
  review connected paths only for functions that actually connect samples.
  `sim` reads supplied simulation outputs without rerunning simulation. The pinned
  helper never truncates X: `tmax_realization`, then `uns['tmax_write']`, then
  `n_obs` chooses boundary spacing and one-based realization ticks. Include a
  partial final realization. Points preserve the [0, 1.25 * n_obs] x limits;
  heatmaps keep the time-series crop. Shuffle matches the seed-1 legacy NumPy
  permutation using a local RandomState and always draws points, including when
  `as_heatmap=True`. Reuse both time-series renderers and the shared native side
  tracks for named numeric ticks. Reject backed/lazy/sparse expression before
  loading or densifying; keep parent marker/palette limits explicit. Acceptance:
  compare metadata precedence, ticks, values, limits, boundaries and permutation
  independently, prove input/global RNG preservation, register complete charts
  and observed hover/zoom/label alignment/offline export, run a packaged simulation
  notebook example and measure a realistic resident simulation workload.
- M11.b: `dpt_groups_pseudotime` reads stored groups, rank coordinates,
  pseudotime and highlights. `dpt_timeseries` indexes X using the distinct saved
  `dpt_order_indices` vector, with heatmap/point modes and exact alignment.
  Missing DPT analysis errors; no trajectory inference in plotting.
  The groups increment composes two existing point panels: categorical codes
  against stored order (sorted observed-group palette; explicit code ticks below
  five categories), then pseudotime against that order with ticks at 0/1.
  Keep unused category codes, mask nonfinite pseudotime only in its panel, and
  preserve every supplied rank/boundary. Read observation/uns metadata only,
  including from backed data. Reuse time-series coordinate validation, preserving
  global ranks and saved boundaries in filtered/reordered views. Native hover,
  independent navigation and 496 × 168-pixel per-panel defaults reuse the existing
  helpers. Verify masks, category/paint order, palettes, markers, defaults, read-only
  behavior, complete registered panels, observed navigation, workflow and resources.
  The pinned parent entry fails on pandas Series indexing; use its public
  time-series component calls with NumPy codes for baseline verification, and
  retain the direct parent-entry comparison as an open upstream gate.
  The expression increment reads resident dense X only, never raw/layers, and
  applies saved row indices verbatim using NumPy semantics. Missing fields,
  invalid/stale indices and unsupported backed/lazy/sparse storage error; no
  sorting, remapping or DPT recomputation runs. Gene-only views work with stored
  indices. Both modes label x as "dpt order" and retain the saved boundaries.
  Heatmaps reuse the transposed/cropped matrix renderer and requested native
  scheme; points retain `[0, 1.3 * n_obs]` limits, native series guides and marker
  semantics. `marker` is inactive in heatmap mode and `color_map` is inactive in
  point mode, as upstream. Shared hover/navigation, fitted heatmap values and
  dimensions add no new rendering path. Acceptance: direct public Scanpy
  comparisons of values/order/limits/labels/colors, missing-input and mutation
  guards, registered chart/overlay checks, observed hover/zoom/pan/offline HTML,
  explicit-analysis notebook execution and measured resident-profile resources.
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
  The bounded native preview reuses embedding preparation/rendering and filtered
  point layers for under/in/over-range colors. Its YlOrRd default selects native
  yelloworangered stops; shared-palette fidelity uses viridis. Reject unsorted
  points spanning those layers instead of changing their overlap order. Broader
  categories, missing-density forms and unsorted mixed ranges retain M14 owners;
  [STATUS](STATUS.md#m12a-stored-embedding-density) records verification and limits.
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
Core upgrade. The adopted Core **1.2.0** exposes `rect`, `point`, `rule`,
`tick`, `text`, `link`, and `arrow`, with no filled-area, raster-image, or 3D
projection primitive in the bundled schema. See the status capability ledger.
Python linkage/KDE/graph computation cannot supply a missing renderer primitive.

- M14.a: adopt released Core capabilities for filled densities/tracks, paths,
  images and 3D as required; review tree/axis alignment, typography, outlines,
  missing colors and numeric normalization individually. No local bundle patches.
  Real Core bugs need an upstream reproducer and observed evidence.
  C11 retains a minimal native legend regression: Core 1.2 clips later columns
  of vertical symbol legends. Recheck a released fix before automatic category-
  guide fitting; keep M07.a/b's complete-chart gate open independently of passed
  resource checks.
- M14.b: adopt the released container layout and improved faceting through the
  wrapper's normal runtime/schema-generation path. The merged
  [container refactor #581](https://github.com/genome-spy/genome-spy/pull/581) and
  upstream [surround design](https://github.com/genome-spy/genome-spy/blob/master/docs/grammar/composition/surround.md)
  inform the migration. Core 1.2.0 and the generated `gs.surround()`/`gs.facet()`
  APIs are now adopted. The [clustered heatmap example](../../docs/examples/clustered_heatmap.py)
  reproduces the published upstream specification; use it as the native layout
  reference without patching the bundle or bypassing generated types.
  Use the focused increments and required group gaps below. Facet/embedding
  changes remain a separate increment: recheck axes/gap/plot zoom routing,
  brush owner/scope, counts, reruns/disposal and snapshots rather than bundling
  them into the expression-grid migration.
- M14.c: close backed/lazy selected-expression access, aliases/kwargs, supported
  marker/legend forms, return modes, tree fallback, save/export and every meaningful
  parameter limit. Maintain a per-family parameter/method matrix as each family
  is added; unexplained omissions block full compatibility claims.
- M14.d: test the oldest/newest declared Scanpy versions plus pinned scientific
  dependencies, signatures/defaults, fresh installs, wheel/namespace imports,
  semantic/reference/browser/resource suites and deprecation behavior.
  Only then widen `scanpy==1.11.5` to the tested range.

Acceptance for M14 as a whole: every inventory entry is verified or an explicit
renderer-specific exception; parameter and method debt is resolved, not hidden
by a function count. If native capability gaps remain, publish a precisely scoped
preview rather than calling the integration a complete drop-in replacement.

#### M14.b native grid layout and group gaps

The released API replaces the adapter's outside-viewport overlays. The center
owns tiles/dots and fitted values; `gs.surround` sides own category bands, labels,
brackets and trees in their own viewports. Declare the aligned index scales on
the surround owner, with explicit domains from the prepared slot counts. Keep
perpendicular tree-height scales and annotation color scales independent. Use
native legends and layout spacing rather than compensating legend offsets or
negative coordinates to reserve room for tracks. Preserve the documented
`width`/`height` and `figsize` budget semantics during this change.

Heatmap cell groups must have real blank space between them. Use native index
`gapPositions`, with a `gapWidth` of 4 CSS pixels, which stays fixed
under zoom and device-pixel-ratio changes. These gaps are a deliberate requested
appearance change; values, ordering and scientific meaning stay unchanged.
Ordinary native scale configuration owns gap styling; do not add a parallel
Scanpy-specific layout configuration system.

- Cell-group cuts come from the final ordered `HeatmapData.intervals` exclusive
  stops, excluding the last stop. For group sizes 2, 3 and 1, use cuts `[2, 5]`:
  a cut at 2 separates slots 1 and 2. With `swap_axes=True`, these cuts move to x.
- Marker groups can supply feature-axis cuts after their final permutation when
  `FeatureGroup` spans form a contiguous, nonoverlapping partition. Inclusive
  group ends become cuts at `end + 1`, excluding the final end. Arbitrary or
  overlapping brackets retain their meaning without inventing a partition.
- A single group has no internal cut. Missing cells and masked tiles retain
  their slots; repeated gene labels retain distinct integer slots. Do not insert
  dummy rows, mask out real cells, or paint white rules over tiles to imitate gaps.
- Supplied numeric matrices and clustermaps keep rows and columns contiguous.
  The clustermap tree-cut gap trial was withdrawn after visual review on
  2026-10-21; remove its cut parameters and grouping computations. Heatmap
  cell-group gaps and dotplot marker gaps remain unchanged.

Deliver in small increments, updating the current queue in STATUS after each:

1. **M14.b.1 — cell heatmap and shared track helpers.** Replace heatmap's category
   strip, group/gene labels, marker brackets and attached tree overlays with
   native side views. Add cell-group and applicable marker-group gaps. Evolve
   existing `_grouped_chart` label/bracket and `_dendrogram_chart` helpers so the
   following families can reuse them. Keep tree computation in Python through
   stored/public Scanpy results. The released `transform_dendrogram` can lay out
   precomputed hierarchy where it matches the stored tree; it does not replace
   clustering or justify recomputation. Preserve merge heights and final leaf
   order, including unequal cell-group spans and fractional branch positions.
2. **M14.b.2 — matrixplot and dotplot.** Apply the same side-view layout through
   `finish_grouped_chart`. Dotplot has marker-group gaps; matrixplot keeps its
   tiles contiguous across marker blocks. Retain the existing
   summary records, means/fractions, authoritative `values_df`, dot footprints,
   native guides, fitted values and ruler. Ranked variants inherit the migration
   through their parent chart paths; do not implement them separately.
3. **M14.b.3 — matrix, clustermap and correlation.** Reuse the migrated labels
   and tree views for both axes, moving clustermap color tracks into native
   sides. Keep supplied/SciPy linkage, masks, palettes and permutations intact.
   Reuse the same numeric tiles and interactions; all three stay contiguous.
   Generic matrix titles belong to their label tracks; retain numeric native axes
   when labels are omitted. Correlation uses vertical top labels, right row labels,
   the shared left tree and a native colorbar beneath the tile area.
   This completes M05.f only after both heatmap and clustermap pass its gates.
   All tree families share native `linkShape="orthogonal"` edges with
   `orient="vertical"`/`"horizontal"`. Emit two parent-to-child links per merge,
   preserving stored heights, leaf order and Python clustering. Reuse the live
   index-offset helper for fractional anchors on gapped tracks. Verify complete
   SVG paths including elbows, all orientations, unequal heatmap group spans,
   zero-height merges, resizing and zoom. The [shared renderer delivery](STATUS.md#shared-native-orthogonal-dendrograms)
   closes this increment; C12's separate straight-link export bug remains upstream.
   Side tracks use native viewport-contained height domains to expand visible
   subtrees after navigation, with zero pinned at the matrix edge. Preserve the
   initial root margin, cached heights, and reset behavior. Entirely zero-height
   trees retain a nonzero range; C13 tracks native fitting of zero-only subtrees
   within larger trees and keeps that edge-case gate open.

Keep the data-access, grouped-summary, ranking and tree-preparation modules
unchanged unless a focused failing semantic test requires a correction. In
`_grid_interactions`, retain shared zoom and fitted-value behavior. The old
`origin + slot * step` annotation projection assumes uniform spacing and is
incorrect after native gaps: migrated views must use the shared gapped scale.
Check tree anchors and group centers through that same scale. Remove obsolete
projection/clipping/padding code as its last actual caller is migrated; do not
introduce another general layout framework alongside `gs.surround`.

Each increment requires:

- Semantic tests proving the same selected records, values, IDs, category/feature
  permutations, normalization, masks and cached-tree behavior. No extra AnnData
  reads, hidden analysis or full-matrix densification for layout.
- Complete registered charts with axes, labels, brackets, trees, legends and
  measured native gaps. Include both orientations, unequal group sizes, a single
  group, reordered/duplicate markers and missing tiles. Preserve parity outside
  the intentional gaps and native track placement; review changed references
  rather than blindly replacing them.
- Observed strip/tile hover, no data hit in blank gaps, y-only/xy zoom, pan,
  resize and multiple DPRs. Check shared leaf/strip/label positions, fixed CSS gap
  widths, viewport bounds, fit-to-band values and the native dotplot ruler.
- Widget and standalone HTML delivery, the updated packaged-PBMC expression
  workflow, and a representative payload/render/memory comparison. Track labels
  and bands must not duplicate the expression measurement table. Keep generated
  media and notebook execution state out of Git. The existing 250,000-value
  heatmap limit stays; larger/chunked transport remains M05.d.

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
