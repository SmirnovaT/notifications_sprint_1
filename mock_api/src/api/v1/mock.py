from uuid import UUID, uuid4

from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(tags=["mock_api"])


class UserProfile(BaseModel):
    email: str
    fullname: str
    notification_settings: dict[str, bool]
    timezone: str


class NewEpisodeData(BaseModel):
    series_name: str
    episode_name: str
    url: str


MOCK_EPISODE_DATA = {
    "series_name": "название сериала",
    "episode_name": "навание эпизода",
    "url": "ссылка на эпизод",
}


@router.get(
    "/profile/{profile_id}",
    status_code=status.HTTP_200_OK,
    description="Мок сервиса профилей",
    tags=["profile"],
)
async def get_user_profile() -> UserProfile:
    return UserProfile(
        email="test@mail.some",
        fullname="Иванов Иван Иванович",
        notification_settings={"email": True, "websocket": True},
        timezone="Europe/Moscow",
    )


@router.get(
    "/filmwork/{filmwork_id}/episode/{episode_id}",
    status_code=status.HTTP_200_OK,
    description="Мок контетного сервиса с данным о сериях",
    tags=["content"],
)
async def get_new_episode() -> NewEpisodeData:
    return NewEpisodeData.model_validate(MOCK_EPISODE_DATA)


@router.get(
    "/subscribers/filmwork/{filmwork_id}",
    status_code=status.HTTP_200_OK,
    description="Мок ugc сервиса с подписчиками кинопроизведения/сериала",
    tags=["ugc"],
)
async def get_subscribed_users() -> list[UUID]:
    return [uuid4(), uuid4()]
