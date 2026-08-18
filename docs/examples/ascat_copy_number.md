:::{admonition} Data use and provenance
:class: note

The example shows simulated example data for sample `S96` from
[Allele-specific copy number analysis of tumors](https://www.pnas.org/content/107/39/16910)
by Loo et al.
:::

## What to notice

The vertically concatenated tracks share one genomic x axis. The top track
shows slightly offset minor- and major-allele copy-number estimates. The middle
track overlays raw LogR probes with segment means, and the bottom track does the
same for B-allele frequency, including the mirrored `1 - BAF` line.

## Python implementation

The segment table is inherited by the copy-number and segment-mean marks, while
the raw LogR and BAF point layers use the probe table. The three tracks are
combined with `&` and share their locus scale and axis.

See the [official GenomeSpy example](https://genomespy.app/docs/examples/genomic-data/ascat/)
for data-wrangling details and the original specification.
