The matrix shows the **mean of log1p counts**, including zeros, for each cell
type and marker. Counts at the left show how many cells contribute to each row.
Hover over a tile for the marker, cell type, and exact mean.

Colored blocks above the genes label the cell type each marker is associated
with. Matching genes share a block; these labels are distinct from the row
cell types. The count axis reports cells, not expression.

The tree groups similar mean marker profiles using single linkage and Euclidean
distance. Python prepares it once; GenomeSpy draws its branches with rule marks.
All three plots use this group order; the tree represents similarity, not lineage.
For variation within each group, see the [cell heatmap](pbmc_cell_heatmap.md)
or [expression tracks](pbmc_expression_tracks.md).

:::{admonition} Data use and provenance
:class: note

12 markers from 2,638 cells in Scanpy's processed
[10x Genomics PBMC3k dataset](https://www.10xgenomics.com/datasets/3-k-pbm-cs-from-a-healthy-donor-1-standard-1-1-0),
licensed CC BY 4.0. This subset retains the saved `raw.X` log1p counts and
original cell-type annotations. The group tree orders cell types; cells retain
their source order within each type.
:::

Inspired by [Scanpy's Marsilea examples](https://scanpy.scverse.org/en/stable/how-to/plotting-with-marsilea.html).
