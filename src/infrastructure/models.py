from uuid import UUID
from beanie import Document, Indexed
from pydantic import EmailStr


class UserCredentialModel(Document):
    user_id: UUID
    email: Indexed(EmailStr, unique=True)
    hashed_password: str

    class Settings:
        name = 'user_credentials'
