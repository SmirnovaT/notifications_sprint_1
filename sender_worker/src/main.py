import asyncio
import json
from logging import config, getLogger

import aio_pika
from pydantic import ValidationError

import mongo
import rabbitmq
from config import settings
from logger import LOGGING
from models import NotificationQueue
from sender import NOTIFICATION_SENDER_REGISTRY

config.dictConfig(LOGGING)
logger = getLogger()


async def process_events(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    """Передача сообщения с событием в обработчик"""
    async with message.process():
        mongo_db = mongo.get_mongo_db(settings.mongo.db_name)
        logger.debug(" [x] Received message %r" % message)
        logger.info("Message body is: %r" % message.body)
        raw_notification = json.loads(message.body.decode(encoding="utf-8"))
        try:
            notification = NotificationQueue.model_validate(raw_notification)
        except ValidationError:
            logger.exception(
                f"invalid message in the notification queue: {message.body}"
            )
            raise
        if processor := NOTIFICATION_SENDER_REGISTRY.get(notification.channel):
            await processor(
                mongo_db=mongo_db,
                event_collection=settings.mongo.event_collection,
                notification_collection=settings.mongo.notification_collection,
            ).process(notification)
        else:
            logger.error("обработчик события не зарегистрирован")


async def main() -> None:
    mongo.mongo = mongo.init_mongo(host=settings.mongo.host, port=settings.mongo.port)
    rabbitmq.connection = await rabbitmq.create_connection()
    async with rabbitmq.connection:
        rabbitmq.channel = await rabbitmq.create_channel(rabbitmq.connection)
        notification_queue = await rabbitmq.channel.declare_queue(
            settings.rabbitmq_queue_notifications, durable=True
        )
        await notification_queue.consume(process_events)

        logger.info(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
