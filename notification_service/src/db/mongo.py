from typing import Optional

import motor
from motor.motor_asyncio import AsyncIOMotorClient

mongo: Optional[AsyncIOMotorClient] = None


def init_mongo(host: str, port: int) -> AsyncIOMotorClient:
    return AsyncIOMotorClient(host=host, port=port)


def get_mongo_db(db_name: str) -> motor.motor_asyncio.AsyncIOMotorDatabase:
    return mongo[db_name]
