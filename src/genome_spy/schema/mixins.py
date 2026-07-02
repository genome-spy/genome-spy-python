"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""

from __future__ import annotations
from typing import Any, Self


class MarkMethodMixin:
    """Grammar-derived mark methods for the handwritten chart API."""

    def mark_rect(self, **kwargs: Any) -> Self:
        """Set the chart mark to ``rect``."""
        return self._with_mark("rect", **kwargs)  # type: ignore[attr-defined, no-any-return]

    def mark_point(self, **kwargs: Any) -> Self:
        """Set the chart mark to ``point``."""
        return self._with_mark("point", **kwargs)  # type: ignore[attr-defined, no-any-return]

    def mark_rule(self, **kwargs: Any) -> Self:
        """Set the chart mark to ``rule``."""
        return self._with_mark("rule", **kwargs)  # type: ignore[attr-defined, no-any-return]

    def mark_tick(self, **kwargs: Any) -> Self:
        """Set the chart mark to ``tick``."""
        return self._with_mark("tick", **kwargs)  # type: ignore[attr-defined, no-any-return]

    def mark_text(self, **kwargs: Any) -> Self:
        """Set the chart mark to ``text``."""
        return self._with_mark("text", **kwargs)  # type: ignore[attr-defined, no-any-return]

    def mark_link(self, **kwargs: Any) -> Self:
        """Set the chart mark to ``link``."""
        return self._with_mark("link", **kwargs)  # type: ignore[attr-defined, no-any-return]


__all__ = ["MarkMethodMixin"]
