from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from infrastructure.models.notifications import NotificationModel, NotificationTemplateModel
from settings.config import settings

async def init_mongodb(client: AsyncIOMotorClient):
    await init_beanie(
        database=client[settings.MONGODB_DB],
        document_models=[NotificationModel, NotificationTemplateModel]
    )

