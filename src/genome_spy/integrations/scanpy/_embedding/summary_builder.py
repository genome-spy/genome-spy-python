"""A small builder for native brush-linked expression summaries."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace
from typing import TYPE_CHECKING, Any, Literal, Self

from genome_spy.integrations.scanpy._guards import _require_scanpy
from genome_spy.schemapi import Undefined, UndefinedType

if TYPE_CHECKING:
    from anndata import AnnData

    from genome_spy import TopLevelSpec

Side = Literal["left", "right", "top", "bottom"]
_CONTEXT = "gsc.pl.EmbeddingSummary"


def _positive(value: float, name: str) -> float:
    """Return a positive dimension, rejecting zero with the caller's option name."""
    from genome_spy.integrations.scanpy._data import number

    result = number(value, name, context=_CONTEXT)
    if result == 0:
        raise ValueError(f"{_CONTEXT}: {name} must be positive.")
    return result


def _side(value: Side) -> Side:
    """Return a supported side so panels can be placed without fallback behavior."""
    if value not in ("left", "right", "top", "bottom"):
        raise ValueError(f"{_CONTEXT}: position must be left, right, top or bottom.")
    return value


def _title(value: str | None | UndefinedType, default: str) -> str | UndefinedType:
    """Return the requested title; omitted uses the default and None hides it."""
    if value is Undefined:
        return default
    if value is None:
        return Undefined
    if not isinstance(value, str):
        raise TypeError(f"{_CONTEXT}: title must be a string or None.")
    return value


class EmbeddingSummary:
    """Build an embedding with brush-linked expression summaries.

    Copy selected resident gene and observation values once. Chained methods change only
    presentation; native browser transforms recompute summaries as the brush moves.
    This GenomeSpy extension is not a Scanpy class. The embedding starts with equal
    coordinate units, and selected cells receive no additional point effects.

    Args:
        adata: AnnData with stored embedding coordinates and resident expression.
        var_names: Unique gene names; a string selects one gene.
        groupby: One categorical or string observation column.
        basis: Stored embedding name, with the usual direct/``X_`` lookup.
        use_raw: Use raw when available unless layer is specified.
        layer: Expression layer instead of raw/X.
        gene_symbols: Variable annotation column for gene lookup.
        categories_order: Complete cell-type order.
        palette: Existing embedding palette forms, including saved AnnData colors.
        obs_keys: Extra categorical/numeric observation columns copied once.
        title: Embedding title; omitted uses groupby, None hides it.
        show_count: Show the selected-cell count inside the brush; defaults to True.
        zoom: Enable embedding zoom and pan. Shift-drag selects cells when True;
            drag outside the selection to pan. False keeps ordinary drag selection.

    Returns:
        A mutable builder; construction does not display a plot.

    Raises:
        ImportError: If the supported Scanpy version is unavailable.
        TypeError: If inputs have unsupported types.
        ValueError: If genes, groups, coordinates or options are invalid.
        NotImplementedError: If expression is not resident or grouping is numeric.

    Example:
        >>> plot = gsc.pl.EmbeddingSummary(adata, ["CD3D", "LYZ"], "cell_type")
        >>> chart = plot.add_heatmap().add_histogram("LYZ").to_chart()
    """

    def __init__(
        self,
        adata: AnnData,
        var_names: str | Sequence[str],
        groupby: str,
        *,
        basis: str = "umap",
        use_raw: bool | None = None,
        layer: str | None = None,
        gene_symbols: str | None = None,
        categories_order: Sequence[str] | None = None,
        palette: Any = None,
        obs_keys: str | Sequence[str] = (),
        title: str | None | UndefinedType = Undefined,
        show_count: bool = True,
        zoom: bool = False,
    ) -> None:
        _require_scanpy(_CONTEXT)
        for name, value in {"show_count": show_count, "zoom": zoom}.items():
            if not isinstance(value, bool):
                raise TypeError(f"{_CONTEXT}: {name} must be boolean.")
        import pandas as pd
        from anndata import AnnData

        from genome_spy.integrations.scanpy._embedding.data import prepare_embedding
        from genome_spy.integrations.scanpy._data import check_value_limit
        from genome_spy.integrations.scanpy._embedding.summary_data import (
            prepare_observations,
        )
        from genome_spy.integrations.scanpy._expression.grouped_data import (
            MAX_HEATMAP_VALUES,
            grouped_expression,
        )

        if not isinstance(adata, AnnData):
            raise TypeError(f"{_CONTEXT}: expected AnnData.")
        names = [var_names] if isinstance(var_names, str) else var_names
        if (
            not isinstance(names, Sequence)
            or not names
            or any(not isinstance(name, str) or not name for name in names)
            or len(set(names)) != len(names)
        ):
            raise ValueError(f"{_CONTEXT}: var_names must contain unique gene names.")
        if not isinstance(groupby, str) or list(adata.obs.columns).count(groupby) != 1:
            raise ValueError(f"{_CONTEXT}: groupby must name one observation column.")
        self._title = _title(title, groupby)
        self._show_count = show_count
        self._zoom = zoom

        # Validate extra annotations before copying any expression values.
        keys = [obs_keys] if isinstance(obs_keys, str) else obs_keys
        if (
            not isinstance(keys, Sequence)
            or any(
                not isinstance(key, str) or list(adata.obs.columns).count(key) != 1
                for key in keys
            )
            or len(set(keys)) != len(keys)
        ):
            raise ValueError(
                f"{_CONTEXT}: obs_keys must name distinct observation columns."
            )
        keys = [key for key in keys if key != groupby]
        check_value_limit(
            adata.n_obs, len(names) + len(keys), MAX_HEATMAP_VALUES, context=_CONTEXT
        )
        groups = adata.obs[groupby]
        if not isinstance(groups.dtype, pd.CategoricalDtype) and (
            pd.api.types.is_numeric_dtype(groups.dtype)
            or not all(isinstance(value, str) for value in groups.dropna())
        ):
            raise NotImplementedError(f"{_CONTEXT}: numeric grouping is unsupported.")
        if any(name in adata.obs for name in names):
            raise ValueError(
                f"{_CONTEXT}: var_names must select genes, not obs columns."
            )

        # Read selected genes once; linked summaries reuse this detached table.
        expression = grouped_expression(
            adata,
            names,
            groupby,
            use_raw=use_raw,
            layer=layer,
            gene_symbols=gene_symbols,
            categories_order=categories_order,
        )
        prepared = prepare_embedding(
            adata,
            basis=basis,
            color=groupby,
            mask_obs=None,
            gene_symbols=None,
            use_raw=False,
            layer=None,
            groups=None,
            components=None,
            dimensions=None,
            size=12,
            marker="o",
            palette=palette,
            cmap=None,
            na_color="lightgray",
            na_in_legend=False,
            sort_order=True,
            vmin=None,
            vmax=None,
            vcenter=None,
            title=None,
            obs_id=None,
            colorbar_loc="right",
        )
        table = prepared.table
        table["_group"] = [
            None if pd.isna(value) else str(value) for value in expression.values.index
        ]
        self._genes = list(names)
        self._fields = {gene: f"_expr_{i}" for i, gene in enumerate(names)}
        for gene, field in self._fields.items():
            table[field] = expression.values[gene].to_numpy(copy=True)
        self._groups = [str(value) for value in expression.values.index.categories]
        if not self._groups:
            raise ValueError(f"{_CONTEXT}: groupby needs at least one category.")
        panel = prepared.panels[0]
        if categories_order is not None:
            palette_by_group = (
                dict(zip(panel.domain, panel.palette, strict=True))
                if panel.scheme is None
                else {}
            )
            ordered = [
                *self._groups,
                *[value for value in panel.domain if value not in self._groups],
            ]
            panel = replace(
                panel,
                domain=tuple(ordered),
                legend_values=tuple(self._groups),
                palette=tuple(palette_by_group[group] for group in ordered)
                if panel.scheme is None
                else (),
            )
        self._prepared = replace(prepared, panels=(panel,))
        self._observations = prepare_observations(adata, keys, groupby, self._prepared)
        self._groupby = groupby
        self._heatmap: dict[str, Any] | None = None
        self._tracks: dict[str, Any] | None = None
        self._histograms: dict[Side, dict[str, Any]] = {}
        self._composition: dict[str, Any] | None = None
        self._size = 320.0
        self._point_size = 12.0
        self._alpha = 0.85
        self._spacing = 12.0
        self._legend_position: Side = "bottom"
        self._legend_show = True

    def _subset(self, names: str | Sequence[str] | None) -> list[str]:
        """Return requested genes in order, rejecting names absent from the builder."""
        if names is None:
            result = self._genes[:]
        elif isinstance(names, str):
            result = [names]
        else:
            result = list(names)
        if (
            not result
            or any(name not in self._fields for name in result)
            or len(set(result)) != len(result)
        ):
            raise ValueError(
                f"{_CONTEXT}: panel genes must be a unique subset of var_names."
            )
        return result

    def add_heatmap(
        self,
        var_names: str | Sequence[str] | None = None,
        *,
        show: bool = True,
        position: Side = "right",
        width: float = 300,
        height: float = 160,
        cmap: str = "seurat",
        vmin: float | None = None,
        vmax: float | None = None,
        title: str | None | UndefinedType = Undefined,
        show_values: bool = False,
        gene_controls: bool = False,
    ) -> Self:
        """Enable or replace the selected-cell group-mean heatmap.

        Args:
            var_names: Subset of constructor genes, in display order; None uses all.
            show: False hides the panel.
            position: Side of the embedding composition.
            width: Minimum plot-area width; native concat aligns adjacent panels.
            height: Minimum plot-area height in logical pixels.
            cmap: Native scheme or zero-centered "seurat" preset.
            vmin: Fixed lower color limit; None derives it from loaded values.
            vmax: Fixed upper color limit; None derives it from loaded values.
            title: Panel title; omitted uses the summary label, None hides it.
            show_values: Show fitted group means with the shared native text style.
            gene_controls: Show one native gene selector per row, using constructor genes.

        Returns:
            This builder for further chaining.

        Raises:
            ValueError: If genes, placement or dimensions are invalid.
            TypeError: If show, show_values or gene_controls is not boolean.

        Example:
            >>> plot.add_heatmap(["LYZ"], position="bottom", vmin=-2.5, vmax=2.5)
        """
        if not isinstance(show, bool):
            raise TypeError(f"{_CONTEXT}: show must be boolean.")
        if not isinstance(show_values, bool):
            raise TypeError(f"{_CONTEXT}: show_values must be boolean.")
        if not isinstance(gene_controls, bool):
            raise TypeError(f"{_CONTEXT}: gene_controls must be boolean.")
        self._heatmap = (
            dict(
                genes=self._subset(var_names),
                position=_side(position),
                width=_positive(width, "width"),
                height=_positive(height, "height"),
                cmap=cmap,
                vmin=vmin,
                vmax=vmax,
                title=_title(title, "Selected cells: mean expression"),
                show_values=show_values,
                gene_controls=gene_controls,
            )
            if show
            else None
        )
        return self

    def add_tracks(
        self,
        var_names: str | Sequence[str] | None = None,
        *,
        show: bool = True,
        position: Side = "bottom",
        width: float = 600,
        height: float = 220,
        zoom: bool = True,
        group_gap: float = 0,
        spacing: float = 0,
        title: str | None | UndefinedType = Undefined,
    ) -> Self:
        """Add marker tracks that highlight cells selected in the embedding.

        Reuse the loaded expression without scaling or analysis. Cell order stays
        fixed by group; unselected cells fade and clearing restores the full tracks.

        Args:
            var_names: Subset of constructor genes; None uses all.
            show: False hides the tracks panel.
            position: Side of the embedding composition.
            width: Track plotting width in logical pixels.
            height: Combined height of the gene tracks in logical pixels.
            zoom: Allow horizontal zoom and pan across all tracks.
            group_gap: Space between cell groups in pixels; zero removes gaps.
            spacing: Space between tracks and the category strip in pixels.
            title: Panel title; omitted uses "Marker expression", None hides it.

        Returns:
            This builder for further chaining.

        Raises:
            TypeError: If show or zoom is not boolean.
            ValueError: If genes, dimensions, placement or spacing are invalid.

        Example:
            >>> plot.add_tracks(["CD3D", "LYZ"], position="bottom")
        """
        from genome_spy.integrations.scanpy._data import number

        for name, value in {"show": show, "zoom": zoom}.items():
            if not isinstance(value, bool):
                raise TypeError(f"{_CONTEXT}: {name} must be boolean.")
        self._tracks = (
            dict(
                genes=self._subset(var_names),
                position=_side(position),
                width=_positive(width, "width"),
                height=_positive(height, "height"),
                zoom=zoom,
                group_gap=number(group_gap, "group_gap", context=_CONTEXT),
                spacing=number(spacing, "spacing", context=_CONTEXT),
                title=_title(title, "Marker expression"),
            )
            if show
            else None
        )
        return self

    def add_histogram(
        self,
        var_names: str | Sequence[str] | None = None,
        *,
        obs: str | None = None,
        show: bool = True,
        position: Side = "bottom",
        width: float = 300,
        height: float = 160,
        bin_width: float = 0.5,
        title: str | None | UndefinedType = Undefined,
        gene_controls: bool = False,
    ) -> Self:
        """Enable or replace selected-versus-all distributions on one side.

        Left/right histograms stack vertically; top/bottom histograms form a row.
        Calls on different sides keep both groups. Each group follows the same brush.

        Args:
            var_names: Constructor genes, one histogram each; None uses the first unless obs is set.
            obs: Stored numeric obs key from obs_keys, instead of var_names.
            show: False removes the histogram group on the requested side.
            position: Side of the embedding composition.
            width: Minimum plot-area width; native concat aligns adjacent panels.
            height: Minimum plot-area height of each histogram in logical pixels.
            bin_width: Positive fixed bin width shared by both cohorts.
            title: Panel title; omitted derives it from the field, None hides it.
            gene_controls: Show a native selector per gene histogram, using constructor genes.

        Returns:
            This builder for further chaining.

        Raises:
            ValueError: If genes, placement, dimensions or bin width are invalid.
            TypeError: If show or gene_controls is not boolean.

        Example:
            >>> plot.add_histogram("LYZ", bin_width=0.25)
        """
        if not isinstance(show, bool):
            raise TypeError(f"{_CONTEXT}: show must be boolean.")
        if not isinstance(gene_controls, bool):
            raise TypeError(f"{_CONTEXT}: gene_controls must be boolean.")
        if obs is not None:
            if gene_controls:
                raise ValueError(f"{_CONTEXT}: gene_controls requires gene histograms.")
            if var_names is not None:
                raise ValueError(f"{_CONTEXT}: choose var_names or obs, not both.")
            if (
                obs not in self._observations
                or self._observations[obs].color is not None
            ):
                raise ValueError(
                    f"{_CONTEXT}: obs must select a loaded numeric column."
                )
            field, label, kind = self._observations[obs].field, obs, "observation"
            genes = []
        else:
            genes = self._subset(self._genes[:1] if var_names is None else var_names)
            field, label, kind = (
                self._fields[genes[0]],
                f"{genes[0]} expression",
                "expression",
            )
        side = _side(position)
        if show:
            self._histograms[side] = dict(
                field=field,
                label=label,
                kind=kind,
                position=side,
                width=_positive(width, "width"),
                height=_positive(height, "height"),
                bin_width=_positive(bin_width, "bin_width"),
                title=_title(
                    title,
                    "Gene expression: selection vs all cells"
                    if gene_controls or len(genes) > 1
                    else f"{label}: selection vs all cells",
                ),
                genes=genes,
                gene_controls=gene_controls,
            )
        else:
            self._histograms.pop(side, None)
        return self

    def add_composition(
        self,
        key: str | None = None,
        *,
        show: bool = True,
        position: Side = "right",
        width: float = 200,
        height: float = 280,
        title: str | None | UndefinedType = Undefined,
    ) -> Self:
        """Enable or replace paired categorical cohort-percentage bars.

        Percentages use all cells in each cohort, including a visible NA category
        for missing metadata. Category order and colors stay fixed during brushing.

        Args:
            key: Categorical obs key from obs_keys; None uses groupby.
            show: False hides the panel.
            position: Side of the embedding composition.
            width: Minimum native plot-area width in logical pixels.
            height: Minimum native plot-area height in logical pixels.
            title: Panel title; omitted derives it from key, None hides it.

        Returns:
            This builder for further chaining.

        Raises:
            TypeError: If show is not boolean.
            ValueError: If the key, placement or dimensions are invalid.
            NotImplementedError: If missing categories need an unsupported palette.

        Example:
            >>> plot.add_composition("sample")
        """
        if not isinstance(show, bool):
            raise TypeError(f"{_CONTEXT}: show must be boolean.")
        key = self._groupby if key is None else key
        if show:
            if key not in self._observations or self._observations[key].color is None:
                raise ValueError(
                    f"{_CONTEXT}: composition needs a loaded categorical column."
                )
            observation = self._observations[key]
            assert observation.color is not None
            if (
                self._prepared.table[observation.field].eq("NA").any()
                and "NA" not in observation.color.to_dict()["domain"]
            ):
                raise NotImplementedError(
                    f"{_CONTEXT}: missing categories need an explicit palette."
                )
        self._composition = (
            dict(
                key=key,
                position=_side(position),
                width=_positive(width, "width"),
                height=_positive(height, "height"),
                title=_title(title, f"{key}: composition"),
            )
            if show
            else None
        )
        return self

    def style(
        self,
        *,
        umap_size: float | UndefinedType = Undefined,
        size: float | UndefinedType = Undefined,
        alpha: float | UndefinedType = Undefined,
        spacing: float | UndefinedType = Undefined,
    ) -> Self:
        """Update supplied embedding styles without reading AnnData again.

        Args:
            umap_size: Square plot-area side length in logical pixels.
            size: Point area in Scanpy's square-point units.
            alpha: Point opacity between zero and one.
            spacing: Native spacing between plots in logical pixels.

        Returns:
            This builder for further chaining.

        Raises:
            ValueError: If a supplied style is invalid.

        Example:
            >>> plot.style(umap_size=360, size=8, alpha=0.85)
        """
        from genome_spy.integrations.scanpy._data import number

        updates = {}
        for name, value in {
            "_size": umap_size,
            "_point_size": size,
            "_alpha": alpha,
            "_spacing": spacing,
        }.items():
            if value is not Undefined:
                updates[name] = number(value, name.lstrip("_"), context=_CONTEXT)
        if (
            updates.get("_size", self._size) == 0
            or updates.get("_alpha", self._alpha) > 1
        ):
            raise ValueError(f"{_CONTEXT}: umap_size must be positive and alpha <= 1.")
        for name, value in updates.items():
            setattr(self, name, value)
        return self

    def legend(self, *, position: Side = "bottom", show: bool = True) -> Self:
        """Collect the independent native legends around the whole composition.

        Args:
            position: Side of the composition for all legends.
            show: Whether to show collected legends.

        Returns:
            This builder for further chaining.

        Raises:
            ValueError: If position is invalid.
            TypeError: If show is not boolean.

        Example:
            >>> plot.legend(position="right")
        """
        if not isinstance(show, bool):
            raise TypeError(f"{_CONTEXT}: show must be boolean.")
        self._legend_position, self._legend_show = _side(position), show
        return self

    def to_chart(self) -> TopLevelSpec:
        """Return a fresh native chart without reading or retaining AnnData.

        Returns:
            A composable chart unaffected by later builder changes.

        Raises:
            ValueError: If a panel's current color settings are invalid.
            NotImplementedError: If a requested color scheme is unsupported.

        Example:
            >>> chart = plot.to_chart()
            >>> chart.save("expression.html", inline=True)
        """
        from genome_spy.integrations.scanpy._embedding.summary_chart import (
            build_summary,
        )

        return build_summary(
            self._prepared,
            self._fields,
            self._groups,
            heatmap=self._heatmap,
            tracks=self._tracks,
            histograms=list(self._histograms.values()),
            composition=self._composition,
            observations=self._observations,
            title=self._title,
            show_count=self._show_count,
            zoom=self._zoom,
            size=self._size,
            point_size=self._point_size,
            alpha=self._alpha,
            spacing=self._spacing,
            legend_position=self._legend_position,
            legend_show=self._legend_show,
        )

    def show(self) -> None:
        """Display the current chart using the native notebook widget.

        Returns:
            None, preventing duplicate notebook output.

        Raises:
            ValueError: If current panel settings are invalid.

        Example:
            >>> plot.add_heatmap().show()
        """
        self.to_chart().display()
