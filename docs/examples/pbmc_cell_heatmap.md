Each row is a cell; each column is a marker gene. Color shows **log-transformed
counts**, and the colored strip identifies cell types. Larger groups occupy more
rows.

Use the mouse wheel to zoom and drag to pan. Hover over a tile for the cell,
gene, and exact value. The color scale stays fixed while zooming.

For a summary by cell type, see the [marker matrix](pbmc_marker_matrix.md).

:::{admonition} Data use and provenance
:class: note

12 markers from 2,638 cells in Scanpy's processed
[10x Genomics PBMC3k dataset](https://www.10xgenomics.com/datasets/3-k-pbm-cs-from-a-healthy-donor-1-standard-1-1-0)
(CC BY 4.0), retaining its log-transformed counts and cell-type labels.
:::

Inspired by [Scanpy's Marsilea examples](https://scanpy.scverse.org/en/stable/how-to/plotting-with-marsilea.html).
