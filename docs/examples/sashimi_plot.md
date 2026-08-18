:::{admonition} Data use and provenance
:class: note

The example is based on igv.js's splice-junction sample data for chr15. The
source files are hosted in IGV's data repository, and the original demo is
available here: [splice junction example](https://igv.org/web/release/3.8.0/examples/spliceJunctions.html).
:::

## What to notice

Arc height follows junction span, while stroke thickness and label text encode
uniquely mapped reads. Horizontal zoom changes the shared arc-and-label height
domain; the coverage track retains an independent y scale.

## Python implementation

The chart layers lazy BigWig coverage with filtered junction links and labels.
Formula transforms derive arc geometry and deterministic label jitter, and an
expression-driven scale couples the junction height to the visible locus.

See the [official GenomeSpy example](https://genomespy.app/docs/examples/genomic-data/sashimi-plot/)
for the source visualization and scale-expression details.
