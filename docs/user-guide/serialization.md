# Save and inspect charts

A GenomeSpy Python chart can be converted to the JSON-compatible specification
that GenomeSpy renders in the browser. Most readers only need this when saving a
chart, passing it to another tool, or inspecting the generated grammar.

## Inspect the specification

`to_dict()` returns the complete specification as Python dictionaries, lists,
strings, and numbers:

```{literalinclude} ../tutorials/serialization.py
:language: python
:start-after: serialization-dict-start
:end-before: serialization-dict-end
```

The result uses GenomeSpy property names. For example, `gs.X("sample:N")`
becomes an x-channel definition with `field` and `type`. The root `$schema` URL
identifies the GenomeSpy schema used to validate the chart. Those property names
are the ones documented in the
[GenomeSpy grammar](https://genomespy.app/docs/grammar/), so a serialized chart
can be read against it directly.

Use `to_json()` when another program expects JSON text:

```{literalinclude} ../tutorials/serialization.py
:language: python
:start-after: serialization-json-start
:end-before: serialization-json-end
```

Both methods validate the chart by default. Inline tables become ordinary JSON
records, while URL and lazy data sources remain URLs for the browser to load.

## Save JSON or HTML

The filename extension selects JSON or standalone HTML output:

```{literalinclude} ../tutorials/serialization.py
:language: python
:start-after: serialization-save-start
:end-before: serialization-save-end
```

```python
from pathlib import Path

json_path, html_path = save_examples(Path("output"))
```

The JSON file contains the validated specification. The HTML file contains the
chart container and embedding code, but still loads the GenomeSpy JavaScript
bundle and any remote datasets over the network. Inline data is included in the
file.

Use `chart.to_html()` when integration code needs the HTML as a string rather
than a file. Complete method signatures and validation options are listed in the
[API reference](../api.md).

The generated HTML calls GenomeSpy's own `embed` function. To adapt it for
another page or build system, see
[embedding](https://genomespy.app/docs/api/embedding/) and the available
[embed options](https://genomespy.app/docs/api/embed-options/), which
`chart.widget(embed_options=...)` also accepts.

`embed_options` configures the browser embedding step; it does not change the
chart specification. The optional PNG, SVG, Inspector, and full-window controls
provided by GenomeSpy are attached after embedding and are not currently exposed
by a Python chart method. They therefore cannot be generated from the
visualization schema; see GenomeSpy's
[controls documentation](https://genomespy.app/docs/api/embedding/#optional-controls)
for the current browser-level contract. In that contract, authors choose an
ordered control list and may set placement, visibility, and error handling;
PNG and SVG exports also accept a filename and export settings.
