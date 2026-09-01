import re
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints, field_validator


class UserBase(BaseModel):
    username: Annotated[str, Field(max_length=32)]
    description: Annotated[str | None, Field(max_length=500)] = None
    email: Annotated[EmailStr, StringConstraints(max_length=254)]


class UserCreate(UserBase):
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


class UserUpdate(BaseModel):
    username: Annotated[str, Field(max_length=32)] | None = None
    description: Annotated[str, Field(max_length=500)] | None = None
    email: Annotated[EmailStr, StringConstraints(max_length=254)] | None = None


class UserChangePassword(BaseModel):
    current_password: Annotated[str, Field(min_length=6, max_length=64)]
    new_password: Annotated[str, Field(min_length=6, max_length=64)]

class UserResponse(UserBase):
    id: UUID

class UserPrivateResponse(UserResponse):
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)
