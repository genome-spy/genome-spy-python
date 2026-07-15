# Charts and marks

A `Chart` pairs data with a mark and a set of encodings. Mark methods return a
new chart, so construction reads as a fluent chain.

```python
import genome_spy as gs

gs.Chart(data).mark_point().encode(x="pos:Q", y="value:Q")
```

Available mark methods are generated from the GenomeSpy `MarkType` grammar and
include `mark_point`, `mark_rect`, `mark_rule`, `mark_text`, and more. Mark
arguments (for example `size`, `filled`, `strokeDash`) map to GenomeSpy mark
properties.

Marks can be configured either inline on the mark method or later through the
generated config surface:

```python
import genome_spy as gs

chart = (
    gs.Chart(data)
    .mark_point(size=80, filled=True)
    .encode(x="x:Q", y="y:Q")
    .configure_mark(opacity=0.7)
)
```

Use `.properties(...)` for chart-level fields such as `width`, `height`,
`title`, and `description`. Use `chart.to_dict()` when you want to inspect the
final validated GenomeSpy specification.
