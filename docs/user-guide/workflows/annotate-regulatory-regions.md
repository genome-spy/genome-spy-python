# Review regulatory regions

{download}`Download the notebook <../../../notebooks/annotate_squid.ipynb>`

Which sequence regions around the *Drosophila sog* enhancer deserve follow-up?
Use the PISA squid plot to inspect model-predicted effects, then record your
candidate regions and reasons in an independent review table.

1. Drag on **Contribution score** to select input bases. Optionally drag on
   **Predicted accessibility** to focus on an output region.
2. Right-click inside the selected input region and choose **Add annotation**.
   The dialog freezes both ranges while you write.
3. Enter a name without spaces, add a note, choose a color, and save.
4. Double-click the track to clear its brush. Your annotation remains in a separate, untitled track below the contribution scores on the same genomic axis and in
   **Saved annotations**, an ordinary HTML table outside GenomeSpy.
5. Download the review CSV or input BED and open it in another application.

```{genomespy-workflow} squid
```

Use **Edit** or **Remove** beside a saved row to correct a review. Browser
records last until the page reloads; download them before leaving. The notebook uses its existing inline controls rather than the browser context
menu and dialog. It stores records in the Python list `annotations` and displays a pandas table.
Its remove control lets you discard an annotation and save a corrected one.

## Reading the evidence

Red links indicate positive PISA effects and blue links negative effects.
Brushing the bottom track constrains input positions; brushing the top track
constrains output positions. Both active ranges constrain the highlighted links.
Zoom in to see reference bases in the contribution track. Shift-hover can
highlight an individual link, but it does not change a frozen annotation.

The top track is a model prediction. Source motif calls and contribution scores
provide context for a review decision; they do not establish experimental
binding or causality. Saved review marks are distinct from the source motifs.
No model inference or experimental analysis runs when you select or annotate.

## What leaves the visualization

CSV contains the annotation ID, assembly, chromosome, input interval, name,
note, chosen color, optional output interval, and source dataset version.
The notebook also has a proposed follow-up field.
BED contains only input chromosome, start, end, and name. It omits color, notes, and
output context. Empty output fields mean that no output brush was active.

All saved intervals use **dm6 chrX, 0-based, half-open coordinates**. Both brush
boundaries are rounded up to integer base edges. The right edge is exclusive;
no extra base is added. Ranges are clipped to available input/output data.
There must be at least one included base. Frozen drafts do not follow later
brush changes, and clearing brushes does not erase saved reviews.

## Code

Python authors the chart with prepared remote Parquet inputs. GenomeSpy loads
those tables and runs the chart's declarative transforms in the browser.
The web example uses JavaScript embed hooks to own, display, and export review
records. The notebook uses the corresponding Python hooks with a live kernel.
This workflow uses the Canvas renderer for the literal colors stored in each
annotation record. Label text automatically contrasts with its color.

::::{dropdown} Chart specification (Python)
```{genomespy-workflow} squid
:code: chart
```
::::

::::{dropdown} Python hooks and controls
```{genomespy-workflow} squid
:code: hooks
```
::::

See the [squid gallery example](../../gallery/pisa_squid) for the visualization
grammar and the [official GenomeSpy example](https://genomespy.app/docs/examples/genomic-data/bpreveal-pisa-squid/)
for the original specification.

:::{admonition} Data use and provenance
:class: note

This example uses the v3 Parquet extract of the dm6 *sog* locus from the
[supporting data](https://doi.org/10.5281/zenodo.20318019) for McAnany et al.,
[*Positional interpretation of cis-regulatory code and nucleosome organization
with deep learning models*](https://doi.org/10.1038/s41467-026-74807-1), prepared
with the [GenomeSpy recipe](https://github.com/genome-spy/genomespy-dataset-recipes/tree/main/recipes/bpreveal-pisa).
The remote extract is distributed under GPL-2.0-or-later. The accessibility
model's training data are GEO accession GSE218852. User review annotations
are created in this application and are not part of the source study.
:::
