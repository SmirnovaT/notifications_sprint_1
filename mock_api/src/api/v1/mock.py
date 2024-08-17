from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(tags=["mock_api"])


class UserProfile(BaseModel):
    email: str
    fullname: str
    notification_settings: dict[str, bool]
    timezone: str


@router.get(
    "/profile/{profile_id}",
    status_code=status.HTTP_200_OK,
    description="Мок сервиса профилей",
    tags=["profile"],
)
async def notification() -> UserProfile:
    return UserProfile(
        email="test@mail.some",
        fullname="Иванов Иван Иванович",
        notification_settings={"email": True, "websockets": True},
        timezone="Europe/Moscow",
    )
