import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import Base

if TYPE_CHECKING:
    from app.modules.auth.models import RecoveryToken

class User(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(450), nullable=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=True)

    recovery_tokens: Mapped[list["RecoveryToken"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
