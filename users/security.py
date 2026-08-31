from datetime import UTC, datetime, timedelta

import jwt

from env import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_JWT_KEY


def create_access_token(email: str) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": email,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        SECRET_JWT_KEY,
        algorithm=ALGORITHM,
    )
