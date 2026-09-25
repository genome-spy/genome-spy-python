# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2026-09-25

### Added

- Compose selection conditions in `gs.when()` with `and`, `or`, and `not`,
  endpoint projections, and named predicate references. Nested selection
  handles retain their empty-selection behavior.
- Add PISA squid and interaction-matrix gallery examples adapted from the
  official GenomeSpy specifications, with endpoint brushing, conditional link
  highlighting, and zoom-dependent cell labels.

### Changed

- Use browser-side `displace2d` label placement in the airway volcano and MA
  gallery plots, with denser gene annotations and adaptive leader lines.

- Reorganize the gallery into 13 categories, separating regulatory model
  interpretation, read alignments and RNA splicing, sequences and alignments,
  and interaction examples from the broader browser, annotation, and basic groups.
- Upgrade GenomeSpy Core, controls, and Inspector from 0.88.1 to 0.89.0.
  Regenerate support for 2D displacement, bidirectional arrows, debounced
  expression parameters and transforms, composed selection predicates, and
  `tickStep` expressions.
- Upstream interval brushes now use half-open boundaries. View-level scale
  declarations require explicit `axes` settings to create axes when no
  positional encoding supplies them.

### Fixed

- Preserve explicitly wrapped `ExprParameter` declarations after upstream
  split expression parameters into plain, transitioned, and debounced variants.
- Refresh the bundled runtime build for the relocated upstream font license.

## [0.4.0] - 2026-09-18

### Added

- Experimental Python access to the live GenomeSpy embed API: read and update
  parameters, subscribe to selections, clear selections, replace named datasets,
  and access parameters inside named views.
- Live web demos and matching notebooks for genomic interval annotation with
  BED export, brush and point gene selection with CSV export, and nucleotide
  editing against a reference sequence with FASTA export. Examples include
  their Python chart specifications and interaction hooks.
- `inline=True` for HTML and notebook rendering with bundled, version-matched
  GenomeSpy JavaScript. Remote data and other external assets still require
  network access.
- An RNF7 ONT direct-RNA browser with paired coverage, individual read
  alignments, and published m6A predictions, plus an adaptive DynSeq example
  that transitions between sequence letters and bars as users zoom.
- Additional gallery examples for BAM coverage and pileups, heatmaps, t-SNE,
  basic marks, and coordinated interactions.

### Changed

- Upgrade GenomeSpy Core, controls, and Inspector from 0.87.0 to 0.88.1 and
  regenerate the Python API, including conditional draw ordering and reactive
  zoom expressions.
- Simplify the embed guide and improve gallery navigation. Gene-selection
  workflows support zooming with points that grow as users zoom in.

### Fixed

- Preserve conditional order encodings when chaining fluent setters and omit
  unsupported sorting from the order-channel API.
- Correct dataset provenance and attribution, and include source-specific data
  and borrowed-code license notices in packages and documentation.
- Fix embed attachment docstring formatting that caused clean documentation
  builds to fail when warnings were treated as errors.

## [0.3.0] - 2026-09-09

### Changed

- **Dataset format change:** `p53_sequence_comparison` now contains 34 protein
  sequences aligned with MAFFT L-INS-i, replacing the unaligned JSON tables.
  Load the aligned FASTA with
  `load_dataset("p53_sequence_comparison", as_format="text")`; code expecting
  the previous mapping of prepared tables must be updated.
- Updated the P53 gallery example to show the aligned sequences and calculate
  conservation, gap-free fractions, and sequence logos in GenomeSpy.
- Made the brush notebook build progressively from a simple p-value chart to
  linked tracks, and added an effect-size zero baseline in the notebook and gallery.

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

[0.5.0]: https://github.com/genome-spy/genome-spy-python/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/genome-spy/genome-spy-python/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/genome-spy/genome-spy-python/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/genome-spy/genome-spy-python/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/genome-spy/genome-spy-python/releases/tag/v0.1.0
