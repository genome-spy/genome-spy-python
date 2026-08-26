:::{admonition} Data use and provenance
:class: note

The mutation calls are the TCGA BRCA sample distributed with the MIT-licensed
[`maftools`](https://github.com/PoisonAlien/maftools) rainfall example. During
data loading, the package selects the most mutated sample, calculates
inter-event distances, and detects compact six-mutation windows. The trimmed
MAF omits `NCBI_Build`; its coordinates and gene-symbol overlaps identify it
as hg19. The displayed
hg19 RefSeq gene bodies come from the assembly-wide resource independently
prepared from the official UCSC `refGene` table. The track design follows the
[MutGlyph gene-annotation pattern](https://genomespy.app/MutGlyph/articles/gene-annotations.html).
GenomeSpy performs the lane packing and scored-label filtering while rendering.
:::

## What to notice

The focal chr8 view contains three nearby compact mutation clusters. The gene
track places **CPQ**, **TSPYL5**, **MTDH**, **LAPTM4B**, and neighboring RefSeq
genes on the same zoomable locus scale, providing context without implying
that a nearby gene caused a cluster.

## Python implementation

The rainfall points, cluster arrows, and full hg19 gene table are vertically
concatenated. Their x scale and genome axis are shared, while their unrelated y
scales remain independent. The domain opens on chr8 but does not pre-filter the
gene table, so annotation bodies remain available when panning. GenomeSpy packs
overlapping genes into three lanes and retains non-overlapping labels according
to their display score.
