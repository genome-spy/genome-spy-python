"""Minimal code generator scaffolding for GenomeSpy schema wrappers.

This module summarizes JSON Schema definitions and emits simple wrapper class
source while accounting for GenomeSpy-specific schema conventions.

Portions are adapted from Vega-Altair's schema-generation tooling:
https://github.com/vega/altair/tree/main/tools/schemapi and
https://github.com/vega/altair/blob/main/tools/generate_schema_wrapper.py
Copyright (c) 2015-2025, Vega-Altair Developers. BSD-3-Clause license; see
``LICENSES/ALTAIR-BSD-3-Clause.txt``.
"""

from __future__ import annotations

import keyword
import re
from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import Any
from urllib.parse import unquote

from .expression_codegen import ExpressionCatalog

_MISSING = object()
KWDS_TARGETS = frozenset(
    {
        "Axis",
        "AxisConfig",
        "BindCheckbox",
        "BindInput",
        "BindRadioSelect",
        "BindRange",
        "CompareParams",
        "DataFormat",
        "DynamicOpacity",
        "Encoding",
        "EventConfig",
        "GenomeAxis",
        "GenomeSpyConfig",
        "HandledTooltip",
        "Legend",
        "LegendConfig",
        "LinkConfig",
        "MarkConfig",
        "Paddings",
        "PointConfig",
        "Parameter",
        "Parse",
        "RangeConfig",
        "RectConfig",
        "Resolve",
        "RuleConfig",
        "RulerConfig",
        "RulerEventConfig",
        "RulerMarkConfig",
        "Scale",
        "ScaleConfig",
        "ScaleInterpolateParams",
        "SchemeParams",
        "SeparatorProps",
        "SizeDef",
        "Step",
        "TextConfig",
        "Title",
        "TitleConfig",
        "ViewConfig",
        "ViewBackground",
        "ZoomParams",
    }
)
ANONYMOUS_PROPERTY_KWDS = {
    "axes": "AxesKwds",
    "legends": "LegendsKwds",
    "resolve": "ResolveKwds",
    "scales": "ScalesKwds",
}


def generate_expression_module(catalog: ExpressionCatalog) -> GeneratedModule:
    """Generate the documented expression authoring namespace.

    Args:
        catalog: Parsed, version-matched upstream expression definitions.

    Returns:
        A generated module containing constants and typed function builders.

    Raises:
        No exceptions are raised.

    Example:
        ``generate_expression_module(catalog).exports`` contains ``expr``.
    """
    constant_properties = "\n\n".join(
        "\n".join(
            [
                "    @property",
                f"    def {name}(cls) -> Expression:",
                f'        """Return the GenomeSpy ``{name}`` constant."""',
                f"        return Expression({name!r})",
            ]
        )
        for name in catalog.constants
    )
    methods: list[str] = []
    for spec in catalog.functions:
        parameters = []
        arguments = []
        has_optional = any(parameter.optional for parameter in spec.parameters)
        for parameter in spec.parameters:
            if parameter.variadic:
                parameters.append(f"*{parameter.name}: IntoExpression")
                arguments.append(f"*{parameter.name}")
            elif parameter.optional:
                parameters.append(
                    f"{parameter.name}: IntoExpression | UndefinedType = Undefined"
                )
                arguments.append(parameter.name)
            else:
                parameters.append(f"{parameter.name}: IntoExpression")
                arguments.append(parameter.name)
        parameter_source = ", ".join(parameters)
        has_variadic = any(parameter.variadic for parameter in spec.parameters)
        if parameter_source and not has_variadic:
            parameter_source += ", /"
        argument_source = ", ".join(arguments)
        if has_optional:
            body = [
                f"        arguments = [{', '.join(parameter.name for parameter in spec.parameters if not parameter.variadic)}]",
                "        while arguments and arguments[-1] is Undefined:",
                "            arguments.pop()",
                "        if any(argument is Undefined for argument in arguments):",
                f"            raise ValueError({f'{spec.name} optional arguments cannot contain gaps'!r})",
                f"        return _function_expression({spec.name!r}, *arguments)",
            ]
        else:
            separator = ", " if argument_source else ""
            body = [
                f"        return _function_expression({spec.name!r}{separator}{argument_source})"
            ]
        methods.append(
            "\n".join(
                [
                    "    @classmethod",
                    f"    def {spec.python_name}(cls{', ' if parameter_source else ''}{parameter_source}) -> Expression:",
                    f'        """Build a GenomeSpy ``{spec.name}`` expression."""',
                    *body,
                ]
            )
        )
    source = "\n".join(
        [
            '"""Generated from GenomeSpy expression-runtime documentation. Do not edit."""',
            "",
            "from __future__ import annotations",
            "",
            "from typing import TYPE_CHECKING",
            "",
            "from genome_spy._expressions import Expression, _function_expression",
            "from genome_spy.schema import core",
            "from genome_spy.schemapi import Undefined, UndefinedType",
            "",
            "if TYPE_CHECKING:",
            "    from genome_spy._expressions import IntoExpression",
            "",
            "",
            "class _ExprMeta(type):",
            '    """Provide read-only GenomeSpy expression constants."""',
            "",
            constant_properties,
            "",
            "",
            "class expr(core.ExprRef, metaclass=_ExprMeta):",
            '    """Build expression references, constants, and function calls."""',
            "",
            "    def __new__(",
            "        cls, expression: str | Expression",
            "    ) -> core.ExprRef:  # type: ignore[misc]",
            "        return core.ExprRef(expr=str(expression))",
            "",
            "\n\n".join(methods),
            "",
            "",
            '__all__ = ["Expression", "expr"]',
            "",
        ]
    )
    return GeneratedModule(source=source, exports=("Expression", "expr"))


@dataclass(frozen=True, slots=True)
class SchemaDefinition:
    """A named definition from the GenomeSpy JSON Schema."""

    name: str
    schema: dict[str, Any]

    @property
    def properties(self) -> dict[str, Any]:
        properties = self.schema.get("properties", {})
        if isinstance(properties, dict):
            return properties
        return {}

    @property
    def required(self) -> tuple[str, ...]:
        required = self.schema.get("required", [])
        if isinstance(required, list):
            return tuple(str(item) for item in required)
        return ()


@dataclass(frozen=True, slots=True)
class GeneratedModule:
    """Generated module source and exported symbols."""

    source: str
    exports: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class GeneratedSchemaClass:
    """Generated schema wrapper source plus import requirements."""

    source: str
    needs_literal: bool = False
    needs_sequence: bool = False
    used_aliases: tuple[str, ...] = ()
    used_kwds: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AnnotationSpec:
    """A rendered annotation plus import requirements."""

    annotation: str
    needs_literal: bool = False
    needs_sequence: bool = False


@dataclass(frozen=True, slots=True)
class PropertySpec:
    """Derived information for one generated schema property."""

    name: str
    annotation: AnnotationSpec
    nested_schema_class_name: str | None = None
    description: str = ""

    @property
    def python_name(self) -> str:
        """Return the Python-safe parameter spelling for this property."""
        return _python_property_name(self.name)


@dataclass(frozen=True, slots=True)
class UnionVariantSpec:
    """One concrete leaf of a recursively expanded schema union."""

    schema_name: str | None
    properties: tuple[PropertySpec, ...]
    required: frozenset[str]
    discriminators: tuple[tuple[str, tuple[Any, ...]], ...]
    additional_properties: bool | dict[str, Any] | None


@dataclass(frozen=True, slots=True)
class SchemaFactorySpec:
    """One generated schema-backed convenience factory."""

    helper_name: str
    class_name: str
    docstring: str
    positional_property: str | None = None
    normalize_view_background: bool = False
    fixed_properties: tuple[tuple[str, Any], ...] = ()


@dataclass(frozen=True, slots=True)
class ParameterConfigFactorySpec:
    """A parameter helper backed by one generated nested configuration."""

    helper_name: str
    parameter_class_name: str
    config_class_name: str
    config_property: str
    parameter_properties: tuple[PropertySpec, ...]
    config_properties: tuple[PropertySpec, ...]
    fixed_properties: tuple[tuple[str, Any], ...] = ()
    supports_empty: bool = False


@dataclass(frozen=True, slots=True)
class _RawUnionVariant:
    """Internal schema fragments accumulated while expanding a union."""

    schema_name: str | None
    properties: dict[str, Any]
    required: frozenset[str]
    additional_properties: bool | dict[str, Any] | None


@dataclass(frozen=True, slots=True)
class TransformMethodSpec:
    """Schema-derived information for one transform convenience method."""

    schema_name: str
    transform_type: str
    properties: tuple[PropertySpec, ...]
    required: frozenset[str]
    method_name_override: str | None = None
    positional_properties: tuple[str, ...] = ()
    property_aliases: tuple[tuple[str, str], ...] = ()
    repeat_keyword_properties: tuple[str, str] | None = None
    example: str | None = None

    @property
    def method_name(self) -> str:
        """Return the generated method name for this transform."""
        if self.method_name_override is not None:
            return self.method_name_override
        return f"transform_{_snake_name(self.transform_type)}"


@dataclass(frozen=True, slots=True)
class TransformMethodTemplate:
    """Describe one additional method emitted from a transform schema."""

    method_name: str
    properties: tuple[str, ...]
    positional_properties: tuple[str, ...] = ()
    property_aliases: tuple[tuple[str, str], ...] = ()
    repeat_keyword_properties: tuple[str, str] | None = None
    example: str | None = None


@dataclass(frozen=True, slots=True)
class TransformMethodOverride:
    """Customize generated methods for one transform schema definition."""

    positional_properties: tuple[str, ...] = ()
    additional_methods: tuple[TransformMethodTemplate, ...] = ()


@dataclass(frozen=True, slots=True)
class LazyDataMethodSpec:
    """Schema-derived information for one named lazy data source helper."""

    source_type: str
    url_annotation: AnnotationSpec
    properties: tuple[PropertySpec, ...]

    @property
    def method_name(self) -> str:
        """Return the Python method name for this lazy source type."""
        return _snake_name(self.source_type)


@dataclass(frozen=True, slots=True)
class SchemaAnalyzer:
    """Inspect schema fragments and derive Python-facing type information."""

    definitions: dict[str, Any]
    kwds_defs: frozenset[str] = frozenset()

    def resolve_properties(
        self,
        schema: dict[str, Any],
        *,
        seen: frozenset[str] = frozenset(),
    ) -> dict[str, Any]:
        ref_name = _ref_name(schema)
        if ref_name is not None:
            target = self.definitions.get(ref_name)
            if not isinstance(target, dict) or ref_name in seen:
                return {}
            return self.resolve_properties(target, seen=seen | {ref_name})

        resolved: dict[str, Any] = {}
        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            resolved.update(properties)
        for key in ("anyOf", "oneOf", "allOf"):
            variants = schema.get(key, [])
            if not isinstance(variants, list):
                continue
            for variant in variants:
                if isinstance(variant, dict):
                    resolved.update(self.resolve_properties(variant, seen=seen))
        return resolved

    def resolved_identifier_properties(self, schema: dict[str, Any]) -> tuple[str, ...]:
        return tuple(sorted(self.resolve_properties(schema)))

    def property_variants(
        self,
        schema: dict[str, Any],
        *,
        seen: frozenset[str] = frozenset(),
    ) -> tuple[dict[str, Any], ...]:
        """Return property mappings without flattening alternative branches."""
        ref_name = _ref_name(schema)
        if ref_name is not None:
            target = self.definitions.get(ref_name)
            if not isinstance(target, dict) or ref_name in seen:
                return ()
            variants = self.property_variants(target, seen=seen | {ref_name})
        else:
            variants = ({},)

        local_properties = schema.get("properties", {})
        if isinstance(local_properties, dict) and local_properties:
            variants = tuple(
                {**variant, **local_properties} for variant in variants
            ) or (dict(local_properties),)

        for key in ("allOf",):
            components = schema.get(key, [])
            if not isinstance(components, list):
                continue
            for component in components:
                if not isinstance(component, dict):
                    continue
                component_variants = self.property_variants(component, seen=seen)
                if component_variants:
                    variants = tuple(
                        {**variant, **component_variant}
                        for variant in variants
                        for component_variant in component_variants
                    )

        for key in ("anyOf", "oneOf"):
            choices = schema.get(key, [])
            if not isinstance(choices, list) or not choices:
                continue
            choice_variants = tuple(
                choice_variant
                for choice in choices
                if isinstance(choice, dict)
                for choice_variant in self.property_variants(choice, seen=seen)
            )
            if choice_variants:
                variants = tuple(
                    {**variant, **choice_variant}
                    for variant in variants
                    for choice_variant in choice_variants
                )
        return variants

    def union_variants(self, definition_name: str) -> tuple[UnionVariantSpec, ...]:
        """Expand a named union into concrete, branch-preserving leaves."""
        schema = self.definitions.get(definition_name)
        if not isinstance(schema, dict):
            return ()
        raw_variants = self._union_variants(
            schema,
            seen=frozenset({definition_name}),
            schema_name=definition_name,
        )
        variants: list[UnionVariantSpec] = []
        for variant in raw_variants:
            discriminators: list[tuple[str, tuple[Any, ...]]] = []
            for name, property_schema in sorted(variant.properties.items()):
                if not isinstance(property_schema, dict):
                    continue
                if "const" in property_schema:
                    values = (property_schema["const"],)
                else:
                    enum = property_schema.get("enum")
                    values = tuple(enum) if isinstance(enum, list) else ()
                if values:
                    discriminators.append((name, values))
            variants.append(
                UnionVariantSpec(
                    schema_name=variant.schema_name,
                    properties=self.property_specs_from_properties(variant.properties),
                    required=variant.required,
                    discriminators=tuple(discriminators),
                    additional_properties=variant.additional_properties,
                )
            )
        return tuple(variants)

    def _union_variants(
        self,
        schema: dict[str, Any],
        *,
        seen: frozenset[str],
        schema_name: str | None,
    ) -> tuple[_RawUnionVariant, ...]:
        ref_name = _ref_name(schema)
        if ref_name is not None:
            if ref_name in seen:
                return ()
            target = self.definitions.get(ref_name)
            if not isinstance(target, dict):
                return ()
            return self._union_variants(
                target,
                seen=seen | {ref_name},
                schema_name=ref_name,
            )

        properties = schema.get("properties", {})
        local_properties = dict(properties) if isinstance(properties, dict) else {}
        required = schema.get("required", [])
        local_required = (
            frozenset(name for name in required if isinstance(name, str))
            if isinstance(required, list)
            else frozenset()
        )
        additional_properties = schema.get("additionalProperties")
        if not isinstance(additional_properties, bool | dict):
            additional_properties = None
        variants = (
            _RawUnionVariant(
                schema_name=schema_name,
                properties=local_properties,
                required=local_required,
                additional_properties=additional_properties,
            ),
        )

        all_of = schema.get("allOf", [])
        if isinstance(all_of, list):
            for component in all_of:
                if not isinstance(component, dict):
                    continue
                component_variants = self._union_variants(
                    component,
                    seen=seen,
                    schema_name=None,
                )
                variants = tuple(
                    self._merge_union_variants(
                        base, extension, prefer_extension_name=False
                    )
                    for base in variants
                    for extension in component_variants
                )

        choices = schema.get("oneOf", schema.get("anyOf", []))
        if isinstance(choices, list) and choices:
            choice_variants = tuple(
                variant
                for choice in choices
                if isinstance(choice, dict)
                for variant in self._union_variants(
                    choice,
                    seen=seen,
                    schema_name=None,
                )
            )
            variants = tuple(
                self._merge_union_variants(base, choice, prefer_extension_name=True)
                for base in variants
                for choice in choice_variants
            )
        return variants

    @staticmethod
    def _merge_union_variants(
        base: _RawUnionVariant,
        extension: _RawUnionVariant,
        *,
        prefer_extension_name: bool,
    ) -> _RawUnionVariant:
        additional_properties = extension.additional_properties
        if additional_properties is None:
            additional_properties = base.additional_properties
        return _RawUnionVariant(
            schema_name=(
                extension.schema_name or base.schema_name
                if prefer_extension_name
                else base.schema_name or extension.schema_name
            ),
            properties={**base.properties, **extension.properties},
            required=base.required | extension.required,
            additional_properties=additional_properties,
        )

    def property_specs(self, definition: SchemaDefinition) -> tuple[PropertySpec, ...]:
        resolved_properties = self.resolve_properties(definition.schema)
        return self.property_specs_from_properties(resolved_properties)

    def property_specs_from_properties(
        self, properties: dict[str, Any]
    ) -> tuple[PropertySpec, ...]:
        """Return property specs from one concrete object-property mapping."""
        object_property_refs = self._resolved_object_property_refs(
            {"properties": properties}
        )
        property_names = [name for name in sorted(properties) if name.isidentifier()]
        return tuple(
            PropertySpec(
                name=name,
                annotation=self._property_spec_annotation(
                    name,
                    properties.get(name, {}),
                ),
                nested_schema_class_name=object_property_refs.get(name),
                description=_property_description(properties.get(name, {})),
            )
            for name in property_names
        )

    def _property_spec_annotation(
        self,
        property_name: str,
        schema: dict[str, Any],
    ) -> AnnotationSpec:
        helper_name = ANONYMOUS_PROPERTY_KWDS.get(property_name)
        if helper_name is not None and self._looks_like_anonymous_kwds_target(
            property_name, schema
        ):
            return AnnotationSpec(helper_name)
        return self.property_annotation_spec(schema)

    def _looks_like_anonymous_kwds_target(
        self,
        property_name: str,
        schema: dict[str, Any],
    ) -> bool:
        if property_name == "axes":
            properties = schema.get("properties", {})
            return (
                isinstance(properties, dict)
                and {"x", "y"}.issubset(properties)
                and all(isinstance(properties.get(axis), dict) for axis in ("x", "y"))
            )
        if property_name == "legends":
            properties = schema.get("properties", {})
            return isinstance(properties, dict) and bool(properties)
        if property_name == "scales":
            properties = schema.get("properties", {})
            return isinstance(properties, dict) and bool(properties)
        if property_name == "resolve":
            properties = schema.get("properties", {})
            return isinstance(properties, dict) and {
                "axis",
                "legend",
                "scale",
            }.issubset(properties)
        return False

    def property_annotation_spec(self, schema: dict[str, Any]) -> AnnotationSpec:
        atomic_types, needs_literal, needs_sequence = self._collect_annotation_atoms(
            schema
        )
        if not atomic_types or "Any" in atomic_types:
            return AnnotationSpec("Any")
        return AnnotationSpec(
            " | ".join(atomic_types),
            needs_literal=needs_literal,
            needs_sequence=needs_sequence,
        )

    def is_scalar_aliasable(
        self,
        schema: dict[str, Any],
        *,
        seen_refs: frozenset[str] = frozenset(),
    ) -> bool:
        if self.schema_looks_object_like(schema):
            return False

        ref_name = _ref_name(schema)
        if ref_name is not None:
            if ref_name in seen_refs:
                return False
            target = self.definitions.get(ref_name)
            if not isinstance(target, dict):
                return False
            return self.is_scalar_aliasable(
                target,
                seen_refs=seen_refs | {ref_name},
            )

        schema_type = schema.get("type")
        if schema_type == "object":
            return False
        if isinstance(schema_type, list) and "object" in schema_type:
            return False

        items = schema.get("items")
        if items is not None:
            if not isinstance(items, dict):
                return False
            if not self.is_scalar_aliasable(items, seen_refs=seen_refs):
                return False

        for key in ("anyOf", "oneOf", "allOf"):
            variants = schema.get(key, [])
            if not isinstance(variants, list):
                continue
            if not all(
                isinstance(variant, dict)
                and self.is_scalar_aliasable(variant, seen_refs=seen_refs)
                for variant in variants
            ):
                return False

        return True

    def schema_looks_object_like(self, schema: dict[str, Any]) -> bool:
        schema_type = schema.get("type")
        if schema_type == "object":
            return True
        if "properties" in schema or "additionalProperties" in schema:
            return True
        for key in ("anyOf", "oneOf", "allOf"):
            variants = schema.get(key, [])
            if not isinstance(variants, list):
                continue
            if any(
                isinstance(variant, dict) and self.schema_looks_object_like(variant)
                for variant in variants
            ):
                return True
        return False

    def _resolved_object_property_refs(
        self, schema: dict[str, Any]
    ) -> dict[str, str | None]:
        properties = self.resolve_properties(schema)
        refs: dict[str, str | None] = {}
        for name, property_schema in properties.items():
            if not isinstance(property_schema, dict):
                continue
            ref_name = _first_ref_name(property_schema)
            if ref_name is None:
                refs[name] = None
                continue
            target = self.definitions.get(ref_name)
            if isinstance(target, dict) and self.schema_looks_object_like(target):
                refs[name] = _class_name(ref_name)
            else:
                refs[name] = None
        return refs

    def _collect_annotation_atoms(
        self,
        schema: dict[str, Any],
        *,
        seen_refs: frozenset[str] = frozenset(),
    ) -> tuple[list[str], bool, bool]:
        if not schema:
            return (["Any"], False, False)

        atoms: list[str] = []
        needs_literal = False
        needs_sequence = False

        ref_name = _ref_name(schema)
        if ref_name is not None:
            if ref_name in seen_refs:
                return (["Any"], False, False)
            target = self.definitions.get(ref_name)
            if not isinstance(target, dict):
                return (["Any"], False, False)
            if self.schema_looks_object_like(target):
                atoms.extend(
                    (_class_name(ref_name), self.raw_mapping_annotation(ref_name))
                )
                return (_dedupe_preserve_order(atoms), False, False)
            if self.is_scalar_aliasable(target, seen_refs=seen_refs | {ref_name}):
                alias_spec = self.property_annotation_spec(target)
                alias_name = _type_alias_name(ref_name)
                if alias_spec.annotation != "Any":
                    return (
                        [alias_name],
                        alias_spec.needs_literal,
                        alias_spec.needs_sequence,
                    )
            return self._collect_annotation_atoms(
                target,
                seen_refs=seen_refs | {ref_name},
            )

        const_value = schema.get("const", _MISSING)
        if const_value is not _MISSING:
            if _is_literal_value(const_value):
                atoms.append(f"Literal[{const_value!r}]")
                needs_literal = True
            else:
                atoms.append("Any")
            schema_type = None
        else:
            schema_type = schema.get("type")

        enum_values = schema.get("enum")
        if isinstance(enum_values, list) and enum_values:
            if all(_is_literal_value(value) for value in enum_values):
                literal_values = ", ".join(repr(value) for value in enum_values)
                atoms.append(f"Literal[{literal_values}]")
                needs_literal = True
            else:
                atoms.append("Any")
            schema_type = None

        if isinstance(schema_type, str):
            type_atoms, type_needs_sequence = self._annotation_for_schema_type(
                schema_type,
                schema,
                seen_refs=seen_refs,
            )
            atoms.extend(type_atoms)
            needs_sequence = needs_sequence or type_needs_sequence
        elif isinstance(schema_type, list):
            for type_name in schema_type:
                if not isinstance(type_name, str):
                    atoms.append("Any")
                    continue
                type_atoms, type_needs_sequence = self._annotation_for_schema_type(
                    type_name,
                    schema,
                    seen_refs=seen_refs,
                )
                atoms.extend(type_atoms)
                needs_sequence = needs_sequence or type_needs_sequence
        elif "properties" in schema:
            atoms.append("dict[str, Any]")

        for key in ("anyOf", "oneOf", "allOf"):
            variants = schema.get(key, [])
            if not isinstance(variants, list):
                continue
            for variant in variants:
                if not isinstance(variant, dict):
                    atoms.append("Any")
                    continue
                variant_atoms, variant_needs_literal, variant_needs_sequence = (
                    self._collect_annotation_atoms(
                        variant,
                        seen_refs=seen_refs,
                    )
                )
                atoms.extend(variant_atoms)
                needs_literal = needs_literal or variant_needs_literal
                needs_sequence = needs_sequence or variant_needs_sequence

        deduped = _dedupe_preserve_order(atoms)
        if "Any" in deduped:
            return (["Any"], needs_literal, needs_sequence)
        return (deduped, needs_literal, needs_sequence)

    def _annotation_for_schema_type(
        self,
        schema_type: str,
        schema: dict[str, Any],
        *,
        seen_refs: frozenset[str],
    ) -> tuple[list[str], bool]:
        if schema_type == "string":
            return (["str"], False)
        if schema_type == "boolean":
            return (["bool"], False)
        if schema_type == "number":
            return (["float"], False)
        if schema_type == "integer":
            return (["int"], False)
        if schema_type == "null":
            return (["None"], False)
        if schema_type == "object":
            return (["dict[str, Any]"], False)
        if schema_type == "array":
            items = schema.get("items", {})
            if not isinstance(items, dict):
                return (["Sequence[Any]"], True)
            item_atoms, _, _ = self._collect_annotation_atoms(
                items,
                seen_refs=seen_refs,
            )
            item_annotation = (
                "Any"
                if not item_atoms or "Any" in item_atoms
                else " | ".join(item_atoms)
            )
            return ([f"Sequence[{item_annotation}]"], True)
        return (["Any"], False)

    def raw_mapping_annotation(self, ref_name: str | None) -> str:
        if ref_name is None:
            return "dict[str, Any]"
        kwds_name = _kwds_type_name(ref_name)
        if kwds_name in self.kwds_defs:
            return kwds_name
        return "dict[str, Any]"


class SchemaWrapperGenerator:
    """Generate small Python wrapper classes from schema definitions.

    This is not yet a full Altair-style generator. It gives us a testable
    local abstraction for schema traversal and class emission while we map
    GenomeSpy's schema structure.
    """

    def __init__(
        self,
        rootschema: dict[str, Any],
        *,
        schema_version: str = "unknown",
        transform_method_overrides: Mapping[str, TransformMethodOverride] | None = None,
    ) -> None:
        self.rootschema = rootschema
        self.schema_version = schema_version
        self._transform_method_overrides = dict(transform_method_overrides or {})

    @property
    def _definitions_map(self) -> dict[str, Any]:
        definitions = self.rootschema.get("definitions", {})
        if isinstance(definitions, dict):
            return definitions
        return {}

    @property
    def _base_analyzer(self) -> SchemaAnalyzer:
        return SchemaAnalyzer(self._definitions_map)

    @property
    def _analyzer(self) -> SchemaAnalyzer:
        return SchemaAnalyzer(self._definitions_map, frozenset(self.kwds_type_names()))

    def definitions(self) -> list[SchemaDefinition]:
        """Return named schema definitions in deterministic order."""
        return [
            SchemaDefinition(name, schema)
            for name, schema in sorted(self._definitions_map.items())
            if isinstance(schema, dict)
        ]

    def mark_types(self) -> tuple[str, ...]:
        """Return mark names declared by the upstream ``MarkType`` enum."""
        definitions = self.rootschema.get("definitions", {})
        if not isinstance(definitions, dict):
            return ()
        mark_schema = definitions.get("MarkType", {})
        if not isinstance(mark_schema, dict):
            return ()
        values = mark_schema.get("enum", [])
        if not isinstance(values, list):
            return ()
        return tuple(value for value in values if isinstance(value, str))

    def encoding_channels(self) -> tuple[str, ...]:
        """Return encoding names declared by the upstream ``Encoding`` object."""
        definitions = self.rootschema.get("definitions", {})
        if not isinstance(definitions, dict):
            return ()
        encoding_schema = definitions.get("Encoding", {})
        if not isinstance(encoding_schema, dict):
            return ()
        properties = encoding_schema.get("properties", {})
        if not isinstance(properties, dict):
            return ()
        return tuple(sorted(name for name in properties if isinstance(name, str)))

    def binding_factory_specs(self) -> tuple[SchemaFactorySpec, ...]:
        """Return factories discovered from concrete ``Binding`` leaves."""
        specs: list[SchemaFactorySpec] = []
        for variant in self._analyzer.union_variants("Binding"):
            if variant.schema_name is None:
                continue
            discriminator = next(
                (values for name, values in variant.discriminators if name == "input"),
                (),
            )
            if "input" not in variant.required:
                specs.append(
                    SchemaFactorySpec(
                        helper_name="binding",
                        class_name=variant.schema_name,
                        docstring="Create a generic input binding.",
                    )
                )
                continue
            for value in discriminator:
                if not isinstance(value, str):
                    continue
                specs.append(
                    SchemaFactorySpec(
                        helper_name=f"binding_{_snake_name(value)}",
                        class_name=variant.schema_name,
                        docstring=f"Create a {value} input binding.",
                        fixed_properties=(("input", value),),
                    )
                )
        names = [spec.helper_name for spec in specs]
        duplicates = sorted({name for name in names if names.count(name) > 1})
        if duplicates:
            raise ValueError(
                "Binding helper discovery produced duplicate names: "
                + ", ".join(duplicates)
            )
        return tuple(sorted(specs, key=lambda spec: spec.helper_name))

    def parameter_config_factory_specs(
        self,
    ) -> tuple[ParameterConfigFactorySpec, ...]:
        """Return selection and nested-config parameter helper definitions."""
        specs: list[ParameterConfigFactorySpec] = []
        selection_schema = self._definitions_map.get("SelectionParameter", {})
        selection_properties = self._analyzer.resolve_properties(selection_schema)
        select_schema = selection_properties.get("select", {})
        choices = (
            select_schema.get("anyOf", select_schema.get("oneOf", []))
            if isinstance(select_schema, dict)
            else []
        )
        if isinstance(choices, list):
            for choice in choices:
                if not isinstance(choice, dict):
                    continue
                config_name = _ref_name(choice)
                config_schema = self._definitions_map.get(config_name or "")
                if (
                    config_name is None
                    or not isinstance(config_schema, dict)
                    or not self._base_analyzer.schema_looks_object_like(config_schema)
                ):
                    continue
                variants = self._analyzer.union_variants(config_name)
                for variant in variants:
                    values = next(
                        (
                            discriminator_values
                            for name, discriminator_values in variant.discriminators
                            if name == "type" and name in variant.required
                        ),
                        (),
                    )
                    for value in values:
                        if not isinstance(value, str) or variant.schema_name is None:
                            continue
                        specs.append(
                            ParameterConfigFactorySpec(
                                helper_name=f"selection_{_snake_name(value)}",
                                parameter_class_name="SelectionParameter",
                                config_class_name=variant.schema_name,
                                config_property="select",
                                parameter_properties=tuple(
                                    prop
                                    for prop in self.schema_property_specs(
                                        "SelectionParameter"
                                    )
                                    if prop.name not in {"name", "select"}
                                ),
                                config_properties=variant.properties,
                                fixed_properties=(("type", value),),
                                supports_empty=True,
                            )
                        )

        for variant in self._analyzer.union_variants("Parameter"):
            required_config_names = variant.required - {"name"}
            if len(required_config_names) != 1:
                continue
            config_property = next(iter(required_config_names))
            if config_property == "select":
                continue
            property_spec = next(
                (prop for prop in variant.properties if prop.name == config_property),
                None,
            )
            if (
                property_spec is None
                or property_spec.nested_schema_class_name is None
                or variant.schema_name is None
            ):
                continue
            config_class_name = property_spec.nested_schema_class_name
            specs.append(
                ParameterConfigFactorySpec(
                    helper_name=_snake_name(config_property),
                    parameter_class_name=variant.schema_name,
                    config_class_name=config_class_name,
                    config_property=config_property,
                    parameter_properties=tuple(
                        prop
                        for prop in variant.properties
                        if prop.name not in {"name", config_property}
                    ),
                    config_properties=self.schema_property_specs(config_class_name),
                )
            )

        names = [spec.helper_name for spec in specs]
        duplicates = sorted({name for name in names if names.count(name) > 1})
        if duplicates:
            raise ValueError(
                "Parameter helper discovery produced duplicate names: "
                + ", ".join(duplicates)
            )
        return tuple(sorted(specs, key=lambda spec: spec.helper_name))

    def transform_method_specs(self) -> tuple[TransformMethodSpec, ...]:
        """Return method metadata for every member of ``TransformParams``."""
        transform_union = self._definitions_map.get("TransformParams", {})
        if not isinstance(transform_union, dict):
            return ()

        variants = transform_union.get("anyOf", transform_union.get("oneOf", []))
        if not isinstance(variants, list):
            return ()

        variant_schema_names = {
            schema_name
            for variant in variants
            if isinstance(variant, dict)
            if (schema_name := _ref_name(variant)) is not None
        }
        unused_overrides = (
            self._transform_method_overrides.keys() - variant_schema_names
        )
        if unused_overrides:
            names = ", ".join(sorted(unused_overrides))
            raise ValueError(
                "Transform method overrides refer to schemas absent from "
                f"TransformParams: {names}."
            )

        specs: list[TransformMethodSpec] = []
        for variant in variants:
            if not isinstance(variant, dict):
                continue
            schema_name = _ref_name(variant)
            definition_schema = self._definitions_map.get(schema_name or "")
            if schema_name is None or not isinstance(definition_schema, dict):
                continue

            properties = self._analyzer.resolve_properties(definition_schema)
            type_schema = properties.get("type", {})
            transform_type = (
                type_schema.get("const") if isinstance(type_schema, dict) else None
            )
            if not isinstance(transform_type, str):
                continue

            property_specs = tuple(
                PropertySpec(
                    name=name,
                    annotation=self._analyzer._property_spec_annotation(
                        name, property_schema
                    ),
                    nested_schema_class_name=None,
                    description=_property_description(property_schema),
                )
                for name, property_schema in sorted(properties.items())
                if name != "type"
                and isinstance(name, str)
                and isinstance(property_schema, dict)
                and (name.isidentifier() or keyword.iskeyword(name))
            )
            required = frozenset(
                name
                for name in definition_schema.get("required", [])
                if isinstance(name, str) and name != "type"
            )
            override = self._transform_method_overrides.get(
                schema_name, TransformMethodOverride()
            )
            specs.append(
                TransformMethodSpec(
                    schema_name=schema_name,
                    transform_type=transform_type,
                    properties=property_specs,
                    required=required,
                    positional_properties=override.positional_properties,
                )
            )
            properties_by_name = {
                property_spec.name: property_spec for property_spec in property_specs
            }
            for template in override.additional_methods:
                missing_properties = (
                    set(template.properties) - properties_by_name.keys()
                )
                if missing_properties:
                    names = ", ".join(sorted(missing_properties))
                    raise ValueError(
                        f"Transform method template {template.method_name!r} refers "
                        f"to missing {schema_name} properties: {names}."
                    )
                specs.append(
                    TransformMethodSpec(
                        schema_name=schema_name,
                        transform_type=transform_type,
                        properties=tuple(
                            properties_by_name[name] for name in template.properties
                        ),
                        required=frozenset(),
                        method_name_override=template.method_name,
                        positional_properties=template.positional_properties,
                        property_aliases=template.property_aliases,
                        repeat_keyword_properties=template.repeat_keyword_properties,
                        example=template.example,
                    )
                )
        specs_by_method: dict[str, list[TransformMethodSpec]] = {}
        for spec in specs:
            specs_by_method.setdefault(spec.method_name, []).append(spec)
        duplicate_methods = {
            method_name: method_specs
            for method_name, method_specs in specs_by_method.items()
            if len(method_specs) > 1
        }
        if duplicate_methods:
            details = "; ".join(
                f"{method_name} ({', '.join(spec.schema_name for spec in method_specs)})"
                for method_name, method_specs in sorted(duplicate_methods.items())
            )
            raise ValueError(f"Duplicate generated transform methods: {details}.")

        return tuple(specs)

    def lazy_data_method_specs(self) -> tuple[LazyDataMethodSpec, ...]:
        """Return URL-backed lazy data helpers declared by ``LazyDataParams``.

        The union also includes internal sources, such as generated axis ticks.
        A public helper is emitted only for a named union member that has both a
        fixed ``type`` and a required ``url`` property.
        """
        lazy_data_schema = self._definitions_map.get("LazyDataParams", {})
        if not isinstance(lazy_data_schema, dict):
            return ()

        variants = lazy_data_schema.get("anyOf", lazy_data_schema.get("oneOf", []))
        if not isinstance(variants, list):
            return ()

        specs: list[LazyDataMethodSpec] = []
        for variant in variants:
            if not isinstance(variant, dict):
                continue
            definition_name = _ref_name(variant)
            definition_schema = self._definitions_map.get(definition_name or "")
            if definition_name is None or not isinstance(definition_schema, dict):
                continue
            properties = self._analyzer.resolve_properties(definition_schema)
            type_schema = properties.get("type", {})
            source_type = (
                type_schema.get("const") if isinstance(type_schema, dict) else None
            )
            required = definition_schema.get("required", [])
            if (
                not isinstance(source_type, str)
                or not _snake_name(source_type).isidentifier()
                or keyword.iskeyword(_snake_name(source_type))
                or "url" not in properties
                or not isinstance(required, list)
                or "url" not in required
            ):
                continue
            all_property_specs = self._analyzer.property_specs(
                SchemaDefinition(definition_name, definition_schema)
            )
            url_annotation = next(
                property_spec.annotation
                for property_spec in all_property_specs
                if property_spec.name == "url"
            )
            property_specs = tuple(
                property_spec
                for property_spec in all_property_specs
                if property_spec.name not in {"type", "url"}
            )
            specs.append(
                LazyDataMethodSpec(source_type, url_annotation, property_specs)
            )
        return tuple(sorted(specs, key=lambda spec: spec.method_name))

    def capability_manifest(self) -> dict[str, Any]:
        """Return deterministic generated-API coverage metadata."""
        root_schema = self._definitions_map.get("CoreRootSpec", {})
        root_variants: list[str] = []
        if isinstance(root_schema, dict):
            variants = root_schema.get("anyOf", root_schema.get("oneOf", []))
            if isinstance(variants, list):
                for variant in variants:
                    if not isinstance(variant, dict):
                        continue
                    required = variant.get("required", [])
                    if not isinstance(required, list):
                        continue
                    structural = [
                        name
                        for name in required
                        if name
                        in {
                            "mark",
                            "layer",
                            "multiscale",
                            "vconcat",
                            "hconcat",
                            "concat",
                        }
                    ]
                    root_variants.extend(structural)

        return {
            "schema_version": self.schema_version,
            "definitions": [definition.name for definition in self.definitions()],
            "marks": list(self.mark_types()),
            "encoding_channels": list(self.encoding_channels()),
            "transforms": [
                {
                    "schema": spec.schema_name,
                    "type": spec.transform_type,
                    "method": spec.method_name,
                }
                for spec in self.transform_method_specs()
            ],
            "lazy_data_sources": [
                {
                    "type": spec.source_type,
                    "method": spec.method_name,
                }
                for spec in self.lazy_data_method_specs()
            ],
            "interaction": {
                "bindings": [
                    {
                        "helper": spec.helper_name,
                        "schema": spec.class_name,
                        "fixed": dict(spec.fixed_properties),
                    }
                    for spec in self.binding_factory_specs()
                ],
                "parameter_helpers": [
                    {
                        "helper": spec.helper_name,
                        "parameter_schema": spec.parameter_class_name,
                        "config_property": spec.config_property,
                        "config_schema": spec.config_class_name,
                        "fixed": dict(spec.fixed_properties),
                    }
                    for spec in self.parameter_config_factory_specs()
                ],
            },
            "root_spec_variants": root_variants,
        }

    def channel_nested_setters(
        self, encoding_name: str
    ) -> tuple[tuple[str, str, str], ...]:
        """Return nested setter properties available for an encoding channel."""
        encoding_schema = self._definitions_map.get("Encoding", {})
        if not isinstance(encoding_schema, dict):
            return ()
        properties = encoding_schema.get("properties", {})
        if not isinstance(properties, dict):
            return ()
        channel_schema = properties.get(encoding_name)
        if not isinstance(channel_schema, dict):
            return ()
        resolved_properties = self._analyzer.resolve_properties(channel_schema)
        available = {
            _class_name(definition.name): definition.schema
            for definition in self.definitions()
        }
        setters: list[tuple[str, str, str]] = []
        for property_name in sorted(resolved_properties):
            if property_name == "sort":
                continue
            nested_schema = resolved_properties[property_name]
            if not isinstance(nested_schema, dict):
                continue
            ref_name = _nested_setter_ref_name(nested_schema)
            if ref_name is None:
                continue
            class_name = _class_name(ref_name)
            definition_schema = available.get(class_name)
            if definition_schema is None or not _looks_like_object_schema(
                definition_schema
            ):
                continue
            setters.append(
                (
                    property_name,
                    class_name,
                    self._analyzer.raw_mapping_annotation(class_name),
                )
            )
        return tuple(setters)

    def channel_simple_setters(self, encoding_name: str) -> tuple[PropertySpec, ...]:
        """Return non-merge channel setters derived directly from the schema."""
        encoding_schema = self._definitions_map.get("Encoding", {})
        if not isinstance(encoding_schema, dict):
            return ()
        properties = encoding_schema.get("properties", {})
        if not isinstance(properties, dict):
            return ()
        channel_schema = properties.get(encoding_name)
        if not isinstance(channel_schema, dict):
            return ()
        nested_property_names = {
            property_name
            for property_name, _, _ in self.channel_nested_setters(encoding_name)
        }
        definition = SchemaDefinition(encoding_name, channel_schema)
        return tuple(
            property_spec
            for property_spec in self._analyzer.property_specs(definition)
            if not keyword.iskeyword(property_spec.name)
            and (
                property_spec.name not in nested_property_names
                or property_spec.name == "sort"
            )
        )

    def channel_property_specs(self, encoding_name: str) -> tuple[PropertySpec, ...]:
        """Return all schema properties accepted by an encoding channel."""
        encoding_schema = self._definitions_map.get("Encoding", {})
        if not isinstance(encoding_schema, dict):
            return ()
        properties = encoding_schema.get("properties", {})
        if not isinstance(properties, dict):
            return ()
        channel_schema = properties.get(encoding_name)
        if not isinstance(channel_schema, dict):
            return ()
        return self._analyzer.property_specs(
            SchemaDefinition(encoding_name, channel_schema)
        )

    def generate_core_module(self) -> GeneratedModule:
        """Generate a compact ``core.py``-style module."""
        exports: list[str] = ["GenomeSpySchema", "MARK_TYPES", "Root", "load_schema"]
        class_chunks: list[GeneratedSchemaClass] = []
        needs_literal = False
        needs_sequence = False
        type_alias_names = set(self.scalar_type_aliases())
        kwds_type_names = set(self.kwds_type_names())
        seen_class_names = {"GenomeSpySchema", "Root"}

        for definition in self.definitions():
            class_name = _class_name(definition.name)
            if class_name in seen_class_names:
                class_name = f"{class_name}Def"
            seen_class_names.add(class_name)
            exports.append(class_name)
            generated_class = _schema_class_source(
                class_name,
                definition,
                analyzer=self._analyzer,
            )
            class_chunks.append(generated_class)
            needs_literal = needs_literal or generated_class.needs_literal
            needs_sequence = needs_sequence or generated_class.needs_sequence
        used_type_aliases = sorted(
            {
                alias_name
                for generated_class in class_chunks
                for alias_name in generated_class.used_aliases
                if alias_name in type_alias_names
            }
        )
        used_kwds_types = sorted(
            {
                kwds_name
                for generated_class in class_chunks
                for kwds_name in generated_class.used_kwds
                if kwds_name in kwds_type_names
            }
        )

        typing_imports = ["Any", "cast"]
        if needs_literal:
            typing_imports.append("Literal")

        chunks = [
            GENERATED_HEADER,
            "from __future__ import annotations",
            "import json",
            ("from collections.abc import Sequence" if needs_sequence else ""),
            "from importlib.resources import files",
            "from typing import " + ", ".join(typing_imports),
            "",
            (
                "from genome_spy.schema._typing import " + ", ".join(used_type_aliases)
                if used_type_aliases
                else ""
            ),
            (
                "from genome_spy.schema._kwds import " + ", ".join(used_kwds_types)
                if used_kwds_types
                else ""
            ),
            "from genome_spy.schemapi import SchemaBase, Undefined, UndefinedType",
            "",
            "def load_schema() -> dict[str, Any]:",
            '    """Load the packaged GenomeSpy JSON Schema."""',
            '    schema_path = files(__package__).joinpath("genome-spy-schema.json")',
            '    schema = json.loads(schema_path.read_text(encoding="utf-8"))',
            "    if not isinstance(schema, dict):",
            '        raise TypeError("Packaged GenomeSpy schema must be a JSON object.")',
            "    return cast(dict[str, Any], schema)",
            "",
            "_ROOT_SCHEMA = load_schema()",
            "MARK_TYPES = " + repr(self.mark_types()),
            "",
            "class GenomeSpySchema(SchemaBase):",
            '    """Base class for generated GenomeSpy schema wrappers."""',
            "",
            "    _rootschema = _ROOT_SCHEMA",
            "",
            "class Root(GenomeSpySchema):",
            '    """Generated wrapper for the root GenomeSpy specification."""',
            "",
            "    _schema = _ROOT_SCHEMA",
            "",
            "    def __init__(self, **kwds: Any) -> None:",
            "        super().__init__(**kwds)",
        ]
        chunks.extend(generated_class.source for generated_class in class_chunks)

        all_line = "__all__ = " + repr(exports)
        return GeneratedModule(
            source="\n".join([*chunks, all_line]) + "\n", exports=tuple(exports)
        )

    def generate_init_module(
        self,
        core_exports: tuple[str, ...],
        typing_exports: tuple[str, ...],
        kwds_exports: tuple[str, ...],
    ) -> GeneratedModule:
        """Generate the package ``__init__.py`` for schema wrappers."""
        exports = (*core_exports, *typing_exports, *kwds_exports, "SCHEMA_VERSION")
        source = "\n".join(
            [
                GENERATED_HEADER,
                "from genome_spy.schema.core import (",
                *[f"    {name}," for name in core_exports],
                ")",
                ("from genome_spy.schema._typing import (" if typing_exports else ""),
                *(
                    [f"    {name}," for name in typing_exports]
                    if typing_exports
                    else []
                ),
                (")" if typing_exports else ""),
                ("from genome_spy.schema._kwds import (" if kwds_exports else ""),
                *([f"    {name}," for name in kwds_exports] if kwds_exports else []),
                (")" if kwds_exports else ""),
                "",
                "SCHEMA_VERSION = " + repr(self.schema_version),
                "",
                "__all__ = " + repr(list(exports)),
                "",
            ]
        )
        return GeneratedModule(source=source, exports=exports)

    def scalar_type_aliases(self) -> tuple[str, ...]:
        """Return exported alias names for scalar-like named definitions."""
        aliases: list[str] = []
        for definition in self.definitions():
            if not self._analyzer.is_scalar_aliasable(
                definition.schema,
                seen_refs=frozenset({definition.name}),
            ):
                continue
            spec = self._analyzer.property_annotation_spec(definition.schema)
            if spec.annotation == "Any":
                continue
            aliases.append(_type_alias_name(definition.name))
        return tuple(aliases)

    def generate_typing_module(self) -> GeneratedModule:
        """Generate a small module of shared scalar-like schema aliases."""
        aliases: list[tuple[str, AnnotationSpec]] = []
        for definition in self.definitions():
            if not self._analyzer.is_scalar_aliasable(
                definition.schema,
                seen_refs=frozenset({definition.name}),
            ):
                continue
            spec = self._analyzer.property_annotation_spec(definition.schema)
            if spec.annotation == "Any":
                continue
            aliases.append((_type_alias_name(definition.name), spec))
        aliases = _sort_alias_specs(aliases)

        needs_literal = any(spec.needs_literal for _, spec in aliases)
        needs_sequence = any(spec.needs_sequence for _, spec in aliases)
        typing_imports = ["TypeAlias"]
        if needs_literal:
            typing_imports.append("Literal")

        source = "\n".join(
            [
                GENERATED_HEADER,
                "from __future__ import annotations",
                ("from collections.abc import Sequence" if needs_sequence else ""),
                ("from typing import " + ", ".join(typing_imports) if aliases else ""),
                "",
                *[
                    f"{alias_name}: TypeAlias = {spec.annotation}"
                    for alias_name, spec in aliases
                ],
                "",
                "__all__ = " + repr([alias_name for alias_name, _ in aliases]),
                "",
            ]
        )
        return GeneratedModule(
            source=source,
            exports=tuple(alias_name for alias_name, _ in aliases),
        )

    def kwds_type_names(self) -> tuple[str, ...]:
        """Return exported TypedDict helper names for selected object-like defs."""
        names: list[str] = []
        for definition in self.definitions():
            class_name = _class_name(definition.name)
            if class_name not in KWDS_TARGETS:
                continue
            if not self._supports_kwds_helper(definition):
                continue
            names.append(_kwds_type_name(definition.name))
        names.extend(self._anonymous_kwds_specs())
        return tuple(names)

    def generate_kwds_module(self) -> GeneratedModule:
        """Generate selective TypedDict helpers for config-heavy object shapes."""
        helper_specs: list[tuple[str, tuple[PropertySpec, ...]]] = []
        needs_any = False
        needs_literal = False
        needs_sequence = False
        used_aliases: set[str] = set()
        available_class_names = {
            _class_name(definition.name) for definition in self.definitions()
        }
        used_core_classes: set[str] = set()

        for definition in self.definitions():
            class_name = _class_name(definition.name)
            if class_name not in KWDS_TARGETS:
                continue
            if not self._supports_kwds_helper(definition):
                continue
            helper_name = _kwds_type_name(definition.name)
            property_specs = self._analyzer.property_specs(definition)
            helper_specs.append((helper_name, property_specs))
            for property_spec in property_specs:
                needs_any = needs_any or _annotation_mentions_any(
                    property_spec.annotation.annotation
                )
                needs_literal = needs_literal or property_spec.annotation.needs_literal
                needs_sequence = (
                    needs_sequence or property_spec.annotation.needs_sequence
                )
                used_aliases.update(
                    _annotation_alias_names(property_spec.annotation.annotation)
                )
                used_core_classes.update(
                    set(_annotation_class_names(property_spec.annotation.annotation))
                    & available_class_names
                )

        extra_helper_specs = self._anonymous_kwds_specs()
        helper_specs.extend(extra_helper_specs.items())
        for _, property_specs in extra_helper_specs.items():
            for property_spec in property_specs:
                annotation = property_spec.annotation
                needs_any = needs_any or _annotation_mentions_any(annotation.annotation)
                needs_literal = needs_literal or annotation.needs_literal
                needs_sequence = needs_sequence or annotation.needs_sequence
                used_aliases.update(_annotation_alias_names(annotation.annotation))
                used_core_classes.update(
                    set(_annotation_class_names(annotation.annotation))
                    & available_class_names
                )

        typing_imports = ["TYPE_CHECKING", "TypedDict"]
        if needs_any:
            typing_imports.append("Any")
        if needs_literal:
            typing_imports.append("Literal")

        source = "\n".join(
            [
                GENERATED_HEADER,
                "from __future__ import annotations",
                ("from collections.abc import Sequence" if needs_sequence else ""),
                (
                    "from typing import " + ", ".join(typing_imports)
                    if helper_specs
                    else ""
                ),
                "",
                (
                    "from genome_spy.schema._typing import "
                    + ", ".join(sorted(used_aliases))
                    if used_aliases
                    else ""
                ),
                (
                    "if TYPE_CHECKING:\n    from genome_spy.schema.core import "
                    + ", ".join(
                        sorted(
                            core_name
                            for core_name in used_core_classes
                            if core_name in available_class_names
                        )
                    )
                    if used_core_classes
                    else ""
                ),
                "",
                *[
                    _typed_dict_source(helper_name, property_specs)
                    for helper_name, property_specs in helper_specs
                ],
                "__all__ = " + repr([helper_name for helper_name, _ in helper_specs]),
                "",
            ]
        )
        return GeneratedModule(
            source=source,
            exports=tuple(helper_name for helper_name, _ in helper_specs),
        )

    def _supports_kwds_helper(self, definition: SchemaDefinition) -> bool:
        """Return whether a definition can produce a useful TypedDict helper."""
        return bool(self._base_analyzer.property_specs(definition)) or (
            self._base_analyzer.schema_looks_object_like(definition.schema)
        )

    def _anonymous_kwds_specs(self) -> dict[str, tuple[PropertySpec, ...]]:
        """Return TypedDict specs for anonymous root mapping properties."""
        specs: dict[str, tuple[PropertySpec, ...]] = {}
        value_annotations = {
            "axes": "GenomeAxis | GenomeAxisKwds",
            "legends": "Legend | LegendKwds",
            "scales": "Scale | ScaleKwds",
        }
        for property_name, helper_name in ANONYMOUS_PROPERTY_KWDS.items():
            schema = self.root_property_schema(property_name)
            properties = schema.get("properties", {})
            if not isinstance(properties, dict) or not properties:
                continue
            if property_name == "resolve":
                outer_specs: list[PropertySpec] = []
                for name, nested_schema in sorted(properties.items()):
                    if not isinstance(name, str) or not isinstance(nested_schema, dict):
                        continue
                    nested_properties = nested_schema.get("properties", {})
                    if not isinstance(nested_properties, dict):
                        continue
                    nested_helper_name = f"{_class_name(name)}ResolveKwds"
                    specs[nested_helper_name] = (
                        self._base_analyzer.property_specs_from_properties(
                            nested_properties
                        )
                    )
                    outer_specs.append(
                        PropertySpec(name, AnnotationSpec(nested_helper_name))
                    )
                specs[helper_name] = tuple(outer_specs)
                continue

            value_annotation = value_annotations[property_name]
            specs[helper_name] = tuple(
                PropertySpec(
                    name=name,
                    annotation=AnnotationSpec(value_annotation),
                    description=_property_description(property_schema),
                )
                for name, property_schema in sorted(properties.items())
                if isinstance(name, str) and isinstance(property_schema, dict)
            )
        return specs

    def generate_mark_mixins_module(self) -> GeneratedModule:
        """Generate schema-driven mixins for the handwritten chart API."""
        mark_property_specs = {
            mark_type: self.mark_property_specs(mark_type)
            for mark_type in self.mark_types()
        }
        mark_methods = [
            _mark_method_source(
                mark_type,
                property_specs=mark_property_specs[mark_type],
            )
            for mark_type in self.mark_types()
        ]
        if "point" in mark_property_specs:
            mark_methods.append(
                _mark_method_source(
                    "point",
                    method_name="circle",
                    property_specs=mark_property_specs["point"],
                )
            )
        mark_annotations = [
            property_spec.annotation
            for property_specs in mark_property_specs.values()
            for property_spec in property_specs
        ]
        encoding_property_specs = self.schema_property_specs("Encoding")
        encoding_method = _encoding_method_source(encoding_property_specs)
        resolution_method_specs = self.resolution_method_specs()
        resolution_methods = [
            _resolution_method_source(name, property_specs)
            for name, property_specs in resolution_method_specs.items()
        ]
        properties_specs = {
            "UnitPropertiesMixin": (
                self.top_level_property_specs("UnitSpec"),
                ("data", "mark", "encoding"),
            ),
            "LayerPropertiesMixin": (
                self.top_level_property_specs("LayerSpec"),
                ("layer",),
            ),
            "HConcatPropertiesMixin": (
                self.top_level_property_specs("HConcatSpec"),
                ("hconcat",),
            ),
            "VConcatPropertiesMixin": (
                self.top_level_property_specs("VConcatSpec"),
                ("vconcat",),
            ),
            "ConcatPropertiesMixin": (
                self.top_level_property_specs("ConcatSpec"),
                ("concat", "columns"),
            ),
            "MultiscalePropertiesMixin": (
                self.top_level_property_specs("MultiscaleSpec"),
                ("multiscale", "stops"),
            ),
        }
        imported_view_specs = self.schema_property_specs("ImportSpec")
        property_mixins = [
            _properties_mixin_source(
                name,
                property_specs,
                positional_properties=positional_properties,
            )
            for name, (
                property_specs,
                positional_properties,
            ) in properties_specs.items()
        ]
        unit_properties = {
            property_spec.name: property_spec
            for property_spec in properties_specs["UnitPropertiesMixin"][0]
        }
        top_level_merge_specs = [
            (
                unit_properties[name],
                (
                    self.schema_property_specs(
                        unit_properties[name].nested_schema_class_name
                    )
                    if unit_properties[name].nested_schema_class_name is not None
                    else self.shared_scale_property_specs()
                ),
            )
            for name in ("config", "view", "scales")
            if name in unit_properties
        ]
        top_level_merge_methods = [
            _top_level_merge_method_source(property_spec, property_specs)
            for property_spec, property_specs in top_level_merge_specs
        ]
        config_property_specs = self.schema_property_specs("GenomeSpyConfig")
        config_method_specs = self.config_method_specs()
        config_methods = [
            _config_method_source(
                property_name,
                annotation=annotation,
                nested_schema_class_name=nested_schema_class_name,
                raw_mapping_annotation=raw_mapping_annotation,
                property_specs=property_specs,
            )
            for (
                property_name,
                annotation,
                nested_schema_class_name,
                raw_mapping_annotation,
                property_specs,
            ) in config_method_specs
        ]
        config_annotations = [
            property_spec.annotation for property_spec in config_property_specs
        ] + [
            property_spec.annotation
            for *_, property_specs in config_method_specs
            for property_spec in property_specs
        ]
        top_level_merge_annotations = [
            property_spec.annotation
            for _, property_specs in top_level_merge_specs
            for property_spec in property_specs
        ]
        config_helper_kwds_names = {
            kwds_name
            for annotation in config_annotations
            for kwds_name in _annotation_kwds_names(annotation.annotation)
        }
        transform_method_specs = self.transform_method_specs()
        has_filter_method = any(
            spec.transform_type == "filter" for spec in transform_method_specs
        )
        has_expression_transform = any(
            property_spec.name == "expr"
            for spec in transform_method_specs
            for property_spec in spec.properties
        )
        transform_methods = [
            _transform_method_source(spec) for spec in transform_method_specs
        ]
        transform_annotations = [
            property_spec.annotation
            for spec in transform_method_specs
            for property_spec in spec.properties
        ]
        all_method_annotations = [
            *mark_annotations,
            *config_annotations,
            *top_level_merge_annotations,
            *(property_spec.annotation for property_spec in encoding_property_specs),
            *(property_spec.annotation for property_spec in imported_view_specs),
            *(
                property_spec.annotation
                for specs, _ in properties_specs.values()
                for property_spec in specs
            ),
            *transform_annotations,
            *(
                property_spec.annotation
                for property_specs in resolution_method_specs.values()
                for property_spec in property_specs
            ),
        ]
        needs_literal = any(
            annotation.needs_literal for annotation in all_method_annotations
        )
        needs_sequence = any(
            annotation.needs_sequence for annotation in all_method_annotations
        )
        transform_alias_names = {
            alias_name
            for annotation in all_method_annotations
            for alias_name in _annotation_alias_names(annotation.annotation)
        }
        transform_kwds_names = {
            kwds_name
            for annotation in all_method_annotations
            for kwds_name in _annotation_kwds_names(annotation.annotation)
        }
        available_class_names = {
            _class_name(definition.name) for definition in self.definitions()
        }
        transform_class_names = {
            class_name
            for annotation in all_method_annotations
            for class_name in _annotation_class_names(annotation.annotation)
            if class_name in available_class_names
        }
        typing_imports = ["Any", "Self"]
        if needs_literal:
            typing_imports.append("Literal")
        if has_expression_transform:
            typing_imports.append("cast")
        source = "\n".join(
            [
                GENERATED_HEADER,
                "from __future__ import annotations",
                ("from collections.abc import Sequence" if needs_sequence else ""),
                "from typing import " + ", ".join(typing_imports),
                "",
                "from typing import TYPE_CHECKING",
                "",
                "if TYPE_CHECKING:",
                "    from genome_spy.channels import Channel",
                *(
                    ["    from genome_spy._parameters import Parameter"]
                    if has_filter_method
                    else []
                ),
                "",
                (
                    "from genome_spy._expressions import ExpressionOperand, _expression_string"
                    if has_expression_transform
                    else ""
                ),
                (
                    "from genome_spy.schema._typing import "
                    + ", ".join(sorted(transform_alias_names))
                    if transform_alias_names
                    else ""
                ),
                "from genome_spy.schemapi import SchemaBase, Undefined, UndefinedType",
                (
                    "from genome_spy.schema import core"
                    if config_method_specs or transform_class_names
                    else ""
                ),
                (
                    "from genome_spy.schema._kwds import "
                    + ", ".join(
                        sorted(
                            config_helper_kwds_names
                            | transform_kwds_names
                            | {"GenomeSpyConfigKwds"}
                        )
                    )
                    if config_helper_kwds_names
                    or transform_kwds_names
                    or config_method_specs
                    else ""
                ),
                "class MarkMethodMixin:",
                '    """Grammar-derived mark methods for the handwritten chart API."""',
                "",
                *(mark_methods or ["    pass"]),
                "",
                "class EncodingMethodMixin:",
                '    """Schema-derived encoding methods for renderable specifications."""',
                "",
                encoding_method,
                "",
                "class ResolutionMethodMixin:",
                '    """Schema-derived composition resolution methods."""',
                "",
                *(resolution_methods if resolution_method_specs else ["    pass"]),
                "",
                "class TopLevelMergeMixin:",
                '    """Schema-derived top-level property merge methods."""',
                "",
                *(top_level_merge_methods or ["    pass"]),
                "",
                _imported_view_constructor_mixin_source(imported_view_specs),
                "",
                *property_mixins,
                *(
                    [
                        "",
                        "class ConfigMethodMixin:",
                        '    """Schema-derived config methods for the handwritten chart API."""',
                        "",
                        _configure_method_source(config_property_specs),
                        *(config_methods or ["    pass"]),
                    ]
                    if config_method_specs
                    else []
                ),
                "",
                "class TransformMethodMixin:",
                '    """Schema-derived transform methods for top-level specifications."""',
                "",
                *(transform_methods or ["    pass"]),
                "",
                (
                    '__all__ = ["ConcatPropertiesMixin", "ConfigMethodMixin", "EncodingMethodMixin", "HConcatPropertiesMixin", "ImportedViewConstructorMixin", "LayerPropertiesMixin", "MarkMethodMixin", "MultiscalePropertiesMixin", "ResolutionMethodMixin", "TopLevelMergeMixin", "TransformMethodMixin", "UnitPropertiesMixin", "VConcatPropertiesMixin"]'
                    if config_method_specs
                    else '__all__ = ["ConcatPropertiesMixin", "EncodingMethodMixin", "HConcatPropertiesMixin", "ImportedViewConstructorMixin", "LayerPropertiesMixin", "MarkMethodMixin", "MultiscalePropertiesMixin", "ResolutionMethodMixin", "TopLevelMergeMixin", "TransformMethodMixin", "UnitPropertiesMixin", "VConcatPropertiesMixin"]'
                ),
                "",
            ]
        )
        return GeneratedModule(
            source=source,
            exports=(
                (
                    "ConcatPropertiesMixin",
                    "ConfigMethodMixin",
                    "EncodingMethodMixin",
                    "HConcatPropertiesMixin",
                    "ImportedViewConstructorMixin",
                    "LayerPropertiesMixin",
                    "MarkMethodMixin",
                    "MultiscalePropertiesMixin",
                    "ResolutionMethodMixin",
                    "TopLevelMergeMixin",
                    "TransformMethodMixin",
                    "UnitPropertiesMixin",
                    "VConcatPropertiesMixin",
                )
                if config_method_specs
                else (
                    "ConcatPropertiesMixin",
                    "EncodingMethodMixin",
                    "HConcatPropertiesMixin",
                    "ImportedViewConstructorMixin",
                    "LayerPropertiesMixin",
                    "MarkMethodMixin",
                    "MultiscalePropertiesMixin",
                    "ResolutionMethodMixin",
                    "TopLevelMergeMixin",
                    "TransformMethodMixin",
                    "UnitPropertiesMixin",
                    "VConcatPropertiesMixin",
                )
            ),
        )

    def mark_signature_class(self, mark_type: str) -> str | None:
        """Return the best generated schema class to use for a mark method signature."""
        class_stem = _class_name(mark_type)
        candidates = (
            f"{class_stem}Props",
            f"{class_stem}Config",
            "MarkProps",
            "MarkConfig",
        )
        available = {_class_name(definition.name) for definition in self.definitions()}
        for candidate in candidates:
            if candidate in available:
                return candidate
        return None

    def mark_property_specs(self, mark_type: str) -> tuple[PropertySpec, ...]:
        """Return the fixed mark's schema-derived keyword parameters."""
        signature_class = self.mark_signature_class(mark_type)
        if signature_class is None:
            return ()
        definition = next(
            definition
            for definition in self.definitions()
            if _class_name(definition.name) == signature_class
        )
        return tuple(
            property_spec
            for property_spec in self._analyzer.property_specs(definition)
            if property_spec.name != "type"
        )

    def schema_property_specs(self, class_name: str) -> tuple[PropertySpec, ...]:
        """Return generated properties for a schema wrapper class name."""
        definition = next(
            (
                definition
                for definition in self.definitions()
                if _class_name(definition.name) == class_name
            ),
            None,
        )
        if definition is None:
            return ()
        return self._analyzer.property_specs(definition)

    def top_level_property_specs(self, class_name: str) -> tuple[PropertySpec, ...]:
        """Return properties from the matching concrete root-spec variant."""
        definition = next(
            (
                definition
                for definition in self.definitions()
                if _class_name(definition.name) == class_name
            ),
            None,
        )
        properties: dict[str, PropertySpec] = {}
        root_schema = self._definitions_map.get("CoreRootSpec", {})
        root_variants = (
            root_schema.get("anyOf", []) if isinstance(root_schema, dict) else []
        )
        if definition is not None and isinstance(root_variants, list):
            required = set(definition.required)
            root_variant = next(
                (
                    variant
                    for variant in root_variants
                    if isinstance(variant, dict)
                    and set(variant.get("required", [])) == required
                ),
                None,
            )
            if root_variant is not None:
                properties.update(
                    {
                        property_spec.name: property_spec
                        for property_spec in self._analyzer.property_specs(
                            SchemaDefinition(
                                f"CoreRootSpec[{class_name}]", root_variant
                            )
                        )
                    }
                )
        properties.update(
            {
                property_spec.name: property_spec
                for property_spec in self.schema_property_specs(class_name)
            }
        )
        if "data" in properties:
            properties["data"] = replace(
                properties["data"], annotation=AnnotationSpec("Any")
            )
        return tuple(properties[name] for name in sorted(properties))

    def root_property_schema(self, property_name: str) -> dict[str, Any]:
        """Return a root property schema from the first concrete root variant."""
        root_schema = self._definitions_map.get("CoreRootSpec", {})
        variants = root_schema.get("anyOf", []) if isinstance(root_schema, dict) else []
        if not isinstance(variants, list):
            return {}
        for variant in variants:
            if not isinstance(variant, dict):
                continue
            properties = variant.get("properties", {})
            if isinstance(properties, dict):
                schema = properties.get(property_name)
                if isinstance(schema, dict):
                    return schema
        return {}

    def shared_scale_property_specs(self) -> tuple[PropertySpec, ...]:
        """Return schema-derived shared-scale channel definitions."""
        properties = self.root_property_schema("scales").get("properties", {})
        if not isinstance(properties, dict):
            return ()
        return self._analyzer.property_specs_from_properties(properties)

    def resolution_method_specs(self) -> dict[str, tuple[PropertySpec, ...]]:
        """Return schema-derived resolution fields grouped by component."""
        properties = self.root_property_schema("resolve").get("properties", {})
        if not isinstance(properties, dict):
            return {}
        specs: dict[str, tuple[PropertySpec, ...]] = {}
        for name, schema in sorted(properties.items()):
            if not isinstance(name, str) or not isinstance(schema, dict):
                continue
            # Since 0.85.0 the components reference a shared ResolutionMap
            # definition instead of inlining their channel properties.
            ref_name = _ref_name(schema)
            if ref_name is not None:
                referenced = self._definitions_map.get(ref_name)
                if isinstance(referenced, dict):
                    schema = referenced
            nested_properties = schema.get("properties", {})
            if isinstance(nested_properties, dict) and nested_properties:
                specs[name] = self._analyzer.property_specs_from_properties(
                    nested_properties
                )
        return specs

    def config_method_specs(
        self,
    ) -> list[tuple[str, str, str | None, str, tuple[PropertySpec, ...]]]:
        """Return generated method specs for GenomeSpyConfig properties."""
        try:
            definition = next(
                definition
                for definition in self.definitions()
                if definition.name == "GenomeSpyConfig"
            )
        except StopIteration:
            return []

        specs: list[tuple[str, str, str | None, str, tuple[PropertySpec, ...]]] = []
        for property_spec in self._analyzer.property_specs(definition):
            raw_mapping_annotation = (
                self._analyzer.raw_mapping_annotation(
                    property_spec.nested_schema_class_name
                )
                if property_spec.nested_schema_class_name is not None
                else "dict[str, Any]"
            )
            specs.append(
                (
                    property_spec.name,
                    property_spec.annotation.annotation,
                    property_spec.nested_schema_class_name,
                    raw_mapping_annotation,
                    (
                        self.schema_property_specs(
                            property_spec.nested_schema_class_name
                        )
                        if property_spec.nested_schema_class_name is not None
                        else ()
                    ),
                )
            )
        return specs

    def generate_channels_module(self) -> GeneratedModule:
        """Generate named channel wrappers from the upstream encoding schema."""
        exports: list[str] = []
        classes: list[str] = []
        kwds_type_names = set(self.kwds_type_names())
        available_class_names = {
            _class_name(definition.name) for definition in self.definitions()
        }
        simple_setters_by_channel = {
            encoding_name: self.channel_simple_setters(encoding_name)
            for encoding_name in self.encoding_channels()
        }
        sort_property_specs = self.schema_property_specs("CompareParams")
        nested_property_specs_by_channel = {
            encoding_name: {
                property_name: self.schema_property_specs(class_name)
                for property_name, class_name, _ in self.channel_nested_setters(
                    encoding_name
                )
            }
            for encoding_name in self.encoding_channels()
        }
        helper_class_names = {
            class_name
            for encoding_name in self.encoding_channels()
            for _, class_name, _ in self.channel_nested_setters(encoding_name)
        }
        simple_setter_specs = tuple(
            property_spec
            for encoding_name in self.encoding_channels()
            for property_spec in simple_setters_by_channel[encoding_name]
        )
        nested_setter_specs = tuple(
            property_spec
            for property_specs in nested_property_specs_by_channel.values()
            for specs in property_specs.values()
            for property_spec in specs
        )
        channel_setter_specs = (
            *simple_setter_specs,
            *nested_setter_specs,
            *sort_property_specs,
        )
        helper_kwds_names = {
            _kwds_type_name(class_name)
            for class_name in helper_class_names
            if _kwds_type_name(class_name) in kwds_type_names
        }
        helper_kwds_names.update(
            kwds_name
            for property_spec in channel_setter_specs
            for kwds_name in _annotation_kwds_names(property_spec.annotation.annotation)
            if kwds_name in kwds_type_names
        )
        helper_alias_names = sorted(
            {
                alias_name
                for property_spec in channel_setter_specs
                for alias_name in _annotation_alias_names(
                    property_spec.annotation.annotation
                )
            }
        )
        simple_setter_class_names = {
            class_name
            for property_spec in simple_setter_specs
            for class_name in _annotation_class_names(
                property_spec.annotation.annotation
            )
            if class_name in available_class_names
        }
        needs_sequence = any(
            property_spec.annotation.needs_sequence
            for property_spec in channel_setter_specs
        )
        needs_literal = any(
            property_spec.annotation.needs_literal
            for property_spec in channel_setter_specs
        )
        for encoding_name in self.encoding_channels():
            class_name = _class_name(encoding_name)
            exports.append(class_name)
            classes.append(
                _channel_class_source(
                    class_name,
                    encoding_name,
                    nested_setters=self.channel_nested_setters(encoding_name),
                    nested_property_specs=nested_property_specs_by_channel[
                        encoding_name
                    ],
                    simple_setters=simple_setters_by_channel[encoding_name],
                    constructor_property_specs=self.channel_property_specs(
                        encoding_name
                    ),
                    sort_property_specs=sort_property_specs,
                )
            )
        needs_compare_params = bool(sort_property_specs)
        source = "\n".join(
            [
                GENERATED_HEADER,
                "from __future__ import annotations",
                ("from collections.abc import Sequence" if needs_sequence else ""),
                "from typing import Any" + (", Literal" if needs_literal else ""),
                "",
                "from genome_spy.channels import Channel, _MISSING, channel",
                "from genome_spy.schemapi import SchemaBase, Undefined, UndefinedType",
                "from genome_spy.schema import core",
                (
                    "from genome_spy.schema._typing import "
                    + ", ".join(helper_alias_names)
                    if helper_alias_names
                    else ""
                ),
                (
                    "from genome_spy.schema.core import "
                    + ", ".join(
                        sorted(
                            helper_class_names
                            | simple_setter_class_names
                            | ({"CompareParams"} if needs_compare_params else set())
                        )
                    )
                    if helper_class_names
                    or simple_setter_class_names
                    or needs_compare_params
                    else ""
                ),
                (
                    "from genome_spy.schema._kwds import "
                    + ", ".join(
                        sorted(
                            helper_kwds_names
                            | ({"CompareParamsKwds"} if needs_compare_params else set())
                        )
                    )
                    if helper_kwds_names or needs_compare_params
                    else ""
                ),
                "",
                *classes,
                "__all__ = " + repr(exports),
                "",
            ]
        )
        return GeneratedModule(source=source, exports=tuple(exports))

    def generate_composition_module(self) -> GeneratedModule:
        """Generate public composition helper functions from top-level specs."""
        specs = (
            ("layer", "LayerSpec", "layer", "LayerChart", ()),
            ("hconcat", "HConcatSpec", "hconcat", "HConcatChart", ()),
            ("vconcat", "VConcatSpec", "vconcat", "VConcatChart", ()),
            ("concat", "ConcatSpec", "concat", "ConcatChart", ("columns",)),
            (
                "multiscale",
                "MultiscaleSpec",
                "multiscale",
                "MultiscaleChart",
                ("stops",),
            ),
        )
        method_specs = [
            (
                name,
                child_key,
                return_class,
                self._composition_property_specs(schema_class, child_key, required),
                tuple(
                    property_spec
                    for property_spec in self.top_level_property_specs(schema_class)
                    if property_spec.name in required
                ),
            )
            for name, schema_class, child_key, return_class, required in specs
        ]
        import_property_specs = tuple(
            property_spec
            for property_spec in self.schema_property_specs("ImportSpec")
            if property_spec.name != "import"
        )
        annotations = [
            property_spec.annotation
            for _, _, _, property_specs, required_specs in method_specs
            for property_spec in (*property_specs, *required_specs)
        ] + [property_spec.annotation for property_spec in import_property_specs]
        aliases = sorted(
            {
                alias
                for annotation in annotations
                for alias in _annotation_alias_names(annotation.annotation)
            }
        )
        kwds = sorted(
            {
                name
                for annotation in annotations
                for name in _annotation_kwds_names(annotation.annotation)
            }
        )
        needs_literal = any(annotation.needs_literal for annotation in annotations)
        needs_sequence = any(annotation.needs_sequence for annotation in annotations)
        return GeneratedModule(
            source="\n".join(
                [
                    GENERATED_HEADER,
                    "from __future__ import annotations",
                    ("from collections.abc import Sequence" if needs_sequence else ""),
                    "from typing import Any, cast"
                    + (", Literal" if needs_literal else ""),
                    "",
                    "from typing import TYPE_CHECKING",
                    "",
                    "if TYPE_CHECKING:",
                    "    from genome_spy.chart import "
                    + ", ".join(
                        sorted(
                            {
                                *(
                                    return_class
                                    for _, _, return_class, _, _ in method_specs
                                ),
                                "ImportedView",
                                "TopLevelSpec",
                            }
                        )
                    ),
                    "",
                    (
                        "from genome_spy.schema._typing import " + ", ".join(aliases)
                        if aliases
                        else ""
                    ),
                    (
                        "from genome_spy.schema._kwds import " + ", ".join(kwds)
                        if kwds
                        else ""
                    ),
                    "from genome_spy.schemapi import Undefined, UndefinedType",
                    "from genome_spy.schema import core",
                    "",
                    *(
                        _composition_function_source(
                            name,
                            child_key=child_key,
                            return_class=return_class,
                            property_specs=property_specs,
                            required_specs=required_specs,
                        )
                        for name, child_key, return_class, property_specs, required_specs in method_specs
                    ),
                    _import_view_function_source(import_property_specs),
                    "",
                    "__all__ = "
                    + repr([*(name for name, *_ in method_specs), "import_view"]),
                    "",
                ]
            ),
            exports=tuple([*(name for name, *_ in method_specs), "import_view"]),
        )

    def generate_lazy_module(self) -> GeneratedModule:
        """Generate named lazy data-source helpers from ``LazyDataParams``."""
        method_specs = self.lazy_data_method_specs()
        annotations = [
            annotation
            for spec in method_specs
            for annotation in (
                spec.url_annotation,
                *(p.annotation for p in spec.properties),
            )
        ]
        aliases = sorted(
            {
                alias
                for annotation in annotations
                for alias in _annotation_alias_names(annotation.annotation)
            }
        )
        kwds = sorted(
            {
                name
                for annotation in annotations
                for name in _annotation_kwds_names(annotation.annotation)
            }
        )
        needs_literal = any(annotation.needs_literal for annotation in annotations)
        needs_sequence = any(annotation.needs_sequence for annotation in annotations)
        source = "\n".join(
            [
                GENERATED_HEADER,
                "from __future__ import annotations",
                ("from collections.abc import Sequence" if needs_sequence else ""),
                "from typing import Any, cast" + (", Literal" if needs_literal else ""),
                "",
                (
                    "from genome_spy.schema._typing import " + ", ".join(aliases)
                    if aliases
                    else ""
                ),
                (
                    "from genome_spy.schema._kwds import " + ", ".join(kwds)
                    if kwds
                    else ""
                ),
                "from genome_spy.schemapi import Undefined, UndefinedType",
                "from genome_spy.schema import core",
                "",
                "class LazyDataMethodMixin:",
                '    """Schema-derived named lazy data-source helpers."""',
                "",
                *(_lazy_data_method_source(spec) for spec in method_specs),
                *(["    pass"] if not method_specs else []),
                "",
                "__all__ = ['LazyDataMethodMixin']",
                "",
            ]
        )
        return GeneratedModule(source=source, exports=("LazyDataMethodMixin",))

    def generate_ergonomics_module(self) -> GeneratedModule:
        """Generate small schema-backed public authoring helpers."""
        locus_properties = self.schema_property_specs("ChromPosDef")
        locus_property_specs = tuple(
            property_spec
            for property_spec in locus_properties
            if property_spec.name not in {"chrom", "pos", "type"}
        )
        locus_annotations = [
            property_spec.annotation for property_spec in locus_property_specs
        ]
        locus_nested_specs = {
            "axis": self.schema_property_specs("GenomeAxis"),
            "scale": self.schema_property_specs("Scale"),
        }
        channel_nested_specs = {
            "axis": (
                "core.GenomeAxis | GenomeAxisKwds | None | object",
                self.schema_property_specs("GenomeAxis"),
            ),
            "scale": (
                "core.Scale | ScaleKwds | None | object",
                self.schema_property_specs("Scale"),
            ),
            "legend": (
                "core.Legend | LegendKwds | None | object",
                self.schema_property_specs("Legend"),
            ),
        }
        compare_properties = self.schema_property_specs("CompareParams")
        datum_properties = self.channel_helper_property_specs("datum")
        value_properties = self.channel_helper_property_specs("value")
        parameter_variants = self._analyzer.union_variants("Parameter")
        parameter_config_factories = self.parameter_config_factory_specs()
        factory_helpers = (
            SchemaFactorySpec("title", "Title", "Create a chart title object.", "text"),
            SchemaFactorySpec(
                "dynamic_opacity",
                "DynamicOpacity",
                "Create a zoom-dependent opacity definition.",
            ),
            SchemaFactorySpec(
                "data_format",
                "DataFormat",
                "Create a data-format wrapper.",
            ),
            SchemaFactorySpec(
                "view", "ViewBackground", "Create a view background configuration."
            ),
            SchemaFactorySpec(
                "view_config", "ViewConfig", "Create a top-level view config object."
            ),
            SchemaFactorySpec(
                "config",
                "GenomeSpyConfig",
                "Create a top-level GenomeSpy config object.",
                normalize_view_background=True,
            ),
            *self.binding_factory_specs(),
        )
        factory_helper_specs = tuple(
            (
                spec,
                self.schema_property_specs(spec.class_name),
            )
            for spec in factory_helpers
            if self.schema_property_specs(spec.class_name)
        )
        has_locus = any(
            property_spec.name == "chrom" for property_spec in locus_properties
        )
        has_compare = {property_spec.name for property_spec in compare_properties} >= {
            "field",
            "order",
        }
        has_datum = bool(datum_properties)
        has_value = bool(value_properties)
        helper_property_names = {
            property_spec.name
            for property_spec in (*datum_properties, *value_properties)
        }
        used_channel_nested_specs = {
            name: nested
            for name, nested in channel_nested_specs.items()
            if name in helper_property_names
        }
        annotations = [
            *locus_annotations,
            *(p.annotation for specs in locus_nested_specs.values() for p in specs),
            *(
                AnnotationSpec(value_annotation)
                for value_annotation, _ in used_channel_nested_specs.values()
            ),
            *(
                p.annotation
                for _, specs in used_channel_nested_specs.values()
                for p in specs
            ),
            *(p.annotation for p in compare_properties),
            *(p.annotation for p in datum_properties),
            *(p.annotation for p in value_properties),
            *(
                property_spec.annotation
                for variant in parameter_variants
                for property_spec in variant.properties
            ),
            *(
                property_spec.annotation
                for spec in parameter_config_factories
                for property_spec in (
                    *spec.parameter_properties,
                    *spec.config_properties,
                )
            ),
            *(
                p.annotation
                for _, property_specs in factory_helper_specs
                for p in property_specs
            ),
        ]
        aliases = sorted(
            {"FieldName_T"}
            | {
                alias
                for annotation in annotations
                for alias in _annotation_alias_names(annotation.annotation)
            }
        )
        kwds = sorted(
            {
                name
                for annotation in annotations
                for name in _annotation_kwds_names(annotation.annotation)
            }
        )
        needs_literal = any(
            "Literal[" in annotation.annotation for annotation in annotations
        )
        needs_sequence = any(annotation.needs_sequence for annotation in annotations)
        return GeneratedModule(
            source="\n".join(
                [
                    GENERATED_HEADER,
                    "from __future__ import annotations",
                    ("from collections.abc import Sequence" if needs_sequence else ""),
                    "from typing import Any, Self"
                    + (", Literal" if needs_literal else "")
                    + (", overload" if parameter_variants else ""),
                    "",
                    "from typing import TYPE_CHECKING",
                    "",
                    "if TYPE_CHECKING:",
                    "    from genome_spy.channels import DatumChannel, LocusChannel, ValueChannel",
                    *(
                        ["    from genome_spy._parameters import Parameter"]
                        if parameter_variants
                        else []
                    ),
                    *(
                        ["    from genome_spy._expressions import ExpressionOperand"]
                        if parameter_variants
                        else []
                    ),
                    "",
                    "from genome_spy._expressions import DatumExpression",
                    (
                        "from genome_spy.schema._typing import " + ", ".join(aliases)
                        if aliases
                        else ""
                    ),
                    (
                        "from genome_spy.schema._kwds import " + ", ".join(kwds)
                        if kwds
                        else ""
                    ),
                    "from genome_spy.schemapi import Undefined, UndefinedType",
                    "from genome_spy.schema import core",
                    "",
                    _channel_helper_mixin_source(
                        "DatumChannelMethodMixin",
                        "datum",
                        datum_properties,
                        nested_specs=channel_nested_specs,
                    ),
                    _channel_helper_mixin_source(
                        "ValueChannelMethodMixin",
                        "value",
                        value_properties,
                        nested_specs=channel_nested_specs,
                    ),
                    "class LocusChannelMethodMixin:",
                    '    """Schema-derived nested setters for locus channels."""',
                    "",
                    _nested_schema_method_source(
                        method_name="axis",
                        value_annotation="core.GenomeAxis | GenomeAxisKwds | None | object",
                        property_specs=locus_nested_specs["axis"],
                        docstring="Return a locus channel with an axis configuration.",
                        call="self._with_nested('axis', value, **defined)",
                    ),
                    _nested_schema_method_source(
                        method_name="scale",
                        value_annotation="core.Scale | ScaleKwds | None | object",
                        property_specs=locus_nested_specs["scale"],
                        docstring="Return a locus channel with a scale configuration.",
                        call="self._with_nested('scale', value, **defined)",
                    ),
                    *(
                        [
                            _locus_helper_source("locus", locus_property_specs),
                            _locus_helper_source("Locus", locus_property_specs),
                        ]
                        if has_locus
                        else []
                    ),
                    *(
                        [_compare_helper_source(compare_properties)]
                        if has_compare
                        else []
                    ),
                    *([_datum_helper_source(datum_properties)] if has_datum else []),
                    *(
                        [
                            _channel_helper_source(
                                "value", value_properties, "ValueChannel"
                            )
                        ]
                        if has_value
                        else []
                    ),
                    *(
                        [_parameter_helper_source(parameter_variants)]
                        if parameter_variants
                        else []
                    ),
                    *(
                        _parameter_config_helper_source(spec)
                        for spec in parameter_config_factories
                    ),
                    *(
                        _schema_factory_helper_source(
                            spec.helper_name,
                            spec.class_name,
                            property_specs,
                            docstring=spec.docstring,
                            positional_property=spec.positional_property,
                            normalize_view_background=spec.normalize_view_background,
                            fixed_properties=spec.fixed_properties,
                        )
                        for spec, property_specs in factory_helper_specs
                    ),
                    "",
                    "__all__ = "
                    + repr(
                        [
                            *(["Locus", "locus"] if has_locus else []),
                            *(["compare"] if has_compare else []),
                            *(["datum"] if has_datum else []),
                            *(["value"] if has_value else []),
                            *(spec.helper_name for spec, _ in factory_helper_specs),
                            *(["param"] if parameter_variants else []),
                            *(spec.helper_name for spec in parameter_config_factories),
                            "DatumChannelMethodMixin",
                            "LocusChannelMethodMixin",
                            "ValueChannelMethodMixin",
                        ]
                    ),
                    "",
                ]
            ),
            exports=tuple(
                [
                    *(["Locus", "locus"] if has_locus else []),
                    *(["compare"] if has_compare else []),
                    *(["datum"] if has_datum else []),
                    *(["value"] if has_value else []),
                    *(spec.helper_name for spec, _ in factory_helper_specs),
                    *(["param"] if parameter_variants else []),
                    *(spec.helper_name for spec in parameter_config_factories),
                    "DatumChannelMethodMixin",
                    "LocusChannelMethodMixin",
                    "ValueChannelMethodMixin",
                ]
            ),
        )

    def channel_helper_property_specs(
        self, helper_name: str
    ) -> tuple[PropertySpec, ...]:
        """Return all schema properties for channels supporting one helper."""
        encoding_schema = self._definitions_map.get("Encoding", {})
        properties = (
            encoding_schema.get("properties", {})
            if isinstance(encoding_schema, dict)
            else {}
        )
        if not isinstance(properties, dict):
            return ()

        specs_by_name: dict[str, list[PropertySpec]] = {}
        for channel_name, channel_schema in properties.items():
            if not isinstance(channel_name, str) or not isinstance(
                channel_schema, dict
            ):
                continue
            for property_variant in self._analyzer.property_variants(channel_schema):
                if helper_name not in property_variant:
                    continue
                for property_spec in self._analyzer.property_specs_from_properties(
                    property_variant
                ):
                    specs_by_name.setdefault(property_spec.name, []).append(
                        property_spec
                    )

        specs: list[PropertySpec] = []
        for name, values in sorted(specs_by_name.items()):
            unique_annotations = tuple(
                dict.fromkeys(value.annotation.annotation for value in values)
            )
            nested_class_names = {
                value.nested_schema_class_name
                for value in values
                if value.nested_schema_class_name is not None
            }
            specs.append(
                PropertySpec(
                    name=name,
                    annotation=AnnotationSpec(
                        unique_annotations[0]
                        if len(unique_annotations) == 1
                        else "Any",
                        needs_literal=any(
                            value.annotation.needs_literal for value in values
                        ),
                        needs_sequence=any(
                            value.annotation.needs_sequence for value in values
                        ),
                    ),
                    nested_schema_class_name=(
                        next(iter(nested_class_names))
                        if len(nested_class_names) == 1
                        else None
                    ),
                    description=next(
                        (value.description for value in values if value.description),
                        "",
                    ),
                )
            )
        return tuple(specs)

    def _composition_property_specs(
        self,
        class_name: str,
        child_key: str,
        required: tuple[str, ...],
    ) -> tuple[PropertySpec, ...]:
        excluded = {"layer", "hconcat", "vconcat", "concat", "multiscale", child_key}
        excluded.update(required)
        return tuple(
            property_spec
            for property_spec in self.top_level_property_specs(class_name)
            if property_spec.name not in excluded
        )


def _class_name(name: str) -> str:
    parts = re.split(r"[^0-9A-Za-z]+", name)
    class_name = "".join(part[:1].upper() + part[1:] for part in parts if part)
    if not class_name:
        return "GeneratedSchema"
    if class_name[0].isdigit():
        return f"Schema{class_name}"
    return class_name


def _ref_name(schema: dict[str, Any]) -> str | None:
    ref = schema.get("$ref")
    if not isinstance(ref, str):
        return None
    return unquote(ref.split("/")[-1])


def _first_ref_name(schema: dict[str, Any]) -> str | None:
    ref = _ref_name(schema)
    if ref is not None:
        return ref
    for key in ("anyOf", "oneOf", "allOf"):
        variants = schema.get(key, [])
        if not isinstance(variants, list):
            continue
        for variant in variants:
            if isinstance(variant, dict):
                ref = _ref_name(variant)
                if ref is not None:
                    return ref
    return None


def _property_description(schema: Any) -> str:
    """Return a compact Sphinx-safe description from a property schema."""
    if not isinstance(schema, dict):
        return ""
    description = schema.get("description")
    if not isinstance(description, str):
        return ""
    normalized = " ".join(description.split())
    # Keep Markdown link labels, but do not feed Markdown links to docutils.
    normalized = re.sub(r"\[([^\]]+)]\([^)]*\)", r"\1", normalized)
    # JSON Schema descriptions also use Markdown's underscore emphasis.
    normalized = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"\1", normalized)
    # GenomeSpy descriptions use Markdown's single-backtick code notation;
    # generated docstrings are parsed as reStructuredText by Sphinx.
    return re.sub(r"(?<!`)`(?!`)", "``", normalized)


def _method_docstring(
    summary: str,
    property_specs: tuple[PropertySpec, ...],
    *,
    indent: int,
    description: tuple[str, ...] = (),
    extra_args: tuple[str, ...] = (),
    returns: str | None = None,
    raises: tuple[str, ...] = (),
    example: str | None = None,
) -> str:
    """Render a complete Google-style generated method docstring."""
    prefix = " " * indent
    lines = [f'{prefix}"""{summary}']
    if description:
        lines.extend(["", *(f"{prefix}{line}" for line in description)])
    if property_specs or extra_args:
        lines.extend(["", f"{prefix}Args:"])
        lines.extend(
            f"{prefix}    {_docstring_parameter_name(property_spec.python_name)} "
            f"({property_spec.annotation.annotation}): "
            + (
                property_spec.description
                or f"Schema-defined ``{property_spec.name}`` property."
            )
            for property_spec in property_specs
        )
        lines.extend(f"{prefix}    {line}" for line in extra_args)
    if returns is not None:
        lines.extend(["", f"{prefix}Returns:", f"{prefix}    {returns}"])
    if raises:
        lines.extend(["", f"{prefix}Raises:"])
        lines.extend(f"{prefix}    {line}" for line in raises)
    if example is not None:
        lines.extend(["", f"{prefix}Example:", f"{prefix}    >>> {example}"])
    lines.append(f'{prefix}"""')
    return "\n".join(lines)


def _docstring_parameter_name(name: str) -> str:
    """Escape a Python keyword suffix for reStructuredText field parsing."""
    return f"{name[:-1]}\\\\_" if name.endswith("_") else name


def _nested_setter_ref_name(schema: dict[str, Any]) -> str | None:
    """Return a nested-setter ref when the schema is object/null only."""
    ref = _ref_name(schema)
    if ref is not None:
        return ref

    refs: list[str] = []
    saw_other_non_null = False
    for key in ("anyOf", "oneOf"):
        variants = schema.get(key)
        if not isinstance(variants, list):
            continue
        for variant in variants:
            if not isinstance(variant, dict):
                saw_other_non_null = True
                continue
            ref = _ref_name(variant)
            if ref is not None:
                refs.append(ref)
                continue
            if variant.get("type") == "null":
                continue
            saw_other_non_null = True
        break

    if saw_other_non_null or len(set(refs)) != 1:
        return None
    return refs[0]


def _looks_like_object_schema(schema: dict[str, Any]) -> bool:
    """Return whether a referenced definition behaves like an object wrapper."""
    if schema.get("type") == "object":
        return True
    for key in ("properties", "required", "additionalProperties"):
        if key in schema:
            return True
    return False


def _schema_class_source(
    class_name: str,
    definition: SchemaDefinition,
    *,
    analyzer: SchemaAnalyzer,
) -> GeneratedSchemaClass:
    property_specs = analyzer.property_specs(definition)
    args = ", ".join(
        f"{property_spec.python_name}: {property_spec.annotation.annotation} | UndefinedType = Undefined"
        for property_spec in property_specs
    )
    if args:
        args = ", " + args

    regular_assignments = ", ".join(
        f"{property_spec.name}={property_spec.python_name}"
        for property_spec in property_specs
        if not keyword.iskeyword(property_spec.name)
    )
    keyword_assignments = ", ".join(
        f"{property_spec.name!r}: {property_spec.python_name}"
        for property_spec in property_specs
        if keyword.iskeyword(property_spec.name)
    )
    call_arguments = regular_assignments
    if keyword_assignments:
        keyword_mapping = f"**{{{keyword_assignments}}}"
        call_arguments = (
            f"{call_arguments}, {keyword_mapping}"
            if call_arguments
            else keyword_mapping
        )
    body = (
        f"super().__init__({call_arguments})"
        if call_arguments
        else "super().__init__()"
    )
    methods = "".join(
        _schema_property_method_source(
            class_name,
            property_spec.name,
            annotation=property_spec.annotation.annotation,
            nested_schema_class_name=property_spec.nested_schema_class_name,
            nested_property_specs=_nested_property_specs(
                analyzer, property_spec.nested_schema_class_name
            ),
        )
        for property_spec in property_specs
    )

    return GeneratedSchemaClass(
        source=(
            f"class {class_name}(GenomeSpySchema):\n"
            f'    """Generated wrapper for ``{definition.name}``."""\n\n'
            f'    _schema = _ROOT_SCHEMA.get("definitions", {{}}).get({definition.name!r}, {{}})\n\n'
            f"    def __init__(self{args}, **kwds: Any) -> None:\n"
            f"        {body}\n"
            f"        if kwds:\n"
            f"            self._kwds.update(kwds)\n"
            f"{methods}"
        ),
        needs_literal=any(
            property_spec.annotation.needs_literal for property_spec in property_specs
        ),
        needs_sequence=any(
            property_spec.annotation.needs_sequence for property_spec in property_specs
        ),
        used_aliases=tuple(
            sorted(
                {
                    alias_name
                    for property_spec in property_specs
                    for alias_name in _annotation_alias_names(
                        property_spec.annotation.annotation
                    )
                }
            )
        ),
        used_kwds=tuple(
            sorted(
                {
                    kwds_name
                    for property_spec in property_specs
                    for kwds_name in _annotation_kwds_names(
                        property_spec.annotation.annotation
                    )
                }
            )
        ),
    )


def _dedupe_preserve_order(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _type_alias_name(name: str) -> str:
    return f"{_class_name(name)}_T"


def _kwds_type_name(name: str) -> str:
    return f"{_class_name(name)}Kwds"


def _annotation_alias_names(annotation: str) -> tuple[str, ...]:
    return tuple(sorted(set(re.findall(r"\b[A-Za-z][A-Za-z0-9]*_T\b", annotation))))


def _annotation_kwds_names(annotation: str) -> tuple[str, ...]:
    return tuple(sorted(set(re.findall(r"\b[A-Za-z][A-Za-z0-9]*Kwds\b", annotation))))


def _annotation_class_names(annotation: str) -> tuple[str, ...]:
    return tuple(
        sorted(
            set(re.findall(r"\b[A-Z][A-Za-z0-9]*\b", annotation))
            - {"Any", "Literal", "None", "Sequence", "TypedDict", "UndefinedType"}
        )
    )


def _annotation_mentions_any(annotation: str) -> bool:
    return bool(re.search(r"\bAny\b", annotation))


def _sort_alias_specs(
    aliases: list[tuple[str, AnnotationSpec]],
) -> list[tuple[str, AnnotationSpec]]:
    remaining = {name: spec for name, spec in aliases}
    ordered: list[tuple[str, AnnotationSpec]] = []

    while remaining:
        progressed = False
        remaining_names = set(remaining)
        for name in sorted(remaining):
            spec = remaining[name]
            dependencies = (
                set(_annotation_alias_names(spec.annotation)) & remaining_names
            )
            dependencies.discard(name)
            if dependencies:
                continue
            ordered.append((name, spec))
            del remaining[name]
            progressed = True
            break
        if not progressed:
            for name in sorted(remaining):
                ordered.append((name, remaining[name]))
            break

    return ordered


def _is_literal_value(value: Any) -> bool:
    return isinstance(value, str | bool | int | float) or value is None


def _mark_method_source(
    mark_type: str,
    *,
    method_name: str | None = None,
    property_specs: tuple[PropertySpec, ...],
) -> str:
    method_name = method_name or mark_type.replace("-", "_")
    parameters = "\n".join(
        f"        {property_spec.python_name}: "
        f"{_qualified_transform_annotation(property_spec.annotation.annotation)} "
        "| UndefinedType = Undefined,"
        for property_spec in property_specs
    )
    if parameters:
        parameters = f",\n        *,\n{parameters}\n"
    else:
        parameters = ""
    property_values = "\n".join(
        f"            {property_spec.name!r}: {property_spec.python_name},"
        for property_spec in property_specs
    )
    if property_values:
        body = (
            "        properties = {\n"
            f"{property_values}\n"
            "        }\n"
            "        defined = {key: value for key, value in properties.items() "
            "if value is not Undefined}\n"
            f"        return self._with_mark({mark_type!r}, **defined)  "
            "# type: ignore[attr-defined, no-any-return]"
        )
    else:
        body = (
            f"        return self._with_mark({mark_type!r})  "
            "# type: ignore[attr-defined, no-any-return]"
        )
    return (
        f"    def mark_{method_name}(self{parameters}) -> Self:\n"
        + _method_docstring(
            f"Set the chart mark to ``{mark_type}``.", property_specs, indent=8
        )
        + "\n"
        f"{body}"
    )


def _lazy_data_method_source(spec: LazyDataMethodSpec) -> str:
    """Render one concrete lazy data-source convenience method."""
    parameters = "\n".join(
        f"        {property_spec.python_name}: "
        f"{_qualified_transform_annotation(property_spec.annotation.annotation)} "
        "| UndefinedType = Undefined,"
        for property_spec in spec.properties
    )
    values = "\n".join(
        f"            {property_spec.name!r}: {property_spec.python_name},"
        for property_spec in spec.properties
    )
    return "\n".join(
        [
            f"    def {spec.method_name}(",
            "        self,",
            f"        url: {_qualified_transform_annotation(spec.url_annotation.annotation)},",
            "        /,",
            *(["        *,", parameters] if parameters else []),
            "    ) -> core.Data:",
            _method_docstring(
                f"Create a lazy ``{spec.source_type}`` data source.",
                spec.properties,
                indent=8,
            ),
            "        properties = {",
            values,
            "        }",
            "        defined: dict[str, Any] = {",
            "            key: value for key, value in properties.items() if value is not Undefined",
            "        }",
            "        return core.Data(",
            "            lazy=core.LazyDataParams(",
            f"                type=cast(Any, {spec.source_type!r}), url=url, **defined",
            "            )",
            "        )",
            "",
        ]
    )


def _locus_helper_source(name: str, property_specs: tuple[PropertySpec, ...]) -> str:
    """Render a schema-derived chromosomal locus helper."""
    parameters = "\n".join(
        f"    {property_spec.python_name}: "
        f"{_qualified_transform_annotation(property_spec.annotation.annotation)} "
        "| UndefinedType = Undefined,"
        for property_spec in property_specs
    )
    values = "\n".join(
        f"        {property_spec.name!r}: {property_spec.python_name},"
        for property_spec in property_specs
    )
    return "\n".join(
        [
            f"def {name}(",
            "    chrom: FieldName_T,",
            "    pos: FieldName_T | None = None,",
            "    /,",
            "    *,",
            parameters,
            ") -> LocusChannel:",
            _method_docstring(
                "Create a GenomeSpy chromosomal locus channel definition.",
                property_specs,
                indent=4,
            ),
            "    properties = {",
            values,
            "    }",
            "    defined: dict[str, Any] = {",
            "        key: value for key, value in properties.items() if value is not Undefined",
            "    }",
            "    definition: dict[str, Any] = {'chrom': chrom, 'type': 'locus', **defined}",
            "    if pos is not None:",
            "        definition['pos'] = pos",
            "    from genome_spy.channels import LocusChannel",
            "",
            "    return LocusChannel(definition)",
            "",
        ]
    )


def _compare_helper_source(property_specs: tuple[PropertySpec, ...]) -> str:
    """Render the schema-derived ``compare`` helper."""
    properties = {property_spec.name: property_spec for property_spec in property_specs}
    field = properties.get("field")
    order = properties.get("order")
    if field is None or order is None:
        raise ValueError("CompareParams must define field and order properties.")
    return "\n".join(
        [
            "def compare(",
            f"    field: {_qualified_transform_annotation(field.annotation.annotation)} | None = None,",
            "    *,",
            f"    order: {_qualified_transform_annotation(order.annotation.annotation)} | None = None,",
            ") -> core.CompareParams:",
            _method_docstring(
                "Create a sort/compare definition.", property_specs, indent=4
            ),
            "    properties = {'field': field, 'order': order}",
            "    defined: dict[str, Any] = {",
            "        key: value for key, value in properties.items() if value is not None",
            "    }",
            "    return core.CompareParams(**defined)",
            "",
        ]
    )


def _channel_helper_source(
    helper_name: str,
    property_specs: tuple[PropertySpec, ...],
    channel_class_name: str,
) -> str:
    """Render a generic channel helper with schema-derived options."""
    main_property = next(
        property_spec
        for property_spec in property_specs
        if property_spec.name == helper_name
    )
    options = tuple(
        property_spec
        for property_spec in property_specs
        if property_spec.name != helper_name
    )
    parameters = "\n".join(
        f"    {property_spec.python_name}: "
        f"{_qualified_transform_annotation(property_spec.annotation.annotation)} "
        "| UndefinedType = Undefined,"
        for property_spec in options
    )
    values = "\n".join(
        f"        {property_spec.name!r}: {property_spec.python_name},"
        for property_spec in options
    )
    return "\n".join(
        [
            f"def {helper_name}(",
            f"    {helper_name}: {_qualified_transform_annotation(main_property.annotation.annotation)},",
            "    /,",
            "    *,",
            parameters,
            f") -> {channel_class_name}:",
            _method_docstring(
                f"Create a constant-{helper_name} encoding channel.",
                property_specs,
                indent=4,
            ),
            "    properties = {",
            f"        {helper_name!r}: {helper_name},",
            values,
            "    }",
            "    defined = {key: value for key, value in properties.items() if value is not Undefined}",
            f"    from genome_spy.channels import {channel_class_name}",
            "",
            f"    return {channel_class_name}(defined)",
            "",
        ]
    )


def _datum_helper_source(property_specs: tuple[PropertySpec, ...]) -> str:
    """Render the callable expression-aware ``datum`` namespace."""
    main_property = next(
        property_spec
        for property_spec in property_specs
        if property_spec.name == "datum"
    )
    options = tuple(
        property_spec
        for property_spec in property_specs
        if property_spec.name != "datum"
    )
    parameters = "\n".join(
        f"        {property_spec.python_name}: "
        f"{_qualified_transform_annotation(property_spec.annotation.annotation)} "
        "| UndefinedType = Undefined,"
        for property_spec in options
    )
    values = "\n".join(
        f"            {property_spec.name!r}: {property_spec.python_name},"
        for property_spec in options
    )
    return "\n".join(
        [
            "class DatumType(DatumExpression):",
            '    """Build datum expressions or constant-datum channels."""',
            "",
            "    def __call__(",
            "        self,",
            "        datum: "
            + _qualified_transform_annotation(main_property.annotation.annotation)
            + ",",
            "        /,",
            "        *,",
            parameters,
            "    ) -> DatumChannel:",
            _method_docstring(
                "Create a constant-datum encoding channel.",
                property_specs,
                indent=8,
            ),
            "        properties = {",
            "            'datum': datum,",
            values,
            "        }",
            "        defined = {",
            "            key: value",
            "            for key, value in properties.items()",
            "            if value is not Undefined",
            "        }",
            "        from genome_spy.channels import DatumChannel",
            "",
            "        return DatumChannel(defined)",
            "",
            "",
            "datum = DatumType()",
            "",
        ]
    )


def _channel_helper_mixin_source(
    class_name: str,
    helper_name: str,
    property_specs: tuple[PropertySpec, ...],
    *,
    nested_specs: dict[str, tuple[str, tuple[PropertySpec, ...]]],
) -> str:
    """Render fluent methods available on one constant-channel branch."""
    methods: list[str] = []
    for property_spec in property_specs:
        if property_spec.name == helper_name:
            continue
        nested = nested_specs.get(property_spec.name)
        if nested is not None:
            value_annotation, nested_property_specs = nested
            methods.append(
                _nested_schema_method_source(
                    method_name=property_spec.python_name,
                    value_annotation=value_annotation,
                    property_specs=nested_property_specs,
                    docstring=(
                        f"Return a channel with a {property_spec.name} configuration."
                    ),
                    call=(
                        f"self._with_nested({property_spec.name!r}, value, **defined)"
                    ),
                )
            )
            continue
        methods.append(
            "\n".join(
                [
                    f"    def {property_spec.python_name}(",
                    "        self,",
                    "        value: "
                    f"{_qualified_transform_annotation(property_spec.annotation.annotation)},",
                    "    ) -> Self:",
                    f'        """Return a channel with ``{property_spec.name}`` updated."""',
                    f"        return self._with_property({property_spec.name!r}, value)  # type: ignore[attr-defined, no-any-return]",
                ]
            )
        )
    return "\n".join(
        [
            f"class {class_name}:",
            f'    """Schema-derived methods for ``{helper_name}`` channels."""',
            "",
            *(methods or ["    pass"]),
            "",
        ]
    )


def _schema_factory_helper_source(
    helper_name: str,
    class_name: str,
    property_specs: tuple[PropertySpec, ...],
    *,
    docstring: str,
    positional_property: str | None,
    normalize_view_background: bool,
    fixed_properties: tuple[tuple[str, Any], ...] = (),
) -> str:
    """Render a schema-object factory with explicit generated properties."""
    fixed_names = {name for name, _ in fixed_properties}
    positional_spec = next(
        (
            property_spec
            for property_spec in property_specs
            if property_spec.name == positional_property
        ),
        None,
    )
    options = tuple(
        property_spec
        for property_spec in property_specs
        if property_spec is not positional_spec
        and property_spec.name not in fixed_names
    )
    parameters = "\n".join(
        f"    {property_spec.python_name}: "
        f"{_qualified_transform_annotation(property_spec.annotation.annotation)} "
        "| UndefinedType = Undefined,"
        for property_spec in options
    )
    values = "\n".join(
        f"        {property_spec.name!r}: {property_spec.python_name},"
        for property_spec in options
    )
    positional_parameter = (
        f"    {positional_spec.python_name}: "
        f"{_qualified_transform_annotation(positional_spec.annotation.annotation)},"
        if positional_spec is not None
        else ""
    )
    positional_value = (
        f"        {positional_spec.name!r}: {positional_spec.python_name},"
        if positional_spec is not None
        else ""
    )
    documented_properties = (
        *((positional_spec,) if positional_spec is not None else ()),
        *options,
    )
    signature = [f"def {helper_name}("]
    if positional_parameter:
        signature.extend([positional_parameter, "    /,"])
    signature.extend(["    *,", parameters, f") -> core.{class_name}:"])
    normalization = (
        [
            "    if isinstance(defined.get('view'), core.ViewBackground):",
            "        defined['view'] = core.ViewConfig(**defined['view'].to_dict(validate=False))",
        ]
        if normalize_view_background
        else []
    )
    return "\n".join(
        [
            *signature,
            _method_docstring(docstring, documented_properties, indent=4),
            "    properties = {",
            *(f"        {name!r}: {value!r}," for name, value in fixed_properties),
            *([positional_value] if positional_value else []),
            *([values] if values else []),
            "    }",
            "    defined: dict[str, Any] = {",
            "        key: value for key, value in properties.items() if value is not Undefined",
            "    }",
            *normalization,
            f"    return core.{class_name}(**defined)",
            "",
            "",
        ]
    )


def _parameter_helper_source(variants: tuple[UnionVariantSpec, ...]) -> str:
    """Render a branch-preserving parameter factory from concrete union leaves."""

    def annotation_for(property_spec: PropertySpec) -> str:
        annotation = _qualified_transform_annotation(
            property_spec.annotation.annotation
        )
        if property_spec.name == "expr" and "ExpressionOperand" not in annotation:
            return f"{annotation} | ExpressionOperand"
        return annotation

    overloads: list[str] = []
    property_specs_by_name: dict[str, list[PropertySpec]] = {}
    for variant in variants:
        for property_spec in variant.properties:
            property_specs_by_name.setdefault(property_spec.name, []).append(
                property_spec
            )

        properties = {
            property_spec.name: property_spec for property_spec in variant.properties
        }
        keyword_specs = [
            properties[name]
            for name in sorted(variant.required - {"name"})
            if name in properties
        ]
        keyword_specs.extend(
            property_spec
            for property_spec in variant.properties
            if property_spec.name not in variant.required
            and property_spec.name != "name"
        )
        parameters = []
        for property_spec in keyword_specs:
            annotation = annotation_for(property_spec)
            default = (
                ""
                if property_spec.name in variant.required
                else " | UndefinedType = Undefined"
            )
            parameters.append(
                f"    {property_spec.python_name}: {annotation}{default},"
            )
        parameters.append("    empty: bool = True,")
        overloads.append(
            "\n".join(
                [
                    "@overload",
                    "def param(",
                    "    name: str | None = None,",
                    "    /,",
                    "    *,",
                    *parameters,
                    ") -> Parameter: ...",
                ]
            )
        )

    merged_specs: list[PropertySpec] = []
    for name, specs in sorted(property_specs_by_name.items()):
        if name == "name":
            continue
        annotations = _dedupe_preserve_order(
            spec.annotation.annotation for spec in specs
        )
        annotation = "Any" if "Any" in annotations else " | ".join(annotations)
        merged_specs.append(
            PropertySpec(
                name=name,
                annotation=AnnotationSpec(annotation),
                description=next(
                    (spec.description for spec in specs if spec.description), ""
                ),
            )
        )

    implementation_parameters = [
        "    name: str | None = None,",
        "    /,",
        "    *,",
        *(
            f"    {spec.python_name}: {annotation_for(spec)} "
            "| UndefinedType = Undefined,"
            for spec in merged_specs
        ),
        "    empty: bool = True,",
    ]
    forwarded = ", ".join(
        f"{spec.python_name}={spec.python_name}" for spec in merged_specs
    )
    if forwarded:
        forwarded += ", "
    variant_names = tuple(
        variant.schema_name for variant in variants if variant.schema_name is not None
    )
    selection_variant_names = tuple(
        variant.schema_name
        for variant in variants
        if variant.schema_name is not None and "select" in variant.required
    )
    variant_classes = _core_class_tuple_source(variant_names)
    selection_variant_classes = _core_class_tuple_source(selection_variant_names)
    return "\n\n".join(
        [
            "\n\n".join(overloads),
            "\n".join(
                [
                    "def param(",
                    *implementation_parameters,
                    ") -> Parameter:",
                    '    """Create a reusable GenomeSpy parameter handle.',
                    "",
                    "    The overloads and accepted properties are generated from the",
                    "    concrete leaves of GenomeSpy's ``Parameter`` union.",
                    "",
                    "    Args:",
                    "        name: Parameter name. A stable name is generated when omitted.",
                    *(
                        f"        {spec.python_name}: {spec.description or 'Schema-defined parameter property.'}"
                        for spec in merged_specs
                    ),
                    "        empty: Whether an empty selection matches as a predicate.",
                    "",
                    "    Returns:",
                    "        A reusable parameter handle.",
                    "",
                    "    Raises:",
                    "        TypeError: If the arguments match no unique parameter branch.",
                    "",
                    "    Example:",
                    '        >>> param("cutoff", value=0.5).param.to_dict()',
                    "        {'name': 'cutoff', 'value': 0.5}",
                    '    """',
                    "    from genome_spy._parameters import _make_parameter",
                    "",
                    "    return _make_parameter(",
                    "        name,",
                    f"        {forwarded}",
                    f"        _variants={variant_classes},",
                    f"        _selection_variants={selection_variant_classes},",
                    "        empty=empty,",
                    "    )",
                ]
            ),
        ]
    )


def _core_class_tuple_source(class_names: tuple[str, ...]) -> str:
    """Render a tuple of generated ``core`` schema classes."""
    if not class_names:
        return "()"
    return "(" + ", ".join(f"core.{name}" for name in class_names) + ",)"


def _parameter_config_helper_source(spec: ParameterConfigFactorySpec) -> str:
    """Render a parameter helper around one generated nested config class."""
    fixed_names = {name for name, _ in spec.fixed_properties}
    config_properties = tuple(
        prop for prop in spec.config_properties if prop.name not in fixed_names
    )
    parameter_names = {prop.name for prop in spec.parameter_properties}
    collisions = parameter_names & {prop.name for prop in config_properties}
    if collisions:
        names = ", ".join(sorted(collisions))
        raise ValueError(
            f"Generated parameter helper {spec.helper_name!r} has ambiguous "
            f"configuration properties: {names}."
        )
    parameters = [
        "    name: str | None = None,",
        "    /,",
        "    *,",
        *(
            f"    {prop.python_name}: "
            f"{_qualified_transform_annotation(prop.annotation.annotation)} "
            "| UndefinedType = Undefined,"
            for prop in (*config_properties, *spec.parameter_properties)
        ),
        *(["    empty: bool = True,"] if spec.supports_empty else []),
    ]
    config_arguments = ", ".join(
        [
            *(
                f"{_python_property_name(name)}={value!r}"
                for name, value in spec.fixed_properties
            ),
            *(f"{prop.python_name}={prop.python_name}" for prop in config_properties),
        ]
    )
    parameter_arguments = ", ".join(
        f"{prop.python_name}={prop.python_name}" for prop in spec.parameter_properties
    )
    if parameter_arguments:
        parameter_arguments = ", " + parameter_arguments
    empty_argument = ", empty=empty" if spec.supports_empty else ""
    selection_variants = (
        f"(core.{spec.parameter_class_name},)" if spec.supports_empty else "()"
    )
    return "\n".join(
        [
            f"def {spec.helper_name}(",
            *parameters,
            ") -> Parameter:",
            f'    """Create a GenomeSpy ``{spec.helper_name}`` parameter.',
            "",
            "    Args:",
            "        name: Parameter name. A stable name is generated when omitted.",
            *(
                f"        {prop.python_name}: {prop.description or 'Schema-defined configuration property.'}"
                for prop in (*config_properties, *spec.parameter_properties)
            ),
            *(
                ["        empty: Whether an empty selection matches as a predicate."]
                if spec.supports_empty
                else []
            ),
            "",
            "    Returns:",
            "        A reusable parameter handle.",
            "",
            "    Raises:",
            "        TypeError: If the generated parameter definition is invalid.",
            "",
            "    Example:",
            f"        >>> {spec.helper_name}().param.to_dict(validate=False)",
            "        {...}",
            '    """',
            f"    config = core.{spec.config_class_name}({config_arguments})",
            "    from genome_spy._parameters import _make_parameter",
            "",
            "    return _make_parameter(",
            "        name,",
            f"        {spec.config_property}=config{parameter_arguments}{empty_argument},",
            f"        _variants=(core.{spec.parameter_class_name},),",
            f"        _selection_variants={selection_variants},",
            "    )",
            "",
            "",
        ]
    )


def _encoding_method_source(property_specs: tuple[PropertySpec, ...]) -> str:
    """Render the schema-derived fluent ``encode`` method."""
    parameters = "\n".join(
        f"        {property_spec.python_name}: "
        "Channel | SchemaBase | str | dict[str, Any] | "
        "Sequence[Channel | SchemaBase | str | dict[str, Any]] | None | "
        "UndefinedType = Undefined,"
        for property_spec in property_specs
    )
    property_values = "\n".join(
        f"            {property_spec.name!r}: {property_spec.python_name},"
        for property_spec in property_specs
    )
    return "\n".join(
        [
            "    def encode(",
            "        self,",
            "        *args: Channel,",
            parameters,
            "    ) -> Self:",
            _method_docstring(
                "Return a new specification with merged channel encodings.",
                property_specs,
                indent=8,
            ),
            "        properties = {",
            property_values,
            "        }",
            "        defined = {",
            "            key: value for key, value in properties.items() if value is not Undefined",
            "        }",
            "        return self._encode(args, defined)  # type: ignore[attr-defined, no-any-return]",
        ]
    )


def _properties_mixin_source(
    class_name: str,
    property_specs: tuple[PropertySpec, ...],
    *,
    positional_properties: tuple[str, ...],
) -> str:
    """Render a concrete top-level property builder."""
    specs_by_name = {spec.name: spec for spec in property_specs}
    positional_specs = tuple(
        specs_by_name[name] for name in positional_properties if name in specs_by_name
    )
    keyword_specs = tuple(
        spec for spec in property_specs if spec.name not in positional_properties
    )
    positional_parameters = "\n".join(
        f"        {spec.python_name}: {_qualified_transform_annotation(spec.annotation.annotation)} | UndefinedType = Undefined,"
        for spec in positional_specs
    )
    keyword_parameters = "\n".join(
        f"        {spec.python_name}: {_qualified_transform_annotation(spec.annotation.annotation)} | UndefinedType = Undefined,"
        for spec in keyword_specs
    )
    parameters = "\n".join(
        f"        {spec.python_name}: {_qualified_transform_annotation(spec.annotation.annotation)} | UndefinedType = Undefined,"
        for spec in property_specs
    )
    values = "\n".join(
        f"            {spec.name!r}: {spec.python_name}," for spec in property_specs
    )
    constructor_docs = (
        *property_specs,
        PropertySpec(
            "schema_url",
            AnnotationSpec("str | None"),
            description="Root JSON Schema URL. Uses the packaged default when omitted.",
        ),
    )
    return "\n".join(
        [
            f"class {class_name}:",
            '    """Schema-derived top-level property builder."""',
            "",
            "    def __init__(",
            "        self,",
            positional_parameters,
            "        *,",
            keyword_parameters,
            "        schema_url: str | None = None,",
            "    ) -> None:",
            _method_docstring(
                "Initialize a schema-derived top-level specification.",
                constructor_docs,
                indent=8,
            ),
            "        properties = {",
            values,
            "        }",
            "        defined = {key: value for key, value in properties.items() if value is not Undefined}",
            "        self._initialize_spec(properties=defined, schema_url=schema_url)  # type: ignore[attr-defined]",
            "",
            "    def properties(",
            "        self,",
            "        *,",
            parameters,
            "    ) -> Self:",
            _method_docstring(
                "Return a new specification with updated top-level properties.",
                property_specs,
                indent=8,
            ),
            "        properties = {",
            values,
            "        }",
            "        defined = {key: value for key, value in properties.items() if value is not Undefined}",
            "        return self._with_properties(defined)  # type: ignore[attr-defined, no-any-return]",
            "",
            _copy_method_source(property_specs),
        ]
    )


def _imported_view_constructor_mixin_source(
    property_specs: tuple[PropertySpec, ...],
) -> str:
    """Render the exact constructor signature for imported child views."""
    specs_by_name = {spec.name: spec for spec in property_specs}
    import_spec = specs_by_name.get("import")
    options = tuple(spec for spec in property_specs if spec is not import_spec)
    positional_parameter = (
        "        import_: "
        f"{_qualified_transform_annotation(import_spec.annotation.annotation)} "
        "| UndefinedType = Undefined,"
        if import_spec is not None
        else ""
    )
    parameters = "\n".join(
        f"        {spec.python_name}: {_qualified_transform_annotation(spec.annotation.annotation)} | UndefinedType = Undefined,"
        for spec in options
    )
    values = "\n".join(
        f"            {spec.name!r}: {spec.python_name}," for spec in property_specs
    )
    return "\n".join(
        [
            "class ImportedViewConstructorMixin:",
            '    """Schema-derived constructor for imported child views."""',
            "",
            "    def __init__(",
            "        self,",
            positional_parameter,
            "        *,",
            parameters,
            "    ) -> None:",
            _method_docstring(
                "Initialize an imported child view.", property_specs, indent=8
            ),
            "        properties = {",
            values,
            "        }",
            "        defined = {key: value for key, value in properties.items() if value is not Undefined}",
            "        self._initialize_import(properties=defined)  # type: ignore[attr-defined]",
        ]
    )


def _copy_method_source(property_specs: tuple[PropertySpec, ...]) -> str:
    """Render an explicit top-level copy method for one spec family."""
    parameters = "\n".join(
        f"        {spec.python_name}: {_qualified_transform_annotation(spec.annotation.annotation)} | UndefinedType = Undefined,"
        for spec in property_specs
    )
    values = "\n".join(
        f"            {spec.name!r}: {spec.python_name}," for spec in property_specs
    )
    return "\n".join(
        [
            "    def copy(",
            "        self,",
            "        *,",
            "        deep: bool = True,",
            parameters,
            "    ) -> Self:",
            _method_docstring(
                "Return a copy with updated top-level properties.",
                property_specs,
                indent=8,
            ),
            "        properties = {",
            values,
            "        }",
            "        defined = {key: value for key, value in properties.items() if value is not Undefined}",
            "        return self._copy_with_properties(deep=deep, properties=defined)  # type: ignore[attr-defined, no-any-return]",
        ]
    )


def _top_level_merge_method_source(
    property_spec: PropertySpec, property_specs: tuple[PropertySpec, ...]
) -> str:
    """Render a merging setter for one top-level mapping property."""
    class_name = property_spec.nested_schema_class_name
    value_annotation = (
        f"core.{class_name} | {property_spec.annotation.annotation.removeprefix(f'{class_name} | ')} | None | object"
        if class_name is not None
        else f"{property_spec.annotation.annotation} | None | object"
    )
    return _nested_schema_method_source(
        method_name=f"with_{property_spec.name}",
        value_annotation=value_annotation,
        property_specs=property_specs,
        docstring=(f"Return a copy with merged top-level ``{property_spec.name}``."),
        call=f"self._merge_top_level({property_spec.name!r}, value, defined)",
    )


def _composition_function_source(
    name: str,
    *,
    child_key: str,
    return_class: str,
    property_specs: tuple[PropertySpec, ...],
    required_specs: tuple[PropertySpec, ...],
) -> str:
    """Render a concrete public composition helper."""
    required_parameters = "\n".join(
        f"    {property_spec.python_name}: "
        f"{_qualified_transform_annotation(property_spec.annotation.annotation)},"
        for property_spec in required_specs
    )
    optional_parameters = "\n".join(
        f"    {property_spec.python_name}: "
        f"{_qualified_transform_annotation(property_spec.annotation.annotation)} "
        "| UndefinedType = Undefined,"
        for property_spec in property_specs
    )
    values = "\n".join(
        f"        {property_spec.name!r}: {property_spec.python_name},"
        for property_spec in (*required_specs, *property_specs)
    )
    return "\n".join(
        [
            f"def {name}(",
            "    *charts: TopLevelSpec | ImportedView,",
            required_parameters,
            optional_parameters,
            f") -> {return_class}:",
            _method_docstring(
                f"Return a {name} composition of the given charts.",
                (*required_specs, *property_specs),
                indent=4,
            ),
            "    properties = {",
            values,
            "    }",
            "    defined: dict[str, Any] = {",
            "        key: value for key, value in properties.items() if value is not Undefined",
            "    }",
            f"    from genome_spy.chart import {return_class}",
            "",
            f"    return {return_class}({child_key}=cast(Any, list(charts)), **defined)",
            "",
        ]
    )


def _import_view_function_source(property_specs: tuple[PropertySpec, ...]) -> str:
    """Render the public imported-view helper."""
    parameters = "\n".join(
        f"    {property_spec.python_name}: "
        f"{_qualified_transform_annotation(property_spec.annotation.annotation)} "
        "| UndefinedType = Undefined,"
        for property_spec in property_specs
    )
    values = "\n".join(
        f"        {property_spec.name!r}: {property_spec.python_name},"
        for property_spec in property_specs
    )
    return "\n".join(
        [
            "def import_view(",
            "    *,",
            "    url: str | UndefinedType = Undefined,",
            "    template: str | UndefinedType = Undefined,",
            parameters,
            ") -> ImportedView:",
            '    """Create an imported child view from a URL or template."""',
            "    if (url is Undefined) == (template is Undefined):",
            '        raise ValueError("Specify exactly one of url or template.")',
            "    properties = {",
            values,
            "    }",
            "    defined: dict[str, Any] = {",
            "        key: value for key, value in properties.items() if value is not Undefined",
            "    }",
            "    import_definition = {'url': url} if url is not Undefined else {'template': template}",
            "    from genome_spy.chart import ImportedView",
            "",
            "    return ImportedView(import_=import_definition, **defined)",
            "",
        ]
    )


def _resolution_method_source(
    channel: str, property_specs: tuple[PropertySpec, ...]
) -> str:
    """Render one composition resolution method."""
    parameters = "\n".join(
        f"        {property_spec.python_name}: "
        f"{property_spec.annotation.annotation} | UndefinedType = Undefined,"
        for property_spec in property_specs
    )
    values = "\n".join(
        f"            {property_spec.name!r}: {property_spec.python_name},"
        for property_spec in property_specs
    )
    return "\n".join(
        [
            f"    def resolve_{channel}(",
            "        self,",
            "        *,",
            parameters,
            "    ) -> Self:",
            f'        """Return a copy with merged {channel} resolutions."""',
            "        properties = {",
            values,
            "        }",
            "        defined = {",
            "            key: value for key, value in properties.items() if value is not Undefined",
            "        }",
            f"        return self._with_resolution({channel!r}, defined)  # type: ignore[attr-defined, no-any-return]",
        ]
    )


def _snake_name(name: str) -> str:
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def _python_property_name(name: str) -> str:
    """Return a Python-safe spelling for a schema property."""
    return f"{name}_" if keyword.iskeyword(name) else name


def _qualified_transform_annotation(annotation: str) -> str:
    """Qualify generated schema classes used by transform annotations."""
    excluded = {
        "Any",
        "False",
        "Literal",
        "None",
        "Sequence",
        "True",
        "UndefinedType",
    }

    def qualify(match: re.Match[str]) -> str:
        name = match.group(0)
        if name in excluded or name.endswith(("_T", "Kwds")):
            return name
        return f"core.{name}"

    return re.sub(r"\b[A-Z][A-Za-z0-9]*\b", qualify, annotation)


def _transform_method_source(spec: TransformMethodSpec) -> str:
    aliases = dict(spec.property_aliases)
    properties_by_name = {
        property_spec.name: property_spec for property_spec in spec.properties
    }
    missing_positionals = set(spec.positional_properties) - properties_by_name.keys()
    if missing_positionals:
        names = ", ".join(sorted(missing_positionals))
        raise ValueError(
            f"Generated method {spec.method_name!r} refers to missing positional "
            f"properties: {names}."
        )

    positional_properties = [
        properties_by_name[name] for name in spec.positional_properties
    ]
    remaining_properties = sorted(
        (
            property_spec
            for property_spec in spec.properties
            if property_spec.name not in spec.positional_properties
        ),
        key=lambda property_spec: (
            property_spec.name not in spec.required,
            property_spec.name,
        ),
    )
    ordered_properties = [*positional_properties, *remaining_properties]

    def parameter_name(property_spec: PropertySpec) -> str:
        return _python_property_name(
            aliases.get(property_spec.name, property_spec.name)
        )

    def parameter_source(property_spec: PropertySpec) -> str:
        annotation = _qualified_transform_annotation(
            property_spec.annotation.annotation
        )
        if property_spec.name == "expr":
            annotation = f"{annotation} | ExpressionOperand"
        name = parameter_name(property_spec)
        if property_spec.name in spec.required:
            return f"        {name}: {annotation},"
        return f"        {name}: {annotation} | UndefinedType = Undefined,"

    parameters: list[str] = []
    assignments: list[str] = []
    for property_spec in ordered_properties:
        schema_name = property_spec.name
        python_name = parameter_name(property_spec)
        value_source = (
            f"_expression_string({python_name})"
            if schema_name == "expr"
            else python_name
        )
        if schema_name == "expr" and schema_name not in spec.required:
            value_source = (
                f"_expression_string(cast(str | ExpressionOperand, {python_name}))"
            )
        parameters.append(parameter_source(property_spec))
        if schema_name in spec.required:
            assignments.append(f"        transform[{schema_name!r}] = {value_source}")
        else:
            assignments.extend(
                [
                    f"        if {python_name} is not Undefined:",
                    f"            transform[{schema_name!r}] = {value_source}",
                ]
            )

    if spec.transform_type == "filter":
        signature = "\n".join(
            [
                f"    def {spec.method_name}(",
                "        self,",
                "        expression: str | Parameter | UndefinedType = Undefined,",
                "        *,",
                *parameters,
                "    ) -> Self:",
            ]
        )
    else:
        positional_parameters = [
            parameter_source(property_spec) for property_spec in positional_properties
        ]
        remaining_parameters = [
            parameter_source(property_spec) for property_spec in remaining_properties
        ]
        signature_lines = [
            f"    def {spec.method_name}(",
            "        self,",
            *positional_parameters,
        ]
        if remaining_parameters:
            signature_lines.extend(["        *,", *remaining_parameters])
        if spec.repeat_keyword_properties is not None:
            _, value_property = spec.repeat_keyword_properties
            value_spec = properties_by_name[value_property]
            value_annotation = _qualified_transform_annotation(
                value_spec.annotation.annotation
            )
            if value_property == "expr":
                value_annotation = f"{value_annotation} | ExpressionOperand"
            signature_lines.append(f"        **kwargs: {value_annotation},")
        signature_lines.append("    ) -> Self:")
        signature = "\n".join(signature_lines)

    validation_lines = (
        [
            "        from genome_spy._parameters import Parameter",
            "",
            "        if expression is not Undefined:",
            "            if expr is not Undefined or param is not Undefined:",
            '                raise TypeError("expression cannot be combined with expr or param")',
            "            if isinstance(expression, Parameter):",
            "                if not expression.is_selection:",
            '                    raise TypeError("Only selection parameters can filter rows directly.")',
            "                param = expression.name",
            "                if empty is Undefined:",
            "                    empty = expression.empty",
            "            else:",
            "                expr = expression",
            "        if expr is Undefined and param is Undefined:",
            '            raise TypeError("filter requires an expression or param")',
        ]
        if spec.transform_type == "filter"
        else []
    )
    doc_properties = [
        PropertySpec(
            name=aliases.get(property_spec.name, property_spec.name),
            annotation=property_spec.annotation,
            nested_schema_class_name=property_spec.nested_schema_class_name,
            description=property_spec.description,
        )
        for property_spec in ordered_properties
    ]

    if spec.repeat_keyword_properties is not None:
        output_property, value_property = spec.repeat_keyword_properties
        if set(spec.repeat_keyword_properties) != set(properties_by_name):
            raise ValueError(
                f"Repeated transform method {spec.method_name!r} must contain "
                "exactly its output and value properties."
            )
        output_name = parameter_name(properties_by_name[output_property])
        value_name = parameter_name(properties_by_name[value_property])
        expression_values = value_property == "expr"
        value_annotation = properties_by_name[value_property].annotation.annotation
        if expression_values:
            value_annotation = f"{value_annotation} | ExpressionOperand"
        missing_pair_message = (
            f"{spec.method_name} requires {output_name!r} and {value_name!r} together."
        )
        if spec.example is None:
            raise ValueError(
                f"Repeated transform method {spec.method_name!r} requires an example."
            )
        docstring = _method_docstring(
            f"Add one or more ``{spec.transform_type}`` transforms.",
            tuple(doc_properties),
            indent=8,
            description=(
                "Pass both direct arguments for one transform, or use keyword",
                "arguments to append one transform per output in insertion order.",
            ),
            extra_args=(
                f"**kwargs ({value_annotation}): Additional output field names",
                f"    mapped to {value_name} values.",
            ),
            returns=(
                "Self: A new specification with the transform or transforms appended."
            ),
            raises=(
                f"TypeError: If only one of ``{output_name}`` and ``{value_name}``",
                "    is provided.",
            ),
            example=spec.example,
        )
        repeated_lines = [
            f"        has_output = {output_name} is not Undefined",
            f"        has_value = {value_name} is not Undefined",
            "        if has_output != has_value:",
            f"            raise TypeError({missing_pair_message!r})",
            "        result = self",
            "        if has_output and has_value:",
            f"            transform: dict[str, Any] = {{'type': {spec.transform_type!r}}}",
            f"            transform[{output_property!r}] = {output_name}",
            f"            transform[{value_property!r}] = "
            + (
                f"_expression_string(cast(str | ExpressionOperand, {value_name}))"
                if expression_values
                else value_name
            ),
            "            result = result._append_transform(transform)  "
            "# type: ignore[attr-defined]",
            "        for output, value in kwargs.items():",
            f"            transform = {{'type': {spec.transform_type!r}}}",
            f"            transform[{output_property!r}] = output",
            f"            transform[{value_property!r}] = "
            + ("_expression_string(value)" if expression_values else "value"),
            "            result = result._append_transform(transform)  "
            "# type: ignore[attr-defined]",
            "        return result",
        ]
    else:
        docstring = _method_docstring(
            f"Add a ``{spec.transform_type}`` transform.",
            tuple(doc_properties),
            indent=8,
        )
        repeated_lines = [
            f"        transform: dict[str, Any] = {{'type': {spec.transform_type!r}}}",
            *validation_lines,
            *assignments,
            "        return self._append_transform(transform)  "
            "# type: ignore[attr-defined, no-any-return]",
        ]

    return "\n".join(
        [
            signature,
            docstring,
            *repeated_lines,
            "",
        ]
    )


def _configure_method_source(property_specs: tuple[PropertySpec, ...]) -> str:
    """Return the explicit top-level config builder method."""
    return _nested_schema_method_source(
        method_name="configure",
        value_annotation="core.GenomeSpyConfig | GenomeSpyConfigKwds | None | object",
        property_specs=property_specs,
        docstring="Return a chart with merged top-level config.",
        call="self._configure(value, **defined)",
    )


def _config_method_source(
    property_name: str,
    *,
    annotation: str,
    nested_schema_class_name: str | None,
    raw_mapping_annotation: str,
    property_specs: tuple[PropertySpec, ...],
) -> str:
    method_name = f"configure_{_snake_name(property_name)}"
    if nested_schema_class_name is None:
        return (
            "\n"
            f"    def {method_name}(\n"
            f"        self,\n"
            f"        value: {annotation},\n"
            "    ) -> Self:\n"
            f'        """Return a chart with ``{property_name}`` config updated."""\n'
            f"        return self._configure_property({property_name!r}, value)  "
            "# type: ignore[attr-defined, no-any-return]\n"
        )
    return "\n" + _nested_schema_method_source(
        method_name=method_name,
        value_annotation=(
            f"core.{nested_schema_class_name} | {raw_mapping_annotation} | None | object"
        ),
        property_specs=property_specs,
        docstring=(f"Return a chart with ``{property_name}`` config updated."),
        call=f"self._configure_nested({property_name!r}, value, **defined)",
    )


def _nested_schema_method_source(
    *,
    method_name: str,
    value_annotation: str,
    property_specs: tuple[PropertySpec, ...],
    docstring: str,
    call: str,
    return_annotation: str = "Self",
    suppress_override: bool = False,
    suppress_return: bool = True,
    qualify_annotations: bool = True,
) -> str:
    """Render a method accepting a mapping object or its explicit properties."""
    parameters = "\n".join(
        f"        {property_spec.python_name}: "
        f"{_qualified_transform_annotation(property_spec.annotation.annotation) if qualify_annotations else property_spec.annotation.annotation} "
        "| UndefinedType = Undefined,"
        for property_spec in property_specs
    )
    property_values = "\n".join(
        f"            {property_spec.name!r}: {property_spec.python_name},"
        for property_spec in property_specs
    )
    body = (
        "        defined = {\n"
        + property_values
        + "\n        }\n"
        + "        defined = {key: item for key, item in defined.items() "
        + "if item is not Undefined}\n"
    )
    if parameters:
        signature = (
            f"    def {method_name}("
            + ("  # type: ignore[override]\n" if suppress_override else "\n")
            + "        self,\n"
            + f"        value: {value_annotation} = Undefined,\n"
            "        /,\n"
            "        *,\n"
            f"{parameters}\n"
            f"    ) -> {return_annotation}:\n"
        )
    else:
        signature = (
            f"    def {method_name}("
            + ("  # type: ignore[override]\n" if suppress_override else "\n")
            + "        self,\n"
            + f"        value: {value_annotation} = Undefined,\n"
            "        /,\n"
            f"    ) -> {return_annotation}:\n"
        )
        body = "        defined: dict[str, Any] = {}\n"
    return (
        signature
        + _method_docstring(docstring, property_specs, indent=8)
        + "\n"
        + body
        + f"        return {call}"
        + ("  # type: ignore[attr-defined, no-any-return]" if suppress_return else "")
        + "\n"
    )


def _channel_class_source(
    class_name: str,
    encoding_name: str,
    *,
    nested_setters: tuple[tuple[str, str, str], ...],
    nested_property_specs: dict[str, tuple[PropertySpec, ...]],
    simple_setters: tuple[PropertySpec, ...],
    constructor_property_specs: tuple[PropertySpec, ...],
    sort_property_specs: tuple[PropertySpec, ...],
) -> str:
    simple_methods = "".join(
        _channel_simple_setter_source(
            class_name,
            property_name=property_spec.name,
            annotation=property_spec.annotation.annotation,
            sort_property_specs=sort_property_specs,
        )
        for property_spec in simple_setters
        if property_spec.name != "sort"
    ) + (
        _channel_simple_setter_source(
            class_name,
            property_name="sort",
            annotation="",
            sort_property_specs=sort_property_specs,
        )
        if sort_property_specs
        else ""
    )
    methods = "".join(
        _channel_nested_setter_source(
            class_name,
            property_name,
            schema_class_name,
            raw_mapping_annotation,
            property_specs=nested_property_specs[property_name],
        )
        for property_name, schema_class_name, raw_mapping_annotation in nested_setters
    )
    nested_property_annotations = {
        property_name: f"{schema_class_name} | {raw_mapping_annotation} | None"
        for property_name, schema_class_name, raw_mapping_annotation in nested_setters
    }
    constructor_properties = [
        (
            property_spec.name,
            property_spec.python_name,
            property_spec.annotation.annotation,
        )
        for property_spec in simple_setters
        if property_spec.name != "value"
    ] + [
        (property_name, property_name, annotation)
        for property_name, annotation in nested_property_annotations.items()
    ]
    constructor_parameters = "\n".join(
        f"        {python_name}: {annotation} | UndefinedType = _MISSING,"
        for _, python_name, annotation in constructor_properties
    )
    constructor_values = "\n".join(
        f"            {property_name!r}: {python_name},"
        for property_name, python_name, _ in constructor_properties
    )
    constructor_property_names = {
        "value",
        *(name for name, _, _ in constructor_properties),
    }
    constructor_docs = tuple(
        property_spec
        for property_spec in constructor_property_specs
        if property_spec.name in constructor_property_names
    )
    return (
        f"class {class_name}(Channel):\n"
        f'    """Generated wrapper for the ``{encoding_name}`` encoding channel."""\n\n'
        "    def __init__(\n"
        "        self,\n"
        "        value: Channel | SchemaBase | str | dict[str, Any],\n"
        "        /,\n"
        "        *,\n"
        f"{constructor_parameters}\n"
        "    ) -> None:\n"
        + _method_docstring(
            f"Create a ``{encoding_name}`` encoding channel.",
            constructor_docs,
            indent=8,
        )
        + "\n"
        "        properties = {\n"
        f"{constructor_values}\n"
        "        }\n"
        "        defined = {key: item for key, item in properties.items() if item is not _MISSING}\n"
        f"        wrapped = channel(value, encoding_name={encoding_name!r}, **defined)\n"
        f"        super().__init__(wrapped.definition, encoding_name={encoding_name!r})\n"
        f"{simple_methods}"
        f"{methods}"
    )


def _channel_simple_setter_source(
    channel_class_name: str,
    *,
    property_name: str,
    annotation: str,
    sort_property_specs: tuple[PropertySpec, ...],
) -> str:
    if property_name == "sort":
        parameters = "\n".join(
            f"        {property_spec.python_name}: "
            f"{property_spec.annotation.annotation} | UndefinedType = Undefined,"
            for property_spec in sort_property_specs
        )
        values = "\n".join(
            f"            {property_spec.name!r}: {property_spec.python_name},"
            for property_spec in sort_property_specs
        )
        return (
            "\n"
            "    def sort(\n"
            "        self,\n"
            "        value: CompareParams | CompareParamsKwds | str | list[str] | None | object = _MISSING,\n"
            "        /,\n"
            "        *,\n"
            f"{parameters}\n"
            "    ) -> "
            f"{channel_class_name}:\n"
            '        """Return a channel with a ``sort`` configuration."""\n'
            "        properties = {\n"
            f"{values}\n"
            "        }\n"
            "        defined = {key: item for key, item in properties.items() if item is not Undefined}\n"
            f"        return self._with_sort(value, defined)\n"
        )
    return (
        "\n"
        f"    def {property_name}(\n"
        "        self,\n"
        f"        value: {annotation},\n"
        f"    ) -> {channel_class_name}:\n"
        f'        """Return a channel with ``{property_name}`` updated."""\n'
        f"        return self._with_property({property_name!r}, value)\n"
    )


def _channel_nested_setter_source(
    channel_class_name: str,
    property_name: str,
    schema_class_name: str,
    raw_mapping_annotation: str,
    *,
    property_specs: tuple[PropertySpec, ...],
) -> str:
    return "\n" + _nested_schema_method_source(
        method_name=property_name,
        value_annotation=(
            f"{schema_class_name} | {raw_mapping_annotation} | None | object"
        ),
        property_specs=property_specs,
        docstring=(f"Return a channel with a ``{schema_class_name}`` {property_name}."),
        call=f"self._with_nested({property_name!r}, value, **defined)",
        return_annotation=channel_class_name,
        suppress_override=False,
        suppress_return=False,
    )


def _nested_property_specs(
    analyzer: SchemaAnalyzer, class_name: str | None
) -> tuple[PropertySpec, ...]:
    """Return schema properties for a generated nested wrapper class."""
    if class_name is None:
        return ()
    for definition_name, definition_schema in analyzer.definitions.items():
        if _class_name(definition_name) == class_name and isinstance(
            definition_schema, dict
        ):
            return analyzer.property_specs(
                SchemaDefinition(definition_name, definition_schema)
            )
    return ()


def _schema_property_method_source(
    class_name: str,
    property_name: str,
    *,
    annotation: str,
    nested_schema_class_name: str | None,
    nested_property_specs: tuple[PropertySpec, ...] = (),
) -> str:
    method_name = _python_property_name(property_name)
    if nested_schema_class_name is None:
        value_annotation = annotation if annotation != "Any" else "Any"
        return (
            "\n"
            f"    def {method_name}(self, value: {value_annotation}) -> {class_name}:\n"
            f'        """Return a copy with ``{property_name}`` updated."""\n'
            f"        return self._with_property({property_name!r}, value)\n"
        )
    return "\n" + _nested_schema_method_source(
        method_name=method_name,
        value_annotation=_nested_value_annotation(annotation),
        property_specs=tuple(
            property_spec
            for property_spec in nested_property_specs
            if property_spec.name != "value"
        ),
        docstring=(
            f"Return a copy with a ``{nested_schema_class_name}`` {property_name}."
        ),
        call=f"self._with_property({property_name!r}, value, **defined)",
        return_annotation=class_name,
        suppress_return=False,
        qualify_annotations=False,
    )


def _nested_value_annotation(annotation: str) -> str:
    """Add optional nested-setter sentinels without duplicating schema variants."""
    return " | ".join(dict.fromkeys([*annotation.split(" | "), "None", "object"]))


def _typed_dict_source(name: str, property_specs: tuple[PropertySpec, ...]) -> str:
    fields = "\n".join(
        f"    {property_spec.name}: {property_spec.annotation.annotation}"
        for property_spec in property_specs
        if not keyword.iskeyword(property_spec.name)
    )
    if not fields:
        fields = "    pass"
    return (
        f"class {name}(TypedDict, total=False):\n"
        f'    """TypedDict helper for raw ``{name.removesuffix("Kwds")}`` mappings."""\n'
        f"{fields}\n"
    )


GENERATED_HEADER = (
    '"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""\n'
)
