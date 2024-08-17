from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class MongoDBSettings(BaseModel):
    host: str = "localhost"
    port: int = 27017
    db_name: str = "notifications"
    notification_collection: str = "notifications"


class Settings(BaseSettings):
    """Главный класс настроек scheduler воркера"""

    mongo: MongoDBSettings = MongoDBSettings()

    rabbitmq_username: str
    rabbitmq_password: str
    rabbitmq_queue_notifications: str
    rabbitmq_delivery_mode: int
    rabbitmq_host: str
    rabbitmq_port: int

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


scheduler_settings = Settings()
