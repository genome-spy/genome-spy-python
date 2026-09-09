# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-09-09

### Added

- Python lists and tuples in `gs.expr()` for array expressions containing
  values, parameters, and calculations.
- A brush-linked notebook example with an Open in Colab link in the README.

### Changed

- Require AnyWidget 0.11.0 or newer to match the widget lifecycle API used for rendering.
- Simplified the contributing guide and added brief notebook troubleshooting advice.

### Fixed

- PIK3CA lollipop connectors now reach the protein track.
- Packaged datasets can be imported on Python 3.14.

## [0.1.0] - 2026-09-09

First public alpha release, targeting GenomeSpy Core 0.87.0.

### Added

- Declarative, schema-backed Python API for authoring GenomeSpy specifications.
- Altair-style marks, encodings, transforms, parameters, conditions, and chart
  composition.
- Genomics-native locus channels, genome assemblies, genomic data sources, and
  coordinated multi-view interactions.
- Specification validation and serialization to dictionaries, JSON, and
  standalone HTML.
- Interactive notebook rendering in Jupyter, VS Code, and Marimo through
  `anywidget`.
- Arrow transport and live named-dataset updates for pandas, Polars, and
  PyArrow tables.
- Per-render GenomeSpy controls and embed options, including image export and
  full-window display controls.
- Packaged example datasets, documentation, tutorials, and an interactive
  visualization gallery.

[0.2.0]: https://github.com/genome-spy/genome-spy-python/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/genome-spy/genome-spy-python/releases/tag/v0.1.0
