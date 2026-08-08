from __future__ import annotations

import io
import subprocess
import sys

import pandas as pd
import polars as pl
import pyarrow as pa
import pytest

import genome_spy as gs
from genome_spy import arrow


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


@pytest.mark.parametrize(
    ("table", "expected"),
    [
        (
            pa.table({"x": [1, 2], "label": ["A", "B"]}),
            [{"x": 1, "label": "A"}, {"x": 2, "label": "B"}],
        ),
        (
            pa.record_batch([[1, 2], ["A", "B"]], names=["x", "label"]),
            [{"x": 1, "label": "A"}, {"x": 2, "label": "B"}],
        ),
    ],
)
def test_to_arrow_ipc_round_trips_pyarrow_tables(
    table: pa.Table | pa.RecordBatch, expected: list[dict[str, object]]
) -> None:
    payload = gs.to_arrow_ipc(table)

    assert pa.ipc.open_file(payload).read_all().to_pylist() == expected


def test_to_arrow_ipc_round_trips_pandas_dataframe() -> None:
    frame = pd.DataFrame({"x": [1, 2], "label": ["A", "B"]})

    payload = gs.to_arrow_ipc(frame)

    assert pa.ipc.open_file(payload).read_all().to_pylist() == frame.to_dict(
        orient="records"
    )


@pytest.mark.parametrize(
    "table",
    [
        pa.table({"x": [1, 2]}),
        pd.DataFrame({"x": [1, 2]}),
    ],
)
def test_prepare_render_supports_pyarrow_and_pandas(table: object) -> None:
    chart = gs.Chart(table).mark_point().encode(x="x")

    prepared = chart._prepare_render()

    assert len(prepared.buffers) == 1
    assert prepared.spec["data"]["format"] == {"type": "arrow"}
    assert chart.to_dict()["data"]["values"] == [{"x": 1}, {"x": 2}]


def test_pandas_falls_back_to_json_when_pyarrow_is_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    frame = pd.DataFrame({"x": [1, 2]})
    monkeypatch.setattr(arrow, "_load_pyarrow", lambda: None)

    prepared = gs.Chart(frame).mark_point().encode(x="x")._prepare_render()

    assert prepared.buffers == {}
    assert prepared.spec["data"] == {"values": [{"x": 1}, {"x": 2}]}
    with pytest.raises(TypeError, match="requires PyArrow"):
        gs.to_arrow_ipc(frame)


def test_importing_genome_spy_does_not_import_optional_table_libraries() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import genome_spy, sys; "
            "assert 'pandas' not in sys.modules; "
            "assert 'pyarrow' not in sys.modules",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr


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
