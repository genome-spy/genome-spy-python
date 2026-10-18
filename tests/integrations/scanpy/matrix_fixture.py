"""Original small numeric matrices for Scanpy's direct matrix helper (MIT)."""

import numpy as np


def matrix_cases():
    base = np.array([[-2.0, 0, 2], [1, 3, 5]])
    labels = {
        "xticks": ["gene A", "B", "B"],
        "yticks": ["group 2", "group 1"],
        "xlabel": "Genes",
        "ylabel": "Groups",
        "title": "Supplied values",
    }
    return {
        "default": (base, {}),
        "labels": (base, labels),
        "constant": (np.full((2, 3), 7.0), labels),
        "zero": (np.zeros((2, 3)), {}),
        "missing": (np.array([[np.nan, 0, 2], [1, 3, 5]]), labels),
        "masked": (np.ma.array(base, mask=[[0, 1, 0], [1, 0, 0]]), labels),
        "row": (base[:1], {"colorbar_shrink": 0.8}),
        "column": (base[:, :1], {"colorbar_shrink": 0.25}),
    }
