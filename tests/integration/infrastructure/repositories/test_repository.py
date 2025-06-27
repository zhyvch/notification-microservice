import logging
from uuid import uuid4

import pytest

from infrastructure.exceptions.notifications import NotificationTemplateNotFoundException, NotificationNotFoundException


logger = logging.getLogger(__name__)


@pytest.mark.asyncio
class TestBeanieNotificationRepository:
    async def test_add_get_email_notification(self, mongodb_db, random_email_notification_entity, beanie_notification_repository):
        await beanie_notification_repository.add(random_email_notification_entity)
        logger.info('Email notification "%s" added to DB', random_email_notification_entity.id)
        assert random_email_notification_entity in beanie_notification_repository.loaded_notifications

        result = await beanie_notification_repository.get(random_email_notification_entity.id)
        logger.info('Email notification "%s" read from DB', result.id)

        assert result.id == random_email_notification_entity.id
        assert result.receivers[0] == random_email_notification_entity.receivers[0]
        assert result.text == random_email_notification_entity.text
        assert result in beanie_notification_repository.loaded_notifications

    async def test_add_get_sms_notification(self, mongodb_db, random_sms_notification_entity, beanie_notification_repository):
        await beanie_notification_repository.add(random_sms_notification_entity)
        logger.info('SMS notification "%s" added to DB', random_sms_notification_entity.id)
        assert random_sms_notification_entity in beanie_notification_repository.loaded_notifications

        result = await beanie_notification_repository.get(random_sms_notification_entity.id)
        logger.info('SMS notification "%s" read from DB', result.id)

        assert result.id == random_sms_notification_entity.id
        assert result.receivers[0] == random_sms_notification_entity.receivers[0]
        assert result.text == random_sms_notification_entity.text
        assert result in beanie_notification_repository.loaded_notifications

    async def test_get_nonexistent_notification(self, mongodb_db, beanie_notification_repository):
        with pytest.raises(NotificationNotFoundException):
            await beanie_notification_repository.get(uuid4())


@pytest.mark.asyncio
class TestBeanieNotificationTemplateRepository:
    async def test_add_get_template(self, mongodb_db, beanie_notification_template_repository):
        template_name = 'test_template'
        text_template = 'Hello, {name}!'
        html_template = '<p>Hello, {name}!</p>'

        await beanie_notification_template_repository.add(
            name=template_name,
            text_template=text_template,
            html_template=html_template
        )
        logger.info('Template "%s" added to DB', template_name)

        result = await beanie_notification_template_repository.get(template_name)
        logger.info('Template "%s" read from DB', template_name)

        assert result['name'] == template_name
        assert result['text_template'] == text_template
        assert result['html_template'] == html_template

    async def test_add_get_template_without_html(self, mongodb_db, beanie_notification_template_repository):
        template_name = 'sms_template'
        text_template = 'Hello, {name}! This is an SMS.'

        await beanie_notification_template_repository.add(
            name=template_name,
            text_template=text_template
        )
        logger.info('Template "%s" added to DB', template_name)

        result = await beanie_notification_template_repository.get(template_name)
        logger.info('Template "%s" read from DB', template_name)

        assert result['name'] == template_name
        assert result['text_template'] == text_template
        assert result['html_template'] is None

    async def test_get_nonexistent_template(self, mongodb_db, beanie_notification_template_repository):
        with pytest.raises(NotificationTemplateNotFoundException):
            await beanie_notification_template_repository.get('nonexistent_template')