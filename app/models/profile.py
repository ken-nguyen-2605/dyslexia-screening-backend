from datetime import datetime

from sqlalchemy import TIMESTAMP, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from .enums import Gender, OfficialDyslexiaDiagnosis, ProfileType


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    profile_type: Mapped[ProfileType] = mapped_column(Enum(ProfileType), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    # Info about user when they enter the test
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    year_of_birth: Mapped[int | None] = mapped_column(nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    mother_tongue: Mapped[str | None] = mapped_column(String(100), nullable=True)
    gender: Mapped[Gender | None] = mapped_column(Enum(Gender), nullable=True)
    official_dyslexia_diagnosis: Mapped[OfficialDyslexiaDiagnosis | None] = (
        mapped_column(Enum(OfficialDyslexiaDiagnosis), nullable=True)
    )

    # Relationships
    account: Mapped["Account"] = relationship(back_populates="profiles")  # type: ignore
    test_sessions: Mapped[list["TestSession"]] = relationship(back_populates="profile")  # type: ignore
