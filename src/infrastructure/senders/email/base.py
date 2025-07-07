import logging
from abc import ABC, abstractmethod

from domain.entities.notifications import EmailNotificationEntity


logger = logging.getLogger(__name__)


class BaseEmailSender(ABC):
    async def send_email(
        self,
        email_notification: EmailNotificationEntity,
    ) -> None:
        if len(email_notification.receivers) > 1:
            await self.send_mass_email(
                sender=email_notification.sender.as_generic(),
                receivers=[receiver.as_generic() for receiver in email_notification.receivers],
                subject=email_notification.subject,
                text=email_notification.text,
                html=email_notification.html,
            )
        else:
            await self.send_targeted_email(
                sender=email_notification.sender.as_generic(),
                receiver=email_notification.receivers[0].as_generic(),
                subject=email_notification.subject,
                text=email_notification.text,
                html=email_notification.html,
            )

    @abstractmethod
    async def send_targeted_email(
        self,
        sender: str,
        receiver: str,
        subject: str,
        text: str,
        html: str | None = None,
    ) -> None:
        ...

    @abstractmethod
    async def send_mass_email(
        self,
        sender: str,
        receivers: list[str],
        subject: str,
        text: str,
        html: str | None = None,
    ) -> None:
        ...
