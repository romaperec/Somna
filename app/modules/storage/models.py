from typing import TYPE_CHECKING
import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import Base

if TYPE_CHECKING:
    from app.modules.users.models import User


class Audio(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(150))
    category: Mapped[str] = mapped_column(String(100))

    original_filename: Mapped[str] = mapped_column(String(100))
    unique_filename: Mapped[str]
    path: Mapped[str]

    user: Mapped["User"] = relationship(back_populates="audios")
