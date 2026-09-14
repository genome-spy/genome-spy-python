The top track counts how many intervals cover each position. The bottom track
places overlapping intervals on separate rows. Zooming either track keeps
their horizontal positions aligned.

:::{admonition} Data use and provenance
:class: note

This adapts the upstream synthetic example with a deterministic mix of
interval lengths instead of random lengths, so it looks the same on each load.
NumPy creates the interval starts. GenomeSpy calculates their ends, coverage,
and row layout in the browser.

Adapted from the [official GenomeSpy example](https://genomespy.app/playground/?spec=/docs/example-specs/docs/grammar/transform/coverage/coverage-pileup.json).
:::
