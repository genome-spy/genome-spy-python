"""Anywidget-backed notebook renderer for GenomeSpy charts."""

from __future__ import annotations

from typing import Any

import anywidget
import traitlets

from genome_spy.chart import DEFAULT_EMBED_URL

_ESM = """
async function renderChart({ model, el, signal }) {
  const moduleUrl = model.get("bundle_url");
  const spec = model.get("spec");
  const options = model.get("embed_options") || {};

  if (!spec) {
    el.textContent = "No GenomeSpy specification provided.";
    return;
  }

  let api = null;

  const renderSpec = async () => {
    if (api && typeof api.finalize === "function") {
      api.finalize();
      api = null;
    }

    el.replaceChildren();

    const module = await import(moduleUrl);
    const embed = module.embed ?? module.default?.embed ?? module.default;
    if (typeof embed !== "function") {
      throw new Error("GenomeSpy embed export was not found.");
    }
    api = await embed(el, spec, options);
  };

  const onSpecChange = async () => {
    await renderSpec();
  };

  model.on("change:spec", onSpecChange);
  model.on("change:bundle_url", onSpecChange);
  model.on("change:embed_options", onSpecChange);

  signal.addEventListener("abort", () => {
    model.off("change:spec", onSpecChange);
    model.off("change:bundle_url", onSpecChange);
    model.off("change:embed_options", onSpecChange);
    if (api && typeof api.finalize === "function") {
      api.finalize();
      api = null;
    }
  });

  await renderSpec();
}

export default { render: renderChart };
"""


class JupyterChart(anywidget.AnyWidget):
    """A lightweight anywidget wrapper around GenomeSpy's ``embed`` API."""

    _esm = _ESM

    spec = traitlets.Dict().tag(sync=True)
    bundle_url = traitlets.Unicode(DEFAULT_EMBED_URL).tag(sync=True)
    embed_options = traitlets.Dict(default_value={}).tag(sync=True)

    def __init__(
        self,
        chart: Any,
        *,
        bundle_url: str = DEFAULT_EMBED_URL,
        embed_options: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        if hasattr(chart, "to_dict"):
            spec = chart.to_dict()
        else:
            spec = dict(chart)

        super().__init__(
            spec=spec,
            bundle_url=bundle_url,
            embed_options=embed_options or {},
            **kwargs,
        )
