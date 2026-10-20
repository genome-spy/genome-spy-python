# Upstream authoring contracts

These are source specifications from GenomeSpy revision
`7c0aaf3545d08841f109f2d95f8c664343893e73`, retrieved on 2026-10-20:

- [PISA interaction matrix](https://github.com/genome-spy/genome-spy/blob/7c0aaf3545d08841f109f2d95f8c664343893e73/examples/docs/examples/genomic-data/bpreveal-pisa-matrix.json)
- [UpSet mutations](https://github.com/genome-spy/genome-spy/blob/7c0aaf3545d08841f109f2d95f8c664343893e73/examples/docs/examples/generic/upsetr-mutations.json)
- [Clustered heatmap](https://github.com/genome-spy/genome-spy/blob/7c0aaf3545d08841f109f2d95f8c664343893e73/examples/docs/examples/generic/clustered-heatmap.json)

The gallery contract tests compare all properties except prose descriptions and
the Python wrapper's versioned `$schema` URL. Python-authored expressions are
compared with the upstream JavaScript expressions by their results across
representative inputs, including hidden/visible labels, reversed and narrow
domains, viewport tile boundaries, motif names, and cursor membership. These are
deliberate source text fixtures, not generated chart exports or rendering artifacts.
