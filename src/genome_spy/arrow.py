"""Arrow IPC serialization helpers for notebook data transport."""

from __future__ import annotations

from typing import Any

__all__ = ["to_arrow_ipc"]


def to_arrow_ipc(data: Any) -> bytes:
    """Serialize a DataFrame-like object as uncompressed Arrow IPC bytes.

    Description:
        The object must provide the Polars-compatible ``write_ipc`` method.
        The helper intentionally requests uncompressed IPC because GenomeSpy's
        Arrow decoder does not support compressed IPC buffers yet.

    Args:
        data: A Polars ``DataFrame`` or compatible object with
            ``write_ipc(file=None, compression="uncompressed")``.

    Returns:
        The complete Arrow IPC file payload as immutable bytes.

    Raises:
        TypeError: If the object does not provide a compatible writer or the
            writer does not return a bytes-like payload.
        ValueError: If the writer returns an empty payload.

    Example:
        >>> import polars as pl
        >>> payload = to_arrow_ipc(pl.DataFrame({"x": [1, 2]}))
        >>> payload[:6]
        b'ARROW1'
    """

    writer = getattr(data, "write_ipc", None)
    if not callable(writer):
        raise TypeError(
            "Arrow IPC serialization requires an object with "
            'write_ipc(file=None, compression="uncompressed").'
        )

    try:
        result = writer(file=None, compression="uncompressed")
    except (TypeError, ValueError) as error:
        raise TypeError(
            f"Could not write uncompressed Arrow IPC data from {type(data).__name__}."
        ) from error

    if hasattr(result, "getvalue"):
        result = result.getvalue()

    if not isinstance(result, bytes | bytearray | memoryview):
        raise TypeError(
            "Arrow IPC writer must return bytes or a binary buffer, "
            f"not {type(result).__name__}."
        )

    payload = bytes(result)
    if not payload:
        raise ValueError("Arrow IPC writer returned an empty payload.")
    return payload
