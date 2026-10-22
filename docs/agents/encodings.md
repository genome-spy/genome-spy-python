# Encodings and composition

## Fields and types

Use actual column names: `Q` quantitative, `N` nominal, `O` ordinal. Put units in
titles; expose dataframe indexes as columns first.

```python
import genome_spy as gs

rows = [{"x": 1, "y": 3, "group": "A"}, {"x": 2, "y": 2, "group": "B"}]
chart = gs.Chart(rows).mark_point(filled=True).encode(
    x=gs.X("x:Q").scale(zero=False).title("x"),
    y=gs.Y("y:Q").scale(zero=False).title("y"),
    color="group:N",
    tooltip=["x:Q", "y:Q", "group:N"],
)
chart.to_dict()
```

## Distinct positions with repeated labels

Use stable position IDs when labels repeat. This keeps two observations separate;
their shared descriptive label remains available in the tooltip.

```python
import genome_spy as gs

rows = [
    {"slot": "visit-1", "label": "Follow-up", "score": 2},
    {"slot": "visit-2", "label": "Follow-up", "score": 4},
]
chart = gs.Chart(rows).mark_point(filled=True).encode(
    x=gs.X("slot:O").scale(type="band", domain=["visit-1", "visit-2"])
    .axis(title="Visit ID"),
    y=gs.Y("score:Q").axis(title="Score"),
    tooltip=["slot:N", "label:N", "score:Q"],
)
chart.to_dict()
```

Expected: two x positions. Encoding `label` instead would place both at the same
position. Preserve the position order across related panels.

## Layers and panels

Use `+` for layers, `|` for horizontal panels, and `&` for vertical panels.
Operators extend a matching composition on the left. Use
`gs.vconcat(group, detail)` to preserve a configured group as a nested view.
This complete example compares two measurements at the same positions.
Input: numeric `position`, `signal`, `score` (0–1), and categorical `group`.

```python
import genome_spy as gs

rows = [
    {"position": 1, "signal": 2, "score": 0.2, "group": "A"},
    {"position": 2, "signal": 7, "score": 0.5, "group": "B"},
    {"position": 3, "signal": 4, "score": 0.8, "group": "A"},
    {"position": 4, "signal": 8, "score": 0.6, "group": "B"},
]
base = gs.Chart(rows).mark_point(filled=True, size=80).encode(
    x=gs.X("position:Q").scale(domain=[0, 5], nice=False, zoom=True),
)
signal = base.encode(
    y=gs.Y("signal:Q").scale(domain=[0, 10], nice=False, zoom=False).title("Signal"),
    color=gs.Color("group:N")
    .scale(domain=["A", "B"], range=["#4c78a8", "#f58518"])
    .legend(title="Group", orient="bottom", columns=2),
    tooltip=["position:Q", "signal:Q", "group:N"],
)
score = base.encode(
    y=gs.Y("score:Q").scale(domain=[0, 1], nice=False, zoom=False),
    color=gs.Color("score:Q")
    .scale(domain=[0, 1], scheme="viridis", nice=False)
    .legend(title="Score", orient="bottom"),
    tooltip=["position:Q", "score:Q"],
).properties(height=180, title="Score")
labels = signal.mark_text(dy=-10).encode(text="group:N")
cutoff = gs.Chart([{"cutoff": 5}]).mark_rule(color="#667382").encode(
    y=gs.Y("cutoff:Q").scale(domain=[0, 10], nice=False, zoom=False).title("Signal"),
)
signal_panel = (cutoff + signal + labels).properties(
    height=180, title="Signal by group"
)
comparison = (
    (signal_panel & score)
    .resolve_scale(x="shared", y="independent", color="independent")
    .resolve_legend(default="collected")
    .properties(width=360, spacing=20)
    .configure_legend(direction="horizontal", titleOrient="top", columnPadding=20)
)
comparison.to_dict()
comparison.save("comparison.html", inline=True)
```

Expected: two stacked panels, four points per panel, labels and a cutoff line in
the upper panel, and separate, collected bottom guides. X zoom/pan moves both
panels; y ranges and color meanings stay independent. Replace records, fields,
domains and titles together. Put a layer's height/title on the combined view and
shared width on the vertical composition. For horizontal panels, replace `&`
with `|` and review dimensions and scale sharing.
Methods return new charts; retain the result. Confirm interactions in the browser.
Use the same intended axis title on layers sharing a scale; otherwise helper
fields such as `cutoff` can appear in the combined title.

## Marginal panels with surround

Use `gs.surround()` to place plots around a main chart. Use it for matrix
annotations and row or column summaries.

```python
import genome_spy as gs

rows = [{"position": 1, "signal": 2}, {"position": 2, "signal": 7}]
center = (
    gs.Chart().mark_point(filled=True)
    .encode(x="position:Q", y="signal:Q")
    .properties(width=320, height=180)
)
top = (
    gs.Chart().mark_tick(orient="vertical")
    .encode(x=gs.X("position:Q").axis(None))
    .properties(height=24)
)
right = (
    gs.Chart().mark_tick(orient="horizontal")
    .encode(y=gs.Y("signal:Q").axis(None))
    .properties(width=24)
)
chart = gs.surround(
    center,
    surround=gs.SurroundSides(
        top=gs.SurroundSideSpec(views=[top], spacing=4),
        right=[right],
    ),
    data=rows,
    spacing=8,
).with_scales(
    x=gs.Scale(domain=[0, 3], zoom=True),
    y=gs.Scale(domain=[0, 8], zoom=True),
)
chart.to_dict()
```

Expected: two points, two ticks above, and two ticks on the right. Top/bottom
plots share x with the center; left/right plots share y. Zoom keeps them aligned.
Other scales stay independent unless shared explicitly.

Set the center's width and height. Set only height on top/bottom plots and width
on left/right plots. Outer `spacing` separates sides from the center. Side-group
`spacing` separates tracks. Outer data and settings apply to all charts unless
overridden. Use outer `.with_scales(...)` for shared domains and zoom.

The center accepts unit, layer, and multiscale charts or imports of these.
Sides also accept surrounds. Put selections and rulers on individual plots.
See [the user guide](../user-guide/composition.md#add-plots-with-surround) for
examples and [the surround reference](https://genomespy.app/docs/grammar/composition/surround/)
for nesting and limits.

## Browser transforms

Use when the browser should filter or derive a visualization field:

```python
import genome_spy as gs

rows = [{"x": 1, "y": 3}, {"x": 2, "y": 2}]
transformed = (
    gs.Chart(rows).mark_point()
    .transform_filter(gs.datum.x > 1)
    .transform_calculate(total=gs.datum.x + gs.datum.y)
    .encode(x="x:Q", y="y:Q", size="total:Q")
)
transformed.to_dict()
```

Expected after rendering: one point at (2, 2), sized by `total=4`. Python serializes
the definitions; GenomeSpy evaluates them. The Python records do not change.
For row calculations, combined tests and conditional values, read
[Expressions](../user-guide/expressions.md).

## Constant positions

```python
import genome_spy as gs

edge_label = gs.Chart([{"label": "Right edge"}]).mark_text(align="right").encode(
    x=gs.value(1), y=gs.value(0.5), text="label:N"
)
edge_label.to_dict()
```

Positional `gs.value(1)` is the far edge, not one pixel. Use band scales for
labelled categories; index scales suit numbered positions needing zoom/pan.

See [scales and guides](scales-axes-legends.md), [API signatures](api.md), and
[reference checks](table-chart.md).
