import logging
from abc import ABC, abstractmethod

from domain.entities.notifications import SMSNotificationEntity


logger = logging.getLogger(__name__)


class BaseSMSSender(ABC):
    async def send_sms(
        self,
        sms_notification: SMSNotificationEntity,
    ) -> None:
        logger.warning(
            '\nSending sms from <%s> to <%s> \nwith text: %s',
            sms_notification.sender.as_generic(),
            ', '.join([receiver.as_generic() for receiver in sms_notification.receivers]),
            sms_notification.text,
        )
        if len(sms_notification.receivers) > 1:
            await self.send_mass_sms(
                sender=sms_notification.sender.as_generic(),
                receivers=[receiver.as_generic() for receiver in sms_notification.receivers],
                text=sms_notification.text,
            )
        else:
            await self.send_targeted_sms(
                sender=sms_notification.sender.as_generic(),
                receiver=sms_notification.receivers[0].as_generic(),
                text=sms_notification.text,
            )

    @abstractmethod
    async def send_targeted_sms(
        self,
        sender: str,
        receiver: str,
        text: str,
    ) -> None:
        ...

    @abstractmethod
    async def send_mass_sms(
        self,
        sender: str,
        receivers: list[str],
        text: str,
    ) -> None:
        ...
