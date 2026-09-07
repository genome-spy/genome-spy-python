## What to notice

Drag the overview to choose the positions shown below. Residue tiles, summary
bars, and consensus share the detail scale, so zooming or panning keeps them
aligned. Hover a tile for its accession and position. Zoom in to read letters.

**Identity** is the most common amino acid's fraction of all 34 sequences at a
position. **Coverage** is the fraction with a residue there. Consensus picks the
most common residue, breaking ties alphabetically. Grey cells pad shorter rows.

This adapts [Dash Bio AlignmentChart](https://dash.plotly.com/dash-bio/alignmentchart)
with GenomeSpy rectangles, text, bars, and a shared brush. The summary uses
identity rather than Dash Bio's default entropy score.

:::{admonition} Data use and provenance
:class: note

The [p53 FASTA](https://github.com/plotly/datasets/blob/0c447c47b757ad74edecab31f0d72f849d2e67c2/Dash_Bio/Genetic/alignment_viewer_p53.fasta)
is from Plotly's MIT-licensed datasets repository: 34 UniProt-labelled sequences
of 207–396 residues. These are **unequal-length, ungapped sequences**, not a
multiple-sequence alignment. Matching column numbers do not establish homologous
positions or evolutionary conservation. Python preserves the source order and
residues, pads shorter rows, and calculates summaries; it does not perform an
alignment. All chart data are packaged locally. For aligned input, see
[Multiple sequence alignment](multiple_sequence_alignment.md).
:::
