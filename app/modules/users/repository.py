import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.modules.users.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        user = await self.session.execute(select(User).where(User.id == user_id))
        user = user.scalar_one_or_none()
        return user

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

    async def update(self, user: User, updated_user_data: dict) -> User:
        for key, value in updated_user_data.items():
            setattr(user, key, value)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
