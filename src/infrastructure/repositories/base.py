from dataclasses import dataclass
from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.users import ...


@dataclass
class BaseRepository(ABC):
    async def get(self, email: str, hashed_password: str) -> ... | None:
        ...

    async def add(self, credentials: ...) -> None:
        ...

    async def update(self, user_id: UUID, credentials: ...) -> None:
        ...

    async def remove(self, user_id: UUID) -> None:
        ...
