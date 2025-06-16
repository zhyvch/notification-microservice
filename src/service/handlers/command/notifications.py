import logging
from dataclasses import dataclass

from domain.commands.notifications import (
    SendUserRegistrationCompletedMessageCommand,
    SendUserEmailUpdateInitiatedMessageCommand,
    SendUserPhoneNumberUpdateInitiatedMessageCommand,
    SendUserPasswordResetInitiatedMessageCommand,
    SendUserEmailUpdatedMessageCommand,
    SendUserPhoneNumberUpdatedMessageCommand, UserCredentialsStatus,
)
from domain.entities.notifications import EmailNotificationEntity, SMSNotificationEntity
from domain.value_objects.notifications import EmailVO, PhoneNumberVO
from infrastructure.repositories.base import BaseNotificationRepository, BaseNotificationTemplateRepository
from infrastructure.senders.email.base import BaseEmailSender
from infrastructure.senders.sms.base import BaseSMSSender
from service.handlers.command.base import BaseCommandHandler
from settings.config import settings


logger = logging.getLogger(__name__)


@dataclass
class SendUserRegistrationCompletedMessageCommandHandler(BaseCommandHandler):
    notification_template_repo: BaseNotificationTemplateRepository
    notification_repo: BaseNotificationRepository
    email_sender: BaseEmailSender
    sms_sender: BaseSMSSender

    async def __call__(self, command: SendUserRegistrationCompletedMessageCommand):
        action_name = (
            'registration_successful' if command.credentials_status == UserCredentialsStatus.SUCCESS
            else 'registration_failed' if command.credentials_status == UserCredentialsStatus.FAILED
            else 'registration_pending'
        )
        notification_template = await self.notification_template_repo.get(action_name)
        initials = {
            'first_name': command.first_name.as_generic() if command.first_name else '',
            'last_name': command.last_name.as_generic() if command.last_name else '',
            'middle_name': command.middle_name.as_generic() if command.middle_name else '',
        }
        if command.email:
            notification = EmailNotificationEntity(
                sender=EmailVO(settings.FROM_EMAIL),
                receivers=[command.email],
                subject=action_name.replace('_', ' ').title(),
                text=notification_template['text_template'] % initials,
                html=notification_template['html_template'] % initials,
            )
            await self.notification_repo.add(notification)
            await self.email_sender.send_email(notification)
        else:
            notification = SMSNotificationEntity(
                sender=PhoneNumberVO(settings.FROM_PHONE_NUMBER),
                receivers=[command.phone_number],
                text=notification_template['text_template'] % initials,
            )
            await self.notification_repo.add(notification)
            await self.sms_sender.send_sms(notification)



@dataclass
class SendUserEmailUpdateInitiatedMessageCommandHandler(BaseCommandHandler):
    notification_template_repo: BaseNotificationTemplateRepository
    notification_repo: BaseNotificationRepository
    email_sender: BaseEmailSender

    async def __call__(self, command: SendUserEmailUpdateInitiatedMessageCommand):
        action_name = 'email_update_initiated'
        notification_template = await self.notification_template_repo.get(action_name)
        notification = EmailNotificationEntity(
            sender=EmailVO(settings.FROM_EMAIL),
            receivers=[command.new_email],
            subject=action_name.replace('_', ' ').title(),
            text=notification_template['text_template'] % {'verify_token': command.verification_token},
            html=notification_template['html_template'] % {'verify_token': command.verification_token},
        )
        await self.notification_repo.add(notification)
        await self.email_sender.send_email(notification)


@dataclass
class SendUserPhoneNumberUpdateInitiatedMessageCommandHandler(BaseCommandHandler):
    notification_template_repo: BaseNotificationTemplateRepository
    notification_repo: BaseNotificationRepository
    sms_sender: BaseSMSSender

    async def __call__(self, command: SendUserPhoneNumberUpdateInitiatedMessageCommand):
        action_name = 'phone_number_update_initiated'
        notification_template = await self.notification_template_repo.get(action_name)
        notification = SMSNotificationEntity(
            sender=PhoneNumberVO(settings.FROM_PHONE_NUMBER),
            receivers=[command.new_phone_number],
            text=notification_template['text_template'] % {'verify_token': command.verification_token},
        )
        await self.notification_repo.add(notification)
        await self.sms_sender.send_sms(notification)


@dataclass
class SendUserPasswordResetInitiatedMessageCommandHandler(BaseCommandHandler):
    notification_template_repo: BaseNotificationTemplateRepository
    notification_repo: BaseNotificationRepository
    email_sender: BaseEmailSender
    sms_sender: BaseSMSSender

    async def __call__(self, command: SendUserPasswordResetInitiatedMessageCommand):
        action_name = 'password_reset_initiated'
        notification_template = await self.notification_template_repo.get(action_name)
        if command.email:
            notification = EmailNotificationEntity(
                sender=EmailVO(settings.FROM_EMAIL),
                receivers=[command.email],
                subject=action_name.replace('_', ' ').title(),
                text=notification_template['text_template'] % {'verify_token': command.verification_token},
                html=notification_template['html_template'] % {'verify_token': command.verification_token},
            )
            await self.notification_repo.add(notification)
            await self.email_sender.send_email(notification)
        else:
            notification = SMSNotificationEntity(
                sender=PhoneNumberVO(settings.FROM_PHONE_NUMBER),
                receivers=[command.phone_number],
                text=notification_template['text_template'] % {'verify_token': command.verification_token},
            )
            await self.notification_repo.add(notification)
            await self.sms_sender.send_sms(notification)


@dataclass
class SendUserEmailUpdatedMessageCommandHandler(BaseCommandHandler):
    notification_template_repo: BaseNotificationTemplateRepository
    notification_repo: BaseNotificationRepository
    email_sender: BaseEmailSender

    async def __call__(self, command: SendUserEmailUpdatedMessageCommand):
        action_name = 'email_updated'
        notification_template = await self.notification_template_repo.get(action_name)
        notification = EmailNotificationEntity(
            sender=EmailVO(settings.FROM_EMAIL),
            receivers=[command.new_email],
            subject=action_name.replace('_', ' ').title(),
            text=notification_template['text_template'] % {'new_email': command.new_email.as_generic()},
            html=notification_template['html_template'] % {'new_email': command.new_email.as_generic()},
        )
        await self.notification_repo.add(notification)
        await self.email_sender.send_email(notification)


@dataclass
class SendUserPhoneNumberUpdatedMessageCommandHandler(BaseCommandHandler):
    notification_template_repo: BaseNotificationTemplateRepository
    notification_repo: BaseNotificationRepository
    sms_sender: BaseSMSSender

    async def __call__(self, command: SendUserPhoneNumberUpdatedMessageCommand):
        action_name = 'phone_number_updated'
        notification_template = await self.notification_template_repo.get(action_name)
        notification = SMSNotificationEntity(
            sender=PhoneNumberVO(settings.FROM_PHONE_NUMBER),
            receivers=[command.new_phone_number],
            text=notification_template['text_template'] % {'new_phone_number': command.new_phone_number.as_generic()},
        )
        await self.notification_repo.add(notification)
        await self.sms_sender.send_sms(notification)
