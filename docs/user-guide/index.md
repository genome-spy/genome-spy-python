# User guide

The user guide begins with the general visualization grammar and then adds
GenomeSpy's composition and genomic concepts.

If declarative visualization is new to you, begin with [data and chart
inputs](data.md), then continue through the Foundations pages in order. If you
already use Altair or Vega-Lite, start with [chromosomes and locus
scales](genomic-axes.md) to learn GenomeSpy's genomic extensions.

## Foundations

- [Data and chart inputs](data.md) explains records, tables, URLs, and inherited
  data.
- [Arrow data transport](arrow-transport.md) moves dataframe data efficiently
  into notebook widgets.
- [Charts and marks](charts.md) introduces the shapes that represent rows.
- [Encodings and channels](encodings.md) maps fields to position, color, size,
  and other visible properties.
- [Scales, axes, and legends](scales-axes-legends.md) controls those mappings and
  their guides.
- [Transforms](transforms.md) filters, derives, and summarizes rows before they
  are drawn.

## Larger and genomic views

- [Composition](composition.md) layers charts and arranges linked panels.
- [Annotations](annotations.md) adds selected point callouts and scored gene
  tracks.
- [Configuration](configuration.md) sets dimensions, titles, and shared visual
  defaults.
- [Chromosomes and locus scales](genomic-axes.md) introduces assemblies and
  genomic coordinates.
- [Large and indexed genomic data](genomic-data.md) loads only the visible part
  of an indexed file.
- [Linked genome tracks](genome-browser-layouts.md) combines tracks on one
  zoomable genomic axis.

## Interaction and output

- [Parameters and interaction](interaction.md) covers zooming, controls,
  selections, and cursor rulers.
- [Notebook display and updates](notebooks.md) displays a chart and replaces a
  named dataset without remounting it.
- [Save and inspect charts](serialization.md) writes specifications and
  standalone HTML.

```{toctree}
:hidden:
:maxdepth: 1
:caption: Foundations

data
arrow-transport
charts
encodings
scales-axes-legends
transforms
```

```{toctree}
:hidden:
:maxdepth: 1
:caption: Building larger views

composition
annotations
configuration
```

```{toctree}
:hidden:
:maxdepth: 1
:caption: Genomics

genomic-axes
genomic-data
genome-browser-layouts
```

```{toctree}
:hidden:
:maxdepth: 1
:caption: Interaction and output

interaction
notebooks
serialization
```
