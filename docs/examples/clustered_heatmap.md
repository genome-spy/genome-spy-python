Rows show 60 cancer cell lines and columns show 72 genes. Red indicates
expression above a gene's mean and blue indicates expression below its mean.
The z-score color scale saturates at ±2.5; tooltips retain the full values and
also show reconstructed log2(TPM + 1) expression.

## What to notice

The trees group similar expression profiles. Branch colors and gaps mark four
row groups and six gene groups. The strips at the right show cancer lineage,
growth pattern, and primary/metastatic sample origin. Gray origin cells mean
unknown values.

Pan and zoom to inspect the matrix. Both trees stay aligned with their leaves,
and their merge-height scales fit branches contained in the visible range.
Hover over a cell for its gene, cell-line metadata, and expression values.

## How the chart is built

Python authors the specification and provides URLs for prepared tables and
clustering trees; it does not compute clusters or load the tables. GenomeSpy
unfolds the wide expression table with `transform_regex_fold()` and joins the
metadata with `transform_lookup()` in the browser. `transform_dendrogram()`
converts the supplied node hierarchies into orthogonal link endpoints.

`gs.surround()` places the gene tree above the matrix, the cell-line tree to its
left, and a `gs.SurroundSideSpec` with annotation strips and labels to its right.
Shared index scales align each side with the matrix. Fractional dendrogram
offsets use `bandstep()` to stay connected across gaps while zooming. The
trees' independent height scales use `gs.ViewportDomainRef(mode="contain")`.

See the [official GenomeSpy example](https://genomespy.app/docs/examples/generic/clustered-heatmap/)
for the original JSON specification and data preparation guide.

:::{admonition} Data use and provenance
:class: note

Data: Broad DepMap (2024),
[DepMap 24Q4 Public](https://doi.org/10.25452/figshare.plus.27993248.v1),
licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
GenomeSpy hosts a processed demonstration subset of 60 cell lines and
72 protein-coding genes, with gene-wise standardization, computed Ward
trees, and extracted cell-line annotations. The
[reproducible recipe](https://github.com/genome-spy/genomespy-dataset-recipes/tree/875ca57dd130bdc2f9777ed63939e49042233f32/recipes/depmap-cell-line-rna-seq/)
records selection and processing; the
[data notice](https://data.genomespy.app/datasets/depmap-cell-line-rna-seq/v1/NOTICE.txt)
accompanies the mirrored extract.
:::
