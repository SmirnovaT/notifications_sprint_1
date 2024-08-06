import time


def time_it(TOTAL):
    """Декоратор, измеряющий время выполнения функции"""

    def inner_decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            speed_time = execution_time / TOTAL
            print(f"Скорость обработки {TOTAL} записей: {execution_time} секунд")
            print(
                f"Средняя скорость обработки одной записи из {TOTAL} записей: {speed_time} секунд"
            )
            return result

        return wrapper

    return inner_decorator
