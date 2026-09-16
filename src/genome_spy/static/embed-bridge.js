// Transport edge only: dispatch an explicit subset of the public embed API.
// The host owns mounting and must call dispose before destroying/replacing api.
export function createEmbedBridge(api, send) {
  const embed = Array.from(globalThis.crypto.getRandomValues(new Uint32Array(4)),
    value => value.toString(16).padStart(8, "0")).join("");
  const clients = new Set();
  const handles = new Map();
  const subscriptions = new Map();
  let closed = false;
  let nextHandle = 0;

  function publish(message) {
    // Check the original value too: JSON calls toJSON before its replacer.
    // JSON.stringify itself handles traversal and cycle detection.
    const json = JSON.stringify(message, function (key, value) {
      const original = this[key];
      if (original !== null && typeof original === "object" &&
          (!Array.isArray(original) && ![Object.prototype, null].includes(Object.getPrototypeOf(original)) ||
           original !== value)) {
        throw new Error("Unsupported embed payload; expected JSON values.");
      }
      if (typeof value === "number" && !Number.isFinite(value)) {
        throw new Error("Cannot transport a nonfinite number.");
      }
      if (["undefined", "function", "symbol", "bigint"].includes(typeof value)) {
        throw new Error(`Cannot transport ${typeof value}.`);
      }
      return value;
    });
    send(JSON.parse(json));
  }

  const reply = (request, result) => {
    if (request.id !== null) publish({
      channel: "genome-spy-embed", kind: "reply", client: request.client,
      embed, id: request.id, ...result,
    });
    else if (result.error) console.error("GenomeSpy cleanup failed:", result.error);
  };

  function handle(client, value, type) {
    const id = String(++nextHandle);
    handles.set(id, { client, value, type });
    return { id, type };
  }

  function target(request) {
    if (request.target === "api") return { value: api, type: "api" };
    if (request.target === "params") return { value: api.params, type: "params" };
    if (request.target === "datasets") return { value: api.datasets, type: "datasets" };
    const entry = handles.get(request.target);
    if (!entry || entry.client !== request.client) throw new Error("Unknown embed handle.");
    return entry;
  }

  async function receive(request) {
    if (request?.channel !== "genome-spy-embed") return;
    if (request.embed !== null && request.embed !== embed) return;
    try {
      if (request.method === "disconnect" && request.target === "api") {
        for (const [key, stop] of subscriptions) {
          if (key.startsWith(`${request.client}:`)) {
            stop();
            subscriptions.delete(key);
          }
        }
        for (const [key, entry] of handles) {
          if (entry.client === request.client) handles.delete(key);
        }
        clients.delete(request.client);
        return;
      }
      if (closed) throw new Error("The browser embed was disposed.");
      if (request.method === "connect" && request.target === "api") {
        clients.add(request.client);
        reply(request, { value: null });
        return;
      }
      if (!clients.has(request.client) || request.embed !== embed) {
        throw new Error("Attach to this embed before calling methods.");
      }
      const { value, type } = target(request);
      const args = request.args;
      let result = null;
      if (type === "params" && ["get", "getSelection"].includes(request.method)) {
        const resolved = value[request.method](...args);
        result = handle(request.client, resolved, request.method === "get" ? "param" : resolved.type);
      } else if (["param", "point", "interval"].includes(type) && request.method === "subscribe") {
        const [id, options] = args;
        const key = `${request.client}:${id}`;
        if (subscriptions.has(key)) throw new Error("Duplicate subscription.");
        const listener = (value) => {
          try {
            publish({ channel: "genome-spy-embed", kind: "event", embed,
              client: request.client, subscription: id, value });
          } catch (error) {
            // A failed stream must be visible, not silently lose selected rows.
            publish({ channel: "genome-spy-embed", kind: "closed", embed,
              client: request.client, error: String(error) });
          }
        };
        subscriptions.set(key, value.subscribe(listener, options ?? undefined));
      } else if (request.method === "unsubscribe") {
        const key = `${request.client}:${args[0]}`;
        subscriptions.get(key)?.();
        subscriptions.delete(key);
      } else {
        const allowed = {
          api: ["finalize"], datasets: ["set", "reset"],
          param: ["getValue", "setValue"], point: ["getValue", "clear"],
          interval: ["getValue", "clear", "contains"],
        };
        if (!allowed[type]?.includes(request.method)) throw new Error("Unsupported embed method.");
        result = (await value[request.method](...args)) ?? null;
      }
      if (closed) throw new Error("The browser embed was disposed during the call.");
      reply(request, { value: result });
      if (type === "api" && request.method === "finalize") {
        try {
          dispose();
        } catch (error) {
          // The operation already replied; report cleanup without a second reply.
          console.error("GenomeSpy cleanup failed:", error);
        }
      }
    } catch (error) {
      reply(request, { error: String(error) });
    }
  }

  function dispose() {
    if (closed) return;
    closed = true;
    const errors = [];
    for (const stop of subscriptions.values()) {
      try {
        stop();
      } catch (error) {
        errors.push(error);
      }
    }
    subscriptions.clear();
    handles.clear();
    for (const client of clients) {
      try {
        publish({ channel: "genome-spy-embed", kind: "closed", client, embed });
      } catch (error) {
        errors.push(error);
      }
    }
    clients.clear();
    if (errors.length) throw new AggregateError(errors, "GenomeSpy bridge cleanup failed.");
  }

  return { receive, dispose };
}
