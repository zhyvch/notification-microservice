from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from infrastructure.models.notifications import NotificationModel, NotificationTemplateModel
from settings.config import settings

async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URL)

    await init_beanie(
        database=client[settings.MONGODB_DB],
        document_models=[NotificationModel, NotificationTemplateModel]
    )

