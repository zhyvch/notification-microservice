import logging
from dataclasses import dataclass

from application.external_events.handlers.base import BaseExternalEventHandler
from domain.commands.notifications import (
    SendUserRegistrationCompletedMessageCommand,
    UserCredentialsStatus,
    SendUserEmailUpdateInitiatedMessageCommand,
    SendUserPhoneNumberUpdateInitiatedMessageCommand,
    SendUserPasswordResetInitiatedMessageCommand,
    SendUserEmailUpdatedMessageCommand,
    SendUserPhoneNumberUpdatedMessageCommand,
)
from domain.value_objects.notifications import EmailVO, PhoneNumberVO, NameVO


logger = logging.getLogger(__name__)



@dataclass
class UserRegistrationCompletedExternalEventHandler(BaseExternalEventHandler):
    async def __call__(self, body: dict) -> None:
        await self.bus.handle(
            SendUserRegistrationCompletedMessageCommand(
                user_id=body['user_id'],
                email=EmailVO(body['email']) if body.get('email') else None,
                phone_number=PhoneNumberVO(body['phone_number']) if body.get('phone_number') else None,
                first_name=NameVO(body['first_name']) if body.get('first_name') else None,
                last_name=NameVO(body['last_name']) if body.get('last_name') else None,
                middle_name=NameVO(body['middle_name']) if body.get('middle_name') else None,
                credentials_status=UserCredentialsStatus(body['credentials_status']),
            )
        )


@dataclass
class UserEmailUpdateInitiatedExternalEventHandler(BaseExternalEventHandler):
    async def __call__(self, body: dict) -> None:
        await self.bus.handle(
            SendUserEmailUpdateInitiatedMessageCommand(
                user_id=body['user_id'],
                new_email=EmailVO(body['new_email']),
                verification_token=body['verification_token'],
            )
        )


@dataclass
class UserPhoneNumberUpdateInitiatedExternalEventHandler(BaseExternalEventHandler):
    async def __call__(self, body: dict) -> None:
        await self.bus.handle(
            SendUserPhoneNumberUpdateInitiatedMessageCommand(
                user_id=body['user_id'],
                new_phone_number=PhoneNumberVO(body['new_phone_number']),
                verification_token=body['verification_token'],
            )
        )


@dataclass
class UserPasswordResetInitiatedExternalEventHandler(BaseExternalEventHandler):
    async def __call__(self, body: dict) -> None:
        await self.bus.handle(
            SendUserPasswordResetInitiatedMessageCommand(
                user_id=body['user_id'],
                email=EmailVO(body['email']) if body.get('email') else None,
                phone_number=PhoneNumberVO(body['phone_number']) if body.get('phone_number') else None,
                verification_token=body['verification_token'],
            )
        )


@dataclass
class UserEmailUpdatedExternalEventHandler(BaseExternalEventHandler):
    async def __call__(self, body: dict) -> None:
        await self.bus.handle(
            SendUserEmailUpdatedMessageCommand(
                user_id=body['user_id'],
                new_email=EmailVO(body['new_email']),
            )
        )


@dataclass
class UserPhoneNumberUpdatedExternalEventHandler(BaseExternalEventHandler):
    async def __call__(self, body: dict) -> None:
        await self.bus.handle(
            SendUserPhoneNumberUpdatedMessageCommand(
                user_id=body['user_id'],
                new_phone_number=PhoneNumberVO(body['new_phone_number']),
            )
        )
