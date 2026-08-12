import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const source = await readFile(
  new URL("../src/genome_spy/static/widget.js", import.meta.url),
  "utf8"
);
const { datasetApi, renderChart } = await import(
  `data:text/javascript,${encodeURIComponent(source)}`
);

class MockModel {
  constructor(values) {
    this.values = values;
    this.listeners = new Map();
    this.saved = 0;
  }

  get(name) {
    return this.values[name];
  }

  set(name, value) {
    this.values[name] = value;
  }

  save_changes() {
    this.saved += 1;
  }

  on(name, callback) {
    const callbacks = this.listeners.get(name) || new Set();
    callbacks.add(callback);
    this.listeners.set(name, callbacks);
  }

  off(name, callback) {
    this.listeners.get(name)?.delete(callback);
  }

  emit(name) {
    for (const callback of this.listeners.get(name) || []) {
      callback();
    }
  }
}

function deferred() {
  let resolve;
  let reject;
  const promise = new Promise((resolvePromise, rejectPromise) => {
    resolve = resolvePromise;
    reject = rejectPromise;
  });
  return { promise, resolve, reject };
}

async function waitFor(predicate) {
  for (let attempt = 0; attempt < 30; attempt += 1) {
    if (predicate()) {
      return;
    }
    await new Promise((resolve) => setImmediate(resolve));
  }
  assert.fail("Timed out waiting for widget state.");
}

function descriptor(name, index, { owner = null, scoped = false } = {}) {
  return {
    name,
    owner,
    scoped,
    payload_trait: `_dataset_${index}_payload`,
    format_trait: `_dataset_${index}_format`,
    revision_trait: `_dataset_${index}_revision`,
  };
}

function fixture(datasets = []) {
  const values = {
    spec: { data: { name: "table" }, datasets: { table: [] } },
    bundle_url:
      "data:text/javascript,export const embed=(...args)=>globalThis.__widgetEmbed(...args)",
    embed_options: {},
    dataset_manifest: datasets,
    parameter_names: [],
    parameter_values: {},
    enable_click_events: false,
    error: "",
  };
  for (const entry of datasets) {
    values[entry.payload_trait] = null;
    values[entry.format_trait] = "arrow";
    values[entry.revision_trait] = 0;
  }
  return {
    model: new MockModel(values),
    el: {
      textContent: "",
      style: {},
      replaceCount: 0,
      replaceChildren() {
        this.replaceCount += 1;
      },
    },
    controller: new AbortController(),
  };
}

function apiFixture({ load, set } = {}) {
  const loads = [];
  const sets = [];
  let finalized = 0;
  let parameterSubscriptions = 0;
  let clickListeners = 0;
  let removedClickListeners = 0;
  let clickHandler;
  const api = {
    datasets: {
      load: async (...args) => {
        loads.push(args);
        return load?.(...args);
      },
      set: (...args) => {
        sets.push(args);
        return set?.(...args);
      },
    },
    getParam() {
      return {
        getValue: () => 0,
        setValue() {},
        subscribe: () => {
          parameterSubscriptions += 1;
          return () => {};
        },
      };
    },
    addEventListener(type, listener) {
      if (type === "click") {
        clickListeners += 1;
        clickHandler = listener;
      }
    },
    removeEventListener(type, listener) {
      if (type === "click" && listener === clickHandler) {
        removedClickListeners += 1;
        clickHandler = undefined;
      }
    },
    finalize() {
      finalized += 1;
    },
  };
  return {
    api,
    loads,
    sets,
    get finalized() {
      return finalized;
    },
    get parameterSubscriptions() {
      return parameterSubscriptions;
    },
    get clickListeners() {
      return clickListeners;
    },
    get removedClickListeners() {
      return removedClickListeners;
    },
    get clickHandler() {
      return clickHandler;
    },
  };
}

test("datasetApi uses the top-level dataset API by default", () => {
  const api = { datasets: { load() {} } };

  assert.equal(datasetApi(api, descriptor("table", 0)), api.datasets);
});

test("datasetApi addresses a scoped declaration through its owner", () => {
  const ownerDatasets = { load() {} };
  const api = {
    views: { get: ({ scope, view }) => (scope.length === 0 && view === "child" ? { datasets: ownerDatasets } : undefined) },
  };

  assert.equal(
    datasetApi(api, descriptor("table", 0, { owner: "child", scoped: true })),
    ownerDatasets
  );
});

test("initial Arrow data passes the original DataView directly to Core", async () => {
  const entry = descriptor("table", 0);
  const testFixture = fixture([entry]);
  const payload = new DataView(Uint8Array.from([0, 7, 8, 0]).buffer, 1, 2);
  testFixture.model.set(entry.payload_trait, payload);
  testFixture.model.set(entry.revision_trait, 1);
  const rendered = apiFixture();
  globalThis.__widgetEmbed = async () => rendered.api;

  await renderChart({ ...testFixture, signal: testFixture.controller.signal });

  assert.equal(rendered.loads.length, 1);
  assert.deepEqual(rendered.loads[0], ["table", payload, { type: "arrow" }]);
  assert.equal(rendered.finalized, 0);
  assert.equal(testFixture.el.style.visibility, "");
  testFixture.controller.abort();
  delete globalThis.__widgetEmbed;
});

test("a dataset payload updates the current embed without structural rerender", async () => {
  const entry = descriptor("table", 0);
  const testFixture = fixture([entry]);
  const rendered = apiFixture();
  let embeds = 0;
  globalThis.__widgetEmbed = async () => {
    embeds += 1;
    return rendered.api;
  };

  await renderChart({ ...testFixture, signal: testFixture.controller.signal });
  const initialReplaceCount = testFixture.el.replaceCount;
  testFixture.model.set(entry.payload_trait, new Uint8Array([1, 2]));
  testFixture.model.set(entry.revision_trait, 1);
  testFixture.model.emit(`change:${entry.payload_trait}`);
  await waitFor(() => rendered.loads.length === 1);

  assert.equal(embeds, 1);
  assert.equal(rendered.finalized, 0);
  assert.equal(testFixture.el.replaceCount, initialReplaceCount);
  assert.equal(testFixture.el.style.visibility, "");
  testFixture.controller.abort();
  delete globalThis.__widgetEmbed;
});

test("a payload arriving after its revision loads the new bytes", async () => {
  const entry = descriptor("table", 0);
  const testFixture = fixture([entry]);
  const rendered = apiFixture();
  globalThis.__widgetEmbed = async () => rendered.api;

  await renderChart({ ...testFixture, signal: testFixture.controller.signal });
  testFixture.model.set(entry.revision_trait, 1);
  testFixture.model.emit(`change:${entry.revision_trait}`);
  await new Promise((resolve) => setImmediate(resolve));
  assert.equal(rendered.loads.length, 0);

  const payload = new Uint8Array([1, 2]);
  testFixture.model.set(entry.payload_trait, payload);
  testFixture.model.emit(`change:${entry.payload_trait}`);
  await waitFor(() => rendered.loads.length === 1);

  assert.equal(rendered.loads[0][1], payload);
  testFixture.controller.abort();
  delete globalThis.__widgetEmbed;
});

test("a dataset update retains parameter subscriptions and click listeners", async () => {
  const entry = descriptor("table", 0);
  const testFixture = fixture([entry]);
  testFixture.model.set("parameter_names", ["threshold"]);
  testFixture.model.set("parameter_values", { threshold: 2 });
  testFixture.model.set("enable_click_events", true);
  const rendered = apiFixture();
  globalThis.__widgetEmbed = async () => rendered.api;

  await renderChart({ ...testFixture, signal: testFixture.controller.signal });
  testFixture.model.set(entry.payload_trait, new Uint8Array([1]));
  testFixture.model.set(entry.revision_trait, 1);
  testFixture.model.emit(`change:${entry.payload_trait}`);
  await waitFor(() => rendered.loads.length === 1);

  assert.equal(rendered.parameterSubscriptions, 1);
  assert.equal(rendered.clickListeners, 1);
  assert.equal(rendered.removedClickListeners, 0);
  testFixture.controller.abort();
  assert.equal(rendered.removedClickListeners, 1);
  delete globalThis.__widgetEmbed;
});

test("repeated clicks publish the datum and advance the revision", async () => {
  const testFixture = fixture();
  testFixture.model.set("enable_click_events", true);
  const rendered = apiFixture();
  globalThis.__widgetEmbed = async () => rendered.api;

  await renderChart({ ...testFixture, signal: testFixture.controller.signal });
  const datum = {
    interaction_kind: "sequence_base",
    chrom: "chr1",
    pos0: 47239295,
    pos1: 47239296,
    base: "C",
  };
  rendered.clickHandler({ datum });
  rendered.clickHandler({ datum });

  assert.deepEqual(testFixture.model.get("clicked_datum"), datum);
  assert.equal(testFixture.model.get("click_revision"), 2);
  testFixture.controller.abort();
  delete globalThis.__widgetEmbed;
});

test("one dataset update does not apply unchanged datasets", async () => {
  const first = descriptor("first", 0);
  const second = descriptor("second", 1);
  const testFixture = fixture([first, second]);
  const rendered = apiFixture();
  globalThis.__widgetEmbed = async () => rendered.api;

  await renderChart({ ...testFixture, signal: testFixture.controller.signal });
  testFixture.model.set(first.payload_trait, new Uint8Array([1]));
  testFixture.model.set(first.revision_trait, 1);
  testFixture.model.emit(`change:${first.payload_trait}`);
  await waitFor(() => rendered.loads.length === 1);

  assert.equal(rendered.loads[0][0], "first");
  assert.equal(testFixture.model.get(second.revision_trait), 0);
  testFixture.controller.abort();
  delete globalThis.__widgetEmbed;
});

test("multiple rendered views apply pre-mount and future updates independently", async () => {
  const entry = descriptor("table", 0);
  const first = fixture([entry]);
  const second = fixture([entry]);
  const payload = new Uint8Array([1]);
  for (const current of [first, second]) {
    current.model.set(entry.payload_trait, payload);
    current.model.set(entry.revision_trait, 1);
  }
  const firstApi = apiFixture();
  const secondApi = apiFixture();
  let calls = 0;
  globalThis.__widgetEmbed = async () => [firstApi.api, secondApi.api][calls++];

  await Promise.all([
    renderChart({ ...first, signal: first.controller.signal }),
    renderChart({ ...second, signal: second.controller.signal }),
  ]);
  assert.equal(firstApi.loads.length, 1);
  assert.equal(secondApi.loads.length, 1);

  for (const current of [first, second]) {
    current.model.set(entry.payload_trait, new Uint8Array([2]));
    current.model.set(entry.revision_trait, 2);
    current.model.emit(`change:${entry.payload_trait}`);
  }
  await waitFor(() => firstApi.loads.length === 2 && secondApi.loads.length === 2);

  first.controller.abort();
  second.controller.abort();
  delete globalThis.__widgetEmbed;
});

test("a current decode failure reports an error without finalizing the embed", async () => {
  const entry = descriptor("table", 0);
  const testFixture = fixture([entry]);
  const rendered = apiFixture({ load: async () => { throw new Error("decode failed"); } });
  globalThis.__widgetEmbed = async () => rendered.api;

  await renderChart({ ...testFixture, signal: testFixture.controller.signal });
  testFixture.model.set(entry.payload_trait, new Uint8Array([1]));
  testFixture.model.set(entry.revision_trait, 1);
  testFixture.model.emit(`change:${entry.payload_trait}`);
  await waitFor(() => /decode failed/.test(testFixture.model.get("error")));

  assert.equal(rendered.finalized, 0);
  testFixture.controller.abort();
  delete globalThis.__widgetEmbed;
});

test("stale dataset failures do not overwrite a newer successful update", async () => {
  const entry = descriptor("table", 0);
  const testFixture = fixture([entry]);
  const first = deferred();
  const second = deferred();
  const rendered = apiFixture({
    load: () => (rendered.loads.length === 1 ? first.promise : second.promise),
  });
  globalThis.__widgetEmbed = async () => rendered.api;

  await renderChart({ ...testFixture, signal: testFixture.controller.signal });
  testFixture.model.set(entry.payload_trait, new Uint8Array([1]));
  testFixture.model.set(entry.revision_trait, 1);
  testFixture.model.emit(`change:${entry.payload_trait}`);
  await waitFor(() => rendered.loads.length === 1);
  testFixture.model.set(entry.payload_trait, new Uint8Array([2]));
  testFixture.model.set(entry.revision_trait, 2);
  testFixture.model.emit(`change:${entry.payload_trait}`);
  await waitFor(() => rendered.loads.length === 2);
  second.resolve();
  await waitFor(() => testFixture.model.get("error") === "");
  first.reject(new Error("stale failure"));
  await new Promise((resolve) => setImmediate(resolve));

  assert.equal(testFixture.model.get("error"), "");
  testFixture.controller.abort();
  delete globalThis.__widgetEmbed;
});

test("structural rerender finalizes the old embed and reapplies current data", async () => {
  const entry = descriptor("table", 0);
  const testFixture = fixture([entry]);
  testFixture.model.set(entry.payload_trait, new Uint8Array([1]));
  testFixture.model.set(entry.revision_trait, 1);
  const first = apiFixture();
  const second = apiFixture();
  let calls = 0;
  globalThis.__widgetEmbed = async () => [first.api, second.api][calls++];

  await renderChart({ ...testFixture, signal: testFixture.controller.signal });
  testFixture.model.emit("change:spec");
  await waitFor(() => second.loads.length === 1);

  assert.equal(first.finalized, 1);
  assert.equal(second.loads.length, 1);
  testFixture.controller.abort();
  delete globalThis.__widgetEmbed;
});

test("disposal removes dataset listeners and finalizes the current embed", async () => {
  const entry = descriptor("table", 0);
  const testFixture = fixture([entry]);
  const rendered = apiFixture();
  globalThis.__widgetEmbed = async () => rendered.api;

  await renderChart({ ...testFixture, signal: testFixture.controller.signal });
  testFixture.controller.abort();
  testFixture.model.set(entry.payload_trait, new Uint8Array([1]));
  testFixture.model.set(entry.revision_trait, 1);
  testFixture.model.emit(`change:${entry.payload_trait}`);
  await new Promise((resolve) => setImmediate(resolve));

  assert.equal(rendered.finalized, 1);
  assert.equal(rendered.loads.length, 0);
  delete globalThis.__widgetEmbed;
});
