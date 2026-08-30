"""Pure normalization helpers for handwritten transform compatibility."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from typing import Any, cast

from genome_spy.schema import AggregateOp_T, WindowOp_T

_AGGREGATE_OPERATIONS = {
    "count",
    "valid",
    "sum",
    "min",
    "max",
    "mean",
    "q1",
    "median",
    "q3",
    "variance",
}
_WINDOW_ONLY_OPERATIONS = {
    "row_number",
    "rank",
    "dense_rank",
    "percent_rank",
    "cume_dist",
    "ntile",
    "lag",
    "lead",
    "first_value",
    "last_value",
    "nth_value",
    "prev_value",
    "next_value",
}
_FIELDLESS_WINDOW_OPERATIONS = {
    "count",
    "row_number",
    "rank",
    "dense_rank",
    "percent_rank",
    "cume_dist",
    "ntile",
}
_PARAMETER_REQUIRED_WINDOW_OPERATIONS = {"ntile", "nth_value"}
_OPERATION_ALIASES = {"average": "mean"}
_OPERATION_SHORTHAND = re.compile(
    r"^\s*(?P<operation>[A-Za-z_][A-Za-z0-9_]*)\s*"
    r"\(\s*(?P<field>[^()]*)\s*\)\s*$"
)
_IDENTIFIER = re.compile(r"^[A-Za-z_$][A-Za-z0-9_$]*$")

_ConstraintValue = str | int | float | bool | None


def _parse_aggregate_shorthand(value: str) -> tuple[AggregateOp_T, str]:
    match = _OPERATION_SHORTHAND.fullmatch(value)
    if match is None:
        raise ValueError(
            f"Invalid aggregate shorthand {value!r}; expected 'operation(field)'."
        )

    operation = _OPERATION_ALIASES.get(
        match.group("operation"), match.group("operation")
    )
    if operation not in _AGGREGATE_OPERATIONS:
        raise ValueError(f"Unsupported GenomeSpy aggregate operation {operation!r}.")

    field = match.group("field").strip()
    if not field:
        raise ValueError("Fieldless aggregate shorthand is not supported.")
    return cast(AggregateOp_T, operation), field


def _normalize_aggregate_definition(
    definition: Mapping[str, Any],
) -> tuple[AggregateOp_T, str, str]:
    extra = set(definition) - {"op", "field", "as"}
    if extra:
        names = ", ".join(sorted(extra))
        raise ValueError(f"Unsupported aggregate definition properties: {names}.")

    missing = {"op", "field", "as"} - set(definition)
    if missing:
        names = ", ".join(sorted(missing))
        raise ValueError(f"Aggregate definition is missing: {names}.")

    operation = definition["op"]
    field = definition["field"]
    output = definition["as"]
    if not all(isinstance(value, str) for value in (operation, field, output)):
        raise TypeError("Aggregate definition 'op', 'field', and 'as' must be strings.")

    normalized_operation = _OPERATION_ALIASES.get(operation, operation)
    if normalized_operation not in _AGGREGATE_OPERATIONS:
        raise ValueError(
            f"Unsupported GenomeSpy aggregate operation {normalized_operation!r}."
        )
    if not field:
        raise ValueError("Fieldless aggregate definitions are not supported.")

    return cast(AggregateOp_T, normalized_operation), field, output


def _constraint_expression(field: str, value: _ConstraintValue) -> str:
    if not isinstance(value, (str, int, float, bool)) and value is not None:
        raise TypeError(
            f"Filter constraint {field!r} must be a string, number, boolean, or None."
        )

    try:
        literal = json.dumps(value, allow_nan=False, separators=(",", ":"))
    except ValueError as error:
        raise ValueError(f"Filter constraint {field!r} must be finite.") from error

    reference = (
        f"datum.{field}"
        if _IDENTIFIER.fullmatch(field)
        else f"datum[{json.dumps(field)}]"
    )
    return f"{reference} === {literal}"


def _normalize_sort_definitions(
    definitions: Sequence[Mapping[str, Any]],
) -> dict[str, list[str]]:
    if not definitions:
        raise ValueError("Sort definitions must not be empty.")

    fields: list[str] = []
    orders: list[str] = []
    for definition in definitions:
        extra = set(definition) - {"field", "order"}
        if extra:
            names = ", ".join(sorted(extra))
            raise ValueError(f"Unsupported sort definition properties: {names}.")

        field = definition.get("field")
        order = definition.get("order", "ascending")
        if not isinstance(field, str):
            raise TypeError("Sort definition 'field' must be a string.")
        if order not in {"ascending", "descending"}:
            raise ValueError("Sort definition 'order' must be ascending or descending.")
        fields.append(field)
        orders.append(cast(str, order))

    return {"field": fields, "order": orders}


def _normalize_window_operation(
    operation: object,
    field: object,
    param: object,
) -> tuple[WindowOp_T, str | None, float | None]:
    if not isinstance(operation, str):
        raise TypeError("Window definition 'op' must be a string.")

    normalized_operation = _OPERATION_ALIASES.get(operation, operation)
    supported = _AGGREGATE_OPERATIONS | _WINDOW_ONLY_OPERATIONS
    if normalized_operation not in supported:
        raise ValueError(
            f"Unsupported GenomeSpy window operation {normalized_operation!r}."
        )

    allows_no_field = normalized_operation in _FIELDLESS_WINDOW_OPERATIONS
    if field is None:
        if not allows_no_field:
            raise ValueError(
                f"Window operation {normalized_operation!r} requires a field."
            )
    elif not isinstance(field, str):
        raise TypeError("Window definition 'field' must be a string or None.")
    elif allows_no_field:
        raise ValueError(
            f"Window operation {normalized_operation!r} does not accept a field."
        )

    if param is None:
        if normalized_operation in _PARAMETER_REQUIRED_WINDOW_OPERATIONS:
            raise ValueError(
                f"Window operation {normalized_operation!r} requires a parameter."
            )
    elif isinstance(param, bool) or not isinstance(param, (int, float)):
        raise TypeError("Window definition 'param' must be a number or None.")

    return (
        cast(WindowOp_T, normalized_operation),
        field,
        cast(float | None, param),
    )


def _normalize_window_definition(
    definition: Mapping[str, Any],
) -> tuple[WindowOp_T, str | None, float | None, str]:
    extra = set(definition) - {"op", "field", "param", "as"}
    if extra:
        names = ", ".join(sorted(extra))
        raise ValueError(f"Unsupported window definition properties: {names}.")

    missing = {"op", "as"} - set(definition)
    if missing:
        names = ", ".join(sorted(missing))
        raise ValueError(f"Window definition is missing: {names}.")

    output = definition["as"]
    if not isinstance(output, str):
        raise TypeError("Window definition 'as' must be a string.")

    operation, field, param = _normalize_window_operation(
        definition["op"],
        definition.get("field"),
        definition.get("param"),
    )
    return operation, field, param, output


def _parse_window_shorthand(value: str) -> tuple[WindowOp_T, str | None, None]:
    match = _OPERATION_SHORTHAND.fullmatch(value)
    if match is None:
        raise ValueError(
            f"Invalid window shorthand {value!r}; expected 'operation(field)'."
        )

    field = match.group("field").strip() or None
    operation, normalized_field, _ = _normalize_window_operation(
        match.group("operation"), field, None
    )
    return operation, normalized_field, None


__all__ = [
    "_ConstraintValue",
    "_constraint_expression",
    "_normalize_aggregate_definition",
    "_normalize_sort_definitions",
    "_normalize_window_definition",
    "_parse_aggregate_shorthand",
    "_parse_window_shorthand",
]
