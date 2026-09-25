Each diagonal link joins an influential input base to an affected ATAC-seq
output position around the *Drosophila sog* enhancer, following Figure 2c of
McAnany et al. Accessibility, contribution scores, and motif intervals provide
context on the same genomic scale.

## What to notice

Positive effects are red and negative effects are blue; opacity shows effect
magnitude. Drag on **Accessibility** to select output positions, or on
**Contribution score** to select input positions. Links matching both active
brushes retain their effect encoding and draw above muted links. An empty brush
leaves its endpoint unconstrained. Bars and sequence letters outside an active
brush turn gray.

Hold **Shift** and hover to highlight a link, including one outside the brushes.
With no active brush or Shift-hover, all links look normal. Double-click a track
to clear its brush. Pan and zoom to inspect the locus; zooming in reveals
base-colored letters in the contribution track.

## How the chart is built

Python authors the chart and references the prepared remote Parquet tables;
it does not load or recalculate PISA effects. GenomeSpy loads the tables and
executes the declarative filters and formulas in the browser. These select the
margin tracks, calculate absolute effect magnitude, and format motif labels.

The link view defines one `highlightedLink` predicate combining Shift-hover
with interval brushes projected onto `x` (input) and `x2` (output).
`gs.when({"ref": "highlightedLink"})` reuses it for color, opacity, and draw
order. The `+` and `&` operators layer the motif annotations and stack the tracks.

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
