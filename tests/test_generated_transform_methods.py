from __future__ import annotations

import inspect

import pytest

import genome_spy as gs
from genome_spy.schema.mixins import TransformMethodMixin


def test_chart_uses_generated_transform_mixin_directly() -> None:
    assert TransformMethodMixin in gs.Chart.__mro__


def test_generated_calculate_adds_keyword_formulas_in_order() -> None:
    original = gs.Chart([{"value": 1}]).mark_point()

    calculated = original.transform_calculate(
        x="cos(datum.value)",
        y="sin(datum.value)",
    )

    assert "transform" not in original.to_dict(validate=False)
    assert calculated.to_dict()["transform"] == [
        {"type": "formula", "as": "x", "expr": "cos(datum.value)"},
        {"type": "formula", "as": "y", "expr": "sin(datum.value)"},
    ]


def test_generated_calculate_combines_direct_and_keyword_forms() -> None:
    chart = (
        gs.Chart([{"value": 1}])
        .mark_point()
        .transform_calculate(
            as_="double_value",
            calculate="datum.value * 2",
            square_value="datum.value ** 2",
        )
    )

    assert chart.to_dict()["transform"] == [
        {"type": "formula", "as": "double_value", "expr": "datum.value * 2"},
        {"type": "formula", "as": "square_value", "expr": "datum.value ** 2"},
    ]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"as_": "result"},
        {"calculate": "datum.value"},
    ],
)
def test_generated_calculate_requires_direct_argument_pair(
    kwargs: dict[str, str],
) -> None:
    with pytest.raises(
        TypeError,
        match="requires 'as_' and 'calculate' together",
    ):
        gs.Chart([{"value": 1}]).transform_calculate(**kwargs)


def test_generated_flatten_accepts_positional_fields_and_outputs() -> None:
    chart = (
        gs.Chart([{"items": [1, 2]}])
        .mark_point()
        .transform_flatten(["items"], ["item"], index="item_index")
    )

    assert chart.to_dict()["transform"] == [
        {
            "type": "flatten",
            "fields": ["items"],
            "as": ["item"],
            "index": "item_index",
        }
    ]


def test_generated_sample_accepts_positional_size_and_preserves_core_default() -> None:
    default_chart = gs.Chart([{"value": 1}]).mark_point().transform_sample()
    sized_chart = gs.Chart([{"value": 1}]).mark_point().transform_sample(250)

    assert default_chart.to_dict()["transform"] == [{"type": "sample"}]
    assert sized_chart.to_dict()["transform"] == [{"type": "sample", "size": 250}]


def test_generated_transform_signatures_expose_schema_typed_parameters() -> None:
    calculate = inspect.signature(gs.Chart.transform_calculate).parameters
    flatten = inspect.signature(gs.Chart.transform_flatten).parameters
    sample = inspect.signature(gs.Chart.transform_sample).parameters

    assert calculate["as_"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert calculate["calculate"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert flatten["fields"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert flatten["as_"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert sample["size"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
