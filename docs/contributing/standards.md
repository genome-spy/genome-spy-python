---
orphan: true
---

# Repository language and gallery standards

These requirements supplement `AGENTS.md`. Read the language sections for Python
changes and the gallery section for documentation examples.

## Python conventions

- Type hints on all public APIs
- Use `list[T]`, `dict[K, V]`, `X | Y` — never `typing.List`, `Optional`
- `src/` layout; explicit `__all__` on public packages
- Protocols (PEP 544) over ABCs for structural typing
- `@dataclass(frozen=True, slots=True)` for value objects
- `pathlib` for paths; `os` for env vars only
- Prefer functions over single-use classes
- Fail fast: custom exceptions with contextual messages; zero silent failures
- `logging.getLogger(__name__)` — never `print()` or `logging.basicConfig()`
- Explicit imports and predictable control flow over cleverness; no package-level magic re-exports
- Keep modules small and names descriptive.

## Docstrings

Use Google-style docstrings for every public API via `sphinx.ext.napoleon`.
Types belong in signatures only and should not be repeated in docstrings.

Required public API sections:

- Summary
- Description
- Args
- Returns
- Raises
- Example

## Documentation gallery

- Write user-facing guides for first-time users. Use plain words, short sentences,
  and short paragraphs. Avoid jargon and tangents. Keep only what helps readers
  understand or use the example. Link to references for advanced details.
- Keep documentation examples focused on the GenomeSpy visualization API, not
  statistical analysis or general-purpose data wrangling. Prepare derived
  example datasets, including p-values, adjusted p-values, transformed values,
  classifications, and plotting domains, in `src/genome_spy/datasets/` or in
  curated packaged data files. Examples should load the prepared table and
  demonstrate encodings, marks, transforms, and composition directly.
- Prefer Altair-style composition operators in examples when they express the
  intended structure clearly: `+` for layers, `&` for vertical concatenation,
  and `|` for horizontal concatenation.
- Documentation gallery embeds must use the direct static GenomeSpy bundle
  import followed by `embed(c, spec, { bare: true })`. Keep the chart container
  direct and avoid transform or resize wrappers around the embedded canvas;
  this is the known-working path for all gallery plots, including sashimi.
- Keep adapted gallery pages self-contained. Link the corresponding official
  GenomeSpy example as further reading, not as a substitute for local
  explanation.
- Put extended prose in an optional same-stem Markdown companion under
  `docs/examples/`.
- For the same data and processing, reuse the official GenomeSpy example's
  concise provenance or disclaimer wording. Update it when the sample, region,
  subset, preprocessing, or intended use differs.
- Keep provenance as brief as possible. Include only details needed to identify
  the data, disclose material processing, satisfy attribution or licensing, or
  prevent misuse. Use a note-styled admonition titled `Data use and
  provenance`; do not repeat it as a section heading.
- Adapt `What to notice` and implementation prose to the chart actually
  rendered. Verify every claim about data, encodings, transforms, interaction,
  and composition against the checked-in Python source.
- Explicitly distinguish processing performed in Python from GenomeSpy's
  browser-side dataflow. State whether an example loads a prepared packaged
  table, derives or filters data in Python, or sends data to GenomeSpy for
  declarative transforms.
- Do not describe packaged derived data as raw source data or imply that
  `.transform_*()` methods execute in Python. The Python API authors and
  serializes those transform definitions; GenomeSpy executes them while
  rendering or interacting with the visualization in the browser.
