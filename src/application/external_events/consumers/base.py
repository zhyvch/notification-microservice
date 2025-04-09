from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from application.external_events.handlers.base import BaseExternalEventHandler


@dataclass
class BaseConsumer(ABC):
    external_events_map: dict[str, BaseExternalEventHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    @abstractmethod
    async def start(self):
        ...

    @abstractmethod
    async def consume(self):
        ...

    @abstractmethod
    async def stop(self):
        ...
