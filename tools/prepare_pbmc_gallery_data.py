"""Prepare the PBMC marker subset: uv run python tools/prepare_pbmc_gallery_data.py.

Download SOURCE_URL to tmp/pbmc/pbmc3k.h5ad first. Scanpy's processed fixture
stores log1p counts in .raw, before normalization, regression and scaling.
"""

from __future__ import annotations

import gzip
import json
from hashlib import sha256
from importlib.metadata import version
from pathlib import Path

import anndata as ad
import numpy as np
from scipy.cluster.hierarchy import leaves_list, linkage

ROOT = Path(__file__).resolve().parents[1]
SOURCE_URL = "https://raw.githubusercontent.com/chanzuckerberg/cellxgene/68dfbcc2eb675e96c6a5e2a6b7a0d3465ccf46bc/example-dataset/pbmc3k.h5ad"
SOURCE_SHA256 = "0db367b991dd95809732b218539ede489bea99113807f62ebd7ccc970025fe38"
MARKERS = {
    "CD4 T cells": ["IL7R"],
    "CD14+ Monocytes": ["CD14", "LYZ"],
    "B cells": ["MS4A1"],
    "CD8 T cells": ["CD8A"],
    "NK cells": ["GNLY", "NKG7"],
    "FCGR3A+ Monocytes": ["FCGR3A", "MS4A7"],
    "Dendritic cells": ["FCER1A", "CST3"],
    "Megakaryocytes": ["PPBP"],
}
COLORS = [
    "#568564",
    "#DC6B19",
    "#F72464",
    "#005585",
    "#9876DE",
    "#405559",
    "#36B8B8",
    "#F85959",
]


def main() -> None:
    """Write a deterministic, marker-only bundle from the pinned source."""
    source = ROOT / "tmp/pbmc/pbmc3k.h5ad"
    if sha256(source.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise ValueError("PBMC source checksum differs from the pinned fixture.")
    original = ad.read_h5ad(source)
    genes = [gene for markers in MARKERS.values() for gene in markers]
    # Select only 12 columns before densifying the sparse saved matrix.
    selected = original.raw[:, genes].to_adata()
    values = selected.X.toarray()
    input_groups = list(MARKERS)
    labels = selected.obs["louvain"].to_numpy()
    profiles = np.vstack(
        [
            values[labels == group].mean(axis=0, dtype=np.float64)
            for group in input_groups
        ]
    )
    # Marsilea 0.3.5 clusters group means with single linkage / Euclidean distance.
    tree = linkage(
        profiles, method="single", metric="euclidean", optimal_ordering=False
    )
    group_order = [input_groups[int(i)] for i in leaves_list(tree)]
    palette = dict(zip(input_groups, COLORS, strict=True))
    order = np.concatenate(
        [
            np.flatnonzero(original.obs["louvain"].to_numpy() == group)
            for group in group_order
        ]
    )
    selected = selected[order].copy()
    values = selected.X.toarray()
    if values.shape != (2638, 12) or not np.isfinite(values).all() or values.min() < 0:
        raise ValueError("Unexpected PBMC marker matrix.")
    cells = [
        {"cell": str(cell), "cell_type": str(group), "cell_order": i}
        for i, (cell, group) in enumerate(
            zip(selected.obs_names, selected.obs["louvain"], strict=True)
        )
    ]
    groups, means, markers = [], [], []
    start = 0
    for row, group in enumerate(group_order):
        count = int((selected.obs["louvain"] == group).sum())
        end = start + count
        groups.append(
            {
                "cell_type": group,
                "group_order": row,
                "row_start": row - 0.5,
                "row_end": row + 0.5,
                "count": count,
                "start": start,
                "end": end,
                "center": (start + end) / 2,
                "color": palette[group],
            }
        )
        for column, gene in enumerate(genes):
            means.append(
                {
                    "cell_type": group,
                    "group_order": row,
                    "row_start": row - 0.5,
                    "row_end": row + 0.5,
                    "gene": gene,
                    "marker_order": column,
                    "mean_expression": float(
                        values[start:end, column].mean(dtype=np.float64)
                    ),
                }
            )
        start = end
    for column, gene in enumerate(genes):
        target = next(group for group, names in MARKERS.items() if gene in names)
        markers.append(
            {
                "gene": gene,
                "marker_order": column,
                "cell_type": target,
                "expression_limit": int(np.ceil(values[:, column].max())),
            }
        )
    marker_groups = [
        {
            "cell_type": group,
            "start_gene": names[0],
            "end_gene": names[-1],
            "start": genes.index(names[0]),
            "end": genes.index(names[-1]) + 1,
            "center": (genes.index(names[0]) + genes.index(names[-1]) + 1) / 2,
            "label_color": "#173238" if group == "Dendritic cells" else "white",
        }
        for group, names in MARKERS.items()
    ]
    # Each merge has two arms and one connector. Use equal group rows for the
    # matrix and actual cell-group centers for the heatmap / expression tracks.
    positions = {
        input_groups.index(group["cell_type"]): (
            float(group["group_order"]),
            group["center"],
            0.0,
        )
        for group in groups
    }
    segments = []
    for merge, (left, right, height, _) in enumerate(tree):
        a, b = positions[int(left)], positions[int(right)]
        for row, cell, distance in (a, b):
            segments.append(
                {
                    "distance": distance,
                    "distance_end": float(height),
                    "row": row,
                    "row_end": row,
                    "cell": cell,
                    "cell_end": cell,
                }
            )
        segments.append(
            {
                "distance": float(height),
                "distance_end": float(height),
                "row": a[0],
                "row_end": b[0],
                "cell": a[1],
                "cell_end": b[1],
            }
        )
        positions[len(input_groups) + merge] = (
            (a[0] + b[0]) / 2,
            (a[1] + b[1]) / 2,
            float(height),
        )
    bundle = {
        "source": {
            "url": SOURCE_URL,
            "sha256": SOURCE_SHA256,
            "expression": "raw.X: log1p counts before normalization",
            "processing": "12 markers; original louvain labels; dendrogram group order; stable cells within groups",
            "license": "CC-BY-4.0",
            "anndata_version": version("anndata"),
        },
        "cells": cells,
        "expression": values.tolist(),
        "groups": groups,
        "markers": markers,
        "marker_groups": marker_groups,
        "marker_domain": [0, len(genes)],
        "means": means,
        "group_domain": [-0.5, len(groups) - 0.5],
        "group_tree": segments,
        "dendrogram": {
            "features": genes,
            "input_groups": input_groups,
            "method": "single",
            "metric": "euclidean",
            "optimal_ordering": False,
            "linkage": tree.tolist(),
            "group_order": group_order,
            "distance_limit": float(tree[-1, 2] * 1.08),
            "scipy_version": version("scipy"),
        },
        "expression_limit": int(np.ceil(values.max())),
        "mean_expression_limit": int(
            np.ceil(max(row["mean_expression"] for row in means))
        ),
        "count_limit": int(
            np.ceil(max(group["count"] for group in groups) / 100) * 100
        ),
    }
    payload = json.dumps(bundle, separators=(",", ":"), allow_nan=False).encode()
    (ROOT / "src/genome_spy/datasets/data/pbmc_markers.json.gz").write_bytes(
        gzip.compress(payload, mtime=0)
    )


if __name__ == "__main__":
    main()
