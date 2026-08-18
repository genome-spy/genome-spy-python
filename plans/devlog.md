# Dev Log

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

## 2026-08-17 - Expanded the Composition user guide

- Replaced the composition summary with beginner examples for layers, vertical
  tracks, horizontal panels, inherited parent properties, and explicit scale
  and guide resolution.
- Added an UpSet-style two-column grid with an empty top-left placeholder,
  shared matrix index scales, and excluded quantitative summary scales.
- Documented shared, independent, and excluded resolution plus the error caused
  by applying one view-level scale to multiple independent resolutions.
- Added single-source examples and regressions for hierarchy, inheritance,
  operator serialization, placeholder ordering, exclusions, and parent scales.
- Validation: seventeen focused tutorial tests, repository-wide Ruff, diff
  checks, and the strict Sphinx build passed.

## 2026-08-17 - Added the Transforms foundation guide

- Added a beginner transform page covering row predicates, derived fields,
  grouped summaries, pipeline order, and the boundary between Python data
  preparation and browser-side visualization transforms.
- Added single-source filter, formula, and aggregate examples based on one
  six-row dataset and linked the page from the foundation navigation.
- Added regressions for exact transform serialization and order, source-data
  preservation, derived and aggregate encoding fields, and rendered targets.
- Validation: fourteen focused tutorial tests, repository-wide Ruff, diff
  checks, and the strict Sphinx build passed.

## 2026-08-17 - Added the Scales, axes, and legends guide

- Added a new foundation page that introduces automatic scales and guides,
  domain-to-range mapping, selective scale configuration, axis and legend
  options, guide removal, and zoomable positional scales.
- Added single-source automatic, customized, and guide-reduced charts and linked
  the page from the user-guide navigation.
- Added regressions that distinguish inferred defaults, explicit scale and guide
  properties, hidden guides, and retained scales; shared and named resolution
  remains scoped to composition.
- Validation: twelve focused tutorial tests, repository-wide Ruff, diff checks,
  and the strict Sphinx build passed.

## 2026-08-17 - Added the Encodings and channels guide

- Replaced the encoding API summary with a beginner guide to field/type
  shorthand, explicit channel classes, visual-channel roles, and the semantic
  difference between quantitative, nominal, ordinal, index, and locus data.
- Added single-source examples for multi-channel points, indexed sequence
  positions, genomic loci, and field/datum/value/expression definitions.
- Documented the common field-versus-value, expression-type, and orphaned
  secondary-position mistakes, while deferring detailed guide customization to
  the next scales, axes, and legends page.
- Validation: ten focused tutorial tests, repository-wide Ruff, diff checks,
  and the strict Sphinx build passed.

## 2026-08-17 - Rewrote Charts and marks as a beginner guide

- Replaced the API-summary page with a progressive explanation of unit views,
  one-row-to-one-mark behavior, static mark properties, data-driven encodings,
  and view-level properties.
- Added single-source point, ranged rule, text, link, and arrow examples, plus a
  task-oriented overview of the core mark families.
- Added regression tests for every rendered chart target and key serialized
  mark, encoding, secondary-position, and view properties.
- Validation: eight focused tutorial tests, repository-wide Ruff, diff checks,
  and the strict Sphinx build passed. In-app visual QA could not run because
  local `file://` navigation was rejected by the browser security policy.

## 2026-08-17 - Added the foundational Data user guide

- Added a beginner Data and chart inputs page covering records and fields,
  pandas/Polars/PyArrow inputs, eager URL sources, parent-view data inheritance,
  long-form tables, and the boundary between Python preparation and GenomeSpy
  transforms.
- Added single-source inline, URL, and inherited-data chart objects and tests
  that verify serialization plus the absence of duplicated child data.
- Grouped the user-guide navigation into Foundations, Building larger views,
  and Genomics without adding links to unfinished pages.
- Validation: six focused tutorial tests, repository-wide Ruff, and the strict
  Sphinx build passed. Browser QA at desktop and 390 px showed two rendered
  canvases, no page overflow, and no console warnings or errors.

## 2026-08-17 - Removed formulaic prose from the beginner docs

- Replaced stock tutorial transitions and duplicated landing-page marketing
  copy with direct descriptions of the code and rendered behavior.
- Changed the documentation plan so examples and navigation remain content
  checks instead of mandatory “What changed?”, recap, and next-step sections.
- Made the composition warning self-contained, taught `+`, `&`, and `|` as the
  primary operators, and aligned the genomic assembly explanation with the
  fluent `.scale(assembly=...)` example.
- Validation: the revised composition examples serialized, all 75 tutorial and
  gallery tests passed, Ruff passed, and the strict Sphinx build completed
  without warnings.

## 2026-08-14 - Rewrote Getting Started as a tested beginner tutorial

- Replaced the API-oriented onboarding page with a progressive data → mark →
  encoding → guide tutorial that ends at one hg38 interval track; installation
  now reflects the package's source-only release state.
- Added one docs-only Python source for displayed snippets and chart objects,
  plus a `genomespy-chart` prose directive in the existing gallery extension.
  The directive validates named charts during the build and uses the direct
  static-bundle `embed(c, spec, { bare: true })` path without iframe, shadow, or
  resize wrappers.
- Revised the documentation plan to keep serialization and composition out of
  the required 15-minute path and to separate foundational data/transforms from
  advanced genomic loading and transforms.
- Validation: focused tutorial tests, repository-wide Ruff, and a strict Sphinx
  HTML build passed. Manual desktop/mobile browser inspection remains pending
  because no browser backend was available in this workspace.

## 2026-08-14 - Planned beginner-first documentation

- Audited the current Python docs against Altair's onboarding, GenomeSpy's
  grammar documentation, and the UW Visualization Curriculum.
- Added `plans/documentation_plan.md` with a progressive Getting Started
  tutorial, a reduced four-part user guide, terminology rules, live-example
  strategy, implementation phases, and acceptance criteria.
- Kept app-only concepts and exhaustive schema reference out of the core
  learning path. Follow-up starts with the Getting Started page and tests.


## 2026-08-13 - Simplified oncoprint composition and shared scales

- Rebuilt the LAML oncoprint as aligned `concat` top and matrix rows, with the
  matrix row owning one shared gene scale rather than repeating gene order,
  direction, and padding on each panel.
- Rebuilt the LUAD oncoprint so its matrix, percentages, and gene counts form
  one shared-scale `concat` row; removed the nine invisible right-column spacer
  panels. The matrix row is flat so its view-level y scale maps to one shared
  resolution; its x resolution is excluded from the surrounding sample tracks.
- Updated gallery regressions to verify the single matrix-row gene scale and
  that child gene encodings no longer serialize duplicate scales. Validation:
  gallery tests, repository-wide Ruff, MyPy, and `git diff --check` passed.
  Browser rendering remains a manual check because no browser is available in
  this workspace and direct headless initialization cannot load upstream font
  assets through Node's source-module loader.

## 2026-08-13 - Scoped oncoprint rulers to concrete sample scales

- Moved each `sampleRuler` and its x-domain to the alteration matrix panel,
  where the ruler overlay has one explicit index scale type. Matrix-summary
  rows are now excluded from the outer x resolution instead of forcing their
  heterogeneous children into it.
- Kept shared x resolution for LUAD's non-matrix sample tracks; the matrix uses
  the identical explicit sample domain for alignment and zoom.
- Validation: gallery tests, Ruff, MyPy, and `git diff --check` passed.

## 2026-08-13 - Restored LUAD's aligned two-column grid

- Replaced the flat matrix-and-summary row with an UpSet-style two-column
  `concat`: the sample-track column contains the matrix and all x-linked
  tracks, while the summary column starts with one explicit empty placeholder
  before the matrix-aligned gene summaries.
- The matrix is again in the shared sample x-scale and ruler subtree, restoring
  linked zoom and panning without including the right-side count scale.
- Validation: gallery tests, Ruff, MyPy, and `git diff --check` passed.

## 2026-08-13 - Consolidated the LUAD sample cursor guide

- Changed the linked sample-track composition to `vconcat` and set the ruler
  extent to `"container"`, producing one x ruler spanning its aligned tracks
  instead of separate overlapping per-track guides.
- Validation: gallery tests, Ruff, MyPy, and `git diff --check` passed.

## 2026-08-13 - Centralized the PIK3CA lollipop position scale

- Kept the lollipop's nested vertical composition because its label, displaced
  mutation, connector, and protein subviews require one aligned protein axis.
  Moved the shared x scale to the root, where its single resolved protein
  position scale is unambiguous.
- Replaced layout and collision literals with named constants and added a
  gallery regression for the root scale declaration.
- Validation: gallery tests, Ruff, MyPy, and `git diff --check` passed.

## 2026-08-13 - Added typed conditional encoding helpers

- Added public `condition(param, value, empty=...)` and exported generated
  `XOffset`/`YOffset` channels, so conditional mark properties and offsets no
  longer require raw channel-definition dictionaries.
- Converted the HCC structural-variant example's size, opacity, and computed
  tooltips; converted equivalent direct channel dictionaries in BAM, DynSeq,
  and PIK3CA examples. The direct `gs.Channel({...})` scan is now empty.
- Fixed the schema generator to retain scalar union branches in fluent nested
  setters, and updated the committed numeric conditional setter accordingly.
  Validation: targeted generator/API tests (100 passed), targeted gallery tests
  (3 passed), Ruff, MyPy, and `git diff --check` passed.

## 2026-08-13 - Removed remaining direct composition encodings

- Replaced the DynSeq baseline's `Chart(encoding=...)` mapping with fluent
  datum/value channels, and moved RefSeq's shared transcript color mapping to
  the layered composition's fluent `encode()` call.
- Added a gallery regression for both serialized shared encodings. Validation:
  targeted gallery tests (3 passed), Ruff, MyPy, and `git diff --check` passed.

## 2026-08-13 - Typed sequence-example transform options

- Replaced the duplicated raw stack-sort mappings in the sequence-logo and
  alignment examples with `gs.compare()`, and replaced the alignment's FASTA
  format mapping with `gs.data_format()`.
- Added gallery assertions for the resulting sort and format specs. Validation:
  targeted gallery tests (5 passed), Ruff, MyPy, and `git diff --check` passed.

## 2026-08-13 - Added typed shared-axis configuration

- Added public `gs.axes()` alongside `gs.scales()` and used it for shared-axis
  declarations in the composed, RefSeq, and stacked genome-browser examples.
- Replaced the scrollable viewport's raw view mapping with `with_view()`.
  Validation: targeted API/gallery tests (7 passed), Ruff, MyPy, and
  `git diff --check` passed.

## 2026-08-13 - Exposed typed layout definitions

- Re-exported generated `Paddings` and `SizeDef` as public API and replaced
  the last simple layout dictionaries in the PIK3CA, UpSet, and ASCAT examples.
- Added API and depth-independent gallery regressions for the serialized
  padding and grow-height definitions. Validation: targeted API/gallery tests
  (7 passed), Ruff, MyPy, and `git diff --check` passed.

## 2026-08-13 - Split copy-number states around the baseline

- Changed the copy-number profile so LOH segments render above zero and retained
  heterozygosity segments render below zero; added ±2 diploid reference guides
  and an explicit axis label.
- Added a gallery regression for the signed formula and zero endpoint.
  Validation: targeted gallery tests (4 passed), Ruff, MyPy, and
  `git diff --check` passed.

## 2026-08-13 - Made the copy-number profile GISTIC-style

- Replaced the zygosity split with signed copy-number change from diploid:
  amplifications are red above zero, deletions blue below zero, and diploid
  segments gray on the midline.
- Updated the gallery assertion to cover the signed formula, event categories,
  and zero endpoint. Validation: targeted gallery tests (4 passed), Ruff,
  MyPy, and `git diff --check` passed.

## 2026-08-13 - Matched GISTIC's zero-baseline rect encoding

- Removed the explicit `y2` endpoint from the signed copy-number rects so they
  use the same zero-baseline behavior as the GISTIC score track: negative
  deletion values extend below the midline and positive amplifications above.
- Validation: targeted gallery tests (4 passed), Ruff, MyPy, and
  `git diff --check` passed.

## 2026-08-13 - Centered the copy-number profile domain at zero

- Fixed the signed copy-number y domain to `[-10, 10]`, matching the observed
  amplification extent and keeping zero at the visual midline rather than near
  the lower edge.
- Validation: targeted gallery tests (4 passed), Ruff, MyPy, and
  `git diff --check` passed.

## 2026-08-13 - Reverted the copy-number profile experiment

- Restored the original total-copy-number and LOH profile after the proposed
  GISTIC-style signed interpretation did not match the intended visualization.
- Validation: targeted gallery checks (3 passed) and `git diff --check` passed.
