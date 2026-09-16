import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const source = await readFile(new URL("../src/genome_spy/static/embed-bridge.js", import.meta.url), "utf8");
const { createEmbedBridge } = await import(`data:text/javascript,${encodeURIComponent(source)}`);

function fixture() {
  let value = 1;
  let options;
  let finalized = 0;
  const listeners = new Set();
  const parameter = {
    getValue: () => value,
    setValue: (v) => { value = v; for (const listener of listeners) listener(v); },
    subscribe: (listener, opts) => {
      options = opts; listeners.add(listener); return () => listeners.delete(listener);
    },
    type: "interval", clear: () => parameter.setValue(null), contains: () => true,
  };
  const messages = [];
  const bridge = createEmbedBridge({
    params: { get: () => parameter, getSelection: () => parameter },
    datasets: { set: () => { throw Error("Unknown dataset"); } },
    finalize: () => finalized++,
  }, (message) => messages.push(message));
  let id = 0;
  const call = async (target, method, ...args) => {
    await bridge.receive({ channel: "genome-spy-embed", client: "client", embed: messages[0]?.embed ?? null,
      id: String(++id), target, method, args });
    return messages.at(-1);
  };
  return { bridge, messages, call, listeners, parameter, options: () => options, finalized: () => finalized };
}

test("upstream selection delivery, explicit read, no injected event, cleanup", async () => {
  const f = fixture();
  await f.call("api", "connect");
  const handle = (await f.call("params", "getSelection", "brush")).value;
  assert.equal(handle.type, "interval");
  await f.call(handle.id, "subscribe", "s", { delivery: "commit" });
  assert.deepEqual(f.options(), { delivery: "commit" });
  assert.equal(f.messages.filter(m => m.kind === "event").length, 0);
  assert.equal((await f.call(handle.id, "getValue")).value, 1);
  await f.call(handle.id, "clear");
  assert.equal(f.messages.find(m => m.kind === "event").value, null);
  await f.call(handle.id, "unsubscribe", "s");
  assert.equal(f.listeners.size, 0);
  f.bridge.dispose();
  assert.equal(f.messages.at(-1).kind, "closed");
});

test("browser errors and unsupported methods are explicit", async () => {
  const f = fixture();
  await f.call("api", "connect");
  assert.match((await f.call("datasets", "set", "missing", [])).error, /Unknown dataset/);
  assert.match((await f.call("api", "constructor")).error, /Unsupported/);
  const handle = (await f.call("params", "getSelection", "brush")).value;
  assert.match((await f.call(handle.id, "setValue", 1)).error, /Unsupported/);
});

test("stream serialization failures are visible and finalization disposes", async () => {
  const f = fixture();
  await f.call("api", "connect");
  const handle = (await f.call("params", "get", "threshold")).value;
  await f.call(handle.id, "subscribe", "s", null);
  f.parameter.setValue(NaN);
  assert.match(f.messages.at(-1).error, /nonfinite/);
  await f.call("api", "finalize");
  assert.equal(f.finalized(), 1);
  assert.equal(f.listeners.size, 0);
});

test("disconnect releases a client's subscriptions without finalizing its host", async () => {
  const f = fixture();
  await f.call("api", "connect");
  const handle = (await f.call("params", "get", "threshold")).value;
  await f.call(handle.id, "subscribe", "s", null);
  await f.call("api", "disconnect");
  assert.equal(f.listeners.size, 0);
  assert.equal(f.finalized(), 0);
  assert.match((await f.call(handle.id, "getValue")).error, /Attach/);
});

test("non-JSON values fail instead of silently changing on the wire", async () => {
  const f = fixture();
  await f.call("api", "connect");
  const handle = (await f.call("params", "get", "threshold")).value;
  f.parameter.setValue(new Date());
  assert.match((await f.call(handle.id, "getValue")).error, /Unsupported/);
  f.parameter.setValue({ missing: undefined });
  assert.match((await f.call(handle.id, "getValue")).error, /undefined/);
  const cyclic = {};
  cyclic.self = cyclic;
  f.parameter.setValue(cyclic);
  assert.match((await f.call(handle.id, "getValue")).error, /circular/i);
  f.parameter.setValue({ toJSON: () => "silently changed" });
  assert.match((await f.call(handle.id, "getValue")).error, /Unsupported/);
  const shared = { x: 1 };
  f.parameter.setValue([shared, shared]);
  assert.deepEqual((await f.call(handle.id, "getValue")).value, [{ x: 1 }, { x: 1 }]);
});

test("cancellation cleanup is a notification, not another pending request", async () => {
  const f = fixture();
  await f.call("api", "connect");
  const handle = (await f.call("params", "get", "threshold")).value;
  await f.call(handle.id, "subscribe", "s", null);
  const count = f.messages.length;
  await f.bridge.receive({ channel: "genome-spy-embed", client: "client",
    embed: f.messages[0].embed, id: null, target: handle.id,
    method: "unsubscribe", args: ["s"] });
  assert.equal(f.listeners.size, 0);
  assert.equal(f.messages.length, count);
});

test("a failed disposer does not prevent remaining cleanup or close notifications", async () => {
  const f = fixture();
  await f.call("api", "connect");
  const handle = (await f.call("params", "get", "threshold")).value;
  const stopped = [];
  let registrations = 0;
  f.parameter.subscribe = () => {
    const number = ++registrations;
    return () => {
      stopped.push(number);
      if (number === 1) throw Error("disposer failed");
    };
  };
  await f.call(handle.id, "subscribe", "first", null);
  await f.call(handle.id, "subscribe", "second", null);
  assert.throws(() => f.bridge.dispose(), error =>
    error instanceof AggregateError && error.errors[0].message === "disposer failed");
  assert.deepEqual(stopped, [1, 2]);
  assert.equal(f.messages.filter(m => m.kind === "closed").length, 1);
  assert.doesNotThrow(() => f.bridge.dispose());
  assert.deepEqual(stopped, [1, 2]);
});

test("one failed close notification does not prevent notifying other clients", async () => {
  const messages = [];
  const bridge = createEmbedBridge({}, message => {
    if (message.kind === "closed" && message.client === "first") throw Error("send failed");
    messages.push(message);
  });
  for (const client of ["first", "second"]) {
    await bridge.receive({channel: "genome-spy-embed", client, embed: null,
      id: client, target: "api", method: "connect", args: []});
  }
  assert.throws(() => bridge.dispose(), AggregateError);
  assert.deepEqual(messages.filter(m => m.kind === "closed").map(m => m.client), ["second"]);
});
