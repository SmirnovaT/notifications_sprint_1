import json

from fastapi import Request

from src.core.config import settings
from src.db.rabbitmq import send_to_rabbitmq
from starlette.responses import JSONResponse


class NotificationService:

    async def send_event(
        self, data: dict | list[dict], request: Request
    ) -> JSONResponse:
        """Функция отправки уведомления в очередь."""

        request_id = request.cookies.get("X-Request-ID")
        data["request_id"] = request_id

        json_string = json.dumps(data)
        bytes_body = json_string.encode("utf-8")

        await send_to_rabbitmq(settings.rabbitmq_queue_events, bytes_body)
        return JSONResponse({"message": "Данные для уведомления успешно приняты"})
