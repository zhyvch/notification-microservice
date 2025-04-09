from dataclasses import dataclass

from domain.entities.users import ...
from infrastructure.models import ...
from infrastructure.repositories.base import BaseRepository


@dataclass
class BeanieRepository(BaseRepository):
    model: type[...]

    async def get(self, email: str, hashed_password: str) -> UserCredentialsEntity | None:
        user_creds = await self.model.find_one({'email': email})
        print(user_creds)

