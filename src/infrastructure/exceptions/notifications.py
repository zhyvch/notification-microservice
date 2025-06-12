from dataclasses import dataclass
from uuid import UUID

from infrastructure.exceptions.base import InfrastructureException


@dataclass(frozen=True, eq=False)
class NotificationNotFoundException(InfrastructureException):
    notification_id: UUID

    @property
    def message(self) -> str:
        return f'Notification with ID <{self.notification_id}> not found'


@dataclass(frozen=True, eq=False)
class NotificationTemplateNotFoundException(InfrastructureException):
    name: str

    @property
    def message(self) -> str:
        return f'Notification template with name <{self.name}> not found'


@dataclass(frozen=True, eq=False)
class MutuallyExclusiveFlagsException(InfrastructureException):
    @property
    def message(self) -> str:
        return 'Both TLS and SSL flags cannot be set to True at the same time'
