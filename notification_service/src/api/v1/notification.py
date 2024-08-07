from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse

from src.services.notification import NotificationService

router = APIRouter(tags=["notification"])


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    description="Сбор данных для уведомлений из других сервисов",
)
async def notification(
    data: dict, service: NotificationService = Depends(NotificationService)
) -> JSONResponse:
    return await service.send_event(data)
