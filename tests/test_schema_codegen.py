from __future__ import annotations

import inspect
import json
from pathlib import Path

import genome_spy as gs
from genome_spy.schema.core import AxisConfig, RectProps

from tools.generate_schema_wrapper import write_schema_files, write_schema_package
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
    assert "with_property_setters" in module.source
    assert "class MarkDef" in module.source
    assert "@with_property_setters" in module.source
    assert "class_: str | UndefinedType = Undefined" in module.source
    assert "'class': class_" in module.source
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
    assert "def with_class(self, value: str) -> MarkDef:" in module.source
    assert "def with_values(self, value: Sequence[int]) -> MarkDef:" in module.source
    assert typing_module.exports == ("AlignDef_T",)
    assert "AlignDef_T: TypeAlias = Literal['left', 'right']" in typing_module.source
    assert kwds_module.exports == ("AxisKwds",)
    assert "class AxisKwds(TypedDict, total=False):" in kwds_module.source
    assert "title: str" in kwds_module.source
    assert mixins_module.exports == ("MarkMethodMixin", "TransformMethodMixin")
    assert "class MarkMethodMixin" in mixins_module.source
    assert "class TransformMethodMixin" in mixins_module.source
    assert channels_module.exports == ()


def test_generate_transform_methods_from_schema_union() -> None:
    schema = {
        "definitions": {
            "LookupParams": {
                "type": "object",
                "required": ["type", "from", "key"],
                "properties": {
                    "type": {"const": "lookup", "type": "string"},
                    "from": {"type": "object"},
                    "key": {"type": "string"},
                    "as": {"type": "array", "items": {"type": "string"}},
                },
            },
            "TransformParams": {"anyOf": [{"$ref": "#/definitions/LookupParams"}]},
        }
    }

    generator = SchemaWrapperGenerator(schema, schema_version="1.2.3")
    specs = generator.transform_method_specs()
    mixins_module = generator.generate_mark_mixins_module()
    manifest = generator.capability_manifest()

    assert len(specs) == 1
    assert specs[0].method_name == "transform_lookup"
    assert specs[0].required == frozenset({"from", "key"})
    assert "def transform_lookup(" in mixins_module.source
    assert "from_: dict[str, Any]," in mixins_module.source
    assert "as_: Sequence[str] | UndefinedType = Undefined" in mixins_module.source
    assert "transform['from'] = from_" in mixins_module.source
    assert "transform['as'] = as_" in mixins_module.source
    assert manifest["transforms"] == [
        {
            "schema": "LookupParams",
            "type": "lookup",
            "method": "transform_lookup",
        }
    ]


def test_generated_filter_requires_a_predicate() -> None:
    schema = {
        "definitions": {
            "ExprFilterParams": {
                "type": "object",
                "required": ["expr", "type"],
                "properties": {
                    "expr": {"type": "string"},
                    "type": {"const": "filter", "type": "string"},
                },
            },
            "SelectionFilterParams": {
                "type": "object",
                "required": ["param", "type"],
                "properties": {
                    "param": {"type": "string"},
                    "type": {"const": "filter", "type": "string"},
                },
            },
            "FilterParams": {
                "anyOf": [
                    {"$ref": "#/definitions/ExprFilterParams"},
                    {"$ref": "#/definitions/SelectionFilterParams"},
                ]
            },
            "TransformParams": {"anyOf": [{"$ref": "#/definitions/FilterParams"}]},
        }
    }

    source = SchemaWrapperGenerator(schema).generate_mark_mixins_module().source

    assert "if expr is Undefined and param is Undefined:" in source
    assert 'raise TypeError("filter requires an expression or param")' in source


def test_generate_mark_mixins_module_emits_config_methods_when_schema_supports_them() -> (
    None
):
    schema = {
        "definitions": {
            "AxisConfig": {
                "type": "object",
                "properties": {"title": {"type": "string"}},
            },
            "GenomeSpyConfig": {
                "type": "object",
                "properties": {"axis": {"$ref": "#/definitions/AxisConfig"}},
            },
            "MarkType": {"type": "string", "enum": ["rect"]},
            "RectProps": {
                "type": "object",
                "properties": {"minWidth": {"type": "number"}},
            },
        }
    }

    mixins_module = SchemaWrapperGenerator(schema).generate_mark_mixins_module()

    assert mixins_module.exports == (
        "ConfigMethodMixin",
        "MarkMethodMixin",
        "TransformMethodMixin",
    )
    assert "class ConfigMethodMixin" in mixins_module.source
    assert "def configure(" in mixins_module.source
    assert "@use_signature(core.GenomeSpyConfig)" in mixins_module.source
    assert "def configure_axis(" in mixins_module.source
    assert "@use_signature(core.AxisConfig)" in mixins_module.source


def test_generate_kwds_module_emits_helper_relevant_kwds_targets() -> None:
    schema = {
        "definitions": {
            "Parse": {
                "type": "object",
                "properties": {"chrom": {"type": "string"}},
            },
            "DataFormat": {
                "anyOf": [
                    {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "parse": {"$ref": "#/definitions/Parse"},
                        },
                    },
                    {"type": "null"},
                ],
            },
            "DynamicOpacity": {
                "type": "object",
                "properties": {
                    "channel": {"type": "string"},
                    "values": {"type": "array", "items": {"type": "number"}},
                },
            },
            "Parameter": {
                "anyOf": [
                    {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "expr": {"type": "string"},
                        },
                    },
                    {"type": "string"},
                ],
            },
        }
    }

    kwds_module = SchemaWrapperGenerator(schema).generate_kwds_module()

    assert "class ParseKwds(TypedDict, total=False):" in kwds_module.source
    assert "class DataFormatKwds(TypedDict, total=False):" in kwds_module.source
    assert "class DynamicOpacityKwds(TypedDict, total=False):" in kwds_module.source
    assert "class ParameterKwds(TypedDict, total=False):" in kwds_module.source
    assert "parse: Parse | ParseKwds" in kwds_module.source
    assert "values: Sequence[float]" in kwds_module.source
    assert "name: str" in kwds_module.source


def test_generate_channels_module_emits_schema_driven_channel_setters() -> None:
    schema = {
        "definitions": {
            "FieldName": {"type": "string"},
            "Type": {"enum": ["quantitative", "nominal"], "type": "string"},
            "CompareParams": {
                "type": "object",
                "properties": {"field": {"type": "string"}},
            },
            "Encoding": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "object",
                        "properties": {
                            "field": {"$ref": "#/definitions/FieldName"},
                            "sort": {"$ref": "#/definitions/CompareParams"},
                            "title": {"type": ["string", "null"]},
                            "type": {"$ref": "#/definitions/Type"},
                        },
                    }
                },
            },
        }
    }

    channels_module = SchemaWrapperGenerator(schema).generate_channels_module()

    assert channels_module.exports == ("X",)
    assert "value: Channel | SchemaBase | str | dict[str, Any]" in (
        channels_module.source
    )
    assert "from genome_spy.schemapi import SchemaBase" in channels_module.source
    assert "from genome_spy.schema.core import CompareParams" in channels_module.source
    assert (
        "from genome_spy.schema._kwds import CompareParamsKwds"
        in channels_module.source
    )
    assert "def title(" in channels_module.source
    assert "value: str | None" in channels_module.source
    assert "return self._with_property('title', value)" in channels_module.source
    assert "def field(" in channels_module.source
    assert "value: str" in channels_module.source
    assert "def type(" in channels_module.source
    assert "value: Type_T" in channels_module.source
    assert "def sort(" in channels_module.source
    assert "CompareParams | CompareParamsKwds | str | list[str] | None | object" in (
        channels_module.source
    )
    assert "return super().sort(value, **kwargs)" in channels_module.source


def test_generate_channels_module_discovers_nested_setters_from_schema() -> None:
    schema = {
        "definitions": {
            "Axis": {
                "type": "object",
                "properties": {"title": {"type": "string"}},
            },
            "ExtraConfig": {
                "type": "object",
                "properties": {"padding": {"type": "number"}},
            },
            "ExprRef": {
                "type": "object",
                "properties": {"expr": {"type": "string"}},
            },
            "FieldName": {"type": "string"},
            "Encoding": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "object",
                        "properties": {
                            "axis": {
                                "anyOf": [
                                    {"$ref": "#/definitions/Axis"},
                                    {"type": "null"},
                                ]
                            },
                            "extra": {
                                "anyOf": [
                                    {"$ref": "#/definitions/ExtraConfig"},
                                    {"type": "null"},
                                ]
                            },
                            "chrom": {"$ref": "#/definitions/FieldName"},
                            "value": {
                                "anyOf": [
                                    {"$ref": "#/definitions/ExprRef"},
                                    {"type": "number"},
                                ]
                            },
                        },
                    }
                },
            },
        }
    }

    channels_module = SchemaWrapperGenerator(schema).generate_channels_module()

    assert "def axis(" in channels_module.source
    assert "def extra(" in channels_module.source
    assert "value: ExtraConfig | dict[str, Any] | None | object = _MISSING" in (
        channels_module.source
    )
    assert "def chrom(" in channels_module.source
    assert "value: FieldName_T" in channels_module.source
    assert "def value(" in channels_module.source


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
    assert json.loads(
        (output_dir / "capabilities.json").read_text(encoding="utf-8")
    ) == {
        "schema_version": "9.8.7",
        "definitions": ["Encoding", "MarkType", "UnitSpec"],
        "marks": ["point", "rect"],
        "encoding_channels": ["color", "x"],
        "transforms": [],
        "root_spec_variants": [],
    }
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


def test_write_schema_files_supports_explicit_schema_input(tmp_path: Path) -> None:
    schema_path = tmp_path / "schema.json"
    output_dir = tmp_path / "generated"
    schema_path.write_text(
        json.dumps(
            {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "definitions": {
                    "MarkType": {"type": "string", "enum": ["point"]},
                },
            }
        ),
        encoding="utf-8",
    )

    write_schema_files(schema_path, output_dir, version="dev-local")

    capabilities = json.loads(
        (output_dir / "capabilities.json").read_text(encoding="utf-8")
    )
    assert capabilities["schema_version"] == "dev-local"
    assert capabilities["marks"] == ["point"]
    assert "SCHEMA_VERSION = 'dev-local'" in (output_dir / "__init__.py").read_text(
        encoding="utf-8"
    )


def test_generated_mark_methods_expose_schema_backed_signatures() -> None:
    rect_signature = inspect.signature(gs.Chart().mark_rect)
    point_signature = inspect.signature(gs.Chart().mark_point)

    assert "minWidth" in rect_signature.parameters
    assert "tooltip" in rect_signature.parameters
    assert "geometricZoomBound" in point_signature.parameters
    assert "kwargs" not in rect_signature.parameters
    assert gs.Chart.mark_rect.__wrapped__ is RectProps.__init__


def test_generated_config_methods_expose_schema_backed_signatures() -> None:
    configure_signature = inspect.signature(gs.Chart().configure)
    axis_signature = inspect.signature(gs.Chart().configure_axis)

    assert "axis" in configure_signature.parameters
    assert "view" in configure_signature.parameters
    assert "title" in axis_signature.parameters
    assert "kwargs" not in axis_signature.parameters
    assert gs.Chart.configure_axis.__wrapped__ is AxisConfig.__init__


def test_generated_schema_classes_expose_altair_style_property_setters() -> None:
    axis = gs.GenomeAxis().title("Position axis").grid(True)
    scale = gs.Scale().zero(False).scheme(name="blues")

    assert axis.to_dict(validate=False) == {
        "title": "Position axis",
        "grid": True,
    }
    assert scale.to_dict(validate=False) == {
        "zero": False,
        "scheme": {"name": "blues"},
    }


def test_generated_channel_title_methods_are_schema_backed() -> None:
    assert "title" in gs.X.__dict__
    assert "title" in gs.Color.__dict__

    titled = gs.X("value:Q").title("Coverage")

    assert isinstance(titled, gs.X)
    assert titled.to_dict()["title"] == "Coverage"
