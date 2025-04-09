from abc import ABC, abstractmethod
from dataclasses import dataclass

from service.message_bus import MessageBus


@dataclass
class BaseExternalEventHandler(ABC):
    bus: MessageBus

    @abstractmethod
    async def __call__(self, body: dict) -> None:
        ...
