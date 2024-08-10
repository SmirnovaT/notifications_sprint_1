import json

from starlette.responses import JSONResponse

from src.core.config import settings
from src.db.rabbitmq import send_to_rabbitmq


class NotificationService:

    async def send_event(self, data: dict | list[dict]) -> JSONResponse:
        """Функция отправки уведомления в очередь."""

        json_string = json.dumps(data)
        bytes_body = json_string.encode("utf-8")
        await send_to_rabbitmq(settings.rabbitmq_queue_notifications, bytes_body)
        return JSONResponse({"message": "Данные для уведомления успешно приняты"})
