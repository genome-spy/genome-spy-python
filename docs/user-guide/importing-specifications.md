# Import remote view specifications

{py:func}`~genome_spy.import_view` adds a view whose GenomeSpy JSON specification lives
in another file. This is useful for composing published, reusable tracks or for
splitting a large visualization into independently maintained specifications.
The Python package records the import definition; GenomeSpy fetches the remote
JSON in the browser when the chart is rendered.

## Import and compose a view

Pass an absolute or relative specification URL and place the imported child in
a composition. This example imports a small layered bar chart with inline data
from GenomeSpy's repository:

```{literalinclude} ../tutorials/importing_specifications.py
:language: python
:start-after: remote-spec-import-start
:end-before: remote-spec-import-end
```

```{genomespy-chart} importing_specifications:imported_chart
:height: 300
:title: A layered bar chart loaded from a remote JSON specification
```

The JSON file contains the data, shared encodings, and two layers: bars and
their value labels. The Python code only declares where GenomeSpy should load
that view. The one-child `vconcat` supplies the parent view context that URL
imports require.

An imported specification may contain a single view, layers, or a concatenated
layout. The returned object composes like any other chart, so it can be passed
to {py:func}`~genome_spy.layer`, {py:func}`~genome_spy.hconcat`, or {py:func}`~genome_spy.vconcat`. Parent properties can
provide shared context such as the assembly, genomic domain, axis resolution,
and configuration. The imported view remains responsible for its own marks and
dataflow.

## URL and version considerations

Use an immutable release or commit URL so the imported visualization cannot
change without a corresponding Python change. The viewer's browser must be
able to fetch the JSON, and relative data URLs inside it are resolved from the
imported specification's directory.

Because Python does not fetch the imported file, local serialization validates
the import declaration rather than the contents of the remote child. Loading
or schema errors in that child appear when GenomeSpy renders the chart.

The [Composing a genome browser](../gallery/composing_genome_browser.md) gallery
example demonstrates four pinned remote imports and links each JSON source to a
Python-authored equivalent. See GenomeSpy's
[Importing Views](https://genomespy.app/docs/grammar/import/) documentation for
templates, parameters, and import-site configuration.
