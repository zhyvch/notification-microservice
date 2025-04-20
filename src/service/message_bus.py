import logging
from dataclasses import dataclass, field
from typing import Union

from domain.commands.base import BaseCommand
from domain.events.base import BaseEvent

from infrastructure.repositories.base import BaseNotificationRepository
from service.handlers.command.base import BaseCommandHandler
from service.handlers.event.base import BaseEventHandler

logger = logging.getLogger(__name__)

Message = Union[BaseEvent, BaseCommand]


@dataclass
class MessageBus:
    repo: BaseNotificationRepository
    commands_map: dict[type[BaseCommand], BaseCommandHandler] = field(
        default_factory=dict,
        kw_only=True,
    )
    events_map: dict[type[BaseEvent], list[BaseEventHandler]] = field(
        default_factory=dict,
        kw_only=True,
    )
    queue: list[Message] = field(
        default_factory=list,
        kw_only=True
    )

    async def handle(self, message: Message):
        self.queue.append(message)
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, BaseCommand):
                await self._handle_command(message)
            elif isinstance(message, BaseEvent):
                await self._handle_event(message)
            else:
                raise Exception(f'{message} was not an Event or Command')

    async def _handle_command(self, command: BaseCommand):
        logger.debug('Handling command %s', command)
        try:
            handler = self.commands_map[command.__class__]
            await handler(command)
            self.queue.extend(self.collect_new_event())
        except Exception:
            logger.exception('Exception handling command %s', command)
            raise

    async def _handle_event(self, event: BaseEvent):
        for handler in self.events_map[event.__class__]:
            try:
                logger.debug('Handling event %s with handler %s', event, handler)
                await handler(event)
                self.queue.extend(self.collect_new_event())
            except Exception:
                logger.exception('Exception handling event %s', event)
                continue

    def collect_new_event(self):
        for notification in self.repo.loaded_notifications:
            while notification.events:
                yield notification.events.pop(0)
