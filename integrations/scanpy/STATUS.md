# Scanpy implementation status

Updated: 2026-10-17. This is the current progress ledger; [PLAN.md](PLAN.md)
describes the work and acceptance criteria. Use the [shared lifecycle and
clearance rules](../README.md#plan-lifecycle). Dates below record observations,
not delivery promises.

## Current position and next work

**Available:** categorical/continuous 2D UMAP development preview, native sizing,
optional hover/zoom, linked interval highlighting/count and Python subset retrieval.
**Implemented families:** UMAP only. Scanpy **1.11.5** is the only accepted version;
bundled GenomeSpy Core is **1.0.0**. This is not full Scanpy plotting compatibility.

Implementation is in
[`src/genome_spy/integrations/scanpy/`](../../src/genome_spy/integrations/scanpy/).
Both `import genome_spy.integrations.scanpy as gsc` and
`import genome_spy.scanpy as gsc` expose the same functions. General library
imports remain independent of the optional scientific stack.

**Next ready slice: M02.a + M02.b**, shared grouped data access and dotplot
statistics. First write small independent fixtures for source precedence,
categories/repeated slots, numeric grouping, strict cutoffs, denominators,
missing values and log/scaling order. Reuse existing access/color functions;
extract focused shared helpers as needed. Then implement/review plain dotplot
(M02.c), validate the PBMC tutorial and resource envelope (M02.d), and move to
matrixplot (M03), trees (M04), heatmap (M05) and ranked summaries (M06).
Do not add brushing before basic plot reproduction passes review.

## Milestones

States apply to the stated scope; a closed preview is not a closed full family.
The completed structural update is M00.c/d, not a new plotting milestone.

| Milestone | State | Delivered evidence or remaining work |
| --- | --- | --- |
| M00 foundation/layout/lifecycle | Closed (foundation scope) | Signature/version fixtures, source/test/workflow layout, full inventory and shared lifecycle exist. Package relocation is `cec0428`; 122 integration checks, 20 browser checks, fresh linked notebook, built-wheel smoke test, Ruff and typing pass. |
| M01 UMAP/linked preview | Closed (preview only) | Runtime modules, three PBMC notebooks, semantic/reference/browser tests and resource baseline listed below. Parameter debt remains explicitly assigned to M07/M14. |
| M02 grouped access/dotplot | Ready (a/b) | Exact target call and hand-check cases in PLAN. No production dotplot yet; render/validation slices c/d follow data verification. |
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
- [Three real packaged-data workflows](README.md#workflow-notebooks).

Layout verification (`cec0428`): 122 integration checks and 20 browser checks
passed, as did the seven existing API-documentation checks, Ruff formatting/lint
and mypy. The linked notebook was executed in a fresh kernel and its chart
inspected. A built-wheel smoke test verified packaged modules, both lazy import
paths and chart authoring. The 50-entry ledger was checked against the pinned
inventory, and integration Markdown file links were checked.

The full documentation site and unrelated test suites were not rebuilt for this
move. Resource results are the retained October 17 baseline, not a new performance
measurement. No new plot family or Core capability was implemented by the move.

## Public callable coverage

The [pinned inventory](../../tests/integrations/scanpy/fixtures/api.json) has 50
entries: 45 plotting functions including aliases, three builders, two settings
helpers. Exactly one function is available as a partial preview; 47 plot/builder
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
| `dotplot` | Not implemented; next family | M02; trees M04; methods M13 |
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
