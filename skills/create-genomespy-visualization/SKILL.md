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

## Find a working pattern through the index

1. Read [llms.txt](https://genomespy.app/genome-spy-python/llms.txt) at the start of
   the task. Use its descriptions and gallery categories to select pages; retain
   the index and selected URLs for the task instead of repeatedly downloading them.
   Follow listed Markdown URLs rather than guessing endpoints.
   Titles can repeat across agent and user-guide sections; keep entries distinct
   by section and URL, and prefer the focused agent guide before the fuller page.
2. Select the closest gallery example by the intended comparison, marks,
   composition, and interaction, rather than just its sample dataset. Read its
   Python source and explanation before authoring. Load only the selected example
   and needed guides, not the entire documentation collection.
   A related example can supply summary and ordering patterns while a documented
   native mark supplies the requested chart form. Reuse only needed components.
3. Adapt the example's public chart API, encodings, composition, and rendering
   path. Replace example data, field names, labels, and domains with the user's
   inputs. Check dependencies, preparation, and provenance; use public data APIs
   rather than copying internal dataset helpers or assuming prepared fields exist.
   For recreation, check example-specific palettes, opacity, zoom-dependent mark
   sizes, and panel dimensions against the frozen reference before retaining them.
4. Resolve missing detail with the indexed pages below. Prefer focused agent
   guides; use the fuller user guides or API signatures for unresolved options.
   If no example fits, use documented native marks and transforms. If the requested
   chart form is unsupported, explain the gap and offer a supported alternative.
   Implement custom geometry only when the user explicitly requests it; label it
   as custom and keep its recipes in task-local code, outside this skill.
   Keep native guides attached to their encodings whenever supported.

| Need | Find in the index |
| --- | --- |
| Minimal chart or delivery workflow | Quickstart; Notebooks and export |
| Table formats, indexes, or prepared fields | Data inputs; Data and chart inputs |
| Fields, types, or channel mappings | Encodings and composition; Encodings and channels |
| Domains, color/size mappings, axes, or legends | Scales, axes, and legends |
| Filtering, derived fields, or aggregation | Transforms |
| Layers, panels, or shared scales | Composition; Chart authoring signatures |
| Notebook interaction or HTML output | Charts in notebooks; Save, export, and share charts |
| Unfamiliar Python options | Python API signatures and the relevant API details page |

Check installed public signatures/docstrings before using unfamiliar options.
If an option is unavailable, prefer matching checkout docs and installed APIs;
do not treat an online example as proof that the installed version supports it.

For recreation, read the bundled [table-chart guide](references/table-chart.md)
for geometry, marker footprints, overlays, and color checks. For grouped
summaries or matrices, read
[grouped charts](references/grouped-charts.md). Load these when relevant.

If the index is unavailable, try the direct [gallery catalog](https://genomespy.app/genome-spy-python/agents/gallery.md)
or [quickstart](https://genomespy.app/genome-spy-python/agents/quickstart.md).
If online pages also fail, use matching local docs or the self-contained bundled
references and report the access limit. The checkout quickstart is
`docs/agents/quickstart.md`; bundled references also work outside this repository.

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
  plot-area dimensions first. Preserve data selection, measurement source, order,
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
   In composed charts, verify which panels should zoom together and which color
   scales should remain independent; observe the interaction when tools support it.
4. Deliver reusable source and the artifact with a brief processing/check report.
   Link the example or guides reused and explain material departures.
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
