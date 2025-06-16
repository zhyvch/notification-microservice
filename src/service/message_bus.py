import logging
from dataclasses import dataclass, field
from typing import Union

from domain.commands.base import BaseCommand
from domain.events.base import BaseEvent

from infrastructure.repositories.base import BaseNotificationRepository
from service.exceptions.notifications import WrongMessageBusMessageType, HandlerNotFoundException
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
        logger.info('Processing message: %s', message.__class__.__name__)
        self.queue.append(message)

        try:
            while self.queue:
                message = self.queue.pop(0)
                if isinstance(message, BaseCommand):
                    await self._handle_command(message)
                elif isinstance(message, BaseEvent):
                    await self._handle_event(message)
                else:
                    logger.error('Unrecognized message type: %r', message)
                    raise WrongMessageBusMessageType(message.__class__.__name__)
        except Exception as e:
            logger.exception('Failed to process message queue')
            raise

        logger.info('Message queue processing completed')

    async def _handle_command(self, command: BaseCommand):
        logger.info('Handling command: %s', command.__class__.__name__)
        try:
            handler = self.commands_map.get(command.__class__)
            if not handler:
                logger.error('No handler found for command: %s', command.__class__.__name__)
                raise HandlerNotFoundException(command.__class__.__name__)

            logger.debug(
                'Using handler %s for command %s',
                handler.__class__.__name__,
                command.__class__.__name__
            )
            await handler(command)
            self.queue.extend(self.collect_new_event())
        except HandlerNotFoundException:
            raise
        except Exception as e:
            logger.exception(
                'Failed to handle command: %s',
                command.__class__.__name__,
                exc_info=e,
            )
            raise
        logger.info('Command handled successfully: %s', command.__class__.__name__)

    async def _handle_event(self, event: BaseEvent):
        logger.info('Handling event: %s', event.__class__.__name__)
        handlers = self.events_map.get(event.__class__)
        if not handlers:
            logger.error('No handlers registered for event: %s', event.__class__.__name__)
            return

        for handler in handlers:
            try:
                logger.debug(
                    'Using handler %s for event %s',
                    handler.__class__.__name__,
                    event.__class__.__name__
                )
                await handler(event)
                self.queue.extend(self.collect_new_event())
            except Exception as e:
                logger.exception(
                    'Handler %s failed for event %s',
                    handler.__class__.__name__,
                    event.__class__.__name__,
                    exc_info=e,
                )
        logger.info('Event handling completed: %s', event.__class__.__name__)

    def collect_new_event(self):
        for notification in self.repo.loaded_notifications:
            while notification.events:
                yield notification.events.pop(0)
