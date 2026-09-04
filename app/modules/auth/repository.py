import uuid
from datetime import datetime
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import RecoveryToken


class AuthRepository:
    def __init__(self, redis: Redis, session: AsyncSession):
        self.redis = redis
        self.session = session

    async def save_recovery_token(self, user_id: uuid.UUID, token_hash: str, expires_at: datetime) -> bool:
        token = RecoveryToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at)

        self.session.add(token)
        await self.session.commit()

        await self.session.refresh(token)
        return True

    async def save_recovery_token_status(self, token_hash: str, status: bool) -> bool:
        token = await self.session.execute(select(RecoveryToken).where(RecoveryToken.token_hash == token_hash))
        token = token.scalar_one_or_none()
        token.is_used = status

        await self.session.commit()
        await self.session.refresh(token)
        return True


    async def get_recovery_token_by_hash(self, token_hash: str) -> RecoveryToken | None:
        token = await self.session.execute(select(RecoveryToken).where(RecoveryToken.token_hash == token_hash))
        token = token.scalar_one_or_none()
        return token

    async def save_refresh_token(self, jti: str, user_id: str, ttl: int) -> bool:
        return bool(await self.redis.set(f"refresh_token:{jti}", value=user_id, ex=ttl))

    async def get_refresh_token(self, jti: str) -> bytes | str | None:
        return await self.redis.get(f"refresh_token:{jti}")

    async def delete_refresh_token(self, jti: str) -> bool:
        return bool(await self.redis.delete(f"refresh_token:{jti}"))
