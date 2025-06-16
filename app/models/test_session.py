from sqlalchemy import Column, Integer, Boolean, String, TIMESTAMP, ForeignKey, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from typing import Optional, Dict, Any
from .base import Base
from .enums import TestStatus


class TestSession(Base):
    __tablename__ = 'test_sessions'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey('participants.id'))
    start_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    end_time: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    completion_status: Mapped[TestStatus] = mapped_column(Enum(TestStatus), nullable=False)  # e.g., 'completed', 'in_progress'
    predict_dyslexia: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    progress: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    
    # Relationships
    participant: Mapped["Participant"] = relationship("Participant", back_populates="test_sessions")  # type: ignore
    human_feature: Mapped["HumanFeatures"] = relationship("HumanFeatures", uselist=False, back_populates="test_session")  # type: ignore
    visual_feature: Mapped["VisualFeatures"] = relationship("VisualFeatures", uselist=False, back_populates="test_session")  # type: ignore
    auditory_feature: Mapped["AuditoryFeatures"] = relationship("AuditoryFeatures", uselist=False, back_populates="test_session")  # type: ignore
    language_feature: Mapped["LanguageFeatures"] = relationship("LanguageFeatures", uselist=False, back_populates="test_session")  # type: ignore
    
    def __repr__(self):
        return f"<TestSession(id={self.id}, participant_id={self.participant_id}, start_time={self.start_time}, completion_status={self.completion_status})>"