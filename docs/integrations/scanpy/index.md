# Scanpy

Keep using Scanpy for preprocessing, embeddings and gene ranking. Use GenomeSpy
for interactive plots of those results.

## Install

```sh
pip install --upgrade 'genome-spy-python[scanpy]'
```

Use that environment as your Jupyter kernel. Scanpy remains an optional dependency.

## Replace a plotting call

After computing UMAP with Scanpy, replace `sc.pl.umap(...)` with:

```python
import genome_spy.integrations.scanpy as gsc

gsc.pl.umap(adata, color="louvain", zoom=True)
```

The plot reads the existing `adata.obsm["X_umap"]` coordinates. It does not compute
an embedding or change your analysis.

Start with [UMAP and embeddings](umap.md) to plot UMAP, t-SNE and diffusion maps,
select cells and customize a chart.
Use [expression plots](expression.md) to compare marker genes across cell groups
with dotplots, matrixplots, heatmaps and clustermaps. That guide also covers
numeric matrices, correlations, dendrograms and builders.
Use [expression tracks](tracks.md) to inspect individual cells with aligned gene
profiles, hover and zoom.
Try [linked expression summaries](linked_expression.md) to brush a UMAP and compare
marker expression within cell types, alongside selected-cell histograms, or highlight
the same PBMC3k cells across marker tracks.

Inspect stored [PCA diagnostics](pca.md) or plot [ranked genes](ranked.md) using
results already computed by Scanpy.

Explore [PAGA graphs and paths](paga.md), or compare [ordered profiles and
simulations](profiles.md), including simulation heatmaps and DPT plots.

Use [data checks](quality.md) with Scanpy's full PBMC3k counts.
See [save and export](export.md) for interactive HTML, chart definitions and
PNG/SVG images, including the plot buttons.
Check [Scanpy compatibility](supported.md) for available calls and differences
from Scanpy. Unsupported options raise an error.

```{toctree}
:hidden:

UMAP and embeddings <umap>
PCA diagnostics <pca>
Expression plots <expression>
Expression tracks <tracks>
Linked expression summaries <linked_expression>
Ranked genes <ranked>
PAGA graphs and paths <paga>
Profiles and simulations <profiles>
Data checks <quality>
Save and export <export>
Scanpy compatibility <supported>
API reference <api>
```
