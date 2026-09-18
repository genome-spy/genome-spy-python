"""Local-only web host. Run: uv run --with aiohttp server.py."""

import asyncio
from contextlib import suppress
from importlib.resources import files
import logging
from pathlib import Path

from aiohttp import WSMsgType, web

from component import annotate, chart
from genome_spy.embed import EmbedError, attach_embed

logger = logging.getLogger(__name__)


async def index(request):
    return web.FileResponse(Path(__file__).with_name("index.html"))


async def specification(request):
    return web.json_response(chart.to_dict())


async def javascript(request):
    name = request.match_info["name"]
    if name not in {"genome-spy.js", "embed-bridge.js"}:
        raise web.HTTPNotFound()
    source = files("genome_spy").joinpath("static", name).read_bytes()
    return web.Response(body=source, content_type="text/javascript")


async def websocket(request):
    # Do not let unrelated websites connect to this local Python process.
    if request.headers.get("Origin") != f"http://{request.host}":
        raise web.HTTPForbidden(text="A same-origin browser connection is required.")
    socket = web.WebSocketResponse(heartbeat=20)
    await socket.prepare(request)
    outgoing = asyncio.Queue()
    listeners = []
    annotations = []  # One Python list per connection, never shared between tabs.

    def subscribe(callback):
        listeners.append(callback)
        return lambda: listeners.remove(callback)

    async def send():
        # One writer preserves the order required by attach_embed.
        while True:
            await socket.send_json(await outgoing.get())

    async def receive():
        async for message in socket:
            if message.type == WSMsgType.TEXT:
                for callback in list(listeners):
                    callback(message.json())
            elif message.type == WSMsgType.ERROR:
                raise socket.exception()

    async def run_annotations():
        async with asyncio.timeout(30):
            api = await attach_embed(outgoing.put_nowait, subscribe)
        try:
            await annotate(
                api,
                annotations,
                lambda text: outgoing.put_nowait({"status": text}),
            )
        finally:
            with suppress(TimeoutError, EmbedError):
                async with asyncio.timeout(2):
                    await api.finalize()

    tasks = [asyncio.create_task(fn()) for fn in (send, receive, run_annotations)]
    try:
        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            task.result()
    except Exception:
        logger.exception("Annotation session failed")
    finally:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        await socket.close()
    return socket


def create_app():
    app = web.Application()
    app.add_routes(
        [
            web.get("/", index),
            web.get("/spec.json", specification),
            web.get("/static/{name}", javascript),
            web.get("/ws", websocket),
        ]
    )
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="127.0.0.1", port=8080)
