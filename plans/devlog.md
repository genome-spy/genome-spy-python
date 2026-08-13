# Dev Log

## 2026-08-13 - Moved AlphaGenome editing into the visualization

- Replaced the Marimo checkpoint, device, precision, and alternate-allele
  controls with pinned notebook defaults and a base-resolution A/C/G/T designer
  inside the shared GenomeSpy view.
- Selected tiles now define an ordered multi-SNV haplotype. Each changed design
  runs one reference/alternate prediction pair regardless of edit count, while
  selecting the reference tile removes that position from the design.
- Kept the full 32 kb pan/zoom extent but opened on an eight-base window around
  the TAL1 control site. The editable grid now covers that complete interval,
  and GenomeSpy expands its four allele rows from one Arrow record per reference
  position, avoiding a fourfold transport payload.
- Split the reference sequence into the topmost track, using a GC overview at
  wide scales and colored reference letters at base resolution. The allele
  designer now follows it, ahead of genes and prediction tracks.
- Switched every shared genomic x encoding from raw quantitative coordinates to
  GenomeSpy locus channels. This avoids float32 precision loss around chr1:47M
  and preserves one distinct clickable column per nucleotide.
- Put the nucleotide letter above every colored selected tile and restored an
  edited position's old reference choice to a neutral letter-only cell. Grouped
  each assay's signal and delta panels under one shared x-axis to remove repeated
  coordinate labels.
- Updated the request identity, backend sequence application, selected-site
  guides, and focused tests for multiple substitutions.
- Validation: 29 focused tests, Marimo check, Ruff, and `git diff --check`
  passed. Headless Chromium rendered all eight base columns and confirmed two
  independent allele clicks with separate aligned guides; the dependency-free
  launch then stopped at the expected missing notebook-only Torch boundary.

## 2026-08-13 - Added locus context to the AlphaGenome view

- Verified that the prediction coordinates are aligned rather than displaced:
  the display starts at native AlphaGenome bin 384, and the default TAL1
  control base begins a 128 bp output bin exactly. Distal peaks therefore
  represent predicted activity or variant effects elsewhere in the locus.
- Added a field-backed dashed guide for the selected base through every gene,
  signal, and delta panel. The one-row guide dataset updates with the existing
  GenomeSpy view and does not reset its shared zoom.
- Added a semantic-zoom sequence treatment: a 128 bp GC-composition strip is
  visible across the full 32 kb interval, while nucleotide blocks and letters
  take over at detailed zoom levels.
- Added representative NCBI RefSeq hg38 models for TAL1 (`NM_003189.5`) and the
  partially visible neighboring STIL transcript (`NM_003035.2`) from UCSC's
  2025-08-13 track release.
- Validation: 29 focused Python tests, Ruff, and `git diff --check` passed.
  Headless Chromium rendered one stable GenomeSpy canvas with the GC overview,
  gene models, and aligned selected-site guides and no displayed runtime error.

## 2026-08-13 - Simplified AlphaGenome interaction state

- Kept the selected reference base, reconciled alternate allele, and processed
  click revision in one Marimo state value. The alternate control now rebuilds
  from that same state, so its displayed allele always matches the submitted
  and inferred variant after a base click.
- Removed separate click-submission, handled-click, and applied-request state.
  Successful frames now update the named prediction dataset directly, and the
  bounded session cache stores frames instead of redundant result wrappers.
- Moved pure click and display-state helpers into
  `_alphagenome_interaction.py` and shared the repeated prediction-tooltip
  definition. The notebook remains responsible for its GenomeSpy composition
  and visible reactive workflow.
- Validation: 29 focused Python tests, Ruff formatting and linting, MyPy for
  `src/`, and `git diff --check` passed. `marimo check` in the installed 0.23.16
  environment hung inside its asynchronous linter without diagnostics; direct
  `app.run()` coverage passed in the notebook tests.

## 2026-08-13 - Linked sequence navigation to click-driven predictions

- Expanded the packaged sequence dataset to the 32 kb display interval and put
  the sequence plus all prediction panels under one shared zoomable x scale.
  Sequence letters use the established semantic-zoom text treatment and the
  selected base is highlighted through a parameter-driven filter.
- Replaced 128 bp signal rules with zero-baseline bars. Dynseq letters were not
  used because these assay outputs are binned signals rather than per-base
  attribution scores.
- Removed the run button. Each valid sequence click submits its selected base
  and current alternate allele exactly once; repeat requests retain session
  caching, while initial rendering remains model-free.
- Validation: 29 focused Python tests, 13 frontend widget tests, Marimo check,
  Ruff, MyPy, and `git diff --check` passed. Headless Chromium confirmed an
  idle model-free render with one GenomeSpy canvas, no runtime errors, and no
  lingering spinner.

## 2026-08-12 - Polished the TAL1 prediction tracks

- Replaced point-only prediction panels with contiguous 128 bp rule segments
  for reference and alternate signals, followed by a compact zero-centered
  alternate-minus-reference delta subtrack for each assay.
- Put all eight prediction subtracks under one fixed, zoomable 32 kb display
  domain; stable named-dataset updates retain that rendered view.
- Added assay, track, biosample, ontology, interval, reference, alternate, and
  delta fields to prediction tooltips. Validation: 17 focused tests, Marimo
  check, Ruff, MyPy, and `git diff --check` passed.

## 2026-08-12 - Hardened AlphaGenome prediction recovery

- Made CUDA OOM failures discard tensor-retaining tracebacks, collect Python
  objects, and empty the CUDA cache while retaining the loaded model so a clean
  retry can succeed without another checkpoint load.
- Consolidated each TAL1 channel index, exact selector, display name, and panel
  title into one immutable display-track definition shared by inference and the
  GenomeSpy composition.
- Validation: Marimo check, Ruff, MyPy, 187 bounded Python tests, 14 focused
  backend tests, and all 13 frontend widget tests passed.

## 2026-08-12 - Validated AlphaGenome end to end on DGX Spark

- Validated the ephemeral launch on aarch64 Linux 6.17 with Python 3.12.3,
  Torch 2.13.0+cu130, and AlphaGenome-PyTorch 0.3.1 on an NVIDIA GB10
  (compute capability 12.1, bfloat16 supported). Unified accelerator memory
  reports 130,663,002,112 bytes total and roughly 1.4-1.8 GB initially free;
  system memory was 121 GiB total / 106 GiB available, with 1.4 TB disk free.
- Corrected two observed upstream integration mismatches: 0.3.1 has no `hf`
  extra and its wheel omits the advertised track metadata parquet. The launch
  now separately pins `huggingface-hub==1.27.0`, and the backend attaches a
  strict notebook-local catalog for the v0.3.1 human channel indices: RNA-seq
  561, DNase 44, H3K27ac 206, and H3K4me1 209. Preserving the Hugging Face
  `.safetensors` symlink suffix also prevents upstream `from_pretrained()` from
  misclassifying the cached blob as a pickle checkpoint.
- Used `uv run --python 3.12 --with alphagenome-pytorch==0.3.1 --with
  huggingface-hub==1.27.0 marimo run
  notebooks/alphagenome/genome_spy_alphagenome_pytorch.py`. The immutable
  checkpoint was `gtca/alphagenome_pytorch:model_all_folds.safetensors@b01c0ffa73e07c053491f3b5ea8bcf67d93b9920`,
  cached under `/home/okusupreme/.cache/huggingface/hub/`, size 920,635,044
  bytes.
- A real TAL1 C>A run loaded in 4.03 s, then completed REF in 1.41 s and warm
  ALT in 0.29 s. Peak CUDA allocation/reservation was 4.68/6.57 GB. All four
  cropped outputs had shape `(256, 1)`, produced 1,024 finite Arrow rows and a
  272,328-byte payload; adaptation, serialization, and stable widget update
  took 2.9, 8.2, and 1.8 ms respectively.
- Chromium verified idle startup, a sequence-base click, exactly one explicit
  prediction, successful CUDA status, one stable canvas, and no console errors.
  Multiple retained Marimo sessions can exhaust the currently free unified
  memory; a clean single session succeeds, while the failure path keeps the
  canvas mounted and reports CUDA OOM. Dense-track visual polish and a manual
  tooltip/zoom review remain follow-up work.

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

## 2026-08-11 - Rotated the devlog into indexed archives

- Normalized the 224-entry legacy log by date while preserving each entry block
  verbatim, kept the Aug 10–11 implementation phase active, and moved older
  entries into four date-range archives.
- Updated the devlog skill to distinguish the archive index from archive files,
  handle out-of-order legacy entries, and keep the active log below its line
  target.
- Validation: per-entry hashes matched exactly once across the active log and
  archives; archive ranges cover all older entries.

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
