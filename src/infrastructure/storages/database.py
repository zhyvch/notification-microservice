from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from infrastrusture.models import UserCredentialModel
from settings.config import settings

async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URL)

    await init_beanie(
        database=client[settings.MONGODB_DATABASE],
        document_models=[UserCredentialModel]
    )
