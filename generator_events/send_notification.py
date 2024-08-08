import random
import time

import requests

from notification_service.src.core.config import settings
from generator_events.events import (
    generate_new_like_for_review,
    generate_new_series,
    generate_new_registration,
    generate_all_users_event
)
from generator_events.jwt import create_access_and_refresh_tokens

event_functions = [
    generate_new_like_for_review,
    generate_new_series,
    generate_new_registration,
    generate_all_users_event
]


def send_event(event: dict) -> None:
    """Функция отправки сгенерированных событий в ручку '/analytics_event'"""
    access_token, refresh_token = create_access_and_refresh_tokens(
        "user_login", "role"
    )
    response = requests.post(settings.api_url, json=event, timeout=15, cookies={"access_token": access_token})
    print(response.status_code)
    print(response.text)


if __name__ == "__main__":
    for i in range(100):
        random_function = random.choice(event_functions)
        event = random_function()
        send_event(event)
        time.sleep(1)
