# About

`genome-spy-python` is a Python wrapper for [GenomeSpy](https://genomespy.app).
It targets the reusable `@genome-spy/core`
[grammar](https://genomespy.app/docs/grammar/) first and expands toward the
richer [cohort application](https://genomespy.app/docs/sample-collections/)
concepts over time.

If you know Altair or Vega-Lite, the grammar will look familiar. GenomeSpy
adds three things for genomics:

- locus scales that place chromosome and position on one continuous axis;
- lazy sources for indexed formats such as BigWig, BAM, and GFF3, which load
  only the visible region;
- GPU rendering, so a track stays interactive with millions of marks.

## Versioning and the GenomeSpy core pin

The chart API is generated from and validated against a pinned version of the
`@genome-spy/core` JSON schema. The examples in this documentation render with
that same pinned bundle, so what you see matches the grammar the API targets.
Where this documentation is silent about a property, the
[GenomeSpy documentation](https://genomespy.app/docs/grammar/) is the reference.

When the schema pin is bumped, the generated wrappers and the gallery are
regenerated together, and the documentation is rebuilt on the next release.

## Credits and references

- [GenomeSpy](https://github.com/genome-spy/genome-spy) — the underlying grammar
  and rendering engine, and its
  [documentation](https://genomespy.app/docs/).
- Example pages show the exact Python source used to build each visualization.
