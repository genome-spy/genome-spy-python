"""Scanpy plotting entry points; analysis continues through Scanpy itself."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from importlib.metadata import PackageNotFoundError, version
from math import isfinite
from numbers import Real
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from anndata import AnnData

    from genome_spy import Parameter, TopLevelSpec

__all__ = ["umap"]

_Bound = float | str | Sequence[float | str | None] | None


def _require_scanpy() -> Any:
    try:
        installed = version("scanpy")
    except PackageNotFoundError as error:
        raise ImportError(
            "gsc.pl.umap requires genome-spy-python[scanpy] (Scanpy 1.11.5)."
        ) from error
    if installed != "1.11.5":
        raise ImportError(
            f"gsc.pl.umap supports Scanpy 1.11.5; found {installed}. "
            "Install genome-spy-python[scanpy]."
        )
    import scanpy

    return scanpy


def umap(
    adata: AnnData,
    *,
    color: str | Sequence[str] | None = None,
    mask_obs: Any = None,
    gene_symbols: str | None = None,
    use_raw: bool | None = None,
    sort_order: bool = True,
    edges: bool = False,
    edges_width: float = 0.1,
    edges_color: Any = "grey",
    neighbors_key: str | None = None,
    arrows: bool = False,
    arrows_kwds: Mapping[str, Any] | None = None,
    groups: str | Sequence[str] | None = None,
    components: str | Sequence[str] | None = None,
    dimensions: tuple[int, int] | Sequence[tuple[int, int]] | None = None,
    layer: str | None = None,
    projection: Literal["2d", "3d"] = "2d",
    scale_factor: float | None = None,
    color_map: Any = None,
    cmap: Any = None,
    palette: Any = None,
    na_color: Any = "lightgray",
    na_in_legend: bool = True,
    size: float | Sequence[float] | None = None,
    frameon: bool | None = None,
    legend_fontsize: float | str | None = None,
    legend_fontweight: int | str = "bold",
    legend_loc: str | None = "right margin",
    legend_fontoutline: int | None = None,
    colorbar_loc: str | None = "right",
    vmax: _Bound = None,
    vmin: _Bound = None,
    vcenter: Any = None,
    norm: Any = None,
    add_outline: bool | None = False,
    outline_width: tuple[float, float] = (0.3, 0.05),
    outline_color: tuple[str, str] = ("black", "white"),
    ncols: int = 4,
    hspace: float = 0.25,
    wspace: float | None = None,
    title: str | Sequence[str] | None = None,
    show: bool | None = None,
    save: bool | str | None = None,
    marker: str | Sequence[str] = ".",
    hover: bool = True,
    zoom: bool = False,
    selection: Parameter | None = None,
    obs_id: str | None = None,
    width: float | None = None,
    height: float | None = None,
    **kwargs: Any,
) -> TopLevelSpec | None:
    """Plot existing UMAP coordinates with Scanpy-compatible color semantics.

    Description:
        Supports Scanpy 1.11.5 categorical and continuous 2D UMAP, including
        multiple panels, selected raw/layer genes, palettes, masks, per-cell
        sizes, color sorting, and percentile bounds. Data preparation happens
        in Python without modifying AnnData or computing an embedding. The
        result is a native GenomeSpy chart, displayed through anywidget.
        Matplotlib object parameters ``ax`` and ``return_fig`` are omitted.
        See the Scanpy integration guide for the complete support table.

    Args:
        adata: AnnData with existing ``umap`` or ``X_umap`` coordinates.
        color: Observation or gene keys, one per panel; None uses na_color.
        mask_obs: Boolean observation mask or observation-column key. Masks
            affect coloring, retaining all coordinates.
        gene_symbols: Variable column used to resolve gene symbols.
        use_raw: Use raw when present by default, unless a layer is selected.
        sort_order: Draw larger continuous values last, following Scanpy ties.
        edges: Graph edges; currently only False is supported.
        edges_width: Reserved upstream edge width.
        edges_color: Reserved upstream edge color.
        neighbors_key: Reserved upstream graph key.
        arrows: Graph arrows; currently only False is supported.
        arrows_kwds: Reserved upstream arrow options.
        groups: Categorical groups to color; other observations remain visible.
        components: One-based component pairs, or "all".
        dimensions: Zero-based component pairs; mutually exclusive with components.
        layer: Expression layer, mutually exclusive with use_raw=True.
        projection: Currently only "2d" is supported.
        scale_factor: Reserved upstream spatial scaling option.
        color_map: Alias for cmap, mutually exclusive with it.
        cmap: Matplotlib colormap name/object; defaults to the current rcParam.
        palette: Categorical colors as a name, sequence, mapping, or color cycler.
        na_color: Color for missing or masked values.
        na_in_legend: Include a missing-category legend entry.
        size: Marker area in points squared, scalar or one value per observation.
        frameon: Show axes and frame; defaults to Scanpy's frame setting.
        legend_fontsize: Legend/annotation font size in points or relative name.
        legend_fontweight: Weight of on-data category labels; currently normal
            (400) only, as other weights require an unbundled font atlas.
        legend_loc: "right margin", "on data", "none", or None.
        legend_fontoutline: Label halos are not yet supported.
        colorbar_loc: Currently "right" or None.
        vmax: Numeric or percentile upper color bound, optionally per panel.
        vmin: Numeric or percentile lower color bound, optionally per panel.
        vcenter: Custom centers are not yet supported.
        norm: Custom normalization is not yet supported.
        add_outline: Cluster outlines are not yet supported.
        outline_width: Reserved upstream outline widths.
        outline_color: Reserved upstream outline colors.
        ncols: Maximum number of panel columns.
        hspace: Relative vertical panel spacing.
        wspace: Relative horizontal panel spacing.
        title: Panel titles, defaulting to color keys.
        show: Display and return None when True; return a chart when False.
            None uses Scanpy settings.autoshow.
        save: Image saving is not yet supported; use native HTML/JSON save.
        marker: Dot (".") or circle ("o"), optionally per panel.
        hover: Enable record/value tooltips without changing initial appearance.
        zoom: Enable coordinate navigation, shared across panels.
        selection: Reserved for the linked-selection phase; currently None.
        obs_id: Unique nonmissing observation-column key, defaulting to obs_names
            or distinct snapshot-local row keys when names repeat.
        width: GenomeSpy plot-area width per panel in logical pixels. None
            retains the Scanpy-compatible default. Axes and guides add space.
        height: GenomeSpy plot-area height per panel in logical pixels. None
            retains the Scanpy-compatible default. Does not resize markers/fonts.
        **kwargs: Supported scatter aliases: s, alpha, edgecolor/edgecolors,
            linewidth/linewidths. Other options fail before data extraction.

    Returns:
        A native chart/composition when show=False, otherwise None.

    Raises:
        ImportError: If the optional dependency/version is unavailable.
        TypeError: If an argument or source type is invalid.
        ValueError: If requested data, sizes, masks, or bounds are invalid.
        NotImplementedError: If a recognized plotting option is unsupported.

    Example:
        >>> import genome_spy.scanpy as gsc
        >>> chart = gsc.pl.umap(adata, color=["cell_type", "MS4A1"], show=False)
        >>> chart.save("umap.html", inline=True)
    """
    unsupported = {
        "edges": edges is not False,
        "edges_width": edges_width != 0.1,
        "edges_color": not isinstance(edges_color, str) or edges_color != "grey",
        "neighbors_key": neighbors_key is not None,
        "arrows": arrows is not False,
        "arrows_kwds": arrows_kwds is not None,
        "projection": projection != "2d",
        "scale_factor": scale_factor is not None,
        "legend_fontoutline": legend_fontoutline is not None,
        "legend_fontweight": legend_loc == "on data"
        and legend_fontweight not in (400, "normal", "regular"),
        "legend_loc": legend_loc not in (None, "none", "right margin", "on data"),
        "colorbar_loc": colorbar_loc not in (None, "right"),
        "vcenter": vcenter is not None,
        "norm": norm is not None,
        "add_outline": add_outline not in (False, None),
        "outline_width": outline_width != (0.3, 0.05),
        "outline_color": outline_color != ("black", "white"),
        "selection": selection is not None,
        "save": save is not None and save is not False,
    }
    for name in ("ax", "return_fig"):
        if name in kwargs:
            raise TypeError(
                f"gsc.pl.umap: {name} is omitted from the native API. "
                "Use show=False and the returned GenomeSpy chart."
            )
    for name, rejected in unsupported.items():
        if rejected:
            raise NotImplementedError(
                f"gsc.pl.umap (Scanpy 1.11.5): {name} is not supported yet. "
                "See the Scanpy integration support table."
            )
    aliases = {"s", "alpha", "edgecolor", "edgecolors", "linewidth", "linewidths"}
    unknown = kwargs.keys() - aliases
    if unknown:
        raise TypeError(
            f"gsc.pl.umap: unknown option(s): {', '.join(sorted(unknown))}."
        )
    for left, right in [("edgecolor", "edgecolors"), ("linewidth", "linewidths")]:
        if left in kwargs and right in kwargs:
            raise TypeError(f"gsc.pl.umap: pass only one of {left} and {right}.")
    if "s" in kwargs:
        if size is not None:
            raise TypeError("gsc.pl.umap: pass only one of size and s.")
        size = kwargs["s"]
    if color_map is not None and cmap is not None:
        raise ValueError("gsc.pl.umap: cannot specify both color_map and cmap.")
    if groups is not None and mask_obs is not None:
        raise ValueError("gsc.pl.umap: groups and mask_obs are incompatible.")
    for name, dimension in {"width": width, "height": height}.items():
        if dimension is not None and (
            isinstance(dimension, bool)
            or not isinstance(dimension, Real)
            or not isfinite(dimension)
            or dimension <= 0
        ):
            raise ValueError(
                f"gsc.pl.umap: {name} must be a positive finite number or None."
            )
    for name, option in {
        "sort_order": sort_order,
        "na_in_legend": na_in_legend,
        "hover": hover,
        "zoom": zoom,
    }.items():
        if not isinstance(option, bool):
            raise TypeError(f"gsc.pl.umap: {name} must be boolean.")
    for name, nullable in {"show": show, "frameon": frameon}.items():
        if nullable is not None and not isinstance(nullable, bool):
            raise TypeError(f"gsc.pl.umap: {name} must be boolean or None.")
    sc = _require_scanpy()
    if sc.settings.autosave and save is None:
        raise NotImplementedError(
            "gsc.pl.umap: automatic image saving is not supported yet; "
            "use save=False and chart.save('umap.html', inline=True)."
        )
    from genome_spy.scanpy._prepare import prepare_umap
    from genome_spy.scanpy._charts import build_umap

    prepared = prepare_umap(
        adata,
        color=color,
        mask_obs=mask_obs,
        gene_symbols=gene_symbols,
        use_raw=use_raw,
        layer=layer,
        groups=groups,
        components=components,
        dimensions=dimensions,
        size=size,
        marker=marker,
        palette=palette,
        cmap=cmap if color_map is None else color_map,
        na_color=na_color,
        na_in_legend=na_in_legend,
        sort_order=sort_order,
        vmin=vmin,
        vmax=vmax,
        title=title,
        obs_id=obs_id,
        frameon=frameon,
        legend_loc=legend_loc,
        legend_fontsize=legend_fontsize,
        legend_fontweight=legend_fontweight,
        colorbar_loc=colorbar_loc,
        ncols=ncols,
        hspace=hspace,
        wspace=wspace,
        width=width,
        height=height,
        alpha=kwargs.get("alpha"),
        edgecolor=kwargs.get("edgecolor", kwargs.get("edgecolors", "none")),
        linewidth=kwargs.get("linewidth", kwargs.get("linewidths", None)),
    )
    chart = build_umap(prepared, hover=hover, zoom=zoom)
    if sc.settings.autoshow if show is None else show:
        chart.display()
        return None
    return chart
