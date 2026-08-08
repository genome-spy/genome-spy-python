import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const source = await readFile(
  new URL("../src/genome_spy/static/widget.js", import.meta.url),
  "utf8"
);
const {
  createRenderSpec,
  releaseInFlightResources,
  renderChart,
  revokeObjectUrls,
  toUint8Array,
} = await import(`data:text/javascript,${encodeURIComponent(source)}`);

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
  for (let attempt = 0; attempt < 20; attempt += 1) {
    if (predicate()) {
      return;
    }
    await new Promise((resolve) => setImmediate(resolve));
  }
  assert.fail("Timed out waiting for widget render state.");
}

function renderFixture() {
  const model = new MockModel({
    spec: { data: { url: "arrow://table", format: { type: "arrow" } } },
    arrow_data: { table: new Uint8Array([1, 2, 3]) },
    bundle_url:
      "data:text/javascript,export const embed=(...args)=>globalThis.__widgetEmbed(...args)",
    embed_options: {},
    parameter_names: [],
    parameter_values: {},
    enable_click_events: false,
  });
  return {
    model,
    el: {
      textContent: "",
      replaceChildren() {},
    },
    controller: new AbortController(),
  };
}

async function withObjectUrlSpies(callback) {
  const originalCreate = URL.createObjectURL;
  const originalRevoke = URL.revokeObjectURL;
  const created = [];
  const revoked = [];
  URL.createObjectURL = () => {
    const url = `blob:test-${created.length + 1}`;
    created.push(url);
    return url;
  };
  URL.revokeObjectURL = (url) => revoked.push(url);
  try {
    await callback({ created, revoked });
  } finally {
    URL.createObjectURL = originalCreate;
    URL.revokeObjectURL = originalRevoke;
    delete globalThis.__widgetEmbed;
  }
}

test("toUint8Array preserves a DataView slice", () => {
  const payload = new DataView(Uint8Array.from([0, 1, 2, 3]).buffer, 1, 2);

  assert.deepEqual([...toUint8Array(payload)], [1, 2]);
});

test("createRenderSpec creates one Blob URL for repeated Arrow data", async () => {
  const created = [];
  const result = createRenderSpec(
    {
      layer: [
        { data: { url: "arrow://signals" } },
        { data: { url: "arrow://signals", format: { type: "arrow" } } },
      ],
    },
    { signals: new DataView(Uint8Array.from([0, 7, 8, 0]).buffer, 1, 2) },
    {
      createUrl: (blob) => {
        created.push(blob);
        return "blob:signals";
      },
    }
  );

  assert.equal(created.length, 1);
  assert.deepEqual([...new Uint8Array(await created[0].arrayBuffer())], [7, 8]);
  assert.equal(result.objectUrls.length, 1);
  assert.equal(result.spec.layer[0].data.url, "blob:signals");
  assert.equal(result.spec.layer[1].data.url, "blob:signals");
  assert.equal(result.spec.layer[0].data.format.type, "arrow");
});

test("createRenderSpec revokes already-created URLs when rewriting fails", () => {
  const revoked = [];

  assert.throws(
    () =>
      createRenderSpec(
        {
          layer: [
            { data: { url: "arrow://present" } },
            { data: { url: "arrow://missing" } },
          ],
        },
        { present: new Uint8Array([1]) },
        {
          createUrl: () => "blob:present",
          revokeUrl: (url) => revoked.push(url),
        }
      ),
    /No Arrow IPC payload provided for missing/
  );

  assert.deepEqual(revoked, ["blob:present"]);
});

test("revokeObjectUrls revokes each URL", () => {
  const revoked = [];

  revokeObjectUrls(["blob:a", "blob:b"], (url) => revoked.push(url));

  assert.deepEqual(revoked, ["blob:a", "blob:b"]);
});

test("releaseInFlightResources revokes stale render URLs", () => {
  const revoked = [];
  const resources = new Set([
    { objectUrls: ["blob:old-a", "blob:old-b"] },
    { objectUrls: ["blob:new"] },
  ]);

  releaseInFlightResources(resources, (url) => revoked.push(url));

  assert.deepEqual(revoked, ["blob:old-a", "blob:old-b", "blob:new"]);
  assert.equal(resources.size, 0);
});

test("renderChart revokes Arrow URLs after a successful embed", async () => {
  await withObjectUrlSpies(async ({ created, revoked }) => {
    const fixture = renderFixture();
    globalThis.__widgetEmbed = async () => ({ finalize() {} });

    await renderChart({
      model: fixture.model,
      el: fixture.el,
      signal: fixture.controller.signal,
    });

    assert.deepEqual(created, ["blob:test-1"]);
    assert.deepEqual(revoked, created);
    assert.equal(fixture.model.get("error"), "");
    fixture.controller.abort();
  });
});

test("renderChart reports embed failures and revokes Arrow URLs", async () => {
  await withObjectUrlSpies(async ({ created, revoked }) => {
    const fixture = renderFixture();
    globalThis.__widgetEmbed = async () => {
      throw new Error("embed failed");
    };

    await assert.rejects(
      renderChart({
        model: fixture.model,
        el: fixture.el,
        signal: fixture.controller.signal,
      }),
      /embed failed/
    );

    assert.deepEqual(revoked, created);
    assert.match(fixture.model.get("error"), /embed failed/);
    fixture.controller.abort();
  });
});

test("renderChart finalizes a stale render and keeps the latest one", async () => {
  await withObjectUrlSpies(async ({ created, revoked }) => {
    const fixture = renderFixture();
    const renders = [deferred(), deferred()];
    const finalized = [0, 0];
    let calls = 0;
    globalThis.__widgetEmbed = () => renders[calls++].promise;

    const initialRender = renderChart({
      model: fixture.model,
      el: fixture.el,
      signal: fixture.controller.signal,
    });
    await waitFor(() => calls === 1);
    fixture.model.emit("change:spec");
    await waitFor(() => calls === 2);

    renders[1].resolve({
      finalize() {
        finalized[1] += 1;
      },
    });
    await waitFor(() => fixture.model.get("error") === "");
    renders[0].resolve({
      finalize() {
        finalized[0] += 1;
      },
    });
    await initialRender;

    assert.equal(finalized[0], 1);
    assert.equal(finalized[1], 0);
    assert.deepEqual(revoked, created);

    fixture.controller.abort();
    assert.equal(finalized[1], 1);
  });
});

test("renderChart releases an in-flight render when disposed", async () => {
  await withObjectUrlSpies(async ({ created, revoked }) => {
    const fixture = renderFixture();
    const pending = deferred();
    let finalized = 0;
    globalThis.__widgetEmbed = () => pending.promise;

    const render = renderChart({
      model: fixture.model,
      el: fixture.el,
      signal: fixture.controller.signal,
    });
    await waitFor(() => created.length === 1);
    fixture.controller.abort();
    assert.deepEqual(revoked, created);

    pending.resolve({
      finalize() {
        finalized += 1;
      },
    });
    await render;
    assert.equal(finalized, 1);
  });
});
