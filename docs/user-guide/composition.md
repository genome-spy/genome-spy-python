# Composition

Combine charts into layered and concatenated views. Operators mirror Altair.

```python
import genome_spy as gs

layered = points + rules          # layer
stacked = gs.vconcat(track_a, track_b)   # vertical concat
side_by_side = gs.hconcat(a, b)          # horizontal concat
```

Composed charts can resolve shared scales, axes, and legends with
`resolve_scale(...)`, `resolve_axis(...)`, and `resolve_legend(...)`.

:::{admonition} Resolution caveat
:class: warning
GenomeSpy rejects mixing view-level `scales`/`axes`/`legends` with a
conflicting encoding-level channel config in the same resolution. Prefer
setting resolution at one level. See `plans/architecture.md` for details.
:::

:::{admonition} Work in progress
:class: note
This guide page is a scaffold. Expand it with worked layer and concat
examples pulled from `docs/examples/`.
:::
