"""Small supplied profiles covering Scanpy's three time-series point modes."""

import numpy as np


def timeseries_cases():
    """Return detached profiles/options with unsorted times, missing values and guides."""
    values = np.array([[0.5, 5], [1, 4], [4, 1], [7, -2]], dtype=float)
    time = np.array([3.0, 1.0, 1.0, -2.0])
    return {
        "multiple": (values, {"time": time, "var_names": ["A", "B"]}),
        "highlights": (
            values,
            {
                "time": time,
                "highlights_x": [-6.0, 8.0],
                "yticks": [-10.0, 10.0],
                "xlabel": "Time",
                "ylabel": "Supplied value",
            },
        ),
        "limits": (
            values,
            {
                "xlim": [4.0, -1.0],
                "highlights_x": [-6.0, 8.0],
                "marker": "o",
                "palette": ["red", "blue"],
            },
        ),
        "categorical": (
            values[:, 0],
            {
                "time": time,
                "color": np.array(["b", "a", "b", "a"]),
                "var_names": ["first", "second"],
                "marker": "s",
            },
        ),
        "integer_groups": (
            values[:, 0],
            {"color": np.array([2, 1, 2, 1]), "var_names": ["one", "two"]},
        ),
        "mixed_integer_first": (
            values[:, 0],
            {"color": [2, 1.0, 2.0, 1], "var_names": ["one", "two"]},
        ),
        "continuous": (
            values[:, 0],
            {
                "time": time,
                "color": np.array([0.1, 0.8, 0.5, 0.3]),
                "var_names": ["value"],
                "marker": "o",
            },
        ),
        "missing": (
            np.array([0.5, np.nan, 4.0, 7.0]),
            {"time": time, "color": np.array([0.1, 0.8, np.nan, 0.3])},
        ),
        "masked_legend_key": (
            np.array([np.nan, 1.0, 4.0, 7.0]),
            {"color": np.array([0.1, 0.8, 0.5, 0.3]), "var_names": ["masked first"]},
        ),
        "constant": (
            values[:, 0],
            {"color": np.full(4, 0.4), "var_names": ["constant"], "marker": "D"},
        ),
        "singleton": (
            np.array([[2.0, 3.0]]),
            {"time": np.array([4.0]), "var_names": ["A", "B"]},
        ),
    }
