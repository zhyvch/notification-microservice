from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID

from domain.commands.base import BaseCommand
from domain.exceptions.notifications import InsufficientCredentialsInfoException
from domain.value_objects.notifications import NameVO, EmailVO, PhoneNumberVO


class UserCredentialsStatus(Enum):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'


@dataclass
class SendUserRegistrationCompletedMessageCommand(BaseCommand):
    user_id: UUID
    email: EmailVO | None
    phone_number: PhoneNumberVO | None
    first_name: NameVO | None
    last_name: NameVO | None
    middle_name: NameVO | None
    credentials_status: UserCredentialsStatus

    def __post_init__(self):
        if not any([self.email, self.phone_number]):
            raise InsufficientCredentialsInfoException


@dataclass
class SendUserEmailUpdateInitiatedMessageCommand(BaseCommand):
    user_id: UUID
    new_email: EmailVO
    verification_token: str


@dataclass
class SendUserPhoneNumberUpdateInitiatedMessageCommand(BaseCommand):
    user_id: UUID
    new_phone_number: PhoneNumberVO
    verification_token: str


@dataclass
class SendUserPasswordResetInitiatedMessageCommand(BaseCommand):
    user_id: UUID
    email: EmailVO | None
    phone_number: PhoneNumberVO | None
    verification_token: str

    def __post_init__(self):
        if not any([self.email, self.phone_number]):
            raise InsufficientCredentialsInfoException


@dataclass
class SendUserEmailUpdatedMessageCommand(BaseCommand):
    user_id: UUID
    new_email: EmailVO


@dataclass
class SendUserPhoneNumberUpdatedMessageCommand(BaseCommand):
    user_id: UUID
    new_phone_number: PhoneNumberVO
