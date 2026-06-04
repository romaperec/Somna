from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from loguru import logger

from app.core.config import settings


class JWTHelper:
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30,
        refresh_token_expire_days: int = 7,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(minutes=self.access_token_expire_minutes)
        )

        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(days=self.refresh_token_expire_days)
        )

        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str, expected_type: str) -> dict[str, Any] | None:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            if payload.get("type") != expected_type:
                logger.warning(
                    f"Token type {payload.get('type')} does not match expected type {expected_type}"
                )
                return None

            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token verification failed: Signature has expired.")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Token verification failed: Invalid token ({e})")
            return None


jwt_helper = JWTHelper(
    secret_key=settings.jwt.secret_key,
    algorithm=settings.jwt.algorithm,
    access_token_expire_minutes=settings.jwt.access_token_expire_minutes,
    refresh_token_expire_days=settings.jwt.refresh_token_expire_days,
)
