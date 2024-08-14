import random
import time

import requests

from notification_service.src.core.config import settings
from generator_events.events import (
    generate_new_like_for_review,
    generate_new_series,
    generate_new_registration,
    generate_all_users_event,
    fake,
)
from src.core.logger import notification_logger

event_functions = [
    generate_new_like_for_review,
    generate_new_series,
    generate_new_registration,
    generate_all_users_event,
]


def send_event(event: dict, access_token: str) -> None:
    """Функция отправки сгенерированных событий в ручку '/analytics_event'"""

    response = requests.post(
        settings.notification_api_url,
        json=event,
        timeout=15,
        cookies={"access_token": access_token, "X-Request-ID": fake.uuid4()},
    )
    notification_logger.info(response.status_code)
    notification_logger.info(response.text)


if __name__ == "__main__":
    for i in range(100):
        random_function = random.choice(event_functions)
        event, access_token = random_function()
        send_event(event, access_token)
        time.sleep(1)
