from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.events.base import BaseEvent
from infrastructure.producers.base import BaseProducer


@dataclass
class BaseEventHandler(ABC):
    producer: BaseProducer
    topic: str

    @abstractmethod
    async def __call__(self, event: BaseEvent) -> None:
        ...
