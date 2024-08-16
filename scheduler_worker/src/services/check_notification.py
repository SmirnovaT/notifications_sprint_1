from datetime import datetime, timezone
from typing import Any, Mapping

from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCursor


class CheckNotificationService:
    def __init__(
            self,
            mongo_db: AsyncIOMotorDatabase,
            notification_collection: str,
    ) -> None:
        self.mongo = mongo_db
        self.notification_collection = notification_collection

    async def check_notification(self) -> AsyncIOMotorCursor[Mapping[str, Any] | Any]:
        """Функция забирающая нотификации, которые пора отправить в очередь
        (со статусом unsent и send_date меньше текущего времени)."""

        return self.mongo[self.notification_collection].find(
            {"send_date": {"$lte": datetime.now(timezone.utc)}, "status": "unsent"}
        )
