from enum import StrEnum

from pydantic import BaseModel


class ChannelEnum(StrEnum):
    EMAIL = "email"
    WEBSOCKET = "websoket"


class NotificationQueue(BaseModel):
    message: str
    channel: ChannelEnum
    recipient: str

    notification_id: str
