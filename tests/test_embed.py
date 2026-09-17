"""Transport-independent tests for the thin embed proxies."""

import asyncio
from typing import Any

import pytest

from genome_spy.embed import EmbedError, IntervalSelectionApi, attach_embed


class Host:
    def __init__(self) -> None:
        self.listener: Any = None
        self.messages: list[dict[str, Any]] = []
        self.removed = False
        self.reply_enabled = True

    def subscribe(self, callback: Any) -> Any:
        self.listener = callback

        def remove() -> None:
            self.removed = True

        return remove

    def send(self, message: dict[str, Any]) -> None:
        self.messages.append(message)
        if not self.reply_enabled or message["method"] == "disconnect":
            return
        result: Any = None
        if message["method"] == "get":
            result = {"id": "threshold", "type": "param"}
        if message["method"] == "getSelection":
            result = {"id": "brush", "type": "interval"}
        if message["method"] == "getValue":
            result = {
                "type": "interval",
                "active": False,
                "intervals": {"x": None},
                "complexIntervals": {"x": None},
            }
        self.listener({**message, "embed": "first", "kind": "reply", "value": result})

    def event(self, subscription: str, value: Any, *, embed: str = "first") -> None:
        self.listener(
            {
                "channel": "genome-spy-embed",
                "client": self.messages[0]["client"],
                "kind": "event",
                "embed": embed,
                "subscription": subscription,
                "value": value,
            }
        )


def test_cross_loop_calls_fail_before_sending_or_closing() -> None:
    host = Host()
    with asyncio.Runner() as owner, asyncio.Runner() as other:
        api = owner.run(attach_embed(host.send, host.subscribe))
        parameter = owner.run(api.params.get("threshold"))
        count = len(host.messages)
        for operation in (
            parameter.set_value(42),
            parameter.subscribe(lambda value: None),
            api.finalize(),
        ):
            with pytest.raises(EmbedError, match="event loop used to attach"):
                other.run(operation)
            assert len(host.messages) == count
            assert not host.removed
        owner.run(parameter.set_value(7))
        assert host.messages[-1]["args"] == [7]
        owner.run(api.finalize())


def test_attachment_retries_when_frontend_misses_first_message() -> None:
    class DelayedHost(Host):
        connects = 0

        def send(self, message: dict[str, Any]) -> None:
            if message["method"] == "connect":
                self.connects += 1
                if self.connects == 1:
                    self.messages.append(message)
                    return  # No frontend listener yet: the message is dropped.
            super().send(message)

    async def run() -> None:
        host = DelayedHost()
        async with asyncio.timeout(2):
            api = await attach_embed(host.send, host.subscribe)
        assert host.connects == 2
        assert host.messages[0] == host.messages[1]
        await api.finalize()

    asyncio.run(run())


def test_attachment_retry_does_not_retry_writes() -> None:
    async def run() -> None:
        host = Host()
        api = await attach_embed(host.send, host.subscribe)
        parameter = await api.params.get("threshold")
        host.reply_enabled = False
        with pytest.raises(TimeoutError):
            await asyncio.wait_for(parameter.set_value(5), timeout=0.35)
        assert sum(m["method"] == "setValue" for m in host.messages) == 1
        host.reply_enabled = True
        await api.finalize()

    asyncio.run(run())


def test_mapping_explicit_reads_delivery_and_unsubscribe() -> None:
    async def run() -> None:
        host = Host()
        api = await attach_embed(host.send, host.subscribe)
        brush = await api.params.get_selection("brush")
        assert isinstance(brush, IntervalSelectionApi)
        assert brush.type == "interval"
        assert (await brush.get_value())["active"] is False
        values: list[Any] = []
        stop = await brush.subscribe(values.append)
        message = host.messages[-1]
        assert message["args"][1] is None  # Let upstream choose its default.
        assert values == []  # No synthetic initial callback.
        subscription = message["args"][0]
        host.event(subscription, 1, embed="stale")
        host.event(subscription, 2)
        host.event(subscription, 2)
        await asyncio.sleep(0)
        assert values == [2, 2]
        await stop()
        await stop()
        assert sum(m["method"] == "unsubscribe" for m in host.messages) == 1
        host.event(subscription, 3)
        await asyncio.sleep(0)
        assert values == [2, 2]
        await api.finalize()
        assert host.removed
        with pytest.raises(EmbedError, match="closed"):
            await brush.clear()

    asyncio.run(run())


def test_writes_and_serialization_fail_before_send() -> None:
    async def run() -> None:
        host = Host()
        api = await attach_embed(host.send, host.subscribe)
        param = await api.params.get("threshold")
        await param.set_value(5)
        assert host.messages[-1]["method"] == "setValue"
        assert host.messages[-1]["args"] == [5]
        await api.datasets.set("table", [{"x": 2}])
        assert host.messages[-1]["target"] == "datasets"
        count = len(host.messages)
        with pytest.raises(ValueError):
            await param.set_value(float("nan"))
        assert len(host.messages) == count
        await api.finalize()

    asyncio.run(run())


def test_disconnect_rejects_pending_call_and_never_rebinds() -> None:
    async def run() -> None:
        host = Host()
        api = await attach_embed(host.send, host.subscribe)
        host.reply_enabled = False
        pending = asyncio.create_task(api.params.get("waiting"))
        await asyncio.sleep(0)
        host.listener({**host.messages[-1], "embed": "first", "kind": "closed"})
        with pytest.raises(EmbedError, match="disposed"):
            await pending
        with pytest.raises(EmbedError, match="closed"):
            await api.params.get("replacement")
        assert host.removed

    asyncio.run(run())


def test_cancelled_attach_unregisters_transport() -> None:
    async def run() -> None:
        host = Host()
        host.reply_enabled = False
        task = asyncio.create_task(attach_embed(host.send, host.subscribe))
        await asyncio.sleep(0)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert host.removed
        assert host.messages[-1]["method"] == "disconnect"

    asyncio.run(run())


def test_cancelled_subscription_cleans_up_without_background_tasks() -> None:
    async def run() -> None:
        host = Host()
        api = await attach_embed(host.send, host.subscribe)
        brush = await api.params.get_selection("brush")
        host.reply_enabled = False
        values: list[Any] = []
        task = asyncio.create_task(brush.subscribe(values.append))
        await asyncio.sleep(0)
        subscription = host.messages[-1]["args"][0]
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert host.messages[-1]["method"] == "unsubscribe"
        assert host.messages[-1]["id"] is None
        assert host.messages[-1]["args"] == [subscription]
        assert asyncio.all_tasks() == {asyncio.current_task()}
        host.event(subscription, "late")
        await asyncio.sleep(0)
        assert values == []
        host.reply_enabled = True
        await api.finalize()

    asyncio.run(run())


@pytest.mark.parametrize("failure", ["send", "reply", "cancel"])
def test_failed_unsubscribe_can_be_retried(failure: str) -> None:
    class FailingHost(Host):
        attempts = 0

        def send(self, message: dict[str, Any]) -> None:
            if message["method"] == "unsubscribe":
                self.attempts += 1
                if self.attempts == 1:
                    if failure == "send":
                        raise OSError("temporary send failure")
                    if failure == "reply":
                        self.listener(
                            {
                                **message,
                                "embed": "first",
                                "kind": "reply",
                                "error": "temporary browser failure",
                            }
                        )
                    return
            super().send(message)

    async def run() -> None:
        host = FailingHost()
        api = await attach_embed(host.send, host.subscribe)
        brush = await api.params.get_selection("brush")
        stop = await brush.subscribe(lambda value: None)
        if failure == "cancel":
            task = asyncio.create_task(stop())
            await asyncio.sleep(0)
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
        else:
            with pytest.raises((OSError, EmbedError), match="temporary"):
                await stop()
        await stop()
        await stop()
        assert host.attempts == 2
        assert sum(m["method"] == "unsubscribe" for m in host.messages) == 1
        await api.finalize()

    asyncio.run(run())
