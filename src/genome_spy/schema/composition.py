"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""

from __future__ import annotations
from collections.abc import Sequence
from typing import Any, cast, Literal

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genome_spy.chart import (
        ConcatChart,
        HConcatChart,
        ImportedView,
        LayerChart,
        MultiscaleChart,
        TopLevelSpec,
        VConcatChart,
    )

from genome_spy.schema._typing import BuiltInThemeName_T
from genome_spy.schema._kwds import (
    AxesKwds,
    DynamicOpacityKwds,
    EncodingKwds,
    GenomeSpyConfigKwds,
    LegendsKwds,
    PaddingsKwds,
    ResolveKwds,
    ScalesKwds,
    SeparatorPropsKwds,
    SizeDefKwds,
    StepKwds,
    TitleKwds,
    ViewBackgroundKwds,
)
from genome_spy.schemapi import Undefined, UndefinedType
from genome_spy.schema import core


def layer(
    *charts: TopLevelSpec | ImportedView,
    assembly: str | UndefinedType = Undefined,
    axes: AxesKwds | UndefinedType = Undefined,
    background: str | UndefinedType = Undefined,
    baseUrl: str | UndefinedType = Undefined,
    config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
    cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    data: Any | UndefinedType = Undefined,
    datasets: dict[str, Any] | UndefinedType = Undefined,
    description: str | Sequence[str] | UndefinedType = Undefined,
    domainInert: bool | UndefinedType = Undefined,
    encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
    genome: core.UrlGenomeConfig
    | dict[str, Any]
    | core.InlineGenomeConfig
    | core.GenomeConfigBase
    | UndefinedType = Undefined,
    genomes: dict[str, Any] | UndefinedType = Undefined,
    height: core.SizeDef
    | SizeDefKwds
    | float
    | core.Step
    | StepKwds
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
    legends: LegendsKwds | UndefinedType = Undefined,
    name: str | UndefinedType = Undefined,
    opacity: float
    | core.DynamicOpacity
    | DynamicOpacityKwds
    | core.ExprRef
    | dict[str, Any]
    | UndefinedType = Undefined,
    overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
    padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
    params: Sequence[
        core.PlainValueParameter
        | dict[str, Any]
        | core.TransitionedValueParameter
        | core.ExprParameter
        | core.SelectionParameter
        | core.RulerParameter
    ]
    | UndefinedType = Undefined,
    resolve: ResolveKwds | UndefinedType = Undefined,
    scales: ScalesKwds | UndefinedType = Undefined,
    templates: dict[str, Any] | UndefinedType = Undefined,
    theme: BuiltInThemeName_T
    | Sequence[BuiltInThemeName_T]
    | UndefinedType = Undefined,
    title: str | core.Title | TitleKwds | UndefinedType = Undefined,
    transform: Sequence[
        core.AlignmentMismatchesParams
        | dict[str, Any]
        | core.AggregateParams
        | core.CollectParams
        | core.CoverageParams
        | core.CoordinateLookupParams
        | core.CrossParams
        | core.FlattenDelimitedParams
        | core.FormulaParams
        | core.LookupParams
        | core.ExprFilterParams
        | core.SelectionFilterParams
        | core.FilterScoredLabelsParams
        | core.FlattenParams
        | core.FlattenCompressedExonsParams
        | core.FlattenCigarParams
        | core.FlattenSequenceParams
        | core.IdentifierParams
        | core.LinearizeGenomicCoordinateParams
        | core.MeasureTextParams
        | core.TruncateTextParams
        | core.PackLegendLabelsParams
        | core.MergeFacetsParams
        | core.PileupParams
        | core.ProjectParams
        | core.RegexExtractParams
        | core.RegexFoldParams
        | core.SampleParams
        | core.SetIntersectionParams
        | core.StackParams
        | core.WindowParams
    ]
    | UndefinedType = Undefined,
    view: core.ViewBackground | ViewBackgroundKwds | UndefinedType = Undefined,
    viewportHeight: core.SizeDef
    | SizeDefKwds
    | float
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
    viewportWidth: core.SizeDef
    | SizeDefKwds
    | float
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
    visible: bool | UndefinedType = Undefined,
    width: core.SizeDef
    | SizeDefKwds
    | float
    | core.Step
    | StepKwds
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
) -> LayerChart:
    """Return a layer composition of the given charts.

    Args:
        assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
        axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
        background (str): Background color of the canvas.
        baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
        config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
        cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
        data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
        datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
        description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
        domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
        encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
        genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
        genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
        height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
        legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
        name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
        opacity (float | DynamicOpacity | DynamicOpacityKwds | ExprRef | dict[str, Any]): Opacity of the view and all its children. This can be: - a fixed number between ``0`` and ``1`` - an expression reference (``ExprRef``) - a ``DynamicOpacity`` definition for zoom-dependent opacity Dynamic opacity is useful for semantic zooming where layers are faded in and out as the user zooms. Example: ```json "opacity": { "unitsPerPixel": [100000, 40000], "values": [0, 1] } ``` In this example, the view fades in while zooming in from 100 000 to 40 000 units per pixel. __Default value:__ ``1.0``
        overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
        padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
        params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
        resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
        scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
        templates (dict[str, Any]): Schema-defined ``templates`` property.
        theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
        title (str | Title | TitleKwds): View title.
        transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
        view (ViewBackground | ViewBackgroundKwds): Schema-defined ``view`` property.
        viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
        viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
        visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
        width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
    """
    properties = {
        "assembly": assembly,
        "axes": axes,
        "background": background,
        "baseUrl": baseUrl,
        "config": config,
        "cursor": cursor,
        "data": data,
        "datasets": datasets,
        "description": description,
        "domainInert": domainInert,
        "encoding": encoding,
        "genome": genome,
        "genomes": genomes,
        "height": height,
        "legends": legends,
        "name": name,
        "opacity": opacity,
        "overhang": overhang,
        "padding": padding,
        "params": params,
        "resolve": resolve,
        "scales": scales,
        "templates": templates,
        "theme": theme,
        "title": title,
        "transform": transform,
        "view": view,
        "viewportHeight": viewportHeight,
        "viewportWidth": viewportWidth,
        "visible": visible,
        "width": width,
    }
    defined: dict[str, Any] = {
        key: value for key, value in properties.items() if value is not Undefined
    }
    from genome_spy.chart import LayerChart

    return LayerChart(layer=cast(Any, list(charts)), **defined)


def hconcat(
    *charts: TopLevelSpec | ImportedView,
    assembly: str | UndefinedType = Undefined,
    axes: AxesKwds | UndefinedType = Undefined,
    background: str | UndefinedType = Undefined,
    baseUrl: str | UndefinedType = Undefined,
    config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
    cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    data: Any | UndefinedType = Undefined,
    datasets: dict[str, Any] | UndefinedType = Undefined,
    description: str | Sequence[str] | UndefinedType = Undefined,
    domainInert: bool | UndefinedType = Undefined,
    encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
    genome: core.UrlGenomeConfig
    | dict[str, Any]
    | core.InlineGenomeConfig
    | core.GenomeConfigBase
    | UndefinedType = Undefined,
    genomes: dict[str, Any] | UndefinedType = Undefined,
    height: core.SizeDef
    | SizeDefKwds
    | float
    | core.Step
    | StepKwds
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
    legends: LegendsKwds | UndefinedType = Undefined,
    name: str | UndefinedType = Undefined,
    overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
    padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
    params: Sequence[
        core.PlainValueParameter
        | dict[str, Any]
        | core.TransitionedValueParameter
        | core.ExprParameter
        | core.SelectionParameter
        | core.RulerParameter
    ]
    | UndefinedType = Undefined,
    resolve: ResolveKwds | UndefinedType = Undefined,
    scales: ScalesKwds | UndefinedType = Undefined,
    separator: bool
    | core.SeparatorProps
    | SeparatorPropsKwds
    | UndefinedType = Undefined,
    spacing: float | UndefinedType = Undefined,
    templates: dict[str, Any] | UndefinedType = Undefined,
    theme: BuiltInThemeName_T
    | Sequence[BuiltInThemeName_T]
    | UndefinedType = Undefined,
    title: str | core.Title | TitleKwds | UndefinedType = Undefined,
    transform: Sequence[
        core.AlignmentMismatchesParams
        | dict[str, Any]
        | core.AggregateParams
        | core.CollectParams
        | core.CoverageParams
        | core.CoordinateLookupParams
        | core.CrossParams
        | core.FlattenDelimitedParams
        | core.FormulaParams
        | core.LookupParams
        | core.ExprFilterParams
        | core.SelectionFilterParams
        | core.FilterScoredLabelsParams
        | core.FlattenParams
        | core.FlattenCompressedExonsParams
        | core.FlattenCigarParams
        | core.FlattenSequenceParams
        | core.IdentifierParams
        | core.LinearizeGenomicCoordinateParams
        | core.MeasureTextParams
        | core.TruncateTextParams
        | core.PackLegendLabelsParams
        | core.MergeFacetsParams
        | core.PileupParams
        | core.ProjectParams
        | core.RegexExtractParams
        | core.RegexFoldParams
        | core.SampleParams
        | core.SetIntersectionParams
        | core.StackParams
        | core.WindowParams
    ]
    | UndefinedType = Undefined,
    viewportHeight: core.SizeDef
    | SizeDefKwds
    | float
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
    viewportWidth: core.SizeDef
    | SizeDefKwds
    | float
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
    visible: bool | UndefinedType = Undefined,
    width: core.SizeDef
    | SizeDefKwds
    | float
    | core.Step
    | StepKwds
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
) -> HConcatChart:
    """Return a hconcat composition of the given charts.

    Args:
        assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
        axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
        background (str): Background color of the canvas.
        baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
        config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
        cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
        data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
        datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
        description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
        domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
        encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
        genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
        genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
        height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
        legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
        name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
        overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
        padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
        params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
        resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
        scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
        separator (bool | SeparatorProps | SeparatorPropsKwds): Draws separator rules between visible child views. The separators are centered within the spacing gaps and do not affect layout. If ``true``, the defaults are equivalent to: ``{"type":"rule","size":1,"color":"#ccc","opacity":1,"strokeDash":[4,4],"strokeCap":"butt"}`` Use ``includePlotMargin`` to control whether the separators extend into the plot margin. __Default value:__ ``false``
        spacing (float): The gap between the views, in pixels.
        templates (dict[str, Any]): Schema-defined ``templates`` property.
        theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
        title (str | Title | TitleKwds): View title.
        transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
        viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
        viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
        visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
        width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
    """
    properties = {
        "assembly": assembly,
        "axes": axes,
        "background": background,
        "baseUrl": baseUrl,
        "config": config,
        "cursor": cursor,
        "data": data,
        "datasets": datasets,
        "description": description,
        "domainInert": domainInert,
        "encoding": encoding,
        "genome": genome,
        "genomes": genomes,
        "height": height,
        "legends": legends,
        "name": name,
        "overhang": overhang,
        "padding": padding,
        "params": params,
        "resolve": resolve,
        "scales": scales,
        "separator": separator,
        "spacing": spacing,
        "templates": templates,
        "theme": theme,
        "title": title,
        "transform": transform,
        "viewportHeight": viewportHeight,
        "viewportWidth": viewportWidth,
        "visible": visible,
        "width": width,
    }
    defined: dict[str, Any] = {
        key: value for key, value in properties.items() if value is not Undefined
    }
    from genome_spy.chart import HConcatChart

    return HConcatChart(hconcat=cast(Any, list(charts)), **defined)


def vconcat(
    *charts: TopLevelSpec | ImportedView,
    assembly: str | UndefinedType = Undefined,
    axes: AxesKwds | UndefinedType = Undefined,
    background: str | UndefinedType = Undefined,
    baseUrl: str | UndefinedType = Undefined,
    config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
    cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    data: Any | UndefinedType = Undefined,
    datasets: dict[str, Any] | UndefinedType = Undefined,
    description: str | Sequence[str] | UndefinedType = Undefined,
    domainInert: bool | UndefinedType = Undefined,
    encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
    genome: core.UrlGenomeConfig
    | dict[str, Any]
    | core.InlineGenomeConfig
    | core.GenomeConfigBase
    | UndefinedType = Undefined,
    genomes: dict[str, Any] | UndefinedType = Undefined,
    height: core.SizeDef
    | SizeDefKwds
    | float
    | core.Step
    | StepKwds
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
    legends: LegendsKwds | UndefinedType = Undefined,
    name: str | UndefinedType = Undefined,
    overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
    padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
    params: Sequence[
        core.PlainValueParameter
        | dict[str, Any]
        | core.TransitionedValueParameter
        | core.ExprParameter
        | core.SelectionParameter
        | core.RulerParameter
    ]
    | UndefinedType = Undefined,
    resolve: ResolveKwds | UndefinedType = Undefined,
    scales: ScalesKwds | UndefinedType = Undefined,
    separator: bool
    | core.SeparatorProps
    | SeparatorPropsKwds
    | UndefinedType = Undefined,
    spacing: float | UndefinedType = Undefined,
    templates: dict[str, Any] | UndefinedType = Undefined,
    theme: BuiltInThemeName_T
    | Sequence[BuiltInThemeName_T]
    | UndefinedType = Undefined,
    title: str | core.Title | TitleKwds | UndefinedType = Undefined,
    transform: Sequence[
        core.AlignmentMismatchesParams
        | dict[str, Any]
        | core.AggregateParams
        | core.CollectParams
        | core.CoverageParams
        | core.CoordinateLookupParams
        | core.CrossParams
        | core.FlattenDelimitedParams
        | core.FormulaParams
        | core.LookupParams
        | core.ExprFilterParams
        | core.SelectionFilterParams
        | core.FilterScoredLabelsParams
        | core.FlattenParams
        | core.FlattenCompressedExonsParams
        | core.FlattenCigarParams
        | core.FlattenSequenceParams
        | core.IdentifierParams
        | core.LinearizeGenomicCoordinateParams
        | core.MeasureTextParams
        | core.TruncateTextParams
        | core.PackLegendLabelsParams
        | core.MergeFacetsParams
        | core.PileupParams
        | core.ProjectParams
        | core.RegexExtractParams
        | core.RegexFoldParams
        | core.SampleParams
        | core.SetIntersectionParams
        | core.StackParams
        | core.WindowParams
    ]
    | UndefinedType = Undefined,
    viewportHeight: core.SizeDef
    | SizeDefKwds
    | float
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
    viewportWidth: core.SizeDef
    | SizeDefKwds
    | float
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
    visible: bool | UndefinedType = Undefined,
    width: core.SizeDef
    | SizeDefKwds
    | float
    | core.Step
    | StepKwds
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
) -> VConcatChart:
    """Return a vconcat composition of the given charts.

    Args:
        assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
        axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
        background (str): Background color of the canvas.
        baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
        config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
        cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
        data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
        datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
        description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
        domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
        encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
        genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
        genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
        height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
        legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
        name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
        overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
        padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
        params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
        resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
        scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
        separator (bool | SeparatorProps | SeparatorPropsKwds): Draws separator rules between visible child views. The separators are centered within the spacing gaps and do not affect layout. If ``true``, the defaults are equivalent to: ``{"type":"rule","size":1,"color":"#ccc","opacity":1,"strokeDash":[4,4],"strokeCap":"butt"}`` Use ``includePlotMargin`` to control whether the separators extend into the plot margin. __Default value:__ ``false``
        spacing (float): The gap between the views, in pixels.
        templates (dict[str, Any]): Schema-defined ``templates`` property.
        theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
        title (str | Title | TitleKwds): View title.
        transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
        viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
        viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
        visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
        width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
    """
    properties = {
        "assembly": assembly,
        "axes": axes,
        "background": background,
        "baseUrl": baseUrl,
        "config": config,
        "cursor": cursor,
        "data": data,
        "datasets": datasets,
        "description": description,
        "domainInert": domainInert,
        "encoding": encoding,
        "genome": genome,
        "genomes": genomes,
        "height": height,
        "legends": legends,
        "name": name,
        "overhang": overhang,
        "padding": padding,
        "params": params,
        "resolve": resolve,
        "scales": scales,
        "separator": separator,
        "spacing": spacing,
        "templates": templates,
        "theme": theme,
        "title": title,
        "transform": transform,
        "viewportHeight": viewportHeight,
        "viewportWidth": viewportWidth,
        "visible": visible,
        "width": width,
    }
    defined: dict[str, Any] = {
        key: value for key, value in properties.items() if value is not Undefined
    }
    from genome_spy.chart import VConcatChart

    return VConcatChart(vconcat=cast(Any, list(charts)), **defined)


def concat(
    *charts: TopLevelSpec | ImportedView,
    columns: float,
    assembly: str | UndefinedType = Undefined,
    axes: AxesKwds | UndefinedType = Undefined,
    background: str | UndefinedType = Undefined,
    baseUrl: str | UndefinedType = Undefined,
    config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
    cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    data: Any | UndefinedType = Undefined,
    datasets: dict[str, Any] | UndefinedType = Undefined,
    description: str | Sequence[str] | UndefinedType = Undefined,
    domainInert: bool | UndefinedType = Undefined,
    encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
    genome: core.UrlGenomeConfig
    | dict[str, Any]
    | core.InlineGenomeConfig
    | core.GenomeConfigBase
    | UndefinedType = Undefined,
    genomes: dict[str, Any] | UndefinedType = Undefined,
    height: core.SizeDef
    | SizeDefKwds
    | float
    | core.Step
    | StepKwds
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
    legends: LegendsKwds | UndefinedType = Undefined,
    name: str | UndefinedType = Undefined,
    overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
    padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
    params: Sequence[
        core.PlainValueParameter
        | dict[str, Any]
        | core.TransitionedValueParameter
        | core.ExprParameter
        | core.SelectionParameter
        | core.RulerParameter
    ]
    | UndefinedType = Undefined,
    resolve: ResolveKwds | UndefinedType = Undefined,
    scales: ScalesKwds | UndefinedType = Undefined,
    separator: bool
    | core.SeparatorProps
    | SeparatorPropsKwds
    | UndefinedType = Undefined,
    spacing: float | UndefinedType = Undefined,
    templates: dict[str, Any] | UndefinedType = Undefined,
    theme: BuiltInThemeName_T
    | Sequence[BuiltInThemeName_T]
    | UndefinedType = Undefined,
    title: str | core.Title | TitleKwds | UndefinedType = Undefined,
    transform: Sequence[
        core.AlignmentMismatchesParams
        | dict[str, Any]
        | core.AggregateParams
        | core.CollectParams
        | core.CoverageParams
        | core.CoordinateLookupParams
        | core.CrossParams
        | core.FlattenDelimitedParams
        | core.FormulaParams
        | core.LookupParams
        | core.ExprFilterParams
        | core.SelectionFilterParams
        | core.FilterScoredLabelsParams
        | core.FlattenParams
        | core.FlattenCompressedExonsParams
        | core.FlattenCigarParams
        | core.FlattenSequenceParams
        | core.IdentifierParams
        | core.LinearizeGenomicCoordinateParams
        | core.MeasureTextParams
        | core.TruncateTextParams
        | core.PackLegendLabelsParams
        | core.MergeFacetsParams
        | core.PileupParams
        | core.ProjectParams
        | core.RegexExtractParams
        | core.RegexFoldParams
        | core.SampleParams
        | core.SetIntersectionParams
        | core.StackParams
        | core.WindowParams
    ]
    | UndefinedType = Undefined,
    viewportHeight: core.SizeDef
    | SizeDefKwds
    | float
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
    viewportWidth: core.SizeDef
    | SizeDefKwds
    | float
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
    visible: bool | UndefinedType = Undefined,
    width: core.SizeDef
    | SizeDefKwds
    | float
    | core.Step
    | StepKwds
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
) -> ConcatChart:
    """Return a concat composition of the given charts.

    Args:
        columns (float): The number of columns in the grid.
        assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
        axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
        background (str): Background color of the canvas.
        baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
        config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
        cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
        data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
        datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
        description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
        domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
        encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
        genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
        genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
        height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
        legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
        name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
        overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
        padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
        params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
        resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
        scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
        separator (bool | SeparatorProps | SeparatorPropsKwds): Draws separator rules between visible child views. The separators are centered within the spacing gaps and do not affect layout. If ``true``, the defaults are equivalent to: ``{"type":"rule","size":1,"color":"#ccc","opacity":1,"strokeDash":[4,4],"strokeCap":"butt"}`` Use ``includePlotMargin`` to control whether the separators extend into the plot margin. __Default value:__ ``false``
        spacing (float): The gap between the views, in pixels.
        templates (dict[str, Any]): Schema-defined ``templates`` property.
        theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
        title (str | Title | TitleKwds): View title.
        transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
        viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
        viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
        visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
        width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
    """
    properties = {
        "columns": columns,
        "assembly": assembly,
        "axes": axes,
        "background": background,
        "baseUrl": baseUrl,
        "config": config,
        "cursor": cursor,
        "data": data,
        "datasets": datasets,
        "description": description,
        "domainInert": domainInert,
        "encoding": encoding,
        "genome": genome,
        "genomes": genomes,
        "height": height,
        "legends": legends,
        "name": name,
        "overhang": overhang,
        "padding": padding,
        "params": params,
        "resolve": resolve,
        "scales": scales,
        "separator": separator,
        "spacing": spacing,
        "templates": templates,
        "theme": theme,
        "title": title,
        "transform": transform,
        "viewportHeight": viewportHeight,
        "viewportWidth": viewportWidth,
        "visible": visible,
        "width": width,
    }
    defined: dict[str, Any] = {
        key: value for key, value in properties.items() if value is not Undefined
    }
    from genome_spy.chart import ConcatChart

    return ConcatChart(concat=cast(Any, list(charts)), **defined)


def multiscale(
    *charts: TopLevelSpec | ImportedView,
    stops: Sequence[float | core.ExprRef | dict[str, Any]]
    | core.FadedMultiscaleStops
    | dict[str, Any]
    | core.TransitionedMultiscaleStops,
    assembly: str | UndefinedType = Undefined,
    axes: AxesKwds | UndefinedType = Undefined,
    background: str | UndefinedType = Undefined,
    baseUrl: str | UndefinedType = Undefined,
    config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
    cursor: str | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    data: Any | UndefinedType = Undefined,
    datasets: dict[str, Any] | UndefinedType = Undefined,
    description: str | Sequence[str] | UndefinedType = Undefined,
    domainInert: bool | UndefinedType = Undefined,
    encoding: core.Encoding | EncodingKwds | UndefinedType = Undefined,
    genome: core.UrlGenomeConfig
    | dict[str, Any]
    | core.InlineGenomeConfig
    | core.GenomeConfigBase
    | UndefinedType = Undefined,
    genomes: dict[str, Any] | UndefinedType = Undefined,
    height: core.SizeDef
    | SizeDefKwds
    | float
    | core.Step
    | StepKwds
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
    legends: LegendsKwds | UndefinedType = Undefined,
    name: str | UndefinedType = Undefined,
    opacity: float
    | core.DynamicOpacity
    | DynamicOpacityKwds
    | core.ExprRef
    | dict[str, Any]
    | UndefinedType = Undefined,
    overhang: core.OverhangConfig | dict[str, Any] | UndefinedType = Undefined,
    padding: core.Paddings | PaddingsKwds | float | UndefinedType = Undefined,
    params: Sequence[
        core.PlainValueParameter
        | dict[str, Any]
        | core.TransitionedValueParameter
        | core.ExprParameter
        | core.SelectionParameter
        | core.RulerParameter
    ]
    | UndefinedType = Undefined,
    resolve: ResolveKwds | UndefinedType = Undefined,
    scales: ScalesKwds | UndefinedType = Undefined,
    templates: dict[str, Any] | UndefinedType = Undefined,
    theme: BuiltInThemeName_T
    | Sequence[BuiltInThemeName_T]
    | UndefinedType = Undefined,
    title: str | core.Title | TitleKwds | UndefinedType = Undefined,
    transform: Sequence[
        core.AlignmentMismatchesParams
        | dict[str, Any]
        | core.AggregateParams
        | core.CollectParams
        | core.CoverageParams
        | core.CoordinateLookupParams
        | core.CrossParams
        | core.FlattenDelimitedParams
        | core.FormulaParams
        | core.LookupParams
        | core.ExprFilterParams
        | core.SelectionFilterParams
        | core.FilterScoredLabelsParams
        | core.FlattenParams
        | core.FlattenCompressedExonsParams
        | core.FlattenCigarParams
        | core.FlattenSequenceParams
        | core.IdentifierParams
        | core.LinearizeGenomicCoordinateParams
        | core.MeasureTextParams
        | core.TruncateTextParams
        | core.PackLegendLabelsParams
        | core.MergeFacetsParams
        | core.PileupParams
        | core.ProjectParams
        | core.RegexExtractParams
        | core.RegexFoldParams
        | core.SampleParams
        | core.SetIntersectionParams
        | core.StackParams
        | core.WindowParams
    ]
    | UndefinedType = Undefined,
    view: core.ViewBackground | ViewBackgroundKwds | UndefinedType = Undefined,
    viewportHeight: core.SizeDef
    | SizeDefKwds
    | float
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
    viewportWidth: core.SizeDef
    | SizeDefKwds
    | float
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
    visible: bool | UndefinedType = Undefined,
    width: core.SizeDef
    | SizeDefKwds
    | float
    | core.Step
    | StepKwds
    | core.ExprRef
    | dict[str, Any]
    | Literal["container"]
    | UndefinedType = Undefined,
) -> MultiscaleChart:
    """Return a multiscale composition of the given charts.

    Args:
        stops (Sequence[float | ExprRef | dict[str, Any]] | FadedMultiscaleStops | dict[str, Any] | TransitionedMultiscaleStops): Stop definition that controls transitions between the multiscale levels. - ``number[]`` is shorthand for ``{ metric: "unitsPerPixel", values: ... }`` - ``(number | ExprRef)[]`` supports mixed constants and expressions - Object form allows configuring metric, channel, and fade.
        assembly (str): Default assembly for locus scales that do not define ``scale.assembly``. Can reference either a key in ``genomes`` or a built-in assembly name.
        axes (AxesKwds): Defines properties for axis resolutions used by this view subtree. Use this when a composed view shares an axis across child views and the axis settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
        background (str): Background color of the canvas.
        baseUrl (str): The base URL for relative URL data sources and URL imports. The base URLs are inherited in the view hierarchy unless overridden with this property. By default, the top-level view's base URL equals to the visualization specification's base URL.
        config (GenomeSpyConfig | GenomeSpyConfigKwds): Configures defaults for this view subtree. Properties in child views override properties inherited from ancestors.
        cursor (str | ExprRef | dict[str, Any]): Mouse cursor shown while the pointer is inside the view. The deepest matching cursor wins: mark cursor first, then the pointed view, then ancestor views outward toward the root. __Default value:__ browser default
        data (Any): Specifies a data source. If omitted, the data source is inherited from the parent view.
        datasets (dict[str, Any]): Named datasets available to this view and its descendants. A descendant declaration with the same name shadows this declaration. Declare named data here to establish reliable lexical scope and enable scoped runtime updates.
        description (str | Sequence[str]): A description of the view. Can be used for documentation. The description of the top-level view is shown in the toolbar of the GenomeSpy App.
        domainInert (bool): If true, this view and its descendants do not contribute to scale domains. Child views inherit this flag automatically. **Default value:** ``false``
        encoding (Encoding | EncodingKwds): Specifies how data are encoded using the visual channels.
        genome (UrlGenomeConfig | dict[str, Any] | InlineGenomeConfig | GenomeConfigBase): Schema-defined ``genome`` property.
        genomes (dict[str, Any]): Named genome assembly definitions. Each object key is the assembly name.
        height (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Height of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default value:** ``"container"``
        legends (LegendsKwds): Defines properties for legend resolutions used by this view subtree. Use this when a composed view shares a legend across child views and the legend settings belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
        name (str): An explicit name used to address the view. It is recommended to keep names unique among siblings. In the App (where view state is bookmarkable), the name must be unique within its import scope for views with configurable visibility, etc.
        opacity (float | DynamicOpacity | DynamicOpacityKwds | ExprRef | dict[str, Any]): Opacity of the view and all its children. This can be: - a fixed number between ``0`` and ``1`` - an expression reference (``ExprRef``) - a ``DynamicOpacity`` definition for zoom-dependent opacity Dynamic opacity is useful for semantic zooming where layers are faded in and out as the user zooms. Example: ```json "opacity": { "unitsPerPixel": [100000, 40000], "values": [0, 1] } ``` In this example, the view fades in while zooming in from 100 000 to 40 000 units per pixel. __Default value:__ ``1.0``
        overhang (OverhangConfig | dict[str, Any]): Controls whether external overhang on each edge reserves layout space. Setting an edge to false lets axes, titles, legends, or custom view overhang overlap nearby content while remaining visible. **Default value:** all edges reserve overhang
        padding (Paddings | PaddingsKwds | float): Padding applied to the view. Accepts either a number representing pixels or an object specifying separate paddings for each edge. Examples: - ``padding: 10`` - ``padding: { top: 10, right: 20, bottom: 10, left: 20 }`` **Default value:** ``0``
        params (Sequence[PlainValueParameter | dict[str, Any] | TransitionedValueParameter | ExprParameter | SelectionParameter | RulerParameter]): Dynamic variables that parameterize a visualization.
        resolve (ResolveKwds): Specifies how scales, axes, and legends are resolved in the view hierarchy. If legend resolution is not configured explicitly, it follows the corresponding scale resolution.
        scales (ScalesKwds): Defines properties for scale resolutions used by this view subtree. Use this when a composed view shares a scale across child views and the scale settings, such as the visible domain, belong to the composed view rather than an individual encoding. An ancestor declaration shadows the whole declaration of a descendant that targets the same resolution. Declarations in separate sibling subtrees are ambiguous and cause an error.
        templates (dict[str, Any]): Schema-defined ``templates`` property.
        theme (BuiltInThemeName_T | Sequence[BuiltInThemeName_T]): Selects built-in theme preset(s) for the whole visualization.
        title (str | Title | TitleKwds): View title.
        transform (Sequence[AlignmentMismatchesParams | dict[str, Any] | AggregateParams | CollectParams | CoverageParams | CoordinateLookupParams | CrossParams | FlattenDelimitedParams | FormulaParams | LookupParams | ExprFilterParams | SelectionFilterParams | FilterScoredLabelsParams | FlattenParams | FlattenCompressedExonsParams | FlattenCigarParams | FlattenSequenceParams | IdentifierParams | LinearizeGenomicCoordinateParams | MeasureTextParams | TruncateTextParams | PackLegendLabelsParams | MergeFacetsParams | PileupParams | ProjectParams | RegexExtractParams | RegexFoldParams | SampleParams | SetIntersectionParams | StackParams | WindowParams]): An array of transformations applied to the data before visual encoding.
        view (ViewBackground | ViewBackgroundKwds): Schema-defined ``view`` property.
        viewportHeight (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport height of the view. If the view size exceeds the viewport height, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``height``)
        viewportWidth (SizeDef | SizeDefKwds | float | ExprRef | dict[str, Any] | Literal['container']): Optional viewport width of the view. If the view size exceeds the viewport width, it will be shown with scrollbars. This property implicitly enables clipping. If an expression reference is provided, it must resolve to a number or ``"container"``. **Default:** ``null`` (same as ``width``)
        visible (bool): The default visibility of the view. An invisible view is removed from the layout and not rendered. For context, see toggleable view visibility. **Default:** ``true``
        width (SizeDef | SizeDefKwds | float | Step | StepKwds | ExprRef | dict[str, Any] | Literal['container']): Width of the view. If a number, it is interpreted as pixels. If an expression reference is provided, it must resolve to a number or ``"container"``. Check child sizing for details. **Default:** ``"container"``
    """
    properties = {
        "stops": stops,
        "assembly": assembly,
        "axes": axes,
        "background": background,
        "baseUrl": baseUrl,
        "config": config,
        "cursor": cursor,
        "data": data,
        "datasets": datasets,
        "description": description,
        "domainInert": domainInert,
        "encoding": encoding,
        "genome": genome,
        "genomes": genomes,
        "height": height,
        "legends": legends,
        "name": name,
        "opacity": opacity,
        "overhang": overhang,
        "padding": padding,
        "params": params,
        "resolve": resolve,
        "scales": scales,
        "templates": templates,
        "theme": theme,
        "title": title,
        "transform": transform,
        "view": view,
        "viewportHeight": viewportHeight,
        "viewportWidth": viewportWidth,
        "visible": visible,
        "width": width,
    }
    defined: dict[str, Any] = {
        key: value for key, value in properties.items() if value is not Undefined
    }
    from genome_spy.chart import MultiscaleChart

    return MultiscaleChart(multiscale=cast(Any, list(charts)), **defined)


def import_view(
    *,
    url: str | UndefinedType = Undefined,
    template: str | UndefinedType = Undefined,
    config: core.GenomeSpyConfig | GenomeSpyConfigKwds | UndefinedType = Undefined,
    name: str | UndefinedType = Undefined,
    params: Sequence[
        core.PlainValueParameter
        | dict[str, Any]
        | core.TransitionedValueParameter
        | core.ExprParameter
        | core.SelectionParameter
        | core.RulerParameter
    ]
    | dict[str, Any]
    | UndefinedType = Undefined,
    visible: bool | UndefinedType = Undefined,
) -> ImportedView:
    """Create an imported child view from a URL or template."""
    if (url is Undefined) == (template is Undefined):
        raise ValueError("Specify exactly one of url or template.")
    properties = {
        "config": config,
        "name": name,
        "params": params,
        "visible": visible,
    }
    defined: dict[str, Any] = {
        key: value for key, value in properties.items() if value is not Undefined
    }
    import_definition = {"url": url} if url is not Undefined else {"template": template}
    from genome_spy.chart import ImportedView

    return ImportedView(import_=import_definition, **defined)


__all__ = ["layer", "hconcat", "vconcat", "concat", "multiscale", "import_view"]
