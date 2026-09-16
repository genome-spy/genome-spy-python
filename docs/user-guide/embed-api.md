# Control a live embed from Python

The experimental embed wrapper mirrors GenomeSpy's public browser API, using
snake_case method names. Calls are asynchronous because they execute in the
browser. It is separate from chart authoring and does not change chart JSON.

The first implementation supports top-level parameters, point and interval
selection reads/subscriptions/clearing, and record dataset replacement/reset.
Scoped views, scales, mark events, binary dataset loading, and exports are not
wrapped yet. Existing widget update methods remain available.

## Notebook connection

Display a widget, then attach to its live embed:

The repository's `notebooks/embed_api.ipynb` provides an executable example.

```python
import asyncio
import genome_spy as gs
from IPython.display import display

brush = gs.selection_interval("brush", encodings=["x"])
chart = (
    gs.Chart([{"x": 1, "y": 2}, {"x": 2, "y": 3}])
    .mark_point()
    .encode(x="x:Q", y="y:Q")
    .add_params(brush)
)
widget = chart.widget()
display(widget)

regions = []

async def connect():
    global api, selection, initial, stop
    async with asyncio.timeout(30):
        api = await widget.get_embed_api()
        selection = await api.params.get_selection("brush")
        initial = await selection.get_value()
        stop = await selection.subscribe(regions.append, {"delivery": "commit"})

connection_task = asyncio.create_task(connect())
```

Let the cell finish before interacting. In VS Code and other frontends that
process widget replies on the same channel as cell execution, top-level `await`
can block those replies. Start browser calls as background tasks instead. The
notebook example also displays connection failures and live selection values.

Brush the chart to append committed snapshots to `regions`. Snapshots retain
upstream fields such as `active`, `intervals`, and `complexIntervals`. Reading
the initial value is explicit: subscribing does not trigger an initial callback.
Without delivery options, subscriptions report every upstream change.

```python
clear_task = asyncio.create_task(selection.clear())  # Once connected.
stop_task = asyncio.create_task(stop())  # When finished listening.
```

Callbacks are synchronous Python functions on the attaching asyncio loop. Keep
them short; queue longer work separately. They do not automatically rerun
notebook cells. Callback exceptions reach the loop's exception handler.

All proxy calls must use the event loop where attachment occurred. Widget
button callbacks may run on another loop in JupyterLab: schedule their work
with `connection_task.get_loop().call_soon_threadsafe(start_action)`, where
`start_action` creates the async task. Calls from another loop are rejected
before sending an operation to the browser.

For charts declaring variable parameters or named datasets, the corresponding
calls are:

These `await` statements belong inside an async function scheduled with
`asyncio.create_task` when using VS Code.

```python
threshold = await api.params.get("threshold")
await threshold.set_value(5)
value = await threshold.get_value()

await api.datasets.set("annotations", [{"start": 100, "end": 150}])
await api.datasets.reset("annotations")
```

These names must exist in the chart's top-level declarations. Computed
parameters are read-only. Selection capabilities have no `set_value` method;
interval writes go through the generic parameter API using upstream's interval
representation. Arbitrary point-selection assignment is not supported.

## Other Python hosts

The wrapper does not import anywidget or notebook libraries. A host connects it
with `genome_spy.embed.attach_embed(send, subscribe)`:

```python
from genome_spy.embed import attach_embed

api = await attach_embed(host.send, host.subscribe)
```

`send(message)` sends a JSON message in order. `subscribe(callback)` registers
incoming messages and returns a function that removes the callback. These are
host-supplied transport functions, not a bundled web framework.

On the browser side, the host serves the packaged `static/embed-bridge.js`
module and connects it to its existing GenomeSpy embed:

```javascript
import { createEmbedBridge } from "./embed-bridge.js";

const bridge = createEmbedBridge(api, message => host.send(message));
const stopReceiving = host.subscribe(message => bridge.receive(message));

// Before replacing or destroying the embed:
stopReceiving();
bridge.dispose();
api.finalize();
```

`host` in these snippets stands for the application's transport, not a package
API. The browser integration tests exercise a non-notebook connection using
Playwright bindings, as well as the widget adapter. No Dash, Streamlit, or
production WebSocket adapter is supplied in this first slice.

## Lifecycle and limits

Keep one displayed frontend per connected widget. Replacing its specification
invalidates the old proxy; attach again explicitly. Hosts must dispose the
bridge on teardown so pending calls fail instead of hanging. Use a timeout when
attachment or a remote call could outlive the connection. Cancelling a wait
does not undo an operation already sent to the browser.

Only call `api.finalize()` when Python owns the embed lifecycle; notebook
widgets normally own their own cleanup. Static HTML without a live Python
connection cannot execute Python callbacks.

This initial transport accepts JSON-compatible values only. Unsupported values
and nonfinite numbers raise errors rather than being silently dropped. Binary
dataset transport remains available through the existing widget methods.

Synchronous event cancellation, DOM menus, and same-frame linking between
embeds still belong in browser JavaScript. Remote Python calls cannot preserve
that timing, and the wrapper does not introduce replacement APIs for it.
