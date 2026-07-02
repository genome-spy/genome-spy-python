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
        resolved_properties = _resolve_properties(channel_schema, self._definitions_map)
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
        chunks = [
            GENERATED_HEADER,
            "from __future__ import annotations",
            "import json",
            "from importlib.resources import files",
            "from typing import Any, cast",
            "",
            "from genome_spy.schemapi import SchemaBase, Undefined",
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
        seen_class_names = {"GenomeSpySchema", "Root"}

        for definition in self.definitions():
            class_name = _class_name(definition.name)
            if class_name in seen_class_names:
                class_name = f"{class_name}Def"
            seen_class_names.add(class_name)
            exports.append(class_name)
            chunks.append(
                _schema_class_source(
                    class_name,
                    definition,
                    definitions_map=self._definitions_map,
                )
            )

        all_line = "__all__ = " + repr(exports)
        return GeneratedModule(
            source="\n".join([*chunks, all_line]) + "\n", exports=tuple(exports)
        )

    def generate_init_module(self, core_exports: tuple[str, ...]) -> GeneratedModule:
        """Generate the package ``__init__.py`` for schema wrappers."""
        exports = (*core_exports, "SCHEMA_VERSION")
        source = "\n".join(
            [
                GENERATED_HEADER,
                "from genome_spy.schema.core import (",
                *[f"    {name}," for name in core_exports],
                ")",
                "",
                "SCHEMA_VERSION = " + repr(self.schema_version),
                "",
                "__all__ = " + repr(list(exports)),
                "",
            ]
        )
        return GeneratedModule(source=source, exports=exports)

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
        helper_class_names = {
            class_name
            for encoding_name in self.encoding_channels()
            for _, class_name in self.channel_nested_setters(encoding_name)
        }
        for encoding_name in self.encoding_channels():
            class_name = _class_name(encoding_name)
            exports.append(class_name)
            classes.append(
                _channel_class_source(
                    class_name,
                    encoding_name,
                    nested_setters=self.channel_nested_setters(encoding_name),
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


def _resolve_properties(
    schema: dict[str, Any],
    definitions: dict[str, Any],
    *,
    seen: frozenset[str] = frozenset(),
) -> dict[str, Any]:
    ref_name = _ref_name(schema)
    if ref_name is not None:
        target = definitions.get(ref_name)
        if not isinstance(target, dict) or ref_name in seen:
            return {}
        return _resolve_properties(target, definitions, seen=seen | {ref_name})

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
                resolved.update(_resolve_properties(variant, definitions, seen=seen))
    return resolved


def _resolved_identifier_properties(
    schema: dict[str, Any], definitions: dict[str, Any]
) -> tuple[str, ...]:
    return tuple(sorted(_resolve_properties(schema, definitions)))


def _schema_class_source(
    class_name: str,
    definition: SchemaDefinition,
    *,
    definitions_map: dict[str, Any],
) -> str:
    arg_names = [
        name
        for name in _resolved_identifier_properties(definition.schema, definitions_map)
        if name.isidentifier() and not keyword.iskeyword(name)
    ]
    args = ", ".join(f"{name}: Any = Undefined" for name in arg_names)
    if args:
        args = ", " + args

    assignments = ", ".join(f"{name}={name}" for name in arg_names)
    body = f"super().__init__({assignments})" if assignments else "super().__init__()"

    return (
        f"class {class_name}(GenomeSpySchema):\n"
        f'    """Generated wrapper for ``{definition.name}``."""\n\n'
        f'    _schema = _ROOT_SCHEMA.get("definitions", {{}}).get({definition.name!r}, {{}})\n\n'
        f"    def __init__(self{args}, **kwds: Any) -> None:\n"
        f"        {body}\n"
        f"        if kwds:\n"
        f"            self._kwds.update(kwds)\n"
    )


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
) -> str:
    methods = "".join(
        _channel_nested_setter_source(class_name, property_name, schema_class_name)
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
    channel_class_name: str, property_name: str, schema_class_name: str
) -> str:
    return (
        "\n"
        f"    def {property_name}(\n"
        f"        self,\n"
        f"        value: {schema_class_name} | dict[str, Any] | None | object = _MISSING,\n"
        f"        /,\n"
        f"        **kwargs: Any,\n"
        f"    ) -> {channel_class_name}:\n"
        f'        """Return a channel with a ``{schema_class_name}`` {property_name}."""\n'
        f"        return self._with_nested({property_name!r}, value, **kwargs)\n"
    )


GENERATED_HEADER = (
    '"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""\n'
)
