from http import HTTPStatus

import pytest

from notification_service.src.core.config import settings
from notification_service.src.tests.utils.jwt_token import generate_access_token
from notification_service.src.utils.services_constant import ServiceEnum


@pytest.mark.asyncio
async def test_notification_success(client_session, make_post_request):
    data = {
        "timestamp": "2024-04-05T09:27:49.783833+03:00",
        "type": "series",
        "data": {"film_id": "73348ebf-a8b3-4b3f-beb0-2f9e895d5ce7"},
    }
    access_token = generate_access_token(ServiceEnum.UGC)
    status, response = await make_post_request(
        settings.notification_api_url, data, cookies={"access_token": access_token}
    )
    assert status == HTTPStatus.OK
    assert response == {"message": "Данные для уведомления успешно приняты"}


@pytest.mark.asyncio
async def test_notification_forbidden(client_session, make_post_request):
    data = {
        "timestamp": "2024-04-05T09:27:49.783833+03:00",
        "type": "series",
        "data": {"film_id": "73348ebf-a8b3-4b3f-beb0-2f9e895d5ce7"},
    }
    status, response = await make_post_request(settings.notification_api_url, data)
    assert status == HTTPStatus.FORBIDDEN
