# Use chart interactions in Python

Select a region in a chart and use its coordinates in your Python analysis.
You can also send results back to the chart—for example, to show saved
regions on an annotation track.

The example below does both. Drag across the chart, then release: Python adds
the region to a list called `annotations`, and a mark appears in the lower
track. The list stays in memory; restarting the example clears it.

The data is fictional: `chrDemo` has 1,000 bases. Coordinates are zero-based,
with the end excluded: an interval from 10 to 20 contains 10 bases.
Overlapping saved regions share one compact track.

The Python connection API used here is experimental.

## Try it in a notebook

Download these two files into the same folder:

- {download}`notebook.ipynb <../integration/notebook.ipynb>` — the notebook to open.
- {download}`component.py <../integration/component.py>` — the chart and Python
  code that handles selections.

Install the dependencies in the Python environment your notebook uses:

```sh
pip install "genome-spy-python>=0.4.0" ipywidgets ipykernel
```

Open the notebook in Jupyter or VS Code and select that environment's kernel
(the Python session running your cells). Run the first code cell and wait for
**Ready**. Drag across the chart and release. The status reports what Python
received, and the lower track shows the saved interval.

Run the next cell to inspect your results:

```python
annotations
```

Rerun that inspection cell after another selection to refresh its output.
The status above the list updates automatically.

### If it does not connect

Make sure you installed the package in the notebook's Python environment,
then restart the kernel and run the cells again. Wait for **Ready** before
selecting a region. Let the setup cell finish: keeping it waiting for a reply
can prevent that reply from arriving in VS Code.

## Add your own Python work

The notebook's widget provides the connection to Python. A background task
keeps listening for selections while you use other cells. Keep that setup
when adapting the example.

In `component.py`, `annotate()` waits for you to finish dragging, adds the
region to `annotations`, and updates the lower track. Put your own processing
after `annotations.append(record)`. In the notebook, you can also process
the list in another cell.

::::{dropdown} Chart and annotation code
```{literalinclude} ../integration/component.py
:language: python
```
::::

For named annotations and BED export, use
[Annotate genomic intervals](workflows/annotate-intervals.md). The other
[interactive workflows](workflows/index.md) show gene selection and sequence
editing. Their web demos run without Python; download their notebooks to
work with the results in Python.

(optional-run-the-same-example-as-a-web-app)=
## Optional: run the same example as a web app

Use this when you want a browser page to send selections to Python outside a
notebook. If you only want to share an interactive chart,
{ref}`save it as HTML <save-an-interactive-chart>` instead—no server is needed.

Put these files in one folder:

- {download}`component.py <../integration/component.py>` — the same Python code.
- {download}`server.py <../integration/server.py>` — the Python program that serves the page.
- {download}`index.html <../integration/index.html>` — the page shown in your browser.

[Install uv](https://docs.astral.sh/uv/getting-started/installation/) if needed.
Open a terminal in that folder and run:

```sh
uv run --with "genome-spy-python>=0.4.0" --with aiohttp server.py
```

Keep the command running and open <http://127.0.0.1:8080>. This address opens
the example on your own computer. Drag and release to save a region in Python.
Stop the program with Ctrl+C.

Each browser tab has its own Python list. Reloading that tab starts over.
Nothing is written to disk.

::::{dropdown} How the web connection works
The notebook normally provides the connection to Python. Here the example
server provides it instead, using [aiohttp](https://docs.aiohttp.org/en/stable/web_quickstart.html#websockets).

The page keeps a two-way connection, called a WebSocket, open to Python.
JavaScript draws the chart and passes messages back and forth; the shared
Python code decides what to save. Both sides use GenomeSpy's existing embed API.
::::

::::{dropdown} Python server
```{literalinclude} ../integration/server.py
:language: python
```
::::

::::{dropdown} HTML and JavaScript
```{literalinclude} ../integration/index.html
:language: html
```
::::

This is a local teaching example, not a public hosting setup. Publishing an
app requires additional security and decisions about storing users' results.
