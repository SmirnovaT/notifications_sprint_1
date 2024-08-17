from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class ChannelEnum(StrEnum):
    EMAIL = "email"
    WEBSOCKET = "websocket"


class EventsEnum(StrEnum):
    NEW_USER = "new_user"
    LIKE = "like"
    SERIES = "series"
    NEWS = "news"


class NotificationStatusEnum(StrEnum):
    UNSENT = "unsent"
    SUCCESS = "success"
    FAILED = "failed"


class Event(BaseModel):
    id: str | None = None
    data: dict
    type: EventsEnum
    event_date: datetime
    send_date: datetime | None = None
    request_id: str | None = None

    # urgent: bool = False


class NewUserEventData(BaseModel):
    user_id: UUID
    url: str


class NotificationDB(BaseModel):
    message: str
    channel: ChannelEnum
    send_date: datetime | None = None
    updated_at: datetime | None = None

    status: NotificationStatusEnum = NotificationStatusEnum.UNSENT
    retry_count: int = 0


class EmailData(BaseModel):
    email: str
    subject: str


class WebsocketData(BaseModel):
    recipients: str


class NotificationQueue(BaseModel):
    message: str
    channel: ChannelEnum
    data: dict

    notification_id: str
