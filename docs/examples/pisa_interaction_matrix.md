Rows show ATAC-seq output positions and columns show input bases around the
*Drosophila sog* enhancer, following Figure 2d of McAnany et al. Each cell's
color encodes the signed PISA effect. Accessibility and contribution-score
margin tracks share the corresponding output and input coordinates.

## What to notice

Positive effects are red and negative effects are blue. Pink and green mark
values beyond the central diverging scale. The dashed diagonal identifies
equal input and output coordinates; the pointer ruler helps trace rows and
columns through the overview. Motif intervals sit near the matrix's bottom edge.

Pan and zoom in both dimensions. Numeric cell values appear when cells are
large enough to read, and the ruler fades away. The contribution track changes
from bars to base-colored sequence letters as you zoom in.

## How the chart is built

Python authors a three-cell `gs.concat(..., columns=2)` grid: matrix, right-hand
accessibility track, and bottom contribution track. Shared index scales align
each margin with the matrix; each margin's signal scale is excluded from the
shared genomic resolution.

The example references prepared remote Parquet tables without loading or
processing them in Python. GenomeSpy loads the tables and executes all
declarative transforms in the browser. Reactive parameters measure the visible
domain spans. A collected branch filters labels to stable 10-by-15-base tiles
intersecting the viewport, and only when cells are readable. The full matrix
stays visible while this smaller text layer changes. This example uses
expression parameters rather than selection conditions, so it does not need
`gs.when()`.

See the [PISA squid plot](pisa_squid) for linked endpoint brushing and the
[official GenomeSpy matrix example](https://genomespy.app/docs/examples/genomic-data/bpreveal-pisa-matrix/)
for the original JSON specification.

:::{admonition} Data use and provenance
:class: note

This example uses a Parquet extract of the dm6 *sog* locus from the
[supporting data](https://doi.org/10.5281/zenodo.20318019) for McAnany et al.,
[*Positional interpretation of cis-regulatory code and nucleosome organization
with deep learning models*](https://doi.org/10.1038/s41467-026-74807-1), prepared
with the [GenomeSpy recipe](https://github.com/genome-spy/genomespy-dataset-recipes/tree/main/recipes/bpreveal-pisa).
The extract is distributed under [GPL-2.0-or-later](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html);
the accessibility model's training data are GEO accession
[GSE218852](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE218852).
:::
