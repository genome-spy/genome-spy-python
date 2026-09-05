"""Altair-style conditional encoding authoring."""

from __future__ import annotations

from typing import TypeAlias

from genome_spy._parameters import Parameter
from genome_spy.channels import Channel, channel
from genome_spy.schemapi import SchemaBase

ConditionValue: TypeAlias = Channel | SchemaBase | str | dict[str, object]


def _branch_definition(value: ConditionValue) -> dict[str, object]:
    return channel(value).to_dict()


class _Then(Channel):
    """A conditional channel awaiting an optional fallback branch."""

    def otherwise(self, value: ConditionValue) -> Channel:
        """Return the conditional channel with its fallback branch."""
        return Channel({**_branch_definition(value), **self.to_dict()})


class _When:
    """A validated parameter predicate awaiting its true branch."""

    def __init__(self, predicate: Parameter) -> None:
        self._predicate = predicate

    def then(self, value: ConditionValue) -> _Then:
        """Return a conditional channel using ``value`` when selected."""
        condition = {
            "param": self._predicate.name,
            "empty": self._predicate.empty,
            **_branch_definition(value),
        }
        return _Then({"condition": condition})


def when(predicate: Parameter) -> _When:
    """Start an Altair-style selection condition.

    GenomeSpy 0.86 supports selection parameters as conditional predicates.
    Expression predicates will become available only if the upstream schema
    adds that grammar.

    Args:
        predicate: A point or interval selection parameter.

    Returns:
        A builder whose ``then()`` method defines the selected branch.

    Raises:
        TypeError: If ``predicate`` is not a selection parameter.

    Example:
        >>> import genome_spy as gs
        >>> brush = gs.selection_interval(encodings=["x"])
        >>> condition = gs.when(brush).then(gs.value("red")).otherwise(
        ...     gs.value("gray")
        ... )
        >>> condition.to_dict()["condition"]["param"] == brush.name
        True
    """
    if not isinstance(predicate, Parameter) or not predicate.is_selection:
        raise TypeError("when() currently requires a selection parameter.")
    return _When(predicate)


__all__ = ["when"]
