# Dev Log

## 2026-08-24 - Split package CI from docs and example tests

- Added pytest markers for package-external documentation and code-generation
  tests, and removed the AlphaGenome-only adapter, backend, request, and
  notebook test modules because AlphaGenome is outside the package scope.
- Limited the Ubuntu/Windows matrix to installable-package behavior and moved
  schema-generator unit tests into the existing codegen job. Both jobs now
  report their ten slowest tests to make future CI bottlenecks visible.

## 2026-08-24 - Tidied stacked genome-browser guides

- Replaced long rotated labels with short horizontal `track-title` labels and
  removed duplicate y-axis titles in the stacked genome-browser example.
- Kept the unrelated cCRE and nucleotide color scales independent while using
  GenomeSpy's collected legend resolution to place both legends together at
  the parent track stack.

## 2026-08-24 - Fixed setup-uv action pins

- Replaced nonexistent `astral-sh/setup-uv@v10` references in the CI,
  documentation, and release workflows with the current immutable `v9.0.0`
  release tag.

## 2026-08-24 - Fixed CI workflow YAML parsing

- Changed the wheel metadata check to a folded YAML block so the metadata
  fields containing colon-space sequences are passed to the shell instead of
  being misparsed as YAML mappings.

## 2026-08-24 - Removed gallery data previews

- Removed opt-in data tables from all gallery examples and deleted the preview
  collection, HTML generation, and CSS that supported them.
- Added a gallery regression check ensuring generated example pages contain no
  data-preview section.

## 2026-08-24 - Added Altair attribution and distribution notices

- Added the complete Vega-Altair BSD-3-Clause license and a third-party notice
  distinguishing adapted code from design references.
- Added exact-source provenance to the schema runtime, schema generator, API
  documentation generator, and two adapted Altair example tests.
- Changed package metadata to `MIT AND BSD-3-Clause`, included both licenses and
  the provenance notice in wheels and source distributions, and tightened CI
  and release checks to verify exact license metadata and archive paths.
- Linked the notices from the README and About page. Validated with 317 tests,
  Ruff format/check, MyPy, the strict Sphinx build, `uv build`, strict Twine
  checks, and direct wheel/sdist content inspection.

## 2026-08-20 - Fixed the CI test failure and added a release workflow

- Made the oncoprint gene ranking deterministic. `laml_oncoplot_data` sorted
  per-gene sample counts with pandas' default quicksort, so NRAS and TP53 (both
  altered in 15 samples) came out in a platform-dependent order; every CI run
  failed `test_laml_oncoprint_uses_shared_sample_index_scale` on Linux while
  passing on macOS. Both this sort and the LUAD `np.argsort(...)[::-1]` gene
  ranking now use stable sorts, so ties keep their input order.
- Added `tests/test_datasets.py::test_laml_gene_order_breaks_sample_count_ties_alphabetically`
  as the regression guard at the dataset level.
- Replaced the wheel-contents check in `ci.yml` with `grep -Fxq`; ripgrep is not
  part of the runner image, so that step would have failed once the suite got
  far enough to reach it.
- Added `.github/workflows/release.yml`: `ci.yml` is now also `workflow_call`
  and runs as the pre-publish gate, then a build job verifies that a release tag
  matches `uv version --short --frozen`, builds both distributions, and runs
  `twine check --strict`. Publishing uses `pypa/gh-action-pypi-publish` with API
  token secrets (`PYPI_API_TOKEN`, `TEST_PYPI_API_TOKEN`) scoped to the `pypi`
  and `testpypi` environments. `workflow_dispatch` takes a target input so the
  workflow can be rehearsed with build-only or TestPyPI runs.
- Added the packaging metadata PyPI needs: MIT `LICENSE`, `license`/
  `license-files`, authors, keywords, classifiers, and `[project.urls]`.
- Bumped every action to its current major; the pinned versions still target
  Node 20, which the runners already force onto Node 24.
- Added `windows-latest` to the CI test matrix (`fail-fast: false`). Formatting,
  linting, and typing stay on the Linux leg, and the wheel-contents check moved
  from `unzip | grep` to a `python -c` one-liner that runs under both bash and
  PowerShell. Prerequisites for the Windows leg: `.gitattributes` pins every
  checkout to LF, because `test_upstream_mutation_files_are_byte_exact` hashes
  the packaged `.tsv` files and a CRLF checkout would change their bytes; and
  `tests/test_docs_api_reference.py` now reads `api.md` as UTF-8 instead of the
  locale encoding, which is cp1252 on Windows. The two `subprocess.run` calls in
  the suite decode child output as UTF-8 rather than `text=True`, for the same
  reason. `src/` had no implicit-encoding I/O to begin with.
- Validated locally: full suite (317 passed), `ruff format --check`, `ruff
  check`, `mypy src/`, the codegen job's `git diff --exit-code`, `uv build`,
  `twine check --strict`, the wheel-contents check, `node --test
  tests/widget.test.mjs`, and the tag/version comparison. The suite was also run
  under `PYTHONWARNDEFAULTENCODING=1 -W error::EncodingWarning` to catch the
  implicit-encoding reads that fail on Windows. The workflows themselves have
  not run on GitHub, and the Windows leg cannot be reproduced locally at all.
- Follow-up: confirm the copyright holder named in `LICENSE`, and decide whether
  CI should test a Python version matrix rather than 3.11 alone.

## 2026-08-18 - Split the API reference into one page per object

- Replaced the single-page API reference with Altair's three-layer structure: a
  generated index of `autosummary` tables, one page per public object, and no
  `:members:` dump on the index. `api.html` went from 3.2 MB with 639 inlined
  method blocks to 54 KB with six grouped tables and 76 generated pages.
- Added `tools/generate_api_docs.py`, which derives the groups from the objects
  themselves — `TopLevelSpec` subclasses, `schema.channels` classes,
  `schema.core` classes, module-level functions — so the index cannot drift from
  `genome_spy.__all__`. Stubs are written into the ignored `docs/generated/`.
- Added `docs/_templates/autosummary/class.rst`: a methods/attributes summary
  table inside the `autoclass` body, so the table renders above the full member
  descriptions rather than replacing them. Our generated methods carry real
  parameter docs, unlike Altair's "Refer to X" stubs, so table-only pages would
  have dropped them.
- `JupyterChart` uses a second template without `:inherited-members:`; the
  inherited ipywidgets docstrings are invalid reStructuredText and broke the
  strict build.
- `:template:` names resolve against templates_path, not its `autosummary/`
  subdirectory, and Sphinx falls back to its base template *silently* when the
  name does not resolve — which produced an options-less stub that still built
  cleanly under `-W`. Names now carry the `autosummary/` prefix and a test
  asserts it.
- `Locus` is grouped with the encoding channels, both because it constructs one
  and because sharing a stub directory with `locus` collides on
  case-insensitive filesystems.
- Validated with the full suite (305 passed, five new API-reference tests),
  Ruff, `git diff --check`, and the strict Sphinx build.
- Follow-up: the `Chart` page is still 1.5 MB, and 872 KB of that is the
  `configure_*` family, whose parameters duplicate the schema objects already
  documented under "Schema objects". Splitting those onto per-method pages or
  shortening their generated docstrings to point at the schema classes would
  address the remaining bulk.
## 2026-08-18 - Switched the Sphinx documentation to Furo

- Replaced `pydata-sphinx-theme` with Furo in the docs dependency group and
  lockfile.
- Migrated the Sphinx theme options and branded CSS variables to Furo while
  preserving the light presentation, landing-page layout, and GitHub link.
- Removed PyData-only secondary-sidebar metadata from authored and generated
  pages; generated pages no longer emit empty YAML front matter.
- Validation: 112 focused documentation tests, repository-wide Ruff, and the
  strict Sphinx HTML build passed.

## 2026-08-18 - Expanded official companion gallery prose

- Added optional same-stem Markdown companions for gallery examples; the
  generated page places this prose after the live chart, and cache tokens now
  include it.
- Added self-contained interpretation and Python implementation notes to all 16
  examples adapted from official GenomeSpy pages, retained the canonical data
  disclaimers, and linked each adaptation to its official source page.
- Documented the companion-file convention for contributors and added
  regressions for rendering and cache invalidation.
- Audited every adapted explanation against its Python source and corrected
  inaccurate claims about GISTIC input, HCC1954 copy number and hover behavior,
  alignment composition, lollipop sizing, GFF3 labels, data inheritance, and
  parameterized template imports.
- Used “Data use and provenance” as the note title on all companion pages
  instead of repeating it as a large section heading above a generic “Note.”
- Recorded the gallery editorial policy in `AGENTS.md`, including concise
  canonical provenance and an explicit distinction between Python-side data
  preparation and GenomeSpy's browser-side dataflow.
- Validation: 74 gallery tests, repository-wide Ruff format/check, and the
  strict Sphinx HTML build passed.

## 2026-08-18 - Linked the documentation to the upstream GenomeSpy docs

- Added upstream links across Getting started, all user-guide pages, the landing
  page, About, and the API reference, placed at the end of the section each one
  deepens. The three widest coverage gaps (transforms, indexed genomic data, and
  interaction) carry per-feature links; the lazy-source and mark tables link
  every row.
- At this stage, decided against metadata-rendered upstream links on gallery
  pages and reverted a `META["upstream"]` prototype. The later same-stem
  companion prose superseded that choice without editing the generated,
  gitignored `docs/gallery/*.md` pages directly.
- Validated with the full pytest suite (300 passed), repository-wide Ruff, MyPy,
  `git diff --check`, the strict Sphinx build, and a curl sweep confirming every
  upstream URL used in the prose returns 200 with its heading anchor present.
- Follow-up: re-run that anchor sweep when the pinned `@genome-spy/core` version
  is bumped; upstream headings can move between releases. Link inventory and
  rationale are in `plans/upstream_doc_links.md`.

## 2026-08-18 - Made documentation embeds own chart dimensions

- Removed the gallery loading label, delayed reveal, shadow DOM, and canvas-size
  polling; gallery examples now use the fixed-height host as the direct
  `embed(c, spec, { bare: true })` container.
- Removed presentation-only root pixel sizes from gallery and live tutorial
  specs. Preserved the fixed-dimension teaching example plus semantic child,
  step, viewport, and aligned-panel sizes; the Quartz example explicitly uses
  container width and height so theme defaults cannot override the embedder.
- Measured all 36 gallery and 40 tutorial embeds in a browser, retained space
  required by parameter controls, and tightened containers that only contained
  unused space.
- Validation: 110 gallery/tutorial tests passed, Ruff passed, the strict Sphinx
  HTML build passed, and browser checks confirmed representative unit,
  composed, scrollable, themed, OncoPrint, cytoband, and Manhattan examples.

## 2026-08-17 - Reduced the beginner documentation scope

- Removed the planned troubleshooting chapter and stripped error-message
  postmortems from composition, configuration, interaction, and encodings.
- Reworked user-guide navigation, source installation, notebook updates,
  specification saving, and indexed-data source guidance around shorter
  task-oriented paths; removed invalid-chart and placeholder genomic examples.
- Kept the UpSet-style grid as an explicitly advanced composition example and
  moved round-trip, validation-control, transport, and multi-dataset details to
  API-reference scope.
- Validation: 37 documentation tutorial tests, repository-wide Ruff, and the
  strict Sphinx HTML build passed.

## 2026-08-17 - Added the serialization and sharing guide

- Added a beginner guide to the boundary between Python chart objects and
  validated GenomeSpy dictionaries and JSON text.
- Added executable examples for `to_dict()`, `to_json()`, schema omission,
  dictionary/JSON round trips, and intentional schema validation failure.
- Explained how inline, URL, lazy, and notebook Arrow data appear at the
  serialization boundary and why `validate=False` is only a diagnostic tool.
- Documented the supported JSON and CDN-backed HTML save paths, explicit format
  selection, network requirements, and the absence of direct PNG/SVG/PDF export.
- Added navigation and regressions for exact serialized definitions, schema
  round trips, validation errors, file output, embed code, and unsupported
  formats.
- Validation: 125 focused chart/tutorial tests, repository-wide Ruff, diff
  checks, and the strict Sphinx build passed.

## 2026-08-17 - Added the notebook display and update guide

- Added a beginner notebook guide that separates implicit one-off chart display
  from retaining a stable `JupyterChart` through `.widget()`.
- Added executable examples for explicit named datasets, record replacement,
  Arrow-backed Polars updates, and the single-dataset `set_data()` shortcut.
- Documented the supported Arrow table types, the pandas/PyArrow dependency,
  fixed widget dataset manifests, field compatibility, and ambiguous scoped
  dataset names.
- Added a stable-cell pattern for Jupyter and reactive notebooks, including
  one-time Marimo wrapping and in-place dataset updates that preserve the
  mounted visualization and transient interaction state.
- Added navigation and regressions for named dataset declarations, widget
  update targets, unchanged widget specifications, and executable snippets.
- Validation: 51 focused notebook/tutorial tests, repository-wide Ruff, diff
  checks, and the strict Sphinx build passed.

## 2026-08-17 - Added the interaction user guide

- Added a progressive interaction guide covering zoomable scales, bound value
  parameters, reactive expression parameters, point selections, conditional
  encodings, stable keys, interval-selection basics, and linked rulers.
- Added four live examples: genomic zoom and pan, slider-driven filtering,
  click selection, and one container-spanning ruler across linked tracks.
- Documented parameter scope and made the single-parent ruler pattern explicit
  to prevent duplicate cursor guides and missing-scale errors.
- Fixed authoring normalization so `gs.Key("id")` never receives an inferred
  encoding type, matching GenomeSpy's field-only key schema.
- Added navigation and regressions for parameter bindings, expression
  dependencies, conditional empty behavior, key serialization, ruler scope,
  and shared positional resolution.
- Validation: 118 focused chart/tutorial tests, repository-wide Ruff, MyPy,
  diff checks, and the strict Sphinx build passed.

## 2026-08-17 - Added the linked genome tracks guide

- Added a progressive two-track genome browser built from lazy BigWig signal
  and layered BigBed annotations.
- Kept track-local data, y encodings, titles, and heights on the children while
  placing the assembly, zoomable locus scale, genome axis, and spacing on their
  closest common parent.
- Explained shared x and independent y scale/axis resolutions, categorical
  step sizing, scrollable viewports, and zoom-dependent label opacity.
- Linked the reduced tutorial to the richer stacked and imported-view genome
  browser gallery examples.
- Added navigation and regressions for child ownership, inherited layer data,
  parent scale resolution, semantic opacity, and viewport height.
- Validation: twenty-nine focused tutorial tests, repository-wide Ruff, diff
  checks, and the strict Sphinx build passed.

## 2026-08-17 - Added the indexed genomic data guide

- Added a beginner guide to viewport-driven lazy loading and the relationship
  between a lazy source, its observed locus scale, and the active assembly.
- Added live, single-source BigWig and BigBed tracks plus typed source examples
  for indexed FASTA, BAM, Tabix TSV, GFF3, and VCF.
- Documented window thresholds, request debouncing, companion-index naming,
  browser hosting requirements, and when eager data remains the simpler choice.
- Linked format-specific transformations to the existing sequence, alignment,
  gene-annotation, and stacked-browser gallery examples.
- Added navigation and regressions for lazy source types, locus domains,
  secondary interval positions, explicit BAM indexes, and Tabix parsing.
- Validation: twenty-six focused tutorial tests, repository-wide Ruff, diff
  checks, and the strict Sphinx build passed.

## 2026-08-17 - Expanded the genomic coordinate guide

- Rewrote the existing genomic-axes page in place as a beginner guide to contig
  linearization, point loci, ranged loci, coordinate counting, and assemblies,
  preserving its published URL.
- Added explicit zero-based half-open guidance, including the one-based VCF/GFF3
  `offset=1` rule and why an inclusive interval end is not also offset.
- Added single-source hg38 point and interval tracks, a one-based interval
  example, a named inline custom assembly, and a two-assembly human/mouse view.
- Added regressions for locus field definitions, secondary endpoints, offsets,
  custom contig order, root assembly scope, and per-scale assembly scope.
- Validation: twenty-three focused tutorial tests, repository-wide Ruff, diff
  checks, and the strict Sphinx build passed.

## 2026-08-17 - Added the Configuration user guide

- Added a beginner configuration page that separates mark and encoding
  properties, explicit view properties, scoped defaults, and root themes.
- Covered structured titles, fixed dimensions, discrete step sizing, container
  sizing, flex-like `SizeDef`, padding versus spacing, and scrollable viewport
  sizing.
- Added a shared-track example that places `gs.axes` and `gs.scales` on one
  unambiguous parent resolution, plus examples for `with_view`, `configure_*`,
  and a built-in theme.
- Added navigation and regressions for configuration blocks, title and padding
  objects, fixed/step/flexible sizes, shared settings, inheritance, and theme
  selection.
- Validation: twenty focused tutorial tests, repository-wide Ruff, diff checks,
  and the strict Sphinx build passed.
