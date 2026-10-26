# Scanpy

Keep using Scanpy for preprocessing, embeddings and gene ranking. Use GenomeSpy
for interactive plots of those results.

:::{note}
This integration is an **unreleased preview**, tested with **Scanpy 1.11.5**.
It is not included in the published genome-spy-python 0.7.0 release.
:::

## Install

From the project folder containing this preview:

```sh
python -m pip install -e '.[scanpy]'
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

Start with [UMAP and embeddings](umap.md) to plot, select cells and customize a chart.
Use [expression plots](expression.md) to compare marker genes across cell groups
with dotplots, matrixplots and heatmaps.
Check [supported plots and options](supported.md) for available calls and differences
from Scanpy. Unsupported options raise an error.

```{toctree}
:hidden:

UMAP and embeddings <umap>
Expression plots <expression>
Supported plots and options <supported>
API reference <api>
```
