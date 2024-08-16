from motor.motor_asyncio import AsyncIOMotorDatabase


class CheckNotificationService:
    def __init__(
            self,
            mongo_db: AsyncIOMotorDatabase,
            event_collection: str,
            notification_collection: str,
    ) -> None:
        self.mongo_db = mongo_db
        self.event_collection = event_collection
        self.notification_collection = notification_collection

    async def check_notification(self):
        notifications = self.mongo_db[self.notification_collection].find()
        print(notifications)



    # Берем из монги все уведомления. которые сос таусом unset и send_date >= date_now
