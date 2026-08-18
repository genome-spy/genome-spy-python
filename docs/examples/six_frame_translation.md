:::{admonition} Data use and provenance
:class: note

The visualization uses a mirrored, indexed copy of UCSC's hg38 / GRCh38
reference FASTA from
[goldenPath/hg38/bigZips/latest/hg38.fa.gz](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/latest/hg38.fa.gz).
UCSC states that its downloadable data files and database tables are freely
available for public and commercial use, subject to any upstream restrictions
noted for the original assembly data.
:::

## What to notice

The reference sequence and all six reading frames stay aligned while panning.
Start codons are green, stop codons are red, and arrow direction distinguishes
forward and reverse translations. Frame assignment remains stable across lazy
data reloads.

## Python implementation

The chart flattens sequence chunks into bases, constructs overlapping codons
with window transforms, and maps them through lookup tables. A named template
is imported for each strand and composed with the reference track.

See the [official GenomeSpy example](https://genomespy.app/docs/examples/genomic-data/indexed-fasta-six-frame-translation/)
for the codon construction and frame calculations.
