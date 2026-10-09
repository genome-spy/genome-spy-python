Each track shows a marker's **log1p counts** across individual cells. Cell types
use the same colors as the [heatmap](pbmc_cell_heatmap.md). Zoom with the mouse
wheel and drag to pan; every track and the bottom strip move together.

The tree above the tracks compares group-mean marker profiles using single
linkage and Euclidean distance. It follows the same cell axis while zooming.

The y ranges differ between genes; read their ticks before comparing heights.
Cells are grouped by type, not ordered in time. Adjacent rectangles span one cell
each, with no smoothing. Use the heatmap to inspect exact cell values.

Python selects and reshapes the AnnData values. GenomeSpy filters one shared
table into gene tracks in the browser and shares their horizontal scale with
the prepared tree's rule marks. The tree shows similarity, not lineage.

:::{admonition} Data use and provenance
:class: note

12 markers from 2,638 cells in Scanpy's processed
[10x Genomics PBMC3k dataset](https://www.10xgenomics.com/datasets/3-k-pbm-cs-from-a-healthy-donor-1-standard-1-1-0),
licensed CC BY 4.0. This subset retains the saved `raw.X` log1p counts and
original cell-type annotations. Source order is preserved within each group.
:::

Inspired by [Scanpy's Marsilea examples](https://scanpy.scverse.org/en/stable/how-to/plotting-with-marsilea.html).
