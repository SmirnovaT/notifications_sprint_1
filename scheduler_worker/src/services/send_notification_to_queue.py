from settings import scheduler_settings
from src.core.logger import scheduler_logger
from src.database.rabbitmq import send_message
from src.models import NotificationQueue


class SendNotificationService:
    """Отправка уведомлений в очередь"""

    async def send_notification_to_queue(self, notifications, channel) -> None:
        for document in await notifications.to_list(length=None):
            queue_notification = NotificationQueue(
                message=document["message"],
                channel=document["channel"],
                recipient=document["recipient"],
                notification_id=str(document["_id"]),
            )
            notification_dict = queue_notification.model_dump()
            try:
                await send_message(
                    notification_dict,
                    scheduler_settings.rabbitmq_queue_notifications,
                    channel,
                )
                scheduler_logger.info(f"Уведомление успешно отправлено в очередь")
            except Exception as e:
                scheduler_logger.error(
                    f"Ошибка {e} при отправке уведомления {queue_notification}"
                )
