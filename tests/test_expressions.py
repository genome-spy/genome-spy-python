"""Tests for Python-authored GenomeSpy expressions."""

from __future__ import annotations

import inspect

import pytest

import genome_spy as gs
from genome_spy.schema import ergonomics as generated_ergonomics
from genome_spy.schema.expressions import expr as generated_expr


def test_datum_builds_python_expression_with_altair_operators() -> None:
    expression = (gs.datum.score >= 10) & (gs.datum.kind == "PASS")

    assert str(expression) == "((datum.score >= 10) && (datum.kind === 'PASS'))"


def test_datum_supports_nested_and_special_field_access() -> None:
    expression = gs.datum.INFO.SVTYPE[0] == gs.datum["mate.chrom"]

    assert str(expression) == "(datum.INFO.SVTYPE[0] === datum['mate.chrom'])"


def test_datum_remains_generated_constant_channel_helper() -> None:
    assert gs.datum is generated_ergonomics.datum
    assert {"axis", "condition", "scale", "type"} <= set(
        inspect.signature(gs.datum).parameters
    )
    assert gs.datum(0, type="quantitative").to_dict() == {
        "datum": 0,
        "type": "quantitative",
    }


def test_generated_expr_namespace_builds_functions_and_conditionals() -> None:
    expression = gs.expr.if_(
        gs.datum.n_minor == 0,
        "LOH",
        gs.expr.upper(gs.datum.status),
    )

    assert gs.expr is generated_expr
    assert str(expression) == ("if((datum.n_minor === 0),'LOH',upper(datum.status))")


def test_expr_call_still_builds_expression_reference() -> None:
    assert gs.expr(gs.datum.amount * 2).to_dict() == {"expr": "(datum.amount * 2)"}


def test_generated_transforms_accept_and_normalize_expressions() -> None:
    spec = (
        gs.Chart([{"x": 1}])
        .transform_calculate(y=2 * gs.expr.sin(gs.datum.x))
        .transform_filter(gs.datum.x > 0)
        .mark_point()
        .encode(x="x:Q", y="y:Q")
        .to_dict()
    )

    assert spec["transform"] == [
        {"type": "formula", "as": "y", "expr": "(2 * sin(datum.x))"},
        {"type": "filter", "expr": "(datum.x > 0)"},
    ]
    assert all(
        type(transform["expr"]) is str  # noqa: E721
        for transform in spec["transform"]
    )


def test_python_boolean_operators_fail_with_actionable_message() -> None:
    with pytest.raises(TypeError, match="use &, \\|, and ~"):
        bool(gs.datum.x > 0)
