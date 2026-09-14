Zoom horizontally with the mouse wheel. Point sizes increase as the view
narrows, making individual points easier to see. A size limit prevents the
points from growing indefinitely.

:::{admonition} Data use and provenance
:class: note

NumPy creates 200,000 positions and noise values with a fixed random seed.
GenomeSpy calculates the wave using the upstream formula. The gallery loads
the table from an Arrow file to keep the specification small.

Adapted from the [official GenomeSpy example](https://genomespy.app/playground/?spec=/docs/example-specs/docs/grammar/mark/point/geometric-zoom.json).
:::
