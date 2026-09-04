Move the **−log10 p cutoff** slider to change the red significance line. Points
above the line turn red immediately; a higher cutoff is stricter. GenomeSpy
updates the rule and highlighted set in the browser.

:::{admonition} Data use and provenance
:class: note

The packaged table is a subset of HapMap variants from the MIT-licensed
[manhattanly](https://github.com/cran/manhattanly) and
[Plotly datasets](https://github.com/plotly/datasets/blob/master/Dash_Bio/Chromosomal/manhattan_data.csv)
projects. Genomic coordinates and annotations are real, but the association
statistics are simulated and are not biological findings. During data loading,
the package removes invalid p-values and calculates `-log10(p)`. GenomeSpy then
renders the prepared table and applies the interactive threshold in the browser.
:::
