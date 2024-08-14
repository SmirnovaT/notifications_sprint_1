from fastapi import APIRouter, status, Depends, Request
from starlette.responses import JSONResponse

from src.services.notification import NotificationService
from src.utils.jwt_and_services import (
    CheckService,
)
from src.utils.services_constant import ALLOWED_SERVICES

router = APIRouter(tags=["notification"])


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    description="Сбор данных для уведомлений из других сервисов",
    dependencies=[Depends(CheckService(services=ALLOWED_SERVICES))],
)
async def notification(
    data: dict,
    request: Request,
    service: NotificationService = Depends(NotificationService),
) -> JSONResponse:
    return await service.send_event(data, request)
