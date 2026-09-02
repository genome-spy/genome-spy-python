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
owns their assembly and shared locus scale. The cytoband track supplies the
single top genome axis. The child views retain their own data, marks, and
vertical scales.

## Python implementation

Each standalone example exposes a small Python builder for its reusable track.
This example calls those builders and combines the returned charts with
`gs.vconcat()`. No JSON specification is imported: the child dataflows and the
parent composition are all authored through the Python API. The BAM builder is
given an explicit viewport height because it is nested inside a larger layout;
its standalone example instead fills its own container.

See the [official GenomeSpy example](https://genomespy.app/docs/examples/genomic-data/genome-browser/)
for the original composition discussion.
