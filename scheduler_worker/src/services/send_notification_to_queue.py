from typing import Mapping, Any

import aio_pika
from motor.motor_asyncio import AsyncIOMotorCursor

from settings import scheduler_settings
from src.core.logger import scheduler_logger
from src.database.rabbitmq import send_message
from src.models import NotificationQueue


class SendNotificationService:
    """Отправка уведомлений в очередь"""

    async def send_notification_to_queue(
        self,
        notifications: AsyncIOMotorCursor[Mapping[str, Any] | Any],
        channel: aio_pika.abc.AbstractRobustChannel,
    ) -> None:
        for document in await notifications.to_list(length=None):
            queue_notification = NotificationQueue(
                message=document["message"],
                channel=document["channel"],
                data=document["data"],
                notification_id=str(document["_id"]),
            )
            notification_dict = queue_notification.model_dump()
            try:
                await send_message(
                    notification_dict,
                    scheduler_settings.rabbitmq_queue_notifications,
                    channel,
                )
                scheduler_logger.info(
                    f"Уведомление успешно отправлено в очередь {notification_dict}"
                )
            except Exception as e:
                scheduler_logger.error(
                    f"Ошибка {e} при отправке уведомления {queue_notification}"
                )
