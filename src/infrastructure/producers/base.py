from abc import ABC, abstractmethod

from domain.events.base import BaseEvent


class BaseProducer(ABC):
    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()

    @abstractmethod
    async def start(self):
        ...

    @abstractmethod
    async def stop(self):
        ...

    @abstractmethod
    async def publish(self, event: BaseEvent, topic: str):
        ...
