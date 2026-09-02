# Import remote view specifications

`gs.import_view(url=...)` adds a view whose GenomeSpy JSON specification lives
in another file. This is useful for composing published, reusable tracks or for
splitting a large visualization into independently maintained specifications.
The Python package records the import definition; GenomeSpy fetches the remote
JSON in the browser when the chart is rendered.

## Import and compose a view

Pass an absolute or relative specification URL and compose the result like any
other chart:

```python
import genome_spy as gs

release = (
    "https://raw.githubusercontent.com/genome-spy/genome-spy/"
    "d2e9bd71/examples/docs/examples/genomic-data"
)

browser = gs.vconcat(
    gs.import_view(url=f"{release}/cytobands.json"),
    gs.import_view(url=f"{release}/scored-refSeq-genes.json"),
).properties(
    assembly="hg38",
    scales=gs.scales(
        x=gs.Scale(
            domain=[
                {"chrom": "chr20", "pos": 10_006_452},
                {"chrom": "chr20", "pos": 10_006_533},
            ]
        )
    ),
)
```

An imported specification may contain a single view, layers, or a concatenated
layout. Parent properties can provide shared context such as the assembly,
genomic domain, axis resolution, and configuration. The imported view remains
responsible for its own marks and dataflow.

## URL and version considerations

- Prefer an immutable release or commit URL for reproducible charts. A moving
  branch can change the imported visualization without changing your Python
  code.
- The browser must be able to fetch the JSON. The server therefore needs to be
  available to viewers and permit cross-origin requests when origins differ.
- Relative import URLs are resolved against the current specification's base
  URL. Relative data URLs inside an imported specification are resolved from
  the imported specification's directory.
- Treat remote specifications as executable visualization dependencies. Import
  only sources you trust and expect to remain available.

Because Python does not fetch the imported file, local serialization validates
the import declaration rather than the contents of the remote child. Loading
or schema errors in that child appear when GenomeSpy renders the chart.

The [Composing a genome browser](../gallery/composing_genome_browser.md) gallery
example demonstrates four pinned remote imports and links each JSON source to a
Python-authored equivalent. See GenomeSpy's
[Importing Views](https://genomespy.app/docs/grammar/import/) documentation for
templates, parameters, and import-site configuration.
