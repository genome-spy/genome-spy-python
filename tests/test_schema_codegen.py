from __future__ import annotations

import json
from pathlib import Path

from tools.generate_schema_wrapper import write_schema_package
from tools.schemapi.codegen import SchemaWrapperGenerator


def test_schema_wrapper_generator_summarizes_definitions() -> None:
    schema = {
        "definitions": {
            "mark-def": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "size": {"type": "number"},
                    "class": {"type": "string"},
                },
                "required": ["type"],
            }
        }
    }

    generator = SchemaWrapperGenerator(schema)
    definitions = generator.definitions()
    module = generator.generate_core_module()
    mixins_module = generator.generate_mark_mixins_module()

    assert definitions[0].name == "mark-def"
    assert definitions[0].required == ("type",)
    assert module.exports == (
        "GenomeSpySchema",
        "MARK_TYPES",
        "Root",
        "load_schema",
        "MarkDef",
    )
    assert "MARK_TYPES = ()" in module.source
    assert "class MarkDef" in module.source
    assert "class=Undefined" not in module.source
    assert "type: Any = Undefined" in module.source
    assert mixins_module.exports == ("MarkMethodMixin",)
    assert "class MarkMethodMixin" in mixins_module.source


def test_write_schema_package_uses_unpacked_npm_package(tmp_path: Path) -> None:
    package_dir = tmp_path / "package"
    schema_dir = package_dir / "dist"
    spec_dir = package_dir / "src" / "spec"
    output_dir = tmp_path / "generated"
    reference_dir = tmp_path / "references"
    schema_dir.mkdir(parents=True)
    spec_dir.mkdir(parents=True)

    (package_dir / "package.json").write_text(
        json.dumps({"name": "@genome-spy/core", "version": "9.8.7"}),
        encoding="utf-8",
    )
    (schema_dir / "schema.json").write_text(
        json.dumps(
            {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "definitions": {
                    "MarkType": {"type": "string", "enum": ["point", "rect"]},
                    "UnitSpec": {
                        "type": "object",
                        "properties": {"mark": {"type": "string"}},
                    },
                },
            }
        )
        + "\n\n",
        encoding="utf-8",
    )
    (spec_dir / "root.d.ts").write_text(
        "export interface RootConfig { $schema?: string; }\n",
        encoding="utf-8",
    )

    write_schema_package(
        package_dir,
        output_dir,
        spec_reference_dir=reference_dir,
    )

    assert (output_dir / "genome-spy-schema.json").exists()
    assert (
        (output_dir / "genome-spy-schema.json")
        .read_text(encoding="utf-8")
        .endswith("}\n")
    )
    assert (
        not (output_dir / "genome-spy-schema.json")
        .read_text(encoding="utf-8")
        .endswith("}\n\n")
    )
    assert "class UnitSpec" in (output_dir / "core.py").read_text(encoding="utf-8")
    assert "MARK_TYPES = ('point', 'rect')" in (output_dir / "core.py").read_text(
        encoding="utf-8"
    )
    mixins = (output_dir / "mixins.py").read_text(encoding="utf-8")
    assert "def mark_point" in mixins
    assert "def mark_rect" in mixins
    assert "SCHEMA_VERSION = '9.8.7'" in (output_dir / "__init__.py").read_text(
        encoding="utf-8"
    )
    assert (
        (reference_dir / "root.d.ts")
        .read_text(encoding="utf-8")
        .startswith("export interface RootConfig")
    )
    assert (reference_dir / "VERSION").read_text(encoding="utf-8") == "9.8.7\n"
