from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

mongo: Optional[AsyncIOMotorClient] = None


def init_mongo(host: str, port: int):
    return AsyncIOMotorClient(host=host, port=port)


def get_mongo_db(db_name: str):
    return mongo[db_name]
