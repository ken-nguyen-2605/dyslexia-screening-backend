from sqlalchemy import Boolean, TIMESTAMP, ForeignKey, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from .enums import AuditoryProgress, VisualProgress, LanguageProgress
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
    auditory_progress: Mapped[AuditoryProgress] = mapped_column(Enum(AuditoryProgress), nullable=True)
    visual_progress: Mapped[VisualProgress] = mapped_column(Enum(VisualProgress), nullable=True)
    language_progress: Mapped[LanguageProgress] = mapped_column(Enum(LanguageProgress), nullable=True)
    
    # Relationships
    participant: Mapped["Participant"] = relationship("Participant", back_populates="test_sessions")  # type: ignore
    human_feature: Mapped["HumanFeatures"] = relationship("HumanFeatures", back_populates="test_session")  # type: ignore
    visual_features: Mapped[list["VisualFeatures"]] = relationship("VisualFeatures", back_populates="test_session")  # type: ignore
    auditory_features: Mapped[list["AuditoryFeatures"]] = relationship("AuditoryFeatures", back_populates="test_session")  # type: ignore
    language_features: Mapped[list["LanguageFeatures"]] = relationship("LanguageFeatures", back_populates="test_session")  # type: ignore
    
    def __repr__(self):
        return f"<TestSession(id={self.id}, participant_id={self.participant_id}, start_time={self.start_time}, completion_status={self.completion_status})>"