from typing import Any
import os
import sys

import httpx
import pendulum

from airflow.decorators import dag, task
from airflow.models import Variable

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import jwt_add

@dag(
    schedule= "@daily",
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
            "event_date": pendulum.now('UTC'),
            "send_date": None,
        }
        httpx.post('http://app:8000/api/v1/notification/',
                   data= data,
                   cookies={"access_token": jwt_add.create_access_token()}
                   )

    raw_json = {"message": Variable.get("message"), "send_date": Variable.get("send_date")}
    prepare_email(raw_json)


send_news()
