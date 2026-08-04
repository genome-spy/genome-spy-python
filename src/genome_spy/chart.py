"""A compact but growing Chart API for GenomeSpy core specifications."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from typing import Any, ClassVar, Protocol, Self, Unpack, cast
from uuid import uuid4

from genome_spy._utils import JsonSpec, compact_json, pretty_json
from genome_spy._chart_authoring import (
    merge_encoding_definitions,
    normalize_data,
    normalize_transform,
)
from genome_spy.channels import Channel
from genome_spy.schema import (
    ConcatSpec,
    EncodingKwds,
    ExprRef,
    FadedMultiscaleStops,
    GenomeSpyConfig,
    HConcatSpec,
    ImportSpec,
    LayerSpec,
    MARK_TYPES,
    MultiscaleSpec,
    Root,
    SCHEMA_VERSION,
    TemplateImport,
    TransitionedMultiscaleStops,
    UnitSpec,
    UrlImport,
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
from genome_spy.schema.mixins import (
    ConfigMethodMixin,
    MarkMethodMixin,
    TransformMethodMixin,
)
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


class _SerializableView(Protocol):
    def to_dict(
        self, *, include_schema: bool = True, validate: bool = True
    ) -> dict[str, Any]: ...


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
    updates: dict[
        str,
        Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None,
    ],
    *,
    data: Any,
) -> dict[str, Any]:
    return merge_encoding_definitions(current_encoding, updates, data=data)


class TopLevelSpec(TransformMethodMixin):
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
        kwargs: dict[
            str,
            Channel
            | SchemaBase
            | str
            | dict[str, Any]
            | Sequence[Channel | SchemaBase | str | dict[str, Any]]
            | None,
        ],
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
        normalized: dict[str, Any] = {}
        for key, value in properties.items():
            if key == "templates" and isinstance(value, Mapping):
                normalized[key] = {
                    name: (
                        template.to_dict(include_schema=False, validate=False)
                        if isinstance(template, TopLevelSpec)
                        else normalize_schema_value(template, validate=False)
                    )
                    for name, template in value.items()
                }
            else:
                normalized[key] = normalize_schema_value(value, validate=False)
        return normalized

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

    @classmethod
    def from_dict(
        cls, spec: Mapping[str, Any], *, validate: bool = True
    ) -> TopLevelSpec:
        """Construct a renderable chart from a GenomeSpy specification.

        Args:
            spec: Complete GenomeSpy specification.
            validate: Validate the input against the generated root schema.

        Returns:
            A chart matching the specification's structural root variant.

        Raises:
            SchemaValidationError: If validation fails.
            TypeError: If the specification is not a mapping.
            ValueError: If no supported root structure is present.

        Example:
            >>> chart = TopLevelSpec.from_dict({"mark": "point"})
        """
        if not isinstance(spec, Mapping):
            raise TypeError(
                f"GenomeSpy specification must be a mapping, got {type(spec)!r}"
            )

        values = deepcopy(dict(spec))
        if validate:
            Root(**values).to_dict()

        schema_url = values.pop("$schema", DEFAULT_SCHEMA_URL)
        if not isinstance(schema_url, str):
            raise TypeError("The $schema property must be a string.")
        return cast(
            TopLevelSpec,
            _view_from_dict(values, schema_url=schema_url, allow_import=False),
        )

    @classmethod
    def from_json(cls, json_string: str, *, validate: bool = True) -> TopLevelSpec:
        """Construct a renderable chart from a JSON specification.

        Args:
            json_string: JSON-encoded GenomeSpy specification.
            validate: Validate the input against the generated root schema.

        Returns:
            A chart matching the specification's structural root variant.

        Raises:
            json.JSONDecodeError: If ``json_string`` is invalid JSON.
            SchemaValidationError: If schema validation fails.
            TypeError: If the decoded value is not a mapping.
            ValueError: If no supported root structure is present.

        Example:
            >>> chart = TopLevelSpec.from_json('{"mark": "point"}')
        """
        decoded = json.loads(json_string)
        if not isinstance(decoded, dict):
            raise TypeError("GenomeSpy JSON specification must decode to an object.")
        return cls.from_dict(decoded, validate=validate)

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

    def __add__(self, other: _SerializableView) -> LayerChart:
        return layer(self, other)

    def __or__(self, other: _SerializableView) -> HConcatChart:
        return hconcat(self, other)

    def __and__(self, other: _SerializableView) -> VConcatChart:
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
        **kwargs: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None,
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
        **kwargs: Channel
        | SchemaBase
        | str
        | dict[str, Any]
        | Sequence[Channel | SchemaBase | str | dict[str, Any]]
        | None,
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
        layer: list[_SerializableView] | UndefinedType = Undefined,
        *,
        schema_url: str = DEFAULT_SCHEMA_URL,
        **kwargs: Any,
    ) -> None:
        LayerSpec.__init__(self, layer=cast(Any, layer), **kwargs)
        self._schema_url = schema_url

    def __add__(self, other: _SerializableView) -> LayerChart:
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
        hconcat: list[_SerializableView] | UndefinedType = Undefined,
        *,
        schema_url: str = DEFAULT_SCHEMA_URL,
        **kwargs: Any,
    ) -> None:
        HConcatSpec.__init__(self, hconcat=cast(Any, hconcat), **kwargs)
        self._schema_url = schema_url

    def __or__(self, other: _SerializableView) -> HConcatChart:
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
        vconcat: list[_SerializableView] | UndefinedType = Undefined,
        *,
        schema_url: str = DEFAULT_SCHEMA_URL,
        **kwargs: Any,
    ) -> None:
        VConcatSpec.__init__(self, vconcat=cast(Any, vconcat), **kwargs)
        self._schema_url = schema_url

    def __and__(self, other: _SerializableView) -> VConcatChart:
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
        concat: list[_SerializableView] | UndefinedType = Undefined,
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


class MultiscaleChart(_CompositionSpec, MultiscaleSpec):
    """A semantic-zoom composition backed by generated schema state."""

    _schema_spec_cls = MultiscaleSpec
    _children_key = "multiscale"

    def __init__(
        self,
        multiscale: list[_SerializableView] | UndefinedType = Undefined,
        stops: Sequence[float | ExprRef | dict[str, Any]]
        | FadedMultiscaleStops
        | dict[str, Any]
        | TransitionedMultiscaleStops
        | UndefinedType = Undefined,
        *,
        schema_url: str = DEFAULT_SCHEMA_URL,
        **kwargs: Any,
    ) -> None:
        MultiscaleSpec.__init__(
            self,
            multiscale=cast(Any, multiscale),
            stops=stops,
            **kwargs,
        )
        self._schema_url = schema_url


class ImportedView(ImportSpec):
    """A child-view import that can participate in chart composition."""

    def __init__(
        self,
        import_: UrlImport
        | dict[str, Any]
        | TemplateImport
        | UndefinedType = Undefined,
        **kwargs: Any,
    ) -> None:
        ImportSpec.__init__(self, import_=cast(Any, import_), **kwargs)

    def to_dict(
        self, *, include_schema: bool = False, validate: bool = True
    ) -> dict[str, Any]:
        """Serialize the imported child view without a root schema URL.

        Args:
            include_schema: Accepted for composition compatibility; imports
                never emit a root ``$schema`` property.
            validate: Validate against the generated import schema.

        Returns:
            The JSON-compatible imported-view specification.

        Raises:
            SchemaValidationError: If validation fails.

        Example:
            >>> ImportedView(import_={"template": "track"}).to_dict()
            {'import': {'template': 'track'}}
        """
        del include_schema
        return ImportSpec(**self._kwds).to_dict(validate=validate)

    def __add__(self, other: _SerializableView) -> LayerChart:
        """Layer this imported view with another view."""
        return LayerChart(layer=[self, other])

    def __and__(self, other: _SerializableView) -> VConcatChart:
        """Vertically concatenate this imported view with another view."""
        return VConcatChart(vconcat=[self, other])

    def __or__(self, other: _SerializableView) -> HConcatChart:
        """Horizontally concatenate this imported view with another view."""
        return HConcatChart(hconcat=[self, other])


def _view_from_dict(
    values: dict[str, Any],
    *,
    schema_url: str,
    allow_import: bool,
) -> TopLevelSpec | ImportedView:
    if allow_import and "import" in values:
        import_definition = values.pop("import")
        return ImportedView(import_=import_definition, **values)

    for structural_key in (
        "mark",
        "layer",
        "multiscale",
        "vconcat",
        "hconcat",
        "concat",
    ):
        if structural_key not in values:
            continue
        if structural_key == "mark":
            return Chart(schema_url=schema_url, **values)

        raw_children = values.pop(structural_key)
        if not isinstance(raw_children, list):
            raise TypeError(f"{structural_key} must be a list of view specifications.")
        children: list[_SerializableView] = []
        for child in raw_children:
            if not isinstance(child, Mapping):
                raise TypeError(
                    f"{structural_key} children must be mappings, got {type(child)!r}"
                )
            children.append(
                _view_from_dict(
                    deepcopy(dict(child)),
                    schema_url=schema_url,
                    allow_import=True,
                )
            )
        if structural_key == "layer":
            return LayerChart(layer=children, schema_url=schema_url, **values)
        if structural_key == "multiscale":
            return MultiscaleChart(multiscale=children, schema_url=schema_url, **values)
        if structural_key == "vconcat":
            return VConcatChart(vconcat=children, schema_url=schema_url, **values)
        if structural_key == "hconcat":
            return HConcatChart(hconcat=children, schema_url=schema_url, **values)
        return ConcatChart(concat=children, schema_url=schema_url, **values)

    if "import" in values:
        raise ValueError("An imported view must be nested inside a composition.")
    raise ValueError("GenomeSpy specification has no supported structural root.")


def layer(*charts: _SerializableView, **kwargs: Any) -> LayerChart:
    """Compose a layered chart from multiple child charts."""
    return LayerChart(layer=list(charts), **kwargs)


def hconcat(*charts: _SerializableView, **kwargs: Any) -> HConcatChart:
    """Compose a horizontally concatenated chart."""
    return HConcatChart(hconcat=list(charts), **kwargs)


def vconcat(*charts: _SerializableView, **kwargs: Any) -> VConcatChart:
    """Compose a vertically concatenated chart."""
    return VConcatChart(vconcat=list(charts), **kwargs)


def concat(*charts: _SerializableView, columns: int, **kwargs: Any) -> ConcatChart:
    """Compose a grid concatenation."""
    return ConcatChart(concat=list(charts), columns=columns, **kwargs)


def multiscale(
    *charts: _SerializableView,
    stops: Sequence[float | ExprRef | dict[str, Any]]
    | FadedMultiscaleStops
    | dict[str, Any]
    | TransitionedMultiscaleStops,
    **kwargs: Any,
) -> MultiscaleChart:
    """Compose semantic-zoom levels using a multiscale view.

    Args:
        *charts: Views ordered from overview to detail.
        stops: Zoom thresholds controlling transitions between levels.
        **kwargs: Additional multiscale view properties.

    Returns:
        A renderable multiscale chart.

    Raises:
        SchemaValidationError: If the resulting specification is invalid when
            serialized.

    Example:
        >>> multiscale(Chart(mark="rect"), Chart(mark="text"), stops=[1])
    """
    return MultiscaleChart(multiscale=list(charts), stops=stops, **kwargs)


def import_view(
    *,
    url: str | UndefinedType = Undefined,
    template: str | UndefinedType = Undefined,
    **kwargs: Any,
) -> ImportedView:
    """Create an imported child view from a URL or template.

    Args:
        url: URL of a GenomeSpy specification to import.
        template: Name of a template in the current view hierarchy.
        **kwargs: Import-site properties such as ``params`` or ``visible``.

    Returns:
        An imported view for use in a composition.

    Raises:
        ValueError: If neither or both import sources are supplied.

    Example:
        >>> view = import_view(template="allele-track", params={"allele": "ref"})
    """
    if (url is Undefined) == (template is Undefined):
        raise ValueError("Specify exactly one of url or template.")
    import_definition = {"url": url} if url is not Undefined else {"template": template}
    return ImportedView(import_=import_definition, **kwargs)
