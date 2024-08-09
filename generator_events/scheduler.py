"""Планировщик для регулярных массовых рассылок"""

import asyncio

from generator_events.events import generate_all_users_event
from generator_events.send_notification import send_event
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.core.logger import notification_logger


def event():
    data_event, token = generate_all_users_event()
    send_event(data_event, token)


async def run_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(event, "interval", seconds=27)
    scheduler.start()
    while True:
        await asyncio.sleep(1)


async def main():
    notification_logger.info("Запуск планировщика")
    _ = asyncio.create_task(run_scheduler())
    await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit) as exception:
        notification_logger.error(exception)
