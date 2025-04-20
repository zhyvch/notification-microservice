from dataclasses import dataclass

from domain.commands.base import BaseCommand
from domain.entities.notifications import EmailNotificationEntity, SMSNotificationEntity


@dataclass
class SendEmailNotificationCommand(BaseCommand):
    email_notification: EmailNotificationEntity


@dataclass
class SendSMSNotificationCommand(BaseCommand):
    sms_notification: SMSNotificationEntity
