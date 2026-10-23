"""Scanpy-style MatrixPlot chains backed by shared summaries and native tiles."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any, Literal, Self

from genome_spy.integrations.scanpy._grouped_builder import _GroupedPlot
from genome_spy.integrations.scanpy._guards import (
    _check_grid_zoom,
    _check_kwargs,
    _check_point_options,
    _require_scanpy,
)
from genome_spy.schemapi import Undefined, UndefinedType

if TYPE_CHECKING:
    from anndata import AnnData
    import pandas as pd

    from genome_spy import TopLevelSpec


class MatrixPlot(_GroupedPlot):
    """Build group-mean tiles with Scanpy-style method chains.

    Compute detached summaries once at construction. Methods mutate this builder
    and return self; each to_chart call creates a fresh native chart for
    composition, display or HTML/JSON saving. Supplied values skip expression
    reads, averaging and scaling.

    Args:
        adata: AnnData containing expression and grouping annotations.
        var_names: Feature keys, repeated slots or labeled feature groups.
        groupby: Observation key or categorical grouping keys.
        use_raw: Use raw when available; layer overrides the automatic choice.
        log: Apply log1p before averaging; ignored for supplied values_df.
        num_categories: Number of bins for numeric grouping annotations.
        categories_order: Complete group order, also applied to values_df rows.
        title: Plot title.
        figsize: Native layout budget in inches at 100 logical pixels/inch.
        gene_symbols: Variable annotation column for symbol lookup.
        var_group_positions: Inclusive feature-slot bracket endpoints.
        var_group_labels: Bracket labels; mappings already supply these.
        var_group_rotation: Bracket label rotation in degrees.
        layer: Expression layer instead of the automatic raw/X source.
        standard_scale: Min–max scale computed means per variable or group once.
        values_df: Authoritative labeled numeric table, copied without scaling.
        vmin: Finite numeric lower color bound.
        vmax: Finite numeric upper color bound.
        vcenter: Reserved; nondefault values error.
        norm: Reserved; Matplotlib normalization objects error.
        hover: Show gene, group and displayed mean or supplied value.
        zoom: True enables y navigation; "xy" also enables x navigation.
        show_values: Show values when native fitted text has enough room.
        width: Plot-area width in logical pixels.
        height: Plot-area height in logical pixels.
        **kwds: Only cmap, scalar edgecolor and linewidth are supported.

    Returns:
        A mutable matrixplot builder; construction does not display a chart.

    Raises:
        ImportError: If Scanpy 1.11.5 is unavailable.
        TypeError: If inputs or forwarded options have invalid types.
        ValueError: If table labels, groups or dimensions are invalid.
        NotImplementedError: If a requested renderer option is unsupported.

    Example:
        >>> plot = gsc.pl.MatrixPlot(pbmc, markers, "louvain", standard_scale="var")
        >>> chart = plot.add_dendrogram().style(cmap="Blues").to_chart()
        >>> chart.save("markers.html", inline=True)
    """

    def __init__(
        self,
        adata: AnnData,
        var_names: str | Sequence[str] | Mapping[str, str | Sequence[str]],
        groupby: str | Sequence[str],
        *,
        use_raw: bool | None = None,
        log: bool = False,
        num_categories: int = 7,
        categories_order: Sequence[str] | None = None,
        title: str | None = None,
        figsize: tuple[float, float] | None = None,
        gene_symbols: str | None = None,
        var_group_positions: Sequence[tuple[int, int]] | None = None,
        var_group_labels: Sequence[str] | None = None,
        var_group_rotation: float | None = None,
        layer: str | None = None,
        standard_scale: Literal["var", "group"] | None = None,
        values_df: pd.DataFrame | None = None,
        vmin: float | None = None,
        vmax: float | None = None,
        vcenter: float | None = None,
        norm: Any = None,
        hover: bool = True,
        zoom: bool | Literal["xy"] = False,
        show_values: bool = False,
        width: float | None = None,
        height: float | None = None,
        **kwds: Any,
    ) -> None:
        context = "gsc.pl.MatrixPlot"
        _check_kwargs(kwds, {"cmap", "edgecolor", "linewidth"}, context=context)
        for name, value in {"vcenter": vcenter, "norm": norm}.items():
            if value is not None:
                raise NotImplementedError(f"{context}: {name} is not supported yet.")
        _check_point_options(
            context=context,
            width=width,
            height=height,
            frameon=None,
            log=log,
            hover=hover,
            show_values=show_values,
        )
        if standard_scale not in (None, "var", "group"):
            raise ValueError(
                f"{context}: standard_scale must be 'var', 'group', or None."
            )
        _check_grid_zoom(zoom, context=context)
        _require_scanpy(context)

        from genome_spy.integrations.scanpy._grouped_data import (
            grouped_expression,
            matrixplot_statistics,
        )

        prepared = grouped_expression(
            adata,
            var_names,
            groupby,
            use_raw=use_raw,
            log=log if values_df is None else False,
            read_values=values_df is None,
            num_categories=num_categories,
            categories_order=categories_order,
            gene_symbols=gene_symbols,
            layer=layer,
            var_group_positions=var_group_positions,
            var_group_labels=var_group_labels,
        )
        colors = matrixplot_statistics(
            prepared.values,
            standard_scale=standard_scale,
            values_df=values_df,
            categories_order=categories_order,
        )
        super().__init__(
            adata,
            groupby,
            colors,
            prepared.feature_groups,
            prepared.counts,
            context=context,
        )
        self._value_title = "Value" if values_df is not None else "Mean expression"
        if values_df is None and standard_scale is not None:
            self._value_title += " (scaled)"
        self._options: dict[str, Any] = {
            "title": title,
            "figsize": figsize,
            "rotation": var_group_rotation,
            "vmin": vmin,
            "vmax": vmax,
            "hover": hover,
            "zoom": zoom,
            "show_values": show_values,
            "width": width,
            "height": height,
            "cmap": kwds.get("cmap", "viridis"),
            "edgecolor": kwds.get("edgecolor", "gray"),
            "linewidth": kwds.get("linewidth", 0.1),
            "colorbar_title": "Mean expression\nin group",
        }

    def style(
        self,
        cmap: Any = Undefined,
        edge_color: str | None | UndefinedType = Undefined,
        edge_lw: float | None | UndefinedType = Undefined,
    ) -> Self:
        """Update supplied tile styles while keeping omitted settings.

        Args:
            cmap: Native GenomeSpy scheme; None selects viridis.
            edge_color: Opaque CSS color; "none" removes edges. None uses black.
            edge_lw: Edge width in points; None uses 1.5 points.

        Returns:
            This builder; the shared renderer validates styles at to_chart.

        Raises:
            ValueError: If the resulting styles are invalid when rendered.
            NotImplementedError: If a style needs an unsupported renderer form.

        Example:
            >>> chart = plot.style(cmap="Blues", edge_color="none").to_chart()
        """
        self._options.update(
            {
                key: value
                for key, value in {
                    "cmap": cmap,
                    "edgecolor": "black" if edge_color is None else edge_color,
                    "linewidth": 1.5 if edge_lw is None else edge_lw,
                }.items()
                if value is not Undefined
            }
        )
        return self

    def legend(
        self,
        *,
        show: bool | None = True,
        title: str | None = "Expression\nlevel in group",
        width: float | None = 1.5,
    ) -> Self:
        """Set native color guide visibility, title and width.

        Args:
            show: False or None hides the color guide.
            title: Color guide title; None removes its title.
            width: Gradient length and figsize guide allowance in inches.

        Returns:
            This builder for further chaining.

        Raises:
            TypeError: If show is not boolean or None.
            ValueError: If a visible guide's width is not positive and finite.

        Example:
            >>> chart = plot.legend(title="Scaled mean", width=2).to_chart()
        """
        self._check_show(show)
        self._options.update(
            show_colorbar=bool(show),
            legend_width=self._track_size(width) if show else 0,
        )
        if show:
            self._options["colorbar_title"] = title
        return self

    def to_chart(self) -> TopLevelSpec:
        """Render the current settings as a detached, composable native chart.

        Returns:
            A fresh chart; later chains do not change this snapshot.

        Raises:
            ValueError: If the current styles or layout are invalid.
            NotImplementedError: If a style needs an unsupported renderer form.

        Example:
            >>> combined = plot.to_chart() | another_chart
        """
        from genome_spy.integrations.scanpy._matrixplot_chart import build_matrixplot

        colors, groups, _ = self._displayed()
        return build_matrixplot(
            colors.T if self._swapped else colors,
            groups,
            swap_axes=self._swapped,
            value_title=self._value_title,
            tree=self._tree if self._extra == "dendrogram" else None,
            tree_size=self._extra_size,
            totals=self._totals(),
            **self._options,
        )

    def show(self, *, return_axes: bool | None = None) -> None:
        """Display one native chart using the notebook widget.

        Args:
            return_axes: Only None/False; use to_chart for a composable result.

        Returns:
            None, preventing a duplicate notebook output.

        Raises:
            TypeError: If return_axes requests Matplotlib axes.

        Example:
            >>> plot.style(cmap="viridis").show()
        """
        if return_axes is not None and return_axes is not False:
            raise TypeError(
                "gsc.pl.MatrixPlot: return_axes is omitted; use to_chart() for the native chart."
            )
        self.to_chart().display()
