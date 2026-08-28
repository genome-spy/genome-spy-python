"""Handwritten Altair-style conveniences for GenomeSpy transforms."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any
from typing import Self, cast

from genome_spy.schema import AggregateOp_T, Field_T
from genome_spy.schema.mixins import TransformMethodMixin
from genome_spy.schemapi import Undefined, UndefinedType

__all__ = ["AltairTransformCompatMixin"]

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
_OPERATION_ALIASES = {"average": "mean"}
_OPERATION_SHORTHAND = re.compile(
    r"^\s*(?P<operation>[A-Za-z_][A-Za-z0-9_]*)\s*"
    r"\(\s*(?P<field>[^()]*)\s*\)\s*$"
)


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

    def transform_aggregate(
        self,
        aggregate: Sequence[Mapping[str, Any]] | UndefinedType = Undefined,
        groupby: Sequence[Field_T] | UndefinedType = Undefined,
        *,
        as_: Sequence[str] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        fields: Sequence[Field_T] | UndefinedType = Undefined,
        ops: Sequence[AggregateOp_T] | UndefinedType = Undefined,
        **kwargs: str,
    ) -> Self:
        """Aggregate fields using Altair shorthand or GenomeSpy arrays.

        Compatibility definitions are normalized into GenomeSpy's aligned
        ``fields``, ``ops``, and ``as`` arrays. Only operations supported by
        GenomeSpy Core are accepted, and fieldless ``count()`` is deliberately
        excluded.

        Args:
            aggregate: Altair-like mappings containing ``op``, ``field``, and
                ``as`` properties.
            groupby: Fields by which to group input rows.
            as_: GenomeSpy-native output field array.
            description: Description of the transform step.
            fields: GenomeSpy-native input field array.
            ops: GenomeSpy-native operation array.
            **kwargs: Output names mapped to ``operation(field)`` shorthand.

        Returns:
            A copied specification with the aggregate transform appended.

        Raises:
            TypeError: If compatibility and native array forms are mixed, or a
                mapping contains non-string values.
            ValueError: If shorthand, mappings, or operations are invalid.

        Example:
            ``chart.transform_aggregate(mean_value="mean(value)")``
        """
        native_arguments = (as_, fields, ops)
        uses_native_arrays = any(value is not Undefined for value in native_arguments)
        uses_compatibility = aggregate is not Undefined or bool(kwargs)
        if uses_native_arrays and uses_compatibility:
            raise TypeError(
                "transform_aggregate cannot mix compatibility definitions with "
                "'fields', 'ops', or 'as_'."
            )

        if not uses_compatibility:
            return super().transform_aggregate(
                as_=as_,
                description=description,
                fields=fields,
                groupby=groupby,
                ops=ops,
            )

        definitions = (
            []
            if aggregate is Undefined
            else list(cast(Sequence[Mapping[str, Any]], aggregate))
        )
        if not definitions and not kwargs:
            raise ValueError("transform_aggregate requires at least one definition.")

        normalized_ops: list[AggregateOp_T] = []
        normalized_fields: list[Field_T] = []
        normalized_outputs: list[str] = []
        for definition in definitions:
            operation, field, output = _normalize_aggregate_definition(definition)
            normalized_ops.append(operation)
            normalized_fields.append(field)
            normalized_outputs.append(output)

        for output, shorthand in kwargs.items():
            operation, field = _parse_aggregate_shorthand(shorthand)
            normalized_ops.append(operation)
            normalized_fields.append(field)
            normalized_outputs.append(output)

        return super().transform_aggregate(
            as_=normalized_outputs,
            description=description,
            fields=normalized_fields,
            groupby=groupby,
            ops=normalized_ops,
        )

    def transform_flatten(
        self,
        flatten: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        as_: Sequence[str] | str | UndefinedType = Undefined,
        *,
        fields: Sequence[Field_T] | Field_T | UndefinedType = Undefined,
        index: str | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
    ) -> Self:
        """Flatten array-valued fields using Altair or GenomeSpy arguments.

        The positional ``flatten`` argument is an alias for GenomeSpy's native
        ``fields`` property. GenomeSpy's optional index output remains
        available as a keyword argument.

        Args:
            flatten: Field or fields to flatten using Altair's call shape.
            as_: Output field name or names for flattened values.
            fields: Field or fields to flatten using GenomeSpy's native name.
            index: Output field for each array value's zero-based index.
            description: Description of the transform step.

        Returns:
            A copied specification with the flatten transform appended.

        Raises:
            TypeError: If both ``flatten`` and ``fields`` are provided.

        Example:
            ``chart.transform_flatten(["items"], ["item"])``
        """
        if flatten is not Undefined and fields is not Undefined:
            raise TypeError("transform_flatten received both 'flatten' and 'fields'.")

        normalized_fields = fields if flatten is Undefined else flatten
        return super().transform_flatten(
            as_=as_,
            description=description,
            fields=normalized_fields,
            index=index,
        )

    def transform_sample(
        self,
        sample: float | UndefinedType = Undefined,
        *,
        size: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
    ) -> Self:
        """Sample rows using Altair or GenomeSpy arguments.

        A positional sample size follows Altair's call shape. Omitting both
        size arguments emits Altair's 1000-row default explicitly, while the
        native GenomeSpy ``size`` keyword remains supported.

        Args:
            sample: Maximum sample size using Altair's positional name.
            size: Maximum sample size using GenomeSpy's native name.
            description: Description of the transform step.

        Returns:
            A copied specification with the sample transform appended.

        Raises:
            TypeError: If both ``sample`` and ``size`` are provided.

        Example:
            ``chart.transform_sample(1000)``
        """
        if sample is not Undefined and size is not Undefined:
            raise TypeError("transform_sample received both 'sample' and 'size'.")

        if sample is Undefined and size is Undefined:
            normalized_size: float = 1000
        else:
            normalized_size = cast(float, size if sample is Undefined else sample)

        return super().transform_sample(
            description=description,
            size=normalized_size,
        )
