import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base import Base

if TYPE_CHECKING:
    from app.modules.users.models import User


class RecoveryToken(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    is_used: Mapped[bool] = mapped_column(default=False, server_default="false")

    user: Mapped["User"] = relationship(back_populates="recovery_tokens")
