# Reference Repo Index

| Repo | Role | What to Read First |
|---|---|---|
| `tmp/altair` | Canonical Python wrapper around a JS visualization grammar | `README.md`, `altair/vegalite/v6/api.py`, `altair/jupyter/jupyter_chart.py`, `altair/utils/schemapi.py` |
| `tmp/gos` | Closest genomics-specific Python wrapper precedent | `README.md`, `gosling/api.py`, `gosling/_widget.py`, `tools/generate_schema_wrapper.py` |
| `tmp/vega-lite` | Upstream grammar and schema source that Altair wraps | `src/index.ts`, relevant schema and encoding files under `src/` |
| `tmp/gosling.js` | Upstream Gosling JS library wrapped by `gos` | `src/index.ts`, compiler/api docs under `src/` |
| `tmp/genome-spy` | Upstream target library for this project | `README.md`, `packages/core/README.md`, `packages/app/README.md`, package schemas and spec types |
| `tmp/anywidget` | Notebook widget toolkit for Python packages | `README.md`, `packages/anywidget/src/`, examples in docs |
| `tmp/dataviz-genomicsdata` | Broad Python genomics-visualization course, deterministic example datasets, and future gallery inspiration | `README.md`, `genomics_course/genomics_course/data/`, `day1/sections/`, `day2/sections/`, `day3/sections/` |
| `tmp/ggwas` | Focused GWAS plot gallery and composable R/ggplot2 design reference | `README.md`, `R/manhattan-plot.R`, `R/qq-plot.R`, `R/locus-plot.R`, `R/gene-track.R`, `R/downsample.R` |
| `tmp/maftools` | Primary cancer-genomics example source with real TCGA MAF/CNV/cohort data and explicit plot semantics in the `.Rd` docs | `inst/extdata/`, `man/oncoplot.Rd`, `man/rainfallPlot.Rd`, `man/lollipopPlot.Rd`, `man/tcgaCompare.Rd`, `man/plotCBSsegments.Rd` |
| `tmp/mutglyph` | GenomeSpy-based R reference for mutation-plot callouts and generic scored genomic annotation tracks | `vignettes/gene-annotations.Rmd`, `vignettes/rainfall-plots.Rmd`, `vignettes/gistic-plots.Rmd`, `R/annotation-views.R`, `R/rainfall-spec.R`, `R/gistic-spec.R` |
| `tmp/pyGenomeTracks` | Track-layout reference for browser-style genomics views, including signal, genes, Hi-C, and matrix examples | `examples/`, especially `bigwig_with_genes.ini`, `hic_track.ini`, and `bedgraph_matrix*.ini` |
| `tmp/pyGenomeViz` | Comparative-genomics and link-layout reference, especially for conserved-block or fastANI-style cross-genome views | `notebooks/fastANI/README.md`, `notebooks/fastANI/visualize.py` |

## Working Conclusions

- Altair demonstrates the cleanest separation between generated schema bindings,
  handwritten API ergonomics, serialization helpers, and notebook rendering.
- `gos` confirms that the Altair pattern works well for a genomics-oriented
  grammar and shows a compact anywidget-based rendering bridge.
- GenomeSpy itself is split into a reusable `core` package and a richer `app`
  package, which matches the intended incremental rollout for this repo.
- `anywidget` is suitable for notebook rendering and can keep the Python-side
  widget implementation relatively small.
- `dataviz-genomicsdata` provides a useful visual syllabus rather than an API
  architecture: its genomics examples can seed documentation examples while
  the Python computations that prepare data remain outside GenomeSpy's core.
- `ggwas` is a strong source for GWAS-specific chart composition, defaults, and
  large-data strategies. It should guide examples first; convenience APIs such
  as format detection, annotation, and downsampling should be evaluated
  separately rather than copied into the core grammar wrapper.
- `maftools` is the strongest current source for realistic cancer-genomics
  gallery work: its bundled extdata and `.Rd` files jointly define candidate
  oncoplots, rainfall plots, mutation burden bars, lollipop plots, and CNV
  segment views without inventing synthetic cohorts.
- `MutGlyph` demonstrates that callouts and gene tracks can remain ordinary
  composable GenomeSpy layers: point annotations use explicit target and label
  positions, while interval-track label scores control layout priority only.
- `pyGenomeTracks` is best used as a composition and data-shape reference rather
  than a direct dependency. Its bigWig and Hi-C examples reinforce that lazy or
  indexed data loaders are the main blocker for truly browser-native track
  examples.
- `pyGenomeViz`'s fastANI notebook is a strong future reference for GenomeSpy
  `link`-based comparative-genomics views: two aligned coordinate systems plus
  colored cross-track links.
