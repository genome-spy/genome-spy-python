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

Four views pan and zoom together because the parent owns their assembly and
shared locus scale. The cytoband track supplies the single top genome axis.
The child views retain their own data, marks, and vertical scales.

## Python implementation

The complete cytoband, six-frame translation, BAM alignment, and RefSeq track
definitions are written in this example and combined with `gs.vconcat()`.
There are no imported Python chart builders, JSON specifications, remote view
specifications, or GenomeSpy view-template imports. URLs in the code identify
the underlying biological datasets; GenomeSpy loads those data while rendering.
The BAM track uses an explicit viewport height because it is nested inside the
larger layout.

See the [official GenomeSpy example](https://genomespy.app/docs/examples/genomic-data/genome-browser/)
for the original composition discussion.
