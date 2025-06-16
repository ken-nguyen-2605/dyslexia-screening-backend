from datetime import datetime, timedelta
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import Base

class VisualFeatures(Base):
    __tablename__ = 'visual_features'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_session_id: Mapped[int] = mapped_column(ForeignKey('test_sessions.id'))

    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)
    total_clicks: Mapped[int | None] = mapped_column()

    first_click_interval: Mapped[timedelta | None] = mapped_column()
    second_click_interval: Mapped[timedelta | None] = mapped_column()
    third_click_interval: Mapped[timedelta | None] = mapped_column()
    fourth_click_interval: Mapped[timedelta | None] = mapped_column()
    fifth_click_interval: Mapped[timedelta | None] = mapped_column()
    sixth_click_interval: Mapped[timedelta | None] = mapped_column()
    time_last_click: Mapped[timedelta | None] = mapped_column()

    correct_answers: Mapped[int | None] = mapped_column()
    wrong_answers: Mapped[int | None] = mapped_column()

    test_session: Mapped["TestSession"] = relationship(back_populates="visual_features")  # type: ignore