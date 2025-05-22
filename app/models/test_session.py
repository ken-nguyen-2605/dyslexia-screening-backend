from sqlalchemy import Column, Integer, Boolean, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base

class TestSession(Base):
    __tablename__ = 'test_session'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    start_time = Column(TIMESTAMP, default=func.now())
    end_time = Column(TIMESTAMP)
    completion_status = Column(String)
    predict_dyslexia = Column(Boolean)

    # Relationships
    account = relationship("Account", back_populates="test_sessions")
    human_features = relationship("HumanFeatures", uselist=False, back_populates="test_session")
    visual_features = relationship("VisualFeatures", uselist=False, back_populates="test_session")
    auditory_features = relationship("AuditoryFeatures", uselist=False, back_populates="test_session")
    language_features = relationship("LanguageFeatures", uselist=False, back_populates="test_session")
    user_contexts = relationship("UserContext", back_populates="test_session")