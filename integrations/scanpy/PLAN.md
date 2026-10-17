# Scanpy implementation plan

Status: UMAP development preview. This tracked plan supersedes the structural
roadmap formerly kept only in ignored `plans/scanpy_integration_plan.md`.
Local coverage audits and research prototypes remain useful evidence, but no
required implementation or validation may depend on their availability.

## Product contract

Users retain their Scanpy analysis and replace supported plotting calls:

```python
import scanpy as sc
import genome_spy.scanpy as gsc

pbmc = sc.datasets.pbmc68k_reduced()  # Includes a prepared UMAP embedding.
chart = gsc.pl.umap(pbmc, color=["louvain", "CD79A"], show=False)
chart.display(inline=True)
```

For a user's own dataset, preprocessing, neighbors, `sc.tl.umap`, clustering,
and differential expression remain explicit Scanpy operations before plotting.
The plotting adapter never silently recomputes those results. Use `genome_spy`, the existing Python package namespace.

The destination is all public Scanpy plot families, including dendrograms and
compound plots. The delivery order below is a sequence of independently reviewed
families, not a permanent UMAP-only scope. The current support table is in the
[compatibility guide](../../docs/integrations/scanpy/index.md); the pinned
[API inventory](../../tests/integrations/scanpy/fixtures/api.json) lists 50 public
callables, including aliases, builders, and settings helpers. An entry in the
inventory is not an implemented function.

Scanpy 1.11.5 is the currently tested and accepted version. Widen the declared
range only after signature/default, semantic, visual, interaction, and resource
checks pass for every supported version. Keep Scanpy optional and base/namespace
imports lightweight.

## Code and ownership

The [workspace README](README.md) maps every current runtime file. Installed code
stays under `src/genome_spy/scanpy/`; workflow notebooks belong in this integration
workspace; all Scanpy validation belongs in `tests/integrations/scanpy/`.
`docs/integrations/scanpy/` is user documentation, not an implementation package.

Each plotting family follows this path:

1. Public Scanpy-shaped function: validate names/defaults/aliases and supported
   options before scientific extraction; handle native display/return behavior.
2. Pure Python preparation: select the required AnnData columns/results and
   produce detached tables plus plotting metadata. Do not construct
   charts, inspect rendered artists, mutate the input, or import test/prototype
   modules here.
3. GenomeSpy authoring: build marks, axes, labels, legends, composition, and
   explicit interactions from prepared data, without reading AnnData again.
4. Existing chart/widget delivery: JSON, notebook display, HTML, and ordinary
   parameter synchronization. Integration notebooks need no connection tasks.

UMAP has explicit `_umap_data.py`, `_umap_colors.py`, `_umap_style.py`,
`_umap_chart.py`, and `_umap_interactions.py` modules. Data access uses public
AnnData vector access and the existing observation/embedding projection. It
contains no analysis, Matplotlib layout emulation, or global style settings.
The chart module uses actual native color scales and their guides; it does not
encode prepainted RGB values or create hidden guide marks. Missing numeric values
use a separate visible native point layer behind valid measurements.

Native color support is the deliberate rendering boundary: accept GenomeSpy
scheme names and opaque CSS color names/hex values. Reject Matplotlib colormap
objects/names without a native equivalent, color cyclers, RGB(A) tuples,
Matplotlib shorthand colors, and entry alpha. Native interpolation can differ
from Matplotlib LUT bins; do not recover exact colors by sampling Matplotlib.
Numeric bounds, source precision, and draw order still have independent checks.
Named schemes with a custom missing-category legend are deferred; explicit CSS
palettes support that legend now. Native dimensions default to 300 by 300 logical
pixels, with fixed point-to-pixel conversion (100/72), independent of rcParams.

For dotplot, start with `_dotplot_data.py` and `_dotplot_chart.py` and review the
plain chart before adding brushing/linking. Keep public signatures discoverable;
if `pl.py` becomes unwieldy, use an explicit `pl/` package with named exports.
Extract shared version/input helpers only when a second production family uses
them. Do not add a registry, adapter base class, plugin dispatcher, or a general
cross-library framework now.

Upstream public computation may be reused when its semantics match the required
result. Review source/provenance and test the resulting values independently.
Write independently tested preparation when public APIs do not expose the needed
computation. Do not copy prototype geometry or call upstream plotting to obtain
production inputs. Keep all browser/core changes upstream; adopt released
capabilities after testing the bundled runtime.

## Per-family completion gates

A family is available only after all of these are reviewed:

- **Contract:** original argument names, supported defaults, aliases, conflict
  rules, and clear unsupported-option errors. Matplotlib `ax`/`return_fig` stay
  omitted with targeted errors; native chart methods replace artist styling.
  `show` is explicit; unsupported image `save` requests error, while native
  HTML/JSON export works. Do not silently discard scatter kwargs.
- **Data semantics:** independently checked raw/layer precedence, gene symbols,
  category order/palettes, missing values, masks, duplicate labels, sparse data,
  views/backed inputs, thresholds, denominators, normalization order, and supplied
  coordinates. Densify selected columns only. Define cache reuse and mutation
  behavior explicitly; UMAP currently reads snapshots without writing caches.
- **Complete charts:** compare axes, labels, legends, native palette interpolation, point/mark
  footprints, and draw order, with measured registered overlays. Record export
  DPI, fonts, and browser rasterization limits; an image mean alone is not parity.
- **Interaction/delivery:** observe real hover, brush/selection, linked views,
  clearing, navigation, Python retrieval, notebook reruns/disposal, and offline
  HTML for the supported modes. Preserve initial appearance unless an interaction
  is explicitly configured. Observation selections retain meaningful source IDs.
- **Resources:** realistic sparse/large-data workloads, allocation guards, payload
  size, render/interaction latency, and retained memory. Record hardware and a
  tested envelope instead of hardware-independent timing promises.
- **Workflow/review:** a small real Scanpy dataset and an adapted official tutorial
  workflow, clear provenance, current support documentation, focused tests, lint,
  formatting, and source typing. No ignored benchmark dependency or runtime import
  from test tooling. Keep commits thematic and reviewable.

## Phased delivery

| Phase | Current evidence and next work | Acceptance |
| --- | --- | --- |
| 0: Compatibility foundation | Implemented: pinned signatures/defaults, optional dependency guard, synthetic semantic fixtures, explicit reference generation, and resource baseline. This reorganization supplies a tracked plan and discoverable source/test/notebook boundaries. | A fresh clone can find the source and run validation without ignored artifacts; no Scanpy-specific helpers in generic `tools/`; no integration notebooks in the generic notebook folder. |
| 1: Categorical/continuous UMAP | Implemented preview: supplied coordinates, selected expression/metadata, native axes/guides, hover, optional zoom, native sizing, and real tutorial examples. Typography, advanced normalization, graph overlays, 3D, and some styling remain documented limits. | Preserve all existing semantic and complete-chart checks; keep unsupported values explicit. A passing preview is not a claim of complete Scanpy parameter support. |
| 2: Linked UMAP interaction | Implemented preview: one interval owner, linked highlighting/count, normal widget parameter synchronization, and Python `selection_mask`. Additive point selection and forthcoming faceting require evaluation against a published Core release. | Plain brushing is discoverable; native count and returned rows agree, including coincident observations and half-open edges; no asynchronous notebook setup or local Core patches. Recheck panel/gap/axis navigation when adopting faceting. |
| 3: Dotplot and matrixplot, with dendrograms | Next implementation: pure group summaries, feature slots/order, fraction/mean definitions, scaling order, native guides, and Python-computed tree layout. Reuse compatible supplied dendrogram results; otherwise compute missing tree results explicitly under a documented cache/mutation policy. | Match thresholds, denominators, category/gene order, normalization and supplied statistics. Tree leaves align with rows/columns and preserve supplied ordering/results; no embedding/ranking rerun. Adapt the official tutorial's grouped plots. |
| 4: Heatmaps and ranked-gene variants | Observation-level heatmaps and the corresponding ranked dotplot/matrixplot/heatmap forms, using supplied rank results. | Preserve cell/group/feature order, repeated feature slots, group annotations and trees; missing/stale rankings error clearly. Check large tile payloads and readable labels. |
| 5: Remaining public plots | Other embeddings/PCA, diagnostics/rankings, distributions/tracks, trajectories/graphs, spatial/density, and builder semantics, ordered by demonstrated feasibility and user value. | Close the inventory one family and parameter group at a time. Violin densities and track data are computed in Python, while filled geometry must use a supported native capability; prototype recipes are not production acceptance. |

For every new family, open a small design slice with an original Scanpy call,
its GenomeSpy equivalent, supported/unsupported parameters, preparation outputs,
mutation/cache contract, native capability requirements, and concrete checks.
Implement preparation and semantic tests before chart authoring, then complete
chart/interaction/resource checks. Update the support matrix and tutorial notebook
in the same slice. Avoid placeholder public functions for unimplemented plots.

## Documentation design before notebook publication

Workflow notebooks are canonical runnable examples in
`integrations/scanpy/notebooks/`. They are downloadable from the existing guide;
rendering them as documentation pages is a separate design and implementation
step. This reorganization does not change the site navigation or install a new
notebook renderer.

Recommended information architecture for review:

```text
Integrations
  Overview: actual integrations, status, tested upstream versions
  Scanpy
    Start here: analysis ownership, installation, first plotting replacement
    Compatibility: supported plots/options, versions, return/save/styling rules
    Workflows
      Core plotting tutorial
      Advanced plotting tutorial
      Linked brushing and Python subset retrieval
    API reference
```

Before implementing this, review a landing-page layout and one workflow-page
layout. Decide the navigation, status/version labels, code visibility, chart
placement, notebook-download/run links, mobile/large-chart behavior, and how a
static page explains Python-only retrieval. Do not publish empty library cards.

Then choose and prove a rendering path using the existing Sphinx setup. Prefer
one canonical notebook source with an explicit pinned preparation step and
reusable browser-native chart artifacts, so the notebook and docs cannot drift.
Do not run unbounded analysis or downloads during an ordinary docs build. An
interactive chart/count can run in static documentation; Python subset retrieval
must clearly require a notebook kernel. Existing generic workflow rendering may
be reusable after this design, but does not settle notebook rendering or the
integration page layout by itself.

Publication acceptance: approved layouts, one real tutorial page rendered from
its canonical source, a working notebook download, observed native interactions,
clear Python/static boundaries, reproducible artifacts, and no added Scanpy
requirement for normal library imports. Keep the general visualization skill and
focused agent guides general; integration policy and examples stay here.
