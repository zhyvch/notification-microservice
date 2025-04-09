from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.commands.base import BaseCommand


@dataclass
class BaseCommandHandler(ABC):
    @abstractmethod
    async def __call__(self, command: BaseCommand) -> None:
        ...
