from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class MongoDBSettings(BaseModel):
    host: str = "localhost"
    port: int = 27017
    db_name: str = "notifications"
    event_collection: str = "events"
    notification_collection: str = "notifications"


class Settings(BaseSettings):
    """Главный класс настроек event воркера"""

    mongo: MongoDBSettings = MongoDBSettings()

    rabbitmq_username: str
    rabbitmq_password: str
    rabbitmq_queue_events: str
    rabbitmq_queue_notifications: str
    rabbitmq_delivery_mode: int
    rabbitmq_host: str
    rabbitmq_port: int

    nighttime_start_hour: int = 22
    nighttime_end_hour: int = 7

    profile_service_host: str = "localhost"
    profile_service_port: int = 8001

    content_service_host: str = "localhost"
    content_service_port: int = 8001

    ugc_service_host: str = "localhost"
    ugc_service_port: int = 8001

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Settings()
