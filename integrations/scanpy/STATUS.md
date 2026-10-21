# Scanpy implementation status

Updated: 2026-10-21. This is the current progress ledger; [PLAN.md](PLAN.md)
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
Stored ranking/score panels and ranked dotplot/matrixplot/heatmap previews now
reuse Scanpy's public result getter and the existing expression plot functions.
Stored PCA loadings and variance ratios reuse the ranking preparation and native
text panels; PCA overview composes these with the existing embedding chart.
UMAP includes native sizing, optional hover/zoom, linked interval highlighting/count
and Python subset retrieval. Dotplot includes index-scaled slots, grouped summaries,
brackets, native size/color guides and optional summary hover. Matrixplot reuses
grouped access/means and native layout, with one-pass scaling, authoritative
`values_df`, tiles and optional summary hover. Trees reuse `sc.tl.dendrogram`
computation/results, with structural checks and native branch rendering.
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

The current canonical workflows contain sixteen UMAP/embedding/scatter/PCA
code cells and thirteen expression/ranked code cells. Public availability does not mean
all slice gates or full-family compatibility are closed.

### Current work queue

**Next work: M14.b.3, matrix/clustermap/correlation native tracks.**
M14.b.1 and M14.b.2 are closed for native WebGL/notebook/HTML layout;
[the grouped-layout record](#m14b2-native-grouped-layout) retains the new evidence.
Heatmap and dotplot have four-pixel group gaps; matrixplot tiles remain contiguous.
Numeric/clustered grids retain their earlier layouts until their own
[migration increment](PLAN.md#m14b-native-grid-layout-and-group-gaps) is verified.
Clustermap must gain group gaps; the grouping/cut input is awaiting clarification.
Core's separately reproduced SVG straight-link issue remains C12/M14 vector-export
work; it does not close or block the native WebGL migration scope.

M07.d's [native colorbar placement increment](#m07d-native-colorbar-placement) is
closed in `730f9ce` for the four sides and None across shared embedding entry points.
Scatter's distinct signature stays unchanged. Default categorical-guide fitting
is separately blocked by C11; keep its upstream reproducer and recheck it on a
released Core fix.

The M06/M07 resource gates now have fresh seven-workload evidence below. This
does not close M07.a/b's newly observed categorical-guide rendering gap.

Core 1.2.0, its generated composition APIs and the published heatmap example are
now adopted; see the [upgrade record](#core-12-runtime-adoption). M14.b.1/b.2 are
closed for their native layout scope. M14.b.3 has released native track APIs;
its clustermap group-gap input still needs a decision. Heatmap bands are
verified inside native track viewports; clustermap still needs its own M05.f migration and checks.

| Slice | Lifecycle state | Commit/evidence | Remaining work before Verified/Closed |
| --- | --- | --- | --- |
| M06.a–d stored ranking | Closed (bounded preview) | `2800f23`, `f043299`; [resource closure and reuse assessment](#m06m07-resource-verification) | Broader parameter/storage/typography/export limits remain M14; ranked distributions/tracks remain M08/M09 and builders remain M13. |
| M07.a shared embeddings | Implemented; resource gate verified | `39b4d7d`; [fresh eight-panel workload](#m06m07-resource-verification) | C11 blocks reliable default multi-column categorical-guide fitting. Existing parameter/storage limits retain M07.d/M14 owners; resource verification alone does not close the preview. |
| M07.b scatter | Implemented; resource gate verified | `0fdcc02`; [cell and gene workloads](#m06m07-resource-verification) | Large default category symbols can overflow short panels; C11 blocks the multi-column correction. Keep this complete-chart gate open independently of passed resource checks. |
| M07.c loadings increment | Closed (bounded preview) | [Contract, tests and resource evidence](#m07c-stored-pca-loadings) | Broader storage/typography/export remain M14. Variance and overview are separate increments; this does not close M07. |
| M07.c variance increment | Closed (bounded preview) | [Contract, tests and resources](#m07c-stored-pca-variance-ratios) | Broader storage/typography/export remain M14; this does not close the overview or M07. |
| M07.c overview increment | Closed (bounded preview) | [Contract, tests and resource evidence](#m07c-pca-overview) | Parent storage, typography and export limits remain M14; broader embedding options remain M07.d and C11 retains their categorical-guide gate. |
| M07.d colorbar placement increment | Closed (bounded increment) | `730f9ce`; [contract, browser/workflow checks and resource reuse](#m07d-native-colorbar-placement) | Four sides/None supported; remaining embedding options stay M07.d/M14 and categorical default fitting stays C11. |
| M05.d larger/chunked tile transport | Planned | Existing tile budget and [heatmap resource envelope](#m05ab-cell-heatmap-preview) | Design/test chunked access and 100k × 50 behavior. This does not own missing resource verification of M06/M07 previews. |
| M14.b.1 heatmap side tracks/gaps | Closed (native heatmap migration) | [Delivery and validation](#m14b1-native-heatmap-tracks-and-gaps) | Wider transport, storage and option closure remain M05.d/M14; other grid families retain their own migration slices. |
| M14.b.2 grouped summary layout | Closed (native WebGL/HTML layout) | [Delivery, browser/workflow and resource evidence](#m14b2-native-grouped-layout) | Vector tree-link export remains C12/M14; broader family options remain in their existing slices. |
| M14.b.3 numeric/clustered layout | Ready for native tracks; group-gap input pending | [Native numeric grid scope](PLAN.md#m14b-native-grid-layout-and-group-gaps) | Migrate matrix/clustermap/correlation labels, trees and color tracks. Define the requested clustermap group gaps before choosing any tree cut or annotation boundaries. |
| M05.f category-strip hover | Heatmap track migration verified; clustermap migration ready | C10; [heatmap evidence](#m14b1-native-heatmap-tracks-and-gaps); [layout route](#m05f-category-strip-tooltips--layout-migration) | Clustermap viewport migration and verification remain M14.b.3. Legacy hover already works on Core 1.2. |

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
| M04 trees/correlation | Closed (standalone/correlation and dot/matrix attachment preview) | Public Scanpy computation, stored-result validation, native rules, shared leaf/marker permutations, registered charts, resize/hover checks and resource observation below. Later-family attachments remain assigned. |
| M05 heatmap/matrix/clustermap | In progress; bounded previews verified | M14.b.1 native heatmap migration is closed; M05.f's remaining clustermap migration belongs to M14.b.3. M05.d and broader kwargs/delivery remain open. |
| M06 ranking/ranked summaries | Closed (bounded preview) | M06.a–d have semantic/chart/workflow/interaction and resource evidence. Broader compatibility remains M14; native builders remain M13 and ranked distributions/tracks remain M08/M09. |
| M07 embeddings/scatter/PCA | In progress | M07.a/b resource gates pass; categorical-guide rendering remains open under C11. M07.c loadings/variance/overview and M07.d colorbar placement are Closed for their stated scope; other options remain open. |
| M08 violin/stacked/ranked | Planned; filled rendering blocked | Data/density work can proceed; full native filled geometry needs a released capability (C01). |
| M09 tracks/ranked tracks | Planned; filled rendering blocked | Profile preparation can proceed; native filled geometry needs C01. |
| M10 QC diagnostics | Planned | Highest expression, variable genes, legacy dispersion and Scrublet distributions. |
| M11 trajectories/graphs/series | Planned | Stored DPT/PAGA, graph layouts, series/simulation, return/side-effect contracts; evaluate C04 paths. |
| M12 density/spatial | Planned; full spatial blocked | Density uses stored analysis; image-backed spatial requires C02. |
| M13 builders | Planned | DotPlot/MatrixPlot/StackedViolin semantic chains are not implemented; develop them with their parent families and track method coverage separately. |
| M14 compatibility/docs/release | In progress; Core 1.2 adopted | M14.b.1/b.2 native layout migrations are closed; M14.b.3 native tracks are ready, with clustermap gap inputs pending. C12 retains vector tree-link export fidelity. Parameter/capability closure, workflow publication and full API evidence remain open. |

## M05.e shared grid interactions

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

Clustermap gaps are requested for M14.b.3. Its current tree order can interleave
annotation categories, so a dendrogram cut and category-change gaps are different
contracts. The group source/cut inputs are awaiting the user's choice; no cut,
reordering or new clustering analysis is selected silently.

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

Current state: heatmap bands are verified inside native track viewports in
[M14.b.1](#m14b1-native-heatmap-tracks-and-gaps). Clustermap still needs M14.b.3;
the heatmap migration alone does not close M05.f for both families.

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

Clearance: retain. M14.b.1 closes the heatmap portion; M14.b.3 still owns replacing
clustermap's overlay and verifying its geometry, navigation and workflow. Core 1.2
already removed the legacy picking failure; keep the retained Core 1.0 results
historical rather than treating them as current expected failures.

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
M05 remains open for M05.d transport, M05.f strip hover and M14 option closure.
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

## Public callable coverage

The [pinned inventory](../../tests/integrations/scanpy/fixtures/api.json) has 50
entries: 45 plotting functions including aliases, three builders, two settings
helpers. 23 functions are available as partial previews; 25 plot/builder
entries remain unimplemented. The two settings helpers are external renderer
exceptions. This count measures entry availability, not parameter completeness.
No placeholder functions are exported for planned work.

| Public entry | Availability | Delivery milestone |
| --- | --- | --- |
| `DotPlot` | Not implemented | M13 (after M02/M04) |
| `MatrixPlot` | Not implemented | M13 (after M03/M04) |
| `StackedViolin` | Not implemented | M13 (after M08) |
| `clustermap` | Partial bounded preview available | M05.c; remaining options/transport M05.d/M14 |
| `correlation_matrix` | Partial preview available | M04 preview; normalization/options M14 |
| `dendrogram` | Partial preview available | M04 preview; options/export M14 |
| `diffmap` | Shared stored-2D preview | M07.a; remaining options M07.d/M14 |
| `dotplot` | Partial plain-chart preview; limits above | M02; trees M04; methods M13 |
| `dpt_groups_pseudotime` | Not implemented | M11 |
| `dpt_timeseries` | Not implemented | M11 |
| `draw_graph` | Shared stored-2D preview | M07.a; remaining options M07.d/M14 |
| `embedding` | Shared stored-2D preview | M07.a; remaining options M07.d/M14 |
| `embedding_density` | Not implemented | M12 |
| `filter_genes_dispersion` | Not implemented; legacy | M10 |
| `heatmap` | Partial cell-level preview available | M05.a/b preview; larger transport M05.d; normalization/options M14 |
| `highest_expr_genes` | Not implemented | M10 |
| `highly_variable_genes` | Not implemented | M10 |
| `matrix` | Partial supplied-numeric preview available | M05.b preview; broader sources/layout M14; transport M05.d |
| `matrixplot` | Partial preview available | M03 preview; trees M04; methods M13; normalization/options M14 |
| `paga` | Not implemented | M11 |
| `paga_adjacency` | Not implemented | M11 |
| `paga_compare` | Not implemented | M11 |
| `paga_path` | Not implemented | M11 |
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
| `scrublet_score_distribution` | Not implemented | M10 |
| `set_rcParams_defaults` | External: use Scanpy | Renderer exception, M00 |
| `set_rcParams_scanpy` | External: use Scanpy | Renderer exception, M00 |
| `sim` | Not implemented | M11 |
| `spatial` | Not implemented | M12; image capability C02 |
| `stacked_violin` | Not implemented | M08 |
| `timeseries` | Not implemented | M11 |
| `timeseries_as_heatmap` | Not implemented | M11 |
| `timeseries_subplot` | Not implemented | M11 |
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
| Graph edges/arrows, scale_factor, outlines, broader markers/categorical guide locations | Nondefault forms reject | M07.d |
| norm/vcenter/callable bounds | Nondefault forms reject; Matplotlib objects remain outside boundary | M07.d/M14.c |
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

| Builder surface (all three classes) | Current state | Completion evidence required |
| --- | --- | --- |
| Constructor signatures/defaults and native result delivery | Not implemented | Pinned class signatures plus family semantic/chart tests, M13 |
| add_dendrogram/add_totals/swap_axes | Not implemented | Chain return behavior, leaf/order/totals alignment, M04/M13 |
| style/legend and useful public defaults/constants | Not implemented | Family-specific option and chain tests, M13 |
| get_axes/figure/artist access | Intentional renderer boundary; builders do not yet exist | Explicit errors and native alternative, M13 |
| make_figure/show(return_axes)/savefig | Contract to resolve before builders ship | Native delivery/export decision and tests, M13/M14 |

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
| C04 | No dedicated line/path mark in bundled mark inventory | Series/graph/path M11 | Verify native rule/link segments can preserve required semantics; otherwise upstream released capability |
| C05 | Font/outline/normalization/NA-guide limits | Parameter closure M07/M14 | Per-option released API inspection and complete-chart tests |
| C06 | Core 1.2 typed surround/facet APIs and native index gaps available; Scanpy migration remains open | Heatmap/clustermap side tracks, related grids, UMAP/repeated panels; M14.b | Use the published heatmap example; verify viewport/scale/guide ownership, required heatmap group gaps and existing navigation/selection contracts |
| C07 | Python linkage + native rule branches verified | Trees M04 and heatmap M05.a/b delivered; later families M08/M09 | Shared geometry projects into equal summary slots or unequal cell-group centers; standalone/attached resize and registered path checks pass. M05.e verifies grouped and heatmap navigation; recheck later families. |
| C08 | Native index slots plus label layers retain repeated dotplot/matrixplot labels | Heatmap/ranked families; wider navigation | Dot/matrix slots, both orientations, optional zoom and duplicate-slot highlighting verified; extend checks with later families |
| C09 | Core 1.0 band rulers failed during initial WebGL rendering; the adopted Core 1.2 capability needs a focused recheck | Optional shaded row/column guides | Keep the native center crosshair until shaded-guide behavior is verified against Core 1.2. [PR #586](https://github.com/genome-spy/genome-spy/pull/586) records the upstream fix and regression evidence. |
| C10 | Heatmap bands and native gap navigation verified in their own viewports; clustermap retains overlays. Core 1.2 passes legacy hover checks. | Remaining clustermap track migration M05.f/M14.b.3 | Reuse the verified heatmap track helpers for clustermap and verify its own geometry/hover/navigation. No patched bundle or custom listeners. |
| C11 | Bundled Core 1.2 allocates one column's width to vertical multi-column legends; later columns clip. Large Scanpy scatter symbols also overflow a single column in short panels. | M07.a/b complete-chart closure, default legend fitting and M14.a guide layout | [Minimal native regression](../../tests/integrations/scanpy/browser/test_native_legend_extent.py) strictly xfails on 1.2.0. [Upstream fix PR #591](https://github.com/genome-spy/genome-spy/pull/591) includes before/after video comments; it is not adopted in the bundled runtime. Recheck after adopting a released Core fix before automatic column fitting; no local bundle patch. |
| C12 | Core 1.2 SVG export bends `linkShape="line"` control points; WebGL tree rendering is unaffected. | M14 vector-export fidelity for native tree links | The minimal straight-link SVG check in [browser/test_dendrogram.py](../../tests/integrations/scanpy/browser/test_dendrogram.py) strictly xfails. Keep this separate from verified WebGL/HTML layout; no local bundle patch. Upstream reproduction/fix and a released-runtime recheck remain open. |

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
