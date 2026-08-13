# Changelog Staging

## 2026-08-13

- Refined the documentation gallery examples with shared scales, typed channel
  and layout builders, simpler composition, and corrected oncoprint alignment.

## 2026-08-12

- Added the notebook-local AlphaGenome-PyTorch TAL1 perturbation explorer with
  stable Arrow-backed sequence and prediction datasets.
- Fixed Marimo live-dataset updates when binary payload synchronization follows
  the revision trait.
- Removed superseded non-model Marimo examples and standalone development
  scripts.

## 2026-08-11

- Added a TCGA-BRCA PIK3CA mutation lollipop plot to the documentation gallery,
  including responsive collision-aware labels and protein-domain context.

## 2026-08-10

- Prepared live anywidget dataset updates in thematic commits: Core 0.83.1
  schema regeneration, direct in-place dataset updates, and reactive Marimo
  documentation with regression coverage.
- Committed the refreshed README, including named live-dataset updates with
  `view.set_dataset(...)`, as `0717448`.

## 2026-08-08

- Added automatic Arrow IPC rendering for supported dataframe inputs across
  notebooks and the documentation gallery, including packaged GISTIC example
  data, lifecycle coverage, and the corresponding build guards.

## 2026-08-07

- Generated the full typed public chart API from the GenomeSpy schema: exact
  chart/composition/import constructors, direct schema fluent setters,
  branch-aware constant channels, parameter descriptions, and generated API
  documentation inventory. Added PEP 561 typing support and regression
  coverage for editor and external type-checker signatures.

## 2026-06-24

- Committed the initial `uv` library scaffold, core GenomeSpy chart/notebook
  implementation, and built-in example dataset support using conventional
  commit messages.

## 2026-06-25

- Committed npm-backed GenomeSpy schema generation infrastructure and
  Altair-style chart API/example updates using conventional commit messages.

## 2026-07-02

- Committed schema-backed validation, generated mark mixins, pinned runtime
  URLs, codegen freshness checks, and cleaned notebook examples in separate
  conventional commits.
- Committed generated wrappers for all GenomeSpy encoding channels while
  preserving the existing public shorthand and locus API.
- Committed the Altair-style migration of `Chart` to direct generated
  `UnitSpec` inheritance with schema-backed copy semantics.
- Committed the GenomeSpy core 0.80.0 upgrade, schema-derived channel nested
  setters, and resolved generated-wrapper constructor signatures in separate
  conventional commits.

## 2026-07-07

- Committed the Sphinx documentation site and interactive example gallery in
  two conventional commits: a `docs:` feature commit (pydata-sphinx-theme + MyST
  site, landing showcase, generated gallery from `docs/examples`, Playwright
  thumbnail rendering, and the build/deploy workflow) and a separate `test:`
  commit validating that gallery examples build valid specs.
- Left the pre-existing uncommitted schema-typing work (`src/genome_spy/schema`,
  codegen tools, schema tests, example notebooks) out of this session's commits
  as unrelated changes.

## 2026-07-07 (schema typing)

- Committed the typed schema-generation arc in three conventional commits:
  `feat(schema)` for the schema-derived constructor/setter types plus the
  `_typing.py` alias layer and `_kwds.py` TypedDict helpers (and regenerated
  package), `test(schema)` for the accompanying codegen/package/chart tests, and
  `docs(examples)` for the Manhattan gallery and genomic interval notebooks.
- Left an unrelated AGENTS.md whitespace reflow uncommitted.

## 2026-07-13

- Committed the x2/y2 schema-type fix, the iframe reveal-on-stable sizing fix
  (eliminates the visible chart resize on gallery detail pages), the Manhattan
  plot's rewrite onto real HapMap data, and a batch of new real-data gallery
  examples (QQ, volcano, ASCAT copy-number/allele-specific, TCGA oncoprint,
  PIK3CA lollipop) plus two synthetic placeholders and the vendored airway
  RNA-seq counts, in five separate conventional commits.
- Added `.DS_Store` to `.gitignore` and removed stray macOS files that had
  appeared as untracked.

## 2026-07-14

- Committed the gallery thumbnail rendering follow-up as a focused
  `fix(docs-gallery)` slice: Playwright now waits for live charts to settle,
  scales them into the fixed card viewport more reliably, and the docs tests
  cover the renderer layout helper plus PNG-required thumbnail behavior.
- Committed the public API/data ergonomics slice as `feat(api)`: added
  Altair-style helper constructors, schema-backed lazy data builders, packaged
  example datasets, airway preprocessing helpers, and the corresponding chart
  and dataset regression coverage plus dependency/artifact updates.
- Committed the remaining docs/examples refresh as `docs(examples)`: updated
  the Sphinx/gallery configuration, docs styling and README examples, vendored
  the curated LAML oncoprint payload for docs provenance, and expanded the
  real-data example set with cleaner authoring and plot-family categorization.
- Committed a repo cleanup as `chore(repo)`: ignored local-only assistant and
  staging files, removed the empty `scripts/` placeholder, and simplified the
  public README/docs copy to stay user-facing.

## 2026-07-15

- Prepared a single conventional commit for the Altair-alignment follow-up:
  generated config/property-setter ergonomics, thinner handwritten
  chart/channel/helper plumbing, refreshed docs/examples/user-guide pages, and
  regression coverage plus generated schema updates.
- Reworked that session into three thematic commits after undoing the first
  bundled attempt: `feat(schema): add generated property setters`,
  `refactor(api): simplify chart and helper plumbing`, and
  `docs(api): refresh examples and guides`.

## 2026-07-26

- Committed the fluent chart-authoring API and generated schema updates as
  `feat(api)`, prepared gallery datasets as `feat(datasets)`, and simplified
  the documentation examples and data previews as `docs(examples)`.

## 2026-07-30

- Committed the GenomeSpy core 0.81.0 schema regeneration, contributor setup
  documentation, and the stacked browser/LUAD viewport gallery changes as
  three thematic commits.
- Committed upstream-derived gallery examples, deterministic grammar datasets,
  tracked PNG thumbnails, and zoom/stack API support as `db9e833`
  (`feat(docs): add upstream genomic examples`).
- Committed the PNG-only gallery policy and incremental Playwright capture
  workflow as `69f773c` (`docs(gallery): require reviewed PNG thumbnails`).

## 2026-08-04

- Committed generated transform helpers, capability metadata, full root/import
  wrapping, expanded public API coverage, and regression tests as `7eb5f80`
  (`feat(api): expand generated grammar coverage`).
- Committed the expanded BAM, Dynseq bQTL, stacked browser, and GISTIC gallery
  examples with refreshed thumbnails and regression coverage as `4cf5d76`
  (`docs(examples): expand genomic track showcases`).
- Validation: Ruff formatting and linting, mypy, all 173 tests, and both
  commits' pre-commit hooks passed.

- Committed the published GenomeSpy core 0.82.0 schema regeneration as
  `5a32637` (`chore(schema): upgrade GenomeSpy core to 0.82`).
- Committed the explicit parameter/click anywidget bridge, Marimo dependency,
  README instructions, and interaction notebook as `190f00c`
  (`feat(notebook): add Marimo interaction bridge`).
- Validation: Ruff, mypy, all 174 tests, Marimo's notebook checker, and both
  commits' pre-commit hooks passed.
- Followed up with `e994b97` (`fix(notebook): clean interaction listener
  lifecycle`) after reviewing the re-embed cleanup path; targeted widget tests,
  Ruff, mypy, and the commit hooks passed.
- Committed the initial Polars-to-GenomeSpy Arrow IPC transport spike as
  `8f789e4` (`feat(notebook): add Arrow IPC transport spike`), including the
  binary widget trait, Blob URL lifecycle, serializer, notebook, and tests.
- Validation: Ruff, mypy, 180 full-suite tests, focused Arrow/widget/notebook
  tests, Marimo checks, browser rendering, and commit hooks passed.
- Committed `bb0d04c` (`feat(notebook): add reactive Arrow updates`) with
  latest-update-wins render revisions, per-render Blob URL cleanup, a reactive
  Polars/Marimo notebook, and widget lifecycle assertions.
- Validation: Ruff, mypy, 180 full-suite tests, focused tests, Marimo checks,
  browser slider updates including rapid changes, and commit hooks passed.
- Committed `8ca3157` (`perf(notebook): benchmark Arrow transport`) with a
  deterministic multi-size Arrow-versus-JSON payload benchmark and README
  usage instructions.
- Validation: benchmark execution, Ruff, mypy, and commit hooks passed.
- Committed `5d77800` (`feat(notebook): add mutation-impact prototype`) with a
  deterministic offline Polars/Arrow notebook for reference, alternate, and
  delta signal tracks plus README guidance.
- Validation: Ruff, focused Arrow/widget/notebook tests, Marimo checks, browser
  rendering and mutation replacement, and commit hooks passed.
- Committed `afc618f` (`fix(notebook): enable mutation track picking`) with
  explicit default tooltip handling and tooltip fields on signal marks.
- Validation: Ruff, mypy, focused tests, Marimo checks, browser rendering, and
  commit hooks passed; click-to-Python sync still needs a reliable probe.
- Committed `5844268` (`feat(datasets): package mutation impact reference`) with
  a deterministic JSON input, dataset-loader registration, notebook loading,
  and regression coverage.
- Validation: Ruff, mypy, 31 focused tests, Marimo checks, and commit hooks
  passed.
- Follow-up full-suite validation after the packaged-input change: 181 tests
  passed.
- Committed `1df8343` (`fix(notebook): mount interaction widget in Marimo`) so
  the interaction demo wraps `JupyterChart` with `mo.ui.anywidget(...)` and
  renders in Marimo's reactive UI surface.
- Validation: Marimo check, Ruff, mypy, and focused widget tests passed.
- Committed `a5ea2fa` (`fix(notebook): emit interaction demo output`) so the
  final Marimo cell emits a visible `mo.vstack(...)` instead of returning its
  markdown as a definition.
- Validation: full pytest suite (181 tests), Ruff, mypy, Marimo check, and a
  programmatic app-run smoke test passed.
- Committed `79247e1` (`feat(notebook): harden Arrow IPC Marimo spike`) with a
  Marimo-mounted one-shot Arrow widget, mixed primitive/nullable columns,
  tooltip inspection, and visible-output regression coverage.
- Validation: Ruff, mypy, Marimo checks, 19 focused tests, all 183 pytest tests,
  and commit hooks passed.
- Committed `1470bf5` (`fix(notebook): mount reactive Arrow demo in Marimo`)
  with a valid initial Arrow payload, Marimo anywidget mounting, documented
  re-embed state resets, and reactive-notebook output coverage.
- Validation: Ruff, mypy, Marimo check, 20 focused tests, all 184 pytest tests,
  a programmatic `ARROW1` payload smoke test, and commit hooks passed.
- Committed `bddd14d` (`feat(datasets): use upstream tabular mutation sources`)
  and `f5a5351` (`refactor(datasets): simplify wrangling helpers`) for the
  dataset source migration and leaner wrangling APIs.
- Validation: 142 non-gallery tests, four affected gallery examples, Ruff, and
  mypy passed; unrelated gallery property failures remain.
