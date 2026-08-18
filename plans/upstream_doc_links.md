# Linking to the upstream GenomeSpy documentation

Status: applied on 2026-08-18. This document remains the inventory and the
rationale for the link placement; use it when adding a page or an example.

Our documentation deliberately teaches a reduced, beginner-first path. The
upstream GenomeSpy documentation carries the detail we intentionally omit:
complete property tables, every transform, scale and axis internals, and the
original example specifications. Every place where a reader is likely to ask
"what else can this do?" should carry one link to the upstream page that
answers it.

Base URL: `https://genomespy.app/docs/`. All targets in this document were
verified to return HTTP 200 on 2026-08-18, including their heading anchors.

## Conventions

- Use ordinary Markdown links. No new roles, directives, or intersphinx setup.
- One consistent name in prose: **the GenomeSpy documentation** (never
  "the JS docs" or "upstream").
- Place a link at the *end* of the section whose concept it deepens, not in the
  middle of an explanation. Beginners should finish the local explanation first.
- Budget roughly two to four links per user-guide page. More than that turns a
  tutorial into a link farm.
- Prefer the deepest accurate anchor. `grammar/scale/#locus-scale` is more
  useful than `grammar/scale/`.
- Never replace local prose with a link. The link is the next step, not the
  explanation.

## 1. Getting started

`docs/getting-started.md`

| Where | Suggested link text | Target |
| --- | --- | --- |
| Declarative-grammar intro, after the three ingredients list (L7–13) | the GenomeSpy visualization grammar | `grammar/` |
| Type-code table (L78–86) | how GenomeSpy interprets data types | `grammar/mark/#visual-encoding` |
| Genomic interval section, after the locus explanation (L153–160) | genomic coordinates in GenomeSpy | `grammar/genomic-coordinates/` |
| "Where to go next" list (L162–169) | the GenomeSpy documentation | `grammar/` |

The "Where to go next" list is the single most valuable spot on the page: a
reader who finished the tutorial is exactly the reader who needs the full
grammar reference.

## 2. User guide

### `docs/user-guide/data.md`

| Where | Link text | Target |
| --- | --- | --- |
| End of "Records and fields" / inline data (L31–33) | inline data sources | `grammar/data/eager/#inline-data` |
| End of "Load a URL in the browser" (L75–77) | URL data and its supported formats | `grammar/data/eager/#url-data` |
| Same section, on format inference | tabular formats and field parsing | `grammar/data/eager/#tabular-formats` |
| Named-dataset mention (add if the page keeps one) | named data | `grammar/data/eager/#named-data` |

### `docs/user-guide/charts.md`

| Where | Link text | Target |
| --- | --- | --- |
| Mark-selection table (L50–58) | the complete mark reference | `grammar/mark/` |
| Each row of that table, optionally | per-mark pages | `grammar/mark/point/`, `rect/`, `rule/`, `tick/`, `text/`, `link/`, `arrow/` |
| "Ranged marks use secondary positions" (L80–82) | secondary position channels | `grammar/mark/#secondary-channels` |
| Static-vs-encoded table (L35–39) | mark properties | `grammar/mark/#properties` |

The per-mark links are worth the density here because our table is the only
place where a reader chooses a mark, and each upstream page documents
mark-specific properties we do not repeat.

### `docs/user-guide/encodings.md`

| Where | Link text | Target |
| --- | --- | --- |
| End of "Data types describe meaning" (L46–49) | how each type affects scales and guides | `grammar/mark/#visual-encoding` |
| End of "Visual channels" table (L66–75) | the full channel list | `grammar/mark/#channels` |
| End of "Index positions" (L97–98) | the index scale | `grammar/scale/#index-scale` |
| End of "Genomic loci" (L116–118) | the locus scale | `grammar/scale/#locus-scale` |
| End of "Field, datum, value, and expression" (L147–149) | GenomeSpy expressions | `grammar/expressions/` |

### `docs/user-guide/scales-axes-legends.md`

| Where | Link text | Target |
| --- | --- | --- |
| End of "Domain and range" (L67–70) | all scale properties | `grammar/scale/#properties` |
| End of "Axes explain positional scales" (L89–91) | axis ticks, labels, and grid lines | `grammar/axis/#ticks-labels-and-grid-lines` |
| End of "Legends explain visual scales" (L106–109) | legend placement and configuration | `grammar/legend/` |
| "Remove a guide with `None`" (L127–130) | disabling legends | `grammar/legend/#disabling-legends` |
| End of "Zoomable positional scales" (L144–147) | zooming and panning | `grammar/scale/#zooming-and-panning` |

### `docs/user-guide/transforms.md`

This page has the largest coverage gap: we document three transforms, GenomeSpy
has about thirty.

| Where | Link text | Target |
| --- | --- | --- |
| Filter section, on expression syntax (L36–39) | the expression language | `grammar/expressions/` |
| Same, constants and functions | available functions | `grammar/expressions/#provided-constants-and-functions` |
| Each documented transform | filter / formula / aggregate reference | `grammar/transform/filter/`, `formula/`, `aggregate/` |
| Closing paragraph (L118–121) — currently points only at our API reference | the complete transform reference | `grammar/transform/` |
| Optional, "Transform order matters" (L88–98) | debugging the data flow | `grammar/transform/#debugging-the-data-flow` |

The closing paragraph currently names sorting, stacking, lookups, windows,
genomic coordinates, sequence data, alignments, and label placement without
linking any of them. That sentence should link to `grammar/transform/`.

### `docs/user-guide/composition.md`

| Where | Link text | Target |
| --- | --- | --- |
| Operator table intro (L3–13) | view composition | `grammar/composition/` |
| End of "Layer complementary marks" (L41–43) | layering views | `grammar/composition/layer/` |
| End of "Stack aligned tracks vertically" / horizontal (L65–67) | view concatenation | `grammar/composition/concat/` |
| End of "Shared, independent, and excluded resolution" (L101–103) | scale, axis, and legend resolution | `grammar/composition/#scale-axis-and-legend-resolution` |
| Same section, on axis sharing | shared axes | `grammar/composition/concat/#shared-axes` |

Worth adding here even though we do not teach it: `grammar/composition/multiscale/`
and `grammar/import/`, since `MultiscaleChart` and `ImportedView` are part of
our public API and the gallery uses imports.

### `docs/user-guide/configuration.md`

| Where | Link text | Target |
| --- | --- | --- |
| Level table (L6–12) | config scopes | `grammar/config/#config-scopes` |
| "Explicit properties win…" (L15–16) | resolution order | `grammar/config/#resolution-order` |
| "Titles and descriptions" (L77–80) | title placement and styling | `grammar/title/` |
| "Step sizing" (L110–113) | step sizing | `grammar/composition/concat/#step-sizing` |
| "Container and flexible sizing" (L131–137) | `SizeDef` and child sizing | `grammar/composition/concat/#sizedef` |
| Same, on `viewportWidth`/`viewportHeight` (L139–141) | scrollable viewports | `grammar/composition/concat/#scrollable-viewports` |
| "Padding and spacing" (L144–147) | `Paddings` | `grammar/types/#paddings` |
| "Built-in themes" (L174–175) — the theme list is currently unsourced | the built-in themes | `grammar/config/#built-in-themes` |

### `docs/user-guide/genomic-axes.md`

| Where | Link text | Target |
| --- | --- | --- |
| Intro / locus channel (L1–9) | genomic coordinates | `grammar/genomic-coordinates/` |
| "How chromosome positions become one axis" (L54–64) | encoding genomic coordinates | `grammar/genomic-coordinates/#encoding-genomic-coordinates` |
| "Coordinate counting and offsets" (L66–99) | coordinate counting | `grammar/genomic-coordinates/#coordinate-counting` |
| "Built-in assemblies" (L101–103) — our list should not be the only source | supported genomes | `grammar/genomic-coordinates/#supported-genomes` |
| "Custom assemblies" (L117–137) | custom genomes | `grammar/genomic-coordinates/#custom-genomes` |
| `GenomeAxis` options (L30–32) | the genome axis | `grammar/axis/#genome-axis-for-loci` |

### `docs/user-guide/genomic-data.md`

| Where | Link text | Target |
| --- | --- | --- |
| Intro on lazy sources (L1–10) | lazy data sources | `grammar/data/lazy/` |
| Format table (L58–66) — one link per row | per-format parameters | `grammar/data/lazy/#bigwig`, `#bigbed`, `#indexed-fasta`, `#bam`, `#tabix-tsv`, `#gff3`, `#vcf` |
| "The scale controls loading" (L71–91), on `windowSize`/`debounce` | the lazy-source parameters | `grammar/data/lazy/` |

The format table is the strongest case in the whole user guide for one link per
row: each upstream section lists the exact parameters and the fields the source
returns, which we summarize in a single sentence.

### `docs/user-guide/genome-browser-layouts.md`

| Where | Link text | Target |
| --- | --- | --- |
| "Concatenate and link the tracks" (L42–51) | view concatenation | `grammar/composition/concat/` |
| "What is shared…" (L61–78) | resolution | `grammar/composition/#scale-axis-and-legend-resolution` |
| "Scroll a tall track" (L96–110) | scrollable viewports | `grammar/composition/concat/#scrollable-viewports` |
| "Reveal detail with semantic zoom" (L112–133) | zoom-driven layer opacity | `grammar/composition/layer/#zoom-driven-layer-opacity` |
| Same section, as an alternative technique | `multiscale` | `grammar/composition/multiscale/` |
| Optional, score-based point filtering | semantic zoom for points | `grammar/mark/point/#semantic-zoom` |

### `docs/user-guide/interaction.md`

| Where | Link text | Target |
| --- | --- | --- |
| Intro on named parameters (L1–9) | parameters | `grammar/parameters/` |
| "Bind a parameter to an input" (L32–39) | input bindings | `grammar/parameters/#using-input-bindings` |
| Reactive expression paragraph (L56–65) | expression parameters | `grammar/parameters/#expressions` |
| "Select marks and style them conditionally" (L70–95) | selection parameters | `grammar/parameters/#selection-parameters` |
| `empty=False` explanation (L90–92) | empty selections | `grammar/conditional-encoding/#empty-selections` |
| Conditional encodings generally | conditional encoding | `grammar/conditional-encoding/` |
| Interval selection snippet (L97–110) | interval selections | `grammar/parameters/#interval-selection` |
| Same, for overview-and-detail | scale domains from selections | `grammar/scale/#domain-from-selection-parameters` |
| "Add one ruler across linked tracks" (L112–137) | ruler parameters | `grammar/parameters/#ruler-parameters` |

This page exceeds the two-to-four budget on purpose: every subsection maps to a
distinct upstream section, and the upstream parameter documentation is
substantially deeper than ours.

### `docs/user-guide/notebooks.md` and `docs/user-guide/serialization.md`

Mostly Python-specific, so few links belong here.

| Where | Link text | Target |
| --- | --- | --- |
| `notebooks.md`, named datasets (L41–49) | named data | `grammar/data/eager/#named-data` |
| `serialization.md`, `$schema` paragraph (L18–20) | the GenomeSpy grammar the schema describes | `grammar/` |
| `serialization.md`, HTML output (L49–55) | embedding GenomeSpy in a web page | `api/embedding/` |
| Same, for `embed_options` / widget options | embed options | `api/embed-options/` |

## 3. Landing, about, and API reference

| File | Where | Target |
| --- | --- | --- |
| `docs/index.md` | The `[GenomeSpy](https://genomespy.app)` lead link (L17) currently points at the marketing site; add or redirect a second link to the documentation | `grammar/` |
| `docs/about.md` | "Versioning and the GenomeSpy core pin" (L7–14) — name the pinned grammar version and link it | `grammar/` |
| `docs/about.md` | Credits (L16–20) | keep the repo link, add the docs link |
| `docs/about.md` | Scope sentence about "richer cohort application concepts" (L3–5) — the deferred app layer is documented upstream | `sample-collections/` |
| `docs/api.md` | Intro (L7–8): state that each generated wrapper mirrors a GenomeSpy schema type | `grammar/types/` |

`grammar/types/` is the right target for the API reference specifically: it is
the upstream page that lists the same schema types our generated wrappers are
derived from (`Scale`, `Legend`, `SizeDef`, `Paddings`, `Parameter`, and so on).

## 4. Gallery examples

Not adopted. Gallery example pages carry no links to the upstream GenomeSpy
documentation, decided on 2026-08-18. Note for anyone revisiting this: most
gallery examples are ports of upstream GenomeSpy examples and reuse the same
`data.genomespy.app` sample files, and the gallery pages under `docs/gallery/`
are generated and gitignored, so any such link would have to come from example
module metadata rather than a Markdown file.

## 5. Suggested order

1. `transforms.md`, `genomic-data.md`, `interaction.md` — the three pages where
   our coverage is deliberately a small subset of the grammar.
2. The remaining user-guide pages.
3. `getting-started.md`, `index.md`, `about.md`, `api.md`.

## Validation

- `uv run pytest tests/test_docs_gallery.py tests/test_docs_tutorial.py -q`
- `uv run sphinx-build -b html -W --keep-going docs docs/_build/html`
- Re-check the anchors with `sphinx-build -b linkcheck` or a one-off `curl`
  sweep whenever the pinned `@genome-spy/core` version is bumped; upstream
  headings can move between releases.
