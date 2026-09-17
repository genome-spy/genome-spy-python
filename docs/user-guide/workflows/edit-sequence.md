# Edit a sequence

{download}`Download the notebook <../../../notebooks/edit_sequence.ipynb>`

Click an A/C/G/T letter to choose the nucleotide at that position. Chosen bases
use their nucleotide colors; the other letters fade to gray. The reference and
edited sequence use the same colors. Changes from the reference are outlined
in the grid.

```{genomespy-workflow} sequence
```

Download FASTA to keep both sequences. **Reset to reference** undoes all edits;
reloading also resets the demo. Positions are 1-based, not genomic coordinates.

## Code

A point-selection hook receives the clicked cell. It updates the named datasets
for the edited sequence and grid, leaving the reference unchanged.
The web demo uses JavaScript; run these Python hooks in the notebook.

::::{dropdown} Chart specification (Python)
```{genomespy-workflow} sequence
:code: chart
```
::::

::::{dropdown} Python hooks
```{genomespy-workflow} sequence
:code: hooks
```
::::

:::{admonition} Data use and provenance
:class: note

An invented 24-base sequence for demonstrating editing, not a biological
reference or a prediction of mutation effects. Inspired by GenomeSpy's
[sequence editor](https://genomespy.app/docs/api/embed-examples/sequenceEditor/).
:::
