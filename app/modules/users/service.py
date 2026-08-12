import uuid

from app.core.security import PasswordSecurityService
from app.modules.users.exceptions import (
    UserEmailAlreadyExistsException,
    UserInvalidPasswordException,
    UserNotFoundException,
    UserPasswordsMatchException,
    UserUsernameExistsException,
)
from app.modules.users.models import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import (
    UserChangePassword,
    UserCreate,
    UserPrivateResponse,
    UserUpdate,
)


class UserService:
    def __init__(self, repo: UserRepository, password_service: PasswordSecurityService):
        self.repo = repo
        self.password_service = password_service

    async def register(self, schema: UserCreate) -> User:
        if await self.repo.get_by_email(schema.email):
            raise UserEmailAlreadyExistsException

        user_data = schema.model_dump()

        raw_password = user_data.pop("password")
        user_data["hashed_password"] = self.password_service.hash(raw_password)

        return await self.repo.create(user_data)

    async def get_for_authentication(self, username_or_email: str) -> User | None:
        if "@" in username_or_email:
            return await self.repo.get_by_email(username_or_email)
        return await self.repo.get_by_username(username_or_email)

    async def get_profile(self, user_id: uuid.UUID) -> UserPrivateResponse | None:
        return await self.repo.get_by_id(user_id)

    async def update_profile(self, user_id: uuid.UUID, user_data: UserUpdate) -> User:
        user = await self.repo.get_orm_by_id(user_id)

        if not user:
            raise UserNotFoundException

        update_data = user_data.model_dump(exclude_unset=True, exclude_none=True)

        if not update_data:
            return user

        if "email" in update_data and update_data["email"] != user.email:
            if await self.repo.get_by_email(update_data["email"]):
                raise UserEmailAlreadyExistsException

        if "username" in update_data and update_data["username"] != user.username:
            if await self.repo.get_by_username(update_data["username"]):
                raise UserUsernameExistsException

        await self.repo.delete_cache(user_id)
        return await self.repo.update(user, update_data)

    async def delete_account(self, user_id: uuid.UUID) -> bool:
        user = await self.repo.get_orm_by_id(user_id)

        if not user:
            raise UserNotFoundException

        await self.repo.delete_cache(user_id)
        return await self.repo.delete(user)

    async def change_password(self, user_id: uuid.UUID, schema: UserChangePassword):
        if schema.current_password == schema.new_password:
            raise UserPasswordsMatchException

        user = await self.repo.get_orm_by_id(user_id)

        if not user:
            raise UserNotFoundException

        if not self.password_service.verify(
            schema.current_password, user.hashed_password
        ):
            raise UserInvalidPasswordException

        new_hashed_password = self.password_service.hash(schema.new_password)
        await self.repo.update(user, {"hashed_password": new_hashed_password})
