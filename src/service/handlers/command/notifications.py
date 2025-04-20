import ssl
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from domain.commands.notifications import SendEmailNotificationCommand, SendSMSNotificationCommand
from infrastructure.repositories.base import BaseNotificationRepository
from service.handlers.command.base import BaseCommandHandler
from settings.config import settings


@dataclass
class SendEmailNotificationCommandHandler(BaseCommandHandler):
    repo: BaseNotificationRepository

    async def __call__(self, command: SendEmailNotificationCommand):
        await self.repo.add(command.email_notification)
        sender = command.email_notification.sender.as_generic()
        receivers = [receiver.as_generic() for receiver in command.email_notification.receivers]

        if len(receivers) == 1:
            await self.send_targeted_mail(command, sender, receivers[0])
        else:
            await self.send_mass_mail(command, sender, receivers)

        produced_events = [
            # EmailNotificationSentEvent(
            #     ...
            # )
        ]
        command.email_notification.events.extend(produced_events)

    async def send_targeted_mail(
            self,
            command: SendEmailNotificationCommand,
            sender: str,
            receiver: str,
    ):
        message = MIMEMultipart('alternative')
        message['Subject'] = command.email_notification.subject
        message['From'] = sender
        message['To'] = receiver
        plain_part = MIMEText(command.email_notification.text, 'plain')
        html_part = MIMEText(command.email_notification.html, 'html')
        message.attach(plain_part), message.attach(html_part)

        async with aiosmtplib.SMTP(hostname=settings.SMTP_HOST, port=settings.SMTP_PORT) as smtp:
            await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            await smtp.sendmail(
                sender, receiver, message.as_string()
            )

    async def send_mass_mail(
            self,
            command: SendEmailNotificationCommand,
            sender: str,
            receivers: list[str],
    ):
        ...


@dataclass
class SendSMSNotificationCommandHandler(BaseCommandHandler):
    repo: BaseNotificationRepository

    async def __call__(self, command: SendSMSNotificationCommand):
        await self.repo.add(command.sms_notification)
        ...

        produced_events = [

        ]
        command.sms_notification.events.extend(produced_events)