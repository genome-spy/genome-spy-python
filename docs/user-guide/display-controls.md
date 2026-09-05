# Display controls and embed options

GenomeSpy Python adds SVG, PNG, and Inspector controls when it displays a chart.
The controls appear when the chart is hovered or receives keyboard focus.

```{literalinclude} ../tutorials/display_controls.py
:language: python
:start-after: display-controls-basic-start
:end-before: display-controls-basic-end
```

```{genomespy-chart} display_controls:chart
:height: 230
:title: Variant scores with export and Inspector controls
:controls: svg,png,inspector
```

| Control | What it does |
|---|---|
| `svg` | Downloads the current view as SVG. |
| `png` | Downloads the current view as PNG. |
| `inspector` | Opens the [GenomeSpy Inspector](https://genomespy.app/docs/api/inspector/), a developer view of the chart's live structure, dataflow, and parameters. |
| `full-window` | Expands the visualization; not enabled by default. |

## Choose or hide controls

Pass `controls=False` to hide all controls. Pass a list to choose the controls
and their order:

```{literalinclude} ../tutorials/display_controls.py
:language: python
:start-after: display-controls-override-start
:end-before: display-controls-override-end
:dedent: 4
```

Here is the same chart with only the PNG control:

```{genomespy-chart} display_controls:chart
:height: 230
:title: Variant scores with only the PNG control
:controls: png
```

The same option is available when retaining the notebook widget:

```{literalinclude} ../tutorials/display_controls.py
:language: python
:start-after: display-controls-widget-start
:end-before: display-controls-widget-end
:dedent: 4
```

Controls are display configuration and are not included in the chart
specification returned by `to_dict()` or `to_json()`.

## Embed options

`embed_options` are passed directly to GenomeSpy's `embed()` function. This
example selects the Canvas renderer:

```{literalinclude} ../tutorials/display_controls.py
:language: python
:start-after: display-controls-embed-options-start
:end-before: display-controls-embed-options-end
:dedent: 4
```

Controls and embed options can be configured together:

```python
chart.widget(
    controls=["png"],
    embed_options={"renderer": "canvas"},
)
```

See GenomeSpy's lists of [embed
options](https://genomespy.app/docs/api/embed-options/) and
[controls](https://genomespy.app/docs/api/embedding/#optional-controls).

## HTML output

The controls option also applies to generated HTML:

```{literalinclude} ../tutorials/display_controls.py
:language: python
:start-after: display-controls-output-start
:end-before: display-controls-output-end
:dedent: 4
```

JSON output contains only the chart specification, so it does not include
controls. See [Save and inspect charts](serialization.md) for JSON and HTML
output.

## Custom browser modules

By default, the widget and generated HTML load version-matched GenomeSpy
modules from jsDelivr. Self-hosted and offline setups can override
`bundle_url`, `controls_module_url`, and `inspector_module_url`. GenomeSpy's
[embedding guide](https://genomespy.app/docs/api/embedding/) lists the browser
entry points.
