import pytest
import logging

from domain.commands.base import BaseCommand
from domain.events.base import BaseEvent
from service.handlers.command.base import BaseCommandHandler
from service.handlers.event.base import BaseEventHandler
from contextlib import nullcontext as not_raises
from service.exceptions.notifications import HandlerNotFoundException, WrongMessageBusMessageType


logger = logging.getLogger(__name__)


class SomeKnownEvent(BaseEvent):
    ...

class SomeKnownCommand(BaseCommand):
    ...

class SomeKnownEventEventHandler(BaseEventHandler):
    async def __call__(self, event: SomeKnownEvent) -> None:
        ...

class SomeKnownCommandCommandHandler(BaseCommandHandler):
    async def __call__(self, command: SomeKnownCommand) -> None:
        ...

class SomeUnknownEvent(BaseEvent):
    ...

class SomeUnknownCommand(BaseCommand):
    ...

class SomeUnrecognizedMessage:
    ...

@pytest.mark.asyncio
class TestMessageBus:
    @pytest.mark.parametrize(
        'message, expectation',
        [
            (SomeKnownEvent(), not_raises()),
            (SomeKnownCommand(), not_raises()),
            (SomeUnknownEvent(), not_raises()),
            (SomeUnknownCommand(), pytest.raises(HandlerNotFoundException)),
            (SomeUnrecognizedMessage(), pytest.raises(WrongMessageBusMessageType)),
        ]
    )
    async def test_messages(self, fake_message_bus, message, expectation):
        fake_message_bus.events_map = {SomeKnownEvent: [SomeKnownEventEventHandler(producer=None, topic=None)]}
        fake_message_bus.commands_map = {SomeKnownCommand: SomeKnownCommandCommandHandler()}
        with expectation:
            await fake_message_bus.handle(message)

