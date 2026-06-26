from uuid import UUID

from app.core.jwt_helper import JWTHelper
from app.core.security import PasswordSecurityService
from app.modules.auth.exceptions import (
    AuthenticationFailedException,
    InvalidTokenException,
    MissingTokenException,
)
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import TokenPair, UserLogin
from app.modules.users.schemas import UserCreate
from app.modules.users.service import UserService


class AuthService:
    def __init__(self, repo: AuthRepository, jwt_service: JWTHelper, user_service: UserService, password_service: PasswordSecurityService):
        self.repo = repo
        self.jwt_service = jwt_service
        self.user_service = user_service
        self.password_service = password_service

    async def register_user(self, schema: UserCreate) -> TokenPair:
        user = await self.user_service.register(schema)

        return await self._generate_and_save_tokens(str(user.id))

    async def login_user(self, schema: UserLogin) -> TokenPair:
        user = await self.user_service.get_for_authentication(schema.username_or_email)
        if not user:
            raise AuthenticationFailedException

        if not self.password_service.verify(schema.password, user.hashed_password):
            raise AuthenticationFailedException

        return await self._generate_and_save_tokens(str(user.id))

    async def update_both_tokens(self, refresh_token: str | None):
        _, user_id = await self._extract_refresh_payload(refresh_token)
        return await self._generate_and_save_tokens(user_id)

    async def logout_user(self, refresh_token: str | None):
        jti, _ = await self._extract_refresh_payload(refresh_token)
        await self.repo.delete_refresh_token(jti)

    def get_user_id_by_token(self, access_token: str):
        payload = self.jwt_service.verify_token(access_token, "access")
        if payload is None:
            raise InvalidTokenException

        user_id = payload.get("sub")
        if not isinstance(user_id, str):
            raise InvalidTokenException

        return UUID(user_id)

    async def _extract_refresh_payload(self, refresh_token: str | None) -> tuple[str, str]:
        if refresh_token is None:
            raise MissingTokenException

        payload = self.jwt_service.verify_token(refresh_token, "refresh")
        if payload is None:
            raise InvalidTokenException

        jti = payload.get("jti")
        user_id = payload.get("sub")

        if not isinstance(user_id, str) or not isinstance(jti, str):
            raise InvalidTokenException

        return jti, user_id

    async def _generate_and_save_tokens(self, user_id: str) -> TokenPair:
        access_token = self.jwt_service.create_access_token({"sub": user_id})
        refresh_token, token_jti = self.jwt_service.create_refresh_token({"sub": user_id})

        await self.repo.save_refresh_token(token_jti, user_id, ttl=self.jwt_service.refresh_expire_seconds)
        return TokenPair(access_token=access_token, refresh_token=refresh_token)
