"""Pure supplied-profile preparation for Scanpy time-series points."""

from collections.abc import Collection, Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from genome_spy.integrations.scanpy._data import (
    coordinate_domain,
    matrix_array,
    number,
    numeric_values,
)
from genome_spy.integrations.scanpy._style import color_bounds, native_color

CONTEXT = "gsc.pl.timeseries"


@dataclass(frozen=True, slots=True)
class TimeseriesData:
    table: pd.DataFrame
    x_domain: tuple[float, float]
    y_domain: tuple[float, float]
    palette: tuple[str, ...]
    color_domain: tuple[float, float] | None
    legend: bool
    yticks: tuple[float, ...] | None
    highlight_y: tuple[float, float]


def _vector(
    values: Any, name: str, count: int | None = None, *, context: str = CONTEXT
) -> pd.Series:
    """Return a resident positional vector, rejecting lazy inputs and wrong lengths."""
    if (
        not isinstance(values, (np.ndarray, pd.Series, pd.Index, list, tuple))
        or np.ndim(values) != 1
    ):
        raise TypeError(f"{context}: {name} must be a resident one-dimensional vector.")
    if count is not None and len(values) != count:
        raise ValueError(f"{context}: {name} must contain {count} values.")
    return pd.Series(values).reset_index(drop=True)


def prepare_timeseries(
    X: Any,
    *,
    time: Any,
    color: Any,
    var_names: Collection[str],
    highlights_x: Any,
    xlim: Any,
    yticks: Any,
    palette: Any,
    legend: bool,
    context: str = CONTEXT,
) -> tuple[TimeseriesData, list[float]]:
    """Return detached points, initial limits and highlights without sorting samples or analysis."""
    array = matrix_array(X, context=context, allow_vector=True)
    values = numeric_values(pd.DataFrame(array), context=context)
    rows, columns = values.shape
    times = (
        np.arange(rows, dtype=float)
        if time is None
        else numeric_values(
            _vector(time, "time", rows, context=context).to_frame(), context=context
        ).ravel()
    )
    continuous = False
    # Multiple variables retain column order; categories sort only in the single-variable case.
    if columns > 1:
        sample = np.tile(np.arange(rows), columns)
        subset = np.repeat(np.arange(columns), rows)
        plotted = values.T.ravel()
        count = columns
        fallback = [str(i) for i in range(count)]
        colors = None
    else:
        if color is None:
            raise ValueError(
                f"{context}: one variable requires color, as in Scanpy's helper."
            )
        source = _vector(color, "color", rows, context=context)
        # Check the supplied type before pandas promotes mixed integer/float lists.
        first_color = color.iloc[0] if isinstance(color, pd.Series) else color[0]
        continuous = isinstance(first_color, (float, np.floating))
        if continuous:
            colors = numeric_values(source.to_frame(), context=context).ravel()
            sample, subset = np.arange(rows), np.zeros(rows, dtype=int)
            count, fallback = 1, ["0"]
        else:
            if source.isna().any():
                raise ValueError(
                    f"{context}: categorical color cannot contain missing values."
                )
            try:
                levels, inverse = np.unique(source.to_numpy(), return_inverse=True)
            except TypeError as error:
                raise TypeError(
                    f"{context}: categorical color values must have a common sortable type."
                ) from error
            # Scanpy draws sorted categories, retaining sample order inside each one.
            sample = np.argsort(inverse, kind="stable")
            subset = inverse[sample]
            count, fallback = len(levels), [str(level) for level in levels]
            colors = None
        plotted = values[sample, 0]
    if isinstance(var_names, (str, bytes)) or not isinstance(var_names, Collection):
        raise TypeError(f"{context}: var_names must be a collection of labels.")
    names = list(var_names)
    if names and (len(names) < count or any(not isinstance(v, str) for v in names)):
        raise ValueError(f"{context}: var_names needs at least {count} string labels.")
    labels = names[:count] if names else fallback
    if len(set(labels)) != len(labels):
        raise NotImplementedError(
            f"{context}: repeated series labels are unsupported; use distinct var_names."
        )
    selected: tuple[str, ...] = ()
    if not continuous:
        if palette is None:
            import scanpy as sc

            palette = sc.pl.palettes.vega_10
        if isinstance(palette, str) or not isinstance(palette, (Sequence, np.ndarray)):
            raise NotImplementedError(
                f"{context}: palette requires a sequence of CSS colors; cyclers are unsupported."
            )
        if len(palette) < count:
            raise ValueError(f"{context}: palette needs at least {count} colors.")
        selected = tuple(
            native_color(c, "palette", context=context) for c in palette[:count]
        )
    table = pd.DataFrame(
        {
            "_sample": sample,
            "_time": times[sample],
            "_value": plotted,
            "_series": np.asarray(labels)[subset],
            "_id": sample * columns + (subset if columns > 1 else 0),
        }
    )
    valid = np.isfinite(table["_time"]) & np.isfinite(plotted)
    domain = None
    if colors is not None:
        table["_color"] = colors
        valid &= np.isfinite(colors)
        low, high, _ = color_bounds(
            colors[valid], None, None, context=context, expand_constant=False
        )
        domain = (low, high)
    if not valid.any():
        raise ValueError(
            f"{context}: at least one point needs finite time, value and color."
        )
    highlights = [
        number(v, "highlights_x", context=context, minimum=-np.inf)
        for v in _vector(highlights_x, "highlights_x", context=context)
    ]
    x_values = np.concatenate([table.loc[valid, "_time"].to_numpy(), highlights])
    x_domain = coordinate_domain(x_values, 0.05)
    if xlim is not None:
        limits = [
            number(v, "xlim", context=context, minimum=-np.inf)
            for v in _vector(xlim, "xlim", 2, context=context)
        ]
        x_domain = (
            (limits[0], limits[1])
            if limits[0] != limits[1]
            else coordinate_domain(np.array(limits), 0)
        )
    y_domain = coordinate_domain(table.loc[valid, "_value"].to_numpy(), 0.05)
    highlight_y = y_domain
    # Explicit y ticks expand the view after Scanpy places highlight endpoints.
    ticks = (
        None
        if yticks is None
        else tuple(
            number(v, "yticks", context=context, minimum=-np.inf)
            for v in _vector(yticks, "yticks", context=context)
        )
    )
    if ticks:
        y_domain = (min(y_domain[0], min(ticks)), max(y_domain[1], max(ticks)))
    return TimeseriesData(
        table,
        x_domain,
        y_domain,
        selected,
        domain,
        bool(names) and legend,
        ticks,
        highlight_y,
    ), highlights
