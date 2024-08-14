from abc import ABC, abstractmethod

from motor.motor_asyncio import AsyncIOMotorDatabase

# TODO: использовать из db, переписать его на aio-pika?
from src.event_worker.rabbitmq import send_message
from src.event_worker.settings import settings
from src.models.event import (
    ChannelEnum,
    Event,
    EventsEnum,
    NotificationDB,
    NotificationQueue,
)
from src.models.profile import UserProfile
from src.services.template import TemplateService


class EventProcessor(ABC):
    """Базовый класс обработчика нотификационных событий"""

    def __init__(
        self,
        mongo_db: AsyncIOMotorDatabase,
        template_service: TemplateService,
        event_collection: str,
        notification_collection: str,
    ) -> None:
        self.mongo = mongo_db
        self.event_collection = event_collection
        self.notification_collection = notification_collection
        self.temlate_service = template_service

    async def process(self, raw_event: dict) -> None:
        event = Event.model_validate(raw_event)
        event = await self.save_event(event)
        await self.process_event(event)

    @abstractmethod
    async def process_event(self, event: Event) -> None:
        """
        Абстрактный метод обработки нотификационного события,
        перегружается конретными обрабочиками
        """
        pass

    async def send_notification(self, notification: NotificationDB):
        """Сохранение нотификации в бд и отправка в очередь мгновенных"""
        try:
            result = await self.mongo[
                settings.mongo.notification_collection
            ].insert_one(notification.model_dump())
            notification_id = str(result.inserted_id)
        except Exception:
            # обработать
            raise

        if notification.send_date is None:
            queue_notification = NotificationQueue(
                message=notification.message,
                channel=notification.channel,
                recipient=notification.recipient,
                notification_id=notification_id,
                # event_id=event_id,
                # user_id=user_id,
            )
            await self._send_notification_to_queue(queue_notification)

    async def _get_user_profile(self, user_id: str) -> UserProfile:
        """Мок получения пользователькой информации"""
        mock_profile = {
            "email": "some@mail.ru",
            "fullname": "Иванов Иван Иванович",
            "notification_settings": {"email": True, "websockets": True},
            "timezone": "Europe/Moscow",
        }
        return UserProfile.model_validate(mock_profile)

    async def save_event(self, event: Event) -> Event:
        """Сохранение нотификационного события в бд"""
        try:
            result = await self.mongo[self.event_collection].insert_one(
                event.model_dump(exclude={"id"})
            )
            event.id = str(result.inserted_id)
            return event
        except Exception:
            # обработать
            raise

    async def _send_notification_to_queue(self, notification: NotificationQueue):
        try:
            await send_message(
                notification.model_dump(),
                queue_name=settings.rabbitmq_queue_notifications,
            )
        except Exception:
            # TODO: обработать
            raise


# Реестр обработчиков событий, чтобы не делать if/else
EVENT_PROCESSOR_REGISTRY: dict[str, type[EventProcessor]] = {}


def register_processor(event_type: EventsEnum):
    """Декоратор для добавления обработчиков событий в реестр"""

    def decorator(event_class):
        EVENT_PROCESSOR_REGISTRY[event_type] = event_class
        return event_class

    return decorator


@register_processor(EventsEnum.NEW_USER)
class NewUserEvent(EventProcessor):
    """Подтверждение регистрации нового пользователя"""

    urgent: bool = True

    async def process_event(self, event: Event) -> None:
        # получение данных
        user_id = event.data["user_id"]
        user_profile = await self._get_user_profile(user_id)
        context = {
            "fullname": user_profile.fullname,
            "url": event.data["url"],
        }
        user_email = user_profile.email

        # рендер шаблона
        notification_channel = ChannelEnum.EMAIL
        template_str = self.temlate_service.get_template(
            event.type, notification_channel
        )
        message = self.temlate_service.render_template(template_str, context)
        print(message)

        # отправка данных в дб/очередь
        db_notification = NotificationDB(
            message=message,
            channel=notification_channel,
            recipient=user_email,
            send_date=event.send_date,
            # event_id=event_id,
            # user_id=user_id,
        )
        await self.send_notification(db_notification)
