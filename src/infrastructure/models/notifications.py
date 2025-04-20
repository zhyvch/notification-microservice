from enum import Enum
from uuid import UUID
from beanie import Document


class NotificationType(Enum):
    EMAIL = 'email'
    SMS = 'sms'


class NotificationModel(Document):
    id: UUID
    notification_type: NotificationType
    email: str
    phone_number: str
    message: str

    class Settings:
        name = 'notifications'
