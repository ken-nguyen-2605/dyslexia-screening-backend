from sqlalchemy import Column, Integer, TIMESTAMP, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class UserContext(Base):
    __tablename__ = 'user_context'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    last_test_session_id = Column(Integer, ForeignKey('test_session.id'))
    test_progress = Column(Text(nullable=True))  # JSON or text representation of test progress
    last_activity = Column(TIMESTAMP)

    account = relationship("Account", back_populates="user_contexts")
    test_session = relationship("TestSession", back_populates="user_contexts")