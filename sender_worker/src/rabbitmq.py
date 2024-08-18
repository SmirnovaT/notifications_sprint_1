import json

import aio_pika
from aio_pika import DeliveryMode, Message

from config import settings

connection: aio_pika.abc.AbstractRobustConnection | None = None
channel: aio_pika.abc.AbstractRobustChannel | None = None


async def create_connection() -> aio_pika.abc.AbstractRobustConnection:
    return await aio_pika.connect_robust(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        login=settings.rabbitmq_username,
        password=settings.rabbitmq_password,
    )


async def create_channel(
    connection: aio_pika.abc.AbstractRobustConnection,
) -> aio_pika.abc.AbstractRobustChannel:
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    return channel


async def send_message(data: dict, queue_name: str) -> None:
    message_body = json.dumps(data).encode("utf-8")

    message = Message(
        message_body,
        delivery_mode=DeliveryMode.PERSISTENT,
    )

    await channel.default_exchange.publish(
        message,
        routing_key=queue_name,
    )
