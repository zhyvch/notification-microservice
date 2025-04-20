from dataclasses import dataclass
from uuid import UUID

from domain.entities.notifications import EmailNotificationEntity, SMSNotificationEntity
from infrastructure.models.notifications import NotificationModel
from infrastructure.repositories.base import BaseNotificationRepository


@dataclass
class BeanieNotificationRepository(BaseNotificationRepository):
    async def get(self, notification_id: UUID) -> EmailNotificationEntity | SMSNotificationEntity | None:
        notification = await NotificationModel.find_one({'id': notification_id})
        print(notification)

    async def add(self, notification: EmailNotificationEntity | SMSNotificationEntity) -> None:
        ...

    async def remove(self, notification_id: UUID) -> None:
        ...


