"""Handwritten Altair-style conveniences for GenomeSpy transforms."""

from __future__ import annotations

from typing import Self, cast

from genome_spy.schema.mixins import TransformMethodMixin
from genome_spy.schemapi import Undefined, UndefinedType

__all__ = ["AltairTransformCompatMixin"]


class AltairTransformCompatMixin(TransformMethodMixin):
    """Add familiar Altair call shapes to generated GenomeSpy transforms."""

    def transform_calculate(
        self,
        as_: str | UndefinedType = Undefined,
        calculate: str | UndefinedType = Undefined,
        **kwargs: str,
    ) -> Self:
        """Add one or more calculated fields.

        Each calculation serializes as a GenomeSpy ``formula`` transform.
        Direct ``as_`` and ``calculate`` arguments add one field, while keyword
        arguments add fields in insertion order.

        Args:
            as_: Field that receives the direct calculation result.
            calculate: GenomeSpy expression for the direct calculation.
            **kwargs: Output field names mapped to GenomeSpy expressions.

        Returns:
            A copied specification with the formula transforms appended.

        Raises:
            TypeError: If only one direct argument is provided.
            ValueError: If both ``as_`` and the ``"as"`` compatibility alias
                are provided.

        Example:
            ``chart.transform_calculate(x="datum.value * 2")``
        """
        if as_ is Undefined:
            as_ = kwargs.pop("as", Undefined)
        elif "as" in kwargs:
            raise ValueError("transform_calculate received both 'as_' and 'as'.")

        has_output = as_ is not Undefined
        has_expression = calculate is not Undefined
        if has_output != has_expression:
            raise TypeError(
                "transform_calculate requires 'as_' and 'calculate' together."
            )

        result = self
        if has_output and has_expression:
            result = result.transform_formula(
                as_=cast(str, as_),
                expr=cast(str, calculate),
            )

        for output, expression in kwargs.items():
            result = result.transform_formula(as_=output, expr=expression)

        return result
