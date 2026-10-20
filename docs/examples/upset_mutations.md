:::{admonition} Data use and provenance
:class: note

The design follows Conway et al., [*UpSetR: an R package for the visualization
of intersecting sets and their properties*](https://doi.org/10.1093/bioinformatics/btx364),
and the original UpSet technique by Lex et al., [*UpSet: Visualization of
Intersecting Sets*](https://doi.org/10.1109/TVCG.2014.2346248).

The example loads UpSetR's bundled
[`mutations.csv`](https://github.com/hms-dbmi/UpSetR/blob/master/inst/extdata/mutations.csv),
attributed to the TCGA Consortium, and displays PTEN, TP53, EGFR, PIK3R1, and
RB1.
:::

## What to notice

Columns are exact mutation profiles ordered by intersection size. Filled cells
identify their genes, upper bars count each exact profile, and side bars count
inclusive gene-set sizes. Hovering a gene highlights every profile containing
it.

## Python implementation

Regex folding normalizes the wide mutation table and the set-intersection
transform groups patients by membership profile. `gs.surround()` places the
intersection bars above the matrix and set-size bars to its left. Each margin
shares the matrix's corresponding index scale and keeps an independent
quantitative count scale. GenomeSpy runs these transforms in the browser.

See the [official GenomeSpy example](https://genomespy.app/docs/examples/generic/upsetr-mutations/)
for the full reading and transform guide.
