:::{admonition} Data use and provenance
:class: note

The alignment file `16SRNA_Deino_87seq.aln` is identified by the NCBI tutorial
and is available from the
[NCBI FTP server](ftp://ftp.ncbi.nlm.nih.gov/toolbox/gbench/samples/16SRNA_Deino_87seq.aln).
NCBI states that it places no restrictions on the use or distribution of
molecular data in its databases, but original submitters may claim
intellectual-property rights in submitted data. This dataset is used here for
demonstration and visualization purposes.
:::

## What to notice

The upper logo summarizes base frequency and information content. The lower
track preserves one row per aligned sequence. Letters become readable when
zoomed in, while colored rectangles provide a compact overview at wider scales.

## Python implementation

FASTA input is flattened to one row per aligned base. Aggregate, formula, and
information-content stack transforms build the logo, and `&` aligns it with
the sequence matrix on a shared index scale.

See the [official GenomeSpy example](https://genomespy.app/docs/examples/genomic-data/multiple-sequence-alignment/)
for the information-content calculation and original specification.
