# Scanpy integration workspace

Start with [status and next work](STATUS.md), the [implementation plan](PLAN.md), and the
[current compatibility guide](../../docs/integrations/scanpy/supported.md).
Use `import genome_spy.integrations.scanpy as gsc`, then `gsc.pl.umap(...)`,
`gsc.pl.scatter(...)`, `gsc.pl.dotplot(...)`, `gsc.pl.matrixplot(...)`, `gsc.pl.heatmap(...)`, `gsc.pl.matrix(...)`, `gsc.pl.dendrogram(...)` or
`gsc.pl.correlation_matrix(...)` or `gsc.pl.clustermap(...)`.
Stored doublet-score QC uses `gsc.pl.scrublet_score_distribution(...)`.
Stored embedding density uses `gsc.pl.embedding_density(...)` after explicit
`sc.tl.embedding_density(...)` preparation.
Highest-expression QC uses `gsc.pl.highest_expr_genes(...)` on count data.
Stored rankings add `gsc.pl.rank_genes_groups(...)`, `gsc.pl.ranking(...)`, and
the ranked dotplot/matrixplot/heatmap wrappers.
`gsc.pl.DotPlot(...)` chains tree/totals, axes, dot styles and native guides on
the existing dotplot path. Use `.to_chart()` for native composition and saving.
`gsc.pl.pca_loadings(...)` and `gsc.pl.pca_variance_ratio(...)` reuse the ranking
panels for stored PCA results.
`gsc.pl.pca_overview(...)` composes these diagnostics with the existing PCA scatter.
`gsc.pl.highly_variable_genes(...)` and the legacy `filter_genes_dispersion(...)`
show stored gene-selection diagnostics without rerunning analysis.
Scanpy still owns preprocessing, embedding, clustering, and gene ranking.

The focused [UMAP](guides/umap.ipynb), [expression](guides/expression.ipynb),
[PCA](guides/pca.ipynb) and [ranked-gene](guides/ranked.ipynb)
guide notebooks each supply their rendered page and notebook download. The longer
notebooks under `notebooks/` remain the development workflows. Documentation builds execute only
the guide's page examples; `jupyter-only` cells are shown without running them.
`gsc.pl.sim(...)` displays stored simulation realizations using the time-series
point and heatmap renderers; it never runs simulation.
`gsc.pl.dpt_groups_pseudotime(...)` reuses the point renderer for stored DPT
metadata, after explicit Scanpy preparation in the expression notebook.
`gsc.pl.dpt_timeseries(...)` applies saved DPT row indices to X and reuses the
heatmap/point renderers for expression profiles.
`gsc.pl.paga(...)` renders stored undirected group connectivity with native graph
marks. `gsc.pl.paga_compare(...)` composes it with stored embedding points
and shared coordinates, using explicit normal on-data labels. Its palette applies
to both panels; separate comparisons compose with independent navigation. Scanpy computes PAGA explicitly; its public no-plot API supplies missing
layout coordinates without reading expression or creating figures.
`gsc.pl.paga_adjacency(...)` reads explicitly assigned top-level adjacency/tree
matrices, showing native matrix tiles or connectivity strips with as_heatmap=False.

When resuming work in another chat, read [the current queue](STATUS.md#current-work-queue)
and inspect recent commits and uncommitted changes first. STATUS owns the active
slice, completed increments and remaining gates; PLAN owns scope and acceptance.
Preserve work already in progress instead of restarting it from an older chat
summary. The source map below describes the working checkout, not release readiness.

The implementation lives in the installable [source package](../../src/genome_spy/integrations/scanpy/),
not in this workspace or the documentation:

| Source | Responsibility |
| --- | --- |
| [__init__.py](../../src/genome_spy/integrations/scanpy/__init__.py) | Lightweight explicit namespace exports. |
| [pl.py](../../src/genome_spy/integrations/scanpy/pl.py) | Public signatures, plot-specific validation and native display/save handling. |
| [_guards.py](../../src/genome_spy/integrations/scanpy/_guards.py) | Shared option guards and lazy optional dependency/version checks used directly by plotting functions and builders. |
| [_grouped_builder.py](../../src/genome_spy/integrations/scanpy/_grouped_builder.py) | Concrete group ordering, tree/totals replacement and axis state shared by DotPlot and MatrixPlot. |
| [_dotplot_builder.py](../../src/genome_spy/integrations/scanpy/_dotplot_builder.py) | Mutable DotPlot chains over detached summaries, shared tree/layout helpers and the native dotplot renderer. |
| [_matrixplot_builder.py](../../src/genome_spy/integrations/scanpy/_matrixplot_builder.py) | Mutable MatrixPlot styles/guides over detached means or supplied summaries and the native tile renderer. |
| [_ranked_data.py](../../src/genome_spy/integrations/scanpy/_ranked_data.py) | Stored ranking checks, public Scanpy result selection, statistic color tables and detached rank-label positions. No expression access or analysis. |
| [_ranking_chart.py](../../src/genome_spy/integrations/scanpy/_ranking_chart.py) | Native score labels, axes and multi-panel layout shared by ranking, PCA loadings/variance and rank_genes_groups. Ranked expression wrappers reuse their existing parent charts. |
| [_data.py](../../src/genome_spy/integrations/scanpy/_data.py) | Shared scalar/numeric-table validation, raw/layer resolution and resident-expression checks; reused by preparation and chart modules. |
| [_grouped_data.py](../../src/genome_spy/integrations/scanpy/_grouped_data.py) | Selected values, feature slots/brackets, group counts and summaries. Shared scale_values serves cells and group means; heatmap adds cell permutations/group spans and an early size guard. No chart authoring. |
| [_style.py](../../src/genome_spy/integrations/scanpy/_style.py) | Shared schemes, CSS colors, continuous color bounds, fonts and point units for every plot; categorical/continuous preparation and explicit embedding style settings live here too. |
| [_dendrogram_data.py](../../src/genome_spy/integrations/scanpy/_dendrogram_data.py) | Read stored Scanpy results, delegate missing trees to sc.tl.dendrogram and share leaf/marker permutations. |
| [_dendrogram_chart.py](../../src/genome_spy/integrations/scanpy/_dendrogram_chart.py) | Shared native orthogonal links from stored branches, including gapped side tracks; no clustering. |
| [_correlation_chart.py](../../src/genome_spy/integrations/scanpy/_correlation_chart.py) | Native correlation tiles, numbers, labels, hover and optional tree. |
| [_grouped_chart.py](../../src/genome_spy/integrations/scanpy/_grouped_chart.py) | Dotplot/matrixplot share index slots, labels, brackets, sizing, guides, native totals and attached-tree layout; correlation reuses index coordinates. |
| [_matrixplot_chart.py](../../src/genome_spy/integrations/scanpy/_matrixplot_chart.py) | Native tiles, edge styling and summary hover; no AnnData access. |
| [_matrix_chart.py](../../src/genome_spy/integrations/scanpy/_matrix_chart.py) | Supplied numeric matrix and time-series heatmap tiles, axes, labels and color guide; shared numeric validation and grid interactions, without AnnData access. |
| [_timeseries_data.py](../../src/genome_spy/integrations/scanpy/_timeseries_data.py) | Supplied-profile point order, color subsets, masks and bounds; shared numeric/color checks, without analysis or chart authoring. |
| [_timeseries_chart.py](../../src/genome_spy/integrations/scanpy/_timeseries_chart.py) | Native time-series points, axes and guides using shared marker, zoom and dashed-highlight helpers. |
| [_paga_data.py](../../src/genome_spy/integrations/scanpy/_paga_data.py) | Read stored sparse group graphs, delegate layouts to Scanpy's public no-plot API, and prepare node/edge tables with shared validation and colors. No PAGA analysis or expression access. |
| [_paga_chart.py](../../src/genome_spy/integrations/scanpy/_paga_chart.py) | Native rules, points and labels with shared coordinate, unit and navigation helpers. No graph analysis or AnnData access. |
| [_clustermap_data.py](../../src/genome_spy/integrations/scanpy/_clustermap_data.py) | Bounded full-subset access, Seaborn-compatible scaling and color tracks, public SciPy or supplied row/column linkage. |
| [_clustermap_chart.py](../../src/genome_spy/integrations/scanpy/_clustermap_chart.py) | Shared matrix tiles, labels, fitted values and native surround tracks; aligned trees, color strips and a native observation-category legend. |
| [_heatmap_chart.py](../../src/genome_spy/integrations/scanpy/_heatmap_chart.py) | Cell tiles and native surround tracks with shared index gaps, category bands, centered labels and stored tree links; reuses grouped labels/brackets and fitted values, with optional aligned zoom (y-only by default). |
| [_dotplot_chart.py](../../src/genome_spy/integrations/scanpy/_dotplot_chart.py) | Native dots, exact area/percentage lookup, size guide and summary hover on the shared grouped layout. |
| [_embedding_data.py](../../src/genome_spy/integrations/scanpy/_embedding_data.py) | Resolve stored bases, shared coordinate labels and selected expression/metadata; retain row identity, masks, sizes and draw order. |
| [_embedding_density_data.py](../../src/genome_spy/integrations/scanpy/_embedding_density_data.py) | Read stored density metadata and group masks into the existing embedding table/panels; no KDE, expression access or independent renderer. |
| [_scatter_data.py](../../src/genome_spy/integrations/scanpy/_scatter_data.py) | Scatter-specific cell/gene orientation, per-axis layers, selected public vectors and legacy basis/order rules; detached variable-gene QC metadata. Reuses shared numeric checks and embedding identities. |
| [_hvg_chart.py](../../src/genome_spy/integrations/scanpy/_hvg_chart.py) | Native paired QC point panels, stored-statistic axis limits, shared bottom legend and optional hover/zoom; no analysis or expression access. |
| [_embedding_chart.py](../../src/genome_spy/integrations/scanpy/_embedding_chart.py) | Native points, axes, legends, labels, and panel composition. |
| [_grid_interactions.py](../../src/genome_spy/integrations/scanpy/_grid_interactions.py) | Shared index navigation/projection and native fitted values/contrast; no AnnData access. Dotplot highlighting uses a native ruler. |
| [_embedding_interactions.py](../../src/genome_spy/integrations/scanpy/_embedding_interactions.py) | Optional hover, plain brush ownership, and count. |
| [_selection.py](../../src/genome_spy/integrations/scanpy/_selection.py) | Pure interval-to-observation membership for Python subset retrieval. |

Scanpy owns analysis. UMAP's data module only resolves the inputs a plotting call
needs: which raw/layer vector a gene refers to, which categories to display, and
which existing coordinate columns to send. Expression access uses AnnData's
public `obs_vector`; no upstream plotting or private plotting helpers run.
`scanpy.get.obs_df` is not used for UMAP because its duplicate-label rejection and
raw symbol lookup differ from UMAP's behavior. Grouped plots use that public
getter directly, with only selected unique keys. Public AnnData string conversion
operates on the detached table, preserving category order without mutating AnnData.
Grouped statistics are independently tested before adding the dotplot chart.
The [computation reuse audit](../../docs/integrations/scanpy/supported.md#reusing-scanpy-computations)
records which public methods are used and why aggregate/scale or plotting-class
shortcuts would change semantics or ownership.

There are no Matplotlib imports, figure creation, global style reads, or Python
colormap sampling in the adapter. CSS palette values, including saved AnnData
palettes and Scanpy's public default palette lists, go directly to native scales.
GenomeSpy maps continuous values and draws the guides. Plotting retains source
measurements; it does not compute embeddings, rankings, or new scientific results.

The [status ledger](STATUS.md#public-callable-coverage) records available previews
and remaining families. New chart families reuse compatible AnnData access, category/color handling, and
plotting computations. A separate data module per family is optional: add one
only when that family needs distinct preparation that merits its own module.
Share common operations directly; there is no requirement to implement another
family before extracting a useful shared helper. Reuse suitable public
Scanpy/AnnData functions and existing library helpers first.

Apply YAGNI to new functionality and abstractions: implement the current plot's
needs with small functions, without building a general adapter framework. Keep
shared functions focused on equivalent semantics, including raw/layer selection,
ordering, thresholds, and normalization. Review basic plot reproduction before
adding interactions.

The shared helpers above have current callers; they are not a general adapter
framework. Keep differing semantics explicit: UMAP and grouped expression use
different lookups, dotplot and matrixplot scale at different stages, and their
layouts differ from standalone trees/correlation matrices. Reuse those common
parts directly when later families arrive. A chart module per family
does not imply a separate validator, color system, data accessor or tree layout.
Heatmap supplies an explicit observation permutation and unequal group centers
to the shared tree renderer. Its native side tracks share gapped index scales;
summary plots retain their equal-slot projection.

## Plotting workflows

Both notebooks run independently on Scanpy's packaged `pbmc68k_reduced()` data:

- [UMAP](notebooks/scanpy_umap.ipynb): basic categorical/continuous plotting with
  x/y zoom and panning, linked brushing/count/Python retrieval, then customization.
  Existing coordinates are retained; gene scoring and the final t-SNE preparation are explicit Scanpy operations. Packaged PCA scatter, stored loadings, variance ratios and their composed overview reuse embedding/ranking helpers. Cell/gene scatter examples read packaged observation and variable annotations without an embedding.
- [Expression plots](notebooks/scanpy_expression.ipynb): marker dotplot, scaled
  matrixplot, individual-cell heatmap, supplied numeric matrix, aligned dendrograms, y-only zoom (both axes optional), fitted tile values and dot row/column highlighting using the core tutorial
  dictionary and existing `bulk_labels`. Scanpy computes the shared tree in Python
  from the dataset’s existing PCA representation. Clustermap then clusters all
  700 individual cells and the same ten raw-snapshot marker genes using public
  SciPy linkage, rather than reusing a group-profile tree.
  A final section reads packaged logreg scores and explicitly computes a separate
  ranking for statistic colors, reusing summaries, trees and interactions.
  Variable-gene QC panels then inspect the packaged stored selection and statistics.
  Supplied time-series heatmaps and point plots reuse the PBMC markers, explicitly
  ordered by the stored S-phase score; neither chart infers time or pseudotime.
  Two native time-series subplots compare stored phase and G2M-score colors,
  reusing the same GNLY values with independent scales, guides and navigation.

These adapt supported portions of the official core and advanced tutorials.
Keep related examples together within each workflow, without placeholder cells
for unimplemented plots.

From the repository root:

```sh
uv sync --dev --extra scanpy --group scanpy-test
uv run jupyter lab integrations/scanpy/notebooks/
```

## Documentation guides

Focused, output-free notebooks in [guides/](guides/) supply both the live pages
and their downloads. [PAGA](guides/paga.ipynb) covers networks, comparisons,
adjacency and paths. [Profiles and simulations](guides/profiles.ipynb) covers
supplied profiles, Krumsiek11 runs and DPT results, with native run/gene focus.
Data checks use full Scanpy PBMC3k counts; the larger-data
guide uses the separate 10x PBMC10k v3 cohort from Scanpy's tutorial. Attribution
and processing are recorded in each notebook and [third-party notices](../../THIRD_PARTY_NOTICES.md).

Prepare their inputs explicitly before building the docs (Python 3.11+):

```sh
uv run integrations/scanpy/prepare_guide_data.py
uv run sphinx-build -b html -W --keep-going docs docs/_build/html
```

The preparation command runs the notebooks' analysis cells and caches AnnData
under ignored `tmp/scanpy-guide-data/`. It reuses matching inputs and rejects
stale or corrupted caches during page builds. Scanpy-version and preparation-code
changes require preparation again. CI runs the same command before Sphinx.
Ordinary Sphinx builds read those files without downloads, Scrublet, PAGA/layout,
DPT or embedding analysis. Downloaded notebooks run the shown Scanpy steps
independently. The docs dependency group includes Scanpy's existing PAGA extra.

## Validation

[Validation sources](../../tests/integrations/scanpy/) contain the tests,
reference contracts, temporary reference images, explicit reference generators,
and resource benchmarks.
They are development code and are not shipped as part of the Python package.

```sh
uv run --no-sync pytest tests/integrations/scanpy --ignore=tests/integrations/scanpy/browser
uv run --no-sync pytest tests/integrations/scanpy/browser
```

The former `tools/scanpy_reference.py` is now
[generate_references.py](../../tests/integrations/scanpy/generate_references.py).
Browser fixtures regenerate images in temporary directories without changing the
tracked JSON. No generated PNGs are committed. Explicit refresh commands write
images to ignored `tmp/scanpy-references/<family>/` and update text metadata.
The generator explicitly runs pinned Scanpy plotting on small synthetic test
fixtures and records signatures, figures, domains, colors, draw order, and point
footprints.
Inspecting Matplotlib artists is confined to this reference-generation step;
production plotting never recovers input data from rendered artists. Ordinary
semantic tests compare frozen numerical results; visual tests render fresh
upstream images in temporary directories.

```sh
uv run --no-sync python -m tests.integrations.scanpy.generate_references --help
uv run --no-sync python -m tests.integrations.scanpy.generate_grouped_references
uv run --no-sync python -m tests.integrations.scanpy.generate_dotplot_references
uv run --no-sync python -m tests.integrations.scanpy.generate_matrixplot_references
uv run --no-sync python -m tests.integrations.scanpy.generate_dendrogram_references
uv run --no-sync python -m tests.integrations.scanpy.generate_heatmap_references
uv run --no-sync python -m tests.integrations.scanpy.generate_matrix_references
uv run --no-sync python -m tests.integrations.scanpy.generate_clustermap_references
uv run --no-sync python -m tests.integrations.scanpy.generate_scatter_references
uv run --no-sync python -m tests.integrations.scanpy.benchmark_grouped --plot dotplot --browser --output /tmp/dotplot.json
uv run --no-sync python -m tests.integrations.scanpy.benchmark_grouped --plot matrixplot --browser --output /tmp/matrixplot.json
uv run --no-sync python -m tests.integrations.scanpy.benchmark_grouped --plot matrixplot --dendrogram --browser --output /tmp/trees.json
uv run --no-sync python -m tests.integrations.scanpy.benchmark_grouped --plot heatmap --browser --output /tmp/heatmap.json
uv run --no-sync python -m tests.integrations.scanpy.benchmark --help
uv run --no-sync python -m tests.integrations.scanpy.benchmark --plot pca --cells 20000 --panels 8 --browser --output /tmp/scanpy-pca.json
uv run --no-sync python -m tests.integrations.scanpy.benchmark --plot scatter --cells 20000 --panels 8 --browser --output /tmp/scanpy-scatter.json
uv run --no-sync python -m tests.integrations.scanpy.benchmark --plot scatter-genes --cells 20000 --panels 8 --browser --output /tmp/scanpy-scatter-genes.json
uv run --no-sync python -m tests.integrations.scanpy.benchmark_ranked --output /tmp/scanpy-rank-labels.json
uv run --no-sync python -m tests.integrations.scanpy.benchmark_grouped --ranked --plot dotplot --browser --output /tmp/scanpy-ranked-dotplot.json
```

Run resource workloads sequentially in fresh processes. `--ranked` also works with
`--plot matrixplot` and `--plot heatmap`: dot/matrix colors use stored scores,
while heatmaps retain cell expression. Sparse-allocation guards check selected
columns or rows; statistic-colored matrixplots only validate features on zero
rows. Reports record their allocation/timing scopes, including optional imports,
JSON dispatch, pointer pauses and garbage collection. Keep screenshots temporary;
retained resource metadata is a local observation, not a portable timing limit.

Reference regeneration is a deliberate compatibility update, not a prerequisite
for using the integration. Notebook examples use real packaged data; synthetic
fixtures remain useful for independently checking missing values, duplicate
labels/coordinates, raw/layer differences, sparse allocation, and exact edges.

The expression workflow also includes PAGA path heatmaps and lines. Scanpy
explicitly computes pseudotime; both plots reuse the same ordered, smoothed
profiles. Native tiles/tracks or round-cap rules display the supplied group
order, without inferring a trajectory. Lines include hover and optional zoom.
