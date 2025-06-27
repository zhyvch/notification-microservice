import logging
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
        return
        message = MIMEMultipart('alternative')
        message['Subject'], message['From'], message['To'] = subject, sender, receiver
        plain_part = MIMEText(text, 'plain')

        if html:
            html_part = MIMEText(html, 'html')
            message.attach(html_part)

        message.attach(plain_part)

        async with aiosmtplib.SMTP(hostname=self.host, port=self.port) as smtp:
            await smtp.login(self.username, self.password)
            await smtp.sendmail(
                sender, receiver, message.as_string()
            )

    async def send_mass_email(
        self,
        sender: str,
        receivers: list[str],
        subject: str,
        text: str,
        html: str | None = None,
    ) -> None:
        ...
