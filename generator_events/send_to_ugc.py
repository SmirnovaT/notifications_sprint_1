import random
import time

import requests

from app.src.core.config import settings
from generator_events.send_to_ugc import (
    generate_new_like,
    generate_new_like_for_review,
    generate_new_review,
    generate_new_bookmark
)
from generator_events.jwt import create_access_and_refresh_tokens

event_functions = [
    generate_new_like,
    generate_new_like_for_review,
    generate_new_review,
    generate_new_bookmark,
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
