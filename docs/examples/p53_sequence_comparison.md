## What to notice

Drag the overview at the bottom to choose the positions shown above. The
summary tracks, consensus logo, and residue matrix stay aligned as the view
moves. Move the pointer across the detail tracks to follow one position with
the vertical ruler. Hover a tile for its accession and position. Zoom in to
read letters.

**Conservation** shows how many sequences share the most common amino acid at
each position. **Gap-free** shows how many sequences contain a residue there;
it stays full until the shorter sequences begin to end. The consensus row shows
the most common residue, while the logo shows the full residue mixture with
larger letters for larger shares.

This adapts [Dash Bio AlignmentChart](https://dash.plotly.com/dash-bio/alignmentchart)
with GenomeSpy rectangles, text, bars, a sequence logo, and a shared brush.

:::{admonition} Data use and provenance
:class: note

The [p53 FASTA](https://github.com/plotly/datasets/blob/0c447c47b757ad74edecab31f0d72f849d2e67c2/Dash_Bio/Genetic/alignment_viewer_p53.fasta)
is from Plotly's MIT-licensed datasets repository: 34 UniProt-labelled sequences
of 207–396 residues. These are **unequal-length, ungapped sequences**, not a
multiple-sequence alignment. The packaged data preserve the source order, pad
shorter rows, and calculate position summaries; they do not perform an
alignment. “Conservation” therefore means position-wise agreement here, not
evolutionary conservation. For aligned input, see
[Multiple sequence alignment](multiple_sequence_alignment.md).
:::
