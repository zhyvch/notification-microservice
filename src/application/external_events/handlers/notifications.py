from dataclasses import dataclass
from enum import Enum

from application.external_events.handlers.base import BaseExternalEventHandler
from domain.commands.notifications import SendEmailNotificationCommand
from domain.entities.notifications import EmailNotificationEntity
from domain.value_objects.notifications import EmailVO, PhoneNumberVO
from settings.config import settings

class UserCredentialsStatus(Enum):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'


@dataclass
class UserRegistrationCompletedExternalEventHandler(BaseExternalEventHandler):
    async def __call__(self, body: dict) -> None:
        initials = {
            'first_name': body['first_name'],
            'last_name': body['last_name'],
            'middle_name': body['middle_name']
        }
        status_based_response = {
            UserCredentialsStatus.SUCCESS: {
                'subject': 'Successful registration',
                'text': 'Dear %(first_name)s %(last_name)s %(middle_name)s we glad to inform you that your registration was successful!' % initials,
                'html': 'Dear <strong>%(first_name)s %(last_name)s %(middle_name)s</strong> we glad to inform you that your registration was successful!' % initials,
            },
            UserCredentialsStatus.FAILED: {
                'subject': 'Failed registration',
                'text': 'Dear %(first_name)s %(last_name)s %(middle_name)s we sorry to inform you that your registration was not successful!' % initials,
                'html': 'Dear <strong>%(first_name)s %(last_name)s %(middle_name)s</strong> we sorry to inform you that your registration was not successful!' % initials,
            },
        }[UserCredentialsStatus(body['credentials_status'])]

        notification = EmailNotificationEntity(
            sender=EmailVO(settings.FROM_EMAIL),
            receivers=[EmailVO(body['email'])],
            subject=status_based_response['subject'],
            text=status_based_response['text'],
            html=status_based_response['html'],
        )
        await self.bus.handle(SendEmailNotificationCommand(email_notification=notification))

