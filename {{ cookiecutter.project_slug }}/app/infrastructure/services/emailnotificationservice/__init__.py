from scaffold.email_notification_service import (
    EmailNotificationService as BaseEmailNotificationService,
)

from app.application.interfaces.notification_service import NotificationService


class EmailNotificationService(BaseEmailNotificationService, NotificationService):
    pass
