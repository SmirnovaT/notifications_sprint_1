import asyncio
import json
from logging import config, getLogger

import aio_pika
import src.db.mongo as mongo
import src.event_worker.rabbitmq as rabbitmq
from src.db.mongo import get_mongo_db
from src.event_worker.logging import LOGGING
from src.event_worker.settings import BASE_DIR, settings
from src.services.event import EVENT_PROCESSOR_REGISTRY
from src.services.template import TemplateService

config.dictConfig(LOGGING)
logger = getLogger()

template_service = TemplateService(template_path=BASE_DIR / "templates")


async def process_events(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    """Передача сообщения с событием в обработчик"""
    async with message.process():
        mongo_db = get_mongo_db(settings.mongo.db_name)
        logger.debug(" [x] Received message %r" % message)
        logger.info("Message body is: %r" % message.body)
        event = json.loads(message.body.decode(encoding="utf-8"))
        if processor := EVENT_PROCESSOR_REGISTRY.get(event["type"]):
            await processor(
                mongo_db=mongo_db,
                template_service=template_service,
                event_collection=settings.mongo.event_collection,
                notification_collection=settings.mongo.notification_collection,
            ).process(event)
        else:
            logger.error("обработчик события не зарегистрирован")


async def main() -> None:
    mongo.mongo = mongo.init_mongo()
    rabbitmq.connection = await rabbitmq.create_connection()
    async with rabbitmq.connection:
        rabbitmq.channel = await rabbitmq.create_channel(rabbitmq.connection)
        even_queue = await rabbitmq.channel.declare_queue(
            settings.rabbitmq_queue_events, durable=True
        )
        await rabbitmq.channel.declare_queue(
            settings.rabbitmq_queue_notifications, durable=True
        )
        await even_queue.consume(process_events)

        logger.info(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
