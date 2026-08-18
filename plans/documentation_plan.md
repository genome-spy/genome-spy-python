# Beginner Documentation Plan

## Goal

Build a small, approachable GenomeSpy-for-Python manual that teaches the
declarative visualization grammar before cataloging API details. The result
should feel like Altair's documentation, cover the reusable core of GenomeSpy,
and lead a new user from a Python table to an interactive genomic track without
requiring prior visualization terminology.

The documentation should answer three questions in order:

1. What do I write to make a chart?
2. Why does that code produce this picture?
3. How do I combine the same building blocks into genomic visualizations?

## Source Material and Scope

Use the references for different purposes:

- Altair's getting-started and user-guide pages define the Python-facing tone,
  progressive examples, and separation between tutorial and reference.
- The [UW Visualization Curriculum](https://idl.uw.edu/visualization-curriculum/)
  defines the teaching sequence: introduction, marks and encodings,
  transformations, scales/axes/legends, composition, and interaction.
- GenomeSpy's local documentation under `tmp/genome-spy/docs/grammar/` defines
  the semantics and edge cases of the grammar.
- The Python gallery supplies working examples and links from concepts to
  complete applications.

This is a reduced core manual. It should document what the Python package
currently exposes and defer these topics:

- GenomeSpy App sample collections, provenance, bookmarks, and app-only APIs;
- exhaustive schema-property listings, which belong in API reference;
- every transform and mark on its own prose page;
- JavaScript embedding instructions;
- statistical analysis or data preparation unrelated to visualization.

## Audience

The primary reader knows basic Python and can recognize a table or dataframe,
but may not know visualization grammars or genomics file formats.

Do not assume the reader knows:

- declarative visualization;
- marks, encodings, channels, scales, or scale resolution;
- nominal, ordinal, quantitative, index, or locus data types;
- genome assemblies, genomic intervals, or coordinate conventions;
- layering versus concatenation;
- parameters, expressions, or transformations.

## Teaching Principles

### Introduce one idea per edit

Use a progressive chart that changes one line at a time:

1. provide data;
2. choose a mark;
3. map one field to `x`;
4. add `y` and `color`;
5. customize a scale, axis, or legend;
6. inspect the generated specification.

The reader should be able to attribute each visual change to one code change.

### Explain the grammar before shorthand

State the central model early:

> A chart describes data, a mark, and encodings. An encoding maps a data field
> to a visual channel such as position, color, or size.

Only then introduce shorthand such as `"value:Q"`. Show the equivalent
explicit form once:

```python
gs.Y("value:Q")
gs.Y("value", type="quantitative")
```

### Define jargon at first use

Use a short parenthetical or one-sentence definition, then use the term
consistently. Avoid standalone theory sections before the first chart.

Required concise definitions:

- **declarative**: describe what should be shown rather than drawing each
  shape manually;
- **mark**: the geometric shape used for a row, such as a point or rectangle;
- **encoding**: a rule that maps data to a visible property;
- **channel**: the property being controlled, such as `x`, `color`, or `size`;
- **scale**: a function that converts data values into positions, colors, or
  sizes;
- **axis**: a visible guide for a positional scale;
- **legend**: a visible guide for color, size, shape, or another channel;
- **transform**: an operation that derives, filters, groups, or rearranges data
  before drawing;
- **composition**: combining multiple views by layering or arranging them;
- **resolution**: the decision to share or separate a scale, axis, or legend;
- **locus**: a position in a genome, usually identified by chromosome and
  within-chromosome position;
- **genome assembly**: the named reference that supplies chromosome names,
  lengths, and order.

### Prefer visible examples over option lists

Use these as content checks rather than a fixed page template:

- one minimal example near the top;
- an additional variation when it clarifies the concept;
- an explanation tied to the specific code and rendered result;
- relevant gallery links when a complete application adds useful context;
- navigation to the next concept when readers need a prescribed sequence.

Let the subject determine the order and section names. Do not repeat stock
headings or transitions such as “What changed?”, “Recap”, and “Next” across the
guide.

Large property inventories and exhaustive signatures should link to the API
reference rather than interrupting the lesson.

### Keep ordinary visualization concepts separate from genomic extensions

Teach points, rectangles, fields, types, scales, and composition using tiny
ordinary tables. Once those concepts are stable, explain that GenomeSpy adds a
chromosome-aware `locus` type, genomic axes, lazy indexed data, and browser-like
multi-track composition.

## Information Architecture

### Getting started

Keep `docs/getting-started.md` as one linear, copy-pasteable tutorial that takes
about 15 minutes. It should not be a condensed API reference.

Proposed outline:

1. **What GenomeSpy for Python is**
   - A declarative Python interface to the GenomeSpy visualization grammar.
   - Suitable for ordinary tabular charts and genomics-native interactive
     views.
   - One diagram-sized sentence: Python objects serialize to a validated
     GenomeSpy specification, which the browser renders.
2. **Install and choose an environment**
   - Until the first package release, use the shortest supported source install
     from the repository. Replace it with `pip install genome-spy-python` only
     after that exact distribution is published and the command is verified in
     a clean environment.
   - State that the tutorial assumes JupyterLab, Notebook, VS Code notebooks,
     or Marimo.
   - Keep repository-development installation in contributing documentation,
     not the beginner path.
3. **Start with a table**
   - Use a six-row list of dictionaries so pandas is not required.
   - Explain rows and named fields.
4. **Create a chart and choose a mark**
   - `gs.Chart(data).mark_point()`.
   - Explain why all points overlap before encodings are added.
5. **Map fields to visual channels**
   - Add `x`, then `y`, then `color`.
   - Define `Q`, `N`, and `O` in a compact table.
   - Explain field/type shorthand and explicit channel objects.
6. **Customize guides without changing the data**
   - Add `.scale(zero=False)`, `.title(...)`, and `.legend(...)`.
   - Explain scale, axis, and legend in three short sentences.
7. **Make the first genomic track**
   - Use three inline genomic intervals.
   - Introduce `assembly="hg38"`, `gs.Locus("chrom", "start")`, `x2`, and a
     rectangle mark.
   - Explain half-open coordinates briefly and link to the detailed guide.
8. **Where to go next**
    - Data and file loading.
    - Grammar fundamentals.
    - Genomic coordinates.
    - Composition and linked tracks.
    - Specification inspection and serialization.
    - Gallery.
    - Reactive notebook updates, clearly labeled as an advanced path.

Move the current live-dataset update material out of Getting Started and into a
dedicated notebook/reactive-data page. It is valuable, but named datasets,
widgets, Arrow IPC, and lifecycle preservation are too many new concepts for a
first chart.

Keep specification inspection, immutability, and multi-track composition out of
the required 15-minute path as well. They may appear in a short optional “Going
further” list, but their explanations belong in the user guide.

### User guide

The user guide should follow the curriculum's conceptual order, with GenomeSpy
extensions inserted after the general grammar foundation.

#### Part 1 — Foundations

1. `data.md` — **Data and chart inputs**
   - records and fields;
   - lists of dictionaries and supported dataframe/table inputs;
   - inline data and URLs;
   - inheritance of data in composed views;
   - boundary between preparing data in Python and transforming it in the
     visualization.
2. `charts-and-marks.md` — **Charts and marks**
   - `Chart`, mark methods, and one-row-to-one-mark intuition;
   - point, rect, rule, text, link, arrow, and tick grouped by purpose;
   - static mark properties versus data-driven encodings;
   - `.properties(...)` for view-level settings.
3. `encodings.md` — **Fields, data types, and visual channels**
   - `Q`, `N`, `O`, `I`, and `L`, each with a concrete example;
   - primary positions, secondary positions, color, opacity, size, shape,
     text, and tooltip;
   - field, datum, value, and expression definitions;
   - shorthand versus explicit channel classes;
   - common mistakes: omitted type for expressions, `x2` without a primary
     position, and field/value confusion.
4. `scales-axes-legends.md` — **Scales and guides**
   - data domain versus visual range;
   - automatic defaults and selective customization;
   - axes and legends as guides generated from scales;
   - disabling guides with `None`;
   - zoomable scales;
   - defer named/shared scales and resolution to composition.
5. `transforms.md` — **Transform data before drawing**
   - teach filter, formula, and one aggregate example;
   - transformations run in order;
   - when to prepare data in Python instead;
   - expressions introduced only as needed;
   - link stack, lookup, window, genomic transforms, and the complete inventory
     to focused examples and API reference.

#### Part 2 — Building larger views

6. `composition.md` — **Layer and arrange views**
   - `+` for layers, `&` for vertical concatenation, `|` for horizontal
     concatenation, and `gs.concat(...)` for explicit grids;
   - inherited data, encodings, scales, and parameters;
   - shared, independent, and excluded resolution;
   - use the UpSet-style placeholder grid as the advanced concat example;
   - explain the view-level scale caveat with a small correct/incorrect pair.
7. `configuration.md` — **Titles, dimensions, padding, and themes**
   - distinguish mark properties, view properties, and global config;
   - fixed sizes, `gs.step(...)`, `gs.SizeDef(...)`, and container sizing;
   - `configure_*`, `with_view`, `gs.axes`, and `gs.scales` at the correct
     levels.

#### Part 3 — Genomics

8. `genomic-coordinates.md` — **Chromosomes and locus scales**
   - locus, assembly, chromosome order, and linearization;
   - point features versus intervals (`x`/`x2`);
   - coordinate counting and offsets;
   - built-in and custom assemblies;
   - multiple assemblies as an advanced subsection.
9. `genomic-data.md` — **Large and indexed genomic data**
   - lazy loading and why genome browsers need it;
   - BigWig, BigBed, indexed FASTA, BAM, and tabular interval sources;
   - viewport-driven loading;
   - link to focused gallery examples rather than duplicating every option.
10. `genome-browser-layouts.md` — **Build linked tracks**
    - vertical track composition;
    - shared locus scales and axes;
    - independent y scales;
    - titles, heights, scrolling, and semantic zoom;
    - a reduced two-track browser built step by step.

#### Part 4 — Interaction and output

11. `interaction.md` — **Parameters and interaction**
    - zoom and pan first;
    - value parameters and input bindings;
    - selections and conditional encoding;
    - rulers and linked cursor guides;
    - expressions as reactive values;
    - persistence/app-specific behavior excluded or linked upstream.
12. `notebooks.md` — **Display and update charts in notebooks**
    - implicit display and `.widget()`;
    - named datasets;
    - `set_dataset()` and `set_data()`;
    - supported dataframe/table inputs and Arrow transport;
    - stable-cell guidance for reactive notebooks.
13. `serialization.md` — **Inspect and share specifications**
    - `to_dict()` and `to_json()`;
    - what the browser receives;
    - saving JSON and HTML;
    - defer round-tripping and validation controls to the API reference.

## Navigation and Page Design

Replace the flat user-guide toctree with four captioned groups matching the
parts above. The landing page should provide a one-sentence description per
page and two entry paths:

- **New to declarative visualization?** Start with Data and chart inputs.
- **Already know Altair or Vega-Lite?** Start with Genomic coordinates.

Keep API reference and gallery separate from the learning sequence. Concept
pages should link to API symbols, but API pages should not carry the teaching
burden.

## Examples and Rendering

### Tutorial example progression

Use a small set of recurring datasets so the reader learns the grammar rather
than repeatedly decoding new data:

- a six-row ordinary table for the first chart;
- a five-row interval table for `x`/`x2` and rect/rule marks;
- a three-feature genomic interval table for the first locus chart;
- one small two-track dataset for composition and shared scales.

### Live output in prose pages

The docs should show the rendered result directly after important code blocks.
Reuse the gallery extension's known-good static GenomeSpy bundle import and
`embed(c, spec, { bare: true })` path. Add a prose-page directive that embeds a
named example/spec without introducing iframe or resize wrappers.

The directive should:

- load a named chart from a checked-in, docs-only Python module;
- render deterministically during the Sphinx build;
- use `literalinclude` regions from that same module for displayed code so the
  copied snippet, rendered output, and tested object have one source;
- support an optional fixed height;
- fail the build if the named example cannot serialize.

Implement the directive in the existing `genomespy_gallery` extension and
extract/reuse its direct static-bundle embed builder. Do not add executable
notebooks or duplicate example code in Markdown and Python. If this small
extension cannot be completed in the first slice, use exact gallery links and
defer prose embeds; do not introduce an untested second rendering path.

## Writing Style Rules

- Address the reader directly and use short paragraphs.
- Lead each section with the result the reader is about to produce.
- Prefer “maps the `score` field to vertical position” over “sets the y
  encoding.”
- Use “view” only after defining it as one chart area with its own marks.
- Avoid “simply,” “obviously,” “just,” and unexplained acronyms.
- Keep notes and warnings rare. A warning must state what fails, why, and the
  corrected pattern.
- Use domain examples without assuming biology knowledge. Define SNV, interval,
  and reference genome only when they first matter.
- Use consistent example colors, field names, and assemblies.
- End each page where the subject naturally concludes. Add a next-step link
  only when the learning sequence requires one.

## Implementation Sequence

### Phase 1 — Getting Started

1. Rewrite `docs/getting-started.md` as the linear tutorial above.
2. Add or reuse the two tiny datasets needed by the tutorial.
3. Put each displayed chart in one docs-only importable Python module, include
   its exact source regions in the page, and render the named chart through the
   existing gallery extension.
4. Move reactive dataset updates to the future notebook page.
5. Add focused tests for all code snippets and serialized tutorial specs.
6. Build the docs with warnings as errors and inspect desktop/mobile layouts.

Acceptance criteria:

- a reader can install the package and render a chart from a copied block;
- the published installation command matches the current release state;
- `data`, `mark`, `encoding`, `channel`, and the basic type codes are defined
  before use;
- the tutorial reaches a genomic interval track without a conceptual jump;
- no section requires knowledge introduced later;
- every shown spec is imported from its documentation source, serialized, and
  validated in tests.

### Phase 2 — User Guide Foundations

Write Data, Charts and marks, Encodings, Scales/axes/legends, and Transforms.
Refactor the current `charts.md` and `encodings.md` rather than preserving their
page boundaries when the new structure is clearer.

Acceptance criteria:

- each page has a minimal example, variation, explanation, gallery links, and
  next step;
- terminology matches GenomeSpy's grammar and the Python API;
- generated signatures are linked rather than copied manually.

### Phase 3 — Composition and Genomics

Write Composition, Configuration, Genomic coordinates, Genomic data, and
Genome-browser layouts. Use the corrected oncoprint and UpSet examples as
advanced references for shared/excluded scale resolution, but keep them out of
the beginner examples.

### Phase 4 — Interaction, Notebooks, and Output

Write Parameters/interaction, notebook display and live updates,
and a concise saving and specification-inspection page. Keep error-message
catalogs and example-specific debugging out of the conceptual guide. Place a
short warning beside a concept only when it prevents a likely misuse.

### Phase 5 — Editorial and Navigation Pass

- remove duplicated explanations across pages;
- add cross-links and “Next” links;
- verify glossary terms are defined once before broad reuse;
- check all code against the public package exports;
- audit links to upstream GenomeSpy for advanced or app-only topics;
- build with `sphinx-build -W`;
- visually inspect representative prose and gallery pages.

## Testing and Maintenance

- Put tutorial chart construction in importable docs-only modules, include the
  exact source with `literalinclude`, and import those same objects in focused
  docs tests so snippets cannot silently drift from the API.
- Validate every complete chart with `.to_dict()`.
- Check all internal links and build Sphinx with warnings treated as errors.
- Keep upstream links near claims they support and prefer local explanations
  for foundational concepts.
- When the schema/API changes, update API reference automatically and revise
  prose only when user-facing concepts change.
- Treat thumbnails and rendered outputs as derived artifacts.

## First Writing Slice

Start with only `docs/getting-started.md` and its tests. Do not restructure the
entire user guide in the same change. The first slice should establish the
voice, terminology, progressive example, and genomic bridge that later pages
will follow.
