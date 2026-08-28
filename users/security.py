import jwt
from datetime import datetime, timezone, timedelta

from env import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_JWT_KEY


def create_access_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
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
