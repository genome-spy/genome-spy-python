# Notebook display and export

This example builds a chart before displaying or saving it:

```python
import genome_spy as gs

chart = gs.Chart([{"x": 1, "y": 2}, {"x": 2, "y": 1}]).mark_point().encode(
    x="x:Q", y="y:Q"
)
spec = chart.to_dict()
chart.save("chart.json")
chart.save("chart.html", inline=True)
```

In a notebook, leave `chart` as the last expression or use
`chart.display(inline=True)`. Retain `view = chart.widget(inline=True)` and display
`view` for a reusable widget. Constructing a widget or executing a notebook does
not verify that the frontend displayed it.

`to_dict()` and `to_json()` validate a spec, not a picture. Inline HTML bundles the
runtime and inline records; it does not download URL datasets or require a running
Python session. JSON contains specs and data references, not rendered output or
a live connection.

Verify actual marks, axes, labels, guides, readability, a known record's tooltip,
and relevant page/resource errors. Check freshness after regenerating artifacts:
embedded previews can retain an older chart. If frontend checks are unavailable,
state that limit separately from successful serialization/export.

For blank charts, inspect browser errors and field/domain definitions; keep
validation enabled. Use a supported preview path. A permitted local HTTP preview
must bind loopback and serve only the output directory. If image download fails,
retain HTML and use a screenshot when available. Bound export waits and record
hover/export limits separately from rendering. Deliver source and the requested
artifact with processing and verification notes.

See [the quickstart](quickstart.md) and [visual comparison checks](table-chart.md).
