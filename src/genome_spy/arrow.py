"""Arrow IPC serialization helpers for notebook data transport."""

from __future__ import annotations

from io import BytesIO
from typing import Any

__all__ = ["to_arrow_ipc"]


def _module_root(value: Any) -> str:
    """Return the top-level module that defines a value's type."""
    return type(value).__module__.partition(".")[0]


def _is_polars_frame(value: Any) -> bool:
    """Return whether a value is a Polars dataframe without importing Polars."""
    return _module_root(value) == "polars" and callable(
        getattr(value, "write_ipc", None)
    )


def _is_pandas_frame(value: Any) -> bool:
    """Return whether a value is a pandas dataframe without importing pandas."""
    return _module_root(value) == "pandas" and type(value).__name__ == "DataFrame"


def _is_pyarrow_table(value: Any) -> bool:
    """Return whether a value is a supported PyArrow tabular object."""
    return _module_root(value) == "pyarrow" and type(value).__name__ in {
        "Table",
        "RecordBatch",
    }


def _validated_payload(value: Any) -> bytes:
    """Return a nonempty immutable IPC payload or raise a contextual error."""
    if hasattr(value, "getvalue"):
        value = value.getvalue()
    if not isinstance(value, bytes | bytearray | memoryview):
        raise TypeError(
            "Arrow IPC writer must return bytes or a binary buffer, "
            f"not {type(value).__name__}."
        )
    payload = bytes(value)
    if not payload:
        raise ValueError("Arrow IPC writer returned an empty payload.")
    return payload


def _write_ipc_method(data: Any) -> bytes:
    """Serialize an object that exposes Polars-compatible ``write_ipc``."""
    try:
        result = data.write_ipc(file=None, compression="uncompressed")
    except (TypeError, ValueError) as error:
        raise TypeError(
            f"Could not write uncompressed Arrow IPC data from {type(data).__name__}."
        ) from error
    return _validated_payload(result)


def _load_pyarrow() -> Any | None:
    """Import PyArrow only when a recognized table requires it."""
    try:
        import pyarrow as pa
    except ImportError:
        return None
    return pa


def _write_pyarrow_ipc(data: Any, pa: Any) -> bytes:
    """Serialize a PyArrow table or record batch as an uncompressed IPC file."""
    table = (
        pa.Table.from_batches([data]) if type(data).__name__ == "RecordBatch" else data
    )
    output = BytesIO()
    options = pa.ipc.IpcWriteOptions(compression=None)
    with pa.ipc.new_file(output, table.schema, options=options) as writer:
        writer.write_table(table)
    return _validated_payload(output.getvalue())


def _write_pandas_ipc(data: Any, pa: Any) -> bytes:
    """Serialize a pandas dataframe through optional PyArrow."""
    table = pa.Table.from_pandas(data, preserve_index=False)
    return _write_pyarrow_ipc(table, pa)


def _try_to_arrow_ipc(data: Any) -> bytes | None:
    """Return IPC bytes for an automatically supported table, if available.

    ``None`` means the input is not an automatically supported Arrow producer
    or pandas support is unavailable because PyArrow is not installed. Errors
    from recognized writers intentionally propagate rather than falling back to
    JSON records.
    """
    if _is_polars_frame(data):
        return _write_ipc_method(data)
    if _is_pyarrow_table(data):
        pa = _load_pyarrow()
        if pa is None:
            raise RuntimeError("PyArrow table support requires the 'arrow' extra.")
        return _write_pyarrow_ipc(data, pa)
    if _is_pandas_frame(data):
        pa = _load_pyarrow()
        return None if pa is None else _write_pandas_ipc(data, pa)
    return None


def to_arrow_ipc(data: Any) -> bytes:
    """Serialize a DataFrame-like object as uncompressed Arrow IPC bytes.

    Description:
        Supports Polars dataframes, PyArrow tables and record batches, pandas
        dataframes when the optional ``arrow`` extra is installed, and custom
        objects with a Polars-compatible ``write_ipc`` method. The helper
        intentionally writes uncompressed IPC because GenomeSpy's Arrow decoder
        does not support compressed IPC buffers yet.

    Args:
        data: A supported table or compatible object with
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

    payload = _try_to_arrow_ipc(data)
    if payload is not None:
        return payload

    if _is_pandas_frame(data):
        raise TypeError(
            "Serializing pandas DataFrames as Arrow IPC requires PyArrow. "
            "Install genome-spy-python[arrow]."
        )

    writer = getattr(data, "write_ipc", None)
    if not callable(writer):
        raise TypeError(
            "Arrow IPC serialization requires an object with "
            'write_ipc(file=None, compression="uncompressed").'
        )
    return _write_ipc_method(data)
