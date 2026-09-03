:::{admonition} Data use and provenance
:class: note

The packaged table is a subset of HapMap variants from the MIT-licensed
[manhattanly](https://github.com/cran/manhattanly) and
[Plotly datasets](https://github.com/plotly/datasets/blob/master/Dash_Bio/Chromosomal/manhattan_data.csv)
projects. Genomic coordinates and annotations are real, but the association
statistics are simulated and are not biological findings. During data loading,
the package removes invalid p-values and calculates `-log10(p)`. GenomeSpy then
renders the prepared table.
:::

## What to notice

Drag across the whole-genome overview to choose the region shown by all three
detail tracks. Association strength, effect size, and Z-score share one locus
scale but keep independent y scales. Zooming or panning a detail track also
updates the overview brush.

## Python implementation

The outer composition declares an empty `brush` parameter. The nested detail
group uses it as the domain of its shared x scale. The overview declares the
interval selection with the same name and `push="outer"`, which writes gestures
back to the outer parameter. An excluded x-scale resolution keeps the overview
on the full genome instead of shrinking it to the selected detail interval.

Python loads the prepared packaged table and authors the selection and scale
definitions. GenomeSpy executes the interaction and updates the linked scales
in the browser. See the user guide's
[overview-brush walkthrough](../user-guide/interaction.md)
and GenomeSpy's documentation on
[interval selections](https://genomespy.app/docs/grammar/parameters/#interval-selection)
and
[selection-driven scale domains](https://genomespy.app/docs/grammar/scale/#domain-from-selection-parameters).
