"""Load and reshape the curated PBMC marker subset for gallery examples."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from genome_spy.datasets import load_dataset

if TYPE_CHECKING:
    import pandas as pd
    from anndata import AnnData


def pbmc_markers(*, umap_genes: bool = False) -> AnnData:
    """Load the prepared PBMC marker expression as AnnData.

    Description:
        By default, contains 2,638 cells and 12 marker genes with saved log1p counts,
        original cell-type labels, UMAP coordinates, and a stable group ordering.

    Args:
        umap_genes: Load the six UMAP-panel markers instead of the twelve heatmap markers.

    Returns:
        A new AnnData object with cell identifiers and plotting coordinates in obs.

    Raises:
        ImportError: If the optional anndata package is not installed.

    Example:
        >>> adata = pbmc_markers()
        >>> adata.shape
        (2638, 12)
    """
    import numpy as np
    import pandas as pd
    from anndata import AnnData

    data = load_dataset("pbmc_markers", as_format="json")
    assert isinstance(data, dict)
    obs = pd.DataFrame.from_records(data["cells"]).set_index("cell", drop=False)
    obs["cell_end"] = obs["cell_order"] + 1
    genes = (
        data["umap_genes"]
        if umap_genes
        else [marker["gene"] for marker in data["markers"]]
    )
    return AnnData(
        X=np.asarray(
            data["umap_expression"] if umap_genes else data["expression"],
            dtype=np.float32,
        ),
        obs=obs,
        var=pd.DataFrame(index=genes),
        obsm={"X_umap": np.asarray(data["umap"], dtype=np.float64)},
    )


def expression_table(projection: pd.DataFrame, genes: Sequence[str]) -> pd.DataFrame:
    """Reshape a selected PBMC AnnData projection into expression tiles.

    Description:
        Keeps cell identifiers, annotations and interval coordinates alongside
        each gene value. This reshape runs in Python before rendering.

    Args:
        projection: Output of from_anndata with cell, cell_type, cell_order and cell_end.
        genes: Selected genes in plotting order.

    Returns:
        One row per cell and gene, with marker_order and expression columns.

    Raises:
        KeyError: If a requested column is absent.

    Example:
        >>> table = expression_table(projection, ["IL7R", "CD14"])
    """
    table = projection.melt(
        id_vars=["cell", "cell_type", "cell_order", "cell_end"],
        value_vars=list(genes),
        var_name="gene",
        value_name="expression",
    )
    table["marker_order"] = table["gene"].map(dict(zip(genes, range(len(genes)))))
    return table
