export function toUint8Array(payload) {
  if (payload instanceof ArrayBuffer) {
    return new Uint8Array(payload);
  }
  if (ArrayBuffer.isView(payload)) {
    return new Uint8Array(payload.buffer, payload.byteOffset, payload.byteLength);
  }
  throw new TypeError("Arrow IPC payload must be an ArrayBuffer or typed-array view.");
}

export function revokeObjectUrls(urls, revoke = URL.revokeObjectURL) {
  for (const url of urls) {
    revoke(url);
  }
}

export function releaseInFlightResources(resources, revoke = URL.revokeObjectURL) {
  for (const resource of resources) {
    revokeObjectUrls(resource.objectUrls, revoke);
  }
  resources.clear();
}

export function createRenderSpec(
  spec,
  arrowData,
  { createUrl = URL.createObjectURL, revokeUrl = URL.revokeObjectURL } = {}
) {
  const renderSpec = structuredClone(spec);
  const objectUrls = [];
  const urlsByName = new Map();

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
      if (payload === undefined) {
        throw new Error(`No Arrow IPC payload provided for ${name}.`);
      }
      if (value.format?.type && value.format.type !== "arrow") {
        throw new Error(`Arrow data source ${name} must use format.type "arrow".`);
      }
      let url = urlsByName.get(name);
      if (!url) {
        url = createUrl(
          new Blob([toUint8Array(payload)], {
            type: "application/vnd.apache.arrow.file",
          })
        );
        urlsByName.set(name, url);
        objectUrls.push(url);
      }
      value.url = url;
      value.format = { ...(value.format || {}), type: "arrow" };
    }
    for (const child of Object.values(value)) {
      visit(child);
    }
  };

  try {
    visit(renderSpec);
    return { spec: renderSpec, objectUrls };
  } catch (error) {
    revokeObjectUrls(objectUrls, revokeUrl);
    throw error;
  }
}

export async function renderChart({ model, el, signal }) {
  if (!model.get("spec")) {
    el.textContent = "No GenomeSpy specification provided.";
    return;
  }

  let api = null;
  let parameterSubscriptions = [];
  let renderRevision = 0;
  let syncingParameterValues = false;
  const inFlightResources = new Set();

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

  const releaseResources = (resources) => {
    if (inFlightResources.delete(resources)) {
      revokeObjectUrls(resources.objectUrls);
    }
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
        model.set("clicked_datum", datum && typeof datum === "object" ? datum : {});
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
    const revision = ++renderRevision;
    const moduleUrl = model.get("bundle_url");
    const options = model.get("embed_options") || {};

    if (api?.finalize) {
      api.finalize();
      api = null;
    }
    releaseInFlightResources(inFlightResources);
    el.replaceChildren();

    let resources = null;
    try {
      const module = await import(moduleUrl);
      const embed = module.embed ?? module.default?.embed ?? module.default;
      if (typeof embed !== "function") {
        throw new Error("GenomeSpy embed export was not found.");
      }
      resources = createRenderSpec(model.get("spec"), model.get("arrow_data") || {});
      inFlightResources.add(resources);
      const nextApi = await embed(el, resources.spec, options);
      if (revision !== renderRevision || signal.aborted) {
        nextApi?.finalize?.();
        return;
      }
      api = nextApi;
      model.set("error", "");
      model.save_changes();
      attachInteractions();
    } catch (error) {
      if (revision !== renderRevision || signal.aborted) {
        return;
      }
      setError(error);
      throw error;
    } finally {
      if (resources) {
        releaseResources(resources);
      }
    }
  };

  const onSpecChange = () => void renderSpec();

  model.on("change:spec", onSpecChange);
  model.on("change:bundle_url", onSpecChange);
  model.on("change:embed_options", onSpecChange);
  model.on("change:arrow_data", onSpecChange);
  model.on("change:parameter_values", onParameterValuesChange);
  model.on("change:parameter_names", attachInteractions);
  model.on("change:enable_click_events", attachInteractions);

  signal.addEventListener("abort", () => {
    renderRevision += 1;
    model.off("change:spec", onSpecChange);
    model.off("change:bundle_url", onSpecChange);
    model.off("change:embed_options", onSpecChange);
    model.off("change:arrow_data", onSpecChange);
    model.off("change:parameter_values", onParameterValuesChange);
    model.off("change:parameter_names", attachInteractions);
    model.off("change:enable_click_events", attachInteractions);
    clearInteractions();
    api?.finalize?.();
    api = null;
    releaseInFlightResources(inFlightResources);
  });

  await renderSpec();
}

export default { render: renderChart };
