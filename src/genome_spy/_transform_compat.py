"""Handwritten Altair-style conveniences for GenomeSpy transforms."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Literal, Self, cast

from genome_spy.schema import AggregateOp_T, Field_T, WindowOp_T, core
from genome_spy.schema.mixins import TransformMethodMixin
from genome_spy.schemapi import Undefined, UndefinedType
from genome_spy._transform_normalization import (
    _ConstraintValue,
    _constraint_expression,
    _normalize_aggregate_definition,
    _normalize_sort_definitions,
    _normalize_window_definition,
    _parse_aggregate_shorthand,
    _parse_window_shorthand,
)

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

    def transform_lookup(
        self,
        lookup: Field_T | UndefinedType = Undefined,
        from_: Any | UndefinedType = Undefined,
        as_: Sequence[str] | str | UndefinedType = Undefined,
        default: Any | UndefinedType = Undefined,
        *,
        key: Field_T | Sequence[Field_T] | UndefinedType = Undefined,
        fields: Field_T | Sequence[Field_T] | None | UndefinedType = Undefined,
        values: Sequence[Field_T] | None | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
    ) -> Self:
        """Look up ordinary data using Altair or GenomeSpy arguments.

        In the compatibility form, ``lookup`` names the local field and
        ``from_`` is a plain mapping with ``data``, ``key``, and ``fields``.
        These values map directly to GenomeSpy's data source, foreign key,
        copied values, and local input field.

        Args:
            lookup: Local input field using Altair's argument name.
            from_: Native GenomeSpy data or an Altair-like plain mapping.
            as_: Output names matching the copied foreign fields.
            default: Value written when no foreign row matches.
            key: GenomeSpy-native foreign key field or fields.
            fields: GenomeSpy-native local input field or fields.
            values: GenomeSpy-native foreign fields to copy.
            description: Description of the transform step.

        Returns:
            A copied specification with the lookup transform appended.

        Raises:
            TypeError: If required values have invalid types or compatibility
                and native lookup arguments are mixed.
            ValueError: If the compatibility mapping is incomplete, contains
                unsupported properties, or output counts do not match.

        Example:
            ``chart.transform_lookup(lookup="id", from_={"data": data, "key":
            "id", "fields": ["label"]}, as_=["label"])``
        """
        if lookup is Undefined:
            if from_ is Undefined or key is Undefined:
                raise TypeError("transform_lookup requires 'from_' and 'key'.")
            return super().transform_lookup(
                from_=cast(Any, from_),
                key=cast(Field_T | Sequence[Field_T], key),
                as_=cast(Any, as_),
                default=default,
                description=description,
                fields=fields,
                values=values,
            )

        if any(value is not Undefined for value in (key, fields, values)):
            raise TypeError(
                "Altair-style 'lookup' cannot be combined with native 'key', "
                "'fields', or 'values'."
            )
        if not isinstance(from_, Mapping):
            raise TypeError(
                "Altair-style lookup requires a plain 'from_' mapping with "
                "'data', 'key', and 'fields'."
            )

        extra = set(from_) - {"data", "key", "fields"}
        if extra:
            names = ", ".join(sorted(extra))
            raise ValueError(f"Unsupported lookup source properties: {names}.")
        missing = {"data", "key", "fields"} - set(from_)
        if missing:
            names = ", ".join(sorted(missing))
            raise ValueError(f"Lookup source is missing: {names}.")

        foreign_key = from_["key"]
        copied_values = from_["fields"]
        if not isinstance(foreign_key, str):
            raise TypeError("Lookup source 'key' must be a string.")
        if isinstance(copied_values, (str, bytes)) or not isinstance(
            copied_values, Sequence
        ):
            raise TypeError("Lookup source 'fields' must be a sequence of strings.")
        if not all(isinstance(value, str) for value in copied_values):
            raise TypeError("Lookup source 'fields' must contain only strings.")
        if isinstance(as_, str) or as_ is Undefined:
            raise TypeError(
                "Altair-style lookup requires an explicit output-name sequence."
            )
        output_names = cast(Sequence[str], as_)
        if len(output_names) != len(copied_values):
            raise ValueError(
                "Lookup output names must match the number of copied fields."
            )

        return super().transform_lookup(
            from_=cast(Any, from_["data"]),
            key=foreign_key,
            as_=output_names,
            default=default,
            description=description,
            fields=lookup,
            values=cast(Sequence[Field_T], copied_values),
        )

    def transform_filter(
        self,
        expression: str | UndefinedType = Undefined,
        *more_expressions: str,
        description: str | UndefinedType = Undefined,
        empty: bool | UndefinedType = Undefined,
        expr: str | UndefinedType = Undefined,
        fields: dict[str, Any] | UndefinedType = Undefined,
        param: str | UndefinedType = Undefined,
        **constraints: _ConstraintValue,
    ) -> Self:
        """Filter rows with raw expressions or scalar equality constraints.

        Multiple expressions and constraints are joined with JavaScript's
        ``&&`` operator. GenomeSpy's native selection-parameter form remains
        available through ``param`` but is not translated from Altair objects.

        Args:
            expression: First raw GenomeSpy expression.
            *more_expressions: Additional raw expressions to combine.
            description: Description of the transform step.
            empty: Native behavior when a selection parameter is empty.
            expr: Native keyword form of the first raw expression.
            fields: Native positional-channel projection for selection filters.
            param: Native GenomeSpy selection parameter name.
            **constraints: Field names mapped to scalar values for equality
                checks.

        Returns:
            A copied specification with the filter transform appended.

        Raises:
            TypeError: If expression forms conflict, an expression is not a
                string, a constraint is not scalar, or compatibility filtering
                is mixed with a selection parameter.
            ValueError: If a numeric constraint is not finite.

        Example:
            ``chart.transform_filter("datum.year > 1980", sex=1)``
        """
        uses_composition = bool(more_expressions) or bool(constraints)
        if not uses_composition:
            return super().transform_filter(
                expression,
                description=description,
                empty=empty,
                expr=expr,
                fields=fields,
                param=param,
            )

        if param is not Undefined:
            raise TypeError(
                "Expression composition cannot be combined with selection 'param'."
            )
        if expression is not Undefined and expr is not Undefined:
            raise TypeError("expression cannot be combined with expr")

        first_expression = expr if expression is Undefined else expression
        expressions: list[str] = []
        if first_expression is not Undefined:
            if not isinstance(first_expression, str):
                raise TypeError("Filter expressions must be strings.")
            expressions.append(first_expression)

        if not all(isinstance(value, str) for value in more_expressions):
            raise TypeError("Filter expressions must be strings.")
        expressions.extend(more_expressions)
        expressions.extend(
            _constraint_expression(field, value) for field, value in constraints.items()
        )

        combined = (
            expressions[0]
            if len(expressions) == 1
            else " && ".join(f"({value})" for value in expressions)
        )
        return super().transform_filter(
            description=description,
            empty=empty,
            expr=combined,
            fields=fields,
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

    def transform_stack(
        self,
        as_: Sequence[str] | str | UndefinedType = Undefined,
        stack: Field_T | UndefinedType = Undefined,
        groupby: Sequence[Field_T] | UndefinedType = Undefined,
        offset: Literal["zero", "center", "normalize", "information"]
        | UndefinedType = Undefined,
        sort: core.CompareParams
        | Mapping[str, Any]
        | Sequence[Mapping[str, Any]]
        | UndefinedType = Undefined,
        *,
        field: Field_T | UndefinedType = Undefined,
        baseField: Field_T | UndefinedType = Undefined,
        cardinality: float | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
    ) -> Self:
        """Stack values using Altair or GenomeSpy arguments.

        Altair's positional ``stack`` name maps to GenomeSpy's ``field`` and a
        list of sort definitions maps to GenomeSpy's parallel compare arrays.
        A single output base name expands to start and ``_end`` fields.

        Args:
            as_: Output field pair or an Altair-style output base name.
            stack: Field to stack using Altair's argument name.
            groupby: Fields that form independent stacks.
            offset: Stack offset mode.
            sort: Native GenomeSpy compare definition or Altair-like sort list.
            field: Field to stack using GenomeSpy's native argument name.
            baseField: Native base field used by the ``information`` offset.
            cardinality: Native cardinality used by the ``information`` offset.
            description: Description of the transform step.

        Returns:
            A copied specification with the stack transform appended.

        Raises:
            TypeError: If ``stack`` and ``field`` are both provided, groupby is
                omitted, or a sort definition has invalid types.
            ValueError: If a sort definition has unsupported properties or
                order values.

        Example:
            ``chart.transform_stack("stacked", "value", ["group"])``
        """
        if stack is not Undefined and field is not Undefined:
            raise TypeError("transform_stack received both 'stack' and 'field'.")
        if groupby is Undefined:
            raise TypeError("transform_stack requires 'groupby'.")

        normalized_field = field if stack is Undefined else stack
        normalized_as: Sequence[str] | UndefinedType
        if isinstance(as_, str):
            normalized_as = [as_, f"{as_}_end"]
        else:
            normalized_as = as_

        normalized_sort = sort
        if isinstance(sort, Sequence) and not isinstance(sort, (str, bytes)):
            normalized_sort = _normalize_sort_definitions(sort)

        return super().transform_stack(
            as_=normalized_as,
            baseField=baseField,
            cardinality=cardinality,
            description=description,
            field=normalized_field,
            groupby=cast(Sequence[Field_T], groupby),
            offset=offset,
            sort=cast(Any, normalized_sort),
        )

    def transform_window(
        self,
        window: Sequence[Mapping[str, Any]] | UndefinedType = Undefined,
        frame: Sequence[float | None] | UndefinedType = Undefined,
        groupby: Sequence[Field_T] | UndefinedType = Undefined,
        ignorePeers: bool | UndefinedType = Undefined,
        sort: core.CompareParams
        | Mapping[str, Any]
        | Sequence[Mapping[str, Any]]
        | UndefinedType = Undefined,
        *,
        ops: Sequence[WindowOp_T] | UndefinedType = Undefined,
        as_: Sequence[str | None] | UndefinedType = Undefined,
        description: str | UndefinedType = Undefined,
        fields: Sequence[Field_T | None] | UndefinedType = Undefined,
        params: Sequence[float | None] | UndefinedType = Undefined,
        **kwargs: str,
    ) -> Self:
        """Calculate window values using Altair shorthand or GenomeSpy arrays.

        Compatibility definitions are normalized into GenomeSpy's aligned
        operation arrays. Altair-like sort lists are normalized to a GenomeSpy
        compare definition, with omitted orders defaulting to ascending.

        Args:
            window: Altair-like mappings with ``op``, ``as``, and optional
                ``field`` and ``param`` properties.
            frame: Inclusive window-frame offsets.
            groupby: Fields defining independent window partitions.
            ignorePeers: Whether frame offsets ignore peer rows.
            sort: Native GenomeSpy compare definition or Altair-like sort list.
            ops: GenomeSpy-native operation array.
            as_: GenomeSpy-native output field array.
            description: Description of the transform step.
            fields: GenomeSpy-native input field array.
            params: GenomeSpy-native operation parameter array.
            **kwargs: Output names mapped to ``operation(field)`` shorthand.

        Returns:
            A copied specification with the window transform appended.

        Raises:
            TypeError: If compatibility and native array forms are mixed or a
                definition has invalid value types.
            ValueError: If definitions, shorthand, or operations are invalid.

        Example:
            ``chart.transform_window(rank="rank()", total="sum(value)")``
        """
        native_arguments = (ops, as_, fields, params)
        uses_native_arrays = any(value is not Undefined for value in native_arguments)
        uses_compatibility = window is not Undefined or bool(kwargs)
        if uses_native_arrays and uses_compatibility:
            raise TypeError(
                "transform_window cannot mix compatibility definitions with "
                "'ops', 'fields', 'params', or 'as_'."
            )

        normalized_sort = sort
        if isinstance(sort, Sequence) and not isinstance(sort, (str, bytes)):
            normalized_sort = _normalize_sort_definitions(sort)

        if not uses_compatibility:
            if ops is Undefined:
                raise TypeError(
                    "transform_window requires 'ops' or window definitions."
                )
            return super().transform_window(
                ops=cast(Sequence[WindowOp_T], ops),
                as_=as_,
                description=description,
                fields=fields,
                frame=frame,
                groupby=groupby,
                ignorePeers=ignorePeers,
                params=params,
                sort=cast(Any, normalized_sort),
            )

        definitions = (
            []
            if window is Undefined
            else list(cast(Sequence[Mapping[str, Any]], window))
        )
        if not definitions and not kwargs:
            raise ValueError("transform_window requires at least one definition.")

        normalized_ops: list[WindowOp_T] = []
        normalized_fields: list[str | None] = []
        normalized_params: list[float | None] = []
        normalized_outputs: list[str] = []
        for definition in definitions:
            operation, field, param, output = _normalize_window_definition(definition)
            normalized_ops.append(operation)
            normalized_fields.append(field)
            normalized_params.append(param)
            normalized_outputs.append(output)

        for output, shorthand in kwargs.items():
            operation, field, param = _parse_window_shorthand(shorthand)
            normalized_ops.append(operation)
            normalized_fields.append(field)
            normalized_params.append(param)
            normalized_outputs.append(output)

        emitted_params: Sequence[float | None] | UndefinedType = Undefined
        if any(param is not None for param in normalized_params):
            emitted_params = normalized_params

        return super().transform_window(
            ops=normalized_ops,
            as_=normalized_outputs,
            description=description,
            fields=normalized_fields,
            frame=frame,
            groupby=groupby,
            ignorePeers=ignorePeers,
            params=emitted_params,
            sort=cast(Any, normalized_sort),
        )
