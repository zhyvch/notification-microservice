from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.value_objects.notifications import EmailVO, PhoneNumberVO



@dataclass(eq=False)
class EmailNotificationEntity(BaseEntity):
    sender: EmailVO
    receivers: list[EmailVO]
    subject: str
    text: str
    html: str | None


@dataclass(eq=False)
class SMSNotificationEntity(BaseEntity):
    sender: PhoneNumberVO
    receivers: list[PhoneNumberVO]
    text: str
