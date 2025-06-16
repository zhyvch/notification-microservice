from contextlib import nullcontext as not_raises
from uuid import UUID

import pytest

from domain.commands.notifications import (
    UserCredentialsStatus,
    SendUserRegistrationCompletedMessageCommand,
    SendUserEmailUpdateInitiatedMessageCommand,
    SendUserPhoneNumberUpdateInitiatedMessageCommand,
    SendUserPasswordResetInitiatedMessageCommand,
    SendUserEmailUpdatedMessageCommand,
    SendUserPhoneNumberUpdatedMessageCommand,
)
from domain.entities.notifications import EmailNotificationEntity, SMSNotificationEntity
from domain.exceptions.notifications import InsufficientCredentialsInfoException
from domain.value_objects.notifications import EmailVO, PhoneNumberVO, NameVO
from service.handlers.command.notifications import (
    SendUserRegistrationCompletedMessageCommandHandler,
    SendUserEmailUpdateInitiatedMessageCommandHandler,
    SendUserPhoneNumberUpdateInitiatedMessageCommandHandler,
    SendUserPasswordResetInitiatedMessageCommandHandler,
    SendUserEmailUpdatedMessageCommandHandler,
    SendUserPhoneNumberUpdatedMessageCommandHandler,
)


@pytest.mark.asyncio
class TestCommandHandlers:
    @pytest.mark.parametrize(
        'command, expectation',
        [
            (
                SendUserRegistrationCompletedMessageCommand(
                    user_id=UUID('12345678-1234-5678-1234-567812345678'),
                    email=EmailVO('example@example.com'),
                    phone_number=PhoneNumberVO('+1234567890'),
                    first_name=NameVO('John'),
                    last_name=NameVO('Doe'),
                    middle_name=NameVO('A.'),
                    credentials_status=UserCredentialsStatus.SUCCESS,
                ),
                not_raises(),
            ),
        ]
    )
    async def test_send_user_registration_completed_message_command_handler(
        self, command, expectation, fake_notification_template_repository, fake_notification_repository, fake_email_sender, fake_sms_sender, fake_consumer, fake_message_bus
    ):
        handler = SendUserRegistrationCompletedMessageCommandHandler(
            notification_template_repo=fake_notification_template_repository,
            notification_repo=fake_notification_repository,
            email_sender=fake_email_sender,
            sms_sender=fake_sms_sender,
        )
        async with fake_consumer:
            with expectation:
                await handler(command=command)
                produced_notification = fake_notification_repository.loaded_notifications.pop()
                assert await fake_notification_repository.get(notification_id=produced_notification.id) == produced_notification


    @pytest.mark.parametrize(
        'command, expectation',
        [
            (
                SendUserEmailUpdateInitiatedMessageCommand(
                    user_id=UUID('12345678-1234-5678-1234-567812345678'),
                    new_email=EmailVO('example@example.com'),
                    verification_token='verification_token_123',
                ),
                not_raises(),
            ),
        ]
    )
    async def test_send_user_email_update_initiated_message_command_handler(
        self, command, expectation, fake_notification_template_repository, fake_notification_repository, fake_email_sender, fake_consumer, fake_message_bus
    ):
        handler = SendUserEmailUpdateInitiatedMessageCommandHandler(
            notification_template_repo=fake_notification_template_repository,
            notification_repo=fake_notification_repository,
            email_sender=fake_email_sender,
        )
        async with fake_consumer:
            with expectation:
                await handler(command=command)
                produced_notification = fake_notification_repository.loaded_notifications.pop()
                assert await fake_notification_repository.get(notification_id=produced_notification.id) == produced_notification


    @pytest.mark.parametrize(
        'command, expectation',
        [
            (
                SendUserPhoneNumberUpdateInitiatedMessageCommand(
                    user_id=UUID('12345678-1234-5678-1234-567812345678'),
                    new_phone_number=PhoneNumberVO('+1234567890'),
                    verification_token='verification_token_456',
                ),
                not_raises(),
            ),
        ]
    )
    async def test_send_user_phone_number_update_initiated_message_command_handler(
        self, command, expectation, fake_notification_template_repository, fake_notification_repository, fake_sms_sender, fake_consumer, fake_message_bus
    ):
        handler = SendUserPhoneNumberUpdateInitiatedMessageCommandHandler(
            notification_template_repo=fake_notification_template_repository,
            notification_repo=fake_notification_repository,
            sms_sender=fake_sms_sender,
        )
        async with fake_consumer:
            with expectation:
                await handler(command=command)
                produced_notification = fake_notification_repository.loaded_notifications.pop()
                assert await fake_notification_repository.get(notification_id=produced_notification.id) == produced_notification


    @pytest.mark.parametrize(
        'command, expectation',
        [
            (
                SendUserPasswordResetInitiatedMessageCommand(
                    user_id=UUID('12345678-1234-5678-1234-567812345678'),
                    email=EmailVO('example@example.com'),
                    phone_number=PhoneNumberVO('+1234567890'),
                    verification_token='verification_token_789',
                ),
                not_raises(),
            ),
            (
                SendUserPasswordResetInitiatedMessageCommand(
                    user_id=UUID('12345678-1234-5678-1234-567812345678'),
                    email=None,
                    phone_number=PhoneNumberVO('+1234567890'),
                    verification_token='verification_token_789',
                ),
                not_raises(),
            ),
            (
                SendUserPasswordResetInitiatedMessageCommand(
                    user_id=UUID('12345678-1234-5678-1234-567812345678'),
                    email=EmailVO('example@example.com'),
                    phone_number=None,
                    verification_token='verification_token_789',
            ),
                not_raises(),
            ),
        ]
    )
    async def test_send_user_password_reset_initiated_message_command_handler(
        self, command, expectation, fake_notification_template_repository, fake_notification_repository, fake_email_sender, fake_sms_sender, fake_consumer, fake_message_bus
    ):
        handler = SendUserPasswordResetInitiatedMessageCommandHandler(
            notification_template_repo=fake_notification_template_repository,
            notification_repo=fake_notification_repository,
            email_sender=fake_email_sender,
            sms_sender=fake_sms_sender,
        )
        async with fake_consumer:
            with expectation:
                await handler(command=command)
                produced_notification = fake_notification_repository.loaded_notifications.pop()
                assert await fake_notification_repository.get(notification_id=produced_notification.id) == produced_notification

                if command.email:
                    assert produced_notification.__class__ is EmailNotificationEntity
                elif command.phone_number:
                    assert produced_notification.__class__ is SMSNotificationEntity


    @pytest.mark.parametrize(
        'command, expectation',
        [
            (
                SendUserEmailUpdatedMessageCommand(
                    user_id=UUID('12345678-1234-5678-1234-567812345678'),
                    new_email=EmailVO('example@example.com'),
                ),
                not_raises(),
            ),
        ]
    )
    async def test_send_user_email_updated_message_command_handler(
        self, command, expectation, fake_notification_template_repository, fake_notification_repository, fake_email_sender, fake_consumer, fake_message_bus
    ):
        handler = SendUserEmailUpdatedMessageCommandHandler(
            notification_template_repo=fake_notification_template_repository,
            notification_repo=fake_notification_repository,
            email_sender=fake_email_sender,
        )
        async with fake_consumer:
            with expectation:
                await handler(command=command)
                produced_notification = fake_notification_repository.loaded_notifications.pop()
                assert await fake_notification_repository.get(notification_id=produced_notification.id) == produced_notification


    @pytest.mark.parametrize(
        'command, expectation',
        [
            (
                SendUserPhoneNumberUpdatedMessageCommand(
                    user_id=UUID('12345678-1234-5678-1234-567812345678'),
                    new_phone_number=PhoneNumberVO('+1234567890'),
                ),
                not_raises(),
            ),
        ]
    )
    async def test_send_user_phone_number_updated_message_command_handler(
        self, command, expectation, fake_notification_template_repository, fake_notification_repository, fake_sms_sender, fake_consumer, fake_message_bus
    ):
        handler = SendUserPhoneNumberUpdatedMessageCommandHandler(
            notification_template_repo=fake_notification_template_repository,
            notification_repo=fake_notification_repository,
            sms_sender=fake_sms_sender,
        )
        async with fake_consumer:
            with expectation:
                await handler(command=command)
                produced_notification = fake_notification_repository.loaded_notifications.pop()
                assert await fake_notification_repository.get(notification_id=produced_notification.id) == produced_notification



