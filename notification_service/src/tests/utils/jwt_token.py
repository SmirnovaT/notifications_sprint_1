from datetime import datetime, timedelta, timezone

import jwt

from notification_service.src.core.config import settings


def generate_access_token(
    service_name,
    ttl: timedelta | None = None,
) -> str:
    if not ttl:
        ttl = timedelta(minutes=60)

    datetime_now = datetime.now(timezone.utc)
    expire = datetime_now + ttl
    access_token_payload = {
        "iss": "Auth service",
        "service_name": service_name,
        "type": "access",
        "exp": expire,
        "iat": datetime_now,
    }
    encoded_jwt = jwt.encode(
        access_token_payload, settings.private_key, algorithm="RS256"
    )
    return encoded_jwt
