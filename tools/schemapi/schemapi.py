"""Runtime primitives for generated GenomeSpy schema wrappers.

Altair copies its development-time ``tools/schemapi/schemapi.py`` into the
installed package as ``altair/utils/schemapi.py``. We keep this file as the
source for the same future pattern, but only implement the small primitives
needed by the first generator scaffold.
"""

from __future__ import annotations

import json
from typing import Any, ClassVar


class UndefinedType:
    """Sentinel for properties omitted from a serialized spec."""

    def __repr__(self) -> str:
        return "Undefined"


Undefined = UndefinedType()


class SchemaBase:
    """Small base class for future generated GenomeSpy schema wrappers.

    The class stores keyword properties and serializes nested schema objects.
    It is intentionally much smaller than Altair's runtime ``SchemaBase`` for
    now: validation, from-dict reconstruction, and property setters will be
    added once the GenomeSpy schema generator needs them.
    """

    _schema: ClassVar[dict[str, Any]] = {}
    _rootschema: ClassVar[dict[str, Any]] = {}

    def __init__(self, **kwds: Any) -> None:
        self._kwds = kwds

    def copy(self, **kwds: Any) -> SchemaBase:
        """Return a shallow copy with updated keyword properties."""
        merged = {**self._kwds, **kwds}
        return self.__class__(**merged)

    def to_dict(self) -> dict[str, Any]:
        """Serialize this schema wrapper to a JSON-compatible dictionary."""
        return {
            key: _todict(value)
            for key, value in self._kwds.items()
            if value is not Undefined
        }

    def to_json(self) -> str:
        """Serialize this schema wrapper to formatted JSON."""
        return json.dumps(self.to_dict(), indent=2)


def _todict(value: Any) -> Any:
    if isinstance(value, SchemaBase):
        return value.to_dict()
    if isinstance(value, list | tuple):
        return [_todict(item) for item in value]
    if isinstance(value, dict):
        return {
            key: _todict(item) for key, item in value.items() if item is not Undefined
        }
    return value
