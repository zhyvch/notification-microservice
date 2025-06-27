import logging
from uuid import UUID

from domain.entities.notifications import EmailNotificationEntity, SMSNotificationEntity
from infrastructure.converters.notifications import convert_notification_entity_to_model, convert_notification_model_to_entity
from infrastructure.exceptions.notifications import NotificationTemplateNotFoundException, NotificationNotFoundException
from infrastructure.models.notifications import NotificationTemplateModel, NotificationModel
from infrastructure.repositories.base import BaseNotificationRepository, BaseNotificationTemplateRepository


logger = logging.getLogger(__name__)


class BeanieNotificationRepository(BaseNotificationRepository):
    async def add(
        self,
        notification: EmailNotificationEntity | SMSNotificationEntity,
    ) -> None:
        logger.debug('Adding notification with ID \'%s\'', notification.id)
        try:
            notification = convert_notification_entity_to_model(notification)
            await notification.insert()
            logger.debug('Notification with ID \'%s\' added to DB', notification.id)
        except Exception as e:
            logger.exception('Error adding notification with ID \'%s\': %s', notification.id, str(e))
            raise

    async def get(
        self,
        notification_id: UUID,
    ) -> EmailNotificationEntity | SMSNotificationEntity:
        logger.debug('Getting notification with ID \'%s\'', notification_id)
        try:
            notification = await NotificationModel.find_one(NotificationModel.id == notification_id)

            if not notification:
                raise NotificationNotFoundException(notification_id=notification_id)

            logger.debug('Notification with ID \'%s\' found', notification_id)
            return convert_notification_model_to_entity(notification)
        except Exception as e:
            logger.exception('Error retrieving notification with ID \'%s\': %s', notification_id, str(e))
            raise


class BeanieNotificationTemplateRepository(BaseNotificationTemplateRepository):
    async def add(
        self,
        name: str,
        text_template: str,
        html_template: str | None = None,
    ) -> None:
        logger.debug('Adding notification template with name \'%s\'', name)
        try:
            template = NotificationTemplateModel(
                name=name,
                text_template=text_template,
                html_template=html_template,
            )
            await template.insert()
            logger.debug('Notification template with name \'%s\' added to DB', name)
        except Exception as e:
            logger.exception('Error adding notification template with name \'%s\': %s', name, str(e))
            raise


    async def get(
        self,
        name: str,
    ) -> dict[str, str]:
        logger.debug('Getting notification template with name \'%s\'', name)
        try:
            template = await NotificationTemplateModel.find_one({'name': name})
            
            if not template:
                raise NotificationTemplateNotFoundException(name=name)

            logger.debug('Notification template with name \'%s\' found', name)
            return {
                'name': template.name,
                'text_template': template.text_template,
                'html_template': template.html_template,
            }
        except Exception as e:
            logger.exception('Error retrieving notification template with name \'%s\': %s', name, str(e))
            raise
