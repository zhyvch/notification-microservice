from dataclasses import dataclass

from service.exceptions.base import ServiceException


@dataclass(frozen=True, eq=False)
class MessageBusException(ServiceException):
    @property
    def message(self) -> str:
        return 'Message bus operation failed'


@dataclass(frozen=True, eq=False)
class WrongMessageBusMessageType(ServiceException):
    message_type: str

    @property
    def message(self) -> str:
        return f'Message bus received wrong message type {self.message_type}'


@dataclass(frozen=True, eq=False)
class HandlerNotFoundException(MessageBusException):
    message_type: str

    @property
    def message(self) -> str:
        return f'No handler found for message type: {self.message_type}'
