from datetime import datetime
from sqlalchemy import ForeignKey, TIMESTAMP, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .enums import LanguageQuestionType

class LanguageFeatures(Base):
    __tablename__ = 'language_features'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_session_id: Mapped[int] = mapped_column(ForeignKey('test_sessions.id'))
    type: Mapped[LanguageQuestionType] = mapped_column(Enum(LanguageQuestionType), nullable=False)
    
    start_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    
    clicks: Mapped[int] = mapped_column(nullable=False)
    hits: Mapped[int] = mapped_column(nullable=False)
    misses: Mapped[int] = mapped_column(nullable=False)
    
    test_session: Mapped["TestSession"] = relationship(back_populates="language_features")  # type: ignore