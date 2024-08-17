from enum import StrEnum

from pydantic import BaseModel


class ChannelEnum(StrEnum):
    EMAIL = "email"
    WEBSOCKET = "websocket"


class NotificationQueue(BaseModel):
    message: str
    channel: ChannelEnum
    data: dict

    notification_id: str
