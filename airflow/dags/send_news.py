from typing import Any
import os
import sys

import httpx
import pendulum
from dotenv import load_dotenv

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
            "event_date": str(pendulum.now('UTC')),
            "send_date": None,
        }
        load_dotenv()
        PRIVATE_KEY = os.getenv('PRIVATE_KEY')
        API_URL = os.getenv('API_URL')
        response = httpx.post(API_URL,
                   json = data,
                   cookies={"access_token": jwt_add.create_access_token(PRIVATE_KEY)}
                   )

    raw_json = {"message": Variable.get("message"), "send_date": Variable.get("send_date")}
    prepare_email(raw_json)


send_news()
