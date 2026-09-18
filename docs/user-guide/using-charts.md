# Using and sharing charts

The previous sections covered chart definitions and interactions. This section
covers displaying those charts, exporting them, and connecting their
interactions to Python code.

GenomeSpy executes the chart's specification in JavaScript, including in
notebooks. Zooming, selections, and declarative transforms run in the browser,
so exported HTML can remain interactive without Python. Receiving selections
or sending new data from Python requires a live connection, provided by the
notebook widget or an application server.

- [Charts in notebooks](notebooks.md): display charts and update their data
  from later cells.
- [Save, export, and share charts](serialization.md): export HTML, images, or
  specifications, and configure display controls.
- [Use chart interactions in Python](embed-api.md): receive selections and
  send results back, with notebook and optional web-app examples.
- [Interactive workflows](workflows/index.md): apply these patterns to interval
  annotation, gene selection, and sequence editing. The web demos use
  JavaScript; the downloadable notebooks connect the results to Python.

```{toctree}
:hidden:
:maxdepth: 2

notebooks
serialization
embed-api
workflows/index
```
