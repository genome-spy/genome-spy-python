"""A compact but growing Chart API for GenomeSpy core specifications."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any, ClassVar, Protocol, Self, Unpack, cast
from uuid import uuid4

from genome_spy._utils import JsonSpec, compact_json, pretty_json
from genome_spy._chart_authoring import (
    merge_encoding_definitions,
    normalize_data,
    normalize_transform,
    normalize_transform_kwarg,
)
from genome_spy.channels import Channel
from genome_spy.schema import (
    ConcatSpec,
    EncodingKwds,
    GenomeSpyConfig,
    HConcatSpec,
    LayerSpec,
    MARK_TYPES,
    Root,
    SCHEMA_VERSION,
    UnitSpec,
    VConcatSpec,
    ViewBackground,
)
from genome_spy.schema._kwds import (
    AxisResolveKwds,
    GenomeSpyConfigKwds,
    LegendResolveKwds,
    ScaleResolveKwds,
    ScalesKwds,
    ViewBackgroundKwds,
)
from genome_spy.schema.mixins import ConfigMethodMixin, MarkMethodMixin
from genome_spy.schemapi import (
    SchemaBase,
    Undefined,
    UndefinedType,
    merge_mapping_value,
    normalize_mapping_value,
    normalize_schema_value,
)

_CORE_DIST_URL = f"https://cdn.jsdelivr.net/npm/@genome-spy/core@{SCHEMA_VERSION}/dist"
DEFAULT_SCHEMA_URL = f"{_CORE_DIST_URL}/schema.json"
DEFAULT_EMBED_URL = f"{_CORE_DIST_URL}/bundle/index.es.js"


class _CopyableSpec(Protocol):
    def copy(self, *, deep: bool = True, **kwargs: Any) -> Any: ...


HTML_TEMPLATE = """
<div id="{container_id}"></div>
<script type="text/javascript">
  (function(spec, moduleUrl) {{
    let outputDiv = document.currentScript.previousElementSibling;
    if (!outputDiv || outputDiv.id !== "{container_id}") {{
      outputDiv = document.getElementById("{container_id}");
    }}

    function showError(error) {{
      outputDiv.innerHTML = (
        '<div style="color:red;">'
        + '<p>JavaScript Error: ' + error.message + '</p>'
        + '<p>GenomeSpy failed to render in this notebook frontend. '
        + 'See the browser console for details.</p>'
        + '</div>'
      );
      throw error;
    }}

    (async function() {{
      try {{
        const module = await import(moduleUrl);
        const embed = module.embed ?? module.default?.embed ?? module.default;
        if (typeof embed !== "function") {{
          throw new Error("GenomeSpy embed export was not found.");
        }}
        await embed(outputDiv, spec);
      }} catch (error) {{
        showError(error);
      }}
    }})();
  }})({spec_json}, {module_url_json});
</script>
""".strip()


def _infer_encoding_name(value: Channel | SchemaBase | str | dict[str, Any]) -> str:
    if isinstance(value, Channel) and value.encoding_name is not None:
        return value.encoding_name
    raise TypeError(
        "Positional encodings must be channel objects such as X(...), Y(...), "
        "Color(...), or Size(...)."
    )


def _merge_encoding_definitions(
    current_encoding: Any,
    updates: dict[str, Channel | SchemaBase | str | dict[str, Any] | None],
    *,
    data: Any,
) -> dict[str, Any]:
    return merge_encoding_definitions(current_encoding, updates, data=data)


class TopLevelSpec:
    """Shared behavior for top-level GenomeSpy specifications."""

    def with_config(
        self,
        value: GenomeSpyConfig | GenomeSpyConfigKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a copy with merged top-level ``config``."""
        merged = merge_mapping_value(
            self._kwds.get("config", Undefined),  # type: ignore[attr-defined]
            "config",
            value,
            **kwargs,
        )
        return cast(Self, cast(_CopyableSpec, self).copy(deep=False, config=merged))

    def with_view(
        self,
        value: ViewBackground | ViewBackgroundKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a copy with merged top-level ``view``."""
        merged = merge_mapping_value(
            self._kwds.get("view", Undefined),  # type: ignore[attr-defined]
            "view",
            value,
            **kwargs,
        )
        return cast(Self, cast(_CopyableSpec, self).copy(deep=False, view=merged))

    def with_scales(
        self,
        value: ScalesKwds | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a copy with merged top-level shared scales."""
        merged = merge_mapping_value(
            self._kwds.get("scales", Undefined),  # type: ignore[attr-defined]
            "scales",
            value,
            **kwargs,
        )
        return cast(Self, cast(_CopyableSpec, self).copy(deep=False, scales=merged))

    def _merged_encoding(
        self,
        args: tuple[Channel, ...],
        kwargs: dict[str, Channel | SchemaBase | str | dict[str, Any] | None],
    ) -> dict[str, Any]:
        """Return merged encoding definitions for fluent ``encode(...)`` calls."""
        updates = dict(kwargs)
        for arg in args:
            name = _infer_encoding_name(arg)
            if name in updates:
                raise TypeError(f"Encoding channel {name!r} was specified twice.")
            updates[name] = arg

        current_encoding = self._kwds.get("encoding", Undefined)  # type: ignore[attr-defined]
        data = self._kwds.get("data", Undefined)  # type: ignore[attr-defined]
        return _merge_encoding_definitions(current_encoding, updates, data=data)

    def _config_object(self) -> GenomeSpyConfig:
        """Return the current top-level config as a schema wrapper."""
        current = self._kwds.get("config", Undefined)  # type: ignore[attr-defined]
        if current is Undefined:
            return GenomeSpyConfig()
        if current is None:
            raise TypeError("Cannot configure nested properties into null 'config'.")
        if isinstance(current, GenomeSpyConfig):
            return current
        return GenomeSpyConfig(
            **normalize_mapping_value(current, key="config", validate=False)
        )

    def _configured_nested(
        self,
        name: str,
        value: SchemaBase | dict[str, Any] | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> GenomeSpyConfig:
        """Return a config object with one nested property updated."""
        return self._config_object()._with_property(name, value, **kwargs)

    def _configured_property(self, name: str, value: Any) -> GenomeSpyConfig:
        """Return a config object with one scalar property updated."""
        config = self._config_object()
        return config._with_property(name, value)

    def _configure_nested(
        self,
        name: str,
        value: SchemaBase | dict[str, Any] | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a copy with one nested config family updated."""
        return cast(
            Self,
            cast(_CopyableSpec, self).copy(
                deep=False, config=self._configured_nested(name, value, **kwargs)
            ),
        )

    def _configure_property(self, name: str, value: Any) -> Self:
        """Return a copy with one scalar config property updated."""
        return cast(
            Self,
            cast(_CopyableSpec, self).copy(
                deep=False, config=self._configured_property(name, value)
            ),
        )

    def properties(self, **kwargs: Any) -> Self:
        """Return a new spec with merged top-level properties."""
        return self._with_properties(kwargs)

    def _normalized_properties(self, properties: dict[str, Any]) -> dict[str, Any]:
        """Return top-level properties normalized for schema-backed copying."""
        return {
            key: normalize_schema_value(value, validate=False)
            for key, value in properties.items()
        }

    def _appended_transform(self, transform: dict[str, Any]) -> Self:
        """Return a copy with one normalized transform appended."""
        current = self._kwds.get("transform", Undefined)  # type: ignore[attr-defined]
        merged = [] if current is Undefined else list(current)
        merged.append(normalize_transform(transform))
        return cast(Self, cast(_CopyableSpec, self).copy(deep=False, transform=merged))

    def _configured(
        self,
        value: SchemaBase | dict[str, Any] | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        """Return a copy with top-level config merged."""
        merged = merge_mapping_value(
            self._kwds.get("config", Undefined),  # type: ignore[attr-defined]
            "config",
            value,
            **kwargs,
        )
        return cast(Self, cast(_CopyableSpec, self).copy(deep=False, config=merged))

    def _with_properties(self, properties: dict[str, Any]) -> Self:
        """Return a copy with normalized top-level properties applied."""
        return cast(
            Self,
            cast(_CopyableSpec, self).copy(
                deep=False,
                **self._normalized_properties(properties),
            ),
        )

    def _merged_resolution(
        self, key: str, updates: Mapping[str, Any]
    ) -> dict[str, Any]:
        """Return a merged composition ``resolve`` mapping."""
        current = self._kwds.get("resolve", Undefined)  # type: ignore[attr-defined]
        merged: dict[str, Any] = {} if current is Undefined else dict(current)
        current_values = merged.get(key, Undefined)
        merged_values: dict[str, Any] = (
            {} if current_values is Undefined else dict(current_values)
        )
        for name, value in updates.items():
            merged_values[name] = normalize_schema_value(value, validate=False)
        merged[key] = merged_values
        return merged

    def _with_resolution(self, key: str, updates: Mapping[str, Any]) -> Self:
        """Return a copy with one composition resolution family merged."""
        return cast(
            Self,
            cast(_CopyableSpec, self).copy(
                deep=False,
                resolve=self._merged_resolution(key, updates),
            ),
        )

    def _serialized_top_level_values(self) -> dict[str, Any]:
        """Return copied top-level state with authoring-edge values normalized."""
        values = dict(self._kwds)  # type: ignore[attr-defined]
        data = values.get("data", Undefined)
        if data is not Undefined:
            normalized_data = normalize_data(data)
            if normalized_data is None:
                values.pop("data")
            else:
                values["data"] = normalized_data
        return values

    def _validated_root_spec(
        self,
        spec: dict[str, Any],
        *,
        include_schema: bool,
        validate: bool,
    ) -> dict[str, Any]:
        """Return a root-validated spec dictionary ready for serialization."""
        if include_schema:
            spec["$schema"] = self._schema_url  # type: ignore[attr-defined]
        return Root(**spec).to_dict(validate=validate)

    def transform(self, *transforms: SchemaBase | dict[str, Any]) -> Self:
        """Add one or more arbitrary GenomeSpy transforms.

        Description:
            Use this generic method when GenomeSpy supports a transform that
            does not yet have a dedicated handwritten helper in the Python API.
            Each transform may be a raw mapping or a generated schema wrapper.

        Args:
            *transforms: One or more transform definitions.

        Returns:
            A new spec with the transforms appended in order.

        Raises:
            TypeError: If a transform is not a mapping or schema wrapper.

        Example:
            >>> chart.transform({"type": "collect", "sort": {"field": ["x"]}})
        """
        result = self
        for transform in transforms:
            result = result._append_transform(normalize_transform(transform))
        return result

    def transform_filter(self, expression: str) -> Self:
        """Add a filter transform using a GenomeSpy expression string."""
        return self._append_transform({"type": "filter", "expr": expression})

    def transform_collect(
        self, *, sort: SchemaBase | dict[str, Any] | None = None
    ) -> Self:
        """Add a collect transform."""
        transform: dict[str, Any] = {"type": "collect"}
        if sort is not None:
            transform["sort"] = normalize_transform_kwarg(sort, key="sort")
        return self._append_transform(transform)

    def transform_flatten(
        self,
        *,
        fields: list[str] | None = None,
        as_: list[str] | None = None,
        index: str | None = None,
    ) -> Self:
        """Add a flatten transform."""
        transform: dict[str, Any] = {"type": "flatten"}
        if fields is not None:
            transform["fields"] = fields
        if as_ is not None:
            transform["as"] = as_
        if index is not None:
            transform["index"] = index
        return self._append_transform(transform)

    def transform_flatten_compressed_exons(self, *, start: str) -> Self:
        """Add a flattenCompressedExons transform."""
        return self._append_transform(
            {"type": "flattenCompressedExons", "start": start}
        )

    def transform_flatten_delimited(
        self,
        *,
        field: str | list[str],
        separator: str | list[str],
        as_: str | list[str] | None = None,
    ) -> Self:
        """Split delimited fields into aligned rows."""
        transform: dict[str, Any] = {
            "type": "flattenDelimited",
            "field": field,
            "separator": separator,
        }
        if as_ is not None:
            transform["as"] = as_
        return self._append_transform(transform)

    def transform_formula(self, *, expr: str, as_: str) -> Self:
        """Add a formula transform."""
        return self._append_transform({"type": "formula", "expr": expr, "as": as_})

    def transform_regex_extract(self, *, field: str, regex: str, as_: str) -> Self:
        """Add a regexExtract transform."""
        return self._append_transform(
            {
                "type": "regexExtract",
                "field": field,
                "regex": regex,
                "as": as_,
            }
        )

    def transform_linearize_genomic_coordinate(
        self, *, chrom: str, pos: str, as_: str
    ) -> Self:
        """Add a linearizeGenomicCoordinate transform."""
        return self._append_transform(
            {
                "type": "linearizeGenomicCoordinate",
                "chrom": chrom,
                "pos": pos,
                "as": as_,
            }
        )

    def transform_measure_text(
        self,
        *,
        field: str,
        as_: str,
        fontSize: float | None = None,
        fontWeight: str | None = None,
        font: str | None = None,
    ) -> Self:
        """Add a measureText transform."""
        transform: dict[str, Any] = {
            "type": "measureText",
            "field": field,
            "as": as_,
        }
        if fontSize is not None:
            transform["fontSize"] = fontSize
        if fontWeight is not None:
            transform["fontWeight"] = fontWeight
        if font is not None:
            transform["font"] = font
        return self._append_transform(transform)

    def transform_flatten_sequence(
        self,
        *,
        field: str,
        as_: list[str] | None = None,
    ) -> Self:
        """Add a flattenSequence transform."""
        transform: dict[str, Any] = {
            "type": "flattenSequence",
            "field": field,
        }
        if as_ is not None:
            transform["as"] = as_
        return self._append_transform(transform)

    def transform_filter_scored_labels(
        self,
        *,
        lane: str,
        score: str,
        width: str,
        pos: str,
        padding: float | None = None,
    ) -> Self:
        """Add a filterScoredLabels transform."""
        transform: dict[str, Any] = {
            "type": "filterScoredLabels",
            "lane": lane,
            "score": score,
            "width": width,
            "pos": pos,
        }
        if padding is not None:
            transform["padding"] = padding
        return self._append_transform(transform)

    def transform_aggregate(
        self,
        *,
        groupby: list[str] | None = None,
        fields: list[str] | None = None,
        ops: list[str] | None = None,
        as_: list[str] | None = None,
    ) -> Self:
        """Add a GenomeSpy aggregate transform."""
        transform: dict[str, Any] = {"type": "aggregate"}
        if groupby is not None:
            transform["groupby"] = groupby
        if fields is not None:
            transform["fields"] = fields
        if ops is not None:
            transform["ops"] = ops
        if as_ is not None:
            transform["as"] = as_
        return self._append_transform(transform)

    def transform_coverage(
        self,
        *,
        start: str,
        end: str,
        as_: str,
        chrom: str | None = None,
    ) -> Self:
        """Add a coverage transform."""
        transform: dict[str, Any] = {
            "type": "coverage",
            "start": start,
            "end": end,
            "as": as_,
        }
        if chrom is not None:
            transform["chrom"] = chrom
        return self._append_transform(transform)

    def transform_pileup(
        self,
        *,
        start: str,
        end: str,
        as_: str,
        preference: str | None = None,
        preferredOrder: list[str] | None = None,
    ) -> Self:
        """Add a pileup transform."""
        transform: dict[str, Any] = {
            "type": "pileup",
            "start": start,
            "end": end,
            "as": as_,
        }
        if preference is not None:
            transform["preference"] = preference
        if preferredOrder is not None:
            transform["preferredOrder"] = preferredOrder
        return self._append_transform(transform)

    def transform_project(
        self, *, fields: list[str], as_: list[str] | None = None
    ) -> Self:
        """Add a project transform."""
        transform: dict[str, Any] = {"type": "project", "fields": fields}
        if as_ is not None:
            transform["as"] = as_
        return self._append_transform(transform)

    def transform_stack(
        self,
        *,
        groupby: list[str],
        field: str | None = None,
        sort: SchemaBase | dict[str, Any] | None = None,
        offset: str | None = None,
        as_: list[str] | None = None,
        baseField: str | None = None,
    ) -> Self:
        """Add a GenomeSpy stack transform."""
        transform: dict[str, Any] = {"type": "stack", "groupby": groupby}
        if field is not None:
            transform["field"] = field
        if sort is not None:
            transform["sort"] = normalize_transform_kwarg(sort, key="sort")
        if offset is not None:
            transform["offset"] = offset
        if as_ is not None:
            transform["as"] = as_
        if baseField is not None:
            transform["baseField"] = baseField
        return self._append_transform(transform)

    def to_dict(
        self, *, include_schema: bool = True, validate: bool = True
    ) -> dict[str, Any]:
        """Serialize the spec to a JSON-compatible dictionary."""
        raise NotImplementedError

    @property
    def spec(self) -> JsonSpec:
        """Return the rendered GenomeSpy specification with JSON display."""
        return JsonSpec(self.to_dict())

    def to_json(self, *, include_schema: bool = True, validate: bool = True) -> str:
        """Serialize the spec to formatted JSON."""
        return pretty_json(
            self.to_dict(include_schema=include_schema, validate=validate)
        )

    def __str__(self) -> str:
        """Print charts as the JSON spec for notebook/debugging workflows."""
        return self.to_json()

    def to_html(
        self,
        *,
        bundle_url: str = DEFAULT_EMBED_URL,
        container_id: str | None = None,
    ) -> str:
        """Render the spec as a small self-contained HTML snippet."""
        container_id = container_id or f"genome-spy-{uuid4().hex}"
        spec_json = compact_json(self.to_dict())
        module_url_json = compact_json(bundle_url)
        return HTML_TEMPLATE.format(
            container_id=container_id,
            spec_json=spec_json,
            module_url_json=module_url_json,
        )

    def save(self, path: str | Path, *, format: str | None = None) -> None:
        """Save the spec as JSON or HTML based on suffix or explicit format."""
        output_path = Path(path)
        file_format = format or output_path.suffix.lstrip(".")
        if file_format == "json":
            output_path.write_text(self.to_json() + "\n", encoding="utf-8")
            return
        if file_format == "html":
            output_path.write_text(self.to_html() + "\n", encoding="utf-8")
            return
        raise ValueError("Unsupported format. Use 'json' or 'html'.")

    def widget(
        self,
        *,
        bundle_url: str = DEFAULT_EMBED_URL,
        embed_options: dict[str, Any] | None = None,
    ) -> Any:
        """Create a notebook widget for the spec."""
        from genome_spy.jupyter import JupyterChart

        return JupyterChart(
            self,
            bundle_url=bundle_url,
            embed_options=embed_options,
        )

    def _repr_mimebundle_(
        self,
        include: object | None = None,
        exclude: object | None = None,
    ) -> object:
        """Display the spec through the anywidget notebook renderer."""
        del include, exclude
        return self.widget()._repr_mimebundle_()

    def __add__(self, other: TopLevelSpec) -> LayerChart:
        return layer(self, other)

    def __or__(self, other: TopLevelSpec) -> HConcatChart:
        return hconcat(self, other)

    def __and__(self, other: TopLevelSpec) -> VConcatChart:
        return vconcat(self, other)

    def _append_transform(self, transform: dict[str, Any]) -> Self:
        raise NotImplementedError


class Chart(TopLevelSpec, ConfigMethodMixin, MarkMethodMixin, UnitSpec):
    """An immutable-style builder backed by generated ``UnitSpec`` state."""

    def __init__(
        self,
        data: Any = Undefined,
        mark: str | dict[str, Any] | UndefinedType = Undefined,
        encoding: EncodingKwds | UndefinedType = Undefined,
        *,
        properties_map: dict[str, Any] | None = None,
        transform: list[dict[str, Any]] | UndefinedType = Undefined,
        schema_url: str = DEFAULT_SCHEMA_URL,
        **kwargs: Any,
    ) -> None:
        if properties_map:
            kwargs = {**properties_map, **kwargs}
        UnitSpec.__init__(
            self,
            data=data,
            mark=cast(Any, mark),
            encoding=cast(Any, encoding),
            transform=transform,
            **kwargs,
        )
        self._schema_url = schema_url

    def copy(self, *, deep: bool = True, **kwargs: Any) -> Self:
        """Return a schema-backed copy while preserving the schema URL."""
        copied = super().copy(deep=deep, **kwargs)
        copied._schema_url = self._schema_url
        return copied

    def mark_circle(self, **kwargs: Any) -> Chart:
        """Set the mark to a point, whose default GenomeSpy shape is a circle."""
        return self._with_mark("point", **kwargs)

    def encode(
        self,
        *args: Channel,
        **kwargs: Channel | SchemaBase | str | dict[str, Any] | None,
    ) -> Chart:
        """Return a new chart with merged channel encodings."""
        merged = self._merged_encoding(args, kwargs)
        return self.copy(deep=False, encoding=merged)

    def to_dict(
        self, *, include_schema: bool = True, validate: bool = True
    ) -> dict[str, Any]:
        """Serialize and optionally validate the complete chart specification."""
        values = self._serialized_top_level_values()
        spec = UnitSpec(**values).to_dict(validate=False)
        return self._validated_root_spec(
            spec,
            include_schema=include_schema,
            validate=validate,
        )

    def _with_mark(self, mark_type: str, **kwargs: Any) -> Chart:
        if mark_type not in MARK_TYPES:
            raise ValueError(f"Unsupported mark type: {mark_type}")
        mark: str | dict[str, Any]
        if kwargs:
            mark = {"type": mark_type, **kwargs}
        else:
            mark = mark_type
        return self.copy(deep=False, mark=mark)

    def _append_transform(self, transform: dict[str, Any]) -> Self:
        return self._appended_transform(transform)

    def _configure(
        self,
        value: SchemaBase | dict[str, Any] | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        return self._configured(value, **kwargs)


class _CompositionSpec(TopLevelSpec, ConfigMethodMixin):
    _schema_spec_cls: ClassVar[type]
    _children_key: ClassVar[str]
    _kwds: dict[str, Any]
    _schema_url: str

    def copy(self, *, deep: bool = True, **kwargs: Any) -> Self:
        """Return a schema-backed copy while preserving the schema URL."""
        copied = cast(Self, SchemaBase.copy(cast(Any, self), deep=deep, **kwargs))
        copied._schema_url = self._schema_url
        return copied

    def to_dict(
        self, *, include_schema: bool = True, validate: bool = True
    ) -> dict[str, Any]:
        values = self._serialized_top_level_values()
        children = values.get(self._children_key, Undefined)
        if children is not Undefined:
            values[self._children_key] = [
                child.to_dict(include_schema=False, validate=False)
                for child in children
            ]
        spec = self._schema_spec_cls(**values).to_dict(validate=False)
        return self._validated_root_spec(
            spec,
            include_schema=include_schema,
            validate=validate,
        )

    def _append_transform(self, transform: dict[str, Any]) -> Self:
        return self._appended_transform(transform)

    def _configure(
        self,
        value: SchemaBase | dict[str, Any] | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        return self._configured(value, **kwargs)

    def encode(
        self,
        *args: Channel,
        **kwargs: Channel | SchemaBase | str | dict[str, Any] | None,
    ) -> Self:
        """Return a copy with merged top-level encodings for composed specs."""
        merged = self._merged_encoding(args, kwargs)
        return self.copy(deep=False, encoding=merged)

    def resolve_axis(self, **kwargs: Unpack[AxisResolveKwds]) -> Self:
        """Return a copy with merged composition-level axis resolutions."""
        return self._with_resolution("axis", kwargs)

    def resolve_scale(self, **kwargs: Unpack[ScaleResolveKwds]) -> Self:
        """Return a copy with merged composition-level scale resolutions."""
        return self._with_resolution("scale", kwargs)

    def resolve_legend(self, **kwargs: Unpack[LegendResolveKwds]) -> Self:
        """Return a copy with merged composition-level legend resolutions."""
        return self._with_resolution("legend", kwargs)


class LayerChart(_CompositionSpec, LayerSpec):
    """A layered GenomeSpy specification."""

    _schema_spec_cls = LayerSpec
    _children_key = "layer"

    def __init__(
        self,
        layer: list[TopLevelSpec] | UndefinedType = Undefined,
        *,
        schema_url: str = DEFAULT_SCHEMA_URL,
        **kwargs: Any,
    ) -> None:
        LayerSpec.__init__(self, layer=cast(Any, layer), **kwargs)
        self._schema_url = schema_url

    def __add__(self, other: TopLevelSpec) -> LayerChart:
        current = self._kwds.get("layer", Undefined)
        merged = [] if current is Undefined else list(current)
        merged.append(other)
        return self.copy(deep=False, layer=merged)


class HConcatChart(_CompositionSpec, HConcatSpec):
    """A horizontally concatenated GenomeSpy specification."""

    _schema_spec_cls = HConcatSpec
    _children_key = "hconcat"

    def __init__(
        self,
        hconcat: list[TopLevelSpec] | UndefinedType = Undefined,
        *,
        schema_url: str = DEFAULT_SCHEMA_URL,
        **kwargs: Any,
    ) -> None:
        HConcatSpec.__init__(self, hconcat=cast(Any, hconcat), **kwargs)
        self._schema_url = schema_url

    def __or__(self, other: TopLevelSpec) -> HConcatChart:
        current = self._kwds.get("hconcat", Undefined)
        merged = [] if current is Undefined else list(current)
        merged.append(other)
        return self.copy(deep=False, hconcat=merged)


class VConcatChart(_CompositionSpec, VConcatSpec):
    """A vertically concatenated GenomeSpy specification."""

    _schema_spec_cls = VConcatSpec
    _children_key = "vconcat"

    def __init__(
        self,
        vconcat: list[TopLevelSpec] | UndefinedType = Undefined,
        *,
        schema_url: str = DEFAULT_SCHEMA_URL,
        **kwargs: Any,
    ) -> None:
        VConcatSpec.__init__(self, vconcat=cast(Any, vconcat), **kwargs)
        self._schema_url = schema_url

    def __and__(self, other: TopLevelSpec) -> VConcatChart:
        current = self._kwds.get("vconcat", Undefined)
        merged = [] if current is Undefined else list(current)
        merged.append(other)
        return self.copy(deep=False, vconcat=merged)


class ConcatChart(_CompositionSpec, ConcatSpec):
    """A grid-concatenated GenomeSpy specification."""

    _schema_spec_cls = ConcatSpec
    _children_key = "concat"

    def __init__(
        self,
        concat: list[TopLevelSpec] | UndefinedType = Undefined,
        columns: int | UndefinedType = Undefined,
        *,
        schema_url: str = DEFAULT_SCHEMA_URL,
        **kwargs: Any,
    ) -> None:
        ConcatSpec.__init__(
            self,
            concat=cast(Any, concat),
            columns=columns,
            **kwargs,
        )
        self._schema_url = schema_url


def layer(*charts: TopLevelSpec, **kwargs: Any) -> LayerChart:
    """Compose a layered chart from multiple child charts."""
    return LayerChart(layer=list(charts), **kwargs)


def hconcat(*charts: TopLevelSpec, **kwargs: Any) -> HConcatChart:
    """Compose a horizontally concatenated chart."""
    return HConcatChart(hconcat=list(charts), **kwargs)


def vconcat(*charts: TopLevelSpec, **kwargs: Any) -> VConcatChart:
    """Compose a vertically concatenated chart."""
    return VConcatChart(vconcat=list(charts), **kwargs)


def concat(*charts: TopLevelSpec, columns: int, **kwargs: Any) -> ConcatChart:
    """Compose a grid concatenation."""
    return ConcatChart(concat=list(charts), columns=columns, **kwargs)
