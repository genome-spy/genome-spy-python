Each diagonal link joins an influential input base to an affected ATAC-seq
output position around the *Drosophila sog* enhancer, following Figure 2c of
McAnany et al. Accessibility, contribution scores, and motif intervals provide
context on the same genomic scale.

## What to notice

Positive effects are red and negative effects are blue; opacity shows effect
magnitude. Drag on **Accessibility** to select output positions, or on
**Contribution score** to select input positions. Links within both selected
ranges keep their colors and appear above gray links. Clearing a brush removes
the restriction on that end of the link. Bars and sequence letters outside an
active brush turn gray.

Hold **Shift** and hover to highlight a link, including one outside the brushes.
With no active brush or Shift-hover, all links look normal. Double-click a track
to clear its brush. Pan and zoom to inspect the locus; zooming in reveals
base-colored letters in the contribution track.

## How the chart is built

The Python example defines the chart using URLs for prepared Parquet tables.
GenomeSpy loads those tables in the browser, filters the rows for each track,
and calculates the values used for opacity and motif labels. Python does not
load the tables or recalculate the PISA effects.

The `highlighted_link` condition decides which links to highlight using the
input brush, output brush, and Shift-hover selection. The chart names this
condition `highlightedLink` so that color, opacity, and drawing order all use
the same rule. See {ref}`combine-selections`
for how to write and reuse these conditions.

The `+` operator places the motif annotations over the links; `&` stacks the
tracks vertically. `EFFECT_COLOR_STOPS` pairs each effect value with its color,
and `effect_scale` applies those pairs to the links.

See the [PISA interaction matrix](pisa_interaction_matrix) for the full effect
field and the [official GenomeSpy squid example](https://genomespy.app/docs/examples/genomic-data/bpreveal-pisa-squid/)
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
