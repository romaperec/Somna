from app.core.jwt_helper import JWTHelper
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import TokenPair
from app.modules.users.schemas import UserCreate
from app.modules.users.service import UserService


class AuthService:
    def __init__(self, repo: AuthRepository, jwt_service: JWTHelper, user_service: UserService):
        self.repo = repo
        self.jwt_service = jwt_service
        self.user_service = user_service

    async def register_user(self, schema: UserCreate) -> TokenPair:
        user = await self.user_service.register(schema)

        access_token = self.jwt_service.create_access_token(data={"sub": str(user.id)})
        refresh_token, token_jti = self.jwt_service.create_refresh_token({"sub": str(user.id)})
        await self.repo.save_refresh_token(token_jti, str(user.id), ttl=self.jwt_service.refresh_expire_seconds)

    async def _generate_and_save_tokens(self, user_id: str) -> TokenPair:
        access_token = self.jwt_service.create_access_token({"sub": user_id})
        refresh_token, token_jti = self.jwt_service.create_refresh_token({"sub": user_id})

        await self.repo.save_refresh_token(token_jti, user_id, ttl=self.jwt_service.refresh_expire_seconds)
        return TokenPair(access_token=access_token, refresh_token=refresh_token)
