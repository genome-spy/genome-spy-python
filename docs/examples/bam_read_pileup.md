Zoom and pan to load reads for the visible region. The top track counts
overlapping read spans; arrows below show each read's position and strand.
Use the row-height slider to make the pileup more compact or easier to inspect.
Scroll vertically to see additional reads.

Reads load only for windows of 30,000 bases or less. This simple example counts
whole read spans, without distinguishing gaps or mismatched bases. For those
details and quality filters, see [BAM read alignments](bam_read_alignments.md).

:::{admonition} Data use and provenance
:class: note

Adapted from GenomeSpy's [lazy BAM example](https://genomespy.app/playground/?spec=/docs/example-specs/docs/grammar/data/lazy/bam-read-alignments.json).
The browser loads GenomeSpy's mirror of UCSC's `bamExample.bam`, described
upstream as 1000 Genomes NA12878 alignments on hg18. The data are not bundled
with the Python package. See [UCSC's data-use terms](https://genome.ucsc.edu/license/).
:::
