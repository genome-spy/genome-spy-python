"""Anywidget-backed notebook renderer for GenomeSpy charts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import anywidget
import traitlets

from genome_spy.chart import DEFAULT_EMBED_URL

_ESM_PATH = Path(__file__).with_name("static") / "widget.js"


class JupyterChart(anywidget.AnyWidget):
    """A lightweight anywidget wrapper around GenomeSpy's ``embed`` API."""

    _esm = _ESM_PATH

    spec = traitlets.Dict().tag(sync=True)
    bundle_url = traitlets.Unicode(DEFAULT_EMBED_URL).tag(sync=True)
    embed_options = traitlets.Dict(default_value={}).tag(sync=True)
    arrow_data = traitlets.Dict(default_value={}).tag(sync=True)
    parameter_names = traitlets.List(trait=traitlets.Unicode(), default_value=[]).tag(
        sync=True
    )
    parameter_values = traitlets.Dict(default_value={}).tag(sync=True)
    enable_click_events = traitlets.Bool(False).tag(sync=True)
    clicked_datum = traitlets.Dict(default_value={}).tag(sync=True)
    click_revision = traitlets.Int(0).tag(sync=True)
    error = traitlets.Unicode("").tag(sync=True)

    def __init__(
        self,
        chart: Any,
        *,
        bundle_url: str = DEFAULT_EMBED_URL,
        embed_options: dict[str, Any] | None = None,
        parameter_names: Sequence[str] = (),
        parameter_values: Mapping[str, Any] | None = None,
        enable_click_events: bool = False,
        **kwargs: Any,
    ) -> None:
        arrow_data: dict[str, bytes]
        if hasattr(chart, "_prepare_render"):
            prepared = chart._prepare_render()
            spec = prepared.spec
            arrow_data = prepared.buffers
        else:
            spec = dict(chart)
            arrow_data = {}

        super().__init__(
            spec=spec,
            bundle_url=bundle_url,
            embed_options=embed_options or {},
            arrow_data=arrow_data,
            parameter_names=list(parameter_names),
            parameter_values=dict(parameter_values or {}),
            enable_click_events=enable_click_events,
            **kwargs,
        )
