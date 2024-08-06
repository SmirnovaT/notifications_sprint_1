import calendar
import datetime as dt
import logging
from datetime import datetime, timedelta
from typing import Tuple

import jwt

from src.core.config import settings


def calculate_current_date_and_time() -> Tuple[dt, int]:
    """Calculates current date and time"""

    current_date_and_time_datetime = datetime.now(dt.timezone.utc)
    current_date_and_time_timestamp = int(
        calendar.timegm(current_date_and_time_datetime.timetuple())
    )

    return current_date_and_time_datetime, current_date_and_time_timestamp


def calculate_iat_and_exp_tokens() -> Tuple[int, int, int]:
    """
    Calculates 'iat' and 'exp' for access and refresh tokens
    """
    current_date_and_time_datetime, iat_timestamp = (
        calculate_current_date_and_time()
    )

    exp_access_token = current_date_and_time_datetime + timedelta(minutes=15)
    exp_refresh_token = current_date_and_time_datetime + timedelta(days=10)

    exp_access_token_timestamp = int(calendar.timegm(exp_access_token.timetuple()))
    exp_refresh_token_timestamp = int(calendar.timegm(exp_refresh_token.timetuple()))

    return iat_timestamp, exp_access_token_timestamp, exp_refresh_token_timestamp


def create_access_and_refresh_tokens(
        user_login: str, user_role: str
) -> Tuple[str, str]:
    """Creates a pair of access and refresh tokens"""

    iat, exp_access_token, exp_refresh_token = calculate_iat_and_exp_tokens()

    headers = {"alg": "RS256", "typ": "JWT"}

    access_token_payload = {
        "iss": "Auth service",
        "user_login": user_login,
        "user_role": user_role,
        "type": "access",
        "exp": exp_access_token,
        "iat": iat,
    }

    refresh_token_payload = {
        "iss": "Auth service",
        "user_login": user_login,
        "user_role": user_role,
        "type": "refresh",
        "exp": exp_refresh_token,
        "iat": iat,
    }

    try:
        encoded_access_token = jwt.encode(
            access_token_payload,
            settings.private_key,
            algorithm="RS256",
            headers=headers,
        )
        encoded_refresh_token = jwt.encode(
            refresh_token_payload,
            settings.private_key,
            algorithm="RS256",
            headers=headers,
        )
    except (TypeError, ValueError) as err:
        logging.error(f"Error while JWT encoding: {err}")

    return encoded_access_token, encoded_refresh_token


def validate_token(token: str) -> dict[str, str]:
    """Validates token"""

    try:
        decoded_token: dict[str, str] = jwt.decode(
            jwt=token,
            key=settings.public_key,
            algorithms=["RS256"],
        )
    except jwt.exceptions.DecodeError as decode_error:
        logging.error(f"Error while JWT decoding: {decode_error}")

    except jwt.ExpiredSignatureError:
        logging.error("Срок действия токена истек")

    except ValueError as err:
        logging.error(f"Error while JWT decoding: {err}")

    return decoded_token
