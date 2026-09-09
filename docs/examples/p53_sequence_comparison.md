## What to notice

Drag the overview at the bottom to choose the positions shown above. The
summary tracks, sequence logo, and residue matrix stay aligned as the view
moves. Move the pointer across the detail tracks to follow one position with
the vertical ruler. Hover a tile for its accession and position. Zoom in to
read letters.

**Conservation** shows the fraction of non-gap sequences that share the most
common amino acid at each alignment column. **Gap-free** shows
the fraction of sequences containing a residue there. Keeping the two measures
separate makes it clear whether a low score reflects disagreement or missing
aligned residues. The sequence logo shows the full non-gap residue mixture,
with larger letters for larger shares. The x-axis reports one-based alignment
columns, not residue numbers in any individual protein.

This adapts [Dash Bio AlignmentChart](https://dash.plotly.com/dash-bio/alignmentchart)
with GenomeSpy rectangles, text, bars, a sequence logo, and a shared brush.

:::{admonition} Data use and provenance
:class: note

The 34 UniProt-labelled p53 protein sequences come from the
[Plotly FASTA](https://github.com/plotly/datasets/blob/0c447c47b757ad74edecab31f0d72f849d2e67c2/Dash_Bio/Genetic/alignment_viewer_p53.fasta)
in Plotly's MIT-licensed datasets repository. They were aligned with MAFFT
v7.526 using the L-INS-i strategy:
`mafft-linsi p53.unaligned.fasta > p53.aligned.fasta`. The resulting alignment
is packaged as `p53_sequence_comparison_aligned.fasta.gz`.
:::

## Python and GenomeSpy processing

Python reads the packaged compressed FASTA, splits its 34 records, preserves
the UniProt identifiers and headers, and verifies that every aligned sequence
has the same length. GenomeSpy then flattens each sequence into residues in the
browser and declaratively calculates gap-free fractions, non-gap conservation,
and logo stacks. The Python API authors and serializes
those transforms; GenomeSpy executes them while rendering and interacting with
the visualization. For comparison, the
[multiple sequence alignment example](multiple_sequence_alignment.md) sends
FASTA directly to GenomeSpy and parses it in the browser-side dataflow.
