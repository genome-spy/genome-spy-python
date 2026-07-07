"""Minimal code generator scaffolding for GenomeSpy schema wrappers.

The module is adapted from Altair's schema-generation architecture.
Altair's generator is broad and mature: it walks Vega-Lite definitions,
derives constructors, emits type annotations, generates channels, and wires
runtime validation. This module is the GenomeSpy starting point. It currently
summarizes JSON Schema definitions and emits simple wrapper class source;
the interfaces are shaped so they can grow toward Altair's architecture while
accounting for GenomeSpy-specific schema conventions.
"""

from __future__ import annotations

import keyword
import re
from urllib.parse import unquote
from dataclasses import dataclass
from typing import Any

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

    def property_specs(self, definition: SchemaDefinition) -> tuple[PropertySpec, ...]:
        resolved_properties = self.resolve_properties(definition.schema)
        object_property_refs = self._resolved_object_property_refs(definition.schema)
        property_names = [
            name
            for name in self.resolved_identifier_properties(definition.schema)
            if name.isidentifier() and not keyword.iskeyword(name)
        ]
        return tuple(
            PropertySpec(
                name=name,
                annotation=self._property_spec_annotation(
                    name,
                    resolved_properties.get(name, {}),
                ),
                nested_schema_class_name=object_property_refs.get(name),
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
        self, rootschema: dict[str, Any], *, schema_version: str = "unknown"
    ) -> None:
        self.rootschema = rootschema
        self.schema_version = schema_version

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

    def channel_nested_setters(self, encoding_name: str) -> tuple[tuple[str, str], ...]:
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
        setters: list[tuple[str, str]] = []
        for property_name in ("axis", "scale", "legend"):
            nested_schema = resolved_properties.get(property_name)
            if not isinstance(nested_schema, dict):
                continue
            ref_name = _first_ref_name(nested_schema)
            if ref_name is None:
                continue
            setters.append((property_name, _class_name(ref_name)))
        return tuple(setters)

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
            if not self._base_analyzer.schema_looks_object_like(definition.schema):
                continue
            names.append(_kwds_type_name(definition.name))
        names.extend(self._anonymous_kwds_sources())
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
            if not self._analyzer.schema_looks_object_like(definition.schema):
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

        extra_helper_sources = self._anonymous_kwds_sources()
        if any(name.endswith("ResolveKwds") for name in extra_helper_sources):
            used_aliases.update({"ResolutionBehavior_T"})
        if any(name == "AxesKwds" for name in extra_helper_sources):
            used_core_classes.update({"GenomeAxis"})
        if any(name == "LegendsKwds" for name in extra_helper_sources):
            used_core_classes.update({"Legend"})
        if any(name == "ScalesKwds" for name in extra_helper_sources):
            used_core_classes.update({"Scale"})

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
                *extra_helper_sources.values(),
                "__all__ = "
                + repr(
                    [
                        *(helper_name for helper_name, _ in helper_specs),
                        *extra_helper_sources,
                    ]
                ),
                "",
            ]
        )
        return GeneratedModule(
            source=source,
            exports=tuple(
                [
                    *(helper_name for helper_name, _ in helper_specs),
                    *extra_helper_sources,
                ]
            ),
        )

    def _anonymous_kwds_sources(self) -> dict[str, str]:
        property_names: set[str] = set()
        for definition in self.definitions():
            resolved_properties = self._base_analyzer.resolve_properties(
                definition.schema
            )
            for property_name, helper_name in ANONYMOUS_PROPERTY_KWDS.items():
                schema = resolved_properties.get(property_name)
                if not isinstance(schema, dict):
                    continue
                if self._base_analyzer._looks_like_anonymous_kwds_target(
                    property_name, schema
                ):
                    property_names.add(property_name)
        return _anonymous_property_kwds_sources(property_names)

    def generate_mark_mixins_module(self) -> GeneratedModule:
        """Generate chart mark methods from the upstream mark enum."""
        methods = [_mark_method_source(mark_type) for mark_type in self.mark_types()]
        source = "\n".join(
            [
                GENERATED_HEADER,
                "from __future__ import annotations",
                "from typing import Any, Self",
                "",
                "class MarkMethodMixin:",
                '    """Grammar-derived mark methods for the handwritten chart API."""',
                "",
                *(methods or ["    pass"]),
                "",
                '__all__ = ["MarkMethodMixin"]',
                "",
            ]
        )
        return GeneratedModule(source=source, exports=("MarkMethodMixin",))

    def generate_channels_module(self) -> GeneratedModule:
        """Generate named channel wrappers from the upstream encoding schema."""
        exports: list[str] = []
        classes: list[str] = []
        kwds_type_names = set(self.kwds_type_names())
        helper_class_names = {
            class_name
            for encoding_name in self.encoding_channels()
            for _, class_name in self.channel_nested_setters(encoding_name)
        }
        helper_kwds_names = {
            _kwds_type_name(class_name)
            for class_name in helper_class_names
            if _kwds_type_name(class_name) in kwds_type_names
        }
        for encoding_name in self.encoding_channels():
            class_name = _class_name(encoding_name)
            exports.append(class_name)
            classes.append(
                _channel_class_source(
                    class_name,
                    encoding_name,
                    nested_setters=self.channel_nested_setters(encoding_name),
                    analyzer=self._analyzer,
                )
            )
        helper_imports = ", ".join(sorted(helper_class_names))
        source = "\n".join(
            [
                GENERATED_HEADER,
                "from __future__ import annotations",
                "from typing import Any",
                "",
                "from genome_spy.channels import Channel, _MISSING, channel",
                (
                    "from genome_spy.schema.core import " + helper_imports
                    if helper_imports
                    else ""
                ),
                (
                    "from genome_spy.schema._kwds import "
                    + ", ".join(sorted(helper_kwds_names))
                    if helper_kwds_names
                    else ""
                ),
                "",
                *classes,
                "__all__ = " + repr(exports),
                "",
            ]
        )
        return GeneratedModule(source=source, exports=tuple(exports))


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


def _schema_class_source(
    class_name: str,
    definition: SchemaDefinition,
    *,
    analyzer: SchemaAnalyzer,
) -> GeneratedSchemaClass:
    property_specs = analyzer.property_specs(definition)
    args = ", ".join(
        f"{property_spec.name}: {property_spec.annotation.annotation} | UndefinedType = Undefined"
        for property_spec in property_specs
    )
    if args:
        args = ", " + args

    assignments = ", ".join(
        f"{property_spec.name}={property_spec.name}" for property_spec in property_specs
    )
    body = f"super().__init__({assignments})" if assignments else "super().__init__()"
    methods = "".join(
        _schema_property_method_source(
            class_name,
            property_spec.name,
            annotation=property_spec.annotation.annotation,
            nested_schema_class_name=property_spec.nested_schema_class_name,
            raw_mapping_annotation=(
                analyzer.raw_mapping_annotation(property_spec.nested_schema_class_name)
                if property_spec.nested_schema_class_name is not None
                else "dict[str, Any]"
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


def _mark_method_source(mark_type: str) -> str:
    method_name = mark_type.replace("-", "_")
    return (
        f"    def mark_{method_name}(self, **kwargs: Any) -> Self:\n"
        f'        """Set the chart mark to ``{mark_type}``."""\n'
        f"        return self._with_mark({mark_type!r}, **kwargs)  "
        "# type: ignore[attr-defined, no-any-return]"
    )


def _channel_class_source(
    class_name: str,
    encoding_name: str,
    *,
    nested_setters: tuple[tuple[str, str], ...],
    analyzer: SchemaAnalyzer,
) -> str:
    methods = "".join(
        _channel_nested_setter_source(
            class_name,
            property_name,
            schema_class_name,
            analyzer.raw_mapping_annotation(schema_class_name),
        )
        for property_name, schema_class_name in nested_setters
    )
    return (
        f"class {class_name}(Channel):\n"
        f'    """Generated wrapper for the ``{encoding_name}`` encoding channel."""\n\n'
        "    def __init__(\n"
        "        self, value: Channel | str | dict[str, Any], /, **kwargs: Any\n"
        "    ) -> None:\n"
        f"        wrapped = channel(value, encoding_name={encoding_name!r}, **kwargs)\n"
        f"        super().__init__(wrapped.definition, encoding_name={encoding_name!r})\n"
        f"{methods}"
    )


def _channel_nested_setter_source(
    channel_class_name: str,
    property_name: str,
    schema_class_name: str,
    raw_mapping_annotation: str,
) -> str:
    return (
        "\n"
        f"    def {property_name}(\n"
        f"        self,\n"
        f"        value: {schema_class_name} | {raw_mapping_annotation} | None | object = _MISSING,\n"
        f"        /,\n"
        f"        **kwargs: Any,\n"
        f"    ) -> {channel_class_name}:\n"
        f'        """Return a channel with a ``{schema_class_name}`` {property_name}."""\n'
        f"        return self._with_nested({property_name!r}, value, **kwargs)\n"
    )


def _schema_property_method_source(
    class_name: str,
    property_name: str,
    *,
    annotation: str,
    nested_schema_class_name: str | None,
    raw_mapping_annotation: str = "dict[str, Any]",
) -> str:
    method_name = f"with_{property_name}"
    if nested_schema_class_name is None:
        value_annotation = annotation if annotation != "Any" else "Any"
        return (
            "\n"
            f"    def {method_name}(self, value: {value_annotation}) -> {class_name}:\n"
            f'        """Return a copy with ``{property_name}`` updated."""\n'
            f"        return self._with_property({property_name!r}, value)\n"
        )
    return (
        "\n"
        f"    def {method_name}(\n"
        f"        self,\n"
        f"        value: {nested_schema_class_name} | {raw_mapping_annotation} | None | Any = Undefined,\n"
        f"        /,\n"
        f"        **kwargs: Any,\n"
        f"    ) -> {class_name}:\n"
        f'        """Return a copy with a ``{nested_schema_class_name}`` {property_name}."""\n'
        f"        return self._with_property({property_name!r}, value, **kwargs)\n"
    )


def _typed_dict_source(name: str, property_specs: tuple[PropertySpec, ...]) -> str:
    fields = "\n".join(
        f"    {property_spec.name}: {property_spec.annotation.annotation}"
        for property_spec in property_specs
    )
    if not fields:
        fields = "    pass"
    return (
        f"class {name}(TypedDict, total=False):\n"
        f'    """TypedDict helper for raw ``{name.removesuffix("Kwds")}`` mappings."""\n'
        f"{fields}\n"
    )


def _anonymous_property_kwds_sources(property_names: set[str]) -> dict[str, str]:
    sources: dict[str, str] = {}
    if "axes" in property_names:
        sources["AxesKwds"] = "\n".join(
            [
                "class AxesKwds(TypedDict, total=False):",
                '    """TypedDict helper for composed-view axis resolution mappings."""',
                "    x: GenomeAxis | GenomeAxisKwds",
                "    y: GenomeAxis | GenomeAxisKwds",
            ]
        )
    if "legends" in property_names:
        sources["LegendsKwds"] = "\n".join(
            [
                "class LegendsKwds(TypedDict, total=False):",
                '    """TypedDict helper for composed-view legend resolution mappings."""',
                "    angle: Legend | LegendKwds",
                "    color: Legend | LegendKwds",
                "    dx: Legend | LegendKwds",
                "    dy: Legend | LegendKwds",
                "    fill: Legend | LegendKwds",
                "    fillOpacity: Legend | LegendKwds",
                "    opacity: Legend | LegendKwds",
                "    shape: Legend | LegendKwds",
                "    size: Legend | LegendKwds",
                "    stroke: Legend | LegendKwds",
                "    strokeOpacity: Legend | LegendKwds",
                "    strokeWidth: Legend | LegendKwds",
            ]
        )
    if "scales" in property_names:
        sources["ScalesKwds"] = "\n".join(
            [
                "class ScalesKwds(TypedDict, total=False):",
                '    """TypedDict helper for composed-view scale resolution mappings."""',
                "    angle: Scale | ScaleKwds",
                "    color: Scale | ScaleKwds",
                "    dx: Scale | ScaleKwds",
                "    dy: Scale | ScaleKwds",
                "    fill: Scale | ScaleKwds",
                "    fillOpacity: Scale | ScaleKwds",
                "    opacity: Scale | ScaleKwds",
                "    shape: Scale | ScaleKwds",
                "    size: Scale | ScaleKwds",
                "    stroke: Scale | ScaleKwds",
                "    strokeOpacity: Scale | ScaleKwds",
                "    strokeWidth: Scale | ScaleKwds",
                "    x: Scale | ScaleKwds",
                "    x2: Scale | ScaleKwds",
                "    y: Scale | ScaleKwds",
                "    y2: Scale | ScaleKwds",
            ]
        )
    if "resolve" in property_names:
        sources["AxisResolveKwds"] = "\n".join(
            [
                "class AxisResolveKwds(TypedDict, total=False):",
                '    """TypedDict helper for axis resolution behavior mappings."""',
                "    angle: ResolutionBehavior_T",
                "    color: ResolutionBehavior_T",
                "    default: ResolutionBehavior_T",
                "    dx: ResolutionBehavior_T",
                "    dy: ResolutionBehavior_T",
                "    facetIndex: ResolutionBehavior_T",
                "    fill: ResolutionBehavior_T",
                "    fillOpacity: ResolutionBehavior_T",
                "    key: ResolutionBehavior_T",
                "    opacity: ResolutionBehavior_T",
                "    sample: ResolutionBehavior_T",
                "    search: ResolutionBehavior_T",
                "    semanticScore: ResolutionBehavior_T",
                "    shape: ResolutionBehavior_T",
                "    size: ResolutionBehavior_T",
                "    stroke: ResolutionBehavior_T",
                "    strokeOpacity: ResolutionBehavior_T",
                "    strokeWidth: ResolutionBehavior_T",
                "    text: ResolutionBehavior_T",
                "    uniqueId: ResolutionBehavior_T",
                "    x: ResolutionBehavior_T",
                "    x2: ResolutionBehavior_T",
                "    y: ResolutionBehavior_T",
                "    y2: ResolutionBehavior_T",
            ]
        )
        sources["LegendResolveKwds"] = "\n".join(
            [
                "class LegendResolveKwds(TypedDict, total=False):",
                '    """TypedDict helper for legend resolution behavior mappings."""',
                "    angle: ResolutionBehavior_T",
                "    color: ResolutionBehavior_T",
                "    default: ResolutionBehavior_T",
                "    dx: ResolutionBehavior_T",
                "    dy: ResolutionBehavior_T",
                "    facetIndex: ResolutionBehavior_T",
                "    fill: ResolutionBehavior_T",
                "    fillOpacity: ResolutionBehavior_T",
                "    key: ResolutionBehavior_T",
                "    opacity: ResolutionBehavior_T",
                "    sample: ResolutionBehavior_T",
                "    search: ResolutionBehavior_T",
                "    semanticScore: ResolutionBehavior_T",
                "    shape: ResolutionBehavior_T",
                "    size: ResolutionBehavior_T",
                "    stroke: ResolutionBehavior_T",
                "    strokeOpacity: ResolutionBehavior_T",
                "    strokeWidth: ResolutionBehavior_T",
                "    text: ResolutionBehavior_T",
                "    uniqueId: ResolutionBehavior_T",
                "    x: ResolutionBehavior_T",
                "    x2: ResolutionBehavior_T",
                "    y: ResolutionBehavior_T",
                "    y2: ResolutionBehavior_T",
            ]
        )
        sources["ScaleResolveKwds"] = "\n".join(
            [
                "class ScaleResolveKwds(TypedDict, total=False):",
                '    """TypedDict helper for scale resolution behavior mappings."""',
                "    angle: ResolutionBehavior_T",
                "    color: ResolutionBehavior_T",
                "    default: ResolutionBehavior_T",
                "    dx: ResolutionBehavior_T",
                "    dy: ResolutionBehavior_T",
                "    facetIndex: ResolutionBehavior_T",
                "    fill: ResolutionBehavior_T",
                "    fillOpacity: ResolutionBehavior_T",
                "    key: ResolutionBehavior_T",
                "    opacity: ResolutionBehavior_T",
                "    sample: ResolutionBehavior_T",
                "    search: ResolutionBehavior_T",
                "    semanticScore: ResolutionBehavior_T",
                "    shape: ResolutionBehavior_T",
                "    size: ResolutionBehavior_T",
                "    stroke: ResolutionBehavior_T",
                "    strokeOpacity: ResolutionBehavior_T",
                "    strokeWidth: ResolutionBehavior_T",
                "    text: ResolutionBehavior_T",
                "    uniqueId: ResolutionBehavior_T",
                "    x: ResolutionBehavior_T",
                "    x2: ResolutionBehavior_T",
                "    y: ResolutionBehavior_T",
                "    y2: ResolutionBehavior_T",
            ]
        )
        sources["ResolveKwds"] = "\n".join(
            [
                "class ResolveKwds(TypedDict, total=False):",
                '    """TypedDict helper for composed-view resolution mappings."""',
                "    axis: AxisResolveKwds",
                "    legend: LegendResolveKwds",
                "    scale: ScaleResolveKwds",
            ]
        )
    return sources


GENERATED_HEADER = (
    '"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""\n'
)
