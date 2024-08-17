from pydantic import BaseModel


class UserProfile(BaseModel):
    email: str
    fullname: str
    notification_settings: dict[str, bool]
    timezone: str


class NewEpisodeData(BaseModel):
    series_name: str
    episode_name: str
    url: str
