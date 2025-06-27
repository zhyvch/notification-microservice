from enum import Enum
from uuid import UUID
from beanie import Document


class NotificationType(Enum):
    EMAIL = 'email'
    SMS = 'sms'


class NotificationModel(Document):
    id: UUID
    notification_type: NotificationType
    sender: str
    receivers: list[str]
    message: str

    class Settings:
        name = 'notifications'


class NotificationTemplateModel(Document):
    name: str
    text_template: str
    html_template: str | None

    class Settings:
        name = 'notification_templates'
