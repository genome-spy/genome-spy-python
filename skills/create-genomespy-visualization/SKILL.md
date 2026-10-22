---
name: create-genomespy-visualization
description: >
  Create, validate, and deliver interactive GenomeSpy Python charts from tables,
  including static scatter plot recreation, CSV/dataframe authoring, and HTML or
  notebook output with genome-spy-python. Covers table charts; genomic tracks,
  complete applications, and agent control of a user's live view are out of scope.
---

# Create a GenomeSpy visualization

Deliver reproducible Python source and a working interactive chart using the
installed public API. Do not invent methods from other plotting libraries or
upstream JavaScript APIs.

Requires Python 3.11+, genome-spy-python and Python/file execution. Plain records
need no extras; other inputs may. Frontend checks need browser/notebook access.

## Discover and reuse

1. Read [llms.txt](https://genomespy.app/genome-spy-python/llms.txt) once per task.
   Follow listed URLs; distinguish repeated titles by section and URL. Load only
   relevant pages, starting with focused agent guides.
2. Read the closest gallery example's source and explanation. Match comparison,
   marks, composition and interaction, not just dataset. Reuse needed components;
   adapt fields, domains, labels and rendering. Check preparation, dependencies
   and provenance. Use public data APIs, not internal example loaders.
3. Use indexed data, encoding, scale, interaction and rendering guides as needed;
   consult fuller guides/API signatures for unresolved options. Check unfamiliar
   options against installed signatures/docstrings; online examples may target a
   different version. Prefer matching checkout docs when versions differ.

If no example fits, use documented native features. Distinguish native support,
custom composition and capability gaps; offer a supported alternative for gaps.
Custom geometry requires an explicit request and stays in task-local code, labeled
as custom. See [capability boundaries](references/grouped-charts.md#supplied-order-and-capability-boundaries).

If the index fails, try the [gallery catalog](https://genomespy.app/genome-spy-python/agents/gallery.md)
or [quickstart](https://genomespy.app/genome-spy-python/agents/quickstart.md).
Otherwise use matching local docs (`docs/agents/quickstart.md`) or bundled
references and report the access limit.

## Author

- Inspect schema, a bounded sample, ranges, missing/nonfinite values, and category
  order; keep large raw tables out of context. Resolve source values, units,
  transformations and aggregation before encoding. Distinguish feature selection,
  record filtering, grouping and display order.
- Preserve supplied values/coordinates and record IDs; expose useful indexes.
  Separate display IDs from repeated labels. Disclose filtering, sampling,
  conversions and derived fields; never silently drop invalid rows.
- Use `import genome_spy as gs`, `gs.Chart(data)` and explicit `Q`, `N` or `O`
  types. Match scales to meaning, with units, deliberate category order/direction
  and native guides. Embeddings usually need `zero=False`; equal units require
  appropriate domains and dimensions.
- For recreation, freeze the reference first and read
  [reference checks](references/table-chart.md). For summaries/matrices, read
  [grouped charts](references/grouped-charts.md). Replace example styling with
  the intended mappings; disclose fidelity limits.

Clarify ambiguity that changes the chart or destination; otherwise state an
assumption and proceed. Python prepares tables/authors specs; GenomeSpy executes
declarative transforms and interactions in the browser.

## Verify and deliver

1. Validate with `chart.to_dict()` or `chart.to_json()`; check fields, types,
   domains and source values, not just row counts.
2. Save with `chart.save(path)` or display in the requested notebook.
   `inline=True` bundles the runtime, not URL datasets or a Python session.
3. Open the latest artifact. Inspect marks, axes, labels, legends, readability,
   runtime/resource errors and a known tooltip. For recreation, compare complete
   charts and registered plot-area overlays per the reference guide. When tools
   allow, check intended shared zoom and independent color meanings in panels.
   For linked selections, verify changed values, no matches and clearing against
   source data.
4. Deliver source/artifact, reused example/guide links, processing and departures.
   Distinguish spec validation, observed rendering, interaction and image export;
   report unverified checks. A canvas alone is not rendering evidence.

Prefer existing rendering paths before adding JavaScript, servers or dependencies.
For Python callbacks or live chart updates, read the
[Embed API guide](https://genomespy.app/genome-spy-python/agents/embed-api.md).
It requires a host connection; Python wraps a subset of the JavaScript API.

## Recover

- Unexpected option: inspect its installed signature before retrying.
- Blank chart: inspect errors, resources, fields and domains; keep validation on.
- File preview blocked: use a supported preview or, when permitted, serve only
  the output directory on loopback.
- Image export fails: bound waits, retain HTML and use a screenshot if available.
  Report export/hover limits separately. Stop when requested checks pass.
