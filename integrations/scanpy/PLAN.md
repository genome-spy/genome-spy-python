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

For supported cases, preserve names, argument names/kinds, aliases, ordering,
statistical meaning, supplied results and data-selection/statistical defaults.
Native presentation and interaction defaults may deliberately differ after
plot-by-plot review; document and test each accepted difference. Add keyword-only
GenomeSpy controls. Track meaningful unsupported parameters until implemented or
explicitly resolved as a renderer boundary. Signature presence alone is not support.
Support Scanpy >=1.11.5,<1.13, with the reference environment pinned to 1.11.5.
Validate both ends of the range and audit changed parameters before widening it.
Keep base and namespace imports free of the scientific stack.

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

Appearance stays faithful to data, order and visual encodings; Scanpy's default
styling is a comparison reference, not the design target. Review visual defaults
and interaction behavior together before changing them. Existing interaction
defaults remain until that review selects useful, predictable behavior. Current
native defaults use 300 by 300 logical pixels per UMAP panel and 100/72 pixels per point.
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
grouped extraction/statistics and layout in `_expression.grouped_data`/`_expression.grouped_chart`,
and tree preparation/rendering in the dendrogram modules. Shared option/dependency
guards live in `_guards`; display handling stays in `pl.py`. Add capabilities
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
The [Scanpy 1.11.5 reuse audit](COMPATIBILITY.md#reusing-scanpy-computations)
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

## Test cleanup and CI selection

This cleanup covers the whole Scanpy suite, not just its slowest tests. Reduce
repeated work and maintenance while retaining distinct supported behavior and
regressions. The collection below is an audit baseline, not a target test count.
Implementation and current verification belong in
[STATUS](STATUS.md#test-cleanup-audit). The cleanup is implemented and locally
verified; updated hosted CI remains the clearance gate.

### Audit baseline (2026-10-28)

| Code | Files | Lines | Collected cases |
| --- | ---: | ---: | ---: |
| Python tests, including workflows | 46 | 14,026 | 2,385 |
| Browser tests and their fixtures | 43 | 11,525 | 634 |
| Small synthetic data fixtures | 21 | 1,290 | — |
| Reference generators | 11 | 1,209 | — |
| Local benchmark scripts | 7 | 1,237 | — |
| Shared helpers and package initializer | 2 | 132 | — |

There are 690 test functions expanding to 3,019 cases. Inventory includes every
Python file, collected case, parameter grid and test-module import. Assertions in
high-repeat areas were inspected; deletion still requires checking each affected
behavior. Before cleanup, CI repeated all Python cases in four environments and all
634 browser cases on three Python versions, plus a latest-version browser subset
and both long notebook renders in each pinned environment.

A previous clean run spent 154.5 seconds in the expression notebook test and
12.9 seconds in the UMAP notebook test. These two tests contain 900 lines. The
four initial hosted Python checks each took roughly 16–18 minutes. These are
observations from those runs, not portable timing limits.

### Keep, reduce or remove

| Area | Decision and retained coverage |
| --- | --- |
| Public API and display (`test_contract`, signature tests) | Keep every entry point covered. Test shared show/autoshow/save behavior at its owner, then one routing case per entry point. Remove duplicate full truth tables from family tests after tracing exceptions. |
| AnnData access (`test_grouped_data`, UMAP/scatter, upstream reuse) | Keep source precedence, symbols, masks, categories, missing values, duplicates, views/backed data, stable IDs and selected-column allocation. Small synthetic inputs make these independently checkable; retain them. |
| Embeddings and PCA | Test shared colors, outlines, bounds and legends at their owner; keep wrapper-specific basis, component, default and forwarding checks. Do not repeat every shared option through every alias. Keep tie order checked against local Scanpy. |
| Expression families/builders/trees | Keep mean/fraction denominators, log/scale order, supplied tables, grouping, linkage/cache behavior and detached builder state. Keep a rendered example per distinct mark/layout, not per storage format. |
| PAGA/path/adjacency | Separate sparse-format handling from graph/profile semantics. Keep real CSC/LIL, orientation, cache, degree, filtered-path, dense/raw allocation and return-data regressions. Avoid rerendering Scanpy for every format. |
| Timeseries, simulation and DPT | Test shared profile validation once, then wrapper metadata/order/default differences. Keep filtered-view and no-hidden-analysis cases. Separate numerical equivalence from expensive rendered comparisons. |
| QC (`highest_expr`, HVG, Scrublet) | Keep normalization denominators, bin edges/density, stored flags/cutoffs, source access and nonmutation. Keep one observed slider interaction for each distinct dataflow. |
| Selection, EmbeddingSummary and linked tracks | Keep brush boundaries, stable membership, clearing/counts, snapshots, group means, histograms and source reuse. Verify linked views in a browser; plain spec assertions cannot establish interaction behavior. |
| Shared grid/presentation/colorbar checks | Test shared options centrally. Keep family wiring and real layout regressions; reduce unrelated option cross-products. |
| Workflows and docs | Keep each workflow runnable, clean notebook checks and representative outputs. Remove repeated per-plot specifications and statistical assertions from the 900-line workflow tests. Keep guide execution with prepared inputs and browser layout checks in deeper validation. |
| Core capability reproducers | Move pure native capability probes out of integration acceptance into an explicitly selected Core-upgrade check. Unsupported triangle geometry is not a release requirement for supported marker shapes. Retain a passing/failing reproducer where it guards a documented limitation. |
| Benchmarks | Remove all seven `benchmark*.py` scripts after accounting for their assertions below. They are manual tools, not CI jobs, and contain no calibrated performance pass/fail limits. Do not replace them with a benchmark framework. |
| Reference generators and JSON | Retain independent expected values and the renderers needed to reproduce visual comparisons. Ten families are called by `reference_images`; grouped generation supplies numeric expectations. Remove unused metadata/exports and identical export boilerplate after tracing consumers. Keep family-specific artist extraction separate. |

The seven benchmark scripts cover embeddings, grouped expression, clustermap,
rank labels, highest expression, HVG and Scrublet. Their useful allocation and
no-expression/no-analysis checks overlap existing tests in the corresponding
families. Before removing a script, identify the protecting test; transfer any
unique invariant into a small deterministic regression. Timing/heap observations
are local historical evidence, not release contracts. Remove obsolete benchmark
commands and update README, fixture notes and compatibility/status records.

Do not delete reference renderers as if they were generated results. They create
fresh Scanpy images outside Git for browser comparison. Synthetic fixture
functions create small, deliberate counterexamples; they are not downloaded
analysis data. Keep their distinctions rather than inventing a universal fixture
factory. Do not regenerate frozen expectations merely to accommodate cleanup.

### Concrete reductions

- The shared display test currently builds charts for 38 functions × four display
  modes: 152 cases. Keep the full setting behavior at the shared owner, one
  forwarding check for each function, and separate actual exceptions such as
  ranking. Keep fast validation-before-import checks for every public entry.
- PAGA adjacency repeats five heatmap and ten stripplot cases over six formats:
  90 live upstream comparisons. Run the 15 semantic cases once on a canonical
  format; use a focused six-format test for conversion/orientation, alongside
  the independent CSC/LIL regressions. Storage and missingness must still combine
  where a known bug depends on both.
- The 35 embedding colorbar cases cross seven wrappers with five positions.
  Check the five positions on shared rendering and wrapper forwarding separately.
- Timeseries duplicates 28 rejection cases through two calls. Keep shared input
  failures at the shared validator, with thin checks for each entry's context and
  its distinct defaults. Preserve tests that establish different accepted inputs.
- Browser heatmaps cross orientation, tree, feature brackets and gaps in 24
  navigation cases. Retain a compact explicit list exercising each branch and
  the combinations that matter, such as gaps with trees and swapped navigation.
- Use one Chromium browser per test session with a fresh context/page per test.
  Preserve device scale, viewport and error checks. The current fixture launches
  a browser for every case. Keep failed-test cleanup reliable and avoid shared
  page state.
- Move reused render/hover/SVG helpers out of test modules into small test support
  modules. There are 111 imports from test modules across 41 non-benchmark files.
  Keep plot-specific assertions beside their tests. Do not build a fixture registry.

A case is removed only when an identified retained case protects the same
behavior, or when its requirement is deliberately retired and documented. Do
not substitute random sampling, arbitrary quotas, large expected failures or
weaker numeric/image tolerances for this review.

### Selection flags and job responsibilities

Use three standard pytest markers, with strict marker checking. No new runner,
custom command flags, path-change classifier or automatic test picker is needed.
Keep local pytest's unfiltered behavior available.

| Marker/selection | Meaning |
| --- | --- |
| Unmarked Python cases | Fast contract, preparation, geometry/spec and regression checks. Includes frozen numeric fixtures and deterministic allocation checks. |
| `reference` | Live upstream plotting/artist extraction and registered pixel comparisons. A frozen numerical assertion alone is not expensive reference work. |
| `workflow` | Executing full notebooks, tutorial preparation or downloaded real-data workflows. |
| `smoke` in `browser/` | A small explicitly marked set of observed native interactions and layout checks for every distinct renderer/dataflow. |

Some reference tests currently mix live plotting and fast invariant checks. Split
these before marking; do not make critical source or allocation checks disappear
from the PR job. Preserve the recent direct tie-order comparisons in reference
checks and basic independent ordering checks in the fast suite.

Commands after marker assignment (implementation evidence is in STATUS):

```sh
# PR: all fast Python checks.
uv run pytest tests/integrations/scanpy --ignore=tests/integrations/scanpy/browser -m 'not reference and not workflow'
# PR: observed interactions and representative layouts.
uv run pytest tests/integrations/scanpy/browser -m smoke
# Deep verification: full Python and browser suites, including marked cases.
uv run pytest tests/integrations/scanpy --ignore=tests/integrations/scanpy/browser
uv run pytest tests/integrations/scanpy/browser
# Workflows only; their shared owners retain the detailed behavior checks.
uv run pytest tests/integrations/scanpy/test_notebooks.py -m workflow
```

| When | Scanpy jobs |
| --- | --- |
| Every PR | Fast Python checks on pinned 1.11.5/Python 3.11 and current 1.12.4/Python 3.12. Browser smoke once on the pinned stack. No full notebook renders, reference generation or timing benchmarks. |
| Main and explicit full dispatch | Full Python checks on supported Python 3.11–3.13 with pinned Scanpy, plus current 1.12.4 compatibility. Full browser/reference comparisons once on the pinned stack; current-version interaction subset. Both workflows once. |
| Release (`workflow_call`) | Require the full checks above before building/publishing. Release must explicitly request full mode so the cheaper PR defaults cannot weaken it. |

Base Linux/Windows jobs continue without Scanpy. Move lightweight import and
missing-extra checks into a dependency-free test module; avoid collecting the
whole scientific suite there. Existing base notebook-rendering and codegen jobs
keep their separate responsibilities.

Add one boolean workflow input, `full_scanpy`, to dispatch/reusable CI. Main uses
full mode. Regular PRs use the shorter selection. Label/input handling must not
prevent a contributor from running all tests locally. Do not duplicate browser
rendering across Python versions when the JavaScript bundle and pinned reference
stack are identical. Proposed performance goals are under five minutes each for
the warm fast and smoke jobs; measure before treating those goals as achieved. Use GitHub's native concurrency group
for superseded PR runs; main and release runs must not be cancelled by that rule.

### Implementation and clearance

1. Account for and remove the seven manual benchmark programs and stale commands.
2. Reduce repeated grids and notebook assertions, and detach shared test helpers.
   Preserve known regressions and independent data calculations before deletion.
3. Split fast/reference/workflow checks and assign browser smoke cases. Cover
   categorical/continuous embeddings, brush clearing/count/Python membership,
   linked means/histograms/tracks, grid zoom/value labels, gaps/trees/labels,
   graph hover/legend, QC sliders, profile focus and offline delivery. This list
   defines behaviors, not a separate smoke framework.
4. Implement the marker and CI selections, retaining full release gates and
   version-boundary checks. Run each selection separately, then all retained
   checks once. Browser context isolation must pass sequentially after reuse.
5. Update contributor commands and retained evidence. Record before/after source
   size, collection counts and measured durations in STATUS; keep detailed
   inventories, timing logs, images and temporary JSON outside Git.

Finish when every removed check has a retained owner or documented retirement,
all supported plotting entries remain covered, dependency-free checks run in the
base jobs, normal PRs avoid full workflows/reference matrices, and the full
release path passes. Documentation must describe the jobs that actually exist.
Do not close this work after adding markers alone. Keep this section in the live
plan until verified; then reduce it to maintained testing commands and a short
completion record in STATUS.

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
| M09 | Tracksplot and ranked tracks | Grouped access; native per-cell rects available; continuous fill remains C01 |
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
One first-panel interval owner supports a plain brush, a native count, and
Python `selection_mask` through the ordinary widget. Use the dedicated PBMC
UMAP notebook and frozen semantic/complete-chart/browser/resource checks as
evidence. Its order is basic plotting, linked selection, then customization.

Acceptance: preserve supplied coordinates and independent per-panel color scales.
With zoom enabled, Shift-drag brushing, clearing, coincident cells and half-open
membership agree in the chart and Python. No local Core patch or notebook connection task.
The publication interaction direction is a default native interval brush without
per-cell point highlighting or fading, using the existing `selection=` parameter.
A live count uses a separate native dataflow branch driven by the brush parameter;
point rendering stays independent of selection. Retain the existing zero-safe
formula/sum counter until the native selection-filter/count path can be adopted
with a published Core release, as requested by the user.
Count all loaded cells inside the bounds regardless of semantic visibility.
Python subset retrieval remains explicit. Review count latency, tooltip content
and navigation before public/canonical-workflow adoption; keep reset zoom separate
from clearing.
The native selection-filter/count candidate needs a released Core with the
upstream empty-global-aggregate fix before package adoption. Its full-table scan
still consumes approximately one frame at 1.1M cells; a proposed native cached
spatial range count remains Core work, not an implemented integration capability.
This closes a preview only. Remaining normalization, overlays, fonts, 3D,
backed expression, and broader selection modes stay in M07/M14.

### M02 — grouped access and dotplot (plain-chart preview closed)

M02.a–d are verified for the plain-chart preview; see [data evidence](STATUS.md#verification)
and [chart evidence and limits](STATUS.md#verification).
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
  Reviewed native dotplot guides use `Cells expressing (%)` and `Mean expression`,
  centered below the gene labels, with native wrapping when needed. Matrixplot
  and both builders use the same bottom layout; explicit titles still override
  these defaults.
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
attachments; see [scope and evidence](STATUS.md#verification).
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
[status record](STATUS.md#verification) and maintained
[heatmap contract](COMPATIBILITY.md#heatmap-compatibility).
It adds one chart module and small functions in the existing grouped data/tree
modules, reusing access, scaling, palettes, feature ordering, labels and branches.
No fixed value cap is imposed. Large sparse cases verify that extraction reads
only requested genes. Larger/chunked transport remains a performance task in M05.d.
The standalone `matrix` part of M05.b is delivered as a numeric-array preview,
reusing numeric validation, linear color bounds, index slots and labels. Heatmap
adds optional zoom with aligned cell annotations and clipped tree branches;
y-only by default, with both axes explicitly available.
Shared grid interactions are M05.e below. M05.c has a bounded clustermap preview
with public SciPy or supplied linkage, ordered annotation tracks and shared
tiles/branches; see its [status evidence](STATUS.md#verification).
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
  No fixed tile or pairwise-distance cap is imposed. Z-score/sample-SD and
  min–max scaling follow Seaborn, including missing
  constant ranges; display masks do not change distances. Native palette/guide
  differences and unsupported kwargs remain explicit in the
  maintained contract, with broader options assigned to M14. Do not claim the
  full clustermap family closed from this preview.
  Observation category strips retain names/order/palettes and use their own native
  categorical legend. M05.f retains the native strip-viewport migration; legacy
  strip hover already passes on Core 1.2. Explicit CSS tracks do not invent
  category names.
- M05.d: test chunked selected-column access and a 100k-cell × 50-marker heatmap;
  measure payload, rendering and memory without imposing fixed caps. Compare
  complete PBMC tutorial heatmaps with registered strips/tree/label alignment.

- M05.e (verified interaction preview; [evidence](STATUS.md#verification)):
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
rank-statistic colors do not alter expression denominators. Ranked violin remains
M08; ranked tracks reuse M09's existing parent renderer in a separate increment.

### M07 — embeddings, scatter and PCA

Named embeddings, generic bases, PCA variance labels, selection retrieval and
scatter share the existing data/chart/style/interaction path. Slice states,
commit evidence and unmet verification gates live in the
[status ledger](STATUS.md#current-work-queue).

- M07.a: extract reusable embedding authoring/access from UMAP for `embedding`,
  `tsne`, `diffmap`, `draw_graph`, `pca` and alias `pca_scatter`. Resolve basis/layout
  names, components/dimensions and explained-variance labels from stored results.
  Missing coordinates error; no neighbors, PCA, t-SNE or force layout rerun.
- M07.b ([contract and evidence](STATUS.md#verification)): `scatter` x/y/basis selection, observation versus variable
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
  reuses `pca`, `pca_loadings` and `pca_variance_ratio` with their existing statistical
  defaults. Cell positions sit above two native diagnostic rows: PC1/PC2, then
  PC3/variance. Loadings use 280-pixel panels, retaining fonts and all components
  while fitting a notebook page. Keep the plots' own titles without section wrappers.
  PCA text axes reserve 30% extra score-range headroom for labels; reference
  checks account for this deliberate display-margin difference.
  Scanpy opens the three plots in that order; compose the native results vertically
  and display once. Forward supported PCA plotting kwargs only to the embedding,
  keeping the diagnostic statistics unchanged; reject unsupported kwargs before any output.
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
  records. Its [completed increment](STATUS.md#verification)
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
  [delivery record](STATUS.md#verification) retains evidence;
  Centered-color acceptance: reuse this resolver for `vcenter=None`, numbers,
  percentiles, callables and singleton/per-panel lists. Match Scanpy's two linear
  slopes around the center through a native three-value domain (equivalent to
  `domainMid`), retaining source values. Automatic limits expand symmetrically
  when all values lie on one side; explicit limits must strictly enclose the
  center. Preserve constant colors with/without a guide, masks, callback inputs,
  clipping and numeric guide positions. Compare public Scanpy limits and painted
  points, including asymmetric ranges, and verify native hover/zoom/brush/HTML,
  packaged notebook execution and a realistic resource workload. The
  [centered-color record](STATUS.md#verification) retains evidence.
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
  The [edge delivery record](STATUS.md#verification) owns evidence;
  remaining edge forms retain M07.d/M14 owners.
  Square-marker acceptance: `marker="s"` maps to native square points in shared
  embeddings, PCA overview and scatter; existing scalar/per-panel broadcasting,
  size units, missing values, outlines and native legend symbols are retained.
  Verify occupied square corners as well as side lengths against Scanpy exports,
  then test hover, linked brushing, zoom and HTML through the shared helpers.
  Run the packaged notebook and a representative multi-panel resource comparison.
  The [square-marker record](STATUS.md#verification) owns delivery evidence.
  Diamond-marker acceptance: `marker="D"` uses native diamonds with Scanpy's
  √2 path-width conversion, including outlines and scalar/per-panel inputs.
  Share marker definitions across validation, points and guide sizing. Category
  keys follow each panel's marker shape through native legend inheritance;
  this deliberately differs from Scanpy's circular embedding keys. Compare sizes
  in Scanpy's units. Verify plain/stroked diamond bounds and
  occupied area, hover/brush/zoom/HTML, unchanged data, the packaged workflow
  and a representative resource workload. Do not enable thin diamonds or other
  markers merely because a similarly named native shape exists. The
  [diamond-marker record](STATUS.md#verification) owns delivery evidence.
  Triangle audit: compare `"^"`, `"v"`, `"<"`, `">"` with their native shapes,
  using Scanpy paths and rendered footprints with/without strokes. Enable them
  through the shared marker table only if both paths and paint match; scalar
  resizing must not hide different aspect ratios. The
  [audit record](STATUS.md#verification) retains the native gap
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
- M09.b: use the gallery's native per-cell rect approach for a tracks preview,
  with shared grouping, palettes, cell ordering, aligned index scales and the
  existing dendrogram renderer. Each rect represents one original observation;
  do not recover values from Matplotlib or approximate a polygon with sampled
  rectangles. Reuse the rendering approach, not the gallery's packaged-data or
  tree preparation. Ranked tracks reuse M06 slots.
- Optional `group_gap` uses native index-scale gaps at the prepared cell-group
  boundaries; `spacing` uses native vertical concat spacing. Both default to zero.
  Keep all tracks, the category strip and tree aligned during navigation; spacing
  changes no expression, cell order, palette or saved analysis result.
- Scanpy 1.11.5 fills linearly between adjacent cell values; per-cell rects give
  a stepped profile. Document this explicit visual difference in the preview.
  Exact continuous-fill parity remains C01; it does not prevent
  a native per-cell preview. Test isolated peaks, zero/negative values where
  accepted, uneven groups, repeated genes and unsupported options explicitly.

Acceptance: values, source/log semantics, category and cell order, baselines and
panel extents match Scanpy references. Record the interpolation difference rather
than claiming exact profile parity. Native zoom keeps tracks, labels and trees
aligned; tooltips retain original observation IDs. Measure realistic cell×track
costs. Prototype geometry is not production code, and the full milestone remains
open while ranked tracks or declared compatibility gates are unfinished.

### M10 — quality-control diagnostics

Prioritize new plot families over remaining marker-shape details; those stay in
M14's compatibility backlog. Start M10.b with stored-statistic scatter panels,
then M10.a's highest-expression summaries and M10.c's histograms. M08 retains its
native filled-geometry gate; M09 can use the per-cell approach above. This order
does not close those milestones.

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
  The optional threshold_slider previews one cutoff per batch, shared by its two
  panels. Above-cutoff bins are accented, below-cutoff bins muted and bins crossing
  the cutoff neutral. Preserve saved scores/calls, fixed bins and denominators.
  Observe independent batch controls, the moving rule, hover and offline HTML;
  measure the preview against the existing stored-score workload.
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
  in [STATUS](STATUS.md#verification).
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
  helpers. Add a readable native DPT group key beside the upper panel, preserving
  observed names, colors and marker shapes; keep the continuous pseudotime guide.
  Verify masks, category/paint order, palettes, markers, defaults, read-only
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
  The first bounded increment renders undirected graphs with group/CSS colors,
  supplied positions or Scanpy-computed layouts, thresholded solid/dashed edges,
  node-size powers, edge-width clipping and native labels, hover and x/y navigation.
  Reuse public `sc.pl.paga(plot=False)` on metadata-only AnnData for layouts; never
  call private layout functions, copy expression or extract artists. With pos=None,
  recompute layout even when cached positions exist, as upstream; explicit pos skips
  layout. Cache positions only after success when add_pos=True; plot=False creates
  no chart. Missing results require explicit sc.tl.paga. Reuse shared numeric,
  CSS/palette, coordinate-domain, point-unit, navigation and delivery helpers;
  graph nodes represent groups, so no observation brush is added. When labels
  are shown, reuse the embedding label renderer: native text measurement and
  displace2d use stable node IDs and pixel-sized anchor obstacles. Hide labels
  whose anchors leave the viewport; preserve supplied positions and group IDs.
  Test duplicate display labels, normal/bold measurement, zero-size nodes,
  obstacle size, live reflow and offline delivery.
  White edge borders await native rule/link outline support (C17). Do not emulate
  them with extra layers or custom geometry; recheck crossings after a Core release
  adds this capability.
  Acceptance: public Scanpy references for thresholds, layout seeds/initialization,
  positions, sizes, colors, aliases, labels, edge order/widths and bounds; sparse
  formats/invalid-result and mutation guards; registered DPI-aware complete-chart
  overlays and point footprints; observed node/edge hover, zoom/pan, composition
  and offline HTML; independent packaged-data notebook execution and metadata-only
  resources. Keep Scanpy's PAGA extra optional and base imports lightweight.
  Sparse regressions cover asymmetric CSC weights/order, computed LIL layouts,
  custom solid-edge keys and preservation of stored matrix values and formats.
  The numeric-color increment reuses grouped_expression/sc.get.obs_df and
  group_means for observation and gene means. Gene colors use raw when present
  by default, otherwise X; use_raw=False uses X. Only one gene column is loaded.
  Observation means skip missing values; gene means propagate them, as in Scanpy.
  Weighted degrees come from the same thresholded solid/dashed graphs and are
  normalized to 0–1. Reuse shared color bounds and native scales/guides; test
  constant and missing means, sparse views, raw/X fallback and graph edge order.
  Native node guides deliberately improve on Scanpy 1.11.5: group colors get
  category keys; numeric observation/gene/degree colors get a colorbar unless
  colorbar=False. Explicit True shows the guide. All-missing
  data and equal-degree normalization fail clearly instead of inventing values.
  CSS/annotation-name collisions, numeric vectors and other categorical colors
  remain explicit limits. Packaged-data examples reuse supplied positions.
  single_component=True retains the largest thresholded solid component by node
  count, choosing the first on ties and preserving original node IDs/coordinates.
  Compute colors/degrees before filtering; size areas use the displayed count and
  median sizes. Keep full layout/cache coordinates and leave plot=False unchanged.
  Filtering disconnected graphs requires dashed_edges=None, as upstream.
  Scanpy 1.11.5's direct disconnected call fails because colors are subsetted but
  coordinates are not. Semantic, subsetted-public-reference, chart, workflow and
  resource checks cover the native intended behavior; the direct parent-reference
  gate stays blocked by C15, with a strict expected-failure test to detect a fix.
  This does not close M11.c: categorical mixtures/pies,
  multiple color panels, directed transitions, file
  positions and GEXF export remain explicit unsupported cases. M14 owns font/global
  style parity and the native fixed dash pattern versus Matplotlib's per-width
  dash lengths. Audit these before claiming full PAGA compatibility. C04's missing
  dedicated path mark does not block straight undirected rule segments.
- M11.d: `paga_adjacency`, `paga_compare` and `paga_path` reuse matrix/embedding/
  graph authoring. Preserve supplied adjacency/tree/positions, panel alignment,
  ordered paths, `n_avg` window/end behavior, annotations, source selection and
  `normalize_to_zero_one`. Specify native return shapes for `return_data` and
  no-plot modes instead of returning fake axes.
  The adjacency heatmap preview reads the legacy top-level uns keys exactly;
  modern uns['paga'] matrices must be assigned explicitly by the caller. Reuse
  bounded sparse access and the numeric matrix renderer, adding native points
  at x=tree row, y=tree column, including asymmetric/diagonal inputs. Preserve
  nonzero selection without thresholds or ordering changes; zeros stay excluded.
  Keep original numeric group axes and shared native color guides, hover, zoom
  and fitted values. Accept matching resident SciPy sparse matrices/arrays without an arbitrary size
  cap; validate shape before densification and never read expression.
  Direct public references cover tiles, points, missing/constant values, guide
  bins and export DPI; observe hover/navigation/HTML and measure a larger matrix.
  as_heatmap=False reuses adjacency access and native point marks: gray points
  exclude diagonal entries, black points use adjacency values at nonzero tree
  entries (including selected diagonals). Preserve per-source gray-then-black
  draw order and numeric indices. Missing points do not affect limits; preserve
  Scanpy's five-percent margins and empty/constant limits through shared helpers.
  Explicit group names use index slots and the shared label view; collect their
  native legend below the names and bottom axis title. Index axes cannot yet
  map positions to arbitrary names, so retain that capability boundary.
  color_map is inactive; show_values=True requires heatmap mode. Default strip
  plot area is 496 by 369.6 pixels. Reuse native hover, y/both-axis navigation,
  composition and HTML delivery; verify sparse formats, source/target IDs, points,
  footprints, ordering and packaged workflows independently. Both modes remain
  bounded by stored-data and native styling/export limits; full M11.d stays open.
  The comparison increment composes the existing embedding and PAGA entries.
  Preserve automatic basis priority (draw_graph_fa, umap, tsne, draw_graph_fr),
  selected-component group medians when color is the PAGA group key, cached
  positions for other colors, supplied positions, title/label precedence and
  add_pos behavior. Both native panels share the embedding limits and optional
  x/y navigation; color and size scales stay independent. Collect the graph
  guide on the comparison container; categorical keys sit below both views.
  Never infer an embedding or recompute PAGA. Retain the existing parent rendering restrictions: on-data
  labels require explicit legend_fontweight="normal" with the bundled regular
  atlas; the pinned bold default errors. Support one color/component pair and
  reject custom margins, plot=False and unsupported parent options explicitly.
  Acceptance: pinned signatures and direct public-call medians/cache/domain/title
  comparisons, native parent reuse, mutation/expression/analysis guards, complete
  aligned charts including out-of-range supplied positions, observed cell/node
  hover and shared navigation/offline HTML, packaged workflow and seeded resources.
  Comparison review corrections: share the existing category-palette resolver
  through the native PAGA palette addition, preserving cached colors and full
  category domains under component filtering. CSS lists/mappings and native
  schemes must paint the same groups identically in both panels; do not sample
  colormaps, copy AnnData or temporarily mutate palette caches. Embeddings use
  native scale identity; independent comparisons must render and navigate without
  caller-provided names. PAGA declares x/y at its layer root so children inherit
  coordinates and comparison can use native encode without private layer access.
  Acceptance adds direct public palette comparisons, rendered scheme/CSS/component
  colors, independent pair zoom/pan/offline composition, parent regression checks,
  and a packaged notebook palette/composition example.
  This bounded comparison does not close paga_path or the full M11.d milestone.
  The path heatmap increment orders each supplied node's cells by stored
  dpt_pseudotime, concatenates nodes including repeats, applies full-window
  cumulative averages and then optional per-key zero–one normalization. Reuse
  grouped_expression/public obs_df and native matrix_tiles, fitted values,
  slot labels, palettes, zoom and surround. Read raw when present or fall back to
  X; never recompute PAGA/DPT. Select columns through the shared reader before
  applying path row order; do not create a row-indexed AnnData that copies all
  genes. Validate only path values, including repeated nodes and mixed obs/gene
  keys; dense X/raw tests must detect copies of unrequested gene columns.
  Original group bands span the full plot width even
  after smoothing shortens profiles/annotations. Keep numeric annotation tracks
  aligned and return (chart, frame) for show=False/return_data=True, or frame
  after display. The preview requires two keys/two smoothed cells, at most one
  numeric annotation. Do not impose a fixed value cap. Reject
  categorical/multiple heatmap annotation tracks and custom margins clearly;
  xlim and legend font options are inactive in heatmap mode as upstream.
  Verify ordered/normalized/raw/sparse values, repeated nodes, annotations,
  native return shapes, analysis/mutation guards, complete registered charts,
  observed hover/navigation/HTML, packaged workflow and resource behavior.
  Scanpy 1.11.5 return_data fails for the default n_avg=1 annotation; retain a
  strict regression check and separate that parent gate from chart verification.
  Retain native Greys as an accepted fidelity limit: assert its 226/30 endpoints
  separately from Scanpy's 255/0 endpoints, while checking identical annotation
  values/domains, geometry and native pixel mapping. Do not substitute a palette.
  The line-mode preview reuses shared preparation and native
  window/lead and rules using round caps. Exact joins/end caps are not required;
  the observed minor stroke/rasterization differences are a documented visual
  limit, not a C04 blocker. Do not add custom join geometry or extra marks to
  imitate Matplotlib. Reuse path data preparation, applying xlim after
  smoothing/normalization and resetting cropped x coordinates to zero. Annotations
  do not render tracks. Support single-key labels and native multi-key legends,
  scoping heatmap-only shape restrictions separately. Acceptance includes bends,
  end caps, missing-value breaks, crop order, observed hover/zoom and the packaged
  workflow before notebook publication.
  Native category10 colors follow the key order and repeat after ten keys.
  Use the built-in color legend with its standard category symbols; show a key
  ylabel instead for a single key. Keep returned data uncropped. Single-sample
  and empty line crops are valid; repeated line keys and show_values=True fail
  clearly. Numeric/categorical annotations may be prepared for return_data but
  do not create line-mode tracks. No embedding, DPT or PAGA analysis is rerun.

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
  [STATUS](STATUS.md#verification) records verification and limits.
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

M13.a implements `DotPlot` first: detached selected-expression summaries shared
with functional `dotplot`, tree/totals replacement and ordering, axis swapping,
native dot limits/areas/exponent/edges/grid/padding, and native guide
visibility/titles/width. Constructor-only `dot_size_df` supplies labeled fractions.
Only dot coloring ships in this bounded slice; square-background styling remains
a separate M13 increment with its own contrast/geometry/guide checks. Padding
below 0.5 and broader Matplotlib color/normalization forms remain explicit limits.
There is no universal builder framework, method dispatcher or chart-spec rewriting.
The builder and public functions import shared guards directly from `_guards`,
so the builder does not depend on the public plotting facade.

Delivery uses mutable chains returning self and fresh `.to_chart()` snapshots
for native composition, display and HTML/JSON saving. `.show()` displays once;
Matplotlib axes/figures, `make_figure`, `get_axes` and `savefig` are omitted in favor
of those native methods. Show with `return_axes=True` rejects the request explicitly.
Verify actual upstream chains, supplied/repeated slots, no expression rereads,
tree/totals replacement, navigation, independent composition, offline output and
both canonical workflows. Reuse parent resource evidence only with an explicit
account of the unchanged workload; measure constructor retention/render snapshots.
M13.b adds `MatrixPlot` over the existing one-pass matrix summaries and native
tile renderer. Supplied `values_df` stays authoritative and is never read back
from expression or scaled. Both builders share concrete group-order/tree/totals
state in `_expression.grouped_builder`, native totals tracks in `_expression.grouped_chart`, and option
guards in `_guards`. Styles remain local to each family. Matrix chains cover
scheme/edge styles, color-guide visibility/title/width, tree/totals replacement,
sorting and transpose, with detached snapshots and the same native delivery.
Matrix summaries stay in group-by-feature order; `to_chart()` owns transposition.
Verify actual upstream chains, supplied/repeated slots, no expression rereads,
shared DotPlot regressions, independent composition, the canonical expression
workflow and construction plus retained snapshots on the grouped resource fixture.
`StackedViolin` follows M08/C01; remaining dot styles stay separate increments.

Target shape: `gsc.pl.DotPlot(pbmc, markers, "louvain").add_dendrogram().swap_axes().style(dot_edge_color="black")`.
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

Group spacing is opt-in. Expose keyword-only `group_gap=0` on heatmap, dotplot and
the DotPlot builder; ranked wrappers reuse their parent options. Positive widths
use native index `gapPositions` and `gapWidth`, fixed under zoom and device-pixel
ratio changes. Heatmap gaps separate cell and marker groups; dotplot gaps separate
marker blocks. Matrixplot remains contiguous. Numeric tile labels also stay
opt-in through `show_values` on every matrix/heatmap entry point. Correlation
matrices retain `show_correlation_numbers=False`; `show_values=None` follows that
flag, and contradictory explicit settings error. Both names reuse the same fitted
value renderer. Values, ordering and scientific meaning stay
unchanged.
Reuse the shared index-scale helper so every side track follows the same gaps;
do not add a parallel layout configuration system.

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
   existing `_expression.grouped_chart` label/bracket and `_dendrogram_chart` helpers so the
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
   zero-height merges, resizing and zoom. The [shared renderer delivery](STATUS.md#verification)
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
  media and notebook execution state out of Git. Do not impose a fixed value cap;
  larger/chunked transport remains a performance task in M05.d.

## Documentation and release

### Publication review of the implemented scope

The target is a Python package and documentation publication during **26 October–
1 November 2026**. Review the implemented subset before adding new plot families;
spatial and violin/stacked violin remain deferred. The user authorized the native
cell-track preview and its focused guide on 27 October 2026. This publication does
not require full Scanpy plotting compatibility and must state its supported scope.
Publish the supported subset as a normal package release. Missing plot families
do not require a preview label. User dependencies accept the tested Scanpy range;
keep the reference environment pinned for reproducible comparisons. The separate
compatibility CI job tests 1.12.4 without changing the pinned reference job.
The long-term inventory and capability backlog remain in this plan and STATUS.

Review plots one at a time with the user, starting with UMAP. Each review covers:

1. **Appearance:** real-data initial view, typography, hierarchy, color meaning,
   point/tile sizing, spacing, axes, labels and guides; inspect long labels,
   missing values and categorical/continuous examples. Show current output and
   a concrete native proposal before adopting new defaults.
2. **Interaction:** define the useful task for hover, zoom/pan, selection and
   linked views; choose defaults, activation, feedback, clearing/reset, tooltip
   content and notebook scrolling behavior. Check notebook and standalone HTML
   delivery, and distinguish browser-only actions from live Python retrieval.
3. **Code:** correctness, shared-helper reuse, self-containment, readability and
   YAGNI; use public GenomeSpy capabilities and retain computation/renderer
   boundaries. Fix shared causes once without bundling unrelated refactors.
4. **Decision and verification:** record accepted design, unresolved blockers,
   focused semantic/render/interaction checks, documentation/notebook changes
   and residual limits in STATUS. Intentional visual differences update visual
   expectations; they do not weaken data/identity/statistical assertions.

Keep implementation and visual decisions in small reviewable slices. Reuse
existing charts, references, native APIs and comparison artifacts; do not add a
theme framework, interaction framework or new renderer for this review. Shared
defaults only propagate to other families after their effects are inspected.
The current review queue and its decisions live only in STATUS.

For UMAP, semantic zoom is a performance optimization only for datasets above
1,000,000 cells, not an appearance treatment. Datasets at or below that threshold
retain full point drawing. Review styling on sufficiently dense embeddings with
semantic thinning disabled; keep point growth on coordinate zoom separate from
semantic zoom. Validate the above-threshold performance path before adopting it.

### Plot presentation proposals

The user approved implementing the native subset on 26 October 2026. The table
defines the presentation scope; STATUS records delivered behavior and remaining
proposals. Use real data and the existing comparison document to review changes.
Native capability limits do not justify custom event bridges or drawing substitutes.

| Plot | Proposed appearance | Proposed interaction |
| --- | --- | --- |
| Scrublet score distribution | Keep fixed histogram bins. A native legend explains preview colors. | Optional threshold slider per batch shares its cutoff between observed and simulated panels. Highlight wholly above-cutoff bins; keep straddling bins neutral. Preserve saved analysis. |
| DPT groups/pseudotime | Native observed-group key and pseudotime colorbar. | Reuse independent profile navigation. |
| Highly variable genes | Pale gray background genes and one clear accent for selected genes; draw selected genes last. Shorter axis and legend titles. | Gentle, capped point growth on zoom. An optional score-cutoff slider updates both panels' preview colors and the gene count, with a cutoff line in the normalized-score panel. |
| Timeseries | Smaller points, lighter outlines and clearer axis labels. Compare several genes in aligned panels when one overlaid view is crowded. | Emphasize one gene while keeping the others visible. Shared time navigation and a native ruler where the composition supports it. |
| Timeseries subplot | Consistent gene colors, aligned axes and one collected legend when panels share its meaning. | Reuse the timeseries interactions; share navigation only when the coordinates mean the same thing. |
| Simulation | Clear run labels and boundaries; consistent gene colors. Collect the point legend below the entire x-axis. Keep heatmap labels compact and values optional. | Reuse timeseries and matrix interactions. Optional gene/run dropdowns emphasize their intersection. Optional connected profiles retain missing-value gaps and run boundaries; shuffled output rejects these run options. |
| PAGA adjacency | Larger tree-edge dots over the heatmap; leave values off in the basic example. In point mode, label the group axis and connectivity axis and explain tree versus other edges with a native legend below the complete x-axis. Explicit group names use index slots and the shared label view until native index axes support name mapping. | Capped dot growth on zoom. Review source/target group focus if labels and hover alone are insufficient. |
| PAGA comparison | Much smaller embedding points at the overview; matching group colors across panels and fewer permanent labels. All network views have native node-color guides. Group-median embedding labels use native displace2d and text measurement. | Use the shared embedding renderer for point growth. Review linked group focus and an optional stored-edge cutoff control. |
| PAGA path | Clear path order and group names; readable expression scale in line mode. Match group colors to the graph and embedding. | Focus one gene and read values along the path. Reuse matrix hover, zoom and fitted labels in heatmap mode. |

Point growth uses the gallery's native zoom-based size expression, capped at four
times the starting area (twice the diameter). Check overview size, x-only, y-only
and combined zoom, maximum size, picking and legends. Keep explicit user
sizes meaningful and preserve ratios where size encodes a measurement. Cap
adjacency dots so they do not obscure the heatmap. Reuse a small helper across
actual consumers if needed; do not add a styling or interaction framework.
Point growth does not require dropping records.

The variable-gene slider is off by default. Its first scope is a clearly labeled
preview cutoff on stored normalized scores, not a rerun of gene selection.
Scanpy's mean limits, top-N selection and batch-aware ranking cannot all be
represented by one cutoff. Preserve the saved selection and AnnData, distinguish
preview status from saved status in hover, and use stable gene IDs across panels.
Reject an unsupported selection mode rather than imply that a score cutoff
reproduces it. Gene selection remains an explicit Python analysis step; use
Scanpy for that computation. See the [Scanpy selection rules](https://scanpy.readthedocs.io/en/stable/generated/scanpy.pp.highly_variable_genes.html).

The timeseries example uses stored S-phase scores, not elapsed time. Do not join
those cells into a curve. Connected simulation profiles are optional for genuinely ordered samples; they
must preserve missing values and never connect different realizations. Do not add smoothing, jitter, normalization
or inferred trajectories as styling changes. Keep group gaps and numeric tile
labels optional. Use released native capabilities; pending Core features do not
justify local patches or duplicate drawing layers.

For each accepted slice, verify unchanged values, identities and stored analysis;
inspect overview and zoomed views; observe hover, controls and reset behavior in
the notebook and standalone HTML. Check long labels, missing values, dense data
and narrow displays. Check parameter/scale names when composing two charts.
Update the relevant workflow and permanent guide after the design is accepted.
Generated comparisons and executed notebook state remain outside Git.

### Documentation delivery

M14.e designs the integrations landing page and one workflow page before choosing
and implementing notebook rendering. Keep the general visualization skill and
focused agent guides general; Scanpy policy/tutorials belong in this integration.
Review plot appearance and interactions first. Documentation work must not delay
those fixes.

```text
Integrations
  Overview: actual libraries, status, tested versions
  Scanpy
    Start here: analysis ownership, install, first replacement
    UMAP and embeddings: basic plots, select cells, customize
    PCA diagnostics: loadings, variance ratios, overview
    Expression plots: summaries, heatmaps, matrices, trees, builders
    Expression tracks: cell-level profiles, hover, shared zoom and a group tree
    Ranked genes: stored scores and expression plots
    Scanpy compatibility: tested versions, differences, limits
    API reference
```

Start with the UMAP and expression guides. Give PAGA and data-check examples their
own guides as those plots are reviewed, rather than publishing the whole current
expression notebook as one long page. Keep one example source for the rendered
page and its downloadable notebook. Extract focused guides from the current
workflows when their layout is agreed; do not maintain hand-copied examples.

#### Example checklist

The first UMAP page proves page/notebook rendering. It is not the full example
set. Expand the section by user task, drawing from the two existing development
workflows and the official Scanpy plotting tutorials. Each distinct supported
plot gets a runnable example; aliases and small option changes can share one
example. Keep the first plotting call short, then demonstrate useful interaction
or customization. STATUS owns delivery states and the active queue.

| Guide | Examples to include |
| --- | --- |
| UMAP and embeddings | Categorical/gene UMAP, linked selection and Python retrieval, category order/palettes, continuous bounds, outlines/stored neighbor edges, PCA, cell/gene scatter and embedding density. The custom color-range UMAP uses all 36,785 ovarian cortex cells from Expression Atlas E-MTAB-8381, loaded through Scanpy in one line and explicitly prepared with public Scanpy calls. Use `sc.datasets.pbmc3k_processed()` for PCA/t-SNE examples with saved coordinates. Compute missing diffusion coordinates explicitly with a fixed seed and show components 2 and 3. The existing preparation cache supplies page data; the downloaded notebook runs the visible Scanpy calls. |
| PCA diagnostics | Loadings, variance ratios and the composed PCA overview, using the supplied PCA results. Link back to the embedding guide for PCA scatter. |
| Expression plots | The same marker dictionary in dotplot, matrixplot and cell heatmap; one explicit Scanpy group tree reused by all three; row zoom, dotplot ruler, optional gaps and zoomed values. Add concise DotPlot/MatrixPlot builder examples after the basic calls. |
| Matrices and trees (on the expression page) | Supplied numeric matrix, stored group correlations, standalone group dendrogram and cell/gene clustermap. Show optional values and zoom; distinguish stored trees from explicitly requested Python clustering. |
| Expression tracks | Basic per-cell tracks and marker groups ordered by a Scanpy-computed group dendrogram. Reuse packaged PBMC data; demonstrate aligned x zoom and hover. Explain stepped bars versus Scanpy's continuous fill. Ranked tracks follow their future implemented API. |
| Ranked genes | Stored rank/score labels and ranked dotplot/matrixplot/heatmap calls; fold-change dots and adjusted-p-value tiles share explicitly prepared complete Wilcoxon rankings. Summary dotplots/matrixplots keep fixed axes with hover; the individual-cell heatmap retains row zoom. Preserve the packaged score results under their original key. The page loads matching cached rankings; the downloaded notebook runs the visible Scanpy preparation. |
| Data checks | Highest-expression genes on counts; stored highly-variable-gene statistics with an optional cutoff preview; Scrublet score distributions with an optional threshold slider. Explain that previews do not change saved classifications. The legacy dispersion entry can share the variable-gene example. |
| Dataset variety within guides | Use different, larger real datasets through one-line `sc.datasets` loaders in the relevant plot examples. Keep data loading simple and show any required Scanpy analysis explicitly. Reuse prepared inputs for page builds. Verify dimensions, selected-column access, provenance and useful interactions. Do not add a separate larger-data page or commit datasets. |
| PAGA | Group and continuous node colors; graph/embedding comparison; adjacency heatmap and connectivity strips; supplied path as heatmap and lines. Use explicitly computed Scanpy PAGA and shared positions. |
| Ordered profiles | Stored DPT groups/pseudotime and DPT expression; supplied time-series heatmap, points and subplot composition; stored simulation points/heatmap with optional run focus. Explain actual sample order and keep separate runs separate. |

Dataset variety started with Scanpy's built-in loaders. The user then requested
a larger Expression Atlas study on 27 October 2026. Keep loading to one line and
vary inputs within the relevant guides:

| Dataset | Cells | Use and remaining work |
| --- | --- | --- |
| `sc.datasets.pbmc68k_reduced()` | 700 | Existing introductory examples with supplied annotations/coordinates. |
| `sc.datasets.pbmc3k_processed()` | 2,638 | PCA/t-SNE examples and existing marker tracks; reuse supplied results. |
| `sc.datasets.pbmc3k()` | 2,700 | Existing count/QC examples. |
| `sc.datasets.ebi_expression_atlas("E-MTAB-8381")` | 36,785 | Existing custom UMAP: public ovarian cortex study, sparse counts, 2,000 variable genes for PCA, explicit Scanpy neighbors/UMAP, VWF expression, native zoom/hover and smaller points. Keep all Atlas cells; this is not a reproduction of the paper's analysis. |
| `sc.datasets.paul15()` | 2,730 | Candidate mouse expression/graph examples; review provenance and show any needed Scanpy preparation explicitly. |
| `sc.datasets.moignard15()` | 3,934 | Candidate mouse embryo diffusion/profile examples. Review provenance and the loader's optional Excel dependency before adding an example. |

Use full datasets where the plot supports them. Do not enlarge examples with
synthetic cells or replicate rows. Add no dataset-specific runtime adapter or
separate large-data guide. Downloads and analysis belong in a guide's explicit
preparation, with cached page inputs. Other Atlas studies remain optional future
work; this example needs no new dependency or dataset-specific runtime code.

The PAGA guide shows group, gene, numeric-score and degree colors, a largest
component, both adjacency modes, the linked graph/UMAP comparison and both path
modes. Its basic network demonstrates the native edge cutoff. The profiles guide
shows supplied heatmap/points/subplots, stored Krumsiek11 runs as points and a
heatmap, and DPT groups/expression. Demonstrate native run/gene focus and fitted
values where offered. Keep the PBMC score order distinct from simulation time
and inferred pseudotime. Use the existing preparation cache for PAGA/layout/DPT;
ordinary Sphinx builds must not compute those results or simulate new data.

For each guide, adapt an existing working example rather than invent a new
analysis. Reuse packaged data or a reviewed prepared fixture instead of invented
cells or analysis results. Label simulations as simulations. A missing released
native capability stays out of the guide. Violin, ranked tracks and spatial examples
follow their implemented and reviewed APIs, rather than appearing as placeholders.
Do not publish empty guide pages. Keep the API reference complete even when an
example guide has not yet been extracted. As the guides replace development
workflow sections, retire redundant examples through the existing clearance
process rather than maintaining two user-facing versions.

Keep related examples together: matrices and trees extend the expression page;
PCA diagnostics and ranked genes have focused companion pages. Each delivered
page needs its own notebook, live charts, working download,
explicit preparation, fresh-kernel run and observed enabled interactions. Check
normal and narrow widths. Small, bounded preparation such as the packaged PBMC
group tree, density on 700 supplied 2D coordinates, or clustering the bounded
700-cell × 10-marker clustermap is allowed in the build and must be explicit.
Expensive
embedding, differential-expression or graph analysis must use reviewed prepared
inputs or be shown as a Jupyter-only step with matching prepared page data.

Each example has one or two short sentences, code and a live chart, in that order.
Use plain user-facing language. Explain what the plot shows, how to use it and
any limit that affects the task. Put module details, helper reuse, milestone IDs,
test counts and benchmark notes in contributor/project records. Shorten the
existing guide while keeping its compatibility facts accessible in the supported
options page and API reference.

The first page design is **plot, select cells, customize**. Start with packaged
Scanpy data that already contains coordinates. Show
`import genome_spy.integrations.scanpy as gsc` and one plotting replacement.
Say that users calculate their own embeddings with Scanpy first. Use direct
instructions such as "Scroll over a plot to zoom. Drag to pan. Hover over a cell
for details." Mark live Python examples with "Run this cell in Jupyter."
Check these instructions against the actual enabled interactions.

Review navigation, status/version labels, code visibility, chart placement,
download/run links, narrow-screen/large-chart behavior and Python-only retrieval.
No empty library cards. Retain the dedicated UMAP workflow and shared expression
workflow under this workspace as the starting examples. Each downloadable guide
notebook must run independently with explicit preparation and tested versions.
Add examples only when their plotting APIs are implemented. The
ordinary Sphinx build must not run unbounded analysis or downloads. A static page
can run hover/brush/count; Python subset retrieval requires a live kernel.

For guides with prepared analysis or downloaded data, including ranked genes, run
`uv run integrations/scanpy/prepare_guide_data.py` explicitly before Sphinx.
Notebook metadata names the ignored H5AD inputs; preparation uses the notebook's
own code, and page builds load those inputs while showing that code. Source,
Scanpy-version and file hashes prevent silent reuse of stale/corrupt results.
Downloaded notebooks perform the same visible preparation in a fresh kernel.
Keep this build helper in the Scanpy workspace and rendering in the existing
notebook extension; no production plotting code depends on either.

The documentation design is ready to implement when the navigation and UMAP page
layout are reviewed, the page/notebook source approach is demonstrated, every
example has a short purpose and interaction instruction, and browser-only versus
live-Python behavior is clear. Publication requires the notebook download to run
from a fresh kernel and the rendered page to work at normal and narrow widths.

Adapt the official [core plotting tutorial](https://scanpy.scverse.org/en/stable/tutorials/plotting/core.html)
and [customization tutorial](https://scanpy.scverse.org/en/stable/tutorials/plotting/advanced.html)
as families arrive. Keep upstream analysis steps explicit; replace the supported
plotting calls. The tracked pinned signature inventory and installed 1.11.5 source
remain authoritative where the moving stable tutorials differ.

Release acceptance for the implemented-scope publication: one rendered real tutorial
page and working notebook download, observed native interactions, offline delivery,
reproducible artifacts and reviewed provenance; an accurate full-core inventory
and supported parameter/method coverage evidence; tested resource
limits and version range. Update STATUS with the release and residual scope before
clearing any completed working plans. Another library starts with its own small
contract, inventory and workflow, reusing this layout without assuming Scanpy's
AnnData semantics apply to it.


### Linked expression documentation example

The user selected a native UMAP-linked heatmap summarized by cell type on
27 October 2026. First deliver a runnable guide, not a new public plot family:
reuse the existing UMAP brush and compose native gene-by-cell-type means with
one selected-vs-all gene histogram. Read a bounded resident gene panel through
Scanpy's public accessor; filter before folding genes in the browser. Preserve
fixed domains/order/bins, independent all-cell reference, native clear semantics
and selected counts. Empty groups remain absent rather than becoming zero means.

Use a native magenta–black–yellow range with an explicit zero midpoint for the
stored scaled values. This demonstrates the palette through an ordinary Scale;
a named cmap alias and a general linked-plot helper are outside this first slice.
Acceptance: source-oracle means/counts, histogram normalization, real brush/clear,
page fit, unchanged reference and an output-free downloadable notebook. Test the
700-cell packaged example honestly; large-data live aggregation remains unverified.


### Linked expression builder

The user chose a class matching the DotPlot/MatrixPlot builder conventions on
27 October 2026. `gsc.pl.EmbeddingSummary` is now an implemented preview. This is a
GenomeSpy extension; no corresponding Scanpy class is claimed. The native boundary
agreement and full retained-memory/resource gates below remain open for release.
Heatmap gene controls also await the released categorical-mapping fix (C18);
changed row positions must match visible GPU pixels, not only means or SVG export.

- Construction initially accepts unique gene names (string or sequence), one
  categorical observation column as `groupby`, `basis="umap"`, `use_raw`/`layer`,
  `gene_symbols`, explicit category order and extra `obs_keys` copied once. Reject unsupported mappings, repeated
  genes, multiple grouping keys and numeric grouping rather than silently changing
  their familiar Scanpy meanings. Reuse `grouped_expression`'s cell-level preparation
  where compatible; do not duplicate source lookup or grouping rules.
  Prepare a detached cell table and requested gene columns once, without display
  or AnnData mutation. Use internal feature fields independent of gene labels.
  Keep cell-level values: means are recomputed by native browser aggregation when
  the brush changes, not frozen at construction like a static MatrixPlot summary.
- Start with the embedding. `add_heatmap(...)` and `add_histogram(...)` enable
  panels and accept a side, dimensions and genes from the constructor's pool.
  The heatmap accepts a subset; the histogram accepts a gene subset or one
  loaded numeric observation key via `obs=...`. `add_composition(...)` accepts a
  loaded categorical observation key, defaulting to the UMAP grouping column.
  Heatmap/composition calls replace their panel; `show=False` hides it. Keep one
  histogram group per side: same-side calls replace that group and `show=False`
  removes only that side. Use a small side-keyed dictionary, without a panel registry.
  The user expanded the histogram slice to several genes on 27 October 2026.
  Reuse the single-histogram renderer: native vertical concat for left/right
  groups and horizontal concat for top/bottom groups. Dimensions apply to each
  histogram. The guide shows two histograms left and three below the same UMAP;
  verify all five means-free distributions, independent histograms, one cohort key,
  unchanged references and shared-brush behavior at desktop/narrow widths.
  Optional gene_controls on histograms/heatmaps create native
  dropdowns per histogram/heatmap row, drawing choices from constructor genes.
  Controls belong to the composition root, with no AnnData reads or callbacks.
  Histogram bins cover all candidate genes when controls are enabled; heatmap
  order follows its controls, with duplicate choices shown once by the native scale.
  The guide uses fixed gene lists without dropdowns at the user's request
  (28 October 2026). After adopting the release with interactive legends, update
  these examples to native legend-based gene selection. Retain the existing
  dropdown API tests and the C18 regression until its released fix is verified.
- `add_tracks(...)` adds one marker-track panel using constructor genes and the
  existing tracks renderer. Reuse `heatmap_values` for group order/original row
  positions and the prepared group color scale. Keep one shared cell table with
  stable observation IDs and fixed track slots. A native interval filter draws
  selected-cell marks over a faint full-cell reference; clearing restores all cells.
  No custom membership expression, browser listener or local Core patch is allowed.
  Preserve independent UMAP/track axes; optional x zoom is shared by tracks and
  category strip. Group gaps and track spacing are explicit and default to zero.
  The PBMC3k guide uses saved UMAP coordinates and raw log-normalized expression;
  no embeddings, normalization or trees are recomputed. Verify source values,
  duplicate-label identity, colors, independent ordering, canvas opacity, hover,
  clear, gap/zoom registration, desktop/narrow delivery and fresh-kernel execution.
- `style(...)` controls UMAP size/appearance and composition spacing;
  `legend(...)` controls the native collected legends, default bottom. Keep
  unrelated scales independent and avoid child placements that defeat collection.
  Heatmap options include the shared Seurat preset and color limits; do not
  recompute expression scaling. Gene/group order and histogram bins stay fixed
  while brushing; optional gene dropdowns change the displayed genes.
  `add_heatmap(show_values=False)` optionally reuses the shared native fitted mean
  text, including two-decimal formatting and contrast. Keep summary data on its
  named tile unit when a text layer is added.
- Exclude missing expression before means and histogram binning; normalize each
  histogram over valid values in its cohort. Missing/all-missing groups have no
  invented zero mean or zero-expression bin. Keep selected-cell counts distinct
  from valid-expression counts. Reuse resident-source guards and selected-column access. Do not impose a fixed
  cell or value cap; measure payload, aggregation and interaction costs with large
  inputs rather than rejecting them at an arbitrary threshold.
- Methods mutate the builder and return self, like DotPlot/MatrixPlot.
  The constructor accepts the embedding title and each add method accepts its
  panel title: omitted retains the automatic default, a string overrides it,
  and None omits the native title property. No generated title is forced.
  `to_chart()` creates a fresh ordinary GenomeSpy chart; `show()` displays it.
  Use the returned chart's existing widget, composition and save methods. Later
  builder edits must not change previously returned charts or reread expression.
- Reuse data access, guards, embedding, brush, palette and native chart helpers.
  Do not inherit `_GroupedPlot`: its static group-summary/tree state does not own
  this interactive cell-level workflow. Add no new general builder framework or
  redundant function wrapper.

UMAP defaults to a square plotting area and equal pixels per coordinate unit.
Pad the shorter domain around its center without altering stored coordinates;
constructor `zoom=False` retains ordinary drag selection. Opt-in `zoom=True`
reuses the shared embedding scales and native interval gestures: wheel zoom,
pan outside the selection, Shift-drag to create a selection, and drag inside it
to move it. Keep brush intervals in data coordinates while navigating. Verify
equal coordinate units during wheel/pan gestures inside the plot, count/summary
agreement after navigation, and independent track axes. Axis-gutter interactions
follow native per-axis behavior; initial isotropy does not lock those axes together.

Placement uses native concat for independent UMAP/summary axes and surround for
aligned annotations/marginals. Surround's aligned axis cannot be disconnected;
do not force cell-type/gene axes onto UMAP coordinates or add positioning wrappers.
Supporting independent surround panels would require separate upstream design.
Resolve x/y independently at every independent-panel composition boundary.
Own the shared brush value at the builder's composition root, with one UMAP
controller using native `push="outer"`; count and summary consumers descend from
that owner. Constructor `show_count=True` preserves the count by default; False
omits its dataflow without changing the brush or linked panels. Validate boolean
input before reading data. Show the total count inside the brush, using native formulas on the
single count row and ranged text tied to all four interval bounds. Hide it when
cleared or too small to fit; no separate count row or point effects. Reuse brush
helpers at this boundary rather than nesting the finished
counted UMAP chart unchanged beside its consumers. Collect distinct cell-type,
expression and cohort legends at the root, removing conflicting child placements;
collection does not merge independent scales.

**Native correctness gate found in review:** the current selection filter includes
the upper boundary, while the embedding count and Python mask exclude it. Require
one convention across native filtering, count and mask, including zero-width and
exact-boundary cases. Do not add a parallel hand-written membership predicate to
hide the discrepancy. If a Core correction is needed, follow the upstream planning
and PR skills and wait for its published release, as previously agreed. Layout and
data preparation can proceed independently; coherent linked selection gates release.

Delivery: settle the chain API, then extract the working example's preparation,
summary rendering and composition helpers. Implement/export the builder and
replace the notebook's construction code with its chain. Keep browser-only native
updates, no-selection behavior, unchanged all-cell reference and no point effects.

Acceptance: constructor data snapshot and no mutation; gene/layer/group choices;
repeat/hide/reposition panel calls; style/legend changes without new data reads;
fresh chart snapshots; real brush updates with every supported panel side and two
composed instances; collected legends and independent domains; square/isotropic
UMAP; source-oracle means and every histogram bin/count/percentage, including
negative values and exact bin edges; punctuation in gene labels and missing
expression, including all-missing genes; exact brush-boundary membership; clear
versus an active brush selecting no cells; unchanged reference; page fit,
notebook/docs, types and lint.
Measure cells × genes, sparse allocations, serialized payload, initial render,
large-selection updates and retained memory using the existing resource gates.
No million-cell aggregation claim or new performance framework is part of this slice.

Review and examples (27 October 2026): keep the existing detached preparation and
shared embedding, brush, palette and fitted-value helpers. Heatmap axis/tooltip
labels must use the requested grouping key, including non-cell-type annotations.
Add two independent guide examples using the existing builder: LYZ distribution
left of the UMAP with legends right, and stored detected-gene QC above a
phase-colored UMAP with marker means right. No new panel types, analysis or layout
framework. Check source-oracle summaries, independent brush state, clear, square
UMAP and actual desktop/mobile Furo bounds for all three guide charts.

### Further brush-linked summaries

User approved the categorical and numeric metadata slice on 27 October 2026;
both are now implemented previews. Other candidates below remain proposals.
The guide places the heatmap below the UMAP/histogram/composition
row. Native concat places left/right panels first, then top/bottom panels across
that row; dimensions remain native layout budgets.

| Priority | Data and question | Proposed view |
| --- | --- | --- |
| Implemented preview | Categorical obs: cell type, donor, sample, batch or condition. Which groups make up this selection? | Native nested-band horizontal paired percentage bars; count/cohort denominator tooltip. Category colors and order reuse the embedding helpers; missing values form a visible NA category. |
| Implemented preview | Stored numeric obs: QC metrics, doublet scores, gene-program scores or pseudotime. How does this region differ? | Reuse fixed-bin selected/reference histograms via obs=; normalize valid values and show valid/missing counts. Read stored values only; ECDF remains later. |
| Later | A chosen marker panel. Is a mean driven by a few cells or broad expression? | Optional selected/reference mean or delta heatmap; detection-fraction dots only with a declared expression source and threshold. Zero in scaled expression is not a detection threshold. |

Selected-cell counts per cell type could sit above the heatmap columns as a native
surround track sharing their categorical x axis. Independent donor/batch panels
remain concat views; distinguish cell counts from per-gene valid-value counts.

Keep comparison semantics explicit. "Share of selected cells" and "fraction of
each category captured" have different denominators; the first is the composition
default, the second is a separately labeled later option. Preserve category order,
colors, bins and all reference categories while brushing. Missing metadata must
have a visible count or category rather than silently changing denominators.
Retain no-selection versus active-zero-selection semantics.

Reference initially remains all loaded cells. An optional unselected-cell reference
could make contrasts clearer, but must be labeled and use consistent denominators
across panels; it is not yet implemented. Users choose loaded genes/obs columns
explicitly to bound transport and browser work. Keep live updates to native
filter/count/aggregate operations. Differential expression and enrichment require
explicit analysis on a selection snapshot, not recomputation during drag.

Implementation keeps one panel per type and one detached observation snapshot.
The constructor's obs_keys plus genes share the pre-read value guard; presentation
methods do not retain or reread AnnData. Histogram and composition reuse one native
cohort-count/percentage transform helper. Empty selected cohorts produce no summary
rows, with the brush's total count still showing zero. The guide uses the packaged
phase and S_score annotations, without rerunning cell-cycle scoring.

Stored metadata sources: Scanpy's [QC metrics](https://scanpy.scverse.org/en/stable/generated/scanpy.pp.calculate_qc_metrics.html)
and [gene scores](https://scanpy.scverse.org/en/stable/generated/scanpy.tl.score_genes.html).

### Optional grid pointer feedback — 27 October 2026

Keep DotPlot/dotplot's existing highlight=False default and highlight=True native
ruler. Extend the same option to MatrixPlot/matrixplot, heatmap, matrix and
clustermap. Add highlight="outline" using the DepMap gallery's native ephemeral
point-selection plus conditional stroke pattern on existing marks. Keep
feedback independent of tooltip hover, with no new data overlay, Python callback
or custom listener. One shared helper owns grid feedback and optional fitted
values; value text must not inherit tile strokes. Preserve normal borders, value
and size encodings, missing/zero-area marks, repeated slots and aligned guides.
Validate flags before data access. Verify leave/clear, zoom, tooltip independence,
rendered outline/ruler geometry and unchanged data. Keep profile/time-series
rulers and unrelated plot interactions unchanged.

Grid feedback review: use native conditional order as well as stroke for the
hovered mark. Centered rect strokes overlap adjacent fills, so draw priority is
required for equally visible edges. Keep fitted-value text at normal order and
remove copied hover parameters from labels. Verify actual WebGL edge pixels on
an interior tile, with and without values, as well as native selection/clear and
SVG behavior. Examples should opt into rulers or outlines explicitly; package
defaults stay off. Keep hover parameter construction inside outline mode and use
simple branches for the numeric-matrix composition.

### Concise public compatibility guide — 28 October 2026

Keep the public compatibility page focused on current callable coverage, shared
renderer differences and limitations that affect users. Link guides and API
docstrings for usage and options. Retain detailed contracts, computation reuse
decisions and validation evidence in COMPATIBILITY.md; STATUS owns delivery
readiness. Preserve existing contract anchors when moving workspace references.

### Saving and image export guide — 28 October 2026

Show HTML/JSON saving and native PNG/SVG controls on a real Scanpy plot. Reuse the
shared export user guide and notebook renderer. Let notebook chart metadata opt
into existing native controls, with shared validation and no custom download code.
Keep save/display cells runnable in the downloaded notebook but unexecuted by
Sphinx. Check actual image downloads, output-free source and the page/download match.
