from datetime import datetime

from pydantic import BaseModel
from src.core.constants import ChannelEnum, NotificationStatusEnum


class NotificationDB(BaseModel):
    message: str
    channel: ChannelEnum
    data: dict
    send_date: datetime | None = None
    updated_at: datetime | None = None

    status: NotificationStatusEnum = NotificationStatusEnum.UNSENT
    retry_count: int = 0


class NotificationEmailData(BaseModel):
    email: str
    subject: str


class NotificationWebsockerData(BaseModel):
    email: str
    subject: str


class NotificationQueue(BaseModel):
    message: str
    channel: ChannelEnum
    data: dict

    notification_id: str
