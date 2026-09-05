export function datasetApi(api, descriptor) {
  if (!descriptor.scoped) {
    return api.datasets;
  }
  if (!descriptor.owner) {
    throw new Error(
      `Dataset "${descriptor.name}" belongs to an unnamed nested view.`
    );
  }
  const owner = api.views?.get({ scope: [], view: descriptor.owner });
  if (!owner) {
    throw new Error(
      `Could not find the view that declares dataset "${descriptor.name}".`
    );
  }
  return owner.datasets;
}

export function setLoading(el, loading) {
  if (el.style) {
    el.style.visibility = loading ? "hidden" : "";
  }
}

export async function mountControls({
  container,
  api,
  names,
  definitions,
  moduleUrls,
}) {
  if (!names.length) {
    return null;
  }

  const controlsModule = await import(moduleUrls.core);
  const modules = { core: controlsModule };
  const controls = [];
  for (const name of names) {
    const definition = definitions[name];
    if (!definition) {
      throw new Error(`Control ${name} has no definition.`);
    }
    if (!modules[definition.module]) {
      const moduleUrl = moduleUrls[definition.module];
      if (!moduleUrl) {
        throw new Error(`Control module ${definition.module} has no URL.`);
      }
      modules[definition.module] = await import(moduleUrl);
    }
    const factory = modules[definition.module][definition.export];
    if (typeof factory !== "function") {
      throw new Error(`Control ${name} is unavailable.`);
    }
    controls.push(factory());
  }

  if (typeof controlsModule.attachControls !== "function") {
    throw new Error("GenomeSpy attachControls export was not found.");
  }
  return controlsModule.attachControls(container, api, { controls });
}

export async function renderChart({ model, el, signal }) {
  if (!model.get("spec")) {
    el.textContent = "No GenomeSpy specification provided.";
    return;
  }

  let api = null;
  let mountedControls = null;
  let parameterSubscriptions = [];
  let renderRevision = 0;
  let syncingParameterValues = false;
  const datasetListeners = [];
  const activeErrors = new Map();

  const publishErrors = () => {
    model.set("error", [...activeErrors.values()].join("\n"));
    model.save_changes();
  };

  const setError = (error, source = "runtime") => {
    activeErrors.delete(source);
    activeErrors.set(source, String(error));
    publishErrors();
  };

  const clearError = (source) => {
    if (activeErrors.delete(source)) {
      publishErrors();
    }
  };

  const disposeCurrent = ({ reportErrors = true } = {}) => {
    const controls = mountedControls;
    const currentApi = api;
    mountedControls = null;
    api = null;
    const errors = [];
    try {
      controls?.dispose?.();
    } catch (error) {
      errors.push(error);
    }
    try {
      currentApi?.finalize?.();
    } catch (error) {
      errors.push(error);
    }
    if (errors.length && reportErrors) {
      setError(errors.map(String).join("\n"), "cleanup");
    } else if (!errors.length) {
      clearError("cleanup");
    } else {
      console.error("GenomeSpy cleanup failed", ...errors);
    }
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

  const applyDataset = async (descriptor) => {
    const errorSource = `dataset:${descriptor.revision_trait}`;
    const revision = model.get(descriptor.revision_trait) || 0;
    const currentApi = api;
    const currentRender = renderRevision;
    if (!currentApi || revision === 0) {
      return;
    }

    const payload = model.get(descriptor.payload_trait);
    const format = model.get(descriptor.format_trait);
    try {
      const datasets = datasetApi(currentApi, descriptor);
      if (format === "arrow") {
        await datasets.load(descriptor.name, payload, { type: "arrow" });
      } else if (format === "records") {
        datasets.set(descriptor.name, payload);
      } else {
        throw new Error(`Unsupported dataset format: ${String(format)}`);
      }
      if (
        signal.aborted ||
        api !== currentApi ||
        renderRevision !== currentRender ||
        model.get(descriptor.revision_trait) !== revision
      ) {
        return;
      }
      clearError(errorSource);
    } catch (error) {
      if (
        !signal.aborted &&
        api === currentApi &&
        renderRevision === currentRender &&
        model.get(descriptor.revision_trait) === revision
      ) {
        setError(error, errorSource);
      }
    }
  };

  const renderSpec = async () => {
    const revision = ++renderRevision;
    const moduleUrl = model.get("bundle_url");
    const options = model.get("embed_options") || {};
    const controlNames = model.get("controls") || [];
    const datasets = model.get("dataset_manifest") || [];
    const hasInitialData = datasets.some(
      (descriptor) => (model.get(descriptor.revision_trait) || 0) > 0
    );

    disposeCurrent();
    setLoading(el, hasInitialData);
    el.replaceChildren();

    try {
      const module = await import(moduleUrl);
      const embed = module.embed ?? module.default?.embed ?? module.default;
      if (typeof embed !== "function") {
        throw new Error("GenomeSpy embed export was not found.");
      }
      const nextApi = await embed(el, model.get("spec"), options);
      if (revision !== renderRevision || signal.aborted) {
        nextApi?.finalize?.();
        return;
      }
      api = nextApi;
      clearError("render");
      try {
        const nextControls = await mountControls({
          container: el,
          api: nextApi,
          names: controlNames,
          definitions: model.get("_control_definitions") || {},
          moduleUrls: {
            core: model.get("controls_module_url"),
            inspector: model.get("inspector_module_url"),
          },
        });
        if (revision !== renderRevision || signal.aborted || api !== nextApi) {
          try {
            nextControls?.dispose?.();
          } catch (error) {
            console.error("GenomeSpy controls cleanup failed", error);
          }
          return;
        }
        mountedControls = nextControls;
        clearError("controls");
      } catch (error) {
        if (revision === renderRevision && !signal.aborted && api === nextApi) {
          setError(
            `GenomeSpy controls failed to load: ${String(error)}`,
            "controls"
          );
        }
      }
      attachInteractions();
      await Promise.all(datasets.map((descriptor) => applyDataset(descriptor)));
      if (revision === renderRevision && !signal.aborted) {
        setLoading(el, false);
      }
    } catch (error) {
      if (revision !== renderRevision || signal.aborted) {
        return;
      }
      setLoading(el, false);
      setError(error, "render");
      throw error;
    }
  };

  const onSpecChange = () => void renderSpec();

  model.on("change:spec", onSpecChange);
  model.on("change:bundle_url", onSpecChange);
  model.on("change:embed_options", onSpecChange);
  model.on("change:controls", onSpecChange);
  model.on("change:controls_module_url", onSpecChange);
  model.on("change:inspector_module_url", onSpecChange);
  model.on("change:parameter_values", onParameterValuesChange);
  model.on("change:parameter_names", attachInteractions);
  model.on("change:enable_click_events", attachInteractions);
  for (const descriptor of model.get("dataset_manifest") || []) {
    const listener = () => void applyDataset(descriptor);
    const event = `change:${descriptor.payload_trait}`;
    model.on(event, listener);
    datasetListeners.push([event, listener]);
  }

  signal.addEventListener("abort", () => {
    renderRevision += 1;
    model.off("change:spec", onSpecChange);
    model.off("change:bundle_url", onSpecChange);
    model.off("change:embed_options", onSpecChange);
    model.off("change:controls", onSpecChange);
    model.off("change:controls_module_url", onSpecChange);
    model.off("change:inspector_module_url", onSpecChange);
    model.off("change:parameter_values", onParameterValuesChange);
    model.off("change:parameter_names", attachInteractions);
    model.off("change:enable_click_events", attachInteractions);
    for (const [event, listener] of datasetListeners) {
      model.off(event, listener);
    }
    try {
      clearInteractions();
    } finally {
      disposeCurrent({ reportErrors: false });
      setLoading(el, false);
    }
  });

  await renderSpec();
}

export default { render: renderChart };
