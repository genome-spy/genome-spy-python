"""Python authoring primitives for GenomeSpy expressions.

The operator model follows Vega-Altair's expression API while keeping the
serialized value a real ``str`` subclass. As a result, generated schema
signatures that accept expression strings also accept ``Expression`` objects
without transform-specific adapters or normalization rules.

Portions are adapted from Vega-Altair's expression runtime:
https://github.com/vega/altair/blob/main/altair/expr/core.py
Copyright (c) 2015-2025, Vega-Altair Developers. BSD-3-Clause license; see
``LICENSES/ALTAIR-BSD-3-Clause.txt``.
"""

from __future__ import annotations

import sys
from typing import Any, Self, TypeAlias


def _js_repr(value: Any) -> str:
    """Return a JavaScript-safe expression representation."""
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    if isinstance(value, Expression):
        return str(value)
    numpy = sys.modules.get("numpy")
    if numpy is not None and isinstance(value, numpy.generic):
        return repr(value.item())
    return repr(value)


def _function_expression(name: str, *arguments: Any) -> Expression:
    """Build a function-call expression."""
    rendered = ",".join(_js_repr(argument) for argument in arguments)
    return Expression(f"{name}({rendered})")


class Expression(str):
    """A composable GenomeSpy expression string.

    Python operators build the JavaScript-like expression syntax understood by
    GenomeSpy. The class remains a string for direct compatibility with every
    generated schema property whose upstream type is ``string``.

    Args:
        value: Serialized expression source.

    Returns:
        A composable expression value.

    Raises:
        TypeError: If Python evaluates an expression as a boolean.

    Example:
        >>> from genome_spy import datum
        >>> str((datum.score >= 10) & (datum.kind == "PASS"))
        "((datum.score >= 10) && (datum.kind === 'PASS'))"
    """

    __hash__ = None  # type: ignore[assignment]

    def __repr__(self) -> str:
        return str(self)

    def __bool__(self) -> bool:
        raise TypeError(
            "GenomeSpy expressions cannot be converted to bool; use &, |, and ~ "
            "instead of Python's and, or, and not."
        )

    def __getattr__(self, name: str) -> Expression:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return Expression(f"{self}.{name}")

    def __getitem__(self, key: Any) -> Expression:
        return Expression(f"{self}[{_js_repr(key)}]")

    def _binary(self, operator: str, other: Any) -> Expression:
        return Expression(f"({self} {operator} {_js_repr(other)})")

    def _reverse_binary(self, operator: str, other: Any) -> Expression:
        return Expression(f"({_js_repr(other)} {operator} {self})")

    def __add__(self, other: Any) -> Expression:
        return self._binary("+", other)

    def __radd__(self, other: Any) -> Expression:
        return self._reverse_binary("+", other)

    def __sub__(self, other: Any) -> Expression:
        return self._binary("-", other)

    def __rsub__(self, other: Any) -> Expression:
        return self._reverse_binary("-", other)

    def __mul__(self, other: Any) -> Expression:
        return self._binary("*", other)

    def __rmul__(self, other: Any) -> Expression:
        return self._reverse_binary("*", other)

    def __truediv__(self, other: Any) -> Expression:
        return self._binary("/", other)

    def __rtruediv__(self, other: Any) -> Expression:
        return self._reverse_binary("/", other)

    def __mod__(self, other: Any) -> Expression:
        return self._binary("%", other)

    def __rmod__(self, other: Any) -> Expression:
        return self._reverse_binary("%", other)

    def __pow__(self, other: Any) -> Expression:
        return _function_expression("pow", self, other)

    def __rpow__(self, other: Any) -> Expression:
        return _function_expression("pow", other, self)

    def __neg__(self) -> Expression:
        return Expression(f"(-{self})")

    def __pos__(self) -> Expression:
        return Expression(f"(+{self})")

    def __eq__(self, other: object) -> Expression:  # type: ignore[override]
        return self._binary("===", other)

    def __ne__(self, other: object) -> Expression:  # type: ignore[override]
        return self._binary("!==", other)

    def __lt__(self, other: Any) -> Expression:  # type: ignore[override]
        return self._binary("<", other)

    def __le__(self, other: Any) -> Expression:  # type: ignore[override]
        return self._binary("<=", other)

    def __gt__(self, other: Any) -> Expression:  # type: ignore[override]
        return self._binary(">", other)

    def __ge__(self, other: Any) -> Expression:  # type: ignore[override]
        return self._binary(">=", other)

    def __and__(self, other: Any) -> Expression:
        return self._binary("&&", other)

    def __rand__(self, other: Any) -> Expression:
        return self._reverse_binary("&&", other)

    def __or__(self, other: Any) -> Expression:
        return self._binary("||", other)

    def __ror__(self, other: Any) -> Expression:
        return self._reverse_binary("||", other)

    def __invert__(self) -> Expression:
        return Expression(f"(!{self})")

    def __abs__(self) -> Expression:
        return _function_expression("abs", self)

    def copy(self) -> Self:
        """Return an equivalent expression value.

        Returns:
            A new expression with the same serialized source.

        Raises:
            No exceptions are raised.

        Example:
            >>> from genome_spy import datum
            >>> str(datum.x.copy())
            'datum.x'
        """
        return type(self)(self)

    def to_dict(self) -> str:
        """Return the schema-compatible expression string.

        Returns:
            The serialized expression source.

        Raises:
            No exceptions are raised.

        Example:
            >>> from genome_spy import datum
            >>> datum.x.to_dict()
            'datum.x'
        """
        return str(self)


class DatumExpression:
    """Expression-field behavior mixed into the generated datum helper."""

    def __repr__(self) -> str:
        return "datum"

    def __getattr__(self, name: str) -> Expression:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return Expression(f"datum.{name}")

    def __getitem__(self, key: Any) -> Expression:
        return Expression(f"datum[{_js_repr(key)}]")


IntoExpression: TypeAlias = (
    str
    | int
    | float
    | bool
    | None
    | Expression
    | list[Any]
    | tuple[Any, ...]
    | dict[str, Any]
)


__all__ = ["DatumExpression", "Expression", "IntoExpression"]
