from __future__ import annotations

import inspect
import json
from pathlib import Path

import genome_spy as gs
import pytest
from tools.generate_schema_wrapper import (
    TRANSFORM_METHOD_OVERRIDES,
    write_schema_files,
    write_schema_package,
)
from tools.schemapi.codegen import (
    SchemaWrapperGenerator,
    TransformMethodOverride,
)
from tools.schemapi.expression_codegen import parse_expression_catalog

pytestmark = pytest.mark.codegen

GENOME_SPY_EXPRESSION_DOCS = """
## Conditional operators
And an equivalent `if` construct:
### Constants and functions from Vega
#### Constants
[`NaN`](https://vega.github.io/vega/docs/expressions/#NaN)
#### Type Checking Functions
[`isValid`](https://vega.github.io/vega/docs/expressions/#isValid)
#### Math Functions
[`max`](https://vega.github.io/vega/docs/expressions/#max),
[`sin`](https://vega.github.io/vega/docs/expressions/#sin)
#### Sequence Functions
[`slice`](https://vega.github.io/vega/docs/expressions/#slice)
### Scale Functions
<a name="scale" href="#scale">#</a>
<b>scale</b>(<i>channel</i>, <i>value</i>)<br/>
### Other Functions
<a name="mapHasKey" href="#mapHasKey">#</a>
<b>mapHasKey</b>(<i>map</i>, <i>key</i>)<br/>
"""
VEGA_EXPRESSION_DOCS = """
<a name="if" href="#if">#</a>
<b>if</b>(<i>test</i>, <i>thenValue</i>, <i>elseValue</i>)<br/>
<a name="isValid" href="#isValid">#</a>
<b>isValid</b>(<i>value</i>)<br/>
<a name="max" href="#max">#</a>
<b>max</b>(<i>value1</i>, <i>value2</i>, ...)<br/>
<a name="sin" href="#sin">#</a>
<b>sin</b>(<i>value</i>)<br/>
<a name="slice" href="#slice">#</a>
<b>slice</b>(<i>array</i>, <i>start</i>[, <i>end</i>])<br/>
"""
EXPRESSION_CATALOG = parse_expression_catalog(
    GENOME_SPY_EXPRESSION_DOCS, VEGA_EXPRESSION_DOCS
)


def test_parse_expression_catalog_uses_upstream_surface_and_signatures() -> None:
    catalog = EXPRESSION_CATALOG

    assert catalog.constants == ("NaN",)
    assert [function.name for function in catalog.functions] == [
        "if",
        "isValid",
        "max",
        "sin",
        "slice",
        "scale",
        "mapHasKey",
    ]
    assert catalog.functions[0].python_name == "if_"
    assert catalog.functions[0].parameters[1].name == "then_value"
    assert catalog.functions[2].parameters[-1].variadic is True
    assert catalog.functions[4].parameters[-1].optional is True


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
                    "axisOrNumber": {
                        "anyOf": [
                            {"$ref": "#/definitions/Axis"},
                            {"type": "number"},
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
    composition_module = generator.generate_composition_module()
    lazy_module = generator.generate_lazy_module()
    ergonomics_module = generator.generate_ergonomics_module()

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
    assert "with_property_setters" not in module.source
    assert "class MarkDef" in module.source
    assert "@with_property_setters" not in module.source
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
    assert (
        "axisOrNumber: Axis | AxisKwds | float | UndefinedType = Undefined"
        in module.source
    )
    assert "def axis(" in module.source
    assert "value: Axis | AxisKwds | None | object = Undefined" in module.source
    assert "value: Axis | AxisKwds | float | None | object = Undefined" in module.source
    assert "title: str | UndefinedType = Undefined" in module.source
    assert "def align(self, value: AlignDef_T) -> MarkDef:" in module.source
    assert "def flag(self, value: bool) -> MarkDef:" in module.source
    assert "def class_(self, value: str) -> MarkDef:" in module.source
    assert "def values(self, value: Sequence[int]) -> MarkDef:" in module.source
    assert typing_module.exports == ("AlignDef_T",)
    assert "AlignDef_T: TypeAlias = Literal['left', 'right']" in typing_module.source
    assert kwds_module.exports == ("AxisKwds",)
    assert "class AxisKwds(TypedDict, total=False):" in kwds_module.source
    assert "title: str" in kwds_module.source
    assert {"EncodingMethodMixin", "MarkMethodMixin", "TransformMethodMixin"} <= set(
        mixins_module.exports
    )
    assert "class MarkMethodMixin" in mixins_module.source
    assert "class TransformMethodMixin" in mixins_module.source
    assert channels_module.exports == ()
    assert composition_module.exports == (
        "layer",
        "hconcat",
        "vconcat",
        "concat",
        "multiscale",
        "import_view",
    )
    assert "def vconcat(" in composition_module.source
    assert "def import_view(" in composition_module.source
    assert "**kwargs" not in composition_module.source
    assert lazy_module.exports == ("LazyDataMethodMixin",)
    assert ergonomics_module.exports == (
        "DatumChannelMethodMixin",
        "LocusChannelMethodMixin",
        "ValueChannelMethodMixin",
    )


def test_generate_ergonomics_module_emits_schema_factory_helpers() -> None:
    schema = json.loads(
        Path("src/genome_spy/schema/genome-spy-schema.json").read_text(encoding="utf-8")
    )
    ergonomics_module = SchemaWrapperGenerator(schema).generate_ergonomics_module()

    assert {
        "title",
        "dynamic_opacity",
        "data_format",
        "param",
        "view",
        "view_config",
        "config",
    } <= set(ergonomics_module.exports)
    assert "def title(\n    text:" in ergonomics_module.source
    assert "def param(\n    name: str," in ergonomics_module.source
    assert "def config(\n    *," in ergonomics_module.source
    assert "if isinstance(defined.get('view'), core.ViewBackground):" in (
        ergonomics_module.source
    )
    assert "def copy(\n        self," in (
        SchemaWrapperGenerator(schema).generate_mark_mixins_module().source
    )


def test_generated_parameter_docs_are_separated_from_method_summaries() -> None:
    schema = json.loads(
        Path("src/genome_spy/schema/genome-spy-schema.json").read_text(encoding="utf-8")
    )
    generator = SchemaWrapperGenerator(schema)

    assert (
        '"""Return a chart with merged top-level config.\n\n        Args:'
        in generator.generate_mark_mixins_module().source
    )
    assert (
        '"""Return a vconcat composition of the given charts.\n\n    Args:'
        in generator.generate_composition_module().source
    )


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


def test_generate_transform_method_overrides_from_schema_properties() -> None:
    schema = {
        "definitions": {
            "FormulaParams": {
                "type": "object",
                "required": ["type", "as", "expr"],
                "properties": {
                    "type": {"const": "formula", "type": "string"},
                    "as": {"type": "string"},
                    "expr": {"type": "string"},
                    "description": {"type": "string"},
                },
            },
            "FlattenParams": {
                "type": "object",
                "required": ["type"],
                "properties": {
                    "type": {"const": "flatten", "type": "string"},
                    "fields": {"type": "array", "items": {"type": "string"}},
                    "as": {"type": "array", "items": {"type": "string"}},
                    "index": {"type": "string"},
                },
            },
            "SampleParams": {
                "type": "object",
                "required": ["type"],
                "properties": {
                    "type": {"const": "sample", "type": "string"},
                    "size": {"type": "number"},
                    "description": {"type": "string"},
                },
            },
            "TransformParams": {
                "anyOf": [
                    {"$ref": "#/definitions/FormulaParams"},
                    {"$ref": "#/definitions/FlattenParams"},
                    {"$ref": "#/definitions/SampleParams"},
                ]
            },
        }
    }

    generator = SchemaWrapperGenerator(
        schema,
        transform_method_overrides=TRANSFORM_METHOD_OVERRIDES,
    )
    specs = {spec.method_name: spec for spec in generator.transform_method_specs()}
    source = generator.generate_mark_mixins_module().source

    assert specs["transform_calculate"].property_aliases == (("expr", "calculate"),)
    assert specs["transform_flatten"].positional_properties == ("fields", "as")
    assert specs["transform_sample"].positional_properties == ("size",)
    assert "def transform_calculate(" in source
    assert "calculate: str | UndefinedType = Undefined" in source
    assert "transform['expr'] = calculate" in source
    assert "for output, value in kwargs.items():" in source
    assert "Add one or more ``formula`` transforms." in source
    assert "**kwargs (str): Additional output field names" in source
    assert "one transform per output in insertion order" in source
    assert "Returns:" in source
    assert "Raises:" in source
    assert "If only one of ``as_`` and ``calculate``" in source
    assert '>>> chart.transform_calculate(doubled="datum.value * 2")' in source
    assert "def transform_flatten(\n        self,\n        fields:" in source
    assert "def transform_sample(\n        self,\n        size:" in source


def test_transform_method_overrides_must_target_union_members() -> None:
    schema = {
        "definitions": {
            "LookupParams": {
                "type": "object",
                "properties": {
                    "type": {"const": "lookup", "type": "string"},
                },
            },
            "TransformParams": {"anyOf": [{"$ref": "#/definitions/LookupParams"}]},
        }
    }
    generator = SchemaWrapperGenerator(
        schema,
        transform_method_overrides={"MissingParams": TransformMethodOverride()},
    )

    with pytest.raises(
        ValueError,
        match="overrides refer to schemas absent from TransformParams: MissingParams",
    ):
        generator.transform_method_specs()


def test_duplicate_generated_transform_methods_fail_generation() -> None:
    schema = {
        "definitions": {
            "FirstSampleParams": {
                "type": "object",
                "properties": {
                    "type": {"const": "sample", "type": "string"},
                },
            },
            "SecondSampleParams": {
                "type": "object",
                "properties": {
                    "type": {"const": "sample", "type": "string"},
                },
            },
            "TransformParams": {
                "anyOf": [
                    {"$ref": "#/definitions/FirstSampleParams"},
                    {"$ref": "#/definitions/SecondSampleParams"},
                ]
            },
        }
    }

    with pytest.raises(
        ValueError,
        match=(
            "Duplicate generated transform methods: transform_sample "
            r"\(FirstSampleParams, SecondSampleParams\)"
        ),
    ):
        SchemaWrapperGenerator(schema).transform_method_specs()


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

    assert {
        "ConfigMethodMixin",
        "EncodingMethodMixin",
        "MarkMethodMixin",
        "TransformMethodMixin",
    } <= set(mixins_module.exports)
    assert "class ConfigMethodMixin" in mixins_module.source
    assert "def mark_rect(" in mixins_module.source
    assert "minWidth: float | UndefinedType = Undefined" in mixins_module.source
    assert "@use_signature(core.RectProps)" not in mixins_module.source
    assert "def configure(" in mixins_module.source
    assert "axis: core.AxisConfig | AxisConfigKwds | UndefinedType = Undefined" in (
        mixins_module.source
    )
    assert "def configure_axis(" in mixins_module.source
    assert "title: str | UndefinedType = Undefined" in mixins_module.source


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
                            "field": {
                                "$ref": "#/definitions/FieldName",
                                "description": "Data field to encode.",
                            },
                            "sort": {"$ref": "#/definitions/CompareParams"},
                            "title": {
                                "type": ["string", "null"],
                                "description": "Channel title.",
                            },
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
    assert (
        '"""Create a ``x`` encoding channel.\n\n        Args:' in channels_module.source
    )
    assert "field (FieldName_T): Data field to encode." in channels_module.source
    assert "title (str | None): Channel title." in channels_module.source
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
    assert "field: str | UndefinedType = Undefined" in channels_module.source
    assert "return self._with_sort(value, defined)" in channels_module.source


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
    assert "value: ExtraConfig | dict[str, Any] | None | object = Undefined" in (
        channels_module.source
    )
    assert "padding: float | UndefinedType = Undefined" in channels_module.source
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
        json.dumps(
            {
                "name": "@genome-spy/core",
                "version": "9.8.7",
                "dependencies": {"vega-expression": "^6.1.0"},
            }
        ),
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
        expression_catalog=EXPRESSION_CATALOG,
        transform_method_overrides={},
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
    assert (output_dir / "lazy.py").exists()
    assert (output_dir / "ergonomics.py").exists()
    expressions = (output_dir / "expressions.py").read_text(encoding="utf-8")
    assert "class expr(core.ExprRef" in expressions
    assert "def if_(" in expressions
    assert "return _function_expression('sin', value)" in expressions
    assert json.loads(
        (output_dir / "capabilities.json").read_text(encoding="utf-8")
    ) == {
        "schema_version": "9.8.7",
        "definitions": ["Encoding", "MarkType", "UnitSpec"],
        "marks": ["point", "rect"],
        "encoding_channels": ["color", "x"],
        "transforms": [],
        "lazy_data_sources": [],
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

    write_schema_files(
        schema_path,
        output_dir,
        version="dev-local",
        expression_catalog=EXPRESSION_CATALOG,
        transform_method_overrides={},
    )

    capabilities = json.loads(
        (output_dir / "capabilities.json").read_text(encoding="utf-8")
    )
    assert capabilities["schema_version"] == "dev-local"
    assert capabilities["marks"] == ["point"]
    assert "SCHEMA_VERSION = 'dev-local'" in (output_dir / "__init__.py").read_text(
        encoding="utf-8"
    )


def test_generate_lazy_data_helpers_from_schema_union() -> None:
    schema = {
        "definitions": {
            "LazyDataParams": {
                "anyOf": [
                    {"$ref": "#/definitions/SignalData"},
                    {"$ref": "#/definitions/InternalData"},
                ]
            },
            "SignalData": {
                "type": "object",
                "required": ["type", "url"],
                "properties": {
                    "type": {"const": "signal", "type": "string"},
                    "url": {"type": "string"},
                    "windowSize": {"type": "number"},
                },
            },
            "InternalData": {
                "type": "object",
                "required": ["type"],
                "properties": {"type": {"const": "internal", "type": "string"}},
            },
        }
    }

    module = SchemaWrapperGenerator(schema).generate_lazy_module()

    assert "def signal(" in module.source
    assert "url: str" in module.source
    assert "windowSize: float | UndefinedType = Undefined" in module.source
    assert "type=cast(Any, 'signal'), url=url, **defined" in module.source
    assert "def internal(" not in module.source
    assert "**kwargs" not in module.source


def test_generated_mark_methods_expose_schema_backed_signatures() -> None:
    rect_signature = inspect.signature(gs.Chart().mark_rect)
    point_signature = inspect.signature(gs.Chart().mark_point)
    circle_signature = inspect.signature(gs.Chart().mark_circle)

    assert "minWidth" in rect_signature.parameters
    assert "tooltip" in rect_signature.parameters
    assert "geometricZoomBound" in point_signature.parameters
    assert "kwargs" not in rect_signature.parameters
    assert "kwargs" not in circle_signature.parameters
    assert "size" in circle_signature.parameters
    assert "type" not in rect_signature.parameters
    assert rect_signature.parameters["minWidth"].kind is inspect.Parameter.KEYWORD_ONLY
    assert not hasattr(gs.Chart.mark_rect, "__wrapped__")


def test_generated_config_methods_expose_schema_backed_signatures() -> None:
    configure_signature = inspect.signature(gs.Chart().configure)
    axis_signature = inspect.signature(gs.Chart().configure_axis)

    assert "axis" in configure_signature.parameters
    assert "view" in configure_signature.parameters
    assert "title" in axis_signature.parameters
    assert "kwargs" not in axis_signature.parameters
    assert axis_signature.parameters["title"].kind is inspect.Parameter.KEYWORD_ONLY
    assert not hasattr(gs.Chart.configure_axis, "__wrapped__")


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


def test_resolution_methods_follow_referenced_resolution_maps() -> None:
    """0.85.0 moved resolve channels behind a shared ResolutionMap reference."""
    schema = {
        "definitions": {
            "ResolutionBehavior": {
                "enum": ["independent", "shared"],
                "type": "string",
            },
            "LegendResolutionBehavior": {
                "anyOf": [
                    {"$ref": "#/definitions/ResolutionBehavior"},
                    {"const": "collected", "type": "string"},
                ]
            },
            "ResolutionMap<ResolutionBehavior>": {
                "properties": {
                    "color": {"$ref": "#/definitions/ResolutionBehavior"},
                    "x": {"$ref": "#/definitions/ResolutionBehavior"},
                },
                "type": "object",
            },
            "ResolutionMap<LegendResolutionBehavior>": {
                "properties": {
                    "color": {"$ref": "#/definitions/LegendResolutionBehavior"},
                },
                "type": "object",
            },
            "CoreRootSpec": {
                "anyOf": [
                    {
                        "properties": {
                            "resolve": {
                                "properties": {
                                    "axis": {
                                        "$ref": "#/definitions/ResolutionMap%3CResolutionBehavior%3E"
                                    },
                                    "legend": {
                                        "$ref": "#/definitions/ResolutionMap%3CLegendResolutionBehavior%3E"
                                    },
                                    "scale": {
                                        "$ref": "#/definitions/ResolutionMap%3CResolutionBehavior%3E"
                                    },
                                },
                                "type": "object",
                            }
                        },
                        "type": "object",
                    }
                ]
            },
        }
    }

    source = SchemaWrapperGenerator(schema).generate_mark_mixins_module().source

    # A dropped reference produced `def resolve_axis(self, *, ) -> Self:`, which
    # is not valid Python, and an uncollected alias left the name undefined.
    start = source.index("class ResolutionMethodMixin:")
    end = source.index("\nclass ", start + 1)
    compile(source[start:end], "mixins.py", "exec")

    assert "def resolve_axis(\n        self,\n        *,\n        color:" in source
    assert "LegendResolutionBehavior_T" in source
    assert "ResolutionBehavior_T" in source
