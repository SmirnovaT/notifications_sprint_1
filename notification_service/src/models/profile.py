from pydantic import BaseModel


class UserProfile(BaseModel):
    email: str
    fullname: str
    notification_settings: dict[str, bool]
    timezone: str
