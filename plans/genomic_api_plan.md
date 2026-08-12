# Genomic API Expansion Plan

## Goal

Enable `genome-spy-python` to recreate GenomeSpy documentation examples,
especially genome tracks and lazy genomic data views, through the handwritten
Altair-style API rather than dropping to `Root(...)` plus raw spec dicts.

This plan focuses on the smallest ergonomic additions that unlock a broad class
of GenomeSpy-native examples:

- lazy data sources
- root/composition-level genomic configuration
- generic and targeted transform helpers
- reusable patterns for browser-style genome tracks

The immediate success target is to reimplement the current
`docs/examples/genome_tracks.py` example fully through the Python chart API.

## Why This Matters

The current schema layer already validates much of what we need. The main gap is
the handwritten ergonomic layer:

- top-level properties like `assembly`, `scales`, `spacing`, `view`,
  `viewportHeight`, and `params` are not yet pleasant to express
- lazy data sources require raw dicts
- many GenomeSpy transforms require raw dicts
- genome-track examples therefore fall off the Altair-style path and into raw
  JSON too quickly

If we close those gaps carefully, we unlock not just one track example but a
large portion of the GenomeSpy docs and example catalog.

## Reference Findings

### Altair

Relevant files reviewed:

- `tmp/altair/altair/vegalite/v6/api.py`
- `tmp/altair/altair/vegalite/v6/data.py`
- `tmp/altair/altair/vegalite/v6/schema/core.py`

Patterns worth mirroring:

1. **Top-level mixin over generated schema classes**
   - `TopLevelMixin.properties(...)` updates top-level schema properties
     generically.
   - `TopLevelMixin._add_transform(...)` appends schema transform objects while
     preserving immutable-style chaining.

2. **Data wrappers stay schema-backed**
   - Altair exposes schema objects like `UrlData`, `InlineData`, and `Data`
     rather than inventing a parallel userland representation.
   - Data preprocessing is centralized inside serialization rather than spread
     across user-facing APIs.

3. **Transform helpers are incremental, not magical**
   - Altair adds many thin `transform_*` methods as convenience wrappers around
     schema transform classes.
   - The core pattern is consistent: construct a schema object, append it, and
     return a shallow copy.

4. **Top-level configuration remains generic**
   - Altair does not create a separate “special chart type” for every
     visualization family. Instead it makes top-level properties and transforms
     expressive enough that many chart patterns emerge naturally.

Implication for us:

- We should prefer a small `TopLevelSpec` expansion plus schema-backed helpers
  over a new specialized genome-track DSL.

### gos

Relevant files reviewed:

- `tmp/gos/gosling/api.py`
- `tmp/gos/gosling/data/__init__.py`
- `tmp/gos/gosling/schema/core.py`

Patterns worth learning from:

1. **Lightweight data constructor functions**
   - `gosling.data` exposes helpers like `csv(...)`, `bigwig(...)`, `bed(...)`,
     `matrix(...)`, and `multivec(...)`.
   - These functions return schema-compatible mappings and optionally adapt
     local files into served URLs.

2. **Thin transform helpers**
   - `gos.Track` exposes small methods like `transform_filter(...)`,
     `transform_coverage(...)`, and `transform_exon_split(...)`.
   - These helpers are minimal wrappers around generated schema classes.

3. **Composition remains ergonomic**
   - `Track`, `View`, `overlay`, `stack`, `horizontal`, and `vertical` keep the
     user-facing API concise while relying on the schema underneath.

Implication for us:

- A small `genome_spy.data` or `genome_spy.lazy` helper surface is likely the
  right fit.
- Genome-specific transform helpers should be thin wrappers, not a new planner
  or separate abstraction layer.

## Proposed Design Direction

### Principle 1: Keep the Altair-style center of gravity

The primary API should remain:

- `Chart(...)`
- `mark_*()`
- `encode(...)`
- composition helpers like `vconcat(...)`, `hconcat(...)`, layering
- `properties(...)`
- `transform_*()` methods

We should not introduce a separate “track builder framework” unless repeated
examples prove the core chart API is insufficient.

### Principle 2: Add a generic escape hatch before adding many bespoke helpers

Before creating a large family of GenomeSpy-specific methods, add a generic way
to append schema-valid transforms and to express schema-backed data objects.

This prevents every new GenomeSpy transform from becoming a blocker.

### Principle 3: Grow from real example ports

API additions should be justified by reimplementing real GenomeSpy docs
examples, not by abstract completeness.

Recommended order:

1. current genome tracks example
2. a second lazy genome-track example from GenomeSpy docs
3. a pyGenomeTracks-inspired browser view
4. a richer annotation or sashimi-style example

## Milestones

### Milestone 0 - Design audit and target-example inventory

Objective:

Define exactly which GenomeSpy docs/examples should drive the first API slice.

Deliverables:

- this plan document
- a shortlist of 2-4 target examples that exercise the required features
- a feature matrix mapping each target example to:
  - data source style
  - top-level properties
  - transforms
  - composition patterns
  - channel features

Success criteria:

- we can point to a minimal, example-driven feature set for the next milestones
- no speculative helper APIs are added yet

### Milestone 1 - Root/composition ergonomic parity

Objective:

Make top-level genomic and composition properties ergonomic enough that complex
GenomeSpy examples do not need `Root(...)` for ordinary configuration.

Scope:

- support convenient setting of:
  - `assembly`
  - `scales`
  - `spacing`
  - `view`
  - `viewportHeight`
  - `params`
- ensure these work on both unit charts and composed charts where schema allows
- keep validation schema-backed

Implementation direction:

- extend `TopLevelSpec.properties(...)` and composition classes where needed
- follow Altair’s generic `properties(...)` pattern rather than introducing
  bespoke setter methods for everything

Success criteria:

- a composed genome-track view can set `assembly="hg38"` and an x-domain at the
  top level without dropping to raw `Root(...)`

### Milestone 2 - Data-source helpers for remote and lazy genomic data

Objective:

Create a first-class data API for GenomeSpy-native and example-friendly data
sources.

Scope:

- add schema-backed or schema-compatible helpers for:
  - URL-backed tabular data
  - lazy data sources
  - optionally inline JSON values through a common API
- likely shapes to evaluate:
  - `gs.Data(...)`
  - `gs.UrlData(...)`
  - `gs.lazy.bigwig(...)`
  - `gs.lazy.gff3(...)`
  - `gs.lazy.bigbed(...)`

Design guidance:

- mirror Altair’s preference for schema-backed data wrappers
- borrow the usability of `gosling.data.bigwig(...)` and similar constructors
- do not overcommit to local file serving yet unless a concrete use case
  requires it

Open design question:

- Should lazy loaders live under `genome_spy.data`, `genome_spy.lazy`, or as
  wrappers exported from `genome_spy` directly?

Recommendation:

- start with a small `genome_spy.data` or `genome_spy.lazy` namespace and keep
  top-level exports minimal

## Upstream genomic example gap audit

The refreshed upstream inventory under
`tmp/genome-spy/examples/docs/genomic-data/examples` contains 14 specs. Seven
patterns are already represented by existing Python examples: cytobands, scored
RefSeq genes, ASCAT segmentation, sashimi, ClinVar, GENCODE GFF3 annotations,
and BAM alignments. The current gallery also has a stacked browser composition.

The remaining gaps are:

| Upstream example | Current fit | Missing ergonomic/API surface |
|---|---|---|
| `msa.json` | Partial | `multiscale` composition; the basic FASTA/flatten/aggregate/stack path works |
| `dynseq-spi1-bqtl.json` | Partial | `coordinateLookup`, template imports, dynamic allele parameters |
| `tcga-ov-gistic.json` | Partial | `regexFold` for the all-lesions panel; q-value panel works |
| `genome-browser.json` | Partial | URL/template view imports; direct composition already works |
| `indexed-fasta-six-frame-translation.json` | No | lookup tables, window/lead operations, named templates, arrow composition |
| `hcc1954-sv-cnv.json` | No | VCF self-lookup, `regexFold`, window operations, conditional hover state |
| `ASCAT-algorithm.json` | No | cross joins, parameterized fitting grid, richer aggregate/filter dataflow |

The generated schema already contains definitions for `LookupParams`,
`CoordinateLookupParams`, `RegexFoldParams`, `WindowParams`, `ImportSpec`,
`TemplateImport`, `MultiscaleSpec`, `AlignmentMismatchesParams`, and the
related data-source classes. They should be exposed through thin handwritten
helpers rather than authored as raw nested dictionaries in gallery examples.

## Next API extension plan

### Phase G1 - Generate schema-driven fluent APIs

Extend `tools/schemapi/codegen.py` so generated schema coverage becomes usable
through the public builder API. The generator should inspect the discriminated
transform union (`TransformParams`) and emit a reusable transform mixin with
signatures derived from each generated `*Params` wrapper. It should likewise
emit data-source constructors and composition/import wrappers for
`ImportSpec`, `TemplateImport`, and `MultiscaleSpec`.

Generated methods should construct generated schema classes, append or compose
them immutably, and preserve the generic `.transform(...)` escape hatch. Adding
a new upstream transform should then require schema regeneration, not a new
handwritten method in `chart.py`.

### Phase G2 - Keep handwritten code Python-specific

After generated coverage exists, keep manual code limited to behavior the JSON
schema cannot describe: pandas/DataFrame normalization, notebook rendering,
validation/copy semantics, and small aliases such as `gs.lazy.bigwig(...)` when
they materially improve discoverability. Do not create one-off wrappers for
individual upstream examples.

### Phase G3 - Parameter and interaction ergonomics

Make `gs.param(...)` and selection definitions work naturally in top-level
`properties(params=...)`, conditional encodings, and transform expressions.
Add the minimal selection/event helpers needed for ASCAT fitting and HCC1954
hover emphasis, with focused tests for serialized parameter state.

### Phase G4 - Regenerate and port the remaining examples

Port in dependency order:

1. Complete MSA with `multiscale`.
2. Complete dynseq with coordinate lookup and allele templates.
3. Complete GISTIC all-lesions with regex folding.
4. Compose the imported genome browser.
5. Port six-frame translation.
6. Port HCC1954 SV/CN.
7. Port ASCAT algorithm last, once joins and parameterized fitting are stable.

Each port must include a focused spec test, a real PNG thumbnail, and no large
user-facing preprocessing block. Dataset-specific preparation belongs in the
datasets module or in the upstream remote dataflow.

Success criteria:

- the genome-track example can declare its BigWig and annotation data without
  raw dict literals

### Milestone 3 - Generic transform escape hatch

Objective:

Ensure any valid GenomeSpy transform can be expressed through the chart API even
before a dedicated helper exists.

Scope:

- add a generic transform appender such as:
  - `.transform(mapping)`
  - or `.transform_custom(type=..., ...)`
- keep existing typed helpers like `transform_filter(...)` and
  `transform_formula(...)`
- preserve immutable chaining semantics

Why this comes early:

- without it, every missing transform blocks example ports
- with it, we can port examples immediately and then selectively promote common
  transforms to first-class methods

Success criteria:

- the current genome-track example can be rebuilt without raw root JSON even if
  some transforms are still generic mappings

### Milestone 4 - First wave of GenomeSpy-native transform helpers

Objective:

Promote the most reused GenomeSpy transforms from raw mappings into ergonomic,
discoverable methods.

Priority candidates:

- `transform_linearize_genomic_coordinate(...)`
- `transform_pileup(...)`
- `transform_measure_text(...)`
- `transform_filter_scored_labels(...)`
- `transform_flatten_compressed_exons(...)`
- `transform_collect(...)`
- `transform_project(...)`
- `transform_flatten(...)`

Design guidance:

- follow Altair and `gos`: thin wrappers over schema transform objects or raw
  validated mappings
- do not attempt to cover every GenomeSpy transform at once

Success criteria:

- the current genome-track example becomes readable as Python code rather than a
  giant block of dict literals
- at least one more GenomeSpy docs example can be ported using the same helper
  set

### Milestone 5 - Example-driven genome-track API validation

Objective:

Reimplement a small set of real examples end-to-end and use them to validate
the API shape.

Target set:

1. current genome tracks with RefSeq annotations example
2. one additional lazy genome-track example from GenomeSpy docs
3. one pyGenomeTracks-inspired browser view

What to evaluate:

- is the API readable?
- are the transforms discoverable?
- do top-level properties compose cleanly?
- are raw dict escape hatches still needed too often?

Success criteria:

- at least 2-3 real genome-browser-style examples can be expressed mostly with
  the handwritten API
- remaining raw dict usage is limited and points to specific next gaps

### Milestone 6 - Optional higher-level genomics conveniences

Objective:

Only after multiple successful example ports, consider reusable track builders.

Candidates:

- `gs.track.refseq_genes(...)`
- `gs.track.gc_bigwig(...)`
- `gs.track.gff3_genes(...)`
- `gs.track.coverage(...)`

Guardrail:

- do not add these unless they remove duplication across multiple examples
- prefer helper functions layered on top of the core chart API, not special
  privileged pathways in the serialization layer

Success criteria:

- any new convenience helper clearly simplifies repeated patterns without hiding
  important GenomeSpy concepts

## Suggested Execution Order

1. Milestone 1: root/composition ergonomics
2. Milestone 2: data-source helpers
3. Milestone 3: generic transform escape hatch
4. Milestone 5: first example port using mostly generic transform mappings
5. Milestone 4: promote repeated transforms into named helpers
6. Milestone 5 again: port additional examples and refine
7. Milestone 6 only if repetition justifies it

This order is intentional:

- top-level properties and data wrappers are foundational
- the generic transform hook keeps progress unblocked
- targeted transform helpers should come after we observe actual repetition

## Risks and Guardrails

### Risk: Overdesigning a genome-track DSL

Guardrail:

- keep the central abstraction as `Chart` plus composition
- add helper namespaces only when they clearly reduce duplication

### Risk: Too many one-off transform methods too early

Guardrail:

- add generic transform support first
- promote only transforms that show up across multiple real examples

### Risk: Diverging from Altair’s mental model

Guardrail:

- keep top-level property mutation generic through `properties(...)`
- keep helpers thin and schema-backed
- avoid hidden serialization magic beyond data normalization

### Risk: Local-file serving scope creep

Guardrail:

- first support remote URLs and explicit lazy specifications cleanly
- defer local lazy-data serving until a concrete, repeated need appears

## Validation Plan

For each milestone:

- add focused unit tests for new API helpers
- port or add one documentation example that uses the new surface
- rebuild docs to ensure gallery import and serialization still work
- keep schema validation enabled by default

Recommended milestone test themes:

- top-level property round-tripping
- data wrapper serialization
- generic transform serialization
- dedicated transform helper serialization
- example spec equivalence for a chosen reference example

## Near-Term Recommendation

The next implementation slice should target Milestones 1-3 together as one
practical package:

- root/composition ergonomics
- data-source helpers
- generic transform escape hatch

That combination is the smallest useful API jump that lets us start porting
real GenomeSpy genomic examples through the handwritten chart API.
