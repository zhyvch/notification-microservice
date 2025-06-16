import logging
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.notifications import EmailNotificationEntity, SMSNotificationEntity


logger = logging.getLogger(__name__)


@dataclass
class BaseNotificationRepository(ABC):
    loaded_notifications: set[EmailNotificationEntity | SMSNotificationEntity] = field(default_factory=set, kw_only=True)

    @abstractmethod
    async def add(
        self,
        notification: EmailNotificationEntity | SMSNotificationEntity,
    ) -> None:
        ...

    @abstractmethod
    async def get(
        self,
        notification_id: UUID,
    ) -> EmailNotificationEntity | SMSNotificationEntity:
        ...

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        logger.debug('Initializing repository subclass: %s', cls.__name__)

        add = cls.add
        get = cls.get

        async def _add(
            self,
            notification: EmailNotificationEntity | SMSNotificationEntity,
        ) -> None:
            logger.debug('Adding notification \'%s\' to repo', notification.id)
            await add(self, notification)
            self.loaded_notifications.add(notification)
            logger.debug('Notification \'%s\' added to loaded_notifications set', notification.id)

        async def _get(
            self,
            notification_id: UUID,
        ) -> EmailNotificationEntity | SMSNotificationEntity:
            logger.debug('Fetching notification with ID \'%s\'', notification_id)
            notification = await get(self, notification_id)
            self.loaded_notifications.add(notification)
            logger.debug('Notification \'%s\' added to loaded_notifications set', notification.id)
            return notification

        cls.add = _add
        cls.get = _get


class BaseNotificationTemplateRepository(ABC):
    @abstractmethod
    async def add(
        self,
        name: str,
        text_template: str,
        html_template: str | None = None,
    ) -> None:
        ...

    @abstractmethod
    async def get(
        self,
        name: str,
    ) -> dict[str, str]:
        ...
