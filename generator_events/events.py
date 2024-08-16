import uuid

from datetime import timedelta, timezone

import faker

from generator_events.jwt_token import create_access_and_refresh_tokens
from src.utils.services_constant import ServiceEnum

fake = faker.Faker()


def generate_event() -> dict:
    """Базовая функция для генерации событий"""

    return {
        "event_date": fake.date_time_this_year(
            before_now=True, after_now=False, tzinfo=timezone(timedelta(hours=3))
        ).isoformat(),
    }


def generate_new_like_for_review() -> [dict, str]:
    """Добавление нового лайка для ревью"""

    event_data = generate_event()
    event_data.update(
        {
            "type": "like",
            "data": {
                "author_id": str(uuid.uuid4()),
                "film_id": str(uuid.uuid4()),
                "review_id": str(uuid.uuid4()),
                "user_id": str(uuid.uuid4()),
                "score": fake.random_int(min=0, max=10),
                "send_date": None,
            },
        }
    )
    access_token, _ = create_access_and_refresh_tokens(ServiceEnum.UGC)
    return event_data, access_token


def generate_new_series() -> [dict, str]:
    """Добавление новой серии сериала"""

    event_data = generate_event()
    event_data.update(
        {
            "type": "series",
            "data": {"film_id": str(uuid.uuid4()), "send_date": generate_send_date()},
        }
    )
    access_token, _ = create_access_and_refresh_tokens(ServiceEnum.ADMIN_PANEL)
    return event_data, access_token


def generate_new_registration() -> [dict, str]:
    """Регистрация нового пользователя"""

    event_data = generate_event()
    event_data.update(
        {
            "type": "new_user",
            "data": {"user_id": str(uuid.uuid4()), "url": fake.text(10)},
            "send_date": generate_send_date(),
        }
    )

    access_token, _ = create_access_and_refresh_tokens(ServiceEnum.AUTH)
    return event_data, access_token


def generate_all_users_event() -> [dict, str]:
    """Добавление оповещения всех пользователей"""

    event_data = generate_event()
    event_data.update(
        {
            "type": "news",
            "data": {"message": fake.text(50), "send_date": generate_send_date()},
        }
    )

    access_token, _ = create_access_and_refresh_tokens(ServiceEnum.SCHEDULER)
    return event_data, access_token


def generate_send_date() -> str:
    send_date = fake.date_time_this_year(
        before_now=False, after_now=True, tzinfo=timezone(timedelta(hours=3))
    )
    return str(send_date)
