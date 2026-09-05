"""A compact but growing Chart API for GenomeSpy core specifications."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Protocol, Self, cast
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
    GenomeSpyConfig,
    HConcatSpec,
    ImportSpec,
    LayerSpec,
    MARK_TYPES,
    MultiscaleSpec,
    Root,
    SCHEMA_VERSION,
    UnitSpec,
    VConcatSpec,
)
from genome_spy.schema.mixins import (
    ConcatPropertiesMixin,
    ConfigMethodMixin,
    EncodingMethodMixin,
    HConcatPropertiesMixin,
    ImportedViewConstructorMixin,
    LayerPropertiesMixin,
    MarkMethodMixin,
    MultiscalePropertiesMixin,
    ResolutionMethodMixin,
    TopLevelMergeMixin,
    TransformMethodMixin,
    UnitPropertiesMixin,
    VConcatPropertiesMixin,
)
from genome_spy.schema.composition import (
    concat as _concat,
    hconcat as _hconcat,
    layer as _layer,
    multiscale as _multiscale,
    import_view as _import_view,
    vconcat as _vconcat,
)
from genome_spy.schemapi import (
    SchemaBase,
    Undefined,
    merge_mapping_value,
    normalize_mapping_value,
    normalize_schema_value,
)

if TYPE_CHECKING:
    from genome_spy._parameters import Parameter
    from genome_spy._render import _PreparedSpec

_CORE_DIST_URL = f"https://cdn.jsdelivr.net/npm/@genome-spy/core@{SCHEMA_VERSION}/dist"
DEFAULT_SCHEMA_URL = f"{_CORE_DIST_URL}/schema.json"
DEFAULT_EMBED_URL = f"{_CORE_DIST_URL}/bundle/index.es.js"


class _CopyableSpec(Protocol):
    def _copy(self, *, deep: bool = True, **kwargs: Any) -> Any: ...


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


def _parameter_declaration_identity(value: Parameter | SchemaBase) -> tuple[str, bool]:
    """Return a parameter declaration's name and explicit-name status."""
    from genome_spy._parameters import Parameter
    from genome_spy.schema.ergonomics import _PARAMETER_TYPES

    if isinstance(value, Parameter):
        return value.name, value.name_is_explicit
    if not isinstance(value, _PARAMETER_TYPES):
        raise TypeError(
            f"Expected a generated GenomeSpy parameter definition, got {type(value)!r}."
        )
    name = value.to_dict(validate=False).get("name")
    if not isinstance(name, str):
        raise TypeError("A parameter declaration must have a string name.")
    return name, True


class TopLevelSpec(TopLevelMergeMixin, EncodingMethodMixin, TransformMethodMixin):
    """Shared behavior for top-level GenomeSpy specifications."""

    _schema_spec_cls: ClassVar[type[SchemaBase]]
    _schema_url: str

    def _initialize_spec(
        self, *, properties: dict[str, Any], schema_url: str | None
    ) -> None:
        """Initialize generated schema state for a top-level specification."""
        self._schema_spec_cls.__init__(cast(Any, self), **properties)
        self._schema_url = DEFAULT_SCHEMA_URL if schema_url is None else schema_url

    def _merge_top_level(
        self, name: str, value: Any, /, properties: Mapping[str, Any]
    ) -> Self:
        """Return a copy with one top-level mapping property merged."""
        merged = merge_mapping_value(
            self._kwds.get(name, Undefined),  # type: ignore[attr-defined]
            name,
            value,
            **properties,
        )
        return cast(Self, cast(_CopyableSpec, self)._copy(deep=False, **{name: merged}))

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

    def _encode(
        self,
        args: tuple[Channel, ...],
        properties: dict[
            str,
            Channel
            | SchemaBase
            | str
            | dict[str, Any]
            | Sequence[Channel | SchemaBase | str | dict[str, Any]]
            | None,
        ],
    ) -> Self:
        """Return a copy with generated encoding arguments merged."""
        merged = self._merged_encoding(args, properties)
        return cast(
            Self,
            cast(_CopyableSpec, self)._copy(deep=False, encoding=merged),
        )

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
            cast(_CopyableSpec, self)._copy(
                deep=False, config=self._configured_nested(name, value, **kwargs)
            ),
        )

    def _configure_property(self, name: str, value: Any) -> Self:
        """Return a copy with one scalar config property updated."""
        return cast(
            Self,
            cast(_CopyableSpec, self)._copy(
                deep=False, config=self._configured_property(name, value)
            ),
        )

    def _properties(self, **kwargs: Any) -> Self:
        """Return a new spec with merged top-level properties."""
        return self._with_properties(kwargs)

    def _normalized_properties(self, properties: dict[str, Any]) -> dict[str, Any]:
        """Return top-level properties normalized for schema-backed copying."""
        normalized: dict[str, Any] = {}
        for key, value in properties.items():
            if key == "params" and isinstance(value, Sequence):
                normalized[key] = list(value)
            elif key == "templates" and isinstance(value, Mapping):
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

    def add_params(self, *params: Parameter | SchemaBase) -> Self:
        """Return a chart with parameter declarations appended.

        Parameter handles are unwrapped only when the chart is serialized, so
        the same handle can also be reused in expressions, conditions, and
        filters.

        Args:
            *params: Parameter handles or generated parameter definitions.

        Returns:
            A new chart with the declarations appended in argument order.

        Raises:
            TypeError: If an argument is not a parameter declaration.
            ValueError: If an explicit parameter name is declared twice.

        Example:
            >>> import genome_spy as gs
            >>> cutoff = gs.param("cutoff", value=0.5)
            >>> gs.Chart().add_params(cutoff).to_dict(validate=False)["params"]
            [{'name': 'cutoff', 'value': 0.5}]
        """
        from genome_spy._parameters import Parameter

        current = self._kwds.get("params", Undefined)  # type: ignore[attr-defined]
        declarations = [] if current is Undefined else list(current)
        names: dict[str, bool] = {}
        for declaration in declarations:
            name, explicit = _parameter_declaration_identity(declaration)
            names[name] = explicit

        for parameter in params:
            if not isinstance(parameter, Parameter | SchemaBase):
                raise TypeError(
                    "add_params() arguments must be parameter handles or generated "
                    f"schema definitions, got {type(parameter)!r}."
                )
            name, explicit = _parameter_declaration_identity(parameter)
            if name in names:
                if explicit or names[name]:
                    raise ValueError(f"Parameter name {name!r} is already declared.")
                continue
            names[name] = explicit
            declarations.append(parameter)
        return cast(
            Self, cast(_CopyableSpec, self)._copy(deep=False, params=declarations)
        )

    def _appended_transform(self, transform: dict[str, Any]) -> Self:
        """Return a copy with one normalized transform appended."""
        current = self._kwds.get("transform", Undefined)  # type: ignore[attr-defined]
        merged = [] if current is Undefined else list(current)
        merged.append(normalize_transform(transform))
        return cast(Self, cast(_CopyableSpec, self)._copy(deep=False, transform=merged))

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
        return cast(Self, cast(_CopyableSpec, self)._copy(deep=False, config=merged))

    def _with_properties(self, properties: dict[str, Any]) -> Self:
        """Return a copy with normalized top-level properties applied."""
        return cast(
            Self,
            cast(_CopyableSpec, self)._copy(
                deep=False,
                **self._normalized_properties(properties),
            ),
        )

    def _copy_with_properties(self, *, deep: bool, properties: dict[str, Any]) -> Self:
        """Return a copy with generated explicit top-level updates."""
        return cast(
            Self,
            cast(_CopyableSpec, self)._copy(
                deep=deep,
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
            cast(_CopyableSpec, self)._copy(
                deep=False,
                resolve=self._merged_resolution(key, updates),
            ),
        )

    def _serialized_top_level_values(
        self, *, normalize_chart_data: Callable[[Any], Any] = normalize_data
    ) -> dict[str, Any]:
        """Return copied top-level state with authoring-edge values normalized."""
        values = dict(self._kwds)  # type: ignore[attr-defined]
        data = values.get("data", Undefined)
        if data is not Undefined:
            normalized_data = normalize_chart_data(data)
            if normalized_data is None:
                values.pop("data")
            else:
                values["data"] = normalized_data
        params = values.get("params", Undefined)
        if params is not Undefined:
            from genome_spy._parameters import _unwrap_parameter

            values["params"] = [
                normalize_schema_value(_unwrap_parameter(param), validate=False)
                for param in params
            ]
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
            spec["$schema"] = self._schema_url
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

    def _to_dict(
        self,
        *,
        include_schema: bool,
        validate: bool,
        normalize_chart_data: Callable[[Any], Any],
    ) -> dict[str, Any]:
        """Serialize with a caller-provided data-normalization policy."""
        raise NotImplementedError

    def _prepare_render(self) -> _PreparedSpec:
        """Prepare this chart for a renderer that supports binary buffers."""
        from genome_spy._render import prepare_render

        return prepare_render(self)

    def _prepare_widget(self) -> Any:
        """Prepare this chart for live named-dataset widget updates."""
        from genome_spy._render import prepare_widget

        return prepare_widget(self)

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
        parameter_names: Sequence[str] = (),
        parameter_values: Mapping[str, Any] | None = None,
        enable_click_events: bool = False,
    ) -> Any:
        """Create a notebook widget for the spec.

        Args:
            bundle_url: GenomeSpy bundle URL used by the widget.
            embed_options: Options passed to GenomeSpy's ``embed`` function.
            parameter_names: Named GenomeSpy parameters synchronized with the
                widget's ``parameter_values`` trait.
            parameter_values: Initial values for the synchronized parameters.
            enable_click_events: Whether clicked mark data is synchronized to
                ``clicked_datum`` and ``click_revision``.

        Returns:
            An anywidget-backed :class:`JupyterChart`.
        """
        from genome_spy.jupyter import JupyterChart

        return JupyterChart(
            self,
            bundle_url=bundle_url,
            embed_options=embed_options,
            parameter_names=parameter_names,
            parameter_values=parameter_values,
            enable_click_events=enable_click_events,
        )

    def _repr_mimebundle_(
        self,
        include: object | None = None,
        exclude: object | None = None,
    ) -> object:
        """Display the spec through the anywidget notebook renderer."""
        del include, exclude
        return self.widget()._repr_mimebundle_()

    def __add__(self, other: TopLevelSpec | ImportedView) -> LayerChart:
        return layer(self, other)

    def __or__(self, other: TopLevelSpec | ImportedView) -> HConcatChart:
        return hconcat(self, other)

    def __and__(self, other: TopLevelSpec | ImportedView) -> VConcatChart:
        return vconcat(self, other)

    def _append_transform(self, transform: dict[str, Any]) -> Self:
        raise NotImplementedError


class Chart(  # type: ignore[misc]  # Generated copy narrows SchemaBase.copy updates.
    UnitPropertiesMixin, TopLevelSpec, ConfigMethodMixin, MarkMethodMixin, UnitSpec
):
    """An immutable-style builder backed by generated ``UnitSpec`` state."""

    _schema_spec_cls = UnitSpec

    def _copy(self, *, deep: bool = True, **kwargs: Any) -> Self:
        """Return a schema-backed copy while preserving the schema URL."""
        copied = cast(Self, SchemaBase.copy(cast(Any, self), deep=deep, **kwargs))
        copied._schema_url = self._schema_url
        return copied

    def to_dict(
        self, *, include_schema: bool = True, validate: bool = True
    ) -> dict[str, Any]:
        """Serialize and optionally validate the complete chart specification."""
        return self._to_dict(
            include_schema=include_schema,
            validate=validate,
            normalize_chart_data=normalize_data,
        )

    def _to_dict(
        self,
        *,
        include_schema: bool,
        validate: bool,
        normalize_chart_data: Callable[[Any], Any],
    ) -> dict[str, Any]:
        """Serialize this unit spec with a configurable data policy."""
        values = self._serialized_top_level_values(
            normalize_chart_data=normalize_chart_data
        )
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
        return self._copy(deep=False, mark=mark)

    def _append_transform(self, transform: dict[str, Any]) -> Self:
        return self._appended_transform(transform)

    def _configure(
        self,
        value: SchemaBase | dict[str, Any] | None | object = Undefined,
        /,
        **kwargs: Any,
    ) -> Self:
        return self._configured(value, **kwargs)


class _CompositionSpec(TopLevelSpec, ConfigMethodMixin, ResolutionMethodMixin):
    _schema_spec_cls: ClassVar[type]
    _children_key: ClassVar[str]
    _kwds: dict[str, Any]
    _schema_url: str

    def _copy(self, *, deep: bool = True, **kwargs: Any) -> Self:
        """Return a schema-backed copy while preserving the schema URL."""
        copied = cast(Self, SchemaBase.copy(cast(Any, self), deep=deep, **kwargs))
        copied._schema_url = self._schema_url
        return copied

    def to_dict(
        self, *, include_schema: bool = True, validate: bool = True
    ) -> dict[str, Any]:
        return self._to_dict(
            include_schema=include_schema,
            validate=validate,
            normalize_chart_data=normalize_data,
        )

    def _to_dict(
        self,
        *,
        include_schema: bool,
        validate: bool,
        normalize_chart_data: Callable[[Any], Any],
    ) -> dict[str, Any]:
        """Serialize this composition with one shared data policy."""
        values = self._serialized_top_level_values(
            normalize_chart_data=normalize_chart_data
        )
        children = values.get(self._children_key, Undefined)
        if children is not Undefined:
            values[self._children_key] = [
                (
                    child._to_dict(
                        include_schema=False,
                        validate=False,
                        normalize_chart_data=normalize_chart_data,
                    )
                    if isinstance(child, TopLevelSpec)
                    else child.to_dict(include_schema=False, validate=False)
                )
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


class LayerChart(  # type: ignore[misc]  # Generated copy narrows SchemaBase.copy updates.
    LayerPropertiesMixin, _CompositionSpec, LayerSpec
):
    """A layered GenomeSpy specification."""

    _schema_spec_cls = LayerSpec
    _children_key = "layer"

    def __add__(self, other: TopLevelSpec | ImportedView) -> LayerChart:
        current = self._kwds.get("layer", Undefined)
        merged = [] if current is Undefined else list(current)
        merged.append(other)
        return self._copy(deep=False, layer=merged)


class HConcatChart(  # type: ignore[misc]  # Generated copy narrows SchemaBase.copy updates.
    HConcatPropertiesMixin, _CompositionSpec, HConcatSpec
):
    """A horizontally concatenated GenomeSpy specification."""

    _schema_spec_cls = HConcatSpec
    _children_key = "hconcat"

    def __or__(self, other: _SerializableView) -> HConcatChart:
        current = self._kwds.get("hconcat", Undefined)
        merged = [] if current is Undefined else list(current)
        merged.append(other)
        return self._copy(deep=False, hconcat=merged)


class VConcatChart(  # type: ignore[misc]  # Generated copy narrows SchemaBase.copy updates.
    VConcatPropertiesMixin, _CompositionSpec, VConcatSpec
):
    """A vertically concatenated GenomeSpy specification."""

    _schema_spec_cls = VConcatSpec
    _children_key = "vconcat"

    def __and__(self, other: _SerializableView) -> VConcatChart:
        current = self._kwds.get("vconcat", Undefined)
        merged = [] if current is Undefined else list(current)
        merged.append(other)
        return self._copy(deep=False, vconcat=merged)


class ConcatChart(  # type: ignore[misc]  # Generated copy narrows SchemaBase.copy updates.
    ConcatPropertiesMixin, _CompositionSpec, ConcatSpec
):
    """A grid-concatenated GenomeSpy specification."""

    _schema_spec_cls = ConcatSpec
    _children_key = "concat"


class MultiscaleChart(  # type: ignore[misc]  # Generated copy narrows SchemaBase.copy updates.
    MultiscalePropertiesMixin, _CompositionSpec, MultiscaleSpec
):
    """A semantic-zoom composition backed by generated schema state."""

    _schema_spec_cls = MultiscaleSpec
    _children_key = "multiscale"


class ImportedView(ImportedViewConstructorMixin, ImportSpec):
    """A child-view import that can participate in chart composition."""

    def _initialize_import(self, *, properties: dict[str, Any]) -> None:
        """Initialize generated schema state for an imported child view."""
        ImportSpec.__init__(self, **properties)

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
        return LayerChart(layer=cast(Any, [self, other]))

    def __and__(self, other: TopLevelSpec | ImportedView) -> VConcatChart:
        """Vertically concatenate this imported view with another view."""
        return VConcatChart(vconcat=cast(Any, [self, other]))

    def __or__(self, other: TopLevelSpec | ImportedView) -> HConcatChart:
        """Horizontally concatenate this imported view with another view."""
        return HConcatChart(hconcat=cast(Any, [self, other]))


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
        children: list[TopLevelSpec | ImportedView] = []
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
            return LayerChart(
                layer=cast(Any, children), schema_url=schema_url, **values
            )
        if structural_key == "multiscale":
            return MultiscaleChart(
                multiscale=cast(Any, children), schema_url=schema_url, **values
            )
        if structural_key == "vconcat":
            return VConcatChart(
                vconcat=cast(Any, children), schema_url=schema_url, **values
            )
        if structural_key == "hconcat":
            return HConcatChart(
                hconcat=cast(Any, children), schema_url=schema_url, **values
            )
        return ConcatChart(concat=cast(Any, children), schema_url=schema_url, **values)

    if "import" in values:
        raise ValueError("An imported view must be nested inside a composition.")
    raise ValueError("GenomeSpy specification has no supported structural root.")


concat = _concat
hconcat = _hconcat
layer = _layer
multiscale = _multiscale
import_view = _import_view
vconcat = _vconcat
