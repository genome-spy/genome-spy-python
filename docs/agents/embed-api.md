# Live charts: the Python Embed API

Use this API to connect a displayed chart to Python: read selections, change
parameters, and send results back. Requires a running notebook kernel and
`genome-spy-python`; exported HTML alone has no Python connection. This API is
experimental. Check [installed signatures](api-embed.md) when versions differ.

## Notebook roundtrip

Run the Python blocks below as consecutive notebook cells. The four synthetic
records need no data files or dataframe dependencies. Python filters the supplied
records; GenomeSpy renders the results. Brush the upper plot and release: the
lower plot receives the selected rows through a declared dataset.
Interval brushes send ranges, not records. Retain the plotted table in Python
and match the actual plotted fields, including any coordinate transformations.
For point marks, use half-open bounds (`lower <= value < upper`) on every
brushed channel, matching GenomeSpy's native selection predicate.

```python
import genome_spy as gs

rows = [
    {"id": "a", "x": 1, "y": 3, "group": "A"},
    {"id": "b", "x": 2, "y": 1, "group": "A"},
    {"id": "c", "x": 3, "y": 4, "group": "B"},
    {"id": "d", "x": 4, "y": 2, "group": "B"},
]
point_size = gs.param("pointSize", value=90)
brush = gs.selection_interval("brush", encodings=["x"], on={"type": "mousedown"})
base = (
    gs.Chart()
    .mark_point(filled=True, size=point_size)
    .encode(
        x=gs.X("x:Q").scale(domain=[0, 5]).title("X"),
        y=gs.Y("y:Q").scale(domain=[0, 5]).title("Y"),
        color=gs.Color("group:N").scale(domain=["A", "B"]).legend(title="Group"),
        tooltip=["id:N", "x:Q", "y:Q", "group:N"],
    )
)
overview = base.properties(
    data=rows, name="overview", width=480, height=160, title="Brush and release"
)
detail = base.properties(
    data={"name": "selected"}, width=480, height=160, title="Rows returned by Python"
)
chart = (
    (overview & detail)
    .properties(datasets={"selected": []})
    .add_params(point_size, brush)
)
chart.to_dict()
```

Continues the chart. Setup runs in a background task so the cell can finish and
browser replies can arrive, including in VS Code. Wait for **Ready** before
brushing. Rerunning this cell stops the previous listener and closes its widget.

```python
import asyncio
import ipywidgets as widgets
from IPython.display import display


async def connect(previous_task, previous_widget):
    global widget, status, api, selection, selected_rows
    if previous_task is not None:
        previous_task.cancel()
        await asyncio.gather(previous_task, return_exceptions=True)
    if previous_widget is not None:
        previous_widget.close()
    selected_rows = []
    api = selection = None
    widget = chart.widget(inline=True, controls=False)
    status = widgets.Label("Connecting…")
    display(widget, status)
    stop = None
    try:
        events = asyncio.Queue()
        async with asyncio.timeout(30):
            api = await widget.get_embed_api()
            selection = await api.params.get_selection("brush")
            stop = await selection.subscribe(events.put_nowait, {"delivery": "commit"})
            events.put_nowait(await selection.get_value())
        while True:
            snapshot = await events.get()
            interval = snapshot["intervals"].get("x")
            selected_rows = (
                [row for row in rows if min(interval) <= row["x"] < max(interval)]
                if snapshot["active"] and interval is not None
                else []
            )
            async with asyncio.timeout(30):
                await api.datasets.set("selected", selected_rows)
            status.value = f"Ready: {len(selected_rows)} selected"
    except Exception as error:
        status.value = f"Connection failed: {type(error).__name__}: {error}"
        raise
    finally:
        if stop is not None:
            async with asyncio.timeout(2):
                await stop()


connection_task = asyncio.create_task(
    connect(globals().get("connection_task"), globals().get("widget"))
)
```

Inspect `selected_rows` in another cell. A brush from 1.5 to 3.5 selects IDs
`b` and `c`; an empty range or clearing produces `[]` and empties the lower plot.
Subscriptions deliver future changes only; the explicit initial read handles
startup. `commit` avoids doing Python work on every pointer move. Callbacks are
synchronous: the queue lets the background task await dataset updates in order.

## Read, write, and clear

Continues after **Ready**. Define this coroutine, then run
`operation_task = asyncio.create_task(change_chart())` in another cell. Check
`operation_task.result()` after it finishes to surface errors.

```python
async def change_chart():
    async with asyncio.timeout(30):
        size = await api.params.get("pointSize")
        before = await size.get_value()
        await size.set_value(140)
        assert await size.get_value() == 140
        view = await api.views.get({"scope": [], "view": "overview"})
        scoped_size = await view.params.get("pointSize")
        assert await scoped_size.get_value() == 140
        await selection.clear()
    return before
```

`api.params` starts at the authored root; `view.params` starts at the resolved
view's lexical scope. Use the declaring view when a child shadows an outer
parameter. Computed parameters are readable but not writable. Point selections
support read, subscribe, and clear; assigning their snapshots is unsupported.

| Selection | Snapshot fields |
| --- | --- |
| Point | `type`, `active`, `data`: selected dataflow records. Join to source rows using stable authored IDs, not row positions. |
| Interval | `type`, `active`, `intervals`: numeric ranges by channel; cleared channels can be `null`. |
| Genomic interval | `complexIntervals`: `{chrom, pos}` endpoints; positions are zero-based. Numeric channels remain numeric. |

See [point selections](../user-guide/workflows/pick-genes.md) and
[genomic interval roundtrips](../user-guide/embed-api.md) for complete examples.
`IntervalSelectionApi.contains()` takes canvas-relative CSS pixels, not data or
genomic coordinates.

## Update data

| Operation | Use when |
| --- | --- |
| `await api.datasets.set(name, records)` | Replace a dataset declared in the authored root's `datasets`; JSON-compatible rows only. |
| `await api.datasets.reset(name)` | Restore that dataset's configured values. |
| `widget.set_dataset(name, table)` | Update a dataset in the widget's fixed manifest; Arrow is the default and requires the `arrow` extra. Use `format="records"` for JSON records. |
| `widget.set_data(table)` | The widget has exactly one declared live dataset. |

Runtime dataset calls target the exact root owner; they do not search child
views. Widget manifest names must be unambiguous; nested declarations need a
named owner. `widget.dataset_names` lists those names. Widget updates retain a
synchronized payload; runtime calls operate directly on the live embed.
An awaited runtime update confirms the setter returned, not that a new frame
has rendered. Check the visible result separately.

For separate widgets, attach to each displayed widget and call the target
embed's dataset API. They have independent dataflows; a declarative selection
filter in one embed does not update another embed.

## Call from widget callbacks

Continues after **Ready**. Widget callbacks can run on a different event loop
from notebook cells. Schedule API work on the connection task's loop; using
`asyncio.create_task()` inside the callback can select the wrong loop.

```python
def change_from_button(_):
    global operation_future
    operation_future = asyncio.run_coroutine_threadsafe(
        change_chart(), connection_task.get_loop()
    )


button = widgets.Button(description="Change chart")
button.on_click(change_from_button)
display(button)
```

Keep the callback nonblocking. Inspect `operation_future.result()` after it
finishes to surface errors. Subscription callbacks already run on the attaching
loop; the queue in the roundtrip example keeps their asynchronous work ordered.

## Stop or reconnect

Continues the notebook. Run `cleanup_task = asyncio.create_task(stop_example())`
when finished. Awaiting `stop()` releases the subscription; closing the widget
owns frontend teardown. Use `api.finalize()` only when you own the embed lifecycle.

```python
async def stop_example():
    connection_task.cancel()
    try:
        await connection_task
    except asyncio.CancelledError:
        pass
    finally:
        widget.close()
```

Keep calls on the event loop that attached the proxy and display each connected
widget once. Re-embedding needs a new proxy; stale handles raise `EmbedError`.
If **Ready** never appears, check the widget frontend and kernel environment,
let the setup cell finish, and inspect `connection_task` for failure. Time out
remote calls; do not blindly retry writes.

## Python versus JavaScript

| Capability | Python connection | JavaScript embed |
| --- | --- | --- |
| Parameters and selections | Async reads/writes where supported, subscriptions, clear | Native runtime handles |
| Datasets | Root JSON set/reset; widget transport also supports Arrow | Root and scoped dataset APIs, binary loading |
| Views | Resolve a view's parameter namespace | Hierarchy, layout bounds, marks, and supported mutations |
| Named-scale domains and programmatic zoom | Not wrapped | Supported |
| Mark events, inspector, live image export | Not wrapped by the Python proxy | See upstream API |

Python's `get_value()`/`set_value()` calls are asynchronous; JavaScript examples
use methods such as `getValue()`/`setValue()`. Do not translate unwrapped methods
into invented Python calls. Check the installed Python and bundled GenomeSpy
versions before adapting newer upstream examples.

- [JavaScript embedding](https://genomespy.app/docs/api/embedding/): entry points and mounting.
- [JavaScript runtime state](https://genomespy.app/docs/api/runtime-state/): datasets, scales, and parameters.
- [JavaScript view hierarchy](https://genomespy.app/docs/api/views/): scoped handles, marks, layout, and mutations.

For a Python web host outside notebooks, reuse the
[existing server example](../user-guide/embed-api.md#optional-run-the-same-example-as-a-web-app).
It uses `attach_embed` and the browser bridge; standalone HTML export needs neither.
