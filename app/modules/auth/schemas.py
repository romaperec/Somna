from pydantic import BaseModel


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

class UserLogin(BaseModel):
    username_or_email: str
    password: str
