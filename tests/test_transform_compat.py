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
