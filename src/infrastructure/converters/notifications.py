from domain.entities.notifications import EmailNotificationEntity, SMSNotificationEntity
from domain.value_objects.notifications import EmailVO, PhoneNumberVO
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
    if notification_model.notification_type == NotificationType.EMAIL:
        return EmailNotificationEntity(
            id=notification_model.id,
            sender=EmailVO(notification_model.sender),
            receivers=[EmailVO(receiver) for receiver in notification_model.receivers],
            subject=None,
            text=notification_model.message,
            html=notification_model.message,
        )
    elif notification_model.notification_type == NotificationType.SMS:
        return SMSNotificationEntity(
            id=notification_model.id,
            sender=PhoneNumberVO(notification_model.sender),
            receivers=[PhoneNumberVO(receiver) for receiver in notification_model.receivers],
            text=notification_model.message,
        )
    else:
        raise ValueError