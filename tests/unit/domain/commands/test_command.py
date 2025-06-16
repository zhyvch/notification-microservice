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
from domain.exceptions.notifications import InsufficientCredentialsInfoException
from domain.value_objects.notifications import NameVO, EmailVO, PhoneNumberVO



@pytest.mark.parametrize(
    'user_id, email, phone_number, first_name, last_name, middle_name, credentials_status, expected_exception',
    [
        (
            UUID('12345678-1234-5678-1234-567812345678'),
            EmailVO('example@email.com'),
            PhoneNumberVO('+1234567890'),
            NameVO('John'),
            NameVO('Doe'),
            NameVO('A.'),
            UserCredentialsStatus.PENDING,
            not_raises(),
        ),
        (
            UUID('12345678-1234-5678-1234-567812345678'),
            None,
            PhoneNumberVO('+1234567890'),
            NameVO('John'),
            None,
            None,
            UserCredentialsStatus.SUCCESS,
            not_raises(),
        ),
        (
            UUID('12345678-1234-5678-1234-567812345678'),
            EmailVO('example@email.com'),
            None,
            None,
            NameVO('Doe'),
            NameVO('A.'),
            UserCredentialsStatus.FAILED,
            not_raises(),
        ),
        (
            UUID('12345678-1234-5678-1234-567812345678'),
            None,
            None,
            NameVO('John'),
            None,
            None,
            UserCredentialsStatus.FAILED,
            pytest.raises(InsufficientCredentialsInfoException),
        ),
    ]
)
def test_send_user_registration_completed_message_command(
    user_id,
    email,
    phone_number,
    first_name,
    last_name,
    middle_name,
    credentials_status,
    expected_exception
):
    with expected_exception:
        command = SendUserRegistrationCompletedMessageCommand(
            user_id=user_id,
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            credentials_status=credentials_status,
        )


@pytest.mark.parametrize(
    'user_id, new_email, verification_token, expected_exception',
    [
        (
            UUID('12345678-1234-5678-1234-567812345678'),
            EmailVO('example@email.com'),
            'verification_token_123',
            not_raises(),
        ),
    ]
)
def test_send_user_email_update_initiated_message_command(
    user_id,
    new_email,
    verification_token,
    expected_exception,
):
    with expected_exception:
        command = SendUserEmailUpdateInitiatedMessageCommand(
            user_id=user_id,
            new_email=new_email,
            verification_token=verification_token,
        )


@pytest.mark.parametrize(
    'user_id, new_phone_number, verification_token, expected_exception',
    [
        (
            UUID('12345678-1234-5678-1234-567812345678'),
            PhoneNumberVO('+1234567890'),
            'verification_token_456',
            not_raises(),
        ),
    ]
)
def test_send_user_phone_number_update_initiated_message_command(
    user_id,
    new_phone_number,
    verification_token,
    expected_exception,
):
    with expected_exception:
        command = SendUserPhoneNumberUpdateInitiatedMessageCommand(
            user_id=user_id,
            new_phone_number=new_phone_number,
            verification_token=verification_token,
        )


@pytest.mark.parametrize(
    'user_id, email, phone_number, verification_token, expected_exception',
    [
        (
            UUID('12345678-1234-5678-1234-567812345678'),
            EmailVO('example@email.com'),
            PhoneNumberVO('+1234567890'),
            'verification_token_789',
            not_raises(),
        ),
        (
            UUID('12345678-1234-5678-1234-567812345678'),
            None,
            PhoneNumberVO('+1234567890'),
            'verification_token_789',
            not_raises(),
        ),
        (
            UUID('12345678-1234-5678-1234-567812345678'),
            EmailVO('example@email.com'),
            None,
            'verification_token_789',
            not_raises(),
        ),
        (
            UUID('12345678-1234-5678-1234-567812345678'),
            None,
            None,
            'verification_token_789',
            pytest.raises(InsufficientCredentialsInfoException),
        ),
    ]
)
def test_send_user_password_reset_initiated_message_command(
    user_id,
    email,
    phone_number,
    verification_token,
    expected_exception,
):
    with expected_exception:
        command = SendUserPasswordResetInitiatedMessageCommand(
            user_id=user_id,
            email=email,
            phone_number=phone_number,
            verification_token=verification_token,
        )


@pytest.mark.parametrize(
    'user_id, new_email, expected_exception',
    [
        (
            UUID('12345678-1234-5678-1234-567812345678'),
            EmailVO('example@email.com'),
            not_raises(),
        ),
    ]
)
def test_send_user_email_updated_message_command(
    user_id,
    new_email,
    expected_exception,
):
    with expected_exception:
        command = SendUserEmailUpdatedMessageCommand(
            user_id=user_id,
            new_email=new_email,
        )


@pytest.mark.parametrize(
    'user_id, new_phone_number, expected_exception',
    [
        (
            UUID('12345678-1234-5678-1234-567812345678'),
            PhoneNumberVO('+1234567890'),
            not_raises(),
        ),
    ]
)
def test_send_user_phone_number_updated_message_command(
    user_id,
    new_phone_number,
    expected_exception,
):
    with expected_exception:
        command = SendUserPhoneNumberUpdatedMessageCommand(
            user_id=user_id,
            new_phone_number=new_phone_number,
        )
