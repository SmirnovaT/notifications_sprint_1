import asyncio
from src.database import rabbitmq
from src.database.mongo import init_mongo
from settings import scheduler_settings


async def main() -> None:
    init_mongo(scheduler_settings.mongo.host, scheduler_settings.mongo.port)
    rabbitmq.connection = await rabbitmq.create_connection()
    async with rabbitmq.connection:
        rabbitmq.channel = await rabbitmq.create_channel(rabbitmq.connection)
        even_queue = await rabbitmq.channel.declare_queue(
            scheduler_settings.rabbitmq_queue_events, durable=True
        )
        await rabbitmq.channel.declare_queue(
            scheduler_settings.rabbitmq_queue_notifications, durable=True
        )

        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()

#
if __name__ == "__main__":
    asyncio.run(main())
