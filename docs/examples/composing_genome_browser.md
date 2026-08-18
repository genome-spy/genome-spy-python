:::{admonition} Data use and provenance
:class: note

This composed view uses the data sources described in the individual official
[cytoband](https://genomespy.app/docs/examples/genomic-data/cytobands/),
[six-frame translation](https://genomespy.app/docs/examples/genomic-data/indexed-fasta-six-frame-translation/),
[BAM alignment](https://genomespy.app/docs/examples/genomic-data/bam-read-alignments/),
and [RefSeq gene annotation](https://genomespy.app/docs/examples/genomic-data/refseq-genes/)
examples. See those pages for source details and applicable disclaimers.
:::

## What to notice

Four independently authored views pan and zoom together because the parent
owns their assembly, locus scale, and genome axis. The child views retain their
own data, marks, and vertical scales.

## Python implementation

This example demonstrates composition rather than rebuilding every track: it
uses `gs.import_view()` for pinned upstream specifications and combines them
with `gs.vconcat()`.

See the [official GenomeSpy example](https://genomespy.app/docs/examples/genomic-data/genome-browser/)
for the original composition discussion.
