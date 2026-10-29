# Scanpy implementation status

Updated: 2026-10-29. [PLAN.md](PLAN.md) owns scope and acceptance criteria;
[README.md](README.md) maps the source files; [COMPATIBILITY.md](COMPATIBILITY.md)
records detailed parameter contracts. This ledger describes the integration
branch, rather than the published 0.7.0 package.
The short [future-work handoff](FUTURE.md) summarizes remaining coverage and the
planned adoption of interactive legends and PAGA rule outlines.

## Current position and next work

The integration replaces supported plotting calls while Scanpy owns analysis.
Use `import genome_spy.integrations.scanpy as gsc`. The implementation lives in
`src/genome_spy/integrations/scanpy/`, grouped into six private family packages.
Shared helpers stay at the root and namespace imports remain lightweight.

The runtime and optional dependency accept Scanpy >=1.11.5,<1.13, excluding
prereleases. Compatibility covers the pinned 1.11.5 environment and Scanpy 1.12.4
on Python 3.12 with current scientific dependencies. The reference environment,
image comparisons and legacy reference signatures stay pinned to 1.11.5. A separate CI job checks
1.12.4 without changing those references.

Swapped dotplot scaling follows the installed Scanpy version through the shared
builder. Scanpy 1.12.4's automatic PAGA tree layout has an upstream missing-argument
bug; the adapter reports it without a fallback, while supplied positions still
work. Deprecated upstream aliases retain their explicit native arguments.
New group-specific dotplot colormaps remain unsupported. See the detailed
[version differences](COMPATIBILITY.md#scanpy-112-differences).

Publication targets a normal package release with a documented supported subset.
Remaining plot families will follow released GenomeSpy capabilities. Milestone
states below describe coverage; they do not require a preview release label.

### Current work queue

1. Complete the [test cleanup and CI selection](PLAN.md#test-cleanup-and-ci-selection)
   before publication. The initial CI-selection cleanup is followed by a deeper file, fixture and
   duplicate-coverage cleanup; current verification is recorded below.
   [PR #20](https://github.com/genome-spy/genome-spy-python/pull/20) remains open.
   Verify the updated hosted selections before closing this maintenance slice.
   Merge and publication still require approval.
2. Keep future version expansions behind compatibility checks; maintain the
   parameter contracts and recheck the upstream PAGA tree-layout issue.
3. Classify known limitations below. Fix, reject or document user-visible cases
   before advertising support; expected failures alone do not establish readiness.
4. Finish the existing plot-by-plot publication reviews, installation checks,
   clean-wheel examples, CI and strict docs build. New plot families remain deferred
   except already authorized tracks work. The next M09 increment is ranked tracks.
5. Adopt the forthcoming released interactive-legend capability before upgrading
   linked-expression examples to legend-based gene selection. Their gene dropdowns
   are currently absent. Preserve the C18 API regression until its released fix passes.

The working guide uses fixed gene lists, native brushing/counts, UMAP-linked
histograms/means and PBMC3k tracks. Embedding and expression workflows remain
separate; focused guides provide the user-facing pages and downloads.

The prototype value and clustering-distance caps are removed. Heatmaps, tracks,
linked summaries, ranked heatmaps, PAGA paths/adjacency and clustermaps accept
larger inputs without an adapter-imposed threshold. Shape, source and storage
checks remain. Large-input tests check selected-column allocation and real
clustering beyond the former distance threshold. Relevant tests passed on both
Scanpy versions: 782 passed and one existing expected failure each.

## Test cleanup audit

The initial pass removed seven manual benchmarks, reduced repeated parameter
grids and notebook assertions, and introduced fast/reference/workflow selections.
The deeper pass also reduces the maintained file and reference footprint:

| Measure | Before deeper cleanup | After |
| --- | ---: | ---: |
| Integration test/support/fixture files | 140 | 61 |
| Python files | 127 | 48 |
| Python lines | 27,586 | 25,744 |
| JSON fixture lines | 18,504 | 13,574 |
| Separate reference generators | 11 | 0 |
| Image-only reference helpers | 0 | 1 |
| Total PR files | 252 | 173 |

Twenty-three tiny data/fixture modules are consolidated into five family modules;
ranked inputs remain separate. PCA diagnostics and shared grid options each have
one test module. Every public entry still has a signature contract check, now
against installed Scanpy. Only four legacy aliases retain frozen parameters.
Unused image checksums, source hashes, version/style metadata, generator reports
and bookkeeping-only tests are removed. The eleven numerical fixtures retain
identical values and geometry. All 123 temporary reference images were verified
pixel-identical to the previous exports, with unchanged registration/tolerances.

Repeated display checks and invalid feedback cross-products now have shared
owners plus public routing checks. Unsupported triangle-shape experiments are
retired; explicit rejection remains. Actual legend clipping and C13/C18 renderer
regressions remain, including strict expected failures that detect upstream fixes.
The CSC/LIL, sparse orientation, filtered-view, dense/raw allocation, source
precedence, mutation, stable selection, tie-order and observed interaction tests
remain. Small allocation regressions replace the removed timing/heap reports.

A follow-up removes another 477 Python lines and 98 repeated fast cases.
DotPlot and MatrixPlot now share builder tests for chains, totals, hidden trees,
swapping and display, while keeping family-specific color/size, supplied-data
and allocation regressions. The display contract covers its shared owner and
representative single/multi-panel charts without a large per-plot data factory.
All public calls still reject invalid display options before optional imports.
Fifty-one repeated generic-option cases are removed; shared guards and distinct
plot-specific errors remain. Sixteen plot-area captures across fourteen browser
files share one helper with the same crop and pixel scale.

The file-layout pass reduces Scanpy test files from 79 to 34: eighteen Python
modules and sixteen browser modules. The files follow plot families and shared
behavior. Pytest classes keep each section's fixtures separate; 540 regrouped
test functions and all 2,572 collected cases are preserved. Shared imports are
combined, helper/fixture names stay distinct, and CI paths and documentation
links follow the new files. This is a file-layout reduction, not removed coverage.

Current collection: 1,641 fast Python cases, 321 live-reference cases, two
workflows and 608 browser cases, including 56 smoke cases. The new collection
still exercises the complete retained suite when markers are not filtered.
PR jobs run fast checks on both Scanpy versions and browser smoke once. Main,
full dispatch and release run the full selections; release sets `full_scanpy`.
Base jobs test lightweight imports and missing extras without the scientific suite.

Previous reduction validation:

- Scanpy 1.11.5 non-workflow Python suite: 1,960 passed, two existing expected
  failures. Scanpy 1.12.4: 1,957 passed, five existing expected failures.
- Both builders and every changed screenshot-helper call: 27 browser checks
  passed, including complete charts, totals, composition, zoom and HTML delivery.
- Lint, format, collection and lock consistency passed. No production API,
  numerical fixtures, image tolerances or regression expectations changed.
- Previous revision CI passed all six configured jobs. Its full local browser
  verification covered 602 passing cases and six expected failures; the current
  follow-up reruns affected browser paths rather than every unchanged case.
- Workflows, base-only tests and the remaining browser checks were not rerun in
  this follow-up. Both workflows and 407 base checks passed in the preceding pass.
  All 123 reference exports previously matched their old pixels exactly.

File-layout verification reruns both Python suites and one browser case per
section plus every smoke test. The naming collision found in the moved Matrixplot
helper was corrected and its complete 162-case grouped-expression module passed
on both Scanpy versions. Collection, lint, format and workflow lint passed.
Workflows and unselected browser parameter combinations are unchanged and are
not rerun in this pass.

The first hosted layout run passed Python compatibility and the other jobs but
failed one UMAP smoke check: it reset the scales while wheel motion was still
running. A local probe confirmed that remaining wheel frames overwrote the reset.
The check now waits for completed navigation through the shared helper, then
verifies both axes against their captured initial domains. Three fresh browser
runs passed, and all 65 UMAP/shared-helper grid checks passed.
No Core bundle, timeout or visual tolerance was changed.

The refreshed hosted run remains the clearance gate. Keep this maintenance slice
open until its configured jobs pass. Generated images, reports, inventories, logs
and notebook outputs stay outside Git.

## Milestones

States apply to the stated scope; a closed preview is not a closed full family.
The completed structural update is M00.c/d, not a new plotting milestone.

| Milestone | State | Delivered evidence or remaining work |
| --- | --- | --- |
| M00 foundation/layout/lifecycle | Closed (foundation scope) | Signature/version fixtures, sole integration namespace, source/test/workflow layout, full inventory and shared lifecycle exist. Initial relocation is `67de26e`; current verification below. |
| M01 UMAP/linked preview | Closed (preview only) | Runtime modules, dedicated PBMC UMAP notebook, semantic/reference/browser tests and resource baseline listed below. Parameter debt remains explicitly assigned to M07/M14. |
| M02 grouped access/dotplot | Closed (plain-chart preview with hover) | Shared access/statistics, public dotplot, index slots, native dots/labels/brackets/guides, summary hover, 11 complete frozen chart cases, real PBMC workflow and sparse/browser resource check. See retained evidence and explicit limits below; trees/builders/selections are not closed. |
| M03 matrixplot | Closed (plain-chart preview with hover) | Shared grouped means/access/layout, one-pass scaling, authoritative values_df, native index tiles/edges, 13 frozen chart cases, packaged-PBMC workflow and sparse/browser resource observation. Trees, builders and broader normalization remain open. |
| M04 trees/correlation | Closed (standalone/correlation and dot/matrix attachment preview) | Public Scanpy computation, stored-result validation, shared native orthogonal links, leaf/marker permutations, registered charts, resize/hover checks and resource observation below. Later-family attachments remain assigned. |
| M05 heatmap/matrix/clustermap | In progress; bounded previews verified | Native heatmap/clustermap track migration and M05.f are closed for WebGL/notebook/HTML. M05.d and broader kwargs/delivery remain open. |
| M06 ranking/ranked summaries | Closed (bounded preview) | M06.a–d have semantic/chart/workflow/interaction and resource evidence. Broader compatibility remains M14; native builders remain M13 and ranked distributions/tracks remain M08/M09. |
| M07 embeddings/scatter/PCA | In progress | M07.a/b resource gates pass; categorical-guide rendering remains open under C11. M07.c loadings/variance/overview and M07.d colorbar placement are Closed for their stated scope; other options remain open. |
| M08 violin/stacked/ranked | Planned; filled rendering blocked | Data/density work can proceed; full native filled geometry needs a released capability (C01). |
| M09 tracks/ranked tracks | In progress; cell-track preview verified | Shared heatmap preparation and native per-cell rects. See [M09 evidence](#verification). Ranked tracks remain unimplemented; exact fill remains C01. |
| M10 QC diagnostics | In progress | M10.a/b/c bounded previews are verified; broader scale/option compatibility remains M14. This does not close the full family. |
| M11 trajectories/graphs/series | In progress; supplied-series/simulation, DPT-expression and both adjacency previews closed; PAGA/compare available and path heatmap implemented | DPT/PAGA direct-reference gates, comparison corrections and broader PAGA options/entries remain open. Native rules handle straight undirected edges; C04 is limited to unverified connected paths. |
| M12 density/spatial | In progress; density preview closed, full spatial blocked | Stored-density preview evidence is retained under M12.a; broader parameters remain M14 and image-backed spatial requires C02. |
| M13 builders | In progress; DotPlot and MatrixPlot previews closed | Both share concrete group layout and their existing functional statistics/renderers, with upstream/native/workflow/resource checks. StackedViolin and remaining styles/constants stay open. |
| M14 compatibility/docs/release | In progress; Core 1.2 adopted | Focused guides, prepared inputs and native interaction checks are available; see the current documentation inventory above. Optional examples, plot reviews, compatibility closure and release gates remain open. |

## Public callable coverage

The [pinned inventory](../../tests/integrations/scanpy/fixtures/api.json) has 50
entries: 45 plotting functions including aliases, three builders, two settings
helpers. 41 plotting functions/builders are available as supported subsets; 7 plot/builder
entries remain unimplemented. The two settings helpers are external renderer
exceptions. This count measures entry availability, not parameter completeness.
No placeholder functions are exported for planned work.

| Public entry | Availability | Delivery milestone |
| --- | --- | --- |
| `DotPlot` | Partial native builder available; bounded preview verified | M13.a; square-background styling and broader options remain M13/M14 |
| `MatrixPlot` | Partial native builder available; bounded preview verified | M13.b; broader styles/constants remain M13/M14 |
| `StackedViolin` | Not implemented | M13 (after M08) |
| `clustermap` | Partial bounded preview available | M05.c; remaining options/transport M05.d/M14 |
| `correlation_matrix` | Partial preview available | M04 preview; normalization/options M14 |
| `dendrogram` | Partial preview available | M04 preview; options/export M14 |
| `diffmap` | Shared stored-2D preview | M07.a; remaining options M07.d/M14 |
| `dotplot` | Partial plain-chart preview; limits above | M02; trees M04; methods M13 |
| `dpt_groups_pseudotime` | Metadata-only preview; component/chart/workflow/resource checks verified | M11.b; direct parent-reference gate blocked upstream |
| `dpt_timeseries` | Stored-X heatmap/point preview available | M11.b expression preview closed; broader storage/style/export M14 |
| `draw_graph` | Shared stored-2D preview | M07.a; remaining options M07.d/M14 |
| `embedding` | Shared stored-2D preview | M07.a; remaining options M07.d/M14 |
| `embedding_density` | Partial stored-density preview available | M12.a; broader groups, missing values and unsorted mixed ranges M14 |
| `filter_genes_dispersion` | Partial stored-results preview available; legacy | M10.b; remaining compatibility M14 |
| `heatmap` | Partial cell-level preview available | M05.a/b preview; larger transport M05.d; normalization/options M14 |
| `highest_expr_genes` | Partial count-percentage preview available | M10.a; remaining compatibility M14 |
| `highly_variable_genes` | Partial stored-results preview available | M10.b; remaining compatibility M14 |
| `matrix` | Partial supplied-numeric preview available | M05.b preview; broader sources/layout M14; transport M05.d |
| `matrixplot` | Partial preview available | M03 preview; trees M04; methods M13; normalization/options M14 |
| `paga` | Stored undirected graphs with group/numeric/gene/degree colors and optional largest-component views | M11.c; C15 direct component reference and other color/directed/export modes open |
| `paga_adjacency` | Partial legacy-key heatmap/stripplot preview available | M11.d; broader storage/styling/export M14 |
| `paga_compare` | Partial aligned preview; confirmed corrections open | M11.d palette/composition corrections; regular-label/parent limits M14 |
| `paga_path` | Partial stored-path heatmap and native rule-line previews; native checks verified | M11.d; C16 direct return_data gate and broader source/annotation/style options remain open |
| `pca` | Shared stored-2D preview | M07.a; remaining options M07.d/M14 |
| `pca_loadings` | Stored-loadings preview available | M07.c loadings increment; shared ranking preparation/renderer |
| `pca_overview` | Composed stored-PCA preview available | M07.c overview increment; existing three parent plots |
| `pca_scatter` | Alias of the shared pca preview | M07.a; same limits as pca |
| `pca_variance_ratio` | Stored-variance preview available | M07.c variance increment; shared ranking helpers |
| `rank_genes_groups` | Preview: stored score panels | M06.a–c; filtered/nonfinite panels and presentation debt M14 |
| `rank_genes_groups_dotplot` | Preview: expression/statistic colors and expression fractions | M06.a–d; compatibility limits M14, builder M13 |
| `rank_genes_groups_heatmap` | Preview: individual-cell expression | M06.a–c; shares parent heatmap limits |
| `rank_genes_groups_matrixplot` | Preview: expression means or stored statistics | M06.a–d; compatibility limits M14, builder M13 |
| `rank_genes_groups_stacked_violin` | Not implemented | M08; rank access M06 |
| `rank_genes_groups_tracksplot` | Not implemented | M09; rank access M06 |
| `rank_genes_groups_violin` | Not implemented | M08; rank access M06 |
| `ranking` | Preview: supplied score attributes/dictionaries | M06.c; shared native rank labels, dense indices only |
| `scatter` | Cell/gene x/y and stored-basis preview | M07.b; remaining options M07.d/M14 |
| `scrublet_score_distribution` | Partial stored-score preview available | M10.c; remaining compatibility M14 |
| `set_rcParams_defaults` | External: use Scanpy | Renderer exception, M00 |
| `set_rcParams_scanpy` | External: use Scanpy | Renderer exception, M00 |
| `sim` | Partial stored-simulation preview available | M11.a; parent storage/markers/layout M14 |
| `spatial` | Not implemented | M12; image capability C02 |
| `stacked_violin` | Not implemented | M08 |
| `timeseries` | Partial supplied-point preview available | M11.a; remaining storage/markers/layout M14 |
| `timeseries_as_heatmap` | Partial supplied-profile preview available | M11.a heatmap; broader storage/layout M14; transport M05.d |
| `timeseries_subplot` | Partial supplied-point panel preview available | M11.a; broader storage/markers/layout M14 |
| `tracksplot` | Verified bounded preview | M09.a/b; native per-cell rects; ranked tracks and exact fill remain open |
| `tsne` | Shared stored-2D preview | M07.a; remaining options M07.d/M14 |
| `umap` | Partial preview available | M01; completion M07/M14 |
| `violin` | Not implemented | M08 |

## Parameter and method debt

For each new family, add its supported parameter groups and remaining work here
(or link a maintained per-family contract if this section becomes unwieldy).
The frozen API inventory supplies names/defaults; passing signatures is not enough.

| UMAP parameter group | Current support | Completion owner |
| --- | --- | --- |
| Existing 2D coordinates, raw/layer, symbols, masks, categories, sizes/order, native axes/guides | Tested supported subset; exact forms in user contract | M01 preview retained |
| Hover, optional zoom, first-owner interval, linked count and Python retrieval | Tested preview; no point selection or initial interval value | M01; broader native selections M14 |
| Continuous colorbar placement | Four sides/None; native defaults and collection supported | M07.d placement increment closed |
| Point outlines | Shared outline layers, relative widths/CSS colors, scalar styles, hover/zoom/brush | [M07.d outline increment](#verification) closed; square support below |
| Square markers | Native squares in shared embeddings/PCA overview/scatter, including outlines, legends and interactions | [M07.d square increment](#verification) closed |
| Diamond markers and category keys | Native diamonds with Scanpy path widths; keys inherit each panel's marker shape | [M07.d diamond increment](#verification) and [legend follow-up](#verification) closed |
| Triangular markers | Clear rejection; native equilateral paths cannot preserve Scanpy's width and height | [M07.d audit](#verification) closed; support Blocked by C14 |
| Stored neighbor-graph edges | First component pair, native segments and endpoint lookups, scalar CSS styles; explicit restrictions on other forms | [M07.d edge increment](#verification) closed |
| Other graph forms, arrows, scale_factor, broader markers/categorical guide locations | Nondefault forms reject | M07.d/M14 |
| Callable color bounds | Shared resolver with masked/sorted copies, per-panel lists and finite results | [M07.d callable increment](#verification) closed |
| Centered numeric colors | Shared scalar/percentile/callable resolver, per-panel centers and native piecewise color scales | [M07.d center increment](#verification) closed |
| norm | Matplotlib normalization objects remain outside the native boundary | Maintained contract |
| Backed/lazy expression; named scheme with NA legend; category/NA label collision | Explicit current restrictions | M14.c |
| 3D, font atlas/weight/outline and complete typography | Native gaps/limits | M14.a; C03/C05 |
| Image save/autosave | Inactive form only; use native HTML/JSON save | M14.c |
| ax/cax/return_fig, artist methods, Matplotlib color/global settings | Intentional native rendering boundary | Maintained contract, not pending artist emulation |

| Scatter parameter group | Current support | Completion owner |
| --- | --- | --- |
| Observation/variable x/y, exact X_ basis/components, per-axis layers, palettes/groups/order, multiple panels | Tested bounded preview; [contract](COMPATIBILITY.md#scatter-cells-or-genes) | M07.b preview retained |
| Native numeric axes, points/guides, cell/gene hover, optional x/y zoom and dimensions | Shared embedding helpers; no scatter brush/Python membership yet | M07.b; broader selection M14 |
| On-data labels/centroids, margins, highlights, more markers/sizes, 3D and storage/export | Nondefault forms reject; native layout/typography differences recorded | M07.d/M14 |

| PCA diagnostics parameter group | Current support | Completion owner |
| --- | --- | --- |
| Stored finite NumPy loadings, component order/repeats, high/low/top ranks, native sizing/hover and common delivery | Bounded loadings preview; [contract](COMPATIBILITY.md#pca-loadings) | M07.c loadings preview retained |
| Sparse/lazy or nonfinite loadings, full typography and image export | Explicit restrictions; no automatic filtering/analysis | M14 |
| Stored variance ratios, PC numbering, linear/natural-log scores, native sizing/hover and common delivery | Bounded variance preview; [contract](COMPATIBILITY.md#pca-variance-ratios) | M07.c variance preview retained |
| Overview | Verified bounded native composition, parent dimensions/defaults, scatter-only kwargs and one display | M07.c preview retained; parent limits M07.d/M14 |

| Matrixplot parameter group | Current support | Completion owner |
| --- | --- | --- |
| Grouped source/categories/repeated slots, log/means/scaling, supplied values_df, native tiles/guides/edges/hover | Tested preview; exact forms in user contract | M03 preview retained |
| Dendrogram ordering/attachment and compatible stored trees | Verified leaf/marker reordering and native branches | M04 preview retained |
| Optional zoom and fitted plotted values | Shared native grid helpers, annotations follow live index scales | M05.e |
| MatrixPlot builder, semantic styling/legend chains | Native means/supplied values, group tracks, tile styles and color-guide chains verified | [M13.b](#verification); broader forms/constants remain M13/M14 |
| norm/vcenter, remaining pcolor kwargs, backed/lazy/sparse arrays and image export | Explicit restrictions/errors | M14.c |

| Tree/correlation parameter group | Current support | Completion owner |
| --- | --- | --- |
| Categorical groups, guarded local computation, compatible stored results, four orientations, labels, attached dot/matrix trees and correlation numbers/hover | Tested preview; exact forms in user contract | M04 preview retained |
| Stored n_pcs/var_names/use_raw/custom-method results | Render the stored Scanpy snapshot without source reconstruction; users recompute after input changes | Maintained Scanpy cache contract |
| Automatic sparse/backed/lazy tree computation | Explicit Scanpy 1.11.5 limits; use a stored result or resident dense representation | M14.c upstream access review |
| Heatmap attachment | Verified unequal cell-group spans in both orientations, including two groups | M05.a/b preview retained |
| Violin/stacked and tracks attachments | Shared tree helpers available; parent families unimplemented | M08/M09 |
| Correlation norm/vcenter, remaining imshow kwargs, typography and image export | Explicit restrictions/errors | M14.c |

| Clustermap parameter group | Current support | Completion owner |
| --- | --- | --- |
| Resident raw/X, row/column linkage, scaling before distances, masks, annotation tracks, duplicates, native labels/hover | Tested bounded preview; exact forms in maintained contract | M05.c preview retained |
| Large values, backed/lazy data and clustering costs | No fixed value/distance caps; resident-data checks remain. Supplied linkage skips computation; chunked transport remains a performance task | M05.d/M14.c |
| Zoom and fitted values | Shared grid helpers; y-only or both-axis navigation with aligned trees/strips/ticks | M05.e preview retained |
| Linked cell selections | Not implemented | M14.c interaction/options review |
| Seaborn rocket/inset colorbar, custom tree/heatmap kwargs, annotation forms and normalization | Native magma/right guide; unsupported options reject by name | M14.c; Matplotlib objects remain outside boundary |

| Supplied time-series heatmap parameters | Current support | Completion owner |
| --- | --- | --- |
| Resident X, supplied order, default/repeated/2D labels, fractional highlights, native color map and delivery | Bounded preview; transposed/cropped limits match the pinned helper | M11.a heatmap preview retained |
| Hover, y-only/xy zoom, fitted values and dimensions | Existing matrix/grid helpers and native quantitative bounds | M11.a heatmap preview retained |
| Sparse/lazy inputs, full typography/global styles and image export | Explicit restrictions; no implicit analysis or materialization | M05.d/M14 |

| Supplied time-series point parameters | Current support | Completion owner |
| --- | --- | --- |
| Resident profiles, supplied times/order, variable/category/continuous colors, masks, labels, limits, ticks and highlights | Tested bounded preview; no sorting, smoothing or analysis | M11.a point preview retained |
| Hover, both-axis zoom, native guides, dimensions and HTML/JSON | Shared helpers and native points/rules | M11.a point preview retained |
| Subplot public entry and independent native composition | Shared point preparation/rendering with explicit defaults, contextual errors and ordinary native layout | M11.a subplot preview retained |
| Simulation entry, metadata precedence, boundaries, one-based labels and exact local shuffle | Tested bounded preview; points/heatmaps reuse existing preparation/rendering | M11.a simulation preview retained; parent storage/markers/layout M14 |
| DPT group/pseudotime panels, stored codes/ranks/boundaries and missing-time masking | Metadata-only composition with shared points, hover and independent navigation | M11.b implemented; direct parent-reference gate remains open |
| DPT expression entry, saved row indices, X-only access, mode-specific colors/markers and native interactions | Shared heatmap/point preparation and rendering, with direct upstream verification | M11.b expression preview retained; broader storage/style/export M14 |
| PAGA stored undirected graphs, group/CSS colors, public layout computation, sizes, widths, labels and cache controls | Shared validation/colors/domains/units/navigation/delivery; native rules/points/text | M11.c bounded increment; remaining node/edge/export modes open |
| Sparse/lazy inputs, repeated labels, differing per-subset shapes, global styles and image export | Explicit restrictions | M14; Matplotlib objects remain outside boundary |

| Builder surface (all three classes) | Current state | Completion evidence required |
| --- | --- | --- |
| Constructor signatures/defaults and native result delivery | DotPlot and MatrixPlot implemented with pinned defaults, native keyword additions and detached to_chart snapshots | [Grouped builder tests](../../tests/integrations/scanpy/test_grouped_builders.py); StackedViolin remains M13 |
| add_dendrogram/add_totals/swap_axes | DotPlot and MatrixPlot share aligned tree/count tracks, sorting/colors and orientation | [Actual upstream chains and native browser checks](../../tests/integrations/scanpy/browser/test_grouped_builders.py); StackedViolin remains M13 |
| style/legend and useful public defaults/constants | DotPlot dot styles, MatrixPlot scheme/edge styles and native guide controls implemented; square backgrounds and public constant customization remain open | Shared native renderers and chain tests; StackedViolin remains M13 |
| get_axes/figure/artist access | Intentional renderer boundary; no Matplotlib objects are offered | Use builder.to_chart for native configuration/composition; StackedViolin remains M13 |
| make_figure/show(return_axes)/savefig | DotPlot and MatrixPlot omit Matplotlib make_figure/savefig; show(return_axes=True) errors with the native alternative | Native to_chart, show and chart.save contract/tests; StackedViolin remains M13 |

## Native capability ledger

Audit: bundled Core/schema **1.2.0** adopted October 20; the native mark inventory
is still rect, point, rule, tick, text, link and arrow. The October 19 Core 1.0
checks of native rules, formula transforms, excluded scales/axes and tree alignment
remain historical evidence. Recheck each capability before implementing an
affected slice.

| ID | Gap or available capability | Affected work | Resolution/recheck trigger |
| --- | --- | --- | --- |
| C01 | No native filled-area/polygon primitive in bundled schema | Filled violin/stacked densities M08 and exact continuous tracks M09; native per-cell rect tracks are available | Released filled geometry and density/profile chart tests for exact fill; no custom trial geometry promotion |
| C02 | No native raster/image primitive | Full spatial M12 | Released image capability with crop/aspect/zoom registration tests |
| C03 | No native 3D projection | 3D embedding options M07/M14 | Released capability or explicit product scope decision; keep unresolved until then |
| C04 | No general joined-path mark; exact shared-join/end-cap parity is a visual limit | PAGA path lines use verified native window/lead/rules with minor documented stroke differences; other connected cases require their own audit | A released path mark may improve stroke parity but is not required for PAGA path. Keep per-entry gap/order/interaction checks. Native rules also support independent undirected PAGA edges. |
| C05 | Font/text-outline/normalization/NA-guide limits | Parameter closure M07/M14 | Per-option released API inspection and complete-chart tests |
| C06 | Core 1.2 typed surround/facet APIs and native index gaps available; Scanpy migration remains open | Heatmap/clustermap side tracks, related grids, UMAP/repeated panels; M14.b | Use the published heatmap example; verify viewport/scale/guide ownership, required heatmap group gaps and existing navigation/selection contracts |
| C07 | Python linkage + shared native orthogonal branches verified | Trees M04 and heatmap M05.a/b delivered; later families M08/M09 | Stored parent/child edges project into equal summary slots or unequal cell-group centers. Complete SVG elbows, four orientations, zero heights, resize and navigation pass; recheck later families. |
| C08 | Native index slots plus label views retain repeated names; Core 1.2 axes lack arbitrary index-to-name mapping | Grouped grids, ranked plots and named PAGA connectivity strips | Shared slots and views align on zoom; named PAGA strips collect their key after the full axis. Recheck native axis name mapping before removing label views. |
| C09 | Core 1.0 band rulers failed during initial WebGL rendering; the adopted Core 1.2 capability needs a focused recheck | Optional shaded row/column guides | Keep the native center crosshair until shaded-guide behavior is verified against Core 1.2. [PR #586](https://github.com/genome-spy/genome-spy/pull/586) records the upstream fix and regression evidence. |
| C10 | Heatmap/clustermap bands and native gap navigation verified in their own viewports. | Closed for M05.f native WebGL/notebook/HTML scope | Native clipped rects use the released Core; no patched bundle or custom listeners. C12 remains independent. |
| C11 | Bundled Core 1.2 allocates one column's width to vertical multi-column legends; later columns clip. Large Scanpy scatter symbols also overflow a single column in short panels. | M07.a/b complete-chart closure, default legend fitting and M14.a guide layout | The native column-clipping regression is retained with the other [guide checks](../../tests/integrations/scanpy/browser/test_embedding_style.py), strictly xfailed on 1.2.0. [Upstream fix PR #591](https://github.com/genome-spy/genome-spy/pull/591) includes before/after video comments; it is not adopted in the bundled runtime. Recheck after adopting a released Core fix before automatic column fitting; no local bundle patch. |
| C12 | Core 1.2 SVG export bends `linkShape="line"` control points. | Upstream straight-link export; adapter trees now use verified orthogonal links. | The minimal straight-link SVG check in [browser/test_dendrogram.py](../../tests/integrations/scanpy/browser/test_dendrogram.py) still strictly xfails. No local bundle patch; recheck on a released fix. The [orthogonal renderer](#verification) passes complete-path SVG checks independently. |
| C13 | A viewport containing only zero-height merges gives a degenerate `[0, 0]` height domain, centering zero in the track. | Native fitting of tied subtrees within larger trees | Minimal native regression in [browser/test_dendrogram.py](../../tests/integrations/scanpy/browser/test_dendrogram.py) strictly xfails on Core 1.2.0. Whole zero-height trees retain their previous nonzero range. Recheck a released native solution; no custom browser logic or patched bundle. |
| C14 | Native equilateral triangles differ from Scanpy's equal-width/height triangles; uniform sizing cannot match both dimensions. | Triangular markers in M07.d | The native SVG/WebGL investigation found mismatched bounds in all four orientations, with/without strokes. Its experimental probes were retired; unsupported triangles remain explicitly rejected. Recheck a released matching shape or native aspect control, including guides and outlines, before enabling support; no custom geometry. |
| C15 | Scanpy 1.11.5's disconnected single_component=True call subsets colors but retains full coordinates and raises a shape error. | M11.c direct parent-reference gate | [Strict expected-failure check](../../tests/integrations/scanpy/test_paga.py) detects a fixed upstream entry. Intended native filtering is independently checked against explicitly subsetted public Scanpy inputs; recheck a compatible release before closing this gate. |
| C16 | Scanpy 1.11.5 paga_path return_data calls .T on an unsmoothed annotation list | Default return_data parent-reference gate; heatmap/other return_data cases verified independently | Strict expected-failure check verifies the exact exception and asserts returned values if fixed; native chart/table return contract is explicit. |
| C17 | Core 1.2 rule/link marks have one paint and no independent edge border. Audited 2026-10-25 against the installed schema/API and official [rule](https://genomespy.app/docs/grammar/mark/rule/) and [link](https://genomespy.app/docs/grammar/mark/link/) channels. Both Python mark methods reject stroke/strokeWidth. | White borders separating overlapping PAGA edges, M11.c/M14 styling | Recheck a released native outline capability with crossing, width, zoom, hover and export cases. No extra edge layers or custom geometry. PAGA charts and the expression notebook remain unchanged; notebook rerun was conditional on native support. |
| C18 | Core 1.2 WebGL retains old categorical row slots when an explicit domain changes. CPU scales and SVG update correctly, while tiles/text can leave the heatmap viewport. | EmbeddingSummary heatmap gene dropdowns; native data/mean checks alone do not verify rendered placement | [Upstream PR #595](https://github.com/genome-spy/genome-spy/pull/595) is merged after the published 1.2.0 release. Strict pixel regressions in [browser/test_linked_embeddings.py](../../tests/integrations/scanpy/browser/test_linked_embeddings.py) check changed/duplicate choices with values on/off. Adopt the released fix and require these tests to pass; no local Core patch or alternate row encoding. |

Python computation alone does not close a renderer gap. Local Core patches are
excluded. Historical violin, filled-track and tree recipes are experimental
research; only reviewed numerical ideas or evidence may be reused with provenance.

## Verification

The latest full working-tree run completed 3,773 tests: 3,757 passed and 16 existing
expected failures, with none skipped. Browser checks and optional web tests were
included. Later linked-guide edits passed eight browser checks for fixed genes
and six relevant checks for tighter heights at desktop/narrow widths, plus the
notebook check and warning-strict Sphinx build. The full suite has not been rerun
after those documentation-only edits.

Module relocation is committed as `58e0215`: 36 runtime modules were moved with
imports/source links updated, six empty initializers, unchanged public signatures,
and no compatibility shims. Thirty-nine affected syntax trees matched their
pre-move versions apart from imports. Wheel contents, lightweight installed imports,
lint and full-source mypy passed. The candidate relocation also imported every
runtime module and built five representative plot families without pending code.

Global lint and formatting pass, including the two previously unformatted
notebooks. Fresh-checkout and final CI verification are still required for the
committed release candidate.

Runtime source, test code, deliberate numeric/API fixtures and maintained user
contracts are release inputs. Screenshots, overlays, videos, chart exports,
benchmark observations and execution outputs belong outside Git. The manual
benchmark scripts were retired during test cleanup; their useful source/allocation
invariants remain in deterministic tests. Historical timing results are local
evidence, not tracked baselines or portable performance promises.

Publication cleanup removed 11 unused benchmark reports and their 12 historical
paths from the unpublished branch under the user's earlier history-cleanup
approval. Required numeric fixtures remain. The outgoing history contains no test
media; all 108 historical notebook blobs and current notebooks have no stored
outputs or widget state. Wheel and source-distribution inspections found no
generated reports, test media or build caches. No PR or push was performed at
that cleanup checkpoint.
The cleanup passed 415 targeted reference, contract, grouped-data, ranked-data,
workflow and repository-documentation checks. Scanpy compatibility verification
is recorded below.

### Scanpy version compatibility

- Scanpy 1.11.5 / Python 3.11, pinned scientific stack: 2,382 data/workflow tests
  passed, two existing expected failures.
- Scanpy 1.12.4 / Python 3.12, AnnData 0.13.4, pandas 3.1.0, NumPy 2.5.4 and
  SciPy 1.18.1: 2,379 data/workflow tests passed, five expected failures. Three
  additionally expose Scanpy's tree-layout bug across CSR, CSC and LIL storage;
  the checks verify the native error and unchanged graph before recording it.
- Current-version browser checks: 59 passed, three existing expected failures.
  They cover grid navigation/values, embedding brushes and linked summaries/tracks.
- Documentation checks: 51 passed; warning-strict Sphinx build, global lint,
  formatting, full-source typing and lock consistency passed.
- Fresh isolated wheel with Scanpy 1.12.4: lightweight imports and UMAP, swapped
  dotplot and matrixplot smoke checks passed. Wheel metadata declares the range;
  reference/docs groups, reference generators and scientific lock pins are unchanged.

The API audit distinguishes keyword-only reordering, new unsupported arguments
and deprecated forwarding wrappers from changes to data semantics. Independent
hand calculations and direct Scanpy colors verify both scaling behaviors.
Sparse tests permit either one-column storage shape while retaining the single
conversion and no-full-matrix assertions; DPT tests permit backing metadata and
X access while forbidding raw/named-layer reads. No reference fixtures were
regenerated and no local Core or Scanpy patch is used. Newer upstream packages
emit deprecation warnings; no new runtime failures were suppressed.

The user docs, guide notebooks and workflow notebooks use the PyPI install/upgrade
command with the scanpy extra. Developer reference setup stays pinned. They have no
temporary unreleased notices, and no stored execution outputs. Compatibility is
documented once as a range. The CI jobs were updated before the approved PR was
opened. Current hosted verification is tracked in the work queue above.

### Initial hosted CI corrections

The base-package jobs omit Scanpy deliberately. Highest-expression preparation
now imports Scanpy only when called, and the remaining Scanpy-only test modules
use the existing optional-dependency guard. The base-only environment passed
412 tests with 55 skips and 327 deselected checks.

All four hosted Scanpy jobs exposed the same eight platform-dependent assertions.
Scanpy and the adapter both use NumPy's default sort; equal scores/colors can
change order across processor architectures. Rank and scatter checks now compare
exact local Scanpy order while preserving the frozen labels, scores, coordinates
and layout assertions. No reference files or plotting sort behavior changed.
The five affected test modules passed all 222 checks on each Scanpy version;
repository lint, formatting and typing passed.

## Plan clearance ledger

### Release candidate handoff

The candidate includes the current main branch (`c055653`). Readability, shared
interactions, linked summaries, Scanpy compatibility and release docs are in
separate commits. `FUTURE.md` retains the missing families/options and the planned
legend-selection/rule-outline follow-ups; no full-family gate was closed merely
to prepare this release.

Clean-checkout verification covered 3,073 existing non-browser checks, two existing
expected failures and 30 codegen checks left to their dedicated CI job. One
workflow initially hit a PBMC3k download timeout; it passed after populating the
standard Scanpy cache with the same previously downloaded file, without changing
the notebook or assertions. The new real-archive packaging regression also passed.
Forty selected browser checks, all 32 JavaScript tests, the strict docs build,
lint, formatting and typing passed. Installed-wheel checks used Scanpy 1.12.4.

The clean build exposed a source-archive leak when Hatch did not apply Git ignores
under a temporary checkout path. Explicit build exclusions now protect research,
downloads and generated docs without Git metadata. The regression rejects the
old configuration. Fresh wheel/source-archive checks verify modules, licenses,
clean notebooks and absence of those caches; the source archive is 20 MB.
Outgoing history has no generated test media/reports, and 119 historical notebook
versions contain no outputs or widget state. Evidence and the draft PR body stay
outside Git. PR #20 is now open; hosted codegen and notebook-rendering checks
passed. The remaining CI jobs and complete browser matrix remain release gates;
no merge to main or publication has occurred. The unrelated
`notebooks/select_genes.ipynb` metadata edit remains unstaged.

The active PLAN, concise STATUS, source map and detailed compatibility contract
remain maintained. Runtime/tests/notebooks and required reference fixtures remain
project assets. Generated reports and superseded run logs are not publication
inputs. Their unique observations were preserved locally before cleanup; the
repository no longer depends on those copies.

No unfinished family or capability gate is cleared by this cleanup. Retire a
working plan only after its contracts, tests, remaining work and provenance have
permanent maintained owners, following [the shared lifecycle](../README.md#plan-lifecycle).
