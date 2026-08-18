:::{admonition} Data use and provenance
:class: note

The visualization uses a mirrored copy of UCSC's hg38 cytoband track,
distributed as
[cytoBand.txt.gz](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/cytoBand.txt.gz).
UCSC states that its downloadable data files and database tables are freely
available for public and commercial use.
:::

## What to notice

Background rectangles encode cytoband intervals and stains, labels reuse the
same intervals, and dashed rules separate chromosomes. Ranged text lets
GenomeSpy hide labels that do not fit while zooming.

## Python implementation

The source declares the headerless TSV columns explicitly. Rectangle, text,
and rule charts are layered with `+` and share locus encodings inherited from
their parent.

See the [official GenomeSpy example](https://genomespy.app/docs/examples/genomic-data/cytobands/)
for the full encoding discussion.
