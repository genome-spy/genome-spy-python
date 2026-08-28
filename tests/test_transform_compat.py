from __future__ import annotations

import pytest

import genome_spy as gs


def test_transform_calculate_adds_keyword_formulas_in_order() -> None:
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


def test_transform_calculate_combines_direct_and_keyword_forms() -> None:
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
    ("kwargs", "message"),
    [
        ({"as_": "result"}, "requires 'as_' and 'calculate' together"),
        ({"calculate": "datum.value"}, "requires 'as_' and 'calculate' together"),
        (
            {"as_": "result", "calculate": "datum.value", "as": "other"},
            "received both 'as_' and 'as'",
        ),
    ],
)
def test_transform_calculate_rejects_incomplete_or_duplicate_arguments(
    kwargs: dict[str, str], message: str
) -> None:
    with pytest.raises((TypeError, ValueError), match=message):
        gs.Chart([{"value": 1}]).mark_point().transform_calculate(**kwargs)


def test_transform_calculate_accepts_altair_as_alias() -> None:
    chart = (
        gs.Chart([{"value": 1}])
        .mark_point()
        .transform_calculate(**{"as": "result", "calculate": "datum.value"})
    )

    assert chart.to_dict()["transform"] == [
        {"type": "formula", "as": "result", "expr": "datum.value"}
    ]


@pytest.mark.parametrize(
    ("args", "kwargs"),
    [
        ((["items"],), {"as_": ["item"]}),
        ((["items"], ["item"]), {}),
    ],
)
def test_transform_flatten_accepts_altair_positional_forms(
    args: tuple[list[str], ...], kwargs: dict[str, list[str]]
) -> None:
    chart = (
        gs.Chart([{"items": [1, 2]}]).mark_point().transform_flatten(*args, **kwargs)
    )

    assert chart.to_dict()["transform"] == [
        {"type": "flatten", "fields": ["items"], "as": ["item"]}
    ]


def test_transform_flatten_preserves_genomespy_arguments() -> None:
    chart = (
        gs.Chart([{"items": [1, 2]}])
        .mark_point()
        .transform_flatten(fields=["items"], as_=["item"], index="item_index")
    )

    assert chart.to_dict()["transform"] == [
        {
            "type": "flatten",
            "fields": ["items"],
            "as": ["item"],
            "index": "item_index",
        }
    ]


def test_transform_flatten_rejects_duplicate_field_arguments() -> None:
    with pytest.raises(TypeError, match="received both 'flatten' and 'fields'"):
        gs.Chart([{"items": [1, 2]}]).transform_flatten(
            ["items"], fields=["other_items"]
        )


@pytest.mark.parametrize(
    ("args", "kwargs", "expected_size"),
    [
        ((), {}, 1000),
        ((250,), {}, 250),
        ((), {"size": 500}, 500),
    ],
)
def test_transform_sample_accepts_altair_and_genomespy_sizes(
    args: tuple[int, ...], kwargs: dict[str, int], expected_size: int
) -> None:
    chart = gs.Chart([{"value": 1}]).mark_point().transform_sample(*args, **kwargs)

    assert chart.to_dict()["transform"] == [{"type": "sample", "size": expected_size}]


def test_transform_sample_preserves_description() -> None:
    chart = (
        gs.Chart([{"value": 1}])
        .mark_point()
        .transform_sample(250, description="Keep a representative subset")
    )

    assert chart.to_dict()["transform"] == [
        {
            "type": "sample",
            "size": 250,
            "description": "Keep a representative subset",
        }
    ]


def test_transform_sample_rejects_duplicate_size_arguments() -> None:
    with pytest.raises(TypeError, match="received both 'sample' and 'size'"):
        gs.Chart([{"value": 1}]).transform_sample(250, size=500)


def test_transform_aggregate_accepts_keyword_shorthand() -> None:
    chart = (
        gs.Chart([{"group": "a", "response": 1}])
        .mark_point()
        .transform_aggregate(
            mean_response="mean(response)",
            total_response="sum(response)",
            groupby=["group"],
        )
    )

    assert chart.to_dict()["transform"] == [
        {
            "type": "aggregate",
            "fields": ["response", "response"],
            "ops": ["mean", "sum"],
            "as": ["mean_response", "total_response"],
            "groupby": ["group"],
        }
    ]


def test_transform_aggregate_appends_kwargs_after_mapping_definitions() -> None:
    definition = {"op": "average", "field": "response", "as": "mean_response"}
    chart = (
        gs.Chart([{"response": 1}])
        .mark_point()
        .transform_aggregate(
            [definition],
            maximum="max(response)",
        )
    )

    assert definition == {
        "op": "average",
        "field": "response",
        "as": "mean_response",
    }
    assert chart.to_dict()["transform"] == [
        {
            "type": "aggregate",
            "fields": ["response", "response"],
            "ops": ["mean", "max"],
            "as": ["mean_response", "maximum"],
        }
    ]


def test_transform_aggregate_preserves_native_arrays() -> None:
    chart = (
        gs.Chart([{"response": 1}])
        .mark_point()
        .transform_aggregate(
            fields=["response"],
            ops=["median"],
            as_=["median_response"],
        )
    )

    assert chart.to_dict()["transform"] == [
        {
            "type": "aggregate",
            "fields": ["response"],
            "ops": ["median"],
            "as": ["median_response"],
        }
    ]


@pytest.mark.parametrize(
    ("shorthand", "message"),
    [
        ("count()", "Fieldless aggregate shorthand is not supported"),
        ("distinct(response)", "Unsupported GenomeSpy aggregate operation"),
        ("mean", "expected 'operation\\(field\\)'"),
    ],
)
def test_transform_aggregate_rejects_unsupported_shorthand(
    shorthand: str, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        gs.Chart([{"response": 1}]).transform_aggregate(result=shorthand)


def test_transform_aggregate_rejects_mixed_call_shapes() -> None:
    with pytest.raises(TypeError, match="cannot mix compatibility definitions"):
        gs.Chart([{"response": 1}]).transform_aggregate(
            fields=["response"], result="mean(response)"
        )


def test_transform_filter_combines_raw_expressions_and_constraints() -> None:
    chart = (
        gs.Chart([{"year": 2000, "age": 20, "sample type": "tumor"}])
        .mark_point()
        .transform_filter(
            "datum.year > 1980",
            "datum.age != 90",
            **{"sample type": "tumor"},
        )
    )

    assert chart.to_dict()["transform"] == [
        {
            "type": "filter",
            "expr": "(datum.year > 1980) && (datum.age != 90) && "
            '(datum["sample type"] === "tumor")',
        }
    ]


def test_transform_filter_accepts_constraints_without_expression() -> None:
    chart = (
        gs.Chart([{"year": 2000, "active": True}])
        .mark_point()
        .transform_filter(year=2000, active=True)
    )

    assert chart.to_dict()["transform"] == [
        {
            "type": "filter",
            "expr": "(datum.year === 2000) && (datum.active === true)",
        }
    ]


def test_transform_filter_preserves_single_expression_and_native_param() -> None:
    expression_chart = (
        gs.Chart([{"year": 2000}]).mark_point().transform_filter("datum.year == 2000")
    )
    selection_chart = (
        gs.Chart([{"year": 2000}])
        .mark_point()
        .transform_filter(param="brush", empty=False, fields={"x": "year"})
    )

    assert expression_chart.to_dict()["transform"] == [
        {"type": "filter", "expr": "datum.year == 2000"}
    ]
    assert selection_chart.to_dict()["transform"] == [
        {
            "type": "filter",
            "param": "brush",
            "empty": False,
            "fields": {"x": "year"},
        }
    ]


def test_transform_filter_rejects_composition_with_selection() -> None:
    with pytest.raises(TypeError, match="cannot be combined with selection 'param'"):
        gs.Chart([{"year": 2000}]).transform_filter(
            "datum.year > 1980", "datum.year < 2020", param="brush"
        )


@pytest.mark.parametrize("value", [[1, 2], {"nested": True}, float("nan")])
def test_transform_filter_rejects_non_scalar_or_non_finite_constraints(
    value: object,
) -> None:
    with pytest.raises((TypeError, ValueError), match="Filter constraint"):
        gs.Chart([{"value": 1}]).transform_filter(value=value)  # type: ignore[arg-type]


def test_transform_stack_accepts_altair_positional_form() -> None:
    chart = (
        gs.Chart([{"group": "a", "site": "x", "value": 1}])
        .mark_rect()
        .transform_stack(
            "stacked",
            "value",
            ["group"],
            sort=[{"field": "site"}],
        )
    )

    assert chart.to_dict()["transform"] == [
        {
            "type": "stack",
            "field": "value",
            "groupby": ["group"],
            "as": ["stacked", "stacked_end"],
            "sort": {"field": ["site"], "order": ["ascending"]},
        }
    ]


def test_transform_stack_normalizes_multiple_sort_fields() -> None:
    chart = (
        gs.Chart([{"group": "a", "site": "x", "value": 1}])
        .mark_rect()
        .transform_stack(
            as_=["start", "end"],
            field="value",
            groupby=["group"],
            sort=[
                {"field": "site", "order": "descending"},
                {"field": "value"},
            ],
        )
    )

    assert chart.to_dict()["transform"] == [
        {
            "type": "stack",
            "field": "value",
            "groupby": ["group"],
            "as": ["start", "end"],
            "sort": {
                "field": ["site", "value"],
                "order": ["descending", "ascending"],
            },
        }
    ]


def test_transform_stack_preserves_native_compare_and_information_options() -> None:
    chart = (
        gs.Chart([{"base": "A", "value": 1}])
        .mark_rect()
        .transform_stack(
            field="value",
            groupby=["base"],
            offset="information",
            baseField="base",
            cardinality=4,
            sort=gs.compare("base", order="ascending"),
        )
    )

    assert chart.to_dict()["transform"] == [
        {
            "type": "stack",
            "field": "value",
            "groupby": ["base"],
            "offset": "information",
            "baseField": "base",
            "cardinality": 4,
            "sort": {"field": "base", "order": "ascending"},
        }
    ]


def test_transform_stack_rejects_ambiguous_field_names() -> None:
    with pytest.raises(TypeError, match="received both 'stack' and 'field'"):
        gs.Chart([{"value": 1}]).transform_stack(
            stack="value", field="other", groupby=["group"]
        )
