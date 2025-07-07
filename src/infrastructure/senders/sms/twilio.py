import logging
from dataclasses import dataclass

from twilio.rest import Client

from infrastructure.senders.sms.base import BaseSMSSender


logger = logging.getLogger(__name__)


@dataclass
class TwilioSMSSender(BaseSMSSender):
    account_sid: str
    auth_token: str

    async def send_targeted_sms(
        self,
        sender: str,
        receiver: str,
        text: str,
    ) -> None:
        client = Client(self.account_sid, self.auth_token)
        client.messages.create(from_=sender, body=text, to=receiver)

    async def send_mass_sms(
        self,
        sender: str,
        receivers: list[str],
        text: str,
    ) -> None:
        ...
