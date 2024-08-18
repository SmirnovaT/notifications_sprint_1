import os
import sys
from typing import Any

import httpx
from dotenv import load_dotenv
import pendulum

from airflow.decorators import dag, task
from airflow.models import Variable

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import jwt_add


@dag(
    schedule="@daily",
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
            "event_date": str(pendulum.now("UTC")),
            "send_date": None,
        }
        load_dotenv()
        private_key = os.getenv("PRIVATE_KEY")
        api_url = os.getenv("API_URL")
        httpx.post(
            api_url,
            json=data,
            cookies={"access_token": jwt_add.create_access_token(private_key)},
        )

    raw_json = {
        "message": Variable.get("message"),
        "send_date": Variable.get("send_date"),
    }
    prepare_email(raw_json)


send_news()
