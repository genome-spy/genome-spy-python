# Scanpy implementation status

Updated: 2026-10-23. This is the current progress ledger; [PLAN.md](PLAN.md)
describes the work and acceptance criteria. Use the [shared lifecycle and
clearance rules](../README.md#plan-lifecycle). Dates below record observations,
not delivery promises.

The 44 unpublished Scanpy commits were cleaned of generated test media and saved
notebook execution state before publication. Code, tests and commit authors/messages
were preserved; evidence commit IDs below refer to the cleaned history. Both
workflow tests and Ruff checks pass. Local notebook edits remain unchanged.

## Current position and next work

The queue and callable inventory below own current progress. Workspace overviews
link here instead of maintaining separate counts or feature queues. Repository
instructions no longer require absent ignored planning files; retained checkpoints
below remain historical evidence, not competing lifecycle states.

This ledger describes `feature/scanpy-integration`, including explicitly marked
working-tree changes. Package version 0.7.0 identifies the adopted release base;
the Scanpy feature branch is not a claim that these previews shipped in 0.7.0.

**Available:** shared categorical/continuous 2D embeddings (UMAP, t-SNE, diffusion
maps, saved graph layouts, PCA and custom bases), cell/gene scatter plots, dotplot/matrixplot and cell heatmaps with dendrograms,
supplied numeric matrices, clustermaps, standalone dendrograms and correlation matrix development previews.
Supplied time-series heatmaps reuse the numeric matrix renderer with transposed
profiles, cropped limits, variable labels, highlights and shared grid interactions.
Supplied time-series points preserve time coordinates, subset order and the three
color modes, using shared numeric, marker, color, zoom and highlight helpers.
The explicit subplot entry reuses the same path; native composition can keep
panel colors, guides and navigation independent. Stored simulation plots reuse
these renderers with realization boundaries, one-based run labels and a local
seed-1 shuffle, without rerunning simulation.
Stored DPT group/pseudotime diagnostics compose two of those panels from metadata
alone, preserving category codes, saved order coordinates and branching boundaries.
Stored DPT expression profiles index X by saved row indices and reuse the existing
heatmap/point renderers without trajectory inference.
Stored undirected PAGA graphs now reuse Scanpy's public no-plot layout computation
and native rules, points and labels, with node/edge hover and optional x/y zoom.
Numeric annotation/gene means reuse grouped data access; solid/dashed weighted
degrees use the displayed thresholded graphs. Native color guides follow Scanpy's
automatic guide choices without creating Matplotlib figures.
Largest-component views retain original node IDs and coordinates through the
same renderer; their direct disconnected Scanpy reference is blocked by C15.
PAGA adjacency heatmaps reuse the supplied-matrix renderer with native tree-edge
points. Connectivity strips reuse the same legacy-key access with gray/black
native points, stored source/target indices and per-row draw order; neither reads
expression or computes graph analysis.
PAGA comparison composes stored embedding points and group graphs with shared
coordinate limits/navigation, group-median or saved positions and independent
color/size guides. On-data labels require explicit normal weight.
Stored ranking/score panels and ranked dotplot/matrixplot/heatmap previews now
reuse Scanpy's public result getter and the existing expression plot functions.
Stored PCA loadings and variance ratios reuse the ranking preparation and native
text panels; PCA overview composes these with the existing embedding chart.
Highest-expression QC ranks per-cell count percentages using public Scanpy normalization
and draws native boxes, whiskers and outliers without changing the input.
Stored Scrublet scores produce separate observed/simulated native density
histograms per batch, with thresholds, hover and optional score-axis zoom.
Stored embedding-density panels reuse the embedding renderer and metadata-only
access, with native gray/continuous/black point layers, hover and linked zoom.
Variable-gene QC panels read stored selection/statistics from AnnData, result
tables or legacy records, with native hover, optional per-panel zoom and one
collected bottom legend.
UMAP includes native sizing, optional hover/zoom, linked interval highlighting/count
and Python subset retrieval. Dotplot includes index-scaled slots, grouped summaries,
brackets, native size/color guides and optional summary hover. Matrixplot reuses
grouped access/means and native layout, with one-pass scaling, authoritative
`values_df`, tiles and optional summary hover. Trees reuse `sc.tl.dendrogram`
computation/results, with structural checks and shared native orthogonal links.
Heatmaps retain individual cells, shared marker/source/scaling helpers, unequal
group spans, category strips and cell hover, with a 250,000-value limit. Optional
zoom keeps their annotations aligned. All four expression grids now offer
shared optional zoom; tile families offer fitted values, and dotplot offers
hover row/column highlighting (M05.e below). Direct matrix plots reuse numeric
validation, color bounds, index slots and labels without AnnData access.
Clustermap adds individual-cell/gene clustering using public SciPy linkage or
supplied trees, ordered CSS annotation tracks and native hover, with explicit
tile and pairwise-distance limits. It shares numeric tiles and tree geometry
rather than constructing Seaborn/Matplotlib objects.
Scanpy **1.11.5** is the only accepted version;
bundled GenomeSpy Core is **1.2.0** in genome-spy-python **0.7.0**.
This is not full Scanpy plotting compatibility.

Implementation is in
[`src/genome_spy/integrations/scanpy/`](../../src/genome_spy/integrations/scanpy/).
Use `import genome_spy.integrations.scanpy as gsc`. This is the sole integration
namespace; there is no parallel compatibility package. General library imports
remain independent of the optional scientific stack.

Workflow notebooks are split into [UMAP](notebooks/scanpy_umap.ipynb) and
[expression plots](notebooks/scanpy_expression.ipynb). Both run independently.
UMAP keeps basic plotting, linked selection and customization together. Dotplot,
matrixplot and heatmap share the expression workflow’s data/marker setup; the
supplied matrix displays the same stored group correlations.

The current canonical workflows contain twenty-three UMAP/embedding/scatter/PCA/density
code cells and forty-two expression/ranked/QC/profile/simulation/DPT/PAGA/builder code cells. Public availability does not mean
all slice gates or full-family compatibility are closed.

### Current work queue

**Next independent builder: M13.b MatrixPlot**, reusing the existing matrixplot
summaries, ordering and native tile renderer. The [M13.a DotPlot builder preview](#m13a-native-dotplot-builder)
is verified within its documented scope. Square-background dot styling remains
a separate M13 increment; StackedViolin follows M08/C01. Coordinate shared
plan/export/notebook edits with the other chat before starting another slice.
The [PAGA path heatmap](#m11d-paga-path-heatmaps)
preview is implemented; native data/chart/workflow/interaction/resource checks
are verified, with C16 retaining the broken upstream default return_data gate.
Native Greys is an explicitly accepted fidelity limit. The next independent
M11.d item is the connected-line capability audit under C04. The
[comparison corrections](#comparison-palette-and-composition-corrections) are
verified and closed; their parent restrictions remain explicit below.

The [adjacency heatmap](#m11d-paga-adjacency-heatmaps) and
[stripplot](#m11d-paga-adjacency-strips) previews are delivered within their declared
bounds. PAGA path heatmap work follows their retained evidence and the corrected
comparison preview; C16 and broader path options keep full M11.d open.
Broader adjacency storage/styling/export coverage retains M14 owners.
The
[undirected group-graph preview](#m11c-stored-undirected-paga-graphs) is closed within its declared bounds;
its acceptance evidence and deliberate limits are recorded below. The
[numeric/gene/degree color increment](#paga-numeric-gene-and-degree-colors) reuses
shared grouped access and color bounds. The [component increment](#paga-single-component-filtering)
is implemented with semantic, subsetted-reference, chart, interaction, workflow
and resource checks verified; C15 blocks its direct parent reference.
Mixtures/pies, directed transitions,
multi-color panels and file/export behavior
remain M11.c. The path heatmap and broader path options keep M11.d open.
Plotting must not recompute DPT/PAGA analysis.
The [DPT expression preview](#m11b-stored-dpt-expression-profiles) is closed for
resident dense X with shared heatmap/point rendering, native interactions,
workflow and resource verification.
The [group/pseudotime increment](#m11b-stored-dpt-groups-and-pseudotime) is implemented
with semantic, component-chart, interaction, workflow and resource checks verified.
Its direct parent-entry comparison remains blocked by Scanpy 1.11.5 indexing a
pandas Series as a NumPy array; carry that gate forward independently.
The [simulation preview](#m11a-stored-simulation-plots), supplied heatmap/point
previews and native subplot preview are closed within their declared bounds.
The DPT/PAGA parent-reference gates and broader PAGA options keep M11 open. C04
does not block native straight undirected rule segments; connected-path audits
remain plot-specific; M08/M09 filled plots still require C01.

Remaining marker details are deferred to M14's compatibility backlog by user
priority. They must not precede new plot families. The
[triangular-marker audit](#m07d-triangular-marker-audit) remains retained evidence,
with C14 recording its geometry difference; no further marker audit is queued.
Existing marker support and explicit unsupported-case errors are unchanged.
Other embedding options retain M07.d/M14 owners; C11 still owns default
categorical-guide fitting.

M14.b.1, M14.b.2 and M14.b.3 are closed for native WebGL/notebook/HTML layout.
Heatmap and dotplot default to four-pixel group gaps; heatmap's `group_gap` also
accepts zero for contiguous tiles or a custom width. Matrixplot, generic matrix,
correlation and clustermap tiles remain contiguous. All these grids now use
native surround tracks; see the [numeric-layout completion](#m14b3-matrix-and-correlation-native-tracks).
All tree families now share [native orthogonal links](#shared-native-orthogonal-dendrograms),
with complete SVG paths verified. C12's separately reproduced straight-link export
bug remains upstream; the adapter no longer uses that shape for trees.
Attached trees now also use [viewport height fitting](#shared-viewport-height-fitting).
C13 retains the zero-only visible-subtree edge case; ordinary fitting and reset
are verified separately from the earlier orthogonal-mark increment.

M07.d's [native colorbar placement increment](#m07d-native-colorbar-placement) is
closed in `730f9ce` for the four sides and None across shared embedding entry points.
Scatter's distinct signature stays unchanged. Default categorical-guide fitting
is separately blocked by C11; keep its upstream reproducer and recheck it on a
released Core fix.

The M06/M07 resource gates now have fresh seven-workload evidence below. This
does not close M07.a/b's newly observed categorical-guide rendering gap.

Core 1.2.0, its generated composition APIs and the published heatmap example are
now adopted; see the [upgrade record](#core-12-runtime-adoption). M14.b.1/b.2 are
closed for their native layout scope. M14.b.3 now shares
those track helpers across clustermap, generic matrix and correlation; the tree-cut
gap trial was withdrawn after visual review. Orthogonal trees pass their SVG fidelity gate;
C12 remains a separate upstream straight-link issue.

| Slice | Lifecycle state | Commit/evidence | Remaining work before Verified/Closed |
| --- | --- | --- | --- |
| M06.a–d stored ranking | Closed (bounded preview) | `2800f23`, `f043299`; [resource closure and reuse assessment](#m06m07-resource-verification) | Broader parameter/storage/typography/export limits remain M14; ranked distributions/tracks remain M08/M09 and builders remain M13. |
| M07.a shared embeddings | Implemented; resource gate verified | `39b4d7d`; [fresh eight-panel workload](#m06m07-resource-verification) | C11 blocks reliable default multi-column categorical-guide fitting. Existing parameter/storage limits retain M07.d/M14 owners; resource verification alone does not close the preview. |
| M07.b scatter | Implemented; resource gate verified | `0fdcc02`; [cell and gene workloads](#m06m07-resource-verification) | Large default category symbols can overflow short panels; C11 blocks the multi-column correction. Keep this complete-chart gate open independently of passed resource checks. |
| M07.c loadings increment | Closed (bounded preview) | [Contract, tests and resource evidence](#m07c-stored-pca-loadings) | Broader storage/typography/export remain M14. Variance and overview are separate increments; this does not close M07. |
| M07.c variance increment | Closed (bounded preview) | [Contract, tests and resources](#m07c-stored-pca-variance-ratios) | Broader storage/typography/export remain M14; this does not close the overview or M07. |
| M07.c overview increment | Closed (bounded preview) | [Contract, tests and resource evidence](#m07c-pca-overview) | Parent storage, typography and export limits remain M14; broader embedding options remain M07.d and C11 retains their categorical-guide gate. |
| M07.d point outlines increment | Closed (bounded increment) | [Contract, semantic/chart/workflow and resource checks](#m07d-embedding-point-outlines) | Broader markers, label outlines, normalization and C11 guide fitting remain M07.d/M14. |
| M07.d callable bounds increment | Closed (bounded increment) | [Shared resolver, upstream comparisons, workflow and resource checks](#m07d-callable-color-bounds) | Center support is delivered below; normalization objects remain outside the native boundary. |
| M07.d centered colors increment | Closed (bounded increment) | [Native domain, upstream paint/guide comparisons, workflow and resources](#m07d-centered-embedding-colors) | Other family options retain M07.d/M14 owners; scatter keeps its distinct signature. |
| M07.d stored neighbor edges increment | Closed (bounded increment) | [Storage, native lookups, fidelity/workflow and resource checks](#m07d-stored-neighbor-graph-edges) | Other component pairs, self-loops and per-edge/numeric colors remain M07.d/M14; arrows remain separate. |
| M07.d square marker increment | Closed (bounded increment) | [Native shape, geometry, guides, workflow and resource checks](#m07d-square-markers) | Other markers remain M07.d; categorical guide fitting stays C11. |
| M07.d diamond marker increment | Closed (bounded increment) | [Shared marker widths, legend parity, workflow and resource checks](#m07d-diamond-markers) | Thin diamonds and other marker geometry remain M07.d; C11 still owns full categorical-guide fitting. |
| M07.d triangular marker audit | Closed (audit); support Blocked | [Native paths, paint and rejection checks](#m07d-triangular-marker-audit) | C14: native equilateral triangles cannot reproduce Scanpy's equal-width/height triangles through uniform sizing. |
| M10.c Scrublet score distributions | Closed (stored-score linear/log preview) | [Contract, workflow and verification](#m10c-scrublet-score-distributions) | Broader axis modes and unused batch categories remain M14. |
| M12.a embedding density | Closed (stored-density native preview) | [Shared embedding path, contract and verification](#m12a-stored-embedding-density) | Broader groups/missing densities and unsorted mixed color ranges remain M14; large JSON export costs are measured below. |
| M11.a supplied heatmap | Closed (resident-profile preview) | [Shared matrix renderer, chart/workflow and resource evidence](#m11a-supplied-time-series-heatmaps) | Simulation is delivered below; broader storage/export/layout M14 and larger transport M05.d. |
| M11.a supplied points | Closed (resident-profile preview) | [Shared helpers, pinned semantics, native chart/workflow and resources](#m11a-supplied-time-series-points) | Simulation is delivered below; broader storage/markers/layout remain M14. |
| M11.a simulation entry | Closed (stored dense-profile preview) | [Shared renderers, upstream semantics, chart/workflow and resources](#m11a-stored-simulation-plots) | Parent storage/markers/layout remain M14; DPT/PAGA keep M11 open. |
| M11.a subplot entry | Closed (native panel preview) | [Explicit signature, shared renderer, independent composition and resource evidence](#m11a-native-time-series-subplots) | Simulation is delivered below; broader storage/markers/layout remain M14. |
| M11.b group/pseudotime entry | Implemented; component/chart/workflow/resource checks verified | `733b04e`, filtered-view fix `5219e3a`; [stored metadata, shared panels and verification](#m11b-stored-dpt-groups-and-pseudotime) | Direct parent-entry comparison blocked by the pinned Scanpy/pandas indexing error; expression entry is independently verified below. |
| M11.b expression entry | Closed (resident dense-X heatmap/point preview) | [Direct public reference, shared renderers, workflow and resources](#m11b-stored-dpt-expression-profiles) | Parent storage/style/export limits remain M14; group-reference gate and PAGA keep M11 open. |
| M11.c undirected graph entry | Closed (bounded group/CSS-color preview) | [Public layout reuse and native charts](#m11c-stored-undirected-paga-graphs); [sparse graph fixes](#paga-sparse-graph-corrections) | Full M11.c stays open for broader node-color modes, direct component reference, directed edges and file/export behavior. |
| M11.c numeric node colors | Closed (numeric annotations, genes and weighted degrees) | [Shared computation and native color guides](#paga-numeric-gene-and-degree-colors) | Other categorical mixtures/pies, direct numeric vectors, CSS-name collisions and broader M11.c remain open. |
| M11.c largest-component views | Implemented; semantic/subsetted-reference/chart/workflow/interaction/resource checks verified | [Shared filtering and retained evidence](#paga-single-component-filtering) | C15 blocks direct disconnected parent-call comparison in Scanpy 1.11.5; keep this gate open. |
| M11.d adjacency heatmaps | Closed (bounded legacy-key heatmap preview) | [Shared matrix renderer and direct references](#m11d-paga-adjacency-heatmaps) | Stripplot increment delivered below; shared font/tick/layout/storage differences remain M14. Full M11.d stays open. |
| M11.d adjacency strips | Closed (bounded legacy-key stripplot preview) | [Shared data/native points and direct references](#m11d-paga-adjacency-strips) | Broader storage/styling/export limits remain M14; full M11.d stays open. |
| M11.d path heatmap | Implemented; native checks verified, C16 parent gate blocked | [Preparation/native chart and verification](#m11d-paga-path-heatmaps) | Connected-line mode retains C04; categorical/multiple annotations and singular shapes retain M14. |
| M11.d comparison panels | Closed (corrected bounded preview) | [Palette, native coordinates and independent composition](#comparison-palette-and-composition-corrections) | Regular-label/parent restrictions remain M11/M14; paga_path heatmap is in progress separately. |
| M10.a highest-expression summaries | Closed (count-percentage preview) | [Contract and evidence](#m10a-highest-expression-summaries) | Broader Seaborn styling, ambiguous labels and backed/lazy counts remain M14. |
| M10.b variable-gene diagnostics | Closed (stored-statistic preview) | [Data, chart, interaction, notebook and resource checks](#m10b-variable-gene-diagnostics) | Remaining input/typography/export limits stay M14; marker details are deferred. M10.a and M10.c are delivered separately. |
| M07.d colorbar placement increment | Closed (bounded increment) | `730f9ce`; [contract, browser/workflow checks and resource reuse](#m07d-native-colorbar-placement) | Four sides/None supported; remaining embedding options stay M07.d/M14 and categorical default fitting stays C11. |
| M05.d larger/chunked tile transport | Planned | Existing tile budget and [heatmap resource envelope](#m05ab-cell-heatmap-preview) | Design/test chunked access and 100k × 50 behavior. This does not own missing resource verification of M06/M07 previews. |
| M14.b.1 heatmap side tracks/gaps | Closed (native heatmap migration) | [Delivery and validation](#m14b1-native-heatmap-tracks-and-gaps) | Wider transport, storage and option closure remain M05.d/M14; other grid families retain their own migration slices. |
| M14.b.2 grouped summary layout | Closed (native layout) | [Layout delivery](#m14b2-native-grouped-layout) and [orthogonal tree verification](#shared-native-orthogonal-dendrograms) | Broader family options remain in their existing slices. |
| M14.b.3 numeric/clustered layout | Closed (native layout) | [Clustermap delivery](#m14b3-clustermap-native-tracks), [numeric tracks](#m14b3-matrix-and-correlation-native-tracks) and [shared trees](#shared-native-orthogonal-dendrograms) | Broader parameters/transport remain M05.d/M14; zero-only viewport fitting remains C13. |
| M05.f category-strip hover | Closed (native WebGL/notebook/HTML track scope) | C10; [heatmap](#m14b1-native-heatmap-tracks-and-gaps) and [clustermap evidence](#m14b3-clustermap-native-tracks) | No remaining work within this track-hover scope. |
| M14.b shared tree rendering | Closed (native orthogonal links) | [Contract, chart/workflow and resource evidence](#shared-native-orthogonal-dendrograms) | C12's straight-link SVG bug remains upstream; adapter trees use the verified orthogonal shape. |
| M14.b viewport tree-height fitting | Implemented; positive-height fitting verified | [Shared scale definition and checks](#shared-viewport-height-fitting) | C13 blocks zero-only visible subtrees within larger trees; whole zero-height trees retain their stable range. |

M07.d/M14 retain the explicitly unsupported options; dotplot brushing remains
deferred pending review. **Clearance: retain; no working document is eligible for removal.**
Delivery records below describe evidence at each implementation checkpoint;
their test counts, notebook sizes and resource observations are not current totals.

## Milestones

States apply to the stated scope; a closed preview is not a closed full family.
The completed structural update is M00.c/d, not a new plotting milestone.

| Milestone | State | Delivered evidence or remaining work |
| --- | --- | --- |
| M00 foundation/layout/lifecycle | Closed (foundation scope) | Signature/version fixtures, sole integration namespace, source/test/workflow layout, full inventory and shared lifecycle exist. Initial relocation is `d148721`; current verification below. |
| M01 UMAP/linked preview | Closed (preview only) | Runtime modules, dedicated PBMC UMAP notebook, semantic/reference/browser tests and resource baseline listed below. Parameter debt remains explicitly assigned to M07/M14. |
| M02 grouped access/dotplot | Closed (plain-chart preview with hover) | Shared access/statistics, public dotplot, index slots, native dots/labels/brackets/guides, summary hover, 11 complete frozen chart cases, real PBMC workflow and sparse/browser resource check. See retained evidence and explicit limits below; trees/builders/selections are not closed. |
| M03 matrixplot | Closed (plain-chart preview with hover) | Shared grouped means/access/layout, one-pass scaling, authoritative values_df, native index tiles/edges, 13 frozen chart cases, packaged-PBMC workflow and sparse/browser resource observation. Trees, builders and broader normalization remain open. |
| M04 trees/correlation | Closed (standalone/correlation and dot/matrix attachment preview) | Public Scanpy computation, stored-result validation, shared native orthogonal links, leaf/marker permutations, registered charts, resize/hover checks and resource observation below. Later-family attachments remain assigned. |
| M05 heatmap/matrix/clustermap | In progress; bounded previews verified | Native heatmap/clustermap track migration and M05.f are closed for WebGL/notebook/HTML. M05.d and broader kwargs/delivery remain open. |
| M06 ranking/ranked summaries | Closed (bounded preview) | M06.a–d have semantic/chart/workflow/interaction and resource evidence. Broader compatibility remains M14; native builders remain M13 and ranked distributions/tracks remain M08/M09. |
| M07 embeddings/scatter/PCA | In progress | M07.a/b resource gates pass; categorical-guide rendering remains open under C11. M07.c loadings/variance/overview and M07.d colorbar placement are Closed for their stated scope; other options remain open. |
| M08 violin/stacked/ranked | Planned; filled rendering blocked | Data/density work can proceed; full native filled geometry needs a released capability (C01). |
| M09 tracks/ranked tracks | Planned; filled rendering blocked | Profile preparation can proceed; native filled geometry needs C01. |
| M10 QC diagnostics | In progress | M10.a/b/c bounded previews are verified; broader scale/option compatibility remains M14. This does not close the full family. |
| M11 trajectories/graphs/series | In progress; supplied-series/simulation, DPT-expression and both adjacency previews closed; PAGA/compare available and path heatmap implemented | DPT/PAGA direct-reference gates, comparison corrections and broader PAGA options/entries remain open. Native rules handle straight undirected edges; C04 is limited to unverified connected paths. |
| M12 density/spatial | In progress; density preview closed, full spatial blocked | Stored-density preview evidence is retained under M12.a; broader parameters remain M14 and image-backed spatial requires C02. |
| M13 builders | In progress; DotPlot preview closed | DotPlot constructor and documented chains share the functional path, with upstream/native/workflow/resource checks. MatrixPlot/StackedViolin and remaining DotPlot style forms stay open; method coverage is recorded separately. |
| M14 compatibility/docs/release | In progress; Core 1.2 adopted | M14.b.1/b.2 native layout and shared orthogonal trees are closed; M14.b.3 native tracks are closed for all three numeric/clustered families. Parameter/capability closure, workflow publication and full API evidence remain open. |

## M05.e shared grid interactions

Visual default update (2026-10-21): dotplots retain a black 1.5-point frame on
their matrix viewport through native view properties; side tracks stay unframed.
Ranked dotplots inherit the shared renderer. Heatmaps, matrices, correlation
grids and their ranked variants omit the outer frame. The shared grouped renderer
has no frame-width option; native view configuration controls framing. Dot and
tile-edge settings remain
unchanged. **337 targeted Python checks** and **63 complete-chart/gap-navigation
browser checks** pass, along with formatting, lint and mypy. The live expression
notebook completed 13 code cells and 11 widgets without errors. Data preparation
and transport are unchanged; existing resource evidence still applies. The full
repository suite and docs build were not rerun. No plan is eligible for clearance.

Dotplot-frame follow-up: **155 dotplot/matrixplot/ranked Python checks** and
**six grouped browser layout checks** pass. The frame is a native property of
the dotplot center, so the existing shared layout and side tracks are unchanged.
The expression notebook reran successfully; its saved outputs remain local.
The centered-color follow-up is recorded below; the current queue owns next work.

Verified (interaction preview): [_grid_interactions.py](../../src/genome_spy/integrations/scanpy/_grid_interactions.py)
shares live index positions, annotation visibility, fitted value text/native
palette contrast. Dotplot uses a native two-axis crosshair ruler. Existing grouped
labels/brackets
and tree rendering serve all applicable families. Dotplot gains `zoom` and
`highlight`; matrixplot/matrix/clustermap gain `zoom` and `show_values`; heatmap gains
`show_values` and uses the shared navigation. All new options default False.
`zoom=True` now uses y-only wheel zoom and drag panning; `zoom="xy"` enables
both axes. This keeps gene columns fixed while exploring long expression grids.

The [expression notebook](notebooks/scanpy_expression.ipynb) enables the new
options on the packaged PBMC data. Text displays plotted/scaled values to two
decimals, preserves native tooltips and omits missing cells. Highlighting retains
duplicate gene slots, tracks gaps between dots and clears on leaving the plot.
Dot sizes and guides remain
fixed under navigation. There is one serialized measurement table per chart;
no extra Scanpy analysis or data extraction is introduced.

Core 1.0.0 has no color-contrast expression helper. The shared text layer samples
its native palette in 256 bins in browser parameters, including clamp bounds and
opacity over white. No Core bundle is patched.

Evidence: [shared behavior tests](../../tests/integrations/scanpy/test_grid_interactions.py),
[observed browser tests](../../tests/integrations/scanpy/browser/test_grid_interactions.py),
[public getter reuse checks](../../tests/integrations/scanpy/test_upstream_reuse.py) and
[workflow execution](../../tests/integrations/scanpy/test_notebooks.py). The initial
shared-interaction implementation (`69908bf`) passed all **476 Python integration checks**, **18 new interaction browser checks** and **70 existing
affected-family browser checks**. The final focused rerun passed 31 checks.
Ruff formatting/lint and mypy pass. The expression notebook completed all five
code cells in its existing Jupyter session; the kernel is idle. All four PBMC
charts also render independently in the released native renderer.

New browser evidence covers dense overview/zoomed values and tooltip access,
clamped native palettes and opacity, normal/swapped summary tree alignment while
zooming/panning, repeated-slot highlighting/clearing, hover disabled, fixed dot
and guide footprints, and standalone HTML. Initial registered SVG positions,
sizes and paints agree with navigation disabled. Raster differences are limited
to native antialiased mark edges; the existing frozen-reference overlays remain
covered. Generated screenshots stay under temporary/ignored directories.

Earlier x/y resource observation (before `zoom=True` became y-only): a resident float64 100 × 500 matrix, seed 17, uniform
values in [-1, 1], `zoom=True, show_values=True`, 600 × 450 logical pixels. With
allocation tracing, preparation took 3.38 s and serialization 3.91 s; peak tracked
Python allocation was 38.8 MiB. Compact JSON was 3.77 MB with exactly one dataset
and 50,000 measurement records. Chromium 156.0.8078.4 rendered in 4.11 s, reported
110.6 MiB JS heap, and observed zoom dispatch/domain change took 400 ms. Paused
hover took 103 ms and succeeded. Other tests were running concurrently; these
are local observations, not portable performance limits.

Y-only navigation follow-up (October 19): all **293 targeted Python checks** and
**42 browser checks** pass, with Ruff formatting/lint and mypy clean. The new
observed tests confirm that `zoom=True` keeps x fixed during wheel zoom and drag
panning for all four grid families, including fitted heatmap values. The existing
two-axis annotation/hover tests now request `zoom="xy"` explicitly. The expression
notebook was rerun successfully in its existing session: five completed cells,
one idle kernel. The full integration suite and resource benchmark were not
repeated for this direction-only follow-up.

The full unrelated repository suites and documentation build were not rerun.
Existing fixed-chart previews and M05.d transport limits remain applicable.
No plan becomes eligible for clearance from this additional interaction slice.

Native ruler follow-up (October 19): dotplot `highlight=True` now adds one
`gs.ruler` parameter with `encodings=["x", "y"]` and `display="center"`.
The old hover selection, two background layers and their slot tables/filter
helper are removed. The crosshair snaps to row/column centers, including gaps,
without changing plotted values, tooltips, dot footprints or guides. Browser
checks cover both orientations, repeated labels, zoomed positions, clearing,
initial appearance and standalone HTML. All **89 focused Python/workflow checks**
and **23 grid browser checks** pass, with Ruff formatting/lint and mypy clean.
The expression notebook was reloaded
and all five code cells rerun in Jupyter; all four charts rendered successfully.
Local matrix zoom experiments were preserved, with the tracked workflow's zoom
settings validated separately. Band shading remains limited by C09 below;
no Core patch is used. No plan is eligible for clearance.

## Core 1.2 runtime adoption

Merge `898ea65` brings the Core 1.2.0 runtime, schema, generated APIs and gallery
updates into this branch without rebasing its Scanpy commits. At that checkpoint,
Scanpy implementations and prepared reference fixtures were unchanged. Native
surround/facet authoring became available; migrating Scanpy layouts remained
separate M14.b work rather than part of the runtime upgrade.

The tooltip regression check now trims presentation whitespace added by the
released tooltip markup while continuing to require the exact category value.
Verification on Core 1.2: **898 Python integration checks**, **393 core package
checks** (excluding docs/codegen), **219 integration browser checks**, and
**32 JavaScript checks** pass. Ruff formatting/lint and mypy pass. The browser
run includes complete registered charts, hover, navigation, selections, resizing,
SVG/raster exports and offline delivery across the existing plot families.
At runtime adoption, resource and parameter-closure gates remained open.
The later resource verification below closes gate 4; parameter and rendering
limits retain their explicit owners.

Layout planning refresh (October 20): inspected the released typed API and the
checked-in clustered-heatmap, PBMC cell-heatmap and marker-matrix surround
examples against the current integration chart helpers. Three clustered-example
structure/expression checks and the callable-inventory check pass; Ruff is clean.
The plan now requires native group gaps and removes stale release/hover blockers.
This is planning evidence, not verification of migrated charts; runtime code and
local notebooks are unchanged.

## M14.b.1 native heatmap tracks and gaps

Closed for the heatmap migration in `4422f8a`. The [chart](../../src/genome_spy/integrations/scanpy/_heatmap_chart.py)
uses `gs.surround`: tiles/fitted values own the center, while bands, labels,
brackets and tree branches have their own clipped side views. Shared authoritative
index scales own the final domains, navigation and gaps. Cell-group cuts use final
exclusive stops; partitioned marker blocks also define feature gaps. Core's
default six-CSS-pixel gaps stayed fixed under zoom and DPR changes at this
checkpoint; M14.b.2 below reduces them to four pixels. Arbitrary
brackets and a single group do not invent gaps or dummy measurements.

Existing grouped labels/brackets, branch records and fitted values are reused.
Native link marks place point endpoints correctly across gaps. The tree uses
the existing distance-domain headroom to keep its root stroke inside its viewport.
Stored linkage, merge heights, cell/marker ordering and scientific preparation
remain unchanged. The only preparation correction is the group-center slot:
`(start + stop - 1) / 2`, replacing the old half-row label/leaf offset. The old
heatmap overlay, white boundary rules and unused overlay leaf-position option
are removed; other families keep their existing paths until their own migration.

Evidence:

- **942 Python integration checks** passed, excluding browser and notebook files.
  A later four-case marker-span rerun also verifies JSON serialization of NumPy
  integer boundaries. Sparse/source/cache/identity/scaling checks remain independent
  of rendering; no extra analysis or AnnData reads are introduced by tracks.
- **54 affected browser checks** passed across heatmap and shared interactions.
  Sixteen frozen complete Scanpy references still supply values, colors, labels
  and branch heights. Registration inserts only the intentional native gaps and
  accounts for track placement/root headroom; paint tolerance remains 12/255 RGB.
  Measured gaps, band/tile/label/tree alignment, connected branches, enabled and
  disabled hover, empty-gap picking, y-only/xy navigation, resize, dense fitted
  values and offline HTML pass. Native track tests cover both orientations at
  DPR 1 and 1.5 and wait for live scale transitions before probing narrow gaps.
- The [canonical expression workflow test](../../tests/integrations/scanpy/test_notebooks.py)
  passes. The expression notebook was also restarted and run in live Jupyter:
  **13 completed code cells, 11 widget charts, no errors, idle kernel**. Ranked
  heatmaps inherit the parent migration. Local sizing/zoom edits remain local;
  the tracked notebook contains source only, without outputs or widget state.
- The [maintained resource observation](../../tests/integrations/scanpy/fixtures/heatmap-surround-performance.json)
  repeats the ranked 5,000-cell × 50-marker workload over 20,000 sparse genes,
  with 50 expression groups. Only 5,000 × 50 values densify. Peak tracked Python
  allocation is 108.85 MiB; compact JSON is 25.109 MiB, **0.46%** above the prior
  workload, including the small per-cell band table. Preparation is 3.21 s,
  validated JSON 4.06 s, browser render/dispatch 16.60 s, hover 107 ms after the
  pointer pause, wheel response 1.27 s and live JS heap 27.35 MiB. These are fresh
  sequential local observations, not portable limits or an Arrow-widget benchmark.

Ruff formatting/lint and mypy pass. The unrelated full repository/JavaScript
suites and documentation build were not rerun. The 250,000-value budget remains;
larger/chunked transport stays M05.d, parameter/storage/export closure stays M14,
and clustermap's track migration stays M14.b.3. Clearance: retain; no working
document becomes eligible for removal from this increment.

### Optional heatmap group spacing

Closed (2026-10-23). `heatmap` and `rank_genes_groups_heatmap` expose keyword-only
`group_gap=4` in CSS pixels. Zero removes the spaces; finite nonnegative widths
apply to both cell groups and partitioned marker blocks. The existing
[`index_scales`](../../src/genome_spy/integrations/scanpy/_grouped_chart.py)
helper passes the width to native scale gaps, keeping category bands, labels,
brackets and trees aligned without extra layers or data copies.

Verification: **398 targeted Python checks**, **42 heatmap browser checks**, and
the canonical expression workflow test pass, along with Ruff formatting/lint
and mypy. The tests cover unchanged values, ordering and IDs; zero and fractional
widths; ranked-wrapper reuse; early invalid-option errors; complete default
charts; and zero/default/custom spacing with hover, zoom and pan in both
orientations at DPR 1 and 1.5. Generated references remain in temporary paths.

The live notebook, full repository suite, docs build and resource benchmark were
not rerun. Existing workflow delivery and resource evidence above remain valid:
measurement tables, data access, transport and chart structure are unchanged;
only native scale gap widths vary. Other grids retain their defaults. The next
queue owns next work. Clearance: retain.

## M14.b.2 native grouped layout

Closed for native WebGL/notebook/HTML layout. Dotplot and matrixplot now use the
existing [`finish_grouped_chart`](../../src/genome_spy/integrations/scanpy/_grouped_chart.py)
to place the prepared center, labels, marker brackets and stored tree inside
`gs.surround`. The heatmap's shared label, tree and feature-partition helpers
serve both families; ranked variants inherit their parent implementation.
Shared index definitions own native four-CSS-pixel gaps, including heatmap cell
groups. Marker cuts use the final feature partition; summary rows do not invent
cluster groups. Width/height still size the center plot area.

Native rule spans end before the next gap; single-slot caps stay on their own
anchors. This also fixes interrupted brackets on adjacent one-gene heatmap
blocks. The obsolete outside bracket mode, grouped origin/step projection,
padding and tree/bracket guide offsets are removed. Numeric grids retain the
legacy helpers they still use. Native rulers belong to the center container;
collected legends belong to the surround. Means, fractions, selected records,
supplied tables, rankings, tree computations/caches and mutation rules are unchanged.

Verification at this checkpoint:

- **947 Python integration checks** pass. Tests traverse actual native tracks,
  preserve frozen Scanpy values/ordering/areas, and prove one measurement table,
  shared scales, duplicate slots and unchanged cached/public getter behavior.
- **128 affected browser checks pass**, with **one strict expected failure** for
  the minimal native C12 SVG-link reproducer. **Seven ranked expression browser
  checks** also pass. After updating temporary overlay registration for the
  intended gaps, all **24 dot/matrix reference cases** pass again. Coverage
  includes complete axes/labels/guides, native rule brackets and connected tree
  endpoints, DPR 1/1.5, four-pixel gaps before/after zoom/pan, blank-gap picking,
  hover, fitted values, fixed dot footprints, native rulers and offline HTML.
- The canonical expression workflow test passes. Live Jupyter was restarted and
  the updated packaged-PBMC notebook ran **13 code cells / 11 widgets without
  errors**, ending idle. Local notebook sizing/title/zoom edits are preserved;
  only clean canonical source is committed.
- [Four sequential resource observations](../../tests/integrations/scanpy/fixtures/grouped-surround-performance.json)
  cover 100,000 cells × 20,000 sparse genes, 40 selected markers and 50 groups:
  ordinary dot/matrix charts with trees and ranked statistic-colored charts.
  Ordinary preparation peaks at 142.7 MiB; ranked peaks remain 258.3 MiB.
  Only 100,000 × 40 expression values densify; ranked matrixplot reads 0 × 40.
  Ranked JSON shrinks **0.92% / 1.27%** from the retained M06/M07 workloads.
  Browser render/dispatch is 1.72–1.97 s, hover 88–184 ms after the pointer pause,
  ranked wheel response 239–280 ms and live JS heap 7.6–8.9 MiB. These are local
  observations, not portable limits. Heatmap transport/data cardinality and its
  existing resource envelope are reused explicitly; its new gap geometry and
  bracket rendering have fresh browser coverage.

Ruff formatting/lint and mypy pass. Full unrelated repository/JavaScript suites
and the documentation build were not rerun. C12 keeps SVG tree-link fidelity
open; no Core bundle was patched. Parameter/storage/transport limits retain
M05.d/M14 owners. M14.b.3 is ready. Clearance: retain; no plan is eligible for removal.

### Matrixplot gap correction

Matrixplot and ranked matrixplot keep their tiles contiguous across marker
blocks, as requested after the native migration. Native surround tracks, brackets,
trees, guides, fitted values and hover are retained; heatmap/dotplot gaps are
unchanged. The expression notebook and compatibility contract reflect this rule.
Verification: **146 targeted Python checks, 35 browser checks and the canonical
expression workflow** pass; Ruff formatting/lint and mypy pass. The live notebook
completed 13 code cells and 11 widgets without errors. Broader suites and the
documentation build were not rerun.
The four grouped resource workloads above already had no matrixplot marker cuts
(one ranked marker list or a plain feature list); their data/layout paths are
unchanged, so those observations are reused rather than remeasured.

The later clustermap distance-cut trial was withdrawn after visual review;
see the native-track record below. Rows and columns now stay contiguous.

## M14.b.3 clustermap native tracks

Native layout was delivered in `624e16b`: clustermap reuses the shared label,
tree, index-scale and fitted-value helpers. Trees, color tracks and labels own
surround viewports; old clustermap outside-coordinate/projection overlays are
removed. Explicit zero side-track spacing keeps tree leaves, strips and matrix
adjacent. Native titles fit their track thickness; category legends retain saved
palettes/order.

The row/column distance-cut trial was withdrawn after user review on 2026-10-21.
Its two threshold parameters, `fcluster` computation and notebook tree-cut setup
are removed. Clustermap returns to contiguous rows/columns while retaining the
native layout, hover, zoom and values. Matrixplot remains contiguous too;
heatmap cell-group gaps and dotplot marker gaps are unchanged. The original
cut-specific test counts and resource observation in `624e16b` describe that
withdrawn configuration, not the current plot.

Current verification: **76 targeted Python checks**, **14 complete-chart/browser
checks**, and the canonical expression workflow pass. The live notebook completed
13 code cells and 11 widgets without errors. Ruff formatting/lint and mypy pass.
These checks retain frozen values/order, native tracks, palettes/legends, hover,
resize, y-only/xy navigation, fitted values and offline HTML. The broader shared
renderer suite is unchanged from `624e16b`; the full repository suite and docs
build were not rerun.

A fresh isolated `benchmark_clustermap` run uses 700 packaged PBMC cells × 40 genes,
xy zoom and fitted values, with no tree cuts. Linkage and chart preparation take
0.925 s; validated JSON serialization takes 3.760 s with tracemalloc active.
Peak traced Python allocations are 54.7 MiB; JSON is 4.34 MiB. First paint including
dispatch is 4.423 s; hover including pointer pause/probes is 0.979 s; observed JS
heap is 35.6 MiB. Source construction is excluded. The 2026-10-21 environment is
macOS 26.6.2 arm64, Python 3.11.15, Scanpy 1.11.5, AnnData 0.12.19, NumPy 2.4.6,
pandas 2.3.3, SciPy 1.17.1, Chromium 156.0.8078.4 at 1800 × 1400 / DPR 1.
These are observations, not CI limits; raw measurements and generated media stay
local. Generic matrix/correlation were still pending at this checkpoint; the
[completion record](#m14b3-matrix-and-correlation-native-tracks) covers their migration. No plan is eligible for clearance.

The shared renderer has since adopted native orthogonal links; see the following
delivery record. The layout/resource measurements above describe the preceding
contiguous clustermap checkpoint.

## M14.b.3 matrix and correlation native tracks

Implemented in `c2b5b79`; retained checks cover [matrix data/API](../../tests/integrations/scanpy/test_matrix.py),
[matrix charts/navigation](../../tests/integrations/scanpy/browser/test_matrix.py)
and [correlation/tree charts](../../tests/integrations/scanpy/browser/test_dendrogram.py).

Closed for native WebGL/notebook/HTML layout. Generic `matrix` reuses shared
slot labels in left/bottom side views, with native titles outside those tracks;
unsupplied numeric ticks remain native axes. `correlation_matrix` reuses the same
labels and `tree_track` for its right/top labels and optional 180-pixel left tree.
Column labels are vertical so long names fit inside the aligned track; trees use
the shared five-percent root headroom. Its native colorbar stays with the center,
beneath the tiles. Matrix area and figsize budgets, contiguous slots, frameless
defaults, tile edges, masks, duplicate labels, color bounds, supplied order and
cached correlation/tree permutations remain unchanged. No public options or
analysis computations were added.

The last outside-viewport tree renderer and uniform slot projection/navigation
helpers were removed. All grid labels now have native viewports and shared index
scales; no fallback overlay mode remains. Data/summary/tree preparation modules
are unchanged, and side tracks contain only labels or branch endpoints.

Verification: **964 Python integration checks**, the canonical expression workflow
and **100 browser checks** pass; C12/C13 remain the two expected Core failures.
Checks include all frozen numeric-matrix and tree charts, complete registered tile
colors/axes/titles/legends/branches, native matrix hover and fitted values, y/xy
zoom and pan, label/leaf registration after resize, DPR 1/2, long correlation
labels and offline HTML. Shared heatmap/dotplot/matrixplot/clustermap navigation
and tree checks also pass. Ruff formatting/lint and mypy pass. The live packaged-PBMC
workflow completes **14 code cells / 12 widgets**, including the added stored
correlation example, without errors. Local notebook customizations remain local;
committed sources contain no outputs or widget state.

A sequential before/after local measurement uses a seed-0, float32 normal
200 × 1,000 supplied matrix with explicit numeric labels and xy zoom at
1,200 × 450 pixels. The same RNG then supplies 3,000 × 20 stored PCA coordinates
for 50 groups of 60 cells in a 3,000 × 20,000 sparse AnnData; Scanpy prepares its
group tree before timing. Correlation renders 50 × 50 cached values with numbers
at 600 × 600. Imports and source construction are excluded; tracemalloc covers
chart preparation and validated JSON. Chromium 156.0.8078.4 runs at 2,000 × 1,800,
DPR 1, on the same macOS/Python/scientific-stack versions recorded above.

| Workload | Prepare s | JSON s | Python peak MiB | JSON MiB | Paint s | JS heap MiB |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| matrix, before | 2.907 | 11.875 | 328.34 | 26.882 | 11.177 | 159.26 |
| matrix, native tracks | 0.096 | 18.005 | 328.14 | 26.856 | 13.093 | 159.26 |
| correlation, before | 0.027 | 0.948 | 4.59 | 0.369 | 1.555 | 20.69 |
| correlation, native tracks | 0.028 | 1.039 | 4.73 | 0.374 | 1.608 | 23.37 |

Observed native hover, including pointer pause/probes, is 0.675 s for the matrix
and 0.696 s for correlation. The large matrix keeps the same payload/memory
scale and prepares faster, but validated serialization remains slower (18.0 s
versus 11.9 s with tracing active). These are observations, not CI limits or a
performance improvement claim. Large-payload validation/transport remains
M05.d/M14 work. Raw measurements, media and exports stay local.

Point outlines were next at this checkpoint; their [delivery record](#m07d-embedding-point-outlines) is below. C11 categorical-guide fitting,
C13 zero-only viewport fitting, M05.d larger transport and wider family options
retain their existing owners. Unrelated full-repository tests and the docs build
were not rerun. Clearance: retain; no plan is eligible for removal.

## Shared native orthogonal dendrograms

Closed for the shared renderer increment. Every existing tree path—standalone,
dotplot, matrixplot, cell heatmap, correlation matrix and both clustermap axes—uses
one native mark helper in
[_dendrogram_chart.py](../../src/genome_spy/integrations/scanpy/_dendrogram_chart.py).
Ranked variants inherit it through their parent expression plots. There are no
public API changes, new dependencies or Core patches.

Each stored SciPy/Scanpy merge becomes two parent-to-child endpoint rows instead
of three separate segments. `linkShape="orthogonal"` and vertical/horizontal
orientation draw the elbows at the parent's stored height. Existing fractional
index offsets keep tracks aligned across native gaps and navigation. Parent
positions are mapped before drawing, preserving connected branches for unequal
heatmap group spans. Heights, leaf permutations, cached results and Python
clustering remain unchanged. Unused legacy overlay projection options were removed;
correlation's subsequent layout migration is recorded in [M14.b.3](#m14b3-matrix-and-correlation-native-tracks).

Verification: **961 Python integration checks**, **133 browser checks** and the
canonical expression workflow pass. SVG assertions inspect all three vertices
of each right-angle path, including the elbow. Registered full-chart checks cover
all four standalone orientations, normal/swapped attachments and both clustermap
trees. Other browser checks retain zero-height/tied merges, unequal cell-group
spans, native gaps, resizing, y/xy zoom, hover, fitted values and offline HTML.
The live expression notebook completed all 13 code cells and 11 widgets without
errors; only the explanatory Markdown changed. User's local plot settings remain
intact. Test media, measurements and notebook outputs stay local.

A fresh isolated `benchmark_clustermap` run covers the shared link/serialization
path with 700 packaged PBMC cells × 40 genes, 28,000 tiles and 244,650 pairwise
row distances, xy zoom and fitted values. Tree computation/chart preparation take
0.930 s; validated JSON serialization takes 4.201 s with tracemalloc active.
Peak traced Python allocations are 52.4 MiB; JSON is 4.20 MiB. First paint including
dispatch is 4.213 s; hover including pointer pause/probes is 1.009 s; observed JS
heap is 35.6 MiB. Runtime versions, allocation scope and browser dimensions match
the preceding contiguous-clustermap checkpoint. These are observations, not CI
limits or a controlled speed comparison. Numeric access, clustering, summaries
and tile transport are unchanged, so their retained resource evidence still applies.
Ruff formatting/lint and mypy pass; the full repository suite and documentation
build were not rerun.

The minimal C12 straight-link SVG reproducer still strictly xfails on Core 1.2.0.
That upstream shape defect is unchanged; the adapter no longer uses straight links
for trees. Complete orthogonal paths now pass the adapter's SVG gate. Generic
matrix/correlation native layout was still pending at this checkpoint; wider family compatibility remains open;
**clearance: retain**.

## Shared viewport height fitting

The official clustered-heatmap example uses `ViewportDomainRef(mode="contain")`
on each tree's independent height scale. The integration previously fixed this
domain to the full tree. `tree_track` now shares the native viewport reference
across dotplot, matrixplot, heatmap and both clustermap axes; ranked plots inherit
it through their parent functions. Native fitting runs after navigation pauses.
The separate `transform_dendrogram` is unnecessary here because Python already
provides the stored endpoint coordinates. No clustering or heights are recomputed.

Zero remains pinned to the matrix edge. Native symmetric padding of `1 / 22`
with that bound preserves the previous five-percent root headroom and overview
geometry. Entirely zero-height trees retain their existing nonzero domain.
Standalone trees retain their existing non-navigable layout. Correlation now uses
the shared side-tree scale through M14.b.3, without adding a navigation option.

The new browser checks reproduce the fixed-domain difference, verify the settled
height against contained stored endpoints across all four families and both
directions, and restore the full height on reset. Existing checks retain actual
wheel/pan interaction, native gaps, aligned leaves/labels, SVG paths and hover.
An independent minimal native check reproduces C13: when a viewport contains only
zero-height merges from a larger tree, Core produces `[0, 0]` and maps zero to the
middle of the track. This strict expected failure is retained without custom
browser logic or a Core patch. The fitting increment stays **Implemented** until
that edge-case gate passes on a released capability; no plan is cleared.

C13's recheck now waits independently of the broken domain value and limits
expected failures to assertion errors. All **43 dendrogram browser checks** pass,
with C12/C13 expected failures. A temporary expanded-domain control produces
strict XPASS, while an injected setup timeout fails normally. Formatting and lint
pass. This hardens the release gate; C13 and the fitting lifecycle state remain open.

Validation: **190 targeted Python checks**, **143 browser checks** and the
canonical expression workflow pass; C12 and C13 have separate strict expected
failures. The live notebook completed 13 code cells and 11 widgets without errors;
wheel zoom and settled tree fitting were observed on the packaged PBMC clustermap.
Formatting, lint and mypy pass. The full repository suite and docs build were not
rerun. Notebook outputs and generated images remain local.

The isolated 700 × 40 clustermap benchmark, with the same workload/environment as
the orthogonal-link record above, takes 0.842 s for preparation and 3.491 s for
validated JSON serialization with tracemalloc active. Peak traced allocations are
52.4 MiB; JSON is 4.20 MiB. First paint including dispatch is 3.425 s; hover including
pointer pause/probes is 1.011 s; observed JS heap is 35.6 MiB. These are local
observations, not timing limits or evidence of a controlled speed improvement.
Data extraction, clustering and tile transport are unchanged.

## M06/M07 resource verification

Seven fresh, sequential workloads on the unchanged `c659bf2` runtime close
resource gate 4 for the stated M06/M07 previews. Reproduction commands, seeds,
allocation scopes and raw measurements are retained in
[`m06-m07-performance.json`](../../tests/integrations/scanpy/fixtures/m06-m07-performance.json).
The [workspace commands](README.md#validation) run the maintained benchmarks;
no ignored research files or generated media are required.

Machine/runtime: Apple M5, 10 logical CPUs, 32 GiB RAM, macOS 26.6.2 arm64,
Python 3.11.15, Scanpy 1.11.5, AnnData 0.12.19, NumPy 2.4.6, pandas 2.3.3,
SciPy 1.17.1, Core 1.2.0 and Chromium 156.0.8078.4, DPR 1.
These are local observations with allocation tracing, not portable timing limits.

| Workload | Displayed output | JSON MiB | Browser render s | JS heap MiB after GC |
| --- | --- | --- | --- | --- |
| PCA | 20,000 cells, eight 300 × 300 panels | 15.065 | 7.799 | 85.57 |
| Cell scatter | 20,000 cells, eight 300 × 300 panels | 15.046 | 9.375 | 87.62 |
| Gene scatter | 20,000 genes, eight 300 × 300 panels | 12.566 | 9.172 | 85.57 |
| Stored gene ranks | Six 300 × 300 panels, 180 labels | 0.016 | 3.476 | 9.35 |
| Ranked dotplot, stored scores | 50 groups × 40 markers | 0.197 | 1.687 | 8.28 |
| Ranked matrixplot, stored scores | 50 groups × 40 markers | 0.144 | 1.503 | 7.68 |
| Ranked cell heatmap | 5,000 cells × 50 markers | 24.993 | 15.884 | 27.01 |

The point workloads use a 20,000 × 20,000 CSR matrix with 20 sparse samples per
cell. PCA selects PC2/PC50 from 50 resident components. Each call sends one shared
table, four unique expression colors and categorical/continuous annotations.
Guards permit only four 20,000 × 1 columns for PCA/cell scatter, or four
1 × 20,000 rows for gene scatter; the full matrix never densifies. All eight
plot bounds fit the viewport (2,800 × 1,800 for PCA; 4,000 × 1,800 for scatter).
Sixteen isolated source IDs are checked by actual hover. Median hover is
about 79 ms after the pointer pause; wheel responses are 0.25–0.78 s.
Warm plotting takes 0.046–0.062 s, Arrow preparation about 0.8 s, and validated
JSON takes 24–25 s under tracing. JSON is 12.6–15.1 MiB versus 4.3–4.4 MiB of Arrow;
browser timings measure JSON dispatch, not an Arrow widget roundtrip. Peak traced
allocations are 126–134 MiB and retained allocations, including both transports,
83–88 MiB. Larger/chunked transport remains M05.d; this does not establish
100,000-cell, eight-panel interactive performance.

M06's six-panel rank renderer reads stored 20,000-gene lists from six groups over
an unread 100,000 × 20,000 sparse source. Cold plotting setup takes 3.452 s and
validated JSON 0.928 s; traced peak/retained allocations are 76.9/76.8 MiB,
including optional plotting imports. Hover checks the correct gene on every
panel in 0.56–0.66 s including the deliberate 450 ms pointer pause. Render timing
includes the entrance animation; the probe waits for the final canvas geometry.

Ranked dot/matrix workloads use 100,000 cells, 20,000 sparse genes and complete
stored lists for 50 groups. Cold preparation is 6.3–6.5 s and traced peaks about
258 MiB. Dotplot densifies exactly 100,000 × 40 selected values; matrixplot's
authoritative score table requires only a 0 × 40 feature-validation read.
Heatmap densifies exactly 5,000 × 50 values at its existing 250,000-tile limit;
preparation is 6.262 s and peak traced allocation 108.8 MiB. Hover is
96–211 ms after the pointer pause, and y-wheel response is 0.18–1.24 s.

Reuse assessment: default expression-colored ranked wrappers still call the
same parent dotplot/matrixplot/heatmap functions after stored-marker selection.
Existing parent selected-access, means/scaling and tree resource observations
remain applicable to those unchanged paths. The new score-colored dotplot adds
the full stored-statistic table and still reads expression for fractions; the
score-colored matrixplot independently covers the metadata-only path. Both
exercise the same 2,000 native marks as the parent workloads on Core 1.2.
The fresh ranked heatmap covers the full parent tile budget. Other stored
statistics alter selected numeric values, not table cardinality or the renderer;
semantic/source tests cover all six metrics. No old parent browser number is
presented as a fresh measurement. The PCA renderer is the unchanged shared
two-coordinate pipeline used by UMAP/t-SNE/diffmap/saved graph layouts; prior
semantic, complete-chart, linked-selection and workflow evidence still applies.

M06 closes only its documented ranking/ranked-summary preview. M07.a/b resource
gates pass, but the captures expose an independent complete-chart gap: large
scatter legends overflow short panels, while native multi-column legends clip
later columns under Core 1.2 (C11). Those previews remain Implemented until that
rendering gate passes. The attempted automatic-column workaround was removed;
no runtime or bundled JavaScript changed. The strict expected-failure
[native reproducer](../../tests/integrations/scanpy/browser/test_native_legend_extent.py)
guards rechecking a released fix. Local plans remain **retain**.

Validation: all seven resource workloads, **218 targeted semantic/source checks**
and **50 ranking/embedding/scatter browser regressions** pass; C11 is one strict
expected failure. Ruff formatting/lint and mypy pass. Runtime sources did not
change, so the canonical-workflow and broader integration evidence in the Core
1.2 upgrade record remains applicable; notebook edits were not modified or run.
The unrelated full repository/integration suites and Sphinx build were not rerun.

## M05.f category-strip tooltips — layout migration

Current state: closed for native WebGL/notebook/HTML tracks after both
[M14.b.1 heatmap](#m14b1-native-heatmap-tracks-and-gaps) and
[M14.b.3 clustermap](#m14b3-clustermap-native-tracks) verification.
The later [shared renderer delivery](#shared-native-orthogonal-dendrograms) verifies
orthogonal tree SVG paths; C12's straight-link issue remains upstream.

Design correction (October 20, before migration): heatmap used negative pixel
offsets; clustermap used normalized positions below 0 or above 1. Both disabled
clipping and reserved padding to keep annotations in the same layered chart.
This was an adapter layout shortcut, not a requirement that Core permit outside hits.

The intended route remains M14.b: use the adopted container layout/schema and
published heatmap example to create separate native
track viewports with shared aligned index scales. Bands remain adjacent to the
matrix and inside their own viewports. Native layout should own registration,
spacing, clipping and guide placement; Python data/statistics/tree preparation
remain reusable. Core 1.2 now passes the legacy strip-hover checks in both heatmap
orientations and clustermap, before and after navigation. This removes the
observed picking failure while leaving the viewport-layout migration open.
Production Scanpy chart construction is unchanged by the runtime upgrade.

Retained observations from the earlier overlay implementation:

Heatmap and clustermap originally set `tooltip=None` on their annotation strips.
They now configure the existing strips with GenomeSpy's default handler and the
category field; `hover=False` disables strip and tile tooltips. Existing geometry,
labels, color scales and data stay in place. No extra marks or listeners are added.

At the Core 1.0.0 checkpoint, rendered hits outside ordinary plot bounds were
rejected, so these strip tooltips were **not yet usable**. The independent native reproduction
shows an identical rectangle working inside the plot and failing outside it with
`clip="never"`. [Core PR #587](https://github.com/genome-spy/genome-spy/pull/587)
contains the proposed picking change, regression tests and required release note. Its
description embeds an observed before/after recording; recording assets and
helpers are not committed. The fixed browser reproduction shows both tooltips.
That checkpoint did not change the integration bundle; the upgrade record above
supersedes its runtime version and hover limit.

Validation: **116 focused semantic/API checks** pass. Browser checks pass for
disabled strip hover and existing cell hover in both orientations and clustermap;
the three enabled-strip cases are precise expected timeout failures only for
Core 1.0.0. The upstream fix passes 66 interaction/facet/identity tests, build,
TypeScript, lint and Changesets checks. Python formatting/lint and mypy pass.
The unrelated full Python suite and documentation build were not rerun.

Clearance: retain. The heatmap and clustermap native track delivery records now
supersede the overlay implementation. Core 1.2 already removed the legacy picking
failure; keep the retained Core 1.0 results historical rather than treating them
as current expected failures.

## M06.a–c stored ranking preview

Implemented: `ranking`, `rank_genes_groups`, and ranked dotplot/matrixplot/heatmap.
The expression wrappers make one public `sc.get.rank_genes_groups_df` request for
the selected rank lists, preserving their order, tail selection, repeated slots,
symbols and strict fold-change filtering. They call the existing expression plot
entry points; summaries, raw/layer access, trees and interactions are shared.
No ranking or embedding analysis runs, and cached results are not modified.

Native rank panels share one text/axis renderer. `rank_genes_groups` reads only
stored names/scores; symbols honor the stored raw/var choice. `ranking` handles
supplied columns/dictionaries, dense array indices, log scores and extreme-rank
gaps. Missing/nonfinite score labels error; filtered marker lists are supported
by the expression wrappers. Native font, tick density and outer layout differ
from Matplotlib. Metric colors were subsequently added in M06.d below.

Evidence: [ranking tests](../../tests/integrations/scanpy/test_ranked.py),
[native browser checks](../../tests/integrations/scanpy/browser/test_ranked.py),
[four frozen complete-panel cases](../../tests/integrations/scanpy/fixtures/ranked.json)
and their [generator](../../tests/integrations/scanpy/generate_ranked_references.py).
Registered SVG anchors, titles, axes, hover, offline HTML and reused y navigation
are checked. Generated figures, captures and overlays remain outside Git.
At this checkpoint, the [expression workflow](notebooks/scanpy_expression.ipynb) had ten code cells
and nine charts on packaged PBMC data, including stored logreg scores and all
three ranked expression variants. Existing local plot settings are preserved.
All ten cells completed in the live Jupyter notebook. The full non-browser
integration run passed **606 checks**; after consolidating rank access into one
getter request, **156 focused API/ranking/workflow checks** passed. All **eight
ranking browser checks** and the final **47 ranking checks** pass, as do Ruff
formatting/lint and mypy. The unrelated full
repository suite and documentation build were not rerun.

A seed-17 float32 sparse 100,000-cell × 20,000-gene observation with 100,000 random
samples selected four unique genes in eight marker slots and serialized 32 summary
records (8,937 compact JSON bytes). Cold preparation took 3.748 s, first serialization
1.996 s, and peak traced Python
allocation was 89.38 MiB, including optional imports and schema validation.
Tests enforce selected-column densification and reject oversized cell heatmaps
before expression access. These are local observations, not portable limits.

Clearance: retain. M14 retains filtered score-panel and native
presentation limits. M08/M09 own ranked distributions/tracks. No plan is cleared.

## M06.d stored statistic colors

Delivered in `f043299`; resource closure is now recorded
[above](#m06m07-resource-verification):
`rank_genes_groups_dotplot` and `rank_genes_groups_matrixplot`
accept all six pinned `values_to_plot` options: scores, logfoldchanges, pvals,
pvals_adj, log10_pvals and log10_pvals_adj. The log variants use −log10(p).
The new preparation helper reuses stored-result validation, the public Scanpy
getter and existing marker-slot parsing. It passes detached tables into the
existing dotplot/matrixplot entry points; no chart, legend or interaction code
is copied. Dot fractions still use the parent expression source and denominator.
Matrix statistics bypass scaling; dot statistics follow the parent's scaling
order, including swapped axes. Default and overridden guide titles are covered.

`groups` selects marker lists; statistics cover every stored group. Explicit
markers, filtered selection, tails, repeated slots, custom keys, symbols and
compatible grouping overrides are retained. Unattached matrix rows preserve
Scanpy's alphabetic statistic-table order; dot rows use observation categories.
Stored raw/layer params do not override the parent's expression source. Plotting
never computes differential expression or changes saved results.

As in pinned Scanpy, metric colors require complete stored rankings. The packaged
PBMC logreg cache has only 100 ranks, so the expression notebook explicitly
prepares a separate complete Wilcoxon result under `rank_stats` before plotting
fold-change dots and −log10 adjusted-p-value tiles. It retains earlier examples
and has thirteen code cells and eleven charts. All thirteen cells completed in
the existing live Jupyter session; the new charts were visually checked and the
kernel is idle. Heatmaps continue to show cell
expression. Missing metrics, ambiguous labels, absent gene/group pairs and
nonfinite selected statistics error. The preview deliberately rejects Scanpy's
missing-statistic fill of 1; log p-values of zero also error without clipping.
M14 owns these explicit compatibility limits.

Evidence: [statistic semantics](../../tests/integrations/scanpy/test_ranked_statistics.py),
[shared ranking/sparse checks](../../tests/integrations/scanpy/test_ranked.py),
[complete native comparisons and interactions](../../tests/integrations/scanpy/browser/test_ranked.py),
and [workflow checks](../../tests/integrations/scanpy/test_notebooks.py).
All **209 targeted ranking/API checks**, both canonical workflows and **12 ranking
browser checks** pass, plus Ruff formatting/lint and mypy. Complete references
use shared viridis at 150 export DPI, with native palette bins and browser
rasterization accounted for; captures and registered overlays remain local.
The 100,000-cell × 20,000-gene sparse tests include both statistic-color families,
read four expression columns and send 32 summaries; the full matrix is never
densified. The earlier resource benchmark was not repeated. The unrelated full
repository suites and documentation build were not rerun.

Clearance: retain the live plan and status. The subsequent resource verification
closes this bounded preview. M13 retains builders and M14 the named compatibility
limits. No working plan is cleared.

## Review follow-up and M07.a shared 2D embeddings

Three Sol reviewers checked reuse, self-containment, readability and YAGNI. Two
found no significant structural issue. The reuse review identified two redundant
reads, fixed in `ff87075`: statistic-colored matrixplots validate feature lookup on zero
rows and read only real group annotations; one detached unfiltered ranking table
serves marker selection and color values. Strict marker thresholds do not remove
the statistic pairs needed for other groups. No cache is shared across calls.
The metadata path retains raw/layer/symbol validation, categories and duplicate
slots. Getter-count and cross-group-value regression tests cover both changes.

Delivered in `39b4d7d`: M07.a generalizes the three UMAP
modules in place to `_embedding_data.py`, `_embedding_chart.py` and
`_embedding_interactions.py`, with shared styles.
`embedding`, `tsne`, `diffmap`, `draw_graph`, `pca` and `pca_scatter` add six public
entries; the alias is the same function as pca. A small effective-signature helper
keeps Scanpy's shared defaults visible without copying every parameter list.
Wrappers select a basis, saved layout or stored PCA variance annotations; all
points, masks, colors, source access, draw order, observation IDs and native
interactions use the existing pipeline. `selection_mask(basis=...)` shares basis
resolution; its default remains UMAP. No embedding or neighbors computation runs.

Direct obsm keys precede X_ keys. Components/dimensions retain pinned semantics,
including DC1/DC2 defaults. Axes and hover share prepared labels; PCA percentages
read stored variance ratios for the displayed components. Graph layouts use an
explicit layout or saved draw_graph params. Missing/malformed coordinates or
required metadata error. Three-dimensional plots, edges/arrows and remaining
UMAP options remain M07.d/M14; PCA diagnostic plots remain M07.c.

At this checkpoint, the [UMAP notebook](notebooks/scanpy_umap.ipynb) had eleven code cells. New
PCA panels reuse packaged coordinates; a separate explicit Scanpy cell computes
t-SNE with the saved PCA representation and random_state=0. All eleven cells
completed in the existing Jupyter session and both examples were visually checked.
Old local notebook settings and outputs are preserved; committed notebooks remain
output-free. No Core patch or new runtime dependency was introduced.

Evidence: [embedding semantics/signatures](../../tests/integrations/scanpy/test_embedding.py),
[eight frozen complete cases](../../tests/integrations/scanpy/fixtures/embedding.json),
[native rendering and interactions](../../tests/integrations/scanpy/browser/test_embedding.py),
[original UMAP browser regression](../../tests/integrations/scanpy/browser/test_umap.py),
and [workflow checks](../../tests/integrations/scanpy/test_notebooks.py).
The full non-browser integration run passed **738 checks**, and **13 new embedding
plus 18 original UMAP browser checks** passed. The new tests observe labels,
registered point paint/footprints, native hover, zoom, offline HTML and brush
counts matching Python membership. Ruff formatting/lint and mypy pass.
The final reruns passed **41 embedding checks** (including malformed metadata)
and **106 ranking/matrix checks** (including the metadata-only table path). The unrelated full repository suites and docs build
were not run. Generated charts and overlays stay outside Git.

A seed-17 local observation used a float32 sparse 100,000-cell × 20,000-gene
AnnData and a resident 100,000 × 50 PCA matrix, selecting columns 2 and 50 with
observation-category colors. Only those two coordinate columns were sent in
100,000 records. Warm preparation took 0.058 s; validated default JSON serialization
took 10.237 s and produced 26,797,446 bytes, with 249.39 MiB peak traced Python
allocation. Input construction is excluded. This is a local observation, not a
capacity guarantee; large-data transport remains M05.d.

Clearance: retain. The later [resource verification](#m06m07-resource-verification)
closes resource gate 4. M07.a remains Implemented because C11 leaves a
complete-chart guide-layout gate open. Existing family/renderer limits retain
their named owners.

## M07.b scatter

Delivered in `0fdcc02`: `gsc.pl.scatter` retains pinned
Scanpy's separate signature and supports observation/gene x/y coordinates, exact X_ basis lookup,
per-axis x/y/color layers, categorical/numeric/literal colors and multiple panels.
It uses public AnnData vector access, existing embedding identity/panel fields,
color/style helpers and the same point renderer. No second scatter chart module,
full AnnData transpose, analysis, Matplotlib call or runtime dependency was added.

Distinct semantics remain explicit: raw defaults before observation layer lookup;
variable orientation drops automatic raw; scatter diffusion maps skip the first
stored column. Categorical background/group paint order, saved palettes, unused
categories, requested group order and no NA legend match the reference. Numeric
colors retain pinned scatter's ascending sort even with sort_order=False; missing
numeric colors are omitted from painting and initial coordinate limits. CSS name
and hex validation now rejects misspelled color/annotation keys before rendering.

Four keyword-only controls reuse native hover, x/y zoom, width and height. Direct
x/y plots retain numeric axes; gene tooltips identify variables. The existing
UMAP notebook adds packaged PBMC observation and variable scatter examples; all
**13 code cells** completed in the existing Jupyter session and both charts were
visually checked. Original code/settings and unrelated local notebooks are
preserved; committed notebook cells have no outputs or widget state.

Evidence: [semantic/signature/source tests](../../tests/integrations/scanpy/test_scatter.py),
[eight complete reference cases](../../tests/integrations/scanpy/fixtures/scatter.json),
[shared browser checks](../../tests/integrations/scanpy/browser/test_scatter.py),
and [workflow regression](../../tests/integrations/scanpy/test_notebooks.py).
The non-browser integration suite passed **789 checks**; the final targeted scatter
run covers **51 checks** including both sparse orientations, raw/layer caching,
views, backed metadata/early expression errors and missing-color domain limits.
**Eight scatter reference browser comparisons plus 33 interaction/embedding/UMAP
checks** passed. Comparisons register point locations, footprints and paints at
100 display / 150 export DPI; native axes, titles, legends, hover, x/y zoom and
offline HTML are checked too. Ruff formatting/lint and mypy pass.
The unrelated full repository suites and documentation build were not run.

A seed-17 local metadata scatter over sparse 100,000-cell × 20,000-gene AnnData
prepared in **0.047 s**, serialized validated JSON in **8.420 s**, and produced
**23,714,299 bytes**, with **241.85 MiB** peak traced Python allocation. Source
construction is excluded; expression was not read. This is a local observation,
not a capacity guarantee. At that checkpoint the large chart was not measured
in a browser; the later eight-panel workload closes representative browser
resource verification. M05.d covers larger/chunked tile transport.
Generated media remains outside Git.

Limits: only finite numeric coordinates, resident expression, scalar sizes and
dot/circle markers. On-data labels, manual margins, stored highlights, 3D,
outline/normalization and broader markers/storage stay M07.d/M14; unsupported
forms fail by name. For multiple categorical panels, use nested palettes: pinned
Scanpy truncates a flat CSS list after the first panel, so that form rejects.
Native guide ticks, typography and automatic panel spacing are not pixel-identical
to Matplotlib. Scatter does not yet expose linked brushing/Python membership.

Clearance: retain the live plan/status and permanent tests/reference provenance.
The later [resource verification](#m06m07-resource-verification) closes resource
gate 4; M07.b remains Implemented because C11 leaves guide fitting unresolved.
No working plan becomes eligible for removal, and full-family closure is not claimed.

### Native legend customization follow-up (2026-10-20)

Shared embedding/scatter presentation defaults now live in native chart
configuration, so `configure_legend` can change guide size and placement. A single
panel row no longer has a redundant outer row wrapper; inner rows allow native
legend collection at the chart root. Ordinary calls retain their existing guide
appearance and independent scales/guides. No plotting parameters or custom guides
were added.

The UMAP notebook's cell-scatter example collects compact native guides below
both panels. `height` remains the plot-area height, with external guides added
outside it. All thirteen notebook code cells completed in the existing Jupyter
session; the final scatter output was visually checked. Tests cover collected categorical and continuous guides below one
and two panel rows, their bounds/symbol footprints, unchanged point data/marks,
nonoverlapping colorbar labels, Scanpy's many-category column defaults and
linked-chart configuration.

Validation: **307 targeted semantic/API checks**, **46 browser checks**, and the
canonical UMAP workflow pass. Ruff formatting/lint and mypy pass. Existing
registered chart comparisons, hover, zoom, brush counts and offline delivery
remain covered. Generated evidence stays outside Git. Full unrelated suites,
documentation build and resource measurements were not repeated; M06/M07 resource
gates and plan clearance remain unchanged.

## M07.c stored PCA loadings

Closed (bounded preview): `pca_loadings` preserves pinned Scanpy's signature and
delegates preparation/rendering to the existing attribute-ranking and native
rank-label helpers. There is no PCA-specific data/chart module, new analysis,
Matplotlib call or expression access. Shared ranking layout chooses the panel
columns; the renderer reserves space for vertical names and uses rotated ASCII
dots for the omitted-rank marker missing from its font atlas. Stored scores and
the Unicode gap label remain unchanged.

Supported: one-based component strings/sequences in supplied order, repeated
components/labels, first-three default, min(30, n_vars) rank default, high/low
splits and gaps, top-only's extra label, numeric sizing, optional native hover,
and common show/save rules. Only selected finite resident NumPy loading columns
are read. Sparse expression, resident backed loadings and views are covered;
sparse/lazy loadings and invalid/missing results fail by name. Plotting never
runs PCA or repairs cached results. A single component works despite Scanpy
1.11.5's indexing error. Its full packaged PBMC loadings also contain 456 missing
rows: the notebook explicitly selects the 309 highly variable genes used in PCA.

Evidence: [semantic/source checks](../../tests/integrations/scanpy/test_pca_loadings.py),
[frozen complete charts](../../tests/integrations/scanpy/fixtures/ranked.json),
[observed chart/hover/offline checks](../../tests/integrations/scanpy/browser/test_ranked.py),
and [canonical workflow checks](../../tests/integrations/scanpy/test_notebooks.py).
The full non-browser integration run passed **838 checks**, followed by **235
focused checks** after final shared label rendering changes. All **18 ranking
browser checks** pass, including the three loadings references and packaged-name
clipping. References register score/text positions, titles, axes and plot bounds
at 100 display/150 export DPI and DPR 1.5; overlays remain temporary. Both canonical
workflows passed; all **14 UMAP notebook code cells** completed in Jupyter and the
loadings output was visually checked. Ruff formatting/lint and mypy pass.

Resource envelope observed on macOS 26.6.2 arm64, Python 3.11.15, Scanpy 1.11.5,
AnnData 0.12.19, NumPy 2.4.6, pandas 2.3.3, Core 1.0.0 and Chromium 156.0.8078.4:
seed 17, 100,000 × 20,000 CSR expression (unread), resident 20,000 × 50 float32
loadings, components `3,1,2`, n_points=30, include_lowest=True, 300 × 300 panels.
Source construction/imports were excluded. Preparation took **0.012 s**, validated
JSON serialization **0.772 s**, peak traced Python allocation **1.02 MiB**, retained
allocation **0.31 MiB**. The payload was **8,841 bytes**, three datasets and 93 labels.
Browser rendering took **2.375 s**; paused label hover succeeded in **348 ms**;
retained JS heap after collection was **6.98 MiB**. This covers this small ranked
output from a realistic gene/PC input, not larger displayed rank/panel counts or
hardware-independent performance. The benchmark does not close M06/M07.a/b gates.

Remaining limits: resident finite loadings only, inherited native font/tick/spacing
differences and inactive image saving; M14 owns these. Variance and overview remain
separate M07.c work. The inventory/export regression now guards coverage counts.
Unrelated repository suites and the documentation build were not rerun.
Clearance: retain the live PLAN/STATUS and permanent source/tests/contracts;
no working document becomes eligible for removal from this increment.

## M07.c stored PCA variance ratios

Closed (bounded preview): `pca_variance_ratio` reads
`uns["pca"]["variance_ratio"]` through the existing attribute-ranking preparation
and native text renderer. No new data/chart module, analysis or expression access
was added. The shared log operation now runs on the source dtype before converting
to plotting floats, matching Scanpy's float32 rounding as well as float64 results.

The pinned signature/defaults, PC labels, NumPy sorting/ties, natural-log score
transformation, top-only extra label and short-result rank extent are preserved.
Results are detached snapshots: no normalization, cache writes or source repair.
Missing/nonfinite/malformed vectors, invalid counts and nonpositive log inputs
error with the plotting function named. NumPy arrays and resident sequences work;
sparse/lazy vectors reject. Views and backed AnnData use resident stored results
without reading X, coordinates or loadings. Native hover, sizing and common
show/save semantics reuse the existing helpers.

Evidence: [semantic/source/precision checks](../../tests/integrations/scanpy/test_pca_variance_ratio.py),
[three complete frozen variance cases](../../tests/integrations/scanpy/fixtures/ranked.json),
[observed hover/offline checks](../../tests/integrations/scanpy/browser/test_ranked.py),
and [canonical notebook execution](../../tests/integrations/scanpy/test_notebooks.py).
All **275 focused semantic/API checks**, the canonical UMAP workflow and **24
ranking/PCA browser checks** pass. Full charts register labels, scores, titles,
axes and plot bounds against Scanpy at 100 display/150 export DPI and DPR 1.5;
overlays stay temporary. Linear/log hover, disabled hover and offline HTML are
observed. All **15 UMAP notebook code cells** completed in Jupyter and the variance
plot was visually checked. Ruff formatting/lint and mypy pass.

Resource observation: macOS 26.6.2 arm64, Python 3.11.15, Scanpy 1.11.5, AnnData
0.12.19, NumPy 2.4.6, pandas 2.3.3, Core 1.0.0, Chromium 156.0.8078.4. Seed 17;
100,000 × 20,000 CSR expression (unread), a resident 5,000-element float64 vector
formed by sorting uniform[0.0001, 1] draws descending and normalizing their sum;
n_pcs=30, log=True, 360 × 240 pixels. Excluding imports/source construction,
preparation took **0.012 s**, validated JSON serialization **0.565 s**, peak traced
Python allocation **0.503 MiB**, retained **0.243 MiB**. The payload contains
**2,816 bytes** and 31 labels. Browser render was **1.294 s**, paused label hover
**113 ms**, retained JS heap after collection **6.29 MiB**. The unchanged renderer
is also covered by the larger three-panel/93-label loadings observation above;
this run adds the variance/log data path. Larger displayed rank counts remain
unmeasured. These are local observations, not timing guarantees or closure of
M06/M07.a/b resource gates.

Remaining limits: finite resident vectors, positive values throughout log input,
inherited native font/tick/spacing differences, and inactive image saving (M14).
The separate overview increment is recorded below. The full repository/integration
suites and documentation build were not rerun for this narrow addition.
Clearance: retain the live PLAN/STATUS and permanent source/tests/contracts;
no working document is eligible for removal.

## M07.c PCA overview

Closed for the bounded stored-PCA preview. The
[public entry point](../../src/genome_spy/integrations/scanpy/pl.py) calls the existing
PCA, loadings and variance-ratio functions with show=False, then uses native
vertical composition and one shared display decision. Each row has a native
horizontal composition so narrow plots retain their dimensions instead of
stretching to the three-loading-panel width. No data/chart module, analysis,
color conversion or Core patch was added.

The [maintained contract](../../docs/integrations/scanpy/index.md#pca-overview)
keeps Scanpy's forwarded scatter options and diagnostic defaults. Explicit
show/save follow the common native contract. Unsupported kwargs or missing
results fail before any output; genes are never silently filtered.

Evidence:

- [Semantic tests](../../tests/integrations/scanpy/test_pca_overview.py) compare
  each child with its standalone parent, including data, nested configuration,
  component choices, independent scales/guides and unchanged diagnostic defaults.
  Instrumented tests prohibit upstream plotting, PCA computation and expression
  reads for metadata-only colors, and check supplied results remain unchanged.
- [Browser tests](../../tests/integrations/scanpy/browser/test_pca_overview.py)
  register all six panels' labels and scores, assert rendered parent dimensions
  within one logical pixel at DPR 1.5, retain axes/legends, observe point and label
  hover, and confirm x/y PCA zoom leaves the diagnostics fixed. Offline HTML
  renders with external requests blocked. Existing frozen ranking/PCA references
  retain their 100 display/150 export DPI, native-font and rasterization limits;
  the unchanged parent renderers were rerun rather than duplicating references.
- The [UMAP notebook](notebooks/scanpy_umap.ipynb) adds the explicit highly-variable-
  gene subset overview on packaged PBMC data. All 16 code cells completed in a
  restarted Jupyter kernel without errors; existing cell sources and local
  experiments were preserved. Canonical notebook execution is also tested.

Validation: **296 targeted Python checks**, **26 distinct browser checks**
(24 existing ranking/PCA checks and two overview checks), Ruff formatting/lint
and mypy pass. The overview checks were repeated after tightening rendered-size
assertions and preserving native row widths. Full unrelated suites and the docs
build were not rerun. Generated media and live notebook state stay outside commits.

Resource observation: macOS 26.6.2 arm64, Python 3.11.15, Scanpy 1.11.5, AnnData
0.12.19, NumPy 2.4.6, pandas 2.3.3, Core 1.0.0 and Chromium 156.0.8078.4. Seed 17;
5,000 cells × 20,000 genes, empty float32 CSR expression (unread), resident float64
normal coordinates (5,000 × 3) followed by normal loadings (20,000 × 3), then
50 descending uniform[0.001,1] ratios normalized by their sum. Colors are five
categorical groups and a linear 0–1 observation score; embedding panels are
280 × 240, diagnostics retain defaults. Six panels share one 5,000-row point
table plus four 31-row label tables. Excluding imports/source construction,
preparation took **0.024 s**, validated JSON serialization **4.04 s**, peak traced
Python allocation **16.00 MiB**, retained **9.77 MiB**, compact payload
**1,325,894 bytes**. Browser render was **3.99 s**, hover on the most exposed
point **0.77 s including the deliberate pointer pause**, zoom response **158 ms**,
retained JS heap after collection **11.76 MiB**. These local observations bound
the tested workload; they are not portable timing limits. This adds composed
PCA evidence. At this checkpoint, reuse against the older M06/M07.a/b resource
gates had not yet been assessed; the later [resource verification](#m06m07-resource-verification)
records the completed assessment and fresh workloads.

The subsequent resource verification closes gate 4; C11 retains the separate
categorical-guide rendering gate. Parent storage, typography and export limits remain M14. Clearance:
retain the live plan/status and permanent source/tests/contracts; no working
document is eligible for removal.

## M07.d embedding point outlines

Closed for the two-marker native increment. The [shared embedding renderer](../../src/genome_spy/integrations/scanpy/_embedding_chart.py)
adds opaque outer/inner point layers behind the existing foreground. All shared
embedding entry points and PCA overview inherit it; scatter retains its separate
Scanpy signature. Public names/defaults stay `add_outline=False`,
`outline_width=(0.3, 0.05)` and `outline_color=("black", "white")`; None also
disables outlines. Widths are finite nonnegative pairs and colors reuse the
existing CSS validator. An omitted alpha becomes 0.7 only with outlines;
explicit alpha, including None, is retained. Foreground edges are disabled;
outline edges honor the existing scalar edge/linewidth options. Zero-size cells
paint no outline edge. Category guides stay opaque.

Each panel shares one source and sort. Coordinates, observation IDs, masks,
missing colors, reordered size vectors, palettes and analysis caches are unchanged.
Only the foreground handles hover; all layers reuse the existing brush opacity
helper and count/membership path. No analysis, Matplotlib imports, dependencies,
new data columns or framework abstractions were added to production code.

Verification: **366 Python checks**, **43 browser checks**, the canonical UMAP workflow,
Ruff formatting/lint and mypy pass. The [numerical checks](../../tests/integrations/scanpy/test_embedding_outlines.py)
compare sizes, opacity and edges with Scanpy 1.11.5 and prove unchanged source
records across every embedding entry point. [Registered browser checks](../../tests/integrations/scanpy/browser/test_embedding_outlines.py)
cover isolated/overlapping dots and circles, custom widths/colors/edges, zero-area
cells, hover, native brush/count/Python membership, layer dimming, zoom and offline
HTML. Reference export is 150 DPI for a 100-DPI figure against browser DPR 1.5.
WebGL/Agg comparisons check occupied bounds and painted colors in both directions,
allowing a one-CSS-pixel antialiasing neighborhood with at least 95% painted-color
agreement within 32 channel steps; tiny halo edges are not claimed
to be pixel-identical across rasterizers. Existing embedding, brushing and native
guide tests retain their own full-chart coverage. The canonical and live packaged
UMAP workflows complete 17 code cells; committed notebooks have no outputs/state,
and local notebook customizations are preserved.

A local 100,000-cell × 20,000-gene sparse AnnData workload (seed 17, stored float32
UMAP coordinates, four categories plus a numeric score, two 320 × 300 panels,
size 4, alpha 0.7 and xy zoom) sends the same 100,000-row dataset with or without
outlines. Imports/source construction are excluded; tracemalloc covers preparation
and validated JSON. Chromium 156.0.8078.4 runs at 1,400 × 900 / DPR 1 on the same
macOS/Python/scientific-stack versions as the preceding records.

| Chart | Prepare s | JSON s | Python peak MiB | JSON MiB | Paint s | JS heap MiB |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Plain | 0.048 | 16.425 | 377.03 | 37.808 | 14.661 | 189.78 |
| Outlined | 0.070 | 16.729 | 374.49 | 37.819 | 13.780 | 202.18 |

These are local observations, not CI limits or a speedup claim. Large JSON
validation/transport remains M05.d/M14 work; generated media and raw reports stay
local. Callable `vmin`/`vmax` is delivered in the following increment; C11, C13 and
wider family limits retain their existing owners. Unrelated repository tests and the
docs build were not rerun. Clearance: retain; no plan is eligible for removal.

## M07.d callable color bounds

Closed for shared 2D embeddings and PCA overview's embedding panel. The existing
[bound resolver](../../src/genome_spy/integrations/scanpy/_style.py) accepts
callable `vmin`/`vmax`, alone, in singleton lists or in panel-length lists mixed
with numbers, percentiles and None. Categorical panels skip bounds. Each callable
runs once per numeric panel and receives a copied NumPy vector after masking,
in Scanpy's painting order, with missing values retained. `sort_order=False`
retains source order. The same draw-order helper serves callbacks and points.
Callback edits cannot affect plotted colors, subsequent bounds or AnnData.
Finite real scalar results, including NumPy scalars, are accepted; invalid
results name the bound and panel. Callback exceptions propagate. Existing
lower/upper and constant-colorbar handling is unchanged. No new renderer,
dependencies, Matplotlib use or analysis computation was added. Scatter's
distinct upstream signature remains unchanged.

Verification: **363 targeted Python checks**, **46 browser checks**, Ruff and mypy
pass. [Semantic tests](../../tests/integrations/scanpy/test_color_bounds.py)
compare callback arrays, dtypes and resulting domains against public Scanpy
1.11.5 for sorted/source order, masks, missing values, raw and layers. Every
shared embedding entry point produces the same complete spec as explicit numeric
bounds, including axes, labels, guides, point sizes and native interactions.
Invalid outputs, isolation, constant limits and reversed bounds have focused
checks. [Browser tests](../../tests/integrations/scanpy/browser/test_umap.py)
exercise callable bounds through zoom/reset and offline HTML without rerunning
Python callbacks. Existing registered overlays, footprints, categorical/numeric
guides, embedding hover/zoom and browser rasterization checks passed unchanged.
The canonical packaged-PBMC workflow test passes; Jupyter executed all eighteen
nonempty UMAP notebook cells without errors, including the two-gene callable example.

Resource recipe: Python 3.11.15 on macOS arm64, seed 17, 100,000 observations,
20,000-gene empty CSR, stored float32 2D coordinates, four-group categorical and
numeric observation colors; two 320 × 300 panels, size 4, alpha 0.7 and zoom.
After imports were warmed, five preparation runs under tracemalloc had median
45.6 ms for explicit numeric bounds and 54.8 ms for `nanmin`/99th-percentile
callbacks, with peak preparation allocations 13.0/12.4 MB. Each callback saw
100,000 values once per chart; no expression columns or full matrix were read.
Both versions serialized to byte-identical 39,644,504-byte JSON. Rendering and
transport therefore use the unchanged numeric chart path; reuse the
[100k-cell rendering/memory envelope](#m07d-embedding-point-outlines), alongside
this increment's browser checks. Callback cost depends on the supplied function;
there is no performance claim for arbitrary user code. Reports/media stay local.

Centered numeric colors are delivered below. C11/C13 and broader storage/export options
retain their existing owners. The full repository suite and docs build were not
rerun. Clearance: retain; no plan is eligible for removal.

## M07.d centered embedding colors

Closed for shared 2D embeddings and PCA overview's embedding panel. `vcenter`
uses the existing [color-bound resolver](../../src/genome_spy/integrations/scanpy/_style.py)
for numbers, percentiles, callables and singleton/per-panel lists; None keeps
the original linear scale. The prepared domain becomes `[low, center, high]`,
which GenomeSpy renders as a native diverging scale, equivalent to `domainMid`.
Source measurements, coordinates, IDs, masks, sizes and drawing order stay intact.
No normalized data columns, renderer layers, runtime modules or dependencies
were added. Categorical panels skip centers and scatter keeps its own signature.

Automatic bounds expand to enclose a center outside the observed range;
explicit bounds must strictly enclose it. The shared constant-range expansion
still supplies the visible colorbar. When every value equals the center and
the colorbar is hidden, Scanpy 1.11.5 uses the last scheme color; the existing
constant-color encoding now handles this case too. Integer observation colors
also retain their NumPy dtype instead of attempting to insert NaN into an
ordinary integer array; nullable pandas columns keep their NA conversion path.
Matplotlib normalization objects remain explicitly unsupported.

Verification: **438 targeted Python checks**, **33 browser checks**, Ruff and mypy
pass. [Semantic checks](../../tests/integrations/scanpy/test_color_bounds.py)
compare public Scanpy callback inputs/dtypes and limits for masks, raw/layers,
per-panel settings, centers outside the data, explicit limits and constant
values. Complete chart equality verifies the shared embedding aliases.
[Registered browser comparisons](../../tests/integrations/scanpy/browser/test_color_bounds.py)
cover asymmetric/clipped colors, percentile centers, expanded limits and
constant colors with/without a guide, at 150 export DPI and browser DPR 1.5.
They reuse the existing complete-chart/overlay helper and check that zero's
guide tick and midpoint color align even with unequal bounds. Existing embedding
hover, zoom, linked brush/count/Python membership, four-side guides and offline
HTML checks pass with centered colors. The canonical PBMC workflow test and all
nineteen nonempty UMAP notebook cells complete successfully. Media and notebook
execution state remain local.

Resource recipe: seed 17, 100,000 observations × 20,000-gene empty CSR, stored
float32 normal 2D coordinates, four-category labels and normal observation scores;
two 320 × 300 panels, size 4, alpha 0.7 and zoom. In one warmed run on Python
3.11.15/macOS arm64 with bundled Core 1.2.0, linear/centered preparation took
49.9/52.2 ms, validated JSON serialization 17.33/16.90 s, peak traced Python
allocation 395.5/392.8 MB and browser first paint 14.78/14.49 s. Reported JS heaps
were 212/199 MB. Payloads were 39,717,366/39,717,385 bytes; the only data-path
addition is the middle scale stop. Expression was unread and no full matrix was
densified. These local observations bound this workload, without a speedup claim.
The renderer, notebook delivery and transport retain their existing limits.

Stored neighbor-graph edges are delivered below. C11/C13, broader storage/export and
other families' center/normalization options retain their existing owners.
The full repository suite and docs build were not rerun. Clearance: retain;
no plan is eligible for removal.

## M07.d stored neighbor-graph edges

Closed for the shared embedding entry points and PCA overview's embedding panel.
`edges=True` reads saved connectivities once; the existing
[embedding preparation](../../src/genome_spy/integrations/scanpy/_embedding_data.py)
uses NetworkX's undirected conversion, as Scanpy does. Default/custom neighbor
keys, current-over-legacy storage, asymmetric entries, negative weights and
explicit sparse zeros retain their upstream meaning. Stable cell IDs connect
each edge to its endpoints. No neighbors, embedding or expression analysis is
run, no matrix is densified, and source arrays/metadata are left intact.

The [shared renderer](../../src/genome_spy/integrations/scanpy/_embedding_chart.py)
draws native rules beneath points and outlines, with two native lookups into
the existing cell table. Multi-panel charts serialize one cell table and one
edge list. Endpoint padding matches Scanpy's initial limits; zoom, point hover,
linked selection/count and Python membership use the existing paths. Edges
are unpickable and brushing does not recolor them. Empty graphs retain the
ordinary point chart, and inactive edge settings have no effect.

This bounded increment supports the first component pair, finite nonnegative
widths in points (default 0.1), and one opaque CSS color (default grey).
Missing/invalid graphs fail clearly. Other component pairs, self-loops and
per-edge/numeric colors remain M07.d/M14. Scanpy 1.11.5's renderer passes the
whole stored coordinate array to NetworkX, ignores requested component pairs,
and fails with more than two stored columns. Our adapter leaves extra columns
intact and renders the first pair; it rejects other requested pairs rather
than drawing misaligned edges. Scatter keeps its distinct upstream signature.

Verification: **475 targeted Python checks**, followed by **38 edge checks**
after adding coincident endpoints to the fixture; **37 browser checks**, Ruff
and mypy pass. [Semantic comparisons](../../tests/integrations/scanpy/test_embedding_edges.py)
use public Scanpy plots to verify edge order, styles and axis limits across
dense/CSR/CSC matrices and arrays, plus views/backed access without densification.
[Registered browser comparisons](../../tests/integrations/scanpy/browser/test_embedding_edges.py)
cover zero/default/thick strokes, two colors, outlines and point draw order at
150 export DPI and browser DPR 1.5. They compare interior paint positions within
one logical pixel, total ink within 10%, point colors and every edge's presence
and hue; boundary cropping excludes two physical pixels. Native title/axis
labels and colorbar geometry are also checked. Existing interaction/HTML checks
now exercise stored edges. The canonical packaged PBMC workflow and all twenty
nonempty live notebook cells complete successfully. The graph example has 700
cells and 4,996 edges. Explicit notebook marker sizes are now 20 (15 in the graph
example); the public Scanpy size default is unchanged. Media and execution state
remain local.

Resource recipe: seed 17, 25,000 cells × 20,000-gene empty CSR, stored float32
normal 2D coordinates, four-category labels and numeric observation scores;
seven forward ring neighbors symmetrized into 350,000 CSR entries / 175,000
undirected edges. Two 320 × 300 panels use size 4 and zoom. In one warmed local
run on Python 3.11/macOS arm64 with Core 1.2.0, points-only/edges preparation
took 0.019/1.726 s, validated JSON serialization 4.55/26.49 s, peak traced Python
allocation 99.2/386.4 MB and browser first paint 4.18/12.80 s. Payloads were
9,902,789/23,754,346 bytes and reported JS heaps 68/225 MB. Expression was unread;
no graph sampling or full-matrix densification was used. These observations
expose the cost of sending all edges; larger graph transport remains M14.

Square/diamond markers are delivered below; further marker details stay M14. C11/C13,
broader storage/export and other graph forms retain their existing owners.
The full repository suite and docs build were not rerun. Clearance: retain;
no plan is eligible for removal.

Sparse-validation follow-up: sparse values are read through COO for the finite
check, leaving the original matrix and NetworkX edge conversion intact. Legacy
LIL graphs now match public Scanpy geometry, order and styles under default and
custom neighbor keys; nonfinite LIL values still raise a named validation error.
**263 targeted Python checks**, Ruff and mypy pass. Earlier browser/workflow
evidence is retained because graph conversion, serialization and rendering are
unchanged; browser, notebook and resource runs were not repeated for this fix.
Scope and clearance remain unchanged; the current queue owns next work.

## M07.d square markers

Closed for shared embeddings, PCA overview's embedding panel and scatter.
`marker="s"` uses one native square encoding in the
[shared renderer](../../src/genome_spy/integrations/scanpy/_embedding_chart.py);
missing-value points, outlines and legend symbols inherit it. The existing
size conversion matches Scanpy's unit-width square path. Scalar/per-panel
marker choices reuse each entry point's current broadcasting. Source data,
draw order, color mapping, graph edges and interactions are unchanged; there
are no new runtime helpers, layers, columns or dependencies.

Verification: **417 targeted Python checks**, the canonical notebook workflow,
**26 browser checks**, Ruff and mypy pass. The numerical outline tests now
include squares and graph tests exercise mixed circle/square panels across all
embedding entry points. Scatter checks retain the same table and size units.
[Registered isolated squares](../../tests/integrations/scanpy/browser/test_umap.py)
verify occupied corners and side lengths, including
strokes, at 150 export DPI / browser DPR 1.5; a circle cannot pass the corner
check. Overlapping outline comparisons retain the occupied-bound checks and
compare flat paint outside each rasterizer's antialiasing transition, allowing
one logical pixel of registration and 32 channel steps. Native square legend
symbols, hover, linked brush/count/Python membership, zoom and offline HTML
are observed through the existing interaction tests. Frozen reference metadata
adds only square cases; images remain local. All twenty-one nonempty live UMAP
notebook cells complete successfully, including a packaged PBMC square example.

Resource recipe: seed 17, 25,000 cells × 20,000-gene empty CSR, stored float32
normal 2D coordinates, four-category labels and numeric observation scores;
two 320 × 300 panels, size 4 and zoom. In one warmed local Python 3.11/macOS
arm64 / Core 1.2.0 run, circle/square preparation took 0.024/0.016 s, validated
JSON serialization 5.79/4.82 s, peak traced Python allocation 99.2/98.0 MB and
browser first paint 4.84/4.39 s. Payloads were 9,902,787/9,902,903 bytes and
reported JS heaps 68/64 MB. Both charts send the same single cell table; square
encodings add 116 bytes. These are workload observations, not a speedup claim.
Expression was unread and no matrix was densified.

The diamond increment below extends this renderer and corrects embedding category
keys to Scanpy's circles at that checkpoint; the legend follow-up below restores
shape-matched keys by request. Other markers, C11/C13, broader storage/export and
other graph forms retain their owners.
The full repository suite and docs build were not rerun. Clearance: retain;
no plan is eligible for removal.

## M07.d diamond markers

Closed for shared embeddings, PCA overview's embedding panel and scatter.
`marker="D"` uses the existing native diamond point shape. Its path width is
√2 times the unit-width square, so the native size encoding receives twice
the nominal area, preserving Scanpy's rotated-square footprint. Stored size
columns, coordinates, colors, point order and graph data are unchanged. One
small [marker table](../../src/genome_spy/integrations/scanpy/_style.py) now serves
validation, point geometry and guide conversion; no new runtime helper or
renderer layer was introduced.

Public Scanpy comparisons exposed an earlier legend assumption: embedding
category keys are circles even for square/diamond points, while scatter keys
retain their actual marker. At this checkpoint the style distinguished those behaviors;
the legend follow-up below supersedes that choice.
Diamond scatter keys carry their converted size on the color legend; a native
size override belongs on that legend's `symbolSize`. This corrects the square
embedding guide too; it does not claim complete scatter legend compatibility.

Verification: **432 targeted Python checks**, the canonical notebook workflow,
**40 browser checks**, Ruff and mypy pass. Existing tests now cover diamonds
across numeric/categorical panels, missing points, outlines, size vectors, mixed
shapes, every embedding alias and stored graph edges. Public artist geometry
remains confined to tests. Registered plain/stroked diamond exports check both
bounds and occupied area, so a same-width circle/square fails the oracle.
Overlapping outlines retain the existing two-way paint comparisons. Native
hover, linked brush/count/Python membership, zoom and offline HTML pass.
[Observed legend comparisons](../../tests/integrations/scanpy/browser/test_scatter.py)
also match public Scanpy's circular embedding keys and diamond scatter keys,
including rendered widths; compact native legend collection remains verified.
The existing PBMC marker cell now compares squares and diamonds instead of adding
another plotting cell. All twenty-one nonempty
live notebook cells complete without errors; committed source excludes outputs.

Resource recipe repeats the square increment's seed-17, 25,000-cell × 20,000-gene
empty-CSR workload, stored float32 coordinates, four labels/numeric scores and
two 320 × 300 panels with size 4/zoom, on Python 3.11/macOS arm64 and Core 1.2.0.
Circle/diamond preparation took 0.029/0.020 s, validated JSON serialization
7.09/5.96 s, peak traced Python allocation 99.2/98.0 MB and first paint
6.17/6.39 s. Payloads were 9,902,817/9,902,933 bytes and reported JS heaps
68/64 MB. Both send the same cell table; native diamond encodings add 116 bytes.
These local observations share a host with tests and are not a speedup claim.
Expression was unread and no matrix was densified. Media/reports remain local.

The subsequent triangle audit is retained below; further marker work is now
deferred to M14. Unsupported markers still fail clearly. C11/C13, larger transport
and broader storage/export retain their owners. The full suite and docs build
were not rerun. Clearance: retain; no plan is eligible for removal.

### Marker legend follow-up

Closed: category keys now inherit each panel's native marker shape, so square
and diamond points have matching keys. This deliberately differs from Scanpy's
circular embedding keys, following visual review. The shared renderer removes
the circle override and its style field; no new helper, data or layer is needed.
Diamond guide sizing reuses the existing path-width conversion in all embeddings.
Native legend configuration still overrides the inherited shape.

Verification: **170 targeted Python tests**, the canonical notebook workflow and
**12 browser tests** pass, along with Ruff and mypy. Browser checks measure circle,
square and diamond keys and widths for UMAP/scatter, compact collected guides,
and existing outline hover/brush/zoom/HTML. All twenty-one live UMAP notebook
cells complete without errors; its marker example visibly has square keys.
No data preparation or point geometry changed, so the diamond resource workload
above remains applicable. The full suite and docs build were not rerun. The
triangle audit is retained under C14; further markers stay M14. Clearance: retain.

## M07.d triangular marker audit

Closed for the audit; support remains blocked by C14. All four Scanpy triangles
(`"^"`, `"v"`, `"<"`, `">"`) have equal path width and height. Native triangles
in the bundled Core 1.2.0 are equilateral: at 100 logical pixels of width the
upright/downward paths are 86.6 pixels tall; horizontal shapes exchange these
dimensions. Source checks confirm the same geometry in WebGL and SVG. The released
point API has uniform size and rotation, without separate width/height controls.
Changing the scalar size cannot preserve both dimensions or the corner angles.
This is a compatibility limit, not evidence that an equilateral native shape is
incorrect. No marker approximation, custom shape or Core patch was introduced.

The [native comparison](../../tests/integrations/scanpy/browser/test_native_triangles.py)
reuses the existing renderer and original observation fixture. It compares public
`sc.pl.umap` paths and painted footprints with native shapes in four directions,
with zero- and two-point strokes. A 72-point marker is 100 logical pixels wide;
references export at 150 DPI from a 100-DPI figure and browser DPR is 1.5. For
the upright case without a stroke, native/reference painted bounds are 148 × 130 /
149 × 150 physical pixels; with a two-point stroke they are 156 × 136 /
155 × 155. One-pixel rasterization differences cannot explain the height gap.
SVG vertices independently show the aspect difference. Generated PNGs and reports
stay in pytest temporary directories.

Verification: **141 targeted Python tests pass**, including explicit triangular
marker rejection across all embedding entry points and scatter. **Eight native
browser comparisons strictly xfail** on the measured geometry mismatch. Their
fixture validates successful rendering, triangle paths and nonempty paint before
the expected-failure assertion; unrelated setup failures remain errors. A future
native match raises an unexpected pass, prompting a support review. Ruff and
mypy pass. Runtime code and the notebook are unchanged, so no notebook example
was added or rerun. Full-suite, docs and resource checks were not run for this
audit. Remaining marker work is now deferred to M14's compatibility backlog;
it does not precede new plot families. Clearance: retain.

## M12.a stored embedding density

Closed for the bounded stored finite 2D density preview. The public function retains
Scanpy 1.11.5's argument names/defaults, omitting ax/return_fig at the maintained
native boundary. It reads obs density values and uns components/covariate only;
never computes KDE, accesses expression, mutates AnnData or creates temporary
columns. Stored coordinates/components and the pinned default-key/FA alias rules
are retained. String categories, supplied group order/repeats, unused levels,
ungrouped results, metadata-only views and backed AnnData are supported.

The density-specific module only prepares metadata and group masks. It reuses
embedding key lookup, coordinate projection/labels, stable IDs, marker validation,
sizes, color bounds, draw order, panel composition and native hover/zoom. No
separate density renderer or adapter framework was added. Shared points project
their own eight fields before native picking makes row copies, avoiding copies
of all other panels' columns. The data source is still serialized once.

Native filtered point layers share geometry, source and sort: gray below range,
continuous colors within range and black above range. They preserve sorted
overlap order. Unsorted mixed ranges fail clearly; native datum predicates or
under/over scale colors would be needed to preserve arbitrary mixed point order
in one mark. A one-element marker list retains the shared helper's normalized
marker; multiple markers fail explicitly. No invalid conditions, hidden guide
marks, Python colormap sampling, custom browser listeners or Core patches remain.

YlOrRd selects the native yelloworangered scheme with different stops from
Matplotlib. Complete chart comparisons use shared viridis; native default
endpoints and under/over colors are checked separately. Numeric/percentile/
callable bounds, centered colors, sizes, coordinate limits, titles and point
order compare to public Scanpy. Hover retains the original stored density for
gray cells; x/y zoom links panels and exported HTML works offline. The packaged
PBMC68k notebook explicitly computes density once, then plots it with smaller
markers; all twenty-three code cells execute. Committed source excludes outputs
and widget state.

Verification: 629 targeted Python/workflow checks and 46 shared embedding browser
checks pass, including seven density browser cases. Schema validation is enabled.
Ruff and mypy pass. The full repository suite and documentation build were not
run for this slice.

Retained evidence: [semantic tests](../../tests/integrations/scanpy/test_embedding_density.py),
[browser comparisons and interactions](../../tests/integrations/scanpy/browser/test_embedding_density.py),
[workflow guard](../../tests/integrations/scanpy/test_notebooks.py),
the existing [embedding benchmark](../../tests/integrations/scanpy/benchmark.py)
with --plot embedding_density, and the
[user contract](../../docs/integrations/scanpy/index.md#stored-embedding-density).
Generated reference images, overlays, exports and resource reports stay in
temporary directories. Broader group types, missing densities, unsorted mixed
colors, typography and image export retain M14 owners; native brushing is not
offered by this preview. No working plan is eligible for clearance.

Resource evidence (Chromium 156, local Apple Silicon, 20,000 sparse genes):
100,000 observations across eight density panels prepare in 0.049 s and produce
29.2 MB Arrow in 1.14 s without densification. Validated JSON is 75.2 MB and takes
124.6 s with allocation tracing; the Python peak of 713.8 MB includes both
transports. This slow large-JSON export remains a measured M14.c limit, not a
promise of interactive serialization. Native inline HTML first paints in 6.84 s,
all sixteen isolated-ID hover probes pass (median 0.064 s, p95 0.100 s after native
dwell), and linked wheel zoom updates in 0.71 s. Retained JS heap is 237.1 MB after
garbage collection. Separate 100,000 × one-panel and 10,000 × eight-panel browser
workloads also pass. These are local observations, not portable timing limits.
The benchmark loads its native HTML file rather than sending this large JSON
through browser automation; earlier dispatch attempts closed without browser
measurements. No Core defect or local patch is inferred from those attempts.

## M10.c Scrublet score distributions

Closed for the stored-score linear/log preview. The new public function preserves
Scanpy 1.11.5's names/defaults, including `show=True`, while omitting Matplotlib
`return_fig`/`ax`. It reads `obs.doublet_score`, `uns.scrublet` simulated scores,
optional thresholds and `batched_by`/`batches` metadata. Plotting never reads
expression, runs Scrublet or modifies obs/uns. Metadata-only views and backed
AnnData work. Category order and missing-batch-label behavior follow Scanpy;
missing results fail rather than pooling or triggering analysis.

Pure preparation uses `np.histogram` with the pinned 50 edges/49 bins from 0 to 1.
Separate observed/simulated denominators include only in-range scores; missing
and finite out-of-range entries are omitted, and the final bin includes 1.
Native rectangles and full-height black threshold rules preserve initial limits,
including thresholds outside the score range. Each pair explicitly keeps its
linear/log density scales independent, as do the batch rows. The existing limit
helper now lives beside numeric validation and handles log constants once for
both Scrublet and highest-expression plots; embeddings/HVG reuse its unchanged
linear path. There is no general histogram/adapter framework.

Keyword-only hover reports populated-bin boundaries, count, density, batch and
sample. Optional score-axis zoom is independent per panel; threshold rules stay
on the same score scale and bins remain fixed. Aggregate marks do not claim cell
selection. Native width/height set panel areas; figsize reserves native title/axis
space at 100 logical pixels per inch. Fonts/ticks/export sizing retain the native
renderer boundary. See the [user contract](../../docs/integrations/scanpy/index.md#scrublet-score-distributions).

Verification: **522 distinct targeted Python/workflow checks** pass across the new
[semantic tests](../../tests/integrations/scanpy/test_scrublet.py), shared contract,
UMAP/embedding/scatter/HVG/highest-expression tests and canonical expression
workflow. Public Scanpy comparisons cover both scales, single/two-batch layouts,
exact density statistics, titles, thresholds and limits. Tests guard expression
and analysis access, validate read-only views/backed metadata, malformed inputs,
duplicate columns and detached chart snapshots. The notebook test permits gene
selection only inside its explicit Scanpy Scrublet preparation call; plot calls
remain guarded. All eighteen live code cells run without errors and produce
fifteen widgets. Tracked source has no outputs or widget state.

**Five new browser checks** register every populated native bar and threshold
against public Scanpy geometry, compare 150-DPI images at DPR 1.5, check labels
and actual scale domains, and observe bin hover, independent zoom and offline
HTML. Registration uses rendered SVG clip bounds to account for viewport
rounding; raster limits allow fractional bin-edge antialiasing. Complete charts,
references and overlays are generated only in temporary directories. Source:
[browser/test_scrublet.py](../../tests/integrations/scanpy/browser/test_scrublet.py).
**Nine existing highest-expression/HVG browser checks** also pass through the
shared limit helper. Ruff and mypy pass; the full repository suite and docs build
were not rerun.

Resource recipe: [benchmark_scrublet.py](../../tests/integrations/scanpy/benchmark_scrublet.py)
uses seed 17, 100,000 observed cells, 200,000 simulated scores, four batches/eight
panels and an empty sparse AnnData shape of 100,000 × 20,000. Expression access
raises. Preparation took 0.024 s, validated JSON 1.01 s and browser first paint
4.36 s on Python 3.11.15/macOS arm64/Core 1.2.0. The payload is 84,610 bytes;
peak traced Python allocation is 5.83 MB and reported JS heap 35.1 MB. Imports,
fixture and warm-up are excluded; Python timings include allocation tracing.
These are local observations, not portable speed guarantees. Reports stay local.

Boundary: only linear/log scales; unsupported Matplotlib modes (including
symlog/logit), unused batch categories, infinite scores and score vectors with no
in-range values fail explicitly. The PBMC3k example computes Scrublet explicitly
with Scanpy, seed 0 and a demonstration threshold of 0.25 on a copy of the counts.
No datasets are vendored. Remaining compatibility stays M14. The stored-density
preview is delivered under M12.a above. Clearance: retain; no working plan is eligible for removal.

## M10.a highest-expression summaries

Closed for the count-percentage preview. `highest_expr_genes` reads X or a requested
layer, never raw, and reuses `sc.pp.normalize_total(target_sum=100, inplace=False)`.
An AnnData shell shares the selected matrix, so Scanpy cannot materialize the
caller's view. Normalization copies counts; only one selected gene column is
made dense at a time. Ranking uses the pinned reverse-argsort mean order,
including ties and zero-total cells in the denominator. NumPy percentiles and
1.5-IQR whiskers are tested independently against public Scanpy output.

Native rectangles, rules and points retain linear percentage summaries, including
on logarithmic axes. Native band labels preserve gene order; log limits depend
on drawn coordinates. Optional box/outlier hover and percentage-axis zoom use
Core directly, with existing stable observation IDs for outliers. Source/layer
checks, identity, fonts, units, display and coordinate-domain helpers are reused.
No plotting artists, benchmark code or Matplotlib utilities enter the adapter.

The PBMC3k notebook example loads actual counts via `sc.datasets.pbmc3k()` rather
than applying percentages to the earlier scaled dataset. The downloaded dataset,
notebook outputs, references, overlays and resource reports stay local.

Boundary: resident finite nonnegative counts, positive n_top, and unique
nonmissing selected labels. Backed/lazy counts, ambiguous selected labels and all
forwarded Seaborn/Matplotlib styling options fail clearly; remaining compatibility
belongs to M14. Boxes use native category10 colors, repeating after ten genes,
without Seaborn saturation adjustments. Fonts/ticks are independent of Matplotlib
global settings. No embeddings, selection or DE are recomputed.

Verification: **270 targeted Python/workflow checks** pass across the new
[semantic tests](../../tests/integrations/scanpy/test_highest_expr.py), shared
contract, stored-variable-gene tests and canonical expression notebook. Tests
compare public Scanpy boxes, quartiles, whiskers, fliers, labels, source precedence,
reverse-argsort order, linear/log limits (including constants), mutation and sparse
column access. **Three browser checks** register linear/log boxes against 150-DPI
Scanpy references at DPR 1.5, check native palette bins and labels, and observe
box/outlier hover, percentage-axis zoom and offline HTML. Source:
[test_highest_expr.py](../../tests/integrations/scanpy/browser/test_highest_expr.py).
References, complete exports and registered overlays are generated only in pytest
temporary directories. All sixteen live notebook code cells run without errors,
producing fourteen widgets; tracked source excludes outputs and widget state.
Ruff and mypy pass. The full repository suite and docs build were not rerun.

Resource recipe: [benchmark_highest_expr.py](../../tests/integrations/scanpy/benchmark_highest_expr.py)
uses seed 17 and 50,000 × 20,000 sparse count data with 1,000,000 stored values,
selecting twenty genes. It enforces exactly twenty dense 50,000 × 1 accesses;
full-matrix densification fails the check. With Python 3.11.15/macOS arm64/Core
1.2.0, preparation took 0.480 s, validated JSON 0.895 s and browser first paint
1.98 s. Payload is 118,801 bytes, peak traced Python allocation 36.0 MB, reported
JS heap 19.3 MB. Imports, fixture and one-time warm-up are excluded; Python timings
include allocation tracing and normalization. The final constant-domain refinement
does not affect this nonconstant workload. These are local observations, not
portable performance guarantees. Reports stay local.

The Scrublet preview is delivered under M10.c above. Broader compatibility
remains M14; the QC family is not closed. Clearance: retain; no working document is eligible for removal.

## M10.b variable-gene diagnostics

Closed for the stored-statistic preview. `highly_variable_genes` and the legacy
`filter_genes_dispersion` share a thin metadata preparation function in
[_scatter_data.py](../../src/genome_spy/integrations/scanpy/_scatter_data.py)
and a dedicated [_hvg_chart.py](../../src/genome_spy/integrations/scanpy/_hvg_chart.py).
They reuse numeric checks, point IDs, coordinate limits, font/point units and
common optional-dependency/display/save handling. No new data module or adapter
framework is introduced. The adapter reads three plotted vectors and a boolean
selection flag; X/raw/layers and gene-selection analysis are never accessed.
Caller data stay unchanged, and charts keep detached snapshots.

Supported input is AnnData.var with stored hvg flavor, a DataFrame or a legacy
record array. The pinned flavor lookup and highly_variable/gene_subset switch
are preserved, including different variance detection for AnnData versus tables.
Duplicate labels keep distinct IDs; views/backed metadata and missing coordinate
pairs retain their order. Selected genes draw before other genes. Log axes keep
stored values and Scanpy's raw-statistic limits on both panels. Native config
domains serialize as ordinary JSON numbers even for float32 inputs. Invalid
flags/fields and unsupported log bounds fail clearly; there is no analysis fallback.

The pair uses native points, explicit fill/stroke scales and one native bottom
fill legend, with actual black/gray guide colors checked. Hover reports gene
identity and original statistics. Optional x/y zoom is independent per panel,
preserving differing initial limits when missing pairs remove different genes.
Native fonts/ticks/guide placement remain deliberate renderer boundaries.
The legacy wrapper preserves its deprecation warning and returns a native chart
for show=False, rather than the old wrapper's None. See the
[maintained contract](../../docs/integrations/scanpy/index.md#variable-gene-diagnostics).

Verification: **299 targeted Python tests** and the canonical expression workflow
pass, plus **seven browser checks**. The
[semantic tests](../../tests/integrations/scanpy/test_hvg.py) compare public Scanpy
coordinates, limits, labels, units, masks and ordering across inputs/flavors/log
modes, guard expression/analysis access and test snapshots. The
[browser tests](../../tests/integrations/scanpy/browser/test_hvg.py) register both
panels against 150-DPI references at browser DPR 1.5, including labels, native
guide colors, hover, zoom and offline HTML. Existing scatter rendering also
passes through the reused test helper. All fifteen live expression notebook cells
complete without errors; committed source excludes outputs and widget state.
Ruff and mypy pass. The full repository suite and docs build were not rerun.

Resource recipe: [benchmark_hvg.py](../../tests/integrations/scanpy/benchmark_hvg.py)
uses seed 17, 20,000 gene metadata rows, two panels and an empty-CSR AnnData shape
of 100,000 × 20,000. Expression access raises; the workload measures metadata,
not expression computation. On Python 3.11.15/macOS arm64/Core 1.2.0, preparation
took 0.024 s, validated JSON 3.03 s and browser first paint 2.90 s. The single
20,000-row table produces a 3,847,678-byte payload, 34.3 MB peak traced Python
allocation and 53.5 MB reported JS heap. Imports/fixture are excluded; allocation
tracing is enabled during Python timings. This is one local observation, not a
portable time limit or speedup claim. Generated reports/images remain local.

Highest-expression and Scrublet previews are delivered under M10.a/c above.
This increment does not close the full QC family; remaining compatibility belongs to M14.
Clearance: retain; no working plan is eligible for removal.

## M07.d native colorbar placement

Delivered in `730f9ce`. The shared `embedding`, `umap`, `tsne`, `diffmap`,
`draw_graph`, `pca` and
`pca_scatter` entry points support `colorbar_loc="right"` (default), `"left"`,
`"top"`, `"bottom"`, and None. Vertical bars use the plot height; horizontal bars
use the plot width, with the existing 30:1 gradient aspect. Categorical legends
retain `legend_loc` and stay explicitly right/vertical when colorbars move.
Numeric defaults remain overridable through native legend configuration and
collection, including linked charts. Scatter's public signature is unchanged.

Permanent checks live in `tests/integrations/scanpy/test_colorbar.py` and
`tests/integrations/scanpy/browser/test_colorbar.py`. The latter measures complete
guide bounds on mixed one/two-row 320 × 180 panels at DPR 1, verifies all category
labels and collected overrides, and allows two logical pixels for native gradient
borders/snapping. Existing embedding/scatter reference and interaction checks
cover default appearance, hover IDs, zoom, linked counts/Python membership and
offline HTML. All seven entry points preserve transported records and point/axis
encodings when changing placement or applying native numeric-guide overrides.

Workflow evidence: a temporary Jupyter notebook uses Scanpy's packaged PBMC
700 × 765 dataset, retains stored UMAP coordinates, and produces five anywidget
displays and inline HTML exports for the four sides/None. All five exports render
with external requests blocked. User notebooks are not edited or executed;
generated notebooks, screenshots and HTML stay in temporary directories.

Resource gate reuse: the [M06/M07 resource envelopes](#m06m07-resource-verification)
cover the unchanged preparation, transport, point marks and interaction paths.
The equality checks retain the same records and encodings; this increment adds
only native guide configuration, with new layout coverage above. The larger
eight-panel timing/heap workloads were not rerun; no new performance claim is made.

Validation: **197 targeted Python checks**, **41 browser checks**, five real-kernel
widget displays and five offline packaged-data exports, Ruff and mypy pass.
The separate Core 1.2 C11 reproducer remains an expected failure; upstream
[PR #591](https://github.com/genome-spy/genome-spy/pull/591) does not change the
bundled runtime. Broader M07.d options and M14 storage/typography/export limits
remain open. The current grid-migration queue and plan clearance remain unchanged.

## M01 retained delivery evidence

The M01 preview is recorded in `a536bf6` and `ecd27c8` with earlier implementation
history in Git. Its retained evidence is:

- [Current compatibility contract](../../docs/integrations/scanpy/index.md),
  including explicit input, color, typography and supported-option limits.
- [API/default/error tests](../../tests/integrations/scanpy/test_contract.py),
  [UMAP semantics](../../tests/integrations/scanpy/test_umap.py),
  [frozen-reference tests](../../tests/integrations/scanpy/test_reference.py), and
  [selection membership](../../tests/integrations/scanpy/test_selection.py).
- [Complete-chart/hover/navigation checks](../../tests/integrations/scanpy/browser/test_umap.py)
  and [observed brush/count/widget/Python/offline checks](../../tests/integrations/scanpy/browser/test_brushing.py).
- [Reference metadata and images](../../tests/integrations/scanpy/fixtures/README.md),
  [resource baseline](../../tests/integrations/scanpy/fixtures/performance-baseline.json),
  and explicit [benchmark](../../tests/integrations/scanpy/benchmark.py).
- [UMAP packaged-data workflow](README.md#plotting-workflows): basic
  plotting, linked brushing/Python retrieval, then customization. Shared setup
  and duplicate charts from the three earlier notebooks have been consolidated.
  All UMAP examples enable x/y zoom and panning. Linked brushing uses Shift-drag
  in the first panel so ordinary dragging remains available for navigation.

UMAP preview baseline (`e04e261`): 119 integration checks and 20 browser checks pass,
as do Ruff formatting/lint and mypy. The workflow test executes every cell,
checks unchanged source UMAP coordinates, and reruns Python retrieval for a
nonempty selection. The UMAP notebook renders in a fresh kernel/browser.
A built-wheel smoke test confirms that the compatibility package is absent,
the sole integration namespace imports lazily, and UMAP chart authoring works.
Notebook format, documentation/download/CI paths, and all 50 inventory rows were
also checked. The shared source/test links above retain the evidence.

The full documentation site and unrelated test suites were not rebuilt for this
cleanup. Resource results are the retained October 17 baseline, not a new
performance measurement. No new plot family or Core capability was implemented.

Workflow split verification (October 17): both notebooks execute independently
in fresh Jupyter kernels and retain their existing charts. The two workflow tests
and repository Ruff checks pass; notebook format and updated download/CI paths
were checked. CI now renders both workflows. The full documentation site was
not rebuilt for this reorganization; no working plan is newly eligible to clear.

## M02.a/b preparation and statistics

Verified scope: [_grouped_data.py](../../src/genome_spy/integrations/scanpy/_grouped_data.py)
reuses public `sc.get.obs_df` for selected expression/metadata, raw/layer and symbol
lookup. AnnData categorization touches only the detached table. Values retain
observation order, repeated feature slots, grouping/category order and bracket
metadata. Means, strict-cutoff fractions and scaling are separate pure functions.
[_data.py](../../src/genome_spy/integrations/scanpy/_data.py) shares source/storage
checks with UMAP; its existing semantics remain covered.

Evidence: [64 focused semantic/resource checks](../../tests/integrations/scanpy/test_grouped_data.py),
[17 frozen upstream cases](../../tests/integrations/scanpy/fixtures/grouped.json)
with [original input/provenance](../../tests/integrations/scanpy/grouped_fixture.py)
and an [explicit generator](../../tests/integrations/scanpy/generate_grouped_references.py).
All **183 integration checks**, Ruff and mypy pass. The allocation guard uses
100,000 observations × 20,000 sparse genes, densifies only three unique requested
columns, retains float32 values, and caps preparation/statistics allocations at
64 MiB. This is a data-allocation guard, not a browser/render performance baseline.

Current input boundaries:

- Dense NumPy and CSR/CSC matrices, views, and resident observation metadata are
  covered. Backed/lazy expression is rejected before reading X. Scanpy 1.11.5's
  public getter does not handle sparse arrays; grouped preparation rejects those
  explicitly. UMAP keeps its existing sparse-array support.
- Raw symbol lookup and duplicate-variable rejection follow the grouped getter,
  which intentionally differs from UMAP. Infinite values, undefined log1p
  inputs, ambiguous index/column grouping and joined-label collisions fail clearly.
- Multi-key grouping currently requires nonmissing categorical string annotations.
  Missing multi-key values are rejected explicitly. Unused categories remain
  metadata; statistics include only observed groups, without invented zero rows.
- Ordinary NaN comparisons are false and count toward the fraction denominator;
  nullable pandas NA retains the upstream comparison/count exclusion. Means have
  their own missing/expressed-only denominator.

M02.a/b are closed for this stated scope, with no separate working plan to clear.
M14.c owns broader backed/lazy and sparse-array access. These were data-only
checks; the chart delivery below supplies separate browser/workflow evidence.

## M02.c/d plain dotplot preview

Runtime: [public callable](../../src/genome_spy/integrations/scanpy/pl.py),
[pure displayed statistics](../../src/genome_spy/integrations/scanpy/_grouped_data.py),
[native chart](../../src/genome_spy/integrations/scanpy/_dotplot_chart.py), and
[shared color validation](../../src/genome_spy/integrations/scanpy/_style.py).
Chart construction takes detached tables, not AnnData. It uses released points,
rules and text; no Core patches, custom polygon recipes or benchmark imports.

Delivered: category/feature ordering, repeated feature slots, brackets on either
orientation, mean/percentage guides, clipped power area mapping, numeric color
bounds, supplied color tables, native sizing and explicit display/export errors.
Scanpy 1.11.5 applies scaling again after transposing the display table; supplied
color tables skip only the constructor pass. Tests retain both behaviors.
The [PBMC expression notebook](notebooks/scanpy_expression.ipynb) uses the core
tutorial marker dictionary against existing `bulk_labels`. Its data/marker setup
will serve matrixplot and heatmap examples too. No clustering or ranking is added
to the example.

Evidence:

- [Dotplot contract/semantic tests](../../tests/integrations/scanpy/test_dotplot.py)
  include hand calculations, frozen geometry, kwargs, source access, missing
  values, allocation shape, immutability, supplied labels and display modes.
- [Eleven frozen full figures/crops](../../tests/integrations/scanpy/fixtures/dotplot.json)
  record Scanpy 1.11.5 exports at 100/150 display/export DPI, input checksums,
  versions, domains, point positions/areas/paint and labels. The
  [explicit generator](../../tests/integrations/scanpy/generate_dotplot_references.py)
  uses original MIT test inputs. No Scanpy source or real dataset is vendored.
- [14 dotplot browser checks](../../tests/integrations/scanpy/browser/test_dotplot.py)
  cover complete charts in both orientations, native guides/brackets, registered
  plot areas/overlays at DPR 1.5, zero footprints, colors and offline HTML.
  Viridis comparisons isolate shared-palette paint from Vega reds' different
  stops. Footprints allow 2 backing pixels; interior paint allows 12/255 per RGB
  channel for palette bins/WebGL rasterization. No fitted image alignment.
- The [resource baseline](../../tests/integrations/scanpy/fixtures/dotplot-performance.json)
  records 100,000 × 20,000 sparse input with 40 selected genes and 50 groups.
  Only a 100,000 × 40 table densifies; 2,000 summary dots serialize to 151 KB.
  Cold plotting including optional imports took 2.90 s, peak tracked allocations
  149 MB and process RSS 513 MB. Chromium 156 first paint including dispatch took
  0.81 s with 10 MB JS heap at DPR 1. These are local observations, not portable
  timing limits. The [benchmark](../../tests/integrations/scanpy/benchmark_grouped.py)
  is explicit and independent of ignored research.

Validation: 222 integration checks passed, followed by all 43 dotplot/workflow
checks including the added missing-value/raw-access and constant-paint cases
(225 distinct integration checks covered in total). All 33 integration browser
checks passed, including UMAP regression checks; the final bracket endpoint/stroke
adjustment and constant-paint case have their own browser reruns (34 distinct
browser checks covered). Ruff and mypy pass.
The PBMC dotplot workflow was run from a fresh live kernel and viewed.
The full documentation site and unrelated test suites were not rebuilt.

Label-placement correction (October 17): rotated text now uses screen-position
offsets, so gene labels clear the matrix and marker-group labels stay centered
outside their brackets. Scanpy's bracket coordinates are unchanged. Browser
checks measure exported text bounds for vertical/horizontal top labels, repeated
genes, unequal label lengths and swapped axes; the new clearance check fails with
the original offsets. All 15 dotplot browser checks and 43 dotplot/workflow checks,
Ruff and mypy pass. The packaged-PBMC notebook was rerun and inspected in Jupyter.
Resource measurements and unrelated families were not rerun for this layout fix.

Index scales and summary hover (October 17): both axes now use integer index slots,
with outer padding and within-band bracket positions preserving registered Scanpy
geometry. Native tooltip rows identify gene, group, displayed mean/color value and
the actual expressing-cell percentage before size clipping. `hover=True` is the
default; `hover=False` disables picking/tooltips. Scaled means and supplied colors
have explicit tooltip labels. Zero-area and missing dots remain unpainted.
All 50 dotplot/workflow checks and 20 dotplot browser checks pass, including native
bracket-span painting for all seven PBMC marker groups, both orientations and
legend title placement. Ruff and mypy pass.
The updated PBMC notebook was rerun from a fresh kernel and hovered in Jupyter.

The [updated resource observation](../../tests/integrations/scanpy/fixtures/dotplot-index-hover-performance.json)
still densifies only the requested 100,000 × 40 columns of the 20,000-gene sparse
matrix. Its 2,000 summaries serialize to 198 KB including tooltip labels; cold
preparation took 3.04 s, peak tracked allocations 149 MB and process RSS 511 MB.
Chromium first paint took 0.86 s with 10 MB JS heap. The earlier baseline remains
retained; these are local observations, not portable timing limits. Other plot
families and the complete documentation site were not rerun for this slice.

Preview limits, retained in the [compatibility guide](../../docs/integrations/scanpy/index.md#dotplot-compatibility):
unused/empty groups error; all-zero fractions require explicit `dot_max=1`;
missing statistics retain slots but do not paint. M05.e adds navigation and hover
highlighting; summary brushing remains deferred.
Native Lato, guide layout, line-break flattening and Vega reds differ from the
Matplotlib reference. `figsize` is a documented native plot/guide budget rather
than a fixed outer canvas. Full typography/palette/export/access closure remains
M14; trees remain M04; `DotPlot` and supplied `dot_size_df`/style chains remain M13.
No unimplemented option is silently ignored. C08's dotplot slot handling is
verified with native text labels; other grouped families still need their checks.

M02 is closed only for this plain-chart preview. The maintained
source, notebook, tests, references and compatibility contract are retained;
there is no per-slice working plan to clear and no research artifacts are deleted.

## M03.a–c plain matrixplot preview

Runtime: [public callable](../../src/genome_spy/integrations/scanpy/pl.py),
[shared statistics](../../src/genome_spy/integrations/scanpy/_grouped_data.py),
[shared grouped layout](../../src/genome_spy/integrations/scanpy/_grouped_chart.py)
and [native tile chart](../../src/genome_spy/integrations/scanpy/_matrixplot_chart.py).
No family-specific data module or adapter framework was added. Dotplot now uses
that same native slot/label/bracket/guide layout; its serialized hover-case spec
was checked against the previous implementation and is unchanged.

Computed values use selected expression, log1p before averaging, then one min–max
scaling pass before optional transpose. Supplied `values_df` bypasses means,
log/scaling, retains its own row/column order, and follows explicit category row
reindexing only. Exact labels and feature multiplicities are required; duplicate
group labels error. Repeated supplied feature slots retain independent values.
Native rectangles fill adjacent index slots with gray 0.1-point edges and a
1.5-point frame. Singular scalar `edgecolor`/`linewidth` are supported; plural
forms error because Scanpy 1.11.5 overwrites them with defaults. Missing tiles
retain slots without painting; constant color bounds expand before mapping.
Hover identifies gene, group and the displayed mean/scaled mean/supplied value.

Evidence: [contract/semantic tests](../../tests/integrations/scanpy/test_matrixplot.py),
[thirteen frozen upstream chart cases](../../tests/integrations/scanpy/fixtures/matrixplot.json),
[original fixture](../../tests/integrations/scanpy/matrixplot_fixture.py),
[explicit generator](../../tests/integrations/scanpy/generate_matrixplot_references.py),
[registered tile/hover/offline checks](../../tests/integrations/scanpy/browser/test_matrixplot.py),
[shared complete-label/bracket checks](../../tests/integrations/scanpy/browser/test_dotplot.py)
and [packaged-PBMC workflow](notebooks/scanpy_expression.ipynb).
Reference metadata records DPI, palette, fonts, bounds, labels and provenance.
Browser captures and registered overlays live in the pytest output directory.

The [resource observation](../../tests/integrations/scanpy/fixtures/matrixplot-performance.json)
uses 100,000 cells × 20,000 sparse genes, reads only 40 selected columns and emits
2,000 tiles. Cold chart preparation took 3.28 s, validated JSON 0.35 s; payload
was 142 KB, tracked peak Python allocations 149 MB and process RSS 513 MB.
Chromium first paint took 1.55 s; observed hover response was 200 ms including
the one-pixel pointer probe, after the tooltip pause. Live JS heap was 12.6 MB.
These are local observations, not portable timing limits. The shared
[benchmark](../../tests/integrations/scanpy/benchmark_grouped.py) accepts either plot family.

Current boundaries: grouped backed/lazy/sparse-array restrictions remain;
dendrograms are M04, MatrixPlot/builder chains M13, broader normalization,
image exports and kwargs closure M14. M05.e adds navigation and fitted values;
summary selection remains deferred. This
preview does not close those full-family requirements. M03 has no separate
working plan to clear; retain PLAN, STATUS and reference evidence.

Validation (October 18): 286 integration checks passed, followed by the final 55
matrixplot/workflow checks after the kwargs decision. All 41 grouped browser
checks passed, including dotplot regressions, matrixplot hover in both
orientations, complete labels/brackets/guides, registered tiles and offline HTML.
Ruff formatting/lint and mypy pass. The expression notebook ran in a fresh
Jupyter kernel with three successful code cells and both plots visible.
The full documentation site, unrelated suites and unchanged UMAP browser tests
were not rerun for this slice.

## M04.a–d dendrogram and correlation preview

Runtime: [Scanpy delegation/results/permutations](../../src/genome_spy/integrations/scanpy/_dendrogram_data.py),
[native tree rules](../../src/genome_spy/integrations/scanpy/_dendrogram_chart.py),
[correlation tiles](../../src/genome_spy/integrations/scanpy/_correlation_chart.py)
and [public entry points](../../src/genome_spy/integrations/scanpy/pl.py).
Dotplot and matrixplot use one leaf and matching marker-block permutation.
Native formula transforms project
stored branch coordinates into the same index slots at the current plot size.
No local Core patch, upstream plotting call or prototype import is involved.

Missing trees delegate to public `sc.tl.dendrogram(..., inplace=False)`, which
owns means, correlations, linkage and leaf geometry. A small representation
guard prevents hidden PCA and expression densification. Automatic computation
uses resident dense X for small feature spaces or existing dense X_pca otherwise;
unsupported sparse/backed/lazy computation errors explicitly. Stored results
require no expression or representation access, including on sparse/backed data.
Their structure/group labels are checked, then correlations, linkage and geometry
are copied. Reordered categories are aligned by labels. No profiles, correlations
or geometry are recomputed to validate an existing tree. Users recompute Scanpy
trees explicitly after changing data or membership, as in Scanpy itself.
The notebook computes one tree from packaged PBMC PCA coordinates with a single
Scanpy call and reuses it in both expression plots.

Standalone trees support four orientations and label removal; correlation plots
support optional trees/numbers, native colors, numeric bounds and summary hover.
Grouped trees attach for more than two groups, matching Scanpy. M05.e adds optional grouped wheel
navigation with live leaf-to-row/column alignment; resizing remains supported.
Native fonts, palette interpolation and outer layout remain documented renderer
differences. The [user contract](../../docs/integrations/scanpy/index.md#dendrograms-and-correlation-matrices)
records exact options and boundaries.

Evidence:

- [Semantic/contract checks](../../tests/integrations/scanpy/test_dendrogram.py)
  include hand correlations, frozen Python results, ties, identical profiles,
  custom correlation/linkage, optimal ordering, multi-key groups, malformed
  results, immutability, views, stored results with sparse arrays/matrices/backed
  data and no-hidden-analysis guards. Delegation and cache tests prove that a
  missing tree calls Scanpy once and an existing tree performs no computation or
  X access. Both summary families cover supplied values and marker-block ordering.
- [Eight numerical and twelve complete chart references](../../tests/integrations/scanpy/fixtures/dendrogram.json)
  use [original MIT inputs](../../tests/integrations/scanpy/dendrogram_fixture.py)
  and an [explicit generator](../../tests/integrations/scanpy/generate_dendrogram_references.py).
  Metadata retains input/image hashes, versions, 100/150 display/export DPI,
  axes, labels and exact upstream branch paths. No real dataset or upstream code
  is copied into these fixtures.
- [25 browser checks](../../tests/integrations/scanpy/browser/test_dendrogram.py)
  cover all complete reference charts, registered branch painting, labels,
  correlation paint/numbers, post-reorder hover, swaps, resize, wheel stability
  and offline HTML. Full captures and registered overlays remain in pytest output.
- The [resource observation](../../tests/integrations/scanpy/fixtures/dendrogram-performance.json)
  uses 100,000 cells × 20,000 sparse genes, 40 selected genes, 50 groups and
  20 existing PCA components. Only the selected 100,000 × 40 table densifies.
  The chart carries 2,000 tiles plus the tree in 155 KB JSON. Cold preparation
  took 3.10 s, validated serialization 0.32 s, peak tracked Python allocations
  149 MB and process RSS 524 MB. Chromium first paint took 1.33 s, observed hover
  195 ms after the tooltip pause (including a one-pixel probe), and live JS heap
  13.2 MB. These are single-machine observations after the Scanpy delegation
  update, not portable timing limits.

Validation (October 18): all 335 integration checks and 66 grouped/tree browser
checks pass. Ruff formatting/lint and mypy pass. The expression notebook ran in
a fresh live Jupyter kernel, saved three successful code cells, and both attached
trees were inspected. The full documentation site, unrelated suites and unchanged
UMAP browser checks were not rerun.

Spacing correction (October 18): attached leaves now meet the matrix boundary.
Removed the fixed gap and distance-axis padding from shared tree overlays;
standalone tree domains are unchanged. Guide and outer padding follow the
smaller occupied region. Browser checks require leaf endpoints at the plot edge
and group centers in both orientations and sizes. All 25 tree browser checks and
53 tree/workflow checks pass, as do Ruff formatting/lint. The expression notebook
was restarted, rerun and inspected. Resource measurements and unrelated suites
were not repeated for this layout adjustment.

Computation simplification (October 18): removed the independent profile,
correlation and linkage path and computation-based cache checks. Public Scanpy
owns every new tree. Stored component subsets and custom methods are honored
without attempting to reconstruct their source from incomplete metadata.
Automatic sparse/backed computation is now an explicit upstream input boundary;
precomputed results remain supported without data reads or densification.
All 333 integration checks (including 49 tree checks and both workflow tests)
and 25 tree browser checks pass. Ruff formatting/lint and mypy pass. The sparse
100,000-cell resource observation above was repeated with public Scanpy
computation. Chart construction and notebook source remain unchanged. The full
documentation site, unrelated suites and unchanged UMAP browser tests were not
rerun; the open live notebook kernel was not restarted for this refactor.

Remaining work: M14 owns normalization/kwargs, typography and export closure.
M05/M08/M09 own attachment
to their new families; M13 owns builder methods. M04 closes only this stated
preview. No working document is newly eligible for clearance.

## M05.a/b cell heatmap preview

Retained evidence for the original preview below predates native surround tracks
and group gaps. [M14.b.1](#m14b1-native-heatmap-tracks-and-gaps) verifies that migration; its
centered group labels/tree leaves deliberately replace the old half-row placement.

Runtime: [public heatmap](../../src/genome_spy/integrations/scanpy/pl.py),
[shared data preparation](../../src/genome_spy/integrations/scanpy/_grouped_data.py)
and [native chart](../../src/genome_spy/integrations/scanpy/_heatmap_chart.py).
Reuses the public Scanpy getter, source/storage validation, min–max operation,
palettes, marker-block permutations, labels/brackets and M04 rule branches.
No separate data module, dependency, upstream plotting or Core patch was added.

One explicit observation permutation carries cell values and stable original-row
IDs into category strips, boundaries and unequal tree spans. Scaling happens on
individual cells, before sorting, with log1p first. Both orientations retain
repeated gene positions. Ordinary marker annotations are brackets; swapped ones
are a colored strip, matching Scanpy. Gene labels default off above 50 slots.
Stored trees require no recomputation; missing trees use the existing guarded
public Scanpy path. Heatmap attaches two-group trees, unlike dot/matrix summaries.
The native projection preserves Scanpy's half-row strip-label/leaf placement.

Evidence:

- [Semantic/API tests](../../tests/integrations/scanpy/test_heatmap.py) include hand
  scaling, a single getter call, raw/layer/symbol access, original cell IDs,
  repeated genes, sparse views/selected-only densification, unchanged analysis
  and data, missing/unused categories, two-group trees and explicit option errors.
- [16 complete Scanpy figures and manifest](../../tests/integrations/scanpy/fixtures/heatmap.json)
  use original MIT inputs with unequal groups and distinct values within groups.
  The [explicit generator](../../tests/integrations/scanpy/generate_heatmap_references.py)
  retains hashes, versions, 100/150 display/export DPI, values, label slots,
  group ticks and exact branch paths. No real dataset or upstream source is copied.
- [18 heatmap browser checks](../../tests/integrations/scanpy/browser/test_heatmap.py)
  register tiles and branches, retain full captures/overlays, and observe original
  cell hover after tree ordering, both orientations, resizing, wheel stability
  and offline HTML. Palette paint tolerance is 12/255 RGB for native bins and
  browser rasterization; typography and outer layout remain documented differences.
- The [resource observation](../../tests/integrations/scanpy/fixtures/heatmap-performance.json)
  tests 5,000 cells × 50 markers from 20,000 sparse genes: only the requested
  5,000 × 50 values densify. Preparation took 3.23 s, validated JSON 2.65 s,
  tracked Python allocations peaked at 114 MB and process RSS at 675 MB. The
  250,000 tiles serialize to 26.2 MB; Chromium first paint including dispatch
  took 16.2 s, observed hover 96 ms after the pointer pause, and JS heap 168 MB.
  These are local observations. Requests above 250,000 cell–gene values error
  before extraction; the 100,000 × 50 test proves no expression read occurs.

The expression notebook ran all four code cells in a fresh live Jupyter kernel,
saved successful outputs and was inspected. It uses all 700 packaged PBMC cells,
the existing marker dictionary and the explicitly computed shared Scanpy tree.
The [maintained contract](../../docs/integrations/scanpy/index.md#heatmap-compatibility)
records palette, missing-group, storage, normalization and size limits.
Validation: the 418-check integration suite and all 104 browser checks passed.
The final 44-check heatmap rerun also covers scaling before a tree's marker subset
and gene-only ticks, bringing distinct integration checks to 421. All 18 heatmap
browser checks were repeated after final guide/tick placement. The shared scaling
helper is now named scale_values to reflect its cell and summary callers; the
data/reuse regression checks pass too. Ruff formatting/lint and mypy pass.
The full documentation site and unrelated test suites were not rebuilt.
This checkpoint covered heatmaps; later matrix/clustermap evidence is separate. No working
plan is newly eligible for clearance; unrelated notebook edits remain unstaged.

## Computation reuse audit

October 18: traced UMAP, dotplot and matrixplot through their data, statistic,
color and chart modules against Scanpy 1.11.5's getters, aggregation, preprocessing
and plotting source. No further safe public-method replacements were found.
Grouped data already uses `sc.get.obs_df` once for unique selected keys and
AnnData categorization on its detached table. UMAP already uses public AnnData
vectors, existing embedding coordinates, the shared projection helper and public
Scanpy palette lists. It never computes embeddings.

The [maintained reuse contract](../../docs/integrations/scanpy/index.md#reusing-scanpy-computations)
records deliberate limits: get.aggregate's NaN propagation/nonzero counts differ
from plotting means/strict-cutoff fractions; pp.scale's z-scores differ from plot
min–max scaling. Grouped plots share the same small pandas/NumPy operations as
Scanpy's documented getter/grouping recipe. Upstream plot constructors use a
private preparer that sanitizes AnnData; MatrixPlot's defaults also read
Matplotlib rcParams. They are not standalone public preparation APIs.

[Nine reuse checks](../../tests/integrations/scanpy/test_upstream_reuse.py) assert
that public getters are called once and their returned values reach both plot
families/UMAP panels, with correct source choices and unchanged coordinates.
Executable counterexamples retain the aggregation/scaling differences above.
Existing sparse, mutation, raw/symbol, threshold, normalization-order and frozen
reference checks remain the numerical oracles. Runtime changes are four brief
comments explaining the retained boundaries; no algorithms or charts changed.

All 238 targeted data/plot/reference tests, Ruff formatting/lint and mypy pass. Browser,
performance and live notebook runs were not repeated for this audit because
runtime behavior is unchanged. No working plan is eligible
for clearance and existing notebook edits/outputs remain outside this change.

## Internal helper reuse audit

October 18: traced current callers across all five plotting previews. Dotplot and
matrixplot already share expression access, statistics, feature slots, labels,
brackets, guides and attached trees. Consolidated the remaining repeated rules:

- [_data.py](../../src/genome_spy/integrations/scanpy/_data.py) owns scalar and
  numeric-table validation alongside source/storage checks. Selected expression
  and supplied summary tables share validation without replacing their labels.
- [_style.py](../../src/genome_spy/integrations/scanpy/_style.py) owns native colors,
  continuous bounds, fonts and point units. It combines the three former color
  and UMAP style modules; its shared rules serve every current chart family.
- [pl.py](../../src/genome_spy/integrations/scanpy/pl.py) shares kwargs checking,
  optional dependency setup, display and save handling. Signatures and
  family-specific validation remain explicit.
- Tree rendering no longer imports the grouped chart just for fonts and number
  validation, removing that circular chart dependency. Each family retains its
  own native chart construction.

The package has 15 modules, down from 17, with no new public API, dependency or
adapter framework. The [source map](README.md#scanpy-integration-workspace) records
each owner. UMAP/grouped lookup and dotplot/matrixplot scaling remain separate
where Scanpy semantics differ. Heatmaps can reuse selected data, feature slots
and branches but still need observation permutations and unequal group centers;
the current equal-slot projection is not a complete heatmap layout.

Validation: all **371 integration checks** (including both workflows), **86 browser
checks**, Ruff formatting/lint and mypy pass. Common display/save checks now cover
all five families together. Before/after comparisons of 44 complete serialized
charts retain every value except a custom matrixplot stroke width rounded by
4.4e-16 logical pixels after sharing the point-unit constant. No data or visual
behavior change was observed. Resource measurements, the full documentation site
and unrelated tests were not repeated; the live notebooks and existing notebook
edits were untouched. No working plan is newly eligible for
clearance.

Readability pass (October 18): short, plain-language comments now separate option
checks, selected-data access, summary calculations, ordering and chart assembly.
They explain choices such as stable cell IDs, repeated genes, scaling order and
tree alignment. Nested choices for legend columns, bracket rotation, plot spacing,
palette defaults and display handling use ordinary statements; supplied matrix
means return early instead of enclosing the computed-means path in an else block.
No helper, module, dependency or public option was added.
All 371 integration tests, Ruff formatting/lint and mypy pass; 44 complete chart
specifications are unchanged. Browser checks, resource benchmarks and the full
documentation site were not rerun for this behavior-preserving edit. Notebook
edits remain outside the change. No plan is newly clearable.

Helper docstrings (October 18): all 71 internal plotting helpers now have concise
descriptions of their purpose, inputs and result, with reasons for non-obvious
choices. The longest is 34 words; public API documentation is unchanged.
Syntax-tree comparison confirms only docstrings changed. All 66 contract tests,
Ruff formatting/lint and mypy pass. Broader tests, browser checks, benchmarks and
the documentation build were not repeated for this documentation-only change.
Notebook edits remain untouched; M05 and plan clearance are unchanged.

## M05.b — supplied matrices and heatmap navigation

The `matrix` preview displays a supplied numeric matrix directly. It keeps
Scanpy's names/defaults except omitted Matplotlib `ax`, adding native hover and
pixel dimensions. Resident numeric arrays, masked arrays, nested sequences and
DataFrames retain value/row/column order; explicit repeated labels keep distinct
index slots. Reuse is confined to existing numeric validation, color bounds,
index encodings, text and style helpers; no new data module or analysis is added.
See the [matrix contract](../../docs/integrations/scanpy/index.md#supplied-matrix-compatibility)
for source, tick-count, color and layout limits.

Heatmap `zoom=True` enables native y-only wheel zoom and drag panning;
`zoom="xy"` enables both axes. Shared live
scale values project category strips, boundaries and unequal tree leaves.
Offscreen gene/category labels disappear; branches and strips stop at the plot
extent. Gene brackets are hidden unless their entire span is visible. Zoom
defaults False, retaining the existing appearance and fixed navigation. No Core
patch, Matplotlib runtime code or notebook interaction glue was added.

Retained evidence:

- [Matrix semantics/defaults/errors](../../tests/integrations/scanpy/test_matrix.py),
  [original matrix cases](../../tests/integrations/scanpy/matrix_fixture.py),
  [frozen references](../../tests/integrations/scanpy/fixtures/matrix.json) and
  [browser checks](../../tests/integrations/scanpy/browser/test_matrix.py): eight
  complete Scanpy charts and registered tile crops, missing/masked paint,
  normalization, repeated labels, titles, axis labels, actual guide length,
  hover after resizing and offline HTML.
- [Heatmap browser checks](../../tests/integrations/scanpy/browser/test_heatmap.py):
  twenty checks including all sixteen frozen chart cases, default fixed scales,
  zoom/pan in both orientations, visible tree/label alignment and annotation clipping.
- [Expression notebook](notebooks/scanpy_expression.ipynb) enables heatmap zoom
  and adds a supplied matrix of Scanpy's stored group correlations. All five
  code cells ran in a fresh live Jupyter kernel and their outputs were saved;
  [workflow tests](../../tests/integrations/scanpy/test_notebooks.py) verify
  unchanged supplied matrix values alongside the three expression charts.
- [Matrix resource observation](../../tests/integrations/scanpy/fixtures/matrix-performance.json):
  a resident 200 × 1,000 float32 matrix retains all 200,000 tiles. Warm preparation
  took 0.14 s, default formatted/validated JSON with allocation tracing took 12.0 s and occupied 28.1 MB;
  peak tracked allocation including JSON serialization was 344 MB. Browser first
  paint including dispatch took 10.3 s, observed hover after a pointer pause
  113 ms and JS heap 177 MB. These are local observations, not portable limits.
  Matrix transport is linear in supplied values; larger/chunked transport remains M05.d.

Validation: the full integration suite passed 455 checks, then all 75 matrix,
heatmap and workflow checks passed after the final changes, including an added
invalid-zoom case (456 distinct integration checks covered). All 20 heatmap and
9 matrix browser checks passed across the targeted runs. Ruff formatting/lint
and mypy pass. The full docs site, unrelated tests and other browser families
were not rebuilt/rerun for this slice.

M05.a/b previews are verified within their stated budgets; later clustermap and
transport work have separate records. Clearance: **retain** the live plan/status
and unique reference/resource evidence; the full family remains open.

Layout follow-up (`fa8d46b`): supplied matrices reserve long-label space once,
including with axis titles. All 15 matrix browser and 30 matrix/workflow checks
passed, plus Ruff/mypy. At that checkpoint, the expression notebook's five cells
and four charts were rerun and inspected. No clearance changed.

## M05.c — clustermap preview

Runtime: [bounded preparation](../../src/genome_spy/integrations/scanpy/_clustermap_data.py)
and [chart composition](../../src/genome_spy/integrations/scanpy/_clustermap_chart.py).
The public function keeps Scanpy 1.11.5's signature and accepts an explicit
subset of its forwarded Seaborn options. Public SciPy `linkage` and
`dendrogram(no_plot=True)` reproduce the actual row/column computations;
`sc.tl.dendrogram` computes group profiles and is not equivalent here.
Supplied linkage is validated and retained without recomputation.

Shared code owns source checks, numeric validation, CSS palettes, index slots,
labels, numeric tile records/tooltips and branch rendering. `TreeData` contains
only order/geometry, so individual-cell trees do not allocate an unused square
correlation matrix. Existing group trees retain their stored correlation data.
The native chart has left/top trees, optional multi-track annotation strips,
right/bottom ticks and hover. Track titles reserve their own outside space.
An `obs_keys` strip retains its categorical values and saved palette/order to
generate a native legend alongside the expression colorbar. Plain CSS tracks
have no category names and do not generate a legend.

The [maintained contract](../../docs/integrations/scanpy/index.md#clustermap-compatibility)
records scaling, masks, duplicates, raw vocabulary, kwargs and layout boundaries.
Native magma and a right color guide replace Seaborn's rocket/inset defaults;
explicit viridis references isolate those differences. Shared grid navigation and
fitted values are now opt-in; both trees, strips and ticks follow live index slots.
No Core patch, Seaborn runtime, analysis rerun or
AnnData mutation is introduced.

Evidence:

- [Semantic/API tests](../../tests/integrations/scanpy/test_clustermap.py)
  check hand-calculated sample z-scores/closest leaves, supplied linkage,
  display-only masks, source precedence, views/sparse/backed storage, duplicate
  labels, annotation reindexing, snapshots and resource errors.
  Both limits reject before expression reads: 250,000 requested values and
  1,000,000 pairwise distances per automatically clustered axis.
  A 1,000 × 20,000 sparse view densifies only its three supplied columns,
  with a 16 MiB peak-allocation assertion. Supplying linkage bypasses the
  distance computation but never the tile guard.
- [Seven frozen references](../../tests/integrations/scanpy/fixtures/clustermap.json),
  [original MIT inputs](../../tests/integrations/scanpy/clustermap_fixture.py) and
  [explicit generator](../../tests/integrations/scanpy/generate_clustermap_references.py)
  retain source/image hashes, Scanpy 1.11.5/Seaborn 0.13.2/SciPy versions,
  values, masks, leaf/branch order, labels and 100/150 display/export DPI.
  PNGs remain temporary/ignored.
- [Browser checks](../../tests/integrations/scanpy/browser/test_clustermap.py)
  register tile colors and exact exported branch endpoints with the reference
  plot area at DPR 1.5, retain complete captures/overlays, and verify annotation
  identity on both axes, long-title bounds, resize hover and offline HTML.
  Palette interiors allow 12/255 RGB; SVG coordinates allow 0.6 logical pixel.
  Raster branch checks establish visibility of subpixel 0.5-point strokes.
- The [expression notebook](notebooks/scanpy_expression.ipynb) uses all 700
  packaged PBMC cells and the same ten raw-snapshot markers. Its six code cells
  were rerun in the existing Jupyter session. Local matrix zoom experiments
  remain intact; the canonical workflow is validated separately.
- [Resource metadata](../../tests/integrations/scanpy/fixtures/clustermap-performance.json)
  and [reproducer](../../tests/integrations/scanpy/benchmark_clustermap.py)
  cover 700 PBMC cells × 40 genes (28,000 tiles; 244,650 row distances).
  Warm preparation took 0.14 s and formatted/validated JSON 3.22 s under
  allocation tracing. Peak Python allocation was 52.6 MiB; JSON 4.45 MB.
  Chromium 156 rendered in 2.89 s, used 44.7 MB JS heap, and hover responded
  in 32 ms after the pointer pause. These are local observations, not timing limits.

Validation: **525 Python semantic/API checks**, the canonical workflow assertions,
**10 clustermap browser checks**, and **63 existing matrix/tree/grid browser
checks** passed across the targeted runs. One existing ruler assertion flaked
while concurrent browser jobs were running; all four ruler cases passed on the
isolated rerun, without code changes. Ruff formatting/lint and mypy pass.
The notebook's existing local `zoom=False` experiments differ from the canonical
workflow's `zoom=True` assertions; canonical cells were checked in a temporary
copy, while the live notebook retained those experiments and rendered five charts.
The full unrelated repository suites and documentation build were not rerun.
At that checkpoint M05 remained open for M05.d transport, M05.f strip hover
and M14 option closure. M05.f is now closed by the native track deliveries above.
No plan is eligible for clearance.

Navigation follow-up (2026-10-19): clustermap reuses the shared `zoom` and
`show_values` helpers. `zoom=True` keeps x fixed; `zoom="xy"` navigates both axes.
Both trees and annotation tracks follow the same live slots, clip at viewport
boundaries, and retain label/color identity while panning. Automatic ticks reveal
more names as slots grow. Measurement records, masks, color limits and default
appearance are unchanged; fitted text shares the tile source and preserves hover.
Verification passed **530 semantic/API tests**, **38 clustermap/shared-grid browser
tests**, both canonical workflow checks, Ruff and mypy. Browser evidence includes
initial pixels, y locking, both-axis tree/strip alignment, dense fitted values,
tooltip access and offline rendering. All six expression notebook cells ran in
the existing Jupyter session; close zoom and panning were observed on the 700-cell
example. Local zoom experiments in other cells remain intact. No Core patch or
new clustering/data access runs during interaction. The unrelated full repository
suite and documentation build were not rerun. No plans were cleared.

Native legend follow-up (2026-10-19): the observation strip's own ordinal color
encoding generates its legend through `gs.Legend`; no custom legend marks or
legend-only datasets are added. The complete category domain stays visible while
zooming, including unused categories and categories sharing a color. Missing
annotations leave white space and do not become legend entries. **67 focused
semantic/API checks** and **15 clustermap browser checks** passed, including native
symbol colors/order/bounds, missing annotation paint, existing registered tiles,
trees and navigation. The expression notebook was rerun with the native
`bulk_labels` legend. Ruff and mypy pass; unrelated suites and docs build were not
rerun. Existing local notebook experiments remain intact; no plan cleared.

## Generated test images — October 19

Removed all 138 generated test PNGs from the tracked tree. The repository
instructions prohibit committing or pushing test images, including references,
screenshots and overlays; Git ignore and a rejecting commit hook enforce PNG
additions. Text metadata, source fixtures and generators remain tracked.

Browser fixtures now regenerate each family's Scanpy images once per test run
under pytest's temporary directory. Generated metadata stays there too; frozen
JSON baselines are never refreshed by the tests. Explicit reference-refresh
commands put PNGs under ignored `tmp/scanpy-references/<family>/` while updating
tracked metadata. Existing historical image-validation records refer to these
reproducible exports, not PNGs that need to ship in a clone.

This initial tree cleanup left old PNG blobs in local history. The later,
explicitly authorized history cleanup removed them before publication; see the
opening status note. Outgoing history is checked again at each handoff.

Validation: all 66 affected visual comparisons passed with no PNGs in `tests/`,
as did the three reference-metadata checks. The tracked JSON checksums remained
unchanged. The commit hook rejected a test PNG as expected, and ignore rules,
Ruff formatting/lint and mypy passed. Runtime code and notebook sources were not
changed; unrelated tests and the full documentation build were not rerun.

## M11.a supplied time-series heatmaps

The resident-profile preview is closed on 2026-10-22. Its
[public contract](../../docs/integrations/scanpy/index.md#supplied-time-series-heatmaps)
keeps Scanpy 1.11.5's `X`, `var_names`, `highlights_x` and `color_map` defaults,
adding native delivery, dimensions, hover, zoom and fitted values.
It never orders samples or runs analysis. The expression workflow explicitly
reads ten PBMC marker genes with `sc.get.obs_df` and stably sorts by the stored
S-phase score; this ordering is not measured time or inferred pseudotime.

Reuse: `_data.matrix_array` checks resident shape without densifying other
sources; `_matrix_chart` transposes profiles and uses its existing numeric
validation, color bounds, tile table, side labels and guide. Shared grid helpers
provide y-only/xy zoom and fitted values. Native quantitative bounds preserve
center cropping, first-variable-at-bottom order and singleton limits that index
bands cannot express. Four native formula transforms supply field-based cell
edges for x zoom; the tiles and text share one source and calculations. Highlights
are ordinary native dashed rules. No new production module, dependency, browser
listener, Matplotlib call or Core patch was added.

Validation: 340 targeted Python/workflow checks and 75 browser checks passed.
[Semantic tests](../../tests/integrations/scanpy/test_timeseries_heatmap.py) compare
the pinned values/limits independently, cover duplicate/2D/default labels,
missing/masked values, read-only views and early lazy/sparse rejection.
[Browser tests](../../tests/integrations/scanpy/browser/test_timeseries_heatmap.py)
register four complete shapes (including both singleton axes) at 100 display /
150 export DPI, checking tile paint, variable labels, numeric sample ticks,
clipped highlight geometry/dashes and the native color guide. They observe hover,
both zoom modes, pan, label/value alignment and offline HTML. Existing matrix,
clustermap and shared-grid browser regressions passed. The 20-cell canonical
expression workflow passed and ran in Jupyter; Ruff formatting/lint and mypy passed.
Test images/overlays and notebook outputs remain temporary or local, outside Git.

DataFrame review follow-up (2026-10-22): normalize pandas columns through the
existing `numeric_values` helper before transposing. Nullable Int64/Float64,
mixed boolean/float columns and missing entries now retain their numeric values;
strings, complex values and infinities still reject. Regression checks verify
transposed values, labels and unchanged inputs. All 68 focused time-series/matrix
tests, Ruff formatting/lint and mypy passed, including the masked-array checks.
Browser, notebook and resource checks were not rerun: chart construction and the
NumPy path are unchanged, so their earlier evidence remains applicable.

Resource observation: warm the import/schema path, then supply
`np.random.default_rng(0).normal(size=(20000, 10)).astype("float32")`, ten gene
labels, a midpoint highlight, xy zoom and fitted values at 700 × 280 pixels.
With allocation tracing enabled, preparation took 0.90 s, Arrow transport 0.96 s
(8.49 MB), and validated compact JSON 16.95 s (16.32 MB); tracked peak allocation
including both transports was 176 MB. Loading native inline HTML painted in
3.57 s; a paused hover appeared in 11 ms. Zoom changed the x domain within a
1.42 s observation including a 700 ms wait. Browser heap after collection was
127 MB, with no page errors. This is one local observation, not a portable timing
limit; compressed columns share screen pixels at the overview.

Remaining limits: native font/tick/colorbar layout and palette sampling differ
from Matplotlib, and native dash lengths round to whole pixels. The pinned
helper discards masks during array conversion, so explicit NaNs hide values;
ordinary `matrix` retains its own masked-array behavior. Sparse/lazy sources,
complex/infinite/all-missing inputs and color objects error. Broader storage,
typography and exports remain M14; larger/chunked transport remains M05.d.
The point/subplot increments are recorded below; simulation, DPT and PAGA keep
M11 open. The live plan and
ledger remain **retain**; no research plan is cleared by this increment.

## M11.a supplied time-series points

The resident-profile `timeseries` preview is closed on 2026-10-22. The pinned
public helper delegates to `timeseries_subplot`, which uses **scatter points**,
not connecting lines. This corrects the earlier connected-path assumption; C04
is not a dependency of these two helpers. The
[public contract](../../docs/integrations/scanpy/index.md#supplied-time-series-points)
preserves `X, **kwargs` and the forwarded defaults while adding native delivery,
dimensions, hover and both-axis navigation. No time ordering or analysis runs.

Reuse: [pure profile preparation](../../src/genome_spy/integrations/scanpy/_timeseries_data.py)
uses existing resident/numeric validation, coordinate margins, CSS colors and
continuous bounds. The [chart module](../../src/genome_spy/integrations/scanpy/_timeseries_chart.py)
uses the shared marker widths, point units, schemes and zoom helper. Dashed
vertical rules now have one shared native helper, also used by the heatmap.
The default palette comes from public `sc.pl.palettes.vega_10`; no private
Scanpy computation, artist recovery, runtime Matplotlib call, dependency,
custom geometry, browser listener or Core patch was added.

Validation: **319 targeted Python/contract/workflow tests** and **18 browser
tests** passed; the missing-first-point legend assertion also passed separately.
[Semantic tests](../../tests/integrations/scanpy/test_timeseries.py) compare public
Scanpy outputs for eleven fixtures: multiple variables, categorical and continuous
colors, integer-first mixed numeric groups, unsorted/repeated times, masks, constant colors, singleton
samples, inverted limits, highlights and explicit ticks. They check paint order,
domains, colors, unchanged inputs and default signatures separately from charts.
[Browser tests](../../tests/integrations/scanpy/browser/test_timeseries.py) register
complete charts at 100 display / 150 export DPI, including point centers/areas,
native labels and guides. The first masked continuous point keeps a transparent
series key, matching upstream. No gradient colorbar is invented. Separate checks
observe source-position hover, both-axis zoom, panning and offline HTML. The
shared heatmap highlight/browser regressions pass unchanged.

The canonical expression workflow now has 21 code cells and adds three existing
PBMC markers against stored S-phase scores. It passes independently and ran in
Jupyter without errors. The chart preserves all 2,100 points and supplied score
positions; this is not measured time. Ruff formatting/lint and mypy pass. Test
images/overlays, browser exports and executed notebook state remain outside Git.
The full test suite and documentation build were not rerun.

Resource observation: warm imports/schema, then supply
`np.random.default_rng(0).lognormal(0, .4, size=(50000, 3)).astype("float32")`,
three labels, `time=np.arange(50000)`, highlight 25,000, zoom and a 600 × 300-pixel
area. With allocation tracing, preparation took 0.26 s, Arrow transport 0.74 s
(5.55 MB), and validated compact JSON 8.31 s (13.15 MB); tracked Python peak was
126 MB including both transports. Native inline HTML painted in 1.09 s; a paused
hover appeared in 51 ms and reported the correct source value. Zoom changed its
domain within a 0.74 s observation including a 700 ms wait. Browser heap after
collection was 29.4 MB, with no page errors. These are local observations,
not portable timing limits; JSON serialization remains a material cost.

Remaining limits: bottom legend placement, native fonts/ticks and palette
sampling follow GenomeSpy. Sparse/lazy data, repeated labels, differing per-subset
marker shapes and global figure styling remain explicit M14 restrictions. The
single-variable path requires `color` rather than exposing upstream's missing
color failure. The subplot entry is delivered below; simulation, DPT and
PAGA remain M11. The live plan and ledger remain **retain**; no document is cleared.

## M11.a native time-series subplots

The `timeseries_subplot` preview is closed on 2026-10-22. Its
[contract](../../docs/integrations/scanpy/index.md#compose-time-series-subplots)
preserves the pinned helper's explicit argument names/defaults, omitting `ax`
and adding the shared native show/save, hover, zoom and dimensions. The default
native plot area is 496 × 369.6 pixels. `show=False` returns a panel for native
`hconcat`/`vconcat`; the wrapper does not use a current figure or mutate axes.

Both entry points share one delivery helper, the same supplied-profile
preparation and the same native point renderer. Context is passed through the
existing helpers so unsupported options and invalid data name the requested
entry. There is no second preparation or chart module. The composition test
caught fixed `timeseries-x/y` names colliding across independent scales; the
shared renderer now leaves names unset and uses GenomeSpy's native view scopes.
The grid zoom helper still accepts names for existing callers. No generated
names, custom listeners, patched Core or extra interaction layer was introduced.

Both entries use the same eleven complete-chart reference cases, including
numeric/categorical subsets, missing values, guides, markers, highlights and
inverted limits. The browser suite observes hover/zoom/pan and offline HTML for
each entry; a separate two-panel check verifies different color modes, correct
source-value tooltips and unchanged sibling geometry while navigating one panel.
The shared heatmap browser regressions also pass. Signature/default tests use
public Scanpy 1.11.5; validation checks prove that unsupported axes/options and
numeric errors retain the caller's context.

The expression notebook now contains 22 code cells. The new example reuses GNLY
expression and stored S-phase positions for all 700 cells in two native panels,
colored by stored phase and G2M score. Scales and legends resolve independently.
All cells ran in Jupyter without errors; source-only notebook content is tracked.
No generated media, chart exports or widget state enters Git. **406 targeted
Python/contract/workflow checks and 31 browser checks passed**, including shared
grid/matrix Python regressions and heatmap browser regressions. Ruff formatting,
repository lint and mypy passed. The full suite and documentation build were not
rerun.

Resource observation: two 50,000-point panels use
`np.random.default_rng(0).lognormal(0, .4, size=50000).astype("float32")`, sample
positions, alternating A/B categories and a linear numeric color vector. Each
panel is 280 × 220 pixels, with independent scales/guides. Warm preparation took
0.30 s, Arrow transport 0.96 s (4.31 MB), and validated compact JSON 9.29 s
(10.33 MB); traced Python peak was 103 MB including both transports. Native inline
HTML painted in 1.91 s, a paused hover appeared in 8 ms and matched the source
sample/value, and collected browser heap was 24.6 MB, with no page errors.
These are local measurements, not portable limits; large JSON serialization
remains a material cost. Independent navigation is observed in the browser test.

Marker/storage/global-style restrictions remain shared with `timeseries` under
M14. The subplot preview is closed; the simulation entry is delivered below,
with DPT and PAGA keeping M11 open. The live plan and ledger remain **retain**; no plan is cleared.

## M11.a stored simulation plots

The bounded `sim` preview is closed on 2026-10-22. Its
[contract](../../docs/integrations/scanpy/index.md#plot-stored-simulation-realizations)
preserves Scanpy 1.11.5's signature/defaults and adds native hover, zoom, fitted
heatmap values and dimensions. The implementation lives in
[pl.py](../../src/genome_spy/integrations/scanpy/pl.py) and the existing
[_timeseries_data.py](../../src/genome_spy/integrations/scanpy/_timeseries_data.py),
with no new preparation or renderer module. It reads resident dense X and names,
chooses `tmax_realization`, then `uns['tmax_write']`, then `n_obs`, and preserves
all rows including partial final realizations. Correcting the earlier plan:
this argument marks run boundaries, never truncates X. The exact seed-1 legacy
permutation uses a local RandomState, preserving global RNG state. Shuffling
always delegates to points, including `as_heatmap=True`, as in the pinned helper.

Both existing renderers now accept named numeric ticks internally. Their shared
native text side track uses the x scale, native visible-range culling and ordinary
surround layout. Point frames are set on the plot view so the label track does
not inherit a rectangle. No custom event listeners, core patches, spec rewriting,
benchmark imports or Matplotlib rendering were added. Existing show/save and
optional dependency rules apply. Heatmap value labels and both families' hover,
wheel zoom, pan and offline HTML reuse their original paths.

[Semantic tests](../../tests/integrations/scanpy/test_sim.py) compare public
Scanpy values, axes, ticks, boundaries and permutations across seven cases:
points, heatmap, explicit override, fractional length, length beyond the data,
shuffle and shuffle-plus-heatmap. They also cover default fallback, read-only
views/input/RNG state, errors and pre-access backed/sparse guards.
[Browser checks](../../tests/integrations/scanpy/browser/test_sim.py) register
complete charts at 100 display/150 export DPI, verify guides and boundary positions,
and compare point footprints or heatmap paint. Point samples under dashed rules
are excluded from color comparison because native dash lengths round to whole
pixels; rule positions are checked separately. Text anchors allow one logical
pixel for native export/rasterization. Observed zoom/pan checks measure adjacent
point spacing despite native viewport culling, test fitted heatmap values and
check run labels against moving boundaries. The parent suites still cover the
same colors, shapes, masks, highlights, independent panels and cell crops.

**440 targeted Python/contract/workflow checks and 41 browser checks passed**,
including shared matrix/grid/time-series regressions. Ruff formatting, repository
lint and mypy passed. The canonical expression notebook has 24 code cells and
20 charts. It loads Scanpy's packaged Krumsiek11 simulation, selects five genes
from all 640 samples and shows four supplied 160-sample realizations as points
and a heatmap. All 24 cells ran in Jupyter with no errors; both outputs were
inspected. Its duplicate observation names are retained from Scanpy's dataset;
positions, not those names, identify time-series samples. No data is vendored.
Review cleanup: the notebook keeps the selected genes as a read-only AnnData
view, avoiding the second duplicate-name warning from an unnecessary copy. The
remaining dataset-loader warning is explained in the example; the workflow check
verifies the same values in both renderers.
Tracked notebook content excludes execution outputs/widget state; all browser
images, overlays, HTML exports and local measurement scripts stay outside Git.
The full test suite and documentation build were not rerun.

Resource observation: seed-0 `default_rng.lognormal(0, .4, size=(10000, 5))`,
float32, realization length 1000, 500 × 280-pixel plots. Each mode draws 50,000
points/tiles. Warm preparation took 0.07 s for points and 0.86 s for the heatmap;
Arrow transport took 0.80/0.81 s (1.85/1.85 MB). Validated JSON took 4.70/4.45 s
(4.27/3.75 MB); traced Python peaks were 42.0/40.8 MB. First paint took 1.28/1.11 s;
paused hover took 73/48 ms and matched the reported source positions/values.
Collected browser heaps were 14.9/37.8 MB with no page errors. These are local
observations, not portable limits; JSON cost remains the parent transport limit.

The preview rejects backed/lazy/sparse X before loading/densifying and inherits
parent point marker, palette and distinct-name limits. Default point colors cover
at most ten genes; heatmaps support single/repeated gene labels. Broader storage,
style and export stay M14. DPT increments are recorded below; the group-reference
gate and PAGA keep M11 open. The
live plan and ledger remain **retain**; no document is eligible for clearance.

## M11.b stored DPT groups and pseudotime

Implemented on 2026-10-22 through the existing
[_timeseries_data.py](../../src/genome_spy/integrations/scanpy/_timeseries_data.py)
and [public plotting module](../../src/genome_spy/integrations/scanpy/pl.py), with
no new production module or renderer. The
[contract](../../docs/integrations/scanpy/index.md#inspect-stored-dpt-groups-and-pseudotime)
preserves Scanpy's signature/defaults and adds native hover, independent x/y
zoom/pan and per-panel dimensions. Metadata-only access supports views and backed
AnnData without reading X, raw or layers. Plotting never computes neighbors,
diffusion coordinates or DPT.

Stored category codes retain their original order, including unused categories;
palette assignment follows sorted observed groups through the existing helper.
Both panels retain observation row positions and use the stored rank coordinates,
without sorting. The lower panel masks missing/infinite pseudotimes without
changing the source. Numeric values, marker shapes, colors, ticks, boundary rules
and native composition reuse the time-series helpers. Required fields, categorical
groups without missing labels and valid boundaries are checked explicitly;
stored order uses shared time-series coordinate validation, including global
ranks in filtered views. Unsupported marker/palette options retain parent limits.

**The direct parent-reference gate remains open.** Scanpy 1.11.5 with pandas
2.3.3 fails before drawing because its group-code Series is indexed as `X[:, None]`.
The [test fixture](../../tests/integrations/scanpy/dpt_fixture.py) invokes the same
two public `sc.pl.timeseries_subplot` calls with group codes converted to NumPy.
This provides a component reference for intended values and appearance, without
patching Scanpy or adding production fallback code. Recheck the parent entry
after an upstream fix before closing that gate.

**402 targeted Python/contract/workflow checks and 32 browser checks passed**,
including parent time-series/heatmap/simulation regressions. The
[semantic checks](../../tests/integrations/scanpy/test_dpt_groups.py) cover six
component-reference cases, metadata-only views/backed access, mutation guards,
missing analysis and invalid metadata/options. The
[browser checks](../../tests/integrations/scanpy/browser/test_dpt_groups.py) compare
registered point paint/footprints, axes and labels at 100 display/150 export DPI
and DPR 1.5. They observe source-position hover, independent wheel zoom/pan and
offline HTML delivery. Reference images, overlays, resource scripts and HTML
exports remain temporary. Ruff formatting/lint and mypy pass.

The canonical expression notebook now has 26 code cells and 21 native charts.
It reuses the full packaged Krumsiek11 simulation (640 observations, 11 genes),
explicitly computes ten-neighbor X distances, a seed-0 diffusion map and one DPT
branching, then plots the stored results. All 26 nonempty cells ran in Jupyter
without errors and the new output was inspected. The packaged loader's duplicate
observation-name warning is retained and explained. Committed notebook content
excludes execution outputs and widget state; existing local notebook edits remain.

Resource observation: 100,000 metadata-only observations, seed-0 permuted ranks,
three groups, pseudotime `rank / 99999`, two boundaries and two 500 × 180-pixel
point panels with native hover/zoom. A warmed local Python 3.11/macOS arm64/Core
1.2.0 run prepared in 0.244 s; Arrow took 0.957 s (8.57 MB), while validated JSON
took 14.53 s (19.26 MB). Peak traced Python allocation was 200.24 MB. Chromium
first paint took 2.22 s, collected JS heap was 37.99 MB and a paused hover verified
the source position/order/value in 0.48 s including five small pointer probes.
No browser errors occurred. These are local observations, not portable limits;
large JSON serialization retains the parent transport cost.

The DPT expression increment is recorded below. Broader style/storage/export
stay M14; the group-reference gate and PAGA keep M11 open. The full
repository suite and documentation build were not rerun. Clearance: **retain**;
no plan is eligible for removal.

Filtered-view follow-up: the metadata reader now passes stored order directly
to the existing time-series coordinate validation. The extra full-rank
permutation check is removed; filtered/reordered views retain global ranks and
saved boundaries without sorting, remapping or analysis. The regression first
failed on the old check, then passed through the existing semantic and registered
browser comparisons. Metadata-only guards now exercise that filtered view too.
**335 targeted Python/contract/workflow checks and eight DPT browser checks passed**;
Ruff formatting/lint and mypy pass. The notebook now explicitly analyzes all 640
Krumsiek11 samples and plots a read-only 320-sample view, preserving its saved
coordinates. All 26 nonempty cells ran in Jupyter without errors and the filtered
DPT output was inspected. Prior resource evidence is retained: preparation
downstream of the removed validation, native rendering and transport are unchanged. Resource
measurements, the full suite and documentation build were not rerun. The direct
parent-reference gate, next slice and clearance remain unchanged.

## M11.b stored DPT expression profiles

Closed for the resident dense-X preview on 2026-10-22. The
[public entry](../../src/genome_spy/integrations/scanpy/pl.py) and existing
[_timeseries_data.py](../../src/genome_spy/integrations/scanpy/_timeseries_data.py)
preserve Scanpy 1.11.5's signature/defaults, adding native hover, navigation,
fitted heatmap values and dimensions. No new production module is needed.
The [contract](../../docs/integrations/scanpy/index.md#plot-expression-in-stored-dpt-order)
uses X and var_names only, applies stored dpt_order_indices verbatim and retains
dpt_changepoints. Missing/stale metadata errors; no analysis, sorting, rank
reconstruction, smoothing or scaling runs. Gene-only views work; backed/lazy and
sparse X reject before loading or densification. NumPy row-index semantics,
including repeated/negative positions, are preserved without imposing a new
permutation rule. Raw/layers and other DPT fields are unused.

Heatmap mode reuses the transposed/cropped matrix path, native schemes/colorbar,
hover, zoom and fitted values. Point mode reuses existing variable colors,
markers, guides, hover and x/y navigation, retaining `[0, 1.3 * n_obs]` x limits.
Inactive color_map/marker options follow Scanpy's mode-specific behavior.
The shared heatmap renderer now accepts an axis title to supply "dpt order";
its previous default is unchanged. Native points/tiles/rules/layout suffice;
no Matplotlib runtime, custom event listener, Core patch or export rewriting is used.

**433 targeted Python/contract/workflow checks and 58 browser checks passed**;
Ruff formatting/lint and mypy pass. The
[semantic tests](../../tests/integrations/scanpy/test_dpt_timeseries.py) compare
seven cases directly with the public `sc.pl.dpt_timeseries` entry, including
both modes, a native scheme, inactive options, repeated indices and singleton
axes. They also guard X-only gene views, input mutation, missing analysis,
invalid indices, unsupported storage and early flag validation. Unlike the
separate group diagnostic, this direct parent-entry reference works.
[Registered browser checks](../../tests/integrations/scanpy/browser/test_dpt_timeseries.py)
compare complete labels/viewport sizes, boundary positions and sampled tile or
point paint/footprints at 100 display/150 export DPI and DPR 1.5. They observe
correct ordered-position hover, wheel zoom, panning, fitted values and offline
HTML. Parent heatmap/point/simulation/group suites pass the shared-renderer change.
The workflow assertion reads the shared tile dataset when value labels inherit
their data, rather than assuming each leaf mark owns a separate data source.

Both canonical workflow tests pass. The expression notebook now has 27 code
cells and 22 charts; all 27 nonempty cells ran in Jupyter without errors and the
new heatmap was inspected. It selects five genes in a fresh full-observation
Krumsiek11 view and reuses the existing explicit neighbors/diffmap/DPT analysis.
The earlier group diagnostic still demonstrates a filtered observation view.
The packaged loader's duplicate-name warning remains explained; no data is vendored.
Committed notebook source excludes outputs/widget state. Local outputs, screenshots,
overlays, exports and measurement scripts remain outside Git.

Resource observation: seed-0 float32 lognormal X with 10,000 observations × five
genes, a seed-0 saved row permutation, boundaries at 2,000/6,000 and 500 × 280-pixel
plots. Each mode retains 50,000 values. Warm point/heatmap preparation took
0.102/0.705 s; Arrow took 0.760/0.793 s (1.85/1.85 MB). Validated JSON took
3.26/4.45 s (4.27/3.74 MB); peak traced Python allocations were 42.01/39.95 MB.
Chromium first paint took 1.39/1.45 s; paused hover verified source values through
the saved indices in 0.47/0.46 s including five small pointer probes. Collected
browser heaps were 14.71/37.86 MB with no page errors. This local Python 3.11/macOS
arm64/Core 1.2.0 observation is not a portable limit; JSON remains the parent
transport cost.

Plan reconciliation: the current queue, milestone rows, callable/parameter
inventory and notebook counts agree. Old checkpoint forecasts for marker work,
QC, density and DPT now link delivered increments; M04 and the user guide describe
the released orthogonal-link renderer. Broader storage/style/export remain M14;
the group-reference gate and PAGA keep M11 open. The next audit is only in the
current queue. The full repository suite and documentation build were not rerun.
Clearance: **retain**; no live plan is eligible for removal.

## M11.c stored undirected PAGA graphs

`gsc.pl.paga` now renders stored undirected group connectivity with native rules,
points and text. [Data preparation](../../src/genome_spy/integrations/scanpy/_paga_data.py)
reads sparse graph copies, categorical metadata and stored group sizes. It reuses
public `sc.pl.paga(plot=False)` on metadata-only AnnData when positions are absent;
no private layout code, expression copy/access, Matplotlib figures, artist
recovery or PAGA analysis is involved. Supplied coordinates skip layout. None
recomputes layout even with cached positions, matching Scanpy. add_pos=True writes
successful coordinates only after chart preparation; plot=False creates no chart.

[Chart construction](../../src/genome_spy/integrations/scanpy/_paga_chart.py) reuses
shared numeric validation, palettes/CSS colors, coordinate domains, point units,
navigation and delivery. Size scales are independent between edge widths and node
areas, while coordinates are shared. Group nodes use group IDs/counts, without an
observation brush or generic graph framework. The Scanpy extra now includes
Scanpy's PAGA/igraph extra; base dependencies and lightweight imports are unchanged.

Initial verification in `b642cbc`: **413 targeted Python checks, two workflow tests and nine browser checks**
passed, along with Ruff formatting/lint and mypy. The full repository suite and
documentation build were not rerun. Retained reproduction:

- [Public reference/guard cases](../../tests/integrations/scanpy/test_paga.py) cover
  default, circle and seeded/initialized layouts; authoritative positions and cache
  flags; threshold ties, empty/asymmetric graphs; aliases, node areas and edge
  widths/order; labels, colors and bounds. Caller expression reads, analysis and
  figure creation are guarded. CSR/CSC/LIL inputs validate without densifying;
  missing/stale/nonfinite/self-loop graphs fail clearly.
- [Native browser checks](../../tests/integrations/scanpy/browser/test_paga.py) compare
  seven complete charts against Scanpy at display DPI 100, export DPI/DPR 150/1.5,
  including the asymmetric CSC regression added below.
  They register positions, dimensions, labels and colored point footprints, and
  retain overlays only in temporary directories. Node/edge hover, both-axis zoom,
  pan, ordinary native composition, offline HTML, zero-size nodes and disabled
  hover are observed. Native viewport culling can sort SVG output, so hover uses
  projected known group coordinates rather than assuming export row order.
- Both canonical workflow tests pass. The expression notebook has **29 code cells
  and 23 charts**, including explicit `sc.tl.paga(pbmc, groups="bulk_labels")` on
  packaged PBMC neighbors. Plotting never calls that analysis again. The local
  notebook's unrelated edits are preserved; the committed source has no outputs.
- A seeded metadata-only 100,000-observation / 100-group / 500-edge workload used
  the default Scanpy layout and native 700 by 450 chart. Warm preparation including
  layout took **0.031 s**, Arrow **0.750 s**, validated compact JSON **0.828 s**;
  payloads were **46,828 / 112,018 bytes** and peak traced Python allocation **3.19 MB**.
  Chromium first paint including dispatch took **1.67 s**; a known exposed group
  reported 1,000 cells, navigation changed the graph and no page errors occurred.
  Post-GC JS heap was **7.03 MB**. Reproduce using seed-0 upper-triangle selection
  of 500 edges among 100 groups, uniform weights 0.02–1 and 1,000 cells per group.
  These are local Python 3.11/Core 1.2.0 observations, not portable limits.

Native font metrics differ from Matplotlib, and native dashed rules use one fixed
pixel pattern rather than per-width dash lengths; M14 owns exact style parity.
The palette helper reads rather than writes color caches; mismatched cached
palette lengths error. Numeric/gene/degree colors, other categorical mixtures/pies,
multiple color panels, component filtering, directed transitions, file positions
and GEXF export remain M11.c, with explicit unsupported errors. The full M11
milestone and DPT's direct parent-reference gate remain open. C04 does not block
these straight native rule segments; other connected paths need separate audits.

Plan reconciliation updates the active queue, milestone, callable/parameter
inventory, source map, optional dependency and user guide together. There are now
35 partial plotting entries and 13 unimplemented plot/builder entries; availability
is not full-family compatibility. The current queue above owns next work.
Clearance: **retain**; no live plan is eligible for removal.

### PAGA sparse graph corrections

Review found that converting CSC to CSR changed which asymmetric edge weight
NetworkX retained, while LIL inputs reached Scanpy's layout path without a
compatible sparse format. The existing storage-format test supplied positions,
so it never exercised the failing LIL layout branch.

The shared `_graph` helper now returns the layout source and thresholded native
edge graph. A COO copy preserves stored edge order while filtering. Layout keeps
CSR/CSC input or uses SciPy to prepare other storage, including LIL; Scanpy's
public no-plot API still computes the layout and applies its own threshold. The
layout source stays unfiltered, preserving tree-layout behavior when the solid
edge key itself names the stored tree. Stored matrices remain unchanged. No
renderer, core code, analysis implementation or new abstraction is needed.

The regressions fail on the previous implementation and cover asymmetric CSC
widths against public Scanpy, automatic/supplied positions for CSR/CSC/LIL,
custom solid-edge keys, cache controls and source identity/format/values. Invalid
weights still fail clearly; expression access, analysis and figure creation stay
guarded. The native chart comparison now also includes asymmetric CSC edges.
The expression notebook explains this storage behavior while retaining the
packaged PBMC example. On 2026-10-23, **300 targeted Python checks, ten PAGA
browser checks and both workflow tests passed**, along with Ruff formatting/lint
and mypy. All 29 nonempty expression-notebook code cells ran in Jupyter without
errors, producing the same 23 charts. Rendering, transport and workload dimensions
are unchanged; the retained resource baseline above still covers those paths.
The full repository suite, docs build and resource benchmark were not rerun.
Scope, next work and clearance remain unchanged.

### PAGA numeric, gene and degree colors

Closed (2026-10-23) for single-key numeric observation, gene and solid/dashed degree
colors. [`_paga_data`](../../src/genome_spy/integrations/scanpy/_paga_data.py)
reuses the grouped public getter and group-mean helpers. Observation means skip
missing values; gene means retain Scanpy's missing-value propagation. Gene colors
use raw when present by default, otherwise X; False chooses X. Only one gene
column is materialized, and source data stay unchanged. Degrees use the existing
thresholded NetworkX graphs, preserving weights/order for CSR/CSC and the shared
LIL conversion. Weighted degrees normalize to 0–1; missing dashed graphs and
equal-degree normalization error explicitly instead of creating substitute values.

[`_paga_chart`](../../src/genome_spy/integrations/scanpy/_paga_chart.py) uses shared
color bounds and native fill/stroke scales and legends. Finite nodes keep the
existing size/position/edge mapping; missing means omit point paint, leaving
labels and edges intact. Hover adds the plotted numeric value. Public Scanpy
1.11.5 references verify its automatic observation/gene guide, absent degree
guide and suppression for explicit colorbar=True/False. Constant means use the
first palette color without a guide and the midpoint with one. Native guide
ticks/fonts/outer layout remain M14 differences.

Verification: **328 targeted Python checks**, **22 PAGA browser checks**, both
canonical workflow tests, Ruff formatting/lint and mypy pass. Tests cover raw/X
fallback, sparse CSR/CSC views and one-column densification, missing means,
constant colors, thresholded solid/dashed degrees, CSC edge order, aliases,
unchanged caches on error, and metadata/degree paths without expression reads,
figures or analysis. Complete registered charts compare colors, footprints,
labels, guide presence and edges at 100 display / 150 export DPI. Point positions
use independently projected stored coordinates through SVG's rounded viewport,
checked against public layout bounds within half a CSS pixel. Native value hover,
zoom/pan, composition, missing-node paint and offline HTML are observed. Generated
references and overlays stay in temporary directories.

The expression notebook adds S-score, raw GNLY and weighted-degree examples using
the same saved graph coordinates. Its live Jupyter run completed **32 code cells
and 26 charts with no errors**, preserving unrelated local notebook edits. The
committed notebook keeps source only, without outputs or widget state.

A seed-0 sparse workload uses 100,000 cells, 20,000 genes, 200,000 sampled nonzero
entries, 100 uniform groups, 500 symmetric edges with weights 0.02–1 and supplied
unit-circle coordinates. Warm observation/gene/degree preparation took
**0.019/0.023/0.013 s**, validated JSON **0.798/0.787/0.783 s**, and peak traced
Python allocation **2.67/2.66/1.88 MiB**. JSON was about **168–169 kB**. The native
700 × 450 gene graph rendered/dispatched in **1.80 s**, showed all 100 nodes and
reported the known 1,000-cell count plus numeric value on hover. JS heap at that
point was **19.55 MiB before explicit GC**. These are local observations, not
portable limits. Base graph layout/geometry and transport code are unchanged;
the earlier group-graph resource evidence remains applicable to those paths.

CSS names that also name genes/annotations, ambiguous getter names, direct numeric
vectors, all-missing colors, other categorical mixtures/pies and broader PAGA
options remain explicit limits. The current queue owns next work; M11 stays
open. The full repository suite and docs build were not rerun. Clearance:
**retain**; no live plan is eligible for removal.

### PAGA single-component filtering

Implemented (2026-10-23); semantic, explicitly subsetted reference, complete-chart,
interaction, workflow and resource checks are verified. The direct disconnected
parent-entry comparison remains blocked by **C15**, so this increment is not closed.

[`_paga_data`](../../src/genome_spy/integrations/scanpy/_paga_data.py) uses
NetworkX's connected components on the existing thresholded solid graph. Select
the most nodes, choosing the first component in original group order on ties.
The existing node table keeps original IDs, labels and coordinates; colors and
degrees are computed before filtering. Areas use the displayed count and median
group sizes. The existing edge table reads a graph subview, retaining original
edge/node IDs. Chart construction is unchanged. Layout and its position cache
retain every group; plot=False retains its existing behavior. When filtering is
needed, dashed_edges must be None, matching upstream's restriction. No expression
copy, analysis rerun, new chart layer or Core patch is introduced.

Scanpy 1.11.5 subsets colors/labels but keeps full coordinates, raising a shape
error on disconnected graphs. A strict expected-failure check asserts this exact
failure and will fail on a future upstream fix. Independent known component IDs
and public Scanpy on explicitly subsetted inputs validate the native intended
view; they do not substitute for the blocked direct parent gate.

Verification: **343 targeted Python checks passed, one expected upstream failure**;
**32 PAGA browser checks** and both canonical workflows passed. Ruff formatting,
full-repository lint and mypy pass. [Semantics](../../tests/integrations/scanpy/test_paga.py)
cover thresholding, isolated nodes, ties independent of cell counts, CSR/CSC/LIL,
supplied/computed positions, full caches and error/mutation guards.
[Browser checks](../../tests/integrations/scanpy/browser/test_paga.py) register
complete categorical/numeric/gene/degree charts against subsetted public references,
including footprints, labels and guides. They observe original-ID hover, edge
hover, zoom/pan, independent composition and offline HTML. Generated files remain
temporary. The live expression notebook completed **33 code cells and 27 charts
without Python errors**, including a visible eight-of-ten-node PBMC component at
threshold 0.2. Committed notebook source has no outputs or widget state; local
edits are preserved.

A seed-0 workload uses 100,000 observations, an unread empty 20,000-gene CSR matrix,
100 equally sized groups, 500 symmetric weighted edges in connected components
of 70 and 30 nodes, normal observation scores and supplied unit-circle positions.
Warm preparation took **0.016 s**, validated JSON **0.792 s**, and peak traced
allocation **2.67 MiB**. It emitted **70 nodes and 102,023 JSON bytes**, retaining
the full 100-by-2 cache. Rendering and transport use unchanged code with fewer
rows; the earlier 100-node/500-edge browser resource observation remains applicable
to those paths. These measurements are local observations, not portable limits.

C15 owns the direct parent-reference recheck; broader PAGA color/directed/export
options remain M11.c. The current queue owns independent next work. The full
repository suite and docs build were not rerun. Clearance: **retain**.

## M11.d PAGA comparison

Closed (2026-10-23) for the corrected bounded preview. The initial delivery in
a9f4d2b and its evidence are retained below. Review reopened palette parity,
independent composition and native coordinate ownership; the verified correction
record follows that initial evidence.

[`paga_compare`](../../src/genome_spy/integrations/scanpy/pl.py) composes the
existing embedding and PAGA entries. No new renderer, graph layout, analysis,
expression conversion or dependency is added. It preserves the pinned signature
and automatic basis priority, one selected component pair, group-median positions
when colored by the PAGA grouping, saved positions for other colors, explicit
positions, title/label precedence and add_pos. Native scale sharing uses only
the embedding's declared limits; graph fields inherit that resolution through
ordinary native encodings. Color/fill/stroke, size and guides stay independent.

[Semantic tests](../../tests/integrations/scanpy/test_paga_compare.py) compare the
public Scanpy call directly for positions/cache, limits, titles and colors,
including supplied and cached layouts and nondefault components. They cover
basis priority, labels, groups, invalid/missing data, add_pos=False, forbidden
analysis/upstream plotting and metadata-only operation with expression access
blocked. **281 comparison/contract checks passed**. The earlier shared-parent
run passed the embedding/PAGA checks. Both combined clean-source workflow tests
passed (35.41 s); the complete working notebook ran in Jupyter with **36 code cells,
30 charts and no Python errors**. The comparison uses explicit normal labels and
add_pos=False, preserving the earlier graph layout. Committed notebook source
contains no outputs or widget state; existing user edits/execution stay local.

All **three browser checks** passed at DPR 1.5, covering aligned complete panels,
labels, independent guides, clipped out-of-range supplied positions, known-cell
and group hover, shared wheel zoom/pan and offline HTML. Unchanged parent marks
reuse their retained point-footprint/paint reference evidence; the new tests
verify their composed coordinate projection and guide ownership. Generated
images, HTML and resource scripts/results remain temporary. Ruff and mypy pass.

A seed-0 resource observation used 100,000 observations, 100 equally sized groups,
100 symmetric ring edges of weight 0.5, and an unread empty 20,000-gene CSR matrix.
Coordinates are normal noise (sd 0.3) around a ten-by-ten grid with spacing three;
one exposed source cell verifies hover. Two 500-by-400 panels use normal on-data
labels, size=36, shared zoom and add_pos=False. With imports/fixture construction
excluded and allocation tracing enabled, preparation took **1.085 s**, Arrow
**1.619 s / 7.18 MB**, and validated JSON **13.777 s / 17.42 MB**. Peak traced
allocation was **135.93 MB** (peak process RSS **582.78 MB**, including imports).
Chromium first paint including dispatch took **12.264 s**, JS heap was **157 MB**,
and the paused known-ID hover completed in **0.794 s**. Wheel navigation changed
the shared domain; no browser errors occurred. These are local observations,
not portable performance limits; JSON validation/dispatch retains parent costs.

The pinned bold/on-data default remains explicitly unsupported with the bundled
regular font atlas; use legend_fontweight="normal" as in the example. Parent
storage/rendering restrictions, custom margins, multiple color/component pairs,
plot=False and broader graph options retain M11/M14 owners. The unstarted PAGA
path retains M11.d; adjacency stripplot delivery is recorded below. Full repository
tests and the docs build were not rerun. Clearance: **retain**.

### Comparison palette and composition corrections

Closed (2026-10-23). Group palettes now pass through PAGA's shared `_palette`
resolver via an explicit native `palette` addition. CSS sequences/mappings retain
Scanpy ordering and cycling; native schemes keep the existing ColorData model
and a full group-index domain through component filtering. Neither path reads or
rewrites the saved palette when a replacement is supplied. Numeric/gene/degree
colors keep their existing path and ignore this categorical option.

The embedding renderer no longer assigns fixed scale names. Native resolution
keeps linked panels together while separate comparisons remain independent.
Explicit names now appear only in validation specs that inspect native scale
getters. The PAGA renderer declares x/y once at its layer root, so marks inherit
coordinates; comparison uses ordinary encode to inherit embedding limits. There
is no private layer traversal, AnnData copy, palette sampling, new dependency,
custom geometry or browser handler in this correction.

Verification: **610 targeted Python checks passed, one existing upstream xfail**;
**134 browser checks passed** (94 embedding/scatter/PCA/density/outline, 36 existing
comparison/PAGA, four new rendered palette/component cases). The comparison
regressions first reproduced mismatched palette colors and the old duplicate-name
browser failure. They now verify public Scanpy CSS palette parity, native scheme
domains, stale-cache preservation, inherited graph authoring, and independent
pair zoom/pan/offline HTML. Parent browser checks retain registered geometry,
hover, brushing, navigation/reset, guides and offline delivery. Both clean-source
workflow tests passed (44.55 s). The live working notebook restarted and executed
**38 code cells / 32 charts with no Python errors**, including native tableau10
colors and the independently composed pairs. User-local edits/outputs remain;
committed notebook source excludes execution and widget state. Ruff and mypy pass.

The original 100,000-cell resource observation is retained for unchanged embedding
access, metadata-only PAGA preparation and transport. Coordinate ownership/name
changes add no data copy; palette preparation is bounded by the group count and
only adds group-index scheme metadata. Full-size timing was not repeated for
these correctness fixes. A 1,000-cell benchmark smoke check also passed all 16 known-ID hover probes
and navigation with explicitly named validation scales. All screenshots and
benchmark artifacts stay temporary.
The full repository suite and documentation build were not rerun. Parent scope,
normal on-data labels and the broader integration remain open as recorded above.
Clearance: **retain**.

## M11.d PAGA adjacency heatmaps

Closed (2026-10-23) for the bounded heatmap preview. The public entry preserves
Scanpy 1.11.5's signature/defaults and top-level uns keys. Modern sc.tl.paga
results remain under uns['paga']; callers assign their sparse matrices explicitly
to the legacy keys, as shown in the expression notebook. There is no hidden
fallback, PAGA computation, expression access or mutation in the plotting call.

[`adjacency_values`](../../src/genome_spy/integrations/scanpy/_paga_data.py)
validates matching nonempty square resident sparse matrices/arrays before loading
up to 250,000 adjacency values. The tree stays sparse; only nonzero entries
become points. Original numeric indices/order, asymmetric entries, diagonal
entries, negative tree weights and missing adjacency values are preserved.
Scanpy's tree placement is x=row, y=column, even though heatmap tiles use
x=column, y=row. This difference is intentional and tested with asymmetric data.

[`build_paga_adjacency`](../../src/genome_spy/integrations/scanpy/_paga_chart.py)
adds fixed-pixel native black points to the existing numeric matrix renderer's
center. That renderer now accepts an optional native overlay; its default path
is unchanged. Tiles, color bounds/schemes, native colorbar, indices, hover,
y/both-axis navigation, fitted values, layout and HTML delivery stay shared.
No custom geometry, legend or Core patch is introduced.

Verification: **429 targeted Python checks passed, one expected pre-existing
upstream failure**; **eight adjacency browser checks**, **19 shared matrix browser
checks**, both canonical workflows, Ruff formatting/full-repository lint and mypy
pass. [Data/contract checks](../../tests/integrations/scanpy/test_paga_adjacency.py)
compare direct public Scanpy values and point positions, plus CSR/CSC/LIL/COO/DOK/BSR,
sparse arrays, custom keys, explicit zeros, empty trees, singletons, constant/
missing values, mutation/analysis guards and rejection before oversized loads.
[Complete charts](../../tests/integrations/scanpy/browser/test_paga_adjacency.py)
register 100-display/150-export-DPI tiles, palette bins, numeric ticks, native
guide placement/length and point footprints. They observe matrix/tree hover,
hover=False, fitted values, exact visible point projection after zoom/pan,
off-screen culling and offline HTML. References, screenshots and overlays remain
temporary. Font metrics, automatic tick density and outer spacing retain M14
owners; whole-image pixel identity is not claimed.

The live PBMC expression notebook completed **34 code cells and 28 charts without
Python errors**. Its explicit assignments share stored PAGA matrices; the analysis
still runs only in the existing preparation cell. Committed notebooks contain
source only; local edits and executed outputs are preserved.

A seed-0 workload uses an unread empty 100,000-by-20,000 float32 CSR expression
matrix, a 200-group CSR adjacency from 4,000 uniformly sampled weighted entries,
and a 199-edge chain tree. Warm preparation with zoom/fitted values took
**0.737 s**, validated JSON **4.353 s**, and peak traced Python allocation
**63.76 MiB**. It serialized **40,000 tiles, 199 points and 5,039,289 JSON bytes**.
The native 600-by-600 chart rendered in **2.78 s**, showing all 199 tree points;
JS heap was **54.17 MiB before explicit GC**. These are local observations, not
portable limits. JSON expansion remains a material cost; the bounded load guard
does not promise large-grid transport efficiency.

The stripplot increment is delivered below. C15's independent PAGA graph
reference gate remains blocked. The full repository suite and docs build were
not rerun. The current queue owns next work. Clearance: **retain**; full M11 and
the integration roadmap remain open.

### Independent matrix composition correction

The shared numeric matrix renderer now leaves x/y scales unnamed. GenomeSpy
resolves their identity through native composition instead of conflicting global
names when two zoomable matrix or adjacency charts appear together. This is one
shared call change, using the existing zoom_axes helper; native zoom, values,
labels, guides and tree points retain their existing behavior. No name generator,
Core patch or runtime listener is added. Time-series, simulation and DPT heatmaps
reuse the same corrected path.

Verification (2026-10-23): **171 targeted Python checks and 47 browser checks
passed**, including four new matrix/adjacency × y-only/both-axis composition
regressions. They render unmodified generated charts, observe tile geometry while
zooming/panning one panel, verify the other stays unchanged, then check hover and
offline HTML. Existing standalone tests explicitly name their test scales where
inspection needs names; production specs remain unnamed. Both canonical workflows
pass, including an isolated output-free source copy for this fix. The independent
matrix example adds one expression cell/chart (35 code cells, 29 charts in this
slice). A coordinated live Jupyter run with the parallel PAGA comparison example
completed 36 cells and 30 charts without Python errors; a wheel gesture visibly
zoomed only the left matrix. Committed notebooks retain source only.

Ruff formatting/full-repository lint and mypy pass. Data preparation, emitted
records and transport are unchanged, so the retained adjacency resource checks
still cover those workloads. The full repository suite and docs build were not
rerun. The current queue owns next work; broader adjacency storage, styling and
export options remain M14.
Clearance: **retain**.

## M11.d PAGA adjacency strips

Closed (2026-10-23) for the bounded `as_heatmap=False` preview. The existing
[`paga_adjacency`](../../src/genome_spy/integrations/scanpy/pl.py) entry reuses
adjacency validation, sparse tree extraction, coordinate bounds, zoom and native
points. Gray points show off-diagonal adjacency values; black points show the
adjacency values at tree nonzeros, including selected diagonal entries. Stable
per-source ordering preserves Scanpy's gray-before-black paint order. Neither
expression nor analysis is read or recomputed; stored matrices remain unchanged.

Default plot dimensions, point footprints and domains match the pinned public
reference, including constant, missing and empty visible values. Native tooltips
show source, target, connectivity and edge kind. Optional y-only/both-axis zoom
and independent composition use the shared navigation helper. `color_map` is
inactive in this mode, as upstream; fitted `show_values` requires heatmap mode.

Verification: **394 targeted Python checks**, **18 adjacency browser checks**,
both canonical workflows, full-repository Ruff lint and mypy pass. The
[semantic references](../../tests/integrations/scanpy/test_paga_adjacency.py)
cover six sparse formats, original indices/values, mutation guards and exact
finite draw order. [Browser references](../../tests/integrations/scanpy/browser/test_paga_adjacency.py)
register 100-display/150-export-DPI complete charts at DPR 1.5, including
point centers, footprints, colors and numeric domains. Observed checks cover
gray/black hover, disabled hover, y/both-axis zoom/pan, independent composed
charts and offline HTML. Reference images and registered overlays stay temporary.
The live expression notebook ran **37 code cells and 31 charts without Python
errors**; committed notebook source contains no outputs or widget state.

A seed-0 observation reuses the heatmap's unread 100,000-by-20,000 CSR expression
fixture, 200-group adjacency and 199-edge chain tree. It emits **39,999 native
points and 4,335,779 JSON bytes**. Preparation took **0.006 s**, validated JSON
**2.516 s**, peak traced Python allocation **53.19 MiB**, and native 600-by-600
browser rendering **2.941 s** with **42.63 MiB JS heap before explicit GC**.
One separate browser resource check confirmed every point rendered. These are
local observations, not portable guarantees; JSON expansion remains material.

The resident 250,000-value bound, legacy top-level keys and broader storage,
styling/export limits retain M14 owners. Path heatmap delivery is recorded below;
the current queue owns subsequent work. The full
repository suite and docs build were not rerun. Clearance: **retain**; full M11
and the integration roadmap remain open.

## M11.d PAGA path heatmaps

Implemented (2026-10-23); native semantics/chart/workflow/interaction/resource
checks verified, **C16 direct default return_data gate remains blocked**. The
native entry reads stored categorical groups and DPT pseudotime. Its pure
[preparation](../../src/genome_spy/integrations/scanpy/_paga_path_data.py) reuses
shared grouped_expression/public Scanpy obs_df access, resident-expression guards
and numeric validation. It preserves supplied group names/indices/repeats,
within-group NumPy sort order, raw/X fallback, cumulative full-window averages,
then optional per-key normalization. Only selected genes are densified; a
250,000 selected cell–key/annotation value guard precedes expression reads.

The [renderer](../../src/genome_spy/integrations/scanpy/_paga_path_chart.py) reuses
matrix_tiles, fitted values, slot labels, shared palette/bounds and zoom helpers.
Native surround holds contiguous original group bands and smoothed numeric
annotation tracks. Their full-width alignment matches upstream's separate image
extents when smoothing shortens profiles. No hidden analysis, custom geometry,
listeners, patched Core, benchmark imports or runtime Matplotlib calls are added.
The notebook computes diffusion coordinates and DPT explicitly on packaged PBMC,
then shows six genes in a supplied group sequence; it does not infer a trajectory.

**354 targeted Python checks pass**, including dense/CSR/CSC references, raw/X,
repeated nodes, smoothing/normalization, metadata-only access, missing values,
backed/oversize guards, mutation/analysis guards and shared display behavior.
C16 is a separate strict expected failure: pinned Scanpy's default return_data
calls .T on a list. The test checks that exact exception and validates the
returned table if an upstream fix lands. Other public return_data cases compare
directly; the native return is (chart, frame) for show=False, or frame after display.
Both clean notebook workflows pass. The live notebook ran 40 nonempty code cells;
33 charts rendered without Python errors; local outputs remain local and the
committed notebook source is output-free.

All **eleven browser checks pass**, covering complete registered charts,
matrix/group/track hover, disabled hover, y/both-axis navigation, fitted values,
independent composed panel zoom/pan and offline HTML. The default annotated
reference retains Scanpy's values, numeric domains and group bands. Native Greys
starts/ends at RGB 226/30, where Scanpy uses 255/0; the user explicitly accepted
that native fidelity limit on 2026-10-23. Tests assert both endpoint pairs and
compare native annotation pixels with their declared scale, while matrix/group
pixels still compare directly with Scanpy. No alternate palette or broadened
pixel tolerance hides the difference. Constant colors with and without a guide
and default plot dimensions compare directly against the public reference.

A seed-0 sparse workload has 100,000 observations, 20,000 genes, 20,000 stored
entries across the first 10,000 cells/twenty selected genes, and two 5,000-cell
path groups. At n_avg=25 with normalization, it emits 199,520 tiles, 10,000
original group bands and 9,976 annotation bands. Preparation took **0.010 s**,
chart construction including preparation **0.189 s**, validated JSON **19.929 s**,
with **357.79 MiB peak traced allocation** and **29,983,240 JSON bytes**. Native
800-by-320 browser rendering took **13.915 s**, with **189.78 MiB JS heap before
explicit GC**. These are local observations; serialization/transport remains a
material cost and the value budget is not a large-grid efficiency guarantee.

**Memory correction (2026-10-23):** the shared reader now accepts observation
positions after public Scanpy column extraction, before grouping and numeric
validation. PAGA path no longer creates a row-indexed AnnData, eliminating its
full-width dense X/raw copies while preserving repeated nodes, mixed obs/gene
keys and path-only validation. Dense X/raw tests intercept column copies and
both failed on the previous implementation. A separate regression ignores
infinite expression outside the path and still rejects it inside the path.
For 1,000 cells by 10,000 float32 genes, selecting two genes now peaks at
**0.54 MiB extra for X / 0.52 MiB for raw**, versus **76.69 / 38.69 MiB** before
the fix (imports and source allocation excluded). Column extraction still spans
the supplied observations; this does not introduce streaming or change Scanpy's
handling of caller-created views. **394 relevant Python tests, eleven PAGA path
browser tests and both clean workflow tests pass**, with the existing C16
expected failure. The updated live expression notebook ran all 42 nonempty code
cells without Python errors. Ruff and mypy pass. Native chart construction is unchanged.

The preview requires two keys/two smoothed samples, at most one numeric track,
finite stored pseudotime and resident expression. Categorical/multiple tracks,
singular shapes, custom margins and broader source/style/export options retain
M14 owners. Connected-line mode remains the next separate native audit under
C04. Full repository tests and docs build were not rerun. Clearance: **retain**;
the native preview does not close the full path family or M11.d.

## M13.a native DotPlot builder

The bounded builder preview is **Closed**. The
[builder](../../src/genome_spy/integrations/scanpy/_dotplot_builder.py) keeps
detached group summaries and small explicit chain state; functional `dotplot`
delegates the same path. Both reuse grouped expression/statistics, stored/public
Scanpy tree preparation, marker permutations, native grouped layout and the
existing dot/guide renderer. No generic builder base, upstream plotting object,
private chart rewriting or custom renderer is introduced.

The self-containment correction moves the existing kwargs, dimensions/flags,
grid zoom and lazy Scanpy dependency guards into
[`_guards.py`](../../src/genome_spy/integrations/scanpy/_guards.py). The builder
and public functions import them directly; the builder no longer imports `pl`.
Validation behavior and native rendering are unchanged.
Correction verification (2026-10-23): **2,016 Python cases pass**, with the two
known upstream expected failures, including missing/incompatible dependency
checks through both public functions and the builder. Ruff formatting/lint and
mypy pass. Browser and notebook runs were skipped for this guard-only refactor.

Constructor defaults match the pinned class except omitted `ax` and the documented
native hover/navigation/dimensions. Supplied `dot_size_df` is copied and checked
against group labels, repeated feature slots and finite [0, 1] fractions.
Methods return self: swap_axes sets orientation; add_dendrogram/add_totals replace
the same native track and retain established ordering when hidden; totals sort
counts and accept scalar/per-displayed-group CSS colors. Dot styles cover native
schemes, fraction limits, both area bounds, exponent, edges, grid and padding;
legend controls cover shared/separate visibility, titles and native gradient
width. Width also controls the figsize guide allowance. Native symbol-guide
layout and typography keep the parent family's documented differences.

Each to_chart call creates a detached native snapshot without rereading
expression. Later chains do not change earlier charts. show displays once with
the existing widget, independently of Scanpy autoshow/autosave; return_axes=True
errors with the native alternative. Matplotlib figure/artist methods are omitted;
use the native chart's configuration/composition/display and HTML/JSON saving.
Automatic fixed dotplot scale names were removed so independent native
compositions do not collide. Validation assigns names only to inspected scales.

Verification (2026-10-23):

- [39 builder tests](../../tests/integrations/scanpy/test_dotplot_builder.py)
  compare actual Scanpy chains for ordering, positions, areas, padding and totals
  in both orientations, plus supplied/repeated slots, no expression rereads,
  snapshots, guide controls and errors. Existing functional/frozen references
  continue through the shared path.
- The integration Python run passed **2,011 cases**, with **two known upstream
  expected failures** (C15/C16). Its single workflow assertion mismatch reflects
  preserved local zoom edits, not the canonical source. **Both canonical workflow
  tests pass separately**, including the new tree/totals builder examples: 42
  expression code cells and 35 charts. Local edits and execution state remain
  untouched; the committed notebook contains source only.
- **133 distinct headless browser cases are verified**, with the two existing
  C12/C13 expected failures retained. The parent run passed 127 cases; one
  initial-pixel check's antialiasing mask now derives its margin from the native
  frame width, and all five initial-pixel cases pass on rerun. The five
  [new builder cases](../../tests/integrations/scanpy/browser/test_dotplot_builder.py)
  verify complete tree/guide/style output, totals paint/hover/navigation, independent
  composition and offline HTML. Exact SVG dot geometry and interior pixel checks
  remain in place. All browser tests use headless Chromium, without desktop apps.
- [The retained resource generator](../../tests/integrations/scanpy/benchmark_grouped.py)
  accepts `--plot dotplot --builder --dendrogram --browser`. Its seed-0 workload
  has 100,000 cells × 20,000 sparse genes, 40 selected genes, 50 groups and 2,000
  summary marks. Construction plus three retained snapshots densifies exactly
  one 100,000 × 40 selection. Observed cold preparation is 3.27 s, serialization
  0.30 s, traced peak/retention 142/79 MiB (including optional imports and all three
  snapshots), process RSS 505 MiB and final JSON 199 KiB. Native first paint is
  1.83 s including dispatch; hover/wheel response is about 0.20 s each, with
  9.3 MB JS heap after collection. These are laptop observations, not portable
  timing limits. Parent frozen/data/layout evidence is reused for unchanged
  storage/statistics/mark paths; this new workload covers builder retention and
  repeated snapshots directly.
- Ruff formatting/lint and mypy pass. Full repository tests, docs build and a
  visible notebook/browser session were not run for this slice.

Remaining M13 scope: square-background dot coloring, padding below 0.5,
public constant customization, broader style forms and the MatrixPlot/StackedViolin
builders. Parent storage/palette/typography/export restrictions retain M14 owners.
The next independent builder is MatrixPlot; this bounded preview does not close
M13. Clearance: **retain**.

## Public callable coverage

The [pinned inventory](../../tests/integrations/scanpy/fixtures/api.json) has 50
entries: 45 plotting functions including aliases, three builders, two settings
helpers. 39 plotting functions/builders are available as partial previews; 9 plot/builder
entries remain unimplemented. The two settings helpers are external renderer
exceptions. This count measures entry availability, not parameter completeness.
No placeholder functions are exported for planned work.

| Public entry | Availability | Delivery milestone |
| --- | --- | --- |
| `DotPlot` | Partial native builder available; bounded preview verified | M13.a; square-background styling and broader options remain M13/M14 |
| `MatrixPlot` | Not implemented | M13 (after M03/M04) |
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
| `paga_path` | Partial stored-path heatmap preview; native checks verified | M11.d; C16 direct return_data gate, line mode and broader annotations remain open |
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
| `tracksplot` | Not implemented | M09 |
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
| Point outlines | Shared outline layers, relative widths/CSS colors, scalar styles, hover/zoom/brush | [M07.d outline increment](#m07d-embedding-point-outlines) closed; square support below |
| Square markers | Native squares in shared embeddings/PCA overview/scatter, including outlines, legends and interactions | [M07.d square increment](#m07d-square-markers) closed |
| Diamond markers and category keys | Native diamonds with Scanpy path widths; keys inherit each panel's marker shape | [M07.d diamond increment](#m07d-diamond-markers) and [legend follow-up](#marker-legend-follow-up) closed |
| Triangular markers | Clear rejection; native equilateral paths cannot preserve Scanpy's width and height | [M07.d audit](#m07d-triangular-marker-audit) closed; support Blocked by C14 |
| Stored neighbor-graph edges | First component pair, native segments and endpoint lookups, scalar CSS styles; explicit restrictions on other forms | [M07.d edge increment](#m07d-stored-neighbor-graph-edges) closed |
| Other graph forms, arrows, scale_factor, broader markers/categorical guide locations | Nondefault forms reject | M07.d/M14 |
| Callable color bounds | Shared resolver with masked/sorted copies, per-panel lists and finite results | [M07.d callable increment](#m07d-callable-color-bounds) closed |
| Centered numeric colors | Shared scalar/percentile/callable resolver, per-panel centers and native piecewise color scales | [M07.d center increment](#m07d-centered-embedding-colors) closed |
| norm | Matplotlib normalization objects remain outside the native boundary | Maintained contract |
| Backed/lazy expression; named scheme with NA legend; category/NA label collision | Explicit current restrictions | M14.c |
| 3D, font atlas/weight/outline and complete typography | Native gaps/limits | M14.a; C03/C05 |
| Image save/autosave | Inactive form only; use native HTML/JSON save | M14.c |
| ax/cax/return_fig, artist methods, Matplotlib color/global settings | Intentional native rendering boundary | Maintained contract, not pending artist emulation |

| Scatter parameter group | Current support | Completion owner |
| --- | --- | --- |
| Observation/variable x/y, exact X_ basis/components, per-axis layers, palettes/groups/order, multiple panels | Tested bounded preview; [contract](../../docs/integrations/scanpy/index.md#scatter-cells-or-genes) | M07.b preview retained |
| Native numeric axes, points/guides, cell/gene hover, optional x/y zoom and dimensions | Shared embedding helpers; no scatter brush/Python membership yet | M07.b; broader selection M14 |
| On-data labels/centroids, margins, highlights, more markers/sizes, 3D and storage/export | Nondefault forms reject; native layout/typography differences recorded | M07.d/M14 |

| PCA diagnostics parameter group | Current support | Completion owner |
| --- | --- | --- |
| Stored finite NumPy loadings, component order/repeats, high/low/top ranks, native sizing/hover and common delivery | Bounded loadings preview; [contract](../../docs/integrations/scanpy/index.md#pca-loadings) | M07.c loadings preview retained |
| Sparse/lazy or nonfinite loadings, full typography and image export | Explicit restrictions; no automatic filtering/analysis | M14 |
| Stored variance ratios, PC numbering, linear/natural-log scores, native sizing/hover and common delivery | Bounded variance preview; [contract](../../docs/integrations/scanpy/index.md#pca-variance-ratios) | M07.c variance preview retained |
| Overview | Verified bounded native composition, parent dimensions/defaults, scatter-only kwargs and one display | M07.c preview retained; parent limits M07.d/M14 |

| Matrixplot parameter group | Current support | Completion owner |
| --- | --- | --- |
| Grouped source/categories/repeated slots, log/means/scaling, supplied values_df, native tiles/guides/edges/hover | Tested preview; exact forms in user contract | M03 preview retained |
| Dendrogram ordering/attachment and compatible stored trees | Verified leaf/marker reordering and native branches | M04 preview retained |
| Optional zoom and fitted plotted values | Shared native grid helpers, annotations follow live index scales | M05.e |
| MatrixPlot builder, semantic styling/legend chains | Not implemented | M13 |
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
| Larger/chunked values, backed/lazy data and quadratic-distance policy | Explicit pre-access guards; supplied linkage bypasses computation only | M05.d/M14.c |
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
| Constructor signatures/defaults and native result delivery | DotPlot implemented with pinned defaults, native keyword additions and detached to_chart snapshots | [Constructor/chain tests](../../tests/integrations/scanpy/test_dotplot_builder.py); other classes remain M13 |
| add_dendrogram/add_totals/swap_axes | DotPlot implemented; native aligned tree or count track, sorting/colors and orientation | [Actual upstream chains and native browser checks](../../tests/integrations/scanpy/browser/test_dotplot_builder.py); other classes remain M13 |
| style/legend and useful public defaults/constants | DotPlot dot styles and native guide controls implemented; square backgrounds and public constant customization remain open | Shared native renderer and chain tests; other classes remain M13 |
| get_axes/figure/artist access | Intentional renderer boundary; no Matplotlib objects are offered | Use DotPlot.to_chart for native configuration/composition; other classes remain M13 |
| make_figure/show(return_axes)/savefig | DotPlot omits Matplotlib make_figure/savefig; show(return_axes=True) errors with the native alternative | Native to_chart, show and chart.save contract/tests; other classes remain M13 |

## Native capability ledger

Audit: bundled Core/schema **1.2.0** adopted October 20; the native mark inventory
is still rect, point, rule, tick, text, link and arrow. The October 19 Core 1.0
checks of native rules, formula transforms, excluded scales/axes and tree alignment
remain historical evidence. Recheck each capability before implementing an
affected slice.

| ID | Gap or available capability | Affected work | Resolution/recheck trigger |
| --- | --- | --- | --- |
| C01 | No native filled-area/polygon primitive in bundled schema | Full violin/stacked/tracks M08/M09 | Released filled geometry and density/profile chart tests; no custom trial geometry promotion |
| C02 | No native raster/image primitive | Full spatial M12 | Released image capability with crop/aspect/zoom registration tests |
| C03 | No native 3D projection | 3D embedding options M07/M14 | Released capability or explicit product scope decision; keep unresolved until then |
| C04 | No dedicated line/path mark in bundled mark inventory | Unverified connected path cases in M11; timeseries helpers are scatter points | PAGA undirected straight edges use native rules and are not blocked. Audit each connected-path entry separately; otherwise await a released capability. |
| C05 | Font/text-outline/normalization/NA-guide limits | Parameter closure M07/M14 | Per-option released API inspection and complete-chart tests |
| C06 | Core 1.2 typed surround/facet APIs and native index gaps available; Scanpy migration remains open | Heatmap/clustermap side tracks, related grids, UMAP/repeated panels; M14.b | Use the published heatmap example; verify viewport/scale/guide ownership, required heatmap group gaps and existing navigation/selection contracts |
| C07 | Python linkage + shared native orthogonal branches verified | Trees M04 and heatmap M05.a/b delivered; later families M08/M09 | Stored parent/child edges project into equal summary slots or unequal cell-group centers. Complete SVG elbows, four orientations, zero heights, resize and navigation pass; recheck later families. |
| C08 | Native index slots plus label layers retain repeated dotplot/matrixplot labels | Heatmap/ranked families; wider navigation | Dot/matrix slots, both orientations, optional zoom and duplicate-slot highlighting verified; extend checks with later families |
| C09 | Core 1.0 band rulers failed during initial WebGL rendering; the adopted Core 1.2 capability needs a focused recheck | Optional shaded row/column guides | Keep the native center crosshair until shaded-guide behavior is verified against Core 1.2. [PR #586](https://github.com/genome-spy/genome-spy/pull/586) records the upstream fix and regression evidence. |
| C10 | Heatmap/clustermap bands and native gap navigation verified in their own viewports. | Closed for M05.f native WebGL/notebook/HTML scope | Native clipped rects use the released Core; no patched bundle or custom listeners. C12 remains independent. |
| C11 | Bundled Core 1.2 allocates one column's width to vertical multi-column legends; later columns clip. Large Scanpy scatter symbols also overflow a single column in short panels. | M07.a/b complete-chart closure, default legend fitting and M14.a guide layout | [Minimal native regression](../../tests/integrations/scanpy/browser/test_native_legend_extent.py) strictly xfails on 1.2.0. [Upstream fix PR #591](https://github.com/genome-spy/genome-spy/pull/591) includes before/after video comments; it is not adopted in the bundled runtime. Recheck after adopting a released Core fix before automatic column fitting; no local bundle patch. |
| C12 | Core 1.2 SVG export bends `linkShape="line"` control points. | Upstream straight-link export; adapter trees now use verified orthogonal links. | The minimal straight-link SVG check in [browser/test_dendrogram.py](../../tests/integrations/scanpy/browser/test_dendrogram.py) still strictly xfails. No local bundle patch; recheck on a released fix. The [orthogonal renderer](#shared-native-orthogonal-dendrograms) passes complete-path SVG checks independently. |
| C13 | A viewport containing only zero-height merges gives a degenerate `[0, 0]` height domain, centering zero in the track. | Native fitting of tied subtrees within larger trees | Minimal native regression in [browser/test_dendrogram.py](../../tests/integrations/scanpy/browser/test_dendrogram.py) strictly xfails on Core 1.2.0. Whole zero-height trees retain their previous nonzero range. Recheck a released native solution; no custom browser logic or patched bundle. |
| C14 | Native equilateral triangles differ from Scanpy's equal-width/height triangles; uniform sizing cannot match both dimensions. | Triangular markers in M07.d | [Native SVG/WebGL comparison](../../tests/integrations/scanpy/browser/test_native_triangles.py) strictly xfails for four orientations, with/without strokes. Recheck a released matching shape or native aspect control, including guides and outlines, before enabling support; no custom geometry. |
| C15 | Scanpy 1.11.5's disconnected single_component=True call subsets colors but retains full coordinates and raises a shape error. | M11.c direct parent-reference gate | [Strict expected-failure check](../../tests/integrations/scanpy/test_paga.py) detects a fixed upstream entry. Intended native filtering is independently checked against explicitly subsetted public Scanpy inputs; recheck a compatible release before closing this gate. |
| C16 | Scanpy 1.11.5 paga_path return_data calls .T on an unsmoothed annotation list | Default return_data parent-reference gate; heatmap/other return_data cases verified independently | Strict expected-failure check verifies the exact exception and asserts returned values if fixed; native chart/table return contract is explicit. |

Python computation alone does not close a renderer gap. Local Core patches are
excluded. Historical violin, filled-track and tree recipes are experimental
research; only reviewed numerical ideas or evidence may be reused with provenance.

## Plan clearance ledger

Lifecycle reconciliation (2026-10-19): removed superseded forecasts, linked the
latest delivery commits, and corrected premature Verified claims for M06/M07.
Required browser resource evidence stays with the originating slices; it was
not completed by the scatter implementation or deferred to tile transport.
No acceptance gate was waived and no research/working plan was cleared.

Resource reconciliation (2026-10-20): seven maintained benchmark workloads and
explicit parent-path reuse close gate 4 for M06/M07. M06's bounded preview closes;
M07.a/b remain Implemented because the newly reproduced C11 guide-layout gap
leaves complete-chart verification open. No plan is eligible for clearance.

No research artifacts are deleted by this update. Paths below can be absent in
a fresh clone; active delivery depends only on tracked files. The ignored
historical plan already links to the tracked roadmap and remains archival;
its old namespace/color proposals are not current policy.

| Artifact | Role and clearance state | What permits clearing |
| --- | --- | --- |
| `integrations/scanpy/PLAN.md` | Active roadmap; retain | Full required scope closed; replace with completion/release record and maintained contracts |
| `integrations/scanpy/STATUS.md` | Current state and completion record; retain | Maintain through implementation and release; do not discard evidence/next-work history |
| Per-slice working plans (none currently) | Create only if useful | Verified commit, decisions/tests/contracts transferred, residual work assigned; then mark eligible and remove in a scoped change |
| `plans/scanpy_integration_plan.md` | Superseded local working plan; retain pending reconciliation | New PLAN owns active scope; check old unresolved decisions/history and remove contradictory policy only after unique findings have durable homes |
| `plans/scanpy_coverage_audit.md` | Local tutorial coverage/fidelity research; retain/archive | Transfer unique measured gaps/provenance to tests/contracts/capability ledger before clearing redundant prose |
| `plans/scanpy_categorical_trial.md` | Historical trial report; not active implementation | Retain useful evidence/provenance or archive; preview completion alone does not authorize deletion |
| `plans/scanpy_agent_benchmark.md` | Separate study design; retain | Its fresh/blinded trial objectives need their own decision; production tests do not complete that study |
| `tmp/agent-benchmarks/` | Local prototype data/scripts/references/overlays; retain pending review | Preserve unique results, licenses, reproduction metadata and recordings before clearing redundant scratch material |
| Runtime, API/reference fixtures, tests, real-data notebooks and user guide | Maintained implementation/evidence, not disposable plans | Normal maintenance/versioning; not cleared when a milestone closes |

When a slice closes, record its verified scope, source/test or commit links,
remaining debt, next ready slice, and whether any working document is eligible.
Clearance never means silently dropping an unimplemented plot or required check.
