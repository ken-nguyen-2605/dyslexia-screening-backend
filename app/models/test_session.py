from sqlalchemy import Boolean, TIMESTAMP, ForeignKey, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from .base import Base
from .enums import TestStatus, TestDifficulty


class TestSession(Base):
    __tablename__ = 'test_sessions'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey('profiles.id'), nullable=False)
    start_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    end_time: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    test_difficulty: Mapped[TestDifficulty] = mapped_column(Enum(TestDifficulty), nullable=False)
    completion_status: Mapped[TestStatus] = mapped_column(Enum(TestStatus), nullable=False)  # e.g., 'completed', 'in_progress'
    predict_dyslexia: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    
    profile: Mapped["Profile"] = relationship(back_populates="test_sessions")  # type: ignore