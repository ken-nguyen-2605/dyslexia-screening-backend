from sqlalchemy import Column, Integer, TIMESTAMP, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class SessionContext(Base):
    __tablename__ = 'session_context'

    id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(Integer, ForeignKey('participants.id'))
    last_test_session_id = Column(Integer, ForeignKey('test_sessions.id'))
    test_progress = Column(Text())  # JSON or text representation of test progress
    last_activity = Column(TIMESTAMP)

    participant = relationship("Participant", back_populates="session_contexts")
    test_session = relationship("TestSession", back_populates="session_context")