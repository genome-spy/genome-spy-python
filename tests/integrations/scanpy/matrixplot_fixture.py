"""Original matrixplot cases on the shared hand-sized grouped input."""

from typing import Any


def matrixplot_cases() -> dict[str, dict[str, Any]]:
    import pandas as pd

    supplied = pd.DataFrame(
        [[4, 8, 2], [8, 2, 6]], index=["A", "B"], columns=["g3", "g1", "g2"]
    )
    return {
        "default": {},
        "reordered": {"categories_order": ["A", "B"]},
        "log": {"log": True},
        "scaled_var": {"standard_scale": "var"},
        "scaled_group": {"standard_scale": "group"},
        "swapped_scaled": {"swap_axes": True, "standard_scale": "var"},
        "supplied": {"values_df": supplied},
        "supplied_scaled": {
            "values_df": supplied,
            "standard_scale": "var",
            "log": True,
        },
        "supplied_reordered": {
            "values_df": supplied,
            "categories_order": ["B", "A"],
            "swap_axes": True,
        },
        "repeated": {"var_names": {"first": ["g2", "g1"], "again": "g2"}},
        "constant": {
            "values_df": pd.DataFrame(4.0, index=["B", "A"], columns=["g1", "g2", "g3"])
        },
        "missing": {"values_df": supplied.mask(supplied == 8)},
        "bounds_edges": {
            "vmin": 1,
            "vmax": 3,
            "edgecolor": "black",
            "linewidth": 1.5,
        },
    }
