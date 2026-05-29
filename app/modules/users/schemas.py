from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, StringConstraints


class UserBase(BaseModel):
    username: Annotated[str, Field(max_length=32)]
    description: Annotated[str, Field(max_length=500)]
    email: Annotated[EmailStr, StringConstraints(max_length=254)]


class UserCreate(UserBase):
    password: str = Field(max_length=64)


class UserUpdate(BaseModel):
    username: Annotated[str, Field(max_length=32)] | None = None
    description: Annotated[str, Field(max_length=500)] | None = None
    email: Annotated[EmailStr, StringConstraints(max_length=254)] | None = None


class UserChangePassword(BaseModel):
    current_password: Annotated[str, Field(max_length=64)]
    new_password: Annotated[str, Field(max_length=64)]
