import uuid

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.modules.users.models import User
from app.modules.users.schemas import UserPrivateResponse


class UserRepository:
    def __init__(self, redis: Redis,  session: AsyncSession):
        self.redis = redis
        self.session = session

    async def get_orm_by_id(self, user_id: uuid.UUID) -> User | None:
        user = await self.session.execute(select(User).where(User.id == user_id))
        user = user.scalar_one_or_none()
        return user

    async def get_by_id(self, user_id: uuid.UUID, ttl: int = 900) -> UserPrivateResponse | None:
        cached_user = await self.redis.get(f"user:{user_id}")
        if cached_user:
            return UserPrivateResponse.model_validate_json(cached_user)
        user = await self.session.execute(select(User).where(User.id == user_id))
        user = user.scalar_one_or_none()

        if not user:
            return None

        user_schema = UserPrivateResponse.model_validate(user)
        await self.redis.set(f"user:{user_id}", user_schema.model_dump_json(), ex=ttl)

        return user_schema

    async def get_by_email(self, email: str) -> User | None:
        user = await self.session.execute(select(User).where(User.email == email))
        user = user.scalar_one_or_none()
        return user

    async def get_by_username(self, username: str) -> User | None:
        user = await self.session.execute(select(User).where(User.username == username))
        user = user.scalar_one_or_none()
        return user

    async def create(self, user_data: dict) -> User:
        new_user = User(**user_data)

        self.session.add(new_user)
        await self.session.commit()

        await self.session.refresh(new_user)

        return new_user

    async def delete(self, user: User) -> bool:
        await self.session.delete(user)
        await self.session.commit()
        return True

    async def delete_cache(self, user_id: uuid.UUID):
        await self.redis.delete(f"user:{user_id}")

    async def update(self, user: User, updated_user_data: dict) -> User:
        for key, value in updated_user_data.items():
            setattr(user, key, value)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
