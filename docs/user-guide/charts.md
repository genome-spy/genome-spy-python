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

:::{admonition} Work in progress
:class: note
This guide page is a scaffold. Expand it with a full mark catalog and
per-mark examples pulled from `docs/examples/`.
:::
