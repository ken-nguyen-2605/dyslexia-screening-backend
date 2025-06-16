from datetime import datetime
from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class LanguageFeatures(Base):
    __tablename__ = 'language_features'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_session_id: Mapped[int] = mapped_column(ForeignKey('test_sessions.id'))
    
    start_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    
    clicks: Mapped[int | None] = mapped_column()
    hits: Mapped[int | None] = mapped_column()
    misses: Mapped[int | None] = mapped_column()
    
    test_session: Mapped["TestSession"] = relationship(back_populates="language_feature")  # type: ignore