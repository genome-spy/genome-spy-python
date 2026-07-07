from __future__ import annotations

import json
from pathlib import Path

from tools.generate_schema_wrapper import write_schema_package
from tools.schemapi.codegen import SchemaWrapperGenerator


def test_schema_wrapper_generator_summarizes_definitions() -> None:
    schema = {
        "definitions": {
            "Axis": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                },
            },
            "align-def": {
                "enum": ["left", "right"],
                "type": "string",
            },
            "mark-def": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "size": {"type": "number"},
                    "flag": {"type": "boolean"},
                    "values": {"type": "array", "items": {"type": "integer"}},
                    "mode": {"enum": ["fast", "slow"]},
                    "axis": {"$ref": "#/definitions/Axis"},
                    "align": {"$ref": "#/definitions/align-def"},
                    "axisOrNull": {
                        "anyOf": [
                            {"$ref": "#/definitions/Axis"},
                            {"type": "null"},
                        ]
                    },
                    "class": {"type": "string"},
                },
                "required": ["type"],
            },
        }
    }

    generator = SchemaWrapperGenerator(schema)
    definitions = generator.definitions()
    module = generator.generate_core_module()
    typing_module = generator.generate_typing_module()
    kwds_module = generator.generate_kwds_module()
    mixins_module = generator.generate_mark_mixins_module()
    channels_module = generator.generate_channels_module()

    assert [definition.name for definition in definitions] == [
        "Axis",
        "align-def",
        "mark-def",
    ]
    assert definitions[2].required == ("type",)
    assert module.exports == (
        "GenomeSpySchema",
        "MARK_TYPES",
        "Root",
        "load_schema",
        "Axis",
        "AlignDef",
        "MarkDef",
    )
    assert "MARK_TYPES = ()" in module.source
    assert "from genome_spy.schema._typing import AlignDef_T" in module.source
    assert "from genome_spy.schema._kwds import AxisKwds" in module.source
    assert "class MarkDef" in module.source
    assert "class=Undefined" not in module.source
    assert "type: str | UndefinedType = Undefined" in module.source
    assert "size: float | UndefinedType = Undefined" in module.source
    assert "flag: bool | UndefinedType = Undefined" in module.source
    assert "values: Sequence[int] | UndefinedType = Undefined" in module.source
    assert "align: AlignDef_T | UndefinedType = Undefined" in module.source
    assert "mode: Literal['fast', 'slow'] | UndefinedType = Undefined" in module.source
    assert "axis: Axis | AxisKwds | UndefinedType = Undefined" in module.source
    assert (
        "axisOrNull: Axis | AxisKwds | None | UndefinedType = Undefined"
        in module.source
    )
    assert "def with_axis(" in module.source
    assert "value: Axis | AxisKwds | None | Any = Undefined" in module.source
    assert "def with_align(self, value: AlignDef_T) -> MarkDef:" in module.source
    assert "def with_flag(self, value: bool) -> MarkDef:" in module.source
    assert "def with_values(self, value: Sequence[int]) -> MarkDef:" in module.source
    assert typing_module.exports == ("AlignDef_T",)
    assert "AlignDef_T: TypeAlias = Literal['left', 'right']" in typing_module.source
    assert kwds_module.exports == ("AxisKwds",)
    assert "class AxisKwds(TypedDict, total=False):" in kwds_module.source
    assert "title: str" in kwds_module.source
    assert mixins_module.exports == ("MarkMethodMixin",)
    assert "class MarkMethodMixin" in mixins_module.source
    assert channels_module.exports == ()


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
                    "Encoding": {
                        "type": "object",
                        "properties": {
                            "color": {"type": "object"},
                            "x": {"type": "object"},
                        },
                    },
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
    assert (output_dir / "_typing.py").exists()
    assert (output_dir / "_kwds.py").exists()
    assert "MARK_TYPES = ('point', 'rect')" in (output_dir / "core.py").read_text(
        encoding="utf-8"
    )
    mixins = (output_dir / "mixins.py").read_text(encoding="utf-8")
    assert "def mark_point" in mixins
    assert "def mark_rect" in mixins
    channels = (output_dir / "channels.py").read_text(encoding="utf-8")
    assert "class Color(Channel)" in channels
    assert "class X(Channel)" in channels
    assert "SCHEMA_VERSION = '9.8.7'" in (output_dir / "__init__.py").read_text(
        encoding="utf-8"
    )
    assert (
        (reference_dir / "root.d.ts")
        .read_text(encoding="utf-8")
        .startswith("export interface RootConfig")
    )
    assert (reference_dir / "VERSION").read_text(encoding="utf-8") == "9.8.7\n"
