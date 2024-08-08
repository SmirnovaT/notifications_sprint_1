from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Главный класс настроек всего приложения"""

    project_name: str = "notification_service"
    app_port: int = 8000
    notification_api_url: str

    private_key: str
    public_key: str

    rabbitmq_username: str
    rabbitmq_password: str
    rabbitmq_queue_notifications: str
    rabbitmq_delivery_mode: int
    rabbitmq_host: str
    rabbitmq_port: int

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Settings()
