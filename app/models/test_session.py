from sqlalchemy import Column, Integer, Boolean, String, TIMESTAMP, ForeignKey, func, Enum
from .enums import TestStatus
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base

class TestSession(Base):
    __tablename__ = 'test_sessions'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey('participants.id'))
    start_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    end_time: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    completion_status: Mapped[TestStatus] = mapped_column(Enum(TestStatus), nullable=False)  # e.g., 'completed', 'in_progress'
    predict_dyslexia: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    
    # Relationships
    participant: Mapped["Participant"] = relationship("Participant", back_populates="test_sessions")  # type: ignore
    session_context: Mapped["SessionContext"] = relationship("SessionContext", back_populates="test_session", uselist=False)  # type: ignore

    human_feature: Mapped["HumanFeatures"] = relationship("HumanFeatures", uselist=False, back_populates="test_session")  # type: ignore
    visual_feature: Mapped["VisualFeatures"] = relationship("VisualFeatures", uselist=False, back_populates="test_session")  # type: ignore
    auditory_feature: Mapped["AuditoryFeatures"] = relationship("AuditoryFeatures", uselist=False, back_populates="test_session")  # type: ignore
    language_feature: Mapped["LanguageFeatures"] = relationship("LanguageFeatures", uselist=False, back_populates="test_session")  # type: ignore