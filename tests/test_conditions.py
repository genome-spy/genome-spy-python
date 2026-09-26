"""Selection predicate authoring follows the upstream conditional grammar."""

import pytest

import genome_spy as gs
from genome_spy.schema import NamedSelectionPredicateRef, SelectionPredicateOperand
from genome_spy.schemapi import SchemaValidationError


def test_composed_selection_condition_validates_complete_chart() -> None:
    left = gs.selection_interval("left", encodings=["x"], empty=False)
    right = gs.selection_interval("right", encodings=["x"])
    predicate = {"and": [left, {"or": [right, {"not": left}]}]}
    condition = gs.when(predicate).then("group:N").otherwise(gs.value("gray"))
    chart = (
        gs.Chart([{"x": 1, "group": "A"}])
        .mark_point()
        .encode(x="x:Q", color=condition)
        .add_params(left, right)
    )
    assert chart.to_dict()["encoding"]["color"] == {
        "value": "gray",
        "condition": {
            "test": {
                "and": [
                    {"param": "left", "empty": False},
                    {
                        "or": [
                            {"param": "right", "empty": True},
                            {"not": {"param": "left", "empty": False}},
                        ]
                    },
                ]
            },
            "field": "group",
            "type": "nominal",
        },
    }
    assert predicate["and"][0] is left


def test_projection_respects_explicit_empty_override_and_copies_input() -> None:
    brush = gs.selection_interval("brush", encodings=["x"], empty=False)
    predicate = {"param": brush, "project": {"x": "x2"}, "empty": True}
    condition = gs.when(predicate)
    predicate["project"]["x"] = "x"
    assert condition.then(gs.value(1)).to_dict()["condition"] == {
        "param": "brush",
        "empty": True,
        "project": {"x": "x2"},
        "value": 1,
    }


@pytest.mark.parametrize(
    "predicate",
    [
        {"ref": "highlight"},
        NamedSelectionPredicateRef(ref="highlight"),
    ],
)
def test_named_predicate_reference(predicate: object) -> None:
    condition = gs.when(predicate).then(gs.value(1)).otherwise(gs.value(0))
    spec = (
        gs.Chart([{"x": 1}])
        .mark_point()
        .encode(x="x:Q", order=condition)
        .add_params(gs.selection_point("hover"))
        .properties(predicates={"highlight": {"param": "hover"}})
        .to_dict()
    )
    assert spec["encoding"]["order"] == {
        "condition": {"test": {"ref": "highlight"}, "value": 1},
        "value": 0,
    }


def test_generated_predicate_and_selection_union() -> None:
    predicate = SelectionPredicateOperand(not_={"param": "brush"})
    assert gs.when(predicate).then(gs.value(1)).to_dict()["condition"]["test"] == {
        "not": {"param": "brush"},
    }
    union = {"param": {"or": ["left", "right"]}, "empty": False}
    assert gs.when(union).then(gs.value(1)).to_dict()["condition"]["test"] == union


@pytest.mark.parametrize(
    "predicate",
    [
        {"and": []},
        {"or": []},
        {"not": {"ref": "nested"}},
        {"param": "brush", "project": {"x": "y"}},
        {"ref": "named", "empty": False},
        {"expr": "datum.x > 0"},
    ],
)
def test_invalid_predicates_fail_before_encoding(predicate: dict) -> None:
    with pytest.raises(SchemaValidationError):
        gs.when(predicate)


def test_value_parameters_and_expressions_are_not_selection_predicates() -> None:
    for predicate in [gs.expr("datum.x > 0"), "brush", {"and": [gs.param(value=1)]}]:
        with pytest.raises(TypeError, match="selection parameter"):
            gs.when(predicate)


def test_public_generated_predicate_classes() -> None:
    from genome_spy import api, schema

    for name in (
        "NamedSelectionPredicateRef",
        "ParameterPredicate",
        "SelectionPredicateDefinition",
        "SelectionPredicateOperand",
        "SelectionUnionTest",
    ):
        assert getattr(gs, name) is getattr(schema, name)
        assert getattr(api, name) is getattr(schema, name)
        assert name in gs.__all__
        assert name in api.__all__


def test_generated_projection_setter_preserves_original_predicate() -> None:
    original = gs.ParameterPredicate(param="brush")
    projected = original.project(x="x2", y="y")
    assert original.to_dict() == {"param": "brush"}
    assert gs.when(projected).then(gs.value(1)).to_dict()["condition"] == {
        "param": "brush",
        "project": {"x": "x2", "y": "y"},
        "value": 1,
    }
    with pytest.raises(SchemaValidationError):
        gs.when(original.project(x="y"))
