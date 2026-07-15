# Composition

Combine charts into layered and concatenated views.

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

Layering is useful when multiple marks share the same coordinate system:

```python
import genome_spy as gs

points = gs.Chart(data).mark_point().encode(x="x:Q", y="y:Q")
labels = gs.Chart(data).mark_text(dy=-10).encode(x="x:Q", y="y:Q", text="label:N")

chart = (points + labels).properties(width=360, height=220)
```

Concatenation is useful when you want stacked browser tracks or side-by-side
views that keep their own marks and encodings but share some top-level config.
