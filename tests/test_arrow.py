from __future__ import annotations

import io

import polars as pl
import pytest

import genome_spy as gs


def test_to_arrow_ipc_round_trips_a_polars_frame() -> None:
    frame = pl.DataFrame(
        {
            "sample": ["A", "B"],
            "value": [1.5, None],
            "selected": [True, False],
        }
    )

    payload = gs.to_arrow_ipc(frame)

    assert payload[:6] == b"ARROW1"
    assert pl.read_ipc(io.BytesIO(payload)).equals(frame)


def test_to_arrow_ipc_requests_uncompressed_bytes() -> None:
    calls: list[tuple[object, str]] = []

    class Writer:
        def write_ipc(self, *, file: object, compression: str) -> bytes:
            calls.append((file, compression))
            return b"payload"

    assert gs.to_arrow_ipc(Writer()) == b"payload"
    assert calls == [(None, "uncompressed")]


@pytest.mark.parametrize("value", [object(), None])
def test_to_arrow_ipc_rejects_objects_without_a_writer(value: object) -> None:
    with pytest.raises(TypeError, match="write_ipc"):
        gs.to_arrow_ipc(value)


def test_to_arrow_ipc_rejects_empty_or_non_binary_writer_results() -> None:
    class EmptyWriter:
        def write_ipc(self, **_: object) -> bytes:
            return b""

    class TextWriter:
        def write_ipc(self, **_: object) -> str:
            return "not bytes"

    with pytest.raises(ValueError, match="empty"):
        gs.to_arrow_ipc(EmptyWriter())
    with pytest.raises(TypeError, match="bytes"):
        gs.to_arrow_ipc(TextWriter())
