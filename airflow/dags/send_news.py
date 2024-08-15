#import datetime
from typing import Any

import httpx
import pendulum

from airflow.decorators import dag, task


@dag(
    schedule=None,
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def send_news():
    """
    DAG to send server IP to email.

    """

    @task(multiple_outputs=True)
    def prepare_email(raw_json: dict[str, Any]) -> dict[str, str]:
        data = {
            "data": raw_json,
            "type": "news",
            "event_date": pendulum.datetime(2024, 1, 1, tz="UTC"),
            "send_date": None,
        }
        httpx.post('http://app:8000/api/v1/notification/', data= data)

    raw_json = {"film_id": None}
    prepare_email(raw_json)


send_news()
