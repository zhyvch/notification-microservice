import logging
from dataclasses import asdict

import pytest

from infrastructure.exceptions.notifications import MutuallyExclusiveFlagsException


logger = logging.getLogger(__name__)


@pytest.mark.asyncio
class TestSMTPEmailSender:
    async def test_mutually_exclusive_flags(self, smtp_email_sender):
        with pytest.raises(MutuallyExclusiveFlagsException):
            smtp_email_sender.use_tls, smtp_email_sender.use_ssl = True, True
            smtp_email_sender.__class__(**asdict(smtp_email_sender))
