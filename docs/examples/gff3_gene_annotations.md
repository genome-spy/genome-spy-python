:::{admonition} Data use and provenance
:class: note

The visualization uses a sorted and bgzip-compressed copy of the GENCODE human
[release 43 (GRCh38.p13) comprehensive gene annotation GFF3](https://www.gencodegenes.org/human/release_43.html).
GENCODE states that all project data are open access.
:::

## What to notice

Transcript bodies, exon and UTR blocks, and transcript labels share packed
lanes. The labels include `<` or `>` to indicate strand and are shown only when
they fit within the transcript interval.

## Python implementation

The lazy GFF3 source is flattened and projected into transcript records, packed
into lanes, and expanded again to draw exon, CDS, and UTR features.

See the [official GenomeSpy example](https://genomespy.app/docs/examples/genomic-data/gencode-gff3-gene-annotations/)
for the feature hierarchy and transform details.
