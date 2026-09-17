# Annotate genomic intervals

{download}`Download the notebook <../../../notebooks/annotate_genomic_intervals.ipynb>`

Brush the chart, enter a name, and click **Save annotation**.
New marks appear in **Your annotations**. Click **Download BED** to keep them.

```{genomespy-workflow} intervals
```

This demo keeps annotations in your browser; reloading clears them.
Use the notebook above to keep the records in a Python list called `annotations`.

The assembly is **hg38**. BED uses **0-based, half-open intervals** and contains
chromosome, start, end, and name. Notes are not included in BED. Brushes spanning
chromosomes are rejected. Gene bodies cover the initial region only.

## Code

The chart and Python hooks below come directly from the downloadable notebook.
The web demo uses JavaScript for the same interactions; Python hooks run in a notebook.

::::{dropdown} Chart specification (Python)
```{genomespy-workflow} intervals
:code: chart
```
::::

::::{dropdown} Python hooks and controls
```{genomespy-workflow} intervals
:code: hooks
```
::::

:::{admonition} Data use and provenance
:class: note

GC content comes from UCSC hg38, served by GenomeSpy. Gene bodies are packaged
UCSC/NCBI RefSeq annotations with overlapping transcripts collapsed—not exon
models. Python selects the gene subset; GenomeSpy loads the signal and renders
the tracks. See <a href="../../THIRD_PARTY_NOTICES.md">data notices</a>.
:::
