"""Original dotplot reference cases; extend the hand-sized grouped input."""

from typing import Any


def dotplot_cases() -> dict[str, dict[str, Any]]:
    import pandas as pd

    cases = {
        "default": {},
        "reordered": {"categories_order": ["A", "B"]},
        "log": {"log": True, "expression_cutoff": 0.8},
        "expressed": {"mean_only_expressed": True, "expression_cutoff": 1},
        "scaled": {"standard_scale": "var"},
        "swapped_scaled": {"swap_axes": True, "standard_scale": "group"},
        "supplied": {
            "dot_color_df": pd.DataFrame(
                [[4, 8, 2], [8, 2, 6]], index=["A", "B"], columns=["g3", "g1", "g2"]
            )
        },
        "supplied_scaled": {
            "standard_scale": "var",
            "dot_color_df": pd.DataFrame(
                [[4, 8, 2], [8, 2, 6]], index=["A", "B"], columns=["g3", "g1", "g2"]
            ),
        },
        "clipped": {"dot_min": 0.4, "dot_max": 0.8, "smallest_dot": 10},
        "repeated": {"var_names": {"first": ["g2", "g1"], "again": "g2"}},
        "constant_colors": {
            "dot_color_df": pd.DataFrame(
                4.0, index=["B", "A"], columns=["g1", "g2", "g3"]
            )
        },
    }
    # Viridis shares a published palette; native reds uses different Vega stops.
    return {name: {"cmap": "viridis", **options} for name, options in cases.items()}
