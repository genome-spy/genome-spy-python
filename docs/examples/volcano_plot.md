:::{admonition} Data use and provenance
:class: note

The packaged table is a subset of HapMap variants from the MIT-licensed
[manhattanly](https://github.com/cran/manhattanly) and
[Plotly datasets](https://github.com/plotly/datasets/blob/master/Dash_Bio/Chromosomal/manhattan_data.csv)
projects. The association p-values and effect sizes are simulated, so the plot
is for visualization demonstration only. During data loading, the package
calculates `-log10(p)` and classifies points using the displayed thresholds.
GenomeSpy then renders the prepared table.
:::
