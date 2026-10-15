# Notebook display and export

## Validate and save

```python
import genome_spy as gs

chart = gs.Chart([{"x": 1, "y": 2}, {"x": 2, "y": 1}]).mark_point().encode(
    x="x:Q", y="y:Q"
)
spec = chart.to_dict()
spec_json = chart.to_json()
chart.save("chart.json")
chart.save("chart.html", inline=True)
```

Validation checks the spec, not the picture. Inline HTML bundles the runtime
and inline records, not URL datasets. It needs no running Python session.
JSON contains a spec and data references, not rendered output.

## Notebook

Continues **Validate and save**. Leave `chart` as the last cell expression, or
explicitly display it:

```python
chart.display(inline=True)
```

Continues **Validate and save**. Retain a widget when later code needs it:

```python
from IPython.display import display

view = chart.widget(inline=True)
display(view)
```

Creating a widget or running a notebook does not prove frontend rendering.

## Inspect an unfamiliar option

```python
import genome_spy as gs
import inspect

save_options = inspect.signature(gs.Chart.save)
legend_options = inspect.signature(gs.Color("x:Q").legend)
```

## Check and recover

| Check or failure | Action |
| --- | --- |
| Export succeeded | Open it; check marks, axes, labels, guides, readability and a known tooltip. |
| Regenerated artifact | Confirm the latest file loaded; embedded previews can stay stale. |
| Blank chart | Inspect page/resource errors and field/domain definitions; keep validation enabled. |
| Files cannot open | Use a supported preview. Any HTTP preview must serve only the output directory on loopback. |
| Image download fails | Keep HTML; use a screenshot if available. Bound waits. |
| No browser or hover tool | Report visual/hover checks as unverified, separately from successful export. |

Deliver source and the requested artifact, with processing and verification limits.
See [quickstart](quickstart.md) and [visual comparison checks](table-chart.md).
