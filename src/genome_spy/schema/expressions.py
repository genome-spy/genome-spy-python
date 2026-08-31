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
    def if_(
        cls,
        test: IntoExpression,
        then_value: IntoExpression,
        else_value: IntoExpression,
    ) -> Expression:
        """Build a GenomeSpy ``if`` expression."""
        return _function_expression("if", test, then_value, else_value)

    @classmethod
    def isArray(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``isArray`` expression."""
        return _function_expression("isArray", value)

    @classmethod
    def isBoolean(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``isBoolean`` expression."""
        return _function_expression("isBoolean", value)

    @classmethod
    def isNumber(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``isNumber`` expression."""
        return _function_expression("isNumber", value)

    @classmethod
    def isObject(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``isObject`` expression."""
        return _function_expression("isObject", value)

    @classmethod
    def isRegExp(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``isRegExp`` expression."""
        return _function_expression("isRegExp", value)

    @classmethod
    def isString(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``isString`` expression."""
        return _function_expression("isString", value)

    @classmethod
    def isDefined(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``isDefined`` expression."""
        return _function_expression("isDefined", value)

    @classmethod
    def isValid(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``isValid`` expression."""
        return _function_expression("isValid", value)

    @classmethod
    def isNaN(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``isNaN`` expression."""
        return _function_expression("isNaN", value)

    @classmethod
    def isFinite(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``isFinite`` expression."""
        return _function_expression("isFinite", value)

    @classmethod
    def abs(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``abs`` expression."""
        return _function_expression("abs", value)

    @classmethod
    def acos(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``acos`` expression."""
        return _function_expression("acos", value)

    @classmethod
    def asin(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``asin`` expression."""
        return _function_expression("asin", value)

    @classmethod
    def atan(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``atan`` expression."""
        return _function_expression("atan", value)

    @classmethod
    def atan2(cls, dy: IntoExpression, dx: IntoExpression) -> Expression:
        """Build a GenomeSpy ``atan2`` expression."""
        return _function_expression("atan2", dy, dx)

    @classmethod
    def ceil(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``ceil`` expression."""
        return _function_expression("ceil", value)

    @classmethod
    def cos(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``cos`` expression."""
        return _function_expression("cos", value)

    @classmethod
    def exp(cls, exponent: IntoExpression) -> Expression:
        """Build a GenomeSpy ``exp`` expression."""
        return _function_expression("exp", exponent)

    @classmethod
    def floor(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``floor`` expression."""
        return _function_expression("floor", value)

    @classmethod
    def hypot(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``hypot`` expression."""
        return _function_expression("hypot", value)

    @classmethod
    def log(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``log`` expression."""
        return _function_expression("log", value)

    @classmethod
    def max(
        cls, value1: IntoExpression, value2: IntoExpression, *values: IntoExpression
    ) -> Expression:
        """Build a GenomeSpy ``max`` expression."""
        return _function_expression("max", value1, value2, *values)

    @classmethod
    def min(
        cls, value1: IntoExpression, value2: IntoExpression, *values: IntoExpression
    ) -> Expression:
        """Build a GenomeSpy ``min`` expression."""
        return _function_expression("min", value1, value2, *values)

    @classmethod
    def pow(cls, value: IntoExpression, exponent: IntoExpression) -> Expression:
        """Build a GenomeSpy ``pow`` expression."""
        return _function_expression("pow", value, exponent)

    @classmethod
    def random(cls) -> Expression:
        """Build a GenomeSpy ``random`` expression."""
        return _function_expression("random")

    @classmethod
    def round(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``round`` expression."""
        return _function_expression("round", value)

    @classmethod
    def sin(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``sin`` expression."""
        return _function_expression("sin", value)

    @classmethod
    def sqrt(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``sqrt`` expression."""
        return _function_expression("sqrt", value)

    @classmethod
    def tan(cls, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``tan`` expression."""
        return _function_expression("tan", value)

    @classmethod
    def clamp(
        cls, value: IntoExpression, min: IntoExpression, max: IntoExpression
    ) -> Expression:
        """Build a GenomeSpy ``clamp`` expression."""
        return _function_expression("clamp", value, min, max)

    @classmethod
    def length(cls, array: IntoExpression) -> Expression:
        """Build a GenomeSpy ``length`` expression."""
        return _function_expression("length", array)

    @classmethod
    def join(
        cls,
        array: IntoExpression,
        separator: IntoExpression | UndefinedType = Undefined,
    ) -> Expression:
        """Build a GenomeSpy ``join`` expression."""
        arguments = [array, separator]
        while arguments and arguments[-1] is Undefined:
            arguments.pop()
        if any(argument is Undefined for argument in arguments):
            raise ValueError("join optional arguments cannot contain gaps")
        return _function_expression("join", *arguments)

    @classmethod
    def indexof(cls, array: IntoExpression, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``indexof`` expression."""
        return _function_expression("indexof", array, value)

    @classmethod
    def lastindexof(cls, array: IntoExpression, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``lastindexof`` expression."""
        return _function_expression("lastindexof", array, value)

    @classmethod
    def reverse(cls, array: IntoExpression) -> Expression:
        """Build a GenomeSpy ``reverse`` expression."""
        return _function_expression("reverse", array)

    @classmethod
    def slice(
        cls,
        array: IntoExpression,
        start: IntoExpression,
        end: IntoExpression | UndefinedType = Undefined,
    ) -> Expression:
        """Build a GenomeSpy ``slice`` expression."""
        arguments = [array, start, end]
        while arguments and arguments[-1] is Undefined:
            arguments.pop()
        if any(argument is Undefined for argument in arguments):
            raise ValueError("slice optional arguments cannot contain gaps")
        return _function_expression("slice", *arguments)

    @classmethod
    def sort(cls, array: IntoExpression) -> Expression:
        """Build a GenomeSpy ``sort`` expression."""
        return _function_expression("sort", array)

    @classmethod
    def span(cls, array: IntoExpression) -> Expression:
        """Build a GenomeSpy ``span`` expression."""
        return _function_expression("span", array)

    @classmethod
    def parseFloat(cls, string: IntoExpression) -> Expression:
        """Build a GenomeSpy ``parseFloat`` expression."""
        return _function_expression("parseFloat", string)

    @classmethod
    def parseInt(cls, string: IntoExpression) -> Expression:
        """Build a GenomeSpy ``parseInt`` expression."""
        return _function_expression("parseInt", string)

    @classmethod
    def upper(cls, string: IntoExpression) -> Expression:
        """Build a GenomeSpy ``upper`` expression."""
        return _function_expression("upper", string)

    @classmethod
    def lower(cls, string: IntoExpression) -> Expression:
        """Build a GenomeSpy ``lower`` expression."""
        return _function_expression("lower", string)

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
    def split(
        cls,
        string: IntoExpression,
        separator: IntoExpression,
        limit: IntoExpression | UndefinedType = Undefined,
    ) -> Expression:
        """Build a GenomeSpy ``split`` expression."""
        arguments = [string, separator, limit]
        while arguments and arguments[-1] is Undefined:
            arguments.pop()
        if any(argument is Undefined for argument in arguments):
            raise ValueError("split optional arguments cannot contain gaps")
        return _function_expression("split", *arguments)

    @classmethod
    def substring(
        cls,
        string: IntoExpression,
        start: IntoExpression,
        end: IntoExpression | UndefinedType = Undefined,
    ) -> Expression:
        """Build a GenomeSpy ``substring`` expression."""
        arguments = [string, start, end]
        while arguments and arguments[-1] is Undefined:
            arguments.pop()
        if any(argument is Undefined for argument in arguments):
            raise ValueError("substring optional arguments cannot contain gaps")
        return _function_expression("substring", *arguments)

    @classmethod
    def trim(cls, string: IntoExpression) -> Expression:
        """Build a GenomeSpy ``trim`` expression."""
        return _function_expression("trim", string)

    @classmethod
    def btoa(cls, string: IntoExpression) -> Expression:
        """Build a GenomeSpy ``btoa`` expression."""
        return _function_expression("btoa", string)

    @classmethod
    def atob(cls, string: IntoExpression) -> Expression:
        """Build a GenomeSpy ``atob`` expression."""
        return _function_expression("atob", string)

    @classmethod
    def format(cls, value: IntoExpression, specifier: IntoExpression) -> Expression:
        """Build a GenomeSpy ``format`` expression."""
        return _function_expression("format", value, specifier)

    @classmethod
    def regexp(
        cls, pattern: IntoExpression, flags: IntoExpression | UndefinedType = Undefined
    ) -> Expression:
        """Build a GenomeSpy ``regexp`` expression."""
        arguments = [pattern, flags]
        while arguments and arguments[-1] is Undefined:
            arguments.pop()
        if any(argument is Undefined for argument in arguments):
            raise ValueError("regexp optional arguments cannot contain gaps")
        return _function_expression("regexp", *arguments)

    @classmethod
    def test(
        cls, regexp: IntoExpression, string: IntoExpression | UndefinedType = Undefined
    ) -> Expression:
        """Build a GenomeSpy ``test`` expression."""
        arguments = [regexp, string]
        while arguments and arguments[-1] is Undefined:
            arguments.pop()
        if any(argument is Undefined for argument in arguments):
            raise ValueError("test optional arguments cannot contain gaps")
        return _function_expression("test", *arguments)

    @classmethod
    def scale(cls, channel: IntoExpression, value: IntoExpression) -> Expression:
        """Build a GenomeSpy ``scale`` expression."""
        return _function_expression("scale", channel, value)

    @classmethod
    def invert(cls, channel: IntoExpression, range: IntoExpression) -> Expression:
        """Build a GenomeSpy ``invert`` expression."""
        return _function_expression("invert", channel, range)

    @classmethod
    def domain(cls, channel: IntoExpression) -> Expression:
        """Build a GenomeSpy ``domain`` expression."""
        return _function_expression("domain", channel)

    @classmethod
    def range(cls, channel: IntoExpression) -> Expression:
        """Build a GenomeSpy ``range`` expression."""
        return _function_expression("range", channel)

    @classmethod
    def bandwidth(cls, channel: IntoExpression) -> Expression:
        """Build a GenomeSpy ``bandwidth`` expression."""
        return _function_expression("bandwidth", channel)

    @classmethod
    def mapHasKey(cls, map: IntoExpression, key: IntoExpression) -> Expression:
        """Build a GenomeSpy ``mapHasKey`` expression."""
        return _function_expression("mapHasKey", map, key)

    @classmethod
    def lerp(cls, array: IntoExpression, fraction: IntoExpression) -> Expression:
        """Build a GenomeSpy ``lerp`` expression."""
        return _function_expression("lerp", array, fraction)

    @classmethod
    def linearstep(
        cls, edge0: IntoExpression, edge1: IntoExpression, x: IntoExpression
    ) -> Expression:
        """Build a GenomeSpy ``linearstep`` expression."""
        return _function_expression("linearstep", edge0, edge1, x)

    @classmethod
    def smoothstep(
        cls, edge0: IntoExpression, edge1: IntoExpression, x: IntoExpression
    ) -> Expression:
        """Build a GenomeSpy ``smoothstep`` expression."""
        return _function_expression("smoothstep", edge0, edge1, x)

    @classmethod
    def center(cls, array: IntoExpression) -> Expression:
        """Build a GenomeSpy ``center`` expression."""
        return _function_expression("center", array)


__all__ = ["Expression", "expr"]
