"""Minimal code generator scaffolding for GenomeSpy schema wrappers.

Altair's generator is broad and mature: it walks Vega-Lite definitions,
derives constructors, emits type annotations, generates channels, and wires
runtime validation. This module is the GenomeSpy starting point. It currently
summarizes JSON Schema definitions and emits simple wrapper class source; the
interfaces are shaped so they can grow toward Altair's architecture.
"""

from __future__ import annotations

from dataclasses import dataclass
import keyword
import re
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

    def definitions(self) -> list[SchemaDefinition]:
        """Return named schema definitions in deterministic order."""
        definitions = self.rootschema.get("definitions", {})
        if not isinstance(definitions, dict):
            return []
        return [
            SchemaDefinition(name, schema)
            for name, schema in sorted(definitions.items())
            if isinstance(schema, dict)
        ]

    def generate_core_module(self) -> GeneratedModule:
        """Generate a compact ``core.py``-style module."""
        exports: list[str] = ["GenomeSpySchema", "Root", "load_schema"]
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
            chunks.append(_schema_class_source(class_name, definition))

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


def _class_name(name: str) -> str:
    parts = re.split(r"[^0-9A-Za-z]+", name)
    class_name = "".join(part[:1].upper() + part[1:] for part in parts if part)
    if not class_name:
        return "GeneratedSchema"
    if class_name[0].isdigit():
        return f"Schema{class_name}"
    return class_name


def _schema_class_source(class_name: str, definition: SchemaDefinition) -> str:
    arg_names = [
        name
        for name in definition.properties
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


GENERATED_HEADER = (
    '"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""\n'
)
