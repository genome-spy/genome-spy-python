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
    HConcatSpec,
    LayerSpec,
    MARK_TYPES,
    Root,
    SCHEMA_VERSION,
    UnitSpec,
    VConcatSpec,
)
from genome_spy.schema.mixins import MarkMethodMixin
from genome_spy.schemapi import SchemaBase, Undefined, UndefinedType

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
    records = _records_from_data(data)
    if records is not None:
        return {"values": _json_safe(records)}
    if hasattr(data, "to_dicts"):
        return {"values": _json_safe(data.to_dicts())}
    if isinstance(data, list):
        return {"values": data}
    if is_mapping(data):
        return dict(data)
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


def _infer_field_type(field: str, data: Any) -> str | None:
    records = _records_from_data(data)
    if not records:
        return None

    for row in records[:100]:
        if not is_mapping(row) or field not in row:
            continue
        value = row[field]
        if value is None:
            continue
        if isinstance(value, bool):
            return "nominal"
        if isinstance(value, int | float):
            return "quantitative"
        return "nominal"
    return None


def _normalize_channel(
    name: str, value: Channel | str | dict[str, Any], *, data: Any = None
) -> dict[str, Any]:
    definition = channel(value).to_dict()
    if "type" not in definition and isinstance(definition.get("field"), str):
        inferred_type = _infer_field_type(definition["field"], data)
        if inferred_type is not None:
            definition["type"] = inferred_type
    if name == "y":
        scale = definition.get("scale")
        if scale is None:
            definition["scale"] = dict(Y_SCALE_DEFAULTS)
        elif is_mapping(scale) and "reverse" not in scale:
            definition["scale"] = {**Y_SCALE_DEFAULTS, **scale}
    if name in {"x2", "y2"} and definition.get("type") == "locus":
        definition.pop("type")
    return definition


def _infer_encoding_name(value: Channel | str | dict[str, Any]) -> str:
    if isinstance(value, Channel) and value.encoding_name is not None:
        return value.encoding_name
    raise TypeError(
        "Positional encodings must be channel objects such as X(...), Y(...), "
        "Color(...), or Size(...)."
    )


def _normalize_transform(transform: dict[str, Any]) -> dict[str, Any]:
    if not is_mapping(transform):
        raise TypeError(f"Unsupported transform value: {type(transform)!r}")
    return dict(transform)


class TopLevelSpec:
    """Shared behavior for top-level GenomeSpy specifications."""

    def properties(self, **kwargs: Any) -> Self:
        """Return a new spec with merged top-level properties."""
        return self._with_properties(kwargs)

    def transform_filter(self, expression: str) -> Self:
        """Add a filter transform using a GenomeSpy expression string."""
        return self._append_transform({"type": "filter", "expr": expression})

    def transform_formula(self, *, expr: str, as_: str) -> Self:
        """Add a formula transform."""
        return self._append_transform({"type": "formula", "expr": expr, "as": as_})

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

    def transform_stack(
        self,
        *,
        groupby: list[str],
        field: str | None = None,
        sort: dict[str, Any] | None = None,
        offset: str | None = None,
        as_: list[str] | None = None,
    ) -> Self:
        """Add a GenomeSpy stack transform."""
        transform: dict[str, Any] = {"type": "stack", "groupby": groupby}
        if field is not None:
            transform["field"] = field
        if sort is not None:
            transform["sort"] = dict(sort)
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


class Chart(TopLevelSpec, MarkMethodMixin, UnitSpec):
    """An immutable-style builder backed by generated ``UnitSpec`` state."""

    def __init__(
        self,
        data: Any = Undefined,
        mark: str | dict[str, Any] | UndefinedType = Undefined,
        encoding: dict[str, dict[str, Any]] | UndefinedType = Undefined,
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
            mark=mark,
            encoding=encoding,
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
        **kwargs: Channel | str | dict[str, Any],
    ) -> Chart:
        """Return a new chart with merged channel encodings."""
        for arg in args:
            name = _infer_encoding_name(arg)
            if name in kwargs:
                raise TypeError(f"Encoding channel {name!r} was specified twice.")
            kwargs[name] = arg

        current_encoding = self._kwds.get("encoding", Undefined)
        merged = {} if current_encoding is Undefined else dict(current_encoding)
        data = self._kwds.get("data", Undefined)
        for name, value in kwargs.items():
            merged[name] = _normalize_channel(name, value, data=data)
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


class _CompositionSpec(TopLevelSpec):
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
        LayerSpec.__init__(self, layer=layer, **kwargs)
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
        HConcatSpec.__init__(self, hconcat=hconcat, **kwargs)
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
        VConcatSpec.__init__(self, vconcat=vconcat, **kwargs)
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
        ConcatSpec.__init__(self, concat=concat, columns=columns, **kwargs)
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
