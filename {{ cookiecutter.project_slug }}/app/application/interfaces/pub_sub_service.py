from collections.abc import AsyncIterator
from typing import Protocol


class PubSubService(Protocol):
    async def init(self) -> None: ...

    async def publish(self, channel_name: str, payload: str) -> None: ...

    def subscribe(self, channel_name: str) -> AsyncIterator[str]: ...
