Each row is a cell; each column is a marker gene. Color shows **log1p counts**,
and the rail identifies cell types. Group heights reflect their cell counts.
Use the mouse wheel to zoom through cells, then drag to pan. Hover for the cell,
gene, and exact value. The color scale stays fixed while zooming.

The tree at the right compares group-mean marker profiles (single linkage,
Euclidean distance). Its branches move with the cells while zooming.

`from_anndata()` selects the marker values. A small dataset helper reshapes that
projection in Python; `Chart(adata)` reads the annotation rail directly from
`obs`. Python prepares the group tree; GenomeSpy draws its rule marks and keeps
the cell axes aligned. The tree shows similarity, not lineage.
Compare with the [group means](pbmc_marker_matrix.md).

:::{admonition} Data use and provenance
:class: note

12 markers from 2,638 cells in Scanpy's processed
[10x Genomics PBMC3k dataset](https://www.10xgenomics.com/datasets/3-k-pbm-cs-from-a-healthy-donor-1-standard-1-1-0),
licensed CC BY 4.0. This subset retains the saved `raw.X` log1p counts and
original cell-type annotations. Source order is preserved within each group.
:::

Inspired by [Scanpy's Marsilea examples](https://scanpy.scverse.org/en/stable/how-to/plotting-with-marsilea.html).
