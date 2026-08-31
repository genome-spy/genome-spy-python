"""Generated from GenomeSpy expression-runtime documentation. Do not edit."""

from __future__ import annotations

from typing import TYPE_CHECKING

from genome_spy._expressions import Expression, _function_expression
from genome_spy.schema import core
from genome_spy.schemapi import Undefined, UndefinedType

if TYPE_CHECKING:
    from genome_spy._expressions import IntoExpression


class _ExprMeta(type):
    """Provide read-only GenomeSpy expression constants."""

    @property
    def NaN(cls) -> Expression:
        """Return the GenomeSpy ``NaN`` constant."""
        return Expression("NaN")

    @property
    def E(cls) -> Expression:
        """Return the GenomeSpy ``E`` constant."""
        return Expression("E")

    @property
    def LN2(cls) -> Expression:
        """Return the GenomeSpy ``LN2`` constant."""
        return Expression("LN2")

    @property
    def LN10(cls) -> Expression:
        """Return the GenomeSpy ``LN10`` constant."""
        return Expression("LN10")

    @property
    def LOG2E(cls) -> Expression:
        """Return the GenomeSpy ``LOG2E`` constant."""
        return Expression("LOG2E")

    @property
    def LOG10E(cls) -> Expression:
        """Return the GenomeSpy ``LOG10E`` constant."""
        return Expression("LOG10E")

    @property
    def PI(cls) -> Expression:
        """Return the GenomeSpy ``PI`` constant."""
        return Expression("PI")

    @property
    def SQRT1_2(cls) -> Expression:
        """Return the GenomeSpy ``SQRT1_2`` constant."""
        return Expression("SQRT1_2")

    @property
    def SQRT2(cls) -> Expression:
        """Return the GenomeSpy ``SQRT2`` constant."""
        return Expression("SQRT2")

    @property
    def MIN_VALUE(cls) -> Expression:
        """Return the GenomeSpy ``MIN_VALUE`` constant."""
        return Expression("MIN_VALUE")

    @property
    def MAX_VALUE(cls) -> Expression:
        """Return the GenomeSpy ``MAX_VALUE`` constant."""
        return Expression("MAX_VALUE")


class expr(core.ExprRef, metaclass=_ExprMeta):
    """Build expression references, constants, and function calls."""

    def __new__(cls, expression: str | Expression) -> core.ExprRef:  # type: ignore[misc]
        return core.ExprRef(expr=str(expression))

    @classmethod
    def abs(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``abs`` expression."""
        return _function_expression("abs", value)

    @classmethod
    def cos(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``cos`` expression."""
        return _function_expression("cos", value)

    @classmethod
    def domain(cls, channel: IntoExpression) -> Expression:
        """Build a GenomeSpy ``domain`` expression."""
        return _function_expression("domain", channel)

    @classmethod
    def if_(
        cls,
        test: IntoExpression,
        then_value: IntoExpression,
        else_value: IntoExpression,
    ) -> Expression:
        """Build a GenomeSpy ``if`` expression."""
        return _function_expression("if", test, then_value, else_value)

    @classmethod
    def isValid(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``isValid`` expression."""
        return _function_expression("isValid", value)

    @classmethod
    def regexp(
        cls, pattern: IntoExpression, flags: IntoExpression | UndefinedType = Undefined
    ) -> Expression:
        """Build a GenomeSpy ``regexp`` expression."""
        if flags is Undefined:
            return _function_expression("regexp", pattern)
        return _function_expression("regexp", pattern, flags)

    @classmethod
    def replace(
        cls,
        string: IntoExpression,
        pattern: IntoExpression,
        replacement: IntoExpression,
    ) -> Expression:
        """Build a GenomeSpy ``replace`` expression."""
        return _function_expression("replace", string, pattern, replacement)

    @classmethod
    def round(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``round`` expression."""
        return _function_expression("round", value)

    @classmethod
    def scale(cls, channel: IntoExpression, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``scale`` expression."""
        return _function_expression("scale", channel, value)

    @classmethod
    def sin(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``sin`` expression."""
        return _function_expression("sin", value)

    @classmethod
    def slice(
        cls, value: IntoExpression, start: IntoExpression, end: IntoExpression
    ) -> Expression:
        """Build a GenomeSpy ``slice`` expression."""
        return _function_expression("slice", value, start, end)

    @classmethod
    def span(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``span`` expression."""
        return _function_expression("span", value)

    @classmethod
    def test(cls, regexp: IntoExpression, string: IntoExpression) -> Expression:
        """Build a GenomeSpy ``test`` expression."""
        return _function_expression("test", regexp, string)

    @classmethod
    def upper(cls, string: IntoExpression) -> Expression:
        """Build a GenomeSpy ``upper`` expression."""
        return _function_expression("upper", string)


__all__ = ["Expression", "expr"]
