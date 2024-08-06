from typing import Generator

import faker

import events

fake = faker.Faker()


def generate_events(count: int, batch_size: int) -> Generator[list[dict], None, None]:
    """Генерирует 10млн записей и возвращает пачками по 500 записей"""

    def event_generator() -> Generator[list[dict], None, None]:
        batch = []
        for i in range(count):
            batch.append(events.generate_new_like())
            # batch.append(events.generate_new_bookmark())
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

    return event_generator()
