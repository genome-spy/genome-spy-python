# Scanpy implementation status

Updated: 2026-10-17. This is the current progress ledger; [PLAN.md](PLAN.md)
describes the work and acceptance criteria. Use the [shared lifecycle and
clearance rules](../README.md#plan-lifecycle). Dates below record observations,
not delivery promises.

## Current position and next work

**Available:** categorical/continuous 2D UMAP and plain dotplot development previews.
UMAP includes native sizing, optional hover/zoom, linked interval highlighting/count
and Python subset retrieval. Dotplot includes grouped summaries, brackets and native
size/color guides, without interactions yet.
**Implemented families:** UMAP and dotplot (partial). Scanpy **1.11.5** is the only accepted version;
bundled GenomeSpy Core is **1.0.0**. This is not full Scanpy plotting compatibility.

Implementation is in
[`src/genome_spy/integrations/scanpy/`](../../src/genome_spy/integrations/scanpy/).
Use `import genome_spy.integrations.scanpy as gsc`. This is the sole integration
namespace; there is no parallel compatibility package. General library imports
remain independent of the optional scientific stack.

**Next ready slice: M03.a–c**, matrixplot using the verified grouped access and
means. Preserve authoritative `values_df` scaling/order, then build and validate
native tiles on the same PBMC marker workflow. Trees attach in M04, heatmaps in
M05 and ranked summaries in M06. Dotplot brushing remains deferred until the
plain-chart preview has user review; this delivery does not add it.

## Milestones

States apply to the stated scope; a closed preview is not a closed full family.
The completed structural update is M00.c/d, not a new plotting milestone.

| Milestone | State | Delivered evidence or remaining work |
| --- | --- | --- |
| M00 foundation/layout/lifecycle | Closed (foundation scope) | Signature/version fixtures, sole integration namespace, source/test/workflow layout, full inventory and shared lifecycle exist. Initial relocation is `cec0428`; current verification below. |
| M01 UMAP/linked preview | Closed (preview only) | Runtime modules, one PBMC plotting notebook, semantic/reference/browser tests and resource baseline listed below. Parameter debt remains explicitly assigned to M07/M14. |
| M02 grouped access/dotplot | Closed (plain-chart preview) | Shared access/statistics, public dotplot, native dots/labels/brackets/guides, 11 complete frozen chart cases, real PBMC workflow and sparse/browser resource check. See retained evidence and explicit limits below; trees/builders/interactions are not closed. |
| M03 matrixplot | Planned | Reuse grouped access/means; authoritative values_df, scaling and native tile chart. |
| M04 trees/correlation | Planned | Python computation/cache policy, shared rule layout, standalone and attached trees. No native tree capability blocker. |
| M05 heatmap/matrix/clustermap | Planned | Observation permutations, annotations, clustering contracts and large tile policy. |
| M06 ranking/ranked summaries | Planned | Stored rank selection and reusable dot/matrix/heatmap wrappers. |
| M07 embeddings/scatter/PCA | Planned | Shared 2D embeddings/alias/PCA diagnostics, then remaining UMAP options. |
| M08 violin/stacked/ranked | Planned; filled rendering blocked | Data/density work can proceed; full native filled geometry needs a released capability (C01). |
| M09 tracks/ranked tracks | Planned; filled rendering blocked | Profile preparation can proceed; native filled geometry needs C01. |
| M10 QC diagnostics | Planned | Highest expression, variable genes, legacy dispersion and Scrublet distributions. |
| M11 trajectories/graphs/series | Planned | Stored DPT/PAGA, graph layouts, series/simulation, return/side-effect contracts; evaluate C04 paths. |
| M12 density/spatial | Planned; full spatial blocked | Density uses stored analysis; image-backed spatial requires C02. |
| M13 builders | Planned | DotPlot/MatrixPlot/StackedViolin semantic chains delivered with their parent families; method ledger below. |
| M14 compatibility/docs/release | Planned | Close parameters/capabilities, versions/exports, designed workflow publication and full API evidence. |

The M01 preview is recorded in `c28cee3` and `2a136b4` with earlier implementation
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
- [Combined real packaged-data workflow](README.md#plotting-workflow): basic
  plotting, linked brushing/Python retrieval, then customization. Shared setup
  and duplicate charts from the three earlier notebooks have been consolidated.
  All UMAP examples enable x/y zoom and panning. Linked brushing uses Shift-drag
  in the first panel so ordinary dragging remains available for navigation.

UMAP preview baseline (`cfc01b7`): 119 integration checks and 20 browser checks pass,
as do Ruff formatting/lint and mypy. The workflow test executes every cell,
checks unchanged source UMAP coordinates, and reruns Python retrieval for a
nonempty selection. The combined notebook renders in a fresh kernel/browser.
A built-wheel smoke test confirms that the compatibility package is absent,
the sole integration namespace imports lazily, and UMAP chart authoring works.
Notebook format, documentation/download/CI paths, and all 50 inventory rows were
also checked. The shared source/test links above retain the evidence.

The full documentation site and unrelated test suites were not rebuilt for this
cleanup. Resource results are the retained October 17 baseline, not a new
performance measurement. No new plot family or Core capability was implemented.

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
[shared color validation](../../src/genome_spy/integrations/scanpy/_colors.py).
Chart construction takes detached tables, not AnnData. It uses released points,
rules and text; no Core patches, custom polygon recipes or benchmark imports.

Delivered: category/feature ordering, repeated feature slots, brackets on either
orientation, mean/percentage guides, clipped power area mapping, numeric color
bounds, supplied color tables, native sizing and explicit display/export errors.
Scanpy 1.11.5 applies scaling again after transposing the display table; supplied
color tables skip only the constructor pass. Tests retain both behaviors.
The combined [PBMC notebook](notebooks/scanpy_plotting.ipynb) now adds the core
tutorial marker dictionary against existing `bulk_labels`, after basic UMAP and
before linking/customization. No clustering or ranking is added to the example.

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
  timing limits. The [benchmark](../../tests/integrations/scanpy/benchmark_dotplot.py)
  is explicit and independent of ignored research.

Validation: 222 integration checks passed, followed by all 43 dotplot/workflow
checks including the added missing-value/raw-access and constant-paint cases
(225 distinct integration checks covered in total). All 33 integration browser
checks passed, including UMAP regression checks; the final bracket endpoint/stroke
adjustment and constant-paint case have their own browser reruns (34 distinct
browser checks covered). Ruff and mypy pass.
The combined notebook was run from a fresh live kernel and its PBMC dotplot viewed.
The full documentation site and unrelated test suites were not rebuilt.

Label-placement correction (October 17): rotated text now uses screen-position
offsets, so gene labels clear the matrix and marker-group labels stay centered
outside their brackets. Scanpy's bracket coordinates are unchanged. Browser
checks measure exported text bounds for vertical/horizontal top labels, repeated
genes, unequal label lengths and swapped axes; the new clearance check fails with
the original offsets. All 15 dotplot browser checks and 43 dotplot/workflow checks,
Ruff and mypy pass. The packaged-PBMC notebook was rerun and inspected in Jupyter.
Resource measurements and unrelated families were not rerun for this layout fix.

Preview limits, retained in the [compatibility guide](../../docs/integrations/scanpy/index.md#dotplot-compatibility):
unused/empty groups error; all-zero fractions require explicit `dot_max=1`;
missing statistics retain slots but do not paint; no dotplot interactions yet.
Native Lato, guide layout, line-break flattening and Vega reds differ from the
Matplotlib reference. `figsize` is a documented native plot/guide budget rather
than a fixed outer canvas. Full typography/palette/export/access closure remains
M14; trees remain M04; `DotPlot` and supplied `dot_size_df`/style chains remain M13.
No unimplemented option is silently ignored. C08's dotplot slot handling is
verified with native text labels; other grouped families still need their checks.

M02 is closed only for this plain-chart preview. M03 is ready. The maintained
source, notebook, tests, references and compatibility contract are retained;
there is no per-slice working plan to clear and no research artifacts are deleted.

## Public callable coverage

The [pinned inventory](../../tests/integrations/scanpy/fixtures/api.json) has 50
entries: 45 plotting functions including aliases, three builders, two settings
helpers. Two functions are available as partial previews; 46 plot/builder
entries remain unimplemented. The two settings helpers are external renderer
exceptions. This count measures entry availability, not parameter completeness.
No placeholder functions are exported for planned work.

| Public entry | Availability | Delivery milestone |
| --- | --- | --- |
| `DotPlot` | Not implemented | M13 (after M02/M04) |
| `MatrixPlot` | Not implemented | M13 (after M03/M04) |
| `StackedViolin` | Not implemented | M13 (after M08) |
| `clustermap` | Not implemented | M05 |
| `correlation_matrix` | Not implemented | M04 |
| `dendrogram` | Not implemented | M04 |
| `diffmap` | Not implemented | M07 |
| `dotplot` | Partial plain-chart preview; limits above | M02; trees M04; methods M13 |
| `dpt_groups_pseudotime` | Not implemented | M11 |
| `dpt_timeseries` | Not implemented | M11 |
| `draw_graph` | Not implemented | M07 |
| `embedding` | Not implemented | M07 |
| `embedding_density` | Not implemented | M12 |
| `filter_genes_dispersion` | Not implemented; legacy | M10 |
| `heatmap` | Not implemented | M05 |
| `highest_expr_genes` | Not implemented | M10 |
| `highly_variable_genes` | Not implemented | M10 |
| `matrix` | Not implemented | M05 |
| `matrixplot` | Not implemented | M03; trees M04; methods M13 |
| `paga` | Not implemented | M11 |
| `paga_adjacency` | Not implemented | M11 |
| `paga_compare` | Not implemented | M11 |
| `paga_path` | Not implemented | M11 |
| `pca` | Not implemented | M07 |
| `pca_loadings` | Not implemented | M07 |
| `pca_overview` | Not implemented | M07 |
| `pca_scatter` | Not implemented; pca alias | M07 |
| `pca_variance_ratio` | Not implemented | M07 |
| `rank_genes_groups` | Not implemented | M06 |
| `rank_genes_groups_dotplot` | Not implemented | M06 |
| `rank_genes_groups_heatmap` | Not implemented | M06 |
| `rank_genes_groups_matrixplot` | Not implemented | M06 |
| `rank_genes_groups_stacked_violin` | Not implemented | M08; rank access M06 |
| `rank_genes_groups_tracksplot` | Not implemented | M09; rank access M06 |
| `rank_genes_groups_violin` | Not implemented | M08; rank access M06 |
| `ranking` | Not implemented | M06 |
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
| `tsne` | Not implemented | M07 |
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

| Builder surface (all three classes) | Current state | Completion evidence required |
| --- | --- | --- |
| Constructor signatures/defaults and native result delivery | Not implemented | Pinned class signatures plus family semantic/chart tests, M13 |
| add_dendrogram/add_totals/swap_axes | Not implemented | Chain return behavior, leaf/order/totals alignment, M04/M13 |
| style/legend and useful public defaults/constants | Not implemented | Family-specific option and chain tests, M13 |
| get_axes/figure/artist access | Intentional renderer boundary; builders do not yet exist | Explicit errors and native alternative, M13 |
| make_figure/show(return_axes)/savefig | Contract to resolve before builders ship | Native delivery/export decision and tests, M13/M14 |

## Native capability ledger

Audit: bundled Core/schema **1.0.0**, October 17. Native marks are rect, point,
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
| C07 | Python linkage + native rule branches are available | Trees M04 | No renderer blocker; implement shared computation/layout and alignment checks |
| C08 | Repeated labels require distinct positional slots | Dot/matrix/heatmap/ranked families | Validate native label mapping or semantic label panels, including zoom/resize; do not collapse labels |

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
