# Save, export, and share charts

Save an interactive chart as an HTML file, or download a picture of the current
view. The examples below assume you have already created a `chart`; see
[Getting started](../getting-started.md) for a complete first example.

(save-an-interactive-chart)=
## Save an interactive chart

```python
chart.save("chart.html")
```

Open the file in a browser or share it with someone else. They do not need
Python to zoom, hover, or use interactions defined in the chart.

The file does **not** include a running Python session. Code that responds to
selections in Python needs a [live connection](embed-api.md).

For HTML as a string rather than a file, use `chart.to_html()`.

### Use it without internet access

By default, the HTML file downloads GenomeSpy's display code when opened.
Include that code in the file instead:

```python
chart.save("chart.html", inline=True)
```

The file is larger, but no download is needed for the display code. Data
supplied directly to the chart is included too. Data loaded from URLs still
needs network access; `inline=True` does not download those datasets.

## Download an image

Hover over the chart, or give it keyboard focus, to reveal its buttons.
Choose **PNG** for a raster image or **SVG** for a vector image. These capture
the current view, including its zoom.

Try the buttons on this chart:

```{genomespy-chart} display_controls:chart
:height: 230
:title: Variant scores with image export controls
:controls: svg,png,inspector
```

(choose-or-hide-the-buttons)=
## Choose or hide the buttons

The default buttons are PNG, SVG, and Inspector. Inspector is a developer tool
for examining a chart; you can hide it if you do not need it.

```{literalinclude} ../tutorials/display_controls.py
:language: python
:start-after: display-controls-override-start
:end-before: display-controls-override-end
:dedent: 4
```

Available names are `"png"`, `"svg"`, `"inspector"`, and `"full-window"`
(which expands the chart). Their order in the list sets their display order.

The same `controls` option works when keeping a notebook widget or saving HTML:

```{literalinclude} ../tutorials/display_controls.py
:language: python
:start-after: display-controls-widget-start
:end-before: display-controls-widget-end
:dedent: 4
```

```python
chart.save("chart.html", controls=False)
```

(save-json-or-html)=
## Save the chart definition as JSON

For another tool to load the chart definition, save JSON instead of HTML:

```python
chart.save("chart.json")
```

JSON stores the instructions and data references, not a displayed chart.
It does not include display buttons or Python callbacks.

## Inspect the specification

A *specification* is the collection of instructions GenomeSpy uses to draw the
chart: its data, marks, axes, and interactions. You normally do not need to
inspect it, but it can help when debugging or using the JavaScript API.

```{literalinclude} ../tutorials/serialization.py
:language: python
:start-after: serialization-dict-start
:end-before: serialization-dict-end
```

`chart.to_dict()` returns Python dictionaries and lists. For JSON text, use:

```{literalinclude} ../tutorials/serialization.py
:language: python
:start-after: serialization-json-start
:end-before: serialization-json-end
```

Both methods check the chart for validity by default. Data supplied directly
becomes JSON records; remote data remains a URL. The property names follow the
[GenomeSpy grammar](https://genomespy.app/docs/grammar/).

See the [API reference](../api.md) for serialization method options.
