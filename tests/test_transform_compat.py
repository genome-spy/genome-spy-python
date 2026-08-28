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
