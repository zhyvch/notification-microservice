from domain.entities.notifications import EmailNotificationEntity, SMSNotificationEntity
from infrastructure.models.notifications import NotificationModel, NotificationType


def convert_notification_entity_to_model(
    notification: EmailNotificationEntity | SMSNotificationEntity,
) -> NotificationModel:
    return NotificationModel(
        id=notification.id,
        notification_type=NotificationType.EMAIL if isinstance(notification, EmailNotificationEntity) else NotificationType.SMS,
        sender=notification.sender.as_generic(),
        receivers=[receiver.as_generic() for receiver in notification.receivers],
        message=notification.text
    )


def convert_notification_model_to_entity(
    notification_model: NotificationModel,
) -> EmailNotificationEntity | SMSNotificationEntity:
    ...
