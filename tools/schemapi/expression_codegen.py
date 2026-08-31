"""Parse upstream expression documentation for Python API generation."""

from __future__ import annotations

import html
import keyword
import re
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExpressionParameterSpec:
    """A parameter parsed from an upstream expression signature."""

    name: str
    optional: bool = False
    variadic: bool = False


@dataclass(frozen=True, slots=True)
class ExpressionFunctionSpec:
    """A function exposed by GenomeSpy's expression runtime."""

    name: str
    parameters: tuple[ExpressionParameterSpec, ...]

    @property
    def python_name(self) -> str:
        """Return a valid Python spelling for the runtime function name."""
        return f"{self.name}_" if keyword.iskeyword(self.name) else self.name


@dataclass(frozen=True, slots=True)
class ExpressionCatalog:
    """Constants and functions parsed from versioned upstream documentation."""

    constants: tuple[str, ...]
    functions: tuple[ExpressionFunctionSpec, ...]


_VEGA_LINK_RE = re.compile(
    r"\[`(?P<name>[A-Za-z_$][\w$]*)`\]"
    r"\(https://vega\.github\.io/vega/docs/expressions/#(?P=name)\)"
)
_SIGNATURE_RE = re.compile(
    r'<a name="(?P<anchor>[^"]+)"[^>]*>.*?</a>\s*\n'
    r"<b>(?P<name>[^<]+)</b>\((?P<parameters>[^\n)]*)\)",
)
_ANCHOR_RE = re.compile(r'<a name="(?P<name>[A-Za-z_$][\w$]*)"')
_PARAMETER_RE = re.compile(r"<i>(?P<name>[^<]+)</i>")


def parse_expression_catalog(genome_spy_docs: str, vega_docs: str) -> ExpressionCatalog:
    """Parse GenomeSpy's documented expression surface and Vega signatures.

    Args:
        genome_spy_docs: Markdown from GenomeSpy's expression grammar page.
        vega_docs: Markdown from the version-matched Vega expression reference.

    Returns:
        The ordered constants and functions supported by GenomeSpy.

    Raises:
        ValueError: If required sections or function signatures cannot be parsed.

    Example:
        ``parse_expression_catalog(genome_docs, vega_docs).functions`` returns
        the functions that should be emitted in the Python namespace.
    """
    vega_section = _section(
        genome_spy_docs,
        "### Constants and functions from Vega",
        "### Scale Functions",
    )
    constants_section = _section(vega_section, "#### Constants", "#### Type Checking")
    constants = tuple(
        match.group("name") for match in _VEGA_LINK_RE.finditer(constants_section)
    )
    if not constants:
        raise ValueError("GenomeSpy expression docs contain no Vega constants.")

    function_names = [
        match.group("name")
        for match in _VEGA_LINK_RE.finditer(vega_section)
        if match.group("name") not in constants
    ]
    if re.search(r"equivalent\s+`if`\s+construct", genome_spy_docs):
        function_names.insert(0, "if")

    vega_signatures = _parse_signatures(vega_docs)
    custom_section = genome_spy_docs[genome_spy_docs.index("### Scale Functions") :]
    custom_signatures = _parse_signatures(custom_section)
    custom_names = tuple(
        match.group("name") for match in _ANCHOR_RE.finditer(custom_section)
    )

    missing = [name for name in function_names if name not in vega_signatures]
    if missing:
        raise ValueError(
            "Vega expression docs contain no signatures for: " + ", ".join(missing)
        )
    missing_custom = [name for name in custom_names if name not in custom_signatures]
    if missing_custom:
        raise ValueError(
            "GenomeSpy expression docs contain no signatures for: "
            + ", ".join(missing_custom)
        )
    if not custom_signatures:
        raise ValueError("GenomeSpy expression docs contain no custom functions.")

    functions = [vega_signatures[name] for name in function_names]
    for name, signature in custom_signatures.items():
        functions = [item for item in functions if item.name != name]
        functions.append(signature)

    return ExpressionCatalog(constants=constants, functions=tuple(functions))


def _section(source: str, start: str, end: str) -> str:
    try:
        start_index = source.index(start)
        end_index = source.index(end, start_index + len(start))
    except ValueError as error:
        raise ValueError(
            f"Expression docs are missing section boundary {error}."
        ) from error
    return source[start_index:end_index]


def _parse_signatures(source: str) -> dict[str, ExpressionFunctionSpec]:
    signatures: dict[str, ExpressionFunctionSpec] = {}
    for match in _SIGNATURE_RE.finditer(source):
        name = html.unescape(match.group("name")).strip()
        signatures.setdefault(
            name,
            ExpressionFunctionSpec(
                name=name,
                parameters=_parse_parameters(match.group("parameters")),
            ),
        )
    return signatures


def _parse_parameters(source: str) -> tuple[ExpressionParameterSpec, ...]:
    parameters: list[ExpressionParameterSpec] = []
    for match in _PARAMETER_RE.finditer(source):
        raw_name = html.unescape(match.group("name")).strip()
        name = _python_identifier(raw_name)
        prefix = source[: match.start()]
        optional = prefix.count("[") > prefix.count("]")
        parameters.append(ExpressionParameterSpec(name=name, optional=optional))

    if "..." in source and parameters:
        parameters.append(ExpressionParameterSpec(name="args", variadic=True))
    return tuple(parameters)


def _python_identifier(name: str) -> str:
    identifier = re.sub(r"\W", "_", name)
    return f"{identifier}_" if keyword.iskeyword(identifier) else identifier


__all__ = [
    "ExpressionCatalog",
    "ExpressionFunctionSpec",
    "ExpressionParameterSpec",
    "parse_expression_catalog",
]
