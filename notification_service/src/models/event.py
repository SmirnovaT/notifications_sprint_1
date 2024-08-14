from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class ChannelEnum(StrEnum):
    EMAIL = "email"
    WEBSOCKET = "websoket"


class EventsEnum(StrEnum):
    NEW_USER = "new_user"


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

    # urgent: bool = False


class NewUserEventData(BaseModel):
    user_id: UUID
    url: str


class NotificationDB(BaseModel):
    message: str
    channel: ChannelEnum
    recipient: str
    send_date: datetime | None = None

    # TODO: убрать или доделать валидацию/важность
    # event_id: str
    # user_id: str
    # urgent: bool = False
    # event_date: datetime

    status: NotificationStatusEnum = NotificationStatusEnum.UNSENT
    retry_count: int = 0


class NotificationQueue(BaseModel):
    message: str
    channel: ChannelEnum
    recipient: str

    notification_id: str

    # TODO: убрать или доделать валидацию/важность
    # event_id: str
    # user_id: str
    # urgent: bool = False
