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

`gs.concat(..., columns=2)` arranges three charts: the matrix, an accessibility
track on its right, and a contribution track below it. The genomic axes are
linked so that positions stay aligned when you pan or zoom. Each side track
has its own scale for the signal it shows.

The Python example provides URLs for prepared Parquet tables. GenomeSpy loads
and filters the data in the browser; Python does not load or process the tables.
Calculations using the visible x and y ranges decide when cells are large
enough for labels. When labels are visible, only rows near the visible region
are used to draw them. Their bounds are rounded to 10 bases horizontally and
15 bases vertically, so small pans do not continually rebuild the labels.

`EFFECT_COLOR_STOPS` pairs each effect value with its color. The chart uses
these pairs through `effect_scale`, preserving the reference example's white
center and green and pink extremes.

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
