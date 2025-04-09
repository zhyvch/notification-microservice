from abc import ABC, abstractmethod

from domain.events.base import BaseEvent


class BaseProducer(ABC):
    @abstractmethod
    async def start(self):
        ...

    @abstractmethod
    async def stop(self):
        ...

    @abstractmethod
    async def publish(self, event: BaseEvent, topic: str):
        ...
