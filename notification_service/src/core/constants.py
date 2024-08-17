from enum import StrEnum


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
