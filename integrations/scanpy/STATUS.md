# Scanpy implementation status

Updated: 2026-10-19. This is the current progress ledger; [PLAN.md](PLAN.md)
describes the work and acceptance criteria. Use the [shared lifecycle and
clearance rules](../README.md#plan-lifecycle). Dates below record observations,
not delivery promises.

The 44 unpublished Scanpy commits were cleaned of generated test media and saved
notebook execution state before publication. Code, tests and commit authors/messages
were preserved; evidence commit IDs below refer to the cleaned history. Both
workflow tests and Ruff checks pass. Local notebook edits remain unchanged.

## Current position and next work

**Available:** shared categorical/continuous 2D embeddings (UMAP, t-SNE, diffusion
maps, saved graph layouts, PCA and custom bases), dotplot/matrixplot and cell heatmaps with dendrograms,
supplied numeric matrices, clustermaps, standalone dendrograms and correlation matrix development previews.
Stored ranking/score panels and ranked dotplot/matrixplot/heatmap previews now
reuse Scanpy's public result getter and the existing expression plot functions.
UMAP includes native sizing, optional hover/zoom, linked interval highlighting/count
and Python subset retrieval. Dotplot includes index-scaled slots, grouped summaries,
brackets, native size/color guides and optional summary hover. Matrixplot reuses
grouped access/means and native layout, with one-pass scaling, authoritative
`values_df`, tiles and optional summary hover. Trees reuse `sc.tl.dendrogram`
computation/results, with structural checks and native rule rendering.
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
**Available public entries: 19**, including the stored-ranking previews below. Scanpy **1.11.5** is the only accepted version;
bundled GenomeSpy Core is **1.0.0**. This is not full Scanpy plotting compatibility.

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

Supplied matrices reserve long-label space once, including when axis titles are
present. The layout regression passed **15 matrix browser checks** and **30
matrix/workflow Python checks**, plus Ruff and mypy. The expression notebook was
reloaded from disk and all five code cells rerun in the visible Jupyter tab;
all four charts rendered with the corrected matrix placement. No plan clearance
changes follow from this fix.

**Next ready slice: M07.b scatter x/y/basis plotting.** M06.a–d have a stored-result preview; larger and
chunked tile transport remains M05.d.
Dotplot brushing remains deferred until the
plain-chart preview has user review; this delivery does not add it.

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
No plan becomes eligible for clearance from this additional interaction slice;
M05.c clustermap remains next.

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
no Core patch is used. M05.c remains next and no plan is eligible for clearance.

## M05.f category-strip tooltips — blocked on a released Core fix

Heatmap and clustermap originally set `tooltip=None` on their annotation strips.
They now configure the existing strips with GenomeSpy's default handler and the
category field; `hover=False` disables strip and tile tooltips. Existing geometry,
labels, color scales and data stay in place. No extra marks or listeners are added.

Bundled Core 1.0.0 still rejects rendered hits outside ordinary plot bounds, so
these strip tooltips are **not yet usable**. The independent native reproduction
shows an identical rectangle working inside the plot and failing outside it with
`clip="never"`. [Core PR #587](https://github.com/genome-spy/genome-spy/pull/587)
contains the upstream fix, regression tests and required release note. Its
description embeds an observed before/after recording; recording assets and
helpers are not committed. The fixed browser reproduction shows both tooltips.
The integration bundle remains unchanged.

Validation: **116 focused semantic/API checks** pass. Browser checks pass for
disabled strip hover and existing cell hover in both orientations and clustermap;
the three enabled-strip cases are precise expected timeout failures only for
Core 1.0.0. The upstream fix passes 66 interaction/facet/identity tests, build,
TypeScript, lint and Changesets checks. Python formatting/lint and mypy pass.
The unrelated full Python suite and documentation build were not rerun.

Clearance: retain. M14 owns adopting a released Core containing #587; then rerun
the three strip cases before/after navigation, remove expected failures and the
known-limit notices, and verify the PBMC notebook. M07.b is the next independent
slice. This records a native capability blocker, not a completed hover feature.

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
The [expression workflow](notebooks/scanpy_expression.ipynb) now has ten code cells
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

Verified preview: `rank_genes_groups_dotplot` and `rank_genes_groups_matrixplot`
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

Clearance: retain the live plan and status. M06's preview is verified; M13 retains
builders and M14 the named compatibility limits. M07.b scatter is
the next ready slice. No working plan is cleared.

## Review follow-up and M07.a shared 2D embeddings

Three Sol reviewers checked reuse, self-containment, readability and YAGNI. Two
found no significant structural issue. The reuse review identified two redundant
reads, fixed in `ff87075`: statistic-colored matrixplots validate feature lookup on zero
rows and read only real group annotations; one detached unfiltered ranking table
serves marker selection and color values. Strict marker thresholds do not remove
the statistic pairs needed for other groups. No cache is shared across calls.
The metadata path retains raw/layer/symbol validation, categories and duplicate
slots. Getter-count and cross-group-value regression tests cover both changes.

M07.a generalizes the three UMAP modules in place to `_embedding_data.py`,
`_embedding_chart.py` and `_embedding_interactions.py`, with shared styles.
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

The [UMAP notebook](notebooks/scanpy_umap.ipynb) now has eleven code cells. New
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

Clearance: retain the live plan and status. M07.a's bounded preview is delivered;
M07.b scatter is next. Existing family/renderer limits retain their named owners.
No working plan becomes eligible for clearance from this slice.

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
| M05 heatmap/matrix/clustermap | In progress; three bounded previews delivered | Heatmap/matrix/shared interactions and clustermap values, masks, two Python trees, annotation tracks, native hover and PBMC workflow are covered below. Larger/chunked transport remains M05.d; broader kwargs and native delivery remain M14. |
| M06 ranking/ranked summaries | Verified preview; compatibility limits retained | M06.a–d select stored ranks, reuse dot/matrix/heatmap charts and color summary plots with six saved statistics. Nonfinite/missing-pair behavior and filtered score panels remain M14; native builders remain M13. |
| M07 embeddings/scatter/PCA | In progress; M07.a shared 2D preview delivered | Generic and named bases, stored components/layouts/variance labels, shared point rendering and selection retrieval. M07.b scatter is next; PCA diagnostics M07.c and remaining options M07.d stay open. |
| M08 violin/stacked/ranked | Planned; filled rendering blocked | Data/density work can proceed; full native filled geometry needs a released capability (C01). |
| M09 tracks/ranked tracks | Planned; filled rendering blocked | Profile preparation can proceed; native filled geometry needs C01. |
| M10 QC diagnostics | Planned | Highest expression, variable genes, legacy dispersion and Scrublet distributions. |
| M11 trajectories/graphs/series | Planned | Stored DPT/PAGA, graph layouts, series/simulation, return/side-effect contracts; evaluate C04 paths. |
| M12 density/spatial | Planned; full spatial blocked | Density uses stored analysis; image-backed spatial requires C02. |
| M13 builders | Planned | DotPlot/MatrixPlot/StackedViolin semantic chains delivered with their parent families; method ledger below. |
| M14 compatibility/docs/release | Planned | Close parameters/capabilities, versions/exports, designed workflow publication and full API evidence. |

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

M02 is closed only for this plain-chart preview. M03 is ready. The maintained
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
were not repeated for this layout adjustment; M05 remains next.

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
preview. M05 is next; no working document is newly eligible for clearance.

## M05.a/b cell heatmap preview

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
M05 stays open for matrix/clustermap and larger/chunked transport. No working
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
runtime behavior is unchanged. M05 remains next; no working plan is eligible
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
edits were untouched. M05 remains next and no working plan is newly eligible for
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
edits remain outside the change. M05 remains next; no plan is newly clearable.

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

M05.a/b previews are verified; M05 remains open for clustermap and transport.
Clearance: **retain** the live plan/status and unique reference/resource evidence.
The next ready item is M05.c; this preview does not close the full family.

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
M05 remains open for M05.d transport and M14 option closure. M06 stored-ranking
selection and ranked summary wrappers are next; no plan is eligible for clearance.

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
suite and documentation build were not rerun. M06 remains next; no plans cleared.

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
helpers. Nineteen functions are available as partial previews; 29 plot/builder
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
| `pca_loadings` | Not implemented | M07 |
| `pca_overview` | Not implemented | M07 |
| `pca_scatter` | Alias of the shared pca preview | M07.a; same limits as pca |
| `pca_variance_ratio` | Not implemented | M07 |
| `rank_genes_groups` | Preview: stored score panels | M06.a–c; filtered/nonfinite panels and presentation debt M14 |
| `rank_genes_groups_dotplot` | Preview: expression/statistic colors and expression fractions | M06.a–d; compatibility limits M14, builder M13 |
| `rank_genes_groups_heatmap` | Preview: individual-cell expression | M06.a–c; shares parent heatmap limits |
| `rank_genes_groups_matrixplot` | Preview: expression means or stored statistics | M06.a–d; compatibility limits M14, builder M13 |
| `rank_genes_groups_stacked_violin` | Not implemented | M08; rank access M06 |
| `rank_genes_groups_tracksplot` | Not implemented | M09; rank access M06 |
| `rank_genes_groups_violin` | Not implemented | M08; rank access M06 |
| `ranking` | Preview: supplied score attributes/dictionaries | M06.c; shared native rank labels, dense indices only |
| `scatter` | Not implemented | M07 |
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
| Graph edges/arrows, scale_factor, outlines, broader markers/guide locations | Nondefault forms reject | M07.d |
| norm/vcenter/callable bounds | Nondefault forms reject; Matplotlib objects remain outside boundary | M07.d/M14.c |
| Backed/lazy expression; named scheme with NA legend; category/NA label collision | Explicit current restrictions | M14.c |
| 3D, font atlas/weight/outline and complete typography | Native gaps/limits | M14.a; C03/C05 |
| Image save/autosave | Inactive form only; use native HTML/JSON save | M14.c |
| ax/cax/return_fig, artist methods, Matplotlib color/global settings | Intentional native rendering boundary | Maintained contract, not pending artist emulation |

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

Audit: bundled Core/schema **1.0.0**, rechecked October 19 for native rules,
formula transforms, excluded scales/axes and tree alignment. Native marks are rect, point,
rule, tick, text, link and arrow. Recheck the installed API before implementing
an affected slice; upcoming releases are triggers to investigate, not assumptions.

| ID | Gap or available capability | Affected work | Resolution/recheck trigger |
| --- | --- | --- | --- |
| C01 | No native filled-area/polygon primitive in bundled schema | Full violin/stacked/tracks M08/M09 | Released filled geometry and density/profile chart tests; no custom trial geometry promotion |
| C02 | No native raster/image primitive | Full spatial M12 | Released image capability with crop/aspect/zoom registration tests |
| C03 | No native 3D projection | 3D embedding options M07/M14 | Released capability or explicit product scope decision; keep unresolved until then |
| C04 | No dedicated line/path mark in bundled mark inventory | Series/graph/path M11 | Verify native rule/link segments can preserve required semantics; otherwise upstream released capability |
| C05 | Font/outline/normalization/NA-guide limits | Parameter closure M07/M14 | Per-option released API inspection and complete-chart tests |
| C06 | Faceting/composition improvement announced, not adopted | UMAP and repeated panel layout | Released version/schema; recheck plot/gap/axis zoom and brush scope/count |
| C07 | Python linkage + native rule branches verified | Trees M04 and heatmap M05.a/b delivered; later families M08/M09 | Shared geometry projects into equal summary slots or unequal cell-group centers; standalone/attached resize and registered path checks pass. M05.e verifies grouped and heatmap navigation; recheck later families. |
| C08 | Native index slots plus label layers retain repeated dotplot/matrixplot labels | Heatmap/ranked families; wider navigation | Dot/matrix slots, both orientations, optional zoom and duplicate-slot highlighting verified; extend checks with later families |
| C09 | Native band rulers fail during initial WebGL rendering with no cursor coordinate; center/line rulers render successfully | Optional shaded row/column guides | Use a native center crosshair now. Upstream [PR #586](https://github.com/genome-spy/genome-spy/pull/586) contains the fix, regression test and before/after recording. Adopt only after a released runtime upgrade; the bundled Core remains unchanged. |
| C10 | Visible marks outside ordinary plot bounds cannot be picked in bundled Core 1.0.0 | Heatmap/clustermap category-strip hover M05.f | Native tooltip settings are prepared. Upstream [PR #587](https://github.com/genome-spy/genome-spy/pull/587) contains the fix, tests and before/after recording. Adopt a released fix in M14, rerun the three expected failures, and remove known-limit notices; no patched bundle or custom listeners. |

Python computation alone does not close a renderer gap. Local Core patches are
excluded. Historical violin, filled-track and tree recipes are experimental
research; only reviewed numerical ideas or evidence may be reused with provenance.

## Plan clearance ledger

No research artifacts are deleted by this roadmap update. Paths below can be
absent in a fresh clone; active delivery depends only on tracked files.

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
