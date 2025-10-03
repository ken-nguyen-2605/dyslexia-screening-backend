from datetime import datetime

from sqlalchemy import TIMESTAMP, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import AccountRole


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    role: Mapped[AccountRole] = mapped_column(
        Enum(AccountRole), default=AccountRole.USER, nullable=False
    )

    # Relationships
    profiles: Mapped[list["Profile"]] = relationship(back_populates="account", cascade="all, delete-orphan")  # type: ignore
