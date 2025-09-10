from sqlalchemy import String, TIMESTAMP, func, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base
from .enums import ProfileType

class Profile(Base):
    __tablename__ = 'profiles'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    profile_type: Mapped[ProfileType] = mapped_column(Enum(ProfileType), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    account: Mapped["Account"] = relationship(back_populates="profiles")  # type: ignore