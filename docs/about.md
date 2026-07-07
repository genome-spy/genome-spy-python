# About

`genome-spy-python` is a Python wrapper for [GenomeSpy](https://genomespy.app),
analogous to how [Altair](https://altair-viz.github.io) wraps Vega-Lite. It
targets the reusable `@genome-spy/core` grammar first and expands toward the
richer cohort application concepts over time.

## Versioning and the GenomeSpy core pin

The chart API is generated from and validated against a pinned version of the
`@genome-spy/core` JSON schema. The examples in this documentation render with
that same pinned bundle, so what you see matches the grammar the API targets.

When the schema pin is bumped, the generated wrappers and the gallery are
regenerated together, and the documentation is rebuilt on the next release.

## Credits and references

- [GenomeSpy](https://github.com/genome-spy/genome-spy) — the underlying grammar
  and rendering engine.
- [Altair](https://github.com/vega/altair) — the design template for a
  schema-backed Python visualization API.
- Gallery datasets are synthetic and deterministic unless otherwise noted; see
  each example's source for how its data is generated.
