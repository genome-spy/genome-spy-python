"""A compact but growing Chart API for GenomeSpy core specifications."""

from __future__ import annotations

import math
from datetime import date, datetime
from pathlib import Path
from typing import Any, ClassVar, Self, cast
from uuid import uuid4

from genome_spy._utils import JsonSpec, compact_json, is_mapping, pretty_json
from genome_spy.channels import Channel, channel
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
Y_SCALE_DEFAULTS = {"reverse": True}

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


def _normalize_data(data: Any) -> Any:
    if data is None:
        return None
    if isinstance(data, SchemaBase):
        return data.to_dict(validate=False)
    records = _records_from_data(data)
    if records is not None:
        return _records_data(records)
    if is_mapping(data):
        return cast(dict[str, Any], normalize_schema_value(data, validate=False))
    raise TypeError(f"Unsupported data value: {type(data)!r}")


def _json_safe(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, datetime | date):
        return value.isoformat()
    if not isinstance(value, str | bytes) and hasattr(value, "item"):
        try:
            item = value.item()
        except (AttributeError, TypeError, ValueError):
            item = value
        if item is not value:
            return _json_safe(item)
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if is_mapping(value):
        return {key: _json_safe(item) for key, item in value.items()}
    return value


def _records_from_data(data: Any) -> list[dict[str, Any]] | None:
    if isinstance(data, list):
        return data
    if hasattr(data, "to_dicts"):
        records = data.to_dicts()
        if isinstance(records, list):
            return records
        return None
    if is_mapping(data):
        values = data.get("values")
        if isinstance(values, list):
            return values
        return None
    if hasattr(data, "to_dict"):
        try:
            records = data.to_dict(orient="records")
        except TypeError:
            return None
        if isinstance(records, list):
            return records
    return None


def _records_data(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {"values": _json_safe(records)}


def _infer_field_type(field: str, data: Any) -> str | None:
    records = _records_from_data(data)
    if not records:
        return None

    for row in records[:100]:
        if not is_mapping(row) or field not in row:
            continue
        value = row[field]
        inferred_type = _infer_value_type(value)
        if inferred_type is not None:
            return inferred_type
    return None


def _infer_value_type(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return "nominal"
    if isinstance(value, int | float):
        return "quantitative"
    return "nominal"


def _normalize_channel(
    name: str,
    value: Channel | SchemaBase | str | dict[str, Any] | None,
    *,
    data: Any = None,
) -> dict[str, Any] | None:
    if value is None:
        return None
    definition = channel(value).to_dict()
    return _normalized_channel_definition(name, definition, data=data)


def _normalized_channel_definition(
    name: str,
    definition: dict[str, Any],
    *,
    data: Any = None,
) -> dict[str, Any]:
    normalized = dict(definition)
    # Secondary positional channels (x2/y2) only carry field/value in GenomeSpy's
    # schema; a `type` is invalid there, so never infer or keep one for them.
    if name in {"x2", "y2"}:
        normalized.pop("type", None)
    elif "type" not in normalized and isinstance(normalized.get("field"), str):
        inferred_type = _infer_field_type(normalized["field"], data)
        if inferred_type is not None:
            normalized["type"] = inferred_type
    if name == "y":
        normalized["scale"] = _normalized_y_scale(normalized.get("scale"))
    return normalized


def _normalized_y_scale(scale: Any) -> Any:
    if scale is None:
        return dict(Y_SCALE_DEFAULTS)
    if is_mapping(scale) and "reverse" not in scale:
        return {**Y_SCALE_DEFAULTS, **scale}
    return scale


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
    merged = {} if current_encoding is Undefined else dict(current_encoding)
    for name, value in updates.items():
        merged[name] = _normalize_channel(name, value, data=data)
    return merged


def _normalize_transform(transform: SchemaBase | dict[str, Any]) -> dict[str, Any]:
    try:
        return normalize_mapping_value(transform, key="transform", validate=False)
    except TypeError as error:
        raise TypeError(f"Unsupported transform value: {type(transform)!r}") from error


def _normalize_transform_kwarg(
    value: SchemaBase | dict[str, Any],
    *,
    key: str,
) -> dict[str, Any]:
    return normalize_mapping_value(value, key=key, validate=False)


class TopLevelSpec:
    """Shared behavior for top-level GenomeSpy specifications."""

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
        return self.copy(
            deep=False, config=self._configured_nested(name, value, **kwargs)
        )  # type: ignore[attr-defined, no-any-return]

    def _configure_property(self, name: str, value: Any) -> Self:
        """Return a copy with one scalar config property updated."""
        return self.copy(deep=False, config=self._configured_property(name, value))  # type: ignore[attr-defined, no-any-return]

    def properties(self, **kwargs: Any) -> Self:
        """Return a new spec with merged top-level properties."""
        return self._with_properties(
            {
                key: normalize_schema_value(value, validate=False)
                for key, value in kwargs.items()
            }
        )

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
            result = result._append_transform(_normalize_transform(transform))
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
            transform["sort"] = _normalize_transform_kwarg(sort, key="sort")
        return self._append_transform(transform)

    def transform_flatten(
        self,
        *,
        fields: list[str],
        as_: list[str] | None = None,
        index: str | None = None,
    ) -> Self:
        """Add a flatten transform."""
        transform: dict[str, Any] = {"type": "flatten", "fields": fields}
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

    def transform_formula(self, *, expr: str, as_: str) -> Self:
        """Add a formula transform."""
        return self._append_transform({"type": "formula", "expr": expr, "as": as_})

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
    ) -> Self:
        """Add a GenomeSpy stack transform."""
        transform: dict[str, Any] = {"type": "stack", "groupby": groupby}
        if field is not None:
            transform["field"] = field
        if sort is not None:
            transform["sort"] = _normalize_transform_kwarg(sort, key="sort")
        if offset is not None:
            transform["offset"] = offset
        if as_ is not None:
            transform["as"] = as_
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

    def _with_properties(self, properties: dict[str, Any]) -> Self:
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

    def properties(self, **kwargs: Any) -> Self:
        """Return a shallow copy with updated unit-spec properties."""
        return self.copy(deep=False, **kwargs)

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
        values = dict(self._kwds)
        data = values.get("data", Undefined)
        if data is not Undefined:
            normalized_data = _normalize_data(data)
            if normalized_data is None:
                values.pop("data")
            else:
                values["data"] = normalized_data
        spec = UnitSpec(**values).to_dict(validate=False)
        if include_schema:
            spec["$schema"] = self._schema_url
        return Root(**spec).to_dict(validate=validate)

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
        current = self._kwds.get("transform", Undefined)
        merged = [] if current is Undefined else list(current)
        merged.append(_normalize_transform(transform))
        return self.copy(deep=False, transform=merged)

    def _with_properties(self, properties: dict[str, Any]) -> Self:
        return self.copy(deep=False, **properties)

    def _configure(
        self,
        value: SchemaBase | dict[str, Any] | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        merged = merge_mapping_value(
            self._kwds.get("config", Undefined), "config", value, **kwargs
        )
        return self.copy(deep=False, config=merged)


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
        values = dict(self._kwds)
        children = values.get(self._children_key, Undefined)
        if children is not Undefined:
            values[self._children_key] = [
                child.to_dict(include_schema=False, validate=False)
                for child in children
            ]
        data = values.get("data", Undefined)
        if data is not Undefined:
            normalized_data = _normalize_data(data)
            if normalized_data is None:
                values.pop("data")
            else:
                values["data"] = normalized_data
        spec = self._schema_spec_cls(**values).to_dict(validate=False)
        if include_schema:
            spec["$schema"] = self._schema_url
        return Root(**spec).to_dict(validate=validate)

    def _append_transform(self, transform: dict[str, Any]) -> Self:
        current = self._kwds.get("transform", Undefined)
        merged = [] if current is Undefined else list(current)
        merged.append(_normalize_transform(transform))
        return self.copy(deep=False, transform=merged)

    def _with_properties(self, properties: dict[str, Any]) -> Self:
        return self.copy(deep=False, **properties)

    def _configure(
        self,
        value: SchemaBase | dict[str, Any] | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        merged = merge_mapping_value(
            self._kwds.get("config", Undefined), "config", value, **kwargs
        )
        return self.copy(deep=False, config=merged)

    def encode(
        self,
        *args: Channel,
        **kwargs: Channel | SchemaBase | str | dict[str, Any] | None,
    ) -> Self:
        """Return a copy with merged top-level encodings for composed specs."""
        merged = self._merged_encoding(args, kwargs)
        return self.copy(deep=False, encoding=merged)

    def resolve_axis(self, **kwargs: str | None) -> Self:
        """Return a copy with merged composition-level axis resolutions."""
        return self._merge_resolution("axis", kwargs)

    def resolve_scale(self, **kwargs: str | None) -> Self:
        """Return a copy with merged composition-level scale resolutions."""
        return self._merge_resolution("scale", kwargs)

    def resolve_legend(self, **kwargs: str | None) -> Self:
        """Return a copy with merged composition-level legend resolutions."""
        return self._merge_resolution("legend", kwargs)

    def _merge_resolution(self, key: str, updates: dict[str, Any]) -> Self:
        current = self._kwds.get("resolve", Undefined)
        merged: dict[str, Any] = {} if current is Undefined else dict(current)
        current_values = merged.get(key, Undefined)
        merged_values: dict[str, Any] = (
            {} if current_values is Undefined else dict(current_values)
        )
        for name, value in updates.items():
            if isinstance(value, SchemaBase):
                merged_values[name] = value.to_dict(validate=False)
            elif is_mapping(value):
                merged_values[name] = dict(value)
            else:
                merged_values[name] = value
        merged[key] = merged_values
        return self.copy(deep=False, resolve=merged)


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
