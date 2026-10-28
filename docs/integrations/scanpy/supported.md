# Scanpy compatibility

Supports Scanpy 1.11.5 through 1.12.x.

Scanpy 1.12.4 cannot compute PAGA tree layouts (`rt` or `rt_circular`). Supply
positions with `pos=...` or use another layout. Other supported PAGA calls work.

## Available plots

See the guides for examples and the [API reference](api.md) for arguments and defaults.

| Plot family | Available calls | Guide |
| --- | --- | --- |
| Embeddings | `embedding`, `umap`, `tsne`, `diffmap`, `draw_graph`, `pca`, `pca_scatter` | [UMAP and embeddings](umap.md) |
| Cell or gene scatter | `scatter` | [UMAP and embeddings](umap.md) |
| PCA diagnostics | `pca_loadings`, `pca_variance_ratio`, `pca_overview` | [PCA diagnostics](pca.md) |
| Grouped expression | `dotplot`, `matrixplot`, `DotPlot`, `MatrixPlot` | [Expression plots](expression.md) |
| Individual-cell expression | `heatmap`, `clustermap`, `tracksplot` | [Expression plots](expression.md), [tracks](tracks.md) |
| Matrices and trees | `matrix`, `correlation_matrix`, `dendrogram` | [Expression plots](expression.md) |
| Ranked genes | `ranking`, `rank_genes_groups`, `rank_genes_groups_dotplot`, `rank_genes_groups_matrixplot`, `rank_genes_groups_heatmap` | [Ranked genes](ranked.md) |
| Embedding density | `embedding_density` | [UMAP and embeddings](umap.md) |
| Quality checks | `highest_expr_genes`, `highly_variable_genes`, `filter_genes_dispersion`, `scrublet_score_distribution` | [Data checks](quality.md) |
| Profiles and trajectories | `timeseries`, `timeseries_subplot`, `timeseries_as_heatmap`, `sim`, `dpt_groups_pseudotime`, `dpt_timeseries` | [Profiles and simulations](profiles.md) |
| PAGA | `paga`, `paga_compare`, `paga_path`, `paga_adjacency` | [PAGA graphs and paths](paga.md) |
| Brush-linked summaries | `EmbeddingSummary` | [Linked expression summaries](linked_expression.md) |

`EmbeddingSummary` is a GenomeSpy addition, rather than a Scanpy class. It links
an embedding brush to group means, histograms, composition bars or gene tracks.

**Not yet available:** `violin`, `stacked_violin`, `StackedViolin`, their ranked
violin variants, `rank_genes_groups_tracksplot` and `spatial`. Keep using Scanpy
for those plots and its global style-setting helpers.

## Shared differences from Scanpy

- **Analysis stays in Scanpy.** Compute embeddings, gene rankings, density and
  scores before plotting. Requested missing dendrograms may be computed through
  Scanpy; clustermap can compute cell/gene linkage, and PAGA can compute layout
  positions. These operations do not rerun the underlying embedding or ranking.
- **Results are native GenomeSpy charts.** Use `show=False` to receive a chart for
  configuration, composition or saving. `show=True` displays it and ordinarily
  returns `None`; `show=None` follows Scanpy's autoshow setting. Builders return
  a chart through `.to_chart()`.
- **Matplotlib objects are not part of this API.** `ax`, `return_fig`, figure/artist
  access and Matplotlib styling objects are unsupported. Unsupported options
  raise named errors rather than being silently ignored.
- **Sizing and colors use GenomeSpy.** `width` and `height` are plot-area sizes in
  logical pixels; axes, titles and legends add space. Native schemes and CSS
  colors are supported. Matplotlib colormap and normalization objects are not.
  Fonts, palette interpolation and layout can differ from Scanpy's rendering.
- **Saving uses the returned chart.** `chart.save("plot.html", inline=True)` creates
  interactive HTML; JSON is also supported. Scanpy's automatic image-saving
  options are unsupported. Use `save=False` if Scanpy autosave is enabled.
- **Browser interactions work in exported HTML.** Reading selected cells back into
  Python requires a live notebook kernel. The guides document each plot's hover,
  navigation and selection controls.

## Known limitations

- **Large cell grids require explicit subsetting.** Heatmaps, tracks and
  clustermaps allow at most 250,000 cell–gene values. `EmbeddingSummary` counts
  loaded extra observation columns toward that limit too. Automatic clustermap
  linkage is limited to 1,000,000 pairwise distances per clustered axis; provide
  linkage or subset the data for larger requests. Storage support varies by
  plot; these cell-expression views require resident expression.
- **Linked selections have a boundary mismatch.** In `EmbeddingSummary`, cells
  exactly on a brush's upper or right edge can appear in summaries but be omitted
  from the displayed count and Python selection results.
- **Changing linked heatmap genes can misplace rows.** With bundled GenomeSpy
  Core 1.2.0, a gene-menu change can leave tiles or value labels at old positions.
  Choose genes in Python when reliable row placement is required.
- **Some legends can clip.** Large symbols or vertical legends with multiple
  columns can exceed their allocated space in the bundled runtime. Inspect the
  final layout, especially with many categories.
- **Large live counts can slow brushing.** Exact counting currently scans plotted
  cells on brush updates. The faster native path awaits an adopted published
  Core release.
