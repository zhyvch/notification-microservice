from contextlib import nullcontext as not_raises
from uuid import uuid4

import pytest


from domain.commands.notifications import (
    SendUserRegistrationCompletedMessageCommand,
    SendUserEmailUpdateInitiatedMessageCommand,
    SendUserPhoneNumberUpdateInitiatedMessageCommand,
    SendUserPasswordResetInitiatedMessageCommand,
    SendUserEmailUpdatedMessageCommand,
    SendUserPhoneNumberUpdatedMessageCommand, UserCredentialsStatus,
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
        'email, phone_number, credentials_status, expectation',
        [
            (
                EmailVO('example@example.com'),
                PhoneNumberVO('+1234567890'),
                UserCredentialsStatus.SUCCESS,
                not_raises(),
            ),
            (
                None,
                PhoneNumberVO('+1234567890'),
                UserCredentialsStatus.FAILED,
                not_raises(),
            ),
            (
                EmailVO('example@example.com'),
                None,
                UserCredentialsStatus.PENDING,
                not_raises(),
            ),
            (
                None,
                None,
                UserCredentialsStatus.SUCCESS,
                pytest.raises(InsufficientCredentialsInfoException),
            ),
        ]
    )
    async def test_send_user_registration_completed_message_command_handler(
        self,
        mongodb_db,
        email,
        phone_number,
        credentials_status,
        expectation,
        beanie_notification_template_repository,
        beanie_notification_repository,
        smtp_email_sender,
        twilio_sms_sender,
    ):
        with expectation:
            command = SendUserRegistrationCompletedMessageCommand(
                user_id=uuid4(),
                email=email,
                phone_number=phone_number,
                first_name=NameVO('John'),
                last_name=NameVO('Doe'),
                middle_name=NameVO('A.'),
                credentials_status=credentials_status,
            )
            handler = SendUserRegistrationCompletedMessageCommandHandler(
                notification_template_repo=beanie_notification_template_repository,
                notification_repo=beanie_notification_repository,
                email_sender=smtp_email_sender,
                sms_sender=twilio_sms_sender,
            )
            await handler(command)

            assert len(beanie_notification_repository.loaded_notifications) == 1
            notification = beanie_notification_repository.loaded_notifications.pop()
            assert len(notification.receivers) == 1
            receiver = notification.receivers[0]

            if email:
                assert notification.__class__ is EmailNotificationEntity
                assert receiver == email
            elif phone_number:
                assert notification.__class__ is SMSNotificationEntity
                assert receiver == phone_number

    @pytest.mark.parametrize(
        'new_email, verification_token, expectation',
        [
            (
                EmailVO('example@example.com'),
                'verification_token_123',
                not_raises(),
            ),
        ]
    )
    async def test_send_user_email_update_initiated_message_command_handler(
        self,
        mongodb_db,
        new_email,
        verification_token,
        expectation,
        beanie_notification_template_repository,
        beanie_notification_repository,
        smtp_email_sender,
    ):
        with expectation:
            command = SendUserEmailUpdateInitiatedMessageCommand(
                user_id=uuid4(),
                new_email=new_email,
                verification_token=verification_token
            )
            handler = SendUserEmailUpdateInitiatedMessageCommandHandler(
                notification_template_repo=beanie_notification_template_repository,
                notification_repo=beanie_notification_repository,
                email_sender=smtp_email_sender
            )
            await handler(command)

            assert len(beanie_notification_repository.loaded_notifications) == 1
            notification = beanie_notification_repository.loaded_notifications.pop()
            assert notification.__class__ is EmailNotificationEntity
            assert notification.receivers[0] == new_email

    @pytest.mark.parametrize(
        'new_phone_number, verification_token, expectation',
        [
            (
                PhoneNumberVO('+1234567890'),
                'verification_token_123',
                not_raises(),
            ),
        ]
    )
    async def test_send_user_phone_number_update_initiated_message_command_handler(
        self,
        mongodb_db,
        new_phone_number,
        verification_token,
        expectation,
        beanie_notification_template_repository,
        beanie_notification_repository,
        twilio_sms_sender,
    ):
        with expectation:
            command = SendUserPhoneNumberUpdateInitiatedMessageCommand(
                user_id=uuid4(),
                new_phone_number=new_phone_number,
                verification_token=verification_token
            )
            handler = SendUserPhoneNumberUpdateInitiatedMessageCommandHandler(
                notification_template_repo=beanie_notification_template_repository,
                notification_repo=beanie_notification_repository,
                sms_sender=twilio_sms_sender
            )
            await handler(command)

            assert len(beanie_notification_repository.loaded_notifications) == 1
            notification = beanie_notification_repository.loaded_notifications.pop()
            assert notification.__class__ is SMSNotificationEntity
            assert notification.receivers[0] == new_phone_number

    @pytest.mark.parametrize(
        'email, phone_number, verification_token, expectation',
        [
            (
                EmailVO('example@example.com'),
                PhoneNumberVO('+1234567890'),
                'verification_token_123',
                not_raises(),
            ),
            (
                None,
                PhoneNumberVO('+1234567890'),
                'verification_token_123',
                not_raises(),
            ),
            (
                EmailVO('example@example.com'),
                None,
                'verification_token_123',
                not_raises(),
            ),
            (
                None,
                None,
                'verification_token_123',
                pytest.raises(InsufficientCredentialsInfoException),
            ),
        ]
    )
    async def test_send_user_password_reset_initiated_message_command_handler(
        self,
        mongodb_db,
        email,
        phone_number,
        verification_token,
        expectation,
        beanie_notification_template_repository,
        beanie_notification_repository,
        smtp_email_sender,
        twilio_sms_sender,
    ):
        with expectation:
            command = SendUserPasswordResetInitiatedMessageCommand(
                user_id=uuid4(),
                email=email,
                phone_number=phone_number,
                verification_token=verification_token
            )
            handler = SendUserPasswordResetInitiatedMessageCommandHandler(
                notification_template_repo=beanie_notification_template_repository,
                notification_repo=beanie_notification_repository,
                email_sender=smtp_email_sender,
                sms_sender=twilio_sms_sender
            )
            await handler(command)

            assert len(beanie_notification_repository.loaded_notifications) == 1
            notification = beanie_notification_repository.loaded_notifications.pop()

            if email:
                assert notification.__class__ is EmailNotificationEntity
                assert notification.receivers[0] == email
            elif phone_number:
                assert notification.__class__ is SMSNotificationEntity
                assert notification.receivers[0] == phone_number

    @pytest.mark.parametrize(
        'new_email, expectation',
        [
            (
                EmailVO('example@example.com'),
                not_raises(),
            ),
        ]
    )
    async def test_send_user_email_updated_message_command_handler(
        self,
        mongodb_db,
        new_email,
        expectation,
        beanie_notification_template_repository,
        beanie_notification_repository,
        smtp_email_sender,
    ):
        with expectation:
            command = SendUserEmailUpdatedMessageCommand(
                user_id=uuid4(),
                new_email=new_email
            )
            handler = SendUserEmailUpdatedMessageCommandHandler(
                notification_template_repo=beanie_notification_template_repository,
                notification_repo=beanie_notification_repository,
                email_sender=smtp_email_sender
            )
            await handler(command)

            assert len(beanie_notification_repository.loaded_notifications) == 1
            notification = beanie_notification_repository.loaded_notifications.pop()
            assert notification.__class__ is EmailNotificationEntity
            assert notification.receivers[0] == new_email

    @pytest.mark.parametrize(
        'new_phone_number, expectation',
        [
            (
                PhoneNumberVO('+1234567890'),
                not_raises(),
            ),
        ]
    )
    async def test_send_user_phone_number_updated_message_command_handler(
        self,
        mongodb_db,
        new_phone_number,
        expectation,
        beanie_notification_template_repository,
        beanie_notification_repository,
        twilio_sms_sender,
    ):
        with expectation:
            command = SendUserPhoneNumberUpdatedMessageCommand(
                user_id=uuid4(),
                new_phone_number=new_phone_number
            )
            handler = SendUserPhoneNumberUpdatedMessageCommandHandler(
                notification_template_repo=beanie_notification_template_repository,
                notification_repo=beanie_notification_repository,
                sms_sender=twilio_sms_sender
            )
            await handler(command)

            assert len(beanie_notification_repository.loaded_notifications) == 1
            notification = beanie_notification_repository.loaded_notifications.pop()
            assert notification.__class__ is SMSNotificationEntity
            assert notification.receivers[0] == new_phone_number



