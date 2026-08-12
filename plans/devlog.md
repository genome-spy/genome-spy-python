# Dev Log

## 2026-08-12 - Removed the standalone Arrow transport benchmark

- Removed `scripts/benchmark_arrow_transport.py`; its encoding-size comparison
  was development-only evidence and did not serve the library or a maintained
  user workflow.
- `scripts/` now contains no tracked project files. Arrow serialization and
  widget update behavior remain covered by focused tests.

## 2026-08-12 - Removed notebook-local operational scripts

- Removed the AlphaGenome display benchmark, CUDA smoke/check commands, TAL1
  and BRCA2 reference fetchers, their shared fetch helper, generated caches,
  and the script-only CUDA test.
- Added focused ignore rules for future AlphaGenome operational scripts and
  reference fetchers so such one-off utilities remain local rather than
  becoming maintained project tooling.
- Kept the established generic Arrow transport benchmark as the only tracked
  file under `scripts/`; DGX measurements now belong in the development log
  after exercising the notebook directly.

## 2026-08-12 - Reduced Marimo examples to the AlphaGenome workflow

- Removed the generic Arrow-reactive, sequence-click, synthetic
  mutation-impact, TCF7L2, and LUAD Marimo notebooks plus their generated
  session/cache artifacts and notebook-specific tests.
- Kept `notebooks/alphagenome/` as the only maintained notebook area and
  retained its model-local helpers, CUDA tooling, packaged references, and
  tests.
- Replaced the mixed showcase plan with a focused AlphaGenome interaction,
  model-boundary, memory, validation, and polish plan. Reusable Arrow/widget
  behavior remains covered at the library level.

## 2026-08-12 - Replaced the three-point showcase with TCGA LUAD cohort triage

- Added an offline Marimo workflow for clinically filtered TCGA LUAD
  MAPK-pathway review: stacked alteration burden, AJCC stage, a four-layer
  oncoprint, MSI, gene prevalence, and selected-gene event classes use linked
  vertical/horizontal composition and one stable GenomeSpy widget.
- Prepared each cohort in Polars and sends all coordinated rows in one named
  Arrow dataset. Stage and sample-order controls, plus gene/sample clicks,
  update the existing view without loading spinners or partial track states.
- Made hover behavior explicit with curated tooltip rows and the default
  handler on every foreground mark; background matrix cells disable tooltips
  so they cannot mask alteration picking.
- Validation: Chromium rendered the composition with no console errors and a
  real matrix hover showed sample, stage, gene, and alteration. Default
  preparation measured 3.8 ms median with a 330 KB Arrow payload; focused
  notebook tests and all 13 widget tests passed.

## 2026-08-12 - Kept credible-set context visible during PIP emphasis

- Replaced destructive PIP filtering in the three-variant TCF7L2 explorer with
  tested display styling: candidates below the threshold fade, the selected
  variant stays fully opaque, and every source-reported candidate remains in
  the Arrow dataset.
- Added a live passing-count explanation and clarified that the compact plot
  compares position, PIP, and fixed-lead LD rather than showing regional GWAS
  associations.
- Validation: Chromium showed all three variants initially and retained two as
  faint context at PIP 0.30, with a `1 of 3` summary and no console errors;
  focused notebook tests and all 13 widget tests passed.

## 2026-08-11 - Fixed the invisible TCF7L2 locus marks

- Reproduced the blank TCF7L2 chart in Chromium and confirmed that the Arrow
  rows were loaded: the default quantitative x scale included zero, compressing
  three variants spanning roughly 4.3 kb against the edge of a 113 Mb domain.
- Added a locus-padded position domain and enabled x-scale zoom. The chart keeps
  its stable named dataset and reactive PIP/selection updates.
- Validation: Chromium displayed all three variants with no console errors and
  changed the domain on wheel zoom; Marimo check, Ruff, all 13 frontend widget
  tests, and the full Python suite (`271 passed, 1 skipped`) passed.

## 2026-08-11 - Fixed reactive Arrow payload ordering in Marimo

- Reproduced the synthetic notebook in Chromium and traced the live AnyWidget
  model and GenomeSpy collectors. Marimo synchronized the dataset revision
  before its binary payload, so the revision listener reloaded the preceding
  empty Arrow table and ignored the later payload.
- Changed live dataset subscriptions to react to payload arrival. Initial data
  still loads during mounting, and revision checks continue to reject stale
  asynchronous results.
- Added a frontend regression for revision-before-payload synchronization and
  restored the selection opacity and original Polars serializer after proving
  they were unrelated.
- Validation: all 13 frontend widget tests and 39 focused Python tests passed;
  Chromium rendered the reference, alternate, and delta marks after the button
  click with no console errors.

## 2026-08-11 - Replaced invalid datum expressions in interactive examples

- Fixed TCF7L2, synthetic mutation-impact, and AlphaGenome sequence-editor
  opacity encodings. GenomeSpy mark-level `ExprRef` values cannot access
  `datum` fields, so selected-state opacity now travels as a quantitative field
  in the named Arrow datasets.
- Selection changes continue to update the stable dataset and parameter state;
  no chart rebuild or model work was introduced.
- Validation: 11 notebook tests passed with one skip, Ruff, and Marimo checks
  passed. `git diff --check` still reports unrelated pre-existing trailing
  whitespace at `README.md:140`.

## 2026-08-11 - Added the upstream PIK3CA lollipop gallery example

- Recreated GenomeSpy's TCGA-BRCA PIK3CA protein lollipop plot with the
  upstream embedded mutation/domain data, responsive `displace1d` collision
  placement, `xOffset` encodings, and true-position connectors.
- Added its gallery regression test and reviewed a browser-rendered thumbnail.
- Fixed incremental Sphinx builds to re-read the landing-page mini-gallery when
  examples change. Validation: gallery tests, Ruff, and strict Sphinx builds
  passed.

## 2026-08-11 - Corrected CUDA smoke targeting and shared fixture preparation

- Made the CUDA smoke report reject CPU devices and use the explicitly selected
  CUDA device for synchronization, allocator peaks, and GPU properties,
  including `cuda:N` runs.
- Extracted shared UCSC fetch, allele validation, checksum, and deterministic
  gzip serialization into `scripts/_fetch_reference.py`; TAL1 and BRCA2
  wrappers now contain only locus-specific metadata.
- Validation: focused dataset/backend/CUDA tests (`30 passed`), Ruff, both
  fetcher `--help` paths, and `git diff --check` passed. No checkpoint or
  model was downloaded.

## 2026-08-10 - Grouped AlphaGenome notebooks and private helpers

- Moved the local AlphaGenome Marimo notebook and its three private support
  modules into `notebooks/alphagenome/`; general examples remain directly in
  `notebooks/`.
- Updated all test, benchmark, CUDA-smoke, launch-command, and showcase-plan
  references. The scripts now add only the scoped AlphaGenome directory to
  their import path.
- Validation: Ruff, Marimo check, focused AlphaGenome/notebook/CUDA-report
  tests (`35 passed, 1 skipped`), the model-free display benchmark, and
  `git diff --check` passed. The benchmark remained at 255,424 Arrow bytes for
  1,024 rows and a 0.15 ms median Python-side dataset update.

## 2026-08-10 - Clarified SNV scope and froze a splicing-example preflight

- Corrected the TAL1 notebook and plan: the official Jurkat insertion is
  biological context only, not a runnable preset. The first local backend
  accepts exactly one SNV, and the UI now states that boundary directly.
- Extracted pure notebook decisions for stale/failure display state and whether
  a successful prediction should replace the live Arrow dataset. Added
  regression coverage that confirms a failed request retains its error and does
  not resend the prior result.
- Audited the next candidate against AlphaGenome's official splicing tutorial:
  the BRCA2 SNV `chr13:32316462 T>G` is a real, SNV-compatible starting point.
  The planned v1 display is limited to the five-class, 1 bp `splice_sites`
  output. It remains gated on a DGX measurement because 1 bp splicing requires
  the decoder and has a materially different memory profile from the TAL1
  128 bp tracks.
- Packaged a checksum-verified 131,072 bp GRCh38 context for that BRCA2 SNV,
  obtained from the UCSC sequence API. The self-contained asset and its
  preparation script are intentionally only the reproducible input fixture;
  they do not download a model, run a splicing head, or imply validated model
  output.

## 2026-08-10 - Added an opt-in CUDA evidence command

- Added `scripts/smoke_alphagenome_pytorch_cuda.py` for the pending DGX-class
  hardware gate. It requires either an existing checkpoint path or an explicit
  `--download` flag, runs the packaged TAL1 SNV through the same notebook-local
  backend, and emits JSON for GPU details, model-load/inference peak allocator
  memory and timing, display adaptation/Arrow timing, output bytes, rows, and
  exact track names.
- It loads no model for `--help`, changes no project dependency or lockfile, and
  always releases the resident model in `finally`. Validation: script Ruff and
  safe `--help` invocation passed.
- Added a dependency-free JSON checker for the fixed TAL1 output contract and
  the two-second post-inference display budget. It reports load/inference memory
  headroom for the development log and rejects missing tracks, wrong bin count,
  oversized Arrow payloads, exhausted device memory, and slow adaptation.
  Validation: full pytest suite (`266 passed, 1 skipped`), 12 Node widget tests,
  repository-wide Ruff, MyPy, and `git diff --check` passed. Both scripts' safe
  `--help` paths completed without loading the model.

## 2026-08-10 - Hardened the local model path against OOM and redundant redraws

- Replaced the implicit one-entry model LRU with an explicit single-model
  lifecycle. A changed checkpoint, on-disk checkpoint revision, device, or
  precision releases the previous model before allocation; failed loads also
  clear unused accelerator memory.
- The loader now constructs and fills the model on CPU before moving the
  completed model to CUDA. Compute precision resolves to bfloat16 mixed mode on
  compatible CUDA devices and float32 on CPU or older CUDA devices; unavailable
  CUDA and unsupported precision choices fail before checkpoint download.
- Expanded request/cache identity to include exact metadata selectors,
  input/display intervals, output resolution, and resolved precision. Notebook
  stale state also responds to checkpoint, device, and precision controls.
- Separated result status from successful dataset application. Failures keep
  the prior visualization without retransmitting its Arrow payload, and cache
  hits only update GenomeSpy when their successful request differs from the
  displayed request.
- Moved the adapter row-budget check ahead of native-array reads and Python-list
  construction, and centralized the empty prediction schema.
- Validation: full pytest suite (`264 passed, 1 skipped`), 12 Node widget tests,
  repository-wide Ruff, MyPy, Marimo check, and `git diff --check` passed. The
  model-free benchmark remained at a 255,424-byte payload, 0.92-second startup,
  and approximately 0.15 ms median Python-side Arrow update.

## 2026-08-10 - Completed the model-free AlphaGenome-PyTorch notebook path

- Audited `genomicsxai/alphagenome-pytorch` v0.3.1 and the
  `gtca/alphagenome_pytorch` Hugging Face model. The notebook pins package
  0.3.1 and checkpoint revision
  `b01c0ffa73e07c053491f3b5ea8bcf67d93b9920`; weights and outputs remain under
  the separate AlphaGenome Model Terms.
- Added a lazy notebook-local backend that validates one SNV, runs only RNA,
  DNase, and histone heads at 128 bp, selects four exact CMP tracks from bundled
  metadata, performs reference/alternate inference sequentially, and crops
  tensors before moving them to CPU.
- Packaged a deterministic, checksum-verified 131,072 bp hg38 TAL1 reference
  context fetched from the UCSC sequence API. The asset records its source,
  interval, coordinate convention, retrieval date, sequence digest, and the
  validated chr1:47,239,296 reference allele; notebook startup performs no
  remote sequence request.
- Added `genome_spy_alphagenome_pytorch.py`, which loads/downloads the
  checkpoint only after explicit prediction, retains failed/stale results,
  and updates one stable Arrow `predictions` dataset. Normal editor
  interactions do not invoke the model or rebuild the chart.
- Added an eight-entry insertion-ordered session cache keyed by package,
  checkpoint identity, reference checksum, organism, assembly, interval,
  variant, and selectors. Local checkpoint identities change when the file is
  replaced, and cached results avoid repeat inference.
- Kept Torch and `alphagenome-pytorch` out of all project dependency groups.
  The notebook documents an ephemeral Python 3.12 `uv --with` launch, and a
  regression test verifies no model import occurs when its setup screen opens.
- Removed the now-obsolete API metadata-audit helper and updated the showcase
  plan to use the local runtime.
- Added a reproducible model-free display benchmark. On the Apple M5
  development host, startup was 0.99 seconds and a 1,024-row, four-track update
  serialized to 255,424 Arrow bytes; Python-side `set_dataset()` timing was
  below 0.2 ms. This does not include browser paint or model inference.
- Validation: full pytest suite (`259 passed, 1 skipped`), 12 Node widget tests,
  Ruff, MyPy, AlphaGenome notebook Marimo check, and `git diff --check` passed.
  The multi-gigabyte checkpoint was intentionally not downloaded because this
  host has no representative CUDA device. Live model latency, peak memory, and
  browser-visible update timing remain the hardware-dependent gates.

## 2026-08-10 - Browser-host Marimo smoke remains externally pending

- Attempted the planned real Marimo click smoke through the available browser
  workflow, but this session exposes no browser instance. No alternative
  browser automation was used, so the host-level acceptance check remains
  distinct from the passing Python/widget tests.

## 2026-08-10 - Avoided redundant reactive dataset work on repeated clicks

- The locus and sequence editor now compare a normalized click with their
  existing Marimo selection before writing state. Repeated clicks remain
  observable through the widget revision but do not trigger redundant state
  propagation or re-send unchanged Arrow data.
- Validation: `uv run pytest tests/test_notebook.py -x` (9 passed, 1 skipped),
  focused Ruff, and `git diff --check` passed.

## 2026-08-10 - Removed full-track materialization from the display adapter

- Changed the AlphaGenome adapter to calculate visible bin bounds from the
  display interval, slice native positional-bin arrays first, and only then
  convert those visible values to Python/Polars. This keeps a 1 Mb inference
  response from becoming a 1 Mb Python-list conversion for a small viewport.
- Added a slice-tracking regression test that rejects a full-track read in the
  crop path. The adapter retains its explicit total-row budget, so visual data
  preparation remains bounded without a loading state.
- Validation: full pytest suite (`251 passed, 1 skipped`), Node widget tests
  (12 passed), Ruff, MyPy, and `git diff --check` passed.

## 2026-08-10 - Applied maintainability review to the Marimo examples

- Made the AlphaGenome adapter require a bounded display interval and enforce a
  total Arrow-row budget. Its output schema now explicitly makes optional
  metadata nullable strings, so RNA/DNase and histone tracks concatenate
  safely. Added mixed-modality, crop, and budget regression tests.
- Tightened the request contract: variants must change alleles and fit their
  full reference span inside the model interval; request IDs include organism
  and normalize duplicate selectors; reference checksums are verified against
  the packaged sequence.
- Simplified the TCF7L2 explorer to its supported credible-set view, retained
  a selected low-PIP point in the display, and reject click keys absent from
  the packaged table. The synthetic editor now derives its GenomeSpy default
  selection from the same state as its Marimo selection.
- Replaced the filename-branching notebook test with a compact parametrized
  smoke test plus focused behavior tests. The TCF7L2 fixture now records the
  full source GraphQL query and has a byte-integrity regression hash.
- Validation: full pytest suite (`250 passed, 1 skipped`), Node widget tests
  (12 passed), Ruff, MyPy, and `git diff --check` passed.

## 2026-08-10 - Added an explicit TAL1 metadata-audit command

- Added `scripts/audit_alphagenome_tal1_metadata.py`, which requires an
  externally supplied `ALPHAGENOME_API_KEY` and explicit model-fold argument,
  makes one `output_metadata()` call, and emits JSON candidate tracks for the
  fixed TAL1 ontology. It does not submit predictions or write files.
- The report requires and preserves stable track-selector fields (`name`,
  `strand`, `ontology_curie`, `biosample_name`) for RNA-seq, DNase, and histone
  ChIP. It intentionally leaves the biological choice of exact panels to
  review rather than selecting a track by dataframe row position.
- Added fixture-based tests for output filtering and missing metadata errors.
  Validation: `uv run pytest tests/test_alphagenome_metadata_audit.py
  tests/test_alphagenome_request.py tests/test_alphagenome_adapter.py -x`
  (7 passed), focused Ruff, and `git diff --check` passed.

## 2026-08-10 - Audited the installable AlphaGenome client boundary

- Verified the current official PyPI client is `alphagenome==0.7.0` and is
  compatible with this project's Python floor. Its `dna_client.create()` API
  accepts an explicit `ModelVersion`; the installed enum exposes `ALL_FOLDS`
  and `FOLD_0` through `FOLD_3`.
- Confirmed the fixed requested modalities (`RNA_SEQ`, `DNASE`, and
  `CHIP_HISTONE`) exist in that client. Official metadata documents 1 bp RNA
  and DNase tracks, 128 bp histone tracks, and selector fields including
  `name`, `strand`, `ontology_curie`, and `biosample_name`.
- Did not freeze a model enum member or exact TAL1 selector tuple: both require
  a credentialed `output_metadata()` response and a scientific choice rather
  than an assumption. No API prediction was submitted.

## 2026-08-10 - Added pure AlphaGenome request-contract helpers

- Added `notebooks/alphagenome/_alphagenome_request.py`, a notebook-local, dependency-free
  contract for normalized variants, zero-based half-open model intervals,
  reference-slice validation, and deterministic request/cache IDs.
- The helpers deliberately construct no client and read no credentials. They
  require an explicit client/model version and keep the AlphaGenome boundary as
  plain Python values until live access and supported metadata are frozen.
- Added regression tests for the one-based `Variant.position` to zero-based
  reference lookup boundary, selector-order-invariant cache IDs, and
  out-of-context variants.
- Validation: `uv run pytest tests/test_alphagenome_request.py
  tests/test_alphagenome_adapter.py -x` (5 passed), focused Ruff, and
  `git diff --check` passed.

## 2026-08-10 - Froze the TCF7L2 fine-mapped locus fixture

- Chose Open Targets Platform as the source for the first offline locus
  example: its Platform data are CC0 1.0 and its GraphQL API returned the
  GRCh38 PICS type-2-diabetes credible set for `GCST000712`, study locus
  `017ce45f7d79a0216126dd31c01b9929` (TCF7L2 lead `rs7903146`).
- Added the compact, provenance-bearing
  `tcf7l2_type2_diabetes_locus` packaged JSON fixture. It contains only the
  three returned 95% credible-set variants, source PIPs, and source-reported
  LD to the reported lead, plus explicit zero-/one-based coordinates.
- Deliberately limited v1 to a fixed-lead credible-set review: the API record
  does not supply a complete LD matrix or regional association statistics for
  tag variants, so neither is inferred. The fixture exposes these limitations
  for the notebook UI.
- Added loader coverage for the fixture. Validation: `uv run pytest
  tests/test_datasets.py -x` (15 passed), focused Ruff, and `git diff --check`
  passed.

## 2026-08-10 - Added the offline TCF7L2 credible-set Marimo explorer

- Added `notebooks/genome_spy_tcf7l2_locus_explorer.py`. It renders the frozen
  fixture as aligned reported-lead association and credible-set PIP tracks,
  with source r² color, an explicit PIP display filter, and a provenance/detail
  card.
- A credible-set click sets one Marimo-owned allele-specific selection state;
  the `selectedVariant` GenomeSpy parameter reflects that state. PIP filtering
  updates only the stable named `variants` Arrow dataset, without rebuilding
  the chart. Repeated clicks retain their widget `click_revision`.
- The notebook makes its fixed-lead and missing-regional-summary-statistics
  limitations visible in the UI, avoiding an implication that it supports
  arbitrary lead recoloring or regional association review.
- Validation: full pytest suite passed (`240 passed, 1 skipped`) and Node
  widget tests passed (12). A subsequent cell-dependency lint correction was
  validated with notebook/dataset tests (`22 passed, 1 skipped`), Ruff, MyPy,
  and `git diff --check`.

## 2026-08-10 - Added a notebook-local AlphaGenome track adapter

- Added `notebooks/alphagenome/_alphagenome_adapter.py`, which converts fixed selected
  reference/alternate AlphaGenome `TrackData` pairs into one long-form Polars
  dataframe for the live `predictions` dataset.
- The adapter uses the published `TrackData` contract only: positional-bin ×
  track values, metadata rows, resolution, and zero-based half-open interval.
  It selects by stable metadata, preserves raw values, computes raw
  `ALT - REF`, and rejects ambiguous selectors or incompatible pairs.
- Added fake-object tests for metadata order independence, bin/coordinate
  alignment, and interval mismatch errors; no AlphaGenome package was added to
  the core dependency set.
- Validation: focused suite passed: `22 passed, 1 skipped`; Node widget tests
  passed (12); `uv run ruff check .`, `uv run mypy src/`, and `git diff --check`
  passed.

## 2026-08-10 - Rebuilt the offline sequence-edit interaction shell

- Added `notebooks/genome_spy_mutation_impact.py` using the packaged synthetic
  reference fixture as development-only input, with explicit text that its
  deterministic signals are neither AlphaGenome output nor biological evidence.
- Implemented a click-selected base, alternate-base control, and explicit
  run-button flow. A synchronized `selectedBase` parameter highlights the
  clicked base without rebuilding the chart, and the last synthetic result is
  retained in Marimo state until the user generates a new one. The alternate
  selector excludes the selected reference base.
- Kept the chart structure stable with immutable `sequence` data and one
  Arrow-backed `predictions` dataset containing reference, alternate, and raw
  `ALT - REF` values. Changing the selected base or alternate allele after a
  successful run produces an explicit stale state while preserving that result.
- Added programmatic Marimo and helper coverage for named datasets, initial
  state, signal alignment, and delta magnitude.
- Validation: `uv run pytest tests/test_notebook.py tests/test_widget.py -x`
  (20 passed, 1 skipped), `node --test tests/widget.test.mjs` (12 passed),
  `uv run ruff check .`, `uv run mypy src/`, and `git diff --check`.

## 2026-08-10 - Began the fine-mapped locus source audit

- Confirmed that the public FinnGen R12 release supplies GRCh38 summary
  association statistics and indexed FINEMAP/SuSiE fine-mapping files from the
  same cohort; the T2D endpoint includes a practical TCF7L2-region fallback
  candidate.
- Kept FinnGen as an audit candidate rather than a frozen source because its
  access flow and terms must explicitly permit redistributing a curated subset
  in the package.
- Corrected the planned association contract: store a harmonized
  `effect_allele_frequency`, and reserve `maf` for a source-provided minor
  allele frequency. FinnGen reports alternate-allele frequency and effects.
- The in-app browser host was unavailable for the manual Marimo click smoke;
  automated notebook and widget-bridge coverage remains the current evidence.

## 2026-08-10 - Added the Marimo sequence-click interaction probe

- Added `notebooks/genome_spy_sequence_click_probe.py`, a focused stable-widget
  Marimo notebook with a named Arrow dataset of base tiles, an
  expression-backed `editorDomain` parameter, and explicit `pos0`/`pos1`
  fields.
- Enabled click synchronization and made the dependent Marimo cell consume both
  `clicked_datum` and `click_revision`; it accepts only well-formed
  `interaction_kind="sequence_base"` payloads, so repeated clicks on one base
  remain observable while unrelated marks are ignored.
- Added notebook checks for the configured parameter/domain and payload
  validation, plus a widget-JavaScript regression confirming that repeated
  identical clicks publish the datum and advance the revision twice.
- Validation: `uv run pytest tests/test_notebook.py tests/test_widget.py -x`
  (18 passed, 1 skipped), `node --test tests/widget.test.mjs` (12 passed),
  `uv run ruff check .`, `uv run mypy src/`, and `git diff --check`.
- A real browser/Marimo-editor click remains the manual M0 acceptance check;
  this slice verifies the notebook and bridge contracts without changing the
  public library API.

## 2026-08-10 - Tightened the Marimo showcase plan after review

- Preserved source-reported credible sets per fine-mapping signal in a
  normalized table and changed the interactive cutoff to a PIP filter rather
  than a credible-set definition.
- Made variant identity allele-specific, documented zero- and one-based
  coordinates, required effect-allele harmonization, and required complete LD
  vectors for selectable lead variants without treating missing LD as zero.
- Froze the AlphaGenome v1 story to the official Jurkat TAL1 insertion, a
  checksum-verified hg38 reference slice, 1,048,576 bp context, fixed metadata
  selectors, and explicitly pinned client and API model versions.
- Restricted synthetic AlphaGenome output to development/tests, simplified v1
  requests to one explicit non-overlapping submission, and required all model
  panels to update through one `predictions` dataset.
- Added initial data/responsiveness budgets and replaced the serial milestone
  dependency with independent locus, AlphaGenome-contract, and interaction
  gates.
- Validation was a plan consistency and source-contract review only; no
  notebook implementation changed.

## 2026-08-10 - Planned interactive Marimo genomics showcases

- Audited the completed live Arrow dataset and parameter/click bridges against
  two biologically grounded Marimo examples.
- Chose an offline fine-mapped GWAS locus explorer as the first common genetics
  workflow, with live LD re-anchoring from clicked variants and a provenance
  gate before freezing the packaged locus.
- Audited the sequence-editing proposal against the current AlphaGenome API and
  recommended a TAL1 enhancer positive-control story, explicit click-select /
  choose-allele / predict interaction, 1 Mb inference context, cropped Arrow
  tracks, and single-variant scope before haplotypes.
- Added coordinate, credential, request-lifecycle, model-terms, scientific
  interpretation, and fixture-redistribution guardrails in
  `plans/marimo_genomics_showcase_plan.md`.
- Validation was plan, repository, upstream source, API documentation, and
  published-paper review only; no notebook implementation was changed.

## 2026-08-10 - Drafted a focused GitHub README

- Reworked the repository landing README around a concise project description,
  source installation, two executable examples, contribution guidance, and
  upstream references.
- Made Altair's role as the main design inspiration explicit in the opening
  description, while distinguishing GenomeSpy Core from deferred App features.
- Verified both README chart examples serialize as valid GenomeSpy specs.

## 2026-08-10 - Implemented live widget dataset updates

- Upgraded the pinned GenomeSpy Core/schema bundle to 0.83.1, which provides
  in-memory Arrow named-dataset loading.
- Reused render preparation to rewrite eager widget data as declared named
  datasets, with collision-safe generated names and explicit scoped-owner
  metadata.
- Added persistent per-dataset payload, format, and revision traits plus
  `JupyterChart.set_dataset()` and unambiguous `set_data()`; data updates do not
  rewrite the synchronized spec.
- Replaced widget Blob/re-embed updates with direct Core `datasets.load()` and
  `datasets.set()` calls, retaining the embed for data-only changes.
- Added Arrow table, multi-dataset, pre-mount, multi-view, lifecycle, error,
  and DataView tests. The tracked Marimo example now creates a stable widget and
  calls `view.set_dataset("table", filtered_dataframe)` downstream.
- Validation: 231 pytest tests passed (one skipped), 11 Node tests passed,
  MyPy and Ruff passed, and a strict Sphinx build passed. Host-browser checks
  for JupyterLab/Marimo interaction and zoom preservation remain manual.

## 2026-08-10 - Planned live widget dataset updates

- Audited issue #2 against the current Arrow preparation, AnyWidget renderer,
  widget tests, and project architecture.
- Confirmed GenomeSpy Core 0.83.1 contains the merged in-memory
  `datasets.load()` API with bounded `DataView`, latest-operation-wins, and
  failure-preservation behavior.
- Planned one widget-only rewrite of the existing prepared spec, persistent
  per-dataset traits, and a strict split between structural rerenders and live
  dataset applies in `plans/issue_2_live_widget_datasets.md`.
- Tightened acceptance coverage with explicit Polars/pandas/PyArrow
  `set_dataset()` tests, state-identity assertions, no-overlay checks for steady
  updates, and a Marimo example that specifically uses `set_dataset("table",
  ...)` from a downstream reactive cell.
- Kept Parquet, runtime dataset creation, custom messages, duplicate serializers,
  and speculative scoped Python APIs out of scope.
- Validation was source and plan review only. A direct environment check
  confirmed Traitlets supports dynamic `add_traits()`; a `uv run` probe could
  not resolve build requirements because sandboxed network access was unavailable.

## 2026-08-11 - Rotated the devlog into indexed archives

- Normalized the 224-entry legacy log by date while preserving each entry block
  verbatim, kept the Aug 10–11 implementation phase active, and moved older
  entries into four date-range archives.
- Updated the devlog skill to distinguish the archive index from archive files,
  handle out-of-order legacy entries, and keep the active log below its line
  target.
- Validation: per-entry hashes matched exactly once across the active log and
  archives; archive ranges cover all older entries.
