"""Anywidget-backed notebook renderer for GenomeSpy charts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import anywidget
import traitlets

from genome_spy.chart import DEFAULT_EMBED_URL

_ESM = """
async function renderChart({ model, el, signal }) {

  if (!model.get("spec")) {
    el.textContent = "No GenomeSpy specification provided.";
    return;
  }

  let api = null;
  let parameterSubscriptions = [];
  let arrowObjectUrls = [];
  let syncingParameterValues = false;

  const setError = (error) => {
    model.set("error", String(error));
    model.save_changes();
  };

  const publishParameterValue = (name, value) => {
    const values = { ...(model.get("parameter_values") || {}) };
    values[name] = value;
    syncingParameterValues = true;
    model.set("parameter_values", values);
    model.save_changes();
    syncingParameterValues = false;
  };

  const clearInteractions = () => {
    for (const unsubscribe of parameterSubscriptions) {
      unsubscribe();
    }
    parameterSubscriptions = [];
  };

  const revokeArrowObjectUrls = () => {
    for (const url of arrowObjectUrls) {
      URL.revokeObjectURL(url);
    }
    arrowObjectUrls = [];
  };

  const createRenderSpec = () => {
    const renderSpec = structuredClone(model.get("spec"));
    const arrowData = model.get("arrow_data") || {};

    const visit = (value) => {
      if (!value || typeof value !== "object") {
        return;
      }
      if (Array.isArray(value)) {
        for (const item of value) {
          visit(item);
        }
        return;
      }
      if (typeof value.url === "string" && value.url.startsWith("arrow://")) {
        const name = value.url.slice("arrow://".length);
        const payload = arrowData[name];
        if (!payload) {
          throw new Error(`No Arrow IPC payload provided for ${name}.`);
        }
        if (value.format?.type && value.format.type !== "arrow") {
          throw new Error(
            `Arrow data source ${name} must use format.type "arrow".`
          );
        }
        const url = URL.createObjectURL(
          new Blob([payload], { type: "application/vnd.apache.arrow.file" })
        );
        arrowObjectUrls.push(url);
        value.url = url;
        value.format = { ...(value.format || {}), type: "arrow" };
      }
      for (const child of Object.values(value)) {
        visit(child);
      }
    };

    visit(renderSpec);
    return renderSpec;
  };

  const attachInteractions = () => {
    if (!api) {
      return;
    }
    clearInteractions();

    for (const name of model.get("parameter_names") || []) {
      try {
        const parameter = api.getParam(name);
        const values = model.get("parameter_values") || {};
        if (Object.prototype.hasOwnProperty.call(values, name)) {
          parameter.setValue(values[name]);
        }
        parameterSubscriptions.push(
          parameter.subscribe((value) => publishParameterValue(name, value))
        );
        publishParameterValue(name, parameter.getValue());
      } catch (error) {
        setError(error);
      }
    }

    if (model.get("enable_click_events")) {
      const interactionApi = api;
      const onClick = (event) => {
        const datum = event?.datum;
        model.set(
          "clicked_datum",
          datum && typeof datum === "object" ? datum : {}
        );
        model.set("click_revision", (model.get("click_revision") || 0) + 1);
        model.save_changes();
      };
      interactionApi.addEventListener("click", onClick);
      parameterSubscriptions.push(() =>
        interactionApi.removeEventListener("click", onClick)
      );
    }
  };

  const onParameterValuesChange = () => {
    if (syncingParameterValues || !api) {
      return;
    }
    const values = model.get("parameter_values") || {};
    for (const name of model.get("parameter_names") || []) {
      if (!Object.prototype.hasOwnProperty.call(values, name)) {
        continue;
      }
      try {
        api.getParam(name).setValue(values[name]);
      } catch (error) {
        setError(error);
      }
    }
  };

  const renderSpec = async () => {
    const moduleUrl = model.get("bundle_url");
    const options = model.get("embed_options") || {};

    if (api && typeof api.finalize === "function") {
      api.finalize();
      api = null;
    }

    revokeArrowObjectUrls();
    el.replaceChildren();

    try {
      const module = await import(moduleUrl);
      const embed = module.embed ?? module.default?.embed ?? module.default;
      if (typeof embed !== "function") {
        throw new Error("GenomeSpy embed export was not found.");
      }
      api = await embed(el, createRenderSpec(), options);
      model.set("error", "");
      model.save_changes();
      attachInteractions();
    } catch (error) {
      revokeArrowObjectUrls();
      model.set("error", String(error));
      model.save_changes();
      throw error;
    }
  };

  const onSpecChange = async () => {
    await renderSpec();
  };

  model.on("change:spec", onSpecChange);
  model.on("change:bundle_url", onSpecChange);
  model.on("change:embed_options", onSpecChange);
  model.on("change:arrow_data", onSpecChange);
  model.on("change:parameter_values", onParameterValuesChange);
  model.on("change:parameter_names", attachInteractions);
  model.on("change:enable_click_events", attachInteractions);

  signal.addEventListener("abort", () => {
    model.off("change:spec", onSpecChange);
    model.off("change:bundle_url", onSpecChange);
    model.off("change:embed_options", onSpecChange);
    model.off("change:arrow_data", onSpecChange);
    model.off("change:parameter_values", onParameterValuesChange);
    model.off("change:parameter_names", attachInteractions);
    model.off("change:enable_click_events", attachInteractions);
    clearInteractions();
    if (api && typeof api.finalize === "function") {
      api.finalize();
      api = null;
    }
    revokeArrowObjectUrls();
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
        arrow_data: Mapping[str, bytes] | None = None,
        parameter_names: Sequence[str] = (),
        parameter_values: Mapping[str, Any] | None = None,
        enable_click_events: bool = False,
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
            arrow_data=dict(arrow_data or {}),
            parameter_names=list(parameter_names),
            parameter_values=dict(parameter_values or {}),
            enable_click_events=enable_click_events,
            **kwargs,
        )
