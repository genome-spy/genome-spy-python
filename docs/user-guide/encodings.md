# Encodings and channels

Channels map data fields to visual properties. Use the shorthand `field:type`
form or the explicit channel classes.

```python
import genome_spy as gs

gs.Chart(data).mark_point().encode(
    x=gs.X("pos:Q"),
    y=gs.Y("value:Q").scale(zero=False).title("Signal"),
    color=gs.Color("group:N").legend(title="Group"),
)
```

Type codes: `Q` quantitative, `N` nominal, `O` ordinal, `L` locus. Channel
classes expose schema-derived fluent setters such as `.scale(...)`, `.axis(...)`,
and `.legend(...)`.

:::{admonition} Work in progress
:class: note
This guide page is a scaffold. Expand it with the full channel list and
scale/axis/legend options.
:::
