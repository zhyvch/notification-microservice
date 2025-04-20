from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.notifications import EmailNotificationEntity, SMSNotificationEntity


@dataclass
class BaseNotificationRepository(ABC):
    loaded_notifications: set[EmailNotificationEntity | SMSNotificationEntity] = field(default_factory=set, kw_only=True)

    @abstractmethod
    async def get(self, notification_id: UUID) -> EmailNotificationEntity | SMSNotificationEntity | None:
        ...

    @abstractmethod
    async def add(self, notification: EmailNotificationEntity | SMSNotificationEntity) -> None:
        ...

    @abstractmethod
    async def remove(self, notification_id: UUID) -> None:
        ...

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        add = cls.add
        get = cls.get

        async def _add(self, notification: EmailNotificationEntity | SMSNotificationEntity) -> None:
            await add(self, notification)
            self.loaded_notifications.add(notification)

        async def _get(self, notification_id: UUID) -> EmailNotificationEntity | SMSNotificationEntity | None:
            notification = await get(self, notification_id)
            if notification:
                self.loaded_notifications.add(notification)
            return notification

        cls.add = _add
        cls.get = _get
