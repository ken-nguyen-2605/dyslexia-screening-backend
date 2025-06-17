from datetime import datetime, timedelta
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, TIMESTAMP
from .base import Base

class AuditoryFeatures(Base):
    __tablename__ = 'auditory_features'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_session_id: Mapped[int] = mapped_column(ForeignKey('test_sessions.id'))
    start_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    
    first_click_interval: Mapped[timedelta | None] = mapped_column()
    second_click_interval: Mapped[timedelta | None] = mapped_column()
    third_click_interval: Mapped[timedelta | None] = mapped_column()
    fourth_click_interval: Mapped[timedelta | None] = mapped_column()
    fifth_click_interval: Mapped[timedelta | None] = mapped_column()
    sixth_click_interval: Mapped[timedelta | None] = mapped_column()

    duration_from_round: Mapped[timedelta | None] = mapped_column()
    duration_from_interaction: Mapped[timedelta | None] = mapped_column()

    total_clicks: Mapped[int | None] = mapped_column()
    logic: Mapped[bool | None] = mapped_column()
    instructions_viewed: Mapped[int | None] = mapped_column()

    test_session: Mapped["TestSession"] = relationship(back_populates="auditory_features") # type: ignore