# Select genes for follow-up

{download}`Download the notebook <../../../notebooks/select_genes.ipynb>`

Scroll to zoom and drag to brush a region, then click
**Download selected genes** to save a CSV. Points grow as you zoom in.

```{genomespy-workflow} genes
```

The table updates as you drag. It shows up to 20 rows; export includes
**all selected genes**, with Ensembl IDs, fold changes, and p-values.
Reloading clears the selection. Use the notebook above to access it in Python
as the pandas table `selected_genes`.

Brushing selects candidates; it does not run a new statistical test.

## Code

The chart and Python hooks below come directly from the downloadable notebook.
The web demo uses JavaScript for the same interactions; Python hooks run in a notebook.

::::{dropdown} Chart specification (Python)
```{genomespy-workflow} genes
:code: chart
```
::::

::::{dropdown} Python hooks and controls
```{genomespy-workflow} genes
:code: hooks
```
::::

:::{admonition} Data use and provenance
:class: note

Himes et al. airway RNA-seq ([GSE52778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE52778)),
using the packaged Bioconnector workshop counts (CC BY-NC-SA 4.0).
The package computes paired log-count tests and Benjamini–Hochberg adjusted
p-values in Python; GenomeSpy plots the results. This is an illustrative
analysis, not DESeq2. See <a href="../../THIRD_PARTY_NOTICES.md">data notices</a>.
:::
