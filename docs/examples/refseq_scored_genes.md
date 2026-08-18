:::{admonition} Data use and provenance
:class: note

The gene annotation track was inspired by [HiGlass](https://higlass.io). The
genes are [scored](https://docs.higlass.io/data_preparation.html#gene-annotation-tracks)
by their [citation counts](https://www.nature.com/articles/d41586-017-07291-9),
overlapping isoforms are merged into a single virtual isoform that includes all
exons, and the annotations were preprocessed with
[compressGeneAnnotations.py](https://github.com/genome-spy/genome-spy/blob/master/utils/compressGeneAnnotations.py).
:::

## What to notice

Only high-scoring symbols that fit in the visible region are shown. Transcript
bodies, exons, and strand arrows fade in at detailed zoom levels, allowing the
same track to work as both a whole-genome landmark view and a gene model view.

## Python implementation

The chart has two top-level layers. One draws transcript bodies and exons and
fades them in as the reader zooms closer. The other measures gene-symbol widths,
uses `transform_filter_scored_labels()` to retain labels that fit, and draws the
retained symbols with strand arrows. These transforms run in the browser again
whenever the visible genomic region changes.

See the [official GenomeSpy example](https://genomespy.app/docs/examples/genomic-data/refseq-genes/)
for preprocessing and label-selection details.
