:::{admonition} Data use and provenance
:class: note

The visualization uses simulated example data from
[Allele-specific copy number analysis of tumors](https://doi.org/10.1073/pnas.1009843107)
by Loo et al. and follows the ASCAT method described there. It is an
explanatory ASCAT-like fit implemented as a GenomeSpy specification. The input
has already been segmented using ASPCF; this visualization does not perform
segmentation. The raw LogR and BAF probe values are shown only as a reference
for the segmented and fitted values.
:::

## What to notice

The sunrise plot shows integer-fit distance over candidate tumor purity and
ploidy. Click or drag to choose an exact fit; the copy-number, LogR, and BAF
tracks update together. Multiple local minima can fit integer copy numbers
similarly well, so a low distance is not by itself a biological conclusion.

## Python implementation

Parameters and a two-dimensional ruler drive the linked views. Cross, formula,
and aggregate transforms calculate the candidate grid in the browser, while
composition operators align the heatmap and genomic tracks.

See the [official GenomeSpy example](https://genomespy.app/docs/examples/genomic-data/ascat-algorithm/)
for the fitting equations, weighting choices, and detailed interpretation.
