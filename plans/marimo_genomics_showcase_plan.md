# Interactive AlphaGenome Marimo Showcase Plan

## Objective

Maintain one polished Marimo notebook that demonstrates GenomeSpy as an
interactive visualization layer for sequence-to-function modeling. The user
selects one or more alternate alleles in a base-resolution sequence designer
and immediately compares local `alphagenome-pytorch` reference, designed, and
delta regulatory tracks.

The notebook lives at
`notebooks/alphagenome/genome_spy_alphagenome_pytorch.py`. Non-model Marimo
prototypes are development history, not user-facing examples, and are not kept
in `notebooks/`.

## Product Contract

- The sequence and prediction panels share one zoomable genomic x scale.
- Wide views show sequence composition and representative gene models; base
  letters replace the composition overview at detailed zoom levels.
- A synchronized guide marks the selected base through the gene and prediction
  panels so distal model effects cannot be mistaken for coordinate offsets.
- A four-row A/C/G/T track acts as the allele designer. Each selected tile sets
  one position in the designed sequence; selecting the reference tile removes
  that edit.
- Initializing the notebook runs one reference-sequence prediction to populate
  and warm the signal tracks. Each changed design then starts one additional
  reference-versus-designed prediction.
- Marimo owns mutation and request state; GenomeSpy parameters and click events
  carry only small interaction values.
- Sequence and prediction tables move through stable named Arrow datasets.
- Dataset changes update the existing GenomeSpy view without rebuilding the
  canvas or resetting zoom.
- The notebook supports multiple non-overlapping SNVs as one designed
  haplotype. Indels remain out of scope.

## Model Boundary

- Use the community `alphagenome-pytorch` implementation and Hugging Face
  checkpoint only from the notebook's transient environment.
- Do not add Torch, `alphagenome-pytorch`, or model weights to project
  dependencies.
- Keep the setup screen importable in the project's Python 3.11 environment
  without importing Torch, initializing CUDA, or downloading weights.
- Pin the package version, checkpoint repository, filename, and immutable
  revision in the request identity.
- Users remain responsible for accepting the model terms governing weights and
  outputs.

## Biological Story

Use the packaged GRCh38 TAL1 enhancer reference as the default sequence-design
workflow. The documented Jurkat TAL1 insertion remains biological context only
because the local backend accepts substitutions, not indels.

Show:

1. a categorical A/C/G/T sequence-design track;
2. representative RefSeq gene context for the displayed locus;
3. aligned reference and alternate regulatory signal tracks;
4. an alternate-minus-reference delta track;
5. selected-site and model-interval context;
6. explicit assay/ontology metadata and provenance;
7. request status, stale state, timing, and actionable errors.

Predictions are hypothesis-generating model output, not causal or clinical
evidence.

## Performance and Memory Guardrails

- Use a fixed 131,072 bp inference context initially.
- Request only required output heads at 128 bp resolution.
- Crop tensors on the accelerator before CPU conversion and Arrow transport.
- Keep at most one resident model; changed checkpoint identity must release the
  old model before loading another.
- Do not run overlapping submissions or duplicate a completed request.
- Keep the cropped prediction table below 250,000 rows and 10 MB Arrow IPC.
- Apply model output to the visualization within two seconds after tensors are
  available, excluding inference time.
- On CUDA OOM, preserve the last successful display, release temporary tensors,
  and show recovery instructions.

## Tests

Pure helper coverage:

- coordinate conversion and reference-allele validation;
- canonical multi-variant and request-key construction;
- checkpoint identity and cache invalidation;
- metadata selection independent of row order;
- tensor crop boundaries and display downsampling;
- model-output adaptation at supported resolutions;
- empty outputs, missing metadata, unsupported variants, and OOM recovery;
- stale display state and prevention of redundant dataset updates.

Notebook/browser coverage:

- notebook opens without importing or loading the model;
- sequence clicks publish well-formed base data;
- a changed allele design is the only inference trigger;
- one successful request produces one live prediction-dataset update;
- reference, alternate, and delta tracks render with useful tooltips;
- zoom and the stable canvas survive prediction updates;
- repeated clicks, errors, stale results, and cached results remain observable.

## Milestones

## Deferred Follow-up

- Preserve the GenomeSpy widget's pan/zoom state across Marimo reactive output
  updates. See [marimo_widget_zoom_state.md](marimo_widget_zoom_state.md).

### M1 — Model-free interaction shell

- Keep the packaged TAL1 reference, linked sequence track, click-submission
  state machine, and empty prediction dataset runnable without Torch.
- Verify click routing, allele validation, deduplicated submissions, stale
  state, and stable widget updates.

### M2 — Local backend contract

- Pin and install the community package only in the notebook environment.
- Load one checkpoint explicitly, validate the frozen metadata selectors, and
  adapt a single-SNV result to the fixed visualization schema.
- Preserve the single-model lifecycle and OOM guardrails.

### M3 — DGX validation

- Exercise the notebook directly on the target DGX Spark and record device
  details, load/inference timing, peak allocator memory, Arrow bytes, output
  rows, and exact track names in the development log.
- Reduce requested heads, interval, or display resolution if the documented
  budgets fail.

### M4 — Showcase polish

- Browser-verify the complete allele, zoom, click-to-predict, inspect, stale,
  and recovery workflow.
- Add concise notebook guidance and scientific limitations.
- Consider additional SNV-compatible loci only after the TAL1 workflow is
  reliable; do not broaden the public library API solely for this notebook.
