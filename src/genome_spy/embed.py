"""Thin, asynchronous proxies for a live GenomeSpy embed.

Browser execution and connection ownership belong to the host adapter. This
module deliberately has no widget or web-framework dependencies.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
import json
from typing import Any, Literal, TypedDict
from uuid import uuid4

__all__ = [
    "DatasetApi",
    "EmbedError",
    "EmbedResult",
    "IntervalSelectionApi",
    "ParamApi",
    "ParamNamespace",
    "PointSelectionApi",
    "SelectionOptions",
    "attach_embed",
]

Message = dict[str, Any]
Listener = Callable[[Any], None]
Unsubscribe = Callable[[], Awaitable[None]]


class EmbedError(RuntimeError):
    """An embed operation failed or its browser connection was lost."""


class SelectionOptions(TypedDict, total=False):
    """Upstream selection delivery options; the default is every change."""

    delivery: Literal["change", "commit"]


class _Connection:
    def __init__(self, send: Callable[[Message], None]) -> None:
        self.send = send
        self.loop = asyncio.get_running_loop()
        self.client = uuid4().hex
        self.embed: str | None = None
        self.pending: dict[str, asyncio.Future[Any]] = {}
        self.listeners: dict[str, Listener] = {}
        self.closed = False
        self.remove_listener: Callable[[], None] = lambda: None

    def receive(self, message: Message) -> None:
        if message.get("channel") == "genome-spy-embed":
            self.loop.call_soon_threadsafe(self._receive, message)

    def _receive(self, message: Message) -> None:
        if self.closed or message.get("client") != self.client:
            return
        if self.embed is not None and message.get("embed") != self.embed:
            return
        if message.get("kind") == "closed":
            if "error" in message:
                self.loop.call_exception_handler(
                    {
                        "message": "GenomeSpy subscription transport failed",
                        "exception": EmbedError(message["error"]),
                    }
                )
            self.close(
                EmbedError(message.get("error", "The browser embed was disposed."))
            )
        elif message.get("kind") == "event":
            callback = self.listeners.get(message["subscription"])
            if callback is not None:
                try:
                    callback(message["value"])
                except Exception as error:
                    self.loop.call_exception_handler(
                        {
                            "message": "GenomeSpy subscription callback failed",
                            "exception": error,
                        }
                    )
        elif message.get("kind") == "reply":
            future = self.pending.get(message.get("id", ""))
            if future is not None and not future.done():
                if "error" in message:
                    future.set_exception(EmbedError(message["error"]))
                else:
                    # Bind before processing any later messages from this embed.
                    if self.embed is None:
                        self.embed = message["embed"]
                    future.set_result(message.get("value"))

    def _send(
        self,
        target: str,
        method: str,
        args: tuple[Any, ...],
        request: str | None = None,
    ) -> None:
        message = {
            "channel": "genome-spy-embed",
            "client": self.client,
            "embed": self.embed,
            "id": request,
            "target": target,
            "method": method,
            "args": list(args),
        }
        # Fail before sending unsupported/nonfinite values rather than changing them.
        self.send(json.loads(json.dumps(message, allow_nan=False)))

    def check_loop(self) -> None:
        if asyncio.get_running_loop() is not self.loop:
            raise EmbedError(
                "Embed calls must run on the event loop used to attach. "
                "Schedule the call on that loop before invoking the API."
            )

    async def call(self, target: str, method: str, *args: Any) -> Any:
        self.check_loop()
        if self.closed:
            raise EmbedError("This embed connection is closed; attach to a live embed.")
        request = uuid4().hex
        future = self.loop.create_future()
        self.pending[request] = future
        try:
            self._send(target, method, args, request)
            # Frontends may drop custom messages before their renderer loads.
            # Only repeat the idempotent handshake, never data writes or actions.
            if method == "connect":
                while not future.done():
                    done, _ = await asyncio.wait([future], timeout=0.25)
                    if not done:
                        self._send(target, method, args, request)
            return await future
        finally:
            self.pending.pop(request, None)
            if not future.done():
                future.cancel()

    async def subscribe(
        self, target: str, callback: Listener, options: SelectionOptions | None = None
    ) -> Unsubscribe:
        self.check_loop()
        subscription = uuid4().hex
        self.listeners[subscription] = callback
        try:
            await self.call(target, "subscribe", subscription, options)
        except BaseException:
            self.listeners.pop(subscription, None)
            # Registration may already have reached the browser on cancellation.
            if not self.closed:
                self._notify(target, "unsubscribe", subscription)
            raise

        async def unsubscribe() -> None:
            if subscription in self.listeners:
                if not self.closed:
                    await self.call(target, "unsubscribe", subscription)
                self.listeners.pop(subscription, None)

        return unsubscribe

    def _notify(self, target: str, method: str, *args: Any) -> None:
        # Cleanup cannot wait for a peer that may already have disconnected.
        try:
            self._send(target, method, args)
        except Exception as send_error:
            self.loop.call_exception_handler(
                {
                    "message": "GenomeSpy connection cleanup failed",
                    "exception": send_error,
                }
            )

    def close(self, error: EmbedError) -> None:
        if self.closed:
            return
        self.closed = True
        self._notify("api", "disconnect")
        self.listeners.clear()
        for future in self.pending.values():
            if not future.done():
                future.set_exception(error)
        self.remove_listener()


class _Proxy:
    def __init__(self, connection: _Connection, target: str) -> None:
        self._connection = connection
        self._target = target


class ParamApi(_Proxy):
    """A live upstream parameter handle, obtained through ParamNamespace.get."""

    async def get_value(self) -> Any:
        """Read the current browser value.

        Description:
            This is an explicit read, not a cached Python property.
        Args:
            None.
        Returns:
            The upstream parameter value.
        Raises:
            EmbedError: If the browser rejects the call or the embed is gone.
        Example:
            >>> value = await parameter.get_value()
        """
        return await self._connection.call(self._target, "getValue")

    async def set_value(self, value: Any) -> None:
        """Write an upstream parameter value.

        Description:
            Computed parameters and unsupported point-selection writes fail.
            Interval writes use upstream's interval value representation.
        Args:
            value: JSON-compatible value to pass unchanged to GenomeSpy.
        Returns:
            None after the upstream setter returns.
        Raises:
            EmbedError: If the write fails or the embed is gone.
            TypeError: If the value is not JSON serializable.
            ValueError: If the value contains nonfinite numbers.
        Example:
            >>> await parameter.set_value(5)
        """
        await self._connection.call(self._target, "setValue", value)

    async def subscribe(self, listener: Listener) -> Unsubscribe:
        """Subscribe to future parameter changes.

        Description:
            Callbacks run synchronously on the attaching Python event loop.
            No initial value is injected. Callback errors go to that loop's
            exception handler. Read initial state with get_value explicitly.
        Args:
            listener: Callback receiving each upstream value.
        Returns:
            An async, idempotent unsubscribe function.
        Raises:
            EmbedError: If registration fails or the embed is gone.
        Example:
            >>> stop = await parameter.subscribe(values.append)
            >>> await stop()
        """
        return await self._connection.subscribe(self._target, listener)


class _SelectionApi(_Proxy):
    """Shared implementation of upstream selection operations."""

    async def get_value(self) -> dict[str, Any]:
        """Read a detached selection snapshot.

        Description:
            Fields retain upstream spelling. Point rows are dataflow rows,
            not indices into the original Python table.
        Args:
            None.
        Returns:
            The upstream snapshot, including type and active fields.
        Raises:
            EmbedError: If the read fails or the embed is gone.
        Example:
            >>> snapshot = await selection.get_value()
        """
        return dict(await self._connection.call(self._target, "getValue"))

    async def subscribe(
        self, listener: Listener, options: SelectionOptions | None = None
    ) -> Unsubscribe:
        """Subscribe to future selection updates.

        Description:
            Upstream defaults to change delivery. Commit must be requested
            explicitly. No initial callback, throttling or coalescing is added.
        Args:
            listener: Synchronous callback on the attaching Python event loop.
            options: Upstream delivery options.
        Returns:
            An async, idempotent unsubscribe function.
        Raises:
            EmbedError: If registration fails or the embed is gone.
        Example:
            >>> stop = await selection.subscribe(values.append, {"delivery": "commit"})
        """
        return await self._connection.subscribe(self._target, listener, options)

    async def clear(self) -> None:
        """Clear the selection through its upstream capability.

        Description:
            Publication of the cleared state follows GenomeSpy's semantics.
        Args:
            None.
        Returns:
            None after the upstream operation returns.
        Raises:
            EmbedError: If clearing fails or the embed is gone.
        Example:
            >>> await selection.clear()
        """
        await self._connection.call(self._target, "clear")


class PointSelectionApi(_SelectionApi):
    """Read/subscribe/clear capability for an upstream point selection."""

    type: str = "point"


class IntervalSelectionApi(_SelectionApi):
    """Upstream interval selection with canvas-coordinate containment."""

    type: str = "interval"

    async def contains(self, point: dict[str, float]) -> bool:
        """Test a canvas point against the current brush.

        Description:
            This remote read cannot synchronously cancel a browser input event.
        Args:
            point: x and y in canvas-relative CSS pixels, not genomic units.
        Returns:
            Whether the point is inside the upstream interval selection.
        Raises:
            EmbedError: If the call fails or the embed is gone.
        Example:
            >>> inside = await brush.contains({"x": 20, "y": 10})
        """
        return bool(await self._connection.call(self._target, "contains", point))


class ParamNamespace(_Proxy):
    """Parameters resolved in the authored top-level lexical scope."""

    async def get(self, name: str) -> ParamApi:
        """Resolve an upstream parameter.

        Description:
            Uses params.get, not legacy global getParam lookup.
        Args:
            name: Authored parameter name.
        Returns:
            A live parameter proxy.
        Raises:
            EmbedError: If lookup fails or the embed is gone.
        Example:
            >>> threshold = await api.params.get("threshold")
        """
        handle = await self._connection.call(self._target, "get", name)
        return ParamApi(self._connection, handle["id"])

    async def get_selection(
        self, name: str
    ) -> PointSelectionApi | IntervalSelectionApi:
        """Resolve an upstream selection capability.

        Description:
            Does not add writable point selections or snapshot assignment.
        Args:
            name: Authored selection name.
        Returns:
            A point or interval proxy matching the upstream capability.
        Raises:
            EmbedError: If lookup fails or the embed is gone.
        Example:
            >>> brush = await api.params.get_selection("brush")
        """
        handle = await self._connection.call(self._target, "getSelection", name)
        cls = (
            IntervalSelectionApi if handle["type"] == "interval" else PointSelectionApi
        )
        return cls(self._connection, handle["id"])


class DatasetApi(_Proxy):
    """Dataset operations for the exact authored top-level owner."""

    async def set(self, name: str, data: list[Any]) -> None:
        """Replace a declared dataset with JSON-compatible rows.

        Description:
            Passes records directly to datasets.set; does not search descendants
            or use the widget's construction-time dataset manifest.
        Args:
            name: Declared dataset name.
            data: Replacement rows.
        Returns:
            None after the upstream operation returns, not after a render frame.
        Raises:
            EmbedError: If replacement fails or the embed is gone.
            TypeError: If rows are not JSON serializable.
            ValueError: If rows contain nonfinite numbers.
        Example:
            >>> await api.datasets.set("table", [{"x": 1}])
        """
        await self._connection.call(self._target, "set", name, data)

    async def reset(self, name: str) -> None:
        """Restore a dataset's configured values.

        Description:
            Delegates to the same owner's upstream datasets.reset method.
        Args:
            name: Declared dataset name.
        Returns:
            None after the upstream operation returns.
        Raises:
            EmbedError: If reset fails or the embed is gone.
        Example:
            >>> await api.datasets.reset("table")
        """
        await self._connection.call(self._target, "reset", name)


class EmbedResult(_Proxy):
    """Proxy for one live embed, obtained by a host using attach_embed.

    This first slice exposes params and datasets; the remaining upstream
    namespaces are not yet wrapped. Replacement requires a new proxy.
    """

    def __init__(self, connection: _Connection) -> None:
        super().__init__(connection, "api")
        self.params = ParamNamespace(connection, "params")
        self.datasets = DatasetApi(connection, "datasets")

    async def finalize(self) -> None:
        """Finalize the upstream embed and release this connection.

        Description:
            Only call when this Python client owns the embed lifecycle.
        Args:
            None.
        Returns:
            None after finalization.
        Raises:
            EmbedError: If upstream finalization fails or the embed is gone.
        Example:
            >>> await api.finalize()
        """
        self._connection.check_loop()
        try:
            await self._connection.call("api", "finalize")
        finally:
            self._connection.close(EmbedError("The embed was finalized."))


async def attach_embed(
    send: Callable[[Message], None],
    subscribe: Callable[[Callable[[Message], None]], Callable[[], None]],
) -> EmbedResult:
    """Attach Python to a host's live browser embed bridge.

    Description:
        Transport edge shared by notebook and non-notebook hosts. The browser
        must have createEmbedBridge attached to a live EmbedResult. Send must
        preserve message order. The host must dispose the bridge on teardown.
        Use asyncio.timeout around attachment when the frontend may be absent.
        All proxy calls must run on the event loop used for attachment.
    Args:
        send: Sends one JSON message to the browser bridge.
        subscribe: Registers an incoming-message callback and returns its remover.
    Returns:
        A thin proxy bound to this particular live embed.
    Raises:
        EmbedError: If browser attachment fails.
    Example:
        >>> api = await attach_embed(host.send, host.subscribe)
    """
    connection = _Connection(send)
    connection.remove_listener = subscribe(connection.receive)
    try:
        await connection.call("api", "connect")
    except BaseException:
        connection.close(EmbedError("Embed attachment failed."))
        raise
    return EmbedResult(connection)
