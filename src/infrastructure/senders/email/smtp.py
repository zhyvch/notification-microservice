import logging
import ssl

import aiosmtplib
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from infrastructure.exceptions.notifications import MutuallyExclusiveFlagsException
from infrastructure.senders.email.base import BaseEmailSender


logger = logging.getLogger(__name__)


@dataclass
class SMTPEmailSender(BaseEmailSender):
    host: str
    port: int
    username: str
    password: str
    use_tls: bool = False
    use_ssl: bool = False

    def __post_init__(self):
        if self.use_tls and self.use_ssl:
            raise MutuallyExclusiveFlagsException

    async def send_targeted_email(
            self,
            sender: str,
            receiver: str,
            subject: str,
            text: str,
            html: str | None = None,
    ) -> None:
        message = MIMEMultipart('alternative')
        message['Subject'], message['From'], message['To'] = subject, sender, receiver
        message.attach(MIMEText(text, 'plain'))

        if html:
            message.attach(MIMEText(html, 'html'))

        ssl_context = ssl.create_default_context()

        smtp_kwargs = {
            'hostname': self.host,
            'port': self.port,
            'tls_context': ssl_context,
            'start_tls': False,
        }

        if self.use_ssl:
            smtp_kwargs['use_tls'] = True
        elif self.use_tls:
            smtp_kwargs['start_tls'] = True

        async with aiosmtplib.SMTP(**smtp_kwargs) as smtp:
            await smtp.login(self.username, self.password)
            await smtp.sendmail(sender, receiver, message.as_string())


    async def send_mass_email(
        self,
        sender: str,
        receivers: list[str],
        subject: str,
        text: str,
        html: str | None = None,
    ) -> None:
        ...
