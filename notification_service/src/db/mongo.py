from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

mongo: Optional[AsyncIOMotorClient] = None


def init_mongo():
    return AsyncIOMotorClient()


def get_mongo_db():
    # TODO: вынести в настройки
    return mongo["notifications"]
