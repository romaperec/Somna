from redis.asyncio import Redis


class AuthRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def save_refresh_token(self, jti: str, user_id: str, ttl: int) -> bool:
        return bool(await self.redis.set(f"refresh_token:{jti}", value=user_id, ex=ttl))

    async def get_refresh_token(self, jti: str) -> bytes | str | None:
        return await self.redis.get(f"refresh_token:{jti}")

    async def delete_refresh_token(self, jti: str) -> bool:
        return bool(self.redis.delete(f"refresh_token:{jti}"))
