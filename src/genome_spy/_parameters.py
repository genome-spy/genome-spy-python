"""Altair-style authoring handles for GenomeSpy parameters."""

from __future__ import annotations

import hashlib
import json
from typing import Any, cast

from genome_spy._expressions import (
    Expression,
    ExpressionOperand,
    ExpressionOperatorMixin,
)
from genome_spy.schema import core
from genome_spy.schemapi import (
    SchemaBase,
    Undefined,
    normalize_schema_value,
)


class Parameter(ExpressionOperatorMixin, core.ExprRef):
    """Represent a declared GenomeSpy parameter in Python expressions.

    A parameter handle keeps its generated declaration in :attr:`param` and
    supplies the parameter name when used in an expression. Attach handles to
    charts with :meth:`genome_spy.TopLevelSpec.add_params`.

    Args:
        param: Exact generated GenomeSpy parameter declaration.
        empty: Whether an empty selection matches when consumed as a predicate.

    Returns:
        A reusable parameter authoring handle.

    Raises:
        TypeError: If the declaration has no string name.

    Example:
        >>> threshold = param("threshold", value=0.5)
        >>> str(threshold * 2)
        '(threshold * 2)'
    """

    def __init__(
        self,
        param: SchemaBase,
        *,
        empty: bool = True,
        _is_selection: bool = False,
        _name_is_explicit: bool = True,
    ) -> None:
        values = param.to_dict(validate=False)
        name = values.get("name")
        if not isinstance(name, str):
            raise TypeError("A parameter declaration must have a string name.")
        self.param = param
        self.empty = empty
        self._name_is_explicit = _name_is_explicit
        self._is_selection = _is_selection
        core.ExprRef.__init__(self, expr=name)

    @property
    def name(self) -> str:
        """Return the declared GenomeSpy parameter name."""
        return cast(str, self._kwds["expr"])

    @property
    def is_selection(self) -> bool:
        """Return whether this handle represents a selection parameter."""
        return self._is_selection

    @property
    def name_is_explicit(self) -> bool:
        """Return whether the parameter name was supplied by the user."""
        return self._name_is_explicit

    def _to_expr(self) -> Expression:
        if self.is_selection:
            raise TypeError("Selection parameters cannot be used as expressions.")
        return Expression(self.name)

    def to_dict(self, *, validate: bool = True) -> dict[str, Any]:
        """Return an expression reference for expression-capable parameters.

        Args:
            validate: Validate the expression reference against its schema.

        Returns:
            A GenomeSpy expression-reference mapping.

        Raises:
            TypeError: If this is a selection parameter, which requires an
                explicit condition or filter context.

        Example:
            >>> param("opacity", value=0.5).to_dict()
            {'expr': 'opacity'}
        """
        if self.is_selection:
            raise TypeError(
                "Selection parameters require a condition or filter context; "
                "attach declarations with chart.add_params(selection)."
            )
        return core.ExprRef(expr=self.name).to_dict(validate=validate)


def _stable_parameter_name(properties: dict[str, Any]) -> str:
    normalized = normalize_schema_value(properties, validate=False)
    payload = json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:10]
    return f"param_{digest}"


def _expression_string(value: str | ExpressionOperand) -> str:
    if isinstance(value, ExpressionOperand):
        return str(value._to_expr())
    return value


def _defined_properties(properties: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in properties.items() if value is not Undefined}


def _select_parameter_class(
    properties: dict[str, Any],
    variants: tuple[type[SchemaBase], ...],
) -> type[SchemaBase]:
    supplied = set(properties)
    matches: list[type[SchemaBase]] = []
    for variant in variants:
        schema = variant.resolve_references()
        allowed = set(schema.get("properties", {}))
        required = set(schema.get("required", ()))
        if required <= supplied <= allowed:
            matches.append(variant)
    if len(matches) != 1:
        names = ", ".join(sorted(supplied)) or "no arguments"
        if not matches:
            raise TypeError(f"No GenomeSpy parameter variant accepts: {names}.")
        choices = ", ".join(variant.__name__ for variant in matches)
        raise TypeError(
            f"Ambiguous GenomeSpy parameter arguments ({names}): {choices}."
        )
    return matches[0]


def _make_parameter(
    name: str | None = None,
    /,
    *,
    _variants: tuple[type[SchemaBase], ...],
    _selection_variants: tuple[type[SchemaBase], ...] = (),
    empty: bool = True,
    **properties: Any,
) -> Parameter:
    """Create a reusable GenomeSpy parameter handle.

    The supplied properties are matched against the concrete parameter leaves
    in GenomeSpy's generated schema. The resulting declaration is available as
    ``handle.param`` and is attached to charts with ``add_params()``.

    Args:
        name: Parameter name. A deterministic name is generated when omitted.
        bind: Optional input binding for a value parameter.
        description: Human-readable parameter description.
        expr: Reactive expression for an expression parameter.
        persist: Whether GenomeSpy App should persist the parameter.
        push: Reuse and update an ancestor parameter with the same name.
        ruler: Ruler configuration.
        select: Point or interval selection configuration.
        transition: Numeric interpolation configuration.
        value: Initial parameter value.
        empty: Whether an empty selection matches in conditions and filters.

    Returns:
        A reusable parameter handle containing the exact generated declaration.

    Raises:
        TypeError: If the supplied properties match no unique parameter branch.

    Example:
        >>> cutoff = param("cutoff", value=0.5)
        >>> cutoff.param.to_dict()
        {'name': 'cutoff', 'value': 0.5}
    """
    properties = _defined_properties(properties)
    if "expr" in properties:
        properties["expr"] = _expression_string(properties["expr"])
    name_is_explicit = name is not None
    properties["name"] = name or _stable_parameter_name(properties)
    parameter_class = _select_parameter_class(properties, _variants)
    definition = parameter_class(**properties)
    return Parameter(
        definition,
        empty=empty,
        _is_selection=parameter_class in _selection_variants,
        _name_is_explicit=name_is_explicit,
    )


def _unwrap_parameter(value: Parameter | SchemaBase) -> SchemaBase:
    return value.param if isinstance(value, Parameter) else value


__all__ = ["Parameter"]
