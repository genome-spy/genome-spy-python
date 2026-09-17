# Pick individual genes

{download}`Download the notebook <../../../notebooks/pick_genes.ipynb>`

Click a point to select a gene. **Shift-click** adds or removes genes.
Scroll to zoom and drag to pan; points grow as you zoom in.
The table shows the selected records; download them as CSV.

```{genomespy-workflow} points
```

Unlike brushing, point selection returns the selected rows directly—no range
filtering needed. In Python, `snapshot["data"]` contains these records.
Reloading clears the selection.

## Code

The web demo uses JavaScript; run these Python hooks in the notebook.

::::{dropdown} Chart specification (Python)
```{genomespy-workflow} points
:code: chart
```
::::

::::{dropdown} Python hooks
```{genomespy-workflow} points
:code: hooks
```
::::

:::{admonition} Data use and provenance
:class: note

The same illustrative airway RNA-seq analysis as [Select genes](select-genes.md):
packaged Bioconnector workshop counts (CC BY-NC-SA 4.0), with paired log-count
tests and adjusted p-values prepared in Python; not DESeq2.
:::
