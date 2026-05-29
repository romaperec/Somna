import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import Base


class User(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    username: Mapped[str] = mapped_column(String(32), unique=True)
    description: Mapped[str] = mapped_column(String(500))
    email: Mapped[str] = mapped_column(String(254), unique=True)
    hashed_password: Mapped[str]
