:::{admonition} Data use and provenance
:class: note

This view uses a prepared RNF7 extract from the CC BY 4.0
[xPore demo archive](https://doi.org/10.5281/zenodo.4587661). Python preparation
retained one transcript-aligned replicate per condition, pseudonymized read
labels, and calculated coverage. It reconstructed the RNF7-201 reference from
three GRCh38 exon sequences returned by Ensembl, then derived mismatches and
CIGAR events from the BAM alignments. The m6A track uses published
condition-level m6Anet site probabilities; they were not recomputed from the
selected demo reads.
:::

## What to notice

The top track overlays WT and METTL3-knockout read depth; the sequence track
marks their condition-level m6Anet probabilities with size-scaled triangles,
including the strong contrast at position 614. The scrollable read tracks show
the individual molecules and their alignment events, not per-read m6A calls.
Drag the bottom overview to brush a transcript interval, reveal sequence letters
on close zoom, and keep every track aligned.

## Python implementation

Python loads prepared coverage, reference bases, m6Anet probabilities,
pseudonymized read spans, alignment events, and exon intervals. GenomeSpy
executes the condition filters, zoom-dependent letter visibility, overview
brush, and shared selection-controlled transcript-coordinate scale in the
browser.
