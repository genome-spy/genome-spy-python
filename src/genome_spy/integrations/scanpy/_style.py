"""Shared native colors, typography and Scanpy plot style preparation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import isfinite
from numbers import Integral, Real
from typing import Any
import warnings

import numpy as np
import pandas as pd

from genome_spy.integrations.scanpy._data import number


FONT = "Lato"
POINTS_TO_PIXELS = 100 / 72
GROUPED_FONT_SIZE = 10 * 0.833 * POINTS_TO_PIXELS


# Color scheme names supported by the bundled GenomeSpy version.
_SCHEMES = frozenset(
    """
accent category10 category20 category20b category20c dark2 observable10 paired
pastel1 pastel2 set1 set2 set3 tableau10 tableau20 blues greens greys oranges
purples reds bluegreen bluepurple greenblue orangered purpleblue purplebluegreen
purplered redpurple yellowgreen yelloworangebrown yelloworangered blueorange
brownbluegreen purplegreen purpleorange redblue redgrey yellowgreenblue
redyellowblue redyellowgreen pinkyellowgreen spectral viridis magma inferno
plasma cividis rainbow sinebow turbo browns tealblues teals warmgreys goldgreen
goldorange goldred lightgreyred lightgreyteal lightmulti lightorange lighttealblue
darkblue darkgold darkgreen darkmulti darkred
""".split()
)


def native_scheme(value: Any, name: str, *, context: str = "Scanpy embedding") -> str:
    """Return a supported color scheme name in lowercase, rejecting other forms."""
    if not isinstance(value, str) or value.lower() not in _SCHEMES:
        raise NotImplementedError(
            f"{context}: {name} requires a GenomeSpy scheme name, such as "
            "'viridis', 'redblue', or 'set1'; Matplotlib colormaps are unsupported."
        )
    return value.lower()


# CSS names distinguish flat scatter colors from misspelled annotation keys.
_CSS_NAMES = frozenset(
    """
aliceblue antiquewhite aqua aquamarine azure beige bisque black blanchedalmond
blue blueviolet brown burlywood cadetblue chartreuse chocolate coral cornflowerblue
cornsilk crimson cyan darkblue darkcyan darkgoldenrod darkgray darkgreen darkgrey
darkkhaki darkmagenta darkolivegreen darkorange darkorchid darkred darksalmon
darkseagreen darkslateblue darkslategray darkslategrey darkturquoise darkviolet
deeppink deepskyblue dimgray dimgrey dodgerblue firebrick floralwhite forestgreen
fuchsia gainsboro ghostwhite gold goldenrod gray green greenyellow grey honeydew
hotpink indianred indigo ivory khaki lavender lavenderblush lawngreen lemonchiffon
lightblue lightcoral lightcyan lightgoldenrodyellow lightgray lightgreen lightgrey
lightpink lightsalmon lightseagreen lightskyblue lightslategray lightslategrey
lightsteelblue lightyellow lime limegreen linen magenta maroon mediumaquamarine
mediumblue mediumorchid mediumpurple mediumseagreen mediumslateblue mediumspringgreen
mediumturquoise mediumvioletred midnightblue mintcream mistyrose moccasin navajowhite
navy oldlace olive olivedrab orange orangered orchid palegoldenrod palegreen
paleturquoise palevioletred papayawhip peachpuff peru pink plum powderblue purple
rebeccapurple red rosybrown royalblue saddlebrown salmon sandybrown seagreen seashell
sienna silver skyblue slateblue slategray slategrey snow springgreen steelblue tan
teal thistle tomato turquoise violet wheat white whitesmoke yellow yellowgreen
""".split()
)


def native_color(value: Any, name: str, *, context: str = "Scanpy embedding") -> str:
    """Return an opaque CSS color unchanged, or reject forms needing conversion."""
    # Validate names without converting colors or importing a rendering library.
    if isinstance(value, str):
        named = value.lower() in _CSS_NAMES
        hex_color = (
            value.startswith("#")
            and len(value) in (4, 7)
            and all(character in "0123456789abcdefABCDEF" for character in value[1:])
        )
        if named or hex_color:
            return value
    raise NotImplementedError(
        f"{context}: {name} requires an opaque CSS color name or #RGB/#RRGGBB. "
        "Matplotlib colors and per-color alpha are unsupported; use scalar alpha."
    )


def color_bounds(
    values: np.ndarray,
    vmin: float | None,
    vmax: float | None,
    *,
    context: str,
    expand_constant: bool = True,
) -> tuple[float, float, bool]:
    """Return color limits and whether they were constant from values and overrides.

    Ignore missing values and optionally widen constant limits for a colorbar.
    """
    valid = values[np.isfinite(values)]
    if not valid.size:
        raise ValueError(f"{context}: colors need at least one finite value.")
    low = (
        float(valid.min())
        if vmin is None
        else number(vmin, "vmin", minimum=-float("inf"), context=context)
    )
    high = (
        float(valid.max())
        if vmax is None
        else number(vmax, "vmax", minimum=-float("inf"), context=context)
    )
    if low > high:
        raise ValueError(f"{context}: vmin cannot exceed vmax.")
    constant = low == high
    # A constant color range still needs visible space on the colorbar.
    if constant and expand_constant:
        delta = abs(low) * 0.1 or 0.1
        low, high = low - delta, high + delta
    return low, high, constant


@dataclass(frozen=True, slots=True)
class ColorData:
    values: np.ndarray
    domain: tuple[Any, ...]
    palette: tuple[str, ...]
    scheme: str | None
    legend_values: tuple[str, ...]
    categorical: bool


def draw_order(values: np.ndarray, *, categorical: bool, sort: bool) -> np.ndarray:
    """Return row positions in Scanpy's painting order for the supplied color values.

    Match Scanpy's order for missing values and ties so overlapping points agree.
    """
    if not sort:
        return np.arange(len(values))
    if categorical:
        return np.argsort(~pd.isna(values), kind="stable")
    # Reversing a stable descending sort also reverses equal-value ties.
    return np.argsort(-values, kind="stable")[::-1]


def _bound(
    bound: Any,
    index: int,
    count: int,
    values: np.ndarray,
    default: float,
    *,
    name: str,
    sort_order: bool,
) -> float:
    """Return one panel's bound from a number, percentile, callable or list.

    Callables receive copied colors in painting order; unset bounds use default.
    """
    # A single bound applies to every panel; a list may set one per panel.
    if isinstance(bound, Sequence) and not isinstance(bound, str):
        if len(bound) not in (1, count):
            raise ValueError(
                "Scanpy embedding: color-bound lists must have one value or one per panel."
            )
        bound = bound[0 if len(bound) == 1 else index]
    if bound is None:
        return default
    if callable(bound):
        # Match Scanpy's callback order without exposing the plotted values to edits.
        order = draw_order(values, categorical=False, sort=sort_order)
        bound = bound(values[order])
        if (
            isinstance(bound, bool)
            or not isinstance(bound, Real)
            or not isfinite(bound)
        ):
            raise ValueError(
                f"Scanpy embedding: {name} callable for panel {index + 1} must return a finite number."
            )
    if isinstance(bound, str):
        if not bound.startswith("p"):
            raise ValueError("Scanpy embedding: percentile bounds must start with 'p'.")
        bound = float(np.nanpercentile(values, float(bound[1:])))
    result = float(bound)
    if not np.isfinite(result):
        raise ValueError("Scanpy embedding: color bounds must be finite.")
    return result


def _categorical(
    values: Any, *, context: str = "Scanpy embedding"
) -> pd.Categorical | None:
    """Return ordered categories for label-like values, or None for numeric colors.

    Preserve saved order; otherwise use Scanpy's string and boolean ordering.
    """
    # Keep a saved category order instead of sorting it again.
    if isinstance(getattr(values, "dtype", None), pd.CategoricalDtype):
        return pd.Categorical(values).copy()
    if pd.api.types.is_bool_dtype(values.dtype):
        return pd.Categorical(pd.Series(values).map({True: "True", False: "False"}))
    if pd.api.types.is_string_dtype(values.dtype) or values.dtype.kind in "OUS":
        from natsort import natsorted

        nonmissing = pd.Series(values).dropna()
        if not all(isinstance(x, str) for x in nonmissing):
            raise TypeError(
                f"{context}: color metadata must be numeric, boolean, string, or categorical."
            )
        return pd.Categorical(values, categories=natsorted(nonmissing.unique()))
    return None


def _palette(
    adata: Any,
    key: str,
    categories: pd.Index,
    palette: Any,
    *,
    context: str = "Scanpy embedding",
) -> tuple[tuple[str, ...], str | None]:
    """Return ordered CSS colors or a scheme name for the requested categories.

    Use the supplied palette, saved AnnData colors or Scanpy defaults, in that order.
    """
    count = len(categories)
    if isinstance(palette, str):
        return (), native_scheme(palette, "palette", context=context)
    if isinstance(palette, Mapping):
        # Named colors follow category order, not dictionary order.
        try:
            selected = [palette[c] for c in categories]
        except KeyError as error:
            raise ValueError(
                f"{context}: palette mapping is missing a category."
            ) from error
    elif palette is not None:
        if not isinstance(palette, (Sequence, np.ndarray)):
            raise NotImplementedError(
                f"{context}: palette requires CSS colors or a native scheme; color cyclers are unsupported."
            )
        selected = list(palette)
        if not selected:
            raise ValueError(f"{context}: palette cannot be empty.")
        if len(selected) < count:
            warnings.warn(
                f"{context}: palette has fewer colors than categories; colors repeat.",
                UserWarning,
                stacklevel=3,
            )
        selected = [selected[i % len(selected)] for i in range(count)]
    else:
        import scanpy as sc

        # Reuse saved colors before choosing the smallest Scanpy palette that fits.
        cached = adata.uns.get(f"{key}_colors", ())
        if len(cached) >= count:
            selected = cached[:count]
        else:
            defaults = [
                sc.pl.palettes.vega_10,
                sc.pl.palettes.default_20,
                sc.pl.palettes.default_28,
                sc.pl.palettes.default_102,
            ]
            selected = next(
                (p[:count] for p in defaults if len(p) >= count), ["grey"] * count
            )
    return tuple(native_color(c, "palette", context=context) for c in selected), None


def categorical_colors(
    adata: Any,
    key: str | None,
    values: pd.Categorical,
    *,
    palette: Any,
    groups: Any,
    mask: Any,
    na_color: str,
    na_in_legend: bool,
) -> ColorData:
    """Return labels, colors and legend entries for a panel's categories.

    Apply groups and masks without changing the remaining groups' assigned colors.
    """
    # Resolve colors before hiding groups so the remaining groups keep their colors.
    categories = values.categories
    original, scheme = (
        _palette(adata, key, categories, palette) if key is not None else ((), None)
    )
    palette_map = dict(zip(categories, original))
    original_names = tuple(str(category) for category in categories)
    if groups is not None:
        groups = [groups] if isinstance(groups, str) else list(groups)
        values = values.remove_categories(categories.difference(groups))
    if mask is not None:
        values[~mask] = np.nan

    # Labels become strings in the browser and must still identify distinct groups.
    names = tuple(str(category) for category in values.categories)
    if len(set(names)) != len(names):
        raise ValueError(
            "Scanpy embedding: category labels collide when serialized as strings."
        )
    palette_colors = (
        tuple(palette_map[category] for category in values.categories)
        if scheme is None
        else ()
    )
    legend_values = names
    missing = pd.isna(values)
    # Missing cells get their own color without becoming an ordinary category.
    if missing.any() or key is None:
        if "NA" in names:
            raise NotImplementedError(
                "Scanpy embedding: a category named 'NA' conflicts with missing values."
            )
        if scheme is not None and na_in_legend:
            raise NotImplementedError(
                "Scanpy embedding: a missing-category legend with a named scheme is not supported yet; "
                "pass an explicit CSS palette or na_in_legend=False."
            )
        if scheme is None:
            names += ("NA",)
            palette_colors += (na_color,)
        if na_in_legend and key is not None:
            legend_values += ("NA",)

    measurements = np.asarray(
        [
            None if absent else str(value)
            for value, absent in zip(values, missing, strict=True)
        ],
        dtype=object,
    )
    return ColorData(
        measurements,
        original_names if scheme is not None else names,
        palette_colors,
        scheme,
        legend_values,
        True,
    )


def continuous_colors(
    values: Any,
    *,
    cmap: Any,
    mask: Any,
    vmin: Any,
    vmax: Any,
    index: int,
    count: int,
    colorbar: bool,
    sort_order: bool = True,
) -> ColorData:
    """Return copied numeric colors, bounds and scheme for one panel.

    Apply masks and panel-specific limits without changing the source values.
    """
    # Use a copy so masking colors never changes the source expression values.
    if isinstance(values, pd.Series):
        values = values.to_numpy(na_value=np.nan)
    values = np.asarray(values).copy()
    if values.dtype.kind not in "fiu" or (
        mask is not None and values.dtype.kind != "f"
    ):
        values = values.astype(float)
    if mask is not None:
        values[~mask] = np.nan
    if np.isinf(values).any() or np.isnan(values).all():
        raise ValueError(
            "Scanpy embedding: continuous colors require finite values and at least one nonmissing value."
        )
    # Resolve Python bounds before choosing the native color scale.
    low = _bound(
        vmin,
        index,
        count,
        values,
        float(np.nanmin(values)),
        name="vmin",
        sort_order=sort_order,
    )
    high = _bound(
        vmax,
        index,
        count,
        values,
        float(np.nanmax(values)),
        name="vmax",
        sort_order=sort_order,
    )
    low, high, _ = color_bounds(
        values, low, high, context="Scanpy embedding", expand_constant=colorbar
    )
    scheme = native_scheme("viridis" if cmap is None else cmap, "cmap")
    return ColorData(values, (low, high), (), scheme, (), False)


@dataclass(frozen=True, slots=True)
class EmbeddingStyle:
    width: float
    height: float
    frameon: bool
    legend_loc: str | None
    colorbar_loc: str | None
    legend_fontsize: float
    ncols: int
    hspace: float
    wspace: float
    alpha: float
    stroke: str
    na_color: str
    stroke_opacity: float
    stroke_width: float
    font: str = FONT
    axis_fontsize: float = 10 * POINTS_TO_PIXELS
    title_fontsize: float = 12 * POINTS_TO_PIXELS
    tick_fontsize: float = 10 * POINTS_TO_PIXELS
    legend_symbol_size: float = 36
    legend_labelspacing: float = 0.5
    legend_handletextpad: float = 0.8
    frame_color: str = "#000000"
    frame_width: float = 0.8 * POINTS_TO_PIXELS
    xmargin: float = 0.05
    ymargin: float = 0.05
    outline_width: tuple[float, float] | None = None
    outline_color: tuple[str, str] = ("black", "white")


def _number(value: Any, name: str, *, minimum: float = 0) -> float:
    """Return a checked embedding number, retaining its existing True/False handling."""
    # Keep embedding plots' existing treatment of True and False as 1 and 0.
    return number(
        float(value) if isinstance(value, bool) else value,
        name,
        context="Scanpy embedding",
        minimum=minimum,
    )


def _font_size(value: float | str | None) -> float:
    """Convert a numeric or named legend font size to pixels, using Scanpy defaults."""
    sizes = {
        "xx-small": 5.79,
        "x-small": 6.94,
        "small": 8.33,
        "medium": 10,
        "large": 12,
        "x-large": 14.4,
        "xx-large": 17.28,
    }
    if isinstance(value, str):
        if value not in sizes:
            raise ValueError(f"Scanpy embedding: unknown legend_fontsize {value!r}.")
        value = sizes[value]
    return _number(10 if value is None else value, "legend_fontsize") * POINTS_TO_PIXELS


def embedding_style(
    *,
    count: int,
    width: float | None,
    height: float | None,
    frameon: bool,
    legend_loc: str | None,
    colorbar_loc: str | None,
    legend_fontsize: float | str | None,
    ncols: int,
    hspace: float,
    wspace: float | None,
    alpha: Any,
    edgecolor: Any,
    linewidth: Any,
    na_color: Any,
    add_outline: bool = False,
    outline_width: tuple[float, float] = (0.3, 0.05),
    outline_color: tuple[str, str] = ("black", "white"),
) -> EmbeddingStyle:
    """Return native embedding settings from plot options, using explicit defaults.

    Validate appearance separately from data so chart building needs no global style.
    """
    if isinstance(ncols, bool) or not isinstance(ncols, Integral) or ncols < 1:
        raise ValueError("Scanpy embedding: ncols must be a positive integer.")
    opacity = _number(1 if alpha is None else alpha, "alpha")
    if opacity > 1:
        raise ValueError("Scanpy embedding: alpha must be a scalar between 0 and 1.")
    no_edge = isinstance(edgecolor, str) and edgecolor.lower() == "none"
    edge = "black" if no_edge else native_color(edgecolor, "edgecolor")
    for name, pair in (
        ("outline_width", outline_width),
        ("outline_color", outline_color),
    ):
        if not isinstance(pair, (tuple, list)) or len(pair) != 2:
            raise ValueError(f"Scanpy embedding: {name} needs a pair of values.")
    widths = tuple(_number(value, "outline_width") for value in outline_width)
    diameter = POINTS_TO_PIXELS * (1 + 2 * sum(widths))
    _number(diameter * diameter, "outline_width")
    colors = tuple(native_color(value, "outline_color") for value in outline_color)
    return EmbeddingStyle(
        width=300 if width is None else width,
        height=300 if height is None else height,
        frameon=frameon,
        legend_loc=legend_loc,
        colorbar_loc=colorbar_loc,
        legend_fontsize=_font_size(legend_fontsize),
        ncols=min(ncols, count),
        hspace=_number(hspace, "hspace"),
        wspace=0.2 if wspace is None else _number(wspace, "wspace"),
        alpha=opacity,
        stroke=edge,
        na_color=native_color(na_color, "na_color"),
        stroke_opacity=0 if no_edge else 1 if add_outline else opacity,
        stroke_width=_number(1.5 if linewidth is None else linewidth, "linewidth")
        * POINTS_TO_PIXELS,
        outline_width=(widths[0], widths[1]) if add_outline else None,
        outline_color=(colors[0], colors[1]),
    )
