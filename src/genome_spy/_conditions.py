"""Altair-style conditional encoding authoring."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeAlias

from genome_spy._parameters import Parameter
from genome_spy.channels import Channel, channel
from genome_spy.schemapi import SchemaBase
from genome_spy.schema.core import (
    NamedSelectionPredicateRef,
    ParameterPredicate,
    SelectionPredicateDefinition,
    SelectionPredicateOperand,
    SelectionUnionTest,
)

ConditionValue: TypeAlias = Channel | SchemaBase | str | dict[str, object]
SelectionTest: TypeAlias = (
    Parameter
    | ParameterPredicate
    | SelectionPredicateDefinition
    | SelectionPredicateOperand
    | SelectionUnionTest
    | NamedSelectionPredicateRef
    | Mapping[str, Any]
)


def _selection_test(value: Any) -> Any:
    """Copy predicate containers and normalize selection handles at their leaves."""
    if isinstance(value, Parameter):
        if not value.is_selection:
            raise TypeError(
                "when() requires selection parameters, not value parameters."
            )
        return {"param": value.name, "empty": value.empty}
    if isinstance(value, SchemaBase):
        return value.to_dict()
    if isinstance(value, Mapping):
        result = {key: _selection_test(item) for key, item in value.items()}
        if isinstance(value.get("param"), Parameter):
            parameter = result.pop("param")
            result = {**parameter, **result}
        return result
    if isinstance(value, (list, tuple)):
        return [_selection_test(item) for item in value]
    return value


def _branch_definition(value: ConditionValue) -> dict[str, object]:
    return channel(value).to_dict()


class _Then(Channel):
    """A conditional channel awaiting an optional fallback branch."""

    def otherwise(self, value: ConditionValue) -> Channel:
        """Return the conditional channel with its fallback branch."""
        return Channel({**_branch_definition(value), **self.to_dict()})


class _When:
    """A validated parameter predicate awaiting its true branch."""

    def __init__(self, predicate: dict[str, Any]) -> None:
        self._predicate = predicate

    def then(self, value: ConditionValue) -> _Then:
        """Return a conditional channel using ``value`` when selected."""
        condition = {
            **self._predicate,
            **_branch_definition(value),
        }
        return _Then({"condition": condition})


def when(predicate: SelectionTest) -> _When:
    """Start an Altair-style selection condition.

    Accept a selection handle, a generated selection predicate, or a mapping
    using GenomeSpy's ``and``, ``or``, ``not``, selection-union, or named ``ref``
    grammar. Selection handles can appear inside mappings, including as the
    ``param`` of an endpoint projection. Declare selections with ``add_params``
    and named predicates with the unit view's ``predicates`` property.

    Args:
        predicate: A selection parameter or a composed selection test.

    Returns:
        A builder whose ``then()`` method defines the selected branch.

    Raises:
        TypeError: If a value parameter or unsupported input is supplied.
        SchemaValidationError: If the predicate does not match the Core grammar.

    Example:
        >>> import genome_spy as gs
        >>> brush = gs.selection_interval(encodings=["x"])
        >>> condition = gs.when(brush).then(gs.value("red")).otherwise(
        ...     gs.value("gray")
        ... )
        >>> condition.to_dict()["condition"]["param"] == brush.name
        True
    """
    if not isinstance(
        predicate,
        (
            Parameter,
            ParameterPredicate,
            SelectionPredicateDefinition,
            SelectionPredicateOperand,
            SelectionUnionTest,
            NamedSelectionPredicateRef,
            Mapping,
        ),
    ):
        raise TypeError("when() requires a selection parameter or predicate mapping.")
    test = _selection_test(predicate)
    if "ref" in test:
        validated = NamedSelectionPredicateRef(**test).to_dict()
    else:
        validated = SelectionPredicateDefinition(**test).to_dict()
    # Preserve the original compact condition format for single selections.
    return _When(
        validated if isinstance(validated.get("param"), str) else {"test": validated}
    )


__all__ = ["when"]
