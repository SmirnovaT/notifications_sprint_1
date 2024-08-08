import uuid

from datetime import datetime, timedelta, timezone

import faker

fake = faker.Faker()


def generate_event() -> dict:
    """Базовая функция для генерации событий"""

    return {
        "timestamp": fake.date_time_this_year(
            before_now=True, after_now=False, tzinfo=timezone(timedelta(hours=3))
        ).isoformat(),
        "service": fake.text(10)
    }

def generate_new_like_for_review() -> dict:
    """Добавление нового лайка для ревью """

    event_data = generate_event()
    event_data.update(
        {
            "type": "like",
            "data":
                {
                    "author_id": str(uuid.uuid4()),
                    "film_id": str(uuid.uuid4()),
                    "review_id": str(uuid.uuid4()),
                    "user_id": str(uuid.uuid4()),
                    "score": fake.random_int(min=0, max=10)
                }
        })
    return event_data

def generate_new_series() -> dict:
    """Добавление новой серии сериала"""
    event_data = generate_event()
    event_data.update(
        {
            "type": "series",
            "data":
                {
                    "film_id": str(uuid.uuid4())
                }
        }
    )

def generate_new_registration() -> dict:
    """Регистрация нового пользователя"""
    event_data = generate_event()
    event_data.update(
        {
            "type": "new_user",
            "data": {
                "user_id": str(uuid.uuid4()),
                "url": fake.text(10)}
        }
    )

def generate_all_users_event() -> dict:
    """Добавление оповещения всех пользователей"""
    event_data = generate_event()
    event_data.update(
        {
            "type": "news"
        }
    )



