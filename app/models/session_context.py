from datetime import datetime
from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class SessionContext(Base):
    __tablename__ = 'session_context'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey('participants.id'))
    last_test_session_id: Mapped[int] = mapped_column(ForeignKey('test_sessions.id'))
    test_progress: Mapped[str] = mapped_column()  # JSON or text representation of test progress
    last_activity: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    
    participant: Mapped["Participant"] = relationship("Participant", back_populates="session_contexts")  # type: ignore
    test_session: Mapped["TestSession"] = relationship("TestSession", back_populates="session_context")  # type: ignore