:::{admonition} Data use and provenance
:class: note

The example uses a small BAM slice derived from public Genome in a Bottle /
NIST HG002 (NA24385) Illumina 300x whole-genome alignments. The slice covers
`chr20:9950000-10100000` on GRCh38 and is downsampled for browser-based
visualization. It is intended only as a visualization demo, not for clinical
interpretation, diagnostic decisions, variant calling, biological inference,
benchmarking, genealogy, or re-identification.

Source attribution: Genome in a Bottle / NIST HG002 (NA24385) data, and Zook,
J.M. et al. Extensive sequencing of seven human genomes to characterize
benchmark reference materials. *Scientific Data* 3, 160025 (2016).
<https://doi.org/10.1038/sdata.2016.25>
:::

## What to notice

The top track summarizes read depth from aligned CIGAR blocks and stacks
MD-derived mismatch support by alternate base. Insertions use vertical rules
because they are anchored between reference bases and have zero reference
width.

The pileup uses arrows for read direction and opacity for mapping quality.
CIGAR overlays mark deletions, skipped regions, insertions, and soft-clipped
ends. Mismatching bases are extracted from MD tags and rendered over the reads;
the two sliders filter low-quality alignments and bases.

## Python implementation

The chart combines lazy BAM loading with `transform_flatten_cigar()`,
`transform_alignment_mismatches()`, coverage and pileup transforms, parameters,
and layered marks. The complete Python source below is the specification used
by the live chart.

See the [official GenomeSpy example](https://genomespy.app/docs/examples/genomic-data/bam-read-alignments/)
for the corresponding grammar-oriented explanation.
