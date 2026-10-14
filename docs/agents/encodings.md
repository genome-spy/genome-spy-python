# Encodings and composition

Use `Q` for quantitative fields, `N` for unordered categories, and `O` for ordered
categories. Encode actual table columns, including indexes deliberately exposed
as columns. Categories use nominal color; measurements use quantitative color.
Give units in axis titles and keep domains consistent with the field's meaning.

```python
import genome_spy as gs

rows = [{"x": 1, "y": 3, "group": "A"}, {"x": 2, "y": 2, "group": "B"}]
chart = (
    gs.Chart(rows).mark_point(filled=True)
    .encode(
        x=gs.X("x:Q").scale(zero=False).title("x"),
        y=gs.Y("y:Q").scale(zero=False).title("y"),
        color=gs.Color("group:N"),
        tooltip=["x:Q", "y:Q", "group:N"],
    )
)
chart.to_dict()
```

Authoring methods return new charts: retain the result of chained edits. Use `+`
for layers, `&` for vertical concatenation, and `|` for horizontal concatenation
when those operators express the intended composition. Layers may share scales;
use `resolve_scale(color="independent")` when color rules differ. Confirm shared
positions and scale direction in the browser.

Constant positional `gs.value(1)` refers to the far edge of a view, not one pixel.
Use band scales for labelled categories; reserve index scales for numbered
positions needing linear zoom/pan. Embedding geometry may need `zero=False`,
explicit domains, and equal coordinate-unit screen scaling.

See [scales and guides](scales-axes-legends.md), [current signatures](api.md), and
[reference fidelity](table-chart.md).
