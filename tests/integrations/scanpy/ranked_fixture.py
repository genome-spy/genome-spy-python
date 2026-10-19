"""Hand-specified rankings over existing test profiles; no differential analysis."""

import numpy as np

from tests.integrations.scanpy.dendrogram_fixture import make_tree_adata


def make_ranked_adata():
    """Return four expression groups with intentionally repeated top-ranked genes."""
    a = make_tree_adata()
    a.var["symbol"] = ["S1", "S2", "S3", "S4"]
    a.raw = a.copy()
    a.layers["counts"] = a.X * 3
    a.varm["PCs"] = np.array([[4, 1], [2, 2], [8, 3], [6, 4]])
    a.uns["provided"] = {"score_name": np.array([1.0, 4.0, 2.0, 8.0, 3.0, 7.0])}
    groups = ["C", "A", "D", "B"]
    names = [
        ["g2", "g1", "g3", "g4"],
        ["g2", "g4", "g1", "g3"],
        ["g3", "g1", "g4", "g2"],
        ["g4", "g3", "g2", "g1"],
    ]
    result = {
        "params": {
            "groupby": "group",
            "method": "t-test",
            "reference": "rest",
            "use_raw": True,
        }
    }
    for metric, rows in {
        "names": names,
        "scores": [[4.0, 2, 1, -3], [6.0, 3, 0, -2], [5.0, 2, 0, -1], [8.0, 2, 1, -4]],
        "logfoldchanges": [[2.0, 1, 0.5, -1]] * 4,
        "pvals": [[0.001, 0.02, 0.4, 0.8]] * 4,
        "pvals_adj": [[0.004, 0.04, 0.6, 0.9]] * 4,
    }.items():
        result[metric] = np.rec.fromarrays(rows, names=groups)
    a.uns["rank_genes_groups"] = result
    return a


def ranked_cases():
    """Return plain chart cases shared by the reference and browser checks."""
    return {
        "genes_shared": (
            "rank_genes_groups",
            (["A", "C"],),
            {"n_genes": 3, "ncols": 2},
        ),
        "genes_independent": (
            "rank_genes_groups",
            (["A", "C"],),
            {"n_genes": 3, "ncols": 2, "sharey": False},
        ),
        "attribute_top": (
            "ranking",
            ("uns", "score_name"),
            {"dictionary": "provided", "labels": "L", "n_points": 2, "log": True},
        ),
        "attribute_extremes": (
            "ranking",
            ("varm", "PCs"),
            {"indices": [1, 0], "n_points": 2, "include_lowest": True},
        ),
    }
