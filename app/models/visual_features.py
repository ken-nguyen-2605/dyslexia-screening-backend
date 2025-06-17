from datetime import datetime, timedelta
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum
from .base import Base
from .enums import VisualQuestionType

class VisualFeatures(Base):
    __tablename__ = 'visual_features'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_session_id: Mapped[int] = mapped_column(ForeignKey('test_sessions.id'))
    question_type: Mapped[VisualQuestionType] = mapped_column(Enum(VisualQuestionType), nullable=False)

    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)
    total_clicks: Mapped[int] = mapped_column(nullable=False)

    first_click_interval: Mapped[timedelta] = mapped_column(nullable=False)
    second_click_interval: Mapped[timedelta] = mapped_column(nullable=False)
    third_click_interval: Mapped[timedelta] = mapped_column(nullable=False)
    fourth_click_interval: Mapped[timedelta] = mapped_column(nullable=False)
    fifth_click_interval: Mapped[timedelta] = mapped_column(nullable=False)
    sixth_click_interval: Mapped[timedelta] = mapped_column(nullable=False)
    time_last_click: Mapped[timedelta] = mapped_column(nullable=False)

    correct_answers: Mapped[int] = mapped_column(nullable=False)
    wrong_answers: Mapped[int] = mapped_column(nullable=False)

    test_session: Mapped["TestSession"] = relationship(back_populates="visual_features")  # type: ignore