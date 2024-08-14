import aiormq
import backoff

from src.core.config import settings

connection: aiormq.Connection | None = None
channel: aiormq.Channel | None = None


@backoff.on_exception(
    backoff.expo(
        aiormq.exceptions.AMQPError,
        aiormq.exceptions.AMQPConnectionError,
        ConnectionError,
    ),
    max_tries=3,
)
async def create_connection_rabbitmq() -> aiormq.abc.AbstractConnection:
    """Создание соединения с RabbitMQ."""

    connection_string = (
        f"amqp://{settings.rabbitmq_username}:{settings.rabbitmq_password}@"
        + f"{settings.rabbitmq_host}:{settings.rabbitmq_port}/"
    )
    return await aiormq.connect(connection_string)


async def create_channel_rabbitmq(
    _connection: aiormq.abc.AbstractConnection,
) -> aiormq.abc.AbstractChannel:
    """Создание канала для отправки сообщений."""

    return await _connection.channel()


async def init_queues(_channel: aiormq.abc.AbstractChannel) -> None:
    """Функция инициализирует очередь в RabbitMQ."""

    await _channel.queue_declare(
        queue=settings.rabbitmq_queue_notifications, durable=True
    )
    await _channel.basic_qos(prefetch_count=1, global_=True)


async def send_to_rabbitmq(routing_key: str, body: bytes) -> None:
    """Функция отправляет сообщение в RabbitMQ."""

    message_properties = aiormq.spec.Basic.Properties(
        delivery_mode=settings.rabbitmq_delivery_mode,
    )
    await channel.basic_publish(
        exchange="", routing_key=routing_key, body=body, properties=message_properties
    )
