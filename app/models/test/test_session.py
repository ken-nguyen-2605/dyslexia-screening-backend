from datetime import datetime

from sqlalchemy import TIMESTAMP, Enum, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from ..enums import TestResult


class TestSession(Base):
    __tablename__ = "test_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    end_time: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    completed: Mapped[bool] = mapped_column(default=False)
    taken_auditory_test: Mapped[bool] = mapped_column(default=False)
    taken_visual_test: Mapped[bool] = mapped_column(default=False)
    taken_language_test: Mapped[bool] = mapped_column(default=False)
    result: Mapped[TestResult | None] = mapped_column(Enum(TestResult), nullable=True)
    total_score: Mapped[float | None] = mapped_column(nullable=True)  # Over 100

    profile: Mapped["Profile"] = relationship(back_populates="test_sessions")  # type: ignore
    auditory_test: Mapped["AuditoryTest"] = relationship(  # type: ignore
        back_populates="test_session", uselist=False, cascade="all, delete-orphan"
    )
    visual_test: Mapped["VisualTest"] = relationship(  # type: ignore
        back_populates="test_session", uselist=False, cascade="all, delete-orphan"
    )
    language_test: Mapped["LanguageTest"] = relationship(  # type: ignore
        back_populates="test_session", uselist=False, cascade="all, delete-orphan"
    )
