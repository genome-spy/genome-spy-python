## Inputs and adaptation

| Table | Fields | Meaning |
| --- | --- | --- |
| Probes | `Position:I`, `logR:Q` | Integer position and a probe measurement. |
| Segments | `startpos:I`, `endpos:I`, `segMean:Q` | Integer interval bounds and a prepared segment mean. |

Replace both URLs with accessible tables or pass prepared tables to `gs.Chart`.
Update field names and units; keep the x coordinates compatible across layers.
The means are supplied, not computed by this chart. Retain independent y scales
and axes only when comparing the two value mappings is intentional. Point size
also changes with zoom here; use a fixed size if that behavior is not needed.
GenomeSpy fetches and renders the URL data in the browser.

Points show individual probe measurements, and black lines show segment
means. Their positions share an x scale, but each layer has its own y scale
and axis. With independent scales, vertical overlap does not imply equal values.

:::{admonition} Data use and provenance
:class: note

This uses the two chromosome 19 copy-number tables hosted with GenomeSpy's
example. They are fetched directly, not bundled with this package. The source
specification does not identify the original study; this is a scale-resolution
demonstration, not a biological interpretation.

Adapted from the [official GenomeSpy example](https://genomespy.app/playground/?spec=/docs/example-specs/docs/grammar/composition/index/independent-resolution.json).
:::
