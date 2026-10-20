# Scanpy integration workspace

Start with [status and next work](STATUS.md), the [implementation plan](PLAN.md), and the
[current compatibility guide](../../docs/integrations/scanpy/index.md).
Use `import genome_spy.integrations.scanpy as gsc`, then `gsc.pl.umap(...)`,
`gsc.pl.scatter(...)`, `gsc.pl.dotplot(...)`, `gsc.pl.matrixplot(...)`, `gsc.pl.heatmap(...)`, `gsc.pl.matrix(...)`, `gsc.pl.dendrogram(...)` or
`gsc.pl.correlation_matrix(...)` or `gsc.pl.clustermap(...)`.
Stored rankings add `gsc.pl.rank_genes_groups(...)`, `gsc.pl.ranking(...)`, and
the ranked dotplot/matrixplot/heatmap wrappers.
`gsc.pl.pca_loadings(...)` and `gsc.pl.pca_variance_ratio(...)` reuse the ranking
panels for stored PCA results.
Scanpy still owns preprocessing, embedding, clustering, and gene ranking.

The implementation lives in the installable [source package](../../src/genome_spy/integrations/scanpy/),
not in this workspace or the documentation:

| Source | Responsibility |
| --- | --- |
| [__init__.py](../../src/genome_spy/integrations/scanpy/__init__.py) | Lightweight explicit namespace exports. |
| [pl.py](../../src/genome_spy/integrations/scanpy/pl.py) | Public signatures and plot-specific validation; common kwargs checks, optional dependency/version setup and native display/save handling. |
| [_ranked_data.py](../../src/genome_spy/integrations/scanpy/_ranked_data.py) | Stored ranking checks, public Scanpy result selection, statistic color tables and detached rank-label positions. No expression access or analysis. |
| [_ranking_chart.py](../../src/genome_spy/integrations/scanpy/_ranking_chart.py) | Native score labels, axes and multi-panel layout shared by ranking, PCA loadings/variance and rank_genes_groups. Ranked expression wrappers reuse their existing parent charts. |
| [_data.py](../../src/genome_spy/integrations/scanpy/_data.py) | Shared scalar/numeric-table validation, raw/layer resolution and resident-expression checks; reused by preparation and chart modules. |
| [_grouped_data.py](../../src/genome_spy/integrations/scanpy/_grouped_data.py) | Selected values, feature slots/brackets and summaries. Shared scale_values serves cells and group means; heatmap adds cell permutations/group spans and an early size guard. No chart authoring. |
| [_style.py](../../src/genome_spy/integrations/scanpy/_style.py) | Shared schemes, CSS colors, continuous color bounds, fonts and point units for every plot; categorical/continuous preparation and explicit embedding style settings live here too. |
| [_dendrogram_data.py](../../src/genome_spy/integrations/scanpy/_dendrogram_data.py) | Read stored Scanpy results, delegate missing trees to sc.tl.dendrogram and share leaf/marker permutations. |
| [_dendrogram_chart.py](../../src/genome_spy/integrations/scanpy/_dendrogram_chart.py) | Native rule branches for standalone and attached trees; no clustering. |
| [_correlation_chart.py](../../src/genome_spy/integrations/scanpy/_correlation_chart.py) | Native correlation tiles, numbers, labels, hover and optional tree. |
| [_grouped_chart.py](../../src/genome_spy/integrations/scanpy/_grouped_chart.py) | Dotplot/matrixplot share index slots, labels, brackets, sizing, guides and attached-tree layout; correlation reuses index coordinates. |
| [_matrixplot_chart.py](../../src/genome_spy/integrations/scanpy/_matrixplot_chart.py) | Native tiles, edge styling and summary hover; no AnnData access. |
| [_matrix_chart.py](../../src/genome_spy/integrations/scanpy/_matrix_chart.py) | Supplied numeric tiles and native axes/color guide; reuses numeric validation, color bounds, index slots and labels without AnnData access. |
| [_clustermap_data.py](../../src/genome_spy/integrations/scanpy/_clustermap_data.py) | Bounded full-subset access, Seaborn-compatible scaling and color tracks, public SciPy or supplied row/column linkage. |
| [_clustermap_chart.py](../../src/genome_spy/integrations/scanpy/_clustermap_chart.py) | Shared matrix tiles, slot labels, fitted values and navigation composed with two aligned trees, ordered color strips and a native observation-category legend. |
| [_heatmap_chart.py](../../src/genome_spy/integrations/scanpy/_heatmap_chart.py) | Cell tiles, category strips, boundaries and cell hover; reuses grouped labels/brackets and trees projected onto unequal group spans, with optional aligned zoom (y-only by default). |
| [_dotplot_chart.py](../../src/genome_spy/integrations/scanpy/_dotplot_chart.py) | Native dots, exact area/percentage lookup, size guide and summary hover on the shared grouped layout. |
| [_embedding_data.py](../../src/genome_spy/integrations/scanpy/_embedding_data.py) | Resolve stored bases, shared coordinate labels and selected expression/metadata; retain row identity, masks, sizes and draw order. |
| [_scatter_data.py](../../src/genome_spy/integrations/scanpy/_scatter_data.py) | Scatter-specific cell/gene orientation, per-axis layers, selected public vectors and legacy basis/order rules. Reuses embedding identities, panel fields, colors and rendering. |
| [_embedding_chart.py](../../src/genome_spy/integrations/scanpy/_embedding_chart.py) | Native points, axes, legends, labels, and panel composition. |
| [_grid_interactions.py](../../src/genome_spy/integrations/scanpy/_grid_interactions.py) | Shared index navigation/projection and native fitted values/contrast; no AnnData access. Dotplot highlighting uses a native ruler. |
| [_embedding_interactions.py](../../src/genome_spy/integrations/scanpy/_embedding_interactions.py) | Optional hover, linked brush highlighting, ownership, and count. |
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
The [computation reuse audit](../../docs/integrations/scanpy/index.md#reusing-scanpy-computations)
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
Heatmap now supplies an explicit observation permutation and unequal group centers
to the shared tree renderer; summary plots retain their equal-slot projection.

## Plotting workflows

Both notebooks run independently on Scanpy's packaged `pbmc68k_reduced()` data:

- [UMAP](notebooks/scanpy_umap.ipynb): basic categorical/continuous plotting with
  x/y zoom and panning, linked brushing/count/Python retrieval, then customization.
  Existing coordinates are retained; gene scoring and the final t-SNE preparation are explicit Scanpy operations. Packaged PCA scatter, stored loadings and variance ratios reuse embedding/ranking helpers. Cell/gene scatter examples read packaged observation and variable annotations without an embedding.
- [Expression plots](notebooks/scanpy_expression.ipynb): marker dotplot, scaled
  matrixplot, individual-cell heatmap, supplied numeric matrix, aligned dendrograms, y-only zoom (both axes optional), fitted tile values and dot row/column highlighting using the core tutorial
  dictionary and existing `bulk_labels`. Scanpy computes the shared tree in Python
  from the dataset’s existing PCA representation. Clustermap then clusters all
  700 individual cells and the same ten raw-snapshot marker genes using public
  SciPy linkage, rather than reusing a group-profile tree.
  A final section reads packaged logreg scores and explicitly computes a separate
  ranking for statistic colors, reusing summaries, trees and interactions.

These adapt supported portions of the official core and advanced tutorials.
Keep related examples together within each workflow, without placeholder cells
for unimplemented plots.

From the repository root:

```sh
uv sync --dev --extra scanpy --group scanpy-test
uv run jupyter lab integrations/scanpy/notebooks/
```

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
```

Reference regeneration is a deliberate compatibility update, not a prerequisite
for using the integration. Notebook examples use real packaged data; synthetic
fixtures remain useful for independently checking missing values, duplicate
labels/coordinates, raw/layer differences, sparse allocation, and exact edges.
