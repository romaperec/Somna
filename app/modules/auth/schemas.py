import re

from pydantic import BaseModel, EmailStr, field_validator, Field


class RecoveryPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    password: str = Field(min_length=6, max_length=64)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(set(value)) < 4:
            raise ValueError("Password is too simple (must contain at least 4 unique characters)")

        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")

        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")

        if not any(char.islower() for char in value):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")

        return value

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

class UserLogin(BaseModel):
    email: EmailStr
    password: str
