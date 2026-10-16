"""Selected AnnData extraction and deterministic UMAP preparation.

No plotting function, artist, analysis routine, or benchmark module is used.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations, product
from numbers import Integral, Real
from typing import Any
import warnings

import numpy as np
import pandas as pd
from matplotlib import colormaps, colors, rcParams
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import Locator
from scipy import sparse


@dataclass(frozen=True, slots=True)
class Panel:
    key: str | None
    source: str
    dimensions: tuple[int, int]
    categorical: bool
    domain: tuple[Any, ...]
    palette: tuple[str, ...]
    legend_values: tuple[str, ...]
    title: str | None
    labels: tuple[dict[str, Any], ...]
    width: float
    height: float


@dataclass(frozen=True, slots=True)
class PreparedUMAP:
    table: pd.DataFrame
    panels: tuple[Panel, ...]
    style: dict[str, Any]


def dimensions_for(
    components: Any, dimensions: Any, count: int
) -> list[tuple[int, int]]:
    pairs: Any
    if components is not None and dimensions is not None:
        raise ValueError(
            "gsc.pl.umap: components and dimensions are mutually exclusive."
        )
    if components == "all":
        pairs = list(combinations(range(count), 2))
    elif components is not None:
        entries = [components] if isinstance(components, str) else components
        try:
            pairs = [tuple(int(x) - 1 for x in pair.split(",")) for pair in entries]
        except (ValueError, AttributeError) as error:
            raise ValueError(
                "gsc.pl.umap: expected one-based component pairs."
            ) from error
    else:
        values = (0, 1) if dimensions is None else dimensions
        pairs = (
            [values] if all(isinstance(x, Integral) for x in values) else list(values)
        )
    if not pairs or any(
        len(p) != 2
        or any(
            isinstance(x, bool)
            or not isinstance(x, Integral)
            or not 0 <= int(x) < count
            for x in p
        )
        for p in pairs
    ):
        raise ValueError(
            f"gsc.pl.umap: expected valid 2D components in an embedding with {count} columns."
        )
    return [(int(p[0]), int(p[1])) for p in pairs]


def coordinate_domain(values: np.ndarray, margin: float) -> tuple[float, float]:
    low, high = Locator().nonsingular(float(values.min()), float(values.max()))
    extra = (high - low) * margin
    return low - extra, high + extra


def draw_order(values: np.ndarray, *, categorical: bool, sort: bool) -> np.ndarray:
    if not sort:
        return np.arange(len(values))
    if categorical:
        return np.argsort(~pd.isna(values), kind="stable")
    # Reversing a stable descending sort also reverses equal-value ties.
    return np.argsort(-values, kind="stable")[::-1]


def _font_size(value: Any) -> float:
    return float(FontProperties(size=value).get_size_in_points())


def _scalar(value: Any, name: str) -> float:
    if not isinstance(value, Real):
        raise ValueError(f"gsc.pl.umap: {name} must be a finite scalar.")
    result = float(value)
    if not np.isfinite(result):
        raise ValueError(f"gsc.pl.umap: {name} must be a finite scalar.")
    return result


def _bound(
    bound: Any, index: int, count: int, values: np.ndarray, default: float
) -> float:
    if isinstance(bound, Sequence) and not isinstance(bound, str):
        if len(bound) not in (1, count):
            raise ValueError(
                "gsc.pl.umap: color-bound lists must have one value or one per panel."
            )
        bound = bound[0 if len(bound) == 1 else index]
    if bound is None:
        return default
    if callable(bound):
        raise NotImplementedError(
            "gsc.pl.umap: callable color bounds are not supported yet."
        )
    if isinstance(bound, str):
        if not bound.startswith("p"):
            raise ValueError("gsc.pl.umap: percentile bounds must start with 'p'.")
        bound = float(np.nanpercentile(values, float(bound[1:])))
    result = float(bound)
    if not np.isfinite(result):
        raise ValueError("gsc.pl.umap: color bounds must be finite.")
    return result


def _expression(
    adata: Any, key: str, use_raw: bool, layer: str | None, symbols: str | None
) -> tuple[Any, str]:
    if key in adata.obs:
        if list(adata.obs.columns).count(key) != 1:
            raise ValueError(f"gsc.pl.umap: observation field {key!r} is ambiguous.")
        if key in adata.var_names or (use_raw and key in adata.raw.var_names):
            raise ValueError(
                f"gsc.pl.umap: {key!r} occurs in both observation and gene names."
            )
        return adata.obs[key].copy(), f"obs[{key!r}]"
    resolved = key
    if symbols is not None and key not in adata.var_names:
        if symbols not in adata.var or list(adata.var.columns).count(symbols) != 1:
            raise ValueError(
                f"gsc.pl.umap: gene-symbol column {symbols!r} is missing or ambiguous."
            )
        matches = np.flatnonzero(adata.var[symbols].eq(key).to_numpy())
        if len(matches) != 1:
            raise ValueError(
                f"gsc.pl.umap: gene symbol {key!r} is missing or ambiguous."
            )
        resolved = str(adata.var_names[matches[0]])
    names = adata.raw.var_names if use_raw else adata.var_names
    matches = np.flatnonzero(names == resolved)
    if len(matches) != 1:
        raise ValueError(
            f"gsc.pl.umap: gene {key!r} is missing or ambiguous in the selected representation."
        )
    if layer is not None and layer not in adata.layers:
        raise ValueError(f"gsc.pl.umap: layer {layer!r} is missing.")
    # In a backed view, even reading the public X/raw.X property may fetch a
    # wide slice. Reject before accessing either property, not after that I/O.
    if adata.isbacked:
        raise TypeError(
            "gsc.pl.umap: backed/lazy expression is not supported yet; "
            "load the required expression into memory explicitly."
        )
    matrix = (
        adata.raw.X if use_raw else adata.X if layer is None else adata.layers[layer]
    )
    if not isinstance(matrix, np.ndarray) and not sparse.issparse(matrix):
        raise TypeError(
            "gsc.pl.umap: selected expression requires in-memory NumPy or SciPy data; backed/lazy expression is not supported yet."
        )
    selected = matrix[:, [int(matches[0])]]
    values = selected.toarray() if sparse.issparse(selected) else selected
    source = "raw.X" if use_raw else "X" if layer is None else f"layers[{layer!r}]"
    return np.asarray(values).ravel().copy(), source


def _categorical(values: Any) -> pd.Categorical | None:
    if isinstance(getattr(values, "dtype", None), pd.CategoricalDtype):
        return pd.Categorical(values).copy()
    if pd.api.types.is_bool_dtype(values.dtype):
        return pd.Categorical(pd.Series(values).map({True: "True", False: "False"}))
    if pd.api.types.is_string_dtype(values.dtype) or values.dtype.kind in "OUS":
        from natsort import natsorted

        nonmissing = pd.Series(values).dropna()
        if not all(isinstance(x, str) for x in nonmissing):
            raise TypeError(
                "gsc.pl.umap: color metadata must be numeric, boolean, string, or categorical."
            )
        return pd.Categorical(values, categories=natsorted(nonmissing.unique()))
    return None


def _palette(
    adata: Any, key: str, categories: pd.Index, palette: Any
) -> tuple[str, ...]:
    import scanpy as sc

    count = len(categories)
    selected: Any
    if isinstance(palette, str):
        selected = colormaps.get_cmap(palette)(np.linspace(0, 1, count))
    elif isinstance(palette, Mapping):
        try:
            selected = [palette[c] for c in categories]
        except KeyError as error:
            raise ValueError(
                "gsc.pl.umap: palette mapping is missing a category."
            ) from error
    elif palette is not None:
        selected = (
            palette.by_key()["color"] if hasattr(palette, "by_key") else list(palette)
        )
        if not len(selected):
            raise ValueError("gsc.pl.umap: palette cannot be empty.")
        if len(selected) < count:
            warnings.warn(
                "gsc.pl.umap: palette has fewer colors than categories; colors repeat.",
                UserWarning,
                stacklevel=3,
            )
        selected = [selected[i % len(selected)] for i in range(count)]
    else:
        cached = adata.uns.get(f"{key}_colors", ())
        if len(cached) >= count:
            selected = cached[:count]
        else:
            cycle = rcParams["axes.prop_cycle"].by_key()["color"]
            selected = (
                cycle
                if len(cycle) >= count
                else sc.pl.palettes.default_20
                if count <= 20
                else sc.pl.palettes.default_28
                if count <= 28
                else sc.pl.palettes.default_102
                if count <= 103
                else ["grey"] * count
            )[:count]
    try:
        return tuple(colors.to_hex(c, keep_alpha=True) for c in selected)
    except ValueError as error:
        raise ValueError(f"gsc.pl.umap: invalid palette for {key!r}.") from error


def prepare_umap(adata: Any, **options: Any) -> PreparedUMAP:
    import scanpy as sc
    from anndata import AnnData
    from genome_spy.anndata import from_anndata

    if not isinstance(adata, AnnData):
        raise TypeError("gsc.pl.umap: expected AnnData.")
    if adata.n_obs == 0:
        raise ValueError("gsc.pl.umap: at least one observation is required.")
    raw = options["use_raw"]
    layer = options["layer"]
    if raw is not None and not isinstance(raw, bool):
        raise TypeError("gsc.pl.umap: use_raw must be True, False, or None.")
    if raw is True and layer is not None:
        raise ValueError("gsc.pl.umap: use_raw=True and layer are incompatible.")
    raw = adata.raw is not None and layer is None if raw is None else raw
    if raw and adata.raw is None:
        raise ValueError("gsc.pl.umap: use_raw=True requires adata.raw.")
    basis = "umap" if "umap" in adata.obsm else "X_umap"
    if basis not in adata.obsm:
        raise ValueError(
            "gsc.pl.umap: missing umap/X_umap in obsm; compute the embedding explicitly with Scanpy first."
        )
    pairs = dimensions_for(
        options["components"], options["dimensions"], adata.obsm[basis].shape[1]
    )
    keys = options["color"]
    keys = [keys] if keys is None or isinstance(keys, str) else list(keys)
    if not keys or any(k is not None and not isinstance(k, str) for k in keys):
        raise ValueError("gsc.pl.umap: color must contain observation or gene keys.")
    if options["components"] is not None:
        keys, pairs = map(list, zip(*product(keys, pairs), strict=True))
    markers = options["marker"]
    markers = [markers] if isinstance(markers, str) else list(markers)
    count = max(len(keys), len(pairs), len(markers))
    if any(len(x) not in (1, count) for x in (keys, pairs, markers)):
        raise ValueError(
            "gsc.pl.umap: color, dimensions, and marker lists cannot be broadcast."
        )
    keys, pairs, markers = [
        x * count if len(x) == 1 else x for x in (keys, pairs, markers)
    ]
    if any(m not in (".", "o") for m in markers):
        raise NotImplementedError(
            "gsc.pl.umap: only '.' and 'o' markers are supported yet."
        )
    needed = sorted({d for p in pairs for d in p})
    coordinates = from_anndata(adata, obs=[], obsm_keys=[(basis, d) for d in needed])
    table = pd.DataFrame(
        {f"_coord_{d}": coordinates[f"{basis}-{d}"].to_numpy().copy() for d in needed}
    )
    if not np.isfinite(table.to_numpy()).all():
        raise ValueError("gsc.pl.umap: coordinates must be finite.")
    id_key = options["obs_id"]
    if id_key is not None:
        if id_key not in adata.obs or list(adata.obs.columns).count(id_key) != 1:
            raise ValueError(
                f"gsc.pl.umap: obs_id column {id_key!r} is missing or ambiguous."
            )
        ids = adata.obs[id_key]
        if ids.isna().any() or not ids.is_unique:
            raise ValueError(
                "gsc.pl.umap: obs_id values must be unique and nonmissing."
            )
        ids = ids.astype(str).to_numpy()
        if len(set(ids)) != len(ids):
            raise ValueError(
                "gsc.pl.umap: obs_id values collide when serialized as strings."
            )
    else:
        ids = (
            adata.obs_names.to_numpy().copy()
            if adata.obs_names.is_unique
            else np.array([f"row-{i}" for i in range(len(adata))])
        )
    table["_obs_id"] = ids
    table["_obs_label"] = adata.obs_names.to_numpy().copy()
    mask = options["mask_obs"]
    if isinstance(mask, str):
        if mask not in adata.obs or list(adata.obs.columns).count(mask) != 1:
            raise ValueError(
                f"gsc.pl.umap: mask_obs field {mask!r} is missing or ambiguous."
            )
        mask = adata.obs[mask]
    if mask is not None:
        if isinstance(mask, pd.Series) and not mask.index.equals(adata.obs_names):
            raise ValueError(
                "gsc.pl.umap: mask_obs index must match observation order."
            )
        mask = np.asarray(mask)
        if mask.shape != (len(adata),) or mask.dtype != np.bool_:
            raise ValueError(
                "gsc.pl.umap: mask_obs must be a nonmissing boolean vector with one entry per observation."
            )
    size = np.asarray(
        120000 / len(adata) if options["size"] is None else options["size"], dtype=float
    )
    if (
        size.ndim > 1
        or (size.ndim == 1 and size.shape != (len(adata),))
        or not np.isfinite(size).all()
        or np.any(size < 0)
    ):
        raise ValueError(
            "gsc.pl.umap: size must be finite and nonnegative, scalar or one per observation."
        )
    dpi = float(rcParams["figure.dpi"])
    alpha = _scalar(1.0 if options["alpha"] is None else options["alpha"], "alpha")
    if not 0 <= alpha <= 1:
        raise ValueError("gsc.pl.umap: alpha must be a scalar between 0 and 1.")
    edge = colors.to_rgba(options["edgecolor"])
    stroke = (
        rcParams["lines.linewidth"]
        if options["linewidth"] is None
        else options["linewidth"]
    )
    stroke = _scalar(stroke, "linewidth")
    if stroke < 0:
        raise ValueError("gsc.pl.umap: linewidth must be finite and nonnegative.")
    ncols = options["ncols"]
    if isinstance(ncols, bool) or not isinstance(ncols, Integral) or ncols < 1:
        raise ValueError("gsc.pl.umap: ncols must be a positive integer.")
    columns = min(int(ncols), count)
    figure_width, figure_height = [float(x) * dpi for x in rcParams["figure.figsize"]]
    hspace = options["hspace"]
    wspace = options["wspace"]
    wspace = 0.75 / rcParams["figure.figsize"][0] + 0.02 if wspace is None else wspace
    if any(not np.isfinite(x) or x < 0 for x in (hspace, wspace)):
        raise ValueError(
            "gsc.pl.umap: hspace and wspace must be finite and nonnegative."
        )
    if count == 1:
        width = figure_width * (
            rcParams["figure.subplot.right"] - rcParams["figure.subplot.left"]
        )
        height = figure_height * (
            rcParams["figure.subplot.top"] - rcParams["figure.subplot.bottom"]
        )
    else:
        rows = int(np.ceil(count / columns))
        width = (
            figure_width
            * (1 + wspace)
            * columns
            * (0.8 - 0.01 / columns)
            / (columns + wspace * (columns - 1))
        )
        height = (
            figure_height * rows * (0.87 - 0.1 / rows) / (rows + hspace * (rows - 1))
        )
    na = colors.to_hex(options["na_color"], keep_alpha=True)
    color_map = colormaps.get_cmap(options["cmap"])
    categorical_palettes: dict[str, tuple[str, ...]] = {}
    extracted: dict[str, tuple[Any, str]] = {}
    panels = []
    for i, (key, dims, marker) in enumerate(zip(keys, pairs, markers, strict=True)):
        domain: tuple[Any, ...]
        if key is None:
            values, source = pd.Categorical([None] * len(adata)), "none"
        else:
            if key not in extracted:
                extracted[key] = _expression(
                    adata, key, raw, layer, options["gene_symbols"]
                )
            values, source = extracted[key]
        categorical = _categorical(values)
        labels: tuple[dict[str, Any], ...] = ()
        legend_values: tuple[str, ...] = ()
        if categorical is not None:
            categories = categorical.categories
            if key is not None and key not in categorical_palettes:
                categorical_palettes[key] = _palette(
                    adata, key, categories, options["palette"]
                )
            original_colors = categorical_palettes[key] if key is not None else ()
            palette_map = dict(zip(categories, original_colors, strict=True))
            if options["groups"] is not None:
                groups = (
                    [options["groups"]]
                    if isinstance(options["groups"], str)
                    else list(options["groups"])
                )
                categorical = categorical.remove_categories(
                    categories.difference(groups)
                )
            if mask is not None:
                categorical[~mask] = np.nan
            values = np.asarray(categorical)
            names = [str(c) for c in categorical.categories]
            if len(set(names)) != len(names):
                raise ValueError(
                    "gsc.pl.umap: category labels collide when serialized as strings."
                )
            domain = tuple(names)
            palette_colors = tuple(palette_map[c] for c in categorical.categories)
            legend_values = domain
            missing = pd.isna(values)
            if missing.any() or key is None:
                if "NA" in names:
                    raise NotImplementedError(
                        "gsc.pl.umap: a category named 'NA' conflicts with missing values."
                    )
                domain += ("NA",)
                palette_colors += (na,)
                if options["na_in_legend"] and key is not None:
                    legend_values += ("NA",)
            displayed = np.array(
                [
                    "NA" if absent else str(v)
                    for v, absent in zip(values, missing, strict=True)
                ]
            )
            table[f"_value_{i}"] = [
                None if absent else str(v)
                for v, absent in zip(values, missing, strict=True)
            ]
            table[f"_color_{i}"] = displayed
            display_palette = dict(zip(domain, palette_colors, strict=True))
            table[f"_paint_{i}"] = [display_palette[v] for v in displayed]
            if options["legend_loc"] == "on data":
                labels = tuple(
                    {
                        "x": float(
                            np.median(table.loc[displayed == name, f"_coord_{dims[0]}"])
                        ),
                        "y": float(
                            np.median(table.loc[displayed == name, f"_coord_{dims[1]}"])
                        ),
                        "label": name,
                    }
                    for name in legend_values
                    if np.any(displayed == name)
                )
        else:
            if isinstance(values, pd.Series):
                values = values.to_numpy(na_value=np.nan)
            values = np.asarray(values)
            if values.dtype.kind not in "fiu":
                values = values.astype(float)
            else:
                values = values.copy()
            if mask is not None:
                if values.dtype.kind != "f":
                    values = values.astype(float)
                values[~mask] = np.nan
            if np.isinf(values).any() or np.isnan(values).all():
                raise ValueError(
                    "gsc.pl.umap: continuous colors require finite values and at least one nonmissing value."
                )
            low = _bound(options["vmin"], i, count, values, float(np.nanmin(values)))
            high = _bound(options["vmax"], i, count, values, float(np.nanmax(values)))
            if low > high:
                raise ValueError("gsc.pl.umap: vmin cannot exceed vmax.")
            if low == high and options["colorbar_loc"] is not None:
                delta = abs(low) * 0.1 if low else 0.1
                low, high = low - delta, high + delta
            domain = (low, high)
            palette_colors = tuple(
                colors.to_hex(c, keep_alpha=True)
                for c in color_map(np.linspace(0, 1, color_map.N))
            )
            mapped = color_map(
                colors.Normalize(low, high)(np.ma.masked_invalid(values))
            )
            mapped[np.isnan(values)] = colors.to_rgba(na)
            table[f"_value_{i}"] = values
            table[f"_color_{i}"] = values
            table[f"_paint_{i}"] = [colors.to_hex(c, keep_alpha=True) for c in mapped]
        visible_guide = (
            categorical is not None
            and key is not None
            and options["legend_loc"] == "right margin"
        ) or (categorical is None and options["colorbar_loc"] is not None)
        if (
            visible_guide
            and options["alpha"] is None
            and any(colors.to_rgba(paint)[3] != 1 for paint in palette_colors)
        ):
            raise NotImplementedError(
                "gsc.pl.umap: transparent palette/cmap/na_color entries with a guide "
                "are not supported yet; use scalar alpha or disable the guide."
            )
        order = draw_order(
            values, categorical=categorical is not None, sort=options["sort_order"]
        )
        table[f"_opacity_{i}"] = [
            colors.to_rgba(paint)[3] if options["alpha"] is None else alpha
            for paint in table[f"_paint_{i}"]
        ]
        rank = np.empty(len(order), dtype=int)
        rank[order] = np.arange(len(order))
        table[f"_order_{i}"] = rank
        table[f"_size_{i}"] = size * (dpi / 72 * (0.5 if marker == "." else 1)) ** 2
        # Scanpy 1.11.5 carries the reordered size vector into the next panel.
        # Preserve that observable behavior, including its equal-value ties.
        if size.ndim == 1:
            size = size[order]
        titles = options["title"]
        titles = [titles] if isinstance(titles, str) else titles
        if titles is not None and len(titles) <= i:
            warnings.warn(
                "gsc.pl.umap: title list is shorter than the panel count; using color keys.",
                UserWarning,
                stacklevel=3,
            )
        panel_title = titles[i] if titles is not None and i < len(titles) else key
        shrinks = (categorical is not None and count > 1) or (
            categorical is None and options["colorbar_loc"] is not None
        )
        panels.append(
            Panel(
                key,
                source,
                dims,
                categorical is not None,
                domain,
                palette_colors,
                legend_values,
                panel_title,
                labels,
                float(options["width"])
                if options["width"] is not None
                else width * (0.91 if shrinks else 1),
                float(options["height"]) if options["height"] is not None else height,
            )
        )
    style = {
        "dpi": dpi,
        "frameon": getattr(sc.settings, "_frameon")
        if options["frameon"] is None
        else options["frameon"],
        "legend_loc": options["legend_loc"],
        "colorbar_loc": options["colorbar_loc"],
        "legend_fontsize": _font_size(
            rcParams["legend.fontsize"]
            if options["legend_fontsize"] is None
            else options["legend_fontsize"]
        )
        * dpi
        / 72,
        "legend_fontweight": options["legend_fontweight"],
        "axis_fontsize": _font_size(rcParams["axes.labelsize"]) * dpi / 72,
        "title_fontsize": _font_size(rcParams["axes.titlesize"]) * dpi / 72,
        "tick_fontsize": _font_size(rcParams["ytick.labelsize"]) * dpi / 72,
        "legend_labelspacing": rcParams["legend.labelspacing"],
        "legend_handletextpad": rcParams["legend.handletextpad"],
        # Lato Regular is embedded in the native runtime. Matplotlib fonts do
        # not have native glyph atlases; naming them would fetch a remote font
        # and then silently fall back, including in otherwise offline HTML.
        "font": "Lato",
        "ncols": columns,
        "hspace": hspace * (height if options["height"] is None else options["height"]),
        "wspace": wspace * (width if options["width"] is None else options["width"]),
        "alpha": float(alpha),
        "stroke": colors.to_hex(edge),
        "stroke_opacity": edge[3]
        if options["alpha"] is None or edge[3] == 0
        else alpha,
        "stroke_width": float(stroke) * dpi / 72,
        "frame_color": colors.to_hex(rcParams["axes.edgecolor"]),
        "frame_width": rcParams["axes.linewidth"] * dpi / 72,
        "xmargin": rcParams["axes.xmargin"],
        "ymargin": rcParams["axes.ymargin"],
    }
    return PreparedUMAP(table, tuple(panels), style)
