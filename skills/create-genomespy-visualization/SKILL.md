---
name: create-genomespy-visualization
description: >
  Create, validate, and deliver interactive GenomeSpy Python charts from tables,
  including static scatter plot recreation, CSV/dataframe authoring, and HTML or
  notebook output with genome-spy-python. Covers table charts; genomic tracks,
  complete applications, and agent control of a user's live view are out of scope.
---

# Create a GenomeSpy visualization

Turn the user's data and intended comparison into reproducible Python source and
a working interactive chart. Use the installed public API; do not invent Python
methods from other plotting libraries or upstream JavaScript APIs.

Requires Python 3.11+, genome-spy-python, and Python/file execution. Frontend
verification needs browser or notebook access. Optional table dependencies depend
on the input; plain records need only the base package.

## Read the relevant guide

Start with the self-contained [table-chart guide](references/table-chart.md) for a
runnable example, API pitfalls, fidelity checks, overlays, and color calibration.
For grouped summaries, matrices, distributions, or clustering trees, also read
[grouped charts](references/grouped-charts.md). Both work outside this repository.
For more context, start with the [agent documentation index](https://genomespy.app/genome-spy-python/llms.txt)
and read only relevant pages. Before authoring, consult the [gallery catalog](https://genomespy.app/genome-spy-python/agents/gallery.md)
for the closest working example. Reuse its public chart API, encodings, composition,
and rendering path; adapt data, labels, and domains. Check dependencies and data
preparation rather than copying internal dataset helpers. Add a workaround only
when the existing pattern cannot meet the task, and explain the specific gap.
The index also links maintained user guides for deeper context. Use its explicit
Markdown endpoints; do not assume arbitrary human pages have Markdown equivalents. The checkout's fuller
quickstart remains `docs/agents/quickstart.md`.

If the index is unavailable, try the direct Markdown links below. If those fail,
use the corresponding human guide, local docs, or bundled references and report
the access limit. Publication builds can precede live deployment.

Read only the relevant agent page for further detail:

| Task | Guide |
| --- | --- |
| Data inputs or index fields | [Data](https://genomespy.app/genome-spy-python/agents/data.md) |
| Fields, types, channels | [Encodings](https://genomespy.app/genome-spy-python/agents/encodings.md) |
| Scales and legends | [Scales and guides](https://genomespy.app/genome-spy-python/agents/scales-axes-legends.md) |
| Notebook display | [Notebooks](https://genomespy.app/genome-spy-python/agents/rendering.md) |
| Export | [Serialization](https://genomespy.app/genome-spy-python/agents/rendering.md) |
| Public signatures | [API](https://genomespy.app/genome-spy-python/agents/api.md) |

Check installed public signatures/docstrings before using unfamiliar options.
If an option is unavailable or web access fails, use matching checkout docs
and bundled references. Report the limitation; do not treat unverified features as available.

## Author from the data's meaning

- Inspect schema, a bounded sample, ranges, missing/nonfinite values, and category
  order. Keep large raw tables out of context.
- Clarify ambiguity that changes the chart: field meaning, units, coordinate
  source, category order, or destination. Otherwise state an assumption and proceed.
- Preserve supplied measurements and coordinates. Disclose filtering, conversions,
  sampling, and derived fields; do not silently drop invalid rows.
- Use `import genome_spy as gs`, `gs.Chart(data)`, marks, and explicit `Q`, `N`,
  or `O` types. Expose pandas indexes when they supply record IDs.
- Choose scales for the comparison: nominal color for categories, quantitative
  color for continuous values, and units in labels. Embeddings usually need
  `zero=False`; use equal screen scaling when geometry requires it.
- For recreation, freeze the reference call, version, data, palette, domains, and
  plot-area dimensions first. Preserve data selection, expression source, order,
  scale limits, and color meaning; disclose departures. Do not recompute supplied
  coordinates/measurements or substitute a similar dataset.
- Python prepares tables and authors specs. GenomeSpy runs declarative transforms
  and interactions in the browser; `.transform_*()` does not compute in Python.

## Verify and deliver

1. Use `chart.to_dict()` or `chart.to_json()` with default validation. Check fields,
   types, domains, and data against the intended comparison.
2. Save HTML with `chart.save(path)` or display in the requested notebook. Use
   `inline=True` to bundle the runtime; it neither downloads URL datasets nor
   includes a running Python session.
3. Open the artifact when frontend tools are available. Inspect marks, labels,
   colors, readability, runtime errors, and a known record's tooltip. Canvas
   presence alone does not verify correct rendering. For recreation, follow the table-chart guide's
   side-by-side, footprint, common-capture color, and overlay checks.
4. Deliver reusable source and the artifact with a brief processing/check report.
   Distinguish spec validation from observed rendering and interaction. State
   frontend verification limits instead of claiming visual success without evidence.

Use existing rendering paths before adding JavaScript, a server, or dependencies.
Charts may support user interaction; this skill cannot read live zooms/selections.

## Recover from failures

- Unexpected keyword: inspect the installed signature before retrying. Use the
  table-chart guide for channel legends versus chart-level `configure_legend()`.
- Blank chart after serialization: inspect browser errors/resources and fields/
  domains. Do not disable validation.
- Local files cannot open: use the tool's supported preview. If appropriate and
  permitted, serve only the output directory on loopback, not the repo or inputs.
- Image download fails: retain working HTML and use a screenshot if supported.
  Bound export waits; report export and hover failures separately from rendering.
  Stop editing once the requested checks pass.
