from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from src.core.constants import EventsEnum


class Event(BaseModel):
    id: str | None = None
    data: dict
    type: EventsEnum
    event_date: datetime
    send_date: datetime | None = None


class NewUserEventData(BaseModel):
    user_id: UUID
    url: str


class NewEpisodeEventData(BaseModel):
    filmwork_id: UUID
    episode_id: UUID
