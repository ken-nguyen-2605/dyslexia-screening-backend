from datetime import datetime, timedelta
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, TIMESTAMP, Enum
from .base import Base
from .enums import AuditoryQuestionType

class AuditoryFeatures(Base):
    __tablename__ = 'auditory_features'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_session_id: Mapped[int] = mapped_column(ForeignKey('test_sessions.id'))
    question_type: Mapped[AuditoryQuestionType] = mapped_column(Enum(AuditoryQuestionType), nullable=False)
    start_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    
    first_click_interval: Mapped[timedelta] = mapped_column(nullable=False)
    second_click_interval: Mapped[timedelta] = mapped_column(nullable=False)
    third_click_interval: Mapped[timedelta] = mapped_column(nullable=False)
    fourth_click_interval: Mapped[timedelta] = mapped_column(nullable=False)
    fifth_click_interval: Mapped[timedelta] = mapped_column(nullable=False)
    sixth_click_interval: Mapped[timedelta] = mapped_column(nullable=False)

    duration_from_round: Mapped[timedelta] = mapped_column(nullable=False)
    duration_from_interaction: Mapped[timedelta] = mapped_column(nullable=False)

    total_clicks: Mapped[int] = mapped_column(nullable=False)
    logic: Mapped[bool] = mapped_column(nullable=False)
    instructions_viewed: Mapped[int] = mapped_column(nullable=False)

    test_session: Mapped["TestSession"] = relationship(back_populates="auditory_features") # type: ignore