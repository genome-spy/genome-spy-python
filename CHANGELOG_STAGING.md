# Changelog Staging

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
  site, Altair-style landing showcase, generated gallery from `docs/examples`,
  Playwright thumbnail rendering, and the build/deploy workflow) and a separate
  `test:` commit validating that gallery examples build valid specs.
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
