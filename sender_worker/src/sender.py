import smtplib
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from email.message import EmailMessage
from logging import getLogger

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from config import settings
from models import (
    ChannelEnum,
    EmailData,
    NotificationDB,
    NotificationQueue,
    NotificationStatusEnum,
)

logger = getLogger()


class NotificationNotFound(Exception):
    """Нотификация не найдена в базе"""


class BaseSender(ABC):
    """Базовый класс обработчика нотификационных событий"""

    def __init__(
        self,
        mongo_db: AsyncIOMotorDatabase,
        event_collection: str,
        notification_collection: str,
    ) -> None:
        self.mongo = mongo_db
        self.event_collection = event_collection
        self.notification_collection = notification_collection

    @abstractmethod
    async def process(self, notification: NotificationQueue) -> None:
        """
        Абстрактный метод обработки нотификационного события,
        перегружается конретными обработчиками
        """

    async def set_success(self, notification_id: str):
        try:
            await self.mongo[self.notification_collection].update_one(
                filter={"_id": ObjectId(notification_id)},
                update={
                    "$set": {
                        "status": NotificationStatusEnum.SUCCESS,
                        "updated_at": datetime.now(tz=timezone.utc),
                    }
                },
            )
        except Exception:
            logger.exception(f"failed to update notificatio status {notification_id}")

    async def proccess_retry(self, notification_id: str):
        try:
            notification_dict = await self.mongo[self.notification_collection].find_one(
                {"_id": ObjectId(notification_id)}
            )
        except Exception:
            logger.exception(f"failed to get notification from db {notification_id}")
            raise
        notification_db = NotificationDB.model_validate(notification_dict)
        retry_count = notification_db.retry_count + 1
        notification_db.retry_count += 1
        notification_db.updated_at = datetime.now(tz=timezone.utc)
        logger.info(
            f"setting retry count {retry_count} for notification {notification_db}"
        )
        if retry_count >= settings.notification_retry_limit:
            notification_db.status = NotificationStatusEnum.FAILED
            logger.info(
                f"retry count for notification {notification_db} exceeded limit,"
                "setting as {NotificationStatusEnum.FAILED}"
            )
        try:
            await self.mongo[self.notification_collection].replace_one(
                filter={"_id": ObjectId(notification_id)},
                replacement=notification_db.model_dump(),
            )
        except Exception:
            logger.exception(f"failed to update notification status {notification_db}")
            raise


# Реестр обработчиков событий, чтобы не делать if/else
NOTIFICATION_SENDER_REGISTRY: dict[str, type[BaseSender]] = {}


def register_processor(channel: ChannelEnum):
    """Декоратор для добавления обработчиков событий в реестр"""

    def decorator(event_class):
        NOTIFICATION_SENDER_REGISTRY[channel] = event_class
        return event_class

    return decorator


@register_processor(ChannelEnum.EMAIL)
class EmailSender(BaseSender):
    """Отправщик почты"""

    def __init__(
        self,
        mongo_db: AsyncIOMotorDatabase,
        event_collection: str,
        notification_collection: str,
    ) -> None:
        super().__init__(mongo_db, event_collection, notification_collection)

        self.smtp_host = settings.email.host
        self.smtp_port = settings.email.port
        self.username = settings.email.username
        self.password = settings.email.password
        self.connect_to_smtp()

    def connect_to_smtp(self):
        smtp_server = smtplib.SMTP(self.smtp_host, self.smtp_port)
        # mailhog не поддерживает TLS
        # smtp_server.starttls()
        smtp_server.login(self.username, self.password)
        self.smtp_server = smtp_server

    def send_email(self, message: str, email_data: EmailData):
        msg = EmailMessage()
        FROM_EMAIL = settings.email.sender_address
        TO_EMAIL = email_data.email

        msg["From"] = FROM_EMAIL
        msg["To"] = ",".join([TO_EMAIL])
        msg["Subject"] = email_data.subject
        msg.add_alternative(message, subtype="html")
        self.smtp_server.sendmail(FROM_EMAIL, [TO_EMAIL], msg.as_string())

    async def process(self, notification: NotificationQueue) -> None:
        email_data = EmailData.model_validate(notification.data)

        try:
            try:
                self.send_email(notification.message, email_data)
            except smtplib.SMTPServerDisconnected:
                if self.smtp_server:
                    self.smtp_server.quit()
                self.connect_to_smtp()
                self.send_email(notification.message, email_data)
        except smtplib.SMTPException:
            await self.proccess_retry(notification.notification_id)
        else:
            await self.set_success(notification.notification_id)
            logger.info(f"notification {notification} succesfully sent")


@register_processor(ChannelEnum.WEBSOCKET)
class WebsockerSender(BaseSender):
    """Подозрительно быстрый отправщик в вебсокеты"""

    async def send_notification(self, raw_notification: dict) -> None:
        notification = NotificationQueue.model_validate(raw_notification)
        await self.set_success(notification.notification_id)
        logger.info(f"sent message to websocket {notification.message}")
