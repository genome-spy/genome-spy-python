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

Positional channels can also be passed positionally to `.encode(...)` when the
channel object already knows its name:

```python
import genome_spy as gs

gs.Chart(data).mark_point().encode(
    gs.X("pos:Q").scale(zero=False),
    gs.Y("value:Q").scale(reverse=False),
    color=gs.Color("group:N"),
)
```

Use `gs.value(...)` for constant encodings, and use `None` to disable nested
schema objects such as legends or axes:

```python
gs.Color("group:N").legend(None)
gs.X("pos:Q").axis(None)
```
